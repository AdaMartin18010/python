# Python Pydantic 数据验证

**Pydantic完全使用指南**

---

## 📋 目录

- [Pydantic简介](#Pydantic简介)
- [模型定义](#模型定义)
- [数据验证](#数据验证)
- [高级特性](#高级特性)
- [实战应用](#实战应用)

---

## Pydantic简介

### 什么是Pydantic

```python
"""
Pydantic: 基于Python类型注解的数据验证库
"""

# 安装
# uv add pydantic

from pydantic import BaseModel

# 基础示例
class User(BaseModel):
    """用户模型"""
    id: int
    name: str
    email: str
    age: int | None = None

# 创建实例
user = User(id=1, name="Alice", email="alice@example.com")
print(user.id)  # 1
print(user.model_dump())  # 转换为字典

# 自动类型转换
user2 = User(id="2", name="Bob", email="bob@example.com", age="30")
print(user2.id)  # 2 (字符串自动转int)
print(user2.age)  # 30 (字符串自动转int)

# 验证失败
try:
    invalid_user = User(id="abc", name="Charlie", email="charlie@example.com")
except ValueError as e:
    print(e)  # validation error
```

### Pydantic vs dataclass

```python
"""
Pydantic与dataclass对比
"""

from dataclasses import dataclass
from pydantic import BaseModel

# dataclass
@dataclass
class UserDC:
    id: int
    name: str

# Pydantic
class UserPD(BaseModel):
    id: int
    name: str

# 区别:
# 1. 数据验证
user_dc = UserDC(id="1", name="Alice")  # ✅ 不验证
print(type(user_dc.id))  # <class 'str'>

user_pd = UserPD(id="1", name="Alice")  # ✅ 自动转换
print(type(user_pd.id))  # <class 'int'>

# 2. JSON支持
import json

# dataclass需要手动转换
# json.dumps(user_dc)  # ❌ 不能直接序列化

# Pydantic内置支持
print(user_pd.model_dump_json())  # ✅ {"id":1,"name":"Alice"}

# 3. 嵌套验证
class Address(BaseModel):
    street: str
    city: str

class UserWithAddress(BaseModel):
    name: str
    address: Address

# 自动验证嵌套结构
user_data = {
    "name": "Alice",
    "address": {"street": "123 Main St", "city": "NYC"}
}
user = UserWithAddress(**user_data)  # ✅ 自动验证
```

---

## 模型定义

### Field配置

```python
"""
Field字段配置
"""
from pydantic import BaseModel, Field

class User(BaseModel):
    """用户模型"""
    
    # 必需字段
    id: int = Field(..., description="User ID")
    
    # 默认值
    name: str = Field(default="Anonymous", description="Username")
    
    # 约束
    age: int = Field(ge=0, le=150, description="Age between 0 and 150")
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", description="Email")
    
    # 数值约束
    score: float = Field(gt=0.0, lt=100.0, description="Score between 0 and 100")
    
    # 字符串约束
    username: str = Field(min_length=3, max_length=20)
    
    # 列表约束
    tags: list[str] = Field(default_factory=list, max_length=10)
    
    # 别名
    user_type: str = Field(alias="type", description="User type")
    
    # 示例值
    bio: str | None = Field(None, examples=["I love Python!"])

# 使用
user = User(
    id=1,
    age=30,
    email="alice@example.com",
    score=95.5,
    username="alice",
    type="admin"  # 使用别名
)
```

### 配置选项

```python
"""
模型配置
"""
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    """用户模型"""
    model_config = ConfigDict(
        # 严格模式
        strict=True,
        
        # 额外字段处理
        extra="forbid",  # 禁止额外字段
        # extra="allow",  # 允许额外字段
        # extra="ignore",  # 忽略额外字段
        
        # 允许可变性
        frozen=False,  # True表示不可变
        
        # 验证赋值
        validate_assignment=True,
        
        # 使用枚举值
        use_enum_values=True,
        
        # 填充默认值
        populate_by_name=True,
        
        # JSON schema
        json_schema_extra={
            "examples": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"}
            ]
        }
    )
    
    id: int
    name: str
    email: str

# 额外字段禁止
try:
    user = User(id=1, name="Alice", email="alice@example.com", extra_field="value")
except ValueError as e:
    print(e)  # Extra inputs are not permitted

# 验证赋值
user = User(id=1, name="Alice", email="alice@example.com")
user.id = 2  # ✅ 自动验证
# user.id = "abc"  # ❌ validation error
```

---

## 数据验证

### 自定义验证器

```python
"""
自定义验证器
"""
from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    """用户模型"""
    name: str
    email: str
    password: str
    password_confirm: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """验证邮箱"""
        if '@' not in v:
            raise ValueError('Invalid email')
        if not v.endswith('.com'):
            raise ValueError('Email must end with .com')
        return v.lower()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """验证密码"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
    
    @model_validator(mode='after')
    def validate_passwords_match(self) -> 'User':
        """验证密码匹配"""
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self

# 使用
try:
    user = User(
        name="Alice",
        email="ALICE@EXAMPLE.COM",
        password="Secure123",
        password_confirm="Secure123"
    )
    print(user.email)  # alice@example.com (已转小写)
except ValueError as e:
    print(e)
```

### 数据转换

```python
"""
数据转换和序列化
"""
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    """事件模型"""
    name: str
    timestamp: datetime
    metadata: dict[str, int | str]
    
    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime, _info) -> str:
        """序列化时间戳"""
        return dt.isoformat()
    
    @field_serializer('metadata')
    def serialize_metadata(self, data: dict, _info) -> str:
        """序列化元数据为JSON字符串"""
        import json
        return json.dumps(data)

# 使用
event = Event(
    name="UserLogin",
    timestamp=datetime.now(),
    metadata={"user_id": 123, "ip": "192.168.1.1"}
)

# 序列化
print(event.model_dump())
# {'name': 'UserLogin', 'timestamp': datetime(...), 'metadata': {...}}

print(event.model_dump(mode='json'))
# {'name': 'UserLogin', 'timestamp': '2025-10-28T...', 'metadata': '{"user_id":123,"ip":"192.168.1.1"}'}
```

---

## 高级特性

### 泛型模型

```python
"""
泛型Pydantic模型
"""
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    """通用响应模型"""
    code: int
    message: str
    data: T

class User(BaseModel):
    """用户模型"""
    id: int
    name: str

# 使用
user_response = Response[User](
    code=200,
    message="Success",
    data=User(id=1, name="Alice")
)

# 列表响应
users_response = Response[list[User]](
    code=200,
    message="Success",
    data=[
        User(id=1, name="Alice"),
        User(id=2, name="Bob")
    ]
)

# 类型检查
reveal_type(user_response.data)  # User
reveal_type(users_response.data)  # list[User]
```

### 计算字段

```python
"""
计算字段
"""
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    """矩形"""
    width: float
    height: float
    
    @computed_field
    @property
    def area(self) -> float:
        """计算面积"""
        return self.width * self.height
    
    @computed_field
    @property
    def perimeter(self) -> float:
        """计算周长"""
        return 2 * (self.width + self.height)

# 使用
rect = Rectangle(width=10, height=5)
print(rect.area)  # 50
print(rect.perimeter)  # 30

# 序列化包含计算字段
print(rect.model_dump())
# {'width': 10.0, 'height': 5.0, 'area': 50.0, 'perimeter': 30.0}
```

### 模型继承

```python
"""
模型继承和组合
"""
from pydantic import BaseModel

# 基础模型
class TimestampMixin(BaseModel):
    """时间戳混入"""
    created_at: datetime
    updated_at: datetime | None = None

class User(TimestampMixin):
    """用户模型"""
    id: int
    name: str
    email: str

# 多重继承
class SoftDeleteMixin(BaseModel):
    """软删除混入"""
    deleted_at: datetime | None = None
    is_deleted: bool = False

class Post(TimestampMixin, SoftDeleteMixin):
    """文章模型"""
    id: int
    title: str
    content: str
    author_id: int

# 使用
post = Post(
    id=1,
    title="Hello",
    content="World",
    author_id=1,
    created_at=datetime.now()
)
```

---

## 实战应用

### FastAPI集成

```python
"""
Pydantic与FastAPI集成
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    """创建用户请求"""
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(ge=0, le=150)

class UserResponse(BaseModel):
    """用户响应"""
    id: int
    name: str
    email: str
    age: int
    
    model_config = ConfigDict(from_attributes=True)

# 创建用户
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate) -> UserResponse:
    """创建用户"""
    # user自动验证
    # 返回类型自动序列化
    return UserResponse(id=1, **user.model_dump())

# 获取用户
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    """获取用户"""
    # 模拟数据库查询
    return UserResponse(
        id=user_id,
        name="Alice",
        email="alice@example.com",
        age=30
    )

# 更新用户
class UserUpdate(BaseModel):
    """更新用户请求"""
    name: str | None = None
    email: str | None = None
    age: int | None = Field(None, ge=0, le=150)

@app.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, update: UserUpdate) -> UserResponse:
    """更新用户"""
    # 只更新提供的字段
    updates = update.model_dump(exclude_unset=True)
    return UserResponse(id=user_id, name="Alice", email="alice@example.com", age=30)
```

### 配置管理

```python
"""
使用Pydantic管理配置
"""
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """应用配置"""
    
    # 数据库配置
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(env="DB_NAME")
    db_user: str = Field(env="DB_USER")
    db_password: str = Field(env="DB_PASSWORD")
    
    # Redis配置
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    
    # API配置
    api_key: str = Field(env="API_KEY")
    api_secret: str = Field(env="API_SECRET")
    debug: bool = Field(default=False, env="DEBUG")
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    @property
    def database_url(self) -> str:
        """数据库URL"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

# 使用
settings = Settings()
print(settings.database_url)
print(settings.debug)
```

### 数据序列化

```python
"""
复杂数据序列化
"""
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """用户角色"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Address(BaseModel):
    """地址"""
    street: str
    city: str
    country: str

class User(BaseModel):
    """用户"""
    id: int
    name: str
    email: str
    role: UserRole
    address: Address
    created_at: datetime
    tags: list[str] = []
    metadata: dict[str, int | str] = {}

# 创建用户
user = User(
    id=1,
    name="Alice",
    email="alice@example.com",
    role=UserRole.ADMIN,
    address=Address(street="123 Main St", city="NYC", country="USA"),
    created_at=datetime.now(),
    tags=["python", "pydantic"],
    metadata={"level": 5, "status": "active"}
)

# 序列化为字典
print(user.model_dump())

# 序列化为JSON
print(user.model_dump_json(indent=2))

# 排除字段
print(user.model_dump(exclude={"email", "metadata"}))

# 只包含字段
print(user.model_dump(include={"id", "name", "role"}))

# 序列化为JSON schema
print(user.model_json_schema())
```

---

## 📚 核心要点

### Pydantic基础

- ✅ **数据验证**: 自动验证和类型转换
- ✅ **JSON支持**: 内置序列化/反序列化
- ✅ **类型安全**: 基于Python类型注解
- ✅ **性能**: 使用Rust核心(v2)

### 模型定义

- ✅ **Field**: 字段约束和配置
- ✅ **ConfigDict**: 模型配置
- ✅ **默认值**: default和default_factory
- ✅ **别名**: alias支持

### 数据验证

- ✅ **field_validator**: 字段验证器
- ✅ **model_validator**: 模型验证器
- ✅ **自定义验证**: 灵活的验证逻辑
- ✅ **数据转换**: serializer

### 高级特性

- ✅ **泛型模型**: Generic支持
- ✅ **计算字段**: computed_field
- ✅ **模型继承**: 继承和混入
- ✅ **递归模型**: 自引用模型

### 实战应用

- ✅ **FastAPI**: 完美集成
- ✅ **配置管理**: BaseSettings
- ✅ **序列化**: model_dump/model_dump_json
- ✅ **JSON Schema**: 自动生成

---

**掌握Pydantic，构建健壮的数据验证！** 🛡️✨

**相关文档**:
- [01-type-hints-basics.md](01-type-hints-basics.md) - 类型注解基础
- [05-typing-best-practices.md](05-typing-best-practices.md) - 类型最佳实践

**最后更新**: 2025年10月28日

