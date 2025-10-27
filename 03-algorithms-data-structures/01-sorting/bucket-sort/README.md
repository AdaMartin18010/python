# Bucket Sort - 桶排序

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

**桶排序（Bucket Sort）** 是一种分布式排序算法，将元素分配到不同的桶中，然后对每个桶排序。

### 核心特点

- ⏱️ **时间复杂度**: O(n+k) 平均 / O(n²) 最坏
- 💾 **空间复杂度**: O(n+k)
- 🔄 **稳定性**: 可以稳定
- 📊 **适用场景**: 均匀分布的浮点数

### 算法优势

✅ **线性时间** - 数据均匀分布时O(n)  
✅ **灵活性** - 适合浮点数  
✅ **可并行** - 每个桶可独立排序

### 算法劣势

❌ **依赖分布** - 数据分布不均时性能差  
❌ **空间消耗** - 需要额外桶空间  
❌ **桶数量** - 需要合适的桶数量

---

## 2. 算法原理

### 核心思想

```
1. 设置固定数量的桶
2. 将元素分配到对应的桶
3. 对每个桶内排序
4. 依次收集所有桶的元素

示例: [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]

假设10个桶，范围[0, 1):

桶0 [0.0-0.1): []
桶1 [0.1-0.2): [0.17, 0.12]
桶2 [0.2-0.3): [0.26, 0.21, 0.23]
桶3 [0.3-0.4): [0.39]
桶4 [0.4-0.5): []
桶5 [0.5-0.6): []
桶6 [0.6-0.7): [0.68]
桶7 [0.7-0.8): [0.78, 0.72]
桶8 [0.8-0.9): []
桶9 [0.9-1.0): [0.94]

对每个桶排序后收集:
[0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]
```

---

## 3. Python实现

### 3.1 基础实现

```python
from typing import List

def bucket_sort(arr: List[float]) -> List[float]:
    """
    桶排序 - 基础实现
    
    时间复杂度: O(n+k) 平均
    空间复杂度: O(n+k)
    稳定性: 稳定（如果桶内排序稳定）
    
    Args:
        arr: 待排序数组（浮点数，范围[0, 1)）
    
    Returns:
        排序后的数组
    
    Example:
        >>> bucket_sort([0.78, 0.17, 0.39, 0.26, 0.72])
        [0.17, 0.26, 0.39, 0.72, 0.78]
    """
    if not arr:
        return arr
    
    n = len(arr)
    
    # 创建n个桶
    buckets = [[] for _ in range(n)]
    
    # 将元素分配到桶中
    for num in arr:
        index = int(num * n)
        buckets[index].append(num)
    
    # 对每个桶排序
    for bucket in buckets:
        bucket.sort()  # 或使用插入排序
    
    # 收集结果
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result


def bucket_sort_general(arr: List[float], num_buckets: int = 10) -> List[float]:
    """
    桶排序 - 通用实现
    
    支持任意范围的浮点数
    """
    if not arr:
        return arr
    
    # 找范围
    min_val = min(arr)
    max_val = max(arr)
    range_val = max_val - min_val
    
    # 创建桶
    buckets = [[] for _ in range(num_buckets)]
    
    # 分配到桶
    for num in arr:
        if range_val == 0:
            index = 0
        else:
            index = int((num - min_val) / range_val * (num_buckets - 1))
        buckets[index].append(num)
    
    # 桶内排序
    for bucket in buckets:
        bucket.sort()
    
    # 收集结果
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result
```

### 3.2 整数桶排序

```python
def bucket_sort_integers(arr: List[int]) -> List[int]:
    """
    整数桶排序
    
    将整数按范围分配到不同桶
    """
    if not arr:
        return arr
    
    # 找范围
    min_val = min(arr)
    max_val = max(arr)
    
    # 确定桶数量
    num_buckets = max(1, (max_val - min_val) // 10 + 1)
    bucket_range = (max_val - min_val) / num_buckets + 1
    
    # 创建桶
    buckets = [[] for _ in range(num_buckets)]
    
    # 分配
    for num in arr:
        index = int((num - min_val) / bucket_range)
        buckets[index].append(num)
    
    # 排序
    for bucket in buckets:
        bucket.sort()
    
    # 收集
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result
```

---

## 4. 复杂度分析

### 时间复杂度

**O(n+k) 平均 / O(n²) 最坏**

```python
# 平均情况（数据均匀分布）:
# 分配到桶: O(n)
# 每个桶排序: O(1) 平均
# 收集结果: O(n)
# 总计: O(n)

# 最坏情况（所有元素在一个桶）:
# 退化为桶内排序的复杂度: O(n²)
```

### 空间复杂度

**O(n+k)** - 需要桶空间

---

## 5. 应用场景

### ✅ 适用场景

1. **均匀分布的浮点数**
   ```python
   scores = [0.78, 0.56, 0.89, 0.34, 0.91]
   bucket_sort(scores)
   ```

2. **外部排序**
   ```python
   # 大文件分桶处理
   ```

### ❌ 不适用场景

1. **分布不均**
   ```python
   # 性能差
   arr = [0.01, 0.01, 0.01, 0.99]
   ```

---

## 6. 与其他排序算法对比

| 算法 | 时间 | 空间 | 稳定性 | 适用 |
|-----|------|------|--------|------|
| **桶排序** | O(n+k) | O(n+k) | ✅ | 均匀分布 |
| **计数排序** | O(n+k) | O(k) | ✅ | 整数、范围小 |
| **基数排序** | O(d(n+k)) | O(n+k) | ✅ | 整数 |

---

## 7. LeetCode相关题目

| 题号 | 题目 | 难度 | 考点 |
|-----|------|------|------|
| 164 | 最大间距 | Hard | 桶排序 |
| 220 | 存在重复元素III | Medium | 桶 |
| 347 | 前K个高频元素 | Medium | 桶排序 |

---

## 8. 性能测试

```python
def benchmark_bucket_sort():
    """性能测试"""
    import time
    import random
    
    # 均匀分布数据
    arr = [random.random() for _ in range(10000)]
    
    start = time.perf_counter()
    bucket_sort(arr.copy())
    bucket_time = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    sorted(arr)
    python_time = (time.perf_counter() - start) * 1000
    
    print(f"桶排序: {bucket_time:.3f}ms")
    print(f"Python内置: {python_time:.3f}ms")

benchmark_bucket_sort()
```

---

## 9. 常见陷阱与最佳实践

### 陷阱1：桶数量选择不当

```python
# ❌ 桶太少：性能差
buckets = [[] for _ in range(2)]

# ❌ 桶太多：空间浪费
buckets = [[] for _ in range(1000000)]

# ✅ 合适的桶数量
num_buckets = len(arr)  # 或根据数据范围
```

### 最佳实践

✅ **检查数据分布**
```python
def smart_bucket_sort(arr):
    # 检查数据是否均匀分布
    # 如果不均匀，使用其他算法
    return bucket_sort(arr)
```

---

## 10. 总结

桶排序是一种分布式排序算法，在数据均匀分布时性能excellent。

### 核心要点

✅ **时间复杂度**: O(n+k) 平均  
✅ **空间复杂度**: O(n+k)  
✅ **稳定性**: 可以稳定  
✅ **限制**: 依赖数据分布

### 使用建议

- ✅ 数据均匀分布
- ✅ 浮点数排序
- ✅ 外部排序
- ❌ 分布不均
- ❌ 内存受限

桶排序是处理均匀分布数据的excellent选择！🚀
