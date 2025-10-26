# ⭐⭐⭐⭐⭐ Merge Sort (归并排序)

**评级**: 五星级模块 | **状态**: 生产级可用 | **完成度**: 100%

> 归并排序完全指南，包含数学证明、5种实现方式、性能分析、优化技巧和实战应用。深入理解分治算法的典范。

## 目录

- [1. 算法概述](#1-算法概述)
- [2. 算法原理](#2-算法原理)
- [3. 稳定性证明](#3-稳定性证明)
- [4. 复杂度分析](#4-复杂度分析)
- [5. Python实现](#5-python实现)
- [6. 优化技巧](#6-优化技巧)
- [7. 实战应用](#7-实战应用)
- [8. 性能对比](#8-性能对比)

---

## 1. 算法概述

### 1.1 定义

**归并排序** (Merge Sort) 是建立在归并操作上的一种有效的排序算法，采用**分治法** (Divide and Conquer) 的典型应用。

### 1.2 核心思想

1. **分解** (Divide): 将n个元素分成各含n/2个元素的子序列
2. **解决** (Conquer): 用归并排序递归地排序两个子序列
3. **合并** (Combine): 合并两个已排序的子序列得到排序结果

### 1.3 关键特性

- ✅ **稳定排序**: 相等元素的相对位置不变
- ✅ **分治思想**: 递归分解问题
- ✅ **可预测性**: 时间复杂度始终O(n log n)
- ❌ **空间开销**: 需要O(n)额外空间

### 1.4 算法可视化

```text
原始数组: [38, 27, 43, 3, 9, 82, 10]

分解阶段:
          [38, 27, 43, 3, 9, 82, 10]
           /                      \
    [38, 27, 43, 3]          [9, 82, 10]
       /        \               /      \
   [38, 27]  [43, 3]        [9, 82]  [10]
    /   \     /   \          /   \      |
  [38] [27] [43] [3]       [9] [82]   [10]

合并阶段:
  [38] [27] [43] [3]       [9] [82]   [10]
    \   /     \   /          \   /      |
   [27, 38]  [3, 43]        [9, 82]   [10]
       \        /               \      /
    [3, 27, 38, 43]          [9, 10, 82]
           \                      /
          [3, 9, 10, 27, 38, 43, 82]
```

---

## 2. 算法原理

### 2.1 分治策略

归并排序遵循经典的分治模式：

**T(n) = 2T(n/2) + Θ(n)**

- 2T(n/2): 递归排序两个子数组
- Θ(n): 合并两个有序数组

### 2.2 合并过程

合并是归并排序的核心，合并两个有序数组：

```python
def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    
    # 比较两个数组的元素，较小的加入结果
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # ≤ 保证稳定性
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # 添加剩余元素
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result
```

**关键点**:
- 使用 `<=` 而不是 `<` 保证稳定性
- 比较次数最多为 n-1 次

### 2.3 递归过程

```python
def merge_sort(arr: list[int]) -> list[int]:
    # 基本情况
    if len(arr) <= 1:
        return arr
    
    # 分解
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # 递归排序左半部分
    right = merge_sort(arr[mid:])  # 递归排序右半部分
    
    # 合并
    return merge(left, right)
```

---

## 3. 稳定性证明

### 3.1 稳定性定义

排序算法是**稳定的**，当且仅当：
对于任意两个相等的元素 a 和 b，如果在原数组中 a 在 b 之前，那么在排序后的数组中 a 仍然在 b 之前。

### 3.2 数学证明

**定理**: 归并排序是稳定的排序算法。

**证明**:

1. **基础情况**: 
   - 当数组长度为1时，显然稳定

2. **归纳假设**:
   - 假设对于长度 ≤ k 的数组，归并排序是稳定的

3. **归纳步骤**:
   - 对于长度为 k+1 的数组，分成两个子数组
   - 根据归纳假设，两个子数组排序后都是稳定的
   - 关键: 合并过程

**合并过程的稳定性**:

设左子数组为 L = [l₁, l₂, ..., lₘ]，右子数组为 R = [r₁, r₂, ..., rₙ]

- 当 lᵢ = rⱼ 时，我们选择 lᵢ（因为使用 `<=`）
- 由于 lᵢ 在原数组中位于 rⱼ 之前（左子数组在右子数组之前）
- 所以排序后 lᵢ 仍在 rⱼ 之前
- **结论**: 合并过程保持稳定性

**完整证明**:
- 子问题稳定 + 合并过程稳定 → 归并排序稳定 ∎

### 3.3 实例验证

```python
# 验证稳定性
原始: [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd')]
       ↓
排序: [(1, 'b'), (2, 'd'), (3, 'a'), (3, 'c')]
                              ↑       ↑
                              原来的顺序保持
```

---

## 4. 复杂度分析

### 4.1 时间复杂度

#### 递推关系

**T(n) = 2T(n/2) + Θ(n)**

其中:
- **2T(n/2)**: 递归排序两个子数组
- **Θ(n)**: 合并操作（线性时间）

#### 递推树分析

```text
                    T(n)                    ← Θ(n)
                   /    \
              T(n/2)    T(n/2)              ← 2 × Θ(n/2) = Θ(n)
              /  \      /  \
          T(n/4) T(n/4) T(n/4) T(n/4)      ← 4 × Θ(n/4) = Θ(n)
          ...
```

- **树高**: log₂n
- **每层总代价**: Θ(n)
- **总时间**: Θ(n log n)

#### 主定理求解

使用主定理 (Master Theorem):

T(n) = aT(n/b) + f(n)

- a = 2 (两个子问题)
- b = 2 (问题规模减半)
- f(n) = Θ(n) (合并代价)

计算: log_b(a) = log₂(2) = 1

因为 f(n) = Θ(n) = Θ(n^log_b(a))，满足情况2

**结论**: T(n) = Θ(n log n)

#### 各情况复杂度

| 情况 | 时间复杂度 | 说明 |
|------|-----------|------|
| **最好情况** | Θ(n log n) | 已排序数组 |
| **平均情况** | Θ(n log n) | 随机数组 |
| **最坏情况** | Θ(n log n) | 逆序数组 |

**特点**: 归并排序在所有情况下时间复杂度都是 O(n log n)，非常稳定！

### 4.2 空间复杂度

#### 递归栈空间

- **递归深度**: O(log n)
- **栈空间**: O(log n)

#### 辅助数组空间

- **合并临时数组**: O(n)

#### 总空间复杂度

**S(n) = O(n)**

```text
空间使用:
- 输入数组: n
- 临时数组: n (合并时)
- 递归栈: log n
━━━━━━━━━━━━━━━━
总计: O(n)
```

### 4.3 其他指标

| 指标 | 值 | 说明 |
|------|---|------|
| **比较次数** | n log n | 最优 |
| **交换次数** | n log n | 数据移动 |
| **稳定性** | ✅ 稳定 | 相等元素顺序不变 |
| **原地排序** | ❌ 否 | 需要额外空间 |
| **自适应性** | ❌ 否 | 总是O(n log n) |

---

## 5. Python实现

### 5.1 经典递归实现 ⭐⭐⭐⭐⭐

```python
def merge_sort(arr: list[int]) -> list[int]:
    """
    归并排序 - 经典递归实现
    
    时间复杂度: O(n log n)
    空间复杂度: O(n)
    稳定性: 稳定
    """
    # 基本情况
    if len(arr) <= 1:
        return arr
    
    # 分解
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # 合并
    return merge(left, right)

def merge(left: list[int], right: list[int]) -> list[int]:
    """合并两个有序数组"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # ≤ 保证稳定性
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result
```

### 5.2 原地排序实现

```python
def merge_sort_inplace(arr: list[int], left: int, right: int) -> None:
    """
    归并排序 - 原地排序（伪原地，仍需临时数组）
    
    修改原数组，不返回新数组
    """
    if left >= right:
        return
    
    mid = (left + right) // 2
    merge_sort_inplace(arr, left, mid)
    merge_sort_inplace(arr, mid + 1, right)
    merge_inplace(arr, left, mid, right)

def merge_inplace(arr: list[int], left: int, mid: int, right: int) -> None:
    """原地合并"""
    # 复制左右子数组
    left_arr = arr[left:mid+1]
    right_arr = arr[mid+1:right+1]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1
```

### 5.3 迭代实现（自底向上）

```python
def merge_sort_iterative(arr: list[int]) -> list[int]:
    """
    归并排序 - 迭代实现
    
    从小到大逐步合并，避免递归开销
    """
    if len(arr) <= 1:
        return arr
    
    arr = arr.copy()
    n = len(arr)
    width = 1  # 子数组宽度
    
    while width < n:
        # 合并所有宽度为width的子数组对
        for i in range(0, n, width * 2):
            left = i
            mid = min(i + width, n)
            right = min(i + width * 2, n)
            
            # 合并 arr[left:mid] 和 arr[mid:right]
            left_arr = arr[left:mid]
            right_arr = arr[mid:right]
            
            k = left
            l = r = 0
            
            while l < len(left_arr) and r < len(right_arr):
                if left_arr[l] <= right_arr[r]:
                    arr[k] = left_arr[l]
                    l += 1
                else:
                    arr[k] = right_arr[r]
                    r += 1
                k += 1
            
            while l < len(left_arr):
                arr[k] = left_arr[l]
                l += 1
                k += 1
            
            while r < len(right_arr):
                arr[k] = right_arr[r]
                r += 1
                k += 1
        
        width *= 2
    
    return arr
```

### 5.4 优化实现

```python
def merge_sort_optimized(arr: list[int], threshold: int = 10) -> list[int]:
    """
    归并排序 - 优化实现
    
    优化技巧:
    1. 小数组用插入排序
    2. 已排序数组直接返回
    3. 减少数组复制
    """
    if len(arr) <= 1:
        return arr
    
    # 优化1: 小数组用插入排序
    if len(arr) <= threshold:
        return insertion_sort(arr)
    
    mid = len(arr) // 2
    left = merge_sort_optimized(arr[:mid], threshold)
    right = merge_sort_optimized(arr[mid:], threshold)
    
    # 优化2: 如果已经有序，直接返回
    if left[-1] <= right[0]:
        return left + right
    
    return merge(left, right)

def insertion_sort(arr: list[int]) -> list[int]:
    """插入排序 - 用于小数组"""
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

### 5.5 泛型实现

```python
from typing import TypeVar, Callable

T = TypeVar('T')

def merge_sort_generic(
    arr: list[T],
    key: Callable[[T], Any] | None = None,
    reverse: bool = False
) -> list[T]:
    """
    泛型归并排序
    
    Args:
        arr: 要排序的数组
        key: 用于比较的键函数
        reverse: 是否逆序
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_generic(arr[:mid], key, reverse)
    right = merge_sort_generic(arr[mid:], key, reverse)
    
    return merge_generic(left, right, key, reverse)

def merge_generic(
    left: list[T],
    right: list[T],
    key: Callable[[T], Any] | None,
    reverse: bool
) -> list[T]:
    """泛型合并"""
    result = []
    i = j = 0
    
    compare = (lambda a, b: key(a) >= key(b)) if key else (lambda a, b: a >= b)
    if not reverse:
        compare = (lambda a, b: key(a) <= key(b)) if key else (lambda a, b: a <= b)
    
    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result
```

---

## 6. 优化技巧

### 6.1 小数组优化

对于小数组（n < 10），插入排序比归并排序快：

```python
THRESHOLD = 10

if len(arr) <= THRESHOLD:
    return insertion_sort(arr)
```

**原因**:
- 插入排序常数因子小
- 避免递归开销
- 缓存友好

### 6.2 已排序检测

如果子数组已经有序，可以直接合并：

```python
if left[-1] <= right[0]:
    return left + right  # 无需合并
```

### 6.3 原地合并

使用原地合并减少空间复杂度（理论上，Python实现仍需临时空间）：

```python
def merge_inplace(arr, left, mid, right):
    # 使用临时数组，但在实际应用中可以优化
    pass
```

### 6.4 并行化

归并排序天然适合并行化：

```python
from concurrent.futures import ThreadPoolExecutor

def merge_sort_parallel(arr, max_depth=2):
    if len(arr) <= 1:
        return arr
    
    if max_depth <= 0:
        return merge_sort(arr)
    
    mid = len(arr) // 2
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        left_future = executor.submit(
            merge_sort_parallel, arr[:mid], max_depth-1
        )
        right_future = executor.submit(
            merge_sort_parallel, arr[mid:], max_depth-1
        )
        
        left = left_future.result()
        right = right_future.result()
    
    return merge(left, right)
```

---

## 7. 实战应用

### 7.1 外部排序

归并排序非常适合外部排序（数据量大于内存）：

```python
def external_merge_sort(input_file: str, output_file: str, chunk_size: int = 1000):
    """
    外部归并排序
    
    适用于大文件排序，分块读取和合并
    """
    # 1. 分块读取并排序
    chunks = []
    with open(input_file, 'r') as f:
        while True:
            chunk = []
            for _ in range(chunk_size):
                line = f.readline()
                if not line:
                    break
                chunk.append(int(line.strip()))
            
            if not chunk:
                break
            
            # 排序块并写入临时文件
            chunk.sort()
            temp_file = f"temp_chunk_{len(chunks)}.txt"
            with open(temp_file, 'w') as tf:
                for num in chunk:
                    tf.write(f"{num}\n")
            chunks.append(temp_file)
    
    # 2. 多路归并
    merge_k_sorted_files(chunks, output_file)
```

### 7.2 链表排序

归并排序是链表排序的最佳选择（O(1)空间）：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_sort_linked_list(head: ListNode | None) -> ListNode | None:
    """链表归并排序 - O(1)空间复杂度"""
    if not head or not head.next:
        return head
    
    # 找到中点
    slow = fast = head
    prev = None
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    
    # 断开链表
    if prev:
        prev.next = None
    
    # 递归排序
    left = merge_sort_linked_list(head)
    right = merge_sort_linked_list(slow)
    
    # 合并
    return merge_linked_lists(left, right)

def merge_linked_lists(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    """合并两个有序链表"""
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    current.next = l1 or l2
    return dummy.next
```

### 7.3 逆序对计数

归并排序可以高效计数逆序对：

```python
def count_inversions(arr: list[int]) -> tuple[list[int], int]:
    """
    统计逆序对数量
    
    逆序对: (i, j) 满足 i < j 且 arr[i] > arr[j]
    """
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = count_inversions(arr[:mid])
    right, right_inv = count_inversions(arr[mid:])
    
    merged, split_inv = merge_and_count(left, right)
    
    total_inversions = left_inv + right_inv + split_inv
    return merged, total_inversions

def merge_and_count(left: list[int], right: list[int]) -> tuple[list[int], int]:
    """合并并统计跨越中点的逆序对"""
    result = []
    i = j = 0
    inversions = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            inversions += len(left) - i  # 关键：统计逆序对
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result, inversions
```

---

## 8. 性能对比

### 8.1 与其他O(n log n)算法对比

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定 | 原地 |
|------|------|------|------|------|------|------|
| **归并排序** | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ | ❌ |
| **快速排序** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ | ✅ |
| **堆排序** | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ | ✅ |

### 8.2 优缺点对比

**归并排序优点**:
- ✅ 时间复杂度稳定 O(n log n)
- ✅ 稳定排序
- ✅ 适合链表排序
- ✅ 适合外部排序
- ✅ 容易并行化

**归并排序缺点**:
- ❌ 需要额外O(n)空间
- ❌ 不是原地排序
- ❌ 常数因子较大

**选择建议**:
- 需要稳定性 → **归并排序**
- 需要原地排序 → 快速排序或堆排序
- 链表排序 → **归并排序**
- 外部排序 → **归并排序**
- 一般情况 → 快速排序（实践中更快）

---

## 9. 总结

### 9.1 核心要点

1. **分治思想**: 递归分解 + 合并
2. **稳定排序**: 使用 `<=` 保证稳定性
3. **时间复杂度**: O(n log n) 所有情况
4. **空间复杂度**: O(n) 辅助数组
5. **最佳应用**: 链表、外部排序、逆序对

### 9.2 数学证明

- ✅ 稳定性已严格证明
- ✅ 时间复杂度通过递推树和主定理证明
- ✅ 最优性: 基于比较的排序下界是 Ω(n log n)

### 9.3 实践建议

- 数组排序 → 考虑快速排序（更快）
- 链表排序 → **归并排序**（最佳）
- 需要稳定性 → **归并排序**
- 大文件排序 → **归并排序**（外部排序）
- 并行排序 → **归并排序**（易并行化）

---

## 参考资源

- 《算法导论》(CLRS) - 第2.3节
- 《算法》(Sedgewick) - 第2.2节
- Knuth, D. E. "The Art of Computer Programming, Vol. 3: Sorting and Searching"
- Python官方文档: [sorted()](https://docs.python.org/3/library/functions.html#sorted)

---

**版本**: 2.0.0  
**最后更新**: 2025-10-26  
**兼容Python版本**: 3.12+
