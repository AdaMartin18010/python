# Quick Sort - 快速排序

## 📚 概述

**快速排序**是最常用的排序算法之一，由Tony Hoare在1960年提出。它使用分治策略，平均时间复杂度为O(n log n)，是实际应用中最快的排序算法之一。

## 🎯 核心概念

### 算法思想

1. 选择一个**基准元素**（pivot）
2. **分区**：将小于pivot的元素移到左边，大于pivot的移到右边
3. **递归**：对左右两个子数组重复此过程

### 复杂度分析

| 情况 | 时间复杂度 | 空间复杂度 |
|------|------------|------------|
| 最好 | O(n log n) | O(log n) |
| 平均 | O(n log n) | O(log n) |
| 最坏 | O(n²) | O(n) |
| 稳定性 | ❌ 不稳定 | - |

### 特点

**优势**:

- ✅ 平均性能优秀
- ✅ 原地排序（in-place）
- ✅ 缓存友好
- ✅ 实际应用中很快

**劣势**:

- ⚠️ 最坏情况O(n²)
- ⚠️ 不稳定排序
- ⚠️ 递归深度可能很大

## 💡 Python实现

### 1. 经典实现（Lomuto分区）⭐⭐⭐⭐

```python
def quick_sort(arr: list[int]) -> list[int]:
    """快速排序（Lomuto分区方案）"""
    if len(arr) <= 1:
        return arr
    
    def partition(low: int, high: int) -> int:
        """分区函数"""
        pivot = arr[high]  # 选择最后一个元素作为pivot
        i = low - 1  # 小于pivot的区域边界
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def quick_sort_helper(low: int, high: int) -> None:
        """递归排序"""
        if low < high:
            pi = partition(low, high)
            quick_sort_helper(low, pi - 1)
            quick_sort_helper(pi + 1, high)
    
    quick_sort_helper(0, len(arr) - 1)
    return arr


# 使用
data = [64, 34, 25, 12, 22, 11, 90]
sorted_data = quick_sort(data)
print(sorted_data)  # [11, 12, 22, 25, 34, 64, 90]
```

### 2. Hoare分区方案 ⭐⭐⭐⭐⭐

```python
def quick_sort_hoare(arr: list[int]) -> list[int]:
    """快速排序（Hoare分区方案 - 更高效）"""
    
    def partition(low: int, high: int) -> int:
        """Hoare分区"""
        pivot = arr[low]  # 选择第一个元素作为pivot
        i = low - 1
        j = high + 1
        
        while True:
            i += 1
            while arr[i] < pivot:
                i += 1
            
            j -= 1
            while arr[j] > pivot:
                j -= 1
            
            if i >= j:
                return j
            
            arr[i], arr[j] = arr[j], arr[i]
    
    def sort_helper(low: int, high: int) -> None:
        if low < high:
            pi = partition(low, high)
            sort_helper(low, pi)
            sort_helper(pi + 1, high)
    
    sort_helper(0, len(arr) - 1)
    return arr
```

### 3. 三路快排（处理重复元素）⭐⭐⭐⭐⭐

```python
def quick_sort_3way(arr: list[int]) -> list[int]:
    """三路快速排序（优化重复元素）"""
    
    def sort_3way(low: int, high: int) -> None:
        if low >= high:
            return
        
        # 三路分区: < pivot | == pivot | > pivot
        lt = low  # arr[low..lt-1] < pivot
        gt = high  # arr[gt+1..high] > pivot
        i = low + 1  # arr[lt..i-1] == pivot
        pivot = arr[low]
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        
        # 递归排序左右两部分
        sort_3way(low, lt - 1)
        sort_3way(gt + 1, high)
    
    sort_3way(0, len(arr) - 1)
    return arr


# 对有大量重复元素的数组特别有效
data = [4, 2, 7, 2, 4, 2, 7, 9, 4, 2]
sorted_data = quick_sort_3way(data)
```

### 4. 优化版本（实用）⭐⭐⭐⭐⭐

```python
import random


def quick_sort_optimized(arr: list[int]) -> list[int]:
    """优化的快速排序"""
    
    INSERTION_SORT_THRESHOLD = 10  # 小数组使用插入排序
    
    def insertion_sort(low: int, high: int) -> None:
        """插入排序（小数组）"""
        for i in range(low + 1, high + 1):
            key = arr[i]
            j = i - 1
            while j >= low and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
    
    def median_of_three(low: int, high: int) -> int:
        """三数取中选择pivot"""
        mid = (low + high) // 2
        if arr[low] > arr[mid]:
            arr[low], arr[mid] = arr[mid], arr[low]
        if arr[low] > arr[high]:
            arr[low], arr[high] = arr[high], arr[low]
        if arr[mid] > arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]
        return mid
    
    def partition(low: int, high: int) -> int:
        """优化的分区"""
        # 三数取中
        pivot_idx = median_of_three(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        pivot = arr[high]
        
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def sort_helper(low: int, high: int) -> None:
        """优化的排序"""
        while low < high:
            # 小数组使用插入排序
            if high - low < INSERTION_SORT_THRESHOLD:
                insertion_sort(low, high)
                return
            
            pi = partition(low, high)
            
            # 尾递归优化：先排序较小的部分
            if pi - low < high - pi:
                sort_helper(low, pi - 1)
                low = pi + 1  # 尾递归转换为迭代
            else:
                sort_helper(pi + 1, high)
                high = pi - 1
    
    if arr:
        sort_helper(0, len(arr) - 1)
    return arr
```

