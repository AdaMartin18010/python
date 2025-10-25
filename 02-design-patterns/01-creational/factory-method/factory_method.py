"""
Factory Method Pattern - 工厂方法模式

提供5种Python实现方式：
1. 经典ABC实现
2. Protocol实现
3. 函数式实现
4. 注册表模式（推荐）
5. 泛型实现
"""

from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, Generic, Any, Callable
from dataclasses import dataclass
import threading
from functools import wraps


# ============================================================================
# 1. 经典实现：使用抽象基类(ABC)
# ============================================================================


class Product(ABC):
    """抽象产品接口"""

    @abstractmethod
    def operation(self) -> str:
        """产品的核心操作"""
        pass

    @abstractmethod
    def get_info(self) -> dict[str, Any]:
        """获取产品信息"""
        pass


class ConcreteProductA(Product):
    """具体产品A"""

    def operation(self) -> str:
        return "产品A的操作结果"

    def get_info(self) -> dict[str, Any]:
        return {
            "name": "Product A",
            "type": "concrete",
            "version": "1.0",
        }


class ConcreteProductB(Product):
    """具体产品B"""

    def operation(self) -> str:
        return "产品B的操作结果"

    def get_info(self) -> dict[str, Any]:
        return {
            "name": "Product B",
            "type": "concrete",
            "version": "2.0",
        }


class Creator(ABC):
    """抽象创建者"""

    @abstractmethod
    def factory_method(self) -> Product:
        """工厂方法：由子类实现具体的产品创建"""
        pass

    def some_operation(self) -> str:
        """
        业务逻辑：使用工厂方法创建产品
        注意：创建者的主要职责不是创建产品，而是包含依赖产品的核心业务逻辑
        """
        product = self.factory_method()
        result = f"Creator: 使用 {product.operation()}"
        return result


class ConcreteCreatorA(Creator):
    """具体创建者A：创建产品A"""

    def factory_method(self) -> Product:
        return ConcreteProductA()


class ConcreteCreatorB(Creator):
    """具体创建者B：创建产品B"""

    def factory_method(self) -> Product:
        return ConcreteProductB()


# ============================================================================
# 2. Protocol实现：结构化类型（鸭子类型）
# ============================================================================


class ProductProtocol(Protocol):
    """产品协议：定义产品应该有的行为"""

    def operation(self) -> str: ...

    def get_info(self) -> dict[str, Any]: ...


class CreatorProtocol(Protocol):
    """创建者协议"""

    def factory_method(self) -> ProductProtocol: ...

    def some_operation(self) -> str: ...


class ProtocolProductA:
    """基于Protocol的产品A（不需要继承）"""

    def operation(self) -> str:
        return "Protocol产品A的操作"

    def get_info(self) -> dict[str, Any]:
        return {"name": "Protocol Product A", "protocol": True}


class ProtocolProductB:
    """基于Protocol的产品B"""

    def operation(self) -> str:
        return "Protocol产品B的操作"

    def get_info(self) -> dict[str, Any]:
        return {"name": "Protocol Product B", "protocol": True}


class ProtocolCreatorA:
    """基于Protocol的创建者A"""

    def factory_method(self) -> ProductProtocol:
        return ProtocolProductA()

    def some_operation(self) -> str:
        product = self.factory_method()
        return f"ProtocolCreator: {product.operation()}"


# ============================================================================
# 3. 函数式实现：使用函数和闭包
# ============================================================================


@dataclass
class FunctionalProduct:
    """函数式产品的数据类"""

    name: str
    operation_func: Callable[[], str]

    def operation(self) -> str:
        return self.operation_func()

    def get_info(self) -> dict[str, Any]:
        return {"name": self.name, "type": "functional"}


def create_product_factory(product_type: str) -> Callable[[], FunctionalProduct]:
    """
    函数式工厂：返回一个创建产品的函数
    
    Args:
        product_type: 产品类型
        
    Returns:
        创建产品的工厂函数
    """
    factories = {
        "type_a": lambda: FunctionalProduct(
            name="Functional Product A", operation_func=lambda: "函数式产品A的操作"
        ),
        "type_b": lambda: FunctionalProduct(
            name="Functional Product B", operation_func=lambda: "函数式产品B的操作"
        ),
        "type_c": lambda: FunctionalProduct(
            name="Functional Product C", operation_func=lambda: "函数式产品C的操作"
        ),
    }

    factory = factories.get(product_type)
    if not factory:
        raise ValueError(
            f"未知的产品类型: {product_type}. "
            f"可用类型: {list(factories.keys())}"
        )

    return factory


