# Python 表达式语义

**表达式的求值与语义**

---

## 📋 目录

- [表达式基础](#表达式基础)
- [运算符表达式](#运算符表达式)
- [函数调用表达式](#函数调用表达式)
- [推导式表达式](#推导式表达式)
- [特殊表达式](#特殊表达式)

---

## 表达式基础

### 表达式的定义

```python
"""
表达式: 可以求值并产生结果的代码片段
"""

# 简单表达式
42                    # 字面量表达式
x                     # 名称表达式
x + y                 # 二元运算表达式
func(arg)             # 函数调用表达式

# 表达式 vs 语句
x = 42                # 赋值语句 (不是表达式)
y = (x := 42)         # 海象运算符 (表达式)

# Python 3.8+ 海象运算符
if (n := len(data)) > 10:
    print(f"List is too long ({n} elements)")
```

### 表达式求值顺序

```python
"""
表达式求值的一般规则
"""

# 1. 从左到右求值
def f(x):
    print(f"f({x})")
    return x

result = f(1) + f(2) + f(3)
# 输出: f(1), f(2), f(3)
# 求值顺序: f(1) → f(2) → f(3) → 加法

# 2. 参数求值顺序
def func(a, b, c):
    print(a, b, c)

func(f(1), f(2), f(3))
# 输出: f(1), f(2), f(3), 1 2 3
# 从左到右求值参数

# 3. 关键字参数求值顺序
func(c=f(3), a=f(1), b=f(2))
# 输出: f(3), f(1), f(2), 1 2 3
# 按出现顺序求值，但按参数名传递

# 4. 操作数求值顺序
x[f(1)] = f(2)
# 先求值 f(1) (索引), 再求值 f(2) (值)
```

---

## 运算符表达式

### 算术运算符

```python
"""
算术运算符及其语义
"""

# 基础算术
a + b        # 加法: __add__
a - b        # 减法: __sub__
a * b        # 乘法: __mul__
a / b        # 除法: __truediv__ (总是返回float)
a // b       # 整除: __floordiv__
a % b        # 取模: __mod__
a ** b       # 幂运算: __pow__ (右结合)
-a           # 负号: __neg__
+a           # 正号: __pos__

# 特殊情况
10 / 3       # 3.3333...
10 // 3      # 3
10 % 3       # 1
-10 % 3      # 2 (结果符号与除数相同)

# 幂运算右结合
2 ** 3 ** 2  # 512 (= 2 ** (3 ** 2))
(2 ** 3) ** 2  # 64

# 复数运算
(3+4j) + (1+2j)  # (4+6j)
abs(3+4j)        # 5.0

# 矩阵乘法 @ (Python 3.5+)
import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
C = A @ B  # 矩阵乘法
```

### 比较运算符

```python
"""
比较运算符的语义
"""

# 基础比较
a < b        # 小于: __lt__
a <= b       # 小于等于: __le__
a > b        # 大于: __gt__
a >= b       # 大于等于: __ge__
a == b       # 等于: __eq__
a != b       # 不等于: __ne__

# 链式比较
x = 5
1 < x < 10   # True (等价于 1 < x and x < 10)
1 < x <= 5   # True
1 < 2 < 3 < 4  # True

# 身份比较
a is b       # 身份相同 (id(a) == id(b))
a is not b   # 身份不同

# 成员测试
x in lst     # __contains__
x not in lst # not (x in lst)

# 特殊情况
float('nan') == float('nan')  # False (NaN不等于自身)
None is None  # True (None是单例)

# 自定义比较
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

v1 = Version(1, 2)
v2 = Version(1, 3)
print(v1 < v2)  # True
```

### 逻辑运算符

```python
"""
逻辑运算符的短路求值
"""

# and 运算符
x and y
# 如果 x 为假，返回 x
# 否则返回 y

False and expensive_function()  # False (不调用函数)
True and expensive_function()   # 调用函数

# or 运算符
x or y
# 如果 x 为真，返回 x
# 否则返回 y

True or expensive_function()   # True (不调用函数)
False or expensive_function()  # 调用函数

# not 运算符
not x  # 如果 x 为假返回 True，否则返回 False

# 实际应用
def get_name(user):
    """获取用户名，提供默认值"""
    return user.get('name') or 'Anonymous'

# 多个条件
value = a or b or c or default  # 返回第一个真值

# 复杂条件
if username and password and is_valid(username):
    login(username, password)
```

### 位运算符

```python
"""
位运算符
"""

# 位运算
a & b        # 按位与: __and__
a | b        # 按位或: __or__
a ^ b        # 按位异或: __xor__
~a           # 按位取反: __invert__
a << n       # 左移: __lshift__
a >> n       # 右移: __rshift__

# 示例
0b1010 & 0b1100  # 0b1000 (8)
0b1010 | 0b1100  # 0b1110 (14)
0b1010 ^ 0b1100  # 0b0110 (6)
~0b1010          # -11 (补码)

# 左移右移
8 << 1   # 16 (相当于 * 2)
8 >> 1   # 4 (相当于 // 2)

# 应用: 权限位
READ = 0b0001
WRITE = 0b0010
EXECUTE = 0b0100
DELETE = 0b1000

permissions = READ | WRITE  # 0b0011
has_write = permissions & WRITE  # 非零表示有写权限

# 位掩码
def set_bit(value, bit):
    return value | (1 << bit)

def clear_bit(value, bit):
    return value & ~(1 << bit)

def toggle_bit(value, bit):
    return value ^ (1 << bit)
```

---

## 函数调用表达式

### 调用语法

```python
"""
函数调用的各种形式
"""

# 1. 位置参数
func(a, b, c)

# 2. 关键字参数
func(a=1, b=2, c=3)
func(1, b=2, c=3)  # 混合

# 3. 参数解包
args = (1, 2, 3)
func(*args)  # func(1, 2, 3)

kwargs = {'a': 1, 'b': 2}
func(**kwargs)  # func(a=1, b=2)

func(*args, **kwargs)  # 组合解包

# 4. 仅位置参数 (Python 3.8+)
def func(a, b, /, c, d, *, e, f):
    """
    a, b: 仅位置
    c, d: 位置或关键字
    e, f: 仅关键字
    """
    pass

func(1, 2, 3, 4, e=5, f=6)  # OK
# func(a=1, b=2, c=3, d=4, e=5, f=6)  # Error!
```

### 调用语义

```python
"""
函数调用的求值过程
"""

# 求值步骤:
"""
1. 求值函数表达式
2. 从左到右求值位置参数
3. 按出现顺序求值关键字参数
4. 应用参数解包
5. 绑定参数到形参
6. 执行函数体
"""

def trace_call():
    """追踪调用过程"""

    def f(x):
        print(f"f({x})")
        return x

    def func(a, b, c):
        print(f"func called: a={a}, b={b}, c={c}")
        return a + b + c

    # 调用
    result = func(f(1), f(2), c=f(3))
    """
    输出:
    f(1)
    f(2)
    f(3)
    func called: a=1, b=2, c=3
    """

# 默认参数陷阱
def append_to(element, lst=[]):  # 危险!
    lst.append(element)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - 共享同一列表!

# 正确做法
def append_to(element, lst=None):
    if lst is None:
        lst = []
    lst.append(element)
    return lst
```

---

## 推导式表达式

### 列表推导式

```python
"""
列表推导式语法与语义
"""

# 基础形式
[expr for var in iterable]

# 示例
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件过滤
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# 嵌套循环
pairs = [(x, y) for x in range(3) for y in range(3)]
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# 等价的嵌套for循环
pairs = []
for x in range(3):
    for y in range(3):
        pairs.append((x, y))

# 多重条件
result = [x for x in range(20) if x % 2 == 0 if x % 3 == 0]
# [0, 6, 12, 18]

# 嵌套推导式
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

transposed = [[row[i] for row in matrix] for i in range(3)]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

### 其他推导式

```python
"""
集合、字典和生成器推导式
"""

# 集合推导式
unique_lengths = {len(word) for word in words}

# 字典推导式
word_lengths = {word: len(word) for word in words}

# 带条件
long_words = {word: len(word) for word in words if len(word) > 5}

# 生成器推导式
gen = (x**2 for x in range(10))  # 生成器对象
print(next(gen))  # 0
print(next(gen))  # 1

# 内存对比
import sys
list_comp = [x for x in range(1000000)]
gen_exp = (x for x in range(1000000))

print(sys.getsizeof(list_comp))  # ~8MB
print(sys.getsizeof(gen_exp))    # ~128字节

# 应用场景
# ✅ 需要多次迭代 → 列表推导式
# ✅ 只迭代一次 → 生成器表达式
# ✅ 大数据集 → 生成器表达式

# 实际例子
total = sum(x**2 for x in range(1000000))  # 使用生成器
```

---

## 特殊表达式

### 条件表达式

```python
"""
三元条件表达式
"""

# 语法: value_if_true if condition else value_if_false
result = x if x > 0 else -x  # 绝对值

# 嵌套条件表达式
sign = "positive" if x > 0 else "negative" if x < 0 else "zero"

# 等价if语句
if x > 0:
    sign = "positive"
elif x < 0:
    sign = "negative"
else:
    sign = "zero"

# 应用场景
# 默认值
name = user.get('name') if user else 'Anonymous'

# 简单映射
color = "red" if score < 60 else "green"

# 列表推导式中
adjusted = [x if x > 0 else 0 for x in values]
```

### Lambda表达式

```python
"""
Lambda表达式: 匿名函数
"""

# 基础语法
lambda arguments: expression

# 示例
square = lambda x: x**2
print(square(5))  # 25

# 多个参数
add = lambda x, y: x + y
print(add(3, 4))  # 7

# 配合高阶函数
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# 排序
pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
# [(1, 'one'), (3, 'three'), (2, 'two')]

# 限制: 只能包含表达式，不能包含语句
# ❌ lambda x: if x > 0: return x  # 语法错误
# ✅ lambda x: x if x > 0 else 0   # OK

# 何时使用lambda
# ✅ 简单的单行函数
# ✅ 作为参数传递
# ❌ 复杂逻辑 (使用def)
# ❌ 需要文档字符串
```

### 属性引用

```python
"""
属性引用表达式
"""

# 基础语法
obj.attribute

# 链式引用
user.profile.address.city

# 动态属性访问
getattr(obj, 'attribute')
getattr(obj, 'attribute', default_value)

# 检查属性
hasattr(obj, 'attribute')

# 设置属性
setattr(obj, 'attribute', value)

# 删除属性
delattr(obj, 'attribute')

# 属性查找顺序
"""
1. 实例字典: obj.__dict__
2. 类字典: type(obj).__dict__
3. 父类字典: (MRO顺序)
4. __getattr__ 方法
"""

# 动态属性示例
class DynamicAttrs:
    def __getattr__(self, name):
        return f"Dynamic: {name}"

obj = DynamicAttrs()
print(obj.anything)  # "Dynamic: anything"
```

### 切片表达式

```python
"""
切片语法与语义
"""

# 基础切片: [start:stop:step]
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

lst[2:5]     # [2, 3, 4]
lst[:5]      # [0, 1, 2, 3, 4]
lst[5:]      # [5, 6, 7, 8, 9]
lst[:]       # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] (浅拷贝)

# 带步长
lst[::2]     # [0, 2, 4, 6, 8] (偶数索引)
lst[1::2]    # [1, 3, 5, 7, 9] (奇数索引)
lst[::-1]    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] (反转)

# 负索引
lst[-3:]     # [7, 8, 9]
lst[:-3]     # [0, 1, 2, 3, 4, 5, 6]

# 切片赋值
lst[2:5] = [20, 30, 40]
lst[2:5] = []  # 删除元素

# 切片对象
s = slice(2, 5, 1)
lst[s]  # 等价于 lst[2:5]

# 多维切片 (NumPy)
import numpy as np
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr[1:, :2]  # [[4, 5], [7, 8]]
```

---

## 📚 核心要点

### 表达式求值

- ✅ **从左到右**: 一般求值顺序
- ✅ **短路求值**: and, or 运算符
- ✅ **优先级**: 决定求值顺序
- ✅ **惰性求值**: 生成器表达式

### 运算符

- ✅ **算术**: +, -, *, /, //, %, **
- ✅ **比较**: <, <=, >, >=, ==, !=, is, in
- ✅ **逻辑**: and, or, not
- ✅ **位运算**: &, |, ^, ~, <<, >>

### 特殊表达式

- ✅ **条件**: value if cond else other
- ✅ **Lambda**: lambda args: expr
- ✅ **推导式**: [expr for x in iter]
- ✅ **切片**: seq[start:stop:step]

### 最佳实践

- ✅ 使用括号明确优先级
- ✅ 推导式优于循环(简单情况)
- ✅ 避免过度使用lambda
- ✅ 利用短路求值优化
- ✅ 注意可变默认参数

---

**掌握表达式语义，写出高效代码！** 💫✨

**相关文档**:

- [02-grammar.md](02-grammar.md) - 语法结构
- [04-statements.md](04-statements.md) - 语句语义
- [05-functions-closures.md](05-functions-closures.md) - 函数与闭包

**最后更新**: 2025年10月28日
