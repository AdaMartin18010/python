# Python性能优化指南

## 1. 性能分析基础

### 1.1 性能分析工具

```python
import time
import cProfile
import pstats
import memory_profiler
from line_profiler import LineProfiler
import psutil
import tracemalloc

# 基础性能计时
class PerformanceTimer:
    """性能计时工具"""
    
    @staticmethod
    def time_function(func, *args, iterations=1000):
        """测量函数执行时间"""
        start_time = time.time()
        for _ in range(iterations):
            func(*args)
        end_time = time.time()
        return (end_time - start_time) / iterations
    
    @staticmethod
    def profile_function(func, *args):
        """使用cProfile分析函数性能"""
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args)
        profiler.disable()
        
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # 显示前10个最耗时的函数
        
        return result

# 内存分析
class MemoryAnalyzer:
    """内存分析工具"""
    
    @staticmethod
    def analyze_memory_usage():
        """分析当前内存使用情况"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss': memory_info.rss / 1024 / 1024,  # MB
            'vms': memory_info.vms / 1024 / 1024,  # MB
            'percent': process.memory_percent()
        }
    
    @staticmethod
    def track_memory_allocation():
        """跟踪内存分配"""
        tracemalloc.start()
        
        # 执行需要分析的代码
        # ...
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return {
            'current_mb': current / 1024 / 1024,
            'peak_mb': peak / 1024 / 1024
        }

# 行级性能分析
class LineProfiler:
    """行级性能分析"""
    
    @staticmethod
    def profile_line_by_line(func, *args):
        """逐行分析函数性能"""
        lp = LineProfiler()
        lp.add_function(func)
        lp.enable_by_count()
        
        result = func(*args)
        
        lp.print_stats()
        return result
```

### 1.2 性能基准测试

```python
import timeit
import statistics
from typing import Callable, List, Dict, Any

class BenchmarkSuite:
    """性能基准测试套件"""
    
    def __init__(self):
        self.results = {}
    
    def benchmark(self, name: str, func: Callable, *args, iterations: int = 1000):
        """执行基准测试"""
        times = []
        for _ in range(iterations):
            start_time = time.perf_counter()
            func(*args)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        self.results[name] = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std': statistics.stdev(times),
            'min': min(times),
            'max': max(times),
            'iterations': iterations
        }
    
    def compare_functions(self, functions: Dict[str, Callable], *args):
        """比较多个函数的性能"""
        for name, func in functions.items():
            self.benchmark(name, func, *args)
        
        return self.results
    
    def print_results(self):
        """打印基准测试结果"""
        print("性能基准测试结果:")
        print("-" * 60)
        
        for name, stats in self.results.items():
            print(f"{name}:")
            print(f"  平均时间: {stats['mean']:.6f}秒")
            print(f"  中位数: {stats['median']:.6f}秒")
            print(f"  标准差: {stats['std']:.6f}秒")
            print(f"  最小值: {stats['min']:.6f}秒")
            print(f"  最大值: {stats['max']:.6f}秒")
            print()

# 使用示例
def example_benchmark():
    """基准测试示例"""
    suite = BenchmarkSuite()
    
    def slow_function(n):
        return sum(i for i in range(n))
    
    def fast_function(n):
        return n * (n - 1) // 2
    
    functions = {
        'slow_sum': slow_function,
        'fast_sum': fast_function
    }
    
    suite.compare_functions(functions, 10000)
    suite.print_results()
```

## 2. 算法优化

### 2.1 数据结构选择

