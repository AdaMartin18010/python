# Python 类型系统

**动态类型与静态类型注解的完美结合**

---

## 📋 目录

- [类型系统概述](#类型系统概述)
- [动态类型机制](#动态类型机制)
- [类型注解系统](#类型注解系统)
- [类型检查工具](#类型检查工具)
- [高级类型特性](#高级类型特性)

---

## 类型系统概述

### Python的双重类型系统

```python
"""
Python的类型系统特点
"""

# 1. 动态类型 (Runtime)
x = 42          # x是int
x = "hello"     # x变成str
x = [1, 2, 3]   # x变成list

# 没有编译时错误,运行时才确定类型

# 2. 静态类型注解 (Type Hints)
def greet(name: str) -> str:
    return f"Hello, {name}"

# 类型注解不影响运行时
result = greet(123)  # 运行时不会报错
print(result)        # Hello, 123

# 但类型检查器会发现问题
# mypy: error: Argument 1 to "greet" has incompatible type "int"
```

### 类型系统的层次

```python
"""
Python类型层次结构
"""

# object - 所有类的基类
print(isinstance(42, object))       # True
print(isinstance("hi", object))     # True
print(isinstance(type, object))     # True

# type - 所有类的元类
print(isinstance(int, type))        # True
print(isinstance(str, type))        # True

# 内置类型层次
"""
object
├── type
├── int
│   └── bool
├── float
├── str
├── list
├── tuple
├── dict
├── set
└── ...
"""
```

---

## 动态类型机制

### 鸭子类型 (Duck Typing)

```python
"""
"如果它走起来像鸭子,叫起来像鸭子,那它就是鸭子"
"""

class Duck:
    def quack(self):
        return "Quack!"

class Person:
    def quack(self):
        return "I'm quacking like a duck!"

def make_it_quack(thing):
    """只要有quack方法就行"""
    return thing.quack()

# 都能工作
print(make_it_quack(Duck()))    # Quack!
print(make_it_quack(Person()))  # I'm quacking like a duck!

# ============================================
# 实际应用: 文件like对象
# ============================================

class StringFile:
    """字符串模拟文件"""
    
    def __init__(self, content: str):
        self.content = content
        self.pos = 0
    
    def read(self, size=-1):
        if size == -1:
            result = self.content[self.pos:]
            self.pos = len(self.content)
        else:
            result = self.content[self.pos:self.pos + size]
            self.pos += size
        return result
    
    def readline(self):
        end = self.content.find('\n', self.pos)
        if end == -1:
            result = self.content[self.pos:]
            self.pos = len(self.content)
        else:
            result = self.content[self.pos:end + 1]
            self.pos = end + 1
        return result

def process_file(file):
    """处理任何file-like对象"""
    return file.read()

# 可以使用真实文件或自定义对象
sf = StringFile("Hello\nWorld")
print(process_file(sf))  # Hello\nWorld
```

### 类型转换与强制

```python
"""
Python的类型转换
"""

# 1. 显式转换
x = "42"
y = int(x)      # str → int
z = float(y)    # int → float
s = str(z)      # float → str

# 2. 隐式转换 (数值类型)
result = 10 + 3.14   # int + float → float
print(type(result))  # <class 'float'>

# 3. bool转换规则
"""
False: None, False, 0, 0.0, "", [], {}, set()
True:  其他所有值
"""

print(bool([]))     # False
print(bool([1]))    # True

# 4. 自定义转换
class Meters:
    def __init__(self, value: float):
        self.value = value
    
    def __int__(self):
        """转换为int"""
        return int(self.value)
    
    def __float__(self):
        """转换为float"""
        return float(self.value)
    
    def __str__(self):
        """转换为str"""
        return f"{self.value}m"

m = Meters(5.5)
print(int(m))    # 5
print(float(m))  # 5.5
print(str(m))    # 5.5m
```

---

## 类型注解系统

### 基础类型注解

```python
"""
基础类型注解 (PEP 484)
"""
from typing import List, Dict, Tuple, Set, Optional, Union, Any

# 变量注解
name: str = "Alice"
age: int = 30
height: float = 1.75
is_active: bool = True

# 容器类型
names: List[str] = ["Alice", "Bob"]
scores: Dict[str, int] = {"Alice": 95, "Bob": 87}
point: Tuple[int, int] = (10, 20)
tags: Set[str] = {"python", "typing"}

# Optional (可以是None)
middle_name: Optional[str] = None
# 等价于: Union[str, None]

# Union (多种类型)
def process(value: Union[int, str]) -> str:
    return str(value)

# Any (任意类型)
def flexible(data: Any) -> Any:
    return data
```

### 函数类型注解

```python
"""
函数和方法的类型注解
"""
from typing import Callable

# 函数注解
def add(x: int, y: int) -> int:
    """两数相加"""
    return x + y

# 无返回值
def log(message: str) -> None:
    print(message)

# 回调函数类型
def process_data(
    data: List[int],
    callback: Callable[[int], str]
) -> List[str]:
    """处理数据并通过回调转换"""
    return [callback(x) for x in data]

# 使用
result = process_data([1, 2, 3], lambda x: str(x * 2))
print(result)  # ['2', '4', '6']

# ============================================
# 方法注解 (Python 3.11+)
# ============================================

from typing import Self

class Builder:
    """流式构建器"""
    
    def __init__(self):
        self.value = 0
    
    def add(self, x: int) -> Self:
        """返回自身"""
        self.value += x
        return self
    
    def multiply(self, x: int) -> Self:
        """返回自身"""
        self.value *= x
        return self

# 链式调用
builder = Builder().add(5).multiply(2).add(3)
print(builder.value)  # 13
```

### 泛型类型

```python
"""
泛型类型 (Generic Types)
"""
from typing import TypeVar, Generic, List

# 类型变量
T = TypeVar('T')

class Stack(Generic[T]):
    """泛型栈"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """压栈"""
        self._items.append(item)
    
    def pop(self) -> T:
        """出栈"""
        return self._items.pop()
    
    def is_empty(self) -> bool:
        """是否为空"""
        return len(self._items) == 0

# 使用
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(int_stack.pop())  # 2

str_stack: Stack[str] = Stack()
str_stack.push("hello")
print(str_stack.pop())  # hello

# ============================================
# Python 3.12+ 新语法
# ============================================

class Stack[T]:
    """使用新泛型语法"""
    
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()
```

---

## 类型检查工具

### mypy类型检查

```python
"""
mypy - Python静态类型检查器
"""

# 正确的代码
def greet(name: str) -> str:
    return f"Hello, {name}"

result: str = greet("Alice")  # ✅ OK

# mypy会发现的错误
# result: int = greet("Alice")  # ❌ error
# greet(123)                     # ❌ error

# ============================================
# 类型守卫 (Type Guards)
# ============================================

from typing import TypeGuard

def is_string_list(val: List[object]) -> TypeGuard[List[str]]:
    """类型守卫: 检查是否全是字符串"""
    return all(isinstance(x, str) for x in val)

def process(items: List[object]) -> None:
    if is_string_list(items):
        # mypy知道这里items是List[str]
        print(items[0].upper())  # ✅ OK
    else:
        # 这里items仍是List[object]
        # print(items[0].upper())  # ❌ error

# ============================================
# TypedDict
# ============================================

from typing import TypedDict

class Person(TypedDict):
    """类型化字典"""
    name: str
    age: int
    email: str

def create_person(name: str, age: int, email: str) -> Person:
    return {
        "name": name,
        "age": age,
        "email": email
    }

person: Person = create_person("Alice", 30, "alice@example.com")
print(person["name"])  # ✅ OK
# print(person["unknown"])  # ❌ mypy error
```

### Protocol - 结构化类型

```python
"""
Protocol - 实现鸭子类型的类型检查
"""
from typing import Protocol

class Drawable(Protocol):
    """可绘制协议"""
    
    def draw(self) -> str:
        ...

class Circle:
    """圆形"""
    
    def draw(self) -> str:
        return "Drawing circle"

class Square:
    """正方形"""
    
    def draw(self) -> str:
        return "Drawing square"

def render(shape: Drawable) -> None:
    """渲染形状"""
    print(shape.draw())

# 不需要继承Protocol,只要实现了draw方法即可
render(Circle())  # ✅ OK
render(Square())  # ✅ OK

# ============================================
# 运行时可检查的Protocol
# ============================================

from typing import runtime_checkable

@runtime_checkable
class Sized(Protocol):
    """有大小的对象"""
    
    def __len__(self) -> int:
        ...

# 运行时检查
print(isinstance([1, 2, 3], Sized))  # True
print(isinstance("hello", Sized))    # True
print(isinstance(42, Sized))         # False
```

---

## 高级类型特性

### Literal类型

```python
"""
Literal - 字面量类型
"""
from typing import Literal

Mode = Literal["r", "w", "a"]

def open_file(filename: str, mode: Mode) -> None:
    """打开文件"""
    print(f"Opening {filename} in mode {mode}")

open_file("data.txt", "r")  # ✅ OK
# open_file("data.txt", "x")  # ❌ mypy error

# ============================================
# 枚举 vs Literal
# ============================================

from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

# 使用Literal更轻量
ColorLiteral = Literal["red", "green", "blue"]

def paint_literal(color: ColorLiteral) -> None:
    print(f"Painting with {color}")

def paint_enum(color: Color) -> None:
    print(f"Painting with {color.value}")
```

### NewType - 创建新类型

```python
"""
NewType - 创建不同的类型
"""
from typing import NewType

# 创建新类型
UserId = NewType('UserId', int)
OrderId = NewType('OrderId', int)

def get_user(user_id: UserId) -> str:
    return f"User {user_id}"

def get_order(order_id: OrderId) -> str:
    return f"Order {order_id}"

# 使用
user_id = UserId(123)
order_id = OrderId(456)

print(get_user(user_id))    # ✅ OK
# print(get_user(order_id))  # ❌ mypy error (类型不匹配)
```

### 类型别名

```python
"""
类型别名 (Type Aliases)
"""
from typing import TypeAlias

# 简单别名
Vector: TypeAlias = List[float]
Matrix: TypeAlias = List[Vector]

def dot_product(v1: Vector, v2: Vector) -> float:
    return sum(x * y for x, y in zip(v1, v2))

# 复杂别名
JSON: TypeAlias = Union[
    Dict[str, "JSON"],
    List["JSON"],
    str,
    int,
    float,
    bool,
    None
]

def parse_json(data: str) -> JSON:
    import json
    return json.loads(data)

# ============================================
# Python 3.12+ type语句
# ============================================

type Vector = list[float]
type Matrix = list[Vector]

type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None
```

---

## 📚 核心要点

### 类型系统特点

- ✅ **动态类型**: 运行时确定类型,灵活性高
- ✅ **类型注解**: 静态分析,提高代码质量
- ✅ **鸭子类型**: 接口大于继承
- ✅ **渐进类型**: 逐步添加类型注解

### 类型注解优势

- 📖 **文档作用**: 代码更易读
- 🐛 **错误检测**: 提前发现类型错误
- 💡 **IDE支持**: 更好的代码补全
- 🔧 **重构支持**: 更安全的重构

### 最佳实践

- ✅ 公开API必须有类型注解
- ✅ 使用`mypy`或`pyright`进行检查
- ✅ 优先使用`Protocol`而不是抽象基类
- ✅ 合理使用`Any`,但要注明原因
- ✅ 使用Python 3.10+的新语法 (`|`代替`Union`)

---

**类型系统让Python更强大、更安全！** 🎯✨

**相关文档**:
- [01-data-model.md](01-data-model.md) - 数据模型
- [03-memory-model.md](03-memory-model.md) - 内存模型
- [../03-type-system/](../03-type-system/) - 类型系统深度解析

**最后更新**: 2025年10月28日

