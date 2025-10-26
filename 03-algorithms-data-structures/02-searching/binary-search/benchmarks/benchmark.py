"""
Binary Search - 性能基准测试

包含6个基准测试：
1. 基础实现对比（迭代 vs 递归）
2. 变种算法性能
3. 不同数据规模性能
4. 批量查询性能
5. 缓存友好性测试
6. 内存使用分析
"""

from __future__ import annotations

import random
import sys
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Callable

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from binary_search import (
    BinarySearch,
    BinarySearcher,
    RecursiveBinarySearch,
    StandardBinarySearch,
    binary_search_bulk,
    binary_search_first,
    binary_search_iterative,
    binary_search_last,
    binary_search_optimized,
    binary_search_recursive,
    lower_bound,
    upper_bound,
)


# ============================================================================
# 性能指标
# ============================================================================


@dataclass
class BenchmarkResult:
    """基准测试结果"""

    name: str
    iterations: int
    total_time: float
    avg_time: float
    operations_per_sec: float
    memory_used: int = 0

    def __str__(self) -> str:
        return (
            f"{self.name:40s} | "
            f"Iterations: {self.iterations:8d} | "
            f"Total: {self.total_time*1000:8.2f} ms | "
            f"Avg: {self.avg_time*1e6:8.2f} μs | "
            f"Ops/s: {self.operations_per_sec:12,.0f}"
        )


def benchmark(
    func: Callable, iterations: int = 1000, measure_memory: bool = False
) -> BenchmarkResult:
    """
    基准测试装饰器

    Args:
        func: 要测试的函数
        iterations: 迭代次数
        measure_memory: 是否测量内存

    Returns:
        基准测试结果
    """
    if measure_memory:
        tracemalloc.start()

    start = perf_counter()

    for _ in range(iterations):
        func()

    elapsed = perf_counter() - start

    memory_used = 0
    if measure_memory:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_used = peak

    avg_time = elapsed / iterations
    ops_per_sec = iterations / elapsed if elapsed > 0 else 0

    return BenchmarkResult(
        name=func.__name__,
        iterations=iterations,
        total_time=elapsed,
        avg_time=avg_time,
        operations_per_sec=ops_per_sec,
        memory_used=memory_used,
    )


# ============================================================================
# 1. 基础实现对比
# ============================================================================


def benchmark_basic_implementations() -> None:
    """基准测试1: 基础实现对比（迭代 vs 递归）"""

    print("\n" + "=" * 100)
    print("基准测试1: 基础实现对比（迭代 vs 递归）")
    print("=" * 100)

    sizes = [100, 1_000, 10_000, 100_000, 1_000_000]

    for size in sizes:
        print(f"\n数组大小: {size:,}")
        print("-" * 100)

        arr = list(range(size))
        target = size // 2  # 中间位置

        # 迭代实现
        def test_iterative() -> None:
            binary_search_iterative(arr, target)

        result_iter = benchmark(test_iterative, iterations=1000)
        print(result_iter)

        # 递归实现
        def test_recursive() -> None:
            binary_search_recursive(arr, target)

        result_rec = benchmark(test_recursive, iterations=1000)
        print(result_rec)

        # 优化实现
        def test_optimized() -> None:
            binary_search_optimized(arr, target)

        result_opt = benchmark(test_optimized, iterations=1000)
        print(result_opt)

        # 性能对比
        speedup_opt = result_iter.avg_time / result_opt.avg_time
        print(f"\n优化版本相对迭代版本提升: {speedup_opt:.2f}x")


# ============================================================================
# 2. 变种算法性能
# ============================================================================