```python
from collections import defaultdict, deque, Counter
from typing import List, Dict, Set, Tuple
import heapq

class DataStructureOptimization:
    """数据结构优化"""
    
    @staticmethod
    def list_vs_set_lookup():
        """列表vs集合查找性能对比"""
        # 准备数据
        items = list(range(10000))
        item_set = set(items)
        
        # 测试列表查找
        def list_lookup():
            return 9999 in items
        
        # 测试集合查找
        def set_lookup():
            return 9999 in item_set
        
        suite = BenchmarkSuite()
        suite.compare_functions({
            'list_lookup': list_lookup,
            'set_lookup': set_lookup
        })
        return suite.results
    
    @staticmethod
    def dict_vs_defaultdict():
        """字典vs默认字典性能对比"""
        def count_with_dict(items):
            counts = {}
            for item in items:
                if item in counts:
                    counts[item] += 1
                else:
                    counts[item] = 1
            return counts
        
        def count_with_defaultdict(items):
            counts = defaultdict(int)
            for item in items:
                counts[item] += 1
            return counts
        
        items = ['a', 'b', 'a', 'c', 'b', 'a'] * 1000
        
        suite = BenchmarkSuite()
        suite.compare_functions({
            'dict_count': count_with_dict,
            'defaultdict_count': count_with_defaultdict
        }, items)
        return suite.results
    
    @staticmethod
    def optimize_list_operations():
        """优化列表操作"""
        # 使用列表推导式
        def traditional_loop(n):
            result = []
            for i in range(n):
                if i % 2 == 0:
                    result.append(i * 2)
            return result
        
        def list_comprehension(n):
            return [i * 2 for i in range(n) if i % 2 == 0]
        
        def generator_expression(n):
            return sum(i * 2 for i in range(n) if i % 2 == 0)
        
        n = 100000
        suite = BenchmarkSuite()
        suite.compare_functions({
            'traditional_loop': traditional_loop,
            'list_comprehension': list_comprehension,
            'generator_expression': generator_expression
        }, n)
        return suite.results
```

### 2.2 算法复杂度优化

```python
class AlgorithmOptimization:
    """算法复杂度优化"""
    
    @staticmethod
    def fibonacci_optimization():
        """斐波那契数列优化"""
        # 递归版本 (O(2^n))
        def fib_recursive(n):
            if n <= 1:
                return n
            return fib_recursive(n-1) + fib_recursive(n-2)
        
        # 动态规划版本 (O(n))
        def fib_dynamic(n):
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
        
        # 矩阵快速幂版本 (O(log n))
        def fib_matrix(n):
            def matrix_multiply(a, b):
                return [
                    [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                    [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
                ]
            
            def matrix_power(matrix, power):
                if power == 0:
                    return [[1, 0], [0, 1]]
                if power == 1:
                    return matrix
                
                half = matrix_power(matrix, power // 2)
                squared = matrix_multiply(half, half)
                
                if power % 2 == 0:
                    return squared
                else:
                    return matrix_multiply(squared, matrix)
            
            if n <= 1:
                return n
            
            matrix = [[1, 1], [1, 0]]
            result_matrix = matrix_power(matrix, n - 1)
            return result_matrix[0][0]
        
        n = 30
        suite = BenchmarkSuite()
        suite.compare_functions({
            'recursive': fib_recursive,
            'dynamic': fib_dynamic,
            'matrix': fib_matrix
        }, n)
        return suite.results
    
    @staticmethod
    def sorting_optimization():
        """排序算法优化"""
        import random
        
        # 生成测试数据
        data = [random.randint(1, 1000) for _ in range(1000)]
        
        # 内置排序
        def builtin_sort(data):
            return sorted(data.copy())
        
        # 快速排序
        def quicksort(data):
            if len(data) <= 1:
                return data
            pivot = data[len(data) // 2]
            left = [x for x in data if x < pivot]
            middle = [x for x in data if x == pivot]
            right = [x for x in data if x > pivot]
            return quicksort(left) + middle + quicksort(right)
        
        # 归并排序
        def mergesort(data):
            if len(data) <= 1:
                return data
            
            mid = len(data) // 2
            left = mergesort(data[:mid])
            right = mergesort(data[mid:])
            
            return merge(left, right)
        
        def merge(left, right):
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        suite = BenchmarkSuite()
        suite.compare_functions({
            'builtin_sort': builtin_sort,
            'quicksort': quicksort,
            'mergesort': mergesort
        }, data)
        return suite.results
```

