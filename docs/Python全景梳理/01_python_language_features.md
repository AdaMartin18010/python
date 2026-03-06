# Python 3.12+ 语言特性全面梳理

> 本文档系统性地梳理Python 3.12及以上版本的全部核心语言特性，采用严谨的学术风格进行形式化描述。

---

## 目录

- [Python 3.12+ 语言特性全面梳理](#python-312-语言特性全面梳理)
  - [目录](#目录)
  - [第一部分：核心语法特性](#第一部分核心语法特性)
    - [1.1 类型注解系统（Type Hints）](#11-类型注解系统type-hints)
      - [1.1.1 概念定义](#111-概念定义)
      - [1.1.2 语法形式（BNF）](#112-语法形式bnf)
      - [1.1.3 核心类型构造器](#113-核心类型构造器)
      - [1.1.4 正例代码](#114-正例代码)
      - [1.1.5 反例代码](#115-反例代码)
      - [1.1.6 形式论证](#116-形式论证)
    - [1.2 模式匹配（Structural Pattern Matching）](#12-模式匹配structural-pattern-matching)
      - [1.2.1 概念定义](#121-概念定义)
      - [1.2.2 语法形式（BNF）](#122-语法形式bnf)
      - [1.2.3 正例代码](#123-正例代码)
      - [1.2.4 反例代码](#124-反例代码)
      - [1.2.5 与if-elif的形式论证](#125-与if-elif的形式论证)
    - [1.3 海象运算符（Walrus Operator :=）](#13-海象运算符walrus-operator-)
      - [1.3.1 概念定义](#131-概念定义)
      - [1.3.2 语法形式（BNF）](#132-语法形式bnf)
      - [1.3.3 属性关系](#133-属性关系)
      - [1.3.4 正例代码](#134-正例代码)
      - [1.3.5 反例代码](#135-反例代码)
      - [1.3.6 形式论证](#136-形式论证)
    - [1.4 f-string高级特性（Python 3.12+）](#14-f-string高级特性python-312)
      - [1.4.1 概念定义](#141-概念定义)
      - [1.4.2 语法形式（BNF）](#142-语法形式bnf)
      - [1.4.3 Python 3.12+ 新特性](#143-python-312-新特性)
      - [1.4.4 正例代码](#144-正例代码)
      - [1.4.5 反例代码](#145-反例代码)
      - [1.4.6 形式论证](#146-形式论证)
    - [1.5 解包操作（Unpacking）](#15-解包操作unpacking)
      - [1.5.1 概念定义](#151-概念定义)
      - [1.5.2 语法形式（BNF）](#152-语法形式bnf)
      - [1.5.3 正例代码](#153-正例代码)
      - [1.5.4 反例代码](#154-反例代码)
      - [1.5.5 形式论证](#155-形式论证)
  - [第二部分：数据模型与特殊方法](#第二部分数据模型与特殊方法)
    - [2.1 \_\_slots\_\_机制](#21-__slots__机制)
      - [2.1.1 概念定义](#211-概念定义)
      - [2.1.2 语法形式](#212-语法形式)
      - [2.1.3 属性关系](#213-属性关系)
      - [2.1.4 正例代码](#214-正例代码)
      - [2.1.5 反例代码](#215-反例代码)
      - [2.1.6 形式论证](#216-形式论证)
    - [2.2 描述符协议（**get**, **set**, **delete**）](#22-描述符协议get-set-delete)
      - [2.2.1 概念定义](#221-概念定义)
      - [2.2.2 语法形式](#222-语法形式)
      - [2.2.3 属性关系](#223-属性关系)
      - [2.2.4 正例代码](#224-正例代码)
      - [2.2.5 反例代码](#225-反例代码)
      - [2.2.6 形式论证](#226-形式论证)
    - [2.3 属性装饰器（@property）](#23-属性装饰器property)
      - [2.3.1 概念定义](#231-概念定义)
      - [2.3.2 语法形式](#232-语法形式)
      - [2.3.3 正例代码](#233-正例代码)
      - [2.3.4 反例代码](#234-反例代码)
      - [2.3.5 形式论证](#235-形式论证)
    - [2.4 元类（metaclass）](#24-元类metaclass)
      - [2.4.1 概念定义](#241-概念定义)
      - [2.4.2 类创建过程](#242-类创建过程)
      - [2.4.3 正例代码](#243-正例代码)
      - [2.4.4 反例代码](#244-反例代码)
      - [2.4.5 形式论证](#245-形式论证)
    - [2.5 抽象基类（ABC）](#25-抽象基类abc)
      - [2.5.1 概念定义](#251-概念定义)
      - [2.5.2 语法形式](#252-语法形式)
      - [2.5.3 正例代码](#253-正例代码)
      - [2.5.4 反例代码](#254-反例代码)
      - [2.5.5 形式论证](#255-形式论证)
  - [第三部分：函数式编程特性](#第三部分函数式编程特性)
    - [3.1 lambda表达式](#31-lambda表达式)
      - [3.1.1 概念定义](#311-概念定义)
      - [3.1.2 语法形式（BNF）](#312-语法形式bnf)
      - [3.1.3 正例代码](#313-正例代码)
      - [3.1.4 反例代码](#314-反例代码)
      - [3.1.5 形式论证](#315-形式论证)
    - [3.2 高阶函数（map, filter, reduce）](#32-高阶函数map-filter-reduce)
      - [3.2.1 概念定义](#321-概念定义)
      - [3.2.2 语法形式](#322-语法形式)
      - [3.2.3 正例代码](#323-正例代码)
      - [3.2.4 反例代码](#324-反例代码)
      - [3.2.5 形式论证](#325-形式论证)
    - [3.3 itertools和functools模块](#33-itertools和functools模块)
      - [3.3.1 概念定义](#331-概念定义)
      - [3.3.2 itertools核心功能](#332-itertools核心功能)
      - [3.3.3 functools核心功能](#333-functools核心功能)
      - [3.3.4 正例代码](#334-正例代码)
      - [3.3.5 反例代码](#335-反例代码)
    - [3.4 偏函数（partial）](#34-偏函数partial)
      - [3.4.1 概念定义](#341-概念定义)
      - [3.4.2 语法形式](#342-语法形式)
      - [3.4.3 正例代码](#343-正例代码)
      - [3.4.4 反例代码](#344-反例代码)
      - [3.4.5 形式论证](#345-形式论证)
  - [第四部分：面向对象高级特性](#第四部分面向对象高级特性)
    - [4.1 多重继承与MRO](#41-多重继承与mro)
      - [4.1.1 概念定义](#411-概念定义)
      - [4.1.2 MRO算法（C3线性化）](#412-mro算法c3线性化)
      - [4.1.3 正例代码](#413-正例代码)
      - [4.1.4 反例代码](#414-反例代码)
      - [4.1.5 形式论证](#415-形式论证)
    - [4.2 混入（Mixin）模式](#42-混入mixin模式)
      - [4.2.1 概念定义](#421-概念定义)
      - [4.2.2 正例代码](#422-正例代码)
      - [4.2.3 反例代码](#423-反例代码)
    - [4.3 数据类（@dataclass）](#43-数据类dataclass)
      - [4.3.1 概念定义](#431-概念定义)
      - [4.3.2 语法形式](#432-语法形式)
      - [4.3.3 正例代码](#433-正例代码)
      - [4.3.4 反例代码](#434-反例代码)
    - [4.4 枚举类（Enum）](#44-枚举类enum)
      - [4.4.1 概念定义](#441-概念定义)
      - [4.4.2 语法形式](#442-语法形式)
      - [4.4.3 正例代码](#443-正例代码)
      - [4.4.4 反例代码](#444-反例代码)
  - [第五部分：迭代器与生成器](#第五部分迭代器与生成器)
    - [5.1 迭代器协议（**iter**, **next**）](#51-迭代器协议iter-next)
      - [5.1.1 概念定义](#511-概念定义)
      - [5.1.2 语法形式](#512-语法形式)
      - [5.1.3 正例代码](#513-正例代码)
      - [5.1.4 反例代码](#514-反例代码)
    - [5.2 生成器（yield, yield from）](#52-生成器yield-yield-from)
      - [5.2.1 概念定义](#521-概念定义)
      - [5.2.2 语法形式](#522-语法形式)
      - [5.2.3 正例代码](#523-正例代码)
      - [5.2.4 反例代码](#524-反例代码)
    - [5.3 异步生成器（async yield）](#53-异步生成器async-yield)
      - [5.3.1 概念定义](#531-概念定义)
      - [5.3.2 正例代码](#532-正例代码)
    - [5.4 生成器表达式](#54-生成器表达式)
      - [5.4.1 概念定义](#541-概念定义)
      - [5.4.2 正例代码](#542-正例代码)
  - [第六部分：上下文管理器](#第六部分上下文管理器)
    - [6.1 with语句原理](#61-with语句原理)
      - [6.1.1 概念定义](#611-概念定义)
      - [6.1.2 语法形式](#612-语法形式)
    - [6.2 上下文管理器协议（**enter**, **exit**）](#62-上下文管理器协议enter-exit)
      - [6.2.1 正例代码](#621-正例代码)
    - [6.3 contextlib模块](#63-contextlib模块)
      - [6.3.1 正例代码](#631-正例代码)
    - [6.4 异步上下文管理器](#64-异步上下文管理器)
      - [6.4.1 正例代码](#641-正例代码)
  - [第七部分：装饰器](#第七部分装饰器)
    - [7.1 函数装饰器](#71-函数装饰器)
      - [7.1.1 概念定义](#711-概念定义)
      - [7.1.2 语法形式](#712-语法形式)
      - [7.1.3 正例代码](#713-正例代码)
    - [7.2 类装饰器](#72-类装饰器)
      - [7.2.1 正例代码](#721-正例代码)
    - [7.3 带参数的装饰器](#73-带参数的装饰器)
      - [7.3.1 正例代码](#731-正例代码)
    - [7.4 functools.wraps](#74-functoolswraps)
      - [7.4.1 概念定义](#741-概念定义)
      - [7.4.2 正例代码](#742-正例代码)
  - [总结](#总结)

---

## 第一部分：核心语法特性

### 1.1 类型注解系统（Type Hints）

#### 1.1.1 概念定义

**类型注解（Type Hints）** 是Python 3.5+引入的静态类型标记机制，允许开发者在代码中显式标注变量、函数参数和返回值的预期类型。该机制在运行时**不产生任何语义影响**，仅服务于静态类型检查工具（如mypy、pyright）和IDE的智能提示。

**形式化定义：**

- 设 `T` 为类型表达式，`v` 为变量标识符
- 类型注解的语法形式为 `v: T`，表示"变量v的预期类型为T"
- 函数签名的类型注解形式为 `def f(p1: T1, p2: T2) -> R:`

#### 1.1.2 语法形式（BNF）

```bnf
annotation      ::= ":" expression
return_annotation ::= "->" expression
parameter       ::= identifier [annotation] ["=" default_value]
function_def    ::= "def" identifier "(" [parameter_list] ")" [return_annotation] ":" suite
variable_annotation ::= identifier annotation ["=" value]
```

#### 1.1.3 核心类型构造器

| 类型构造器 | 语法形式 | 语义描述 | Python版本 |
|-----------|---------|---------|-----------|
| `Union` | `T1 \| T2` 或 `Union[T1, T2]` | 联合类型（多选一） | 3.10+ |
| `Optional` | `T \| None` 或 `Optional[T]` | 可选类型 | 3.10+ |
| `Callable` | `Callable[[Arg1, Arg2], Return]` | 可调用对象类型 | 3.5+ |
| `Generic` | `Generic[T]` | 泛型基类 | 3.5+ |
| `TypeVar` | `TypeVar('T', bound=Base)` | 类型变量 | 3.5+ |
| `Literal` | `Literal['a', 'b']` | 字面量类型 | 3.8+ |
| `Final` | `Final[T]` | 不可变类型 | 3.8+ |

#### 1.1.4 正例代码

```python
from typing import (
    Union, Optional, Callable, Generic, TypeVar,
    Literal, Final, List, Dict, Any
)
from collections.abc import Iterator

# ========== 基本类型注解 ==========
name: str = "Alice"
age: int = 30
height: float = 1.75
is_active: bool = True

# ========== 容器类型注解 ==========
numbers: list[int] = [1, 2, 3, 4, 5]
scores: dict[str, float] = {"math": 95.5, "english": 88.0}
pairs: tuple[int, str, bool] = (1, "hello", True)
unique_items: set[str] = {"a", "b", "c"}

# ========== Union类型（Python 3.10+ 新语法）==========
def process_value(value: int | str | None) -> str:
    """处理可能是整数、字符串或None的值"""
    if value is None:
        return "null"
    return str(value)

# 旧语法（兼容3.5-3.9）
def process_value_old(value: Union[int, str, None]) -> str:
    return str(value) if value is not None else "null"

# ========== Optional类型 ==========
def find_user(user_id: int) -> dict[str, Any] | None:
    """查找用户，可能返回None"""
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return users.get(user_id)

# ========== Callable类型 ==========
BinaryOperator = Callable[[int, int], int]

def apply_operation(a: int, b: int, op: BinaryOperator) -> int:
    """应用二元操作"""
    return op(a, b)

# 使用
result = apply_operation(5, 3, lambda x, y: x + y)  # 8

# ========== 泛型函数与类 ==========
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

def first_element(items: list[T]) -> T | None:
    """获取列表第一个元素"""
    return items[0] if items else None

class Container(Generic[T]):
    """泛型容器类"""
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

    def set(self, value: T) -> None:
        self.value = value

# 使用泛型
int_container: Container[int] = Container(42)
str_container: Container[str] = Container("hello")

# ========== 类型约束 ==========
Numeric = TypeVar('Numeric', int, float)

def add_numbers(a: Numeric, b: Numeric) -> Numeric:
    """只能接受int或float的加法"""
    return a + b

# ========== Literal类型 ==========
def set_status(status: Literal["pending", "active", "inactive"]) -> None:
    """状态只能是特定字符串字面量"""
    print(f"Status set to: {status}")

set_status("active")  # ✓ 合法
# set_status("unknown")  # ✗ 类型检查器会报错

# ========== Final类型 ==========
MAX_SIZE: Final[int] = 100  # 不应被重新赋值
PI: Final[float] = 3.14159

# ========== 复杂类型示例 ==========
NestedDict = Dict[str, Dict[str, List[int]]]

def process_nested(data: NestedDict) -> Iterator[tuple[str, int]]:
    """处理嵌套字典结构"""
    for outer_key, inner_dict in data.items():
        for inner_key, values in inner_dict.items():
            for value in values:
                yield (f"{outer_key}.{inner_key}", value)

# ========== 自引用类型 ==========
from typing import Self

class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None

    def set_left(self, node: Self) -> Self:  # Python 3.11+
        self.left = node
        return self
```

#### 1.1.5 反例代码

```python
from typing import List

# ========== 反例1：运行时类型检查误解 ==========
def add(a: int, b: int) -> int:
    return a + b

# 类型注解不会在运行时检查！
result = add("hello", "world")  # 运行时不会报错，返回 "helloworld"
# 但静态类型检查器（如mypy）会警告

# ========== 反例2：循环导入问题 ==========
# file_a.py
# from file_b import ClassB  # 循环导入！
# class ClassA:
#     def method(self) -> ClassB: ...

# file_b.py
# from file_a import ClassA  # 循环导入！
# class ClassB:
#     def method(self) -> ClassA: ...

# 解决方案：使用字符串前向引用
# file_a.py
class ClassA:
    def method(self) -> "ClassB": ...  # 字符串前向引用

# ========== 反例3：可变默认参数的类型陷阱 ==========
from typing import List

def append_item(item: int, items: List[int] = []) -> List[int]:  # 危险！
    items.append(item)
    return items

# 正确做法
def append_item_safe(item: int, items: List[int] | None = None) -> List[int]:
    if items is None:
        items = []
    items.append(item)
    return items

# ========== 反例4：泛型类型变量的误用 ==========
from typing import TypeVar, Generic

T = TypeVar('T')

class BadContainer(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []  # 问题：T在此上下文中未绑定

    def add(self, item: T) -> None:
        self.items.append(item)

# 问题：实例化时无法推断T
# container = BadContainer()  # T是什么？
# container.add("hello")  # 现在T是str，但为时已晚

# 正确做法
good_container: BadContainer[str] = BadContainer()
good_container.add("hello")
```

#### 1.1.6 形式论证

**定理1.1（类型注解的语义中性）**
> 设程序P包含类型注解，程序P'为P去除所有类型注解后的版本，则对于任意输入I，有 `P(I) ≡ P'(I)`。

**证明：**

1. 类型注解在CPython实现中被存储于 `__annotations__` 字典
2. 解释器在执行代码时不访问 `__annotations__`
3. 因此类型注解不影响运行时语义 ∎

**定理1.2（泛型的类型擦除）**
> 泛型类型信息在运行时被擦除，即 `Container[int]` 和 `Container[str]` 在运行时均为 `Container` 类型。

**证明：**

```python
from typing import Generic, TypeVar

T = TypeVar('T')
class Container(Generic[T]): pass

print(Container[int] == Container[str])  # False（静态时）
print(Container[int]().__class__ == Container[str]().__class__)  # True（运行时）
```

---

### 1.2 模式匹配（Structural Pattern Matching）

#### 1.2.1 概念定义

**结构模式匹配（Structural Pattern Matching）** 是Python 3.10引入的语法特性，基于PEP 634/635/636实现。它允许程序根据数据结构的形式进行条件分支，而非仅基于值相等性判断。

**核心概念：**

- **匹配对象（Subject）**：被匹配的表达式
- **模式（Pattern）**：描述期望的数据结构形式
- **守卫子句（Guard）**：模式匹配后的附加条件
- **绑定（Binding）**：将匹配的部分赋值给变量

#### 1.2.2 语法形式（BNF）

```bnf
match_statement ::= "match" subject ":" NEWLINE INDENT case_block+ DEDENT
case_block      ::= "case" pattern [guard] ":" suite
guard           ::= "if" expression
pattern         ::= literal_pattern
                  | capture_pattern
                  | wildcard_pattern
                  | sequence_pattern
                  | mapping_pattern
                  | class_pattern
                  | or_pattern
literal_pattern ::= stringliteral | bytesliteral
                  | number | "None" | "True" | "False"
capture_pattern ::= identifier
wildcard_pattern ::= "_"
sequence_pattern ::= "[" [pattern ("," pattern)* [","]] "]"
                   | "(" [pattern ("," pattern)* [","]] ")"
mapping_pattern ::= "{" [pattern_pair ("," pattern_pair)* [","]] "}"
pattern_pair    ::= (stringliteral | attr) ":" pattern
class_pattern   ::= name "(" [pattern_arg ("," pattern_arg)*] ")"
```

#### 1.2.3 正例代码

```python
from dataclasses import dataclass
from typing import Any
from enum import Enum, auto

# ========== 基本模式匹配 ==========
def describe_value(value: Any) -> str:
    match value:
        case None:
            return "空值"
        case True:
            return "真"
        case False:
            return "假"
        case 0:
            return "零"
        case 1:
            return "一"
        case int(n) if n < 0:
            return f"负整数: {n}"
        case int(n) if n > 100:
            return f"大整数: {n}"
        case int():
            return f"整数: {value}"
        case str(s) if len(s) > 10:
            return f"长字符串: {s[:10]}..."
        case str():
            return f"字符串: {value}"
        case _:
            return f"其他类型: {type(value).__name__}"

# ========== 序列模式匹配 ==========
def analyze_sequence(seq: list[Any]) -> str:
    match seq:
        case []:
            return "空列表"
        case [single]:  # 单元素
            return f"单元素列表: {single}"
        case [first, second]:  # 两个元素
            return f"双元素列表: {first}, {second}"
        case [first, *middle, last]:  # 解构
            return f"多元素列表: 首={first}, 中={middle}, 尾={last}"
        case _:
            return "未知序列"

# ========== 字典/映射模式匹配 ==========
def process_config(config: dict[str, Any]) -> str:
    match config:
        case {"type": "database", "host": str(h), "port": int(p)}:
            return f"数据库配置: {h}:{p}"
        case {"type": "cache", "ttl": int(t)} if t > 0:
            return f"缓存配置: TTL={t}秒"
        case {"debug": True, **rest}:
            return f"调试模式开启, 其他配置: {rest}"
        case {}:
            return "空配置"
        case _:
            return "未知配置格式"

# ========== 类模式匹配（数据类）==========
@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    radius: float

@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point

def describe_shape(shape: Any) -> str:
    match shape:
        case Point(0, 0):
            return "原点"
        case Point(x, 0):
            return f"x轴上的点: ({x}, 0)"
        case Point(0, y):
            return f"y轴上的点: (0, {y})"
        case Point(x, y) if x == y:
            return f"对角线上的点: ({x}, {y})"
        case Point(x, y):
            return f"点: ({x}, {y})"
        case Circle(Point(0, 0), r):
            return f"以原点为圆心的圆, 半径={r}"
        case Circle(c, r) if r <= 0:
            return f"无效圆: 中心{c}, 非正半径{r}"
        case Circle(center, radius):
            return f"圆: 中心{center}, 半径={radius}"
        case Rectangle(Point(x1, y1), Point(x2, y2)) if x1 < x2 and y1 > y2:
            width = x2 - x1
            height = y1 - y2
            return f"矩形: 宽={width}, 高={height}"
        case _:
            return "未知形状"

# ========== OR模式 ==========
def categorize(value: Any) -> str:
    match value:
        case "red" | "green" | "blue":
            return "原色"
        case "cyan" | "magenta" | "yellow":
            return "次色"
        case int() | float():
            return "数字"
        case list() | tuple():
            return "序列"
        case _:
            return "其他"

# ========== 枚举模式匹配 ==========
class Status(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()

def handle_status(status: Status) -> str:
    match status:
        case Status.PENDING:
            return "等待处理..."
        case Status.PROCESSING:
            return "处理中..."
        case Status.COMPLETED:
            return "处理完成！"
        case Status.FAILED:
            return "处理失败！"

# ========== 嵌套模式匹配（JSON处理）==========
def process_api_response(response: dict[str, Any]) -> dict[str, Any]:
    match response:
        case {"status": "success", "data": {"users": list(users)}}:
            return {"type": "users", "count": len(users), "items": users}
        case {"status": "success", "data": {"user": dict(user)}}:
            return {"type": "single_user", "item": user}
        case {"status": "error", "message": str(msg), "code": int(code)}:
            return {"type": "error", "message": msg, "code": code}
        case {"status": "error", **rest}:
            return {"type": "error", "details": rest}
        case _:
            return {"type": "unknown", "raw": response}

# ========== 实际应用：表达式求值 ==========
@dataclass
class Num:
    value: int

@dataclass
class Add:
    left: Any
    right: Any

@dataclass
class Mul:
    left: Any
    right: Any

def evaluate(expr: Any) -> int:
    match expr:
        case Num(value):
            return value
        case Add(left, right):
            return evaluate(left) + evaluate(right)
        case Mul(left, right):
            return evaluate(left) * evaluate(right)
        case _:
            raise ValueError(f"未知表达式: {expr}")

# 使用
expr = Mul(Add(Num(1), Num(2)), Num(3))  # (1 + 2) * 3
print(evaluate(expr))  # 9
```

#### 1.2.4 反例代码

```python
from dataclasses import dataclass

# ========== 反例1：变量名与常量混淆 ==========
RED = "red"
BLUE = "blue"

def wrong_match(color: str) -> str:
    match color:
        case RED:  # 错误：这会将color绑定到RED变量，而非比较
            return "红色"
        case BLUE:  # 同样的问题
            return "蓝色"
        case _:
            return "其他"

# 正确做法：使用枚举或字面量
def correct_match(color: str) -> str:
    match color:
        case "red":  # 使用字面量
            return "红色"
        case "blue":
            return "蓝色"
        case _:
            return "其他"

# ========== 反例2：模式覆盖顺序错误 ==========
def wrong_order(value: int) -> str:
    match value:
        case _:  # 通配符放在前面！
            return "其他"
        case 0:  # 这些永远不会匹配
            return "零"
        case n if n > 0:  # 永远不会执行
            return f"正数: {n}"

# 正确顺序
def correct_order(value: int) -> str:
    match value:
        case 0:
            return "零"
        case n if n > 0:
            return f"正数: {n}"
        case _:  # 通配符最后
            return "其他"

# ========== 反例3：守卫子句中的绑定变量问题 ==========
@dataclass
class Item:
    name: str
    price: float

def wrong_guard(items: list[Item]) -> None:
    match items:
        case [Item(name, price)] if price > 100:  # name可能未定义！
            print(f"昂贵物品: {name}")
        # 如果price <= 100，name不会被绑定，但守卫仍尝试访问

# 正确做法：确保守卫中只使用已绑定的变量
def correct_guard(items: list[Item]) -> None:
    match items:
        case [item] if item.price > 100:
            print(f"昂贵物品: {item.name}")

# ========== 反例4：可变对象的误用 ==========
def mutable_pattern(data: list) -> None:
    match data:
        case [[1, 2], [3, 4]]:  # 这创建的是元组模式，不是列表模式！
            print("匹配")

# 序列模式使用方括号或圆括号，但匹配的是序列结构
# 要匹配列表字面量，需要使用类模式

# ========== 反例5：绑定变量的作用域问题 ==========
def scope_issue():
    x = 1
    match 2:
        case x:  # 这会重新绑定x！
            print(f"匹配: {x}")  # 输出: 2
    print(f"x现在是: {x}")  # 输出: 2，不是1！

# 正确做法：使用不同名称
def scope_correct():
    x = 1
    match 2:
        case matched:  # 使用不同名称
            print(f"匹配: {matched}")
    print(f"x仍然是: {x}")  # 输出: 1
```

#### 1.2.5 与if-elif的形式论证

**定理1.3（模式匹配的表达能力）**
> 对于任意模式匹配语句，存在等价的if-elif链；反之，某些数据结构处理任务，模式匹配的代码复杂度为O(1)，而if-elif链为O(n)。

**证明（正向）：**

```python
# 模式匹配
match value:
    case A(): result = "A"
    case B(): result = "B"
    case _: result = "other"

# 等价if-elif
if isinstance(value, A):
    result = "A"
elif isinstance(value, B):
    result = "B"
else:
    result = "other"
```

**证明（反向 - 复杂性差异）：**

```python
# 嵌套JSON处理 - 模式匹配
match response:
    case {"data": {"users": [{"name": name}]}}:
        return name

# 等价的if-elif - 复杂且易错
if isinstance(response, dict) and "data" in response:
    data = response["data"]
    if isinstance(data, dict) and "users" in data:
        users = data["users"]
        if isinstance(users, list) and len(users) > 0:
            first = users[0]
            if isinstance(first, dict) and "name" in first:
                return first["name"]
```

**结论：** 模式匹配在处理复杂数据结构时显著降低认知复杂度 ∎

---

### 1.3 海象运算符（Walrus Operator :=）

#### 1.3.1 概念定义

**海象运算符（Walrus Operator）** 是Python 3.8引入的赋值表达式运算符，符号为 `:=`。它允许在表达式内部进行赋值，将赋值和求值合并为单一操作。

**形式化定义：**

- 语法形式：`name := expression`
- 语义：计算 `expression` 的值，将其赋给 `name`，并返回该值
- 与常规赋值 `name = expression` 的区别：海象运算符是表达式，可出现在任何表达式位置

#### 1.3.2 语法形式（BNF）

```bnf
named_expression ::= identifier ":=" expression
                   | expression
```

#### 1.3.3 属性关系

| 特性 | `=` 赋值 | `:=` 海象运算符 |
|-----|---------|---------------|
| 语法类别 | 语句 | 表达式 |
| 返回值 | 无 | 被赋的值 |
| 使用位置 | 语句级别 | 任何表达式位置 |
| 优先级 | N/A | 最低（类似逗号） |
| 作用域 | 当前作用域 | 当前作用域 |

#### 1.3.4 正例代码

```python
import re
from typing import Iterator

# ========== 场景1：while循环中的条件检查 ==========
def read_file_lines(filename: str) -> Iterator[str]:
    """读取文件，使用海象运算符简化循环"""
    with open(filename, 'r') as f:
        while (line := f.readline()):  # 读取并检查
            yield line.strip()

# 对比：传统写法
# line = f.readline()
# while line:
#     yield line.strip()
#     line = f.readline()

# ========== 场景2：正则表达式匹配 ==========
def extract_emails(text: str) -> list[str]:
    """从文本中提取所有邮箱"""
    pattern = re.compile(r'\b[\w.-]+@[\w.-]+\.\w+\b')
    emails = []
    pos = 0
    while (match := pattern.search(text, pos)):
        emails.append(match.group())
        pos = match.end()
    return emails

# ========== 场景3：列表推导中的过滤 ==========
def process_data(data: list[str]) -> list[tuple[str, int]]:
    """处理数据，只保留能转换为整数的项"""
    return [(item, length) for item in data
            if (length := len(item.strip())) > 0]

# 更复杂的例子：嵌套海象运算符
def analyze_numbers(numbers: list[str]) -> dict[str, list[int]]:
    """分析数字列表，分类正数、负数、零"""
    result = {"positive": [], "negative": [], "zero": []}
    for s in numbers:
        if (n := int(s)) > 0:
            result["positive"].append(n)
        elif n < 0:
            result["negative"].append(n)
        else:
            result["zero"].append(n)
    return result

# ========== 场景4：字典get的优化 ==========
def count_words(text: str) -> dict[str, int]:
    """统计词频"""
    counts = {}
    for word in text.lower().split():
        counts[word] = (count := counts.get(word, 0)) + 1
    return counts

# 更清晰的写法
def count_words_clear(text: str) -> dict[str, int]:
    """统计词频（清晰版本）"""
    counts = {}
    for word in text.lower().split():
        if (count := counts.get(word)) is None:
            counts[word] = 1
        else:
            counts[word] = count + 1
    return counts

# ========== 场景5：避免重复计算 ==========
def expensive_computation(x: int) -> int:
    """模拟昂贵计算"""
    print(f"计算 {x}...")
    return x * x

def process_with_cache(values: list[int]) -> list[int]:
    """处理值，避免重复计算"""
    results = []
    for v in values:
        if (result := expensive_computation(v)) > 10:
            results.append(result)
        elif result > 5:  # 复用result
            results.append(result // 2)
    return results

# ========== 场景6：与any/all结合 ==========
def has_valid_item(items: list[str]) -> bool:
    """检查是否有有效项"""
    return any((length := len(item)) > 5 for item in items)

# ========== 场景7：多条件检查 ==========
def check_value(value: int) -> str:
    """多条件检查"""
    if (squared := value ** 2) > 100 and (cubed := value ** 3) < 1000:
        return f"平方={squared}, 立方={cubed}"
    return "不满足条件"

# ========== 场景8：数据验证管道 ==========
def validate_data(data: dict) -> list[str]:
    """验证数据，返回错误列表"""
    errors = []

    if not (name := data.get("name")):
        errors.append("缺少name字段")
    elif len(name) < 3:
        errors.append(f"name太短: {name}")

    if (age := data.get("age")) is None:
        errors.append("缺少age字段")
    elif not isinstance(age, int):
        errors.append(f"age类型错误: {type(age)}")
    elif age < 0 or age > 150:
        errors.append(f"age范围错误: {age}")

    return errors
```

#### 1.3.5 反例代码

```python
# ========== 反例1：不必要的使用 ==========
def unnecessary_walrus(x: int) -> int:
    # 错误：简单的赋值不需要海象运算符
    if (y := x + 1) > 0:
        return y

    # 正确：直接返回
    y = x + 1
    if y > 0:
        return y

# ========== 反例2：降低可读性 ==========
def confusing_code(data: list) -> list:
    # 错误：过度使用海象运算符使代码难以理解
    return [y for x in data if (y := f(x)) if (z := g(y)) if z > 0]

    # 正确：分解为多个步骤
    result = []
    for x in data:
        y = f(x)
        z = g(y)
        if z > 0:
            result.append(y)
    return result

def f(x): return x * 2
def g(x): return x - 1

# ========== 反例3：作用域问题 ==========
def scope_problem():
    x = 1
    # 错误：海象运算符在列表推导中创建变量
    [y := x + i for i in range(3)]
    print(y)  # y = 3 (列表推导的最后一次迭代)

    # 正确：使用普通循环
    y = None
    for i in range(3):
        y = x + i
    print(y)

# ========== 反例4：语法错误 ==========
def syntax_errors():
    # 错误：不能单独作为语句
    # x := 1  # SyntaxError

    # 错误：不能用于赋值目标
    # (x := 1) = 2  # SyntaxError

    # 错误：不能在lambda中使用
    # f = lambda: (x := 1)  # SyntaxError

    # 错误：不能在f-string表达式字段中使用（Python 3.12之前）
    # f"{x := 1}"  # 在3.12之前是SyntaxError

    pass

# ========== 反例5：优先级问题 ==========
def precedence_issue():
    # 错误：优先级可能导致意外行为
    if (x := 1, 2):  # x = (1, 2)，不是 x = 1
        print(x)  # (1, 2)

    # 正确：使用括号明确意图
    if ((x := 1), 2):
        print(x)  # 1

# ========== 反例6：与None比较 ==========
def none_comparison():
    data = {"key": None}

    # 潜在问题：None是falsy值
    if value := data.get("key"):  # 当value为None时，不会进入if
        print(f"值: {value}")
    else:
        print("键不存在或为None")

    # 正确：显式检查None
    if (value := data.get("key")) is not None:
        print(f"值: {value}")
    else:
        print("键不存在或为None")
```

#### 1.3.6 形式论证

**定理1.4（海象运算符的完备性）**
> 设E为包含海象运算符的表达式，则存在等价的不含海象运算符的语句序列。

**证明：**

```python
# 海象运算符形式
if (x := expr) > 0:
    use(x)

# 等价形式
x = expr
if x > 0:
    use(x)
```

**定理1.5（海象运算符的简洁性）**
> 对于涉及重复子表达式的条件判断，海象运算符可将代码行数从O(n)减少到O(1)。

**证明：**

```python
# 不使用海象运算符 - 3行，重复表达式
match = re.search(pattern, text)
if match:
    process(match.group())

# 使用海象运算符 - 1行
if (match := re.search(pattern, text)):
    process(match.group())
```

---

### 1.4 f-string高级特性（Python 3.12+）

#### 1.4.1 概念定义

**f-string（格式化字符串字面量）** 是Python 3.6引入的字符串格式化机制，使用 `f"..."` 语法。Python 3.12对f-string进行了重大改进，允许嵌套f-string、更灵活的引号使用和调试格式。

**形式化定义：**

- 语法形式：`f"...{expression}..."`
- 表达式字段：`{expression}` 或 `{expression!conversion}` 或 `{expression:format_spec}`
- 调试格式：`{expression=}` 同时显示表达式和值

#### 1.4.2 语法形式（BNF）

```bnf
f_string ::= "f" string_prefix? "'" f_string_content* "'"
           | "f" string_prefix? '"' f_string_content* '"'
           | "f" string_prefix? "'''" f_string_content* "'''"
           | "f" string_prefix? '"""' f_string_content* '"""'
f_string_content ::= literal_text | replacement_field
replacement_field ::= "{" expression ["="] ["!" conversion] [":" format_spec] "}"
conversion ::= "s" | "r" | "a"
format_spec ::= 任意格式说明符
```

#### 1.4.3 Python 3.12+ 新特性

| 特性 | 描述 | 示例 |
|-----|------|------|
| 嵌套f-string | f-string内可包含f-string | `f"{f'{x}'}"` |
| 任意引号 | 表达式内可使用任意引号 | `f"{'it\'s'}"` |
| 多行表达式 | 表达式可跨多行 | `f"{x +\n y}"` |
| 调试格式 | `=` 显示表达式和值 | `f"{x=}"` |
| 重复括号 | 表达式内可使用任意括号 | `f"{(x)}"` |

#### 1.4.4 正例代码

```python
from datetime import datetime
from decimal import Decimal

# ========== 基本f-string ==========
name = "Alice"
age = 30
print(f"姓名: {name}, 年龄: {age}")

# ========== 调试格式（Python 3.8+）==========
x, y = 10, 20
print(f"{x=}")           # x=10
print(f"{x=}")           # x=10
print(f"{x = }")         # x = 10（带空格）
print(f"{x+y=}")         # x+y=30
print(f"{x**2=}")        # x**2=100

# ========== 格式说明符 ==========
pi = 3.14159265359

# 数值格式
print(f"{pi:.2f}")       # 3.14（2位小数）
print(f"{pi:10.2f}")     # "      3.14"（宽度10，右对齐）
print(f"{pi:<10.2f}")    # "3.14      "（左对齐）
print(f"{pi:^10.2f}")    # "   3.14   "（居中）
print(f"{pi:010.2f}")    # 0000003.14（前导零）

# 千位分隔符
large_number = 1234567890
print(f"{large_number:,}")      # 1,234,567,890
print(f"{large_number:_}")      # 1_234_567_890

# 科学计数法
print(f"{pi:.2e}")       # 3.14e+00

# 百分比
ratio = 0.8567
print(f"{ratio:.1%}")    # 85.7%

# ========== 进制转换 ==========
n = 255
print(f"{n:b}")          # 11111111（二进制）
print(f"{n:o}")          # 377（八进制）
print(f"{n:x}")          # ff（十六进制小写）
print(f"{n:X}")          # FF（十六进制大写）
print(f"{n:#x}")         # 0xff（带前缀）

# ========== 字符串格式 ==========
text = "hello"
print(f"{text:>10}")     # "     hello"（右对齐）
print(f"{text:<10}")     # "hello     "（左对齐）
print(f"{text:^10}")     # "  hello   "（居中）
print(f"{text:*^10}")    # "**hello***"（填充字符）
print(f"{text:.3}")      # "hel"（截断）

# ========== Python 3.12+ 嵌套f-string ==========
value = 42
# 嵌套表达式
print(f"{f'{value}'} is the answer")  # 42 is the answer

# 动态格式说明符
width = 10
precision = 2
print(f"{pi:{width}.{precision}f}")  # 动态宽度和精度

# 嵌套引号自由
print(f"It's {'great'}!")  # Python 3.12+ 允许
print(f'He said "{"hello"}"')  # 混合引号

# ========== 多行f-string ==========
user = "Alice"
score = 95
report = f"""
========== 成绩报告 ==========
学生: {user}
分数: {score}
等级: {
    'A' if score >= 90 else
    'B' if score >= 80 else
    'C' if score >= 70 else
    'D' if score >= 60 else 'F'
}
评价: {
    "优秀" if score >= 90 else
    "良好" if score >= 80 else
    "及格" if score >= 60 else "不及格"
}
=============================
"""
print(report)

# ========== 字典和对象访问 ==========
person = {"name": "Bob", "age": 25}
print(f"{person['name']} is {person['age']} years old")

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __format__(self, format_spec: str) -> str:
        if format_spec == "short":
            return f"({self.x:.1f}, {self.y:.1f})"
        return f"Point({self.x}, {self.y})"

p = Point(3.14159, 2.71828)
print(f"{p}")            # Point(3.14159, 2.71828)
print(f"{p:short}")      # (3.1, 2.7)

# ========== 日期时间格式 ==========
now = datetime.now()
print(f"当前时间: {now:%Y-%m-%d %H:%M:%S}")
print(f"日期: {now:%A, %B %d, %Y}")

# ========== 自定义格式 ==========
class Money:
    def __init__(self, amount: Decimal, currency: str):
        self.amount = amount
        self.currency = currency

    def __format__(self, format_spec: str) -> str:
        if format_spec == "short":
            return f"{self.currency}{self.amount:.0f}"
        return f"{self.currency}{self.amount:.2f}"

price = Money(Decimal("99.99"), "$")
print(f"价格: {price}")       # $99.99
print(f"价格: {price:short}") # $100

# ========== 调试输出技巧 ==========
def debug_variables(**kwargs):
    """调试输出多个变量"""
    for name, value in kwargs.items():
        print(f"{name} = {value!r}")  # !r 使用repr()

a, b, c = 1, "hello", [1, 2, 3]
debug_variables(a=a, b=b, c=c)
# a = 1
# b = 'hello'
# c = [1, 2, 3]

# ========== 表格格式化 ==========
data = [
    ("Alice", 25, "Engineer"),
    ("Bob", 30, "Designer"),
    ("Charlie", 35, "Manager"),
]

print(f"{'Name':<10} {'Age':>5} {'Role':<15}")
print("-" * 32)
for name, age, role in data:
    print(f"{name:<10} {age:>5} {role:<15}")
```

#### 1.4.5 反例代码

```python
# ========== 反例1：表达式副作用 ==========
counter = 0
def increment():
    global counter
    counter += 1
    return counter

# 危险：f-string中的表达式可能被多次求值（实现相关）
# result = f"{increment()}, {increment()}"  # 不确定的行为

# 正确：先计算再格式化
val1 = increment()
val2 = increment()
result = f"{val1}, {val2}"

# ========== 反例2：转义问题（Python 3.12之前）==========
# Python 3.11及之前，反斜杠在f-string中有特殊限制
# 错误：
# f"Newline: {\n}"  # SyntaxError

# 正确：使用原始字符串或表达式外计算
newline = "\n"
f"Newline: {newline}"

# ========== 反例3：过度复杂的表达式 ==========
data = {"a": 1, "b": 2}
# 错误：f-string中表达式过于复杂
# result = f"{[v for k, v in data.items() if k.startswith('a')]}"

# 正确：先计算
values = [v for k, v in data.items() if k.startswith('a')]
result = f"{values}"

# ========== 反例4：引号嵌套错误 ==========
# Python 3.11及之前
# 错误：
# f"{'it\'s'}"  # SyntaxError in 3.11-

# Python 3.12+ 支持
# f"{'it\'s'}"  # OK in 3.12+

# ========== 反例5：空表达式 ==========
# 错误：
# f"{}"  # SyntaxError

# 正确：必须有表达式
x = 1
f"{x}"

# ========== 反例6：格式说明符语法错误 ==========
# 错误：
# f"{x:}"  # 当x未定义时

# 正确：
x = 42
f"{x:}"

# ========== 反例7：递归f-string（Python 3.12之前）==========
# Python 3.11及之前
# 错误：
# f"{f'{x}'}"  # SyntaxError in 3.11-

# Python 3.12+ 支持
x = 42
f"{f'{x}'}"  # OK in 3.12+
```

#### 1.4.6 形式论证

**定理1.6（f-string的表达能力）**
> f-string的表达能力等价于 `str.format()` 方法，但具有更高的运行时效率。

**证明：**

```python
# f-string
name = "Alice"
f"Hello, {name}!"

# 等价的format调用
"Hello, {}!".format(name)

# 效率差异：f-string在编译时解析，format在运行时解析
```

**定理1.7（调试格式的唯一性）**
> `=` 调试格式是f-string独有的特性，无法通过其他字符串格式化方法直接实现。

**证明：**

```python
x = 10

# f-string调试格式
print(f"{x=}")  # x=10

# 等价但冗长的实现
print(f"x={x}")  # 需要重复变量名
```

---

### 1.5 解包操作（Unpacking）

#### 1.5.1 概念定义

**解包（Unpacking）** 是Python中将可迭代对象或映射对象解构为独立元素的操作。Python 3.0+ 扩展了解包能力，允许在更多上下文中使用，包括函数调用、赋值语句和推导式。

**形式化定义：**

- 序列解包：`*iterable` 将序列展开为位置参数或列表元素
- 字典解包：`**mapping` 将字典展开为关键字参数
- 嵌套解包：支持多级解构

#### 1.5.2 语法形式（BNF）

```bnf
starred_expression ::= "*" expression
starred_target     ::= "*" target

unpacking_assignment ::= target_list "=" expression_list
target_list          ::= target ("," target)* [","]
target               ::= identifier | "(" target_list ")" | "[" target_list "]" | starred_target

function_call        ::= name "(" [argument_list] ")"
argument_list        ::= positional_args ["," starred_arg] ["," keyword_args]
                      | starred_arg ["," keyword_args]
                      | keyword_args
starred_arg          ::= "*" expression
keyword_args         ::= keyword_item ("," keyword_item)* ["," starred_keyword]
starred_keyword      ::= "**" expression
```

#### 1.5.3 正例代码

```python
from typing import Any

# ========== 基本序列解包 ==========
# 元组解包
a, b, c = (1, 2, 3)
print(a, b, c)  # 1 2 3

# 列表解包
first, second, *rest = [1, 2, 3, 4, 5]
print(first, second, rest)  # 1 2 [3, 4, 5]

# 字符串解包
a, b, c = "abc"
print(a, b, c)  # a b c

# ========== 扩展解包（Python 3+）==========
# 开头解包
*beginning, last = [1, 2, 3, 4, 5]
print(beginning, last)  # [1, 2, 3, 4] 5

# 中间解包
first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)  # 1 [2, 3, 4] 5

# 多个星号（错误，只能有一个）
# first, *a, *b, last = [1, 2, 3, 4, 5]  # SyntaxError

# ========== 嵌套解包 ==========
data = (1, (2, 3), [4, 5, 6])
a, (b, c), d = data
print(a, b, c, d)  # 1 2 3 [4, 5, 6]

# 深层嵌套
nested = ((1, 2), (3, (4, 5)))
(a, b), (c, (d, e)) = nested
print(a, b, c, d, e)  # 1 2 3 4 5

# 混合嵌套和解包
data = [1, [2, 3, 4], 5]
first, [second, *middle], last = data
print(first, second, middle, last)  # 1 2 [3, 4] 5

# ========== 字典解包 ==========
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# 使用字典作为关键字参数
params = {"name": "Alice", "greeting": "Hi"}
print(greet(**params))  # Hi, Alice!

# 合并字典
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
merged = {**dict1, **dict2}  # 后面的覆盖前面的
print(merged)  # {'a': 1, 'b': 3, 'c': 4}

# 创建新字典时解包
base = {"x": 10, "y": 20}
extended = {**base, "z": 30, "x": 100}  # x被覆盖
print(extended)  # {'x': 100, 'y': 20, 'z': 30}

# ========== 函数调用解包 ==========
def func(a: int, b: int, c: int, d: int = 0) -> int:
    return a + b + c + d

# 位置解包
args = [1, 2, 3]
print(func(*args))  # 6

# 关键字解包
kwargs = {"a": 1, "b": 2, "c": 3, "d": 4}
print(func(**kwargs))  # 10

# 混合解包
print(func(*[1, 2], **{"c": 3, "d": 4}))  # 10
print(func(1, *[2, 3], d=4))  # 10

# ========== 列表/元组构造中的解包 ==========
# 合并列表
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2]
print(combined)  # [1, 2, 3, 4, 5, 6]

# 合并元组
tuple1 = (1, 2)
tuple2 = (3, 4)
combined_tuple = (*tuple1, *tuple2)
print(combined_tuple)  # (1, 2, 3, 4)

# 混合构造
mixed = [0, *list1, 10, *list2, 100]
print(mixed)  # [0, 1, 2, 3, 10, 4, 5, 6, 100]

# ========== 集合解包 ==========
set1 = {1, 2, 3}
set2 = {3, 4, 5}
combined_set = {*set1, *set2}
print(combined_set)  # {1, 2, 3, 4, 5}

# ========== 忽略值解包 ==========
data = (1, 2, 3, 4, 5)
first, _, third, _, fifth = data
print(first, third, fifth)  # 1 3 5

# 使用*_忽略多个值
first, *_, last = data
print(first, last)  # 1 5

# ========== for循环解包 ==========
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
for num, char in pairs:
    print(f"{num}: {char}")

# 嵌套循环解包
matrix = [[(i, j) for j in range(3)] for i in range(3)]
for row in matrix:
    for (i, j) in row:
        print(f"({i}, {j})", end=" ")
    print()

# enumerate解包
for index, (key, value) in enumerate({"a": 1, "b": 2}.items()):
    print(f"{index}: {key} = {value}")

# ========== 生成器表达式解包 ==========
# 解包生成器到列表
numbers = range(5)
result = [*numbers]
print(result)  # [0, 1, 2, 3, 4]

# 解包到集合
unique = {*"hello"}
print(unique)  # {'h', 'e', 'l', 'o'}

# ========== 实际应用：函数参数转发 ==========
def wrapper(*args: Any, **kwargs: Any) -> Any:
    """通用包装器，转发所有参数"""
    print(f"位置参数: {args}")
    print(f"关键字参数: {kwargs}")
    return args, kwargs

def logged_func(func):
    """日志装饰器"""
    def inner(*args, **kwargs):
        print(f"调用 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 返回 {result}")
        return result
    return inner

@logged_func
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)

# ========== 实际应用：配置合并 ==========
def merge_configs(*configs: dict) -> dict:
    """合并多个配置字典"""
    result = {}
    for config in configs:
        result = {**result, **config}
    return result

base = {"debug": False, "timeout": 30}
override = {"debug": True}
final = merge_configs(base, override)
print(final)  # {'debug': True, 'timeout': 30}
```

#### 1.5.4 反例代码

```python
# ========== 反例1：星号位置错误 ==========
# 错误：星号不能在赋值左侧单独使用
# * = [1, 2, 3]  # SyntaxError

# 错误：星号不能在表达式中单独使用
# x = *[1, 2, 3]  # SyntaxError

# 正确：星号必须在可迭代对象前
x = [*[1, 2, 3]]  # [1, 2, 3]

# ========== 反例2：多个星号解包 ==========
data = [1, 2, 3, 4, 5]
# 错误：只能有一个星号解包
# first, *a, *b, last = data  # SyntaxError

# 正确：只有一个星号
first, *middle, last = data

# ========== 反例3：解包到不可迭代目标 ==========
# 错误：不能解包到单个变量
# a = *[1, 2, 3]  # SyntaxError

# 正确：需要可迭代目标
a, b, c = [1, 2, 3]

# ========== 反例4：长度不匹配 ==========
# 错误：元素数量不匹配
data = [1, 2, 3]
# a, b = data  # ValueError: too many values to unpack
# a, b, c, d = data  # ValueError: not enough values to unpack

# 正确：使用星号捕获多余元素
a, *rest = data  # a=1, rest=[2, 3]

# ========== 反例5：字典解包到非字典 ==========
# 错误：不能对非映射对象使用**
def func(a, b):
    pass

# func(**[1, 2])  # TypeError: 'list' object is not a mapping

# 正确：只能解包映射类型
func(**{"a": 1, "b": 2})

# ========== 反例6：关键字参数重复 ==========
# 错误：关键字参数重复
# func(a=1, **{"a": 2})  # TypeError: func() got multiple values for argument 'a'

# 正确：避免重复
func(**{"a": 1, "b": 2})

# ========== 反例7：集合解包顺序问题 ==========
# 集合是无序的，解包顺序不确定
s = {3, 1, 4, 1, 5}
a, *rest = s
# a的值不确定，可能是3、1、4或5

# ========== 反例8：生成器多次解包 ==========
def gen():
    yield 1
    yield 2

g = gen()
a, b = g  # 第一次解包，消耗生成器
c, d = g  # ValueError: not enough values to unpack

# 正确：先转换为列表
g_list = list(gen())
a, b = g_list
c, d = g_list  # OK
```

#### 1.5.5 形式论证

**定理1.8（解包的完备性）**
> 对于任意可迭代对象 `iter`，存在唯一的解包方式将其元素分配给目标变量。

**证明：**

```python
# 设 iter = [e1, e2, ..., en]
# 解包 a, *b, c = iter
# 则 a = e1, b = [e2, ..., e_{n-1}], c = en
# 当 n < 2 时，b = []
```

**定理1.9（字典解包的优先级）**
> 多个字典解包时，后解包的字典键值覆盖先解包的字典键值。

**证明：**

```python
{**{"a": 1}, **{"a": 2}}  # {"a": 2}
# 因为 {"a": 1} 先展开，{"a": 2} 后展开并覆盖 "a"
```

---

## 第二部分：数据模型与特殊方法

### 2.1 __slots__机制

#### 2.1.1 概念定义

**`__slots__`** 是Python类的一个类属性，用于显式声明实例可以拥有的属性。使用 `__slots__` 的类不会为每个实例创建 `__dict__`，从而节省内存并加快属性访问速度。

**形式化定义：**

- `__slots__` 是一个字符串序列或可迭代对象，定义允许的实例属性名
- 使用 `__slots__` 的实例：无 `__dict__`（除非在 `__slots__` 中包含 `'__dict__'`）
- 使用 `__slots__` 的实例：无 `__weakref__`（除非在 `__slots__` 中包含 `'__weakref__'`）

#### 2.1.2 语法形式

```python
class ClassName:
    __slots__ = ('attr1', 'attr2', ...)  # 元组形式
    # 或
    __slots__ = ['attr1', 'attr2', ...]  # 列表形式
```

#### 2.1.3 属性关系

| 特性 | 普通类 | `__slots__`类 |
|-----|-------|--------------|
| `__dict__` | 有 | 无（默认） |
| `__weakref__` | 有 | 无（默认） |
| 内存占用 | 大 | 小（约40-50%节省） |
| 属性访问速度 | 较慢 | 较快 |
| 动态添加属性 | 可以 | 不可以（除非有`__dict__`） |

#### 2.1.4 正例代码

```python
from typing import Any
import sys

# ========== 基本__slots__使用 ==========
class Point:
    """使用__slots__的点类"""
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

p = Point(1.0, 2.0)
print(p)  # Point(1.0, 2.0)
print(p.x, p.y)  # 1.0 2.0

# 检查内存差异
print(hasattr(p, '__dict__'))  # False

# ========== 内存对比 ==========
class RegularPoint:
    """普通点类"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class SlottedPoint:
    """使用__slots__的点类"""
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# 内存对比
regular = RegularPoint(1.0, 2.0)
slotted = SlottedPoint(1.0, 2.0)

print(f"Regular size: {sys.getsizeof(regular)} bytes")
print(f"Slotted size: {sys.getsizeof(slotted)} bytes")
# 通常slotted节省约40-50%内存

# ========== 继承中的__slots__ ==========
class Base:
    """基类使用__slots__"""
    __slots__ = ('a',)

    def __init__(self, a: int):
        self.a = a

class Derived(Base):
    """派生类添加更多slots"""
    __slots__ = ('b', 'c')  # 不重复父类的slots

    def __init__(self, a: int, b: int, c: int):
        super().__init__(a)
        self.b = b
        self.c = c

d = Derived(1, 2, 3)
print(d.a, d.b, d.c)  # 1 2 3

# ========== 保留__dict__ ==========
class Flexible:
    """保留__dict__以支持动态属性"""
    __slots__ = ('fixed_attr', '__dict__')

    def __init__(self):
        self.fixed_attr = "fixed"

f = Flexible()
f.dynamic_attr = "dynamic"  # 可以动态添加属性
print(f.fixed_attr)  # fixed
print(f.dynamic_attr)  # dynamic
print(f.__dict__)  # {'dynamic_attr': 'dynamic'}

# ========== 保留__weakref__ ==========
import weakref

class WeakRefSupport:
    """支持弱引用"""
    __slots__ = ('data', '__weakref__')

    def __init__(self, data: Any):
        self.data = data

obj = WeakRefSupport("test")
ref = weakref.ref(obj)
print(ref())  # <__main__.WeakRefSupport object>

# ========== 类变量与实例变量 ==========
class Config:
    """配置类：类变量 + slots实例变量"""
    DEFAULT_TIMEOUT = 30  # 类变量
    __slots__ = ('timeout', 'retries')

    def __init__(self, timeout: int = None, retries: int = 3):
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.retries = retries

c = Config()
print(c.timeout)  # 30
print(Config.DEFAULT_TIMEOUT)  # 30

# ========== 属性访问优化 ==========
class FastAccess:
    """优化属性访问"""
    __slots__ = ('_value',)

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, v: int) -> None:
        if v < 0:
            raise ValueError("Value must be non-negative")
        self._value = v

f = FastAccess(10)
print(f.value)  # 10
f.value = 20
print(f.value)  # 20
# f.value = -1  # ValueError

# ========== 大量实例的场景 ==========
class DataRecord:
    """数据记录类 - 适合大量实例"""
    __slots__ = ('id', 'name', 'value', 'timestamp')

    def __init__(self, id: int, name: str, value: float, timestamp: str):
        self.id = id
        self.name = name
        self.value = value
        self.timestamp = timestamp

# 创建大量实例
records = [DataRecord(i, f"item_{i}", i * 1.5, "2024-01-01") for i in range(10000)]
print(f"Created {len(records)} records")
```

#### 2.1.5 反例代码

```python
# ========== 反例1：尝试添加未声明的属性 ==========
class Strict:
    __slots__ = ('x',)

    def __init__(self):
        self.x = 1

s = Strict()
# s.y = 2  # AttributeError: 'Strict' object has no attribute 'y'

# ========== 反例2：__slots__不是序列 ==========
# 错误：__slots__必须是字符串序列
# class Bad:
#     __slots__ = 123  # TypeError

# ========== 反例3：重复声明slots ==========
class Base:
    __slots__ = ('a',)

# 错误：派生类不应重复父类的slots
class BadDerived(Base):
    __slots__ = ('a', 'b')  # 'a'已在父类中声明
    # 这不是语法错误，但会造成混淆

# 正确做法
class GoodDerived(Base):
    __slots__ = ('b',)  # 只添加新slots

# ========== 反例4：多重继承中的slots冲突 ==========
class A:
    __slots__ = ('x',)

class B:
    __slots__ = ('x',)  # 相同的slot名

# 错误：多重继承时slots冲突
# class C(A, B):  # 可能有问题
#     pass

# 解决方案：避免冲突或使用空slots
class C(A, B):
    __slots__ = ()  # 空slots，继承父类的

# ========== 反例5：忘记调用父类__init__ ==========
class Parent:
    __slots__ = ('a',)

    def __init__(self, a: int):
        self.a = a

class Child(Parent):
    __slots__ = ('b',)

    def __init__(self, a: int, b: int):
        # 错误：忘记调用super().__init__(a)
        self.b = b  # 这可以
        # 但self.a未初始化

c = Child(1, 2)
# print(c.a)  # AttributeError

# 正确做法
class GoodChild(Parent):
    __slots__ = ('b',)

    def __init__(self, a: int, b: int):
        super().__init__(a)
        self.b = b

# ========== 反例6：pickle问题 ==========
import pickle

class PickleTest:
    __slots__ = ('data',)

    def __init__(self, data: str):
        self.data = data

pt = PickleTest("test")
# pickled = pickle.dumps(pt)
# unpickled = pickle.loads(pickled)  # 可能需要__getstate__/__setstate__

# 正确做法：实现pickle支持
class PickleSafe:
    __slots__ = ('data',)

    def __init__(self, data: str):
        self.data = data

    def __getstate__(self):
        return {'data': self.data}

    def __setstate__(self, state):
        self.data = state['data']

# ========== 反例7：文档字符串和注解位置 ==========
class WrongOrder:
    """文档字符串"""
    x: int  # 类型注解
    __slots__ = ('x',)  # 应该在文档字符串之后，但在类型注解之前

    def __init__(self):
        self.x = 1

# 正确顺序
class RightOrder:
    """文档字符串"""
    __slots__ = ('x',)

    def __init__(self, x: int):
        self.x = x
```

#### 2.1.6 形式论证

**定理2.1（内存节省）**
> 使用 `__slots__` 的类实例比不使用 `__slots__` 的实例节省约40-50%内存。

**证明：**

- 普通实例：`__dict__` 是哈希表，有额外开销
- Slotted实例：属性存储在固定偏移的C数组中
- 每个 `__dict__` 约占用 72+ 字节（64位系统）
- Slotted实例无 `__dict__` 开销 ∎

**定理2.2（属性访问速度）**
> Slotted实例的属性访问速度比普通实例快。

**证明：**

- 普通实例：通过 `__dict__` 哈希查找
- Slotted实例：直接数组索引访问
- 时间复杂度：O(1)哈希 vs O(1)数组索引，但后者常数更小 ∎

---

### 2.2 描述符协议（**get**, **set**, **delete**）

#### 2.2.1 概念定义

**描述符（Descriptor）** 是实现描述符协议的类，该协议包含 `__get__`、`__set__` 和 `__delete__` 方法。描述符用于自定义属性访问行为，是Python属性系统的基础机制。

**形式化定义：**

- 描述符类：实现 `__get__(self, obj, type=None)` 的类
- 数据描述符：同时实现 `__set__` 或 `__delete__` 的描述符
- 非数据描述符：仅实现 `__get__` 的描述符
- 优先级：数据描述符 > 实例属性 > 非数据描述符

#### 2.2.2 语法形式

```python
class Descriptor:
    def __get__(self, obj: Any, objtype: type = None) -> Any:
        """获取属性值"""
        ...

    def __set__(self, obj: Any, value: Any) -> None:
        """设置属性值"""
        ...

    def __delete__(self, obj: Any) -> None:
        """删除属性"""
        ...
```

#### 2.2.3 属性关系

```
属性查找顺序（MRO）：
1. 数据描述符（在类中定义）
2. 实例的 __dict__
3. 非数据描述符（在类中定义）
4. 类的 __dict__
5. 父类的数据描述符
6. 父类的非数据描述符
```

#### 2.2.4 正例代码

```python
from typing import Any, Callable, Optional
import weakref

# ========== 基本描述符 ==========
class TypedAttribute:
    """类型检查描述符"""

    def __init__(self, name: str, expected_type: type):
        self.name = name
        self.expected_type = expected_type
        self.private_name = f"_{name}"

    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Expected {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(obj, self.private_name, value)

    def __delete__(self, obj: Any) -> None:
        raise AttributeError(f"Cannot delete attribute {self.name}")

class Person:
    name = TypedAttribute("name", str)
    age = TypedAttribute("age", int)

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(p.name)  # Alice
p.age = 31
print(p.age)  # 31
# p.age = "thirty"  # TypeError

# ========== 验证描述符 ==========
class Validated:
    """带验证的描述符"""

    def __init__(
        self,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.values = weakref.WeakKeyDictionary()

    def __set_name__(self, owner: type, name: str) -> None:
        """Python 3.6+ 自动设置名称"""
        self.name = name

    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self
        return self.values.get(obj)

    def __set__(self, obj: Any, value: int) -> None:
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be <= {self.max_value}")
        self.values[obj] = value

class Product:
    price = Validated(min_value=0)
    quantity = Validated(min_value=0, max_value=1000)

    def __init__(self, price: int, quantity: int):
        self.price = price
        self.quantity = quantity

product = Product(100, 50)
print(product.price)  # 100
# product.price = -10  # ValueError

# ========== 懒加载描述符 ==========
class LazyProperty:
    """懒加载属性描述符"""

    def __init__(self, func: Callable):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self
        # 计算并缓存值
        value = self.func(obj)
        setattr(obj, self.name, value)  # 变为实例属性
        return value

class DataProcessor:
    def __init__(self, data: list):
        self.data = data

    @LazyProperty
    def expensive_computation(self) -> int:
        """昂贵计算 - 只执行一次"""
        print("Computing...")
        return sum(x ** 2 for x in self.data)

dp = DataProcessor([1, 2, 3, 4, 5])
print(dp.expensive_computation)  # Computing... 55
print(dp.expensive_computation)  # 55（已缓存）

# ========== 方法绑定描述符 ==========
class MethodType:
    """模拟方法绑定"""

    def __init__(self, func: Callable):
        self.func = func

    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self.func
        # 返回绑定方法
        return lambda *args, **kwargs: self.func(obj, *args, **kwargs)

class MyClass:
    def method(self, x: int) -> int:
        return x * 2

    # 使用自定义描述符
    custom_method = MethodType(lambda self, x: x ** 2)

obj = MyClass()
print(obj.method(5))  # 10
print(obj.custom_method(5))  # 25

# ========== 缓存描述符 ==========
class CachedProperty:
    """带过期时间的缓存属性"""

    def __init__(self, ttl: float = 60.0):
        self.ttl = ttl
        self.cache = weakref.WeakKeyDictionary()
        self.timestamps = weakref.WeakKeyDictionary()

    def __call__(self, func: Callable) -> "CachedProperty":
        self.func = func
        self.name = func.__name__
        return self

    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self

        import time
        now = time.time()

        # 检查缓存是否有效
        if obj in self.cache:
            if now - self.timestamps[obj] < self.ttl:
                return self.cache[obj]

        # 重新计算
        value = self.func(obj)
        self.cache[obj] = value
        self.timestamps[obj] = now
        return value

class APIClient:
    def __init__(self):
        self.call_count = 0

    @CachedProperty(ttl=5.0)
    def data(self) -> dict:
        """模拟API调用"""
        self.call_count += 1
        print(f"API call #{self.call_count}")
        return {"users": 100, "posts": 500}

client = APIClient()
print(client.data)  # API call #1
print(client.data)  # 使用缓存

# ========== 只读描述符 ==========
class ReadOnly:
    """只读属性描述符"""

    def __init__(self, func: Callable):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self
        return self.func(obj)

    def __set__(self, obj: Any, value: Any) -> None:
        raise AttributeError(f"Cannot set attribute {self.name}")

class Immutable:
    def __init__(self, value: int):
        self._value = value

    @ReadOnly
    def value(self) -> int:
        return self._value

im = Immutable(42)
print(im.value)  # 42
# im.value = 100  # AttributeError
```

#### 2.2.5 反例代码

```python
# ========== 反例1：描述符定义在实例上 ==========
class Wrong:
    def __init__(self):
        # 错误：描述符必须定义在类上，不能在实例上
        self.descriptor = SomeDescriptor()

# ========== 反例2：忘记self参数 ==========
class BadDescriptor:
    def __get__(obj, objtype=None):  # 错误：缺少self
        return obj

# 正确
class GoodDescriptor:
    def __get__(self, obj, objtype=None):
        return obj

# ========== 反例3：__set_name__在3.6之前 ==========
# Python 3.6+ 支持 __set_name__
# 在3.6之前需要手动设置名称

class CompatibleDescriptor:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        """3.6+ 自动调用"""
        self.name = name

# ========== 反例4：数据描述符与非数据描述符混淆 ==========
class DataDescriptor:
    """数据描述符（有__set__）"""
    def __get__(self, obj, objtype=None):
        return "data descriptor"

    def __set__(self, obj, value):
        pass

class NonDataDescriptor:
    """非数据描述符（只有__get__）"""
    def __get__(self, obj, objtype=None):
        return "non-data descriptor"

class Test:
    data = DataDescriptor()
    non_data = NonDataDescriptor()

t = Test()
t.__dict__['data'] = 'instance'
t.__dict__['non_data'] = 'instance'

print(t.data)  # "data descriptor"（数据描述符优先）
print(t.non_data)  # "instance"（实例属性优先于非数据描述符）

# ========== 反例5：循环引用问题 ==========
class LeakyDescriptor:
    """可能导致内存泄漏的描述符"""

    def __init__(self):
        self.values = {}  # 直接引用实例

    def __get__(self, obj, objtype=None):
        return self.values.get(obj)

    def __set__(self, obj, value):
        self.values[obj] = value  # 强引用，实例不会被垃圾回收

# 正确做法：使用WeakKeyDictionary
import weakref

class SafeDescriptor:
    def __init__(self):
        self.values = weakref.WeakKeyDictionary()

    def __set__(self, obj, value):
        self.values[obj] = value

# ========== 反例6：描述符与property混淆 ==========
class Confused:
    """混淆描述符和property"""

    # property是描述符的一种
    @property
    def prop(self):
        return self._value

    # 自定义描述符
    class CustomDesc:
        def __get__(self, obj, objtype=None):
            return obj._other

    custom = CustomDesc()

# 两者都可以工作，但property更简洁
```

#### 2.2.6 形式论证

**定理2.2（描述符优先级）**
> 设C为类，x为C的实例，a为属性名，则属性查找顺序为：
>
> 1. 如果 `C.__dict__['a']` 是数据描述符 → 使用描述符
> 2. 如果 `'a' in x.__dict__` → 使用实例属性
> 3. 如果 `C.__dict__['a']` 是非数据描述符 → 使用描述符
> 4. 否则使用 `C.__dict__['a']`

**证明：** 由Python属性查找算法定义 ∎

---

### 2.3 属性装饰器（@property）

#### 2.3.1 概念定义

**`@property`** 是Python内置的装饰器，用于将方法转换为属性访问。它是描述符协议的便捷封装，实现getter、setter和deleter功能。

**形式化定义：**

- `@property`：将方法转换为只读属性
- `@name.setter`：定义属性设置器
- `@name.deleter`：定义属性删除器

#### 2.3.2 语法形式

```python
class ClassName:
    @property
    def name(self) -> T:
        """Getter"""
        return self._name

    @name.setter
    def name(self, value: T) -> None:
        """Setter"""
        self._name = value

    @name.deleter
    def name(self) -> None:
        """Deleter"""
        del self._name
```

#### 2.3.3 正例代码

```python
from typing import Optional
import re

# ========== 基本property ==========
class Temperature:
    """温度类 - 摄氏度与华氏度转换"""

    def __init__(self, celsius: float = 0):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """获取摄氏度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """设置摄氏度"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """获取华氏度（计算属性）"""
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """设置华氏度"""
        self.celsius = (value - 32) * 5/9

# 使用
temp = Temperature(25)
print(f"{temp.celsius}°C = {temp.fahrenheit}°F")
temp.fahrenheit = 98.6
print(f"{temp.celsius}°C = {temp.fahrenheit}°F")

# ========== 只读property ==========
class Circle:
    """圆类 - 只读属性"""

    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def area(self) -> float:
        """只读：面积"""
        import math
        return math.pi * self._radius ** 2

    @property
    def circumference(self) -> float:
        """只读：周长"""
        import math
        return 2 * math.pi * self._radius

circle = Circle(5)
print(f"Area: {circle.area:.2f}")
# circle.area = 100  # AttributeError: can't set attribute

# ========== 验证property ==========
class Email:
    """邮箱类 - 带验证"""

    EMAIL_PATTERN = re.compile(r'^[\w.-]+@[\w.-]+\.\w+$')

    def __init__(self, address: str):
        self._address = None
        self.address = address  # 使用setter验证

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not self.EMAIL_PATTERN.match(value):
            raise ValueError(f"Invalid email format: {value}")
        self._address = value.lower()

    @address.deleter
    def address(self) -> None:
        print("Email deleted")
        self._address = None

email = Email("User@Example.COM")
print(email.address)  # user@example.com
# email.address = "invalid"  # ValueError

# ========== 延迟计算property ==========
class Matrix:
    """矩阵类 - 延迟计算属性"""

    def __init__(self, data: list[list[float]]):
        self._data = data
        self._determinant: Optional[float] = None

    @property
    def data(self) -> list[list[float]]:
        return self._data

    @property
    def determinant(self) -> float:
        """延迟计算行列式"""
        if self._determinant is None:
            print("Computing determinant...")
            self._determinant = self._compute_determinant()
        return self._determinant

    def _compute_determinant(self) -> float:
        """计算行列式（简化版）"""
        if len(self._data) == 2:
            return (self._data[0][0] * self._data[1][1] -
                   self._data[0][1] * self._data[1][0])
        return 0.0  # 简化处理

m = Matrix([[1, 2], [3, 4]])
print(m.determinant)  # Computing determinant... -2
print(m.determinant)  # -2（已缓存）

# ========== property工厂函数 ==========
def validated_property(name: str, validator: callable):
    """创建带验证的property"""
    private_name = f"_{name}"

    def getter(self):
        return getattr(self, private_name)

    def setter(self, value):
        validated_value = validator(value)
        setattr(self, private_name, validated_value)

    return property(getter, setter)

def positive_int(value):
    """验证正整数"""
    if not isinstance(value, int):
        raise TypeError("Must be an integer")
    if value <= 0:
        raise ValueError("Must be positive")
    return value

class Rectangle:
    width = validated_property("width", positive_int)
    height = validated_property("height", positive_int)

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @property
    def area(self) -> int:
        return self.width * self.height

rect = Rectangle(5, 10)
print(rect.area)  # 50
# rect.width = -5  # ValueError

# ========== 抽象property ==========
from abc import ABC, abstractmethod

class Shape(ABC):
    """抽象形状类"""

    @property
    @abstractmethod
    def area(self) -> float:
        """面积 - 子类必须实现"""
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        """周长 - 子类必须实现"""
        pass

class Square(Shape):
    def __init__(self, side: float):
        self._side = side

    @property
    def area(self) -> float:
        return self._side ** 2

    @property
    def perimeter(self) -> float:
        return 4 * self._side

sq = Square(5)
print(f"Area: {sq.area}, Perimeter: {sq.perimeter}")
```

#### 2.3.4 反例代码

```python
# ========== 反例1：setter没有对应的getter ==========
class Bad:
    def __init__(self):
        self._value = 0

    # 错误：先定义setter但没有getter
    # @value.setter  # NameError: name 'value' is not defined
    # def value(self, v):
    #     self._value = v

    # 正确顺序
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

# ========== 反例2：无限递归 ==========
class Recursive:
    def __init__(self):
        self._value = 0

    @property
    def value(self):
        # 错误：访问self.value会递归调用getter
        return self.value  # RecursionError

    @value.setter
    def value(self, v):
        # 错误：self.value = v 会调用setter
        self.value = v  # RecursionError

# 正确做法：使用私有属性
class Correct:
    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

# ========== 反例3：property名称冲突 ==========
class Conflict:
    def __init__(self):
        self.value = 0  # 实例属性

    @property
    def value(self):  # 与实例属性同名
        return 0

# 这会导致意外行为

# ========== 反例4：忘记self参数 ==========
class ForgotSelf:
    @property
    def value():  # 错误：缺少self
        return 0

# ========== 反例5：在旧式类中使用property ==========
# Python 2中，需要继承object才能使用property
# class OldStyle:  # Python 2 旧式类
#     @property
#     def value(self):
#         return 0

# Python 3中所有类都是新式类
class NewStyle:  # Python 3
    @property
    def value(self):
        return 0

# ========== 反例6：property与描述符混用 ==========
class Descriptor:
    def __get__(self, obj, objtype=None):
        return "descriptor"

class Mixed:
    # 错误：property和描述符可能冲突
    @property
    def value(self):
        return "property"

    # 这会覆盖property
    value = Descriptor()
```

#### 2.3.5 形式论证

**定理2.3（property的等价性）**
> `property(fget, fset, fdel, doc)` 等价于实现描述符协议的类实例。

**证明：**

```python
# property等价实现
class Property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
```

---

### 2.4 元类（metaclass）

#### 2.4.1 概念定义

**元类（Metaclass）** 是创建类的类。在Python中，`type` 是默认元类，所有类都是 `type` 的实例。自定义元类通过继承 `type` 并重写特定方法，可以在类创建时自定义类的行为。

**形式化定义：**

- 元类是 `type` 的子类
- 元类控制类的创建过程：`__new__` 和 `__init__`
- 元类可以修改类的名称空间、基类、方法等

#### 2.4.2 类创建过程

```
class MyClass(Base, metaclass=Meta):
    x = 1
    def method(self): pass

# 等价于
MyClass = Meta('MyClass', (Base,), {'x': 1, 'method': <function>})
```

#### 2.4.3 正例代码

```python
from typing import Any, Dict, Tuple

# ========== 基本元类 ==========
class BasicMeta(type):
    """基本元类 - 打印类创建信息"""

    def __new__(
        mcs: type,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any]
    ) -> type:
        print(f"Creating class: {name}")
        print(f"  Bases: {bases}")
        print(f"  Methods: {[k for k in namespace if callable(namespace[k])]}")
        return super().__new__(mcs, name, bases, namespace)

    def __init__(
        cls: type,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any]
    ) -> None:
        print(f"Initializing class: {name}")
        super().__init__(name, bases, namespace)

class MyClass(metaclass=BasicMeta):
    def method1(self):
        pass

    def method2(self):
        pass

# ========== 单例元类 ==========
class SingletonMeta(type):
    """单例元类"""
    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """数据库连接 - 单例"""

    def __init__(self, connection_string: str):
        # 注意：__init__每次都会调用
        print(f"Initializing with {connection_string}")
        self.connection_string = connection_string

db1 = Database("postgresql://localhost/db")
db2 = Database("mysql://localhost/db")
print(db1 is db2)  # True
print(db1.connection_string)  # postgresql://localhost/db

# ========== 自动注册元类 ==========
class PluginMeta(type):
    """插件注册元类"""
    registry: Dict[str, type] = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'BasePlugin':  # 不注册基类
            PluginMeta.registry[name] = cls
            print(f"Registered plugin: {name}")
        return cls

class BasePlugin(metaclass=PluginMeta):
    """插件基类"""
    def execute(self):
        raise NotImplementedError

class EmailPlugin(BasePlugin):
    def execute(self):
        return "Sending email"

class SMSPlugin(BasePlugin):
    def execute(self):
        return "Sending SMS"

print(PluginMeta.registry)

# ========== 接口检查元类 ==========
class InterfaceMeta(type):
    """接口检查元类 - 确保子类实现必需方法"""

    required_methods: Tuple[str, ...] = ()

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # 检查必需方法
        if name != 'Interface':
            for method in mcs.required_methods:
                if method not in namespace:
                    raise TypeError(
                        f"{name} must implement {method}()"
                    )

        return cls

class Interface(metaclass=InterfaceMeta):
    """接口基类"""
    required_methods = ('process', 'validate')

# 正确实现
class GoodImpl(Interface):
    def process(self):
        pass

    def validate(self):
        pass

# 错误实现 - 会抛出TypeError
# class BadImpl(Interface):
#     def process(self):
#         pass

# ========== 方法自动转换元类 ==========
class AutoPropertyMeta(type):
    """自动将方法转换为property"""

    def __new__(mcs, name, bases, namespace):
        # 转换以'_get_'开头的方法为property
        new_namespace = {}
        properties = {}

        for key, value in namespace.items():
            if key.startswith('_get_') and callable(value):
                prop_name = key[5:]  # 去掉'_get_'前缀
                properties[prop_name] = value
            else:
                new_namespace[key] = value

        # 创建property
        for prop_name, getter in properties.items():
            new_namespace[prop_name] = property(getter)

        return super().__new__(mcs, name, bases, new_namespace)

class DataModel(metaclass=AutoPropertyMeta):
    def __init__(self, value: int):
        self._value = value

    def _get_value(self):
        return self._value

    def _get_double(self):
        return self._value * 2

model = DataModel(5)
print(model.value)   # 5（自动转换为property）
print(model.double)  # 10

# ========== 带参数的元类 ==========
class ConfigurableMeta(type):
    """可配置元类"""

    def __new__(mcs, name, bases, namespace, prefix=""):
        # 添加前缀到所有方法名
        if prefix:
            new_namespace = {}
            for key, value in namespace.items():
                if callable(value) and not key.startswith('_'):
                    new_namespace[f"{prefix}_{key}"] = value
                else:
                    new_namespace[key] = value
            namespace = new_namespace

        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, prefix=""):
        super().__init__(name, bases, namespace)

class PrefixedClass(metaclass=ConfigurableMeta, prefix="api"):
    def get_data(self):
        return "data"

    def save_data(self):
        return "saved"

# 方法名被添加了前缀
# obj = PrefixedClass()
# obj.api_get_data()  # 需要这样调用

# ========== 元类继承 ==========
class BaseMeta(type):
    """基础元类"""
    def __new__(mcs, name, bases, namespace):
        print(f"BaseMeta creating {name}")
        return super().__new__(mcs, name, bases, namespace)

class DerivedMeta(BaseMeta):
    """派生元类"""
    def __new__(mcs, name, bases, namespace):
        print(f"DerivedMeta creating {name}")
        return super().__new__(mcs, name, bases, namespace)

class TestClass(metaclass=DerivedMeta):
    pass
```

#### 2.4.4 反例代码

```python
# ========== 反例1：元类冲突 ==========
class Meta1(type):
    pass

class Meta2(type):
    pass

class A(metaclass=Meta1):
    pass

class B(metaclass=Meta2):
    pass

# 错误：多重继承时元类冲突
# class C(A, B):  # TypeError
#     pass

# 解决方案：创建共同子元类
class CommonMeta(Meta1, Meta2):
    pass

class C(A, B, metaclass=CommonMeta):
    pass

# ========== 反例2：忘记调用super ==========
class BadMeta(type):
    def __new__(mcs, name, bases, namespace):
        # 错误：忘记调用super().__new__
        return type.__new__(mcs, name, bases, namespace)
        # 可能丢失某些功能

# 正确做法
class GoodMeta(type):
    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)

# ========== 反例3：修改不可变对象 ==========
class DangerousMeta(type):
    def __new__(mcs, name, bases, namespace):
        # 危险：直接修改传入的namespace
        namespace['new_attr'] = 1
        # 这会影响原始字典
        return super().__new__(mcs, name, bases, namespace)

# 正确做法：复制namespace
class SafeMeta(type):
    def __new__(mcs, name, bases, namespace):
        new_namespace = dict(namespace)
        new_namespace['new_attr'] = 1
        return super().__new__(mcs, name, bases, new_namespace)

# ========== 反例4：__init__与__new__混淆 ==========
class ConfusedMeta(type):
    def __new__(mcs, name, bases, namespace):
        print("__new__ called")
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        print("__init__ called")
        # 这里cls是已创建的类
        # 可以修改类，但不能改变类的身份
        super().__init__(name, bases, namespace)

# ========== 反例5：递归元类 ==========
# 错误：元类不能是自己的实例
# class Recursive(type, metaclass=Recursive):
#     pass

# ========== 反例6：使用type()创建类时的元类 ==========
# 使用type()直接创建类时，无法指定元类
# MyClass = type('MyClass', (), {}, metaclass=MyMeta)  # 错误

# 正确做法
MyClass = MyMeta('MyClass', (), {})
```

#### 2.4.5 形式论证

**定理2.4（元类的传递性）**
> 若类C的元类为M，则C的子类的默认元类也为M（除非显式指定）。

**证明：**

```python
class Meta(type):
    pass

class Base(metaclass=Meta):
    pass

class Derived(Base):  # 元类自动为Meta
    pass

type(Derived) == Meta  # True
```

**定理2.5（元类优先级）**
> 多重继承时，元类由最具体的元类决定（遵循MRO）。

**证明：**

```python
class Meta1(type): pass
class Meta2(Meta1): pass  # Meta2更具体

class A(metaclass=Meta1): pass
class B(metaclass=Meta2): pass

class C(A, B): pass  # 需要Meta2或其后代
```

---

### 2.5 抽象基类（ABC）

#### 2.5.1 概念定义

**抽象基类（Abstract Base Class, ABC）** 是不能实例化的类，用于定义接口规范。子类必须实现所有抽象方法才能被实例化。Python通过 `abc` 模块提供ABC支持。

**形式化定义：**

- 抽象类：继承 `ABC` 或使用 `ABCMeta` 元类
- 抽象方法：使用 `@abstractmethod` 装饰器
- 抽象属性：使用 `@abstractmethod` 与 `@property` 组合

#### 2.5.2 语法形式

```python
from abc import ABC, abstractmethod

class AbstractClass(ABC):
    @abstractmethod
    def method(self):
        pass
```

#### 2.5.3 正例代码

```python
from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod
from typing import List

# ========== 基本抽象类 ==========
class Shape(ABC):
    """形状抽象基类"""

    @abstractmethod
    def area(self) -> float:
        """计算面积 - 子类必须实现"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """计算周长 - 子类必须实现"""
        pass

    def describe(self) -> str:
        """具体方法 - 子类可直接使用"""
        return f"Area: {self.area()}, Perimeter: {self.perimeter()}"

class Rectangle(Shape):
    """矩形"""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# shape = Shape()  # TypeError: Can't instantiate abstract class
rect = Rectangle(5, 3)
print(rect.describe())  # Area: 15.0, Perimeter: 16.0

# ========== 抽象属性 ==========
class Vehicle(ABC):
    """交通工具抽象基类"""

    @property
    @abstractmethod
    def max_speed(self) -> float:
        """最大速度 - 抽象属性"""
        pass

    @abstractmethod
    def move(self) -> str:
        """移动方式"""
        pass

class Car(Vehicle):
    def __init__(self):
        self._max_speed = 200.0

    @property
    def max_speed(self) -> float:
        return self._max_speed

    def move(self) -> str:
        return "Driving on road"

car = Car()
print(f"Max speed: {car.max_speed} km/h")
print(car.move())

# ========== 抽象类方法和静态方法 ==========
class Database(ABC):
    """数据库抽象基类"""

    @abstractclassmethod
    def connect(cls, connection_string: str) -> "Database":
        """连接数据库 - 抽象类方法"""
        pass

    @abstractstaticmethod
    def validate_query(query: str) -> bool:
        """验证查询 - 抽象静态方法"""
        pass

    @abstractmethod
    def execute(self, query: str) -> List[dict]:
        """执行查询"""
        pass

class PostgreSQL(Database):
    @classmethod
    def connect(cls, connection_string: str) -> "PostgreSQL":
        print(f"Connecting to PostgreSQL: {connection_string}")
        return cls()

    @staticmethod
    def validate_query(query: str) -> bool:
        return query.strip().upper().startswith("SELECT")

    def execute(self, query: str) -> List[dict]:
        return [{"result": "data"}]

db = PostgreSQL.connect("postgresql://localhost")
print(PostgreSQL.validate_query("SELECT * FROM users"))  # True

# ========== 抽象方法组合 ==========
class DataSource(ABC):
    """数据源抽象基类"""

    @abstractmethod
    def read(self) -> str:
        """读取数据"""
        pass

    @abstractmethod
    def write(self, data: str) -> None:
        """写入数据"""
        pass

    def read_write(self, transform: callable) -> None:
        """模板方法 - 组合抽象方法"""
        data = self.read()
        transformed = transform(data)
        self.write(transformed)

class FileSource(DataSource):
    def __init__(self, filename: str):
        self.filename = filename

    def read(self) -> str:
        try:
            with open(self.filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def write(self, data: str) -> None:
        with open(self.filename, 'w') as f:
            f.write(data)

# ========== 注册虚拟子类 ==========
from abc import ABC, abstractmethod

class JSONSerializable(ABC):
    """JSON可序列化接口"""

    @abstractmethod
    def to_json(self) -> str:
        pass

class CustomData:
    """普通类 - 不是JSONSerializable的子类"""

    def __init__(self, value: int):
        self.value = value

    def to_json(self) -> str:
        return f'{{"value": {self.value}}}'

# 注册为虚拟子类
JSONSerializable.register(CustomData)

print(issubclass(CustomData, JSONSerializable))  # True
print(isinstance(CustomData(5), JSONSerializable))  # True

# ========== 抽象基类检查 ==========
class Container(ABC):
    """容器抽象基类"""

    @abstractmethod
    def __contains__(self, item) -> bool:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

class MyList(Container):
    def __init__(self):
        self._items = []

    def __contains__(self, item) -> bool:
        return item in self._items

    def __len__(self) -> int:
        return len(self._items)

    def append(self, item):
        self._items.append(item)

my_list = MyList()
my_list.append(1)
print(len(my_list))  # 1
print(1 in my_list)  # True

# ========== 组合抽象 ==========
class Flyable(ABC):
    @abstractmethod
    def fly(self) -> str:
        pass

class Swimmable(ABC):
    @abstractmethod
    def swim(self) -> str:
        pass

class Duck(Flyable, Swimmable):
    """鸭子 - 会飞也会游泳"""

    def fly(self) -> str:
        return "Duck flying"

    def swim(self) -> str:
        return "Duck swimming"

duck = Duck()
print(duck.fly())
print(duck.swim())
```

#### 2.5.4 反例代码

```python
from abc import ABC, abstractmethod

# ========== 反例1：实例化抽象类 ==========
class Abstract(ABC):
    @abstractmethod
    def method(self):
        pass

# obj = Abstract()  # TypeError: Can't instantiate abstract class

# ========== 反例2：未实现所有抽象方法 ==========
class PartialImpl(Abstract):
    pass  # 没有实现method

# obj = PartialImpl()  # TypeError

# ========== 反例3：抽象方法有实现但子类未调用 ==========
class BaseWithImpl(ABC):
    @abstractmethod
    def method(self):
        """抽象方法可以有默认实现"""
        print("Default implementation")

class Derived(BaseWithImpl):
    def method(self):
        # 可以选择调用父类实现
        super().method()
        print("Extended implementation")

d = Derived()
d.method()

# ========== 反例4：抽象方法装饰器顺序 ==========
class WrongOrder(ABC):
    # 错误：@abstractmethod必须在@property之前
    # @property
    # @abstractmethod
    # def value(self):  # 这会失败
    #     pass

    # 正确顺序
    @property
    @abstractmethod
    def value(self):
        pass

# ========== 反例5：抽象类中的非抽象方法调用抽象方法 ==========
class Risky(ABC):
    @abstractmethod
    def get_data(self):
        pass

    def process(self):
        # 危险：如果在抽象类中调用抽象方法
        data = self.get_data()  # 如果子类未实现会失败
        return data.upper()

# ========== 反例6：多重继承中的抽象方法冲突 ==========
class A(ABC):
    @abstractmethod
    def method(self):
        pass

class B(ABC):
    @abstractmethod
    def method(self):
        pass

class C(A, B):
    def method(self):
        # 必须实现一次，但满足两个抽象基类
        return "implemented"

c = C()
print(c.method())

# ========== 反例7：忘记继承ABC ==========
class NotReallyAbstract:
    @abstractmethod  # 没有继承ABC，装饰器无效
    def method(self):
        pass

obj = NotReallyAbstract()  # 可以实例化！
```

#### 2.5.5 形式论证

**定理2.6（抽象类的不可实例化性）**
> 若类C包含至少一个抽象方法，则 `C()` 抛出 `TypeError`。

**证明：** 由 `ABCMeta.__call__` 实现保证 ∎

**定理2.7（抽象方法的继承）**
> 若类C继承抽象类A，且C未实现A的所有抽象方法，则C也是抽象类。

**证明：**

```python
class A(ABC):
    @abstractmethod
    def m1(self): pass
    @abstractmethod
    def m2(self): pass

class B(A):
    def m1(self): pass  # 只实现一个

# B仍然是抽象类，因为m2未实现
```

---

## 第三部分：函数式编程特性

### 3.1 lambda表达式

#### 3.1.1 概念定义

**lambda表达式** 是创建匿名函数的语法结构。lambda函数是单表达式函数，可以捕获周围作用域的变量，常用于需要简单函数作为参数的场景。

**形式化定义：**

- 语法：`lambda [parameters]: expression`
- 语义：创建函数对象，参数为 `parameters`，返回 `expression` 的值
- 限制：只能包含单个表达式，不能包含语句

#### 3.1.2 语法形式（BNF）

```bnf
lambda_expr ::= "lambda" [parameter_list] ":" expression
parameter_list ::= identifier ("," identifier)*
```

#### 3.1.3 正例代码

```python
from typing import Callable, List

# ========== 基本lambda ==========
# 无参数
get_five = lambda: 5
print(get_five())  # 5

# 单参数
square = lambda x: x ** 2
print(square(5))  # 25

# 多参数
add = lambda x, y: x + y
print(add(3, 4))  # 7

# 默认参数
power = lambda base, exp=2: base ** exp
print(power(3))     # 9 (3^2)
print(power(2, 3))  # 8 (2^3)

# ========== lambda与高阶函数 ==========
numbers = [1, 2, 3, 4, 5]

# 映射
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# 过滤
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# 排序
pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
sorted_by_length = sorted(pairs, key=lambda x: len(x[1]))
print(sorted_by_length)  # [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]

# ========== lambda闭包 ==========
def make_multiplier(n: int) -> Callable[[int], int]:
    """创建乘数函数"""
    return lambda x: x * n

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15

# ========== lambda作为回调 ==========
def process_data(data: List[int], transform: Callable[[int], int]) -> List[int]:
    """处理数据，应用转换函数"""
    return [transform(x) for x in data]

result = process_data([1, 2, 3, 4], lambda x: x * 2 + 1)
print(result)  # [3, 5, 7, 9]

# ========== lambda在GUI回调中的应用（概念）==========
# button.on_click(lambda: print("Clicked!"))
# menu.on_select(lambda item: process(item))

# ========== lambda条件表达式 ==========
classify = lambda x: "positive" if x > 0 else "negative" if x < 0 else "zero"
print(classify(5))   # positive
print(classify(-3))  # negative
print(classify(0))   # zero

# ========== lambda与类型注解（Python 3.10+）==========
from typing import TypeVar

T = TypeVar('T')

# lambda本身不能有类型注解，但可以赋值给带类型的变量
identity: Callable[[T], T] = lambda x: x
print(identity(5))      # 5
print(identity("hello"))  # hello

# ========== 嵌套lambda ==========
make_adder = lambda x: lambda y: x + y
add_five = make_adder(5)
print(add_five(3))  # 8

# 柯里化
 curry = lambda f: lambda x: lambda y: f(x, y)
add_curried = curry(lambda x, y: x + y)
print(add_curried(3)(4))  # 7

# ========== lambda与数据结构 ==========
# 作为字典值
operations = {
    'add': lambda x, y: x + y,
    'subtract': lambda x, y: x - y,
    'multiply': lambda x, y: x * y,
    'divide': lambda x, y: x / y if y != 0 else float('inf')
}

print(operations['add'](5, 3))       # 8
print(operations['multiply'](4, 7))  # 28

# 作为排序键
students = [
    {'name': 'Alice', 'score': 85},
    {'name': 'Bob', 'score': 92},
    {'name': 'Charlie', 'score': 78}
]
top_student = max(students, key=lambda s: s['score'])
print(top_student)  # {'name': 'Bob', 'score': 92}
```

#### 3.1.4 反例代码

```python
# ========== 反例1：lambda包含语句 ==========
# 错误：lambda不能包含语句
# bad = lambda x: if x > 0: return x  # SyntaxError

# 正确：使用条件表达式
ok = lambda x: x if x > 0 else 0

# ========== 反例2：lambda包含多条语句 ==========
# 错误：lambda只能有一个表达式
# bad = lambda x: print(x); x + 1  # SyntaxError

# 正确：使用普通函数
def good(x):
    print(x)
    return x + 1

# ========== 反例3：lambda递归 ==========
# 错误：lambda不能直接递归
# factorial = lambda n: 1 if n <= 1 else n * factorial(n - 1)  # NameError

# 解决方案：使用Y组合子或命名函数
factorial = (lambda f: lambda n: 1 if n <= 1 else n * f(f)(n - 1))(lambda f: lambda n: 1 if n <= 1 else n * f(f)(n - 1))
print(factorial(5))  # 120

# 更好的方案：使用普通函数
def factorial_normal(n: int) -> int:
    return 1 if n <= 1 else n * factorial_normal(n - 1)

# ========== 反例4：lambda捕获循环变量（经典陷阱）==========
# 错误：所有lambda都捕获了同一个i（循环结束后的值）
functions = [lambda x: x + i for i in range(5)]
print([f(0) for f in functions])  # [4, 4, 4, 4, 4] - 不是[0, 1, 2, 3, 4]

# 正确：使用默认参数捕获当前值
functions = [lambda x, i=i: x + i for i in range(5)]
print([f(0) for f in functions])  # [0, 1, 2, 3, 4]

# ========== 反例5：lambda过于复杂 ==========
# 错误：lambda太长，可读性差
process = lambda data: [
    item.strip().lower()
    for item in data
    if item and len(item) > 3
]

# 正确：使用普通函数
def process_data(data):
    return [
        item.strip().lower()
        for item in data
        if item and len(item) > 3
    ]

# ========== 反例6：lambda与类型注解 ==========
# 错误：lambda不能有类型注解
# bad = lambda x: int, y: int -> int: x + y  # SyntaxError

# 正确：使用普通函数
def add(x: int, y: int) -> int:
    return x + y

# ========== 反例7：lambda赋值给变量（PEP 8建议）==========
# 不推荐：
f = lambda x: x + 1

# 推荐：
def f(x):
    return x + 1

# lambda应该直接作为参数使用
# sorted(data, key=lambda x: x.value)  # OK
```

#### 3.1.5 形式论证

**定理3.1（lambda的表达能力）**
> 对于任意单表达式函数，存在等价的lambda表达式；对于多语句函数，不存在等价的lambda表达式。

**证明：** 由lambda语法定义限制 ∎

**定理3.2（lambda闭包捕获）**
> lambda表达式在定义时捕获周围作用域的变量引用，而非值拷贝。

**证明：**

```python
x = 1
f = lambda: x
x = 2
print(f())  # 2（捕获引用，不是值）
```

---

### 3.2 高阶函数（map, filter, reduce）

#### 3.2.1 概念定义

**高阶函数（Higher-Order Function）** 是以函数为参数或返回函数的函数。Python内置的高阶函数包括 `map`、`filter`、`reduce` 等。

**形式化定义：**

- `map(f, iterable)`：将函数f应用于iterable的每个元素
- `filter(f, iterable)`：返回使f返回True的元素
- `reduce(f, iterable[, initializer])`：累积计算

#### 3.2.2 语法形式

```python
map(function, iterable, ...) -> iterator
filter(function, iterable) -> iterator
reduce(function, iterable[, initializer]) -> value
```

#### 3.2.3 正例代码

```python
from functools import reduce
from typing import List, Callable, Iterator

# ========== map函数 ==========
numbers = [1, 2, 3, 4, 5]

# 基本用法
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# 多可迭代对象
list1 = [1, 2, 3]
list2 = [10, 20, 30]
sums = list(map(lambda x, y: x + y, list1, list2))
print(sums)  # [11, 22, 33]

# 不同长度 - 以最短为准
list3 = [1, 2, 3, 4, 5]
list4 = [10, 20]
result = list(map(lambda x, y: x + y, list3, list4))
print(result)  # [11, 22]

# 使用内置函数
strings = ["hello", "world", "python"]
lengths = list(map(len, strings))
print(lengths)  # [5, 5, 6]

# 使用None作为函数（zip的行为）
pairs = list(map(None, [1, 2, 3], ['a', 'b', 'c']))  # Python 2风格
# Python 3中应该使用zip
pairs = list(zip([1, 2, 3], ['a', 'b', 'c']))
print(pairs)  # [(1, 'a'), (2, 'b'), (3, 'c')]

# ========== filter函数 ==========
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 基本过滤
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# 过滤None
mixed = [1, None, 2, None, 3, 0, '', False, 4]
truthy = list(filter(None, mixed))  # 过滤falsy值
print(truthy)  # [1, 2, 3, 4]

# 字符串过滤
words = ["apple", "", "banana", "", "cherry"]
non_empty = list(filter(lambda s: len(s) > 0, words))
print(non_empty)  # ['apple', 'banana', 'cherry']

# 对象过滤
class Product:
    def __init__(self, name: str, price: float, in_stock: bool):
        self.name = name
        self.price = price
        self.in_stock = in_stock

    def __repr__(self):
        return f"Product({self.name}, ${self.price})"

products = [
    Product("Apple", 1.5, True),
    Product("Banana", 0.5, False),
    Product("Cherry", 3.0, True)
]

in_stock = list(filter(lambda p: p.in_stock, products))
print(in_stock)  # [Product(Apple, $1.5), Product(Cherry, $3.0)]

# ========== reduce函数 ==========
numbers = [1, 2, 3, 4, 5]

# 累加
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# 带初始值
total_with_init = reduce(lambda x, y: x + y, numbers, 10)
print(total_with_init)  # 25

# 累乘
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120

# 找最大值
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(maximum)  # 5

# 字符串连接
words = ["Hello", " ", "World", "!"]
sentence = reduce(lambda x, y: x + y, words)
print(sentence)  # Hello World!

# 扁平化列表
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda x, y: x + y, nested)
print(flat)  # [1, 2, 3, 4, 5, 6]

# ========== 组合使用 ==========
numbers = range(1, 11)

# 先过滤偶数，再平方，最后求和
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers))
)
print(result)  # 220 (4 + 16 + 36 + 64 + 100)

# 使用列表推导式更简洁
result = sum(x ** 2 for x in numbers if x % 2 == 0)
print(result)  # 220

# ========== 自定义高阶函数 ==========
def compose(*functions: Callable) -> Callable:
    """函数组合"""
    def composed(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return composed

def add_one(x: int) -> int:
    return x + 1

def double(x: int) -> int:
    return x * 2

def square(x: int) -> int:
    return x ** 2

# (x + 1) * 2 ^ 2 = (5 + 1) * 2 ^ 2 = 6 ^ 2 = 36
composed = compose(square, double, add_one)
print(composed(5))  # ((5 + 1) * 2) ^ 2 = 144

# 修正：正确的组合顺序
def compose_right(*functions: Callable) -> Callable:
    """函数组合：f(g(h(x)))"""
    def composed(x):
        result = x
        for f in functions:
            result = f(result)
        return result
    return composed

composed = compose_right(add_one, double, square)
print(composed(5))  # square(double(add_one(5))) = square(double(6)) = square(12) = 144

# ========== 管道操作 ==========
def pipe(value, *functions):
    """管道操作：将值通过一系列函数"""
    for f in functions:
        value = f(value)
    return value

result = pipe(
    [1, 2, 3, 4, 5],
    lambda xs: filter(lambda x: x > 2, xs),
    lambda xs: map(lambda x: x * 2, xs),
    list,
    sum
)
print(result)  # 24 (6 + 8 + 10)
```

#### 3.2.4 反例代码

```python
from functools import reduce

# ========== 反例1：reduce空序列无初始值 ==========
# 错误：空序列且无初始值
# result = reduce(lambda x, y: x + y, [])  # TypeError

# 正确：提供初始值
result = reduce(lambda x, y: x + y, [], 0)
print(result)  # 0

# ========== 反例2：map的副作用 ==========
# 错误：在map中使用有副作用的函数
side_effects = []
def bad_func(x):
    side_effects.append(x)  # 副作用
    return x * 2

result = list(map(bad_func, [1, 2, 3]))
# 副作用难以追踪

# 正确：纯函数
result = list(map(lambda x: x * 2, [1, 2, 3]))

# ========== 反例3：filter与类型检查 ==========
mixed = [1, "2", 3, "4", 5]

# 错误：假设所有元素都是数字
# result = list(map(lambda x: x * 2, mixed))  # TypeError

# 正确：先过滤
numbers = list(filter(lambda x: isinstance(x, int), mixed))
result = list(map(lambda x: x * 2, numbers))
print(result)  # [2, 6, 10]

# ========== 反例4：reduce的可读性问题 ==========
# 错误：复杂的reduce难以理解
data = [(1, 2), (3, 4), (5, 6)]
result = reduce(lambda a, b: (a[0] + b[0], a[1] * b[1]), data)

# 正确：使用显式循环
sum_first = sum(x[0] for x in data)
prod_second = reduce(lambda a, b: a * b, (x[1] for x in data))

# ========== 反例5：map/filter vs 列表推导式 ==========
numbers = [1, 2, 3, 4, 5]

# 可以工作，但不够Pythonic
result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))

# 更Pythonic的做法
result = [x ** 2 for x in numbers if x % 2 == 0]

# ========== 反例6：惰性求值的陷阱 ==========
# map返回迭代器，只能遍历一次
mapped = map(lambda x: x * 2, [1, 2, 3])
print(list(mapped))  # [2, 4, 6]
print(list(mapped))  # []（已耗尽）

# 正确：如果需要多次使用，转换为列表
mapped = list(map(lambda x: x * 2, [1, 2, 3]))
print(list(mapped))  # [2, 4, 6]
print(list(mapped))  # [2, 4, 6]

# ========== 反例7：reduce与内置函数重复 ==========
numbers = [1, 2, 3, 4, 5]

# 不必要：用reduce实现sum
sum_reduce = reduce(lambda x, y: x + y, numbers)

# 更好：使用内置函数
sum_builtin = sum(numbers)

# 不必要：用reduce实现max
max_reduce = reduce(lambda x, y: x if x > y else y, numbers)

# 更好：使用内置函数
max_builtin = max(numbers)
```

#### 3.2.5 形式论证

**定理3.3（map的等价性）**
> `map(f, xs)` 等价于列表推导式 `[f(x) for x in xs]`。

**证明：** 两者都产生f应用于xs每个元素的结果 ∎

**定理3.4（reduce的结合性）**
> 若操作f满足结合律，则 `reduce(f, xs)` 与计算顺序无关。

**证明：**

```python
# 加法满足结合律
reduce(lambda x, y: x + y, [1, 2, 3])  # 6
# (1 + 2) + 3 == 1 + (2 + 3) == 6

# 减法不满足结合律
reduce(lambda x, y: x - y, [1, 2, 3])  # -4
# (1 - 2) - 3 == -4
# 1 - (2 - 3) == 2
```

---

### 3.3 itertools和functools模块

#### 3.3.1 概念定义

**itertools** 模块提供创建高效迭代器的工具，用于循环和组合操作。**functools** 模块提供高阶函数和可调用对象操作工具。

#### 3.3.2 itertools核心功能

| 类别 | 函数 | 功能 |
|-----|------|-----|
| 无限迭代器 | count, cycle, repeat | 无限序列 |
| 有限迭代器 | accumulate, chain, compress, dropwhile, filterfalse, groupby, islice, starmap, takewhile, tee, zip_longest | 有限序列操作 |
| 组合迭代器 | product, permutations, combinations, combinations_with_replacement | 组合生成 |

#### 3.3.3 functools核心功能

| 函数 | 功能 |
|-----|-----|
| reduce | 累积计算 |
| partial | 偏函数 |
| wraps | 装饰器辅助 |
| lru_cache | 缓存装饰器 |
| total_ordering | 自动比较方法 |
| singledispatch | 单分派泛函数 |
| cmp_to_key | 比较函数转键函数 |

#### 3.3.4 正例代码

```python
import itertools
import functools
from typing import Iterator, Callable

# ========== itertools: 无限迭代器 ==========
# count - 计数
for i in itertools.count(10, 2):  # 从10开始，步长2
    if i > 20:
        break
    print(i, end=' ')  # 10 12 14 16 18 20
print()

# cycle - 循环
for i, char in zip(range(7), itertools.cycle('ABC')):
    print(char, end=' ')  # A B C A B C A
print()

# repeat - 重复
trues = list(itertools.repeat(True, 5))
print(trues)  # [True, True, True, True, True]

# ========== itertools: 有限迭代器 ==========
# accumulate - 累积
numbers = [1, 2, 3, 4, 5]
running_sum = list(itertools.accumulate(numbers))
print(running_sum)  # [1, 3, 6, 10, 15]

running_product = list(itertools.accumulate(numbers, lambda x, y: x * y))
print(running_product)  # [1, 2, 6, 24, 120]

# chain - 链接
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
list3 = [True, False]
chained = list(itertools.chain(list1, list2, list3))
print(chained)  # [1, 2, 3, 'a', 'b', 'c', True, False]

# chain.from_iterable - 扁平化
nested = [[1, 2], [3, 4], [5, 6]]
flat = list(itertools.chain.from_iterable(nested))
print(flat)  # [1, 2, 3, 4, 5, 6]

# compress - 选择性过滤
data = ['a', 'b', 'c', 'd', 'e']
selectors = [1, 0, 1, 0, 1]
result = list(itertools.compress(data, selectors))
print(result)  # ['a', 'c', 'e']

# dropwhile / takewhile
numbers = [1, 2, 3, 4, 5, 1, 2, 3]

# 丢弃直到条件不满足
dropped = list(itertools.dropwhile(lambda x: x < 4, numbers))
print(dropped)  # [4, 5, 1, 2, 3]

# 获取直到条件不满足
taken = list(itertools.takewhile(lambda x: x < 4, numbers))
print(taken)  # [1, 2, 3]

# filterfalse - 反向过滤
numbers = [1, 2, 3, 4, 5, 6]
odd_numbers = list(itertools.filterfalse(lambda x: x % 2 == 0, numbers))
print(odd_numbers)  # [1, 3, 5]

# groupby - 分组（需要先排序）
data = [('A', 1), ('A', 2), ('B', 1), ('B', 2), ('A', 3)]
data.sort(key=lambda x: x[0])  # 必须先排序！

for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 1), ('A', 2)]
# B: [('B', 1), ('B', 2)]
# A: [('A', 3)]

# islice - 切片（支持无限迭代器）
first_10 = list(itertools.islice(itertools.count(), 10))
print(first_10)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# starmap - 展开参数
pairs = [(1, 2), (3, 4), (5, 6)]
products = list(itertools.starmap(lambda x, y: x * y, pairs))
print(products)  # [2, 12, 30]

# tee - 复制迭代器
original = iter([1, 2, 3, 4, 5])
copy1, copy2 = itertools.tee(original, 2)
print(list(copy1))  # [1, 2, 3, 4, 5]
print(list(copy2))  # [1, 2, 3, 4, 5]

# zip_longest - 不等长zip
list1 = [1, 2, 3]
list2 = ['a', 'b']
zipped = list(itertools.zip_longest(list1, list2, fillvalue='?'))
print(zipped)  # [(1, 'a'), (2, 'b'), (3, '?')]

# ========== itertools: 组合迭代器 ==========
# product - 笛卡尔积
colors = ['red', 'blue']
sizes = ['S', 'M']
products = list(itertools.product(colors, sizes))
print(products)  # [('red', 'S'), ('red', 'M'), ('blue', 'S'), ('blue', 'M')]

# permutations - 排列
items = ['A', 'B', 'C']
perms = list(itertools.permutations(items, 2))
print(perms)  # [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

# combinations - 组合
combs = list(itertools.combinations(items, 2))
print(combs)  # [('A', 'B'), ('A', 'C'), ('B', 'C')]

# combinations_with_replacement - 可重复组合
combs_wr = list(itertools.combinations_with_replacement(items, 2))
print(combs_wr)  # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]

# ========== functools: lru_cache ==========
@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """带缓存的斐波那契"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # 快速计算，因为有缓存
print(fibonacci.cache_info())  # 缓存统计

# ========== functools: total_ordering ==========
@functools.total_ordering
class Person:
    """自动实现比较方法"""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age

    def __lt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age

    def __repr__(self):
        return f"Person({self.name}, {self.age})"

p1 = Person("Alice", 30)
p2 = Person("Bob", 25)
p3 = Person("Charlie", 30)

print(p1 > p2)   # True（由__lt__推导）
print(p1 <= p3)  # True（由__eq__和__lt__推导）
print(p1 >= p2)  # True（由__lt__推导）

# ========== functools: singledispatch ==========
@functools.singledispatch
def process(data):
    """默认处理函数"""
    return f"Unknown type: {type(data)}"

@process.register(int)
def _(data):
    return f"Integer: {data}"

@process.register(str)
def _(data):
    return f"String: {data!r}"

@process.register(list)
def _(data):
    return f"List with {len(data)} items"

print(process(42))        # Integer: 42
print(process("hello"))   # String: 'hello'
print(process([1, 2, 3])) # List with 3 items
print(process(3.14))      # Unknown type: <class 'float'>

# ========== functools: cmp_to_key ==========
def compare_length(s1: str, s2: str) -> int:
    """比较函数：返回负数、零或正数"""
    return len(s1) - len(s2)

words = ["python", "is", "awesome", "!"]
sorted_words = sorted(words, key=functools.cmp_to_key(compare_length))
print(sorted_words)  # ['!', 'is', 'python', 'awesome']
```

#### 3.3.5 反例代码

```python
import itertools
import functools

# ========== 反例1：groupby忘记排序 ==========
data = [('B', 1), ('A', 2), ('B', 3), ('A', 4)]

# 错误：未排序导致意外分组
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# B: [('B', 1)]
# A: [('A', 2)]
# B: [('B', 3)] - 又一个B组！
# A: [('A', 4)] - 又一个A组！

# 正确：先排序
data.sort(key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 2), ('A', 4)]
# B: [('B', 1), ('B', 3)]

# ========== 反例2：tee后使用原迭代器 ==========
original = iter([1, 2, 3, 4, 5])
copy1, copy2 = itertools.tee(original, 2)

# 错误：继续使用原迭代器
# next(original)  # 这会消耗原迭代器，但tee可能受影响

# 正确：只使用tee返回的副本
print(list(copy1))
print(list(copy2))

# ========== 反例3：无限迭代器无终止条件 ==========
# 错误：无限循环
# for i in itertools.count():
#     print(i)  # 永远运行

# 正确：使用islice或条件终止
for i in itertools.islice(itertools.count(), 10):
    print(i, end=' ')
print()

# ========== 反例4：lru_cache与可变参数 ==========
@functools.lru_cache(maxsize=128)
def bad_cache(data: list) -> int:
    """错误：缓存可变对象"""
    return sum(data)

# 正确：使用不可变类型
@functools.lru_cache(maxsize=128)
def good_cache(data: tuple) -> int:
    return sum(data)

print(good_cache((1, 2, 3)))

# ========== 反例5：lru_cache的maxsize ==========
# 错误：maxsize=None可能占用大量内存
@functools.lru_cache(maxsize=None)
def unbounded_cache(x):
    return x * 2

# 正确：设置合理的maxsize
@functools.lru_cache(maxsize=128)
def bounded_cache(x):
    return x * 2

# ========== 反例6：total_ordering的陷阱 ==========
@functools.total_ordering
class BadComparison:
    """错误：只实现__eq__，没有__lt__"""

    def __eq__(self, other):
        return True

    # 缺少__lt__会导致AttributeError

# ========== 反例7：singledispatch类型检查 ==========
@functools.singledispatch
def process(data):
    return "default"

@process.register(int)
def _(data):
    return f"int: {data}"

# 注意：singledispatch基于类型，不是isinstance检查
class MyInt(int):
    pass

print(process(MyInt(5)))  # "int: 5"（继承也适用）
```

---

### 3.4 偏函数（partial）

#### 3.4.1 概念定义

**偏函数（Partial Function）** 是通过固定函数的部分参数而创建的新函数。`functools.partial` 返回一个可调用对象，其行为类似于原函数，但某些参数已被预设。

**形式化定义：**

- `partial(func, *args, **keywords)`：返回偏函数对象
- 调用偏函数时，预设参数与新参数合并后调用原函数

#### 3.4.2 语法形式

```python
partial(func, /, *args, **keywords) -> partial object
```

#### 3.4.3 正例代码

```python
from functools import partial
from typing import Callable

# ========== 基本partial ==========
def power(base: float, exp: float) -> float:
    """计算幂"""
    return base ** exp

# 创建平方函数
square = partial(power, exp=2)
print(square(5))   # 25
print(square(3))   # 9

# 创建立方函数
cube = partial(power, exp=3)
print(cube(2))     # 8

# 创建以2为底的幂函数
power_of_2 = partial(power, base=2)
print(power_of_2(10))  # 1024

# ========== 多参数partial ==========
def format_string(template: str, **kwargs) -> str:
    """格式化字符串"""
    return template.format(**kwargs)

greeting = partial(format_string, "Hello, {name}!")
print(greeting(name="Alice"))  # Hello, Alice!
print(greeting(name="Bob"))    # Hello, Bob!

# ========== partial与内置函数 ==========
# 自定义int转换
int_base_2 = partial(int, base=2)
print(int_base_2("1010"))  # 10
print(int_base_2("1111"))  # 15

# 自定义排序
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]

sort_by_score = partial(sorted, key=lambda s: s["score"])
print(sort_by_score(students))

# ========== partialmethod（类中使用）==========
from functools import partialmethod

class Cell:
    """电子表格单元格"""

    def __init__(self):
        self._value = 0

    def set_value(self, value: float) -> None:
        self._value = value

    def get_value(self) -> float:
        return self._value

    # 创建快捷方法
    set_zero = partialmethod(set_value, 0)
    set_one = partialmethod(set_value, 1)

cell = Cell()
cell.set_zero()
print(cell.get_value())  # 0
cell.set_one()
print(cell.get_value())  # 1

# ========== 实际应用：回调函数 ==========
def send_notification(user: str, message: str, priority: str) -> None:
    """发送通知"""
    print(f"[{priority}] To {user}: {message}")

# 创建特定用户的通知函数
notify_alice = partial(send_notification, user="Alice", priority="NORMAL")
notify_bob = partial(send_notification, user="Bob", priority="HIGH")

notify_alice(message="Meeting at 3pm")
notify_bob(message="Server down!")

# ========== 实际应用：数据处理管道 ==========
def transform(data: list, filter_fn=None, map_fn=None, sort_key=None) -> list:
    """数据转换管道"""
    result = data
    if filter_fn:
        result = list(filter(filter_fn, result))
    if map_fn:
        result = list(map(map_fn, result))
    if sort_key:
        result = sorted(result, key=sort_key)
    return result

# 创建特定的转换管道
process_scores = partial(
    transform,
    filter_fn=lambda x: x >= 0,
    map_fn=lambda x: round(x, 2),
    sort_key=None
)

scores = [85.567, -10, 92.345, 78.901, -5]
print(process_scores(scores))  # [85.57, 92.35, 78.9]

# ========== partial与装饰器 ==========
def retry(max_attempts: int, func: Callable) -> Callable:
    """重试装饰器"""
    def wrapper(*args, **kwargs):
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise
                print(f"Attempt {attempt + 1} failed, retrying...")
    return wrapper

# 创建特定重试次数的装饰器
retry_3_times = partial(retry, max_attempts=3)
retry_5_times = partial(retry, max_attempts=5)

@retry_3_times
def fetch_data(url: str) -> str:
    """获取数据（模拟）"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return f"Data from {url}"

# ========== 检查partial属性 ==========
def example(a, b, c, d=4):
    return a + b + c + d

p = partial(example, 1, c=3)
print(p.func)   # <function example>
print(p.args)   # (1,)
print(p.keywords)  # {'c': 3}
print(p(2, d=5))  # 1 + 2 + 3 + 5 = 11
```

#### 3.4.4 反例代码

```python
from functools import partial

# ========== 反例1：关键字参数冲突 ==========
def func(a, b):
    return a + b

p = partial(func, a=1)
# p(a=2, b=3)  # TypeError: func() got multiple values for argument 'a'

# 正确：位置参数优先
p = partial(func, 1)  # a=1
print(p(2))  # 3

# ========== 反例2：忘记partial是对象不是函数 ==========
p = partial(lambda x, y: x + y, 1)

# partial对象有一些特殊属性
print(p.func)  # 原函数
print(p.args)  # 预设位置参数
print(p.keywords)  # 预设关键字参数

# 这些属性可以被修改（通常不建议）
p.args = (2,)
print(p(3))  # 5 (2 + 3)

# ========== 反例3：partial与可变默认参数 ==========
def append(item, items=[]):
    items.append(item)
    return items

# 危险：共享可变对象
append_1 = partial(append, 1)
print(append_1())  # [1]
print(append_1())  # [1, 1] - 累积！

# 正确：使用不可变默认参数
def append_safe(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# ========== 反例4：partial与类型注解 ==========
def typed_func(x: int, y: str) -> str:
    return f"{x}: {y}"

p = partial(typed_func, x=10)
# partial对象丢失了类型注解
# 需要使用typing.Protocol或自定义类来保留类型信息

# ========== 反例5：过度使用partial ==========
def multiply(x, y):
    return x * y

# 不必要：简单的lambda更清晰
double = partial(multiply, 2)
# vs
double = lambda x: x * 2

# ========== 反例6：partialmethod在实例方法中的问题 ==========
from functools import partialmethod

class Problematic:
    def method(self, x):
        return x * 2

    # partialmethod需要self，但调用时不需要传
    doubled = partialmethod(method, 2)

p = Problematic()
print(p.doubled())  # 4
```

#### 3.4.5 形式论证

**定理3.5（partial的等价性）**
> `partial(f, a, b=c)(d, e=f)` 等价于 `f(a, d, b=c, e=f)`。

**证明：** 由partial定义，预设参数与新参数合并后调用原函数 ∎

---

## 第四部分：面向对象高级特性

### 4.1 多重继承与MRO

#### 4.1.1 概念定义

**多重继承（Multiple Inheritance）** 是一个类继承多个父类的特性。**MRO（Method Resolution Order，方法解析顺序）** 是Python确定方法调用顺序的算法，使用C3线性化算法。

**形式化定义：**

- MRO是类的线性排序，满足局部优先性和单调性
- C3线性化：合并父类的MRO，保持继承层次结构

#### 4.1.2 MRO算法（C3线性化）

```
L(C) = C + merge(L(B1), L(B2), ..., L(Bn), [B1, B2, ..., Bn])
其中B1, B2, ..., Bn是C的父类
```

#### 4.1.3 正例代码

```python
# ========== 基本多重继承 ==========
class Flyable:
    def fly(self):
        return "Flying"

    def move(self):
        return "Flying through air"

class Swimmable:
    def swim(self):
        return "Swimming"

    def move(self):
        return "Swimming in water"

class Duck(Flyable, Swimmable):
    """鸭子：会飞也会游泳"""
    def quack(self):
        return "Quack!"

duck = Duck()
print(duck.fly())    # Flying
print(duck.swim())   # Swimming
print(duck.quack())  # Quack!
print(duck.move())   # Flying through air（来自Flyable）

# 查看MRO
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Flyable'>, <class 'Swimmable'>, <class 'object'>)

# ========== super()的使用 ==========
class A:
    def __init__(self):
        print("A.__init__")
        self.a = "A"

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()
        self.b = "B"

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()
        self.c = "C"

class D(B, C):
    def __init__(self):
        print("D.__init__")
        super().__init__()
        self.d = "D"

d = D()
# D.__init__
# B.__init__
# C.__init__
# A.__init__
print(d.__dict__)  # {'d': 'D', 'b': 'B', 'c': 'C', 'a': 'A'}

# ========== 菱形继承 ==========
class Base:
    def method(self):
        return "Base"

class Left(Base):
    def method(self):
        return f"Left -> {super().method()}"

class Right(Base):
    def method(self):
        return f"Right -> {super().method()}"

class Diamond(Left, Right):
    def method(self):
        return f"Diamond -> {super().method()}"

diamond = Diamond()
print(diamond.method())  # Diamond -> Left -> Right -> Base
print(Diamond.__mro__)
# (<class 'Diamond'>, <class 'Left'>, <class 'Right'>, <class 'Base'>, <class 'object'>)

# ========== 协作多重继承 ==========
class BaseMixin:
    def __init__(self, **kwargs):
        print(f"BaseMixin.__init__: {self.__class__.__name__}")
        super().__init__(**kwargs)

class NamedMixin(BaseMixin):
    def __init__(self, name=None, **kwargs):
        print(f"NamedMixin.__init__: name={name}")
        self.name = name
        super().__init__(**kwargs)

class DatedMixin(BaseMixin):
    def __init__(self, date=None, **kwargs):
        print(f"DatedMixin.__init__: date={date}")
        self.date = date
        super().__init__(**kwargs)

class Document(NamedMixin, DatedMixin):
    def __init__(self, content=None, **kwargs):
        print(f"Document.__init__")
        self.content = content
        super().__init__(**kwargs)

doc = Document(name="Report", date="2024-01-01", content="Content")
print(doc.name)     # Report
print(doc.date)     # 2024-01-01
print(doc.content)  # Content

# ========== 混入模式 ==========
class JSONSerializableMixin:
    """JSON序列化混入"""
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__)

class ComparableMixin:
    """可比较混入"""
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

class Person(JSONSerializableMixin, ComparableMixin):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

p1 = Person("Alice", 30)
p2 = Person("Alice", 30)
p3 = Person("Bob", 25)

print(p1.to_json())  # {"name": "Alice", "age": 30}
print(p1 == p2)      # True
print(p1 == p3)      # False

# ========== 抽象基类与多重继承 ==========
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Resizable(ABC):
    @abstractmethod
    def resize(self, factor: float):
        pass

class Rectangle(Drawable, Resizable):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def draw(self):
        return f"Drawing rectangle {self.width}x{self.height}"

    def resize(self, factor: float):
        self.width *= factor
        self.height *= factor

rect = Rectangle(10, 5)
print(rect.draw())
rect.resize(2)
print(rect.width, rect.height)  # 20 10
```

#### 4.1.4 反例代码

```python
# ========== 反例1：MRO冲突 ==========
class A:
    pass

class B(A):
    pass

class C(A):
    pass

# 错误：无法创建一致的MRO
# class D(B, C, B):  # TypeError: duplicate base class B
#     pass

# ========== 反例2：super()调用顺序问题 ==========
class A:
    def __init__(self):
        print("A")
        self.value = "A"

class B(A):
    def __init__(self):
        print("B")
        self.value = "B"  # 覆盖A的值
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        self.value = "C"  # 覆盖A的值
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()

d = D()
print(d.value)  # A（最后调用的是A.__init__）

# ========== 反例3：忘记super() ==========
class Base:
    def __init__(self):
        self.base_initialized = True

class Derived(Base):
    def __init__(self):
        # 错误：忘记调用super().__init__()
        self.derived_initialized = True

d = Derived()
print(hasattr(d, 'base_initialized'))  # False

# ========== 反例4：不兼容的方法签名 ==========
class Printer:
    def print(self, document: str):
        print(f"Printing: {document}")

class ColorPrinter(Printer):
    # 错误：改变了方法签名
    def print(self, document: str, color: str):
        print(f"Printing in {color}: {document}")

# ========== 反例5：钻石继承中的重复初始化 ==========
class Base:
    def __init__(self):
        print("Base init")
        self.counter = getattr(self, 'counter', 0) + 1

class Left(Base):
    def __init__(self):
        print("Left init")
        Base.__init__(self)  # 错误：直接调用父类

class Right(Base):
    def __init__(self):
        print("Right init")
        Base.__init__(self)  # 错误：直接调用父类

class Diamond(Left, Right):
    def __init__(self):
        print("Diamond init")
        Left.__init__(self)
        Right.__init__(self)

d = Diamond()
print(d.counter)  # 2（Base被初始化了两次！）

# 正确做法：使用super()
class Base2:
    def __init__(self):
        print("Base2 init")
        self.counter = getattr(self, 'counter', 0) + 1
        super().__init__()

class Left2(Base2):
    def __init__(self):
        print("Left2 init")
        super().__init__()

class Right2(Base2):
    def __init__(self):
        print("Right2 init")
        super().__init__()

class Diamond2(Left2, Right2):
    def __init__(self):
        print("Diamond2 init")
        super().__init__()

d2 = Diamond2()
print(d2.counter)  # 1（Base只初始化一次）
```

#### 4.1.5 形式论证

**定理4.1（C3线性化的完备性）**
> 对于任意合法的类继承层次，C3线性化产生唯一的MRO。

**证明：** C3算法保证：

1. 子类在父类之前
2. 父类声明顺序被保留
3. 单调性：子类的MRO是父类MRO的扩展

**定理4.2（super()的MRO遵循）**
> `super().method()` 调用MRO中下一个类的method。

**证明：** `super()` 返回一个代理对象，该对象使用当前类的MRO查找下一个类 ∎

---

### 4.2 混入（Mixin）模式

#### 4.2.1 概念定义

**混入（Mixin）** 是一种设计模式，通过多重继承为类提供可选功能。混入类通常不独立使用，而是与其他类组合提供特定功能。

**混入特征：**

1. 不单独实例化
2. 通常位于继承列表的前面
3. 使用 `super()` 确保协作

#### 4.2.2 正例代码

```python
from typing import Dict, Any
import json
import time

# ========== 日志混入 ==========
class LoggableMixin:
    """日志记录混入"""

    def log(self, message: str) -> None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.__class__.__name__}: {message}")

    def __init__(self, *args, **kwargs):
        self.log("Initializing")
        super().__init__(*args, **kwargs)

# ========== 验证混入 ==========
class ValidatableMixin:
    """数据验证混入"""

    _validators: Dict[str, Any] = {}

    def validate(self) -> bool:
        for field, validator in self._validators.items():
            value = getattr(self, field, None)
            if not validator(value):
                raise ValueError(f"Validation failed for {field}")
        return True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate()

# ========== 序列化混入 ==========
class JSONSerializableMixin:
    """JSON序列化混入"""

    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=str, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "JSONSerializableMixin":
        data = json.loads(json_str)
        return cls(**data)

# ========== 缓存混入 ==========
class CacheableMixin:
    """简单缓存混入"""

    _cache: Dict[str, Any] = {}

    def cached(self, key: str, compute: callable) -> Any:
        if key not in self._cache:
            self._cache[key] = compute()
        return self._cache[key]

    def clear_cache(self) -> None:
        self._cache.clear()

# ========== 组合使用混入 ==========
class User(LoggableMixin, ValidatableMixin, JSONSerializableMixin):
    """用户类，组合多个混入"""

    _validators = {
        'name': lambda x: x and len(x) >= 2,
        'email': lambda x: '@' in str(x)
    }

    def __init__(self, name: str, email: str, age: int = 0):
        self.name = name
        self.email = email
        self.age = age
        super().__init__()  # 调用所有混入的__init__

    def __str__(self) -> str:
        return f"User({self.name}, {self.email})"

# 使用
user = User("Alice", "alice@example.com", 30)
# [2024-01-15 10:30:00] User: Initializing
print(user.to_json())
# {
//   "name": "Alice",
//   "email": "alice@example.com",
//   "age": 30
// }

# ========== 权限混入 ==========
class PermissionMixin:
    """权限检查混入"""

    _permissions: set = set()

    def has_permission(self, permission: str) -> bool:
        return permission in self._permissions

    def add_permission(self, permission: str) -> None:
        self._permissions.add(permission)

    def check_permission(self, permission: str) -> None:
        if not self.has_permission(permission):
            raise PermissionError(f"Missing permission: {permission}")

class AdminUser(User, PermissionMixin):
    """管理员用户"""

    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        self.add_permission("read")
        self.add_permission("write")
        self.add_permission("delete")

admin = AdminUser("Admin", "admin@example.com")
print(admin.has_permission("write"))  # True
admin.check_permission("read")  # OK
# admin.check_permission("execute")  # PermissionError

# ========== 上下文管理器混入 ==========
class ContextManagerMixin:
    """上下文管理器混入"""

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.teardown()
        return False

    def setup(self):
        raise NotImplementedError

    def teardown(self):
        raise NotImplementedError

class DatabaseConnection(ContextManagerMixin):
    """数据库连接"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    def setup(self):
        print(f"Connecting to {self.connection_string}")
        self.connection = "connected"

    def teardown(self):
        print("Closing connection")
        self.connection = None

    def query(self, sql: str):
        return f"Result of: {sql}"

# 使用
# with DatabaseConnection("postgresql://localhost") as db:
#     print(db.query("SELECT * FROM users"))

# ========== 事件混入 ==========
class EventMixin:
    """事件处理混入"""

    _handlers: Dict[str, list] = {}

    def on(self, event: str, handler: callable) -> None:
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)

    def emit(self, event: str, *args, **kwargs) -> None:
        for handler in self._handlers.get(event, []):
            handler(*args, **kwargs)

class Button(EventMixin):
    """按钮类"""

    def click(self):
        print("Button clicked")
        self.emit("click", self)

button = Button()
button.on("click", lambda btn: print(f"Handler 1: {btn}"))
button.on("click", lambda btn: print(f"Handler 2: {btn}"))
button.click()

# ========== 混入最佳实践 ==========
class OrderedMixin:
    """排序支持混入 - 最佳实践示例"""

    _order_field = 'id'

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return getattr(self, self._order_field) < getattr(other, self._order_field)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return getattr(self, self._order_field) == getattr(other, self._order_field)

class Product(OrderedMixin, JSONSerializableMixin):
    _order_field = 'price'

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

products = [Product("A", 30), Product("B", 20), Product("C", 40)]
sorted_products = sorted(products)
print([p.name for p in sorted_products])  # ['B', 'A', 'C']
```

#### 4.2.3 反例代码

```python
# ========== 反例1：混入有独立功能 ==========
class BadMixin:
    """错误：混入不应该有独立功能"""

    def standalone_method(self):
        # 这个方法不依赖于主类
        return "I don't need a host class"

# 混入应该只提供辅助功能

# ========== 反例2：混入位于继承列表末尾 ==========
class Base:
    pass

class Mixin:
    def method(self):
        return "Mixin"

# 错误：Mixin在末尾，可能被Base覆盖
class WrongOrder(Base, Mixin):
    pass

# 正确：Mixin在前面
class RightOrder(Mixin, Base):
    pass

# ========== 反例3：混入不使用super() ==========
class BadInitMixin:
    def __init__(self):
        # 错误：不使用super()，打断MRO链
        self.mixin_initialized = True

class GoodInitMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mixin_initialized = True

# ========== 反例4：混入依赖特定属性 ==========
class FragileMixin:
    """脆弱混入：假设self.name存在"""

    def greet(self):
        return f"Hello, {self.name}"  # 可能AttributeError

# 正确做法：检查或使用抽象方法
class RobustMixin:
    def greet(self):
        name = getattr(self, 'name', 'Unknown')
        return f"Hello, {name}"

# ========== 反例5：混入与主类方法名冲突 ==========
class LoggerMixin:
    def log(self, msg):
        print(f"Mixin: {msg}")

class Service:
    def log(self, msg):
        print(f"Service: {msg}")

class MyService(LoggerMixin, Service):
    pass  # LoggerMixin.log会覆盖Service.log

# 解决方案：使用不同的方法名或显式调用
```

---

### 4.3 数据类（@dataclass）

#### 4.3.1 概念定义

**数据类（Dataclass）** 是Python 3.7+引入的装饰器，用于自动生成特殊方法（`__init__`、`__repr__`、`__eq__`等），简化数据容器类的编写。

**形式化定义：**

- `@dataclass` 装饰器自动生成数据相关方法
- 字段使用类型注解声明
- 支持默认值、默认值工厂、字段排序等

#### 4.3.2 语法形式

```python
@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class ClassName:
    field1: type
    field2: type = default_value
    field3: type = field(default_factory=list)
```

#### 4.3.3 正例代码

```python
from dataclasses import dataclass, field, asdict, astuple, replace
from typing import List, Optional
from datetime import datetime

# ========== 基本数据类 ==========
@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
print(p)           # Point(x=1.0, y=2.0)
print(repr(p))     # Point(x=1.0, y=2.0)
print(p.x, p.y)    # 1.0 2.0

# 相等比较
p2 = Point(1.0, 2.0)
p3 = Point(2.0, 3.0)
print(p == p2)     # True
print(p == p3)     # False

# ========== 带默认值的数据类 ==========
@dataclass
class Person:
    name: str
    age: int = 0
    email: Optional[str] = None

person = Person("Alice")
print(person)  # Person(name='Alice', age=0, email=None)

person2 = Person("Bob", 30, "bob@example.com")
print(person2)  # Person(name='Bob', age=30, email='bob@example.com')

# ========== 可变默认值工厂 ==========
@dataclass
class ShoppingCart:
    items: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

cart1 = ShoppingCart()
cart1.items.append("apple")

cart2 = ShoppingCart()
print(cart2.items)  # []（独立列表）

# ========== 字段选项 ==========
@dataclass
class Product:
    name: str
    price: float = field(compare=False)  # 不参与比较
    quantity: int = field(default=0, repr=False)  # 不参与repr
    tags: List[str] = field(default_factory=list, hash=False)  # 不参与哈希

p1 = Product("Apple", 1.5, 100, ["fruit"])
p2 = Product("Apple", 2.0, 200, ["food"])
print(p1 == p2)  # True（只比较name）
print(p1)        # Product(name='Apple', price=1.5)

# ========== 有序数据类 ==========
@dataclass(order=True)
class Student:
    """可排序的学生类"""
    name: str = field(compare=False)
    grade: float

    def __post_init__(self):
        if self.grade < 0 or self.grade > 100:
            raise ValueError("Grade must be between 0 and 100")

students = [
    Student("Alice", 85.5),
    Student("Bob", 92.0),
    Student("Charlie", 78.0)
]

sorted_students = sorted(students)
print([s.name for s in sorted_students])  # ['Charlie', 'Alice', 'Bob']

# ========== 不可变数据类 ==========
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

ip = ImmutablePoint(1.0, 2.0)
# ip.x = 3.0  # FrozenInstanceError

# 创建新实例
new_point = replace(ip, x=3.0)
print(new_point)  # ImmutablePoint(x=3.0, y=2.0)
print(ip)         # ImmutablePoint(x=1.0, y=2.0)（不变）

# ========== 继承数据类 ==========
@dataclass
class Animal:
    name: str
    age: int

@dataclass
class Dog(Animal):
    breed: str
    tricks: List[str] = field(default_factory=list)

dog = Dog("Buddy", 3, "Golden Retriever", ["sit", "fetch"])
print(dog)  # Dog(name='Buddy', age=3, breed='Golden Retriever', tricks=['sit', 'fetch'])

# ========== 实用函数 ==========
@dataclass
class Config:
    debug: bool = False
    timeout: int = 30
    retries: int = 3

config = Config(debug=True, timeout=60)

# 转换为字典
config_dict = asdict(config)
print(config_dict)  # {'debug': True, 'timeout': 60, 'retries': 3}

# 转换为元组
config_tuple = astuple(config)
print(config_tuple)  # (True, 60, 3)

# 创建副本并修改
new_config = replace(config, retries=5)
print(new_config)  # Config(debug=True, timeout=60, retries=5)

# ========== 复杂数据类 ==========
@dataclass
class Address:
    street: str
    city: str
    zip_code: str
    country: str = "USA"

@dataclass
class Customer:
    id: int
    name: str
    email: str
    address: Address
    orders: List[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

address = Address("123 Main St", "New York", "10001")
customer = Customer(1, "John Doe", "john@example.com", address)
print(customer)

# ========== __post_init__ ==========
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    perimeter: float = field(init=False)

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive")
        self.area = self.width * self.height
        self.perimeter = 2 * (self.width + self.height)

rect = Rectangle(5, 3)
print(f"Area: {rect.area}, Perimeter: {rect.perimeter}")

# ========== 类变量 ==========
@dataclass
class Counter:
    count: int = 0
    _total: int = field(default=0, init=False, repr=False)

    def __post_init__(self):
        Counter._total += self.count

    @classmethod
    def get_total(cls) -> int:
        return cls._total

c1 = Counter(10)
c2 = Counter(20)
print(Counter.get_total())  # 30
```

#### 4.3.4 反例代码

```python
from dataclasses import dataclass, field

# ========== 反例1：可变默认值 ==========
# 错误：使用可变默认值
@dataclass
class BadCart:
    items: list = []  # 危险！所有实例共享同一个列表

# 正确：使用field(default_factory=...)
@dataclass
class GoodCart:
    items: list = field(default_factory=list)

# ========== 反例2：类型注解缺失 ==========
# 错误：缺少类型注解的字段被忽略
@dataclass
class BadClass:
    x = 1  # 没有类型注解，不是数据类字段
    y: int = 2  # 这是数据类字段

b = BadClass()
print(b)  # BadClass(y=2) - x不是字段

# ========== 反例3：frozen与可变字段 ==========
@dataclass(frozen=True)
class BadImmutable:
    items: list  # 字段不可变，但列表内容可变

bi = BadImmutable([1, 2, 3])
bi.items.append(4)  # 这可以！
print(bi.items)  # [1, 2, 3, 4]

# ========== 反例4：继承中的默认值顺序 ==========
@dataclass
class Parent:
    x: int
    y: int = 0

# 错误：子类不能有带默认值的字段在父类无默认值字段之前
# @dataclass
# class BadChild(Parent):
#     z: int = 0  # OK
#     w: int      # Error: non-default argument follows default argument

# 正确：调整顺序或使用更多默认值
@dataclass
class GoodChild(Parent):
    w: int
    z: int = 0

# ========== 反例5：__init__覆盖 ==========
@dataclass
class BadOverride:
    x: int
    y: int

    def __init__(self, x, y):  # 覆盖自动生成的__init__
        self.x = x
        # 忘记设置self.y

b = BadOverride(1, 2)
print(b.y)  # AttributeError

# ========== 反例6：字段名冲突 ==========
@dataclass
class Conflicting:
    name: str
    # name: int = 0  # Error: duplicate field name

# ========== 反例7：order=True但没有eq=True ==========
# @dataclass(order=True, eq=False)  # 错误：order需要eq
# class BadOrder:
#     x: int
```

---

### 4.4 枚举类（Enum）

#### 4.4.1 概念定义

**枚举（Enum）** 是Python 3.4+引入的枚举类型，用于定义具名常量集合。枚举成员是单例对象，支持比较和迭代。

**形式化定义：**

- `Enum` 是创建枚举的基类
- 枚举成员：`Name = value`
- 成员具有 `name` 和 `value` 属性

#### 4.4.2 语法形式

```python
class EnumName(Enum):
    MEMBER1 = value1
    MEMBER2 = value2
```

#### 4.4.3 正例代码

```python
from enum import Enum, auto, IntEnum, Flag, IntFlag, unique
from typing import List

# ========== 基本枚举 ==========
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED)         # Color.RED
print(Color.RED.name)    # RED
print(Color.RED.value)   # 1

# 访问枚举成员
print(Color(1))          # Color.RED
print(Color['RED'])      # Color.RED

# 迭代
for color in Color:
    print(color)

# 成员检查
print(Color.RED in Color)  # True

# ========== 自动值 ==========
class Status(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()

print(Status.PENDING.value)  # 1
print(Status.PROCESSING.value)  # 2

# ========== 唯一值强制 ==========
@unique
class UniqueColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    # YELLOW = 1  # ValueError: duplicate values

# ========== IntEnum ==========
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# IntEnum成员可以像整数一样比较
print(Priority.HIGH > Priority.LOW)  # True
print(Priority.HIGH + Priority.LOW)  # 4
print(Priority(2))  # Priority.MEDIUM

# ========== Flag枚举 ==========
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

# 组合权限
read_write = Permission.READ | Permission.WRITE
print(read_write)  # Permission.READ|WRITE
print(Permission.READ in read_write)  # True

# 检查权限
def check_permission(user_perm: Permission, required: Permission) -> bool:
    return required in user_perm

admin = Permission.READ | Permission.WRITE | Permission.EXECUTE
print(check_permission(admin, Permission.WRITE))  # True

# ========== 带方法的枚举 ==========
class HTTPStatus(Enum):
    OK = 200
    NOT_FOUND = 404
    ERROR = 500

    @property
    def is_success(self) -> bool:
        return 200 <= self.value < 300

    @property
    def is_error(self) -> bool:
        return self.value >= 400

    def description(self) -> str:
        descriptions = {
            HTTPStatus.OK: "Request succeeded",
            HTTPStatus.NOT_FOUND: "Resource not found",
            HTTPStatus.ERROR: "Server error"
        }
        return descriptions.get(self, "Unknown status")

print(HTTPStatus.OK.is_success)  # True
print(HTTPStatus.NOT_FOUND.is_error)  # True
print(HTTPStatus.OK.description())  # Request succeeded

# ========== 带__str__和__repr__的枚举 ==========
class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    def __str__(self) -> str:
        return self.name.capitalize()

    def __repr__(self) -> str:
        return f"Weekday.{self.name}"

    @property
    def is_weekend(self) -> bool:
        return self in (Weekday.SATURDAY, Weekday.SUNDAY)

print(str(Weekday.MONDAY))  # Monday
print(repr(Weekday.FRIDAY))  # Weekday.FRIDAY
print(Weekday.SATURDAY.is_weekend)  # True

# ========== 枚举与模式匹配 ==========
def handle_status(status: HTTPStatus) -> str:
    match status:
        case HTTPStatus.OK:
            return "Success"
        case HTTPStatus.NOT_FOUND:
            return "Not found"
        case s if s.is_error:
            return f"Error: {s.value}"
        case _:
            return "Unknown"

print(handle_status(HTTPStatus.OK))  # Success

# ========== 枚举序列化 ==========
import json

class SerializableEnum(Enum):
    def to_json(self) -> str:
        return json.dumps({"name": self.name, "value": self.value})

    @classmethod
    def from_json(cls, json_str: str) -> "SerializableEnum":
        data = json.loads(json_str)
        return cls[data["name"]]

class Direction(SerializableEnum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"

direction_json = Direction.NORTH.to_json()
print(direction_json)  # {"name": "NORTH", "value": "N"}
restored = Direction.from_json(direction_json)
print(restored)  # Direction.NORTH
```

#### 4.4.4 反例代码

```python
from enum import Enum, unique

# ========== 反例1：重复值 ==========
class BadColor(Enum):
    RED = 1
    CRIMSON = 1  # 允许，但RED和CRIMSON是同一成员的别名
    GREEN = 2

print(BadColor(1))  # BadColor.RED
print(BadColor.CRIMSON is BadColor.RED)  # True

# 使用@unique防止重复
# @unique
# class UniqueColor(Enum):
#     RED = 1
#     CRIMSON = 1  # ValueError

# ========== 反例2：修改枚举成员 ==========
class Color(Enum):
    RED = 1

c = Color.RED
# c.name = "BLUE"  # AttributeError: can't set attribute

# ========== 反例3：枚举成员比较 ==========
class Color(Enum):
    RED = 1

class Status(Enum):
    ERROR = 1

# 不同枚举的成员即使值相同也不相等
print(Color.RED == Status.ERROR)  # False

# ========== 反例4：枚举继承问题 ==========
class BaseEnum(Enum):
    A = 1

# 错误：枚举通常不用于继承
# class DerivedEnum(BaseEnum):
#     B = 2  # 可能有问题

# 正确：使用混合或组合

# ========== 反例5：枚举值类型不一致 ==========
class Inconsistent(Enum):
    INT = 1
    STR = "hello"  # 允许，但不推荐
    FLOAT = 3.14

# 推荐：保持值类型一致

# ========== 反例6：枚举实例化错误 ==========
class Color(Enum):
    RED = 1

# 错误：用不存在的值实例化
# Color(999)  # ValueError: 999 is not a valid Color

# 错误：用不存在的名称访问
# Color['PURPLE']  # KeyError: 'PURPLE'
```

---

## 第五部分：迭代器与生成器

### 5.1 迭代器协议（**iter**, **next**）

#### 5.1.1 概念定义

**迭代器（Iterator）** 是实现了迭代器协议的对象，该协议要求对象实现 `__iter__()` 和 `__next__()` 方法。迭代器允许逐个访问集合中的元素，而无需暴露底层表示。

**形式化定义：**

- `__iter__()`：返回迭代器对象自身
- `__next__()`：返回下一个元素，无元素时抛出 `StopIteration`

#### 5.1.2 语法形式

```python
class Iterator:
    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> Any:
        # 返回下一个元素或抛出StopIteration
        ...
```

#### 5.1.3 正例代码

```python
from typing import Iterator, Any, Optional

# ========== 基本迭代器 ==========
class CountDown:
    """倒计时迭代器"""

    def __init__(self, start: int):
        self.start = start
        self.current = start

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self.current < 0:
            raise StopIteration
        num = self.current
        self.current -= 1
        return num

# 使用
countdown = CountDown(5)
for num in countdown:
    print(num, end=' ')  # 5 4 3 2 1 0
print()

# ========== 集合迭代器 ==========
class LinkedList:
    """链表实现"""

    class Node:
        def __init__(self, value: Any):
            self.value = value
            self.next: Optional['LinkedList.Node'] = None

    def __init__(self):
        self.head: Optional[LinkedList.Node] = None
        self._size = 0

    def append(self, value: Any) -> None:
        new_node = self.Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def __iter__(self) -> Iterator[Any]:
        """返回生成器迭代器"""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __len__(self) -> int:
        return self._size

# 使用
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
print(list(ll))  # [1, 2, 3]

# ========== 独立迭代器类 ==========
class BinaryTree:
    """二叉树"""

    class Node:
        def __init__(self, value: Any):
            self.value = value
            self.left: Optional[BinaryTree.Node] = None
            self.right: Optional[BinaryTree.Node] = None

    def __init__(self):
        self.root: Optional[BinaryTree.Node] = None

    def insert(self, value: Any) -> None:
        if not self.root:
            self.root = self.Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: 'BinaryTree.Node', value: Any) -> None:
        if value < node.value:
            if node.left is None:
                node.left = self.Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = self.Node(value)
            else:
                self._insert_recursive(node.right, value)

class InOrderIterator:
    """中序遍历迭代器"""

    def __init__(self, root: Optional[BinaryTree.Node]):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node: Optional[BinaryTree.Node]) -> None:
        while node:
            self.stack.append(node)
            node = node.left

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        if not self.stack:
            raise StopIteration

        node = self.stack.pop()
        self._push_left(node.right)
        return node.value

class BinaryTreeWithIterator(BinaryTree):
    def inorder(self) -> InOrderIterator:
        return InOrderIterator(self.root)

# 使用
tree = BinaryTreeWithIterator()
for val in [5, 3, 7, 1, 4, 6, 8]:
    tree.insert(val)

print(list(tree.inorder()))  # [1, 3, 4, 5, 6, 7, 8]

# ========== 反向迭代器 ==========
class ReverseIterator:
    """反向迭代器"""

    def __init__(self, data: list):
        self.data = data
        self.index = len(data)

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        if self.index <= 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]

# 使用
rev = ReverseIterator([1, 2, 3, 4, 5])
print(list(rev))  # [5, 4, 3, 2, 1]

# ========== 可重复迭代 ==========
class RepeatableRange:
    """可重复迭代的范围"""

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __iter__(self) -> Iterator[int]:
        """每次返回新的迭代器"""
        return iter(range(self.start, self.end))

rr = RepeatableRange(1, 4)
print(list(rr))  # [1, 2, 3]
print(list(rr))  # [1, 2, 3] - 可以再次迭代

# ========== 迭代器工具 ==========
class PeekableIterator:
    """可预览下一个元素的迭代器"""

    def __init__(self, iterator: Iterator[Any]):
        self._iterator = iterator
        self._peeked: list[Any] = []

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        if self._peeked:
            return self._peeked.pop(0)
        return next(self._iterator)

    def peek(self, default: Any = None) -> Any:
        """预览下一个元素，不消耗"""
        if not self._peeked:
            try:
                self._peeked.append(next(self._iterator))
            except StopIteration:
                return default
        return self._peeked[0]

    def has_next(self) -> bool:
        return self.peek() is not None

# 使用
peekable = PeekableIterator(iter([1, 2, 3]))
print(peekable.peek())  # 1（预览）
print(peekable.peek())  # 1（再次预览）
print(next(peekable))   # 1（实际消耗）
print(peekable.peek())  # 2
```

#### 5.1.4 反例代码

```python
# ========== 反例1：__iter__返回非迭代器 ==========
class BadIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self.data  # 错误：返回了列表，不是self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value

# ========== 反例2：忘记抛出StopIteration ==========
class InfiniteIterator:
    """错误：永远不会停止"""

    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            self.index = 0  # 重置，永远循环
        value = self.data[self.index]
        self.index += 1
        return value

# ========== 反例3：迭代器只能使用一次 ==========
class OneTimeIterator:
    """一次性迭代器"""

    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value

oti = OneTimeIterator([1, 2, 3])
print(list(oti))  # [1, 2, 3]
print(list(oti))  # [] - 已耗尽

# 正确：每次返回新迭代器
class ReusableIterable:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return iter(self.data)  # 每次返回新的迭代器

# ========== 反例4：修改正在迭代的集合 ==========
numbers = [1, 2, 3, 4, 5]

# 错误：在迭代时修改
# for n in numbers:
#     if n % 2 == 0:
#         numbers.remove(n)  # 危险！

# 正确：创建副本
for n in numbers[:]:
    if n % 2 == 0:
        numbers.remove(n)

# 或使用列表推导式
numbers = [n for n in numbers if n % 2 != 0]

# ========== 反例5：__next__没有self参数 ==========
class BadNext:
    def __iter__(self):
        return self

    def __next__():  # 错误：缺少self
        return 1
```

---

### 5.2 生成器（yield, yield from）

#### 5.2.1 概念定义

**生成器（Generator）** 是使用 `yield` 语句的特殊函数，返回生成器迭代器。生成器函数在每次 `yield` 时暂停执行，下次调用时从暂停处继续。

**形式化定义：**

- `yield expression`：产生值并暂停
- `yield from iterable`：委托给子生成器
- 生成器是迭代器的子类型，支持 `send()`、`throw()`、`close()`

#### 5.2.2 语法形式

```python
def generator():
    yield value           # 产生值
    received = yield      # 接收值
    yield from iterable   # 委托迭代
```

#### 5.2.3 正例代码

```python
from typing import Generator, Iterator, Any

# ========== 基本生成器 ==========
def count_up(start: int, end: int) -> Generator[int, None, None]:
    """从start计数到end"""
    current = start
    while current <= end:
        yield current
        current += 1

# 使用
for num in count_up(1, 5):
    print(num, end=' ')  # 1 2 3 4 5
print()

# 手动迭代
gen = count_up(10, 15)
print(next(gen))  # 10
print(next(gen))  # 11

# ========== 生成器表达式 ==========
squares = (x ** 2 for x in range(10))
print(list(squares))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 惰性求值
evens = (x for x in range(1000000) if x % 2 == 0)
print(next(evens))  # 0
print(next(evens))  # 2

# ========== 双向通信（send）==========
def echo() -> Generator[str, str, None]:
    """回声生成器"""
    print("Generator started")
    while True:
        received = yield "Ready"
        print(f"Received: {received}")
        yield f"Echo: {received}"

e = echo()
print(next(e))  # Generator started, "Ready"
print(e.send("Hello"))  # Received: Hello, "Echo: Hello"
print(e.send("World"))  # Received: World, "Echo: World"

# ========== 带初始化的双向通信 ==========
def running_average() -> Generator[float, float, None]:
    """运行平均值"""
    total = 0.0
    count = 0
    average = None

    while True:
        term = yield average
        total += term
        count += 1
        average = total / count

avg = running_average()
next(avg)  # 初始化
print(avg.send(10))   # 10.0
print(avg.send(20))   # 15.0
print(avg.send(30))   # 20.0

# ========== yield from 委托 ==========
def sub_generator():
    """子生成器"""
    yield 1
    yield 2
    yield 3

def main_generator():
    """主生成器委托给子生成器"""
    yield "Start"
    yield from sub_generator()
    yield "End"

print(list(main_generator()))  # ['Start', 1, 2, 3, 'End']

# ========== yield from 双向通信 ==========
def delegator():
    """委托生成器"""
    print("Delegator started")
    result = yield from sub_generator_with_send()
    print(f"Sub-generator returned: {result}")
    yield f"Final: {result}"

def sub_generator_with_send():
    """支持send的子生成器"""
    total = 0
    while True:
        try:
            x = yield total
            if x is None:
                break
            total += x
        except ValueError as e:
            print(f"Caught in sub: {e}")
    return total

d = delegator()
print(next(d))       # 0
print(d.send(10))    # 10
print(d.send(20))    # 30
try:
    d.send(None)     # 结束子生成器
except StopIteration as e:
    print(f"Got: {e.value}")

# ========== 递归生成器 ==========
def tree_generator(node):
    """递归遍历树"""
    if node is None:
        return
    yield from tree_generator(node.get('left'))
    yield node.get('value')
    yield from tree_generator(node.get('right'))

tree = {
    'value': 5,
    'left': {
        'value': 3,
        'left': {'value': 1},
        'right': {'value': 4}
    },
    'right': {
        'value': 7,
        'left': {'value': 6},
        'right': {'value': 8}
    }
}

print(list(tree_generator(tree)))  # [1, 3, 4, 5, 6, 7, 8]

# ========== 生成器状态 ==========
def stateful_generator():
    """展示生成器状态"""
    try:
        yield "State 1"
        yield "State 2"
        yield "State 3"
    except GeneratorExit:
        print("Generator closed")
        raise

g = stateful_generator()
print(next(g))  # State 1
print(g.gi_frame.f_locals)  # 查看局部变量
g.close()  # 关闭生成器

# ========== 实际应用：文件分块读取 ==========
def read_in_chunks(file_path: str, chunk_size: int = 1024) -> Generator[bytes, None, None]:
    """分块读取大文件"""
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# ========== 实际应用：无限序列 ==========
def fibonacci() -> Generator[int, None, None]:
    """无限斐波那契序列"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib), end=' ')  # 0 1 1 2 3 5 8 13 21 34
print()

# ========== 实际应用：流水线处理 ==========
def read_lines(file_path: str) -> Generator[str, None, None]:
    """读取文件行"""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

def filter_comments(lines: Generator[str, None, None]) -> Generator[str, None, None]:
    """过滤注释行"""
    for line in lines:
        if not line.startswith('#'):
            yield line

def parse_key_value(lines: Generator[str, None, None]) -> Generator[tuple[str, str], None, None]:
    """解析键值对"""
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            yield key.strip(), value.strip()

# 构建处理流水线
# pipeline = parse_key_value(filter_comments(read_lines('config.txt')))
```

#### 5.2.4 反例代码

```python
# ========== 反例1：return与yield混用 ==========
def mixed_return():
    yield 1
    yield 2
    return 3  # 返回值在StopIteration中

g = mixed_return()
print(list(g))  # [1, 2]
# return值被忽略，除非使用yield from

# ========== 反例2：忘记初始化send ==========
def needs_init():
    received = yield "Ready"
    yield f"Got: {received}"

g = needs_init()
# g.send("Hello")  # TypeError: can't send non-None value to a just-started generator

# 正确：先调用next()或send(None)
print(next(g))  # Ready
print(g.send("Hello"))  # Got: Hello

# ========== 反例3：生成器表达式与列表推导混淆 ==========
# 列表推导 - 立即求值
list_result = [x ** 2 for x in range(1000000)]  # 占用大量内存

# 生成器表达式 - 惰性求值
gen_result = (x ** 2 for x in range(1000000))  # 几乎不占用内存

# ========== 反例4：生成器只能迭代一次 ==========
def gen():
    yield 1
    yield 2
    yield 3

g = gen()
print(sum(g))  # 6
print(sum(g))  # 0 - 已耗尽

# 正确：如果需要多次使用，转换为列表或重新创建

# ========== 反例5：yield from 与 return ==========
def bad_yield_from():
    result = yield from [1, 2, 3]
    # result是None，因为列表迭代器没有返回值
    yield result

print(list(bad_yield_from()))  # [1, 2, 3, None]

# 正确：使用生成器返回值
def good_sub():
    yield 1
    yield 2
    return "Done"

def good_main():
    result = yield from good_sub()
    yield result

print(list(good_main()))  # [1, 2, 'Done']
```

---

### 5.3 异步生成器（async yield）

#### 5.3.1 概念定义

**异步生成器（Async Generator）** 是使用 `async def` 和 `async for` 的生成器，支持异步迭代。Python 3.6+ 引入异步生成器，3.8+ 引入异步推导式。

**形式化定义：**

- `async def` + `yield` = 异步生成器函数
- `async for` = 异步迭代
- `async with` = 异步上下文管理器

#### 5.3.2 正例代码

```python
import asyncio
from typing import AsyncGenerator, AsyncIterator

# ========== 基本异步生成器 ==========
async def async_count(start: int, end: int, delay: float = 0.1) -> AsyncGenerator[int, None]:
    """异步计数"""
    for i in range(start, end + 1):
        await asyncio.sleep(delay)
        yield i

# 使用
async def main():
    async for num in async_count(1, 5):
        print(num, end=' ')  # 1 2 3 4 5（每隔0.1秒）
    print()

# asyncio.run(main())

# ========== 异步生成器表达式 ==========
async def async_squares(n: int) -> AsyncGenerator[int, None]:
    """异步平方生成器"""
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i ** 2

async def use_async_gen_expr():
    """使用异步生成器表达式"""
    # 异步生成器表达式
    async_gen = (x async for x in async_squares(5) if x > 5)
    async for val in async_gen:
        print(val, end=' ')  # 9 16
    print()

# ========== 异步列表推导 ==========
async def async_list_comp():
    """异步列表推导"""
    # Python 3.8+ 支持异步列表推导
    result = [x async for x in async_count(1, 5)]
    print(result)  # [1, 2, 3, 4, 5]

# ========== 异步生成器send ==========
async def async_echo() -> AsyncGenerator[str, str]:
    """异步回声生成器"""
    while True:
        received = yield "Ready"
        print(f"Async received: {received}")
        yield f"Echo: {received}"

# ========== 实际应用：异步数据获取 ==========
async def fetch_pages(urls: list[str]) -> AsyncGenerator[dict, None]:
    """异步获取页面"""
    for url in urls:
        # 模拟异步请求
        await asyncio.sleep(0.1)
        yield {"url": url, "status": 200, "content": f"Content of {url}"}

async def process_urls():
    urls = ["http://a.com", "http://b.com", "http://c.com"]
    async for page in fetch_pages(urls):
        print(f"Fetched {page['url']}: {page['status']}")

# ========== 异步生成器与同步生成器组合 ==========
def sync_data_source():
    """同步数据源"""
    for i in range(5):
        yield f"item_{i}"

async def async_processor(source) -> AsyncGenerator[str, None]:
    """异步处理器"""
    for item in source:
        await asyncio.sleep(0.01)  # 模拟异步处理
        yield item.upper()

async def combined():
    async for item in async_processor(sync_data_source()):
        print(item)

# asyncio.run(combined())
```

---

### 5.4 生成器表达式

#### 5.4.1 概念定义

**生成器表达式（Generator Expression）** 是创建生成器的紧凑语法，类似于列表推导式，但使用圆括号并返回生成器对象。

**形式化定义：**

- 语法：`(expression for item in iterable if condition)`
- 语义：惰性求值的迭代器

#### 5.4.2 正例代码

```python
from typing import Iterator
import sys

# ========== 基本生成器表达式 ==========
numbers = [1, 2, 3, 4, 5]
squares = (x ** 2 for x in numbers)
print(list(squares))  # [1, 4, 9, 16, 25]

# ========== 带条件的生成器表达式 ==========
evens = (x for x in range(20) if x % 2 == 0)
print(list(evens))  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# ========== 嵌套生成器表达式 ==========
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = (x for row in matrix for x in row)
print(list(flattened))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ========== 内存效率对比 ==========
# 列表推导 - 占用内存
list_comp = [x ** 2 for x in range(1000000)]
print(f"List size: {sys.getsizeof(list_comp)} bytes")

# 生成器表达式 - 几乎不占用内存
gen_expr = (x ** 2 for x in range(1000000))
print(f"Generator size: {sys.getsizeof(gen_expr)} bytes")

# ========== 生成器表达式作为函数参数 ==========
result = sum(x ** 2 for x in range(100))
print(result)  # 328350

result = max(len(word) for word in ["apple", "banana", "cherry"])
print(result)  # 6

# ========== 组合生成器表达式 ==========
def positive_integers() -> Iterator[int]:
    """正整数生成器"""
    n = 1
    while True:
        yield n
        n += 1

# 组合多个生成器表达式
primes = (
    n for n in positive_integers()
    if n > 1 and all(n % d != 0 for d in range(2, int(n ** 0.5) + 1))
)

# 获取前10个素数
for _ in range(10):
    print(next(primes), end=' ')  # 2 3 5 7 11 13 17 19 23 29
print()

# ========== 生成器表达式与字典/集合 ==========
# 字典推导
dict_gen = {x: x ** 2 for x in range(5)}
print(dict_gen)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 集合推导
set_gen = {x % 3 for x in range(10)}
print(set_gen)  # {0, 1, 2}

# ========== 惰性管道 ==========
def read_lines(file_path: str) -> Iterator[str]:
    """读取文件行"""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

def filter_empty(lines: Iterator[str]) -> Iterator[str]:
    """过滤空行"""
    return (line for line in lines if line)

def extract_words(lines: Iterator[str]) -> Iterator[str]:
    """提取单词"""
    return (word for line in lines for word in line.split())

def filter_long_words(words: Iterator[str], min_len: int = 5) -> Iterator[str]:
    """过滤长单词"""
    return (word for word in words if len(word) >= min_len)

# 构建处理管道（惰性求值）
# pipeline = filter_long_words(extract_words(filter_empty(read_lines('text.txt'))))
```

---

## 第六部分：上下文管理器

### 6.1 with语句原理

#### 6.1.1 概念定义

**上下文管理器（Context Manager）** 是定义运行时上下文的对象，使用 `with` 语句管理资源的获取和释放。上下文管理器确保资源正确清理，即使在发生异常时。

**形式化定义：**

- `__enter__()`：进入上下文，返回值绑定到 `as` 变量
- `__exit__()`：退出上下文，处理异常

#### 6.1.2 语法形式

```python
with expression [as variable]:
    with-block

# 等价于
context = expression
variable = context.__enter__()
try:
    with-block
finally:
    context.__exit__(exc_type, exc_val, exc_tb)
```

---

### 6.2 上下文管理器协议（**enter**, **exit**）

#### 6.2.1 正例代码

```python
from typing import Optional, Type
import time

# ========== 基本上下文管理器 ==========
class Timer:
    """计时上下文管理器"""

    def __enter__(self) -> "Timer":
        self.start = time.time()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any]
    ) -> bool:
        self.end = time.time()
        self.elapsed = self.end - self.start
        print(f"Elapsed: {self.elapsed:.4f} seconds")
        return False  # 不抑制异常

# 使用
with Timer() as t:
    time.sleep(0.1)
# Elapsed: 0.1001 seconds

# ========== 资源管理上下文管理器 ==========
class ManagedResource:
    """管理资源的生命周期"""

    def __init__(self, name: str):
        self.name = name
        self.is_open = False

    def __enter__(self) -> "ManagedResource":
        print(f"Opening resource: {self.name}")
        self.is_open = True
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any]
    ) -> bool:
        print(f"Closing resource: {self.name}")
        self.is_open = False
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False

    def do_work(self) -> str:
        if not self.is_open:
            raise RuntimeError("Resource not open")
        return f"Working with {self.name}"

# 使用
with ManagedResource("database") as resource:
    print(resource.do_work())
# Opening resource: database
# Working with database
# Closing resource: database

# ========== 异常处理上下文管理器 ==========
class Suppress:
    """抑制指定异常"""

    def __init__(self, *exceptions: Type[BaseException]):
        self.exceptions = exceptions

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any]
    ) -> bool:
        if exc_type and issubclass(exc_type, self.exceptions):
            print(f"Suppressed: {exc_val}")
            return True  # 抑制异常
        return False

# 使用
with Suppress(ZeroDivisionError):
    result = 1 / 0  # 不会抛出异常
print("Continue after suppressed exception")

# ========== 返回值上下文管理器 ==========
class DatabaseConnection:
    """数据库连接"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    def __enter__(self) -> "DatabaseConnection.Cursor":
        print(f"Connecting to {self.connection_string}")
        self.connection = f"Connection({self.connection_string})"
        return self.Cursor(self)

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any]
    ) -> bool:
        print("Closing connection")
        self.connection = None
        return False

    class Cursor:
        def __init__(self, conn: "DatabaseConnection"):
            self.conn = conn

        def execute(self, query: str) -> list:
            print(f"Executing: {query}")
            return [{"id": 1, "name": "Alice"}]

# 使用
with DatabaseConnection("postgresql://localhost") as cursor:
    results = cursor.execute("SELECT * FROM users")
    print(results)

# ========== 重入上下文管理器 ==========
class ReentrantLock:
    """可重入锁"""

    def __init__(self):
        self._owner = None
        self._count = 0

    def __enter__(self) -> "ReentrantLock":
        import threading
        current = threading.current_thread()
        if self._owner is None or self._owner == current:
            self._owner = current
            self._count += 1
            print(f"Lock acquired, count: {self._count}")
        else:
            raise RuntimeError("Lock held by another thread")
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any]
    ) -> bool:
        self._count -= 1
        if self._count == 0:
            self._owner = None
        print(f"Lock released, count: {self._count}")
        return False

# 使用
lock = ReentrantLock()
with lock:
    print("First level")
    with lock:
        print("Second level")
```

---

### 6.3 contextlib模块

#### 6.3.1 正例代码

```python
from contextlib import contextmanager, closing, suppress, ExitStack
from typing import Generator
import tempfile
import os

# ========== @contextmanager装饰器 ==========
@contextmanager
def managed_file(filename: str, mode: str = 'r') -> Generator:
    """管理文件上下文"""
    print(f"Opening {filename}")
    f = open(filename, mode)
    try:
        yield f
    finally:
        print(f"Closing {filename}")
        f.close()

# 使用
# with managed_file('test.txt', 'w') as f:
#     f.write('Hello')

# ========== 计时装饰器版本 ==========
@contextmanager
def timer(name: str = "Operation") -> Generator[None, None, None]:
    """计时上下文管理器（装饰器版本）"""
    import time
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{name} took {elapsed:.4f} seconds")

# 使用
with timer("Sleep operation"):
    import time
    time.sleep(0.1)

# ========== 临时目录上下文管理器 ==========
@contextmanager
def temp_directory() -> Generator[str, None, None]:
    """创建临时目录，退出时自动清理"""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()
    print(f"Created temp directory: {temp_dir}")
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)
        print(f"Removed temp directory: {temp_dir}")

# 使用
# with temp_directory() as tmpdir:
#     file_path = os.path.join(tmpdir, 'test.txt')
#     with open(file_path, 'w') as f:
#         f.write('test')

# ========== closing上下文管理器 ==========
class Resource:
    """需要显式关闭的资源"""
    def __init__(self, name: str):
        self.name = name
        self.closed = False

    def close(self):
        print(f"Closing {self.name}")
        self.closed = True

# 使用closing
with closing(Resource("test")) as r:
    print(f"Using {r.name}")
# Closing test

# ========== suppress上下文管理器 ==========
from contextlib import suppress

# 抑制特定异常
with suppress(FileNotFoundError):
    os.remove('nonexistent_file.txt')
print("Continue after suppressed exception")

# 等价于
try:
    os.remove('nonexistent_file.txt')
except FileNotFoundError:
    pass

# ========== ExitStack ==========
with ExitStack() as stack:
    # 动态管理多个上下文
    files = []
    for filename in ['file1.txt', 'file2.txt', 'file3.txt']:
        try:
            f = stack.enter_context(open(filename, 'w'))
            files.append(f)
        except FileNotFoundError:
            pass

    # 所有文件会在此自动关闭
    print(f"Opened {len(files)} files")

# ========== 异步上下文管理器装饰器 ==========
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def async_timer(name: str = "Operation"):
    """异步计时上下文管理器"""
    start = asyncio.get_event_loop().time()
    try:
        yield
    finally:
        elapsed = asyncio.get_event_loop().time() - start
        print(f"{name} took {elapsed:.4f} seconds")

# 使用
async def async_main():
    async with async_timer("Async operation"):
        await asyncio.sleep(0.1)

# asyncio.run(async_main())

# ========== redirect_stdout/stderr ==========
from contextlib import redirect_stdout, redirect_stderr
import io

output = io.StringIO()
with redirect_stdout(output):
    print("This goes to StringIO")
    print("Not to console")

print(f"Captured: {output.getvalue()}")
```

---

### 6.4 异步上下文管理器

#### 6.4.1 正例代码

```python
import asyncio
from typing import AsyncGenerator, Optional, Type

# ========== 基本异步上下文管理器 ==========
class AsyncResource:
    """异步资源管理"""

    async def __aenter__(self) -> "AsyncResource":
        print("Async: Acquiring resource")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any]
    ) -> bool:
        print("Async: Releasing resource")
        await asyncio.sleep(0.1)
        return False

    async def do_work(self) -> str:
        await asyncio.sleep(0.05)
        return "Work done"

# 使用
async def use_async_resource():
    async with AsyncResource() as resource:
        result = await resource.do_work()
        print(result)

# asyncio.run(use_async_resource())

# ========== 异步数据库连接池 ==========
class AsyncConnectionPool:
    """异步数据库连接池"""

    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections = []
        self.in_use = set()

    async def __aenter__(self) -> "AsyncConnectionPool":
        print("Initializing connection pool")
        for i in range(self.max_connections):
            self.connections.append(f"Connection-{i}")
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any]
    ) -> bool:
        print("Closing all connections")
        self.connections.clear()
        self.in_use.clear()
        return False

    async def acquire(self) -> str:
        """获取连接"""
        while not self.connections:
            await asyncio.sleep(0.01)
        conn = self.connections.pop()
        self.in_use.add(conn)
        return conn

    async def release(self, conn: str) -> None:
        """释放连接"""
        self.in_use.discard(conn)
        self.connections.append(conn)

# 使用
async def use_pool():
    async with AsyncConnectionPool(5) as pool:
        conn = await pool.acquire()
        print(f"Using {conn}")
        await pool.release(conn)

# asyncio.run(use_pool())

# ========== 异步上下文管理器装饰器 ==========
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_transaction() -> AsyncGenerator[str, None]:
    """异步事务上下文"""
    print("BEGIN TRANSACTION")
    try:
        yield "transaction_active"
        print("COMMIT")
    except Exception as e:
        print(f"ROLLBACK: {e}")
        raise

# 使用
async def use_transaction():
    async with async_transaction() as tx:
        print(f"In transaction: {tx}")
        # 模拟操作
        await asyncio.sleep(0.1)

# asyncio.run(use_transaction())

# ========== 异步ExitStack ==========
from contextlib import AsyncExitStack

async def use_async_exit_stack():
    async with AsyncExitStack() as stack:
        resources = []
        for i in range(3):
            resource = await stack.enter_async_context(AsyncResource())
            resources.append(resource)
        print(f"Managing {len(resources)} resources")
    print("All resources released")

# asyncio.run(use_async_exit_stack())
```

---

## 第七部分：装饰器

### 7.1 函数装饰器

#### 7.1.1 概念定义

**装饰器（Decorator）** 是修改函数或类行为的函数。装饰器使用 `@decorator` 语法糖，本质上是一个返回函数的高阶函数。

**形式化定义：**

- `@decorator` 等价于 `function = decorator(function)`
- 装饰器可以带参数：`@decorator(args)`

#### 7.1.2 语法形式

```python
@decorator
def function():
    pass

# 等价于
def function():
    pass
function = decorator(function)
```

#### 7.1.3 正例代码

```python
from functools import wraps
from typing import Callable, Any
import time

# ========== 基本装饰器 ==========
def my_decorator(func: Callable) -> Callable:
    """基本装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After calling {func.__name__}")
        return result
    return wrapper

@my_decorator
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"

print(greet("Alice"))
# Before calling greet
# After calling greet
# Hello, Alice!

# ========== 计时装饰器 ==========
def timer(func: Callable) -> Callable:
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.1)
    return "Done"

slow_function()

# ========== 日志装饰器 ==========
def log_call(func: Callable) -> Callable:
    """调用日志装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

@log_call
def add(a: int, b: int) -> int:
    return a + b

add(3, 4)

# ========== 重试装饰器 ==========
def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.1)
def unreliable_function():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return "Success"

# unreliable_function()

# ========== 缓存装饰器 ==========
def memoize(func: Callable) -> Callable:
    """简单缓存装饰器"""
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(30))  # 快速计算

# ========== 权限检查装饰器 ==========
def require_permission(permission: str):
    """权限检查装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(user: dict, *args, **kwargs):
            if permission not in user.get('permissions', []):
                raise PermissionError(f"Missing permission: {permission}")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_permission("admin")
def delete_user(user: dict, user_id: int) -> str:
    return f"User {user_id} deleted"

admin = {'name': 'Admin', 'permissions': ['admin', 'read']}
# print(delete_user(admin, 123))

# ========== 类型检查装饰器 ==========
def type_check(*types):
    """类型检查装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for (arg, expected_type) in zip(args, types):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Expected {expected_type.__name__}, "
                        f"got {type(arg).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@type_check(int, int)
def safe_add(a: int, b: int) -> int:
    return a + b

print(safe_add(3, 4))  # 7
# safe_add("3", 4)  # TypeError

# ========== 单例装饰器 ==========
def singleton(cls: type) -> type:
    """单例装饰器"""
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class Database:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

db1 = Database("postgresql://localhost")
db2 = Database("mysql://localhost")
print(db1 is db2)  # True
```

---

### 7.2 类装饰器

#### 7.2.1 正例代码

```python
from typing import Type, Callable, Any
from functools import wraps

# ========== 基本类装饰器 ==========
def add_repr(cls: Type) -> Type:
    """添加__repr__方法的装饰器"""
    def __repr__(self):
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    cls.__repr__ = __repr__
    return cls

@add_repr
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(p)  # Person(name='Alice', age=30)

# ========== 注册类装饰器 ==========
registry: dict[str, Type] = {}

def register(name: str):
    """类注册装饰器"""
    def decorator(cls: Type) -> Type:
        registry[name] = cls
        return cls
    return decorator

@register("email")
class EmailSender:
    def send(self, message: str) -> str:
        return f"Email: {message}"

@register("sms")
class SMSSender:
    def send(self, message: str) -> str:
        return f"SMS: {message}"

print(registry)

# ========== 属性注入装饰器 ==========
def add_properties(**properties: Any):
    """注入类属性的装饰器"""
    def decorator(cls: Type) -> Type:
        for name, value in properties.items():
            setattr(cls, name, value)
        return cls
    return decorator

@add_properties(VERSION="1.0", AUTHOR="Alice")
class MyClass:
    pass

print(MyClass.VERSION)  # 1.0
print(MyClass.AUTHOR)   # Alice

# ========== 方法注入装饰器 ==========
def add_method(name: str, func: Callable):
    """注入方法的装饰器"""
    def decorator(cls: Type) -> Type:
        setattr(cls, name, func)
        return cls
    return decorator

def greet(self):
    return f"Hello from {self.__class__.__name__}"

@add_method("greet", greet)
class Greeter:
    pass

g = Greeter()
print(g.greet())  # Hello from Greeter

# ========== 抽象方法检查装饰器 ==========
def require_abstract_methods(*methods: str):
    """要求实现抽象方法的装饰器"""
    def decorator(cls: Type) -> Type:
        for method in methods:
            if not hasattr(cls, method) or not callable(getattr(cls, method)):
                raise TypeError(f"{cls.__name__} must implement {method}()")
        return cls
    return decorator

@require_abstract_methods("process", "validate")
class DataProcessor:
    def process(self, data: str) -> str:
        return data.upper()

    def validate(self, data: str) -> bool:
        return len(data) > 0

# ========== 混入装饰器 ==========
def mixin(*mixins: Type):
    """混入类装饰器"""
    def decorator(cls: Type) -> Type:
        for mixin_cls in mixins:
            for name in dir(mixin_cls):
                if not name.startswith('_'):
                    setattr(cls, name, getattr(mixin_cls, name))
        return cls
    return decorator

class JSONMixin:
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__)

class ComparableMixin:
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

@mixin(JSONMixin, ComparableMixin)
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

p = Product("Apple", 1.5)
print(p.to_json())  # {"name": "Apple", "price": 1.5}
```

---

### 7.3 带参数的装饰器

#### 7.3.1 正例代码

```python
from functools import wraps
from typing import Callable, Any

# ========== 三层嵌套装饰器 ==========
def decorator_with_args(arg1: Any, arg2: Any = None):
    """带参数的装饰器"""
    def actual_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Decorator args: {arg1}, {arg2}")
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator

@decorator_with_args("hello", 42)
def my_function():
    return "result"

my_function()

# ========== 灵活的参数装饰器 ==========
def flexible_decorator(*decorator_args, **decorator_kwargs):
    """灵活的参数装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Decorator received: {decorator_args}, {decorator_kwargs}")
            print(f"Function received: {args}, {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@flexible_decorator("arg1", "arg2", key="value")
def example(a: int, b: int) -> int:
    return a + b

example(1, 2)

# ========== 可带参数也可不带参数的装饰器 ==========
def optional_args_decorator(func: Callable = None, *, prefix: str = ""):
    """可选参数的装饰器"""
    def actual_decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"{prefix}Calling {f.__name__}")
            return f(*args, **kwargs)
        return wrapper

    if func is None:
        # 被调用时带参数：@decorator(prefix="...")
        return actual_decorator
    else:
        # 被调用时不带参数：@decorator
        return actual_decorator(func)

# 不带参数使用
@optional_args_decorator
def func1():
    return "func1"

# 带参数使用
@optional_args_decorator(prefix="[DEBUG] ")
def func2():
    return "func2"

func1()
func2()

# ========== 参数验证装饰器 ==========
def validate_types(**types: type):
    """类型验证装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 验证位置参数
            arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
            for arg, name in zip(args, arg_names):
                if name in types and not isinstance(arg, types[name]):
                    raise TypeError(
                        f"{name} should be {types[name].__name__}, "
                        f"got {type(arg).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def create_person(name: str, age: int) -> dict:
    return {"name": name, "age": age}

print(create_person("Alice", 30))
# create_person("Bob", "thirty")  # TypeError

# ========== 条件装饰器 ==========
def conditional(condition: bool, decorator: Callable) -> Callable:
    """条件装饰器"""
    def actual_decorator(func: Callable) -> Callable:
        if condition:
            return decorator(func)
        return func
    return actual_decorator

def log_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Logging: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

DEBUG = True

@conditional(DEBUG, log_decorator)
def sensitive_operation():
    return "Secret data"

sensitive_operation()
```

---

### 7.4 functools.wraps

#### 7.4.1 概念定义

**`functools.wraps`** 是装饰器辅助函数，用于保留被装饰函数的元数据（`__name__`、`__doc__`、 `__module__` 等）。

#### 7.4.2 正例代码

```python
from functools import wraps
import functools

# ========== 不使用wraps的问题 ==========
def bad_decorator(func):
    """问题装饰器 - 不使用wraps"""
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_function():
    """Original docstring"""
    return "result"

print(my_function.__name__)  # wrapper（丢失了原函数名）
print(my_function.__doc__)   # Wrapper docstring（丢失了原文档）

# ========== 使用wraps ==========
def good_decorator(func):
    """正确装饰器 - 使用wraps"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_function2():
    """Original docstring"""
    return "result"

print(my_function2.__name__)  # my_function2（正确）
print(my_function2.__doc__)   # Original docstring（正确）

# ========== wraps保留的属性 ==========
def inspect_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@inspect_decorator
def example_func(a: int, b: str) -> bool:
    """Example function"""
    return True

print(f"__name__: {example_func.__name__}")
print(f"__doc__: {example_func.__doc__}")
print(f"__module__: {example_func.__module__}")
print(f"__annotations__: {example_func.__annotations__}")
print(f"__qualname__: {example_func.__qualname__}")

# ========== 自定义wraps ==========
def custom_wraps(func):
    """自定义wraps - 添加额外功能"""
    def decorator(wrapper_func):
        wrapper_func = functools.wraps(func)(wrapper_func)
        wrapper_func._decorated = True
        wrapper_func._original = func
        return wrapper_func
    return decorator

@custom_wraps
def my_func():
    pass

@my_decorator
def my_func2():
    pass

print(hasattr(my_func2, '_decorated'))  # True
print(my_func2._original.__name__)  # my_func2

# ========== 类方法装饰器中的wraps ==========
def method_decorator(func):
    """类方法装饰器"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"Calling {func.__name__} on {self}")
        return func(self, *args, **kwargs)
    return wrapper

class MyClass:
    @method_decorator
    def do_something(self):
        """Do something"""
        return "done"

obj = MyClass()
print(obj.do_something.__name__)  # do_something
print(obj.do_something.__doc__)   # Do something

# ========== 属性装饰器中的wraps ==========
def property_decorator(func):
    """属性装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class Example:
    @property
    @property_decorator
    def value(self):
        """Get value"""
        return 42

e = Example()
print(Example.value.fget.__name__)  # value
print(Example.value.fget.__doc__)   # Get value
```

---

## 总结

本文档全面梳理了Python 3.12+的全部核心语言特性，涵盖：

1. **核心语法特性**：类型注解、模式匹配、海象运算符、f-string、解包
2. **数据模型与特殊方法**：`__slots__`、描述符协议、`@property`、元类、抽象基类
3. **函数式编程特性**：lambda、高阶函数、itertools/functools、偏函数
4. **面向对象高级特性**：多重继承与MRO、混入模式、数据类、枚举类
5. **迭代器与生成器**：迭代器协议、生成器、异步生成器、生成器表达式
6. **上下文管理器**：with语句、上下文管理器协议、contextlib、异步上下文管理器
7. **装饰器**：函数装饰器、类装饰器、带参数的装饰器、`functools.wraps`

每个特性都包含概念定义、语法形式、属性关系、正例、反例和形式论证，确保读者能够全面理解并正确使用Python的这些高级特性。

---

*文档版本：1.0*
*适用Python版本：3.12+*
*最后更新：2024年*
