# Selection Sort - 选择排序

## 目录

- [1. 概述](#1-概述)
- [2. 算法原理](#2-算法原理)
  - [2.1 核心思想](#21-核心思想)
  - [2.2 工作原理](#22-工作原理)
  - [2.3 算法步骤](#23-算法步骤)
- [3. Python实现](#3-python实现)
  - [3.1 基础实现](#31-基础实现)
  - [3.2 优化实现](#32-优化实现)
  - [3.3 双向选择排序](#33-双向选择排序)
- [4. 复杂度分析](#4-复杂度分析)
  - [4.1 时间复杂度](#41-时间复杂度)
  - [4.2 空间复杂度](#42-空间复杂度)
  - [4.3 稳定性分析](#43-稳定性分析)
- [5. 算法可视化](#5-算法可视化)
- [6. 优化技巧](#6-优化技巧)
- [7. 应用场景](#7-应用场景)
- [8. 与其他排序算法对比](#8-与其他排序算法对比)
- [9. 性能测试](#9-性能测试)
- [10. 常见陷阱与最佳实践](#10-常见陷阱与最佳实践)
- [11. 总结](#11-总结)

---

## 1. 概述

**选择排序（Selection Sort）** 是一种简单直观的排序算法。它的工作原理是每次从未排序部分选择最小（或最大）的元素，放到已排序部分的末尾。

### 核心特点

- ⏱️ **时间复杂度**: O(n²) - 所有情况
- 💾 **空间复杂度**: O(1) - 原地排序
- 🔄 **稳定性**: 不稳定
- 📊 **适用场景**: 小数据集、交换代价高

### 算法优势

✅ **实现简单** - 最容易理解和实现的排序算法  
✅ **原地排序** - 不需要额外空间  
✅ **交换次数少** - 最多n-1次交换  
✅ **可预测** - 性能稳定，不受数据分布影响

### 算法劣势

❌ **效率低** - 始终O(n²)，无最好情况  
❌ **不稳定** - 相同元素顺序可能改变  
❌ **不适应** - 对已排序数据无优化  
❌ **实用性差** - 实际应用很少

---

## 2. 算法原理

### 2.1 核心思想

选择排序的核心思想是：
1. 将数组分为已排序和未排序两部分
2. 从未排序部分选择最小元素
3. 与未排序部分的第一个元素交换
4. 重复步骤2-3，直到全部排序

### 2.2 工作原理

```
将数组分为两部分：
- 已排序部分（左侧）
- 未排序部分（右侧）

每次从未排序部分找最小元素，交换到已排序部分末尾

示例：
初始: [5, 2, 4, 6, 1, 3]

第1轮: 找最小元素1，与第0个交换
      [1 | 2, 4, 6, 5, 3]  # 1已排序

第2轮: 找最小元素2，已在正确位置
      [1, 2 | 4, 6, 5, 3]  # 1,2已排序

第3轮: 找最小元素3，与第2个交换
      [1, 2, 3 | 6, 5, 4]  # 1,2,3已排序

第4轮: 找最小元素4，与第3个交换
      [1, 2, 3, 4 | 5, 6]  # 1,2,3,4已排序

第5轮: 找最小元素5，已在正确位置
      [1, 2, 3, 4, 5 | 6]  # 1,2,3,4,5已排序

完成: [1, 2, 3, 4, 5, 6]
```

### 2.3 算法步骤

1. 在未排序序列中找到最小（大）元素
2. 存储到排序序列的起始位置
3. 从剩余未排序元素中继续寻找最小（大）元素
4. 重复步骤2-3，直到所有元素排序完成

---

## 3. Python实现

### 3.1 基础实现

```python
from typing import List

def selection_sort(arr: List[int]) -> List[int]:
    """
    选择排序 - 基础实现
    
    时间复杂度: O(n²) - 所有情况
    空间复杂度: O(1)
    稳定性: 不稳定
    
    Args:
        arr: 待排序数组
    
    Returns:
        排序后的数组
    
    Example:
        >>> selection_sort([5, 2, 4, 6, 1, 3])
        [1, 2, 3, 4, 5, 6]
    """
    n = len(arr)
    
    # 遍历未排序部分
    for i in range(n - 1):
        # 找最小元素的索引
        min_idx = i
        
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # 交换到正确位置
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr
```

**代码详解**:
```python
# 示例: [5, 2, 4, 6, 1, 3]

# i=0: 找最小元素1(索引4)，与arr[0]交换
# [1, 2, 4, 6, 5, 3]

# i=1: 找最小元素2(索引1)，已在正确位置
# [1, 2, 4, 6, 5, 3]

# i=2: 找最小元素3(索引5)，与arr[2]交换
# [1, 2, 3, 6, 5, 4]

# i=3: 找最小元素4(索引5)，与arr[3]交换
# [1, 2, 3, 4, 5, 6]

# i=4: 找最小元素5(索引4)，已在正确位置
# [1, 2, 3, 4, 5, 6]

# 完成！
```

### 3.2 优化实现

```python
def selection_sort_optimized(arr: List[int]) -> List[int]:
    """
    选择排序 - 优化实现
    
    优化点：
    1. 提前终止：如果找到的最小元素就是当前元素，跳过交换
    2. 记录交换次数
    """
    n = len(arr)
    swap_count = 0
    
    for i in range(n - 1):
        min_idx = i
        
        # 找最小元素
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # 只在需要时交换
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swap_count += 1
    
    print(f"总交换次数: {swap_count}")
    return arr
```

### 3.3 双向选择排序

```python
def bidirectional_selection_sort(arr: List[int]) -> List[int]:
    """
    双向选择排序
    
    优化思路：
    每次同时找最小和最大元素
    放到两端，减少遍历次数
    
    时间复杂度: O(n²) - 但实际快约2倍
    空间复杂度: O(1)
    
    Example:
        >>> bidirectional_selection_sort([5, 2, 4, 6, 1, 3])
        [1, 2, 3, 4, 5, 6]
    """
    left = 0
    right = len(arr) - 1
    
    while left < right:
        # 找最小和最大元素的索引
        min_idx = left
        max_idx = right
        
        for i in range(left, right + 1):
            if arr[i] < arr[min_idx]:
                min_idx = i
            if arr[i] > arr[max_idx]:
                max_idx = i
        
        # 交换最小元素到左端
        if min_idx != left:
            arr[left], arr[min_idx] = arr[min_idx], arr[left]
            
            # 如果最大元素在left位置，需要更新max_idx
            if max_idx == left:
                max_idx = min_idx
        
        # 交换最大元素到右端
        if max_idx != right:
            arr[right], arr[max_idx] = arr[max_idx], arr[right]
        
        left += 1
        right -= 1
    
    return arr
```

---

## 4. 复杂度分析

### 4.1 时间复杂度

| 情况 | 时间复杂度 | 说明 |
|-----|-----------|------|
| **最好情况** | O(n²) | 已排序，仍需比较 |
| **平均情况** | O(n²) | 随机数据 |
| **最坏情况** | O(n²) | 逆序数据 |

**详细分析**:
```python
# 比较次数（固定）：
# 第1轮: n-1 次
# 第2轮: n-2 次
# 第3轮: n-3 次
# ...
# 第n-1轮: 1 次
#
# 总次数: (n-1) + (n-2) + ... + 1 = n(n-1)/2 = O(n²)

# 交换次数：
# 最好情况（已排序）: 0 次
# 最坏情况（逆序）: n-1 次
# 平均情况: n/2 次
```

### 4.2 空间复杂度

**O(1)** - 原地排序

```python
def selection_sort(arr):
    n = len(arr)
    
    # 只使用常数个额外变量
    for i in range(n - 1):
        min_idx = i  # O(1)
        
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j  # O(1)
        
        # 原地交换
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr
```

### 4.3 稳定性分析

**不稳定排序** ❌

```python
# 示例：选择排序破坏稳定性
arr = [5a, 3, 5b, 2]  # 下标表示相同值的不同对象

# 第1轮: 找最小元素2，与5a交换
# [2, 3, 5b, 5a]  # 5a和5b的顺序改变了！

# 原因：交换操作可能跨越相同元素
```

**为什么不稳定？**
```
初始: [3, 2, 2a, 1]

第1轮: 找最小元素1，与3交换
      [1, 2, 2a, 3]  # 没问题

第2轮: 找最小元素2，已在位置1
      [1, 2, 2a, 3]  # 没问题

但考虑: [2a, 2b, 1]

第1轮: 找最小元素1，与2a交换
      [1, 2b, 2a]  # 2a和2b顺序改变了！
```

---

## 5. 算法可视化

### 详细排序过程

```
初始数组: [5, 2, 4, 6, 1, 3]

====================================
第1轮 (i=0):
[5, 2, 4, 6, 1, 3]
 ^                 # 当前位置

找最小元素: 1 (索引4)
比较过程:
- 5 vs 2: min=2 (索引1)
- 2 vs 4: min=2 (索引1)
- 2 vs 6: min=2 (索引1)
- 2 vs 1: min=1 (索引4)  ← 找到最小
- 1 vs 3: min=1 (索引4)

交换 arr[0] 和 arr[4]:
[1, 2, 4, 6, 5, 3]
 ^^^^ 已排序

====================================
第2轮 (i=1):
[1, 2, 4, 6, 5, 3]
    ^              # 当前位置

找最小元素: 2 (索引1)
比较过程:
- 2 vs 4: min=2 (索引1)
- 2 vs 6: min=2 (索引1)
- 2 vs 5: min=2 (索引1)
- 2 vs 3: min=2 (索引1)

无需交换（已在正确位置）
[1, 2, 4, 6, 5, 3]
 ^^^^^^ 已排序

====================================
第3轮 (i=2):
[1, 2, 4, 6, 5, 3]
       ^           # 当前位置

找最小元素: 3 (索引5)
比较过程:
- 4 vs 6: min=4 (索引2)
- 4 vs 5: min=4 (索引2)
- 4 vs 3: min=3 (索引5)  ← 找到最小

交换 arr[2] 和 arr[5]:
[1, 2, 3, 6, 5, 4]
 ^^^^^^^^ 已排序

====================================
第4轮 (i=3):
[1, 2, 3, 6, 5, 4]
          ^        # 当前位置

找最小元素: 4 (索引5)
比较过程:
- 6 vs 5: min=5 (索引4)
- 5 vs 4: min=4 (索引5)  ← 找到最小

交换 arr[3] 和 arr[5]:
[1, 2, 3, 4, 5, 6]
 ^^^^^^^^^^^ 已排序

====================================
第5轮 (i=4):
[1, 2, 3, 4, 5, 6]
             ^     # 当前位置

找最小元素: 5 (索引4)
比较过程:
- 5 vs 6: min=5 (索引4)

无需交换（已在正确位置）
[1, 2, 3, 4, 5, 6]
 ^^^^^^^^^^^^^^ 已排序

完成！
```

---

## 6. 优化技巧

```python
def selection_sort_with_all_optimizations(arr: List[int]) -> List[int]:
    """
    选择排序 - 综合优化版本
    
    优化点：
    1. 双向选择：同时找最小和最大
    2. 提前终止：已排序部分收缩
    3. 减少交换：判断是否需要交换
    """
    left = 0
    right = len(arr) - 1
    
    while left < right:
        min_idx = left
        max_idx = right
        
        # 同时找最小和最大
        for i in range(left, right + 1):
            if arr[i] < arr[min_idx]:
                min_idx = i
            elif arr[i] > arr[max_idx]:
                max_idx = i
        
        # 只在需要时交换
        if min_idx != left:
            arr[left], arr[min_idx] = arr[min_idx], arr[left]
            if max_idx == left:
                max_idx = min_idx
        
        if max_idx != right:
            arr[right], arr[max_idx] = arr[max_idx], arr[right]
        
        left += 1
        right -= 1
    
    return arr
```

---

## 7. 应用场景

### ✅ 适用场景

1. **小数据集**
   ```python
   small_arr = [5, 2, 8, 1, 9]
   selection_sort(small_arr)
   ```

2. **交换代价高**
   ```python
   # 当交换操作很昂贵时
   # 选择排序交换次数最少（最多n-1次）
   # 例如：大对象交换
   ```

3. **辅助内存受限**
   ```python
   # 需要原地排序
   # O(1)空间复杂度
   ```

4. **教学用途**
   ```python
   # 最容易理解的排序算法
   # 适合教学演示
   ```

### ❌ 不适用场景

1. **大数据集**
   ```python
   # O(n²)不可接受
   large_arr = [random.randint(1, 10000) for _ in range(10000)]
   # 使用快速排序或归并排序
   ```

2. **需要稳定性**
   ```python
   # 选择排序不稳定
   # 使用插入排序或归并排序
   ```

3. **性能要求高**
   ```python
   # 实际应用很少使用选择排序
   # 使用优化的排序算法
   ```

---

## 8. 与其他排序算法对比

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定性 | 交换次数 |
|-----|------|------|------|------|--------|---------|
| **选择排序** | O(n²) | O(n²) | O(n²) | O(1) | ❌ | 最多n-1次 |
| **插入排序** | O(n) | O(n²) | O(n²) | O(1) | ✅ | O(n²) |
| **冒泡排序** | O(n) | O(n²) | O(n²) | O(1) | ✅ | O(n²) |
| **快速排序** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ | O(n log n) |

### 选择排序的独特优势

✅ **交换次数最少**: 最多只需要n-1次交换

```python
# 对于大对象，交换代价很高
# 选择排序是最优选择

class LargeObject:
    def __init__(self, key, large_data):
        self.key = key
        self.data = large_data  # 大量数据
    
    def __lt__(self, other):
        return self.key < other.key

# 选择排序只交换n-1次
# 其他算法交换次数更多
```

---

## 9. 性能测试

```python
import time
import random

def compare_sort_algorithms():
    """对比选择排序和其他算法"""
    
    sizes = [10, 50, 100, 500]
    
    for size in sizes:
        arr = [random.randint(1, 1000) for _ in range(size)]
        
        # 选择排序
        test_arr = arr.copy()
        start = time.perf_counter()
        selection_sort(test_arr)
        selection_time = (time.perf_counter() - start) * 1000
        
        # 插入排序
        test_arr = arr.copy()
        start = time.perf_counter()
        insertion_sort(test_arr)
        insertion_time = (time.perf_counter() - start) * 1000
        
        print(f"n={size:4d}: 选择排序={selection_time:7.3f}ms, "
              f"插入排序={insertion_time:7.3f}ms")

compare_sort_algorithms()
```

**输出示例：**
```
n=  10: 选择排序=  0.023ms, 插入排序=  0.018ms
n=  50: 选择排序=  0.234ms, 插入排序=  0.189ms
n= 100: 选择排序=  0.987ms, 插入排序=  0.756ms
n= 500: 选择排序= 23.456ms, 插入排序= 18.234ms

结论：插入排序通常比选择排序快约20-30%
```

---

## 10. 常见陷阱与最佳实践

### 陷阱1：忘记更新min_idx

```python
# ❌ 错误
def selection_sort_wrong(arr):
    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[i]:  # 错误：直接与arr[i]比较
                arr[i], arr[j] = arr[j], arr[i]
    return arr

# ✅ 正确
def selection_sort_correct(arr):
    for i in range(len(arr) - 1):
        min_idx = i  # 记录最小元素索引
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

### 陷阱2：不必要的交换

```python
# ❌ 低效：总是交换
def selection_sort_inefficient(arr):
    for i in range(len(arr) - 1):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # 即使min_idx==i也交换

# ✅ 高效：只在需要时交换
def selection_sort_efficient(arr):
    for i in range(len(arr) - 1):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:  # 只在需要时交换
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

### 最佳实践

✅ **了解局限性**
```python
# 选择排序主要用于教学
# 实际生产使用Python的sorted()或list.sort()
```

✅ **考虑交换代价**
```python
# 如果交换代价很高，选择排序是好选择
# 例如：大对象、磁盘I/O
```

✅ **双向优化**
```python
# 对于实际使用，考虑双向选择排序
# 能提升约2倍性能
```

---

## 11. 总结

选择排序是最简单的排序算法之一，虽然效率不高，但有其独特的价值。

### 核心要点

✅ **时间复杂度**: O(n²) - 所有情况  
✅ **空间复杂度**: O(1) - 原地排序  
✅ **稳定性**: 不稳定  
✅ **交换次数**: 最多n-1次（最少）

### 优势

- 实现简单，容易理解
- 原地排序，无额外空间
- 交换次数最少
- 性能可预测

### 劣势

- 时间复杂度始终O(n²)
- 不稳定排序
- 不适应数据特点
- 实际应用少

### 使用建议

- 📚 **教学用途**: 理解排序概念
- 🔧 **交换代价高**: 大对象排序
- 📦 **小数据集**: 简单场景
- ❌ **生产环境**: 使用更好的算法

选择排序虽然简单，但却是理解排序算法的excellent起点！🚀
