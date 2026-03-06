# PEP 702: @deprecated 装饰器

> Python 3.13 新特性 - 标准化的弃用标记机制

---

## 概述

**PEP 702** 引入了 `warnings.deprecated()` 装饰器，提供了一种统一的方式来标记函数、类和方法的弃用状态。

**发布版本**: Python 3.13+
**PEP链接**: [PEP 702](https://peps.python.org/pep-0702/)

**核心优势**:

- ✅ 运行时发出 `DeprecationWarning`
- ✅ 类型检查器识别弃用
- ✅ IDE 显示删除线提示
- ✅ 统一的弃用信息格式

---

## 基础用法

### 1. 弃用函数

```python
import warnings

@warnings.deprecated("Use new_function() instead.")
def old_function():
    """这个函数已被弃用"""
    return "deprecated"

# 调用时会发出警告
old_function()
# DeprecationWarning: old_function is deprecated: Use new_function() instead.
```

### 2. 弃用类

```python
import warnings

@warnings.deprecated("Use NewClass instead.", category=FutureWarning)
class OldClass:
    """这个类已被弃用"""
    pass

# 实例化时发出警告
obj = OldClass()
# FutureWarning: OldClass is deprecated: Use NewClass instead.
```

### 3. 弃用方法

```python
import warnings

class MyClass:
    @warnings.deprecated("Use new_method() instead. Will be removed in v2.0.")
    def old_method(self):
        return "old"

    def new_method(self):
        return "new"

obj = MyClass()
obj.old_method()  # 发出 DeprecationWarning
```

---

## 高级用法

### 添加更多元数据

```python
import warnings
from typing import final

@warnings.deprecated(
    "Use SecureConnection instead.",
    category=DeprecationWarning,
    stacklevel=2
)
class InsecureConnection:
    """
    不安全的连接类

    弃用说明:
        - 弃用版本: 1.5.0
        - 移除版本: 2.0.0
        - 替代方案: SecureConnection
    """
    def connect(self):
        pass
```

### 渐进式弃用策略

```python
import warnings
from datetime import date

# 阶段 1: 即将弃用（提前通知）
@warnings.deprecated(
    "Will be deprecated in v2.0. Start using new_api() now.",
    category=PendingDeprecationWarning
)
def preview_deprecated_api():
    """即将弃用的 API"""
    pass

# 阶段 2: 正式弃用
@warnings.deprecated(
    "Deprecated since v2.0. Use new_api() instead.",
    category=DeprecationWarning
)
def deprecated_api():
    """已弃用的 API"""
    pass

# 阶段 3: 即将移除
@warnings.deprecated(
    "Will be removed in v3.0. Use new_api() instead.",
    category=FutureWarning
)
def soon_to_remove_api():
    """即将移除的 API"""
    pass
```

---

## 实战模式

### 模式 1: 库版本管理

```python
import warnings
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")

class DeprecationManager:
    """管理库中所有弃用的组件"""

    LIBRARY_VERSION = "2.0.0"

    @staticmethod
    def deprecated_since(
        version: str,
        replacement: str | None = None,
        removal_version: str | None = None
    ) -> Callable[[T], T]:
        """
        标记自指定版本弃用的装饰器

        Args:
            version: 开始弃用的版本
            replacement: 替代方案
            removal_version: 计划移除的版本
        """
        message = f"Deprecated since v{version}."

        if replacement:
            message += f" Use {replacement} instead."

        if removal_version:
            message += f" Will be removed in v{removal_version}."

        return warnings.deprecated(message, stacklevel=3)

# 使用
class MyLibrary:
    @DeprecationManager.deprecated_since(
        version="1.5",
        replacement="MyLibrary.new_compute",
        removal_version="2.5"
    )
    def old_compute(self, x: int) -> int:
        return x * 2

    def new_compute(self, x: int) -> int:
        return x * 2 + 1

# 调用
lib = MyLibrary()
lib.old_compute(5)
# DeprecationWarning: old_compute is deprecated:
# Deprecated since v1.5. Use MyLibrary.new_compute instead.
# Will be removed in v2.5.
```

### 模式 2: API 版本控制

```python
import warnings
from typing import Protocol

class APIv1(Protocol):
    """API 版本 1（已弃用）"""

    @warnings.deprecated("Use APIv2.process() instead.")
    def process(self, data: dict) -> dict: ...

class APIv2:
    """API 版本 2（当前）"""

    def process(self, data: dict) -> dict:
        """处理数据的新实现"""
        return {"v2": True, **data}

class CompatibilityLayer:
    """兼容性层，支持旧 API"""

    def __init__(self):
        self._v2 = APIv2()

    @warnings.deprecated(
        "API v1 is deprecated. Migrate to API v2.",
        category=FutureWarning
    )
    def legacy_process(self, data: dict) -> dict:
        """兼容旧版 API"""
        # 转换 v1 格式到 v2 格式
        converted = self._convert_v1_to_v2(data)
        result = self._v2.process(converted)
        # 转换回 v1 格式
        return self._convert_v2_to_v1(result)

    def _convert_v1_to_v2(self, data: dict) -> dict:
        return data

    def _convert_v2_to_v1(self, data: dict) -> dict:
        return data
```

### 模式 3: 重构助手

```python
import warnings
import functools
from typing import TypeVar

T = TypeVar("T")

def deprecated_property(message: str):
    """弃用属性的装饰器"""
    def decorator(func):
        @warnings.deprecated(message)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

class User:
    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @property
    @warnings.deprecated("Use email instead. Username is being removed.")
    def username(self) -> str:
        """已弃用：使用 email 替代"""
        return self._email.split("@")[0]

    @property
    def email(self) -> str:
        return self._email

# 使用
user = User("Alice", "alice@example.com")
print(user.username)  # 发出 DeprecationWarning
print(user.email)     # 正常，无警告
```

---

## 测试弃用警告

### 使用 pytest

```python
import warnings
import pytest

@warnings.deprecated("This function is deprecated.")
def deprecated_func():
    return 42

def test_deprecated_emits_warning():
    """测试弃用警告是否正确发出"""
    with pytest.warns(DeprecationWarning, match="deprecated"):
        result = deprecated_func()

    assert result == 42

# 更精确的匹配
def test_deprecated_message():
    """测试弃用消息内容"""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        deprecated_func()

        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "deprecated" in str(w[0].message)
```

### 抑制弃用警告

```python
import warnings

# 方法 1: 上下文管理器
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    deprecated_func()  # 不会发出警告

# 方法 2: 全局过滤
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 方法 3: 仅忽略特定模块
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="legacy_module"
)
```

---

## 与类型检查器集成

### mypy 支持

```python
# mypy 会识别 @deprecated 并标记调用
import warnings

@warnings.deprecated("Use new_func() instead.")
def old_func() -> int:
    return 42

def new_func() -> int:
    return 42

def main() -> None:
    x = old_func()  # mypy: 警告 - 使用了已弃用的函数
    y = new_func()  # OK
```

### IDE 支持

大多数现代 IDE（VS Code、PyCharm）会：

- 在已弃用的代码上显示删除线
- 在悬停时显示弃用消息
- 提供快速修复建议

---

## 完整示例: 库迁移

```python
"""
示例: 一个库的弃用和迁移策略
"""
import warnings
from typing import TypeVar

T = TypeVar("T")

class MyLibrary:
    """
    示例库，展示完整的弃用策略

    版本历史:
        v1.0: 初始版本
        v1.5: 标记 old_api 为弃用
        v2.0: 移除 old_api
    """

    VERSION = "1.5.0"

    # ========== 新 API ==========

    def process_data(self, data: list[dict]) -> list[dict]:
        """
        处理数据的新 API（推荐）

        Args:
            data: 输入数据列表

        Returns:
            处理后的数据列表
        """
        return [{"processed": True, **item} for item in data]

    def transform(self, value: int) -> int:
        """数据转换（新）"""
        return value * 2 + 1

    # ========== 弃用 API ==========

    @warnings.deprecated(
        f"Use process_data() instead. Will be removed in v2.0.",
        category=DeprecationWarning
    )
    def old_process(self, items: list) -> list:
        """
        旧的数据处理方法（已弃用）

        .. deprecated:: 1.5.0
            Use :meth:`process_data` instead.
        """
        return self.process_data([{"item": item} for item in items])

    @warnings.deprecated(
        "Use transform() instead. Will be removed in v2.0.",
        category=DeprecationWarning
    )
    def old_transform(self, x: int) -> int:
        """旧的数据转换（已弃用）"""
        return self.transform(x)


# 迁移指南脚本
def migration_guide():
    """打印迁移指南"""
    guide = """
    迁移指南: v1.x → v2.0
    ====================

    弃用的 API              替代方案
    ----------------------  --------------------
    old_process(items)      process_data(data)
    old_transform(x)        transform(value)

    示例:
        # 旧代码
        lib = MyLibrary()
        result = lib.old_process([1, 2, 3])

        # 新代码
        lib = MyLibrary()
        result = lib.process_data([{"item": 1}, {"item": 2}])
    """
    print(guide)

if __name__ == "__main__":
    # 演示
    lib = MyLibrary()

    # 使用新 API（无警告）
    print("Using new API:")
    result = lib.process_data([{"name": "Alice"}])
    print(f"  Result: {result}")

    # 使用旧 API（有警告）
    print("\nUsing deprecated API:")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = lib.old_process([1, 2, 3])
        if w:
            print(f"  Warning: {w[0].message}")
        print(f"  Result: {result}")
```

---

## 最佳实践总结

### ✅ 应该做的

1. **提供清晰的迁移路径**

   ```python
   @warnings.deprecated("Use new_function() instead.")
   ```

2. **指定移除版本**

   ```python
   @warnings.deprecated("Will be removed in v3.0. Use X instead.")
   ```

3. **使用适当的警告类别**
   - `PendingDeprecationWarning`: 即将弃用
   - `DeprecationWarning`: 已弃用
   - `FutureWarning`: 行为将改变或即将移除

4. **在文档中说明**

   ```python
   def func():
       """
       功能说明

       .. deprecated:: 1.5
           Use :func:`new_func` instead.
       """
   ```

### ❌ 不应该做的

1. **不要突然移除没有警告的 API**
2. **不要使用模糊的弃用消息**
3. **不要在没有替代方案的情况下弃用**

---

## 兼容性

| Python 版本 | 支持情况 |
|-------------|----------|
| 3.13+ | ✅ `warnings.deprecated()` 原生支持 |
| 3.12 | ❌ 需要第三方库 `typing_extensions` |
| <3.12 | ❌ 需要自定义实现 |

### 向后兼容方案

```python
try:
    from warnings import deprecated
except ImportError:
    # Python < 3.13 的兼容实现
    import functools
    import warnings
    from typing import Callable, TypeVar

    T = TypeVar("T")

    def deprecated(msg: str, /, *, category=DeprecationWarning, stacklevel=1):
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                warnings.warn(
                    f"{func.__name__} is deprecated: {msg}",
                    category=category,
                    stacklevel=stacklevel + 1
                )
                return func(*args, **kwargs)
            return wrapper
        return decorator
```

---

## 延伸阅读

- [PEP 702 - Marking deprecations](https://peps.python.org/pep-0702/)
- [Python warnings 模块](https://docs.python.org/3/library/warnings.html)
- [Python 3.13 What's New](https://docs.python.org/3.13/whatsnew/3.13.html)

---

**使用 @deprecated，优雅地管理 API 生命周期！** 📝⚠️
