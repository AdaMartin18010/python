"""
Abstract Factory Pattern - 抽象工厂模式

提供5种Python实现方式：
1. 经典ABC实现
2. Protocol实现
3. 函数式实现  
4. 注册表模式（推荐）
5. 泛型实现
"""

from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, Generic, Any, Callable, NamedTuple
from dataclasses import dataclass
from enum import Enum
import threading


# ============================================================================
# 1. 经典实现：使用抽象基类(ABC)
# ============================================================================


class AbstractProductA(ABC):
    """抽象产品A"""

    @abstractmethod
    def operation_a(self) -> str:
        """产品A的操作"""
        pass

    @abstractmethod
    def get_info(self) -> dict[str, Any]:
        """获取产品信息"""
        pass


class AbstractProductB(ABC):
    """抽象产品B"""

    @abstractmethod
    def operation_b(self) -> str:
        """产品B的操作"""
        pass

    @abstractmethod
    def collaborate_with_a(self, collaborator: AbstractProductA) -> str:
        """与产品A协作"""
        pass

    @abstractmethod
    def get_info(self) -> dict[str, Any]:
        """获取产品信息"""
        pass


# 具体产品：产品族1


class ConcreteProductA1(AbstractProductA):
    """具体产品A1"""

    def operation_a(self) -> str:
        return "产品A1的操作结果"

    def get_info(self) -> dict[str, Any]:
        return {"name": "Product A1", "family": "family1", "type": "A"}


class ConcreteProductB1(AbstractProductB):
    """具体产品B1"""

    def operation_b(self) -> str:
        return "产品B1的操作结果"

    def collaborate_with_a(self, collaborator: AbstractProductA) -> str:
        result_a = collaborator.operation_a()
        return f"产品B1与({result_a})协作"

    def get_info(self) -> dict[str, Any]:
        return {"name": "Product B1", "family": "family1", "type": "B"}


# 具体产品：产品族2


class ConcreteProductA2(AbstractProductA):
    """具体产品A2"""

    def operation_a(self) -> str:
        return "产品A2的操作结果"

    def get_info(self) -> dict[str, Any]:
        return {"name": "Product A2", "family": "family2", "type": "A"}


class ConcreteProductB2(AbstractProductB):
    """具体产品B2"""

    def operation_b(self) -> str:
        return "产品B2的操作结果"

    def collaborate_with_a(self, collaborator: AbstractProductA) -> str:
        result_a = collaborator.operation_a()
        return f"产品B2与({result_a})协作"

    def get_info(self) -> dict[str, Any]:
        return {"name": "Product B2", "family": "family2", "type": "B"}


# 抽象工厂


class AbstractFactory(ABC):
    """抽象工厂：创建产品族"""

    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        """创建产品A"""
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        """创建产品B"""
        pass

    def create_product_family(self) -> tuple[AbstractProductA, AbstractProductB]:
        """创建整个产品族"""
        return (self.create_product_a(), self.create_product_b())


# 具体工厂


class ConcreteFactory1(AbstractFactory):
    """具体工厂1：创建产品族1"""

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()


class ConcreteFactory2(AbstractFactory):
    """具体工厂2：创建产品族2"""

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()


# ============================================================================
# 2. Protocol实现：结构化类型（鸭子类型）
# ============================================================================


class ProductAProtocol(Protocol):
    """产品A协议"""

    def operation_a(self) -> str: ...

    def get_info(self) -> dict[str, Any]: ...


class ProductBProtocol(Protocol):
    """产品B协议"""

    def operation_b(self) -> str: ...

    def collaborate_with_a(self, collaborator: ProductAProtocol) -> str: ...

    def get_info(self) -> dict[str, Any]: ...


class FactoryProtocol(Protocol):
    """工厂协议"""

    def create_product_a(self) -> ProductAProtocol: ...

    def create_product_b(self) -> ProductBProtocol: ...


# Protocol产品实现（不需要继承）


class ProtocolProductA1:
    """基于Protocol的产品A1"""

    def operation_a(self) -> str:
        return "Protocol产品A1的操作"

    def get_info(self) -> dict[str, Any]:
        return {"name": "Protocol Product A1", "protocol": True}


class ProtocolProductB1:
    """基于Protocol的产品B1"""

    def operation_b(self) -> str:
        return "Protocol产品B1的操作"

    def collaborate_with_a(self, collaborator: ProductAProtocol) -> str:
        return f"Protocol B1与{collaborator.operation_a()}协作"

    def get_info(self) -> dict[str, Any]:
        return {"name": "Protocol Product B1", "protocol": True}


class ProtocolFactory1:
    """基于Protocol的工厂1"""

    def create_product_a(self) -> ProductAProtocol:
        return ProtocolProductA1()

    def create_product_b(self) -> ProductBProtocol:
        return ProtocolProductB1()


