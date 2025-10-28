# Python 数据模型与对象系统

**一切皆对象的Python世界**

---

## 📋 目录

- [对象模型基础](#对象模型基础)
- [属性访问机制](#属性访问机制)
- [描述符协议](#描述符协议)
- [特殊方法](#特殊方法)
- [元类系统](#元类系统)

---

## 对象模型基础

### Python对象的本质

```python
"""
Python中一切皆对象
"""

# 1. 所有东西都是对象
print(type(42))          # <class 'int'>
print(type(int))         # <class 'type'>
print(type(type))        # <class 'type'>

# 2. 对象三要素
"""
每个对象都有:
- id:    对象的唯一标识（内存地址）
- type:  对象的类型
- value: 对象的值
"""

x = 42
print(f"id: {id(x)}")        # 内存地址
print(f"type: {type(x)}")    # <class 'int'>
print(f"value: {x}")         # 42

# 3. 可变对象 vs 不可变对象
"""
不可变对象: int, float, str, tuple, frozenset
可变对象:   list, dict, set, 自定义类实例
"""

# 不可变对象
a = [1, 2, 3]
b = a
a.append(4)
print(b)  # [1, 2, 3, 4] - 同一对象

# 可变对象
s = "hello"
t = s
s = s + " world"
print(t)  # "hello" - 不同对象
```

### 对象的内部结构

```python
"""
CPython对象的C结构
"""

# PyObject基础结构
"""
typedef struct _object {
    Py_ssize_t ob_refcnt;      # 引用计数
    PyTypeObject *ob_type;      # 类型对象
} PyObject;
"""

# PyVarObject (可变大小对象)
"""
typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size;         # 元素数量
} PyVarObject;
"""

# 查看对象的引用计数
import sys

x = []
print(sys.getrefcount(x))  # 2 (本身 + getrefcount参数)

y = x
print(sys.getrefcount(x))  # 3

del y
print(sys.getrefcount(x))  # 2
```

---

## 属性访问机制

### 属性查找顺序

```python
"""
属性查找顺序 (Attribute Lookup Order)
"""

class Base:
    x = "base"
    
    def __init__(self):
        self.y = "instance"

obj = Base()

# 1. 实例字典
print(obj.__dict__)  # {'y': 'instance'}

# 2. 类字典
print(Base.__dict__['x'])  # 'base'

# 3. 继承链
print(obj.x)  # 'base' - 从类中找到
print(obj.y)  # 'instance' - 从实例中找到

# 完整的属性查找顺序:
"""
1. 实例的 __dict__
2. 类的 __dict__
3. 父类的 __dict__ (MRO顺序)
4. 触发 __getattribute__
5. 如果没找到,触发 __getattr__
"""
```

### 属性访问魔法方法

```python
"""
属性访问的底层机制
"""

class TrackedAccess:
    """追踪属性访问"""
    
    def __init__(self):
        self._data = {}
    
    def __getattribute__(self, name: str):
        """获取属性时调用"""
        print(f"Getting: {name}")
        return super().__getattribute__(name)
    
    def __getattr__(self, name: str):
        """属性不存在时调用"""
        print(f"Attribute {name} not found, creating...")
        return f"default_{name}"
    
    def __setattr__(self, name: str, value):
        """设置属性时调用"""
        print(f"Setting: {name} = {value}")
        super().__setattr__(name, value)
    
    def __delattr__(self, name: str):
        """删除属性时调用"""
        print(f"Deleting: {name}")
        super().__delattr__(name)

# 使用
obj = TrackedAccess()
# Setting: _data = {}

obj.x = 10
# Setting: x = 10

print(obj.x)
# Getting: x
# 10

print(obj.missing)
# Getting: missing
# Attribute missing not found, creating...
# default_missing
```

---

## 描述符协议

### 描述符基础

```python
"""
描述符协议: __get__, __set__, __delete__
"""

class Descriptor:
    """数据描述符"""
    
    def __init__(self, name: str):
        self.name = name
    
    def __get__(self, instance, owner):
        """获取属性"""
        if instance is None:
            return self
        print(f"Getting {self.name}")
        return instance.__dict__.get(self.name, None)
    
    def __set__(self, instance, value):
        """设置属性"""
        print(f"Setting {self.name} = {value}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        """删除属性"""
        print(f"Deleting {self.name}")
        del instance.__dict__[self.name]

class MyClass:
    """使用描述符"""
    x = Descriptor("x")
    y = Descriptor("y")

obj = MyClass()
obj.x = 10      # Setting x = 10
print(obj.x)    # Getting x
                # 10
del obj.x       # Deleting x
```

### 实用描述符示例

```python
"""
实用描述符: 验证、类型检查、懒加载
"""

class Validated:
    """类型验证描述符"""
    
    def __init__(self, name: str, expected_type: type):
        self.name = name
        self.expected_type = expected_type
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}"
            )
        instance.__dict__[self.name] = value
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

class Person:
    """带验证的类"""
    name = Validated("name", str)
    age = Validated("age", int)
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# 使用
person = Person("Alice", 30)
print(person.name)  # Alice

try:
    person.age = "30"  # TypeError!
except TypeError as e:
    print(e)  # age must be int

# ============================================
# 懒加载描述符
# ============================================

class LazyProperty:
    """懒加载属性"""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # 第一次访问时计算
        value = self.func(instance)
        # 缓存结果
        setattr(instance, self.name, value)
        return value

class DataProcessor:
    """使用懒加载"""
    
    @LazyProperty
    def expensive_result(self):
        """昂贵的计算"""
        print("Computing...")
        return sum(range(1000000))

processor = DataProcessor()
print(processor.expensive_result)  # Computing... 499999500000
print(processor.expensive_result)  # 499999500000 (缓存,不再计算)
```

---

## 特殊方法

### 运算符重载

```python
"""
特殊方法实现运算符重载
"""

class Vector:
    """2D向量类"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        """官方字符串表示"""
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self) -> str:
        """用户友好的字符串"""
        return f"({self.x}, {self.y})"
    
    def __add__(self, other: "Vector") -> "Vector":
        """向量加法"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar: float) -> "Vector":
        """标量乘法"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other: "Vector") -> bool:
        """相等比较"""
        return self.x == other.x and self.y == other.y
    
    def __abs__(self) -> float:
        """向量长度"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __bool__(self) -> bool:
        """布尔转换"""
        return bool(abs(self))

# 使用
v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)      # (4, 6)
print(v1 * 2)       # (2, 4)
print(abs(v1))      # 2.23606797749979
print(v1 == v2)     # False
```

### 容器协议

```python
"""
容器特殊方法
"""

class CustomList:
    """自定义列表类"""
    
    def __init__(self):
        self._items = []
    
    def __len__(self) -> int:
        """长度"""
        return len(self._items)
    
    def __getitem__(self, index: int):
        """索引访问"""
        return self._items[index]
    
    def __setitem__(self, index: int, value):
        """索引赋值"""
        self._items[index] = value
    
    def __delitem__(self, index: int):
        """删除元素"""
        del self._items[index]
    
    def __contains__(self, item) -> bool:
        """成员测试"""
        return item in self._items
    
    def __iter__(self):
        """迭代"""
        return iter(self._items)
    
    def append(self, item):
        """添加元素"""
        self._items.append(item)

# 使用
lst = CustomList()
lst.append(1)
lst.append(2)

print(len(lst))     # 2
print(lst[0])       # 1
print(2 in lst)     # True

for item in lst:
    print(item)     # 1, 2
```

### 上下文管理器

```python
"""
上下文管理器协议
"""

class DatabaseConnection:
    """数据库连接上下文管理器"""
    
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        """进入上下文"""
        print(f"Connecting to {self.db_name}")
        self.connection = f"Connection to {self.db_name}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        print(f"Closing connection to {self.db_name}")
        self.connection = None
        
        # 返回True抑制异常,False传播异常
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}")
        return False

# 使用
with DatabaseConnection("mydb") as conn:
    print(f"Using {conn}")
    # Connecting to mydb
    # Using Connection to mydb
# Closing connection to mydb
```

---

## 元类系统

### 元类基础

```python
"""
元类: 类的类
"""

# type是所有类的元类
print(type(int))    # <class 'type'>
print(type(str))    # <class 'type'>
print(type(type))   # <class 'type'>

# 使用type动态创建类
def __init__(self, x):
    self.x = x

MyClass = type(
    "MyClass",              # 类名
    (object,),              # 基类
    {                       # 类字典
        "__init__": __init__,
        "value": 42
    }
)

obj = MyClass(10)
print(obj.x)        # 10
print(obj.value)    # 42
```

### 自定义元类

```python
"""
自定义元类实现单例模式
"""

class SingletonMeta(type):
    """单例元类"""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """控制类的实例化"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """使用单例元类"""
    
    def __init__(self, host: str):
        self.host = host

# 使用
db1 = Database("localhost")
db2 = Database("127.0.0.1")

print(db1 is db2)   # True (同一个实例)
print(db1.host)     # localhost (第一次的参数)
```

### 元类的实际应用

```python
"""
元类应用: ORM示例
"""

class ModelMeta(type):
    """ORM元类"""
    
    def __new__(mcs, name, bases, namespace):
        # 收集字段
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                fields[key] = value
                value.name = key
        
        # 保存字段信息
        namespace['_fields'] = fields
        
        return super().__new__(mcs, name, bases, namespace)

class Field:
    """字段基类"""
    
    def __init__(self, field_type: type):
        self.field_type = field_type
        self.name = None

class Model(metaclass=ModelMeta):
    """模型基类"""
    
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

# 定义模型
class User(Model):
    """用户模型"""
    name = Field(str)
    age = Field(int)
    email = Field(str)

# 使用
user = User(name="Alice", age=30, email="alice@example.com")
print(User._fields)  # 字段信息
print(user.name)     # Alice
```

---

## 📚 核心要点

### 对象模型

- ✅ **一切皆对象**: 类、函数、模块都是对象
- ✅ **对象三要素**: id、type、value
- ✅ **可变性**: 理解可变对象和不可变对象的区别

### 属性访问

- ✅ **查找顺序**: 实例 → 类 → 父类 → __getattr__
- ✅ **魔法方法**: `__getattribute__`, `__getattr__`, `__setattr__`
- ✅ **描述符**: 实现属性的高级控制

### 特殊方法

- ✅ **运算符重载**: `__add__`, `__mul__`, `__eq__`等
- ✅ **容器协议**: `__len__`, `__getitem__`, `__iter__`
- ✅ **上下文管理**: `__enter__`, `__exit__`

### 元类

- ✅ **type是元类**: 所有类的类
- ✅ **自定义元类**: 控制类的创建
- ✅ **实际应用**: ORM、验证、单例等

---

**理解Python对象模型，掌握语言核心！** 🐍✨

**相关文档**:
- [02-type-system.md](02-type-system.md) - 类型系统
- [03-memory-model.md](03-memory-model.md) - 内存模型
- [04-execution-model.md](04-execution-model.md) - 执行模型

**最后更新**: 2025年10月28日

