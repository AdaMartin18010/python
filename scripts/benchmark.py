#!/usr/bin/env python3
"""
Python 2025 Knowledge Base - Benchmark Script
性能基准测试脚本：测试各种Python操作的性能

Usage:
    python scripts/benchmark.py
    python scripts/benchmark.py --json
    python scripts/benchmark.py --compare
"""

import sys
import time
import json
import platform
from typing import Dict, List, Callable, Any
from dataclasses import dataclass, asdict
import statistics

# 颜色代码
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    name: str
    iterations: int
    total_time: float
    avg_time: float
    min_time: float
    max_time: float
    std_dev: float
    ops_per_sec: float


class Benchmarker:
    """性能基准测试器"""

    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def print_header(self, text: str) -> None:
        """打印标题"""
        print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
        print(f"{BLUE}{BOLD}{text:^60}{RESET}")
        print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

    def print_info(self, text: str) -> None:
        """打印信息"""
        print(f"{BLUE}ℹ{RESET} {text}")

    def benchmark(
        self,
        name: str,
        func: Callable,
        iterations: int = 10000,
        warmup: int = 100
    ) -> BenchmarkResult:
        """执行基准测试"""
        # 预热
        for _ in range(warmup):
            func()

        # 测试
        times: List[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            times.append(end - start)

        total_time = sum(times)
        avg_time = total_time / iterations
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        ops_per_sec = iterations / total_time if total_time > 0 else 0

        result = BenchmarkResult(
            name=name,
            iterations=iterations,
            total_time=total_time,
            avg_time=avg_time,
            min_time=min_time,
            max_time=max_time,
            std_dev=std_dev,
            ops_per_sec=ops_per_sec
        )

        self.results.append(result)
        return result

    def print_result(self, result: BenchmarkResult) -> None:
        """打印测试结果"""
        print(f"{BOLD}{result.name}{RESET}")
        print(f"  迭代次数: {result.iterations:,}")
        print(f"  总时间:   {result.total_time:.6f}s")
        print(f"  平均时间: {result.avg_time*1e6:.2f}μs")
        print(f"  最小时间: {result.min_time*1e6:.2f}μs")
        print(f"  最大时间: {result.max_time*1e6:.2f}μs")
        print(f"  标准差:   {result.std_dev*1e6:.2f}μs")
        print(f"  吞吐量:   {result.ops_per_sec:,.0f} ops/s")
        print()

    def run_basic_benchmarks(self) -> None:
        """运行基础基准测试"""
        self.print_header("基础操作基准测试")

        # 1. 列表操作
        self.print_info("测试列表操作...")
        result = self.benchmark(
            "列表创建和追加",
            lambda: [i for i in range(100)],
            iterations=10000
        )
        self.print_result(result)

        # 2. 字典操作
        self.print_info("测试字典操作...")
        result = self.benchmark(
            "字典创建和访问",
            lambda: {i: i*2 for i in range(100)},
            iterations=10000
        )
        self.print_result(result)

        # 3. 字符串操作
        self.print_info("测试字符串操作...")
        test_str = "Hello, Python 2025!"
        result = self.benchmark(
            "字符串拼接",
            lambda: test_str + " " + test_str,
            iterations=100000
        )
        self.print_result(result)

        # 4. 函数调用
        self.print_info("测试函数调用...")
        def test_func(x: int) -> int:
            return x * 2

        result = self.benchmark(
            "简单函数调用",
            lambda: test_func(42),
            iterations=100000
        )
        self.print_result(result)

    def run_data_structure_benchmarks(self) -> None:
        """运行数据结构基准测试"""
        self.print_header("数据结构基准测试")

        # 1. List vs Tuple
        self.print_info("测试 List vs Tuple...")
        
        result_list = self.benchmark(
            "List 迭代",
            lambda: [x for x in range(1000)],
            iterations=10000
        )
        self.print_result(result_list)

        result_tuple = self.benchmark(
            "Tuple 迭代",
            lambda: tuple(x for x in range(1000)),
            iterations=10000
        )
        self.print_result(result_tuple)

        # 2. Dict vs Set
        self.print_info("测试 Dict vs Set...")
        
        test_dict = {i: i for i in range(1000)}
        result_dict = self.benchmark(
            "Dict 查找",
            lambda: 500 in test_dict,
            iterations=100000
        )
        self.print_result(result_dict)

        test_set = set(range(1000))
        result_set = self.benchmark(
            "Set 查找",
            lambda: 500 in test_set,
            iterations=100000
        )
        self.print_result(result_set)

    def run_comprehension_benchmarks(self) -> None:
        """运行推导式基准测试"""
        self.print_header("推导式基准测试")

        # 1. List Comprehension vs Loop
        self.print_info("测试 List Comprehension vs Loop...")
        
        result_comp = self.benchmark(
            "List Comprehension",
            lambda: [x*2 for x in range(100)],
            iterations=10000
        )
        self.print_result(result_comp)

        def loop_version():
            result = []
            for x in range(100):
                result.append(x*2)
            return result

        result_loop = self.benchmark(
            "For Loop",
            loop_version,
            iterations=10000
        )
        self.print_result(result_loop)

        # 2. Dict Comprehension
        self.print_info("测试 Dict Comprehension...")
        result = self.benchmark(
            "Dict Comprehension",
            lambda: {x: x*2 for x in range(100)},
            iterations=10000
        )
        self.print_result(result)

    def generate_system_info(self) -> Dict[str, Any]:
        """生成系统信息"""
        return {
            "python_version": sys.version,
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0],
        }

    def generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        return {
            "system_info": self.generate_system_info(),
            "results": [asdict(r) for r in self.results],
            "summary": {
                "total_tests": len(self.results),
                "fastest": asdict(max(self.results, key=lambda r: r.ops_per_sec)),
                "slowest": asdict(min(self.results, key=lambda r: r.ops_per_sec)),
            }
        }

    def print_summary(self) -> None:
        """打印总结"""
        self.print_header("基准测试总结")
        
        system_info = self.generate_system_info()
        print(f"{BOLD}系统信息:{RESET}")
        print(f"  Python: {system_info['python_version'].split()[0]}")
        print(f"  实现:   {system_info['python_implementation']}")
        print(f"  平台:   {system_info['platform']}")
        print(f"  处理器: {system_info['processor']}")
        print()

        print(f"{BOLD}测试统计:{RESET}")
        print(f"  总测试数: {len(self.results)}")
        
        if self.results:
            fastest = max(self.results, key=lambda r: r.ops_per_sec)
            slowest = min(self.results, key=lambda r: r.ops_per_sec)
            
            print(f"\n{GREEN}最快操作:{RESET}")
            print(f"  {fastest.name}")
            print(f"  {fastest.ops_per_sec:,.0f} ops/s")
            
            print(f"\n{YELLOW}最慢操作:{RESET}")
            print(f"  {slowest.name}")
            print(f"  {slowest.ops_per_sec:,.0f} ops/s")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Python 2025 知识库 - 性能基准测试"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出结果"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10000,
        help="每个测试的迭代次数"
    )
    
    args = parser.parse_args()
    
    benchmarker = Benchmarker()
    
    print(f"\n{BOLD}Python 2025 知识库 - 性能基准测试{RESET}")
    print(f"迭代次数: {args.iterations:,}\n")
    
    benchmarker.run_basic_benchmarks()
    benchmarker.run_data_structure_benchmarks()
    benchmarker.run_comprehension_benchmarks()
    
    if args.json:
        report = benchmarker.generate_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        benchmarker.print_summary()
    
    print(f"\n{GREEN}✓{RESET} 基准测试完成！\n")


if __name__ == "__main__":
    main()