# ============================================================================
# 3. 函数式实现：使用函数和闭包
# ============================================================================


class ProductFamily(NamedTuple):
    """产品族数据结构"""

    product_a: Any
    product_b: Any
    family_name: str


def create_factory_function(
    family: str,
) -> Callable[[], ProductFamily]:
    """
    函数式工厂：返回创建产品族的函数

    Args:
        family: 产品族名称

    Returns:
        创建产品族的工厂函数
    """
    factories = {
        "family1": lambda: ProductFamily(
            product_a=ConcreteProductA1(),
            product_b=ConcreteProductB1(),
            family_name="family1",
        ),
        "family2": lambda: ProductFamily(
            product_a=ConcreteProductA2(),
            product_b=ConcreteProductB2(),
            family_name="family2",
        ),
    }

    factory = factories.get(family)
    if not factory:
        raise ValueError(
            f"未知的产品族: {family}. " f"可用族: {list(factories.keys())}"
        )

    return factory


def functional_factory(family: str) -> ProductFamily:
    """简化版函数式工厂"""
    factory = create_factory_function(family)
    return factory()


# ============================================================================
# 4. 注册表模式（推荐⭐）：自动注册和管理工厂
# ============================================================================


class FactoryError(Exception):
    """工厂相关错误"""

    pass


class UnknownFactoryError(FactoryError):
    """未知工厂错误"""

    pass


