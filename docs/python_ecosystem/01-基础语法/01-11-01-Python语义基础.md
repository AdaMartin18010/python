# Python语义模型基础

## 1. Python语义模型概述

### 1.1 语义模型定义

Python语义模型描述了Python语言中程序的含义和行为规则，包括：

1. **语法语义映射**：将语法结构映射到语义含义
2. **执行语义**：描述程序如何执行
3. **类型语义**：描述类型系统和类型检查
4. **作用域语义**：描述变量和函数的作用域规则
5. **对象语义**：描述对象的创建、修改和销毁

### 1.2 Python语义特点

**特点 11.1.1** 动态语义
Python采用动态语义，类型检查在运行时进行：

```python
x = 42          # 运行时确定类型为int
x = "hello"     # 运行时改变类型为str
x = [1, 2, 3]   # 运行时改变类型为list
```

**特点 11.1.2** 引用语义
Python使用引用语义，变量是对象的引用：

```python
a = [1, 2, 3]
b = a           # b和a引用同一个对象
b.append(4)     # 修改会影响a
print(a)        # [1, 2, 3, 4]
```

**特点 11.1.3** 鸭子类型语义
Python采用鸭子类型，关注对象的行为而非类型：

```python
def process_data(obj):
    # 只要对象有__len__方法就可以
    if hasattr(obj, '__len__'):
        return len(obj)
    return 0

# 可以处理不同类型的对象
process_data([1, 2, 3])    # 3
process_data("hello")       # 5
process_data({"a": 1})     # 1
```

## 2. Python语义层次结构

### 2.1 语义层次

Python语义模型分为多个层次：

```text
第0层：词法语义
├── 标识符语义
├── 字面量语义
└── 运算符语义

第1层：表达式语义
├── 算术表达式语义
├── 比较表达式语义
├── 逻辑表达式语义
└── 函数调用语义

第2层：语句语义
├── 赋值语句语义
├── 控制流语句语义
├── 函数定义语义
└── 类定义语义

第3层：模块语义
├── 导入语义
├── 命名空间语义
└── 包语义

第4层：程序语义
├── 执行语义
├── 错误处理语义
└── 并发语义
```

### 2.2 语义关系映射

**定义 11.1.1** 语义映射函数
设 $S$ 是语法结构集合，$M$ 是语义含义集合，则语义映射函数为：
$$\text{SemMap}: S \rightarrow M$$

**定义 11.1.2** 语义等价关系
两个语法结构 $s_1, s_2 \in S$ 语义等价，当且仅当：
$$\text{SemMap}(s_1) = \text{SemMap}(s_2)$$

## 3. Python核心语义规则

### 3.1 变量绑定语义

**规则 11.1.1** 变量赋值语义

```python
# 语义规则：变量赋值
x = expression
# 语义含义：
# 1. 计算expression的值
# 2. 创建对计算结果的引用
# 3. 将引用绑定到变量名x
```

**规则 11.1.2** 多重赋值语义

```python
# 语义规则：多重赋值
a, b = b, a
# 语义含义：
# 1. 计算右侧所有表达式的值
# 2. 创建临时元组存储结果
# 3. 将元组元素分别绑定到左侧变量
```

### 3.2 函数调用语义

**规则 11.1.3** 函数调用语义

```python
# 语义规则：函数调用
result = function(arg1, arg2, kwarg=value)
# 语义含义：
# 1. 计算所有参数的值
# 2. 创建函数调用帧
# 3. 绑定参数到函数参数名
# 4. 执行函数体
# 5. 返回结果值
```

**规则 11.1.4** 方法调用语义

```python
# 语义规则：方法调用
obj.method(arg)
# 语义含义：
# 1. 获取obj的method属性
# 2. 将obj作为第一个参数(self)
# 3. 执行方法调用
```

### 3.3 控制流语义

**规则 11.1.5** 条件语句语义

```python
# 语义规则：if语句
if condition:
    block1
else:
    block2
# 语义含义：
# 1. 计算condition的布尔值
# 2. 如果为True，执行block1
# 3. 如果为False，执行block2
```

**规则 11.1.6** 循环语句语义

```python
# 语义规则：for循环
for item in iterable:
    block
# 语义含义：
# 1. 获取iterable的迭代器
# 2. 对每个元素执行block
# 3. 直到迭代器耗尽
```

## 4. Python类型语义

### 4.1 类型系统语义

**类型语义 11.1.1** 动态类型语义

```python
# Python类型语义特点
x = 42          # 类型：int
x = "hello"     # 类型：str
x = [1, 2, 3]   # 类型：list

# 类型检查在运行时进行
def add(a, b):
    return a + b  # 运行时检查a和b是否支持+

add(1, 2)       # 正常执行
add("a", "b")   # 正常执行
add(1, "a")     # 运行时错误
```

**类型语义 11.1.2** 类型注解语义

