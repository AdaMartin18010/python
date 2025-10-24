# Python 语言核心特性

**深入理解 Python 的核心机制**-

---

## 📚 目录

1. [数据模型与对象系统](01-data-model.md) - Python 对象模型
2. [类型系统](02-type-system.md) - 类型系统详解
3. [内存模型](03-memory-model.md) - 内存管理机制
4. [执行模型](04-execution-model.md) - 代码执行过程
5. [作用域与命名空间](05-scope-namespace.md) - 作用域规则

---

## 🎯 核心概念速查

### 1. 一切皆对象

Python 中**一切都是对象**，包括数字、字符串、函数、类：

```python
# 所有东西都是对象
x = 42
print(type(x))  # <class 'int'>
print(type(int))  # <class 'type'>
print(type(type))  # <class 'type'>

# 函数也是对象
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(type(greet))  # <class 'function'>
greet.custom_attr = "metadata"  # 函数可以有属性

# 类也是对象
class Person:
    pass

print(type(Person))  # <class 'type'>
```

### 2. 对象的身份、类型和值

每个对象都有三个特性：

```python
x = [1, 2, 3]

# 1. 身份 (identity) - 内存地址
print(id(x))  # 140123456789

# 2. 类型 (type) - 对象的类
print(type(x))  # <class 'list'>

# 3. 值 (value) - 对象的内容
print(x)  # [1, 2, 3]

# is vs ==
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True (值相等)
print(a is b)  # False (不是同一个对象)
print(a is c)  # True (是同一个对象)
```

---

## 🔤 数据模型

### 特殊方法（Magic Methods）

Python 通过特殊方法实现运算符重载和协议：

```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self) -> str:
        """用户友好的字符串"""
        return f"<{self.x}, {self.y}>"
    
    def __add__(self, other: "Vector") -> "Vector":
        """向量加法"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar: float) -> "Vector":
        """标量乘法"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __abs__(self) -> float:
        """向量长度"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __bool__(self) -> bool:
        """真值测试"""
        return abs(self) != 0
    
    def __eq__(self, other: object) -> bool:
        """相等比较"""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __getitem__(self, index: int) -> float:
        """索引访问"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")
    
    def __len__(self) -> int:
        """长度"""
        return 2

# 使用
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(repr(v1))  # Vector(3, 4)
print(str(v1))   # <3, 4>
print(v1 + v2)   # Vector(4, 6)
print(v1 * 2)    # Vector(6, 8)
print(abs(v1))   # 5.0
print(bool(v1))  # True
print(v1 == v2)  # False
print(v1[0])     # 3
print(len(v1))   # 2
```

### 常用特殊方法

```python
class MyClass:
    # 构造与析构
    def __init__(self): pass
    def __del__(self): pass
    
    # 字符串表示
    def __repr__(self): pass
    def __str__(self): pass
    def __format__(self, format_spec): pass
    
    # 数值运算
    def __add__(self, other): pass
    def __sub__(self, other): pass
    def __mul__(self, other): pass
    def __truediv__(self, other): pass
    def __floordiv__(self, other): pass
    def __mod__(self, other): pass
    def __pow__(self, other): pass
    
    # 比较运算
    def __eq__(self, other): pass
    def __ne__(self, other): pass
    def __lt__(self, other): pass
    def __le__(self, other): pass
    def __gt__(self, other): pass
    def __ge__(self, other): pass
    
    # 容器协议
    def __len__(self): pass
    def __getitem__(self, key): pass
    def __setitem__(self, key, value): pass
    def __delitem__(self, key): pass
    def __contains__(self, item): pass
    def __iter__(self): pass
    def __next__(self): pass
    
    # 上下文管理
    def __enter__(self): pass
    def __exit__(self, exc_type, exc_val, exc_tb): pass
    
    # 可调用对象
    def __call__(self, *args, **kwargs): pass
    
    # 属性访问
    def __getattr__(self, name): pass
    def __setattr__(self, name, value): pass
    def __delattr__(self, name): pass
    def __getattribute__(self, name): pass
```

---

## 💾 内存模型

### 引用计数

Python 使用引用计数管理内存：

```python
import sys

# 创建对象
x = [1, 2, 3]
print(sys.getrefcount(x))  # 2 (x + getrefcount 临时引用)

# 增加引用
y = x
print(sys.getrefcount(x))  # 3

# 减少引用
del y
print(sys.getrefcount(x))  # 2

# 引用计数归零时，对象被销毁
```

### 垃圾回收

```python
import gc

# 手动触发垃圾回收
gc.collect()

# 查看垃圾回收统计
print(gc.get_stats())

# 禁用/启用垃圾回收
gc.disable()
gc.enable()
```

### 对象池

Python 对小整数和小字符串使用对象池：

```python
# 小整数 (-5 到 256) 被缓存
a = 100
b = 100
print(a is b)  # True (同一个对象)

a = 1000
b = 1000
print(a is b)  # False (不同对象)

# 小字符串被内部化
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True (同一个对象)
```

---

## 🔄 执行模型

### 字节码

Python 代码被编译为字节码：

```python
import dis

def add(a: int, b: int) -> int:
    return a + b

# 反汇编查看字节码
dis.dis(add)

# 输出:
#   2           0 LOAD_FAST                0 (a)
#               2 LOAD_FAST                1 (b)
#               4 BINARY_ADD
#               6 RETURN_VALUE
```

### 执行流程

```text
源代码 (.py)
    ↓ 词法分析
Token 流
    ↓ 语法分析
抽象语法树 (AST)
    ↓ 编译
字节码 (.pyc)
    ↓ 解释执行
Python 虚拟机 (PVM)
    ↓
结果
```

### AST 示例

