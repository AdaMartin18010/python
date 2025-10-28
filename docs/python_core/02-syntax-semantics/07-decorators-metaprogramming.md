# Python 装饰器与元编程

**高级代码抽象技术**

---

## 📋 目录

- [装饰器深入](#装饰器深入)
- [类装饰器](#类装饰器)
- [元类](#元类)
- [描述符](#描述符)
- [代码生成](#代码生成)

---

## 装饰器深入

### 装饰器原理

```python
"""
装饰器的本质
"""

# 装饰器就是一个返回函数的函数
def my_decorator(func):
    """简单装饰器"""
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}")

# 等价于:
def greet(name):
    print(f"Hello, {name}")

greet = my_decorator(greet)

# 保留函数元信息
from functools import wraps

def my_decorator(func):
    @wraps(func)  # 保留原函数的__name__, __doc__等
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 带参数的装饰器

```python
"""
装饰器工厂
"""

# 装饰器工厂: 返回装饰器的函数
def repeat(n):
    """重复执行n次的装饰器"""
    def decorator(func):
        @wraps(func)
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

print(greet("Alice"))
# ['Hello, Alice', 'Hello, Alice', 'Hello, Alice']

# 等价于:
greet = repeat(3)(greet)

# 可选参数的装饰器
def optional_arg_decorator(func=None, *, option=None):
    """可选参数装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"Option: {option}")
            return f(*args, **kwargs)
        return wrapper
    
    if func is None:
        # 带参数调用: @decorator(option="value")
        return decorator
    else:
        # 无参数调用: @decorator
        return decorator(func)

@optional_arg_decorator
def func1():
    pass

@optional_arg_decorator(option="test")
def func2():
    pass
```

### 装饰器链

```python
"""
多个装饰器的组合
"""

def decorator1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Decorator 1")
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Decorator 2")
        return func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def greet():
    print("Hello")

# 等价于:
greet = decorator1(decorator2(greet))

# 执行顺序:
greet()
# Decorator 1 (外层先执行)
# Decorator 2 (内层后执行)
# Hello

# 实际应用
from functools import lru_cache
import time

@lru_cache(maxsize=128)
@timer
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 实用装饰器

```python
"""
常用装饰器实现
"""

# 1. 计时装饰器
import time
from functools import wraps

def timer(func):
    """测量执行时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end-start:.4f}s")
        return result
    return wrapper

# 2. 缓存装饰器
def memoize(func):
    """缓存函数结果"""
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# 3. 重试装饰器
def retry(max_attempts=3, delay=1):
    """失败时重试"""
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

# 4. 类型检查装饰器
def type_check(*types):
    """检查参数类型"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg, expected_type in zip(args, types):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Expected {expected_type}, got {type(arg)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@type_check(int, int)
def add(a, b):
    return a + b
```

---

## 类装饰器

### 装饰类

```python
"""
类装饰器: 修改类行为
"""

# 1. 添加方法的装饰器
def add_repr(cls):
    """添加__repr__方法"""
    def __repr__(self):
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(repr(p))  # Point(x=1, y=2)

# 2. 单例装饰器
def singleton(cls):
    """单例模式装饰器"""
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class Database:
    def __init__(self, url):
        self.url = url

db1 = Database("localhost")
db2 = Database("remote")
print(db1 is db2)  # True (同一实例)

# 3. 验证装饰器
def validate_attributes(cls):
    """验证属性装饰器"""
    original_init = cls.__init__
    
    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        # 验证属性
        for attr, value in self.__dict__.items():
            if value is None:
                raise ValueError(f"{attr} cannot be None")
    
    cls.__init__ = new_init
    return cls

@validate_attributes
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### 可调用类装饰器

```python
"""
使用类实现装饰器
"""

class CountCalls:
    """计数函数调用"""
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hello, {name}"

greet("Alice")  # Call 1 to greet
greet("Bob")    # Call 2 to greet

# 带参数的类装饰器
class Retry:
    """重试装饰器类"""
    def __init__(self, max_attempts=3):
        self.max_attempts = max_attempts
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
        return wrapper

@Retry(max_attempts=3)
def unreliable_function():
    import random
    if random.random() < 0.7:
        raise ValueError("Failed")
    return "Success"
```

---

## 元类

### 元类基础

```python
"""
元类: 类的类
"""

# type是所有类的元类
class MyClass:
    pass

print(type(MyClass))  # <class 'type'>
print(type(int))      # <class 'type'>
print(type(type))     # <class 'type'>

# 使用type动态创建类
def init(self, x):
    self.x = x

MyClass = type(
    'MyClass',        # 类名
    (object,),        # 基类元组
    {                 # 类字典
        '__init__': init,
        'value': 42
    }
)

obj = MyClass(10)
print(obj.x)      # 10
print(obj.value)  # 42
```

### 自定义元类

```python
"""
自定义元类实现
"""

class Meta(type):
    """自定义元类"""
    
    def __new__(mcs, name, bases, namespace):
        """创建类"""
        print(f"Creating class {name}")
        # 修改类
        namespace['class_id'] = id(mcs)
        return super().__new__(mcs, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace):
        """初始化类"""
        print(f"Initializing class {name}")
        super().__init__(name, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        """创建实例"""
        print(f"Creating instance of {cls.__name__}")
        return super().__call__(*args, **kwargs)

class MyClass(metaclass=Meta):
    """使用自定义元类"""
    pass

# 输出:
# Creating class MyClass
# Initializing class MyClass

obj = MyClass()
# Creating instance of MyClass
```

### 元类应用

```python
"""
元类的实际应用
"""

# 1. 单例元类
class SingletonMeta(type):
    """单例元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, url):
        self.url = url

db1 = Database("localhost")
db2 = Database("remote")
print(db1 is db2)  # True

# 2. 注册元类
class PluginRegistry(type):
    """插件注册元类"""
    plugins = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'Plugin':  # 不注册基类
            mcs.plugins[name] = cls
        return cls

class Plugin(metaclass=PluginRegistry):
    """插件基类"""
    pass

class AudioPlugin(Plugin):
    """音频插件"""
    pass

class VideoPlugin(Plugin):
    """视频插件"""
    pass

print(PluginRegistry.plugins)
# {'AudioPlugin': <class 'AudioPlugin'>, 'VideoPlugin': <class 'VideoPlugin'>}

# 3. ORM元类
class ModelMeta(type):
    """ORM模型元类"""
    def __new__(mcs, name, bases, namespace):
        # 收集字段
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                fields[key] = value
                value.name = key
        
        namespace['_fields'] = fields
        return super().__new__(mcs, name, bases, namespace)

class Field:
    """字段基类"""
    def __init__(self, field_type):
        self.field_type = field_type
        self.name = None

class Model(metaclass=ModelMeta):
    """模型基类"""
    pass

class User(Model):
    """用户模型"""
    name = Field(str)
    age = Field(int)
    email = Field(str)

print(User._fields)  # 字段信息
```

---

## 描述符

### 描述符协议

```python
"""
描述符: __get__, __set__, __delete__
"""

class Descriptor:
    """描述符基类"""
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        """获取属性"""
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        """设置属性"""
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        """删除属性"""
        del instance.__dict__[self.name]

# 数据描述符 vs 非数据描述符
# 数据描述符: 定义了__get__和__set__
# 非数据描述符: 只定义了__get__

# 优先级:
# 1. 数据描述符
# 2. 实例字典
# 3. 非数据描述符
# 4. __getattr__
```

### 描述符应用

```python
"""
描述符的实际应用
"""

# 1. 类型验证描述符
class TypedProperty:
    """类型验证描述符"""
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}"
            )
        instance.__dict__[self.name] = value

class Person:
    name = TypedProperty("name", str)
    age = TypedProperty("age", int)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
# person.age = "30"  # TypeError

# 2. 惰性属性描述符
class LazyProperty:
    """惰性计算属性"""
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # 计算值
        value = self.func(instance)
        # 替换描述符为计算值
        setattr(instance, self.name, value)
        return value

class DataProcessor:
    @LazyProperty
    def expensive_result(self):
        """昂贵计算"""
        print("Computing...")
        return sum(range(1000000))

processor = DataProcessor()
print(processor.expensive_result)  # Computing... 499999500000
print(processor.expensive_result)  # 499999500000 (缓存)

# 3. 验证描述符
class Validated:
    """验证描述符"""
    def __init__(self, validator):
        self.validator = validator
        self.name = None
    
    def __set_name__(self, owner, name):
        """Python 3.6+ 自动获取属性名"""
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        instance.__dict__[self.name] = value

class User:
    email = Validated(lambda x: '@' in x)
    age = Validated(lambda x: 0 <= x <= 150)

user = User()
user.email = "alice@example.com"  # OK
# user.email = "invalid"  # ValueError
```

---

## 代码生成

### 动态类创建

```python
"""
动态创建类和函数
"""

# 1. 动态创建类
def create_class(name, **attrs):
    """动态创建类"""
    return type(name, (object,), attrs)

Person = create_class(
    'Person',
    __init__=lambda self, name: setattr(self, 'name', name),
    greet=lambda self: f"Hello, I'm {self.name}"
)

person = Person("Alice")
print(person.greet())

# 2. 动态创建函数
def create_function(name, params, body):
    """动态创建函数"""
    code = f"def {name}({params}):\n    {body}"
    namespace = {}
    exec(code, namespace)
    return namespace[name]

add = create_function('add', 'a, b', 'return a + b')
print(add(3, 4))  # 7

# 3. 使用exec动态执行
code = """
class DynamicClass:
    def __init__(self, value):
        self.value = value
"""

namespace = {}
exec(code, namespace)

DynamicClass = namespace['DynamicClass']
obj = DynamicClass(42)
```

### 代码生成工具

```python
"""
代码生成和模板
"""

# 1. 字符串模板
from string import Template

code_template = Template("""
class $classname:
    def __init__(self, $params):
        $assignments
    
    def __repr__(self):
        return f"$classname($repr_format)"
""")

def generate_class(name, fields):
    """生成数据类代码"""
    params = ', '.join(fields)
    assignments = '\n        '.join(f"self.{f} = {f}" for f in fields)
    repr_format = ', '.join(f"{f}={{self.{f}!r}}" for f in fields)
    
    code = code_template.substitute(
        classname=name,
        params=params,
        assignments=assignments,
        repr_format=repr_format
    )
    
    namespace = {}
    exec(code, namespace)
    return namespace[name]

Point = generate_class('Point', ['x', 'y'])
p = Point(1, 2)
print(repr(p))  # Point(x=1, y=2)
```

---

## 📚 核心要点

### 装饰器

- ✅ **本质**: 函数包装器
- ✅ **@wraps**: 保留元信息
- ✅ **装饰器工厂**: 带参数装饰器
- ✅ **装饰器链**: 组合多个装饰器

### 元类

- ✅ **type**: 默认元类
- ✅ **__new__**: 创建类
- ✅ **__init__**: 初始化类
- ✅ **__call__**: 创建实例
- ✅ **应用**: 单例、注册、ORM

### 描述符

- ✅ **__get__**: 获取属性
- ✅ **__set__**: 设置属性
- ✅ **__delete__**: 删除属性
- ✅ **应用**: 验证、懒加载、属性管理

### 最佳实践

- ✅ 装饰器优先于元类
- ✅ 简单问题用装饰器
- ✅ 复杂框架用元类
- ✅ 属性管理用描述符
- ✅ 谨慎使用动态代码生成

---

**掌握元编程，构建强大框架！** 🔮✨

**相关文档**:
- [05-functions-closures.md](05-functions-closures.md) - 函数与闭包
- [06-classes-inheritance.md](06-classes-inheritance.md) - 类与继承
- [../01-language-core/01-data-model.md](../01-language-core/01-data-model.md) - 数据模型

**最后更新**: 2025年10月28日

