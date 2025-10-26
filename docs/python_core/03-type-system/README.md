# Python 类型系统深度解析

**Python 3.12/3.13 类型系统完全指南**

---

## 📚 目录

- [1. 类型系统概述](#1-类型系统概述)
  - [1.1 核心概念](#11-核心概念)
- [2. Python 3.12 类型系统新特性](#2-python-312-类型系统新特性)
  - [2.1 PEP 695: 类型参数语法](#21-pep-695-类型参数语法)
  - [2.2 PEP 698: @override 装饰器](#22-pep-698-override-装饰器)
- [3. 基础类型注解](#3-基础类型注解)
- [4. 高级类型特性](#4-高级类型特性)
- [5. 泛型编程](#5-泛型编程)
- [6. 协议与结构化子类型](#6-协议与结构化子类型)
- [7. 类型检查工具](#7-类型检查工具)
- [8. 实战案例](#8-实战案例)
- [9. 延伸阅读](#9-延伸阅读)

**相关子文档**:
- [类型注解基础](01-type-hints-basics.md) - Python 类型注解入门
- [泛型与协议](02-generics-protocols.md) - 高级类型特性
- [类型推导](03-type-inference.md) - 类型推导机制
- [mypy 静态检查](04-mypy.md) - mypy 使用指南
- [pyright 类型检查](05-pyright.md) - pyright 使用指南
- [运行时类型检查](06-runtime-checking.md) - 运行时验证
- [PEP 695 类型参数](07-pep695-type-parameters.md) - Python 3.12 新特性

---

## 1. 类型系统概述

Python 的类型系统是**渐进式**的：

- **动态类型**：运行时类型检查
- **静态类型注解**：可选的类型提示
- **结构化子类型**：基于协议的类型匹配

### 1.1 核心概念

```python
from typing import TypeVar, Generic, Protocol, TypeAlias

# 1. 基础类型注解
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 2. 泛型类型
T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()

# 3. 协议（结构化子类型）
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()

# 4. 类型别名 (Python 3.12+)
type Point = tuple[float, float]
type Matrix = list[list[float]]
```

---

## 2. Python 3.12 类型系统新特性

### 2.1 PEP 695: 类型参数语法

```python
# 旧语法 (Python < 3.12)
from typing import TypeVar, Generic

T = TypeVar("T")

class OldStack(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []

# 新语法 (Python 3.12+)
class Stack[T]:
    def __init__(self) -> None:
        self.items: list[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()

# 泛型函数
def first[T](items: list[T]) -> T:
    return items[0]

# 类型别名
type IntStack = Stack[int]
type Point[T] = tuple[T, T]
```

### 2.2 PEP 698: @override 装饰器

```python
from typing import override

class Base:
    def method(self) -> None:
        pass

class Derived(Base):
    @override  # 确保是覆盖父类方法
    def method(self) -> None:
        super().method()
    
    @override
    def typo_method(self) -> None:  # 错误！父类没有此方法
        pass
```

---

## 3. 类型注解层次

### Level 1: 基础类型

```python
# 内置类型
age: int = 25
name: str = "Alice"
is_active: bool = True
score: float = 95.5

# 集合类型
numbers: list[int] = [1, 2, 3]
names: tuple[str, ...] = ("Alice", "Bob")
mapping: dict[str, int] = {"a": 1, "b": 2}
unique: set[int] = {1, 2, 3}
```

### Level 2: 可选与联合

```python
from typing import Optional, Union

# 可选类型
def find_user(user_id: int) -> Optional[str]:
    if user_id > 0:
        return "User"
    return None

# 联合类型 (Python 3.10+)
def process(value: int | str) -> None:
    match value:
        case int():
            print(f"Integer: {value}")
        case str():
            print(f"String: {value}")

# None 类型
def log(message: str) -> None:
    print(message)
```

### Level 3: 泛型与类型变量

```python
from typing import TypeVar, Generic, Sequence

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value

def first[T](items: Sequence[T]) -> T:
    return items[0]

# 约束类型变量
Number = TypeVar("Number", int, float)

def add[Number](a: Number, b: Number) -> Number:
    return a + b  # type: ignore
```

### Level 4: 协议与结构化子类型

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool: ...
    def __gt__(self, other: "Comparable") -> bool: ...

def sort_items[T: Comparable](items: list[T]) -> list[T]:
    return sorted(items)

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __lt__(self, other: "Person") -> bool:
        return self.age < other.age
    
    def __gt__(self, other: "Person") -> bool:
        return self.age > other.age

# Person 自动满足 Comparable 协议
people = [Person("Alice", 30), Person("Bob", 25)]
sorted_people = sort_items(people)
```

---

## 4. 高级类型特性

### 1. 类型守卫

```python
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process_strings(items: list[object]) -> None:
    if is_str_list(items):
        # items 的类型现在是 list[str]
        for item in items:
            print(item.upper())  # OK
```

### 2. 字面量类型

```python
from typing import Literal

Mode = Literal["r", "w", "a"]

def open_file(name: str, mode: Mode) -> None:
    with open(name, mode) as f:
        pass

open_file("test.txt", "r")  # OK
open_file("test.txt", "x")  # 类型错误！
```

### 3. 类型别名

```python
# Python 3.12+ 新语法
type UserId = int
type UserName = str
type UserData = dict[UserId, UserName]

# 泛型类型别名
type Matrix[T] = list[list[T]]
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
```

### 4. 参数规范

```python
from typing import ParamSpec, Concatenate

P = ParamSpec("P")
R = TypeVar("R")

def add_logging[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@add_logging
def greet(name: str, age: int) -> str:
    return f"Hello, {name} ({age})"
```

---

## 5. 类型检查工具

### mypy 配置

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
strict = true

[[tool.mypy.overrides]]
module = "third_party.*"
ignore_missing_imports = true
```

### pyright 配置

```json
// pyrightconfig.json
{
  "pythonVersion": "3.12",
  "typeCheckingMode": "strict",
  "reportMissingTypeStubs": true,
  "reportUnknownParameterType": true,
  "reportUnknownArgumentType": true,
  "reportUnknownLambdaType": true
}
```

---

## 6. 类型系统最佳实践

### 1. 优先使用内置泛型

```python
# ✅ 推荐 (Python 3.9+)
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ❌ 避免 (旧式)
from typing import List, Dict

def process(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}
```

### 2. 使用协议而非继承

```python
# ✅ 推荐
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...

def close_resource(resource: SupportsClose) -> None:
    resource.close()

# ❌ 避免强制继承
from abc import ABC, abstractmethod

class Closeable(ABC):
    @abstractmethod
    def close(self) -> None: ...
```

### 3. 使用 TypeAlias 明确意图

```python
from typing import TypeAlias

# ✅ 明确这是类型别名
UserId: TypeAlias = int
UserName: TypeAlias = str

# Python 3.12+
type UserId = int
type UserName = str
```

### 4. 避免过度使用 Any

```python
from typing import Any

# ❌ 避免
def process(data: Any) -> Any:
    return data

# ✅ 使用泛型
def process[T](data: T) -> T:
    return data
```

---

## 7. 实际应用案例

### 案例 1: 类型安全的配置类

```python
from typing import Generic, TypeVar, Literal
from dataclasses import dataclass

Environment = Literal["development", "staging", "production"]

@dataclass
class Config:
    app_name: str
    debug: bool
    environment: Environment
    port: int = 8000
    
    def is_production(self) -> bool:
        return self.environment == "production"

config = Config(
    app_name="MyApp",
    debug=True,
    environment="development"
)
```

### 案例 2: 类型安全的 API 响应

```python
from typing import Generic, TypeVar, Literal
from pydantic import BaseModel

T = TypeVar("T")
Status = Literal["success", "error"]

class ApiResponse(BaseModel, Generic[T]):
    status: Status
    data: T | None = None
    message: str | None = None

class User(BaseModel):
    id: int
    name: str
    email: str

def get_user(user_id: int) -> ApiResponse[User]:
    if user_id > 0:
        user = User(id=user_id, name="Alice", email="alice@example.com")
        return ApiResponse(status="success", data=user)
    return ApiResponse(status="error", message="User not found")
```

### 案例 3: 类型安全的装饰器

```python
from typing import TypeVar, ParamSpec, Callable
from functools import wraps
import time

P = ParamSpec("P")
R = TypeVar("R")

def timer[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function(n: int) -> int:
    time.sleep(n)
    return n * 2

result: int = slow_function(2)  # 类型正确
```

---

## 8. 延伸阅读

- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 544 - Protocols](https://peps.python.org/pep-0544/)
- [PEP 585 - Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)
- [PEP 604 - Union Types](https://peps.python.org/pep-0604/)
- [PEP 612 - Parameter Specification Variables](https://peps.python.org/pep-0612/)
- [PEP 613 - TypeAlias](https://peps.python.org/pep-0613/)
- [PEP 647 - TypeGuard](https://peps.python.org/pep-0647/)
- [PEP 673 - Self Type](https://peps.python.org/pep-0673/)
- [PEP 675 - Literal String Type](https://peps.python.org/pep-0675/)
- [PEP 681 - Data Class Transforms](https://peps.python.org/pep-0681/)
- [PEP 692 - TypedDict with Unpack](https://peps.python.org/pep-0692/)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [PEP 698 - Override Decorator](https://peps.python.org/pep-0698/)

---

**掌握类型系统，编写更安全的 Python 代码！** 🔤✨