def benchmark_variant_algorithms() -> None:
    """基准测试2: 变种算法性能"""

    print("\n" + "=" * 100)
    print("基准测试2: 变种算法性能")
    print("=" * 100)

    # 创建有重复元素的数组
    size = 100_000
    arr = []
    for i in range(0, size, 100):
        arr.extend([i] * 100)  # 每个值重复100次

    target = size // 2
    iterations = 1000

    print(f"\n数组大小: {len(arr):,} (有重复元素)")
    print("-" * 100)

    # 标准搜索
    def test_standard() -> None:
        binary_search_iterative(arr, target)

    result_standard = benchmark(test_standard, iterations)
    print(result_standard)

    # 查找第一次出现
    def test_first() -> None:
        binary_search_first(arr, target)

    result_first = benchmark(test_first, iterations)
    print(result_first)

    # 查找最后一次出现
    def test_last() -> None:
        binary_search_last(arr, target)

    result_last = benchmark(test_last, iterations)
    print(result_last)

    # Lower Bound
    def test_lower() -> None:
        lower_bound(arr, target)

    result_lower = benchmark(test_lower, iterations)
    print(result_lower)

    # Upper Bound
    def test_upper() -> None:
        upper_bound(arr, target)

    result_upper = benchmark(test_upper, iterations)
    print(result_upper)


# ============================================================================
# 3. 不同数据规模性能
# ============================================================================


def benchmark_data_scales() -> None:
    """基准测试3: 不同数据规模性能"""

    print("\n" + "=" * 100)
    print("基准测试3: 不同数据规模性能分析")
    print("=" * 100)

    sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]

    print("\n| 数组大小 | 平均时间 (μs) | 比较次数 | 理论最大比较次数 |")
    print("|----------|---------------|----------|------------------|")

    for size in sizes:
        arr = list(range(size))
        target = size // 2

        searcher = BinarySearcher[int]()

        def test() -> None:
            searcher.search(arr, target)

        result = benchmark(test, iterations=100)

        # 理论最大比较次数
        import math

        max_comparisons = math.ceil(math.log2(size + 1))

        print(
            f"| {size:>8,} | {result.avg_time*1e6:>13.2f} | "
            f"{searcher.comparisons:>8d} | {max_comparisons:>16d} |"
        )


# ============================================================================
# 4. 批量查询性能
# ============================================================================


def benchmark_bulk_queries() -> None:
    """基准测试4: 批量查询性能"""

    print("\n" + "=" * 100)
    print("基准测试4: 批量查询性能")
    print("=" * 100)

    arr_size = 100_000
    query_counts = [10, 100, 1_000, 10_000]

    arr = list(range(arr_size))

    for query_count in query_counts:
        print(f"\n查询数量: {query_count:,}")
        print("-" * 100)

        # 生成随机查询
        targets = [random.randint(0, arr_size - 1) for _ in range(query_count)]

        # 方法1: 逐个查询
        def test_individual() -> None:
            for target in targets:
                binary_search_iterative(arr, target)

        result_individual = benchmark(test_individual, iterations=100)
        print(f"逐个查询: {result_individual}")

        # 方法2: 批量查询
        def test_bulk() -> None:
            binary_search_bulk(arr, targets)

        result_bulk = benchmark(test_bulk, iterations=100)
        print(f"批量查询: {result_bulk}")

        # 性能提升
        speedup = result_individual.avg_time / result_bulk.avg_time
        print(f"批量查询提升: {speedup:.2f}x")


# ============================================================================
# 5. 缓存友好性测试
# ============================================================================