## 3. 内存优化

### 3.1 内存使用优化

```python
import sys
import gc
import weakref
from typing import List, Dict, Any

class MemoryOptimization:
    """内存优化技术"""
    
    @staticmethod
    def use_slots_for_memory_efficiency():
        """使用__slots__减少内存使用"""
        class RegularClass:
            def __init__(self, name, age):
                self.name = name
                self.age = age
        
        class SlotsClass:
            __slots__ = ['name', 'age']
            
            def __init__(self, name, age):
                self.name = name
                self.age = age
        
        # 比较内存使用
        regular_objects = [RegularClass(f"user_{i}", i) for i in range(1000)]
        slots_objects = [SlotsClass(f"user_{i}", i) for i in range(1000)]
        
        regular_size = sum(sys.getsizeof(obj) for obj in regular_objects)
        slots_size = sum(sys.getsizeof(obj) for obj in slots_objects)
        
        return {
            'regular_class_size': regular_size,
            'slots_class_size': slots_size,
            'memory_saved': regular_size - slots_size,
            'percentage_saved': ((regular_size - slots_size) / regular_size) * 100
        }
    
    @staticmethod
    def use_generators_for_large_data():
        """使用生成器处理大数据"""
        def create_large_list(n):
            return [i * 2 for i in range(n)]
        
        def create_generator(n):
            return (i * 2 for i in range(n))
        
        n = 1000000
        
        # 测量内存使用
        import psutil
        process = psutil.Process()
        
        # 测试列表
        memory_before = process.memory_info().rss
        large_list = create_large_list(n)
        memory_after_list = process.memory_info().rss
        
        # 测试生成器
        memory_before_gen = process.memory_info().rss
        generator = create_generator(n)
        memory_after_gen = process.memory_info().rss
        
        return {
            'list_memory_usage': memory_after_list - memory_before,
            'generator_memory_usage': memory_after_gen - memory_before_gen,
            'memory_saved': (memory_after_list - memory_before) - (memory_after_gen - memory_before_gen)
        }
    
    @staticmethod
    def use_weak_references():
        """使用弱引用避免内存泄漏"""
        class Cache:
            def __init__(self):
                self._cache = weakref.WeakValueDictionary()
            
            def get(self, key):
                return self._cache.get(key)
            
            def set(self, key, value):
                self._cache[key] = value
        
        # 测试弱引用缓存
        cache = Cache()
        
        # 创建对象
        obj1 = {'data': 'important'}
        obj2 = {'data': 'also_important'}
        
        cache.set('key1', obj1)
        cache.set('key2', obj2)
        
        # 删除一个对象
        del obj1
        
        # 强制垃圾回收
        gc.collect()
        
        return {
            'key1_exists': cache.get('key1') is not None,
            'key2_exists': cache.get('key2') is not None
        }
    
    @staticmethod
    def optimize_list_operations():
        """优化列表操作"""
        # 预分配列表大小
        def grow_list_dynamically(n):
            result = []
            for i in range(n):
                result.append(i)
            return result
        
        def preallocate_list(n):
            result = [None] * n
            for i in range(n):
                result[i] = i
            return result
        
        n = 100000
        suite = BenchmarkSuite()
        suite.compare_functions({
            'dynamic_growth': grow_list_dynamically,
            'preallocated': preallocate_list
        }, n)
        return suite.results
```

### 3.2 垃圾回收优化

