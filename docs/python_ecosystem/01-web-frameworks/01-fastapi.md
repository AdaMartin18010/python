# FastAPI 完全指南

**现代、快速（高性能）的Web框架**

---

## 📋 概述

FastAPI是一个现代、快速（高性能）的Web框架，用于构建API。基于标准Python类型提示，提供自动API文档生成、数据验证等强大功能。

### 核心特性

- ⚡ **高性能** - 与NodeJS和Go相当的性能
- 🔒 **类型安全** - 基于Python类型提示
- 📝 **自动文档** - 自动生成交互式API文档
- ✅ **数据验证** - 基于Pydantic自动验证
- 🔄 **异步支持** - 原生支持async/await

---

## 🚀 快速开始

### 安装

```bash
# 使用 uv (推荐)
uv add fastapi uvicorn

# 或使用 pip
pip install fastapi uvicorn[standard]
```

### Hello World

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### 运行

```bash
uvicorn main:app --reload
```

访问:

- API: <http://localhost:8000>
- 交互式文档: <http://localhost:8000/docs>
- 备用文档: <http://localhost:8000/redoc>

---

## 💻 核心功能

### 1. Pydantic模型

```python
from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    full_name: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

@app.post("/users/", response_model=User)
def create_user(user: User):
    # 自动验证和序列化
    return user
```

### 2. 依赖注入

```python
from fastapi import Depends, HTTPException
from typing import Annotated

def get_current_user(token: str) -> User:
    # 验证token并返回用户
    if not token:
        raise HTTPException(status_code=401)
    return User(id=1, username="john", email="john@example.com")

@app.get("/me")
def read_current_user(user: Annotated[User, Depends(get_current_user)]):
    return user
```

### 3. 异步端点

```python
import asyncio
from databases import Database

database = Database("postgresql://user:pass@localhost/db")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    results = await database.fetch_all(query)
    return results
```

### 4. 路径参数和查询参数

```python
from typing import Literal

@app.get("/items/{item_id}")
def read_item(
    item_id: int,
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
    sort: Literal["asc", "desc"] = "asc"
):
    return {
        "item_id": item_id,
        "q": q,
        "skip": skip,
        "limit": limit,
        "sort": sort
    }
```

### 5. 请求体验证

```python
from pydantic import BaseModel, validator

class Item(BaseModel):
    name: str
    price: float
    tax: float | None = None

    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("price must be positive")
        return v

@app.post("/items/")
def create_item(item: Item):
    return item
```

---

## 🏗️ 项目结构

### 标准结构

```
my-api/
├── pyproject.toml
├── src/
│   └── my_api/
│       ├── __init__.py
│       ├── main.py          # FastAPI应用
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes/      # 路由
│       │   │   ├── users.py
│       │   │   └── items.py
│       │   └── deps.py      # 依赖
│       ├── models/          # Pydantic模型
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── item.py
│       ├── services/        # 业务逻辑
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── db/              # 数据库
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── models.py
│       └── core/            # 配置
│           ├── __init__.py
│           ├── config.py
│           └── security.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_api/
        └── test_users.py
```

---

## 🔒 安全认证

### JWT认证

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected")
def protected_route(payload: dict = Depends(verify_token)):
    return {"message": "This is protected", "user": payload}
```

---

## 📊 数据库集成

### SQLAlchemy + asyncpg

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# 使用
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## 🧪 测试

### pytest + httpx

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

@pytest.mark.asyncio
async def test_create_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

---

## ⚡ 性能优化

### 1. 使用异步

```python
# ✅ 好 - 异步
@app.get("/users")
async def get_users():
    users = await db.fetch_all("SELECT * FROM users")
    return users

# ❌ 差 - 同步阻塞
@app.get("/users")
def get_users():
    users = db.fetch_all("SELECT * FROM users")  # 阻塞
    return users
```

### 2. 连接池

```python
from databases import Database

# 使用连接池
database = Database(
    "postgresql://user:pass@localhost/db",
    min_size=10,
    max_size=20
)
```

### 3. 响应缓存

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/users")
@cache(expire=60)  # 缓存60秒
async def get_users():
    return await db.fetch_all("SELECT * FROM users")
```

---

## 📚 最佳实践

### 1. 配置管理

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My API"
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. 异常处理

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str, detail: str):
        self.name = name
        self.detail = detail

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=400,
        content={"error": exc.name, "detail": exc.detail}
    )
```

### 3. 响应模型

```python
from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    # 不包含password等敏感信息

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    user = await get_user_from_db(user_id)
    return user  # 自动过滤敏感字段
```

---

## 🔗 相关资源

- [官方文档](https://fastapi.tiangolo.com/)
- [GitHub仓库](https://github.com/tiangolo/fastapi)
- [教程合集](https://fastapi.tiangolo.com/tutorial/)

---

**最后更新**: 2025年10月28日
