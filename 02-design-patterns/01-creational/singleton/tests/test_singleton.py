"""
Singleton Pattern (单例模式) 测试套件

测试覆盖:
- 所有5种实现方式的单例特性
- 线程安全性
- 边界条件
- 异常处理
- 性能基准
"""

from __future__ import annotations

import sys
import threading
from pathlib import Path
from typing import Any

import pytest

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from singleton import (
    ConfigManager,
    Logger,
    SingletonDCL,
    SingletonMeta,
    SingletonNew,
    global_config,
    is_singleton,
    singleton,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def reset_singletons() -> None:
    """每个测试后重置单例实例 (用于测试隔离)"""
    yield
    # 测试后清理
    SingletonMeta._reset_instance(ConfigManager)
    if hasattr(Logger, "_reset_instance"):
        Logger._reset_instance()  # type: ignore[attr-defined]
    SingletonNew._reset_instance()
    SingletonDCL._reset_instance()


# ============================================================================
# 测试1: 元类方式 (SingletonMeta)
# ============================================================================

class TestSingletonMeta:
    """测试元类单例实现"""
    
    def test_same_instance(self) -> None:
        """测试返回相同实例"""
        obj1 = ConfigManager()
        obj2 = ConfigManager()
        assert obj1 is obj2
    
    def test_id_equality(self) -> None:
        """测试实例ID相同"""
        obj1 = ConfigManager()
        obj2 = ConfigManager()
        assert id(obj1) == id(obj2)
    
    def test_state_sharing(self) -> None:
        """测试状态共享"""
        config1 = ConfigManager()
        config1.set("key1", "value1")
        
        config2 = ConfigManager()
        assert config2.get("key1") == "value1"
    
    def test_multiple_calls(self) -> None:
        """测试多次调用都返回相同实例"""
        instances = [ConfigManager() for _ in range(10)]
        first = instances[0]
        assert all(inst is first for inst in instances)
    
    def test_custom_class_with_metaclass(self) -> None:
        """测试自定义类使用元类"""
        class MyConfig(metaclass=SingletonMeta):
            def __init__(self) -> None:
                if not hasattr(self, "_initialized"):
                    self.value = 42
                    self._initialized = True
        
        obj1 = MyConfig()
        obj2 = MyConfig()
        assert obj1 is obj2
        assert obj1.value == 42


# ============================================================================
# 测试2: 装饰器方式 (@singleton)
# ============================================================================

class TestSingletonDecorator:
    """测试装饰器单例实现"""
    
    def test_same_instance(self) -> None:
        """测试返回相同实例"""
        log1 = Logger()
        log2 = Logger()
        assert log1 is log2
    
    def test_state_sharing(self) -> None:
        """测试状态共享"""
        logger1 = Logger()
        logger1.info("test message")
        
        logger2 = Logger()
        logs = logger2.get_logs()
        assert len(logs) > 0
        assert "test message" in logs[0]
    
    def test_custom_decorated_class(self) -> None:
        """测试自定义装饰器类"""
        @singleton
        class Counter:
            def __init__(self) -> None:
                self.count = 0
            
            def increment(self) -> None:
                self.count += 1
        
        c1 = Counter()
        c1.increment()
        
        c2 = Counter()
        assert c2.count == 1
        assert c1 is c2


# ============================================================================
# 测试3: 模块级单例
# ============================================================================

class TestModuleSingleton:
    """测试模块级单例"""
    
    def test_module_singleton_exists(self) -> None:
        """测试模块级单例存在"""
        assert global_config is not None
        assert hasattr(global_config, "version")
    
    def test_module_singleton_state(self) -> None:
        """测试模块级单例状态"""
        original_name = global_config.app_name
        global_config.app_name = "TestApp"
        assert global_config.app_name == "TestApp"
        # 恢复
        global_config.app_name = original_name


# ============================================================================
# 测试4: __new__方式 (SingletonNew)
# ============================================================================

class TestSingletonNew:
    """测试__new__单例实现"""
    
    def test_same_instance(self) -> None:
        """测试返回相同实例"""
        class TestClass(SingletonNew):
            pass
        
        obj1 = TestClass()
        obj2 = TestClass()
        assert obj1 is obj2
    
    def test_init_called_multiple_times(self) -> None:
        """测试__init__被多次调用的问题"""
        class Counter(SingletonNew):
            def __init__(self) -> None:
                if not hasattr(self, "_initialized"):
                    self.count = 0
                    self._initialized = True
                else:
                    # __init__会被多次调用
                    pass
        
        c1 = Counter()
        c1.count = 5
        
        c2 = Counter()
        # 应该是同一个实例,状态保持
        assert c2.count == 5


# ============================================================================
# 测试5: 双重检查锁方式 (DCL)
# ============================================================================

class TestSingletonDCL:
    """测试双重检查锁单例实现"""
    
    def test_same_instance(self) -> None:
        """测试返回相同实例"""
        class TestCache(SingletonDCL):
            pass
        
        obj1 = TestCache()
        obj2 = TestCache()
        assert obj1 is obj2
    
    def test_state_preservation(self) -> None:
        """测试状态保持"""
        class Cache(SingletonDCL):
            def __init__(self) -> None:
                if not hasattr(self, "_initialized"):
                    self.data: dict[str, Any] = {}
                    self._initialized = True
        
        c1 = Cache()
        c1.data["key"] = "value"
        
        c2 = Cache()
        assert c2.data["key"] == "value"


# ============================================================================
# 测试6: 线程安全性
# ============================================================================

class TestThreadSafety:
    """测试线程安全性"""
    
    def test_metaclass_thread_safety(self) -> None:
        """测试元类实现的线程安全"""
        instances: list[ConfigManager] = []
        
        def create_instance() -> None:
            inst = ConfigManager()
            instances.append(inst)
        
        # 创建100个线程同时创建实例
        threads = [threading.Thread(target=create_instance) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 所有实例应该是同一个
        first = instances[0]
        assert all(inst is first for inst in instances)
    
    def test_decorator_thread_safety(self) -> None:
        """测试装饰器实现的线程安全"""
        @singleton
        class ThreadSafeCounter:
            def __init__(self) -> None:
                self.value = 0
        
        instances: list[ThreadSafeCounter] = []
        
        def create_instance() -> None:
            inst = ThreadSafeCounter()
            instances.append(inst)
        
        threads = [threading.Thread(target=create_instance) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        first = instances[0]
        assert all(inst is first for inst in instances)


# ============================================================================
# 测试7: ConfigManager 功能测试
# ============================================================================

class TestConfigManager:
    """测试ConfigManager类"""
    
    def test_set_and_get(self) -> None:
        """测试设置和获取配置"""
        config = ConfigManager()
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"
    
    def test_get_nonexistent(self) -> None:
        """测试获取不存在的配置"""
        config = ConfigManager()
        assert config.get("nonexistent") is None
        assert config.get("nonexistent", "default") == "default"
    
    def test_has(self) -> None:
        """测试配置存在性检查"""
        config = ConfigManager()
        config.set("exists", "yes")
        assert config.has("exists") is True
        assert config.has("not_exists") is False
    
    def test_clear(self) -> None:
        """测试清空配置"""
        config = ConfigManager()
        config.set("key1", "value1")
        config.set("key2", "value2")
        config.clear()
        assert config.has("key1") is False
        assert config.has("key2") is False


# ============================================================================
# 测试8: Logger 功能测试
# ============================================================================

class TestLogger:
    """测试Logger类"""
    
    def test_info_logging(self) -> None:
        """测试info日志"""
        logger = Logger()
        logger.clear_logs()
        logger.info("test info")
        logs = logger.get_logs()
        assert len(logs) == 1
        assert "[INFO]" in logs[0]
        assert "test info" in logs[0]
    
    def test_warning_logging(self) -> None:
        """测试warning日志"""
        logger = Logger()
        logger.clear_logs()
        logger.warning("test warning")
        logs = logger.get_logs()
        assert "[WARNING]" in logs[0]
    
    def test_error_logging(self) -> None:
        """测试error日志"""
        logger = Logger()
        logger.clear_logs()
        logger.error("test error")
        logs = logger.get_logs()
        assert "[ERROR]" in logs[0]
    
    def test_multiple_logs(self) -> None:
        """测试多条日志"""
        logger = Logger()
        logger.clear_logs()
        logger.info("info1")
        logger.warning("warning1")
        logger.error("error1")
        logs = logger.get_logs()
        assert len(logs) == 3


# ============================================================================
# 测试9: 边界条件
# ============================================================================

class TestBoundaryConditions:
    """测试边界条件"""
    
    def test_empty_config_manager(self) -> None:
        """测试空配置管理器"""
        config = ConfigManager()
        config.clear()
        assert not config.has("any_key")
    
    def test_overwrite_config(self) -> None:
        """测试覆盖配置"""
        config = ConfigManager()
        config.set("key", "value1")
        config.set("key", "value2")
        assert config.get("key") == "value2"
    
    def test_large_number_of_configs(self) -> None:
        """测试大量配置"""
        config = ConfigManager()
        config.clear()
        for i in range(1000):
            config.set(f"key{i}", f"value{i}")
        assert config.get("key500") == "value500"


# ============================================================================
# 测试10: 工具函数
# ============================================================================

class TestUtilityFunctions:
    """测试工具函数"""
    
    def test_is_singleton_metaclass(self) -> None:
        """测试is_singleton函数 - 元类"""
        assert is_singleton(ConfigManager) is True
    
    def test_is_singleton_decorator(self) -> None:
        """测试is_singleton函数 - 装饰器"""
        assert is_singleton(Logger) is True
    
    def test_is_singleton_regular_class(self) -> None:
        """测试is_singleton函数 - 普通类"""
        class RegularClass:
            pass
        assert is_singleton(RegularClass) is False
    
    def test_is_singleton_new_subclass(self) -> None:
        """测试is_singleton函数 - __new__子类"""
        class MyClass(SingletonNew):
            pass
        assert is_singleton(MyClass) is True


# ============================================================================
# 测试11: 继承特性
# ============================================================================

class TestInheritance:
    """测试继承特性"""
    
    def test_metaclass_inheritance(self) -> None:
        """测试元类继承"""
        class BaseConfig(metaclass=SingletonMeta):
            def __init__(self) -> None:
                if not hasattr(self, "_initialized"):
                    self.base_value = "base"
                    self._initialized = True
        
        class DerivedConfig(BaseConfig):
            def __init__(self) -> None:
                super().__init__()
                if not hasattr(self, "_derived_initialized"):
                    self.derived_value = "derived"
                    self._derived_initialized = True
        
        # 父类和子类应该是不同的单例
        base1 = BaseConfig()
        base2 = BaseConfig()
        derived1 = DerivedConfig()
        derived2 = DerivedConfig()
        
        assert base1 is base2
        assert derived1 is derived2
        assert base1 is not derived1


# ============================================================================
# 测试12: 性能测试 (基础)
# ============================================================================

@pytest.mark.benchmark
class TestPerformance:
    """性能测试"""
    
    def test_metaclass_creation_performance(self, benchmark: Any) -> None:
        """测试元类实例创建性能"""
        result = benchmark(ConfigManager)
        assert result is not None
    
    def test_decorator_creation_performance(self, benchmark: Any) -> None:
        """测试装饰器实例创建性能"""
        result = benchmark(Logger)
        assert result is not None
    
    def test_repeated_access_performance(self) -> None:
        """测试重复访问性能"""
        import time
        
        # 第一次创建
        start = time.perf_counter()
        for _ in range(10000):
            _ = ConfigManager()
        elapsed = time.perf_counter() - start
        
        # 应该非常快 (< 100ms for 10k calls)
        assert elapsed < 0.1


# ============================================================================
# 集成测试
# ============================================================================

class TestIntegration:
    """集成测试"""
    
    def test_multiple_singletons_coexist(self) -> None:
        """测试多个单例可以共存"""
        config = ConfigManager()
        logger = Logger()
        
        config.set("app", "test")
        logger.clear_logs()
        logger.info("test")
        
        # 验证各自独立
        assert config.get("app") == "test"
        assert len(logger.get_logs()) == 1
    
    def test_singleton_in_complex_scenario(self) -> None:
        """测试复杂场景下的单例"""
        # 模拟实际应用场景
        config = ConfigManager()
        config.clear()
        config.set("db_host", "localhost")
        config.set("db_port", "5432")
        
        logger = Logger()
        logger.clear_logs()
        logger.info(f"Connecting to {config.get('db_host')}")
        
        # 在另一个"模块"中使用
        config2 = ConfigManager()
        logger2 = Logger()
        
        assert config2.get("db_host") == "localhost"
        assert len(logger2.get_logs()) == 1


# ============================================================================
# 运行所有测试
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