```python
# 类型注解（Python 3.5+）
def greet(name: str) -> str:
    return f"Hello, {name}"

# 语义含义：
# 1. 类型注解提供类型提示
# 2. 不影响运行时行为
# 3. 可被类型检查器使用
```

### 4.2 对象语义

**对象语义 11.1.1** 对象创建语义

```python
# 对象创建语义
class MyClass:
    def __init__(self, value):
        self.value = value

obj = MyClass(42)
# 语义含义：
# 1. 创建MyClass的实例
# 2. 调用__init__方法
# 3. 返回实例对象
```

**对象语义 11.1.2** 属性访问语义

```python
# 属性访问语义
obj.attribute
# 语义含义：
# 1. 在obj的__dict__中查找attribute
# 2. 如果未找到，调用__getattr__
# 3. 返回属性值
```

## 5. Python作用域语义

### 5.1 作用域规则

**作用域语义 11.1.1** LEGB规则

```python
# Python作用域查找顺序：LEGB
# L: Local (局部作用域)
# E: Enclosing (闭包作用域)
# G: Global (全局作用域)
# B: Built-in (内置作用域)

x = 1  # 全局作用域

def outer():
    x = 2  # 闭包作用域
    
    def inner():
        x = 3  # 局部作用域
        print(x)  # 3
    
    inner()

outer()
```

**作用域语义 11.1.2** 变量声明语义

```python
# global声明语义
x = 1

def func():
    global x  # 声明使用全局变量
    x = 2     # 修改全局变量

# nonlocal声明语义
def outer():
    x = 1
    
    def inner():
        nonlocal x  # 声明使用闭包变量
        x = 2       # 修改闭包变量
```

### 5.2 命名空间语义

**命名空间语义 11.1.1** 模块命名空间

```python
# 模块命名空间语义
import math
from math import sqrt

# 语义含义：
# 1. import math: 创建math命名空间
# 2. from math import sqrt: 将sqrt导入当前命名空间
```

**命名空间语义 11.1.2** 类命名空间

```python
# 类命名空间语义
class MyClass:
    class_var = 1  # 类变量
    
    def __init__(self):
        self.instance_var = 2  # 实例变量

# 语义含义：
# 1. class_var属于类命名空间
# 2. instance_var属于实例命名空间
```

## 6. Python执行语义

### 6.1 程序执行语义

**执行语义 11.1.1** 程序启动语义

```python
# 程序启动语义
if __name__ == "__main__":
    main()
# 语义含义：
# 1. 创建主模块命名空间
# 2. 执行模块代码
# 3. 如果作为主程序运行，执行main()
```

**执行语义 11.1.2** 异常处理语义

```python
# 异常处理语义
try:
    risky_operation()
except ValueError as e:
    handle_error(e)
finally:
    cleanup()
# 语义含义：
# 1. 执行try块
# 2. 如果发生异常，执行except块
# 3. 无论是否异常，都执行finally块
```

### 6.2 并发语义

**并发语义 11.1.1** 线程语义

```python
# 线程语义
import threading

def worker():
    print("Working...")

thread = threading.Thread(target=worker)
thread.start()
# 语义含义：
# 1. 创建新线程
# 2. 在新线程中执行worker函数
# 3. 主线程继续执行
```

**并发语义 11.1.2** 异步语义

```python
# 异步语义
import asyncio

async def async_worker():
    await asyncio.sleep(1)
    return "Done"

# 语义含义：
# 1. 创建协程对象
# 2. 在事件循环中调度执行
# 3. 支持await暂停和恢复
```

## 7. Python语义模型的形式化描述

### 7.1 语义状态

**定义 11.1.3** 程序状态
程序状态 $S$ 是一个五元组：
$$S = (E, V, H, C, T)$$

其中：

- $E$ 是环境（命名空间映射）
- $V$ 是变量绑定
- $H$ 是堆（对象存储）
- $C$ 是控制流
- $T$ 是类型信息

### 7.2 语义转换规则

**规则 11.1.7** 赋值转换规则
$$\frac{S \vdash e \Rightarrow v \quad S' = S[V \mapsto V[x \mapsto v]]}{S \vdash x = e \Rightarrow S'}$$

**规则 11.1.8** 函数调用转换规则
$$\frac{S \vdash f \Rightarrow func \quad S \vdash args \Rightarrow vals \quad S' = func(vals, S)}{S \vdash f(args) \Rightarrow S'}$$

## 8. 总结

Python语义模型的核心特点包括：

1. **动态语义**：类型检查在运行时进行
2. **引用语义**：变量是对象的引用
3. **鸭子类型**：关注行为而非类型
4. **多层次语义**：从词法到程序的完整语义层次
5. **形式化描述**：可以用数学方法描述语义规则

Python语义模型为理解Python程序的行为提供了理论基础，也为Python解释器的实现提供了指导。
