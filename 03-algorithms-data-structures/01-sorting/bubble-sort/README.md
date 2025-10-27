# Bubble Sort - 冒泡排序

## 目录

- [1. 概述](#1-概述)
- [2. 算法原理](#2-算法原理)
- [3. Python实现](#3-python实现)
- [4. 复杂度分析](#4-复杂度分析)
- [5. 应用场景](#5-应用场景)
- [6. 与其他排序算法对比](#6-与其他排序算法对比)
- [7. 性能测试](#8-性能测试)
- [8. 常见陷阱与最佳实践](#9-常见陷阱与最佳实践)
- [9. 总结](#10-总结)

---

## 1. 概述

**冒泡排序（Bubble Sort）** 是最简单的排序算法，通过重复交换相邻的错序元素来排序。

### 核心特点

- ⏱️ **时间复杂度**: O(n²) 平均 / O(n) 最好
- 💾 **空间复杂度**: O(1)
- 🔄 **稳定性**: 稳定
- 📊 **适用场景**: 教学、小数据

### 算法优势

✅ **实现最简单** - 代码最容易理解  
✅ **稳定排序** - 保持相同元素相对顺序  
✅ **原地排序** - 不需要额外空间  
✅ **自适应** - 已排序时O(n)

### 算法劣势

❌ **效率最低** - O(n²)性能差  
❌ **实用性差** - 实际几乎不用  
❌ **交换次数多** - 比插入排序慢

---

## 2. 算法原理

### 核心思想

```
重复遍历数组，比较相邻元素
如果顺序错误就交换
每轮把最大元素"冒泡"到末尾

示例: [5, 2, 4, 6, 1, 3]

第1轮: [2, 4, 5, 1, 3, 6]  # 6冒泡到末尾
第2轮: [2, 4, 1, 3, 5, 6]  # 5冒泡
第3轮: [2, 1, 3, 4, 5, 6]  # 4冒泡
第4轮: [1, 2, 3, 4, 5, 6]  # 3冒泡
第5轮: [1, 2, 3, 4, 5, 6]  # 已排序

结果: [1, 2, 3, 4, 5, 6]
```

---

## 3. Python实现

### 3.1 基础实现

```python
from typing import List

def bubble_sort(arr: List[int]) -> List[int]:
    """
    冒泡排序 - 基础实现
    
    时间复杂度: O(n²)
    空间复杂度: O(1)
    稳定性: 稳定
    
    Example:
        >>> bubble_sort([5, 2, 4, 6, 1, 3])
        [1, 2, 3, 4, 5, 6]
    """
    n = len(arr)
    
    for i in range(n - 1):
        # 每轮把最大元素冒泡到末尾
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr
```

### 3.2 优化实现

```python
def bubble_sort_optimized(arr: List[int]) -> List[int]:
    """
    冒泡排序 - 优化版
    
    优化：如果某轮没有交换，说明已排序，提前退出
    
    最好情况: O(n) - 已排序
    平均情况: O(n²)
    最坏情况: O(n²)
    """
    n = len(arr)
    
    for i in range(n - 1):
        swapped = False
        
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # 如果本轮没有交换，说明已排序
        if not swapped:
            break
    
    return arr
```

### 3.3 鸡尾酒排序

```python
def cocktail_sort(arr: List[int]) -> List[int]:
    """
    鸡尾酒排序 - 双向冒泡排序
    
    优化：交替从两端冒泡
    """
    n = len(arr)
    left = 0
    right = n - 1
    
    while left < right:
        # 从左到右冒泡
        for i in range(left, right):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        right -= 1
        
        # 从右到左冒泡
        for i in range(right, left, -1):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
        left += 1
    
    return arr
```

---

## 4. 复杂度分析

### 时间复杂度

**O(n²) 平均 / O(n) 最好**

```python
# 最坏情况（逆序）:
# 比较: n(n-1)/2 = O(n²)
# 交换: n(n-1)/2 = O(n²)

# 最好情况（已排序）:
# 比较: n-1 = O(n)
# 交换: 0

# 平均情况:
# O(n²)
```

### 空间复杂度

**O(1)** - 原地排序

### 稳定性

**稳定排序** ✅

---

## 5. 应用场景

### ✅ 适用场景

1. **教学用途**
   ```python
   # 最容易理解的排序算法
   # 适合教学演示
   ```

2. **小数据 + 基本有序**
   ```python
   small_sorted = [1, 2, 3, 5, 4]
   bubble_sort(small_sorted)  # O(n)
   ```

### ❌ 不适用场景

1. **生产环境**
   ```python
   # 性能太差
   # 使用更好的算法
   ```

2. **大数据**
   ```python
   # O(n²)不可接受
   ```

---

## 6. 与其他排序算法对比

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定性 |
|-----|------|------|------|------|--------|
| **冒泡排序** | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| **插入排序** | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| **选择排序** | O(n²) | O(n²) | O(n²) | O(1) | ❌ |

**结论**：冒泡排序通常比插入排序慢，实际很少使用。

---

## 7. 性能测试

```python
def compare_bubble_insert():
    """对比冒泡和插入排序"""
    import time
    import random
    
    arr = [random.randint(1, 1000) for _ in range(1000)]
    
    start = time.perf_counter()
    bubble_sort(arr.copy())
    bubble_time = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    insertion_sort(arr.copy())
    insertion_time = (time.perf_counter() - start) * 1000
    
    print(f"冒泡排序: {bubble_time:.3f}ms")
    print(f"插入排序: {insertion_time:.3f}ms")
    print(f"插入排序快 {bubble_time/insertion_time:.2f}倍")

compare_bubble_insert()
```

---

## 8. 常见陷阱与最佳实践

### 陷阱：忘记优化标志

```python
# ❌ 低效：无法提前退出
def bubble_sort_slow(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# ✅ 高效：使用优化标志
def bubble_sort_fast(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
```

### 最佳实践

✅ **仅用于教学**
```python
# 生产环境使用Python内置sorted()
# 冒泡排序主要用于理解排序概念
```

---

## 9. 总结

冒泡排序是最简单但效率最低的排序算法，主要用于教学。

### 核心要点

✅ **时间复杂度**: O(n²) - 性能差  
✅ **空间复杂度**: O(1)  
✅ **稳定性**: 稳定  
✅ **用途**: 教学演示

### 使用建议

- 📚 **教学用途**: 理解排序概念
- ❌ **生产环境**: 使用更好的算法
- ❌ **大数据**: 性能不可接受

冒泡排序虽简单，但实际价值有限！🚀