```python
import ast

code = "x = 1 + 2"
tree = ast.parse(code)
print(ast.dump(tree, indent=2))

# 输出:
# Module(
#   body=[
#     Assign(
#       targets=[Name(id='x', ctx=Store())],
#       value=BinOp(
#         left=Constant(value=1),
#         op=Add(),
#         right=Constant(value=2)
#       )
#     )
#   ]
# )
```

---

## 📐 作用域与命名空间

### LEGB 规则

Python 的名称查找遵循 LEGB 顺序：

```python
# L: Local (局部)
# E: Enclosing (闭包)
# G: Global (全局)
# B: Built-in (内置)

x = "global"  # G

def outer():
    x = "enclosing"  # E
    
    def inner():
        x = "local"  # L
        print(x)  # local
    
    inner()
    print(x)  # enclosing

outer()
print(x)  # global
```

### 命名空间

```python
# 内置命名空间
print(len)  # <built-in function len>

# 全局命名空间
global_var = "global"

def function():
    # 局部命名空间
    local_var = "local"
    
    # 访问全局变量
    global global_var
    global_var = "modified"
    
    # 查看局部命名空间
    print(locals())  # {'local_var': 'local'}

# 查看全局命名空间
print(globals().keys())
```

### nonlocal 与 global

```python
x = 0  # 全局

def outer():
    x = 1  # 闭包
    
    def inner1():
        x = 2  # 局部
        print(f"inner1 local: {x}")  # 2
    
    def inner2():
        nonlocal x  # 修改闭包变量
        x = 3
        print(f"inner2 nonlocal: {x}")  # 3
    
    def inner3():
        global x  # 修改全局变量
        x = 4
        print(f"inner3 global: {x}")  # 4
    
    inner1()
    print(f"outer after inner1: {x}")  # 1
    
    inner2()
    print(f"outer after inner2: {x}")  # 3
    
    inner3()
    print(f"outer after inner3: {x}")  # 3

outer()
print(f"global x: {x}")  # 4
```

---

## 🎭 类与元类

### 类的创建

```python
# 类也是对象，由元类创建
class MyClass:
    pass

print(type(MyClass))  # <class 'type'>
print(isinstance(MyClass, type))  # True

# type 是所有类的元类
print(type(int))   # <class 'type'>
print(type(str))   # <class 'type'>
print(type(list))  # <class 'type'>
```

### 自定义元类

```python
class Meta(type):
    def __new__(mcs, name, bases, dct):
        # 在类创建时执行
        print(f"Creating class: {name}")
        # 自动添加属性
        dct['created_at'] = "2025-10-24"
        return super().__new__(mcs, name, bases, dct)
    
    def __init__(cls, name, bases, dct):
        # 在类初始化时执行
        print(f"Initializing class: {name}")
        super().__init__(name, bases, dct)

class MyClass(metaclass=Meta):
    pass

# 输出:
# Creating class: MyClass
# Initializing class: MyClass

print(MyClass.created_at)  # 2025-10-24
```

---

## 🔍 描述符协议

描述符是实现 `__get__`、`__set__`、`__delete__` 的对象：

```python
class Descriptor:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be str")
        obj.__dict__[self.name] = value

class Person:
    name = Descriptor()  # 描述符
    
    def __init__(self, name: str):
        self.name = name

# 使用
p = Person("Alice")
print(p.name)  # Alice

p.name = "Bob"
print(p.name)  # Bob

try:
    p.name = 123  # TypeError
except TypeError as e:
    print(e)  # name must be str
```

### 内置描述符

```python
# property 是描述符
class Circle:
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self) -> float:
        """半径"""
        return self._radius
    
    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    @property
    def area(self) -> float:
        """面积（只读）"""
        return 3.14159 * self._radius ** 2

# 使用
circle = Circle(5)
print(circle.radius)  # 5
print(circle.area)    # 78.53975

circle.radius = 10
print(circle.area)    # 314.159

try:
    circle.area = 100  # AttributeError (只读)
except AttributeError as e:
    print(e)
```

---

## 🎯 协议（Protocols）

Python 通过协议定义接口：

### 迭代器协议

```python
class Countdown:
    def __init__(self, start: int):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

# 使用
for n in Countdown(5):
    print(n)  # 5, 4, 3, 2, 1
```

### 上下文管理器协议

```python
class FileManager:
    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        # 返回 False 表示不抑制异常
        return False

# 使用
with FileManager("test.txt", "w") as f:
    f.write("Hello, World!")
```

---

## 📚 实战案例

### 案例 1: 单例模式

```python
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        print("Initializing database...")

# 测试
db1 = Database()  # Initializing database...
db2 = Database()  # (不会再次初始化)
print(db1 is db2)  # True
```

### 案例 2: 属性验证

```python
class ValidatedAttribute:
    def __init__(self, validator):
        self.validator = validator
    
    def __set_name__(self, owner, name):
        self.name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, None)
    
    def __set__(self, obj, value):
        self.validator(value)
        setattr(obj, self.name, value)

class User:
    name = ValidatedAttribute(
        lambda x: len(x) > 0 or (_ for _ in ()).throw(ValueError("Name cannot be empty"))
    )
    age = ValidatedAttribute(
        lambda x: 0 <= x <= 150 or (_ for _ in ()).throw(ValueError("Invalid age"))
    )
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# 使用
user = User("Alice", 30)
print(user.name, user.age)  # Alice 30

try:
    user.name = ""  # ValueError
except ValueError as e:
    print(e)
```

---

## 📖 延伸阅读

- [Python 数据模型](https://docs.python.org/3/reference/datamodel.html)
- [Python 执行模型](https://docs.python.org/3/reference/executionmodel.html)
- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [Python 内存管理](https://realpython.com/python-memory-management/)

---

**深入理解 Python 核心，成为 Python 专家！** 🐍✨

