# Python mypy 静态类型检查

**mypy完全使用指南**

---

## 📋 目录

- [mypy简介](#mypy简介)
- [mypy配置](#mypy配置)
- [类型检查严格度](#类型检查严格度)
- [常见错误处理](#常见错误处理)
- [高级特性](#高级特性)

---

## mypy简介

### 什么是mypy

```python
"""
mypy: Python静态类型检查器
"""

# 安装
# uv add --dev mypy

# 基础使用
# mypy script.py
# mypy src/

# mypy的作用:
# 1. 在运行前发现类型错误
# 2. 提供更好的IDE支持
# 3. 作为文档
# 4. 重构支持

# 示例代码
def greet(name: str) -> str:
    return f"Hello, {name}"

# 类型错误
result = greet(123)  # mypy会报错
# error: Argument 1 to "greet" has incompatible type "int"; expected "str"
```

### 渐进式类型

```python
"""
渐进式类型系统
"""

# 1. 无类型注解 - mypy跳过
def add(x, y):
    return x + y

# 2. 部分类型注解
def multiply(x: int, y):  # y没有注解
    return x * y

# 3. 完整类型注解
def divide(x: int, y: int) -> float:
    return x / y

# 可以逐步添加类型注解
# mypy支持渐进式迁移
```

---

## mypy配置

### pyproject.toml配置

```toml
# pyproject.toml
[tool.mypy]
# Python版本
python_version = "3.12"

# 严格模式
strict = true

# 或者手动配置各项
disallow_untyped_defs = true
disallow_any_generics = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_return_any = true
warn_unreachable = true
check_untyped_defs = true
no_implicit_reexport = true

# 排除目录
exclude = [
    "build/",
    "dist/",
    "venv/",
]

# 第三方库存根
[[tool.mypy.overrides]]
module = "pandas.*"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "matplotlib.*"
ignore_missing_imports = true
```

### mypy.ini配置

```ini
# mypy.ini
[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

[mypy-tests.*]
ignore_errors = True

[mypy-pandas.*]
ignore_missing_imports = True
```

---

## 类型检查严格度

### 严格度级别

```python
"""
mypy严格度配置
"""

# 1. 默认模式 - 最宽松
# mypy script.py

# 2. 中等严格
# mypy --warn-return-any --warn-unused-ignores script.py

# 3. 严格模式
# mypy --strict script.py

# 4. 自定义严格度
# pyproject.toml中配置

# 严格模式包括:
# - disallow_untyped_calls
# - disallow_untyped_defs
# - disallow_incomplete_defs
# - check_untyped_defs
# - disallow_any_generics
# - disallow_subclassing_any
# - disallow_untyped_decorators
# - warn_redundant_casts
# - warn_unused_ignores
# - warn_return_any
# - warn_unreachable
# - no_implicit_reexport
```

### 逐步迁移

```python
"""
逐步启用严格类型检查
"""

# 步骤1: 从宽松开始
# mypy --ignore-missing-imports src/

# 步骤2: 逐个模块添加类型
# 在文件顶部添加
# mypy: disallow-untyped-defs

def greet(name: str) -> str:
    return f"Hello, {name}"

# 步骤3: 启用更多检查
# mypy: strict

# 步骤4: 最终配置到pyproject.toml

# 或者使用--strict-equality等单个选项逐步启用
```

---

## 常见错误处理

### 忽略错误

```python
"""
忽略mypy错误
"""

# 忽略单行
result = some_untyped_function()  # type: ignore

# 忽略特定错误
result = some_untyped_function()  # type: ignore[no-untyped-call]

# 忽略整个文件
# mypy: ignore-errors

# 忽略函数
def legacy_function(x):  # type: ignore
    return x + 1

# 最佳实践: 尽量不使用ignore
# 应该修复类型问题而不是忽略
```

### Missing imports

```python
"""
处理缺失的类型存根
"""

# 方法1: 安装类型存根
# uv add --dev types-requests
# uv add --dev types-redis

import requests  # 现在有类型了

# 方法2: 在配置中忽略
# pyproject.toml:
# [[tool.mypy.overrides]]
# module = "some_package.*"
# ignore_missing_imports = true

# 方法3: 创建stub文件
# some_package.pyi
from typing import Any

def some_function(x: int) -> str: ...

# 方法4: 使用# type: ignore
import some_package  # type: ignore
```

### 常见类型错误

```python
"""
常见类型错误及解决方法
"""

# 1. Incompatible return type
def get_name() -> str:
    return None  # ❌ error
    # 修复: 使用Optional
    return None  # 但返回类型应该是str | None

def get_name() -> str | None:
    return None  # ✅ OK

# 2. Missing type parameters
def process(items: list) -> None:  # ❌ 缺少类型参数
    pass

def process(items: list[int]) -> None:  # ✅ OK
    pass

# 3. Incompatible types in assignment
x: int = "hello"  # ❌ error

# 修复: 使用Union
x: int | str = "hello"  # ✅ OK

# 4. Call to untyped function
def untyped_func(x):
    return x * 2

result = untyped_func(5)  # ❌ warning

# 修复: 添加类型
def typed_func(x: int) -> int:
    return x * 2

# 5. Argument has incompatible type
def greet(name: str) -> str:
    return f"Hello, {name}"

greet(123)  # ❌ error

# 修复: 转换类型
greet(str(123))  # ✅ OK
```

---

## 高级特性

### reveal_type和assert_type

```python
"""
调试类型推断
"""

# reveal_type: 显示mypy推断的类型
x = [1, 2, 3]
reveal_type(x)  # Revealed type is "builtins.list[builtins.int]"

# assert_type: 断言类型
from typing import assert_type

def get_value() -> int:
    return 42

result = get_value()
assert_type(result, int)  # ✅ OK
# assert_type(result, str)  # ❌ error

# 实际应用
def process_data(data: list[int] | list[str]) -> None:
    if isinstance(data[0], int):
        reveal_type(data)  # list[int] or list[str]?
        # mypy无法细化类型
```

### Type narrowing

```python
"""
类型细化
"""

def process(value: int | str | None) -> str:
    """处理多种类型"""
    
    # isinstance检查
    if isinstance(value, str):
        # mypy知道这里value是str
        return value.upper()
    elif isinstance(value, int):
        # 这里value是int
        return str(value * 2)
    else:
        # 这里value是None
        return "empty"

# is None检查
def handle_optional(value: str | None) -> str:
    if value is None:
        return "default"
    # 这里value是str
    return value.upper()

# 自定义类型守卫
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process_list(items: list[object]) -> None:
    if is_str_list(items):
        # mypy知道items是list[str]
        print(items[0].upper())
```

### 插件系统

```python
"""
mypy插件
"""

# pyproject.toml
# [tool.mypy]
# plugins = ["pydantic.mypy"]

from pydantic import BaseModel

class User(BaseModel):
    """用户模型"""
    name: str
    age: int

# mypy会检查Pydantic模型
user = User(name="Alice", age=30)
print(user.name.upper())  # ✅ mypy知道name是str

# user = User(name=123, age="30")  # ❌ mypy error

# 常用插件:
# - pydantic.mypy
# - sqlalchemy.ext.mypy.plugin
# - numpy.typing (mypy内置)
```

### 存根文件 (.pyi)

```python
"""
类型存根文件
"""

# mymodule.py
def calculate(x, y):
    return x + y

# mymodule.pyi (存根文件)
def calculate(x: int, y: int) -> int: ...

# mypy会使用.pyi文件的类型信息

# 为第三方库创建存根
# third_party_lib.pyi
from typing import Any

class SomeClass:
    def method(self, x: int) -> str: ...

def some_function(x: Any) -> None: ...

# 存根文件位置:
# 1. 与.py文件同目录
# 2. typeshed (官方存根库)
# 3. 自定义路径 (MYPYPATH环境变量)
```

---

## 📚 核心要点

### mypy基础

- ✅ **渐进式**: 可以逐步添加类型
- ✅ **静态检查**: 运行前发现错误
- ✅ **配置灵活**: pyproject.toml/mypy.ini
- ✅ **零运行时开销**: 不影响性能

### 配置

- ✅ **strict模式**: 最严格的类型检查
- ✅ **模块覆盖**: 针对不同模块不同配置
- ✅ **忽略导入**: ignore_missing_imports
- ✅ **排除目录**: exclude选项

### 错误处理

- ✅ **type: ignore**: 忽略错误
- ✅ **安装存根**: types-*包
- ✅ **类型细化**: isinstance, is None
- ✅ **TypeGuard**: 自定义类型守卫

### 高级特性

- ✅ **reveal_type**: 调试类型推断
- ✅ **assert_type**: 断言类型
- ✅ **插件**: Pydantic, SQLAlchemy等
- ✅ **存根文件**: .pyi类型定义

### 最佳实践

- ✅ 从宽松到严格逐步迁移
- ✅ 优先修复而非忽略错误
- ✅ 为公开API添加完整类型
- ✅ 使用CI/CD集成mypy检查
- ✅ 定期更新类型存根

---

**掌握mypy，构建类型安全的Python应用！** 🔍✨

**相关文档**:
- [01-type-hints-basics.md](01-type-hints-basics.md) - 类型注解基础
- [05-typing-best-practices.md](05-typing-best-practices.md) - 类型最佳实践

**最后更新**: 2025年10月28日

