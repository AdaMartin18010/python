# Counting Sort - 计数排序

## 目录

- [1. 概述](#1-概述)
- [2. 算法原理](#2-算法原理)
- [3. Python实现](#3-python实现)
- [4. 复杂度分析](#4-复杂度分析)
- [5. 应用场景](#5-应用场景)
- [6. 与其他排序算法对比](#6-与其他排序算法对比)
- [7. LeetCode相关题目](#7-leetcode相关题目)
- [8. 性能测试](#8-性能测试)
- [9. 常见陷阱与最佳实践](#9-常见陷阱与最佳实践)
- [10. 总结](#10-总结)

---

## 1. 概述

**计数排序（Counting Sort）** 是一种非比较排序算法，通过统计每个元素出现的次数来实现排序。

### 核心特点

- ⏱️ **时间复杂度**: O(n+k) - k是数据范围
- 💾 **空间复杂度**: O(k) 
- 🔄 **稳定性**: 稳定
- 📊 **适用场景**: 整数排序、范围小

### 算法优势

✅ **线性时间** - O(n+k)比O(n log n)更快  
✅ **稳定排序** - 保持相同元素相对顺序  
✅ **可预测** - 性能不受数据分布影响

### 算法劣势

❌ **仅限整数** - 只能排序非负整数  
❌ **空间消耗** - 数据范围大时空间大  
❌ **范围限制** - 数据范围必须已知

---

## 2. 算法原理

### 核心思想

```
1. 统计每个值出现的次数
2. 计算累计次数（确定位置）
3. 从后向前填充结果数组

示例: [2, 5, 3, 0, 2, 3, 0, 3]

步骤1: 统计次数
count[0] = 2  (0出现2次)
count[1] = 0
count[2] = 2  (2出现2次)
count[3] = 3  (3出现3次)
count[4] = 0
count[5] = 1  (5出现1次)

步骤2: 累计次数
count[0] = 2  (≤0的有2个)
count[1] = 2  (≤1的有2个)
count[2] = 4  (≤2的有4个)
count[3] = 7  (≤3的有7个)
count[4] = 7
count[5] = 8  (≤5的有8个)

步骤3: 填充结果
从后向前遍历原数组，根据count确定位置

结果: [0, 0, 2, 2, 3, 3, 3, 5]
```

---

## 3. Python实现

### 3.1 基础实现

```python
from typing import List

def counting_sort(arr: List[int]) -> List[int]:
    """
    计数排序 - 基础实现
    
    时间复杂度: O(n+k) where k = max(arr) - min(arr) + 1
    空间复杂度: O(k)
    稳定性: 稳定
    
    Args:
        arr: 待排序数组（非负整数）
    
    Returns:
        排序后的数组
    
    Example:
        >>> counting_sort([2, 5, 3, 0, 2, 3, 0, 3])
        [0, 0, 2, 2, 3, 3, 3, 5]
    """
    if not arr:
        return arr
    
    # 找出最大值和最小值
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    # 创建计数数组
    count = [0] * range_size
    output = [0] * len(arr)
    
    # 统计每个元素出现次数
    for num in arr:
        count[num - min_val] += 1
    
    # 计算累计次数
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    # 从后向前填充结果数组（保持稳定性）
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        index = count[num - min_val] - 1
        output[index] = num
        count[num - min_val] -= 1
    
    return output


def counting_sort_simple(arr: List[int]) -> List[int]:
    """
    计数排序 - 简化版（仅适用于非负整数）
    
    不保证稳定性，但更简单
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    count = [0] * (max_val + 1)
    
    # 统计次数
    for num in arr:
        count[num] += 1
    
    # 重建数组
    result = []
    for num, freq in enumerate(count):
        result.extend([num] * freq)
    
    return result
```

### 3.2 优化实现

```python
def counting_sort_optimized(arr: List[int]) -> List[int]:
    """
    计数排序 - 优化版
    
    优化点：
    1. 处理负数
    2. 减少空间使用
    3. 原地排序（如果可能）
    """
    if not arr:
        return arr
    
    # 找范围
    max_val = max(arr)
    min_val = min(arr)
    
    # 特殊情况：所有元素相同
    if max_val == min_val:
        return arr
    
    range_size = max_val - min_val + 1
    count = [0] * range_size
    
    # 统计
    for num in arr:
        count[num - min_val] += 1
    
    # 重建
    index = 0
    for num in range(range_size):
        while count[num] > 0:
            arr[index] = num + min_val
            index += 1
            count[num] -= 1
    
    return arr
```

---

## 4. 复杂度分析

### 4.1 时间复杂度

**O(n + k)** - 其中n是元素个数，k是数据范围

```python
# 分析：
# 1. 找最大最小值: O(n)
# 2. 统计次数: O(n)
# 3. 计算累计: O(k)
# 4. 填充结果: O(n)
#
# 总计: O(n + k)

# 当k = O(n)时，总复杂度为O(n)
# 当k >> n时，复杂度主要取决于k
```

### 4.2 空间复杂度

**O(k)** - 需要额外的计数数组

```python
# count数组: O(k)
# output数组: O(n)
# 总空间: O(n + k)
```

### 4.3 稳定性

**稳定排序** ✅

```python
# 从后向前填充保证稳定性
# 相同元素按原顺序排列
```

---

## 5. 应用场景

### ✅ 适用场景

1. **整数排序**
   ```python
   ages = [25, 18, 30, 22, 18, 25]
   counting_sort(ages)
   ```

2. **范围小的数据**
   ```python
   grades = [85, 90, 75, 85, 95, 80]  # 0-100
   counting_sort(grades)
   ```

3. **需要稳定性**
   ```python
   # 多关键字排序的子过程
   ```

### ❌ 不适用场景

1. **浮点数**
   ```python
   # 计数排序只适用于整数
   ```

2. **范围很大**
   ```python
   # 数据范围大时空间消耗大
   arr = [1, 1000000]  # 需要1000000大小的数组
   ```

---

## 6. 与其他排序算法对比

| 算法 | 时间 | 空间 | 稳定性 | 适用 |
|-----|------|------|--------|------|
| **计数排序** | O(n+k) | O(k) | ✅ | 整数、范围小 |
| **基数排序** | O(d(n+k)) | O(n+k) | ✅ | 整数 |
| **桶排序** | O(n+k) | O(n+k) | ✅ | 均匀分布 |
| **快速排序** | O(n log n) | O(log n) | ❌ | 通用 |

---

## 7. LeetCode相关题目

| 题号 | 题目 | 难度 | 考点 |
|-----|------|------|------|
| 912 | 排序数组 | Medium | 排序实现 |
| 75 | 颜色分类 | Medium | 计数排序应用 |
| 274 | H指数 | Medium | 计数+排序 |
| 451 | 根据字符出现频率排序 | Medium | 计数排序 |

---

## 8. 性能测试

```python
import time
import random

def benchmark_counting_sort():
    """性能测试"""
    
    # 小范围大数据
    arr = [random.randint(0, 100) for _ in range(10000)]
    
    start = time.perf_counter()
    counting_sort(arr.copy())
    counting_time = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    sorted(arr)
    python_time = (time.perf_counter() - start) * 1000
    
    print(f"计数排序: {counting_time:.3f}ms")
    print(f"Python内置: {python_time:.3f}ms")

benchmark_counting_sort()
```

---

## 9. 常见陷阱与最佳实践

### 陷阱1：忘记处理负数

```python
# ❌ 错误
def counting_sort_wrong(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    # 负数会导致索引错误！

# ✅ 正确
def counting_sort_correct(arr):
    max_val = max(arr)
    min_val = min(arr)
    count = [0] * (max_val - min_val + 1)
```

### 陷阱2：范围过大导致内存溢出

```python
# ❌ 危险
arr = [1, 10000000]
counting_sort(arr)  # 需要10000000大小的数组！

# ✅ 检查范围
def safe_counting_sort(arr, max_range=1000000):
    range_size = max(arr) - min(arr) + 1
    if range_size > max_range:
        return sorted(arr)  # 使用其他算法
    return counting_sort(arr)
```

### 最佳实践

✅ **检查数据范围**
```python
def smart_sort(arr):
    if not arr:
        return arr
    
    range_size = max(arr) - min(arr) + 1
    
    # 范围小：计数排序
    if range_size < len(arr) * 10:
        return counting_sort(arr)
    
    # 范围大：快速排序
    return sorted(arr)
```

---

## 10. 总结

计数排序是一种高效的非比较排序算法，在特定场景下性能优异。

### 核心要点

✅ **时间复杂度**: O(n+k) - 线性时间  
✅ **空间复杂度**: O(k)  
✅ **稳定性**: 稳定排序  
✅ **限制**: 仅适用于整数、范围小的数据

### 使用建议

- ✅ 整数排序
- ✅ 数据范围小（k ≈ n）
- ✅ 需要稳定性
- ❌ 浮点数
- ❌ 数据范围大（k >> n）

计数排序是理解非比较排序的excellent起点！🚀
