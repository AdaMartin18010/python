"""
Factory Method Pattern - 完整测试套件

测试所有实现方式的正确性、线程安全性和边界条件
"""

import pytest
import threading
import time
from typing import Any

import sys
from pathlib import Path

# 添加父目录到路径以导入factory_method模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from factory_method import (
    # 经典实现
    Product,
    Creator,
    ConcreteProductA,
    ConcreteProductB,
    ConcreteCreatorA,
    ConcreteCreatorB,
    # Protocol实现
    ProductProtocol,
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
    # 配置化实现
    ConfigurableFactory,
    FactoryConfig,
    # 工具
    factory_timer,
    factory_logger,
)


# ============================================================================
# 测试: 经典ABC实现
# ============================================================================


class TestClassicImplementation:
    """测试经典ABC实现"""

    def test_concrete_product_a(self):
        """测试具体产品A"""
        product = ConcreteProductA()
        assert isinstance(product, Product)
        assert "产品A" in product.operation()
        info = product.get_info()
        assert info["name"] == "Product A"
        assert info["type"] == "concrete"

    def test_concrete_product_b(self):
        """测试具体产品B"""
        product = ConcreteProductB()
        assert isinstance(product, Product)
        assert "产品B" in product.operation()
        info = product.get_info()
        assert info["name"] == "Product B"

    def test_creator_a(self):
        """测试创建者A"""
        creator = ConcreteCreatorA()
        assert isinstance(creator, Creator)

        product = creator.factory_method()
        assert isinstance(product, ConcreteProductA)

        result = creator.some_operation()
        assert "产品A" in result

    def test_creator_b(self):
        """测试创建者B"""
        creator = ConcreteCreatorB()
        assert isinstance(creator, Creator)

        product = creator.factory_method()
        assert isinstance(product, ConcreteProductB)

        result = creator.some_operation()
        assert "产品B" in result

    def test_polymorphism(self):
        """测试多态性"""
        creators: list[Creator] = [ConcreteCreatorA(), ConcreteCreatorB()]

        results = []
        for creator in creators:
            result = creator.some_operation()
            results.append(result)

        assert len(results) == 2
        assert "产品A" in results[0]
        assert "产品B" in results[1]

    def test_abstract_instantiation(self):
        """测试抽象类不能直接实例化"""
        with pytest.raises(TypeError):
            Product()  # type: ignore

        with pytest.raises(TypeError):
            Creator()  # type: ignore


# ============================================================================
# 测试: Protocol实现
# ============================================================================


class TestProtocolImplementation:
    """测试Protocol实现"""

    def test_protocol_product_a(self):
        """测试Protocol产品A"""
        product = ProtocolProductA()
        assert "Protocol产品A" in product.operation()
        info = product.get_info()
        assert info["protocol"] is True

    def test_protocol_product_b(self):
        """测试Protocol产品B"""
        product = ProtocolProductB()
        assert "Protocol产品B" in product.operation()

    def test_protocol_creator(self):
        """测试Protocol创建者"""
        creator = ProtocolCreatorA()
        product = creator.factory_method()
        assert isinstance(product, ProtocolProductA)

        result = creator.some_operation()
        assert "Protocol产品A" in result

    def test_duck_typing(self):
        """测试鸭子类型"""

        # 创建一个不继承Protocol的类，但实现了所需方法
        class DuckProduct:
            def operation(self) -> str:
                return "鸭子类型产品"

            def get_info(self) -> dict[str, Any]:
                return {"duck": True}

        # 应该可以作为ProductProtocol使用
        product = DuckProduct()
        assert product.operation() == "鸭子类型产品"
        assert product.get_info()["duck"] is True


# ============================================================================
# 测试: 函数式实现
# ============================================================================


