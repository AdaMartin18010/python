# Python 函数与闭包

**函数定义、参数传递与闭包机制**

---

## 📋 目录

- [函数定义](#函数定义)
- [参数传递](#参数传递)
- [闭包机制](#闭包机制)
- [装饰器基础](#装饰器基础)
- [函数式编程](#函数式编程)

---

## 函数定义

### 基础函数定义

```python
"""
函数定义的各种形式
"""

# 1. 基础函数
def greet(name):
    """问候函数"""
    return f"Hello, {name}"

# 2. 带类型注解的函数
def add(x: int, y: int) -> int:
    """两数相加"""
    return x + y

# 3. 文档字符串
def complex_function(arg1, arg2):
    """
    复杂函数示例
    
    Args:
        arg1: 第一个参数
        arg2: 第二个参数
    
    Returns:
        处理结果
    
    Raises:
        ValueError: 参数无效时
    """
    pass

# 4. 函数属性
def func():
    pass

func.custom_attr = "value"  # 函数也是对象
print(func.__name__)        # 'func'
print(func.__doc__)         # None
```

### 函数对象

```python
"""
函数是一等公民(first-class)
"""

# 函数可以赋值给变量
def square(x):
    return x ** 2

sq = square
print(sq(5))  # 25

# 函数可以作为参数传递
def apply(func, value):
    return func(value)

result = apply(square, 5)  # 25

# 函数可以作为返回值
def make_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier

double = make_multiplier(2)
print(double(5))  # 10

# 函数可以存储在数据结构中
operations = {
    'add': lambda x, y: x + y,
    'sub': lambda x, y: x - y,
    'mul': lambda x, y: x * y,
}

print(operations['add'](3, 4))  # 7

# 查看函数信息
import inspect

def example(a, b=10):
    pass

sig = inspect.signature(example)
print(sig)  # (a, b=10)
print(sig.parameters)
```

---

## 参数传递

### 参数类型

```python
"""
Python函数参数的完整语法
"""

def full_syntax(
    pos1, pos2,              # 仅位置参数 (3.8+之前)
    /,                        # 仅位置参数分隔符 (3.8+)
    pos_or_kw1, pos_or_kw2,  # 位置或关键字参数
    *args,                    # 可变位置参数
    kw1, kw2,                 # 仅关键字参数
    **kwargs                  # 可变关键字参数
):
    """完整的参数语法"""
    pass

# 调用示例
full_syntax(
    1, 2,                     # 仅位置
    3, 4,                     # 位置或关键字
    5, 6,                     # *args
    kw1=7, kw2=8,            # 仅关键字
    extra1=9, extra2=10      # **kwargs
)
```

### 位置参数与关键字参数

```python
"""
位置参数和关键字参数详解
"""

# 1. 位置参数
def func(a, b, c):
    return a + b + c

func(1, 2, 3)  # OK

# 2. 关键字参数
func(a=1, b=2, c=3)  # OK
func(1, b=2, c=3)    # OK (混合)
# func(a=1, 2, 3)    # Error! 位置参数必须在关键字参数前

# 3. 仅位置参数 (Python 3.8+)
def func(a, b, /, c, d):
    """
    a, b: 仅位置参数
    c, d: 位置或关键字参数
    """
    pass

func(1, 2, 3, 4)        # OK
func(1, 2, c=3, d=4)    # OK
# func(a=1, b=2, c=3, d=4)  # Error! a,b必须用位置传递

# 4. 仅关键字参数
def func(a, b, *, c, d):
    """
    a, b: 位置或关键字参数
    c, d: 仅关键字参数
    """
    pass

func(1, 2, c=3, d=4)    # OK
# func(1, 2, 3, 4)      # Error! c,d必须用关键字传递

# 5. 完整示例
def create_user(
    user_id, /,              # 仅位置
    name, email,             # 位置或关键字
    *,                       # 仅关键字分隔符
    age=None, phone=None     # 仅关键字(带默认值)
):
    """创建用户"""
    pass

create_user(123, "Alice", "alice@example.com", age=30)
```

### 可变参数

```python
"""
*args 和 **kwargs
"""

# 1. 可变位置参数 (*args)
def sum_all(*args):
    """接受任意数量的位置参数"""
    return sum(args)

print(sum_all(1, 2, 3, 4, 5))  # 15

# 2. 可变关键字参数 (**kwargs)
def print_info(**kwargs):
    """接受任意数量的关键字参数"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")

# 3. 组合使用
def flexible_func(required, *args, **kwargs):
    """组合各种参数"""
    print(f"Required: {required}")
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

flexible_func(1, 2, 3, x=4, y=5)
# Required: 1
# Args: (2, 3)
# Kwargs: {'x': 4, 'y': 5}

# 4. 参数解包
def func(a, b, c):
    return a + b + c

args = (1, 2, 3)
print(func(*args))  # 6

kwargs = {'a': 1, 'b': 2, 'c': 3}
print(func(**kwargs))  # 6

# 5. 转发参数
def wrapper(*args, **kwargs):
    """转发所有参数"""
    return original_func(*args, **kwargs)
```

### 默认参数

```python
"""
默认参数的陷阱
"""

# ❌ 可变默认参数陷阱
def append_to(element, lst=[]):
    """危险!默认参数只创建一次"""
    lst.append(element)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - 危险!共享同一列表

# ✅ 正确做法
def append_to(element, lst=None):
    """使用None作为哨兵值"""
    if lst is None:
        lst = []
    lst.append(element)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [2] - 正确!

# 默认参数求值时机
def func(x, lst=None):
    """默认参数在函数定义时求值"""
    if lst is None:
        lst = []
    return lst

# 时间戳陷阱
from datetime import datetime

def log(message, timestamp=datetime.now()):  # ❌ 错误!
    """时间戳在函数定义时确定"""
    print(f"[{timestamp}] {message}")

# 正确做法
def log(message, timestamp=None):  # ✅ 正确
    if timestamp is None:
        timestamp = datetime.now()
    print(f"[{timestamp}] {message}")
```

---

## 闭包机制

### 闭包基础

```python
"""
闭包: 函数 + 捕获的外部变量
"""

# 1. 基础闭包
def make_counter():
    """创建计数器闭包"""
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

c1 = make_counter()
print(c1())  # 1
print(c1())  # 2

c2 = make_counter()
print(c2())  # 1 (独立的计数器)

# 2. 查看闭包变量
print(c1.__closure__)  # 闭包单元格
print(c1.__closure__[0].cell_contents)  # 2

# 3. 多个闭包共享外部变量
def make_accumulator():
    """创建累加器"""
    total = 0
    
    def add(x):
        nonlocal total
        total += x
        return total
    
    def reset():
        nonlocal total
        total = 0
    
    return add, reset

add, reset = make_accumulator()
print(add(10))  # 10
print(add(5))   # 15
reset()
print(add(1))   # 1
```

### 闭包应用

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

# 2. 数据隐藏/封装
def make_account(initial_balance):
    """创建银行账户"""
    balance = initial_balance
    
    def deposit(amount):
        nonlocal balance
        if amount > 0:
            balance += amount
        return balance
    
    def withdraw(amount):
        nonlocal balance
        if 0 < amount <= balance:
            balance -= amount
            return balance
        return "Insufficient funds"
    
    def get_balance():
        return balance
    
    # 返回操作接口
    return {
        'deposit': deposit,
        'withdraw': withdraw,
        'balance': get_balance
    }

account = make_account(100)
print(account['deposit'](50))      # 150
print(account['withdraw'](30))     # 120
print(account['balance']())        # 120
# 无法直接访问balance变量!

# 3. 回调函数
def setup_button(button_id, callback_factory):
    """设置按钮回调"""
    def on_click():
        callback = callback_factory(button_id)
        callback()
    return on_click

def make_callback(button_id):
    def callback():
        print(f"Button {button_id} clicked")
    return callback

button1 = setup_button(1, make_callback)
button1()  # Button 1 clicked

# 4. 延迟求值
def make_lazy_value(func):
    """惰性求值"""
    cached = None
    computed = False
    
    def get_value():
        nonlocal cached, computed
        if not computed:
            cached = func()
            computed = True
        return cached
    
    return get_value

expensive = make_lazy_value(lambda: sum(range(1000000)))
# 此时还未计算

print(expensive())  # 第一次调用时计算
print(expensive())  # 使用缓存值
```

### 闭包陷阱

```python
"""
闭包常见陷阱
"""

# 陷阱1: 循环中的闭包
functions = []
for i in range(3):
    def func():
        return i
    functions.append(func)

# 期望: [0, 1, 2]
# 实际: [2, 2, 2]
print([f() for f in functions])

# 原因: 闭包捕获的是变量i本身,不是值!
# 当调用func时,循环已结束,i=2

# ✅ 解决方法1: 默认参数
functions = []
for i in range(3):
    def func(x=i):  # 立即绑定i的当前值
        return x
    functions.append(func)

print([f() for f in functions])  # [0, 1, 2]

# ✅ 解决方法2: 额外的闭包层
functions = []
for i in range(3):
    def make_func(x):
        def func():
            return x
        return func
    functions.append(make_func(i))

print([f() for f in functions])  # [0, 1, 2]

# ✅ 解决方法3: functools.partial
from functools import partial

def func(x):
    return x

functions = [partial(func, i) for i in range(3)]
print([f() for f in functions])  # [0, 1, 2]
```

---

## 装饰器基础

### 函数装饰器

```python
"""
装饰器: 修改函数行为的函数
"""

# 1. 基础装饰器
def trace(func):
    """追踪函数调用"""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@trace
def add(a, b):
    return a + b

add(3, 4)
# Calling add
# add returned 7

# 等价于
def add(a, b):
    return a + b

add = trace(add)

# 2. 保留函数元数据
from functools import wraps

def trace(func):
    @wraps(func)  # 保留原函数的__name__, __doc__等
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# 3. 带参数的装饰器
def repeat(n):
    """重复执行n次"""
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

# 4. 类装饰器
class CountCalls:
    """计数函数调用次数"""
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()  # Call 1 to say_hello
say_hello()  # Call 2 to say_hello
```

### 装饰器应用

```python
"""
装饰器的实际应用
"""

# 1. 计时装饰器
import time
from functools import wraps

def timer(func):
    """测量函数执行时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

# 2. 缓存装饰器
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    """缓存斐波那契结果"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 3. 验证装饰器
def validate_positive(func):
    """验证参数为正数"""
    @wraps(func)
    def wrapper(x):
        if x <= 0:
            raise ValueError("Argument must be positive")
        return func(x)
    return wrapper

@validate_positive
def square_root(x):
    return x ** 0.5

# 4. 重试装饰器
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
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def unreliable_operation():
    """可能失败的操作"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Failed")
    return "Success"
```

---

## 函数式编程

### 高阶函数

```python
"""
高阶函数: 接受函数作为参数或返回函数
"""

# 1. map: 映射
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
# [1, 4, 9, 16, 25]

# 2. filter: 过滤
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4]

# 3. reduce: 归约
from functools import reduce

sum_all = reduce(lambda x, y: x + y, numbers)
# 15

product = reduce(lambda x, y: x * y, numbers)
# 120

# 4. 组合使用
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers))
)
# 2**2 + 4**2 = 4 + 16 = 20

# 5. 列表推导式 vs 函数式
# 函数式
result = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))

# 列表推导式 (更Pythonic)
result = [x**2 for x in numbers if x % 2 == 0]
```

### 函数组合

```python
"""
函数组合模式
"""

# 1. 简单组合
def compose(f, g):
    """组合两个函数"""
    return lambda x: f(g(x))

def double(x):
    return x * 2

def increment(x):
    return x + 1

# f(g(x))
double_then_increment = compose(increment, double)
print(double_then_increment(5))  # (5*2)+1 = 11

# 2. 多函数组合
def compose_all(*funcs):
    """组合多个函数"""
    def composed(x):
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return composed

pipeline = compose_all(
    lambda x: x + 1,
    lambda x: x * 2,
    lambda x: x ** 2
)

print(pipeline(3))  # ((3**2)*2)+1 = 19

# 3. 管道模式
class Pipeline:
    """函数管道"""
    def __init__(self, value):
        self.value = value
    
    def pipe(self, func):
        """应用函数"""
        self.value = func(self.value)
        return self
    
    def get(self):
        """获取结果"""
        return self.value

result = (Pipeline(5)
    .pipe(lambda x: x ** 2)
    .pipe(lambda x: x * 2)
    .pipe(lambda x: x + 1)
    .get())

print(result)  # 51
```

---

## 📚 核心要点

### 函数定义

- ✅ **def关键字**: 定义函数
- ✅ **文档字符串**: 函数说明
- ✅ **类型注解**: 提高可读性
- ✅ **函数对象**: 一等公民

### 参数

- ✅ **位置参数**: 按顺序传递
- ✅ **关键字参数**: 按名称传递
- ✅ ***args**: 可变位置参数
- ✅ ****kwargs**: 可变关键字参数
- ✅ **/和***: 参数类型分隔符

### 闭包

- ✅ **定义**: 函数+捕获的变量
- ✅ **nonlocal**: 修改外层变量
- ✅ **应用**: 工厂、封装、回调
- ✅ **陷阱**: 循环中的闭包

### 装饰器

- ✅ **@语法**: 语法糖
- ✅ **wraps**: 保留元数据
- ✅ **带参数**: 装饰器工厂
- ✅ **应用**: 计时、缓存、验证

### 最佳实践

- ✅ 避免可变默认参数
- ✅ 使用类型注解
- ✅ 编写文档字符串
- ✅ 单一职责原则
- ✅ 合理使用闭包和装饰器

---

**掌握函数与闭包，写出优雅代码！** 🎯✨

**相关文档**:
- [04-statements.md](04-statements.md) - 语句语义
- [06-classes-inheritance.md](06-classes-inheritance.md) - 类与继承
- [07-decorators-metaprogramming.md](07-decorators-metaprogramming.md) - 装饰器与元编程

**最后更新**: 2025年10月28日

