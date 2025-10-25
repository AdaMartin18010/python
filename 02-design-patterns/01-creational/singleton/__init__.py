"""
Singleton Pattern (单例模式)

本模块提供多种Python单例模式实现方式。

导出:
    - SingletonMeta: 元类单例
    - singleton: 装饰器单例
    - SingletonNew: __new__方式单例
    - SingletonDCL: 双重检查锁单例
    - ConfigManager: 配置管理器示例
    - Logger: 日志管理器示例
    - global_config: 模块级单例示例
    - is_singleton: 单例验证工具

Example:
    >>> from singleton import SingletonMeta
    >>> class MyClass(metaclass=SingletonMeta):
    ...     pass
    >>> obj1 = MyClass()
    >>> obj2 = MyClass()
    >>> assert obj1 is obj2
"""

from .singleton import (
    ConfigManager,
    Logger,
    SingletonDCL,
    SingletonMeta,
    SingletonNew,
    global_config,
    is_singleton,
    singleton,
)

__all__ = [
    "SingletonMeta",
    "singleton",
    "SingletonNew",
    "SingletonDCL",
    "ConfigManager",
    "Logger",
    "global_config",
    "is_singleton",
]

__version__ = "1.0.0"
__author__ = "Python 2025 Knowledge Base Team"