class TestFunctionalImplementation:
    """测试函数式实现"""

    def test_functional_product(self):
        """测试函数式产品"""
        product = FunctionalProduct(
            name="Test Product", operation_func=lambda: "测试操作"
        )
        assert product.operation() == "测试操作"
        assert product.get_info()["name"] == "Test Product"

    def test_create_product_factory(self):
        """测试创建产品工厂"""
        factory_a = create_product_factory("type_a")
        product = factory_a()
        assert isinstance(product, FunctionalProduct)
        assert "函数式产品A" in product.operation()

    def test_all_product_types(self):
        """测试所有产品类型"""
        for product_type in ["type_a", "type_b", "type_c"]:
            factory = create_product_factory(product_type)
            product = factory()
            assert isinstance(product, FunctionalProduct)

    def test_unknown_product_type(self):
        """测试未知产品类型"""
        with pytest.raises(ValueError, match="未知的产品类型"):
            create_product_factory("unknown_type")

    def test_functional_factory_method(self):
        """测试函数式工厂方法"""
        product = functional_factory_method("type_a")
        assert isinstance(product, FunctionalProduct)

    def test_factory_closure(self):
        """测试工厂闭包"""

        def custom_factory_creator(prefix: str):
            def factory():
                return FunctionalProduct(
                    name=f"{prefix} Product",
                    operation_func=lambda: f"{prefix} 操作",
                )

            return factory

        factory = custom_factory_creator("Custom")
        product = factory()
        assert "Custom Product" in product.get_info()["name"]
        assert "Custom 操作" in product.operation()


# ============================================================================
# 测试: 注册表模式
# ============================================================================


class TestFactoryRegistry:
    """测试注册表模式"""

    def setup_method(self):
        """每个测试前清空注册表"""
        # 保存原有注册
        self.original_factories = FactoryRegistry._factories.copy()

    def teardown_method(self):
        """每个测试后恢复注册表"""
        FactoryRegistry._factories = self.original_factories

    def test_registry_product_a(self):
        """测试注册表产品A"""
        product = FactoryRegistry.create("registry_product_a")
        assert isinstance(product, RegistryProductA)
        assert "注册表产品A" in product.operation()

    def test_registry_product_b(self):
        """测试注册表产品B"""
        product = FactoryRegistry.create("registry_product_b", version="2.0")
        assert isinstance(product, RegistryProductB)
        assert "2.0" in product.operation()

    def test_list_products(self):
        """测试列出所有产品"""
        products = FactoryRegistry.list_products()
        assert "registry_product_a" in products
        assert "registry_product_b" in products

    def test_is_registered(self):
        """测试检查产品是否已注册"""
        assert FactoryRegistry.is_registered("registry_product_a")
        assert not FactoryRegistry.is_registered("non_existent")

    def test_unknown_product_error(self):
        """测试未知产品错误"""
        with pytest.raises(UnknownProductError, match="未注册的产品类型"):
            FactoryRegistry.create("unknown_product")

    def test_register_decorator(self):
        """测试注册装饰器"""

        @FactoryRegistry.register("test_product")
        class TestProduct:
            def __init__(self, value: int):
                self.value = value

        assert FactoryRegistry.is_registered("test_product")
        product = FactoryRegistry.create("test_product", value=42)
        assert product.value == 42

        # 清理
        FactoryRegistry.unregister("test_product")

    def test_duplicate_registration(self):
        """测试重复注册"""
        FactoryRegistry.clear()

        @FactoryRegistry.register("duplicate")
        class Product1:
            pass

        with pytest.raises(FactoryError, match="已经注册"):

            @FactoryRegistry.register("duplicate")
            class Product2:
                pass

    def test_unregister(self):
        """测试注销产品"""
        FactoryRegistry.clear()

        @FactoryRegistry.register("temp_product")
        class TempProduct:
            pass

        assert FactoryRegistry.is_registered("temp_product")

        FactoryRegistry.unregister("temp_product")
        assert not FactoryRegistry.is_registered("temp_product")

    def test_clear_registry(self):
        """测试清空注册表"""
        FactoryRegistry.clear()
        assert len(FactoryRegistry.list_products()) == 0

    def test_thread_safety(self):
        """测试线程安全性"""
        FactoryRegistry.clear()
        errors = []
        success_count = [0]

        def register_product(index: int):
            try:

                @FactoryRegistry.register(f"product_{index}")
                class DynamicProduct:
                    def __init__(self):
                        self.index = index

                success_count[0] += 1
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=register_product, args=(i,)) for i in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0
        assert success_count[0] == 10
        assert len(FactoryRegistry.list_products()) == 10

    def test_create_with_args_kwargs(self):
        """测试带参数的创建"""

        @FactoryRegistry.register("configurable")
        class ConfigurableProduct:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        product = FactoryRegistry.create("configurable", 1, 2, 3, key="value")
        assert product.args == (1, 2, 3)
        assert product.kwargs == {"key": "value"}

        FactoryRegistry.unregister("configurable")


# ============================================================================
# 测试: 泛型实现
# ============================================================================


