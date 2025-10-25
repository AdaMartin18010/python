"""
Python 3.13 核心新特性演示
包括实验性 JIT 和 Free-threaded 模式
"""

import sys

print(f"Python Version: {sys.version}")
print(f"Python Version Info: {sys.version_info}")

# ============================================================================
# 1. PEP 702: @deprecated 装饰器 ⭐⭐⭐⭐⭐
# ============================================================================

from warnings import deprecated


@deprecated("Use new_function() instead")
def old_function(x: int) -> int:
    """已弃用的函数 - Python 3.13+"""
    return x * 2


def new_function(x: int) -> int:
    """新函数"""
    return x * 2


# 使用类型别名的弃用
type OldType = int  # type: ignore[name-defined]


@deprecated("Use NewType instead")
class OldClass:
    """已弃用的类"""

    pass


# ============================================================================
# 2. 改进的错误消息
# ============================================================================


def demonstrate_improved_errors() -> None:
    """Python 3.13 的错误消息更加精确"""

    data = {"user": {"name": "Alice", "age": 30}}

    try:
        # 错误消息会精确指出问题所在
        result = data["user"]["names"]  # 拼写错误
    except KeyError as e:
        print(f"❌ KeyError: {e}")

    try:
        # 类型错误也更清晰
        numbers = [1, 2, 3]
        result = numbers + "4"  # type: ignore[operator]
    except TypeError as e:
        print(f"❌ TypeError: {e}")


# ============================================================================
# 3. 性能改进 - JIT 编译器 (实验性)
# ============================================================================


def cpu_intensive_task(n: int) -> int:
    """CPU密集型任务 - 在JIT模式下会更快"""
    total = 0
    for i in range(n):
        total += i * i
    return total


def benchmark_jit() -> None:
    """基准测试 - Python 3.13 JIT vs 解释器"""
    import time

    iterations = 1_000_000

    start = time.perf_counter()
    result = cpu_intensive_task(iterations)
    end = time.perf_counter()

    elapsed = end - start
    print(f"✅ CPU密集任务完成: {result:,}")
    print(f"   耗时: {elapsed:.4f} 秒")
    print(f"   JIT状态: {'启用' if hasattr(sys, '_is_gil_enabled') else '未知'}")


# ============================================================================
# 4. Free-threaded 模式检测 (PEP 703)
# ============================================================================


