# PEP 667: locals() 语义定义

> Python 3.13 新特性 - locals() 的确定性行为

---

## 概述

**PEP 667** 为 `locals()` 内置函数定义了明确、可预测的行为语义，特别是在修改返回的映射时的行为。

**发布版本**: Python 3.13+
**PEP链接**: [PEP 667](https://peps.python.org/pep-0667/)

**核心改进**:

- ✅ 明确的 `locals()` 修改语义
- ✅ 改进的调试器可靠性
- ✅ 并发代码中更可靠的变量更新
- ✅ 一致的跨作用域行为

---

## 背景问题

### Python 3.12 及之前的问题

```python
# 问题 1: 行为不一致
def example():
    x = 1
    locals_dict = locals()
    locals_dict['x'] = 2
    print(x)  # 可能输出 1 或 2，取决于优化级别！
    print(locals_dict['x'])  # 2

# 问题 2: 类作用域 vs 函数作用域
class MyClass:
    x = 1
    locals_dict = locals()
    locals_dict['x'] = 2
    # 类作用域中可能工作不同

# 问题 3: 调试器可靠性
def debug_me():
    x = 1
    # 调试器尝试修改 x
    locals()['x'] = 2  # 不一定生效！
    return x  # 可能仍返回 1
```

### 优化导致的不确定性

```python
# 未优化（-O0）：locals() 返回实际的局部变量字典
# 修改可能反映到局部变量

def unoptimized():
    x = 1
    loc = locals()
    loc['x'] = 2
    print(x)  # 2（可能）

# 优化（-O2）：locals() 返回快照
# 修改不影响实际局部变量

def optimized():
    x = 1
    loc = locals()
    loc['x'] = 2
    print(x)  # 1
```

---

## Python 3.13 的新语义

### 核心规则

```python
"""
Python 3.13+ locals() 语义规则：

1. locals() 返回一个映射（dict-like）
2. 在函数作用域中：
   - 返回写入时复制的快照
   - 修改不直接影响局部变量
   - 但可以通过特定方式更新

3. 在模块和类作用域中：
   - 返回可写的局部命名空间
   - 修改会直接影响命名空间

4. 调试和框架钩子有特殊处理
"""
```

### 函数作用域行为

```python
def function_scope_demo():
    """
    函数作用域中的 locals() 行为
    """
    x = 1
    y = 2

    # 获取局部变量快照
    local_vars = locals()

    # 修改返回的映射
    local_vars['x'] = 100
    local_vars['z'] = 3  # 添加新键

    # Python 3.13+ 行为：
    print(f"x = {x}")  # x = 1（原始值，不受修改影响）
    print(f"local_vars['x'] = {local_vars['x']}")  # 100
    print(f"'z' in locals(): {'z' in locals()}")  # False（新变量未创建）

    # locals() 每次调用返回新的快照
    locals2 = locals()
    print(f"locals() is locals2: {locals() is locals2}")  # False
    print(f"'z' in locals2: {'z' in locals2}")  # False

function_scope_demo()
```

### 模块作用域行为

```python
# 模块级代码
"""
模块作用域中的 locals() 等同于 globals()
"""

x = 1

# 在模块作用域中
module_locals = locals()
module_locals['y'] = 2  # 创建模块级变量 y

print(f"y = {y}")  # y = 2（模块作用域中修改有效）
print(f"globals()['y'] = {globals()['y']}")  # 2

# locals() 和 globals() 在模块作用域中是同一个对象
print(f"locals() is globals(): {locals() is globals()}")  # True
```

### 类作用域行为

```python
class MyClass:
    """
    类作用域中的 locals() 行为
    """
    x = 1

    # 在类体中，locals() 是类的命名空间
    class_namespace = locals()
    class_namespace['y'] = 2  # 创建类属性

    # 类属性被创建
    # print(y)  # NameError，类体执行时 y 还未绑定

# 类创建后，y 是类属性
print(f"MyClass.y = {MyClass.y}")  # 2
print(f"MyClass.x = {MyClass.x}")  # 1
```

---

## 实际应用

### 应用 1: 安全的局部变量检查

```python
def safe_locals_inspection():
    """
    安全地检查局部变量而不影响它们
    """
    user_id = 12345
    user_name = "Alice"
    is_active = True

    # 获取当前局部变量快照
    current_locals = locals()

    # 安全检查 - 不影响实际变量
    if 'user_id' in current_locals:
        print(f"User ID: {current_locals['user_id']}")

    # 修改快照不会修改变量
    current_locals['user_id'] = 99999
    print(f"Actual user_id: {user_id}")  # 仍然是 12345

    # 可以安全地遍历
    for name, value in current_locals.items():
        if not name.startswith('_'):
            print(f"  {name} = {value}")

safe_locals_inspection()
```

### 应用 2: 调试器实现

```python
"""
改进的调试器变量检查 - Python 3.13+
"""
import sys
import inspect

class ImprovedDebugger:
    """利用 PEP 667 的改进调试器"""

    @staticmethod
    def get_frame_locals(frame) -> dict:
        """
        获取帧的局部变量

        Python 3.13+ 提供更可靠的访问
        """
        if sys.version_info >= (3, 13):
            # Python 3.13+：frame.f_locals 行为改进
            return frame.f_locals.copy()
        else:
            # 旧版本：需要特殊处理
            return frame.f_locals.copy()

    @staticmethod
    def set_frame_local(frame, name: str, value) -> bool:
        """
        在帧中设置局部变量值

        Python 3.13+ 更可靠
        """
        if sys.version_info >= (3, 13):
            # Python 3.13+：修改更可靠
            frame.f_locals[name] = value
            # 需要调用 f_locals 来触发更新
            _ = frame.f_locals
            return True
        else:
            # 旧版本：修改可能不可靠
            try:
                frame.f_locals[name] = value
                return True
            except Exception:
                return False

    def print_frame_info(self, frame):
        """打印帧信息"""
        print(f"Frame: {frame.f_code.co_name}")
        print(f"File: {frame.f_code.co_filename}")
        print(f"Line: {frame.f_lineno}")
        print("Locals:")

        for name, value in self.get_frame_locals(frame).items():
            value_str = repr(value)[:50]
            print(f"  {name} = {value_str}")

# 使用示例
def debug_target():
    x = 10
    y = 20

    # 获取当前帧
    frame = inspect.currentframe()
    debugger = ImprovedDebugger()

    print("Before modification:")
    debugger.print_frame_info(frame)

    # 尝试修改变量
    debugger.set_frame_local(frame, 'x', 100)

    print("\nAfter setting x = 100:")
    debugger.print_frame_info(frame)
    print(f"Actual x value: {x}")  # 注意：实际值可能仍取决于上下文

    # 清理
    del frame

debug_target()
```

### 应用 3: 代码分析和检查

```python
"""
代码分析工具 - 利用改进的 locals() 语义
"""
import ast
import inspect
from typing import Any, Dict, Set

class VariableAnalyzer:
    """变量使用分析器"""

    def analyze_function(self, func) -> Dict[str, Any]:
        """
        分析函数的变量使用情况
        """
        # 获取源代码
        source = inspect.getsource(func)
        tree = ast.parse(source)

        # 查找函数定义
        func_def = tree.body[0]

        analysis = {
            'parameters': [],
            'local_variables': [],
            'used_names': set(),
            'modified_names': set()
        }

        # 收集参数
        for arg in func_def.args.args:
            analysis['parameters'].append(arg.arg)

        # 遍历 AST 收集变量
        for node in ast.walk(func_def):
            if isinstance(node, ast.Name):
                analysis['used_names'].add(node.id)
            elif isinstance(node, ast.NameConstant):
                pass
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        analysis['modified_names'].add(target.id)
                        if target.id not in analysis['parameters']:
                            analysis['local_variables'].append(target.id)

        return analysis

    def compare_with_runtime(self, func, *args, **kwargs):
        """
        对比静态分析和运行时变量
        """
        # 静态分析
        static_info = self.analyze_function(func)

        # 运行时分析
        frame = None

        def capture_frame():
            nonlocal frame
            frame = inspect.currentframe()
            return 42

        # 注入帧捕获
        original_source = inspect.getsource(func)

        # 调用函数
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = f"Error: {e}"

        # 获取函数完成后的 locals()（如果可能）
        # 注意：函数执行完毕后帧已释放

        return {
            'static': static_info,
            'result': result
        }

# 使用示例
def example_function(a, b):
    """示例函数用于分析"""
    x = a + b
    y = x * 2
    z = y - a
    return z

analyzer = VariableAnalyzer()
analysis = analyzer.analyze_function(example_function)

print("Static Analysis Results:")
print(f"Parameters: {analysis['parameters']}")
print(f"Local Variables: {analysis['local_variables']}")
print(f"Modified Names: {analysis['modified_names']}")
```

---

## 并发场景

### 线程安全考虑

```python
"""
Python 3.13+ 中 locals() 的并发行为
"""
import threading
import time

def concurrent_locals_demo():
    """
    演示并发代码中的 locals() 行为
    """
    thread_local_data = {}

    def worker(thread_id: int):
        # 每个线程有自己的局部变量
        local_var = f"thread_{thread_id}_data"
        counter = 0

        for i in range(5):
            counter += 1

            # 获取当前 locals()
            current_locals = locals()

            # 记录到线程本地存储
            thread_local_data[thread_id] = {
                'local_var': local_var,
                'counter': counter,
                'iteration': i
            }

            time.sleep(0.01)

    # 启动多个线程
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    # 等待所有线程
    for t in threads:
        t.join()

    # 检查数据
    print("Thread-local data captured:")
    for thread_id, data in thread_local_data.items():
        print(f"  Thread {thread_id}: {data}")

concurrent_locals_demo()
```

### 异步代码中的 locals()

```python
"""
异步代码中的 locals() 行为
"""
import asyncio

async def async_locals_demo():
    """
    异步函数中的 locals() 行为
    """
    async_var = "I am async"
    counter = 0

    async def inner_task(task_id: int):
        nonlocal counter

        task_local = f"task_{task_id}"
        counter += 1

        # 获取 locals()
        current_locals = locals()

        print(f"Task {task_id} locals:")
        for name, value in current_locals.items():
            print(f"  {name} = {value}")

        await asyncio.sleep(0.01)

        # 修改 locals() 不影响实际变量
        current_locals['task_local'] = 'modified'
        print(f"  After modification: task_local = {task_local}")

    # 运行多个任务
    await asyncio.gather(
        inner_task(1),
        inner_task(2),
        inner_task(3)
    )

    print(f"\nFinal counter: {counter}")

# 运行
asyncio.run(async_locals_demo())
```

---

## 迁移指南

### 从旧代码迁移

```python
"""
迁移指南：更新依赖 locals() 修改行为的代码
"""

# ===== 旧模式（Python < 3.13）=====

def old_pattern_modify_locals():
    """
    旧代码：依赖 locals() 修改影响实际变量
    这种代码在 Python 3.13+ 中可能不工作
    """
    x = 1
    locals()['x'] = 2  # 不确定是否生效
    return x

# ===== 新模式（Python 3.13+）=====

def new_pattern_explicit_vars():
    """
    新代码：显式修改变量
    """
    x = 1
    x = 2  # 明确赋值
    return x

def new_pattern_dict_storage():
    """
    新代码：使用字典存储动态数据
    """
    context = {'x': 1}
    context['x'] = 2  # 明确修改字典
    return context['x']

def new_pattern_nonlocal():
    """
    新代码：使用 nonlocal 修改外层变量
    """
    x = 1

    def inner():
        nonlocal x
        x = 2

    inner()
    return x

# ===== 框架/调试器迁移 =====

class OldDebugger:
    """旧调试器实现"""

    def set_variable_old(self, frame, name: str, value):
        """旧的变量设置方法 - 可能不可靠"""
        frame.f_locals[name] = value
        # 在 Python 3.13+ 中需要额外处理

class NewDebugger:
    """新调试器实现 - Python 3.13+"""

    def set_variable_new(self, frame, name: str, value):
        """新的变量设置方法 - 更可靠"""
        frame.f_locals[name] = value

        # Python 3.13+：触发更新
        if hasattr(frame, 'f_locals'):
            # 重新访问 f_locals 触发同步
            _ = frame.f_locals

        return True
```

---

## 性能考虑

```python
"""
locals() 性能特征
"""
import time

def benchmark_locals():
    """测试 locals() 性能"""
    x = 1
    y = 2
    z = 3

    iterations = 100000

    # 测试 1: 调用 locals()
    start = time.perf_counter()
    for _ in range(iterations):
        _ = locals()
    locals_time = time.perf_counter() - start

    # 测试 2: 直接访问变量
    start = time.perf_counter()
    for _ in range(iterations):
        _ = (x, y, z)
    direct_time = time.perf_counter() - start

    print(f"locals() calls: {locals_time:.3f}s")
    print(f"Direct access:  {direct_time:.3f}s")
    print(f"Overhead: {locals_time/direct_time:.1f}x")

benchmark_locals()
```

---

## 兼容性

| Python 版本 | locals() 行为 |
|-------------|---------------|
| 3.13+ | ✅ 确定性语义，写入时复制 |
| 3.12 | ⚠️ 行为取决于优化级别 |
| <3.12 | ⚠️ 行为不一致 |

### 检测 Python 版本

```python
import sys

def check_locals_semantics():
    """检查 locals() 语义版本"""
    if sys.version_info >= (3, 13):
        return "PEP 667 - Deterministic semantics"
    else:
        return "Legacy - Implementation dependent"

print(f"locals() semantics: {check_locals_semantics()}")
```

---

## 最佳实践

### ✅ 应该做的

1. **不要依赖 locals() 修改行为**

   ```python
   # 不好
   locals()['x'] = new_value

   # 好
   x = new_value
   ```

2. **使用 locals() 只读检查**

   ```python
   # 好：只读使用
   def debug():
       current_vars = locals()
       print(f"Variables: {current_vars}")
   ```

3. **调试器使用 frame.f_locals**

   ```python
   # 调试器应该使用 frame.f_locals
   frame.f_locals['var'] = value
   _ = frame.f_locals  # 触发更新
   ```

### ❌ 不应该做的

1. **不要在生产代码中依赖 locals() 修改**
2. **不要假设 locals() 返回的是可变引用**
3. **不要频繁调用 locals()（性能开销）**

---

## 延伸阅读

- [PEP 667 - Consistent views of locals()
](https://peps.python.org/pep-0667/)
- [Python 3.13 Data Model](https://docs.python.org/3.13/reference/datamodel.html)
- [inspect 模块文档](https://docs.python.org/3/library/inspect.html)

---

**理解 locals() 语义，编写更可靠的 Python 代码！** 🔍📊
