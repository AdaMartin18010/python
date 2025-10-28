# Pydantic 数据验证

**基于Python类型提示的数据验证库**

---

## 📋 概述

Pydantic是一个使用Python类型提示进行数据验证和设置管理的库。FastAPI的核心依赖,提供运行时类型检查和数据验证。

### 核心特性

- ✅ **数据验证** - 自动验证输入数据
- 🔒 **类型安全** - 基于类型提示
- ⚡ **高性能** - 使用Rust加速
- 📝 **自动文档** - 生成JSON Schema
- 🎯 **易用** - 简洁的API

---

## 🚀 快速开始

### 安装

```bash
uv add pydantic
```

### Hello Pydantic

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# 验证通过
user = User(id=1, name="Alice", email="alice@example.com")
print(user)
# User(id=1, name='Alice', email='alice@example.com')

# 自动类型转换
user = User(id="123", name="Bob", email="bob@example.com")
print(user.id)  # 123 (int)

# 验证失败
try:
    user = User(id="invalid", name="Charlie")
except Exception as e:
    print(e)
# validation error for User
```

---

## 💻 核心功能

### 1. 基本模型

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime = datetime.now()
    is_active: bool = True

# 使用
user = User(
    id=1,
    username="alice",
    email="alice@example.com"
)

# 访问字段
print(user.username)

# 转换为字典
print(user.model_dump())

# 转换为JSON
print(user.model_dump_json())
```

### 2. 字段验证

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0, le=1000000)
    quantity: int = Field(default=0, ge=0)
    description: Optional[str] = Field(None, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "quantity": 10,
                "description": "High-performance laptop"
            }
        }

# 验证
product = Product(name="Phone", price=699.99, quantity=5)
```

### 3. 自定义验证器

```python
from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    username: str
    email: str
    password: str
    password_confirm: str
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
    
    @field_validator('email')
    @classmethod
    def email_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
    
    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self
```

---

## 🎯 高级特性

### 1. 嵌套模型

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class User(BaseModel):
    name: str
    email: str
    addresses: List[Address]

# 使用
user = User(
    name="Alice",
    email="alice@example.com",
    addresses=[
        {"street": "123 Main St", "city": "NYC", "country": "USA", "zip_code": "10001"},
        {"street": "456 Oak Ave", "city": "LA", "country": "USA", "zip_code": "90001"}
    ]
)
```

### 2. 泛型模型

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
    message: str
    status: int

class User(BaseModel):
    id: int
    name: str

# 使用
response = Response[User](
    data=User(id=1, name="Alice"),
    message="Success",
    status=200
)

response_list = Response[List[User]](
    data=[User(id=1, name="Alice"), User(id=2, name="Bob")],
    message="Success",
    status=200
)
```

### 3. 配置

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 去除字符串首尾空格
        str_min_length=1,           # 字符串最小长度
        validate_assignment=True,   # 赋值时验证
        frozen=False,               # 是否不可变
        extra='forbid',             # 禁止额外字段
    )
    
    name: str
    email: str

# 赋值验证
user = User(name="Alice", email="alice@example.com")
user.name = "Bob"  # 会触发验证
```

---

## 🔒 高级验证

### EmailStr, HttpUrl等

```python
from pydantic import BaseModel, EmailStr, HttpUrl, conint, constr

class User(BaseModel):
    email: EmailStr              # 验证邮箱格式
    website: HttpUrl             # 验证URL格式
    age: conint(ge=0, le=120)   # 限制整数范围
    username: constr(
        min_length=3,
        max_length=20,
        pattern=r'^[a-zA-Z0-9_]+$'
    )
```

### JSON Schema

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price", gt=0)

# 生成JSON Schema
schema = Product.model_json_schema()
print(schema)
```

---

## 📝 Pydantic Settings

### 环境变量配置

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My App"
    debug: bool = False
    database_url: str
    secret_key: str
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 从环境变量或.env文件加载
settings = Settings()
```

### .env文件

```env
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key
DEBUG=True
REDIS_PORT=6380
```

---

## 🚀 FastAPI集成

### 请求验证

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    # 自动验证输入
    # 自动序列化输出
    return UserResponse(
        id=1,
        username=user.username,
        email=user.email
    )
```

### 查询参数验证

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, conint

app = FastAPI()

@app.get("/items/")
def read_items(
    skip: conint(ge=0) = 0,
    limit: conint(ge=1, le=100) = 10,
    q: str = Query(None, min_length=3, max_length=50)
):
    return {"skip": skip, "limit": limit, "q": q}
```

---

## ⚡ 性能优化

### Pydantic V2

```python
# Pydantic V2使用Rust编写的pydantic-core
# 比V1快5-50倍

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# 性能测试
import timeit

data = {"id": 1, "name": "Alice", "email": "alice@example.com"}

def test():
    User(**data)

time = timeit.timeit(test, number=100000)
print(f"Time: {time:.4f}s")
```

---

## 📚 最佳实践

### 1. 模型重用

```python
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
```

### 2. 响应模型

```python
from pydantic import BaseModel, computed_field

class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    
    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

### 3. ORM模式

```python
from pydantic import BaseModel, ConfigDict

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str

# 从ORM对象创建
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

# 使用
user_db = UserModel(id=1, username="alice", email="alice@example.com")
user_schema = UserSchema.model_validate(user_db)
```

---

## 🔗 相关资源

- [官方文档](https://docs.pydantic.dev/)
- [Pydantic V2迁移指南](https://docs.pydantic.dev/latest/migration/)
- [FastAPI + Pydantic](https://fastapi.tiangolo.com/tutorial/body/)

---

**最后更新**: 2025年10月28日

