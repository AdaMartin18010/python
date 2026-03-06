# PEP 742: TypeIs - 更好的类型收窄

> Python 3.13 新特性 - TypeIs 作为 TypeGuard 的改进替代

---

## 概述

**PEP 742** 引入了 `typing.TypeIs`，作为 `TypeGuard` 的更直观替代方案，用于类型收窄（Type Narrowing）。

**发布版本**: Python 3.13+
**PEP链接**: [PEP 742](https://peps.python.org/pep-0742/)

**核心改进**:

- ✅ 更直观的语义（正向 vs 反向收窄）
- ✅ 更灵活的类型推断
- ✅ 更好的错误处理支持
- ✅ 与类型守卫模式的更好集成

---

## TypeGuard vs TypeIs

### 回顾 TypeGuard (Python 3.10+)

```python
from typing import TypeGuard

def is_str_list(values: list[object]) -> TypeGuard[list[str]]:
    """检查是否所有元素都是字符串"""
    return all(isinstance(x, str) for x in values)

def process(items: list[object]) -> None:
    if is_str_list(items):
        # items 被收窄为 list[str]
        for item in items:
            print(item.upper())  # OK
    else:
        # items 保持 list[object]
        pass
```

### TypeIs 的改进

```python
from typing import TypeIs

def is_string(value: object) -> TypeIs[str]:
    """检查值是否为字符串"""
    return isinstance(value, str)

def process(value: object) -> None:
    if is_string(value):
        # value 被收窄为 str
        print(value.upper())  # OK
    else:
        # value 被收窄为 ~str（不是 str 的类型）
        # 这在某些场景下更有用
        pass
```

**关键区别**: `TypeIs` 在 `else` 分支中也能提供类型信息！

---

## 基础用法

### 1. 基本类型守卫

```python
from typing import TypeIs

def is_positive_int(value: int) -> TypeIs[int]:
    """检查整数是否为正数"""
    return value > 0

def calculate(value: int) -> None:
    if is_positive_int(value):
        # value: int (正数)
        result = 100 / value  # 安全，不会除零
        print(f"Result: {result}")
    else:
        # value: int (<= 0)
        print("Value must be positive")
```

### 2. 联合类型的收窄

```python
from typing import TypeIs
from dataclasses import dataclass

@dataclass
class Success:
    data: str

@dataclass
class Error:
    message: str

Result = Success | Error

def is_success(result: Result) -> TypeIs[Success]:
    """检查结果是否为成功"""
    return isinstance(result, Success)

def handle_result(result: Result) -> None:
    if is_success(result):
        # result: Success
        print(f"Success: {result.data}")
    else:
        # result: Error（被收窄为不是 Success 的类型）
        print(f"Error: {result.message}")
```

### 3. 复杂类型检查

```python
from typing import TypeIs, TypedDict

class APIResponse(TypedDict):
    status: str
    data: dict

def is_valid_response(obj: object) -> TypeIs[APIResponse]:
    """验证对象是否为有效的 API 响应"""
    if not isinstance(obj, dict):
        return False

    required_keys = {"status", "data"}
    if not required_keys.issubset(obj.keys()):
        return False

    if not isinstance(obj["status"], str):
        return False

    if not isinstance(obj["data"], dict):
        return False

    return True

def process_api_result(result: object) -> None:
    if is_valid_response(result):
        # result: APIResponse
        print(f"Status: {result['status']}")
        print(f"Data: {result['data']}")
    else:
        # result: object（但不是 APIResponse）
        print("Invalid response format")
```

---

## 实战模式

### 模式 1: 错误处理

```python
from typing import TypeIs, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T")
E = TypeVar("E")

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err(Generic[E]):
    error: E

Result = Ok[T] | Err[E]

def is_ok(result: Result[T, E]) -> TypeIs[Ok[T]]:
    """检查是否为成功结果"""
    return isinstance(result, Ok)

def is_err(result: Result[T, E]) -> TypeIs[Err[E]]:
    """检查是否为错误结果"""
    return isinstance(result, Err)

# 使用
def divide(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

result = divide(10, 2)

if is_ok(result):
    # result: Ok[float]
    print(f"Result: {result.value}")
elif is_err(result):
    # result: Err[str]
    print(f"Error: {result.error}")
```

### 模式 2: 类型安全的数据验证

```python
from typing import TypeIs, TypedDict, NotRequired
import json

class UserData(TypedDict):
    name: str
    age: int
    email: NotRequired[str]

def is_user_data(obj: object) -> TypeIs[UserData]:
    """验证对象是否符合 UserData 结构"""
    if not isinstance(obj, dict):
        return False

    # 检查必需字段
    if "name" not in obj or not isinstance(obj["name"], str):
        return False

    if "age" not in obj or not isinstance(obj["age"], int):
        return False

    # 检查可选字段
    if "email" in obj and not isinstance(obj["email"], str):
        return False

    return True

def parse_user_json(json_str: str) -> UserData | None:
    """解析 JSON 并验证"""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return None

    if is_user_data(data):
        # data: UserData
        return data

    return None

# 使用
json_input = '{"name": "Alice", "age": 30, "email": "alice@example.com"}'
user = parse_user_json(json_input)

if user:
    print(f"Name: {user['name']}")
    print(f"Age: {user['age']}")
    if "email" in user:
        print(f"Email: {user['email']}")
```

### 模式 3: 集合元素检查

```python
from typing import TypeIs, TypeVar

T = TypeVar("T")

def all_of_type(
    items: list[object],
    type_check: callable[[object], TypeIs[T]]
) -> TypeIs[list[T]]:
    """
    检查列表中所有元素是否都符合指定类型

    Args:
        items: 要检查的列表
        type_check: 类型检查函数

    Returns:
        如果所有元素都符合类型则返回 True，同时收窄类型
    """
    return all(type_check(item) for item in items)

def is_int(value: object) -> TypeIs[int]:
    return isinstance(value, int)

def is_str(value: object) -> TypeIs[str]:
    return isinstance(value, str)

# 使用
mixed_values: list[object] = [1, 2, 3, 4, 5]

if all_of_type(mixed_values, is_int):
    # mixed_values: list[int]
    total = sum(mixed_values)  # OK
    print(f"Sum: {total}")

string_values: list[object] = ["a", "b", "c"]

if all_of_type(string_values, is_str):
    # string_values: list[str]
    combined = "".join(string_values)  # OK
    print(f"Combined: {combined}")
```

### 模式 4: 条件类型处理

```python
from typing import TypeIs
from dataclasses import dataclass
from enum import Enum, auto

class ShapeType(Enum):
    CIRCLE = auto()
    RECTANGLE = auto()
    TRIANGLE = auto()

@dataclass
class Circle:
    radius: float

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

@dataclass
class Rectangle:
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height

@dataclass
class Triangle:
    base: float
    height: float

    def area(self) -> float:
        return 0.5 * self.base * self.height

Shape = Circle | Rectangle | Triangle

def is_circle(shape: Shape) -> TypeIs[Circle]:
    return isinstance(shape, Circle)

def is_rectangle(shape: Shape) -> TypeIs[Rectangle]:
    return isinstance(shape, Rectangle)

def is_triangle(shape: Shape) -> TypeIs[Triangle]:
    return isinstance(shape, Triangle)

def describe_shape(shape: Shape) -> str:
    """描述形状并计算面积"""
    if is_circle(shape):
        # shape: Circle
        return f"Circle with radius {shape.radius}, area = {shape.area():.2f}"
    elif is_rectangle(shape):
        # shape: Rectangle
        return f"Rectangle {shape.width}x{shape.height}, area = {shape.area():.2f}"
    elif is_triangle(shape):
        # shape: Triangle
        return f"Triangle base={shape.base}, height={shape.height}, area = {shape.area():.2f}"
    else:
        # shape: Never（穷尽检查）
        return "Unknown shape"

# 使用
shapes: list[Shape] = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 4)
]

for shape in shapes:
    print(describe_shape(shape))
```

---

## 高级用法

### 与泛型结合

```python
from typing import TypeIs, TypeVar, Generic

T = TypeVar("T")

def is_instance_of(
    value: object,
    cls: type[T]
) -> TypeIs[T]:
    """通用类型检查"""
    return isinstance(value, cls)

# 使用
value: object = "hello"

if is_instance_of(value, str):
    # value: str
    print(value.upper())

if is_instance_of(value, int):
    # value: int
    print(value + 1)
```

### 反向类型收窄

```python
from typing import TypeIs
from dataclasses import dataclass

@dataclass
class Cat:
    name: str
    meow_volume: int

@dataclass
class Dog:
    name: str
    bark_volume: int

Pet = Cat | Dog

def is_cat(pet: Pet) -> TypeIs[Cat]:
    return isinstance(pet, Cat)

def interact(pet: Pet) -> None:
    if is_cat(pet):
        # pet: Cat
        print(f"{pet.name} meows at volume {pet.meow_volume}")
    else:
        # pet: Dog（被收窄为不是 Cat 的类型）
        print(f"{pet.name} barks at volume {pet.bark_volume}")
```

---

## TypeIs vs TypeGuard 对比

| 特性 | TypeGuard | TypeIs |
|------|-----------|--------|
| 正向收窄 | ✅ | ✅ |
| 反向收窄 (else 分支) | ❌ | ✅ |
| 语义直观性 | 一般 | 更好 |
| Python 版本 | 3.10+ | 3.13+ |
| 推荐程度 | 一般 | ⭐ 推荐 |

### 迁移示例

```python
# 使用 TypeGuard（旧）
from typing import TypeGuard

def is_str_guard(value: object) -> TypeGuard[str]:
    return isinstance(value, str)

# 使用 TypeIs（新）- 推荐
from typing import TypeIs

def is_str_is(value: object) -> TypeIs[str]:
    return isinstance(value, str)

# 两者在使用时看起来相同
def process(value: object) -> None:
    if is_str_is(value):
        print(value.upper())
    else:
        # TypeIs 的优势：else 分支也有类型信息
        # value 被收窄为 ~str
        pass
```

---

## 最佳实践

### ✅ 应该做的

1. **使用 TypeIs 替代 TypeGuard**

   ```python
   # 推荐
   from typing import TypeIs

   def is_valid(value: object) -> TypeIs[str]:
       return isinstance(value, str) and len(value) > 0
   ```

2. **为类型守卫函数提供清晰的文档**

   ```python
   def is_positive(value: int) -> TypeIs[int]:
       """
       检查整数是否为正数

       Returns:
           True 如果 value > 0，同时收窄类型到正整数
       """
       return value > 0
   ```

3. **在验证函数中使用 TypeIs**

   ```python
   def is_config(obj: object) -> TypeIs[Config]:
       """验证对象是否为有效的配置"""
       # 复杂的验证逻辑
       ...
   ```

### ❌ 不应该做的

1. **不要返回矛盾的 TypeIs**

   ```python
   # 错误：逻辑矛盾
   def is_string(value: int) -> TypeIs[str]:
       return True  # 错误：int 不可能是 str
   ```

2. **不要过度使用 TypeIs**

   ```python
   # 不必要的 TypeIs
   def is_not_none(value: T | None) -> TypeIs[T]:
       return value is not None

   # 简单场景直接用 value is not None
   ```

---

## 兼容性

| Python 版本 | 支持情况 |
|-------------|----------|
| 3.13+ | ✅ `typing.TypeIs` 原生支持 |
| 3.12 | ❌ 不支持 |
| 3.11 | ❌ 不支持 |
| 3.10 | ❌ 使用 `TypeGuard` 替代 |

### 向后兼容方案

```python
import sys
from typing import TypeVar

T = TypeVar("T")

if sys.version_info >= (3, 13):
    from typing import TypeIs
else:
    from typing import TypeGuard as TypeIs  # 降级方案

# 使用
def is_string(value: object) -> TypeIs[str]:
    return isinstance(value, str)
```

---

## 延伸阅读

- [PEP 742 - TypeIs](https://peps.python.org/pep-0742/)
- [PEP 647 - TypeGuard](https://peps.python.org/pep-0647/)
- [Python 3.13 What's New](https://docs.python.org/3.13/whatsnew/3.13.html)

---

**使用 TypeIs，实现更精确、更直观的类型收窄！** 🔍✨