```python
class GarbageCollectionOptimization:
    """垃圾回收优化"""
    
    @staticmethod
    def manual_garbage_collection():
        """手动垃圾回收"""
        import gc
        
        # 获取垃圾回收统计
        def get_gc_stats():
            return {
                'collections': gc.get_stats(),
                'counts': gc.get_count(),
                'thresholds': gc.get_threshold()
            }
        
        # 执行垃圾回收
        def force_garbage_collection():
            collected = gc.collect()
            return {
                'objects_collected': collected,
                'stats_after': get_gc_stats()
            }
        
        return {
            'initial_stats': get_gc_stats(),
            'after_collection': force_garbage_collection()
        }
    
    @staticmethod
    def optimize_gc_settings():
        """优化垃圾回收设置"""
        import gc
        
        # 获取当前设置
        current_thresholds = gc.get_threshold()
        
        # 设置更激进的垃圾回收
        gc.set_threshold(700, 10, 10)  # 更频繁的垃圾回收
        
        return {
            'original_thresholds': current_thresholds,
            'new_thresholds': gc.get_threshold()
        }
    
    @staticmethod
    def detect_memory_leaks():
        """检测内存泄漏"""
        import tracemalloc
        
        def analyze_memory_usage():
            tracemalloc.start()
            
            # 执行可能产生内存泄漏的操作
            objects = []
            for i in range(1000):
                objects.append({'id': i, 'data': 'x' * 1000})
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            return {
                'current_memory': current,
                'peak_memory': peak,
                'objects_created': len(objects)
            }
        
        return analyze_memory_usage()
```

## 4. 并发优化

### 4.1 异步编程优化

```python
import asyncio
import aiohttp
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class AsyncOptimization:
    """异步编程优化"""
    
    @staticmethod
    async def concurrent_requests(urls: List[str]):
        """并发请求优化"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.create_task(session.get(url))
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses
    
    @staticmethod
    async def batch_processing(items: List[Any], batch_size: int = 10):
        """批量处理优化"""
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            # 并发处理批次
            tasks = [asyncio.create_task(process_item(item)) for item in batch]
            batch_results = await asyncio.gather(*tasks)
            
            results.extend(batch_results)
        
        return results
    
    @staticmethod
    async def process_item(item):
        """处理单个项目"""
        await asyncio.sleep(0.1)  # 模拟处理时间
        return f"processed_{item}"
    
    @staticmethod
    def thread_pool_optimization():
        """线程池优化"""
        def cpu_bound_task(n):
            # 模拟CPU密集型任务
            result = 0
            for i in range(n):
                result += i ** 2
            return result
        
        def io_bound_task():
            # 模拟IO密集型任务
            import time
            time.sleep(0.1)
            return "io_completed"
        
        # 使用线程池处理IO密集型任务
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(io_bound_task) for _ in range(10)]
            results = [future.result() for future in futures]
        
        return results
    
    @staticmethod
    def process_pool_optimization():
        """进程池优化"""
        def cpu_intensive_task(n):
            # CPU密集型任务
            result = 0
            for i in range(n):
                result += i ** 2
            return result
        
        # 使用进程池处理CPU密集型任务
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(cpu_intensive_task, 1000000) for _ in range(4)]
            results = [future.result() for future in futures]
        
        return results
```

### 4.2 并行计算优化