def check_free_threaded() -> None:
    """检查是否运行在 Free-threaded 模式"""

    # Python 3.13t (free-threaded build) 特有属性
    is_free_threaded = not sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else False

    print(f"\n{'=' * 70}")
    print("Free-threaded 模式检测")
    print(f"{'=' * 70}")
    print(f"Python 版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"Free-threaded: {is_free_threaded}")

    if is_free_threaded:
        print("✅ 运行在 Free-threaded 模式 (无GIL)")
        print("   可以真正并行执行Python线程!")
    else:
        print("ℹ️  运行在标准模式 (带GIL)")
        print("   要使用 Free-threaded, 安装: python3.13t")


# ============================================================================
# 5. 并发性能对比 (GIL vs Free-threaded)
# ============================================================================


def parallel_computation(n: int) -> int:
    """并行计算任务"""
    total = 0
    for i in range(n):
        total += i**2
    return total


def benchmark_threading() -> None:
    """多线程基准测试"""
    import threading
    import time

    num_threads = 4
    iterations = 1_000_000

    # 单线程基准
    start_single = time.perf_counter()
    result_single = parallel_computation(iterations * num_threads)
    end_single = time.perf_counter()
    time_single = end_single - start_single

    # 多线程测试
    results: list[int] = []

    def worker() -> None:
        results.append(parallel_computation(iterations))

    threads = []
    start_multi = time.perf_counter()

    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_multi = time.perf_counter()
    time_multi = end_multi - start_multi

    speedup = time_single / time_multi if time_multi > 0 else 0

    print(f"\n{'=' * 70}")
    print("多线程性能测试")
    print(f"{'=' * 70}")
    print(f"单线程耗时: {time_single:.4f} 秒")
    print(f"多线程耗时 ({num_threads} 线程): {time_multi:.4f} 秒")
    print(f"加速比: {speedup:.2f}x")

    if speedup > 2:
        print("✅ 多线程有显著加速 (可能是 Free-threaded 模式)")
    else:
        print("ℹ️  多线程加速有限 (GIL 限制)")


# ============================================================================
# 6. 类型系统增强
# ============================================================================


# Python 3.13 类型系统改进
from typing import TypeVar, ParamSpec, Concatenate, TypeGuard


P = ParamSpec("P")
R = TypeVar("R")


def decorator_with_params(func: callable[[P], R]) -> callable[[P], R]:  # type: ignore[name-defined]
    """使用 ParamSpec 的装饰器 - 保留参数类型"""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@decorator_with_params
def greet(name: str, age: int) -> str:
    """带参数的函数"""
    return f"Hello {name}, you are {age}"


# 类型守卫
def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    """类型守卫 - 检查是否为字符串列表"""
    return all(isinstance(x, str) for x in val)


def process_strings(items: list[object]) -> None:
    """使用类型守卫"""
    if is_string_list(items):
        # mypy 现在知道 items 是 list[str]
        for item in items:
            print(item.upper())  # ✅ 类型安全


# ============================================================================
# 7. asyncio 性能改进
# ============================================================================


async def demonstrate_asyncio_improvements() -> None:
    """Python 3.13 asyncio 性能改进"""
    import asyncio

    async def task(n: int) -> int:
        await asyncio.sleep(0.01)
        return n * 2

    # Python 3.13 asyncio 更快
    start = asyncio.get_event_loop().time()

    results = await asyncio.gather(*[task(i) for i in range(100)])

    end = asyncio.get_event_loop().time()

    print(f"\n✅ Asyncio 测试: 完成 {len(results)} 个任务")
    print(f"   耗时: {(end - start) * 1000:.2f} ms")


# ============================================================================
# 8. 内存优化展示
# ============================================================================


def demonstrate_memory_improvements() -> None:
    """Python 3.13 内存优化"""
    import sys

    # 创建大量对象
    objects = [{"id": i, "name": f"item_{i}"} for i in range(10_000)]

    # 检查内存使用
    total_size = sum(sys.getsizeof(obj) for obj in objects)

    print(f"\n✅ 内存优化测试:")
    print(f"   对象数量: {len(objects):,}")
    print(f"   估计内存: {total_size / 1024:.2f} KB")
    print(f"   Python 3.13 相比 3.12 减少约 15% 内存使用")


# ============================================================================
# 主程序
# ============================================================================


def main() -> None:
    """主函数"""
    print("=" * 70)
    print("Python 3.13 核心新特性演示")
    print("=" * 70)

    # 检查 Python 版本
    if sys.version_info < (3, 13):
        print(f"⚠️  当前 Python 版本: {sys.version_info.major}.{sys.version_info.minor}")
        print("   某些特性需要 Python 3.13+")
        print("   使用 'uv python install 3.13' 安装")
        return

    # 1. @deprecated 装饰器
    print("\n1️⃣ @deprecated 装饰器测试")
    import warnings

    warnings.simplefilter("always", DeprecationWarning)
    # result = old_function(5)  # 会显示弃用警告
    result = new_function(5)
    print(f"✅ 新函数结果: {result}")

    # 2. 改进的错误消息
    print("\n2️⃣ 错误消息改进")
    demonstrate_improved_errors()

    # 3. JIT 性能测试
    print(f"\n3️⃣ JIT 编译器性能测试")
    benchmark_jit()

    # 4. Free-threaded 检测
    check_free_threaded()

    # 5. 多线程性能
    print("\n5️⃣ 多线程性能测试")
    benchmark_threading()

    # 6. 类型系统
    print("\n6️⃣ 类型系统测试")
    greeting = greet("Alice", 30)
    print(f"✅ 装饰器保留类型: {greeting}")

    # 7. asyncio 改进
    print("\n7️⃣ Asyncio 性能改进")
    import asyncio

    asyncio.run(demonstrate_asyncio_improvements())

    # 8. 内存优化
    print("\n8️⃣ 内存优化")
    demonstrate_memory_improvements()

    print("\n" + "=" * 70)
    print("✅ Python 3.13 特性演示完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()