def functional_factory_method(product_type: str) -> FunctionalProduct:
    """简化版函数式工厂"""
    factory = create_product_factory(product_type)
    return factory()


# ============================================================================
# 4. 注册表模式（推荐⭐）：自动注册和管理工厂
# ============================================================================


class FactoryError(Exception):
    """工厂相关错误"""

    pass


class UnknownProductError(FactoryError):
    """未知产品错误"""

    pass


class FactoryRegistry:
    """
    工厂注册表：管理所有产品工厂
    
    特点：
    - 支持装饰器注册
    - 自动管理产品类型
    - 支持插件式扩展
    - 线程安全
    """

    _factories: dict[str, type] = {}
    _lock = threading.RLock()

    @classmethod
    def register(cls, name: str):
        """
        注册工厂装饰器
        
        Args:
            name: 产品类型名称
            
        Returns:
            装饰器函数
            
        Example:
            @FactoryRegistry.register("mysql")
            class MySQLConnection:
                pass
        """

        def decorator(factory_class: type) -> type:
            with cls._lock:
                if name in cls._factories:
                    raise FactoryError(f"产品类型 '{name}' 已经注册")
                cls._factories[name] = factory_class
            return factory_class

        return decorator

    @classmethod
    def unregister(cls, name: str) -> None:
        """注销工厂"""
        with cls._lock:
            if name in cls._factories:
                del cls._factories[name]

    @classmethod
    def create(cls, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        创建产品实例
        
        Args:
            name: 产品类型名称
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            产品实例
            
        Raises:
            UnknownProductError: 未注册的产品类型
            FactoryError: 创建失败
        """
        with cls._lock:
            factory = cls._factories.get(name)
            if not factory:
                available = list(cls._factories.keys())
                raise UnknownProductError(
                    f"未注册的产品类型: '{name}'. " f"可用类型: {available}"
                )

        try:
            return factory(*args, **kwargs)
        except Exception as e:
            raise FactoryError(f"创建产品 '{name}' 失败: {e}") from e

    @classmethod
    def list_products(cls) -> list[str]:
        """列出所有已注册的产品类型"""
        with cls._lock:
            return list(cls._factories.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """检查产品类型是否已注册"""
        with cls._lock:
            return name in cls._factories

    @classmethod
    def clear(cls) -> None:
        """清空所有注册（主要用于测试）"""
        with cls._lock:
            cls._factories.clear()


# 使用注册表注册产品


@FactoryRegistry.register("registry_product_a")
class RegistryProductA:
    """注册表产品A"""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}

    def operation(self) -> str:
        return f"注册表产品A的操作 (config: {self.config})"

    def get_info(self) -> dict[str, Any]:
        return {
            "name": "Registry Product A",
            "type": "registry",
            "config": self.config,
        }


@FactoryRegistry.register("registry_product_b")
class RegistryProductB:
    """注册表产品B"""

    def __init__(self, version: str = "1.0"):
        self.version = version

    def operation(self) -> str:
        return f"注册表产品B的操作 (version: {self.version})"

    def get_info(self) -> dict[str, Any]:
        return {
            "name": "Registry Product B",
            "type": "registry",
            "version": self.version,
        }


# ============================================================================
# 5. 泛型实现（Python 3.12+）
# ============================================================================

T = TypeVar("T")


class GenericProduct(Protocol):
    """泛型产品协议"""

    def operation(self) -> str: ...

    def get_info(self) -> dict[str, Any]: ...


class GenericFactory(Generic[T]):
    """
    泛型工厂：类型安全的产品创建
    
    Args:
        product_class: 产品类
        
    Example:
        factory = GenericFactory(ConcreteProductA)
        product = factory.create()
    """

    def __init__(self, product_class: type[T]):
        self._product_class = product_class

    def create(self, *args: Any, **kwargs: Any) -> T:
        """创建产品实例"""
        return self._product_class(*args, **kwargs)

    def get_product_class(self) -> type[T]:
        """获取产品类"""
        return self._product_class


class CachedGenericFactory(Generic[T]):
    """
    带缓存的泛型工厂
    
    特点：
    - 缓存已创建的实例
    - 支持单例模式
    - 线程安全
    """

    def __init__(self, product_class: type[T], cache_enabled: bool = True):
        self._product_class = product_class
        self._cache_enabled = cache_enabled
        self._cache: dict[str, T] = {}
        self._lock = threading.Lock()

    def create(self, cache_key: str | None = None, *args: Any, **kwargs: Any) -> T:
        """
        创建或获取缓存的产品实例
        
        Args:
            cache_key: 缓存键，如果为None则不缓存
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            产品实例
        """
        if not self._cache_enabled or cache_key is None:
            return self._product_class(*args, **kwargs)

        with self._lock:
            if cache_key not in self._cache:
                self._cache[cache_key] = self._product_class(*args, **kwargs)
            return self._cache[cache_key]

    def clear_cache(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()

    def get_cache_size(self) -> int:
        """获取缓存大小"""
        with self._lock:
            return len(self._cache)


# ============================================================================
# 实用工具函数
# ============================================================================


def factory_timer(func: Callable) -> Callable:
    """
    工厂计时装饰器：测量产品创建时间
    
    Example:
        @factory_timer
        def create_product():
            return Product()
    """
    import time

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = (end_time - start_time) * 1000  # 转换为毫秒

        print(f"⏱️  工厂方法 '{func.__name__}' 耗时: {elapsed:.4f}ms")
        return result

    return wrapper


def factory_logger(func: Callable) -> Callable:
    """
    工厂日志装饰器：记录产品创建日志
    
    Example:
        @factory_logger
        def create_product(name: str):
            return Product(name)
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"📝 开始创建产品: {func.__name__}")
        print(f"   参数: args={args}, kwargs={kwargs}")

        try:
            result = func(*args, **kwargs)
            print(f"✅ 产品创建成功: {result}")
            return result
        except Exception as e:
            print(f"❌ 产品创建失败: {e}")
            raise

    return wrapper


