# Heap Sort - 堆排序

## 目录

- [1. 概述](#1-概述)
- [2. 算法原理](#2-算法原理)
  - [2.1 核心思想](#21-核心思想)
  - [2.2 堆的性质](#22-堆的性质)
  - [2.3 算法步骤](#23-算法步骤)
- [3. Python实现](#3-python实现)
  - [3.1 基础实现](#31-基础实现)
  - [3.2 优化实现](#32-优化实现)
  - [3.3 使用heapq实现](#33-使用heapq实现)
- [4. 复杂度分析](#4-复杂度分析)
  - [4.1 时间复杂度](#41-时间复杂度)
  - [4.2 空间复杂度](#42-空间复杂度)
  - [4.3 稳定性分析](#43-稳定性分析)
- [5. 算法可视化](#5-算法可视化)
- [6. 优化技巧](#6-优化技巧)
  - [6.1 减少交换次数](#61-减少交换次数)
  - [6.2 迭代vs递归](#62-迭代vs递归)
  - [6.3 小数据优化](#63-小数据优化)
- [7. 应用场景](#7-应用场景)
- [8. 与其他排序算法对比](#8-与其他排序算法对比)
- [9. LeetCode相关题目](#9-leetcode相关题目)
- [10. 性能测试](#10-性能测试)
  - [10.1 不同数据规模测试](#101-不同数据规模测试)
  - [10.2 不同数据分布测试](#102-不同数据分布测试)
  - [10.3 与其他算法对比](#103-与其他算法对比)
- [11. 常见陷阱与最佳实践](#11-常见陷阱与最佳实践)
  - [11.1 陷阱1：索引计算错误](#111-陷阱1索引计算错误)
  - [11.2 陷阱2：边界条件处理](#112-陷阱2边界条件处理)
  - [11.3 陷阱3：稳定性误解](#113-陷阱3稳定性误解)
  - [11.4 最佳实践](#114-最佳实践)
- [12. 扩展应用](#12-扩展应用)
  - [12.1 Top K问题](#121-top-k问题)
  - [12.2 优先级队列](#122-优先级队列)
  - [12.3 外部排序](#123-外部排序)
- [13. 总结](#13-总结)

---

## 1. 概述

**堆排序（Heap Sort）** 是一种基于堆数据结构的比较排序算法。它利用堆的性质，在O(n log n)时间内完成排序。

### 核心特点

- ⏱️ **时间复杂度**: O(n log n) - 所有情况
- 💾 **空间复杂度**: O(1) - 原地排序
- 🔄 **稳定性**: 不稳定
- 📊 **适用场景**: 不需要稳定性的大数据排序

### 算法优势

✅ **最坏情况也是O(n log n)** - 性能稳定  
✅ **原地排序** - 不需要额外空间  
✅ **简单可靠** - 实现相对简单  
✅ **适合大数据** - 内存效率高

### 算法劣势

❌ **不稳定** - 相同元素顺序可能改变  
❌ **缓存不友好** - 跳跃式访问  
❌ **实际性能** - 常数因子较大

---

## 2. 算法原理

### 2.1 核心思想

堆排序的核心思想是：
1. **建堆**: 将无序数组构建成最大堆（或最小堆）
2. **排序**: 反复将堆顶元素（最大值）移到末尾，然后调整剩余元素为堆

### 2.2 堆的性质

**最大堆（Max Heap）**:
```
父节点的值 ≥ 子节点的值

示例：
       9
      / \
     7   6
    / \
   5   3
```

**最小堆（Min Heap）**:
```
父节点的值 ≤ 子节点的值

示例：
       1
      / \
     3   6
    / \
   7   9
```

**堆在数组中的表示**:
```python
# 对于索引 i 的节点：
父节点: (i - 1) // 2
左子节点: 2 * i + 1
右子节点: 2 * i + 2

示例数组: [9, 7, 6, 5, 3]
对应堆:
       9 (i=0)
      / \
   7(i=1) 6(i=2)
   / \
5(i=3) 3(i=4)
```

### 2.3 算法步骤

**步骤1: 建堆（Heapify）**
```
初始数组: [4, 10, 3, 5, 1]

从最后一个非叶子节点开始向上调整
最后非叶子节点索引: (n-1-1)//2 = 1

调整后的最大堆: [10, 5, 3, 4, 1]
```

**步骤2: 排序**
```
循环执行：
1. 交换堆顶和末尾元素
2. 堆大小减1
3. 对新堆顶进行下沉调整

第1次: [10, 5, 3, 4, 1] -> [1, 5, 3, 4 | 10] -> [5, 4, 3, 1 | 10]
第2次: [5, 4, 3, 1 | 10] -> [1, 4, 3 | 5, 10] -> [4, 1, 3 | 5, 10]
第3次: [4, 1, 3 | 5, 10] -> [3, 1 | 4, 5, 10] -> [3, 1 | 4, 5, 10]
第4次: [3, 1 | 4, 5, 10] -> [1 | 3, 4, 5, 10] -> [1 | 3, 4, 5, 10]

最终结果: [1, 3, 4, 5, 10]
```

---

## 3. Python实现

### 3.1 基础实现

```python
from typing import List

def heap_sort(arr: List[int]) -> List[int]:
    """
    堆排序 - 基础实现
    
    时间复杂度: O(n log n)
    空间复杂度: O(1)
    
    Args:
        arr: 待排序数组
    
    Returns:
        排序后的数组
    
    Example:
        >>> heap_sort([4, 10, 3, 5, 1])
        [1, 3, 4, 5, 10]
    """
    n = len(arr)
    
    # 1. 建堆 - 从最后一个非叶子节点开始向上调整
    # 最后一个非叶子节点索引: (n-1-1)//2 = n//2 - 1
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # 2. 排序 - 依次将堆顶元素移到末尾
    for i in range(n - 1, 0, -1):
        # 交换堆顶和末尾元素
        arr[0], arr[i] = arr[i], arr[0]
        
        # 对新堆顶进行下沉调整
        heapify(arr, i, 0)
    
    return arr


def heapify(arr: List[int], n: int, i: int) -> None:
    """
    堆调整（下沉操作）
    
    将以 i 为根的子树调整为最大堆
    
    Args:
        arr: 数组
        n: 堆的大小
        i: 当前节点索引
    """
    largest = i  # 初始化最大值为根节点
    left = 2 * i + 1  # 左子节点
    right = 2 * i + 2  # 右子节点
    
    # 如果左子节点存在且大于根节点
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # 如果右子节点存在且大于当前最大值
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # 如果最大值不是根节点，交换并继续调整
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # 递归调整被交换的子树
        heapify(arr, n, largest)
```

### 3.2 优化实现

```python
def heap_sort_optimized(arr: List[int]) -> List[int]:
    """
    堆排序 - 优化实现（迭代版本）
    
    优化点：
    1. 使用迭代代替递归
    2. 减少不必要的交换
    
    时间复杂度: O(n log n)
    空间复杂度: O(1)
    """
    n = len(arr)
    
    # 1. 建堆
    for i in range(n // 2 - 1, -1, -1):
        heapify_iterative(arr, n, i)
    
    # 2. 排序
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_iterative(arr, i, 0)
    
    return arr


def heapify_iterative(arr: List[int], n: int, i: int) -> None:
    """
    堆调整 - 迭代实现
    
    优势：
    - 避免递归调用开销
    - 更好的缓存性能
    """
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest == i:
            break
        
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest
```

### 3.3 使用heapq实现

```python
import heapq

def heap_sort_heapq(arr: List[int]) -> List[int]:
    """
    堆排序 - 使用Python的heapq模块
    
    注意：heapq是最小堆，结果自然是升序
    
    时间复杂度: O(n log n)
    空间复杂度: O(1) - heapify是原地操作
    
    Example:
        >>> heap_sort_heapq([4, 10, 3, 5, 1])
        [1, 3, 4, 5, 10]
    """
    # 将数组转换为最小堆
    heapq.heapify(arr)
    
    # 依次弹出最小元素
    return [heapq.heappop(arr) for _ in range(len(arr))]


def heap_sort_heapq_inplace(arr: List[int]) -> List[int]:
    """
    堆排序 - heapq原地排序版本
    
    不创建新列表，直接在原数组上排序
    """
    n = len(arr)
    heapq.heapify(arr)
    
    for i in range(n):
        arr[i] = heapq.heappop(arr)
    
    return arr
```

---

## 4. 复杂度分析

### 4.1 时间复杂度

| 情况 | 时间复杂度 | 说明 |
|-----|-----------|------|
| **最好情况** | O(n log n) | 已排序或逆序 |
| **平均情况** | O(n log n) | 随机数据 |
| **最坏情况** | O(n log n) | 任何数据 |

**详细分析**:

1. **建堆阶段**: O(n)
   ```
   从最后一个非叶子节点开始向上调整
   虽然看起来是 n/2 * log n，但实际是 O(n)
   
   证明：
   - 叶子节点：n/2 个，不需要调整
   - 倒数第2层：n/4 个，最多下沉1层
   - 倒数第3层：n/8 个，最多下沉2层
   - ...
   
   总时间：n/4*1 + n/8*2 + n/16*3 + ... < n
   ```

2. **排序阶段**: O(n log n)
   ```
   n 次循环，每次调整 O(log n)
   总时间：n * log n
   ```

3. **总时间**: O(n) + O(n log n) = O(n log n)

### 4.2 空间复杂度

**O(1)** - 原地排序

```python
# 只使用常数个额外变量
def heap_sort(arr):
    n = len(arr)  # O(1)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # 只交换，不创建新数组
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr  # 返回原数组
```

### 4.3 稳定性分析

**不稳定排序** ❌

```python
# 示例：堆排序破坏稳定性
arr = [3a, 3b, 1]  # 下标表示相同值的不同对象

# 建堆后：[3a, 3b, 1] 或 [3b, 3a, 1]
# 排序后可能：[1, 3b, 3a]  # 3a和3b的相对顺序改变了

# 原因：在堆调整过程中，相同值的元素可能被交换
```

**为什么不稳定？**
```
初始：[3₁, 1, 3₂]  # 3₁在3₂前面

建堆：
       3₁
      /  \
     1    3₂

交换后：
       3₂
      /  \
     1    3₁

结果：[1, 3₂, 3₁]  # 顺序改变了
```

---

## 5. 算法可视化

### 建堆过程可视化

```
初始数组: [4, 10, 3, 5, 1]

步骤1: 从最后一个非叶子节点(索引1)开始
       4
      / \
     10  3
    / \
   5   1

调整节点1(值10):
10和子节点5、1比较，10最大，不需要调整

步骤2: 调整节点0(值4)
       4
      / \
     10  3
    / \
   5   1

4和子节点10、3比较，10最大，交换4和10:
       10
      / \
      4  3
    / \
   5   1

继续调整位置1(值4):
4和子节点5、1比较，5最大，交换4和5:
       10
      / \
      5  3
    / \
   4   1

建堆完成！
```

### 排序过程可视化

```
堆: [10, 5, 3, 4, 1]

第1轮:
交换堆顶和末尾: [1, 5, 3, 4 | 10]
调整: [5, 4, 3, 1 | 10]

第2轮:
交换: [1, 4, 3 | 5, 10]
调整: [4, 1, 3 | 5, 10]

第3轮:
交换: [3, 1 | 4, 5, 10]
调整: [3, 1 | 4, 5, 10]

第4轮:
交换: [1 | 3, 4, 5, 10]

最终: [1, 3, 4, 5, 10]
```

---

## 6. 优化技巧

### 6.1 减少交换次数

```python
def heapify_optimized(arr: List[int], n: int, i: int) -> None:
    """
    优化的堆调整 - 减少交换次数
    
    思路：
    1. 保存当前节点的值
    2. 找到最终位置
    3. 一次性赋值，而不是多次交换
    """
    value = arr[i]  # 保存当前值
    
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest == i:
            break
        
        # 直接赋值，不交换
        arr[i] = arr[largest]
        i = largest
    
    # 最后一次赋值
    arr[i] = value
```

### 6.2 迭代vs递归

```python
# 递归版本 - 简洁但有栈开销
def heapify_recursive(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_recursive(arr, n, largest)  # 递归


# 迭代版本 - 更快，无栈开销
def heapify_iterative(arr, n, i):
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest == i:
            break
        
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest
```

### 6.3 小数据优化

```python
def heap_sort_hybrid(arr: List[int]) -> List[int]:
    """
    混合堆排序 - 小数据用插入排序
    
    优化原因：
    - 小数据插入排序更快
    - 减少堆排序的常数因子
    """
    THRESHOLD = 10
    
    if len(arr) < THRESHOLD:
        # 使用插入排序
        return insertion_sort(arr)
    
    # 使用堆排序
    return heap_sort(arr)


def insertion_sort(arr: List[int]) -> List[int]:
    """插入排序 - 用于小数据"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr
```

---

## 7. 应用场景

### ✅ 适用场景

1. **大数据排序**
   ```python
   # 内存受限，需要原地排序
   large_data = [random.randint(1, 1000000) for _ in range(1000000)]
   heap_sort(large_data)  # O(1)空间
   ```

2. **不需要稳定性**
   ```python
   # 只关心大小关系，不关心相同元素顺序
   scores = [85, 90, 85, 78, 92]
   heap_sort(scores)
   ```

3. **最坏情况保证**
   ```python
   # 需要保证O(n log n)性能
   # 快速排序最坏O(n²)，堆排序总是O(n log n)
   critical_data = load_critical_data()
   heap_sort(critical_data)
   ```

4. **嵌入式系统**
   ```python
   # 内存有限，不能使用额外空间
   # 堆排序O(1)空间复杂度
   embedded_data = read_sensor_data()
   heap_sort(embedded_data)
   ```

### ❌ 不适用场景

1. **需要稳定性**
   ```python
   # 需要保持相同元素的相对顺序
   # 使用归并排序或稳定的快速排序
   students = [(Tom, 85), (Jerry, 85), (Alice, 90)]
   # heap_sort会破坏Tom和Jerry的顺序
   ```

2. **小数据量**
   ```python
   # 小数据插入排序更快
   small_arr = [5, 2, 8, 1, 9]
   # 插入排序 O(n²) 但常数小，实际更快
   ```

3. **基本有序**
   ```python
   # 对于基本有序的数据
   # 插入排序或冒泡排序更优
   nearly_sorted = [1, 2, 3, 5, 4, 6, 7]
   # 插入排序可以达到O(n)
   ```

4. **需要频繁访问**
   ```python
   # 堆排序缓存不友好
   # 对于需要频繁访问的数据
   # 快速排序或归并排序更优
   ```

---

## 8. 与其他排序算法对比

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定性 | 适用场景 |
|-----|------|------|------|------|--------|---------|
| **堆排序** | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ | 大数据，保证性能 |
| **快速排序** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ | 一般情况最优 |
| **归并排序** | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ | 需要稳定性 |
| **插入排序** | O(n) | O(n²) | O(n²) | O(1) | ✅ | 小数据/基本有序 |
| **冒泡排序** | O(n) | O(n²) | O(n²) | O(1) | ✅ | 教学用途 |
| **选择排序** | O(n²) | O(n²) | O(n²) | O(1) | ❌ | 小数据 |
| **计数排序** | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅ | 整数，范围小 |

### 详细对比

**堆排序 vs 快速排序**
```python
# 快速排序：
# ✅ 平均更快（缓存友好）
# ✅ 简单实现
# ❌ 最坏O(n²)
# ❌ 递归深度可能很大

# 堆排序：
# ✅ 保证O(n log n)
# ✅ 原地排序
# ❌ 常数因子较大
# ❌ 缓存不友好
```

**堆排序 vs 归并排序**
```python
# 归并排序：
# ✅ 稳定排序
# ✅ 缓存友好
# ❌ 需要O(n)额外空间

# 堆排序：
# ✅ O(1)空间
# ✅ 保证O(n log n)
# ❌ 不稳定
# ❌ 实际性能较慢
```

---

## 9. LeetCode相关题目

### 9.1 直接应用堆排序

| 题号 | 题目 | 难度 | 考点 |
|-----|------|------|------|
| 912 | 排序数组 | Medium | 堆排序实现 |
| 215 | 数组中的第K个最大元素 | Medium | 堆排序变种 |

### 9.2 堆的应用

| 题号 | 题目 | 难度 | 考点 |
|-----|------|------|------|
| 23 | 合并K个升序链表 | Hard | 最小堆 |
| 295 | 数据流的中位数 | Hard | 双堆 |
| 347 | 前K个高频元素 | Medium | 最小堆 |
| 373 | 查找和最小的K对数字 | Medium | 最小堆 |
| 378 | 有序矩阵中第K小的元素 | Medium | 最小堆 |
| 502 | IPO | Hard | 最大堆+贪心 |
| 703 | 数据流中的第K大元素 | Easy | 最小堆 |
| 973 | 最接近原点的K个点 | Medium | 最大堆 |
| 1046 | 最后一块石头的重量 | Easy | 最大堆 |

### 9.3 示例：第K个最大元素

```python
def find_kth_largest(nums: List[int], k: int) -> int:
    """
    LeetCode 215: 数组中的第K个最大元素
    
    方法1：完整堆排序
    时间复杂度: O(n log n)
    空间复杂度: O(1)
    """
    heap_sort(nums)
    return nums[-k]


def find_kth_largest_optimized(nums: List[int], k: int) -> int:
    """
    方法2：部分堆排序
    
    只需要找到第K大，不需要完全排序
    时间复杂度: O(n + k log n)
    空间复杂度: O(1)
    """
    n = len(nums)
    
    # 建堆
    for i in range(n // 2 - 1, -1, -1):
        heapify(nums, n, i)
    
    # 只弹出K次
    for i in range(k - 1):
        nums[0], nums[n - 1 - i] = nums[n - 1 - i], nums[0]
        heapify(nums, n - 1 - i, 0)
    
    return nums[0]


def find_kth_largest_heap(nums: List[int], k: int) -> int:
    """
    方法3：维护大小为K的最小堆
    
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    """
    import heapq
    
    # 维护最小堆，保留最大的K个元素
    heap = nums[:k]
    heapq.heapify(heap)
    
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    
    return heap[0]
```

---

## 10. 性能测试

### 10.1 不同数据规模测试

```python
import time
import random

def benchmark_heap_sort(sizes: List[int]):
    """测试不同数据规模的性能"""
    
    print("数据规模性能测试:")
    print(f"{'规模':<10} {'时间(ms)':<15} {'比较次数':<15}")
    print("-" * 40)
    
    for size in sizes:
        arr = [random.randint(1, 10000) for _ in range(size)]
        
        start = time.perf_counter()
        heap_sort(arr.copy())
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"{size:<10} {elapsed:<15.3f}")

# 运行测试
benchmark_heap_sort([100, 1000, 5000, 10000])
```

**输出示例：**
```
数据规模性能测试:
规模       时间(ms)        
----------------------------------------
100        0.234          
1000       3.456          
5000       21.789         
10000      48.123         
```

### 10.2 不同数据分布测试

```python
def test_different_distributions():
    """测试不同数据分布的性能"""
    
    size = 10000
    
    # 1. 随机数据
    random_data = [random.randint(1, 10000) for _ in range(size)]
    start = time.perf_counter()
    heap_sort(random_data.copy())
    random_time = (time.perf_counter() - start) * 1000
    
    # 2. 已排序数据
    sorted_data = list(range(size))
    start = time.perf_counter()
    heap_sort(sorted_data.copy())
    sorted_time = (time.perf_counter() - start) * 1000
    
    # 3. 逆序数据
    reversed_data = list(range(size, 0, -1))
    start = time.perf_counter()
    heap_sort(reversed_data.copy())
    reversed_time = (time.perf_counter() - start) * 1000
    
    # 4. 重复数据
    repeated_data = [random.randint(1, 10) for _ in range(size)]
    start = time.perf_counter()
    heap_sort(repeated_data.copy())
    repeated_time = (time.perf_counter() - start) * 1000
    
    print("数据分布性能测试 (n=10000):")
    print(f"随机数据:   {random_time:.3f}ms")
    print(f"已排序:     {sorted_time:.3f}ms")
    print(f"逆序:       {reversed_time:.3f}ms")
    print(f"大量重复:   {repeated_time:.3f}ms")

test_different_distributions()
```

**输出示例：**
```
数据分布性能测试 (n=10000):
随机数据:   48.123ms
已排序:     47.856ms
逆序:       48.234ms
大量重复:   45.678ms

结论：堆排序对不同数据分布性能稳定！
```

### 10.3 与其他算法对比

```python
def compare_sorting_algorithms():
    """对比不同排序算法的性能"""
    
    size = 10000
    data = [random.randint(1, 10000) for _ in range(size)]
    
    algorithms = [
        ("堆排序", heap_sort),
        ("快速排序", quick_sort),
        ("归并排序", merge_sort),
        ("Python内置", sorted)
    ]
    
    print(f"排序算法性能对比 (n={size}):")
    print(f"{'算法':<15} {'时间(ms)':<15}")
    print("-" * 30)
    
    for name, func in algorithms:
        test_data = data.copy()
        
        start = time.perf_counter()
        if name == "Python内置":
            result = func(test_data)
        else:
            result = func(test_data)
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"{name:<15} {elapsed:<15.3f}")

compare_sorting_algorithms()
```

**输出示例：**
```
排序算法性能对比 (n=10000):
算法            时间(ms)       
------------------------------
堆排序          48.123         
快速排序        28.456         
归并排序        35.789         
Python内置      12.345         

结论：
- Python内置最快（Timsort，优化的归并+插入）
- 快速排序次之（缓存友好）
- 归并排序第三（稳定但需要额外空间）
- 堆排序较慢（常数因子大，缓存不友好）
```

---

## 11. 常见陷阱与最佳实践

### 11.1 陷阱1：索引计算错误

```python
# ❌ 错误：索引计算错误
def heapify_wrong(arr, n, i):
    largest = i
    left = 2 * i  # 错误！应该是 2*i+1
    right = 2 * i + 1  # 错误！应该是 2*i+2
    
    # ... 会导致访问错误的子节点

# ✅ 正确：正确的索引计算
def heapify_correct(arr, n, i):
    largest = i
    left = 2 * i + 1  # 正确的左子节点
    right = 2 * i + 2  # 正确的右子节点
    
    # 记忆方法：
    # 父节点 i
    # 左子节点 2*i+1
    # 右子节点 2*i+2
    # 父节点 (i-1)//2
```

### 11.2 陷阱2：边界条件处理

```python
# ❌ 错误：未检查子节点是否存在
def heapify_wrong(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # 错误：未检查 left < n
    if arr[left] > arr[largest]:  # 可能越界！
        largest = left
    
    if arr[right] > arr[largest]:  # 可能越界！
        largest = right

# ✅ 正确：先检查边界
def heapify_correct(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # 正确：先检查索引是否有效
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
```

### 11.3 陷阱3：稳定性误解

```python
# ❌ 错误：认为堆排序是稳定的
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

students = [
    Student("Tom", 85),
    Student("Jerry", 85),
    Student("Alice", 90)
]

# 堆排序后，Tom和Jerry的相对顺序可能改变
heap_sort(students, key=lambda s: s.score)
# 结果可能：Jerry, Tom, Alice

# ✅ 正确：需要稳定性时使用稳定排序
# 使用归并排序或Python的sorted()
sorted_students = sorted(students, key=lambda s: s.score)
```

### 11.4 最佳实践

✅ **实践1：使用Python的heapq模块**
```python
import heapq

# 推荐：使用标准库
def sort_with_heapq(arr):
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]

# 而不是自己实现（除非学习目的）
```

✅ **实践2：迭代优于递归**
```python
# 推荐：迭代版本
def heapify_iterative(arr, n, i):
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest == i:
            break
        
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest
```

✅ **实践3：选择合适的排序算法**
```python
def smart_sort(arr):
    """根据情况选择排序算法"""
    n = len(arr)
    
    # 小数据：插入排序
    if n < 10:
        return insertion_sort(arr)
    
    # 需要稳定性：归并排序
    if need_stability:
        return merge_sort(arr)
    
    # 一般情况：快速排序
    # 内存受限：堆排序
    return heap_sort(arr)
```

✅ **实践4：避免不必要的复制**
```python
# ❌ 低效：创建新列表
def heap_sort_bad(arr):
    result = arr.copy()
    # ... 排序 result
    return result

# ✅ 高效：原地排序
def heap_sort_good(arr):
    # 直接修改原数组
    heap_sort(arr)
    return arr
```

✅ **实践5：性能测试**
```python
def choose_sort_algorithm(arr_size):
    """根据测试选择算法"""
    
    # 对不同数据规模测试
    if arr_size < 100:
        return insertion_sort
    elif arr_size < 10000:
        return quick_sort
    else:
        return heap_sort  # 大数据保证性能
```

---

## 12. 扩展应用

### 12.1 Top K问题

```python
def find_top_k_elements(arr: List[int], k: int) -> List[int]:
    """
    找出最大的K个元素
    
    方法1：完整堆排序 - O(n log n)
    方法2：部分堆排序 - O(n + k log n)
    方法3：维护K大小堆 - O(n log k)
    """
    # 方法3最优：维护大小为K的最小堆
    import heapq
    
    if k >= len(arr):
        return sorted(arr, reverse=True)
    
    # 维护最小堆
    heap = arr[:k]
    heapq.heapify(heap)
    
    for num in arr[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    
    return sorted(heap, reverse=True)


# 应用示例：实时排名系统
class Leaderboard:
    """游戏排行榜"""
    
    def __init__(self, k: int = 10):
        self.k = k
        self.top_k = []  # 最小堆
    
    def add_score(self, player: str, score: int):
        """添加分数"""
        import heapq
        
        if len(self.top_k) < self.k:
            heapq.heappush(self.top_k, (score, player))
        elif score > self.top_k[0][0]:
            heapq.heapreplace(self.top_k, (score, player))
    
    def get_top_k(self) -> List[tuple]:
        """获取Top K"""
        return sorted(self.top_k, reverse=True)
```

### 12.2 优先级队列

```python
class PriorityQueue:
    """基于堆的优先级队列"""
    
    def __init__(self):
        self.heap = []
    
    def push(self, item, priority):
        """添加元素（优先级越小越优先）"""
        import heapq
        heapq.heappush(self.heap, (priority, item))
    
    def pop(self):
        """弹出最高优先级元素"""
        import heapq
        if self.heap:
            return heapq.heappop(self.heap)[1]
        raise IndexError("Priority queue is empty")
    
    def peek(self):
        """查看最高优先级元素"""
        if self.heap:
            return self.heap[0][1]
        raise IndexError("Priority queue is empty")


# 应用示例：任务调度
class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.pq = PriorityQueue()
    
    def add_task(self, task, priority):
        """添加任务"""
        self.pq.push(task, priority)
    
    def execute_next(self):
        """执行下一个任务"""
        try:
            task = self.pq.pop()
            print(f"执行任务: {task}")
            return task
        except IndexError:
            print("没有待执行任务")
            return None
```

### 12.3 外部排序

```python
def external_sort(input_file: str, output_file: str, memory_limit: int):
    """
    外部排序 - 用于超大文件排序
    
    思路：
    1. 将文件分块，每块用堆排序
    2. 使用K路归并排序合并所有块
    3. 使用堆维护K个块的当前最小值
    
    Args:
        input_file: 输入文件
        output_file: 输出文件
        memory_limit: 内存限制（元素个数）
    """
    import heapq
    import os
    
    # 阶段1：分块排序
    chunk_files = []
    chunk_id = 0
    
    with open(input_file, 'r') as f:
        while True:
            # 读取一块数据
            chunk = []
            for _ in range(memory_limit):
                line = f.readline()
                if not line:
                    break
                chunk.append(int(line.strip()))
            
            if not chunk:
                break
            
            # 堆排序这一块
            heap_sort(chunk)
            
            # 写入临时文件
            chunk_file = f"chunk_{chunk_id}.tmp"
            chunk_files.append(chunk_file)
            
            with open(chunk_file, 'w') as cf:
                for num in chunk:
                    cf.write(f"{num}\n")
            
            chunk_id += 1
    
    # 阶段2：K路归并
    # 打开所有chunk文件
    files = [open(cf, 'r') for cf in chunk_files]
    
    # 初始化堆：(值, 文件索引)
    heap = []
    for i, f in enumerate(files):
        line = f.readline()
        if line:
            heapq.heappush(heap, (int(line.strip()), i))
    
    # K路归并
    with open(output_file, 'w') as out:
        while heap:
            value, file_idx = heapq.heappop(heap)
            out.write(f"{value}\n")
            
            # 从同一文件读取下一个
            line = files[file_idx].readline()
            if line:
                heapq.heappush(heap, (int(line.strip()), file_idx))
    
    # 清理
    for f in files:
        f.close()
    
    for cf in chunk_files:
        os.remove(cf)


# 使用示例
# external_sort("huge_file.txt", "sorted_file.txt", memory_limit=1000000)
```

---

## 13. 总结

堆排序是一种基于堆数据结构的高效排序算法，具有稳定的O(n log n)时间复杂度和O(1)空间复杂度。

### 核心要点

✅ **时间复杂度**
- 所有情况都是 O(n log n)
- 建堆 O(n)
- 排序 O(n log n)

✅ **空间复杂度**
- O(1) - 原地排序
- 只需常数个额外变量

✅ **稳定性**
- 不稳定排序
- 相同元素顺序可能改变

✅ **优势**
- 最坏情况也是 O(n log n)
- 原地排序，内存效率高
- 实现相对简单
- 适合大数据排序

✅ **劣势**
- 不稳定
- 缓存不友好
- 实际性能不如快速排序
- 常数因子较大

### 使用建议

1. **大数据排序**: 内存受限时优先考虑
2. **性能保证**: 需要最坏情况O(n log n)时使用
3. **不需稳定性**: 只关心大小关系时使用
4. **嵌入式系统**: 内存有限时使用

### 学习路径

1. **理解堆的性质** - 完全二叉树、堆性质
2. **掌握基本实现** - 建堆、调整堆
3. **理解复杂度** - 时间、空间、稳定性
4. **应用扩展** - Top K、优先队列、外部排序
5. **性能优化** - 迭代、减少交换、混合算法

### 实践建议

- 📚 **学习用途**: 实现完整的堆排序
- 💼 **生产用途**: 使用heapq模块或sorted()
- 🎯 **面试准备**: 掌握原理和复杂度
- 🚀 **性能优化**: 根据场景选择合适算法

掌握堆排序是理解高级数据结构和算法的重要一步！🚀
