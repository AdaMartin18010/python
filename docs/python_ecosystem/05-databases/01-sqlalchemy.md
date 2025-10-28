# SQLAlchemy ORM

**Python最强大的SQL工具包和ORM**

---

## 📋 概述

SQLAlchemy是Python中最流行的SQL工具包和对象关系映射器(ORM)。提供完整的企业级持久化模式。

### 核心特性

- 🗄️ **强大ORM** - 完整的对象关系映射
- ⚡ **高性能** - 连接池、惰性加载
- 🔄 **异步支持** - AsyncIO原生支持
- 🎯 **灵活** - Core + ORM双API
- 🔐 **安全** - SQL注入防护

---

## 🚀 快速开始

### 安装

```bash
uv add sqlalchemy
# 异步支持
uv add sqlalchemy[asyncio] asyncpg
```

### Hello SQLAlchemy

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# 创建引擎
engine = create_engine("sqlite:///example.db")
Base = declarative_base()

# 定义模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# 创建表
Base.metadata.create_all(engine)

# 使用
with Session(engine) as session:
    user = User(name="Alice", email="alice@example.com")
    session.add(user)
    session.commit()
```

---

## 💻 核心功能

### 1. 模型定义

```python
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    
    # 关系
    author = relationship("User", back_populates="posts")
```

### 2. CRUD操作

```python
from sqlalchemy.orm import Session

# 创建
with Session(engine) as session:
    user = User(username="alice", email="alice@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)  # 获取生成的ID

# 查询
with Session(engine) as session:
    # 获取所有
    users = session.query(User).all()
    
    # 获取单个
    user = session.query(User).filter_by(username="alice").first()
    user = session.get(User, 1)  # 按主键
    
    # 条件查询
    users = session.query(User).filter(User.is_active == True).all()

# 更新
with Session(engine) as session:
    user = session.get(User, 1)
    user.email = "newemail@example.com"
    session.commit()

# 删除
with Session(engine) as session:
    user = session.get(User, 1)
    session.delete(user)
    session.commit()
```

---

## 🔍 查询API

### 基本查询

```python
from sqlalchemy import select

# SQLAlchemy 2.0风格
with Session(engine) as session:
    # 查询所有
    stmt = select(User)
    users = session.scalars(stmt).all()
    
    # 条件查询
    stmt = select(User).where(User.username == "alice")
    user = session.scalar(stmt)
    
    # 多条件
    stmt = select(User).where(
        User.is_active == True,
        User.email.like("%@example.com")
    )
    users = session.scalars(stmt).all()
```

### 高级查询

```python
from sqlalchemy import and_, or_, not_

# AND/OR/NOT
stmt = select(User).where(
    and_(
        User.is_active == True,
        or_(
            User.email.endswith("@gmail.com"),
            User.email.endswith("@yahoo.com")
        )
    )
)

# 排序
stmt = select(User).order_by(User.created_at.desc())

# 限制
stmt = select(User).limit(10).offset(20)

# Join
stmt = select(User, Post).join(Post, User.id == Post.author_id)
```

---

## ⚡ 异步SQLAlchemy

### 异步引擎

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 创建异步引擎
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True
)

# 会话工厂
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 使用
async with async_session() as session:
    stmt = select(User).where(User.username == "alice")
    result = await session.execute(stmt)
    user = result.scalar_one()
```

### 异步CRUD

```python
async def create_user(username: str, email: str):
    async with async_session() as session:
        user = User(username=username, email=email)
        session.add(user)
        await session.commit()
        return user

async def get_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

async def update_user(user_id: int, email: str):
    async with async_session() as session:
        user = await session.get(User, user_id)
        user.email = email
        await session.commit()
        return user

async def delete_user(user_id: int):
    async with async_session() as session:
        user = await session.get(User, user_id)
        await session.delete(user)
        await session.commit()
```

---

## 🔗 关系

### 一对多

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

# 使用
user = session.get(User, 1)
for post in user.posts:
    print(post.title)
```

### 多对多

```python
from sqlalchemy import Table

# 关联表
user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("groups.id"))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    groups = relationship("Group", secondary=user_group, back_populates="users")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    users = relationship("User", secondary=user_group, back_populates="groups")
```

---

## 🔒 事务

```python
from sqlalchemy import exc

# 自动提交
with Session(engine) as session:
    user = User(username="alice")
    session.add(user)
    session.commit()

# 回滚
with Session(engine) as session:
    try:
        user = User(username="bob")
        session.add(user)
        # ... 其他操作
        session.commit()
    except exc.SQLAlchemyError:
        session.rollback()
        raise

# 嵌套事务
with Session(engine) as session:
    with session.begin():
        user1 = User(username="user1")
        session.add(user1)
        
        with session.begin_nested():
            user2 = User(username="user2")
            session.add(user2)
            session.rollback()  # 只回滚user2
```

---

## 📚 最佳实践

### 1. 使用上下文管理器

```python
# ✅ 好
with Session(engine) as session:
    user = session.get(User, 1)

# ❌ 差
session = Session(engine)
user = session.get(User, 1)
session.close()  # 容易忘记
```

### 2. 预加载关系

```python
from sqlalchemy.orm import selectinload, joinedload

# Lazy loading (N+1问题)
users = session.query(User).all()
for user in users:
    print(user.posts)  # 每次查询

# Eager loading (一次查询)
users = session.query(User).options(
    selectinload(User.posts)
).all()
```

### 3. 批量操作

```python
# 批量插入
session.bulk_insert_mappings(User, [
    {"username": "user1", "email": "user1@example.com"},
    {"username": "user2", "email": "user2@example.com"},
])

# 批量更新
session.bulk_update_mappings(User, [
    {"id": 1, "email": "new1@example.com"},
    {"id": 2, "email": "new2@example.com"},
])
```

---

## 🔗 相关资源

- [官方文档](https://docs.sqlalchemy.org/)
- [异步教程](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

**最后更新**: 2025年10月28日

