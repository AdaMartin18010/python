# Pythonic 惯用法

**编写优雅、地道的 Python 代码**-

---

## 🐍 什么是 Pythonic？

"Pythonic" 指的是充分利用 Python 语言特性，编写简洁、可读、高效的代码。

> "There should be one-- and preferably only one --obvious way to do it."  
> —— The Zen of Python

---

## 📚 目录

- [1. 核心惯用法速查](#1-核心惯用法速查)
  - [1.1 序列操作](#11-序列操作)
  - [1.2 字典操作](#12-字典操作)
  - [1.3 列表推导式](#13-列表推导式)
  - [1.4 真值测试](#14-真值测试)
  - [1.5 字符串操作](#15-字符串操作)
- [2. 函数式编程](#2-函数式编程)
- [3. 上下文管理器](#3-上下文管理器)
- [4. 生成器与迭代器](#4-生成器与迭代器)
- [5. 异步编程模式](#5-异步编程模式)
- [6. 性能优化技巧](#6-性能优化技巧)
- [7. 反模式（避免）](#7-反模式避免)
- [8. 延伸阅读](#8-延伸阅读)

> **详细文档**:
> 1. [基础惯用法](01-basic-idioms.md) - Python 基础惯用法
> 2. [集合与迭代](02-collections-iteration.md) - 数据结构和迭代技巧
> 3. [函数式编程](03-functional-programming.md) - 函数式编程模式
> 4. [上下文管理器](04-context-managers.md) - 资源管理最佳实践
> 5. [生成器与迭代器](05-generators-iterators.md) - 惰性求值技术
> 6. [异步编程模式](06-async-patterns.md) - 现代异步编程
> 7. [性能优化技巧](07-performance-tips.md) - 性能优化实践

---

## 1. 核心惯用法速查

### 1.1 序列操作

```python
# ✅ 使用切片
numbers = [1, 2, 3, 4, 5]
first_three = numbers[:3]  # [1, 2, 3]
last_two = numbers[-2:]    # [4, 5]
reversed_nums = numbers[::-1]  # [5, 4, 3, 2, 1]

# ✅ 序列解包
a, b, c = [1, 2, 3]
first, *middle, last = [1, 2, 3, 4, 5]  # first=1, middle=[2,3,4], last=5

# ✅ 使用 enumerate
for i, value in enumerate(["a", "b", "c"]):
    print(f"{i}: {value}")

# ✅ 使用 zip 并行迭代
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")
```

### 1.2 字典操作

```python
# ✅ 字典推导式
squares = {x: x**2 for x in range(5)}

# ✅ get() 方法提供默认值
count = counts.get(key, 0)

# ✅ setdefault() 设置默认值
cache.setdefault(key, []).append(value)

# ✅ 字典合并 (Python 3.9+)
combined = dict1 | dict2

# ✅ 遍历字典
for key, value in my_dict.items():
    print(f"{key}: {value}")
```

### 1.3 列表推导式

```python
# ✅ 基础列表推导式
squares = [x**2 for x in range(10)]

# ✅ 带条件的列表推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# ✅ 嵌套列表推导式
matrix = [[i * j for j in range(5)] for i in range(5)]

# ✅ 字典推导式
word_lengths = {word: len(word) for word in words}

# ✅ 集合推导式
unique_lengths = {len(word) for word in words}
```

### 1.4 真值测试

```python
# ✅ 直接测试真值
if my_list:  # 非空列表为 True
    process(my_list)

if not my_dict:  # 空字典为 False
    initialize()

# ✅ is None 检查
if value is None:
    handle_none()

# ❌ 避免显式比较
if len(my_list) > 0:  # 不推荐
    pass

if my_list == []:  # 不推荐
    pass
```

### 1.5 字符串操作

```python
# ✅ f-string (Python 3.6+)
name = "World"
greeting = f"Hello, {name}!"

# ✅ 多行字符串
query = """
SELECT *
FROM users
WHERE active = 1
"""

# ✅ join() 连接字符串
words = ["Hello", "World"]
sentence = " ".join(words)

# ✅ 字符串方法链
result = text.strip().lower().replace(" ", "_")
```

### 6. 函数参数

```python
# ✅ 默认参数
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# ✅ *args 和 **kwargs
def flexible_function(*args, **kwargs):
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# ✅ 仅关键字参数 (Python 3.8+)
def process(data: str, *, format: str = "json") -> None:
    pass

# 必须这样调用
process("data", format="xml")
```

### 7. 上下文管理器

```python
# ✅ with 语句
with open("file.txt") as f:
    content = f.read()

# ✅ 多个上下文管理器
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read())

# ✅ 自定义上下文管理器
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    import time
    start = time.time()
    yield
    end = time.time()
    print(f"{name} took {end - start:.2f}s")

with timer("Operation"):
    do_something()
```

### 8. 异常处理

```python
# ✅ EAFP (请求原谅比许可更容易)
try:
    value = my_dict[key]
except KeyError:
    value = default

# ❌ LBYL (三思而后行) - 不推荐
if key in my_dict:
    value = my_dict[key]
else:
    value = default

# ✅ 具体异常优先
try:
    result = risky_operation()
except ValueError as e:
    handle_value_error(e)
except TypeError as e:
    handle_type_error(e)
except Exception as e:
    handle_generic_error(e)

# ✅ else 和 finally
try:
    file = open("data.txt")
except FileNotFoundError:
    print("File not found")
else:
    data = file.read()
    file.close()
finally:
    cleanup()
```

### 9. 生成器

```python
# ✅ 生成器表达式
sum_of_squares = sum(x**2 for x in range(1000000))

# ✅ 生成器函数
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 使用
fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]

# ✅ yield from (Python 3.3+)
def chain(*iterables):
    for iterable in iterables:
        yield from iterable
```

### 10. 装饰器

```python
# ✅ 函数装饰器
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)

# ✅ 带参数的装饰器
def repeat(times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name: str):
    print(f"Hello, {name}!")
```

---

## 2. 函数式编程

### 1. 数据类 (Python 3.7+)

```python
from dataclasses import dataclass, field

@dataclass
class Person:
    name: str
    age: int
    email: str | None = None
    friends: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age must be non-negative")

# 自动生成 __init__, __repr__, __eq__ 等方法
person = Person("Alice", 30)
```

### 2. 结构化模式匹配 (Python 3.10+)

```python
def handle_command(command):
    match command.split():
        case ["quit"]:
            return "Goodbye!"
        case ["load", filename]:
            return f"Loading {filename}"
        case ["save", filename, *options]:
            return f"Saving {filename} with options {options}"
        case _:
            return "Unknown command"

# 匹配数据结构
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y-axis at {y}")
    case (x, 0):
        print(f"X-axis at {x}")
    case (x, y):
        print(f"Point at ({x}, {y})")
```

### 3. 类型守卫

```python
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(items: list[object]) -> None:
    if is_str_list(items):
        # items 现在的类型是 list[str]
        for item in items:
            print(item.upper())
```

### 4. 协议 (Protocol)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

def render(obj: Drawable) -> None:
    obj.draw()

# Circle 和 Square 自动满足 Drawable 协议
render(Circle())
render(Square())
```

### 5. 描述符

```python
class Validator:
    def __init__(self, min_value: int = 0):
        self.min_value = min_value
    
    def __set_name__(self, owner, name):
        self.name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, None)
    
    def __set__(self, obj, value):
        if value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        setattr(obj, self.name, value)

class Person:
    age = Validator(min_value=0)
    
    def __init__(self, age: int):
        self.age = age
```

---

## 7. 反模式（避免）

### 1. 避免可变默认参数

```python
# ❌ 错误
def append_to_list(item, my_list=[]):
    my_list.append(item)
    return my_list

# ✅ 正确
def append_to_list(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list
```

### 2. 避免裸 except

```python
# ❌ 错误
try:
    risky_operation()
except:  # 捕获所有异常，包括 KeyboardInterrupt
    pass

# ✅ 正确
try:
    risky_operation()
except Exception as e:  # 只捕获 Exception 及其子类
    log_error(e)
```

### 3. 避免修改正在迭代的容器

```python
# ❌ 错误
for item in my_list:
    if should_remove(item):
        my_list.remove(item)  # 可能跳过元素

# ✅ 正确
my_list = [item for item in my_list if not should_remove(item)]

# 或使用 filter
my_list = list(filter(lambda x: not should_remove(x), my_list))
```

---

## 4. 生成器与迭代器

### 1. 链式比较

```python
# ✅ Python 支持链式比较
if 0 < x < 10:
    print("x is between 0 and 10")

# 等价于
if x > 0 and x < 10:
    pass
```

### 2. 条件表达式

```python
# ✅ 三元运算符
result = value_if_true if condition else value_if_false

# 示例
status = "active" if user.is_active else "inactive"
```

### 3. 多重赋值

```python
# ✅ 交换变量
a, b = b, a

# ✅ 链式赋值
x = y = z = 0

# ✅ 增强赋值
count += 1
total *= 2
```

---

## 6. 性能优化技巧

### 1. 使用内置函数

```python
# ✅ 使用内置 sum()
total = sum(numbers)

# ❌ 手动循环
total = 0
for num in numbers:
    total += num

# ✅ 使用 any() 和 all()
has_negative = any(x < 0 for x in numbers)
all_positive = all(x > 0 for x in numbers)
```

### 2. 列表推导式 vs map/filter

```python
# ✅ 列表推导式（更 Pythonic）
squares = [x**2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]

# 也可以，但不够 Pythonic
squares = list(map(lambda x: x**2, range(10)))
evens = list(filter(lambda x: x % 2 == 0, range(10)))
```

### 3. 使用生成器节省内存

```python
# ✅ 对大数据集使用生成器
sum_of_squares = sum(x**2 for x in range(1000000))

# ❌ 创建完整列表（占用大量内存）
sum_of_squares = sum([x**2 for x in range(1000000)])
```

---

## 3. 上下文管理器

### 案例 1: 配置管理

```python
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    
    @classmethod
    def from_file(cls, path: Path) -> "Config":
        with path.open() as f:
            data = json.load(f)
        return cls(**data)
    
    def to_file(self, path: Path) -> None:
        with path.open("w") as f:
            json.dump(self.__dict__, f, indent=2)

config = Config.from_file(Path("config.json"))
```

### 案例 2: 命令模式

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    
    @abstractmethod
    def undo(self) -> None: ...

class CreateFileCommand(Command):
    def __init__(self, filename: str):
        self.filename = filename
    
    def execute(self) -> None:
        Path(self.filename).touch()
    
    def undo(self) -> None:
        Path(self.filename).unlink(missing_ok=True)

class CommandInvoker:
    def __init__(self):
        self.history: list[Command] = []
    
    def execute(self, command: Command) -> None:
        command.execute()
        self.history.append(command)
    
    def undo(self) -> None:
        if self.history:
            command = self.history.pop()
            command.undo()
```

### 案例 3: 装饰器链

```python
from functools import wraps
import time

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@log
@timer
def slow_function(n: int) -> int:
    time.sleep(n)
    return n * 2

result = slow_function(2)
```

---

## 5. 异步编程模式

（详见 [异步编程模式](06-async-patterns.md)）

---

## 8. 延伸阅读

- [PEP 20 - The Zen of Python](https://peps.python.org/pep-0020/)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Effective Python](https://effectivepython.com/)
- [Fluent Python](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)
- [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)

---

**编写 Pythonic 代码，让 Python 代码更优雅！** 🐍✨
