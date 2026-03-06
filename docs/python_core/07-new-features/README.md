# Python 3.12/3.13 新特性完全指南

> 2025 最新 Python 版本特性详解

---

## 📚 目录

- [Python 3.12/3.13 新特性完全指南](#python-312313-新特性完全指南)
  - [📚 目录](#-目录)
  - [1. Python 3.12 核心特性](#1-python-312-核心特性)
    - [PEP 695: 类型参数语法](#pep-695-类型参数语法)
    - [PEP 698: @override 装饰器](#pep-698-override-装饰器)
    - [PEP 701: f-string 增强](#pep-701-f-string-增强)
  - [2. Python 3.13 革命性特性](#2-python-313-革命性特性)
    - [PEP 703: Free-Threaded 模式](#pep-703-free-threaded-模式)
    - [PEP 744: JIT 编译器](#pep-744-jit-编译器)
    - [PEP 667: locals() 语义](#pep-667-locals-语义)
  - [3. Python 3.13 类型系统](#3-python-313-类型系统)
    - [PEP 696: 类型参数默认值](#pep-696-类型参数默认值)
    - [PEP 702: @deprecated](#pep-702-deprecated)
    - [PEP 705: ReadOnly](#pep-705-readonly)
    - [PEP 742: TypeIs](#pep-742-typeis)
  - [4. 性能改进](#4-性能改进)
    - [启动时间](#启动时间)
    - [内存使用](#内存使用)
    - [执行速度](#执行速度)
  - [5. 迁移指南](#5-迁移指南)
    - [升级到 Python 3.12](#升级到-python-312)
    - [尝试 Python 3.13](#尝试-python-313)
    - [版本选择建议](#版本选择建议)
  - [📖 详细文档索引](#-详细文档索引)
    - [Python 3.12 特性](#python-312-特性)
    - [Python 3.13 特性](#python-313-特性)

---

## 1. Python 3.12 核心特性

### PEP 695: 类型参数语法

```python
# 旧语法 (Python < 3.12)
from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []

# 新语法 (Python 3.12+) ✨
class Stack[T]:
    def __init__(self) -> None:
        self.items: list[T] = []

# 泛型函数
def first[T](items: list[T]) -> T:
    return items[0]
```

### PEP 698: @override 装饰器

```python
from typing import override

class Base:
    def process(self) -> None: pass

class Derived(Base):
    @override
    def process(self) -> None:  # 正确覆盖
        pass

    @override
    def typo(self) -> None:  # 错误！父类没有此方法
        pass
```

### PEP 701: f-string 增强

```python
# Python 3.12+ 支持在 f-string 中使用相同引号
songs = ["Take me back to Eden", "Alkaline"]
result = f"Playing: {', '.join(songs)}"

# 支持多行
message = f"""
User: {user.name}
Status: {user.status}
"""

# 支持嵌套
print(f"{f'{data['name']} is {data['age']} years old'}")
```

---

## 2. Python 3.13 革命性特性

### PEP 703: Free-Threaded 模式

**重大突破**：移除全局解释器锁（GIL）！

```python
# 启用 Free-Threaded 模式
# python3.13t (t = threaded)

import threading
import time

def cpu_intensive_task(n: int) -> int:
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# 真正的并行执行！
threads = []
for i in range(4):
    t = threading.Thread(target=cpu_intensive_task, args=(10000000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# 性能提升: 接近 4x (4 核 CPU)
```

**详细文档**:

- [Free-Threaded 完全指南](../10-concurrency/01-free-threaded-guide.md) ⭐
- [Python 3.13 新特性概述](03-free-threaded.md)

### PEP 744: JIT 编译器

```bash
# 启用 JIT 编译器
PYTHON_JIT=1 python3.13 script.py

# 性能提升: 5-20%
```

```python
import sys

# 检查 JIT 是否启用
def is_jit_enabled() -> bool:
    return hasattr(sys, 'flags') and getattr(sys.flags, 'jit', False)
```

**详细文档**:

- [JIT 编译器深度解析](04-jit-compiler-deep-dive.md) ⭐

### PEP 667: locals() 语义

```python
# Python 3.13+：locals() 行为确定
def example():
    x = 1
    local_vars = locals()
    local_vars['x'] = 2  # 不影响实际变量 x
    print(x)  # 1
    print(local_vars['x'])  # 2
```

**详细文档**:

- [locals() 语义定义](../01-language-core/06-pep667-locals-semantics.md) ⭐

---

## 3. Python 3.13 类型系统

### PEP 696: 类型参数默认值

```python
from typing import TypeVar

T = TypeVar("T", default=str)

class Container[T = str]:
    def __init__(self) -> None:
        self.items: list[T] = []

container = Container()  # Container[str]
```

**详细文档**: [PEP 696 类型参数默认值](../03-type-system/08-pep696-type-defaults.md)

### PEP 702: @deprecated

```python
import warnings

@warnings.deprecated("Use new_function() instead.")
def old_function():
    pass

old_function()  # DeprecationWarning
```

**详细文档**: [PEP 702 @deprecated](../03-type-system/09-pep702-deprecated.md)

### PEP 705: ReadOnly

```python
from typing import TypedDict, ReadOnly

class Config(TypedDict):
    debug: bool
    version: ReadOnly[str]  # 只读
```

**详细文档**: [PEP 705 ReadOnly](../03-type-system/10-pep705-readonly.md)

### PEP 742: TypeIs

```python
from typing import TypeIs

def is_string(value: object) -> TypeIs[str]:
    return isinstance(value, str)
```

**详细文档**: [PEP 742 TypeIs](../03-type-system/11-pep742-typeis.md)

---

## 4. 性能改进

### 启动时间

```
Python 3.11: 24ms
Python 3.12: 18ms (-25%)  ✨
Python 3.13: 15ms (-38%)  ✨
```

### 内存使用

```
Python 3.11: 128 MB
Python 3.12: 105 MB (-18%)  ✨
Python 3.13: 95 MB  (-26%)  ✨
```

### 执行速度

```
Python 3.11: 1.00x (baseline)
Python 3.12: 1.11x faster  (+11%)  ✨
Python 3.13: 1.18x faster  (+18%)  ✨
Python 3.13t (no GIL): 2.5-3.5x faster (多核)  🚀
Python 3.13 + JIT: 1.25x faster  (+25%)  🚀
```

---

## 5. 迁移指南

### 升级到 Python 3.12

```bash
# 1. 安装 Python 3.12
uv python install 3.12

# 2. 更新 pyproject.toml
[project]
requires-python = ">=3.12"

# 3. 使用新语法
type UserId = int  # Python 3.12+
```

### 尝试 Python 3.13

```bash
# 1. 安装 Python 3.13
uv python install 3.13

# 2. 尝试 Free-Threaded 模式
uv python install 3.13t

# 3. 测试性能
PYTHON_JIT=1 python3.13 benchmark.py
```

### 版本选择建议

| 场景 | 推荐版本 |
|------|----------|
| 生产环境 | Python 3.12 ✅ |
| 性能敏感 | Python 3.13 + JIT |
| 多核并行 | Python 3.13t |
| 前沿特性 | Python 3.13 |

---

## 📖 详细文档索引

### Python 3.12 特性

- [类型参数语法](02-python-3.12.md)
- [@override 装饰器](02-python-3.12.md#override)
- [f-string 增强](02-python-3.12.md#f-string)

### Python 3.13 特性

- [Free-Threaded 模式](03-free-threaded.md) / [完整指南](../10-concurrency/01-free-threaded-guide.md)
- [JIT 编译器](04-jit-compiler-deep-dive.md)
- [locals() 语义](../01-language-core/06-pep667-locals-semantics.md)
- [类型参数默认值](../03-type-system/08-pep696-type-defaults.md)
- [@deprecated](../03-type-system/09-pep702-deprecated.md)
- [ReadOnly](../03-type-system/10-pep705-readonly.md)
- [TypeIs](../03-type-system/11-pep742-typeis.md)
- [标准库更新](../08-standard-library-updates/README.md)

---

**拥抱 Python 的未来，享受更快的性能！** 🚀✨

**最后更新**: 2025-03-07
**覆盖版本**: Python 3.12, 3.13
**完成度**: ⭐⭐⭐⭐⭐
