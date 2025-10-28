# Python 导入规范与组织

**Import完全指南**

---

## 📋 目录

- [导入基础](#导入基础)
- [导入顺序](#导入顺序)
- [导入风格](#导入风格)
- [避免的模式](#避免的模式)
- [自动化工具](#自动化工具)

---

## 导入基础

### 导入语法

```python
"""
Python导入语法
"""

# 1. 标准导入
import os
import sys

# 2. from导入
from pathlib import Path
from typing import List, Dict

# 3. 别名导入
import numpy as np
import pandas as pd

# 4. 相对导入
from . import sibling_module
from .. import parent_module
from ..sibling_package import module

# 5. 导入所有 (不推荐)
from module import *
```

### 导入规则

```python
"""
PEP 8导入规则
"""

# ✅ 每行一个导入
import os
import sys

# ❌ 不要多个导入在一行
import os, sys  # 错误

# ✅ from import可以在一行
from subprocess import Popen, PIPE

# ✅ 或者分行
from subprocess import (
    Popen,
    PIPE,
    STDOUT,
)

# ✅ 导入放在文件顶部
"""Module docstring"""

import os  # 在docstring之后
import sys

# 代码...

# ❌ 不要在文件中间导入
def function():
    import os  # 错误,应该在顶部
    pass

# 例外: 可选依赖或避免循环导入
def optional_feature():
    try:
        import optional_package
    except ImportError:
        print("Optional package not available")
```

---

## 导入顺序

### 标准顺序

```python
"""
导入顺序: 标准库 -> 第三方 -> 本地
"""

# 1. 标准库导入
import os
import sys
from pathlib import Path
from typing import List, Dict

# 2. 第三方库导入
import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI
from pydantic import BaseModel

# 3. 本地应用/库导入
from my_package import module1
from my_package.subpackage import module2
from . import sibling
from .. import parent

# 每组之间空一行
# 每组内按字母顺序排列
```

### isort配置

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

# 导入分组
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
known_first_party = ["my_package"]
known_third_party = ["numpy", "pandas", "requests"]

# 跳过文件
skip_gitignore = true
skip = ["migrations", "build", "dist"]
```

---

## 导入风格

### 绝对导入 vs 相对导入

```python
"""
绝对导入 vs 相对导入
"""

# 项目结构:
# my_package/
#   __init__.py
#   module_a.py
#   module_b.py
#   subpackage/
#     __init__.py
#     module_c.py

# ✅ 绝对导入 (推荐)
# 在module_c.py中
from my_package import module_a
from my_package.module_b import function

# ✅ 显式相对导入 (包内使用)
# 在module_c.py中
from .. import module_a  # 上一级
from ..module_b import function  # 上一级的module_b
from . import module_d  # 同级

# ❌ 隐式相对导入 (Python 3已移除)
import module_a  # 错误

# 何时使用相对导入:
# 1. 包内模块间导入
# 2. 避免包名改变的影响
# 3. 减少导入路径长度

# 何时使用绝对导入:
# 1. 从其他包导入
# 2. 顶层脚本
# 3. 更清晰的依赖关系
```

### 别名约定

```python
"""
常用别名约定
"""

# ✅ 常用别名
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns

# ✅ 避免命名冲突
from my_package import User as MyUser
from third_party import User as ThirdPartyUser

# ✅ 简化长名称
from my_package.very_long_module_name import SomeClass as SC

# ❌ 避免无意义别名
import requests as r  # 不要随意缩写
import os as o  # 不要单字母

# ❌ 避免混淆别名
import numpy as pandas  # 完全错误!
```

### 选择性导入

```python
"""
选择性导入 vs 模块导入
"""

# ✅ 导入模块 (推荐)
import os

os.path.join("a", "b")
os.environ["PATH"]

# ✅ 导入特定对象 (频繁使用时)
from pathlib import Path

path = Path("/home/user")

# ❌ 不要过度导入
from os import (
    path, environ, getcwd, listdir, mkdir, rmdir, remove,
    rename, stat, chmod, chown, ...  # 太多了
)

# 推荐: 导入模块
import os

# ❌ 不要使用通配符
from os import *  # 污染命名空间

# 例外: __init__.py中重新导出
# my_package/__init__.py
from .module_a import ClassA
from .module_b import ClassB

__all__ = ["ClassA", "ClassB"]

# 用户可以:
from my_package import *  # 只导入__all__中的
```

---

## 避免的模式

### 循环导入

```python
"""
避免循环导入
"""

# ❌ 循环导入示例
# module_a.py
from module_b import ClassB

class ClassA:
    def use_b(self):
        return ClassB()

# module_b.py
from module_a import ClassA  # 循环!

class ClassB:
    def use_a(self):
        return ClassA()

# ✅ 解决方案1: 重构,消除循环依赖
# module_a.py
class ClassA:
    pass

# module_b.py
from module_a import ClassA

class ClassB:
    def use_a(self):
        return ClassA()

# ✅ 解决方案2: 延迟导入
# module_a.py
class ClassA:
    def use_b(self):
        from module_b import ClassB  # 函数内导入
        return ClassB()

# ✅ 解决方案3: 类型注解使用字符串
# module_a.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module_b import ClassB

class ClassA:
    def use_b(self) -> "ClassB":  # 字符串类型
        from module_b import ClassB
        return ClassB()
```

### 通配符导入

```python
"""
避免通配符导入
"""

# ❌ 通配符导入问题
from os import *

# 问题:
# 1. 不知道导入了什么
# 2. 可能覆盖现有名称
# 3. 工具无法追踪
# 4. 影响性能

# ✅ 明确导入
from os import path, environ, getcwd

# 或
import os

# 例外: __init__.py重新导出
# my_package/__init__.py
from .core import *  # 可以接受

# 但要定义__all__
__all__ = ["ClassA", "ClassB", "function_c"]
```

### 导入顺序混乱

```python
"""
导入顺序混乱
"""

# ❌ 混乱的导入
from my_package import module1
import sys
from third_party import something
import os
from . import sibling

# ✅ 有序的导入
# 标准库
import os
import sys

# 第三方
from third_party import something

# 本地
from . import sibling
from my_package import module1
```

---

## 自动化工具

### isort自动排序

```bash
# 安装isort
uv add --dev isort

# 排序单个文件
isort script.py

# 排序目录
isort src/

# 检查不修改
isort --check-only src/

# 查看diff
isort --diff src/

# 与black兼容
isort --profile black src/
```

### 配置示例

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true

# 导入分组
sections = [
    "FUTURE",
    "STDLIB",
    "THIRDPARTY",
    "FIRSTPARTY",
    "LOCALFOLDER"
]

# 已知包分类
known_first_party = ["my_package"]
known_third_party = [
    "numpy",
    "pandas",
    "requests",
    "fastapi",
]

# 特殊导入处理
force_single_line = false
force_sort_within_sections = false

# 跳过文件
skip_gitignore = true
extend_skip = [".venv", "build", "dist"]

# 每组内排序
force_alphabetical_sort_within_sections = true
```

### ruff导入检查

```bash
# ruff也支持导入检查和自动修复
ruff check --select I src/  # 只检查导入
ruff check --fix --select I src/  # 自动修复导入
```

```toml
# pyproject.toml
[tool.ruff]
select = ["I"]  # 启用isort规则

[tool.ruff.isort]
known-first-party = ["my_package"]
```

### pre-commit集成

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]
  
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --select, I]
```

---

## 📚 核心要点

### 导入基础

- ✅ **每行一个**: import os
- ✅ **文件顶部**: 在docstring之后
- ✅ **分组**: 标准库/第三方/本地
- ✅ **排序**: 每组内字母顺序

### 导入顺序

1. **标准库**: os, sys, pathlib
2. **第三方**: numpy, pandas, requests
3. **本地**: my_package, 相对导入
4. **空行分隔**: 每组之间

### 导入风格

- ✅ **绝对导入**: 优先使用
- ✅ **相对导入**: 包内使用
- ✅ **别名**: np, pd等约定
- ✅ **选择性**: from import特定对象

### 避免

- ❌ 通配符导入: from x import *
- ❌ 循环导入: 重构或延迟导入
- ❌ 多个导入一行: import os, sys
- ❌ 文件中间导入: 应在顶部

### 自动化

- ✅ **isort**: 自动排序
- ✅ **ruff**: 快速检查
- ✅ **pre-commit**: Git hooks
- ✅ **CI/CD**: 自动检查

### 最佳实践

- ✅ 使用isort自动化
- ✅ 配置pyproject.toml
- ✅ 避免循环导入
- ✅ TYPE_CHECKING优化
- ✅ __all__控制导出

---

**规范的导入让代码更清晰！** 📦✨

**相关文档**:
- [01-pep8.md](01-pep8.md) - PEP 8代码风格
- [02-naming.md](02-naming.md) - 命名约定

**最后更新**: 2025年10月28日

