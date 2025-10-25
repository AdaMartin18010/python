# 模块开发标准模板

本模板定义了Python 2025知识库中所有模块的标准结构和质量要求。

---

## 📁 文件结构

```text
module-name/
├── README.md                    # 模块文档
├── __init__.py                  # 模块入口
├── implementation.py            # 主要实现
├── examples.py                  # 使用示例
├── tests/
│   ├── test_implementation.py   # 单元测试
│   ├── test_integration.py      # 集成测试
│   └── test_performance.py      # 性能测试
├── benchmarks/
│   └── benchmark.py             # 性能基准
└── docs/
    ├── theory.md                # 理论说明
    ├── uml/                     # UML图(如适用)
    └── references.md            # 参考资料
```

---

## 📄 README.md 模板

```markdown
# [模块名称]

**分类**: [创建型/结构型/行为型/...]  
**难度**: ⭐⭐⭐☆☆  
**Python版本**: 3.12+  
**状态**: ✅ 完成 / 🚧 进行中 / 📝 规划中

---

## 📖 简介

[一句话描述模块的作用]

## 🎯 适用场景

- 场景1
- 场景2
- 场景3

## ⚠️ 注意事项

- 注意点1
- 注意点2

## 📊 性能特征

- 时间复杂度: O(?)
- 空间复杂度: O(?)

## 🔗 相关模块

- 模块A
- 模块B

## 📚 参考资料

- [资料1](url)
- [资料2](url)
```

---

## 💻 代码模板 (implementation.py)

```python
"""
[模块名称] - [简短描述]

本模块实现了...[详细说明]

Example:
    >>> from module_name import Class
    >>> obj = Class()
    >>> obj.method()
    'result'

Attributes:
    MODULE_CONSTANT (str): 模块级常量说明

Note:
    重要提示说明

See Also:
    相关模块或函数

References:
    - Design Patterns (GoF)
    - Python Cookbook
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, ClassVar, Protocol, Self, TypeVar, override

# ============================================================================
# 类型定义
# ============================================================================

T = TypeVar("T")
P = TypeVar("P", bound="SomeProtocol")


# ============================================================================
# 协议定义 (如需要)
# ============================================================================

class SomeProtocol(Protocol):
    """协议说明"""
    
    def method(self) -> str:
        """方法说明"""
        ...


# ============================================================================
# 主要实现
# ============================================================================

class MainClass:
    """
    主类说明
    
    这是主类的详细说明...
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
    
    Attributes:
        attr1: 属性1说明
        attr2: 属性2说明
    
    Example:
        >>> obj = MainClass(param1="value")
        >>> result = obj.method()
        >>> print(result)
        'expected'
    
    Note:
        重要提示
    """
    
    # 类变量
    _class_var: ClassVar[dict[str, Any]] = {}
    
    def __init__(self, param1: str, param2: int = 0) -> None:
        """
        初始化方法
        
        Args:
            param1: 参数1
            param2: 参数2,默认为0
        
        Raises:
            ValueError: 当参数不合法时
        """
        self._attr1 = param1
        self._attr2 = param2
        self._validate()
    
    def _validate(self) -> None:
        """验证内部状态"""
        if self._attr2 < 0:
            raise ValueError("attr2 must be non-negative")
    
    def method(self, arg: str) -> str:
        """
        公开方法
        
        Args:
            arg: 方法参数
        
        Returns:
            处理结果
        
        Raises:
            RuntimeError: 当处理失败时
        
        Example:
            >>> obj.method("input")
            'processed: input'
        """
        return f"processed: {arg}"
    
    def _private_method(self) -> None:
        """私有辅助方法"""
        pass
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"{self.__class__.__name__}(attr1={self._attr1!r}, attr2={self._attr2})"
    
    def __eq__(self, other: object) -> bool:
        """相等性比较"""
        if not isinstance(other, MainClass):
            return NotImplemented
        return self._attr1 == other._attr1 and self._attr2 == other._attr2


# ============================================================================
# 辅助类
# ============================================================================

class HelperClass:
    """辅助类说明"""
    pass


# ============================================================================
# 工厂函数/便捷函数
# ============================================================================

def create_instance(config: dict[str, Any]) -> MainClass:
    """
    工厂函数
    
    Args:
        config: 配置字典
    
    Returns:
        创建的实例
    """
    return MainClass(
        param1=config["param1"],
        param2=config.get("param2", 0)
    )


# ============================================================================
# 模块级别函数
# ============================================================================

def utility_function(data: list[T]) -> list[T]:
    """
    工具函数
    
    Args:
        data: 输入数据
    
    Returns:
        处理后的数据
    """
    return sorted(data)
```

---

## 🧪 测试模板 (test_implementation.py)

