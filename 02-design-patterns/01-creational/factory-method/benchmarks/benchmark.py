"""
Factory Method Pattern - 性能基准测试

对比不同实现方式的性能特征：
1. 直接实例化
2. 函数工厂
3. 类工厂（ABC）
4. 注册表工厂
5. 泛型工厂
6. 缓存工厂
"""

import sys
from pathlib import Path
import time
import statistics
from dataclasses import dataclass
from typing import Callable, Any
import threading

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from factory_method import (
    ConcreteProductA,
    ConcreteCreatorA,
    functional_factory_method,
    FactoryRegistry,
    GenericFactory,
    CachedGenericFactory,
)


@dataclass
class BenchmarkResult:
    """基准测试结果"""

    name: str
    iterations: int
    total_time: float
    avg_time: float
    ops_per_second: float
    std_dev: float

    def __str__(self) -> str:
        return (
            f"{self.name:25s} | "
            f"{self.iterations:10,d} 次 | "
            f"{self.total_time:8.4f}s | "
            f"{self.avg_time * 1000:10.6f}ms | "
            f"{self.ops_per_second:12,.0f} ops/s | "
            f"±{self.std_dev * 1000:.6f}ms"
        )


class Benchmark:
    """基准测试工具"""

    def __init__(self, iterations: int = 10000, warmup: int = 1000):
        self.iterations = iterations
        self.warmup = warmup
        self.results: list[BenchmarkResult] = []

    def run(self, name: str, func: Callable[[], Any]) -> BenchmarkResult:
        """
        运行基准测试

        Args:
            name: 测试名称
            func: 要测试的函数

        Returns:
            测试结果
        """
        print(f"⏳ 运行基准测试: {name}...")

        # 预热
        for _ in range(self.warmup):
            func()

        # 测试
        times: list[float] = []
        start_total = time.perf_counter()

        for _ in range(self.iterations):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            times.append(end - start)

        end_total = time.perf_counter()
        total_time = end_total - start_total

        # 统计
        avg_time = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        ops_per_second = self.iterations / total_time

        result = BenchmarkResult(
            name=name,
            iterations=self.iterations,
            total_time=total_time,
            avg_time=avg_time,
            ops_per_second=ops_per_second,
            std_dev=std_dev,
        )

        self.results.append(result)
        return result

    def print_results(self) -> None:
        """打印所有结果"""
        print("\n" + "=" * 120)
        print("📊 基准测试结果")
        print("=" * 120)
        print(
            f"{'实现方式':25s} | {'迭代次数':>10s} | "
            f"{'总时间':>8s} | {'平均时间':>10s} | "
            f"{'操作/秒':>12s} | {'标准差':>15s}"
        )
        print("-" * 120)

        for result in self.results:
            print(result)

        print("=" * 120)

        # 找出最快的
        if self.results:
            fastest = min(self.results, key=lambda r: r.avg_time)
            print(f"\n🏆 最快的实现: {fastest.name}")
            print(f"   平均时间: {fastest.avg_time * 1000:.6f}ms")
            print(f"   操作/秒: {fastest.ops_per_second:,.0f}\n")

            # 对比其他实现
            print("📈 性能对比（相对于最快实现）:")
            for result in sorted(self.results, key=lambda r: r.avg_time):
                if result == fastest:
                    print(f"   {result.name:30s}: 1.00x (基准)")
                else:
                    ratio = result.avg_time / fastest.avg_time
                    print(f"   {result.name:30s}: {ratio:.2f}x")

    def compare_memory(self) -> None:
        """对比内存使用（简化版）"""
        import sys

        print("\n" + "=" * 70)
        print("💾 内存使用对比")
        print("=" * 70)

        # 直接实例化
        product_direct = ConcreteProductA()
        size_direct = sys.getsizeof(product_direct)
        print(f"直接实例化: {size_direct} bytes")

        # 工厂创建
        creator = ConcreteCreatorA()
        product_factory = creator.factory_method()
        size_factory = sys.getsizeof(product_factory)
        print(f"工厂创建: {size_factory} bytes")

        # 泛型工厂
        generic_factory = GenericFactory(ConcreteProductA)
        product_generic = generic_factory.create()
        size_generic = sys.getsizeof(product_generic)
        print(f"泛型工厂: {size_generic} bytes")

        print("=" * 70)


# ============================================================================
# 基准测试: 创建速度
# ============================================================================