# ============================================================================
# 配置化工厂
# ============================================================================


@dataclass
class FactoryConfig:
    """工厂配置"""

    product_class: str
    default_params: dict[str, Any]
    enabled: bool = True
    cache: bool = False


class ConfigurableFactory:
    """
    配置化工厂：从配置创建产品
    
    Example:
        config = {
            "mysql": FactoryConfig(
                product_class="MySQLConnection",
                default_params={"port": 3306}
            )
        }
        factory = ConfigurableFactory(config)
        conn = factory.create("mysql", host="localhost")
    """

    def __init__(self, config: dict[str, FactoryConfig]):
        self.config = config
        self._cache: dict[str, Any] = {}

    def create(self, product_type: str, **kwargs: Any) -> Any:
        """创建产品"""
        if product_type not in self.config:
            raise UnknownProductError(
                f"未配置的产品类型: {product_type}. "
                f"可用类型: {list(self.config.keys())}"
            )

        cfg = self.config[product_type]

        if not cfg.enabled:
            raise FactoryError(f"产品类型 '{product_type}' 已禁用")

        # 检查缓存
        if cfg.cache and product_type in self._cache:
            return self._cache[product_type]

        # 合并参数
        params = {**cfg.default_params, **kwargs}

        # 创建产品
        try:
            # 这里简化处理，实际应该通过模块导入
            product_class = globals().get(cfg.product_class)
            if not product_class:
                raise FactoryError(f"找不到产品类: {cfg.product_class}")

            product = product_class(**params)

            # 缓存
            if cfg.cache:
                self._cache[product_type] = product

            return product
        except Exception as e:
            raise FactoryError(f"创建产品失败: {e}") from e


# ============================================================================
# 对外接口
# ============================================================================

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


if __name__ == "__main__":
    print("=" * 70)
    print("Factory Method Pattern - 演示")
    print("=" * 70)

    # 1. 经典实现
    print("\n1️⃣  经典ABC实现:")
    creator_a = ConcreteCreatorA()
    print(creator_a.some_operation())

    # 2. Protocol实现
    print("\n2️⃣  Protocol实现:")
    protocol_creator = ProtocolCreatorA()
    print(protocol_creator.some_operation())

    # 3. 函数式实现
    print("\n3️⃣  函数式实现:")
    product = functional_factory_method("type_a")
    print(product.operation())

    # 4. 注册表模式
    print("\n4️⃣  注册表模式:")
    print(f"已注册产品: {FactoryRegistry.list_products()}")
    registry_product = FactoryRegistry.create(
        "registry_product_a", config={"env": "production"}
    )
    print(registry_product.operation())

    # 5. 泛型实现
    print("\n5️⃣  泛型实现:")
    generic_factory = GenericFactory(ConcreteProductA)
    generic_product = generic_factory.create()
    print(generic_product.operation())

    print("\n" + "=" * 70)
    print("✅ 所有实现演示完成！")
    print("=" * 70)