```python
"""
[模块名称] 的单元测试

测试覆盖:
- 正常情况
- 边界情况
- 异常情况
- 性能测试
"""

from __future__ import annotations

import pytest

from module_name import MainClass, create_instance


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_instance() -> MainClass:
    """创建测试用实例"""
    return MainClass(param1="test", param2=10)


# ============================================================================
# 基础功能测试
# ============================================================================

class TestMainClass:
    """MainClass 测试套件"""
    
    def test_init(self) -> None:
        """测试初始化"""
        obj = MainClass(param1="value", param2=5)
        assert obj._attr1 == "value"
        assert obj._attr2 == 5
    
    def test_init_default(self) -> None:
        """测试默认参数"""
        obj = MainClass(param1="value")
        assert obj._attr2 == 0
    
    def test_method(self, sample_instance: MainClass) -> None:
        """测试主要方法"""
        result = sample_instance.method("input")
        assert result == "processed: input"
    
    def test_repr(self, sample_instance: MainClass) -> None:
        """测试字符串表示"""
        result = repr(sample_instance)
        assert "MainClass" in result
        assert "test" in result
    
    def test_equality(self) -> None:
        """测试相等性"""
        obj1 = MainClass(param1="test", param2=10)
        obj2 = MainClass(param1="test", param2=10)
        obj3 = MainClass(param1="other", param2=10)
        
        assert obj1 == obj2
        assert obj1 != obj3


# ============================================================================
# 边界条件测试
# ============================================================================

class TestBoundaryConditions:
    """边界条件测试"""
    
    def test_empty_string(self) -> None:
        """测试空字符串"""
        obj = MainClass(param1="")
        assert obj._attr1 == ""
    
    def test_zero_value(self) -> None:
        """测试零值"""
        obj = MainClass(param1="test", param2=0)
        assert obj._attr2 == 0


# ============================================================================
# 异常处理测试
# ============================================================================

class TestExceptions:
    """异常处理测试"""
    
    def test_invalid_param(self) -> None:
        """测试无效参数"""
        with pytest.raises(ValueError):
            MainClass(param1="test", param2=-1)


# ============================================================================
# 性能测试
# ============================================================================

@pytest.mark.benchmark
class TestPerformance:
    """性能测试"""
    
    def test_method_performance(self, benchmark: Any) -> None:
        """测试方法性能"""
        obj = MainClass(param1="test")
        result = benchmark(obj.method, "input")
        assert result == "processed: input"


# ============================================================================
# 集成测试
# ============================================================================

class TestIntegration:
    """集成测试"""
    
    def test_factory_function(self) -> None:
        """测试工厂函数"""
        config = {"param1": "test", "param2": 5}
        obj = create_instance(config)
        assert isinstance(obj, MainClass)
        assert obj._attr1 == "test"
        assert obj._attr2 == 5
```

---

## 📝 示例模板 (examples.py)

```python
"""
[模块名称] 使用示例

本文件包含实际使用场景的示例代码。
"""

from __future__ import annotations

from module_name import MainClass


# ============================================================================
# 基础用法
# ============================================================================

def basic_usage() -> None:
    """基础使用示例"""
    print("=== 基础用法 ===")
    
    # 创建实例
    obj = MainClass(param1="example", param2=10)
    
    # 使用方法
    result = obj.method("data")
    print(f"结果: {result}")


# ============================================================================
# 高级用法
# ============================================================================

def advanced_usage() -> None:
    """高级使用示例"""
    print("\n=== 高级用法 ===")
    
    # 复杂场景
    instances = [
        MainClass(param1=f"instance_{i}", param2=i)
        for i in range(5)
    ]
    
    for instance in instances:
        result = instance.method("data")
        print(f"{instance}: {result}")


# ============================================================================
# 实际场景
# ============================================================================

def real_world_scenario() -> None:
    """实际应用场景"""
    print("\n=== 实际场景 ===")
    
    # TODO: 填写实际场景代码
    pass


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    """运行所有示例"""
    basic_usage()
    advanced_usage()
    real_world_scenario()


if __name__ == "__main__":
    main()
```

---

## 📊 性能基准模板 (benchmarks/benchmark.py)

```python
"""
[模块名称] 性能基准测试

使用: python benchmarks/benchmark.py
"""

from __future__ import annotations

import time
from typing import Callable

from module_name import MainClass


# ============================================================================
# 基准测试工具
# ============================================================================

def benchmark(func: Callable[[], None], iterations: int = 10000) -> float:
    """
    基准测试工具
    
    Args:
        func: 要测试的函数
        iterations: 迭代次数
    
    Returns:
        平均执行时间(秒)
    """
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    end = time.perf_counter()
    return (end - start) / iterations


# ============================================================================
# 基准测试
# ============================================================================

def benchmark_creation() -> None:
    """测试实例创建性能"""
    def create() -> None:
        MainClass(param1="test", param2=10)
    
    avg_time = benchmark(create)
    print(f"实例创建: {avg_time * 1000:.4f}ms")


def benchmark_method() -> None:
    """测试方法调用性能"""
    obj = MainClass(param1="test", param2=10)
    
    def call_method() -> None:
        obj.method("data")
    
    avg_time = benchmark(call_method)
    print(f"方法调用: {avg_time * 1000:.4f}ms")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    """运行所有基准测试"""
    print("=== 性能基准测试 ===\n")
    benchmark_creation()
    benchmark_method()


if __name__ == "__main__":
    main()
```

---

## ✅ 质量检查清单

在提交模块前,确保:

### 代码质量

- [ ] Ruff 检查通过 (`ruff check .`)
- [ ] Ruff 格式化完成 (`ruff format .`)
- [ ] Mypy strict mode 通过 (`mypy --strict .`)
- [ ] 所有类型都有注解
- [ ] 所有公开API有文档字符串

### 测试

- [ ] 单元测试覆盖率 >= 90%
- [ ] 所有测试通过 (`pytest`)
- [ ] 边界条件测试完整
- [ ] 异常处理测试完整
- [ ] 性能基准测试完成

### 文档

- [ ] README.md 完整
- [ ] 理论说明清晰
- [ ] 使用示例完整
- [ ] 参考资料齐全
- [ ] UML图清晰(如适用)

### 提交

- [ ] Git commit message 规范
- [ ] 更新 progress.yaml
- [ ] 更新主索引文件
- [ ] 运行完整测试套件

---

## 🎯 额外加分项

- [ ] 交互式可视化
- [ ] Jupyter Notebook 示例
- [ ] 视频教程链接
- [ ] 博客文章链接
- [ ] 性能对比图表
- [ ] 复杂度分析图表

---

## 📞 帮助

如有疑问,参考:

- 已完成的模块示例
- 项目规范文档
- 社区讨论