def benchmark_creation_speed():
    """测试不同实现方式的创建速度"""
    print("\n" + "=" * 70)
    print("🚀 基准测试1: 对象创建速度")
    print("=" * 70)

    bench = Benchmark(iterations=50000, warmup=5000)

    # 1. 直接实例化（基准）
    bench.run("1. 直接实例化", lambda: ConcreteProductA())

    # 2. 函数工厂
    bench.run("2. 函数工厂", lambda: functional_factory_method("type_a"))

    # 3. 类工厂（ABC）
    creator = ConcreteCreatorA()
    bench.run("3. 类工厂(ABC)", lambda: creator.factory_method())

    # 4. 注册表工厂
    FactoryRegistry.register("bench_product")(ConcreteProductA)
    bench.run("4. 注册表工厂", lambda: FactoryRegistry.create("bench_product"))

    # 5. 泛型工厂
    generic_factory = GenericFactory(ConcreteProductA)
    bench.run("5. 泛型工厂", lambda: generic_factory.create())

    # 6. 缓存工厂（无缓存）
    cached_factory_no = CachedGenericFactory(ConcreteProductA, cache_enabled=False)
    bench.run(
        "6. 缓存工厂(无缓存)", lambda: cached_factory_no.create(cache_key=None)
    )

    bench.print_results()


# ============================================================================
# 基准测试: 缓存性能
# ============================================================================


def benchmark_cache_performance():
    """测试缓存对性能的影响"""
    print("\n" + "=" * 70)
    print("🚀 基准测试2: 缓存性能")
    print("=" * 70)

    bench = Benchmark(iterations=100000, warmup=10000)

    # 无缓存
    factory_no_cache = CachedGenericFactory(ConcreteProductA, cache_enabled=False)
    bench.run(
        "无缓存 (每次新建)", lambda: factory_no_cache.create(cache_key="key1")
    )

    # 单键缓存
    factory_single_cache = CachedGenericFactory(ConcreteProductA, cache_enabled=True)
    bench.run(
        "单键缓存 (同一实例)", lambda: factory_single_cache.create(cache_key="key1")
    )

    # 多键缓存
    factory_multi_cache = CachedGenericFactory(ConcreteProductA, cache_enabled=True)
    keys = [f"key_{i % 10}" for i in range(100000)]
    key_iter = iter(keys)
    bench.run(
        "多键缓存 (10个键)", lambda: factory_multi_cache.create(cache_key=next(key_iter))
    )

    bench.print_results()


# ============================================================================
# 基准测试: 注册表性能
# ============================================================================


def benchmark_registry_scale():
    """测试注册表在不同规模下的性能"""
    print("\n" + "=" * 70)
    print("🚀 基准测试3: 注册表规模性能")
    print("=" * 70)

    # 清空注册表
    FactoryRegistry.clear()

    # 注册不同数量的产品
    scales = [10, 100, 1000]

    for scale in scales:
        FactoryRegistry.clear()

        # 注册产品
        for i in range(scale):

            @FactoryRegistry.register(f"product_{i}")
            class DynamicProduct:
                def __init__(self):
                    pass

        # 测试查找和创建性能
        bench = Benchmark(iterations=10000, warmup=1000)

        # 测试第一个产品
        bench.run(
            f"注册表({scale}项)-首项",
            lambda: FactoryRegistry.create("product_0"),
        )

        # 测试中间产品
        mid = scale // 2
        bench.run(
            f"注册表({scale}项)-中项",
            lambda: FactoryRegistry.create(f"product_{mid}"),
        )

        # 测试最后一个产品
        bench.run(
            f"注册表({scale}项)-尾项",
            lambda: FactoryRegistry.create(f"product_{scale - 1}"),
        )

        bench.print_results()


# ============================================================================
# 基准测试: 并发性能
# ============================================================================


