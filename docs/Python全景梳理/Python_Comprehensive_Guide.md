# Python 最新版本全面技术指南

> 基于 Python 3.12+ 的完整技术梳理
>
> 涵盖语言特性、设计模式、并发并行、分布式系统、架构设计、可观测性、CI/CD、AI/ML

---

## 目录

- [Python 最新版本全面技术指南](#python-最新版本全面技术指南)
  - [目录](#目录)
  - [文档统计](#文档统计)
  - [第一部分：语言特性全面梳理](#第一部分语言特性全面梳理)
    - [1.1 核心语法特性](#11-核心语法特性)
      - [类型注解系统（Type Hints）](#类型注解系统type-hints)
      - [模式匹配（Structural Pattern Matching）](#模式匹配structural-pattern-matching)
      - [海象运算符（Walrus Operator）](#海象运算符walrus-operator)
    - [1.2 数据模型与特殊方法](#12-数据模型与特殊方法)
      - [`__slots__` 机制](#__slots__-机制)
      - [描述符协议](#描述符协议)
    - [1.3 函数式编程特性](#13-函数式编程特性)
    - [1.4 面向对象高级特性](#14-面向对象高级特性)
      - [多重继承与MRO](#多重继承与mro)
      - [数据类（@dataclass）](#数据类dataclass)
    - [1.5 迭代器与生成器](#15-迭代器与生成器)
    - [1.6 上下文管理器](#16-上下文管理器)
    - [1.7 装饰器](#17-装饰器)
  - [第二部分：包管理与标准库](#第二部分包管理与标准库)
    - [2.1 包管理工具对比](#21-包管理工具对比)
    - [2.2 pyproject.toml 标准配置](#22-pyprojecttoml-标准配置)
    - [2.3 标准库核心模块速查](#23-标准库核心模块速查)
      - [collections 模块](#collections-模块)
      - [itertools 模块](#itertools-模块)
      - [functools 模块](#functools-模块)
  - [第三部分：程序设计机制](#第三部分程序设计机制)
    - [3.1 编程范式对比](#31-编程范式对比)
    - [3.2 类型系统形式化](#32-类型系统形式化)
    - [3.3 内存模型](#33-内存模型)
    - [3.4 错误处理模式](#34-错误处理模式)
  - [第四部分：设计模式](#第四部分设计模式)
    - [4.1 创建型模式](#41-创建型模式)
      - [单例模式（线程安全）](#单例模式线程安全)
      - [建造者模式](#建造者模式)
    - [4.2 结构型模式](#42-结构型模式)
      - [装饰器模式（与Python装饰器区分）](#装饰器模式与python装饰器区分)
    - [4.3 行为型模式](#43-行为型模式)
      - [观察者模式](#观察者模式)
  - [第五部分：并发并行同步异步](#第五部分并发并行同步异步)
    - [5.1 并发模型选择指南](#51-并发模型选择指南)
    - [5.2 asyncio 核心模式](#52-asyncio-核心模式)
    - [5.3 并发原语](#53-并发原语)
    - [5.4 死锁避免](#54-死锁避免)
  - [第六部分：分布式设计模型](#第六部分分布式设计模型)
    - [6.1 CAP定理形式化](#61-cap定理形式化)
    - [6.2 熔断器模式](#62-熔断器模式)
    - [6.3 分布式事务 - Saga模式](#63-分布式事务---saga模式)
  - [第七部分：工作流设计模式](#第七部分工作流设计模式)
    - [7.1 23种可判断模式概览](#71-23种可判断模式概览)
    - [7.2 工作流模式Python实现](#72-工作流模式python实现)
  - [第八部分：架构设计模型](#第八部分架构设计模型)
    - [8.1 架构模式选择指南](#81-架构模式选择指南)
    - [8.2 领域驱动设计（DDD）Python实现](#82-领域驱动设计dddpython实现)
    - [8.3 六边形架构（端口与适配器）](#83-六边形架构端口与适配器)
  - [第九部分：可观测性与eBPF](#第九部分可观测性与ebpf)
    - [9.1 OpenTelemetry Python实现](#91-opentelemetry-python实现)
    - [9.2 Prometheus指标暴露](#92-prometheus指标暴露)
  - [第十部分：CI/CD与AI/ML](#第十部分cicd与aiml)
    - [10.1 GitHub Actions 完整配置](#101-github-actions-完整配置)
    - [10.2 MLOps - MLflow完整示例](#102-mlops---mlflow完整示例)
    - [10.3 RAG系统实现](#103-rag系统实现)
  - [附录：综合速查表](#附录综合速查表)
    - [Python版本特性演进](#python版本特性演进)
    - [设计模式速查](#设计模式速查)
    - [并发模型选择](#并发模型选择)
    - [架构选择矩阵](#架构选择矩阵)
  - [完整文档文件列表](#完整文档文件列表)

---

## 文档统计

| 章节 | 文件 | 大小 | 行数 |
|------|------|------|------|
| 第一部分 | 语言特性 | 197 KB | 7,341 |
| 第二部分 | 包管理与标准库 | 173 KB | 6,644 |
| 第三部分 | 程序设计机制 | 80 KB | 3,162 |
| 第四部分 | 设计模式 | 232 KB | 8,880 |
| 第五部分 | 并发并行 | 107 KB | 3,676 |
| 第六部分 | 分布式系统 | 297 KB | 8,772 |
| 第七部分 | 工作流模式 | 117 KB | 3,973 |
| 第八部分 | 架构设计 | 326 KB | 9,279 |
| 第九部分 | 可观测性/eBPF | 28 KB | 889 |
| 第十部分 | CI/CD与AI/ML | 203 KB | 7,124 |
| **总计** | - | **1.78 MB** | **59,740** |

---

## 第一部分：语言特性全面梳理

*详细内容见：`01_python_language_features.md`*

### 1.1 核心语法特性

#### 类型注解系统（Type Hints）

```python
from typing import List, Dict, Optional, Union, Callable, Generic, TypeVar

# 基本类型注解
def greet(name: str) -> str:
    return f"Hello, {name}"

# 复杂类型
T = TypeVar('T')

def process_items(items: List[Dict[str, Union[int, str]]]) -> Optional[T]:
    pass

# Callable类型
handler: Callable[[int, str], bool] = lambda x, y: True
```

**概念定义**：类型注解是Python 3.5+引入的静态类型提示机制，不影响运行时行为，用于静态类型检查。

**形式论证**：

- 设程序P，类型系统T
- 若P通过T的类型检查，则P在类型安全方面具有形式保证
- Python采用渐进式类型（Gradual Typing），允许混合使用类型化和非类型化代码

#### 模式匹配（Structural Pattern Matching）

```python
def handle_command(command: str) -> str:
    match command.split():
        case ["quit"]:
            return "Exiting..."
        case ["load", filename] if filename.endswith(".txt"):
            return f"Loading {filename}"
        case ["save", filename, *options]:
            return f"Saving {filename} with {options}"
        case _:
            return "Unknown command"
```

**概念定义**：模式匹配是Python 3.10+引入的结构化匹配机制，支持值匹配、序列解构、映射解构和类模式。

#### 海象运算符（Walrus Operator）

```python
# 在while循环中使用
while (line := input()) != "quit":
    print(f"Processing: {line}")

# 在列表推导中使用
results = [y for x in data if (y := process(x)) > 0]
```

**概念定义**：`:=` 运算符允许在表达式内部进行赋值并返回赋值结果。

**正例 vs 反例**：

```python
# 正例：减少重复计算
if (n := len(data)) > 10:
    print(f"Data has {n} items")  # n可复用

# 反例：滥用导致可读性下降
if (x := 1) and (y := 2) and (z := x + y):
    pass  # 过于复杂，应拆分为多行
```

### 1.2 数据模型与特殊方法

#### `__slots__` 机制

```python
class Point:
    __slots__ = ['x', 'y']  # 限制属性，节省内存

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# 正例：大量对象时节省内存
points = [Point(i, i) for i in range(1000000)]  # 内存占用显著降低

# 反例：需要动态属性时
p = Point(1, 2)
p.z = 3  # AttributeError: 'Point' object has no attribute 'z'
```

#### 描述符协议

```python
class Validator:
    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"{self.name} must be in [{self.min_value}, {self.max_value}]")
        setattr(obj, self.private_name, value)

class Temperature:
    celsius = Validator(-273.15, 1000)

    def __init__(self, celsius: float):
        self.celsius = celsius
```

### 1.3 函数式编程特性

```python
from functools import reduce, partial
from itertools import groupby, chain, combinations

# 高阶函数
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
product = reduce(lambda x, y: x * y, numbers)

# 偏函数
base_two_log = partial(lambda base, x: __import__('math').log(x, base), 2)

# 迭代器工具
for combo in combinations([1, 2, 3, 4], 2):
    print(combo)
```

### 1.4 面向对象高级特性

#### 多重继承与MRO

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):  # MRO: D -> B -> C -> A
    pass

d = D()
print(d.method())  # "B"
print(D.__mro__)   # (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

#### 数据类（@dataclass）

```python
from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True, order=True)
class Person:
    name: str
    age: int = field(default=0, compare=False)
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")

# 使用
p1 = Person("Alice", 30, ["developer"])
p2 = Person("Bob", 25)
print(p1 == p2)  # False
print(p1 < p2)   # True (按name排序)
```

### 1.5 迭代器与生成器

```python
# 生成器函数
def fibonacci(n: int):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# 生成器表达式
squares = (x**2 for x in range(1000000))  # 惰性求值，节省内存

# 异步生成器
async def async_data_stream():
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i

# yield from 委托
def combined_gen():
    yield from range(3)
    yield from "abc"
```

### 1.6 上下文管理器

```python
from contextlib import contextmanager, asynccontextmanager

# 类式上下文管理器
class DatabaseConnection:
    def __enter__(self):
        self.conn = create_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return False  # 不抑制异常

# 函数式上下文管理器
@contextmanager
def managed_resource(name: str):
    resource = acquire(name)
    try:
        yield resource
    finally:
        release(resource)

# 异步上下文管理器
@asynccontextmanager
async def async_managed_resource():
    resource = await async_acquire()
    try:
        yield resource
    finally:
        await async_release(resource)
```

### 1.7 装饰器

```python
from functools import wraps
import time

# 函数装饰器
def timing_decorator(func):
    @wraps(func)  # 保留原函数元数据
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

# 带参数的装饰器
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# 类装饰器
def singleton(cls):
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class Database:
    pass
```

---

## 第二部分：包管理与标准库

*详细内容见：`02_python_packaging_stdlib.md`*

### 2.1 包管理工具对比

| 工具 | 依赖锁定 | 虚拟环境 | 构建后端 | 适用场景 |
|------|----------|----------|----------|----------|
| pip | requirements.txt | 需配合venv | 可选 | 简单项目 |
| Poetry | poetry.lock | 内置 | 内置 | 现代Python项目 |
| PDM | pdm.lock | 内置 | 内置 | 与PEP标准对齐 |
| uv | uv.lock | 内置 | 内置 | 极速安装 |
| conda | conda-lock | 内置 | 内置 | 数据科学 |

### 2.2 pyproject.toml 标准配置

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "1.0.0"
description = "A sample package"
readme = "README.md"
license = {text = "MIT"}
authors = [{name = "Author", email = "author@example.com"}]
requires-python = ">=3.10"
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
]
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = ["pytest", "black", "mypy"]

[tool.black]
line-length = 88
target-version = ['py310']

[tool.mypy]
python_version = "3.10"
strict = true
```

### 2.3 标准库核心模块速查

#### collections 模块

```python
from collections import Counter, defaultdict, OrderedDict, deque, namedtuple

# Counter - 计数器
counter = Counter(['a', 'b', 'a', 'c', 'a'])
print(counter.most_common(2))  # [('a', 3), ('b', 1)]

# defaultdict - 默认字典
grouped = defaultdict(list)
for item in items:
    grouped[item.category].append(item)

# deque - 双端队列
d = deque(maxlen=100)  # 固定长度，自动淘汰
d.appendleft(item)
d.pop()

# namedtuple - 命名元组
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)
```

#### itertools 模块

```python
from itertools import (
    count, cycle, repeat,           # 无限迭代器
    chain, compress, dropwhile,     # 筛选
    groupby, tee,                   # 分组和复制
    product, permutations, combinations  # 组合
)

# 无限迭代器
for i in count(10, 2):  # 10, 12, 14, ...
    if i > 20: break

# 链式迭代
all_items = chain(list1, list2, list3)

# 分组（需先排序）
for key, group in groupby(sorted(data, key=lambda x: x.category),
                          key=lambda x: x.category):
    print(key, list(group))

# 笛卡尔积
for x, y in product([1, 2], ['a', 'b']):
    print(x, y)  # (1,a), (1,b), (2,a), (2,b)
```

#### functools 模块

```python
from functools import lru_cache, wraps, partial, reduce, cmp_to_key

# 缓存装饰器
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 比较函数转key函数
def compare(x, y):
    return (x > y) - (x < y)

sorted_list = sorted(data, key=cmp_to_key(compare))
```

---

## 第三部分：程序设计机制

*详细内容见：`03_programming_mechanisms.md`*

### 3.1 编程范式对比

| 范式 | 核心思想 | Python支持 | 适用场景 |
|------|----------|------------|----------|
| 命令式 | 状态+语句序列 | 原生 | 通用编程 |
| 函数式 | 纯函数+不可变 | 部分支持 | 数据处理 |
| 面向对象 | 对象+消息传递 | 原生 | 复杂系统建模 |
| 声明式 | 描述"是什么" | 部分支持 | 配置、查询 |

### 3.2 类型系统形式化

**鸭子类型（Duck Typing）形式定义**：

```
给定对象 o 和协议 P = {m₁, m₂, ..., mₙ}
o 满足 P 当且仅当：∀mᵢ ∈ P, ∃ o.mᵢ

即：不检查类型，只检查行为
```

```python
# 鸭子类型示例
class Duck:
    def quack(self): return "Quack!"
    def fly(self): return "Flying..."

class Person:
    def quack(self): return "I'm quacking!"
    def fly(self): return "I'm flying!"

def make_it_quack_and_fly(duck_like):
    """不检查类型，只检查方法存在"""
    print(duck_like.quack())
    print(duck_like.fly())

make_it_quack_and_fly(Duck())   # 正常工作
make_it_quack_and_fly(Person()) # 同样正常工作
```

### 3.3 内存模型

```python
import sys
import gc

# 引用计数
a = []
b = a
print(sys.getrefcount(a))  # 3 (a, b, getrefcount参数)

# 垃圾回收
class Node:
    def __init__(self):
        self.ref = None
    def __del__(self):
        print("Node deleted")

# 循环引用
n1 = Node()
n2 = Node()
n1.ref = n2
n2.ref = n1

del n1, n2
gc.collect()  # 强制垃圾回收

# GIL影响分析
import threading
import time

def cpu_bound_task():
    count = 0
    for i in range(10_000_000):
        count += i
    return count

# 多线程无法加速CPU密集型任务（GIL限制）
start = time.time()
threads = [threading.Thread(target=cpu_bound_task) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Multi-threaded: {time.time() - start:.2f}s")

# 多进程可以加速
from multiprocessing import Process
start = time.time()
processes = [Process(target=cpu_bound_task) for _ in range(2)]
for p in processes: p.start()
for p in processes: p.join()
print(f"Multi-process: {time.time() - start:.2f}s")
```

### 3.4 错误处理模式

```python
from typing import Optional, Union
from dataclasses import dataclass

# Result类型模式（函数式错误处理）
@dataclass
class Ok:
    value: any

@dataclass
class Err:
    error: Exception

Result = Union[Ok, Err]

def divide(a: float, b: float) -> Result:
    if b == 0:
        return Err(ZeroDivisionError("Cannot divide by zero"))
    return Ok(a / b)

# 使用
result = divide(10, 0)
match result:
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

---

## 第四部分：设计模式

*详细内容见：`04_design_patterns.md`*

### 4.1 创建型模式

#### 单例模式（线程安全）

```python
import threading
from functools import wraps

def thread_safe_singleton(cls):
    instances = {}
    lock = threading.Lock()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            with lock:
                # 双重检查锁定
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@thread_safe_singleton
class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = "Connected"
        return self.connection
```

#### 建造者模式

```python
from typing import Self

class Computer:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None

    def __str__(self):
        return f"Computer(cpu={self.cpu}, memory={self.memory}GB, storage={self.storage}GB)"

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu: str) -> Self:
        self.computer.cpu = cpu
        return self

    def set_memory(self, memory: int) -> Self:
        self.computer.memory = memory
        return self

    def set_storage(self, storage: int) -> Self:
        self.computer.storage = storage
        return self

    def build(self) -> Computer:
        return self.computer

# 使用
computer = (ComputerBuilder()
    .set_cpu("Intel i9")
    .set_memory(32)
    .set_storage(1000)
    .build())
```

### 4.2 结构型模式

#### 装饰器模式（与Python装饰器区分）

```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: pass

    @abstractmethod
    def description(self) -> str: pass

class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 10.0

    def description(self) -> str:
        return "Simple coffee"

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()

class Milk(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 2.0

    def description(self) -> str:
        return self._coffee.description() + ", milk"

class Sugar(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return self._coffee.description() + ", sugar"

# 使用
coffee = Sugar(Milk(SimpleCoffee()))
print(f"{coffee.description()} = ${coffee.cost()}")
```

### 4.3 行为型模式

#### 观察者模式

```python
from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    @abstractmethod
    def update(self, subject: 'Subject') -> None: pass

class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []
        self._state = None

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.notify()

class ConcreteSubject(Subject):
    pass

class EmailObserver(Observer):
    def update(self, subject: Subject) -> None:
        print(f"Email: State changed to {subject.state}")

class SMSObserver(Observer):
    def update(self, subject: Subject) -> None:
        print(f"SMS: State changed to {subject.state}")

# 使用
subject = ConcreteSubject()
subject.attach(EmailObserver())
subject.attach(SMSObserver())
subject.state = "Active"  # 自动通知所有观察者
```

---

## 第五部分：并发并行同步异步

*详细内容见：`05_concurrency_parallelism.md`*

### 5.1 并发模型选择指南

| 场景 | 推荐模型 | 原因 |
|------|----------|------|
| I/O密集型 | asyncio | 协程开销小，可处理大量连接 |
| CPU密集型 | multiprocessing | 绕过GIL，利用多核 |
| 混合场景 | ProcessPoolExecutor + asyncio | 各取所长 |
| 简单并行 | concurrent.futures | 接口简洁 |

### 5.2 asyncio 核心模式

```python
import asyncio
from asyncio import Queue, Task

# 生产者-消费者模式
async def producer(queue: Queue, n: int):
    for i in range(n):
        await asyncio.sleep(0.1)  # 模拟生产
        await queue.put(i)
        print(f"Produced {i}")
    await queue.put(None)  # 结束信号

async def consumer(queue: Queue, name: str):
    while True:
        item = await queue.get()
        if item is None:  # 结束信号
            break
        await asyncio.sleep(0.2)  # 模拟消费
        print(f"Consumer {name} processed {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=10)

    producers = [asyncio.create_task(producer(queue, 5)) for _ in range(2)]
    consumers = [asyncio.create_task(consumer(queue, f"C{i}")) for i in range(3)]

    await asyncio.gather(*producers)
    await queue.join()  # 等待所有任务完成

    # 发送结束信号
    for _ in consumers:
        await queue.put(None)
    await asyncio.gather(*consumers)

asyncio.run(main())
```

### 5.3 并发原语

```python
import asyncio
from asyncio import Lock, Semaphore, Event, Condition

# 互斥锁
class SharedResource:
    def __init__(self):
        self._value = 0
        self._lock = Lock()

    async def increment(self):
        async with self._lock:
            current = self._value
            await asyncio.sleep(0)  # 模拟操作
            self._value = current + 1
            return self._value

# 信号量（限制并发数）
semaphore = Semaphore(5)  # 最多5个并发

async def limited_task(task_id: int):
    async with semaphore:
        print(f"Task {task_id} started")
        await asyncio.sleep(1)
        print(f"Task {task_id} completed")

# 事件（信号通知）
event = Event()

async def waiter():
    print("Waiting for event...")
    await event.wait()
    print("Event received!")

async def setter():
    await asyncio.sleep(2)
    event.set()
    print("Event set!")
```

### 5.4 死锁避免

```python
import asyncio
from asyncio import Lock

# 死锁示例（反例）
async def deadlock_example():
    lock1 = Lock()
    lock2 = Lock()

    async def task1():
        async with lock1:
            await asyncio.sleep(0.1)
            async with lock2:  # 等待task2释放lock2
                print("Task 1")

    async def task2():
        async with lock2:
            await asyncio.sleep(0.1)
            async with lock1:  # 等待task1释放lock1 - 死锁！
                print("Task 2")

    await asyncio.gather(task1(), task2())  # 死锁！

# 解决方案：按固定顺序获取锁
async def safe_example():
    lock1 = Lock()
    lock2 = Lock()
    locks = [lock1, lock2]  # 固定顺序

    async def task():
        async with locks[0]:
            async with locks[1]:
                print("Safe execution")

    await asyncio.gather(task(), task())
```

---

## 第六部分：分布式设计模型

*详细内容见：`06_distributed_systems.md`*

### 6.1 CAP定理形式化

```
CAP定理：分布式系统最多同时满足以下两项：
- C (Consistency): 所有节点在同一时间看到相同数据
- A (Availability): 每个请求都能收到非错误响应
- P (Partition tolerance): 网络分区时系统仍能运行

证明概要：
1. 假设网络分区发生
2. 若要保持一致性，必须等待分区恢复 → 牺牲可用性
3. 若要保持可用性，必须允许分区期间数据不一致 → 牺牲一致性
∴ P发生时，C和A不可兼得
```

### 6.2 熔断器模式

```python
import time
from enum import Enum, auto
from dataclasses import dataclass
from typing import Callable, Optional

class CircuitState(Enum):
    CLOSED = auto()      # 正常
    OPEN = auto()        # 熔断
    HALF_OPEN = auto()   # 半开测试

@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    half_open_max_calls: int = 3

    def __post_init__(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_calls = 0

    def call(self, func: Callable, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise Exception("Circuit breaker is OPEN")

        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise Exception("Circuit breaker is HALF_OPEN (max calls reached)")
            self.half_open_calls += 1

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_max_calls:
                self.state = CircuitState.CLOSED
                self.success_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# 使用
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=5.0)

def unreliable_service():
    import random
    if random.random() < 0.7:
        raise Exception("Service failed")
    return "Success"

for i in range(10):
    try:
        result = breaker.call(unreliable_service)
        print(f"Call {i}: {result}")
    except Exception as e:
        print(f"Call {i}: {e}")
```

### 6.3 分布式事务 - Saga模式

```python
from abc import ABC, abstractmethod
from typing import List, Callable
from dataclasses import dataclass

@dataclass
class SagaStep:
    action: Callable
    compensation: Callable
    name: str

class Saga:
    def __init__(self):
    self.steps: List[SagaStep] = []
        self.completed_steps: List[SagaStep] = []

    def add_step(self, action: Callable, compensation: Callable, name: str):
        self.steps.append(SagaStep(action, compensation, name))
        return self

    def execute(self):
        for step in self.steps:
            try:
                print(f"Executing: {step.name}")
                step.action()
                self.completed_steps.append(step)
            except Exception as e:
                print(f"Failed at {step.name}: {e}")
                self.compensate()
                raise SagaFailedException(f"Saga failed at {step.name}")

    def compensate(self):
        print("Starting compensation...")
        for step in reversed(self.completed_steps):
            try:
                print(f"Compensating: {step.name}")
                step.compensation()
            except Exception as e:
                print(f"Compensation failed for {step.name}: {e}")
                # 记录需要人工处理的补偿失败

class SagaFailedException(Exception):
    pass

# 使用示例：订单处理Saga
def create_order():
    print("Order created")

def cancel_order():
    print("Order cancelled")

def reserve_inventory():
    print("Inventory reserved")

def release_inventory():
    print("Inventory released")

def process_payment():
    import random
    if random.random() < 0.5:
        raise Exception("Payment failed")
    print("Payment processed")

def refund_payment():
    print("Payment refunded")

saga = (Saga()
    .add_step(create_order, cancel_order, "Create Order")
    .add_step(reserve_inventory, release_inventory, "Reserve Inventory")
    .add_step(process_payment, refund_payment, "Process Payment")
)

try:
    saga.execute()
    print("Order completed successfully!")
except SagaFailedException:
    print("Order failed, compensation completed")
```

---

## 第七部分：工作流设计模式

*详细内容见：`07_workflow_patterns.md`*

### 7.1 23种可判断模式概览

| 模式 | 可判定性 | 时间复杂度 | 说明 |
|------|----------|------------|------|
| 顺序 | ✅ | O(n) | 线性执行 |
| 并行分支 | ✅ | O(m) | AND-Split |
| 同步 | ✅ | O(m) | AND-Join |
| 排他选择 | ✅ | O(k²) | XOR-Split |
| 简单合并 | ✅ | O(1) | XOR-Join |
| 多选 | ✅ | O(2ⁿ) | OR-Split |
| 结构化同步合并 | ✅ | O(n) | OR-Join |
| 多合并 | ✅ | O(m) | 多入单出 |
| 鉴别器 | ✅ | O(n) | N选1 |
| 部分加入 | ✅ | O(N) | M-out-of-N |
| 任意循环 | ⚠️ | - | 部分可判定 |
| 隐式终止 | ✅ | O(\|T\|) | 无显式结束 |
| 延迟选择 | ✅ | O(k) | 运行时决策 |
| 里程碑 | ✅ | O(1) | 状态检查点 |
| 关键区域 | ✅ | O(n²) | 互斥区 |
| 取消任务 | ✅ | O(1) | 活动取消 |
| 取消案例 | ✅ | O(\|T\|) | 流程取消 |

### 7.2 工作流模式Python实现

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Set, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import asyncio

class TokenState(Enum):
    ACTIVE = auto()
    COMPLETED = auto()
    CANCELLED = auto()

@dataclass
class Token:
    id: str
    data: Dict = field(default_factory=dict)
    state: TokenState = TokenState.ACTIVE

class Node(ABC):
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.inputs: List['Node'] = []
        self.outputs: List['Node'] = []
        self.tokens: List[Token] = []

    @abstractmethod
    async def execute(self, token: Token) -> List[Token]:
        pass

    def add_output(self, node: 'Node'):
        self.outputs.append(node)
        node.inputs.append(self)

# 顺序模式（可判定：O(n)）
class SequenceNode(Node):
    """顺序执行节点"""
    async def execute(self, token: Token) -> List[Token]:
        print(f"SequenceNode {self.node_id} executing")
        token.state = TokenState.COMPLETED
        return [token]

# 并行分支模式（可判定：O(m)）
class ParallelSplitNode(Node):
    """AND-Split: 一个输入，多个并行输出"""
    async def execute(self, token: Token) -> List[Token]:
        print(f"ParallelSplitNode {self.node_id} splitting to {len(self.outputs)} branches")
        # 为每个输出分支创建新token
        return [Token(id=f"{token.id}_{i}", data=token.data.copy())
                for i in range(len(self.outputs))]

# 同步模式（可判定：O(m)）
class SynchronizationNode(Node):
    """AND-Join: 等待所有输入分支完成"""
    def __init__(self, node_id: str, expected_inputs: int):
        super().__init__(node_id)
        self.expected_inputs = expected_inputs
        self.received_tokens: List[Token] = []

    async def execute(self, token: Token) -> List[Token]:
        self.received_tokens.append(token)
        print(f"SynchronizationNode {self.node_id} received {len(self.received_tokens)}/{self.expected_inputs}")

        if len(self.received_tokens) >= self.expected_inputs:
            # 合并所有token数据
            merged_data = {}
            for t in self.received_tokens:
                merged_data.update(t.data)
            self.received_tokens = []
            return [Token(id=f"sync_{self.node_id}", data=merged_data)]
        return []  # 继续等待

# 排他选择模式（可判定：O(k²)）
class ExclusiveChoiceNode(Node):
    """XOR-Split: 根据条件选择一个分支"""
    def __init__(self, node_id: str):
        super().__init__(node_id)
        self.conditions: List[Callable[[Dict], bool]] = []

    def add_conditional_output(self, node: Node, condition: Callable[[Dict], bool]):
        self.add_output(node)
        self.conditions.append(condition)

    async def execute(self, token: Token) -> List[Token]:
        for i, condition in enumerate(self.conditions):
            if condition(token.data):
                print(f"ExclusiveChoiceNode {self.node_id} selected branch {i}")
                # 只返回一个token给选中的分支
                result = [Token(id=f"{token.id}_choice_{i}", data=token.data.copy())]
                # 其他分支需要取消（发送取消token）
                for j in range(len(self.outputs)):
                    if j != i:
                        cancel_token = Token(id=f"{token.id}_cancel_{j}", data=token.data.copy())
                        cancel_token.state = TokenState.CANCELLED
                return result
        # 默认选择第一个
        return [Token(id=f"{token.id}_choice_default", data=token.data.copy())]

# 工作流引擎
class WorkflowEngine:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}

    def add_node(self, node: Node):
        self.nodes[node.node_id] = node

    async def execute(self, start_node_id: str, initial_data: Dict = None):
        start_node = self.nodes[start_node_id]
        initial_token = Token(id="start", data=initial_data or {})

        # BFS执行
        queue = [(start_node, initial_token)]
        completed_tokens = []

        while queue:
            current_node, token = queue.pop(0)

            if token.state == TokenState.CANCELLED:
                continue

            output_tokens = await current_node.execute(token)

            for i, output_token in enumerate(output_tokens):
                if output_token.state == TokenState.COMPLETED:
                    completed_tokens.append(output_token)

                if i < len(current_node.outputs):
                    next_node = current_node.outputs[i]
                    queue.append((next_node, output_token))

        return completed_tokens

# 使用示例
async def demo():
    engine = WorkflowEngine()

    # 创建节点
    start = SequenceNode("start")
    split = ParallelSplitNode("split")
    task_a = SequenceNode("task_a")
    task_b = SequenceNode("task_b")
    sync = SynchronizationNode("sync", 2)
    end = SequenceNode("end")

    # 连接节点
    start.add_output(split)
    split.add_output(task_a)
    split.add_output(task_b)
    task_a.add_output(sync)
    task_b.add_output(sync)
    sync.add_output(end)

    # 添加到引擎
    for node in [start, split, task_a, task_b, sync, end]:
        engine.add_node(node)

    # 执行
    result = await engine.execute("start", {"order_id": "12345"})
    print(f"Workflow completed with {len(result)} tokens")

asyncio.run(demo())
```

---

## 第八部分：架构设计模型

*详细内容见：`08_architecture_patterns.md`*

### 8.1 架构模式选择指南

| 架构 | 复杂度 | 可扩展性 | 适用场景 |
|------|--------|----------|----------|
| 分层架构 | 低 | 中 | 传统企业应用 |
| 微服务 | 高 | 高 | 大型分布式系统 |
| 事件驱动 | 中 | 高 | 实时处理、流式数据 |
| DDD | 中 | 高 | 复杂业务领域 |
| 六边形架构 | 中 | 高 | 需要可测试性的系统 |
| Serverless | 低 | 高 | 事件触发、间歇性负载 |

### 8.2 领域驱动设计（DDD）Python实现

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid

# 值对象（不可变，通过属性相等判断）
@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

# 实体（有唯一标识）
class Entity:
    def __init__(self):
        self.id = str(uuid.uuid4())

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class OrderLine(Entity):
    def __init__(self, product_id: str, product_name: str,
                 quantity: int, unit_price: Money):
        super().__init__()
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def total_price(self) -> Money:
        return Money(
            self.unit_price.amount * self.quantity,
            self.unit_price.currency
        )

# 聚合根
class Order(Entity):
    def __init__(self, customer_id: str):
        super().__init__()
        self.customer_id = customer_id
        self._lines: List[OrderLine] = []
        self._total: Money = Money(0, "USD")
        self._status = "pending"
        self._created_at = datetime.now()
        self._version = 0  # 乐观锁

    def add_line(self, line: OrderLine):
        if self._status != "pending":
            raise ValueError("Cannot modify submitted order")
        self._lines.append(line)
        self._total = self._total.add(line.total_price)
        self._version += 1

    def submit(self):
        if not self._lines:
            raise ValueError("Cannot submit empty order")
        self._status = "submitted"
        self._version += 1

    @property
    def total(self) -> Money:
        return self._total

    @property
    def status(self) -> str:
        return self._status

# 仓储接口
class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]: pass

    @abstractmethod
    def save(self, order: Order) -> None: pass

    @abstractmethod
    def delete(self, order_id: str) -> None: pass

# 领域服务
class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    def create_order(self, customer_id: str) -> Order:
        order = Order(customer_id)
        self._order_repo.save(order)
        return order

    def add_item_to_order(self, order_id: str, product_id: str,
                          product_name: str, quantity: int,
                          unit_price: Money) -> None:
        order = self._order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")

        line = OrderLine(product_id, product_name, quantity, unit_price)
        order.add_line(line)
        self._order_repo.save(order)

    def submit_order(self, order_id: str) -> None:
        order = self._order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        order.submit()
        self._order_repo.save(order)
```

### 8.3 六边形架构（端口与适配器）

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

# 领域层（核心）
@dataclass
class Product:
    id: str
    name: str
    price: float

class ProductRepository(ABC):
    """端口：定义领域需要的接口"""
    @abstractmethod
    def get_by_id(self, product_id: str) -> Optional[Product]: pass

    @abstractmethod
    def save(self, product: Product) -> None: pass

    @abstractmethod
    def list_all(self) -> List[Product]: pass

class ProductService:
    """领域服务"""
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._repository.get_by_id(product_id)

    def create_product(self, product_id: str, name: str, price: float) -> Product:
        if price < 0:
            raise ValueError("Price cannot be negative")
        product = Product(product_id, name, price)
        self._repository.save(product)
        return product

# 适配器层
class InMemoryProductRepository(ProductRepository):
    """内存适配器（测试用）"""
    def __init__(self):
        self._products: dict = {}

    def get_by_id(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def save(self, product: Product) -> None:
        self._products[product.id] = product

    def list_all(self) -> List[Product]:
        return list(self._products.values())

class SQLProductRepository(ProductRepository):
    """数据库适配器（生产用）"""
    def __init__(self, connection_string: str):
        self._conn = connection_string

    def get_by_id(self, product_id: str) -> Optional[Product]:
        # SQL查询实现
        pass

    def save(self, product: Product) -> None:
        # SQL插入/更新实现
        pass

    def list_all(self) -> List[Product]:
        # SQL查询实现
        pass

# 应用层（用例）
class ProductUseCases:
    def __init__(self, product_service: ProductService):
        self._product_service = product_service

    def handle_get_product(self, product_id: str) -> dict:
        product = self._product_service.get_product(product_id)
        if not product:
            return {"error": "Product not found"}
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }

    def handle_create_product(self, data: dict) -> dict:
        try:
            product = self._product_service.create_product(
                data["id"], data["name"], data["price"]
            )
            return {"id": product.id, "status": "created"}
        except ValueError as e:
            return {"error": str(e)}

# 基础设施层（Web适配器）
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 依赖注入（实际项目中使用依赖注入框架）
repository = InMemoryProductRepository()  # 或 SQLProductRepository
product_service = ProductService(repository)
product_use_cases = ProductUseCases(product_service)

class CreateProductRequest(BaseModel):
    id: str
    name: str
    price: float

@app.get("/products/{product_id}")
def get_product(product_id: str):
    result = product_use_cases.handle_get_product(product_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.post("/products")
def create_product(request: CreateProductRequest):
    result = product_use_cases.handle_create_product(request.dict())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
```

---

## 第九部分：可观测性与eBPF

*详细内容见：`09_observability_ebpf.md`*

### 9.1 OpenTelemetry Python实现

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.propagate import extract, inject
from functools import wraps

# 配置资源
resource = Resource(attributes={SERVICE_NAME: "my-service"})

# 配置Tracer
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
trace.set_tracer_provider(trace_provider)

# 配置Meter
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metrics_provider)

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# 创建指标
counter = meter.create_counter(
    "request_count",
    description="Number of requests",
    unit="1"
)

histogram = meter.create_histogram(
    "request_duration",
    description="Request duration",
    unit="ms"
)

# 装饰器自动追踪
def traced(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with tracer.start_as_current_span(func.__name__) as span:
            span.set_attribute("function.args", str(args))
            span.set_attribute("function.kwargs", str(kwargs))

            import time
            start = time.time()
            try:
                result = func(*args, **kwargs)
                span.set_attribute("result", str(result))
                span.set_status(trace.Status(trace.StatusCode.OK))
                return result
            except Exception as e:
                span.set_attribute("error", str(e))
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
            finally:
                duration = (time.time() - start) * 1000
                histogram.record(duration)
                counter.add(1)
    return wrapper

# 使用
@traced
def process_order(order_id: str):
    # 业务逻辑
    return f"Processed {order_id}"

process_order("12345")
```

### 9.2 Prometheus指标暴露

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Flask, Response
import time
import random

app = Flask(__name__)

# 定义指标
REQUEST_COUNT = Counter(
    'app_request_count',
    'Total request count',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'app_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'app_active_connections',
    'Number of active connections'
)

# 中间件
@app.before_request
def before_request():
    ACTIVE_CONNECTIONS.inc()
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.endpoint
    ).observe(random.random())

@app.after_request
def after_request(response):
    ACTIVE_CONNECTIONS.dec()
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint,
        status=response.status_code
    ).inc()
    return response

# 指标端点
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/')
def index():
    time.sleep(random.random())
    return "Hello World"

if __name__ == '__main__':
    app.run(port=5000)
```

---

## 第十部分：CI/CD与AI/ML

*详细内容见：`10_cicd_ai_ml.md`*

### 10.1 GitHub Actions 完整配置

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Lint with flake8
      run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

    - name: Type check with mypy
      run: mypy src/

    - name: Test with pytest
      run: pytest --cov=src --cov-report=xml --cov-report=html

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .
        docker tag myapp:${{ github.sha }} myapp:latest

    - name: Push to registry
      if: github.ref == 'refs/heads/main'
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push myapp:${{ github.sha }}
        docker push myapp:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - name: Deploy to production
      run: |
        # 蓝绿部署或金丝雀部署
        kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
        kubectl rollout status deployment/myapp
```

### 10.2 MLOps - MLflow完整示例

```python
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 配置MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("iris-classification")

def train_and_log_model():
    # 加载数据
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    # 超参数搜索空间
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7],
        'min_samples_split': [2, 5, 10]
    }

    with mlflow.start_run() as run:
        # 记录参数
        mlflow.log_param("model_type", "RandomForest")
        mlflow.log_param("test_size", 0.2)

        # 网格搜索
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_

        # 评估
        y_pred = best_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # 记录指标
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("best_cv_score", grid_search.best_score_)

        # 记录最佳参数
        for param_name, param_value in grid_search.best_params_.items():
            mlflow.log_param(f"best_{param_name}", param_value)

        # 记录模型
        mlflow.sklearn.log_model(
            best_model,
            "model",
            registered_model_name="iris-random-forest"
        )

        # 记录特征重要性
        import matplotlib.pyplot as plt
        importances = best_model.feature_importances_
        plt.figure(figsize=(10, 6))
        plt.bar(iris.feature_names, importances)
        plt.title("Feature Importances")
        plt.tight_layout()
        plt.savefig("feature_importances.png")
        mlflow.log_artifact("feature_importances.png")

        # 记录分类报告
        report = classification_report(y_test, y_pred, target_names=iris.target_names)
        with open("classification_report.txt", "w") as f:
            f.write(report)
        mlflow.log_artifact("classification_report.txt")

        print(f"Run ID: {run.info.run_id}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Best params: {grid_search.best_params_}")

# 模型服务
import mlflow.pyfunc

def load_and_predict(model_name: str, model_version: str, data):
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.pyfunc.load_model(model_uri)
    return model.predict(data)

if __name__ == "__main__":
    train_and_log_model()
```

### 10.3 RAG系统实现

```python
from typing import List
from dataclasses import dataclass
import numpy as np
from openai import OpenAI
import faiss

@dataclass
class Document:
    id: str
    content: str
    embedding: np.ndarray = None

class VectorStore:
    """向量存储（使用FAISS）"""
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # 内积（余弦相似度）
        self.documents: List[Document] = []

    def add_documents(self, documents: List[Document]):
        embeddings = np.array([doc.embedding for doc in documents])
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(documents)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Document]:
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        return [self.documents[i] for i in indices[0]]

class RAGSystem:
    """检索增强生成系统"""
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.vector_store = VectorStore()

    def embed_text(self, text: str) -> np.ndarray:
        """生成文本嵌入"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return np.array(response.data[0].embedding)

    def add_knowledge_base(self, documents: List[str]):
        """添加知识库文档"""
        docs = []
        for i, content in enumerate(documents):
            embedding = self.embed_text(content)
            docs.append(Document(
                id=f"doc_{i}",
                content=content,
                embedding=embedding
            ))
        self.vector_store.add_documents(docs)

    def query(self, question: str, k: int = 3) -> str:
        """RAG查询"""
        # 1. 检索相关文档
        query_embedding = self.embed_text(question)
        relevant_docs = self.vector_store.search(query_embedding, k)

        # 2. 构建上下文
        context = "\n\n".join([doc.content for doc in relevant_docs])

        # 3. 生成回答
        prompt = f"""基于以下上下文回答问题。如果上下文不包含答案，请说明。

上下文：
{context}

问题：{question}

回答："""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一个有帮助的助手，基于提供的上下文回答问题。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

# 使用示例
rag = RAGSystem("your-api-key")

# 添加知识库
documents = [
    "Python是一种高级编程语言，由Guido van Rossum于1991年创建。",
    "Python支持多种编程范式，包括面向对象、函数式和过程式编程。",
    "Python的GIL（全局解释器锁）限制了多线程的并行执行。",
    "asyncio是Python用于编写并发代码的库，使用async/await语法。"
]
rag.add_knowledge_base(documents)

# 查询
answer = rag.query("Python的GIL是什么？")
print(answer)
```

---

## 附录：综合速查表

### Python版本特性演进

| 版本 | 主要特性 |
|------|----------|
| 3.8 | Walrus运算符 `:=`, positional-only参数, f-string `=` |
| 3.9 | 字典合并 `\|`, 类型注解泛型内置 |
| 3.10 | 模式匹配 `match/case`, 联合类型 `X \| Y` |
| 3.11 | 性能提升10-60%, 异常组, TOML解析器 |
| 3.12 | f-string嵌套, 类型参数语法, 性能优化 |
| 3.13 | 实验性JIT, 改进解释器, 移除死电池 |

### 设计模式速查

| 类型 | 模式 | 使用场景 |
|------|------|----------|
| 创建型 | 单例 | 全局唯一实例 |
| 创建型 | 工厂 | 对象创建逻辑复杂 |
| 结构型 | 适配器 | 接口不兼容 |
| 结构型 | 装饰器 | 动态添加功能 |
| 行为型 | 观察者 | 事件订阅 |
| 行为型 | 策略 | 算法可替换 |

### 并发模型选择

| 场景 | 模型 | 库 |
|------|------|-----|
| I/O密集型 | 异步 | asyncio |
| CPU密集型 | 多进程 | multiprocessing |
| 混合 | 进程池+协程 | ProcessPoolExecutor + asyncio |

### 架构选择矩阵

| 因素 | 分层 | 微服务 | 事件驱动 | DDD |
|------|------|--------|----------|-----|
| 复杂度 | 低 | 高 | 中 | 中 |
| 可扩展性 | 中 | 高 | 高 | 高 |
| 团队规模 | 小 | 大 | 中 | 中 |
| 领域复杂度 | 低 | 中 | 中 | 高 |

---

## 完整文档文件列表

| 文件 | 内容 | 大小 |
|------|------|------|
| `01_python_language_features.md` | 语言特性全面梳理 | 197 KB |
| `02_python_packaging_stdlib.md` | 包管理与标准库 | 173 KB |
| `03_programming_mechanisms.md` | 程序设计机制 | 80 KB |
| `04_design_patterns.md` | 设计模式（GoF 23种） | 232 KB |
| `05_concurrency_parallelism.md` | 并发并行同步异步 | 107 KB |
| `06_distributed_systems.md` | 分布式设计模型 | 297 KB |
| `07_workflow_patterns.md` | 工作流设计模式（43种） | 117 KB |
| `08_architecture_patterns.md` | 架构设计模型 | 326 KB |
| `09_observability_ebpf.md` | 可观测性与eBPF | 28 KB |
| `10_cicd_ai_ml.md` | CI/CD与AI/ML | 203 KB |
| `workflow_patterns_impl.py` | 工作流模式Python实现 | 75 KB |

---

*本文档由多专业子代理协作生成，涵盖Python 3.12+全部核心技术领域*
