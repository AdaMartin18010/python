# Python 类型注解最佳实践

**类型系统实战指南**

---

## 📋 目录

- [何时使用类型注解](#何时使用类型注解)
- [类型注解风格指南](#类型注解风格指南)
- [性能考虑](#性能考虑)
- [与设计模式结合](#与设计模式结合)
- [实战技巧](#实战技巧)

---

## 何时使用类型注解

### 应该添加类型注解的场景

```python
"""
推荐添加类型注解的场景
"""

# 1. 公开API - 必须
def public_function(x: int, y: str) -> dict[str, int]:
    """公开函数必须有类型注解"""
    return {"result": x}

# 2. 类的公开方法 - 必须
class UserService:
    """用户服务"""
    
    def get_user(self, user_id: int) -> dict[str, str] | None:
        """获取用户"""
        return {"name": "Alice"}
    
    def create_user(self, name: str, age: int) -> int:
        """创建用户，返回ID"""
        return 123

# 3. 复杂函数 - 推荐
def process_data(
    items: list[dict[str, int]],
    threshold: float = 0.5
) -> tuple[list[int], list[int]]:
    """复杂逻辑推荐类型注解"""
    passed = [item["value"] for item in items if item["value"] > threshold]
    failed = [item["value"] for item in items if item["value"] <= threshold]
    return passed, failed

# 4. 回调函数 - 推荐
from typing import Callable

def register_callback(
    callback: Callable[[str, int], bool]
) -> None:
    """注册回调"""
    callback("event", 42)

# 5. 数据模型 - 推荐
from dataclasses import dataclass

@dataclass
class User:
    """用户数据模型"""
    id: int
    name: str
    email: str
    age: int | None = None
```

### 可以省略类型注解的场景

```python
"""
可以省略类型注解的场景
"""

# 1. 显而易见的类型
def main() -> None:
    name = "Alice"  # 明显是str
    age = 30  # 明显是int
    items = [1, 2, 3]  # 明显是list[int]

# 2. 简单的私有辅助函数
def _helper(x):
    """内部简单辅助函数"""
    return x * 2

# 3. 推导式和生成器表达式
numbers = [1, 2, 3, 4, 5]
squares = [x * x for x in numbers]  # 类型可推断
doubled = (x * 2 for x in numbers)  # 类型可推断

# 4. Lambda函数
apply = lambda x: x * 2  # 简单lambda

# 5. 临时变量
for i in range(10):  # i明显是int
    temp = i * 2  # temp可推断
```

---

## 类型注解风格指南

### 现代Python类型语法

```python
"""
推荐使用Python 3.10+语法
"""

# ❌ 旧语法 (Python 3.9之前)
from typing import List, Dict, Optional, Union

def process(items: Optional[List[int]]) -> Dict[str, Union[int, str]]:
    pass

# ✅ 新语法 (Python 3.10+)
def process(items: list[int] | None) -> dict[str, int | str]:
    pass

# ❌ 旧Union
def handle(value: Union[int, str, None]) -> str:
    pass

# ✅ 新|运算符
def handle(value: int | str | None) -> str:
    pass

# Python 3.12+ 泛型语法
# ❌ 旧语法
T = TypeVar('T')

class Stack(Generic[T]):
    pass

# ✅ 新语法
class Stack[T]:
    pass
```

### 类型注解格式

```python
"""
类型注解格式规范
"""

# 1. 变量注解
name: str = "Alice"
age: int = 30
scores: list[int] = [95, 87, 92]

# 2. 函数注解 - 参数和返回值
def greet(name: str, age: int) -> str:
    return f"Hello {name}, age {age}"

# 3. 长参数列表 - 分行
def complex_function(
    param1: str,
    param2: int,
    param3: list[dict[str, int]],
    param4: Callable[[int], str] | None = None
) -> tuple[str, int, bool]:
    """复杂函数签名"""
    pass

# 4. 类型别名 - 简化复杂类型
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
type Handler = Callable[[str, int], bool]

def process_json(data: JSON) -> None:
    pass

def register(handler: Handler) -> None:
    pass

# 5. 属性注解
class Config:
    """配置类"""
    host: str
    port: int
    debug: bool = False
    
    def __init__(self):
        self.host = "localhost"
        self.port = 8080
```

---

## 性能考虑

### 类型注解的性能影响

```python
"""
类型注解性能分析
"""

# 类型注解不影响运行时性能
def add(x: int, y: int) -> int:
    return x + y

# 等价于
def add(x, y):
    return x + y

# 运行时性能完全相同

# 但是会影响:
# 1. 启动时间 - 解析类型注解
# 2. 内存占用 - 存储类型信息

# 如果需要优化启动时间
from __future__ import annotations

# 类型注解变成字符串,延迟求值
def func(x: list[int]) -> dict[str, int]:
    pass

# 等价于
def func(x: "list[int]") -> "dict[str, int]":
    pass

# 类型检查工具仍然工作
# 但运行时开销更小
```

### 避免运行时类型检查

```python
"""
避免不必要的运行时类型检查
"""

# ❌ 不推荐 - 运行时检查
def process(items: list[int]) -> int:
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    if not all(isinstance(x, int) for x in items):
        raise TypeError("items must contain only integers")
    return sum(items)

# ✅ 推荐 - 依赖类型检查器
def process(items: list[int]) -> int:
    """类型由mypy保证"""
    return sum(items)

# 但是对于外部输入,应该验证
def process_user_input(data: str) -> dict[str, int]:
    """外部数据需要验证"""
    import json
    try:
        parsed = json.loads(data)
        if not isinstance(parsed, dict):
            raise ValueError("Expected dict")
        return parsed
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")

# 或者使用Pydantic
from pydantic import BaseModel, ValidationError

class UserInput(BaseModel):
    """输入验证"""
    name: str
    age: int

def process_input(data: dict) -> UserInput:
    """自动验证"""
    return UserInput(**data)
```

---

## 与设计模式结合

### 工厂模式类型

```python
"""
工厂模式的类型注解
"""
from typing import Protocol
from abc import ABC, abstractmethod

# 使用Protocol定义接口
class Shape(Protocol):
    """形状协议"""
    def area(self) -> float: ...
    def perimeter(self) -> float: ...

class Circle:
    """圆形"""
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

class Rectangle:
    """矩形"""
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# 工厂函数
from typing import Literal

ShapeType = Literal["circle", "rectangle"]

def create_shape(
    shape_type: ShapeType,
    **kwargs: float
) -> Shape:
    """创建形状"""
    if shape_type == "circle":
        return Circle(kwargs["radius"])
    elif shape_type == "rectangle":
        return Rectangle(kwargs["width"], kwargs["height"])
    raise ValueError(f"Unknown shape type: {shape_type}")

# 类型安全的工厂
shape = create_shape("circle", radius=5.0)
```

### 单例模式类型

```python
"""
单例模式的类型注解
"""
from typing import TypeVar, Type

T = TypeVar('T')

class Singleton:
    """单例基类"""
    _instance: "Singleton | None" = None
    
    def __new__(cls: Type[T]) -> T:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance  # type: ignore

class Config(Singleton):
    """配置单例"""
    def __init__(self):
        self.settings: dict[str, str] = {}
    
    def get(self, key: str) -> str | None:
        return self.settings.get(key)

# 使用
config1 = Config()
config2 = Config()
assert config1 is config2  # 同一实例
```

### 装饰器模式类型

```python
"""
装饰器的类型注解
"""
from typing import Callable, TypeVar, ParamSpec
from functools import wraps

P = ParamSpec('P')
R = TypeVar('R')

def timer(func: Callable[P, R]) -> Callable[P, R]:
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function(n: int) -> int:
    """慢函数"""
    import time
    time.sleep(n)
    return n * 2

# 类型完全保留
result: int = slow_function(1)

# 带参数的装饰器
def repeat(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """重复装饰器"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for _ in range(times - 1):
                func(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def greet(name: str) -> str:
    print(f"Hello {name}")
    return name
```

---

## 实战技巧

### 第三方库集成

```python
"""
与第三方库结合使用
"""

# 1. Pydantic数据验证
from pydantic import BaseModel, Field, validator

class User(BaseModel):
    """用户模型"""
    id: int = Field(..., gt=0, description="User ID")
    name: str = Field(..., min_length=1, max_length=50)
    email: str
    age: int | None = Field(None, ge=0, le=150)
    
    @validator('email')
    def validate_email(cls, v: str) -> str:
        """验证邮箱"""
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

# 2. SQLAlchemy ORM
from sqlalchemy.orm import Mapped, mapped_column

class UserModel:
    """用户表"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int | None] = mapped_column(default=None)

# 3. FastAPI路由
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int) -> User:
    """获取用户"""
    # 返回类型自动验证和序列化
    return User(id=user_id, name="Alice", email="alice@example.com")

@app.post("/users")
async def create_user(user: User) -> User:
    """创建用户"""
    # 请求体自动验证
    return user
```

### 错误处理类型

```python
"""
错误处理的类型注解
"""
from typing import TypeVar, Generic

T = TypeVar('T')
E = TypeVar('E', bound=Exception)

class Result(Generic[T, E]):
    """结果类型"""
    
    def __init__(self, value: T | None = None, error: E | None = None):
        self._value = value
        self._error = error
    
    @property
    def is_ok(self) -> bool:
        return self._error is None
    
    @property
    def value(self) -> T:
        if self._error is not None:
            raise self._error
        assert self._value is not None
        return self._value
    
    @property
    def error(self) -> E | None:
        return self._error

def safe_divide(a: int, b: int) -> Result[float, ZeroDivisionError]:
    """安全除法"""
    try:
        return Result(value=a / b)
    except ZeroDivisionError as e:
        return Result(error=e)

# 使用
result = safe_divide(10, 2)
if result.is_ok:
    print(result.value)  # 5.0
else:
    print(f"Error: {result.error}")
```

### 测试中的类型

```python
"""
测试代码的类型注解
"""
import pytest
from typing import Callable

# 测试函数推荐添加类型
def test_addition() -> None:
    """测试加法"""
    assert 1 + 1 == 2

# Fixture类型
@pytest.fixture
def user() -> dict[str, str]:
    """用户fixture"""
    return {"name": "Alice", "email": "alice@example.com"}

def test_user(user: dict[str, str]) -> None:
    """测试用户"""
    assert user["name"] == "Alice"

# Mock类型
from unittest.mock import Mock

def test_with_mock() -> None:
    """使用Mock测试"""
    mock_func: Callable[[int], str] = Mock(return_value="result")
    result = mock_func(42)
    assert result == "result"
    mock_func.assert_called_once_with(42)
```

---

## 📚 核心要点

### 何时使用

- ✅ **公开API**: 必须添加类型
- ✅ **复杂逻辑**: 推荐添加类型
- ✅ **回调函数**: 推荐添加类型
- ✅ **数据模型**: 推荐添加类型
- ❌ **显而易见**: 可以省略

### 风格指南

- ✅ **使用Python 3.10+语法**: | 而非Union
- ✅ **使用内置泛型**: list 而非 List
- ✅ **类型别名**: 简化复杂类型
- ✅ **分行**: 长参数列表分行

### 性能

- ✅ **零运行时开销**: 类型注解不影响性能
- ✅ **from __future__ import annotations**: 延迟求值
- ✅ **避免运行时检查**: 依赖类型检查器
- ✅ **外部输入验证**: 使用Pydantic

### 设计模式

- ✅ **Protocol**: 定义接口
- ✅ **ParamSpec**: 装饰器类型
- ✅ **Generic**: 泛型模式
- ✅ **TypeVar**: 类型变量

### 实战技巧

- ✅ **Pydantic**: 数据验证
- ✅ **SQLAlchemy**: ORM类型
- ✅ **FastAPI**: 路由类型
- ✅ **pytest**: 测试类型
- ✅ **Result**: 错误处理

---

**掌握最佳实践，写出优雅类型安全代码！** 🎯✨

**相关文档**:
- [01-type-hints-basics.md](01-type-hints-basics.md) - 类型注解基础
- [04-mypy.md](04-mypy.md) - mypy类型检查

**最后更新**: 2025年10月28日