```python
import multiprocessing as mp
from multiprocessing import Pool, Queue, Process
import numpy as np

class ParallelComputing:
    """并行计算优化"""
    
    @staticmethod
    def parallel_data_processing(data: List[Any], num_processes: int = None):
        """并行数据处理"""
        if num_processes is None:
            num_processes = mp.cpu_count()
        
        def process_chunk(chunk):
            # 处理数据块
            return [item * 2 for item in chunk]
        
        # 分割数据
        chunk_size = len(data) // num_processes
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        # 并行处理
        with Pool(processes=num_processes) as pool:
            results = pool.map(process_chunk, chunks)
        
        # 合并结果
        return [item for chunk in results for item in chunk]
    
    @staticmethod
    def parallel_matrix_operations():
        """并行矩阵操作"""
        def matrix_multiply_worker(args):
            matrix_a, matrix_b, start_row, end_row = args
            result = np.zeros((end_row - start_row, matrix_b.shape[1]))
            
            for i in range(start_row, end_row):
                for j in range(matrix_b.shape[1]):
                    for k in range(matrix_a.shape[1]):
                        result[i - start_row, j] += matrix_a[i, k] * matrix_b[k, j]
            
            return result
        
        # 创建测试矩阵
        size = 100
        matrix_a = np.random.rand(size, size)
        matrix_b = np.random.rand(size, size)
        
        # 并行矩阵乘法
        num_processes = mp.cpu_count()
        chunk_size = size // num_processes
        
        args_list = []
        for i in range(num_processes):
            start_row = i * chunk_size
            end_row = start_row + chunk_size if i < num_processes - 1 else size
            args_list.append((matrix_a, matrix_b, start_row, end_row))
        
        with Pool(processes=num_processes) as pool:
            results = pool.map(matrix_multiply_worker, args_list)
        
        # 合并结果
        final_result = np.vstack(results)
        return final_result
    
    @staticmethod
    def shared_memory_optimization():
        """共享内存优化"""
        def worker_function(shared_array, start_idx, end_idx):
            # 在共享内存上操作
            for i in range(start_idx, end_idx):
                shared_array[i] = shared_array[i] * 2
        
        # 创建共享数组
        shared_array = mp.Array('i', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
        # 创建进程
        processes = []
        chunk_size = len(shared_array) // 2
        
        for i in range(2):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < 1 else len(shared_array)
            
            p = Process(target=worker_function, args=(shared_array, start_idx, end_idx))
            processes.append(p)
            p.start()
        
        # 等待所有进程完成
        for p in processes:
            p.join()
        
        return list(shared_array)
```

## 5. 缓存优化

### 5.1 函数缓存

```python
from functools import lru_cache, cache
import time
from typing import Dict, Any

class CacheOptimization:
    """缓存优化"""
    
    @staticmethod
    def lru_cache_example():
        """LRU缓存示例"""
        @lru_cache(maxsize=128)
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        
        # 测试缓存效果
        start_time = time.time()
        result1 = fibonacci(35)
        time1 = time.time() - start_time
        
        start_time = time.time()
        result2 = fibonacci(35)  # 应该从缓存获取
        time2 = time.time() - start_time
        
        return {
            'first_call_time': time1,
            'cached_call_time': time2,
            'speedup': time1 / time2 if time2 > 0 else float('inf'),
            'result': result1
        }
    
    @staticmethod
    def custom_cache_implementation():
        """自定义缓存实现"""
        class CustomCache:
            def __init__(self, max_size=100):
                self.max_size = max_size
                self.cache = {}
                self.access_order = []
            
            def get(self, key):
                if key in self.cache:
                    # 更新访问顺序
                    self.access_order.remove(key)
                    self.access_order.append(key)
                    return self.cache[key]
                return None
            
            def set(self, key, value):
                if key in self.cache:
                    # 更新现有项
                    self.access_order.remove(key)
                elif len(self.cache) >= self.max_size:
                    # 移除最久未使用的项
                    oldest_key = self.access_order.pop(0)
                    del self.cache[oldest_key]
                
                self.cache[key] = value
                self.access_order.append(key)
        
        return CustomCache()
    
    @staticmethod
    def cache_invalidation_strategies():
        """缓存失效策略"""
        class TimeBasedCache:
            def __init__(self, ttl_seconds=300):
                self.cache = {}
                self.ttl = ttl_seconds
            
            def get(self, key):
                if key in self.cache:
                    value, timestamp = self.cache[key]
                    if time.time() - timestamp < self.ttl:
                        return value
                    else:
                        del self.cache[key]
                return None
            
            def set(self, key, value):
                self.cache[key] = (value, time.time())
        
        return TimeBasedCache()
```

### 5.2 数据缓存