### 5. 函数式实现 ⭐⭐⭐

```python
def quick_sort_functional(arr: list[int]) -> list[int]:
    """函数式快速排序（简洁但需要额外空间）"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort_functional(left) + middle + quick_sort_functional(right)
```

## 🏗️ 现代Python实现（2025标准）

### 类型安全的泛型快排

```python
from typing import TypeVar, Callable


T = TypeVar('T')


def quick_sort_generic(
    arr: list[T],
    key: Callable[[T], Any] | None = None,
    reverse: bool = False
) -> list[T]:
    """泛型快速排序"""
    
    if key is None:
        key = lambda x: x
    
    def compare(a: T, b: T) -> bool:
        """比较函数"""
        if reverse:
            return key(a) > key(b)
        return key(a) < key(b)
    
    def partition(low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if compare(arr[j], pivot) or key(arr[j]) == key(pivot):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def sort_helper(low: int, high: int) -> None:
        if low < high:
            pi = partition(low, high)
            sort_helper(low, pi - 1)
            sort_helper(pi + 1, high)
    
    if arr:
        sort_helper(0, len(arr) - 1)
    return arr


# 使用示例
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

people = [
    Person("Alice", 30),
    Person("Bob", 25),
    Person("Charlie", 35)
]

# 按年龄排序
sorted_people = quick_sort_generic(people, key=lambda p: p.age)
```

## 📊 性能对比

### 不同实现的性能

```python
import timeit
import random


def benchmark_sorts():
    """性能测试"""
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        data = [random.randint(1, 1000) for _ in range(size)]
        
        # Lomuto分区
        lomuto_time = timeit.timeit(
            lambda: quick_sort(data.copy()),
            number=10
        )
        
        # Hoare分区
        hoare_time = timeit.timeit(
            lambda: quick_sort_hoare(data.copy()),
            number=10
        )
        
        # 三路快排
        three_way_time = timeit.timeit(
            lambda: quick_sort_3way(data.copy()),
            number=10
        )
        
        # Python内置
        builtin_time = timeit.timeit(
            lambda: sorted(data.copy()),
            number=10
        )
        
        print(f"\nSize: {size}")
        print(f"Lomuto:    {lomuto_time:.4f}s")
        print(f"Hoare:     {hoare_time:.4f}s")
        print(f"3-Way:     {three_way_time:.4f}s")
        print(f"Built-in:  {builtin_time:.4f}s")
```

**典型结果**（参考）:

- Hoare分区比Lomuto快~15%
- 三路快排在有重复元素时更快
- Python内置sort（Timsort）更稳定

## 🎯 应用场景

### 1. Top K问题（快速选择）

```python
def quick_select(arr: list[int], k: int) -> int:
    """找到第k小的元素（O(n)平均）"""
    
    def partition(low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    low, high = 0, len(arr) - 1
    
    while low <= high:
        pi = partition(low, high)
        
        if pi == k - 1:
            return arr[pi]
        elif pi < k - 1:
            low = pi + 1
        else:
            high = pi - 1
    
    return -1


# 找到第5小的元素
data = [7, 10, 4, 3, 20, 15]
result = quick_select(data, 3)  # 7
```

### 2. 并行快速排序

```python
from concurrent.futures import ThreadPoolExecutor


def parallel_quick_sort(
    arr: list[int],
    max_workers: int = 4
) -> list[int]:
    """并行快速排序"""
    
    def sort_parallel(low: int, high: int, depth: int = 0) -> None:
        if low >= high:
            return
        
        pi = partition(low, high)
        
        # 深度较浅时并行执行
        if depth < 2:
            with ThreadPoolExecutor(max_workers=2) as executor:
                future1 = executor.submit(
                    sort_parallel, low, pi - 1, depth + 1
                )
                future2 = executor.submit(
                    sort_parallel, pi + 1, high, depth + 1
                )
                future1.result()
                future2.result()
        else:
            # 深度较深时串行执行
            sort_parallel(low, pi - 1, depth + 1)
            sort_parallel(pi + 1, high, depth + 1)
    
    def partition(low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    if arr:
        sort_parallel(0, len(arr) - 1)
    return arr
```

## 📚 最佳实践

### 1. 选择合适的pivot

```python
# ✅ 好：三数取中
def median_of_three(arr, low, high):
    mid = (low + high) // 2
    # 排序low, mid, high
    # 返回中位数索引

# ❌ 差：总是选择第一个或最后一个
# 对已排序数组会退化到O(n²)
```

### 2. 处理小数组

```python
# ✅ 好：小数组切换到插入排序
if size < 10:
    insertion_sort(arr)
else:
    quick_sort(arr)
```

### 3. 避免栈溢出

```python
# ✅ 好：尾递归优化
while low < high:
    pi = partition(low, high)
    if pi - low < high - pi:
        sort(low, pi - 1)  # 递归较小部分
        low = pi + 1        # 迭代较大部分
    else:
        sort(pi + 1, high)
        high = pi - 1
```

## 🔗 相关算法

- **Merge Sort**: 稳定的O(n log n)
- **Heap Sort**: 最坏O(n log n)
- **Intro Sort**: 混合算法（C++ std::sort）

## 📚 参考资源

- **Algorithms** - Robert Sedgewick
- **Introduction to Algorithms** - CLRS
- **The Art of Computer Programming** - Donald Knuth

---

**快速排序：实践中最快的通用排序算法！** ⚡
