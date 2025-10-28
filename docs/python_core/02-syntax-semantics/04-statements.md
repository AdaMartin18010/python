# Python 语句语义

**语句的执行与控制流**

---

## 📋 目录

- [语句基础](#语句基础)
- [赋值语句](#赋值语句)
- [控制流语句](#控制流语句)
- [异常处理](#异常处理)
- [上下文管理](#上下文管理)

---

## 语句基础

### 语句 vs 表达式

```python
"""
语句和表达式的区别
"""

# 表达式: 有返回值
x + y          # 表达式
func(a, b)     # 表达式
[i for i in range(10)]  # 表达式

# 语句: 执行动作，通常无返回值
x = 42         # 赋值语句
if x > 0:      # if语句
    print(x)
for i in range(10):  # for语句
    pass

# 表达式语句: 表达式作为语句
print("hello")  # 函数调用表达式作为语句
x + y           # 表达式语句 (结果被丢弃)

# 海象运算符: 赋值表达式 (Python 3.8+)
if (n := len(data)) > 10:  # 赋值同时是表达式
    print(f"Length: {n}")
```

### 简单语句

```python
"""
简单语句 (single-line)
"""

# 1. 表达式语句
func()
x + y

# 2. 赋值语句
x = 42

# 3. assert语句
assert x > 0, "x must be positive"

# 4. pass语句 (空操作)
if condition:
    pass  # 什么都不做

# 5. del语句
del x
del lst[0]
del dict['key']

# 6. return语句
def func():
    return value

# 7. yield语句
def generator():
    yield value

# 8. raise语句
raise ValueError("error message")

# 9. break/continue
for i in range(10):
    if i == 5:
        break

# 10. import语句
import module
from module import name

# 11. global/nonlocal
global x
nonlocal y

# 12. type语句 (Python 3.12+)
type Point = tuple[float, float]
```

---

## 赋值语句

### 基础赋值

```python
"""
赋值语句的各种形式
"""

# 1. 简单赋值
x = 42

# 2. 多重赋值
x = y = z = 0

# 3. 解包赋值
a, b = 1, 2
x, y, z = [1, 2, 3]
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2,3,4]
*init, last = [1, 2, 3, 4]   # init=[1,2,3], last=4

# 4. 交换
x, y = y, x  # 不需要临时变量

# 5. 嵌套解包
(a, b), (c, d) = [(1, 2), (3, 4)]

# 6. 忽略值
x, _, z = (1, 2, 3)  # 忽略中间值
for _ in range(10):  # 不关心循环变量
    do_something()
```

### 增强赋值

```python
"""
增强赋值运算符
"""

# 算术增强赋值
x += 1   # x = x + 1
x -= 1   # x = x - 1
x *= 2   # x = x * 2
x /= 2   # x = x / 2
x //= 2  # x = x // 2
x %= 2   # x = x % 2
x **= 2  # x = x ** 2

# 位增强赋值
x &= mask   # x = x & mask
x |= mask   # x = x | mask
x ^= mask   # x = x ^ mask
x <<= 1     # x = x << 1
x >>= 1     # x = x >> 1

# 注意: 增强赋值是原地修改
lst = [1, 2, 3]
lst += [4, 5]  # lst.extend([4, 5])

# vs 普通赋值创建新对象
lst = lst + [4, 5]  # 创建新列表

# 可变对象 vs 不可变对象
a = [1, 2]
b = a
a += [3]    # a和b都是[1,2,3] (原地修改)

a = (1, 2)
b = a
a += (3,)   # a是(1,2,3), b仍是(1,2) (创建新对象)
```

### 注解赋值

```python
"""
类型注解赋值 (Python 3.6+)
"""

# 变量注解
name: str = "Alice"
age: int = 30
scores: list[int] = [95, 87, 92]

# 仅注解(不赋值)
pending: list[str]  # 声明但不初始化

# 类属性注解
class User:
    name: str
    age: int
    email: str | None = None  # 带默认值

# 注解不影响运行时
x: int = "hello"  # 不会报错(运行时)
# 但mypy会报错(静态检查)
```

---

## 控制流语句

### if语句

```python
"""
条件语句
"""

# 基础if语句
if condition:
    do_something()

# if-else
if condition:
    do_something()
else:
    do_other()

# if-elif-else
if x > 0:
    print("positive")
elif x < 0:
    print("negative")
else:
    print("zero")

# 嵌套if
if outer_condition:
    if inner_condition:
        do_something()

# 条件表达式(三元运算符)
result = value_if_true if condition else value_if_false

# 真值测试
"""
False值: None, False, 0, 0.0, "", [], {}, set()
True值: 其他所有值
"""

if lst:  # 列表非空
    process(lst)

if not dict:  # 字典为空
    dict = {}
```

### while循环

```python
"""
while循环语句
"""

# 基础while
while condition:
    do_something()

# while-else
while condition:
    do_something()
else:
    # 循环正常结束时执行(没有break)
    print("Loop completed")

# 无限循环
while True:
    data = get_data()
    if not data:
        break
    process(data)

# 哨兵循环
while (line := file.readline()) != "":  # Python 3.8+
    process(line)

# break vs continue
while condition:
    if should_skip:
        continue  # 跳过本次循环
    if should_stop:
        break     # 退出循环
    process()
```

### for循环

```python
"""
for循环语句
"""

# 基础for循环
for item in iterable:
    process(item)

# for-else
for item in iterable:
    if found(item):
        break
else:
    # 循环正常结束时执行(没有break)
    print("Not found")

# 遍历索引
for i in range(len(lst)):
    print(f"{i}: {lst[i]}")

# enumerate (更Pythonic)
for i, item in enumerate(lst):
    print(f"{i}: {item}")

# zip并行迭代
for x, y in zip(list1, list2):
    print(f"{x} - {y}")

# 字典迭代
for key in dict:  # 迭代键
    process(key)

for value in dict.values():  # 迭代值
    process(value)

for key, value in dict.items():  # 迭代键值对
    print(f"{key}: {value}")

# 嵌套循环
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")

# break在嵌套循环中
for i in range(3):
    for j in range(3):
        if i == j == 1:
            break  # 只退出内层循环
    print(f"i = {i}")

# 需要退出外层循环的技巧
found = False
for i in range(3):
    for j in range(3):
        if i == j == 1:
            found = True
            break
    if found:
        break
```

---

## 异常处理

### try-except语句

```python
"""
异常处理语句
"""

# 基础try-except
try:
    risky_operation()
except Exception as e:
    handle_error(e)

# 多个except
try:
    operation()
except ValueError:
    handle_value_error()
except TypeError:
    handle_type_error()
except (KeyError, IndexError) as e:
    handle_lookup_error(e)

# try-except-else
try:
    result = operation()
except Exception as e:
    handle_error(e)
else:
    # 没有异常时执行
    process_result(result)

# try-except-finally
try:
    file = open("data.txt")
    process(file)
except FileNotFoundError:
    print("File not found")
finally:
    # 总是执行(无论是否异常)
    if file:
        file.close()

# 完整形式
try:
    operation()
except SpecificError as e:
    handle_specific(e)
except Exception as e:
    handle_general(e)
else:
    # 无异常时
    success_handler()
finally:
    # 总是执行
    cleanup()

# 捕获所有异常(不推荐)
try:
    operation()
except:  # 危险!会捕获KeyboardInterrupt等
    handle_error()

# 推荐方式
try:
    operation()
except Exception as e:  # 不捕获系统异常
    handle_error(e)
```

### raise语句

```python
"""
抛出异常
"""

# 基础raise
raise ValueError("Invalid value")

# raise已捕获的异常
try:
    operation()
except Exception as e:
    log_error(e)
    raise  # 重新抛出原异常

# 异常链(Python 3)
try:
    operation()
except Exception as e:
    raise RuntimeError("Operation failed") from e

# 抑制异常上下文
try:
    operation()
except Exception:
    raise RuntimeError("New error") from None

# 自定义异常
class ValidationError(Exception):
    """验证错误"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

raise ValidationError("email", "Invalid format")

# 异常组 (Python 3.11+)
try:
    operation()
except* ValueError as eg:
    # 处理异常组中的ValueError
    for e in eg.exceptions:
        handle_error(e)
```

### assert语句

```python
"""
断言语句
"""

# 基础assert
assert condition, "error message"

# 等价于
if __debug__:
    if not condition:
        raise AssertionError("error message")

# 使用场景
def divide(a, b):
    assert b != 0, "Division by zero"
    return a / b

# 多个断言
assert isinstance(x, int), "x must be int"
assert x > 0, "x must be positive"

# 注意: -O优化模式会禁用assert
# python -O script.py  # __debug__ == False

# 不要用assert处理运行时错误
# ❌ assert user.is_authenticated(), "Not logged in"
# ✅ if not user.is_authenticated():
#        raise PermissionError("Not logged in")
```

---

## 上下文管理

### with语句

```python
"""
with语句和上下文管理器
"""

# 基础with
with open("file.txt") as f:
    data = f.read()
# 自动关闭文件

# 等价代码
f = open("file.txt")
try:
    data = f.read()
finally:
    f.close()

# 多个上下文管理器
with open("input.txt") as fin, open("output.txt", "w") as fout:
    data = fin.read()
    fout.write(data)

# 嵌套with
with A() as a:
    with B() as b:
        use(a, b)

# 等价的简化形式 (Python 3.1+)
with A() as a, B() as b:
    use(a, b)

# 自定义上下文管理器
class ManagedResource:
    def __enter__(self):
        print("Acquiring resource")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        # 返回True抑制异常,False传播异常
        return False

with ManagedResource() as resource:
    use(resource)

# 使用contextlib
from contextlib import contextmanager

@contextmanager
def managed_resource():
    # __enter__
    print("Acquiring")
    resource = acquire()
    try:
        yield resource
    finally:
        # __exit__
        print("Releasing")
        release(resource)

with managed_resource() as r:
    use(r)

# 异步with (Python 3.5+)
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.text()
```

---

## 📚 核心要点

### 语句类型

- ✅ **简单语句**: 赋值、断言、pass、del等
- ✅ **复合语句**: if、for、while、try、with等
- ✅ **控制流**: break、continue、return、raise

### 赋值

- ✅ **解包**: a, b = 1, 2
- ✅ **增强**: x += 1
- ✅ **注解**: x: int = 42
- ✅ **海象**: (n := expr)

### 控制流

- ✅ **if**: 条件分支
- ✅ **for**: 遍历迭代
- ✅ **while**: 条件循环
- ✅ **else**: 循环正常结束

### 异常处理

- ✅ **try-except**: 捕获异常
- ✅ **try-finally**: 清理资源
- ✅ **raise**: 抛出异常
- ✅ **assert**: 调试断言

### 上下文管理

- ✅ **with**: 自动资源管理
- ✅ **__enter__/__exit__**: 协议
- ✅ **contextmanager**: 装饰器
- ✅ **async with**: 异步上下文

### 最佳实践

- ✅ 使用with管理资源
- ✅ 具体异常优先捕获
- ✅ 避免裸except
- ✅ finally中清理资源
- ✅ assert用于调试而非错误处理

---

**掌握语句语义，控制程序流程！** 🎮✨

**相关文档**:
- [03-expressions.md](03-expressions.md) - 表达式语义
- [05-functions-closures.md](05-functions-closures.md) - 函数与闭包
- [../01-language-core/04-execution-model.md](../01-language-core/04-execution-model.md) - 执行模型

**最后更新**: 2025年10月28日