```python
import redis
import json
import pickle
from typing import Any, Optional

class DataCacheOptimization:
    """数据缓存优化"""
    
    @staticmethod
    def redis_cache_example():
        """Redis缓存示例"""
        # 连接Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        def cache_function_result(func, key, ttl=300):
            """缓存函数结果"""
            # 尝试从缓存获取
            cached_result = r.get(key)
            if cached_result:
                return pickle.loads(cached_result)
            
            # 执行函数并缓存结果
            result = func()
            r.setex(key, ttl, pickle.dumps(result))
            return result
        
        return cache_function_result
    
    @staticmethod
    def in_memory_cache_with_eviction():
        """带淘汰策略的内存缓存"""
        from collections import OrderedDict
        
        class LRUCache:
            def __init__(self, capacity=1000):
                self.capacity = capacity
                self.cache = OrderedDict()
            
            def get(self, key):
                if key in self.cache:
                    # 移动到末尾（最近使用）
                    self.cache.move_to_end(key)
                    return self.cache[key]
                return None
            
            def put(self, key, value):
                if key in self.cache:
                    # 更新现有项
                    self.cache.move_to_end(key)
                elif len(self.cache) >= self.capacity:
                    # 移除最久未使用的项
                    self.cache.popitem(last=False)
                
                self.cache[key] = value
            
            def size(self):
                return len(self.cache)
        
        return LRUCache()
    
    @staticmethod
    def cache_serialization_optimization():
        """缓存序列化优化"""
        import json
        import pickle
        import msgpack
        
        data = {'name': 'John', 'age': 30, 'city': 'New York'}
        
        # 比较不同序列化方法
        json_size = len(json.dumps(data))
        pickle_size = len(pickle.dumps(data))
        msgpack_size = len(msgpack.packb(data))
        
        return {
            'json_size': json_size,
            'pickle_size': pickle_size,
            'msgpack_size': msgpack_size,
            'fastest': min(json_size, pickle_size, msgpack_size)
        }
```

## 6. 数据库优化

### 6.1 查询优化

```python
from sqlalchemy import create_engine, text, Index
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Dict, Any

Base = declarative_base()

class DatabaseOptimization:
    """数据库优化"""
    
    @staticmethod
    def optimize_sql_queries():
        """SQL查询优化"""
        # 创建数据库连接
        engine = create_engine('sqlite:///test.db')
        Session = sessionmaker(bind=engine)
        
        # 创建表
        from sqlalchemy import Column, Integer, String, ForeignKey
        from sqlalchemy.orm import relationship
        
        class User(Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            email = Column(String(100))
            orders = relationship("Order", back_populates="user")
        
        class Order(Base):
            __tablename__ = 'orders'
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('users.id'))
            amount = Column(Integer)
            user = relationship("User", back_populates="orders")
        
        Base.metadata.create_all(engine)
        
        # 优化查询示例
        session = Session()
        
        # 1. 使用索引
        Index('idx_user_email', User.email)
        
        # 2. 使用JOIN而不是N+1查询
        users_with_orders = session.query(User).options(
            joinedload(User.orders)
        ).all()
        
        # 3. 使用批量操作
        def batch_insert_users(users_data):
            users = [User(**data) for data in users_data]
            session.bulk_save_objects(users)
            session.commit()
        
        # 4. 使用原生SQL优化复杂查询
        def optimized_complex_query():
            query = text("""
                SELECT u.name, COUNT(o.id) as order_count, SUM(o.amount) as total_amount
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                GROUP BY u.id, u.name
                HAVING total_amount > 1000
                ORDER BY total_amount DESC
            """)
            return session.execute(query)
        
        session.close()
        return "Database optimization examples completed"
    
    @staticmethod
    def connection_pool_optimization():
        """连接池优化"""
        from sqlalchemy.pool import QueuePool
        
        # 配置连接池
        engine = create_engine(
            'sqlite:///test.db',
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=3600
        )
        
        return {
            'pool_size': 10,
            'max_overflow': 20,
            'pool_timeout': 30,
            'pool_recycle': 3600
        }
```

### 6.2 索引优化