class TestGenericFactory:
    """测试泛型工厂"""

    def test_generic_factory_creation(self):
        """测试泛型工厂创建"""
        factory = GenericFactory(ConcreteProductA)
        product = factory.create()
        assert isinstance(product, ConcreteProductA)

    def test_generic_factory_with_different_types(self):
        """测试不同类型的泛型工厂"""
        factory_a = GenericFactory(ConcreteProductA)
        factory_b = GenericFactory(ConcreteProductB)

        product_a = factory_a.create()
        product_b = factory_b.create()

        assert isinstance(product_a, ConcreteProductA)
        assert isinstance(product_b, ConcreteProductB)

    def test_get_product_class(self):
        """测试获取产品类"""
        factory = GenericFactory(ConcreteProductA)
        assert factory.get_product_class() == ConcreteProductA

    def test_cached_generic_factory(self):
        """测试带缓存的泛型工厂"""
        factory = CachedGenericFactory(ConcreteProductA, cache_enabled=True)

        # 创建两个实例，使用相同的缓存键
        product1 = factory.create(cache_key="key1")
        product2 = factory.create(cache_key="key1")

        # 应该是同一个实例
        assert product1 is product2

    def test_cached_factory_different_keys(self):
        """测试不同缓存键"""
        factory = CachedGenericFactory(ConcreteProductA, cache_enabled=True)

        product1 = factory.create(cache_key="key1")
        product2 = factory.create(cache_key="key2")

        # 应该是不同的实例
        assert product1 is not product2

    def test_cached_factory_no_cache(self):
        """测试禁用缓存"""
        factory = CachedGenericFactory(ConcreteProductA, cache_enabled=False)

        product1 = factory.create(cache_key="key1")
        product2 = factory.create(cache_key="key1")

        # 应该是不同的实例
        assert product1 is not product2

    def test_clear_cache(self):
        """测试清空缓存"""
        factory = CachedGenericFactory(ConcreteProductA, cache_enabled=True)

        factory.create(cache_key="key1")
        assert factory.get_cache_size() == 1

        factory.clear_cache()
        assert factory.get_cache_size() == 0

    def test_cache_thread_safety(self):
        """测试缓存线程安全"""
        factory = CachedGenericFactory(ConcreteProductA, cache_enabled=True)
        results = []

        def create_product():
            product = factory.create(cache_key="shared")
            results.append(id(product))

        threads = [threading.Thread(target=create_product) for _ in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # 所有线程应该获得同一个实例
        assert len(set(results)) == 1


# ============================================================================
# 测试: 配置化工厂
# ============================================================================


class TestConfigurableFactory:
    """测试配置化工厂"""

    def test_factory_config(self):
        """测试工厂配置"""
        config = FactoryConfig(
            product_class="ConcreteProductA",
            default_params={},
            enabled=True,
        )
        assert config.product_class == "ConcreteProductA"
        assert config.enabled is True

    def test_create_with_config(self):
        """测试使用配置创建产品"""
        config = {
            "product_a": FactoryConfig(
                product_class="ConcreteProductA", default_params={}
            )
        }
        factory = ConfigurableFactory(config)
        product = factory.create("product_a")
        assert isinstance(product, ConcreteProductA)

    def test_disabled_product(self):
        """测试禁用的产品"""
        config = {
            "disabled": FactoryConfig(
                product_class="ConcreteProductA",
                default_params={},
                enabled=False,
            )
        }
        factory = ConfigurableFactory(config)

        with pytest.raises(FactoryError, match="已禁用"):
            factory.create("disabled")

    def test_unknown_product_config(self):
        """测试未配置的产品"""
        factory = ConfigurableFactory({})

        with pytest.raises(UnknownProductError, match="未配置的产品类型"):
            factory.create("unknown")

    def test_cached_config(self):
        """测试配置缓存"""
        config = {
            "cached": FactoryConfig(
                product_class="ConcreteProductA",
                default_params={},
                cache=True,
            )
        }
        factory = ConfigurableFactory(config)

        product1 = factory.create("cached")
        product2 = factory.create("cached")

        # 应该是同一个实例
        assert product1 is product2


# ============================================================================
# 测试: 工具函数
# ============================================================================


class TestUtilityFunctions:
    """测试工具函数"""

    def test_factory_timer(self, capsys):
        """测试工厂计时装饰器"""

        @factory_timer
        def create_product():
            time.sleep(0.01)  # 模拟耗时操作
            return ConcreteProductA()

        product = create_product()
        assert isinstance(product, ConcreteProductA)

        # 检查输出
        captured = capsys.readouterr()
        assert "⏱️" in captured.out
        assert "create_product" in captured.out
        assert "ms" in captured.out

    def test_factory_logger(self, capsys):
        """测试工厂日志装饰器"""

        @factory_logger
        def create_product(name: str):
            return ConcreteProductA()

        product = create_product("test")
        assert isinstance(product, ConcreteProductA)

        # 检查输出
        captured = capsys.readouterr()
        assert "📝 开始创建产品" in captured.out
        assert "✅ 产品创建成功" in captured.out

    def test_factory_logger_with_error(self, capsys):
        """测试工厂日志装饰器（错误情况）"""

        @factory_logger
        def create_product():
            raise ValueError("创建失败")

        with pytest.raises(ValueError, match="创建失败"):
            create_product()

        # 检查输出
        captured = capsys.readouterr()
        assert "❌ 产品创建失败" in captured.out

    def test_combined_decorators(self, capsys):
        """测试组合装饰器"""

        @factory_timer
        @factory_logger
        def create_product():
            time.sleep(0.01)
            return ConcreteProductA()

        product = create_product()
        assert isinstance(product, ConcreteProductA)

        # 检查输出
        captured = capsys.readouterr()
        assert "📝" in captured.out  # 日志
        assert "⏱️" in captured.out  # 计时


# ============================================================================
# 测试: 边界条件
# ============================================================================


class TestEdgeCases:
    """测试边界条件"""

    def test_none_parameters(self):
        """测试None参数"""
        product = RegistryProductA(config=None)
        assert product.config == {}

    def test_empty_config(self):
        """测试空配置"""
        product = RegistryProductA(config={})
        assert product.config == {}

    def test_large_number_of_products(self):
        """测试大量产品创建"""
        FactoryRegistry.clear()

        # 注册大量产品
        for i in range(100):

            @FactoryRegistry.register(f"product_{i}")
            class DynamicProduct:
                def __init__(self, index=i):
                    self.index = index

        assert len(FactoryRegistry.list_products()) == 100

        # 创建所有产品
        for i in range(100):
            product = FactoryRegistry.create(f"product_{i}")
            assert hasattr(product, "index")

    def test_concurrent_access(self):
        """测试并发访问"""
        FactoryRegistry.clear()

        @FactoryRegistry.register("concurrent_product")
        class ConcurrentProduct:
            def __init__(self):
                self.created_at = time.time()

        results = []
        errors = []

        def create_products():
            try:
                for _ in range(10):
                    product = FactoryRegistry.create("concurrent_product")
                    results.append(product)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=create_products) for _ in range(5)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0
        assert len(results) == 50  # 5 threads * 10 products


