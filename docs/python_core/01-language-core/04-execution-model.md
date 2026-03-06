# Python 执行模型

**理解Python代码如何运行**

---

## 📋 目录

- [Python解释器](#Python解释器)
- [字节码与虚拟机](#字节码与虚拟机)
- [执行流程](#执行流程)
- [异常处理机制](#异常处理机制)
- [并发模型](#并发模型)

---

## Python解释器

### CPython架构

```python
"""
CPython执行流程
"""

# 执行流程:
"""
1. 源代码 (.py)
   ↓
2. 词法分析 (Lexer) → Tokens
   ↓
3. 语法分析 (Parser) → AST
   ↓
4. 编译器 (Compiler) → 字节码
   ↓
5. 虚拟机 (VM) → 执行
"""

# 查看字节码
import dis

def add(a, b):
    return a + b

dis.dis(add)
"""
输出:
  2           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
"""
```

### 编译与执行

```python
"""
Python代码的编译和执行
"""

# 1. 编译源代码
code_string = """
def greet(name):
    return f"Hello, {name}"

result = greet("Alice")
"""

# 编译为代码对象
code_obj = compile(code_string, "<string>", "exec")
print(type(code_obj))  # <class 'code'>

# 2. 执行代码对象
namespace = {}
exec(code_obj, namespace)
print(namespace['result'])  # Hello, Alice

# 3. eval执行表达式
result = eval("2 + 3 * 4")
print(result)  # 14

# ============================================
# .pyc文件
# ============================================

"""
.pyc文件包含:
- Magic number (Python版本)
- 时间戳
- 源文件大小
- 编译的字节码

位置: __pycache__/module.cpython-312.pyc
"""

# 禁用.pyc生成
import sys
sys.dont_write_bytecode = True

# 查看.pyc内容
import importlib.util
spec = importlib.util.find_spec("os")
print(spec.cached)  # .pyc文件路径
```

---

## 字节码与虚拟机

### 字节码分析

```python
"""
深入理解字节码
"""
import dis

# 简单函数
def example(x):
    if x > 0:
        return x * 2
    else:
        return 0

dis.dis(example)
"""
  2           0 LOAD_FAST                0 (x)
              2 LOAD_CONST               1 (0)
              4 COMPARE_OP               4 (>)
              6 POP_JUMP_IF_FALSE        7 (to 14)

  3           8 LOAD_FAST                0 (x)
             10 LOAD_CONST               2 (2)
             12 BINARY_MULTIPLY
             14 RETURN_VALUE

  5     >>   16 LOAD_CONST               1 (0)
             18 RETURN_VALUE
"""

# ============================================
# 常见字节码指令
# ============================================

"""
栈操作:
- LOAD_FAST: 加载局部变量
- LOAD_CONST: 加载常量
- STORE_FAST: 存储局部变量
- POP_TOP: 弹出栈顶

运算:
- BINARY_ADD: 加法
- BINARY_MULTIPLY: 乘法
- COMPARE_OP: 比较

控制流:
- POP_JUMP_IF_FALSE: 条件跳转
- JUMP_ABSOLUTE: 无条件跳转
- RETURN_VALUE: 返回

函数调用:
- CALL_FUNCTION: 调用函数
- MAKE_FUNCTION: 创建函数
"""
```

### 栈式虚拟机

```python
"""
Python虚拟机是栈式虚拟机
"""

# 示例: a + b * c
# 对应字节码:
"""
LOAD_FAST       0 (a)      # 栈: [a]
LOAD_FAST       1 (b)      # 栈: [a, b]
LOAD_FAST       2 (c)      # 栈: [a, b, c]
BINARY_MULTIPLY            # 栈: [a, (b*c)]
BINARY_ADD                 # 栈: [(a + b*c)]
"""

# 可以手动模拟
def simulate_expression():
    """模拟栈式计算"""
    stack = []

    # a = 10, b = 3, c = 4
    stack.append(10)  # LOAD_FAST a
    stack.append(3)   # LOAD_FAST b
    stack.append(4)   # LOAD_FAST c

    # BINARY_MULTIPLY
    c = stack.pop()
    b = stack.pop()
    stack.append(b * c)

    # BINARY_ADD
    bc = stack.pop()
    a = stack.pop()
    stack.append(a + bc)

    return stack[0]  # RETURN_VALUE

print(simulate_expression())  # 22
```

---

## 执行流程

### 程序执行流程

```python
"""
Python程序执行的完整流程
"""

# 1. 模块初始化
"""
if __name__ == "__main__":
    main()

执行流程:
1. 设置__name__ = "__main__"
2. 执行模块顶层代码
3. 遇到if __name__ == "__main__"时进入
"""

# 2. 导入机制
import sys

print("Import hooks:")
print(sys.meta_path)  # 导入钩子

# 导入流程:
"""
1. 检查sys.modules (已导入模块)
2. 查找模块 (sys.path)
3. 加载模块
4. 执行模块代码
5. 缓存到sys.modules
"""

# 3. 查看模块代码
import json
import inspect

print(inspect.getsourcefile(json))  # 模块文件路径
```

### 代码对象详解

```python
"""
代码对象 (code object) 的属性
"""

def example(x, y=10):
    """示例函数"""
    z = x + y
    return z

code = example.__code__

print("Code object attributes:")
print(f"co_argcount: {code.co_argcount}")      # 参数数量: 2
print(f"co_kwonlyargcount: {code.co_kwonlyargcount}")  # 仅关键字参数: 0
print(f"co_nlocals: {code.co_nlocals}")        # 局部变量数: 3
print(f"co_stacksize: {code.co_stacksize}")    # 栈大小: 2
print(f"co_flags: {code.co_flags}")            # 标志位
print(f"co_consts: {code.co_consts}")          # 常量: (None, 10)
print(f"co_names: {code.co_names}")            # 名称: ()
print(f"co_varnames: {code.co_varnames}")      # 变量名: ('x', 'y', 'z')
print(f"co_filename: {code.co_filename}")      # 文件名
print(f"co_name: {code.co_name}")              # 函数名: example
print(f"co_firstlineno: {code.co_firstlineno}")# 首行行号
```

---

## 异常处理机制

### 异常处理流程

```python
"""
异常处理的执行流程
"""

def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    else:
        print("Success!")
        return result
    finally:
        print("Cleanup")

# 执行流程:
"""
正常情况:
1. 执行try块
2. 执行else块 (可选)
3. 执行finally块

异常情况:
1. 执行try块
2. 发生异常,跳转到对应except块
3. 执行finally块
"""

# 查看异常处理的字节码
import dis
dis.dis(divide)
```

### 异常传播

```python
"""
异常在调用栈中的传播
"""

def level3():
    """第3层"""
    raise ValueError("Error in level 3")

def level2():
    """第2层"""
    level3()

def level1():
    """第1层"""
    try:
        level2()
    except ValueError as e:
        print(f"Caught in level1: {e}")
        import traceback
        traceback.print_exc()

level1()

# 异常传播路径:
"""
level3 (raise)
  ↓
level2 (未捕获,继续传播)
  ↓
level1 (捕获)
"""

# ============================================
# 查看异常链
# ============================================

try:
    try:
        1 / 0
    except ZeroDivisionError as e:
        raise ValueError("New error") from e
except ValueError as e:
    print(f"Exception: {e}")
    print(f"Cause: {e.__cause__}")      # 显式链接
    print(f"Context: {e.__context__}")  # 隐式链接
```

---

## 并发模型

### GIL (全局解释器锁)

```python
"""
GIL限制了多线程并行执行
"""

import threading
import time

counter = 0

def increment():
    """增加计数器"""
    global counter
    for _ in range(1000000):
        counter += 1

# 单线程
start = time.time()
increment()
print(f"Single thread: {time.time() - start:.2f}s")
print(f"Counter: {counter}")

# 多线程 (受GIL限制)
counter = 0
threads = []

start = time.time()
for _ in range(2):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Multi thread: {time.time() - start:.2f}s")
print(f"Counter: {counter}")

# 多线程不会更快,因为GIL!

# ============================================
# GIL释放时机
# ============================================

"""
GIL在以下情况会释放:
1. I/O操作 (read, write, recv, send)
2. time.sleep()
3. 每执行一定数量的字节码指令
4. C扩展显式释放
"""

# 查看GIL切换间隔
import sys
print(sys.getswitchinterval())  # 默认0.005秒
```

### Free-Threaded模式 (Python 3.13+)

```python
"""
Python 3.13+支持无GIL模式
"""

# 编译时启用: --disable-gil
# 运行时检查:
import sys

if hasattr(sys, 'is_gil_enabled'):
    if not sys.is_gil_enabled():
        print("Free-threaded mode enabled!")

        # 在此模式下,多线程可真正并行
        # 性能显著提升!

# 使用方式:
"""
# 编译
./configure --disable-gil
make

# 运行
python -X gil=0 script.py
"""
```

---

## 📚 核心要点

### 执行流程

- ✅ **编译**: 源代码 → 字节码
- ✅ **执行**: 字节码 → 虚拟机
- ✅ **缓存**: .pyc文件加速加载
- ✅ **栈式VM**: 基于栈的指令执行

### 异常处理

- ✅ **try/except**: 捕获异常
- ✅ **finally**: 总是执行
- ✅ **异常链**: 保留异常上下文
- ✅ **传播机制**: 沿调用栈向上

### 并发模型

- ✅ **GIL**: 限制多线程并行
- ✅ **I/O密集**: 异步更高效
- ✅ **CPU密集**: 多进程更高效
- ✅ **Free-Threaded**: 未来的并行

---

**深入理解执行模型，掌控程序运行！** ⚙️✨

**相关文档**:

- [01-data-model.md](01-data-model.md) - 数据模型
- [03-memory-model.md](03-memory-model.md) - 内存模型
- [05-scope-namespace.md](05-scope-namespace.md) - 作用域

**最后更新**: 2025年10月28日
