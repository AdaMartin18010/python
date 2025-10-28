# Python 作用域与命名空间

**理解Python的名称解析机制**

---

## 📋 目录

- [命名空间基础](#命名空间基础)
- [作用域规则](#作用域规则)
- [LEGB规则](#LEGB规则)
- [闭包机制](#闭包机制)
- [名称解析](#名称解析)

---

## 命名空间基础

### 什么是命名空间

```python
"""
命名空间是名称到对象的映射
本质上就是字典
"""

# 1. 内置命名空间
import builtins
print(dir(builtins))  # 所有内置名称

# 2. 全局命名空间 (模块级)
x = 10
y = 20

print(globals())  # 全局命名空间 (字典)

# 3. 局部命名空间 (函数内)
def func():
    a = 1
    b = 2
    print(locals())  # 局部命名空间

func()  # {'a': 1, 'b': 2}

# 4. 对象命名空间
class MyClass:
    class_var = 100
    
    def __init__(self):
        self.instance_var = 200

obj = MyClass()
print(obj.__dict__)        # 实例命名空间
print(MyClass.__dict__)    # 类命名空间
```

### 命名空间的生命周期

```python
"""
命名空间的创建和销毁
"""

# 1. 内置命名空间
# - 创建: Python解释器启动时
# - 销毁: 解释器退出时

# 2. 全局命名空间 (模块)
# - 创建: 模块被import时
# - 销毁: 程序退出时或手动del

# 3. 局部命名空间 (函数)
# - 创建: 函数调用时
# - 销毁: 函数返回时

def example():
    """函数调用时创建新的命名空间"""
    local_var = 42
    print(f"Local namespace: {locals()}")

example()  # 创建命名空间
# 函数返回后,local_var不再存在

# 4. 类和实例命名空间
# - 类命名空间: class定义时创建
# - 实例命名空间: 实例创建时(__init__)
```

---

## 作用域规则

### 四种作用域

```python
"""
Python的LEGB作用域规则
"""

# L - Local (局部作用域)
# E - Enclosing (嵌套函数外层)
# G - Global (全局作用域)
# B - Built-in (内置作用域)

# 示例
x = "global"  # G - 全局

def outer():
    x = "enclosing"  # E - 外层
    
    def inner():
        x = "local"  # L - 局部
        print(f"Local: {x}")
        
        # 访问不同作用域的x
        # 无法直接访问enclosing的x
    
    inner()
    print(f"Enclosing: {x}")

outer()
print(f"Global: {x}")

"""
输出:
Local: local
Enclosing: enclosing
Global: global
"""
```

### global和nonlocal

```python
"""
global和nonlocal关键字
"""

# 1. global - 访问全局变量
count = 0

def increment():
    global count  # 声明使用全局count
    count += 1

increment()
print(count)  # 1

# 2. nonlocal - 访问外层函数变量
def outer():
    count = 0
    
    def inner():
        nonlocal count  # 声明使用外层count
        count += 1
    
    inner()
    print(count)  # 1

outer()

# 3. 对比
x = 10

def test_global():
    global x
    x = 20  # 修改全局x

def test_local():
    x = 30  # 创建新的局部x,不影响全局

test_global()
print(x)  # 20

test_local()
print(x)  # 20 (未改变)

# ============================================
# 陷阱: 默认参数
# ============================================

def append_to(element, lst=[]):
    """危险!默认参数只创建一次"""
    lst.append(element)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - 危险!

# 正确做法:
def append_to(element, lst=None):
    if lst is None:
        lst = []
    lst.append(element)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [2] - 正确!
```

---

## LEGB规则

### 名称查找顺序

```python
"""
LEGB查找顺序详解
"""

x = "global x"

def outer():
    x = "outer x"
    
    def inner():
        # 查找顺序: L → E → G → B
        print(x)  # 找到outer的x (E)
    
    inner()

outer()  # 输出: outer x

# ============================================
# 详细查找流程
# ============================================

def example():
    # 1. Local: 查找局部变量
    local_var = "local"
    
    # 2. Enclosing: 查找外层函数
    def inner():
        print(local_var)  # 从enclosing找到
    
    # 3. Global: 查找全局
    print(x)  # 从global找到
    
    # 4. Built-in: 查找内置
    print(len([1, 2, 3]))  # 从built-in找到
    
    inner()

example()
```

### 作用域陷阱

```python
"""
常见的作用域陷阱
"""

# 陷阱1: 循环变量作用域
for i in range(3):
    pass

print(i)  # 2 - i泄漏到外部!

# Python 3中列表推导式有独立作用域
[i for i in range(3)]
# print(i)  # NameError - i不泄漏

# 陷阱2: 修改全局列表
lst = []

def append_one():
    lst.append(1)  # 可以修改全局列表

append_one()
print(lst)  # [1]

# 但重新赋值需要global
def reassign():
    # lst = [1, 2, 3]  # 创建局部lst
    global lst
    lst = [1, 2, 3]  # 修改全局lst

reassign()
print(lst)  # [1, 2, 3]

# 陷阱3: 类变量 vs 实例变量
class MyClass:
    x = []  # 类变量 (所有实例共享!)
    
    def __init__(self):
        self.y = []  # 实例变量 (每个实例独立)

a = MyClass()
b = MyClass()

a.x.append(1)
print(b.x)  # [1] - 共享!

a.y.append(2)
print(b.y)  # [] - 独立
```

---

## 闭包机制

### 闭包基础

```python
"""
闭包: 函数+外部环境
"""

def make_counter():
    """创建计数器"""
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

# 创建两个独立的计数器
c1 = make_counter()
c2 = make_counter()

print(c1())  # 1
print(c1())  # 2
print(c2())  # 1 - 独立的计数

# 查看闭包变量
print(c1.__closure__)  # 闭包单元格
print(c1.__closure__[0].cell_contents)  # 2
```

### 闭包的应用

```python
"""
闭包的实际应用
"""

# 1. 函数工厂
def make_multiplier(factor):
    """创建乘法函数"""
    def multiplier(x):
        return x * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15

# 2. 数据隐藏
def make_account(initial_balance):
    """创建账户"""
    balance = initial_balance
    
    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance
    
    def withdraw(amount):
        nonlocal balance
        if balance >= amount:
            balance -= amount
            return balance
        else:
            return "Insufficient funds"
    
    def get_balance():
        return balance
    
    return deposit, withdraw, get_balance

# 使用
deposit, withdraw, get_balance = make_account(100)
print(deposit(50))      # 150
print(withdraw(30))     # 120
print(get_balance())    # 120

# 3. 装饰器 (闭包的经典应用)
def repeat(n):
    """重复执行装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    return f"Hello, {name}"

print(greet("Alice"))  # ['Hello, Alice', 'Hello, Alice', 'Hello, Alice']
```

### 闭包陷阱

```python
"""
闭包的常见陷阱
"""

# 陷阱: 循环中的闭包
functions = []
for i in range(3):
    def func():
        return i
    functions.append(func)

# 期望: [0, 1, 2]
# 实际: [2, 2, 2]
print([f() for f in functions])  # [2, 2, 2]

# 原因: 闭包捕获的是变量i本身,不是值!
# 当调用func时,i已经是2了

# 解决方法1: 默认参数
functions = []
for i in range(3):
    def func(x=i):  # 立即绑定i的值
        return x
    functions.append(func)

print([f() for f in functions])  # [0, 1, 2]

# 解决方法2: functools.partial
from functools import partial

def func(x):
    return x

functions = [partial(func, i) for i in range(3)]
print([f() for f in functions])  # [0, 1, 2]
```

---

## 名称解析

### 名称绑定

```python
"""
名称绑定的时机
"""

# 1. 赋值绑定
x = 10  # x绑定到10

# 2. import绑定
import os  # os绑定到模块对象

# 3. 函数定义绑定
def func():  # func绑定到函数对象
    pass

# 4. 类定义绑定
class MyClass:  # MyClass绑定到类对象
    pass

# 5. for循环绑定
for i in range(3):  # i绑定到0, 1, 2
    pass

# 6. with语句绑定
with open("file.txt") as f:  # f绑定到文件对象
    pass

# 7. except语句绑定
try:
    1 / 0
except ZeroDivisionError as e:  # e绑定到异常对象
    print(e)
```

### 名称空间操作

```python
"""
直接操作命名空间
"""

# 1. 动态访问
obj = object()
setattr(obj, 'x', 10)  # obj.x = 10
print(getattr(obj, 'x'))  # 10
print(hasattr(obj, 'x'))  # True
delattr(obj, 'x')  # del obj.x

# 2. vars()获取命名空间
class Example:
    def __init__(self):
        self.x = 1
        self.y = 2

obj = Example()
print(vars(obj))  # {'x': 1, 'y': 2}

# 3. 动态执行
namespace = {}
exec("x = 10; y = 20", namespace)
print(namespace['x'])  # 10

# 4. 模块命名空间
import sys
current_module = sys.modules[__name__]
print(dir(current_module))  # 模块的所有名称
```

---

## 📚 核心要点

### 命名空间

- ✅ **本质**: 名称到对象的映射(字典)
- ✅ **类型**: 内置、全局、局部、对象
- ✅ **生命周期**: 创建、使用、销毁

### 作用域

- ✅ **LEGB规则**: Local → Enclosing → Global → Built-in
- ✅ **global**: 访问全局变量
- ✅ **nonlocal**: 访问外层函数变量

### 闭包

- ✅ **定义**: 函数+捕获的外部变量
- ✅ **应用**: 函数工厂、装饰器、数据隐藏
- ✅ **陷阱**: 循环中的闭包

### 最佳实践

- ✅ 最小化全局变量使用
- ✅ 优先使用参数传递
- ✅ 注意可变默认参数
- ✅ 理解类变量 vs 实例变量
- ✅ 小心循环中的闭包

---

**掌握作用域,写出清晰的代码！** 🎯✨

**相关文档**:
- [01-data-model.md](01-data-model.md) - 数据模型
- [04-execution-model.md](04-execution-model.md) - 执行模型

**最后更新**: 2025年10月28日