```python
class IndexOptimization:
    """索引优化"""
    
    @staticmethod
    def create_optimal_indexes():
        """创建最优索引"""
        from sqlalchemy import Index, UniqueConstraint
        
        class OptimizedUser(Base):
            __tablename__ = 'optimized_users'
            id = Column(Integer, primary_key=True)
            email = Column(String(100), unique=True)
            username = Column(String(50))
            created_at = Column(DateTime)
            
            # 复合索引
            __table_args__ = (
                Index('idx_username_email', 'username', 'email'),
                Index('idx_created_at', 'created_at'),
                UniqueConstraint('email', name='uq_email')
            )
        
        return OptimizedUser
    
    @staticmethod
    def query_plan_analysis():
        """查询计划分析"""
        # 使用EXPLAIN分析查询
        explain_query = text("""
            EXPLAIN QUERY PLAN
            SELECT * FROM users 
            WHERE email = 'test@example.com' 
            AND created_at > '2023-01-01'
        """)
        
        return explain_query
```

## 7. 网络优化

### 7.1 HTTP请求优化

```python
import aiohttp
import requests
from typing import List, Dict, Any
import asyncio

class NetworkOptimization:
    """网络优化"""
    
    @staticmethod
    async def async_http_requests():
        """异步HTTP请求优化"""
        async def fetch_url(session, url):
            async with session.get(url) as response:
                return await response.text()
        
        urls = [
            'https://httpbin.org/delay/1',
            'https://httpbin.org/delay/2',
            'https://httpbin.org/delay/3'
        ]
        
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
        
        return results
    
    @staticmethod
    def connection_pooling():
        """连接池优化"""
        import requests
        
        # 使用Session复用连接
        session = requests.Session()
        
        # 配置连接池
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        return session
    
    @staticmethod
    def request_batching():
        """请求批处理"""
        async def batch_requests(urls: List[str], batch_size: int = 5):
            """批量处理请求"""
            results = []
            
            for i in range(0, len(urls), batch_size):
                batch = urls[i:i + batch_size]
                
                async with aiohttp.ClientSession() as session:
                    tasks = [session.get(url) for url in batch]
                    responses = await asyncio.gather(*tasks)
                    
                    for response in responses:
                        results.append(await response.text())
            
            return results
        
        return batch_requests
```

### 7.2 数据传输优化

```python
import gzip
import json
import pickle
from typing import Any, Dict

class DataTransferOptimization:
    """数据传输优化"""
    
    @staticmethod
    def compression_optimization():
        """压缩优化"""
        data = "This is a very long string that needs to be compressed for efficient transmission"
        
        # 原始大小
        original_size = len(data.encode('utf-8'))
        
        # Gzip压缩
        compressed_data = gzip.compress(data.encode('utf-8'))
        compressed_size = len(compressed_data)
        
        # 压缩率
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio
        }
    
    @staticmethod
    def serialization_optimization():
        """序列化优化"""
        data = {
            'users': [
                {'id': i, 'name': f'user_{i}', 'email': f'user_{i}@example.com'}
                for i in range(1000)
            ]
        }
        
        # 比较不同序列化方法
        json_size = len(json.dumps(data))
        pickle_size = len(pickle.dumps(data))
        
        return {
            'json_size': json_size,
            'pickle_size': pickle_size,
            'recommended': 'json' if json_size < pickle_size else 'pickle'
        }
```

---

## 总结

Python性能优化指南涵盖了以下关键领域：

1. **性能分析基础**：使用各种工具分析代码性能
2. **算法优化**：选择合适的数据结构和算法
3. **内存优化**：减少内存使用和避免内存泄漏
4. **并发优化**：利用异步编程和并行计算
5. **缓存优化**：使用各种缓存策略提高性能
6. **数据库优化**：优化查询和索引
7. **网络优化**：优化HTTP请求和数据传输

通过这些优化技术，开发者可以：

- 显著提高应用程序性能
- 减少资源消耗
- 提升用户体验
- 降低运营成本

建议根据具体应用场景选择合适的优化策略，并通过基准测试验证优化效果。
