"""
Singleton Pattern (单例模式) - 完整实现

本模块提供了5种Python实现单例模式的方式:
1. 元类方式 (Metaclass) - ⭐推荐
2. 装饰器方式 (Decorator) - ⭐推荐
3. 模块方式 (Module) - ⭐最Pythonic
4. __new__方式 - 标准
5. 双重检查锁方式 (DCL) - 高级

所有实现都是线程安全的。

Example:
    使用元类:
    >>> class MyClass(metaclass=SingletonMeta):
    ...     pass
    >>> obj1 = MyClass()
    >>> obj2 = MyClass()
    >>> assert obj1 is obj2

    使用装饰器:
    >>> @singleton
    ... class MyClass:
    ...     pass
    >>> obj1 = MyClass()
    >>> obj2 = MyClass()
    >>> assert obj1 is obj2

Attributes:
    SingletonMeta: 单例元类
    singleton: 单例装饰器

Note:
    - 所有方式都保证线程安全
    - 推荐使用元类或装饰器方式
    - 模块级单例最简单但灵活性较低

See Also:
    - Multiton Pattern: 控制实例数量的变体
    - Borg Pattern: 共享状态的变体

References:
    - Design Patterns (GoF)
    - Python Cookbook
    - PEP 3115 - Metaclasses in Python 3
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from functools import wraps
from typing import Any, ClassVar, TypeVar, cast

# ============================================================================
# 类型定义
# ============================================================================

T = TypeVar("T")
ClassType = TypeVar("ClassType", bound=type)


# ============================================================================
# 方式1: 元类实现 (Metaclass) ⭐推荐
# ============================================================================

class SingletonMeta(type):
    """
    单例元类 - 线程安全实现
    
    使用元类来控制类的实例化,确保每个类只有一个实例。
    使用锁来保证线程安全。
    
    Example:
        >>> class Database(metaclass=SingletonMeta):
        ...     def __init__(self) -> None:
        ...         self.connection = "connected"
        >>> 
        >>> db1 = Database()
        >>> db2 = Database()
        >>> assert db1 is db2
        >>> assert db1.connection == "connected"
    
    Note:
        - 线程安全: 使用threading.Lock
        - 性能优化: 使用双重检查锁定
        - 子类友好: 每个子类都是独立的单例
    """
    
    _instances: ClassVar[dict[type, Any]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """
        拦截类的实例化调用
        
        使用双重检查锁定模式:
        1. 第一次检查: 快速路径,无锁
        2. 加锁
        3. 第二次检查: 确保线程安全
        4. 创建实例
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            类的单例实例
        """
        # 第一次检查 (无锁,快速路径)
        if cls not in cls._instances:
            # 获取锁
            with cls._lock:
                # 第二次检查 (有锁,确保线程安全)
                if cls not in cls._instances:
                    # 创建实例
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        
        return cls._instances[cls]
    
    @classmethod
    def _reset_instance(mcs, cls: type) -> None:
        """
        重置单例实例 (仅用于测试)
        
        Args:
            cls: 要重置的类
        
        Warning:
            此方法仅应在测试中使用!
        """
        with mcs._lock:
            if cls in mcs._instances:
                del mcs._instances[cls]


# ============================================================================
# 方式2: 装饰器实现 (Decorator) ⭐推荐
# ============================================================================

def singleton(cls: type[T]) -> type[T]:
    """
    单例装饰器 - 线程安全实现
    
    使用装饰器包装类,控制实例化。
    简单易用,适合大多数场景。
    
    Args:
        cls: 要转换为单例的类
    
    Returns:
        包装后的单例类
    
    Example:
        >>> @singleton
        ... class Logger:
        ...     def __init__(self) -> None:
        ...         self.level = "INFO"
        >>> 
        >>> logger1 = Logger()
        >>> logger2 = Logger()
        >>> assert logger1 is logger2
    
    Note:
        - 线程安全
        - 保留原类的所有属性
        - 支持类型检查
    """
    instances: dict[type, Any] = {}
    lock = threading.Lock()
    
    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> T:
        """获取单例实例"""
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return cast(T, instances[cls])
    
    # 保留原类的属性
    get_instance.__name__ = cls.__name__  # type: ignore[attr-defined]
    get_instance.__doc__ = cls.__doc__  # type: ignore[attr-defined]
    
    # 添加重置方法 (用于测试)
    def reset_instance() -> None:
        """重置单例实例 (仅用于测试)"""
        with lock:
            if cls in instances:
                del instances[cls]
    
    get_instance._reset_instance = reset_instance  # type: ignore[attr-defined]
    
    return cast(type[T], get_instance)


# ============================================================================
# 方式3: __new__方法实现
# ============================================================================

class SingletonNew:
    """
    使用__new__方法实现单例
    
    重写__new__方法来控制实例创建。
    标准但不如元类和装饰器优雅。
    
    Example:
        >>> class Config(SingletonNew):
        ...     def __init__(self) -> None:
        ...         if not hasattr(self, "_initialized"):
        ...             self.app_name = "MyApp"
        ...             self._initialized = True
        >>> 
        >>> config1 = Config()
        >>> config2 = Config()
        >>> assert config1 is config2
    
    Note:
        - 需要注意__init__可能被多次调用
        - 使用_initialized标志防止重复初始化
    """
    
    _instance: ClassVar[SingletonNew | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    
    def __new__(cls, *args: Any, **kwargs: Any) -> SingletonNew:
        """
        创建或返回单例实例
        
        Returns:
            类的单例实例
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def _reset_instance(cls) -> None:
        """重置单例实例 (仅用于测试)"""
        with cls._lock:
            cls._instance = None


