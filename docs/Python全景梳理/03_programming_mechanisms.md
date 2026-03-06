# Python程序设计机制：形式论证与推理

> 本文档系统梳理Python程序设计的核心机制，包含形式定义、属性关系、逻辑推导、正例反例及性能分析。

---

## 目录

- [Python程序设计机制：形式论证与推理](#python程序设计机制形式论证与推理)
  - [目录](#目录)
  - [第一部分：编程范式](#第一部分编程范式)
    - [1.1 命令式编程（Imperative Programming）](#11-命令式编程imperative-programming)
      - [1.1.1 形式定义](#111-形式定义)
      - [1.1.2 Python实现特征](#112-python实现特征)
      - [1.1.3 与函数式对比的形式论证](#113-与函数式对比的形式论证)
      - [1.1.4 性能影响与适用场景](#114-性能影响与适用场景)
    - [1.2 函数式编程（Functional Programming）](#12-函数式编程functional-programming)
      - [1.2.1 纯函数的形式定义](#121-纯函数的形式定义)
      - [1.2.2 Python中的函数式特性](#122-python中的函数式特性)
      - [1.2.3 不可变性的形式论证](#123-不可变性的形式论证)
      - [1.2.4 反例：违反纯函数原则](#124-反例违反纯函数原则)
    - [1.3 面向对象编程（Object-Oriented Programming）](#13-面向对象编程object-oriented-programming)
      - [1.3.1 三大特性的形式定义](#131-三大特性的形式定义)
      - [1.3.2 Python的OOP实现机制](#132-python的oop实现机制)
      - [1.3.3 MRO（方法解析顺序）的形式论证](#133-mro方法解析顺序的形式论证)
      - [1.3.4 反例：OOP常见错误](#134-反例oop常见错误)
    - [1.4 声明式编程（Declarative Programming）](#14-声明式编程declarative-programming)
      - [1.4.1 形式定义](#141-形式定义)
      - [1.4.2 Python中的声明式特性](#142-python中的声明式特性)
      - [1.4.3 与命令式对比的形式论证](#143-与命令式对比的形式论证)
      - [1.4.4 性能分析](#144-性能分析)
  - [第二部分：类型系统](#第二部分类型系统)
    - [2.1 静态类型 vs 动态类型](#21-静态类型-vs-动态类型)
      - [2.1.1 形式定义](#211-形式定义)
      - [2.1.2 对比论证](#212-对比论证)
      - [2.1.3 形式证明：动态类型的运行时检查](#213-形式证明动态类型的运行时检查)
    - [2.2 强类型 vs 弱类型](#22-强类型-vs-弱类型)
      - [2.2.1 形式定义](#221-形式定义)
      - [2.2.2 Python的强类型特性证明](#222-python的强类型特性证明)
      - [2.2.3 对比：强类型 vs 弱类型](#223-对比强类型-vs-弱类型)
    - [2.3 鸭子类型（Duck Typing）](#23-鸭子类型duck-typing)
      - [2.3.1 概念定义](#231-概念定义)
      - [2.3.2 Python实现](#232-python实现)
      - [2.3.3 形式论证](#233-形式论证)
    - [2.4 结构子类型（Structural Subtyping）](#24-结构子类型structural-subtyping)
      - [2.4.1 形式定义](#241-形式定义)
      - [2.4.2 Python中的Protocol类](#242-python中的protocol类)
      - [2.4.3 运行时检查机制](#243-运行时检查机制)
      - [2.4.4 名义子类型 vs 结构子类型对比](#244-名义子类型-vs-结构子类型对比)
  - [第三部分：内存模型](#第三部分内存模型)
    - [3.1 引用计数（Reference Counting）](#31-引用计数reference-counting)
      - [3.1.1 原理与形式化描述](#311-原理与形式化描述)
      - [3.1.2 引用计数的优缺点](#312-引用计数的优缺点)
      - [3.1.3 反例：循环引用问题](#313-反例循环引用问题)
    - [3.2 垃圾回收（Garbage Collection）](#32-垃圾回收garbage-collection)
      - [3.2.1 分代垃圾回收机制](#321-分代垃圾回收机制)
      - [3.2.2 循环引用检测算法](#322-循环引用检测算法)
      - [3.2.3 垃圾回收调优](#323-垃圾回收调优)
    - [3.3 GIL（全局解释器锁）](#33-gil全局解释器锁)
      - [3.3.1 机制形式化描述](#331-机制形式化描述)
      - [3.3.2 绕过GIL的方法](#332-绕过gil的方法)
      - [3.3.3 GIL的性能影响](#333-gil的性能影响)
    - [3.4 内存池和对象复用](#34-内存池和对象复用)
      - [3.4.1 小对象分配器（pymalloc）](#341-小对象分配器pymalloc)
      - [3.4.2 对象复用机制](#342-对象复用机制)
      - [3.4.3 内存优化技巧](#343-内存优化技巧)
  - [第四部分：执行模型](#第四部分执行模型)
    - [4.1 解释执行流程](#41-解释执行流程)
      - [4.1.1 Python执行流程形式化](#411-python执行流程形式化)
      - [4.1.2 编译与执行分离](#412-编译与执行分离)
    - [4.2 字节码编译（dis模块）](#42-字节码编译dis模块)
      - [4.2.1 字节码指令集](#421-字节码指令集)
      - [4.2.2 字节码优化](#422-字节码优化)
      - [4.2.3 反汇编与调试](#423-反汇编与调试)
    - [4.3 帧栈机制](#43-帧栈机制)
      - [4.3.1 调用栈的形式定义](#431-调用栈的形式定义)
      - [4.3.2 栈帧操作](#432-栈帧操作)
      - [4.3.3 异常与栈展开](#433-异常与栈展开)
  - [第五部分：错误处理机制](#第五部分错误处理机制)
    - [5.1 异常处理](#51-异常处理)
      - [5.1.1 try/except/finally/else 形式定义](#511-tryexceptfinallyelse-形式定义)
      - [5.1.2 异常层次结构](#512-异常层次结构)
      - [5.1.3 自定义异常](#513-自定义异常)
      - [5.1.4 异常链与上下文](#514-异常链与上下文)
    - [5.2 错误处理模式对比](#52-错误处理模式对比)
      - [5.2.1 异常 vs 错误码](#521-异常-vs-错误码)
      - [5.2.2 Result类型模式](#522-result类型模式)
      - [5.2.3 Option类型模式](#523-option类型模式)
      - [5.2.4 错误处理模式选择指南](#524-错误处理模式选择指南)
  - [第六部分：模块化设计](#第六部分模块化设计)
    - [6.1 封装机制](#61-封装机制)
      - [6.1.1 封装的形式定义](#611-封装的形式定义)
      - [6.1.2 属性装饰器](#612-属性装饰器)
    - [6.2 接口设计](#62-接口设计)
      - [6.2.1 抽象基类（ABC）](#621-抽象基类abc)
      - [6.2.2 协议类（Protocol）](#622-协议类protocol)
    - [6.3 依赖注入](#63-依赖注入)
      - [6.3.1 依赖注入的形式定义](#631-依赖注入的形式定义)
      - [6.3.2 依赖注入模式对比](#632-依赖注入模式对比)
    - [6.4 插件架构](#64-插件架构)
      - [6.4.1 插件系统设计](#641-插件系统设计)
      - [6.4.2 钩子系统](#642-钩子系统)
  - [总结](#总结)
    - [关键概念回顾](#关键概念回顾)
    - [最佳实践](#最佳实践)

## 第一部分：编程范式

### 1.1 命令式编程（Imperative Programming）

#### 1.1.1 形式定义

**定义 1.1**（命令式程序）：命令式程序是一个状态转换系统，可形式化为五元组：

$$
P = (S, s_0, \Sigma, T, F)
$$

其中：

- $S$：程序状态空间（所有变量到值的映射）
- $s_0 \in S$：初始状态
- $\Sigma$：操作指令集合
- $T: S \times \Sigma \rightarrow S$：状态转换函数
- $F \subseteq S$：终止状态集合

**定义 1.2**（状态）：程序状态 $s$ 是变量名到值的映射：

$$
s: Var \rightarrow Value \cup \{\bot\}
$$

其中 $\bot$ 表示未定义。

#### 1.1.2 Python实现特征

```python
# 正例：典型的命令式编程
x = 10          # 状态更新: s[x] = 10
y = 20          # 状态更新: s[y] = 20
z = x + y       # 状态更新: s[z] = 30

for i in range(5):  # 循环控制流
    z += i          # 状态更新: s[z] = s[z] + s[i]
```

**形式化推导**：

设初始状态 $s_0 = \{\}$，执行序列：

$$
\begin{aligned}
s_1 &= T(s_0, x=10) = \{x \mapsto 10\} \\
s_2 &= T(s_1, y=20) = \{x \mapsto 10, y \mapsto 20\} \\
s_3 &= T(s_2, z=x+y) = \{x \mapsto 10, y \mapsto 20, z \mapsto 30\}
\end{aligned}
$$

#### 1.1.3 与函数式对比的形式论证

**定理 1.1**（命令式vs函数式语义差异）：

设 $f_{imp}$ 为命令式函数，$f_{fun}$ 为等价的纯函数，则：

$$
\forall s \in S, x \in Input: \\
f_{fun}(x) = f_{imp}(x) \iff \forall v \in Var(s): v \notin \text{SideEffect}(f_{imp})
$$

**证明**：

```python
# 反例：命令式函数有副作用
def imperative_sum(lst):
    """命令式实现 - 修改外部状态"""
    global total
    total = 0           # 副作用：修改全局变量
    for x in lst:
        total += x      # 副作用：修改全局变量
    return total

# 正例：纯函数式实现
def functional_sum(lst):
    """函数式实现 - 无副作用"""
    return sum(lst)     # 纯计算，无状态修改

# 验证定理
total = 100
result1 = imperative_sum([1, 2, 3])
print(f"命令式后 total = {total}")  # total = 6 (被修改！)

total = 100
result2 = functional_sum([1, 2, 3])
print(f"函数式后 total = {total}")  # total = 100 (保持不变)
```

#### 1.1.4 性能影响与适用场景

| 特性 | 命令式 | 函数式 |
|------|--------|--------|
| 内存使用 | 可变状态，原地修改 | 不可变，创建新对象 |
| 并发安全 | 需显式同步 | 天然线程安全 |
| 调试难度 | 状态追踪复杂 | 输入输出可预测 |
| 适用场景 | I/O操作、状态机、性能敏感 | 数据处理、并行计算、验证 |

---

### 1.2 函数式编程（Functional Programming）

#### 1.2.1 纯函数的形式定义

**定义 1.3**（纯函数）：函数 $f: A \rightarrow B$ 是纯函数当且仅当：

$$
\forall a_1, a_2 \in A: a_1 = a_2 \implies f(a_1) = f(a_2) \quad \text{(确定性)} \\
\land \quad \text{SideEffect}(f) = \emptyset \quad \text{(无副作用)}
$$

**定义 1.4**（引用透明性）：表达式 $e$ 是引用透明的当且仅当：

$$
\forall \text{上下文 } C: C[e] \equiv C[e'] \text{ 其中 } e \equiv e'
$$

#### 1.2.2 Python中的函数式特性

```python
# 正例：纯函数
from typing import List

def pure_double(x: int) -> int:
    """纯函数：确定性 + 无副作用"""
    return x * 2

# 高阶函数
def apply_to_all(func: callable, lst: List[int]) -> List[int]:
    """高阶函数：接受函数作为参数"""
    return [func(x) for x in lst]

# 不可变性示例
original = (1, 2, 3)  # 元组不可变
# original[0] = 10    # TypeError: 反例，尝试修改不可变对象

# 函数组合
from functools import reduce, partial

# 偏函数
add_five = partial(lambda x, y: x + y, 5)
print(add_five(10))  # 15

# 函数组合
def compose(f, g):
    """函数组合: (f ∘ g)(x) = f(g(x))"""
    return lambda x: f(g(x))

double_then_add_one = compose(lambda x: x + 1, lambda x: x * 2)
print(double_then_add_one(5))  # 11
```

#### 1.2.3 不可变性的形式论证

**定理 1.2**（不可变性与线程安全）：

设 $O$ 为不可变对象，$T_1, T_2$ 为两个线程，则：

$$
\forall t_1, t_2: T_1(O, t_1) \parallel T_2(O, t_2) \implies \text{NoRaceCondition}
$$

**证明**：

```python
import threading

# 正例：使用不可变数据保证线程安全
immutable_data = frozenset([1, 2, 3, 4, 5])

results = []
def worker(data, multiplier):
    """线程安全：只读取不可变数据"""
    result = sum(x * multiplier for x in data)
    results.append(result)

# 多线程同时访问不可变数据
threads = [
    threading.Thread(target=worker, args=(immutable_data, 2)),
    threading.Thread(target=worker, args=(immutable_data, 3)),
]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Results: {results}")  # 总是 [30, 45]，无竞争条件
```

#### 1.2.4 反例：违反纯函数原则

```python
# 反例1：非确定性
import random

def impure_random(x):
    """非纯函数：相同输入可能产生不同输出"""
    return x + random.randint(1, 10)

# 反例2：有副作用
def impure_logger(x):
    """非纯函数：有I/O副作用"""
    print(f"Processing: {x}")  # I/O副作用
    return x * 2

# 反例3：修改外部状态
external_cache = {}

def impure_cache(x):
    """非纯函数：修改外部状态"""
    if x not in external_cache:
        external_cache[x] = x ** 2
    return external_cache[x]
```

---

### 1.3 面向对象编程（Object-Oriented Programming）

#### 1.3.1 三大特性的形式定义

**定义 1.5**（封装）：封装是数据与操作的绑定机制：

$$
\text{Object} = (Data, Methods, Interface)
$$

其中 $Interface \subseteq Methods$ 是外部可见的操作集合。

**定义 1.6**（继承）：类 $C$ 继承自类 $P$ 当且仅当：

$$
C \prec P \iff \forall m \in P: m \in C \text{ (除非被覆盖)}
$$

**定义 1.7**（多态/子类型多态）：设 $T$ 为类型，$S$ 为 $T$ 的子类型：

$$
S <: T \implies \forall f: T \rightarrow R, \forall s \in S: f(s) \text{ 是良定义的}
$$

#### 1.3.2 Python的OOP实现机制

```python
# 正例：完整的OOP实现
from abc import ABC, abstractmethod
from typing import List

# 抽象基类 - 定义接口
class Shape(ABC):
    """形状抽象基类 - 封装 + 接口定义"""

    def __init__(self, name: str):
        self._name = name  # 受保护属性（封装）

    @property
    def name(self) -> str:
        """属性访问器 - 控制的封装"""
        return self._name

    @abstractmethod
    def area(self) -> float:
        """抽象方法 - 子类必须实现"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

# 具体类 - 继承 + 实现
class Rectangle(Shape):
    """矩形类 - 继承Shape"""

    def __init__(self, name: str, width: float, height: float):
        super().__init__(name)
        self._width = width   # 私有属性
        self._height = height

    def area(self) -> float:      # 多态实现
        return self._width * self._height

    def perimeter(self) -> float: # 多态实现
        return 2 * (self._width + self._height)

class Circle(Shape):
    """圆形类 - 继承Shape"""

    def __init__(self, name: str, radius: float):
        super().__init__(name)
        self._radius = radius

    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self._radius

# 多态使用
def total_area(shapes: List[Shape]) -> float:
    """多态函数：接受任何Shape子类"""
    return sum(s.area() for s in shapes)

# 演示
shapes = [
    Rectangle("Rect1", 5, 3),
    Circle("Circle1", 4),
    Rectangle("Rect2", 2, 2),
]

print(f"Total area: {total_area(shapes):.2f}")
```

#### 1.3.3 MRO（方法解析顺序）的形式论证

**定理 1.3**（C3线性化）：Python使用C3算法计算MRO，保证：

1. 子类先于父类
2. 保持父类的声明顺序
3. 单调性：$C_1 \prec C_2 \implies MRO(C_1) \subseteq MRO(C_2)$

```python
# 正例：MRO演示
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):  # 多重继承
    pass

# 查看MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

d = D()
print(d.method())  # "B" - 按MRO顺序解析

# 反例：不合法的继承顺序
# class E(C, B):  # 这会创建与D不同的MRO，但不会报错
#     pass
```

#### 1.3.4 反例：OOP常见错误

```python
# 反例1：违反里氏替换原则
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):  # 企鹅是鸟，但不会飞
    def fly(self):
        raise NotImplementedError("Penguins can't fly!")

# 反例2：过度继承（组合优于继承）
# 错误：使用继承实现代码复用
class Logger:
    def log(self, msg):
        print(msg)

class UserService(Logger):  # UserService不是Logger！
    pass

# 正确：使用组合
class UserService:
    def __init__(self):
        self._logger = Logger()  # 组合

    def log(self, msg):
        self._logger.log(msg)
```

---

### 1.4 声明式编程（Declarative Programming）

#### 1.4.1 形式定义

**定义 1.8**（声明式程序）：声明式程序描述"是什么"而非"怎么做"：

$$
P_{declarative} = \{ (input, output) \mid output = f(input) \}
$$

对比命令式：

$$
P_{imperative} = (s_0, \sigma_1, \sigma_2, ..., \sigma_n, s_n)
$$

#### 1.4.2 Python中的声明式特性

```python
# 正例：列表推导（声明式）
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 声明式：描述"偶数的平方"
squares_even = [x**2 for x in numbers if x % 2 == 0]
print(squares_even)  # [4, 16, 36, 64, 100]

# 等价的命令式
squares_even_imp = []
for x in numbers:
    if x % 2 == 0:
        squares_even_imp.append(x**2)

# 正例：生成器表达式（惰性求值）
large_data = range(1, 1000000)
sum_of_squares = sum(x**2 for x in large_data if x % 3 == 0)

# 正例：字典推导
word_lengths = {word: len(word) for word in ["apple", "banana", "cherry"]}
print(word_lengths)  # {'apple': 5, 'banana': 6, 'cherry': 6}

# 正例：集合推导
unique_lengths = {len(word) for word in ["apple", "banana", "cherry", "date"]}
print(unique_lengths)  # {4, 5, 6}
```

#### 1.4.3 与命令式对比的形式论证

**定理 1.4**（声明式vs命令式等价性）：

设 $L$ 为列表推导，$I$ 为等价的命令式循环，则：

$$
\forall lst: L(lst) = I(lst)
$$

**证明（结构归纳法）**：

```python
# 基础情况：简单推导
# 声明式
result_d = [f(x) for x in lst]

# 命令式
result_i = []
for x in lst:
    result_i.append(f(x))

# 归纳步骤：带条件的推导
# 声明式
result_d2 = [f(x) for x in lst if p(x)]

# 命令式
result_i2 = []
for x in lst:
    if p(x):
        result_i2.append(f(x))

# 验证等价性
import random

def verify_equivalence(lst, f, p):
    decl = [f(x) for x in lst if p(x)]
    impl = []
    for x in lst:
        if p(x):
            impl.append(f(x))
    return decl == impl

# 测试
f = lambda x: x * 2
p = lambda x: x > 0
test_list = [random.randint(-10, 10) for _ in range(100)]
print(f"Equivalence verified: {verify_equivalence(test_list, f, p)}")
```

#### 1.4.4 性能分析

| 特性 | 列表推导 | 命令式循环 |
|------|----------|------------|
| 执行速度 | 更快（C层优化） | 较慢（Python层） |
| 内存使用 | 立即求值，占用内存 | 相同 |
| 可读性 | 高（声明式） | 中（过程式） |
| 惰性求值 | 生成器表达式支持 | 需手动实现 |

```python
import timeit

# 性能对比
def list_comprehension():
    return [x**2 for x in range(1000) if x % 2 == 0]

def imperative_loop():
    result = []
    for x in range(1000):
        if x % 2 == 0:
            result.append(x**2)
    return result

# 测试
t1 = timeit.timeit(list_comprehension, number=10000)
t2 = timeit.timeit(imperative_loop, number=10000)
print(f"List comprehension: {t1:.4f}s")
print(f"Imperative loop: {t2:.4f}s")
print(f"Speedup: {t2/t1:.2f}x")
```

---

## 第二部分：类型系统

### 2.1 静态类型 vs 动态类型

#### 2.1.1 形式定义

**定义 2.1**（类型系统）：类型系统是一个三元组：

$$
TS = (Types, \vdash, Rules)
$$

其中：

- $Types$：类型集合
- $\vdash$：类型推导关系
- $Rules$：类型规则集合

**定义 2.2**（静态类型）：在静态类型系统中，类型检查发生在**编译期**：

$$
\forall e \in Expr: \Gamma \vdash e : T \text{ at compile-time}
$$

**定义 2.3**（动态类型）：在动态类型系统中，类型检查发生在**运行时**：

$$
\forall e \in Expr: \vdash e : T \text{ at run-time}
$$

#### 2.1.2 对比论证

| 特性 | 静态类型（如Java/C++） | 动态类型（Python） |
|------|----------------------|-------------------|
| 类型检查时机 | 编译期 | 运行时 |
| 错误发现 | 早期 | 晚期 |
| 代码灵活性 | 较低 | 较高 |
| 运行时开销 | 无类型检查开销 | 有类型检查开销 |
| 重构支持 | 强 | 弱 |

```python
# Python是动态类型语言
x = 10      # x的类型在运行时被推断为int
x = "hello" # x的类型在运行时被重新绑定为str

# 类型错误在运行时发现
def add(a, b):
    return a + b

# 运行时错误
# result = add(10, "20")  # TypeError: unsupported operand type(s)

# Python 3.5+ 支持类型提示（但不强制）
def typed_add(a: int, b: int) -> int:
    return a + b

# 类型提示不会阻止运行时错误
result = typed_add(10, "20")  # 仍然可以执行（虽然IDE会警告）
```

#### 2.1.3 形式证明：动态类型的运行时检查

**定理 2.1**（动态类型检查的必要性）：

设 $op$ 为二元操作，$T_1, T_2$ 为操作数类型，则：

$$
\text{DynamicCheck}(op, v_1, v_2) =
\begin{cases}
\text{result} & \text{if } op \in \text{Supported}(type(v_1), type(v_2)) \\
\text{TypeError} & \text{otherwise}
\end{cases}
$$

```python
# 正例：Python的运行时类型检查机制
def demonstrate_type_checking():
    """展示Python的动态类型检查"""

    # 情况1：成功的类型检查
    a, b = 10, 20
    result = a + b  # 通过：int + int 是合法的
    print(f"int + int = {result}")

    # 情况2：失败的类型检查
    try:
        c, d = 10, "20"
        result = c + d  # 失败：int + str 不合法
    except TypeError as e:
        print(f"Type check failed: {e}")

    # 情况3：鸭子类型（稍后详述）
    class Addable:
        def __init__(self, value):
            self.value = value
        def __add__(self, other):
            return Addable(self.value + other.value)

    x, y = Addable(10), Addable(20)
    result = x + y  # 通过：对象实现了__add__方法
    print(f"Addable + Addable = {result.value}")

demonstrate_type_checking()
```

---

### 2.2 强类型 vs 弱类型

#### 2.2.1 形式定义

**定义 2.4**（强类型）：强类型语言禁止隐式类型转换：

$$
\forall e_1: T_1, e_2: T_2: T_1 \neq T_2 \implies e_1 \oplus e_2 \text{ is ill-typed (without explicit cast)}
$$

**定义 2.5**（弱类型）：弱类型语言允许隐式类型转换：

$$
\exists e_1: T_1, e_2: T_2: T_1 \neq T_2 \land e_1 \oplus e_2 \text{ is well-typed (with implicit cast)}
$$

#### 2.2.2 Python的强类型特性证明

**定理 2.2**（Python是强类型语言）：

```python
# 证明1：不允许隐式数值转换
a = 10      # int
b = 3.14    # float

# 正例：需要显式转换
c = a + int(b)    # 显式转换
print(f"Explicit cast: {c}")  # 13

# 反例：JavaScript会隐式转换
# JavaScript: 10 + "20" = "1020" (隐式转换)
# Python: 10 + "20" = TypeError

try:
    result = 10 + "20"  # 强类型：拒绝隐式转换
except TypeError as e:
    print(f"Strong typing prevents: {e}")

# 证明2：布尔值不与整数隐式等价
print(True == 1)   # True（值相等）
print(True is 1)   # False（身份不等）
print(type(True))  # <class 'bool'>

# 证明3：None的强类型特性
result = None
# if result:  # 可以，但None是假值
# print(None + 1)  # TypeError

# 证明4：字符串与数字的严格区分
s = "123"
n = 123
print(s == n)      # False
print(int(s) == n) # True（显式转换）
```

#### 2.2.3 对比：强类型 vs 弱类型

| 语言 | 类型强度 | 示例 |
|------|----------|------|
| Python | 强 | `1 + "2"` → TypeError |
| JavaScript | 弱 | `1 + "2"` → `"12"` |
| PHP | 弱 | `1 + "2"` → `3` |
| Java | 强 | `1 + "2"` → 编译错误 |
| C | 弱 | `1 + 2.0` → 隐式转换 |

---

### 2.3 鸭子类型（Duck Typing）

#### 2.3.1 概念定义

**定义 2.6**（鸭子类型）：鸭子类型是一种动态类型风格，对象的适用性由其实现的方法/属性决定，而非继承关系：

$$
\text{DuckType}(o, T) \iff \forall m \in Methods(T): m \in Methods(o)
$$

**EAFP原则**（Easier to Ask for Forgiveness than Permission）：

```
优先尝试执行，失败时捕获异常
而不是预先检查条件
```

#### 2.3.2 Python实现

```python
# 正例：鸭子类型
class Duck:
    def quack(self):
        return "Quack!"
    def swim(self):
        return "Swimming like a duck"

class Person:
    def quack(self):
        return "I'm quacking like a duck!"
    def swim(self):
        return "Swimming like a human"

class Dog:
    def bark(self):  # 没有quack方法
        return "Woof!"

# 鸭子类型函数
def make_it_quack(thing):
    """不检查类型，只检查行为"""
    try:
        return thing.quack()
    except AttributeError:
        return "This thing can't quack"

# 测试
print(make_it_quack(Duck()))    # "Quack!"
print(make_it_quack(Person()))  # "I'm quacking like a duck!"
print(make_it_quack(Dog()))     # "This thing can't quack"

# EAFP vs LBYL对比
# LBYL (Look Before You Leap) - 预先检查
def lbyl_process(obj):
    if hasattr(obj, 'process') and callable(getattr(obj, 'process')):
        return obj.process()
    return None

# EAFP - 尝试执行
def eafp_process(obj):
    try:
        return obj.process()
    except AttributeError:
        return None

# EAFP通常更快（避免重复属性查找）
import timeit

class Processor:
    def process(self):
        return "processed"

p = Processor()
t1 = timeit.timeit(lambda: lbyl_process(p), number=100000)
t2 = timeit.timeit(lambda: eafp_process(p), number=100000)
print(f"LBYL: {t1:.4f}s, EAFP: {t2:.4f}s")
```

#### 2.3.3 形式论证

**定理 2.3**（鸭子类型与继承的等价性）：

设 $I$ 为接口（方法集合），$C$ 为实现类，则：

$$
C \text{ 满足 } I \iff \forall m \in I: hasmethod(C, m)
$$

```python
# 正例：使用collections.abc验证鸭子类型
from collections.abc import Sequence, Mapping

class MyList:
    """自定义序列 - 通过鸭子类型满足Sequence协议"""
    def __init__(self, data):
        self._data = list(data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __iter__(self):
        return iter(self._data)

my_list = MyList([1, 2, 3])

# 鸭子类型验证
print(f"Has __len__: {hasattr(my_list, '__len__')}")
print(f"Has __getitem__: {hasattr(my_list, '__getitem__')}")

# 使用isinstance检查（Python 3.5+支持）
print(f"Is Sequence: {isinstance(my_list, Sequence)}")

# 反例：不满足协议
class FakeList:
    pass

fake = FakeList()
print(f"Fake is Sequence: {isinstance(fake, Sequence)}")  # False
```

---

### 2.4 结构子类型（Structural Subtyping）

#### 2.4.1 形式定义

**定义 2.7**（名义子类型 Nominal Subtyping）：

$$
S <:_{nominal} T \iff S \text{ 显式声明继承自 } T
$$

**定义 2.8**（结构子类型 Structural Subtyping）：

$$
S <:_{structural} T \iff \forall m \in Methods(T): m \in Methods(S) \land type_S(m) <: type_T(m)
$$

#### 2.4.2 Python中的Protocol类

```python
# Python 3.8+ 引入 Protocol 支持结构子类型
from typing import Protocol, runtime_checkable

# 定义协议（接口）
@runtime_checkable
class Drawable(Protocol):
    """可绘制对象的协议"""
    def draw(self) -> str:
        ...

@runtime_checkable
class Measurable(Protocol):
    """可测量对象的协议"""
    def measure(self) -> float:
        ...

# 实现类 - 无需显式继承
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Drawing circle with radius {self.radius}"

    def measure(self) -> float:
        import math
        return 2 * math.pi * self.radius

class Square:
    def __init__(self, side: float):
        self.side = side

    def draw(self) -> str:
        return f"Drawing square with side {self.side}"

    def measure(self) -> float:
        return 4 * self.side

# 使用结构子类型
def render(drawable: Drawable) -> str:
    """接受任何实现了draw方法的对象"""
    return drawable.draw()

# 测试
circle = Circle(5)
square = Square(4)

print(render(circle))  # 通过：Circle实现了draw
print(render(square))  # 通过：Square实现了draw

# 运行时检查
print(f"Circle is Drawable: {isinstance(circle, Drawable)}")
print(f"Square is Measurable: {isinstance(square, Measurable)}")
```

#### 2.4.3 运行时检查机制

```python
from typing import Protocol, get_type_hints
import inspect

def check_protocol(obj, protocol: type[Protocol]) -> bool:
    """手动实现协议检查"""
    # 获取协议要求的方法
    protocol_methods = {
        name for name in dir(protocol)
        if not name.startswith('_') and callable(getattr(protocol, name, None))
    }

    # 检查对象是否实现所有方法
    for method_name in protocol_methods:
        if not hasattr(obj, method_name):
            return False
        obj_method = getattr(obj, method_name)
        if not callable(obj_method):
            return False

    return True

# 测试
class TestClass:
    def draw(self):
        pass

print(f"Manual check: {check_protocol(TestClass(), Drawable)}")
```

#### 2.4.4 名义子类型 vs 结构子类型对比

| 特性 | 名义子类型 | 结构子类型 |
|------|------------|------------|
| 声明方式 | 显式继承 | 隐式实现 |
| 类型检查 | 基于类层次 | 基于方法签名 |
| 灵活性 | 较低 | 较高 |
| 文档性 | 强（显式声明） | 弱（隐式契约） |
| 重构安全 | 高 | 中 |

---

## 第三部分：内存模型

### 3.1 引用计数（Reference Counting）

#### 3.1.1 原理与形式化描述

**定义 3.1**（引用计数）：每个Python对象维护一个引用计数器，记录指向该对象的引用数量：

$$
RC: Object \rightarrow \mathbb{N}_0
$$

**定义 3.2**（引用计数规则）：

1. **创建对象**：$RC(o) := 1$
2. **增加引用**：$RC(o) := RC(o) + 1$
3. **减少引用**：$RC(o) := RC(o) - 1$
4. **回收对象**：$RC(o) = 0 \implies \text{deallocate}(o)$

```python
import sys

# 正例：引用计数演示
def demonstrate_ref_count():
    """展示Python的引用计数机制"""

    # 创建对象，引用计数 = 1
    a = [1, 2, 3]
    print(f"After a = [1,2,3]: ref count = {sys.getrefcount(a) - 1}")  # -1 for getrefcount itself

    # 增加引用
    b = a
    print(f"After b = a: ref count = {sys.getrefcount(a) - 1}")

    # 再增加引用
    c = b
    print(f"After c = b: ref count = {sys.getrefcount(a) - 1}")

    # 减少引用
    del b
    print(f"After del b: ref count = {sys.getrefcount(a) - 1}")

    # 减少引用
    c = None
    print(f"After c = None: ref count = {sys.getrefcount(a) - 1}")

    # 当a被删除或重新赋值时，引用计数变为0，对象被回收

demonstrate_ref_count()

# 特殊情况：小整数和字符串的驻留
a = 100
b = 100
print(f"Small int identity: {a is b}")  # True（-5到256被驻留）

c = 1000
d = 1000
print(f"Large int identity: {c is d}")  # 可能False
```

#### 3.1.2 引用计数的优缺点

| 优点 | 缺点 |
|------|------|
| 内存回收即时 | 无法处理循环引用 |
| 实现简单 | 引用计数维护有开销 |
| 可预测性高 | 多线程需要额外同步 |

#### 3.1.3 反例：循环引用问题

```python
import gc

# 反例：循环引用导致引用计数失效
class Node:
    def __init__(self, name):
        self.name = name
        self.next = None

    def __repr__(self):
        return f"Node({self.name})"

    def __del__(self):
        print(f"Node {self.name} is being deleted")

# 创建循环引用
node1 = Node("A")
node2 = Node("B")
node1.next = node2
node2.next = node1  # 循环引用！

# 此时引用计数：node1=2 (node1, node2.next), node2=2 (node2, node1.next)
print(f"node1 ref count: {sys.getrefcount(node1) - 1}")
print(f"node2 ref count: {sys.getrefcount(node2) - 1}")

# 删除外部引用
del node1
del node2

# 对象不会被立即回收，因为引用计数仍大于0
print("After del, objects still exist due to circular reference")

# 需要垃圾回收器介入
gc.collect()  # 强制垃圾回收
print("After gc.collect()")
```

---

### 3.2 垃圾回收（Garbage Collection）

#### 3.2.1 分代垃圾回收机制

**定义 3.3**（分代GC假设）：

$$
\text{弱代假设}: P(\text{对象存活} \mid \text{已存活} n \text{ 轮}) > P(\text{对象存活} \mid \text{新创建})
$$

Python使用三代垃圾回收器（0代、1代、2代）：

```python
import gc

# 查看GC配置
print(f"GC enabled: {gc.isenabled()}")
print(f"GC thresholds: {gc.get_threshold()}")  # (700, 10, 10)

# 700: 0代对象数量阈值
# 10: 1代回收频率（0代回收10次后1代回收1次）
# 10: 2代回收频率（1代回收10次后2代回收1次）

# 查看各代对象数量
print(f"Generation counts: {gc.get_count()}")

# 强制垃圾回收
collected = gc.collect()
print(f"Collected objects: {collected}")

# 禁用/启用GC
gc.disable()
print(f"GC enabled after disable: {gc.isenabled()}")
gc.enable()
```

#### 3.2.2 循环引用检测算法

**算法 3.1**（循环引用检测）：

```
1. 遍历容器对象（list, dict, class实例等）
2. 对每个对象，减少其引用对象的引用计数（模拟删除）
3. 引用计数变为0的对象是垃圾
4. 恢复引用计数
5. 回收垃圾对象
```

```python
# 正例：GC处理循环引用
class ManagedObject:
    _instances = []

    def __init__(self, name):
        self.name = name
        self.ref = None
        ManagedObject._instances.append(self)

    def __del__(self):
        print(f"ManagedObject {self.name} deleted")

    @classmethod
    def cleanup(cls):
        cls._instances.clear()
        gc.collect()

# 创建循环引用
obj1 = ManagedObject("X")
obj2 = ManagedObject("Y")
obj1.ref = obj2
obj2.ref = obj1

print("Before cleanup:")
print(f"Tracked objects: {len(gc.get_objects())}")

# 清理
ManagedObject.cleanup()
print("After cleanup and gc.collect()")

# 使用弱引用避免循环引用
import weakref

class NodeWithWeakRef:
    def __init__(self, name):
        self.name = name
        self._next = None

    @property
    def next(self):
        return self._next() if self._next else None

    @next.setter
    def next(self, node):
        self._next = weakref.ref(node) if node else None

    def __del__(self):
        print(f"NodeWithWeakRef {self.name} deleted")

# 测试弱引用
w1 = NodeWithWeakRef("W1")
w2 = NodeWithWeakRef("W2")
w1.next = w2
w2.next = w1

# 删除引用后对象立即被回收
del w1
del w2
print("Weak reference nodes deleted immediately")
```

#### 3.2.3 垃圾回收调优

```python
import gc

# 调整GC阈值
gc.set_threshold(500, 5, 5)  # 更频繁的回收

# 监控GC统计
print("GC stats:", gc.get_stats())

# 对象跟踪
gc.set_debug(gc.DEBUG_STATS)

# 手动管理特定对象
class LargeObject:
    def __init__(self):
        self.data = [0] * 1000000

# 创建大对象
large = LargeObject()

# 使用完毕后强制回收
del large
gc.collect()

# 关闭调试
gc.set_debug(0)
```

---

### 3.3 GIL（全局解释器锁）

#### 3.3.1 机制形式化描述

**定义 3.4**（GIL）：GIL是一个互斥锁，确保任何时候只有一个线程执行Python字节码：

$$
\forall t_1, t_2 \in \text{Threads}: \text{Execute}(t_1) \implies \neg \text{Execute}(t_2)
$$

**GIL释放时机**：

1. I/O操作阻塞时
2. 执行固定数量的字节码指令后（默认约100个）

```python
import threading
import time

# 正例：GIL影响的CPU密集型任务
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        # 非原子操作：读-修改-写
        current = self.value
        time.sleep(0.000001)  # 模拟一些工作
        self.value = current + 1

def worker(counter, iterations):
    for _ in range(iterations):
        counter.increment()

# 测试多线程
counter = Counter()
iterations = 100000

# 单线程
start = time.time()
for _ in range(iterations * 2):
    counter.increment()
single_thread_time = time.time() - start
print(f"Single thread: {single_thread_time:.2f}s, counter={counter.value}")

# 多线程（由于GIL，不会更快）
counter.value = 0
start = time.time()

t1 = threading.Thread(target=worker, args=(counter, iterations))
t2 = threading.Thread(target=worker, args=(counter, iterations))
t1.start()
t2.start()
t1.join()
t2.join()

multi_thread_time = time.time() - start
print(f"Multi thread: {multi_thread_time:.2f}s, counter={counter.value}")
print(f"Expected: {iterations * 2}, Actual: {counter.value}")  # 可能不一致！
```

#### 3.3.2 绕过GIL的方法

```python
# 方法1：使用多进程（每个进程有自己的GIL）
from multiprocessing import Pool
import os

def cpu_intensive(n):
    """CPU密集型任务"""
    count = 0
    for i in range(n):
        count += i * i
    return count

# 多进程并行
if __name__ == "__main__":
    start = time.time()
    with Pool(processes=4) as pool:
        results = pool.map(cpu_intensive, [1000000] * 4)
    print(f"Multiprocessing: {time.time() - start:.2f}s")

# 方法2：使用C扩展释放GIL
"""
// C扩展示例（伪代码）
static PyObject* compute(PyObject* self, PyObject* args) {
    Py_BEGIN_ALLOW_THREADS  // 释放GIL
    // 执行计算...
    Py_END_ALLOW_THREADS    // 重新获取GIL
    return result;
}
"""

# 方法3：使用NumPy等已释放GIL的库
import numpy as np

def numpy_computation():
    """NumPy在C层面释放GIL"""
    a = np.random.rand(1000, 1000)
    b = np.random.rand(1000, 1000)
    return np.dot(a, b)

# 方法4：使用asyncio（单线程并发）
import asyncio

async def async_task(n):
    await asyncio.sleep(0.1)  # I/O操作释放GIL
    return n * n

async def main():
    tasks = [async_task(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    return results

# asyncio.run(main())
```

#### 3.3.3 GIL的性能影响

| 场景 | GIL影响 | 解决方案 |
|------|---------|----------|
| CPU密集型 | 严重（无法并行） | 多进程、C扩展 |
| I/O密集型 | 轻微（I/O释放GIL） | 多线程、asyncio |
| 混合负载 | 中等 | 进程池+线程池 |

---

### 3.4 内存池和对象复用

#### 3.4.1 小对象分配器（pymalloc）

**定义 3.5**（内存池）：Python对小对象（≤512字节）使用内存池管理：

```
内存层级：
- Arena: 256KB 大块内存
- Pool: 4KB，管理相同大小的块
- Block: 实际分配的对象内存
```

```python
import sys

# 正例：小对象的内存复用
# Python会复用小整数对象
a = 100
b = 100
print(f"Small int same object: {a is b}")  # True

# 字符串驻留
c = "hello"
d = "hello"
print(f"String same object: {c is d}")  # True（编译时驻留）

e = "hello world"
f = "hello world"
print(f"Long string same object: {e is f}")  # 可能False

# 强制驻留
g = sys.intern("hello world")
h = sys.intern("hello world")
print(f"Interned string same object: {g is h}")  # True
```

#### 3.4.2 对象复用机制

```python
# 正例：列表和字典的内存复用
import gc

# 列表复用
list1 = [1, 2, 3]
list_id1 = id(list1)
del list1

list2 = [4, 5, 6]
list_id2 = id(list2)
print(f"List memory reused: {list_id1 == list_id2}")  # 可能True

# 使用对象池模式
class ObjectPool:
    """对象池实现"""
    def __init__(self, factory, max_size=100):
        self._factory = factory
        self._max_size = max_size
        self._available = []
        self._in_use = set()

    def acquire(self):
        if self._available:
            obj = self._available.pop()
        else:
            obj = self._factory()
        self._in_use.add(id(obj))
        return obj

    def release(self, obj):
        obj_id = id(obj)
        if obj_id in self._in_use:
            self._in_use.remove(obj_id)
            if len(self._available) < self._max_size:
                # 重置对象状态
                if hasattr(obj, 'reset'):
                    obj.reset()
                self._available.append(obj)

# 使用对象池
class Connection:
    def __init__(self):
        self.active = True

    def reset(self):
        self.active = False

pool = ObjectPool(Connection, max_size=10)
conn1 = pool.acquire()
print(f"Connection active: {conn1.active}")
pool.release(conn1)
```

#### 3.4.3 内存优化技巧

```python
# 技巧1：使用__slots__减少内存占用
class RegularClass:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

class SlotClass:
    __slots__ = ['a', 'b', 'c']
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

import sys
r = RegularClass(1, 2, 3)
s = SlotClass(1, 2, 3)
print(f"Regular class size: {sys.getsizeof(r)} bytes")
print(f"Slot class size: {sys.getsizeof(s)} bytes")

# 技巧2：使用生成器代替列表
# 大列表
# big_list = [x**2 for x in range(10000000)]  # 内存占用大

# 生成器（惰性求值）
big_gen = (x**2 for x in range(10000000))  # 几乎不占用内存

# 技巧3：使用array.array存储数值
import array
arr = array.array('i', [1, 2, 3, 4, 5])  # 比list更紧凑
print(f"Array size: {sys.getsizeof(arr)} bytes")
print(f"List size: {sys.getsizeof([1, 2, 3, 4, 5])} bytes")

# 技巧4：使用__del__手动释放资源
class Resource:
    def __init__(self):
        self.handle = None  # 模拟资源句柄

    def __del__(self):
        if self.handle:
            # 释放资源
            print("Resource released")
```

---

## 第四部分：执行模型

### 4.1 解释执行流程

#### 4.1.1 Python执行流程形式化

**定义 4.1**（Python执行流程）：Python代码执行经历以下阶段：

$$
\text{Source Code} \xrightarrow{\text{Parser}} \text{AST} \xrightarrow{\text{Compiler}} \text{Bytecode} \xrightarrow{\text{VM}} \text{Execution}
$$

```python
import ast
import dis
import compileall

# 正例：查看执行流程
source = """
def add(a, b):
    return a + b

result = add(3, 4)
"""

# 阶段1：解析为AST
tree = ast.parse(source)
print("=== AST ===")
print(ast.dump(tree, indent=2))

# 阶段2：编译为字节码
code = compile(source, '<string>', 'exec')
print("\n=== Bytecode ===")
dis.dis(code)
```

#### 4.1.2 编译与执行分离

```python
# 正例：编译时vs运行时分离

# 编译时错误（语法错误）
# def broken(  # SyntaxError: unexpected EOF

# 运行时错误（语义错误）
def divide(a, b):
    return a / b  # 编译通过，但b=0时运行时错误

# 编译时检查
try:
    compile("def broken(", '<string>', 'exec')
except SyntaxError as e:
    print(f"Compile-time error: {e}")

# 运行时检查
try:
    divide(10, 0)
except ZeroDivisionError as e:
    print(f"Runtime error: {e}")
```

---

### 4.2 字节码编译（dis模块）

#### 4.2.1 字节码指令集

**定义 4.2**（字节码）：Python字节码是栈式虚拟机的中间表示：

```
常见字节码指令：
- LOAD_CONST: 加载常量到栈
- LOAD_NAME: 加载变量到栈
- STORE_NAME: 存储栈顶到变量
- BINARY_ADD: 弹出两个值，相加后压栈
- CALL_FUNCTION: 调用函数
- RETURN_VALUE: 返回栈顶值
```

```python
import dis
import opcode

# 正例：分析函数字节码
def example_function(x, y):
    z = x + y
    if z > 10:
        return z * 2
    else:
        return z

print("=== Bytecode Analysis ===")
dis.dis(example_function)

# 详细分析
print("\n=== Instruction Details ===")
for instr in dis.get_instructions(example_function):
    print(f"{instr.offset:3d}: {instr.opname:20s} {instr.argrepr}")

# 查看操作码常量
print(f"\nBINARY_ADD opcode: {opcode.opmap['BINARY_ADD']}")
print(f"CALL_FUNCTION opcode: {opcode.opmap['CALL_FUNCTION']}")
```

#### 4.2.2 字节码优化

```python
# 正例：常量折叠优化
def constant_folding():
    """Python会在编译时进行常量折叠"""
    x = 1 + 2 + 3  # 编译为: LOAD_CONST 6
    y = "hello" + " " + "world"  # 编译为: LOAD_CONST "hello world"
    return x, y

print("=== Constant Folding ===")
dis.dis(constant_folding)

# 反例：无法优化的动态表达式
def no_optimization(n):
    """动态值无法进行常量折叠"""
    x = n + 1 + 2  # 需要运行时计算
    return x

print("\n=== No Optimization ===")
dis.dis(no_optimization)

# 正例：列表和元组的差异
def use_list():
    return [1, 2, 3, 4, 5]

def use_tuple():
    return (1, 2, 3, 4, 5)

print("\n=== List vs Tuple Bytecode ===")
print("List:")
dis.dis(use_list)
print("\nTuple:")
dis.dis(use_tuple)
# 元组作为常量会被优化
```

#### 4.2.3 反汇编与调试

```python
import dis
import types

# 正例：动态生成代码的字节码分析
code_str = """
for i in range(3):
    print(i)
"""
dynamic_code = compile(code_str, '<dynamic>', 'exec')
print("=== Dynamic Code Bytecode ===")
dis.dis(dynamic_code)

# 正例：比较不同实现的字节码
def loop_for():
    """for循环"""
    result = 0
    for i in range(1000):
        result += i
    return result

def loop_while():
    """while循环"""
    result = 0
    i = 0
    while i < 1000:
        result += i
        i += 1
    return result

def loop_sum():
    """内置函数"""
    return sum(range(1000))

print("\n=== Loop Comparison ===")
print("For loop:")
dis.dis(loop_for)
print("\nWhile loop:")
dis.dis(loop_while)
print("\nBuilt-in sum:")
dis.dis(loop_sum)
```

---

### 4.3 帧栈机制

#### 4.3.1 调用栈的形式定义

**定义 4.3**（帧/Frame）：帧是函数调用的执行上下文：

$$
Frame = (CodeObject, LocalVars, Stack, Globals, Builtins, BlockStack)
$$

**定义 4.4**（调用栈）：调用栈是帧的LIFO结构：

$$
CallStack = [Frame_1, Frame_2, ..., Frame_n]
$$

```python
import sys
import inspect

# 正例：查看调用栈
def function_c():
    """最深层函数"""
    # 获取当前帧
    current_frame = inspect.currentframe()

    print("=== Call Stack ===")
    frame = current_frame
    depth = 0
    while frame:
        print(f"Depth {depth}: {frame.f_code.co_name}")
        frame = frame.f_back
        depth += 1

    # 查看帧信息
    print("\n=== Frame Info ===")
    print(f"Function name: {current_frame.f_code.co_name}")
    print(f"Filename: {current_frame.f_code.co_filename}")
    print(f"Line number: {current_frame.f_lineno}")
    print(f"Local variables: {list(current_frame.f_locals.keys())}")

    return depth

def function_b():
    return function_c()

def function_a():
    return function_b()

# 触发调用链
function_a()
```

#### 4.3.2 栈帧操作

```python
import sys

# 正例：递归深度限制
print(f"Default recursion limit: {sys.getrecursionlimit()}")

# 修改递归限制（谨慎使用）
sys.setrecursionlimit(2000)
print(f"New recursion limit: {sys.getrecursionlimit()}")

# 反例：栈溢出
def infinite_recursion(n):
    """会导致RecursionError"""
    return infinite_recursion(n + 1)

# 正例：尾递归优化（Python不支持，需手动实现）
class TailRecur:
    """使用迭代模拟尾递归"""
    def factorial(self, n, acc=1):
        while True:
            if n <= 1:
                return acc
            n, acc = n - 1, acc * n

tr = TailRecur()
print(f"Factorial(100): {tr.factorial(100)}")

# 正例：使用lru_cache优化递归
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    """带缓存的斐波那契"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"Fibonacci(100): {fibonacci(100)}")
```

#### 4.3.3 异常与栈展开

```python
import traceback
import sys

# 正例：异常传播与栈展开
def level_3():
    raise ValueError("Error at level 3")

def level_2():
    level_3()

def level_1():
    level_2()

try:
    level_1()
except ValueError as e:
    print("=== Exception Caught ===")
    print(f"Exception: {e}")
    print("\n=== Traceback ===")
    traceback.print_exc()

    # 获取异常信息
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f"\nException type: {exc_type}")
    print(f"Exception value: {exc_value}")

# 正例：自定义异常处理
def safe_call(func, *args, **kwargs):
    """安全的函数调用包装"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        # 记录完整堆栈
        tb = traceback.format_exc()
        print(f"Error calling {func.__name__}:")
        print(tb)
        return None

def may_fail(x):
    if x < 0:
        raise ValueError("x must be non-negative")
    return x ** 2

result = safe_call(may_fail, -5)
print(f"Result: {result}")
```

---

## 第五部分：错误处理机制

### 5.1 异常处理

#### 5.1.1 try/except/finally/else 形式定义

**定义 5.1**（异常处理结构）：异常处理可形式化为：

$$
\text{try-block} \rightarrow \begin{cases}
\text{else-block} & \text{if no exception} \\
\text{except-block}_i & \text{if } exception \in Exceptions_i \\
\text{finally-block} & \text{always}
\end{cases}
$$

```python
# 正例：完整的异常处理结构
def comprehensive_exception_handling(x, y):
    """展示完整的try/except/else/finally结构"""
    result = None

    try:
        # 可能引发异常的代码
        print(f"Trying to divide {x} by {y}")
        result = x / y

    except ZeroDivisionError as e:
        # 处理特定异常
        print(f"Caught ZeroDivisionError: {e}")
        result = float('inf')

    except TypeError as e:
        # 处理类型错误
        print(f"Caught TypeError: {e}")
        result = None

    except Exception as e:
        # 捕获所有其他异常（不推荐过度使用）
        print(f"Caught unexpected error: {e}")
        raise  # 重新抛出

    else:
        # 没有异常时执行
        print(f"Division successful: {result}")

    finally:
        # 总是执行（用于清理）
        print("Cleanup: finally block executed")

    return result

# 测试各种情况
print("=== Test 1: Normal division ===")
comprehensive_exception_handling(10, 2)

print("\n=== Test 2: Division by zero ===")
comprehensive_exception_handling(10, 0)

print("\n=== Test 3: Type error ===")
comprehensive_exception_handling("10", 2)
```

#### 5.1.2 异常层次结构

```python
# 正例：Python异常层次结构
"""
BaseException (所有异常的基类)
├── SystemExit              # sys.exit()引发
├── KeyboardInterrupt       # Ctrl+C
├── GeneratorExit           # 生成器关闭
└── Exception               # 常规异常的基类
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── TypeError
    ├── ValueError
    │   └── UnicodeError
    ├── RuntimeError
    │   └── RecursionError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── TimeoutError
    └── ...
"""

# 正例：异常层次结构的应用
def handle_file_operation(filepath):
    """根据异常类型采取不同处理"""
    try:
        with open(filepath, 'r') as f:
            return f.read()

    except FileNotFoundError:
        # 文件不存在
        print(f"File not found: {filepath}")
        return ""

    except PermissionError:
        # 权限不足
        print(f"Permission denied: {filepath}")
        return None

    except IsADirectoryError:
        # 路径是目录
        print(f"Path is a directory: {filepath}")
        return None

    except OSError as e:
        # 其他OS相关错误
        print(f"OS error: {e}")
        return None

# 测试
# handle_file_operation("/nonexistent/file.txt")
```

#### 5.1.3 自定义异常

```python
# 正例：自定义异常层次结构
class ApplicationError(Exception):
    """应用程序基础异常"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {super().__str__()}"
        return super().__str__()

class ValidationError(ApplicationError):
    """数据验证错误"""
    pass

class DatabaseError(ApplicationError):
    """数据库操作错误"""
    pass

class NotFoundError(ApplicationError):
    """资源未找到"""
    pass

# 使用自定义异常
class UserService:
    def __init__(self):
        self._users = {}

    def create_user(self, user_id, data):
        """创建用户"""
        if not user_id:
            raise ValidationError("User ID is required", error_code="VAL001")

        if user_id in self._users:
            raise ValidationError(f"User {user_id} already exists", error_code="VAL002")

        if 'email' not in data:
            raise ValidationError("Email is required", error_code="VAL003")

        self._users[user_id] = data
        return user_id

    def get_user(self, user_id):
        """获取用户"""
        if user_id not in self._users:
            raise NotFoundError(f"User {user_id} not found", error_code="NF001")
        return self._users[user_id]

# 测试
service = UserService()

try:
    service.create_user("", {})
except ValidationError as e:
    print(f"Validation failed: {e}")

try:
    service.get_user("nonexistent")
except NotFoundError as e:
    print(f"Not found: {e}")
```

#### 5.1.4 异常链与上下文

```python
# 正例：异常链（Python 3）
def process_data(data):
    try:
        result = int(data) / 0  # 会引发ZeroDivisionError
    except ValueError as e:
        # 转换异常类型，保留原始异常
        raise DataProcessingError(f"Invalid data: {data}") from e
    except ZeroDivisionError as e:
        # 添加上下文信息
        raise CalculationError("Division failed") from e

class DataProcessingError(Exception):
    pass

class CalculationError(Exception):
    pass

# 测试异常链
try:
    process_data("10")
except CalculationError as e:
    print(f"Caught: {e}")
    print(f"Caused by: {e.__cause__}")
    import traceback
    traceback.print_exc()

# 正例：上下文管理器与异常
def process_with_context(items):
    """使用上下文管理器处理异常"""
    processed = []
    errors = []

    for i, item in enumerate(items):
        try:
            result = 10 / item  # 可能除零
            processed.append(result)
        except ZeroDivisionError:
            errors.append((i, item, "Division by zero"))
        except Exception as e:
            errors.append((i, item, str(e)))

    return processed, errors

results, errs = process_with_context([1, 2, 0, 4, 0, 5])
print(f"Processed: {results}")
print(f"Errors: {errs}")
```

---

### 5.2 错误处理模式对比

#### 5.2.1 异常 vs 错误码

**定义 5.2**（错误处理模式对比）：

| 模式 | 优点 | 缺点 |
|------|------|------|
| 异常 | 错误处理与正常逻辑分离 | 控制流不清晰 |
| 错误码 | 显式错误处理 | 代码冗长，易遗漏 |

```python
# 反例：错误码模式（C风格）
def divide_error_code(a, b):
    """返回错误码和结果"""
    if b == 0:
        return None, "DIVISION_BY_ZERO"
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return None, "INVALID_TYPE"
    return a / b, None

# 使用错误码（需要每次检查）
result, error = divide_error_code(10, 0)
if error:
    print(f"Error: {error}")
else:
    print(f"Result: {result}")

# 正例：异常模式（Python风格）
def divide_exception(a, b):
    """使用异常处理错误"""
    return a / b  # 简洁，错误自动传播

# 使用异常（在适当层级处理）
try:
    result = divide_exception(10, 0)
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Error: Division by zero")

# 正例：混合模式（API设计）
def safe_divide(a, b, default=None):
    """提供默认值的安全除法"""
    try:
        return a / b
    except ZeroDivisionError:
        return default
    except TypeError:
        return default

print(safe_divide(10, 0, default=0))  # 0
print(safe_divide(10, 2, default=0))  # 5.0
```

#### 5.2.2 Result类型模式

```python
# 正例：Result类型实现（类似Rust）
from typing import Generic, TypeVar, Union

T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    """Result类型：显式错误处理"""

    def __init__(self, value: Union[T, E], is_ok: bool):
        self._value = value
        self._is_ok = is_ok

    @staticmethod
    def Ok(value: T) -> 'Result[T, E]':
        return Result(value, True)

    @staticmethod
    def Err(error: E) -> 'Result[T, E]':
        return Result(error, False)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self._is_ok

    def unwrap(self) -> T:
        if self._is_ok:
            return self._value
        raise ValueError(f"Called unwrap on Err: {self._value}")

    def unwrap_or(self, default: T) -> T:
        return self._value if self._is_ok else default

    def map(self, func) -> 'Result':
        if self._is_ok:
            return Result.Ok(func(self._value))
        return self

    def __repr__(self):
        if self._is_ok:
            return f"Ok({self._value!r})"
        return f"Err({self._value!r})"

# 使用Result类型
def parse_number(s: str) -> Result[float, str]:
    try:
        return Result.Ok(float(s))
    except ValueError:
        return Result.Err(f"Cannot parse '{s}' as number")

def divide_result(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Result.Err("Division by zero")
    return Result.Ok(a / b)

# 链式处理
result = parse_number("10") \
    .map(lambda x: x * 2) \
    .map(lambda x: divide_result(x, 5)) \
    .map(lambda r: r.unwrap_or(0))

print(f"Result: {result}")

# 错误处理
error_result = parse_number("not_a_number")
print(f"Error result: {error_result}")
print(f"Unwrap or default: {error_result.unwrap_or(0)}")
```

#### 5.2.3 Option类型模式

```python
# 正例：Option类型实现（类似Rust/Swift）
from typing import Generic, TypeVar, Callable, Optional

T = TypeVar('T')
U = TypeVar('U')

class Option(Generic[T]):
    """Option类型：表示可能不存在的值"""

    def __init__(self, value: Optional[T]):
        self._value = value

    @staticmethod
    def Some(value: T) -> 'Option[T]':
        return Option(value)

    @staticmethod
    def None_() -> 'Option[T]':
        return Option(None)

    def is_some(self) -> bool:
        return self._value is not None

    def is_none(self) -> bool:
        return self._value is None

    def unwrap(self) -> T:
        if self._value is None:
            raise ValueError("Called unwrap on None")
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value if self._value is not None else default

    def map(self, func: Callable[[T], U]) -> 'Option[U]':
        if self._value is not None:
            return Option.Some(func(self._value))
        return Option.None_()

    def flat_map(self, func: Callable[[T], 'Option[U]']) -> 'Option[U]':
        if self._value is not None:
            return func(self._value)
        return Option.None_()

    def filter(self, predicate: Callable[[T], bool]) -> 'Option[T]':
        if self._value is not None and predicate(self._value):
            return self
        return Option.None_()

    def __repr__(self):
        if self._value is None:
            return "None"
        return f"Some({self._value!r})"

# 使用Option类型
def find_user(users: dict, user_id: str) -> Option[dict]:
    """查找用户，返回Option"""
    user = users.get(user_id)
    return Option.Some(user) if user else Option.None_()

def get_email(user: dict) -> Option[str]:
    """获取用户邮箱"""
    email = user.get('email')
    return Option.Some(email) if email else Option.None_()

# 测试数据
users_db = {
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob"},  # 没有email
}

# 链式操作
email_option = find_user(users_db, "user1") \
    .flat_map(get_email) \
    .map(lambda e: e.upper())

print(f"User1 email: {email_option}")

# 不存在的用户
no_user = find_user(users_db, "user3")
print(f"User3: {no_user}")

# 没有email的用户
no_email = find_user(users_db, "user2") \
    .flat_map(get_email)
print(f"User2 email: {no_email}")
```

#### 5.2.4 错误处理模式选择指南

| 场景 | 推荐模式 | 理由 |
|------|----------|------|
| 异常条件罕见 | 异常 | 正常路径清晰 |
| 错误是正常结果 | Result/Option | 强制错误处理 |
| 库API设计 | 混合 | 提供多种接口 |
| 性能敏感 | 错误码 | 无异常开销 |

```python
# 正例：混合模式API设计
class FileProcessor:
    """提供多种错误处理方式的文件处理器"""

    def read_file_exception(self, path: str) -> str:
        """使用异常模式 - 适合简单场景"""
        with open(path, 'r') as f:
            return f.read()

    def read_file_result(self, path: str) -> Result[str, str]:
        """使用Result模式 - 适合需要显式处理的场景"""
        try:
            with open(path, 'r') as f:
                return Result.Ok(f.read())
        except FileNotFoundError:
            return Result.Err(f"File not found: {path}")
        except PermissionError:
            return Result.Err(f"Permission denied: {path}")
        except Exception as e:
            return Result.Err(f"Error reading {path}: {e}")

    def read_file_option(self, path: str) -> Option[str]:
        """使用Option模式 - 适合简单存在性检查"""
        try:
            with open(path, 'r') as f:
                return Option.Some(f.read())
        except Exception:
            return Option.None_()

# 使用示例
processor = FileProcessor()

# 方式1：异常模式
try:
    content = processor.read_file_exception("test.txt")
except FileNotFoundError:
    content = ""

# 方式2：Result模式
result = processor.read_file_result("test.txt")
content = result.unwrap_or("")

# 方式3：Option模式
option = processor.read_file_option("test.txt")
content = option.unwrap_or("")
```

---

## 第六部分：模块化设计

### 6.1 封装机制

#### 6.1.1 封装的形式定义

**定义 6.1**（封装）：封装是将数据与操作数据的方法绑定，并隐藏内部实现的机制：

$$
Encapsulation: Object = (PrivateState, PublicInterface, InternalMethods)
$$

```python
# 正例：Python的封装机制
class BankAccount:
    """银行账户类 - 展示封装"""

    # 类变量（共享）
    _interest_rate = 0.05  # 受保护
    __bank_code = "BANK001"  # 私有（名称修饰）

    def __init__(self, owner: str, initial_balance: float = 0.0):
        # 实例变量
        self._owner = owner          # 受保护（约定）
        self.__balance = initial_balance  # 私有（名称修饰）
        self.__transaction_history = []   # 私有

    # 属性访问器（getter）
    @property
    def balance(self) -> float:
        """只读属性：余额"""
        return self.__balance

    @property
    def owner(self) -> str:
        """只读属性：所有者"""
        return self._owner

    # 公共方法
    def deposit(self, amount: float) -> bool:
        """存款"""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.__balance += amount
        self.__log_transaction("DEPOSIT", amount)
        return True

    def withdraw(self, amount: float) -> bool:
        """取款"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")

        self.__balance -= amount
        self.__log_transaction("WITHDRAW", amount)
        return True

    # 私有方法
    def __log_transaction(self, transaction_type: str, amount: float):
        """记录交易（私有）"""
        from datetime import datetime
        self.__transaction_history.append({
            'type': transaction_type,
            'amount': amount,
            'timestamp': datetime.now()
        })

    def get_transaction_history(self) -> list:
        """获取交易历史（副本）"""
        return self.__transaction_history.copy()

# 使用封装类
account = BankAccount("Alice", 1000.0)
print(f"Owner: {account.owner}")
print(f"Balance: {account.balance}")

account.deposit(500.0)
print(f"Balance after deposit: {account.balance}")

account.withdraw(200.0)
print(f"Balance after withdrawal: {account.balance}")

print(f"Transaction history: {account.get_transaction_history()}")

# 反例：尝试访问私有成员
# print(account.__balance)  # AttributeError
# 但可以通过名称修饰访问（不推荐）
print(f"Direct access (don't do this): {account._BankAccount__balance}")
```

#### 6.1.2 属性装饰器

```python
# 正例：完整的属性控制
class Temperature:
    """温度类 - 展示属性控制"""

    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """摄氏度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        """设置摄氏度（带验证）"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """华氏度（计算属性）"""
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        """通过华氏度设置"""
        self.celsius = (value - 32) * 5/9

    @property
    def kelvin(self) -> float:
        """开尔文"""
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value: float):
        self.celsius = value - 273.15

    @celsius.deleter
    def celsius(self):
        """删除属性"""
        print("Temperature reset to default")
        self._celsius = 0.0

# 使用
temp = Temperature(25.0)
print(f"Celsius: {temp.celsius}")
print(f"Fahrenheit: {temp.fahrenheit}")
print(f"Kelvin: {temp.kelvin}")

temp.fahrenheit = 98.6
print(f"After setting to 98.6F: {temp.celsius:.1f}C")

# 反例：无效温度
try:
    temp.celsius = -300
except ValueError as e:
    print(f"Validation caught: {e}")
```

---

### 6.2 接口设计

#### 6.2.1 抽象基类（ABC）

```python
from abc import ABC, abstractmethod
from typing import List

# 正例：抽象基类定义接口
class DataStore(ABC):
    """数据存储抽象基类"""

    @abstractmethod
    def connect(self) -> bool:
        """连接到存储"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """断开连接"""
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        """获取值"""
        pass

    @abstractmethod
    def set(self, key: str, value: str) -> bool:
        """设置值"""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """删除值"""
        pass

    # 具体方法（可选实现）
    def exists(self, key: str) -> bool:
        """检查键是否存在（默认实现）"""
        try:
            self.get(key)
            return True
        except KeyError:
            return False

# 具体实现：内存存储
class InMemoryStore(DataStore):
    """内存数据存储实现"""

    def __init__(self):
        self._data = {}
        self._connected = False

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False
        self._data.clear()

    def get(self, key: str) -> str:
        if not self._connected:
            raise ConnectionError("Not connected")
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found")
        return self._data[key]

    def set(self, key: str, value: str) -> bool:
        if not self._connected:
            raise ConnectionError("Not connected")
        self._data[key] = value
        return True

    def delete(self, key: str) -> bool:
        if not self._connected:
            raise ConnectionError("Not connected")
        if key in self._data:
            del self._data[key]
            return True
        return False

# 具体实现：文件存储
class FileStore(DataStore):
    """文件数据存储实现"""

    def __init__(self, filepath: str):
        self._filepath = filepath
        self._data = {}
        self._connected = False

    def connect(self) -> bool:
        import json
        try:
            with open(self._filepath, 'r') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {}
        self._connected = True
        return True

    def disconnect(self) -> None:
        import json
        if self._connected:
            with open(self._filepath, 'w') as f:
                json.dump(self._data, f)
            self._connected = False

    def get(self, key: str) -> str:
        if not self._connected:
            raise ConnectionError("Not connected")
        return self._data.get(key)

    def set(self, key: str, value: str) -> bool:
        if not self._connected:
            raise ConnectionError("Not connected")
        self._data[key] = value
        return True

    def delete(self, key: str) -> bool:
        if not self._connected:
            raise ConnectionError("Not connected")
        if key in self._data:
            del self._data[key]
            return True
        return False

# 使用接口
def test_data_store(store: DataStore):
    """测试任何DataStore实现"""
    store.connect()
    store.set("key1", "value1")
    assert store.get("key1") == "value1"
    assert store.exists("key1")
    store.delete("key1")
    assert not store.exists("key1")
    store.disconnect()
    print(f"{type(store).__name__} passed all tests")

# 测试不同实现
test_data_store(InMemoryStore())
# test_data_store(FileStore("/tmp/test_store.json"))
```

#### 6.2.2 协议类（Protocol）

```python
from typing import Protocol, runtime_checkable

# 正例：协议定义（Python 3.8+）
@runtime_checkable
class Serializable(Protocol):
    """可序列化协议"""

    def to_dict(self) -> dict:
        """转换为字典"""
        ...

    @classmethod
    def from_dict(cls, data: dict) -> 'Serializable':
        """从字典创建"""
        ...

@runtime_checkable
class Comparable(Protocol):
    """可比较协议"""

    def __lt__(self, other) -> bool:
        ...

    def __eq__(self, other) -> bool:
        ...

# 实现协议（无需显式继承）
class Person:
    """隐式实现Serializable协议"""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def to_dict(self) -> dict:
        return {"name": self.name, "age": self.age}

    @classmethod
    def from_dict(cls, data: dict) -> 'Person':
        return cls(data["name"], data["age"])

    def __lt__(self, other: 'Person') -> bool:
        return self.age < other.age

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age

# 使用协议
def serialize_items(items: List[Serializable]) -> List[dict]:
    """序列化任何可序列化对象"""
    return [item.to_dict() for item in items]

def sort_items(items: List[Comparable]) -> List[Comparable]:
    """排序任何可比较对象"""
    return sorted(items)

# 测试
people = [Person("Bob", 30), Person("Alice", 25), Person("Charlie", 35)]
print(f"Serialized: {serialize_items(people)}")
print(f"Sorted: {[p.name for p in sort_items(people)]}")

# 运行时检查
print(f"Person is Serializable: {isinstance(Person("A", 1), Serializable)}")
```

---

### 6.3 依赖注入

#### 6.3.1 依赖注入的形式定义

**定义 6.2**（依赖注入）：依赖注入是将依赖关系从内部创建转移到外部提供的模式：

```
传统方式：A → 创建 B → 使用 B
DI方式：A ← 接收 B ← 外部提供 B
```

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# 正例：依赖注入实现

# 1. 定义抽象接口
class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass

class Database(ABC):
    @abstractmethod
    def query(self, sql: str) -> list:
        pass

# 2. 具体实现
class ConsoleLogger(Logger):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")

class FileLogger(Logger):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def log(self, message: str) -> None:
        with open(self._filepath, 'a') as f:
            f.write(f"{message}\n")

class MockDatabase(Database):
    """测试用的模拟数据库"""
    def query(self, sql: str) -> list:
        return [{"id": 1, "name": "Test"}]

class PostgreSQLDatabase(Database):
    """真实PostgreSQL实现"""
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def query(self, sql: str) -> list:
        # 真实数据库查询
        # import psycopg2
        # conn = psycopg2.connect(self._connection_string)
        # ...
        return []

# 3. 依赖注入的Service类
class UserService:
    """用户服务 - 通过构造函数注入依赖"""

    def __init__(self, logger: Logger, database: Database):
        self._logger = logger
        self._database = database

    def get_user(self, user_id: int) -> dict:
        self._logger.log(f"Getting user {user_id}")
        result = self._database.query(f"SELECT * FROM users WHERE id = {user_id}")
        return result[0] if result else None

    def create_user(self, name: str) -> int:
        self._logger.log(f"Creating user: {name}")
        # ...
        return 1

# 4. 使用依赖注入
# 生产环境配置
production_logger = FileLogger("/var/log/app.log")
production_db = PostgreSQLDatabase("postgresql://...")
production_service = UserService(production_logger, production_db)

# 测试环境配置
test_logger = ConsoleLogger()
test_db = MockDatabase()
test_service = UserService(test_logger, test_db)

# 测试
test_user = test_service.get_user(1)
print(f"Test user: {test_user}")

# 正例：使用容器管理依赖
class DIContainer:
    """简单的依赖注入容器"""

    def __init__(self):
        self._registrations = {}
        self._singletons = {}

    def register(self, interface: type, implementation: type,
                 instance=None, singleton=False):
        """注册依赖"""
        self._registrations[interface] = {
            'implementation': implementation,
            'instance': instance,
            'singleton': singleton
        }

    def resolve(self, interface: type):
        """解析依赖"""
        if interface not in self._registrations:
            raise KeyError(f"No registration for {interface}")

        reg = self._registrations[interface]

        # 返回已有实例
        if reg['instance']:
            return reg['instance']

        # 单例模式
        if reg['singleton']:
            if interface not in self._singletons:
                self._singletons[interface] = reg['implementation']()
            return self._singletons[interface]

        # 创建新实例
        return reg['implementation']()

# 使用容器
container = DIContainer()
container.register(Logger, ConsoleLogger, singleton=True)
container.register(Database, MockDatabase)

logger = container.resolve(Logger)
database = container.resolve(Database)
service = UserService(logger, database)
```

#### 6.3.2 依赖注入模式对比

| 模式 | 优点 | 缺点 |
|------|------|------|
| 构造函数注入 | 依赖明确，不可变 | 参数可能过多 |
| Setter注入 | 可选依赖 | 运行时可能未设置 |
| 接口注入 | 灵活 | 复杂度高 |

```python
# 正例：构造函数注入（推荐）
class ConstructorInjection:
    def __init__(self, dep1, dep2, dep3):
        self._dep1 = dep1
        self._dep2 = dep2
        self._dep3 = dep3

# 正例：Setter注入（可选依赖）
class SetterInjection:
    def __init__(self):
        self._optional_dep = None

    def set_optional_dep(self, dep):
        self._optional_dep = dep

    def do_something(self):
        if self._optional_dep:
            self._optional_dep.help()

# 反例：服务定位器（反模式）
class ServiceLocator:
    """避免使用 - 隐藏依赖关系"""
    _services = {}

    @classmethod
    def register(cls, name, service):
        cls._services[name] = service

    @classmethod
    def get(cls, name):
        return cls._services[name]

# 使用服务定位器（不推荐）
class BadService:
    def do_something(self):
        logger = ServiceLocator.get('logger')  # 隐藏依赖！
        logger.log("Doing something")
```

---

### 6.4 插件架构

#### 6.4.1 插件系统设计

```python
import importlib
import pkgutil
from abc import ABC, abstractmethod
from typing import Dict, Type, List

# 正例：插件系统实现

class Plugin(ABC):
    """插件基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本"""
        pass

    @abstractmethod
    def initialize(self, context: dict) -> bool:
        """初始化插件"""
        pass

    @abstractmethod
    def execute(self, data: dict) -> dict:
        """执行插件功能"""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """关闭插件"""
        pass

class PluginManager:
    """插件管理器"""

    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._context = {}

    def register(self, plugin: Plugin) -> bool:
        """注册插件"""
        if plugin.name in self._plugins:
            print(f"Plugin {plugin.name} already registered")
            return False

        if plugin.initialize(self._context):
            self._plugins[plugin.name] = plugin
            print(f"Plugin {plugin.name} v{plugin.version} registered")
            return True
        return False

    def unregister(self, name: str) -> bool:
        """注销插件"""
        if name in self._plugins:
            self._plugins[name].shutdown()
            del self._plugins[name]
            return True
        return False

    def execute(self, name: str, data: dict) -> dict:
        """执行指定插件"""
        if name not in self._plugins:
            raise KeyError(f"Plugin {name} not found")
        return self._plugins[name].execute(data)

    def execute_all(self, data: dict) -> Dict[str, dict]:
        """执行所有插件"""
        results = {}
        for name, plugin in self._plugins.items():
            try:
                results[name] = plugin.execute(data)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results

    def load_from_module(self, module_path: str) -> List[Plugin]:
        """从模块加载插件"""
        loaded = []
        try:
            module = importlib.import_module(module_path)
            for name, obj in module.__dict__.items():
                if (isinstance(obj, type) and
                    issubclass(obj, Plugin) and
                    obj is not Plugin):
                    instance = obj()
                    if self.register(instance):
                        loaded.append(instance)
        except ImportError as e:
            print(f"Failed to load module {module_path}: {e}")
        return loaded

    def discover_plugins(self, package_path: str) -> List[Plugin]:
        """自动发现包中的插件"""
        loaded = []
        try:
            package = importlib.import_module(package_path)
            for _, name, ispkg in pkgutil.iter_modules(package.__path__):
                if not ispkg:
                    full_name = f"{package_path}.{name}"
                    loaded.extend(self.load_from_module(full_name))
        except ImportError as e:
            print(f"Failed to discover plugins: {e}")
        return loaded

    @property
    def plugins(self) -> Dict[str, Plugin]:
        return self._plugins.copy()

# 示例插件实现
class LoggingPlugin(Plugin):
    """日志插件"""

    @property
    def name(self) -> str:
        return "logging"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, context: dict) -> bool:
        context['logger'] = self
        return True

    def execute(self, data: dict) -> dict:
        message = data.get('message', '')
        level = data.get('level', 'INFO')
        print(f"[{level}] {message}")
        return {"logged": True}

    def shutdown(self) -> None:
        print("Logging plugin shutdown")

class ValidationPlugin(Plugin):
    """验证插件"""

    @property
    def name(self) -> str:
        return "validation"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, context: dict) -> bool:
        context['validator'] = self
        return True

    def execute(self, data: dict) -> dict:
        rules = data.get('rules', {})
        values = data.get('values', {})
        errors = {}

        for field, rule in rules.items():
            if rule == 'required' and not values.get(field):
                errors[field] = "Field is required"

        return {"valid": len(errors) == 0, "errors": errors}

    def shutdown(self) -> None:
        print("Validation plugin shutdown")

# 使用插件系统
manager = PluginManager()

# 手动注册插件
manager.register(LoggingPlugin())
manager.register(ValidationPlugin())

# 执行插件
print("\n=== Execute logging plugin ===")
result = manager.execute("logging", {"message": "Hello World", "level": "INFO"})
print(f"Result: {result}")

print("\n=== Execute validation plugin ===")
result = manager.execute("validation", {
    "rules": {"name": "required", "email": "required"},
    "values": {"name": "John", "email": ""}
})
print(f"Result: {result}")

print("\n=== Execute all plugins ===")
results = manager.execute_all({"message": "Test"})
print(f"All results: {results}")

# 注销插件
manager.unregister("logging")
print(f"\nRemaining plugins: {list(manager.plugins.keys())}")
```

#### 6.4.2 钩子系统

```python
from typing import Callable, List, Any

# 正例：钩子系统实现
class HookSystem:
    """钩子系统 - 允许插件在特定点扩展功能"""

    def __init__(self):
        self._hooks: Dict[str, List[Callable]] = {}

    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """注册钩子回调"""
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        self._hooks[hook_name].append(callback)

    def unregister_hook(self, hook_name: str, callback: Callable) -> bool:
        """注销钩子回调"""
        if hook_name in self._hooks:
            if callback in self._hooks[hook_name]:
                self._hooks[hook_name].remove(callback)
                return True
        return False

    def do_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """执行钩子（返回所有结果）"""
        results = []
        if hook_name in self._hooks:
            for callback in self._hooks[hook_name]:
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Hook {hook_name} callback failed: {e}")
        return results

    def apply_filter(self, hook_name: str, value: Any, *args, **kwargs) -> Any:
        """应用过滤器（链式处理值）"""
        if hook_name in self._hooks:
            for callback in self._hooks[hook_name]:
                try:
                    value = callback(value, *args, **kwargs)
                except Exception as e:
                    print(f"Filter {hook_name} callback failed: {e}")
        return value

# 使用钩子系统
hooks = HookSystem()

# 注册过滤器
hooks.register_hook("format_text", lambda text: text.upper())
hooks.register_hook("format_text", lambda text: f"[{text}]")

# 应用过滤器
result = hooks.apply_filter("format_text", "hello")
print(f"Filtered: {result}")  # [HELLO]

# 注册动作钩子
hooks.register_hook("before_save", lambda data: print(f"Before save: {data}"))
hooks.register_hook("before_save", lambda data: print(f"Validating: {data}"))

# 执行动作
hooks.do_hook("before_save", {"name": "test"})
```

---

## 总结

本文档系统梳理了Python程序设计的核心机制：

### 关键概念回顾

1. **编程范式**：Python支持多范式，理解各范式的适用场景
2. **类型系统**：动态强类型，鸭子类型提供灵活性
3. **内存模型**：引用计数+GC，注意GIL的影响
4. **执行模型**：字节码解释执行，理解帧栈机制
5. **错误处理**：异常为主，Result/Option模式提供替代方案
6. **模块化设计**：封装、接口、依赖注入、插件架构

### 最佳实践

- 根据场景选择合适的编程范式
- 利用类型提示提高代码可维护性
- 注意内存管理，避免循环引用
- 合理使用异常，考虑替代模式
- 设计松耦合的模块化架构

---

*文档生成时间：2024年*
