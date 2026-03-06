# PEP 696: 类型参数默认值

> Python 3.13 新特性 - 类型参数支持默认值

---

## 概述

**PEP 696** 为 `TypeVar`、`ParamSpec` 和 `TypeVarTuple` 引入了默认值支持，这是 Python 类型系统的重大增强。

**发布版本**: Python 3.13+  
**PEP链接**: [PEP 696](https://peps.python.org/pep-0696/)

---

## 核心概念

### 为什么需要默认值？

在 Python 3.12 及之前，泛型类/函数必须显式指定所有类型参数：

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Container(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item

# 必须指定类型
container = Container[int](42)  # 或 Container(42)，但需要推断
```

**Python 3.13** 允许为类型参数提供默认值，使泛型更易用：

```python
from typing import TypeVar

# 带默认值的类型变量
T = TypeVar("T", default=str)  # 默认值为 str

class Container[T = str]:  # Python 3.13+ 语法
    def __init__(self, item: T) -> None:
        self.item = item

# 可以不指定类型，使用默认值
container1 = Container()  # Container[str]
container2 = Container(42)  # Container[int]，推断类型
```

---

## 语法详解

### 1. TypeVar 默认值

```python
from typing import TypeVar

# 基本语法
T = TypeVar("T", default=str)
U = TypeVar("U", default=int)

# 带约束的默认值
Number = TypeVar("Number", int, float, default=int)

# 带边界的默认值
Sortable = TypeVar("Sortable", bound=str, default=str)
```

### 2. ParamSpec 默认值

```python
from typing import ParamSpec

# 参数规范的默认值
P = ParamSpec("P", default=...)  # 默认为 (() -> None)

class Decorator[P = ()]:
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        ...
```

### 3. TypeVarTuple 默认值

```python
from typing import TypeVarTuple

# 类型变量元组的默认值
Ts = TypeVarTuple("Ts", default=())  # 默认为空元组
Ts2 = TypeVarTuple("Ts2", default=(int, str))  # 默认为 (int, str)
```

---

## 实战示例

### 示例 1: 带默认值的泛型类

```python
from typing import TypeVar, Generic

T = TypeVar("T", default=str)
K = TypeVar("K", default=str)
V = TypeVar("V", default=object)

class FlexibleDict[K = str, V = object]:
    """灵活的字典类，带类型默认值"""
    
    def __init__(self) -> None:
        self._data: dict[K, V] = {}
    
    def set(self, key: K, value: V) -> None:
        self._data[key] = value
    
    def get(self, key: K) -> V | None:
        return self._data.get(key)
    
    def items(self) -> list[tuple[K, V]]:
        return list(self._data.items())


# 使用默认类型 (str, object)
dict1 = FlexibleDict()
dict1.set("name", "Alice")  # OK
dict1.set("age", 30)        # OK - value 默认为 object

# 显式指定类型
dict2 = FlexibleDict[str, int]()
dict2.set("age", 30)        # OK
# dict2.set("age", "thirty")  # 类型错误！

# 混合使用 - 使用默认值推断
dict3 = FlexibleDict()
reveal_type(dict3)  # FlexibleDict[str, object]
```

### 示例 2: 带默认值的泛型函数

```python
from typing import TypeVar

T = TypeVar("T", default=str)

def get_first[T = str](items: list[T]) -> T | None:
    """获取列表第一个元素，默认为 str 类型"""
    return items[0] if items else None

# 使用默认类型
result1 = get_first([])  # T 默认为 str，返回 str | None

# 类型推断
result2 = get_first([1, 2, 3])  # T 推断为 int，返回 int | None

# 显式指定类型
result3 = get_first[float]([1.0, 2.0])  # 显式指定 T = float
```

### 示例 3: 渐进式类型化

```python
from typing import TypeVar

# 为遗留代码添加类型，保持向后兼容
T = TypeVar("T", default=object)

class LegacyContainer[T = object]:
    """
    遗留容器类 - 默认 object 保持与旧代码兼容
    新代码可以指定更具体的类型
    """
    def __init__(self, items: list[T] | None = None) -> None:
        self.items = items or []
    
    def add(self, item: T) -> None:
        self.items.append(item)
    
    def get_all(self) -> list[T]:
        return self.items.copy()

# 旧代码 - 仍然工作
old_container = LegacyContainer()
old_container.add("anything")  # OK - 默认为 object
old_container.add(123)         # OK

# 新代码 - 类型安全
new_container = LegacyContainer[str]()
new_container.add("typed")     # OK
# new_container.add(123)       # 类型错误！
```

### 示例 4: 复杂的默认值场景

```python
from typing import TypeVar, Callable
from dataclasses import dataclass

T = TypeVar("T", default=str)
E = TypeVar("E", default=Exception)

@dataclass
class Result[T = str, E = Exception]:
    """
    结果类型，支持成功值和错误值
    默认: 成功值为 str，错误为 Exception
    """
    value: T | None = None
    error: E | None = None
    
    @property
    def is_ok(self) -> bool:
        return self.error is None
    
    def map[U](self, func: Callable[[T], U]) -> "Result[U, E]":
        """映射成功值"""
        if self.is_ok and self.value is not None:
            return Result(value=func(self.value))
        return Result(error=self.error)

# 使用默认类型
result1 = Result(value="success")  # Result[str, Exception]
result2 = Result(error=ValueError("bad"))  # Result[str, ValueError]

# 显式指定类型
result3 = Result[int, TypeError](value=42)  # Result[int, TypeError]

# 类型转换
result4 = result3.map(str)  # Result[str, TypeError]
```

---

## 高级用法

### 嵌套默认值

```python
from typing import TypeVar

T = TypeVar("T", default=int)
U = TypeVar("U", default=list[T])  # U 的默认值依赖于 T

class NestedGeneric[T = int, U = list[T]]:
    def __init__(self, value: U) -> None:
        self.value = value

# 使用
nested = NestedGeneric()  # NestedGeneric[int, list[int]]
```

### 与 Protocol 结合

```python
from typing import TypeVar, Protocol

class Serializable(Protocol):
    def serialize(self) -> str: ...

T = TypeVar("T", bound=Serializable, default=str)

class Serializer[T = str]:
    """序列化器，默认处理 str（str 可序列化）"""
    def serialize(self, obj: T) -> str:
        return obj.serialize()
```

---

## 类型检查器支持

### mypy 配置

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.13"
enable_incomplete_feature = "NewGenericSyntax"
```

### pyright 配置

```json
{
  "pythonVersion": "3.13",
  "enableExperimentalFeatures": true
}
```

---

## 迁移指南

### 从旧代码迁移

**Before (Python 3.12)**:
```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)

# 必须指定类型
stack = Stack()  # 类型不完整
```

**After (Python 3.13)**:
```python
from typing import TypeVar

T = TypeVar("T", default=object)

class Stack[T = object]:
    def __init__(self) -> None:
        self.items: list[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)

# 可以省略类型，使用默认值
stack = Stack()  # Stack[object]
```

---

## 最佳实践

### ✅ 应该做的

1. **使用有意义的默认值**
   ```python
   # 好：str 是常见的默认选择
   T = TypeVar("T", default=str)
   
   # 好：object 提供最大灵活性
   T = TypeVar("T", default=object)
   ```

2. **保持向后兼容**
   ```python
   # 为现有泛型添加默认值时，选择最通用的类型
   T = TypeVar("T", default=object)  # 保持与未类型化代码兼容
   ```

3. **文档化默认值**
   ```python
   class Container[T = str]:
       """
       通用容器
       
       类型参数:
           T: 存储的元素类型，默认为 str
       """
   ```

### ❌ 不应该做的

1. **不要使用过于具体的默认值**
   ```python
   # 不好：int 可能不是好的默认选择
   T = TypeVar("T", default=int)  # 除非有明确理由
   ```

2. **避免默认值循环依赖**
   ```python
   # 错误：循环依赖
   T = TypeVar("T", default=U)
   U = TypeVar("U", default=T)
   ```

---

## 兼容性说明

| Python 版本 | 支持情况 |
|-------------|----------|
| 3.13+ | ✅ 原生支持 |
| 3.12 | ❌ 不支持 |
| 3.11 | ❌ 不支持 |

---

## 延伸阅读

- [PEP 696 - Type Parameter Syntax](https://peps.python.org/pep-0696/)
- [Python 3.13 Release Notes](https://docs.python.org/3.13/whatsnew/3.13.html)
- [typing 模块文档](https://docs.python.org/3/library/typing.html)

---

**掌握类型参数默认值，编写更灵活的泛型代码！** 🔤✨