def benchmark_cache_friendliness() -> None:
    """基准测试5: 缓存友好性测试"""

    print("\n" + "=" * 100)
    print("基准测试5: 缓存友好性测试")
    print("=" * 100)

    # 测试不同访问模式
    size = 1_000_000
    arr = list(range(size))
    iterations = 1000

    print(f"\n数组大小: {size:,}")
    print("-" * 100)

    # 1. 顺序访问（缓存友好）
    print("\n1. 顺序访问模式")
    targets_sequential = list(range(0, size, size // 100))

    def test_sequential() -> None:
        for target in targets_sequential:
            binary_search_iterative(arr, target)

    result_seq = benchmark(test_sequential, iterations=100)
    print(result_seq)

    # 2. 随机访问（缓存不友好）
    print("\n2. 随机访问模式")
    targets_random = [random.randint(0, size - 1) for _ in range(100)]

    def test_random() -> None:
        for target in targets_random:
            binary_search_iterative(arr, target)

    result_rand = benchmark(test_random, iterations=100)
    print(result_rand)

    # 3. 局部访问（中等缓存友好）
    print("\n3. 局部访问模式")
    base = size // 2
    targets_local = [base + i for i in range(-50, 50)]

    def test_local() -> None:
        for target in targets_local:
            binary_search_iterative(arr, target)

    result_local = benchmark(test_local, iterations=100)
    print(result_local)


# ============================================================================
# 6. 内存使用分析
# ============================================================================


def benchmark_memory_usage() -> None:
    """基准测试6: 内存使用分析"""

    print("\n" + "=" * 100)
    print("基准测试6: 内存使用分析")
    print("=" * 100)

    sizes = [1_000, 10_000, 100_000, 1_000_000]

    print("\n| 数组大小 | 迭代版本 (bytes) | 递归版本 (bytes) | OOP版本 (bytes) |")
    print("|----------|------------------|------------------|-----------------|")

    for size in sizes:
        arr = list(range(size))
        target = size // 2

        # 迭代版本
        def test_iterative() -> None:
            binary_search_iterative(arr, target)

        result_iter = benchmark(test_iterative, iterations=10, measure_memory=True)

        # 递归版本
        def test_recursive() -> None:
            binary_search_recursive(arr, target)

        result_rec = benchmark(test_recursive, iterations=10, measure_memory=True)

        # OOP版本
        def test_oop() -> None:
            bs = BinarySearch(arr)
            bs.search(target)

        result_oop = benchmark(test_oop, iterations=10, measure_memory=True)

        print(
            f"| {size:>8,} | {result_iter.memory_used:>16,} | "
            f"{result_rec.memory_used:>16,} | {result_oop.memory_used:>15,} |"
        )


# ============================================================================
# 7. OOP vs 函数式性能对比
# ============================================================================


def benchmark_oop_vs_functional() -> None:
    """基准测试7: OOP vs 函数式实现对比"""

    print("\n" + "=" * 100)
    print("基准测试7: OOP vs 函数式实现对比")
    print("=" * 100)

    size = 100_000
    arr = list(range(size))
    target = size // 2
    iterations = 1000

    print(f"\n数组大小: {size:,}")
    print("-" * 100)

    # 函数式实现
    def test_functional() -> None:
        binary_search_iterative(arr, target)

    result_func = benchmark(test_functional, iterations)
    print(f"函数式实现: {result_func}")

    # OOP实现
    bs = BinarySearch(arr)

    def test_oop() -> None:
        bs.search(target)

    result_oop = benchmark(test_oop, iterations)
    print(f"OOP实现:    {result_oop}")

    # 泛型实现
    searcher = BinarySearcher[int]()

    def test_generic() -> None:
        searcher.search(arr, target)

    result_generic = benchmark(test_generic, iterations)
    print(f"泛型实现:   {result_generic}")

    # 抽象基类实现
    algo = StandardBinarySearch()

    def test_abc() -> None:
        algo.search(arr, target)

    result_abc = benchmark(test_abc, iterations)
    print(f"抽象基类:   {result_abc}")


# ============================================================================
# 8. 最坏情况 vs 最好情况
# ============================================================================


def benchmark_best_vs_worst_case() -> None:
    """基准测试8: 最好情况 vs 最坏情况"""

    print("\n" + "=" * 100)
    print("基准测试8: 最好情况 vs 最坏情况性能对比")
    print("=" * 100)

    size = 1_000_000
    arr = list(range(size))
    iterations = 10000

    print(f"\n数组大小: {size:,}")
    print("-" * 100)

    # 最好情况：目标在中间
    target_best = size // 2

    def test_best() -> None:
        binary_search_iterative(arr, target_best)

    result_best = benchmark(test_best, iterations)
    print(f"最好情况（中间）: {result_best}")

    # 最坏情况：目标不存在
    target_worst = -1

    def test_worst() -> None:
        binary_search_iterative(arr, target_worst)

    result_worst = benchmark(test_worst, iterations)
    print(f"最坏情况（不存在）: {result_worst}")

    # 平均情况：随机目标
    def test_average() -> None:
        target = random.randint(0, size - 1)
        binary_search_iterative(arr, target)

    result_avg = benchmark(test_average, iterations)
    print(f"平均情况（随机）: {result_avg}")


# ============================================================================
# 9. 比较次数统计
# ============================================================================


def benchmark_comparison_counts() -> None:
    """基准测试9: 比较次数统计"""

    print("\n" + "=" * 100)
    print("基准测试9: 比较次数统计")
    print("=" * 100)

    import math

    sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]

    print("\n| 数组大小 | 最好次数 | 平均次数 | 最坏次数 | 理论最大 |")
    print("|----------|----------|----------|----------|----------|")

    for size in sizes:
        arr = list(range(size))
        searcher = BinarySearcher[int]()

        # 最好情况：第一次就找到
        target_best = size // 2
        searcher.search(arr, target_best)
        best_count = searcher.comparisons

        # 最坏情况：不存在
        searcher.reset_metrics()
        searcher.search(arr, -1)
        worst_count = searcher.comparisons

        # 平均情况：随机查找多次
        total_comparisons = 0
        trials = 100
        for _ in range(trials):
            searcher.reset_metrics()
            target = random.randint(0, size - 1)
            searcher.search(arr, target)
            total_comparisons += searcher.comparisons
        avg_count = total_comparisons / trials

        # 理论最大
        theoretical_max = math.ceil(math.log2(size + 1))

        print(
            f"| {size:>8,} | {best_count:>8d} | {avg_count:>8.1f} | "
            f"{worst_count:>8d} | {theoretical_max:>8d} |"
        )


# ============================================================================
# 10. 综合性能报告
# ============================================================================


def generate_performance_report() -> None:
    """生成综合性能报告"""

    print("\n" + "=" * 100)
    print("二分搜索算法 - 综合性能报告")
    print("=" * 100)

    # 标准测试配置
    size = 1_000_000
    arr = list(range(size))
    target = size // 2
    iterations = 10000

    print(f"\n测试配置:")
    print(f"  数组大小: {size:,}")
    print(f"  迭代次数: {iterations:,}")
    print(f"  目标位置: 中间")

    print("\n" + "-" * 100)
    print("性能指标:")
    print("-" * 100)

    searcher = BinarySearcher[int]()

    def test() -> None:
        searcher.search(arr, target)

    result = benchmark(test, iterations)

    print(f"\n总耗时:     {result.total_time*1000:.2f} ms")
    print(f"平均耗时:   {result.avg_time*1e6:.2f} μs")
    print(f"每秒操作数: {result.operations_per_sec:,.0f}")
    print(f"比较次数:   {searcher.comparisons}")

    # 理论分析
    import math

    theoretical_comparisons = math.ceil(math.log2(size + 1))
    print(f"\n理论分析:")
    print(f"  时间复杂度: O(log n)")
    print(f"  空间复杂度: O(1)")
    print(f"  最大比较次数: {theoretical_comparisons}")
    print(f"  实际比较次数: {searcher.comparisons}")

    # 性能对比
    linear_time_estimate = size / 2  # 线性搜索平均比较次数
    speedup = linear_time_estimate / searcher.comparisons

    print(f"\n与线性搜索对比:")
    print(f"  线性搜索平均比较次数: {linear_time_estimate:,.0f}")
    print(f"  二分搜索比较次数: {searcher.comparisons}")
    print(f"  性能提升: {speedup:,.0f}x")


# ============================================================================
# 主函数
# ============================================================================


def main() -> None:
    """运行所有基准测试"""

    print("\n" + "=" * 100)
    print("Binary Search - 性能基准测试套件")
    print("=" * 100)

    # 运行所有基准测试
    benchmark_basic_implementations()
    benchmark_variant_algorithms()
    benchmark_data_scales()
    benchmark_bulk_queries()
    benchmark_cache_friendliness()
    benchmark_memory_usage()
    benchmark_oop_vs_functional()
    benchmark_best_vs_worst_case()
    benchmark_comparison_counts()
    generate_performance_report()

    print("\n" + "=" * 100)
    print("所有基准测试完成！")
    print("=" * 100)


if __name__ == "__main__":
    main()