# ============================================================================
# 测试: 性能
# ============================================================================


class TestPerformance:
    """测试性能"""

    def test_creation_speed(self):
        """测试创建速度"""
        import timeit

        # 直接创建
        direct_time = timeit.timeit(lambda: ConcreteProductA(), number=10000)

        # 工厂创建
        factory = GenericFactory(ConcreteProductA)
        factory_time = timeit.timeit(lambda: factory.create(), number=10000)

        # 注册表创建
        @FactoryRegistry.register("perf_test")
        class PerfProduct:
            pass

        registry_time = timeit.timeit(
            lambda: FactoryRegistry.create("perf_test"), number=10000
        )

        print(f"\n直接创建: {direct_time:.4f}s")
        print(f"工厂创建: {factory_time:.4f}s")
        print(f"注册表创建: {registry_time:.4f}s")

        # 工厂方法不应该比直接创建慢太多（<5倍）
        assert factory_time < direct_time * 5
        assert registry_time < direct_time * 10

        FactoryRegistry.unregister("perf_test")

    def test_cache_performance(self):
        """测试缓存性能"""
        import timeit

        # 无缓存
        factory_no_cache = CachedGenericFactory(ConcreteProductA, cache_enabled=False)
        no_cache_time = timeit.timeit(
            lambda: factory_no_cache.create(cache_key="key"), number=10000
        )

        # 有缓存
        factory_with_cache = CachedGenericFactory(
            ConcreteProductA, cache_enabled=True
        )
        with_cache_time = timeit.timeit(
            lambda: factory_with_cache.create(cache_key="key"), number=10000
        )

        print(f"\n无缓存: {no_cache_time:.4f}s")
        print(f"有缓存: {with_cache_time:.4f}s")

        # 缓存应该显著提高性能
        assert with_cache_time < no_cache_time


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

