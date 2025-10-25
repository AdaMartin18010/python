"""
Abstract Factory Pattern (抽象工厂模式)

创建型设计模式，提供创建产品族的接口。

版本: 1.0.0
Python版本: 3.12+
"""

from .abstract_factory import (
    # 抽象基类
    AbstractProductA,
    AbstractProductB,
    AbstractFactory,
    ConcreteProductA1,
    ConcreteProductA2,
    ConcreteProductB1,
    ConcreteProductB2,
    ConcreteFactory1,
    ConcreteFactory2,
    # Protocol
    ProductAProtocol,
    ProductBProtocol,
    FactoryProtocol,
    ProtocolProductA1,
    ProtocolProductB1,
    ProtocolFactory1,
    # 函数式
    ProductFamily,
    create_factory_function,
    functional_factory,
    # 注册表
    FactoryRegistry,
    RegistryFactory1,
    RegistryFactory2,
    FactoryError,
    UnknownFactoryError,
    # 泛型
    GenericFactory,
    CachedGenericFactory,
    # 客户端
    client_code,
)

__version__ = "1.0.0"
__all__ = [
    "AbstractProductA",
    "AbstractProductB",
    "AbstractFactory",
    "ConcreteFactory1",
    "ConcreteFactory2",
    "FactoryRegistry",
    "GenericFactory",
    "client_code",
]

