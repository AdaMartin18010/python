# Python 泛型与协议

**结构化类型与泛型编程**

---

## 📋 目录

- [泛型基础](#泛型基础)
- [Protocol协议](#Protocol协议)
- [泛型类与函数](#泛型类与函数)
- [协变与逆变](#协变与逆变)
- [高级泛型特性](#高级泛型特性)

---

## 泛型基础

### TypeVar类型变量

```python
"""
TypeVar: 泛型类型变量
"""
from typing import TypeVar, Generic

# 定义类型变量
T = TypeVar('T')

def identity(x: T) -> T:
    """返回相同类型"""
    return x

# 类型推断
result1 = identity(42)      # int
result2 = identity("hello") # str

# 约束类型变量
NumberT = TypeVar('NumberT', int, float)

def add(x: NumberT, y: NumberT) -> NumberT:
    """只接受int或float"""
    return x + y

# 有界类型变量
from collections.abc import Sized

SizedT = TypeVar('SizedT', bound=Sized)

def get_length(obj: SizedT) -> int:
    """获取长度，要求有__len__"""
    return len(obj)

get_length([1, 2, 3])  # ✅
get_length("hello")    # ✅
# get_length(42)       # ❌ int没有__len__
```

### 泛型容器

```python
"""
泛型容器实现
"""
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    """泛型栈"""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """压栈"""
        self._items.append(item)

    def pop(self) -> T:
        """出栈"""
        return self._items.pop()

    def peek(self) -> T | None:
        """查看栈顶"""
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        """是否为空"""
        return len(self._items) == 0

# 使用
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
value = int_stack.pop()  # type: int

str_stack: Stack[str] = Stack()
str_stack.push("hello")
# str_stack.push(42)  # ❌ mypy error

# 多个类型参数
K = TypeVar('K')
V = TypeVar('V')

class Pair(Generic[K, V]):
    """泛型键值对"""

    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

    def get_key(self) -> K:
        return self.key

    def get_value(self) -> V:
        return self.value

pair: Pair[str, int] = Pair("age", 30)
```

---

## Protocol协议

### Protocol基础

```python
"""
Protocol: 结构化类型(鸭子类型的类型检查)
"""
from typing import Protocol

class Drawable(Protocol):
    """可绘制协议"""

    def draw(self) -> str:
        """绘制方法"""
        ...

# 不需要继承Protocol，只要实现了draw方法即可
class Circle:
    def draw(self) -> str:
        return "Drawing circle"

class Square:
    def draw(self) -> str:
        return "Drawing square"

def render(shape: Drawable) -> None:
    """渲染形状"""
    print(shape.draw())

# 类型检查通过
render(Circle())
render(Square())

# 运行时检查
from typing import runtime_checkable

@runtime_checkable
class Sized(Protocol):
    """有大小的协议"""
    def __len__(self) -> int: ...

# 运行时检查
print(isinstance([1, 2, 3], Sized))  # True
print(isinstance("hello", Sized))    # True
print(isinstance(42, Sized))         # False
```

### 内置Protocol

```python
"""
常用内置Protocol
"""
from typing import (
    Iterable, Iterator, Sequence,
    Mapping, Container, Sized
)

# Iterable: 可迭代
def process(items: Iterable[int]) -> int:
    """处理可迭代对象"""
    return sum(items)

process([1, 2, 3])      # list
process({1, 2, 3})      # set
process((1, 2, 3))      # tuple
process(range(1, 4))    # range

# Iterator: 迭代器
def consume(it: Iterator[str]) -> list[str]:
    """消费迭代器"""
    return list(it)

# Sequence: 序列
def get_middle(seq: Sequence[int]) -> int:
    """获取中间元素"""
    return seq[len(seq) // 2]

# Mapping: 映射
def get_value(mapping: Mapping[str, int], key: str) -> int | None:
    """从映射获取值"""
    return mapping.get(key)

# Container: 容器
def contains(container: Container[int], value: int) -> bool:
    """检查是否包含"""
    return value in container
```

---

## 泛型类与函数

### 泛型函数

```python
"""
泛型函数示例
"""
from typing import TypeVar, Sequence

T = TypeVar('T')

def first(items: Sequence[T]) -> T | None:
    """返回第一个元素"""
    return items[0] if items else None

def last(items: Sequence[T]) -> T | None:
    """返回最后一个元素"""
    return items[-1] if items else None

def reverse(items: list[T]) -> list[T]:
    """反转列表"""
    return items[::-1]

# 多类型参数
K = TypeVar('K')
V = TypeVar('V')

def swap_dict(d: dict[K, V]) -> dict[V, K]:
    """交换字典键值"""
    return {v: k for k, v in d.items()}

original = {"a": 1, "b": 2}
swapped = swap_dict(original)  # dict[int, str]
```

### Python 3.12+ 新语法

```python
"""
Python 3.12泛型新语法 (PEP 695)
"""

# 泛型函数
def first[T](items: list[T]) -> T | None:
    """返回第一个元素"""
    return items[0] if items else None

# 泛型类
class Stack[T]:
    """泛型栈"""
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# 类型别名
type Vector[T] = list[T]
type Matrix[T] = list[Vector[T]]

# 有界类型参数
def get_length[T: Sized](obj: T) -> int:
    """要求T是Sized的子类型"""
    return len(obj)

# 多个类型参数
def zip_dicts[K, V1, V2](
    d1: dict[K, V1],
    d2: dict[K, V2]
) -> dict[K, tuple[V1, V2]]:
    """合并两个字典"""
    return {k: (d1[k], d2[k]) for k in d1.keys() & d2.keys()}
```

---

## 协变与逆变

### 型变基础

```python
"""
协变、逆变和不变
"""
from typing import TypeVar, Generic

# 不变 (Invariant) - 默认
T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

# Box[Dog]不是Box[Animal]的子类型

# 协变 (Covariant) - 用于输出
T_co = TypeVar('T_co', covariant=True)

class Producer(Generic[T_co]):
    """只产生T_co，不消费"""
    def produce(self) -> T_co:
        ...

# Producer[Dog]是Producer[Animal]的子类型

# 逆变 (Contravariant) - 用于输入
T_contra = TypeVar('T_contra', contravariant=True)

class Consumer(Generic[T_contra]):
    """只消费T_contra，不产生"""
    def consume(self, value: T_contra) -> None:
        ...

# Consumer[Animal]是Consumer[Dog]的子类型

# 实际例子
class Animal:
    pass

class Dog(Animal):
    def bark(self) -> str:
        return "Woof!"

class Cat(Animal):
    def meow(self) -> str:
        return "Meow!"

# 协变: 可以用子类替换父类
dogs: list[Dog] = [Dog()]
animals: Sequence[Animal] = dogs  # ✅ Sequence是协变的

# 不变: 不能替换
dogs_list: list[Dog] = [Dog()]
# animals_list: list[Animal] = dogs_list  # ❌ list是不变的
```

### 实际应用

```python
"""
型变的实际应用
"""
from typing import TypeVar, Generic, Callable

# 示例1: 只读容器(协变)
T_co = TypeVar('T_co', covariant=True)

class ReadOnlyCollection(Generic[T_co]):
    """只读集合"""
    def __init__(self, items: list[T_co]):
        self._items = items

    def get(self, index: int) -> T_co:
        """获取元素"""
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

# 可以用子类型替换
dogs = ReadOnlyCollection([Dog()])
animals: ReadOnlyCollection[Animal] = dogs  # ✅

# 示例2: 比较器(逆变)
T_contra = TypeVar('T_contra', contravariant=True)

class Comparator(Generic[T_contra]):
    """比较器"""
    def compare(self, a: T_contra, b: T_contra) -> int:
        """比较两个对象"""
        ...

# 可以用父类型替换
animal_comparator: Comparator[Animal] = ...
dog_comparator: Comparator[Dog] = animal_comparator  # ✅
```

---

## 高级泛型特性

### ParamSpec和Concatenate

```python
"""
ParamSpec: 参数规范 (Python 3.10+)
"""
from typing import ParamSpec, Concatenate, Callable, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

def add_logging(
    func: Callable[P, R]
) -> Callable[P, R]:
    """添加日志装饰器"""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@add_logging
def greet(name: str, age: int) -> str:
    return f"Hello {name}, age {age}"

# 保留原函数的参数类型
result = greet("Alice", 30)  # 类型检查正确

# Concatenate: 添加额外参数
def with_context(
    func: Callable[Concatenate[str, P], R]
) -> Callable[P, R]:
    """添加上下文参数"""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func("context", *args, **kwargs)
    return wrapper
```

### TypeGuard

```python
"""
TypeGuard: 类型守卫 (Python 3.10+)
"""
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    """类型守卫: 检查是否全是字符串"""
    return all(isinstance(x, str) for x in val)

def process(items: list[object]) -> None:
    """处理列表"""
    if is_str_list(items):
        # mypy知道这里items是list[str]
        print(items[0].upper())  # ✅ OK
    else:
        # 这里items仍是list[object]
        # print(items[0].upper())  # ❌ error

# 实际应用
def is_int_dict(val: dict[str, object]) -> TypeGuard[dict[str, int]]:
    """检查字典值是否都是int"""
    return all(isinstance(v, int) for v in val.values())

def sum_values(data: dict[str, object]) -> int:
    """求和字典值"""
    if is_int_dict(data):
        return sum(data.values())  # ✅ 类型安全
    return 0
```

### Unpack和TypeVarTuple

```python
"""
Unpack和TypeVarTuple (Python 3.11+)
"""
from typing import TypeVarTuple, Unpack

# TypeVarTuple: 类型变量元组
Ts = TypeVarTuple('Ts')

def call_with_args(
    func: Callable[[Unpack[Ts]], None],
    *args: Unpack[Ts]
) -> None:
    """调用函数并传递参数"""
    func(*args)

# 泛型类中使用
class Array(Generic[Unpack[Ts]]):
    """多维数组"""
    def __init__(self, *shape: Unpack[Ts]):
        self.shape = shape

# 使用
arr: Array[int, int, int] = Array(2, 3, 4)  # 3维数组
```

---

## 📚 核心要点

### 泛型

- ✅ **TypeVar**: 类型变量
- ✅ **Generic**: 泛型基类
- ✅ **约束**: 限制类型范围
- ✅ **有界**: bound参数

### Protocol

- ✅ **结构化类型**: 鸭子类型的类型检查
- ✅ **runtime_checkable**: 运行时检查
- ✅ **内置Protocol**: Iterable, Sequence等
- ✅ **自定义Protocol**: 定义接口

### 型变

- ✅ **不变**: 默认，不能替换
- ✅ **协变**: covariant=True，输出位置
- ✅ **逆变**: contravariant=True，输入位置
- ✅ **应用**: 容器、函数类型

### 高级特性

- ✅ **ParamSpec**: 参数规范
- ✅ **TypeGuard**: 类型守卫
- ✅ **Concatenate**: 添加参数
- ✅ **Python 3.12+**: 新泛型语法

### 最佳实践

- ✅ Protocol优先于抽象基类
- ✅ 合理使用型变
- ✅ 保持泛型简单
- ✅ 使用Python 3.12+新语法
- ✅ 类型守卫提高安全性

---

**掌握泛型与协议，构建类型安全代码！** 🔒✨

**相关文档**:

- [01-type-hints-basics.md](01-type-hints-basics.md) - 类型注解基础
- [04-mypy.md](04-mypy.md) - mypy类型检查

**最后更新**: 2025年10月28日