# ============================================================================
# 方式4: 双重检查锁实现 (DCL)
# ============================================================================

class SingletonDCL:
    """
    双重检查锁定 (Double-Checked Locking) 实现
    
    经典的线程安全单例实现方式。
    性能优化版本,减少锁竞争。
    
    Example:
        >>> class Cache(SingletonDCL):
        ...     def __init__(self) -> None:
        ...         super().__init__()
        ...         self._data: dict[str, Any] = {}
        >>> 
        >>> cache1 = Cache()
        >>> cache2 = Cache()
        >>> assert cache1 is cache2
    
    Note:
        - 高性能: 仅在首次创建时加锁
        - 线程安全: 双重检查确保安全
        - 复杂度较高
    """
    
    _instances: ClassVar[dict[type, Any]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()
    
    def __new__(cls, *args: Any, **kwargs: Any) -> SingletonDCL:
        """
        双重检查锁定模式创建实例
        
        Returns:
            类的单例实例
        """
        # 第一次检查 (无锁)
        if cls not in cls._instances:
            # 加锁
            with cls._lock:
                # 第二次检查 (有锁)
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[cls] = instance
        
        return cls._instances[cls]
    
    @classmethod
    def _reset_instance(cls) -> None:
        """重置单例实例 (仅用于测试)"""
        with cls._lock:
            if cls in cls._instances:
                del cls._instances[cls]


# ============================================================================
# 实用工具类
# ============================================================================

class ConfigManager(metaclass=SingletonMeta):
    """
    配置管理器示例 - 使用元类单例
    
    全局配置管理,保证配置一致性。
    
    Example:
        >>> config = ConfigManager()
        >>> config.set("db_host", "localhost")
        >>> config.set("db_port", "5432")
        >>> 
        >>> # 在其他地方
        >>> config2 = ConfigManager()
        >>> print(config2.get("db_host"))
        localhost
    """
    
    def __init__(self) -> None:
        """初始化配置管理器"""
        if not hasattr(self, "_initialized"):
            self._config: dict[str, str] = {}
            self._lock = threading.Lock()
            self._initialized = True
    
    def set(self, key: str, value: str) -> None:
        """
        设置配置项
        
        Args:
            key: 配置键
            value: 配置值
        """
        with self._lock:
            self._config[key] = value
    
    def get(self, key: str, default: str | None = None) -> str | None:
        """
        获取配置项
        
        Args:
            key: 配置键
            default: 默认值
        
        Returns:
            配置值或默认值
        """
        with self._lock:
            return self._config.get(key, default)
    
    def has(self, key: str) -> bool:
        """
        检查配置是否存在
        
        Args:
            key: 配置键
        
        Returns:
            是否存在
        """
        with self._lock:
            return key in self._config
    
    def clear(self) -> None:
        """清空所有配置"""
        with self._lock:
            self._config.clear()
    
    def __repr__(self) -> str:
        """字符串表示"""
        with self._lock:
            return f"ConfigManager({len(self._config)} items)"


@singleton
class Logger:
    """
    日志管理器示例 - 使用装饰器单例
    
    全局日志管理,统一日志输出。
    
    Example:
        >>> logger = Logger()
        >>> logger.info("Application started")
        [INFO] Application started
        >>> 
        >>> # 在其他地方
        >>> logger2 = Logger()
        >>> logger2.error("An error occurred")
        [ERROR] An error occurred
        >>> assert logger is logger2
    """
    
    def __init__(self) -> None:
        """初始化日志管理器"""
        self.level = "INFO"
        self._logs: list[str] = []
    
    def _log(self, level: str, message: str) -> None:
        """内部日志方法"""
        log_entry = f"[{level}] {message}"
        self._logs.append(log_entry)
        print(log_entry)
    
    def info(self, message: str) -> None:
        """记录信息日志"""
        self._log("INFO", message)
    
    def warning(self, message: str) -> None:
        """记录警告日志"""
        self._log("WARNING", message)
    
    def error(self, message: str) -> None:
        """记录错误日志"""
        self._log("ERROR", message)
    
    def get_logs(self) -> list[str]:
        """获取所有日志"""
        return self._logs.copy()
    
    def clear_logs(self) -> None:
        """清空日志"""
        self._logs.clear()


# ============================================================================
# 模块级单例示例
# ============================================================================

class _GlobalConfig:
    """全局配置类 (内部使用)"""
    
    def __init__(self) -> None:
        self.version = "1.0.0"
        self.debug = False
        self.app_name = "Python2025"


# 模块级单例实例
global_config = _GlobalConfig()


# ============================================================================
# 测试工具函数
# ============================================================================

def is_singleton(cls: type, *args: Any, **kwargs: Any) -> bool:
    """
    测试一个类是否是单例
    
    Args:
        cls: 要测试的类
        *args: 实例化参数
        **kwargs: 实例化关键字参数
    
    Returns:
        是否为单例
    
    Example:
        >>> class MyClass(metaclass=SingletonMeta):
        ...     pass
        >>> assert is_singleton(MyClass)
    """
    try:
        obj1 = cls(*args, **kwargs)
        obj2 = cls(*args, **kwargs)
        return obj1 is obj2
    except Exception:
        return False


# ============================================================================
# 导出接口
# ============================================================================

__all__ = [
    # 元类
    "SingletonMeta",
    # 装饰器
    "singleton",
    # 基类
    "SingletonNew",
    "SingletonDCL",
    # 示例
    "ConfigManager",
    "Logger",
    "global_config",
    # 工具
    "is_singleton",
]