def benchmark_concurrent_access():
    """测试并发访问性能"""
    print("\n" + "=" * 70)
    print("🚀 基准测试4: 并发访问性能")
    print("=" * 70)

    iterations_per_thread = 1000
    thread_counts = [1, 2, 4, 8, 16]

    results = []

    for num_threads in thread_counts:
        # 准备工厂
        factory = CachedGenericFactory(ConcreteProductA, cache_enabled=True)
        factory.clear_cache()

        # 测试函数
        def worker():
            for i in range(iterations_per_thread):
                factory.create(cache_key=f"key_{i % 10}")

        # 运行测试
        start_time = time.perf_counter()

        threads = [threading.Thread(target=worker) for _ in range(num_threads)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        end_time = time.perf_counter()
        total_time = end_time - start_time
        total_ops = iterations_per_thread * num_threads
        ops_per_second = total_ops / total_time

        results.append((num_threads, total_time, ops_per_second))

        print(
            f"{num_threads:2d} 线程: {total_time:8.4f}s | "
            f"{total_ops:8,d} 操作 | {ops_per_second:12,.0f} ops/s"
        )

    # 计算加速比
    print("\n加速比分析:")
    baseline_time = results[0][1]
    for num_threads, total_time, ops_per_second in results:
        speedup = baseline_time / total_time
        efficiency = speedup / num_threads * 100
        print(
            f"{num_threads:2d} 线程: 加速比 {speedup:.2f}x | "
            f"并行效率 {efficiency:.1f}%"
        )


# ============================================================================
# 基准测试: 复杂对象创建
# ============================================================================


def benchmark_complex_creation():
    """测试复杂对象创建的性能"""
    print("\n" + "=" * 70)
    print("🚀 基准测试5: 复杂对象创建")
    print("=" * 70)

    # 定义复杂对象
    class ComplexProduct:
        def __init__(self):
            self.data = [i for i in range(100)]
            self.config = {f"key_{i}": f"value_{i}" for i in range(50)}
            self.nested = {
                "level1": {"level2": {"level3": [1, 2, 3, 4, 5]}}
            }

    bench = Benchmark(iterations=10000, warmup=1000)

    # 直接创建
    bench.run("直接创建复杂对象", lambda: ComplexProduct())

    # 注册表工厂
    FactoryRegistry.register("complex_product")(ComplexProduct)
    bench.run(
        "注册表创建复杂对象",
        lambda: FactoryRegistry.create("complex_product"),
    )

    # 泛型工厂
    generic_factory = GenericFactory(ComplexProduct)
    bench.run("泛型工厂创建复杂对象", lambda: generic_factory.create())

    # 缓存工厂
    cached_factory = CachedGenericFactory(ComplexProduct, cache_enabled=True)
    bench.run(
        "缓存工厂创建复杂对象",
        lambda: cached_factory.create(cache_key="complex"),
    )

    bench.print_results()


# ============================================================================
# 基准测试: 内存使用
# ============================================================================


def benchmark_memory_usage():
    """测试内存使用"""
    print("\n" + "=" * 70)
    print("🚀 基准测试6: 内存使用")
    print("=" * 70)

    import sys
    import gc

    # 强制垃圾回收
    gc.collect()

    results = []

    # 创建大量对象并测量内存
    n = 1000

    # 1. 直接创建
    gc.collect()
    products_direct = []
    for _ in range(n):
        products_direct.append(ConcreteProductA())
    size_direct = sum(sys.getsizeof(p) for p in products_direct)
    results.append(("直接创建", size_direct))

    # 2. 工厂创建
    gc.collect()
    factory = GenericFactory(ConcreteProductA)
    products_factory = []
    for _ in range(n):
        products_factory.append(factory.create())
    size_factory = sum(sys.getsizeof(p) for p in products_factory)
    results.append(("泛型工厂创建", size_factory))

    # 3. 缓存工厂（多实例）
    gc.collect()
    cached_factory = CachedGenericFactory(ConcreteProductA, cache_enabled=True)
    products_cached = []
    for i in range(n):
        products_cached.append(cached_factory.create(cache_key=f"key_{i}"))
    size_cached = sum(sys.getsizeof(p) for p in products_cached)
    results.append(("缓存工厂(多实例)", size_cached))

    # 4. 缓存工厂（单实例）
    gc.collect()
    cached_factory_single = CachedGenericFactory(ConcreteProductA, cache_enabled=True)
    products_cached_single = []
    for _ in range(n):
        products_cached_single.append(
            cached_factory_single.create(cache_key="single")
        )
    size_cached_single = sum(sys.getsizeof(p) for p in products_cached_single)
    results.append(("缓存工厂(单实例)", size_cached_single))

    # 打印结果
    print(f"\n创建 {n:,} 个对象的内存使用:")
    print("-" * 70)
    for name, size in results:
        avg_size = size / n
        print(f"{name:25s}: {size:12,d} bytes 总计 | {avg_size:8.2f} bytes 平均")

    print("=" * 70)


# ============================================================================
# 主程序
# ============================================================================


def main():
    """运行所有基准测试"""
    print("\n" + "=" * 70)
    print("🎯 Factory Method Pattern - 性能基准测试")
    print("=" * 70)
    print("\n⚠️  注意：基准测试需要一些时间，请耐心等待...\n")

    try:
        # 运行所有基准测试
        benchmark_creation_speed()
        benchmark_cache_performance()
        benchmark_registry_scale()
        benchmark_concurrent_access()
        benchmark_complex_creation()
        benchmark_memory_usage()

        print("\n" + "=" * 70)
        print("✅ 所有基准测试完成！")
        print("=" * 70)

        # 总结建议
        print("\n📝 性能建议:")
        print("1. 简单对象创建: 直接实例化或泛型工厂")
        print("2. 需要类型安全: 泛型工厂")
        print("3. 需要灵活扩展: 注册表工厂")
        print("4. 高频创建同一对象: 缓存工厂")
        print("5. 并发场景: 缓存工厂 + 线程安全")
        print("6. 复杂对象创建: 注册表工厂 + 缓存")

    except Exception as e:
        print(f"\n❌ 基准测试失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