class FactoryRegistry:
    """
    工厂注册表：管理所有抽象工厂

    特点：
    - 支持装饰器注册
    - 自动管理工厂类型
    - 支持插件式扩展
    - 线程安全
    """

    _factories: dict[str, type[AbstractFactory]] = {}
    _lock = threading.RLock()

    @classmethod
    def register(cls, name: str):
        """
        注册工厂装饰器

        Args:
            name: 工厂名称

        Returns:
            装饰器函数
        """

        def decorator(factory_class: type[AbstractFactory]) -> type[AbstractFactory]:
            with cls._lock:
                if name in cls._factories:
                    raise FactoryError(f"工厂 '{name}' 已经注册")
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
    def get_factory(cls, name: str, *args: Any, **kwargs: Any) -> AbstractFactory:
        """
        获取工厂实例

        Args:
            name: 工厂名称
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            工厂实例

        Raises:
            UnknownFactoryError: 未注册的工厂
        """
        with cls._lock:
            factory_class = cls._factories.get(name)
            if not factory_class:
                available = list(cls._factories.keys())
                raise UnknownFactoryError(
                    f"未注册的工厂: '{name}'. " f"可用工厂: {available}"
                )

        try:
            return factory_class(*args, **kwargs)
        except Exception as e:
            raise FactoryError(f"创建工厂 '{name}' 失败: {e}") from e

    @classmethod
    def list_factories(cls) -> list[str]:
        """列出所有已注册的工厂"""
        with cls._lock:
            return list(cls._factories.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """检查工厂是否已注册"""
        with cls._lock:
            return name in cls._factories

    @classmethod
    def clear(cls) -> None:
        """清空所有注册（主要用于测试）"""
        with cls._lock:
            cls._factories.clear()


# 使用注册表注册工厂


@FactoryRegistry.register("registry_factory1")
class RegistryFactory1(AbstractFactory):
    """注册表工厂1"""

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()


@FactoryRegistry.register("registry_factory2")
class RegistryFactory2(AbstractFactory):
    """注册表工厂2"""

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()


# ============================================================================
# 5. 泛型实现（Python 3.12+）
# ============================================================================

PA = TypeVar("PA", bound=AbstractProductA)
PB = TypeVar("PB", bound=AbstractProductB)


class GenericFactory(Generic[PA, PB]):
    """
    泛型工厂：类型安全的抽象工厂

    Args:
        product_a_class: 产品A的类
        product_b_class: 产品B的类
    """

    def __init__(self, product_a_class: type[PA], product_b_class: type[PB]):
        self._product_a_class = product_a_class
        self._product_b_class = product_b_class

    def create_product_a(self) -> PA:
        """创建产品A"""
        return self._product_a_class()

    def create_product_b(self) -> PB:
        """创建产品B"""
        return self._product_b_class()

    def create_product_family(self) -> tuple[PA, PB]:
        """创建整个产品族"""
        return (self.create_product_a(), self.create_product_b())

    def get_product_classes(self) -> tuple[type[PA], type[PB]]:
        """获取产品类"""
        return (self._product_a_class, self._product_b_class)


class CachedGenericFactory(Generic[PA, PB]):
    """
    带缓存的泛型工厂

    特点：
    - 缓存已创建的产品
    - 支持产品族单例
    - 线程安全
    """

    def __init__(
        self,
        product_a_class: type[PA],
        product_b_class: type[PB],
        cache_enabled: bool = True,
    ):
        self._product_a_class = product_a_class
        self._product_b_class = product_b_class
        self._cache_enabled = cache_enabled
        self._cache_a: dict[str, PA] = {}
        self._cache_b: dict[str, PB] = {}
        self._lock = threading.Lock()

    def create_product_a(self, cache_key: str | None = None) -> PA:
        """创建或获取缓存的产品A"""
        if not self._cache_enabled or cache_key is None:
            return self._product_a_class()

        with self._lock:
            if cache_key not in self._cache_a:
                self._cache_a[cache_key] = self._product_a_class()
            return self._cache_a[cache_key]

    def create_product_b(self, cache_key: str | None = None) -> PB:
        """创建或获取缓存的产品B"""
        if not self._cache_enabled or cache_key is None:
            return self._product_b_class()

        with self._lock:
            if cache_key not in self._cache_b:
                self._cache_b[cache_key] = self._product_b_class()
            return self._cache_b[cache_key]

    def clear_cache(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache_a.clear()
            self._cache_b.clear()

    def get_cache_size(self) -> tuple[int, int]:
        """获取缓存大小 (产品A数量, 产品B数量)"""
        with self._lock:
            return (len(self._cache_a), len(self._cache_b))


# ============================================================================
# 客户端代码示例
# ============================================================================


def client_code(factory: AbstractFactory) -> None:
    """
    客户端代码：使用抽象工厂

    注意：客户端只依赖抽象接口，不依赖具体实现
    """
    product_a = factory.create_product_a()
    product_b = factory.create_product_b()

    print(f"产品A: {product_a.operation_a()}")
    print(f"产品B: {product_b.operation_b()}")
    print(f"产品B与A协作: {product_b.collaborate_with_a(product_a)}")

    # 验证产品族一致性
    info_a = product_a.get_info()
    info_b = product_b.get_info()
    if info_a.get("family") == info_b.get("family"):
        print(f"✅ 产品族一致: {info_a.get('family')}")
    else:
        print(f"❌ 产品族不一致!")


# ============================================================================
# 对外接口
# ============================================================================

__all__ = [
    # 抽象基类
    "AbstractProductA",
    "AbstractProductB",
    "AbstractFactory",
    "ConcreteProductA1",
    "ConcreteProductA2",
    "ConcreteProductB1",
    "ConcreteProductB2",
    "ConcreteFactory1",
    "ConcreteFactory2",
    # Protocol
    "ProductAProtocol",
    "ProductBProtocol",
    "FactoryProtocol",
    "ProtocolProductA1",
    "ProtocolProductB1",
    "ProtocolFactory1",
    # 函数式
    "ProductFamily",
    "create_factory_function",
    "functional_factory",
    # 注册表
    "FactoryRegistry",
    "RegistryFactory1",
    "RegistryFactory2",
    "FactoryError",
    "UnknownFactoryError",
    # 泛型
    "GenericFactory",
    "CachedGenericFactory",
    # 客户端
    "client_code",
]


if __name__ == "__main__":
    print("=" * 70)
    print("Abstract Factory Pattern - 演示")
    print("=" * 70)

    # 1. 经典实现
    print("\n1️⃣  经典ABC实现:")
    factory1 = ConcreteFactory1()
    client_code(factory1)

    print("\n   切换产品族:")
    factory2 = ConcreteFactory2()
    client_code(factory2)

    # 2. Protocol实现
    print("\n2️⃣  Protocol实现:")
    protocol_factory = ProtocolFactory1()
    product_a = protocol_factory.create_product_a()
    product_b = protocol_factory.create_product_b()
    print(f"产品A: {product_a.operation_a()}")
    print(f"产品B: {product_b.operation_b()}")

    # 3. 函数式实现
    print("\n3️⃣  函数式实现:")
    family = functional_factory("family1")
    print(f"产品族: {family.family_name}")
    print(f"产品A: {family.product_a.operation_a()}")
    print(f"产品B: {family.product_b.operation_b()}")

    # 4. 注册表模式
    print("\n4️⃣  注册表模式:")
    print(f"已注册工厂: {FactoryRegistry.list_factories()}")
    registry_factory = FactoryRegistry.get_factory("registry_factory1")
    client_code(registry_factory)

    # 5. 泛型实现
    print("\n5️⃣  泛型实现:")
    generic_factory = GenericFactory(ConcreteProductA1, ConcreteProductB1)
    product_a, product_b = generic_factory.create_product_family()
    print(f"产品A: {product_a.operation_a()}")
    print(f"产品B: {product_b.operation_b()}")

    print("\n" + "=" * 70)
    print("✅ 所有实现演示完成！")
    print("=" * 70)

