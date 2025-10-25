"""
Factory Method Pattern (工厂方法模式)

创建型设计模式，定义创建对象的接口，让子类决定实例化哪个类。

主要组件:
- Product: 抽象产品接口
- ConcreteProduct: 具体产品实现
- Creator: 抽象创建者
- ConcreteCreator: 具体创建者

实现方式:
1. 经典ABC实现
2. Protocol实现
3. 函数式实现
4. 注册表模式（推荐）
5. 泛型实现

版本: 1.0.0
Python版本: 3.12+
"""

from .factory_method import (
    # 抽象基类实现
    Product,
    Creator,
    ConcreteProductA,
    ConcreteProductB,
    ConcreteCreatorA,
    ConcreteCreatorB,
    # Protocol实现
    ProductProtocol,
    CreatorProtocol,
    ProtocolProductA,
    ProtocolProductB,
    ProtocolCreatorA,
    # 函数式实现
    FunctionalProduct,
    create_product_factory,
    functional_factory_method,
    # 注册表实现
    FactoryRegistry,
    RegistryProductA,
    RegistryProductB,
    FactoryError,
    UnknownProductError,
    # 泛型实现
    GenericFactory,
    CachedGenericFactory,
    GenericProduct,
    # 配置化实现
    ConfigurableFactory,
    FactoryConfig,
    # 工具函数
    factory_timer,
    factory_logger,
)

__version__ = "1.0.0"
__author__ = "Python 2025 Project"
__all__ = [
    # 抽象基类
    "Product",
    "Creator",
    "ConcreteProductA",
    "ConcreteProductB",
    "ConcreteCreatorA",
    "ConcreteCreatorB",
    # Protocol
    "ProductProtocol",
    "CreatorProtocol",
    "ProtocolProductA",
    "ProtocolProductB",
    "ProtocolCreatorA",
    # 函数式
    "FunctionalProduct",
    "create_product_factory",
    "functional_factory_method",
    # 注册表
    "FactoryRegistry",
    "RegistryProductA",
    "RegistryProductB",
    "FactoryError",
    "UnknownProductError",
    # 泛型
    "GenericFactory",
    "CachedGenericFactory",
    "GenericProduct",
    # 配置化
    "ConfigurableFactory",
    "FactoryConfig",
    # 工具
    "factory_timer",
    "factory_logger",
]

