# Python 类与继承

**面向对象编程核心机制**

---

## 📋 目录

- [类定义基础](#类定义基础)
- [属性与方法](#属性与方法)
- [继承机制](#继承机制)
- [特殊方法](#特殊方法)
- [高级特性](#高级特性)

---

## 类定义基础

### 基础类定义

```python
"""
类的定义与实例化
"""

# 1. 基础类
class Person:
    """人类"""

    def __init__(self, name, age):
        """构造方法"""
        self.name = name
        self.age = age

    def greet(self):
        """实例方法"""
        return f"Hello, I'm {self.name}"

# 实例化
person = Person("Alice", 30)
print(person.greet())  # Hello, I'm Alice

# 2. 类变量 vs 实例变量
class Counter:
    """计数器类"""
    count = 0  # 类变量 (所有实例共享)

    def __init__(self):
        Counter.count += 1
        self.id = Counter.count  # 实例变量 (每个实例独立)

c1 = Counter()
c2 = Counter()
print(Counter.count)  # 2
print(c1.id, c2.id)   # 1 2

# 3. 类方法和静态方法
class Math:
    """数学工具类"""

    @classmethod
    def from_string(cls, s):
        """类方法: 接收类作为第一个参数"""
        return cls(int(s))

    @staticmethod
    def is_even(n):
        """静态方法: 不接收self或cls"""
        return n % 2 == 0
```

### 访问控制

```python
"""
Python的访问控制约定
"""

class BankAccount:
    """银行账户"""

    def __init__(self, balance):
        self.public = "公开属性"
        self._protected = "受保护属性"  # 约定: 内部使用
        self.__private = balance        # 名称改写: _BankAccount__private

    def get_balance(self):
        """访问私有属性"""
        return self.__private

    def _internal_method(self):
        """受保护方法"""
        pass

    def __private_method(self):
        """私有方法"""
        pass

account = BankAccount(1000)

print(account.public)          # OK
print(account._protected)      # 可以访问但不推荐
# print(account.__private)     # AttributeError
print(account._BankAccount__private)  # 名称改写后可访问

# Python没有真正的私有, 只是约定:
# - public: 公开API
# - _protected: 内部使用(子类可访问)
# - __private: 名称改写(避免子类覆盖)
```

---

## 属性与方法

### 实例方法、类方法、静态方法

```python
"""
三种方法类型对比
"""

class Example:
    class_var = "类变量"

    def instance_method(self):
        """实例方法: 操作实例数据"""
        return f"Instance method called by {self}"

    @classmethod
    def class_method(cls):
        """类方法: 操作类数据或创建实例"""
        return f"Class method called by {cls}"

    @staticmethod
    def static_method():
        """静态方法: 不访问实例或类数据"""
        return "Static method called"

obj = Example()

# 调用方式
obj.instance_method()      # 实例调用
Example.class_method()     # 类调用
Example.static_method()    # 类调用

# 实际应用
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_string):
        """工厂方法: 从字符串创建"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        """工厂方法: 创建今天的日期"""
        from datetime import date
        today = date.today()
        return cls(today.year, today.month, today.day)

    @staticmethod
    def is_date_valid(date_string):
        """静态方法: 验证日期格式"""
        try:
            year, month, day = map(int, date_string.split('-'))
            return 1 <= month <= 12 and 1 <= day <= 31
        except:
            return False

# 使用
date1 = Date(2025, 10, 28)
date2 = Date.from_string("2025-10-28")
date3 = Date.today()
print(Date.is_date_valid("2025-10-28"))  # True
```

### 属性装饰器

```python
"""
@property 装饰器
"""

class Temperature:
    """温度类"""

    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        """获取摄氏度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """设置摄氏度"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        """删除温度"""
        print("Deleting temperature")
        del self._celsius

    @property
    def fahrenheit(self):
        """计算华氏度"""
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """从华氏度设置"""
        self._celsius = (value - 32) * 5/9

# 使用
temp = Temperature(25)
print(temp.celsius)      # 25
print(temp.fahrenheit)   # 77.0

temp.celsius = 30
print(temp.fahrenheit)   # 86.0

temp.fahrenheit = 100
print(temp.celsius)      # 37.777...

# 属性的优势:
# 1. 提供getter/setter而不破坏接口
# 2. 可以添加验证逻辑
# 3. 可以计算衍生值
# 4. 保持属性访问的语法
```

---

## 继承机制

### 单继承

```python
"""
Python单继承
"""

# 基类
class Animal:
    """动物基类"""

    def __init__(self, name):
        self.name = name

    def speak(self):
        """动物叫声"""
        return "Some sound"

    def move(self):
        """动物移动"""
        return f"{self.name} is moving"

# 派生类
class Dog(Animal):
    """狗类"""

    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类构造方法
        self.breed = breed

    def speak(self):
        """重写父类方法"""
        return "Woof!"

    def fetch(self):
        """狗特有的方法"""
        return f"{self.name} is fetching"

dog = Dog("Buddy", "Golden Retriever")
print(dog.speak())  # Woof! (重写)
print(dog.move())   # Buddy is moving (继承)
print(dog.fetch())  # Buddy is fetching (新方法)

# 检查继承关系
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True
print(issubclass(Dog, Animal))  # True
```

### 多重继承

```python
"""
Python多重继承和MRO
"""

# 多重继承
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    """多重继承: D继承自B和C"""
    pass

d = D()
print(d.method())  # "B"

# 查看方法解析顺序(MRO)
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

print(D.mro())  # 等价

# MRO算法: C3线性化
# 规则:
# 1. 子类优先于父类
# 2. 多个父类按照声明顺序
# 3. 如果有多个路径到达同一个基类,使用第一个

# 钻石继承问题
class Base:
    def __init__(self):
        print("Base.__init__")

class Left(Base):
    def __init__(self):
        super().__init__()
        print("Left.__init__")

class Right(Base):
    def __init__(self):
        super().__init__()
        print("Right.__init__")

class Child(Left, Right):
    def __init__(self):
        super().__init__()
        print("Child.__init__")

child = Child()
# 输出:
# Base.__init__
# Right.__init__
# Left.__init__
# Child.__init__

# super()按照MRO调用下一个类
```

### Mixin模式

```python
"""
Mixin: 提供可重用功能的类
"""

# Mixin类
class LoggerMixin:
    """日志Mixin"""
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class SerializableMixin:
    """序列化Mixin"""
    def to_dict(self):
        return self.__dict__

class ValidatableMixin:
    """验证Mixin"""
    def validate(self):
        for key, value in self.__dict__.items():
            if value is None:
                raise ValueError(f"{key} cannot be None")

# 使用Mixin
class User(LoggerMixin, SerializableMixin, ValidatableMixin):
    """用户类"""
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.log(f"User {name} created")

user = User("Alice", "alice@example.com")
user.log("Doing something")
print(user.to_dict())
user.validate()

# Mixin命名约定:
# - 以Mixin结尾
# - 提供单一功能
# - 不应该单独实例化
# - 通常不定义__init__
```

---

## 特殊方法

### 基础特殊方法

```python
"""
常用特殊方法(魔法方法)
"""

class Point:
    """2D点类"""

    def __init__(self, x, y):
        """构造方法"""
        self.x = x
        self.y = y

    def __repr__(self):
        """官方字符串表示(调试用)"""
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        """用户友好的字符串表示"""
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        """相等比较"""
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        """小于比较"""
        return (self.x, self.y) < (other.x, other.y)

    def __add__(self, other):
        """加法"""
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """标量乘法"""
        return Point(self.x * scalar, self.y * scalar)

    def __abs__(self):
        """绝对值(距离)"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self):
        """布尔转换"""
        return self.x != 0 or self.y != 0

    def __len__(self):
        """长度"""
        return 2

    def __getitem__(self, index):
        """索引访问"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

# 使用
p1 = Point(1, 2)
p2 = Point(3, 4)

print(p1)           # (1, 2) (__str__)
print(repr(p1))     # Point(1, 2) (__repr__)
print(p1 == p2)     # False (__eq__)
print(p1 < p2)      # True (__lt__)
print(p1 + p2)      # Point(4, 6) (__add__)
print(p1 * 2)       # Point(2, 4) (__mul__)
print(abs(p1))      # 2.236... (__abs__)
print(bool(p1))     # True (__bool__)
print(len(p1))      # 2 (__len__)
print(p1[0])        # 1 (__getitem__)
```

### 容器特殊方法

```python
"""
实现容器协议
"""

class CustomList:
    """自定义列表"""

    def __init__(self):
        self._items = []

    def __len__(self):
        """长度"""
        return len(self._items)

    def __getitem__(self, index):
        """获取元素"""
        return self._items[index]

    def __setitem__(self, index, value):
        """设置元素"""
        self._items[index] = value

    def __delitem__(self, index):
        """删除元素"""
        del self._items[index]

    def __contains__(self, item):
        """成员测试"""
        return item in self._items

    def __iter__(self):
        """迭代"""
        return iter(self._items)

    def __reversed__(self):
        """反向迭代"""
        return reversed(self._items)

    def append(self, item):
        """添加元素"""
        self._items.append(item)

# 使用
lst = CustomList()
lst.append(1)
lst.append(2)
lst.append(3)

print(len(lst))     # 3
print(lst[0])       # 1
print(2 in lst)     # True

for item in lst:
    print(item)     # 1, 2, 3

for item in reversed(lst):
    print(item)     # 3, 2, 1
```

---

## 高级特性

### 抽象基类

```python
"""
抽象基类(ABC)
"""
from abc import ABC, abstractmethod

class Shape(ABC):
    """形状抽象基类"""

    @abstractmethod
    def area(self):
        """计算面积(必须实现)"""
        pass

    @abstractmethod
    def perimeter(self):
        """计算周长(必须实现)"""
        pass

    def describe(self):
        """描述(可选实现)"""
        return f"Area: {self.area()}, Perimeter: {self.perimeter()}"

class Circle(Shape):
    """圆形"""
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    """矩形"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# 使用
# shape = Shape()  # TypeError: 不能实例化抽象类

circle = Circle(5)
print(circle.describe())

rectangle = Rectangle(4, 5)
print(rectangle.describe())
```

### 数据类

```python
"""
dataclass: 简化数据类定义 (Python 3.7+)
"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class Point:
    """2D点数据类"""
    x: float
    y: float

    def distance(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

# 自动生成:
# - __init__
# - __repr__
# - __eq__

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1)  # Point(x=1, y=2)
print(p1 == p2)  # True

# 高级特性
@dataclass(order=True, frozen=True)
class Product:
    """产品数据类"""
    name: str
    price: float = field(compare=True)
    quantity: int = field(default=0, compare=False)
    tags: List[str] = field(default_factory=list)

    def total_price(self):
        return self.price * self.quantity

# order=True: 生成比较方法
# frozen=True: 不可变
# field(): 字段配置
```

---

## 📚 核心要点

### 类定义

- ✅ **class关键字**: 定义类
- ✅ ****init****: 构造方法
- ✅ **self**: 实例引用
- ✅ **类变量vs实例变量**: 作用域

### 方法类型

- ✅ **实例方法**: self参数
- ✅ **类方法**: @classmethod, cls参数
- ✅ **静态方法**: @staticmethod
- ✅ **property**: @property装饰器

### 继承

- ✅ **单继承**: class Child(Parent)
- ✅ **多重继承**: class Child(A, B)
- ✅ **super()**: 调用父类方法
- ✅ **MRO**: 方法解析顺序(C3算法)

### 特殊方法

- ✅ ****init****: 构造
- ✅ ****str**/**repr****: 字符串表示
- ✅ ****eq**/**lt****: 比较
- ✅ ****add**/**mul****: 运算
- ✅ ****len**/**getitem****: 容器

### 最佳实践

- ✅ 遵循单一职责原则
- ✅ 优先使用组合而非继承
- ✅ 使用Mixin提供可重用功能
- ✅ 实现抽象基类定义接口
- ✅ 使用dataclass简化数据类

---

**掌握类与继承，构建优雅架构！** 🏗️✨

**相关文档**:

- [05-functions-closures.md](05-functions-closures.md) - 函数与闭包
- [07-decorators-metaprogramming.md](07-decorators-metaprogramming.md) - 装饰器与元编程
- [../01-language-core/01-data-model.md](../01-language-core/01-data-model.md) - 数据模型

**最后更新**: 2025年10月28日
