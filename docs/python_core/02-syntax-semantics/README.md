# Python 语法与语义

**Python 语法规则和语义模型深度解析**

---

## 📚 目录

- [1. 词法分析](#1-词法分析)
- [2. 语法结构](#2-语法结构)
- [3. 表达式语义](#3-表达式语义)
- [4. 语句语义](#4-语句语义)
- [5. 函数与闭包](#5-函数与闭包)
- [6. 类与继承](#6-类与继承)
- [7. 装饰器与元编程](#7-装饰器与元编程)
- [8. 实战案例](#8-实战案例)
- [9. 延伸阅读](#9-延伸阅读)

**相关子文档**:

- [词法分析](01-lexical.md) - Token 和词法规则
- [语法结构](02-grammar.md) - 语法规则和 BNF
- [表达式语义](03-expressions.md) - 表达式求值
- [语句语义](04-statements.md) - 语句执行
- [函数与闭包](05-functions-closures.md) - 函数机制
- [类与继承](06-classes-inheritance.md) - 面向对象
- [装饰器与元编程](07-decorators-metaprogramming.md) - 高级特性

---

## 1. 词法分析

### Token 类型

Python 源代码首先被分解为 Token：

```python
# Python Token 类型
KEYWORDS = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
    'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
    'try', 'while', 'with', 'yield', 'match', 'case', 'type'
]

# 示例：词法分析
import tokenize
import io

code = "x = 1 + 2"
tokens = tokenize.generate_tokens(io.StringIO(code).readline)

for token in tokens:
    print(token)

# 输出:
# TokenInfo(type=1 (NAME), string='x', ...)
# TokenInfo(type=54 (OP), string='=', ...)
# TokenInfo(type=2 (NUMBER), string='1', ...)
# TokenInfo(type=54 (OP), string='+', ...)
# TokenInfo(type=2 (NUMBER), string='2', ...)
```

### 标识符规则

```python
# ✅ 合法标识符
x = 1
_private = 2
__dunder__ = 3
camelCase = 4
snake_case = 5
中文变量 = 6  # Python 3+ 支持 Unicode

# ❌ 非法标识符
# 2x = 1        # 不能以数字开头
# my-var = 2    # 不能包含连字符
# class = 3     # 不能是关键字
```

### 字面量

```python
# 整数字面量
decimal = 42
binary = 0b101010
octal = 0o52
hexadecimal = 0x2A

# 浮点数字面量
float_num = 3.14
scientific = 1.5e-3
infinity = float('inf')

# 字符串字面量
single = 'hello'
double = "world"
triple = """multi
line"""
raw = r"C:\path\to\file"
formatted = f"x = {x}"
bytes_literal = b"bytes"

# 布尔和 None
true_val = True
false_val = False
none_val = None

# 集合字面量
list_literal = [1, 2, 3]
tuple_literal = (1, 2, 3)
dict_literal = {'a': 1, 'b': 2}
set_literal = {1, 2, 3}
```

---

## 2. 语法结构

### BNF 语法示例

Python 的语法可以用 BNF (Backus-Naur Form) 表示：

```bnf
# 简化的 Python 语法规则

file_input: (NEWLINE | stmt)* ENDMARKER

stmt: simple_stmt | compound_stmt

simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE

small_stmt: (expr_stmt | del_stmt | pass_stmt | flow_stmt |
             import_stmt | global_stmt | nonlocal_stmt | assert_stmt)

compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt |
               with_stmt | funcdef | classdef | match_stmt

if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]

while_stmt: 'while' test ':' suite ['else' ':' suite]

for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]
```

### 语句层次

```python
# 简单语句
x = 1           # 赋值语句
pass            # 空语句
del x           # 删除语句
return x        # 返回语句
break           # 中断语句
continue        # 继续语句

# 复合语句
if condition:   # if 语句
    pass
elif other:
    pass
else:
    pass

while condition:  # while 循环
    break

for item in items:  # for 循环
    continue

try:            # 异常处理
    risky()
except Error:
    handle()
finally:
    cleanup()

with resource:  # 上下文管理
    use()

def function(): # 函数定义
    pass

class MyClass:  # 类定义
    pass
```

---

## 3. 表达式语义

### 运算符优先级

从高到低：

```python
# 1. 括号和列表/字典/集合
(expression)
[list]
{dict}
{set}

# 2. 属性引用、下标、切片、调用
x.attribute
x[index]
x[start:stop]
x(arguments)

# 3. 幂运算
x ** y

# 4. 一元运算符
+x, -x, ~x

# 5. 乘除运算
x * y, x / y, x // y, x % y

# 6. 加减运算
x + y, x - y

# 7. 移位运算
x << y, x >> y

# 8. 按位与
x & y

# 9. 按位异或
x ^ y

# 10. 按位或
x | y

# 11. 比较运算
x < y, x <= y, x > y, x >= y, x == y, x != y
x is y, x is not y
x in y, x not in y

# 12. 布尔非
not x

# 13. 布尔与
x and y

# 14. 布尔或
x or y

# 15. 条件表达式
x if condition else y

# 16. lambda 表达式
lambda args: expression

# 17. 赋值表达式 (Python 3.8+)
(x := expression)
```

### 短路求值

```python
# and 短路：如果左边为 False，不评估右边
def expensive():
    print("Expensive computation")
    return True

result = False and expensive()  # 不会打印
result = True and expensive()   # 会打印

# or 短路：如果左边为 True，不评估右边
result = True or expensive()    # 不会打印
result = False or expensive()   # 会打印

# 实际应用
def safe_divide(a, b):
    return b != 0 and a / b  # 避免除零错误
```

### 表达式类型

```python
# 原子表达式
x                    # 标识符
42                   # 字面量
(1 + 2)             # 括号表达式

# 算术表达式
x + y               # 加法
x - y               # 减法
x * y               # 乘法
x / y               # 除法
x // y              # 整除
x % y               # 取模
x ** y              # 幂运算

# 比较表达式
x == y              # 相等
x != y              # 不等
x < y               # 小于
x > y               # 大于
x <= y              # 小于等于
x >= y              # 大于等于

# 逻辑表达式
x and y             # 逻辑与
x or y              # 逻辑或
not x               # 逻辑非

# 成员测试
x in collection     # 成员测试
x not in collection # 非成员测试

# 身份测试
x is y              # 身份测试
x is not y          # 非身份测试

# 条件表达式（三元运算符）
x if condition else y

# 赋值表达式（海象运算符，Python 3.8+）
if (n := len(items)) > 10:
    print(f"List is too long ({n} elements)")
```

---

## 4. 语句语义

### 赋值语句

```python
# 简单赋值
x = 42

# 多重赋值
x = y = z = 0

# 序列解包
a, b, c = [1, 2, 3]
first, *rest = [1, 2, 3, 4]
*head, last = [1, 2, 3, 4]

# 增强赋值
x += 1    # x = x + 1
x -= 1    # x = x - 1
x *= 2    # x = x * 2
x /= 2    # x = x / 2
x //= 2   # x = x // 2
x %= 2    # x = x % 2
x **= 2   # x = x ** 2

# 赋值表达式（Python 3.8+）
if (match := pattern.search(text)):
    print(match.group())
```

### 控制流语句

```python
# if-elif-else
x = 10
if x > 0:
    print("Positive")
elif x < 0:
    print("Negative")
else:
    print("Zero")

# while 循环
count = 0
while count < 5:
    print(count)
    count += 1
else:
    print("Loop completed")  # 正常结束时执行

# for 循环
for i in range(5):
    print(i)
else:
    print("Loop completed")  # 正常结束时执行

# break 和 continue
for i in range(10):
    if i == 3:
        continue  # 跳过 3
    if i == 7:
        break     # 在 7 时退出
    print(i)

# match-case (Python 3.10+)
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500 | 502 | 503:
            return "Server Error"
        case _:
            return "Unknown"
```

### 异常处理

```python
# try-except-else-finally
try:
    risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except (TypeError, KeyError) as e:
    print(f"Type or Key error: {e}")
except Exception as e:
    print(f"Other error: {e}")
else:
    print("No errors occurred")
finally:
    print("Always executed")

# raise 语句
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age is unrealistic")
    return age

# 异常链
try:
    process_data()
except DataError as e:
    raise ProcessingError("Failed to process") from e

# 上下文管理
with open("file.txt") as f:
    content = f.read()
```

---

## 5. 函数与闭包

### 函数定义

```python
# 基础函数
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"

# 默认参数
def power(base: float, exponent: float = 2) -> float:
    return base ** exponent

# 可变参数
def sum_all(*args: int) -> int:
    return sum(args)

def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# 仅位置参数 (Python 3.8+)
def divide(a, b, /):
    return a / b

# 仅关键字参数
def create_user(*, name: str, email: str):
    return {"name": name, "email": email}

# 混合参数
def complex_function(pos_only, /, standard, *, kw_only):
    pass
```

### 闭包

```python
# 闭包示例
def make_multiplier(n: int):
    def multiplier(x: int) -> int:
        return x * n
    return multiplier

times2 = make_multiplier(2)
times3 = make_multiplier(3)

print(times2(5))  # 10
print(times3(5))  # 15

# 闭包捕获变量
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c1 = make_counter()
print(c1())  # 1
print(c1())  # 2

# 装饰器（闭包的应用）
def timer(func):
    import time
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
```

---

## 6. 类与继承

### 类定义

```python
# 基础类
class Person:
    # 类变量
    species = "Homo sapiens"

    def __init__(self, name: str, age: int):
        # 实例变量
        self.name = name
        self.age = age

    def introduce(self) -> str:
        """实例方法"""
        return f"I'm {self.name}, {self.age} years old"

    @classmethod
    def from_birth_year(cls, name: str, birth_year: int):
        """类方法"""
        from datetime import datetime
        age = datetime.now().year - birth_year
        return cls(name, age)

    @staticmethod
    def is_adult(age: int) -> bool:
        """静态方法"""
        return age >= 18

# 使用
person = Person("Alice", 30)
person2 = Person.from_birth_year("Bob", 1995)
print(Person.is_adult(20))  # True
```

### 继承

```python
# 单继承
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "Some sound"

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"

# 多重继承
class Flyable:
    def fly(self) -> str:
        return "Flying..."

class Swimmable:
    def swim(self) -> str:
        return "Swimming..."

class Duck(Animal, Flyable, Swimmable):
    def speak(self) -> str:
        return f"{self.name} says Quack!"

# MRO (Method Resolution Order)
print(Duck.mro())

# super() 调用
class Employee(Person):
    def __init__(self, name: str, age: int, employee_id: str):
        super().__init__(name, age)
        self.employee_id = employee_id
```

### 属性和方法

```python
class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        """只读属性"""
        return self._radius

    @property
    def area(self) -> float:
        """计算属性"""
        return 3.14159 * self._radius ** 2

    @property
    def diameter(self) -> float:
        return self._radius * 2

    @diameter.setter
    def diameter(self, value: float):
        self._radius = value / 2

# 私有属性
class BankAccount:
    def __init__(self, balance: float):
        self.__balance = balance  # 名称修饰

    def get_balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float):
        self.__balance += amount
```

---

## 7. 装饰器与元编程

### 函数装饰器

```python
from functools import wraps
import time

# 简单装饰器
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def add(a, b):
    return a + b

# 带参数的装饰器
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

# 类装饰器
class Memoize:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@Memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 类装饰器

```python
# 装饰类
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

# dataclass (Python 3.7+)
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def distance(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

### 元编程

```python
# 动态创建类
def create_class(name: str, **attrs):
    return type(name, (), attrs)

MyClass = create_class("MyClass", x=1, y=2)
obj = MyClass()
print(obj.x)  # 1

# __new__ 和 __init__
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MyClass(metaclass=Singleton):
    pass

# 属性访问控制
class DynamicAttrs:
    def __getattr__(self, name):
        return f"Dynamic: {name}"

    def __setattr__(self, name, value):
        print(f"Setting {name} = {value}")
        super().__setattr__(name, value)
```

---

## 8. 实战案例

### 案例 1: 状态机

```python
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()

class StateMachine:
    def __init__(self):
        self._state = State.IDLE

    @property
    def state(self) -> State:
        return self._state

    def start(self):
        if self._state == State.IDLE:
            self._state = State.RUNNING
            print("Started")
        else:
            raise ValueError(f"Cannot start from {self._state}")

    def pause(self):
        if self._state == State.RUNNING:
            self._state = State.PAUSED
            print("Paused")

    def stop(self):
        if self._state in (State.RUNNING, State.PAUSED):
            self._state = State.STOPPED
            print("Stopped")
```

### 案例 2: 上下文管理器

```python
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    import time
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"{name} took {end - start:.4f}s")

# 使用
with timer("Operation"):
    # 耗时操作
    sum(range(1000000))
```

### 案例 3: 描述符验证器

```python
class Validated:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.name, value)

    def validate(self, value):
        pass

class PositiveNumber(Validated):
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Must be a number")
        if value <= 0:
            raise ValueError("Must be positive")

class Product:
    price = PositiveNumber()
    quantity = PositiveNumber()

    def __init__(self, price: float, quantity: int):
        self.price = price
        self.quantity = quantity
```

---

## 9. 延伸阅读

- [Python Grammar](https://docs.python.org/3/reference/grammar.html)
- [Python Language Reference](https://docs.python.org/3/reference/)
- [AST Module](https://docs.python.org/3/library/ast.html)
- [Tokenize Module](https://docs.python.org/3/library/tokenize.html)

---

**深入理解 Python 语法，编写优雅的代码！** 📝✨
