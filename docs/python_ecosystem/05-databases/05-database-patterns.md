# 数据库设计模式

**Python数据库最佳实践**

---

## 📋 核心模式

### 1. Repository模式

```python
from typing import Protocol, Optional
from dataclasses import dataclass

@dataclass
class User:
    id: Optional[int]
    name: str
    email: str

class UserRepository(Protocol):
    def find_by_id(self, user_id: int) -> Optional[User]: ...
    def find_by_email(self, email: str) -> Optional[User]: ...
    def save(self, user: User) -> User: ...
    def delete(self, user_id: int) -> None: ...

# SQLAlchemy实现
class SQLAlchemyUserRepository:
    def __init__(self, session):
        self.session = session
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(UserModel).filter_by(id=user_id).first()
    
    def save(self, user: User) -> User:
        user_model = UserModel(**user.__dict__)
        self.session.add(user_model)
        self.session.commit()
        return user
```

---

## 🔄 Unit of Work模式

```python
class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    def __enter__(self):
        self.session = self.session_factory()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.session.close()
    
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()

# 使用
with UnitOfWork(session_factory) as uow:
    user = uow.users.find_by_id(1)
    user.name = 'New Name'
    uow.users.save(user)
    # 自动commit或rollback
```

---

## 🎯 查询对象模式

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserQuery:
    name: Optional[str] = None
    email: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    is_active: Optional[bool] = None

class UserRepository:
    def find(self, query: UserQuery) -> list[User]:
        q = self.session.query(User)
        
        if query.name:
            q = q.filter(User.name.like(f'%{query.name}%'))
        if query.email:
            q = q.filter(User.email == query.email)
        if query.min_age:
            q = q.filter(User.age >= query.min_age)
        if query.max_age:
            q = q.filter(User.age <= query.max_age)
        if query.is_active is not None:
            q = q.filter(User.is_active == query.is_active)
        
        return q.all()

# 使用
query = UserQuery(name='Alice', is_active=True)
users = repo.find(query)
```

---

## 💾 缓存模式

### 1. Read-Through Cache

```python
from functools import lru_cache
import redis

class CachedUserRepository:
    def __init__(self, db_repo, cache: redis.Redis):
        self.db_repo = db_repo
        self.cache = cache
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        # 先查缓存
        cache_key = f'user:{user_id}'
        cached = self.cache.get(cache_key)
        
        if cached:
            return User.from_json(cached)
        
        # 缓存未命中，查数据库
        user = self.db_repo.find_by_id(user_id)
        if user:
            self.cache.setex(cache_key, 3600, user.to_json())
        
        return user
```

### 2. Write-Through Cache

```python
class CachedUserRepository:
    def save(self, user: User) -> User:
        # 先写数据库
        saved_user = self.db_repo.save(user)
        
        # 更新缓存
        cache_key = f'user:{saved_user.id}'
        self.cache.setex(cache_key, 3600, saved_user.to_json())
        
        return saved_user
```

---

## 🔐 连接池模式

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# 配置连接池
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=10,          # 连接池大小
    max_overflow=20,       # 最大溢出
    pool_timeout=30,       # 超时时间
    pool_recycle=3600,     # 连接回收时间
    pool_pre_ping=True     # 连接前ping
)

SessionLocal = sessionmaker(bind=engine)

# 使用上下文管理器
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# 使用
with get_db() as db:
    user = db.query(User).first()
```

---

## 📊 读写分离

```python
from enum import Enum

class DatabaseType(Enum):
    MASTER = 'master'
    REPLICA = 'replica'

class DatabaseRouter:
    def __init__(self):
        self.master = create_engine('postgresql://master/db')
        self.replica = create_engine('postgresql://replica/db')
    
    def get_engine(self, db_type: DatabaseType):
        if db_type == DatabaseType.MASTER:
            return self.master
        return self.replica

class UserRepository:
    def __init__(self, router: DatabaseRouter):
        self.router = router
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        # 读操作使用从库
        engine = self.router.get_engine(DatabaseType.REPLICA)
        with engine.connect() as conn:
            result = conn.execute(
                "SELECT * FROM users WHERE id = %s", (user_id,)
            )
            return result.fetchone()
    
    def save(self, user: User) -> User:
        # 写操作使用主库
        engine = self.router.get_engine(DatabaseType.MASTER)
        with engine.connect() as conn:
            conn.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (user.name, user.email)
            )
            conn.commit()
        return user
```

---

## 🔄 分页模式

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass
class Page(Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size
    
    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages
    
    @property
    def has_prev(self) -> bool:
        return self.page > 1

class UserRepository:
    def find_all(self, page: int = 1, page_size: int = 20) -> Page[User]:
        offset = (page - 1) * page_size
        
        # 查询总数
        total = self.session.query(User).count()
        
        # 查询当前页
        items = (self.session.query(User)
                 .offset(offset)
                 .limit(page_size)
                 .all())
        
        return Page(items=items, total=total, page=page, page_size=page_size)
```

---

## 🎭 软删除模式

```python
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean

class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

class User(Base, SoftDeleteMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class UserRepository:
    def find_by_id(self, user_id: int) -> Optional[User]:
        return (self.session.query(User)
                .filter_by(id=user_id, is_deleted=False)
                .first())
    
    def delete(self, user_id: int) -> None:
        user = self.find_by_id(user_id)
        if user:
            user.soft_delete()
            self.session.commit()
```

---

## 🔒 乐观锁模式

```python
from sqlalchemy import Column, Integer

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    version = Column(Integer, default=0)  # 版本号

class UserRepository:
    def update(self, user: User) -> bool:
        result = (self.session.query(User)
                  .filter_by(id=user.id, version=user.version)
                  .update({
                      'name': user.name,
                      'version': user.version + 1
                  }))
        
        if result == 0:
            # 版本冲突
            raise OptimisticLockError('数据已被其他用户修改')
        
        self.session.commit()
        user.version += 1
        return True
```

---

## 📚 最佳实践

### 1. 使用事务

```python
from sqlalchemy.orm import Session

def transfer_money(from_account: int, to_account: int, amount: float, db: Session):
    with db.begin():
        # 所有操作在一个事务中
        from_acc = db.query(Account).filter_by(id=from_account).with_for_update().first()
        to_acc = db.query(Account).filter_by(id=to_account).with_for_update().first()
        
        from_acc.balance -= amount
        to_acc.balance += amount
        # 自动commit或rollback
```

### 2. N+1查询优化

```python
# ❌ 差 - N+1问题
users = session.query(User).all()
for user in users:
    print(user.posts)  # 每次都查询一次

# ✅ 好 - 使用joinedload
from sqlalchemy.orm import joinedload

users = session.query(User).options(joinedload(User.posts)).all()
for user in users:
    print(user.posts)  # 不再查询
```

---

## 🔗 相关资源

- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [数据库设计模式](https://martinfowler.com/eaaCatalog/)

---

**最后更新**: 2025年10月28日

