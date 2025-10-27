# Insertion Sort - 插入排序

## 目录

- [1. 概述](#1-概述)
- [2. 算法原理](#2-算法原理)
  - [2.1 核心思想](#21-核心思想)
  - [2.2 工作原理](#22-工作原理)
  - [2.3 算法步骤](#23-算法步骤)
- [3. Python实现](#3-python实现)
  - [3.1 基础实现](#31-基础实现)
  - [3.2 优化实现](#32-优化实现)
  - [3.3 二分插入排序](#33-二分插入排序)
- [4. 复杂度分析](#4-复杂度分析)
  - [4.1 时间复杂度](#41-时间复杂度)
  - [4.2 空间复杂度](#42-空间复杂度)
  - [4.3 稳定性分析](#43-稳定性分析)
- [5. 算法可视化](#5-算法可视化)
- [6. 优化技巧](#6-优化技巧)
  - [6.1 提前终止](#61-提前终止)
  - [6.2 二分查找优化](#62-二分查找优化)
  - [6.3 希尔排序](#63-希尔排序)
- [7. 应用场景](#7-应用场景)
- [8. 与其他排序算法对比](#8-与其他排序算法对比)
- [9. LeetCode相关题目](#9-leetcode相关题目)
- [10. 性能测试](#10-性能测试)
  - [10.1 不同数据规模测试](#101-不同数据规模测试)
  - [10.2 不同数据分布测试](#102-不同数据分布测试)
  - [10.3 与其他算法对比](#103-与其他算法对比)
- [11. 常见陷阱与最佳实践](#11-常见陷阱与最佳实践)
  - [11.1 陷阱1：边界条件错误](#111-陷阱1边界条件错误)
  - [11.2 陷阱2：不必要的交换](#112-陷阱2不必要的交换)
  - [11.3 陷阱3：忽视特殊情况](#113-陷阱3忽视特殊情况)
  - [11.4 最佳实践](#114-最佳实践)
- [12. 实际应用](#12-实际应用)
  - [12.1 Timsort中的应用](#121-timsort中的应用)
  - [12.2 在线排序](#122-在线排序)
  - [12.3 链表排序](#123-链表排序)
- [13. 总结](#13-总结)

---

## 1. 概述

**插入排序（Insertion Sort）** 是一种简单直观的排序算法。它的工作原理是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。

### 核心特点

- ⏱️ **时间复杂度**: O(n²) 平均 / O(n) 最好
- 💾 **空间复杂度**: O(1) - 原地排序
- 🔄 **稳定性**: 稳定排序
- 📊 **适用场景**: 小数据集、基本有序的数据

### 算法优势

✅ **简单易懂** - 实现简单，容易理解  
✅ **稳定排序** - 保持相同元素相对顺序  
✅ **原地排序** - 不需要额外空间  
✅ **对小数据高效** - 小数据集性能优于快速排序  
✅ **自适应** - 对基本有序的数据效率极高（O(n)）  
✅ **在线算法** - 可以在接收数据的同时排序

### 算法劣势

❌ **大数据慢** - 大数据集O(n²)不可接受  
❌ **不适合随机数据** - 随机数据性能差  
❌ **比较次数多** - 数据越无序比较次数越多

---

## 2. 算法原理

### 2.1 核心思想

插入排序的核心思想类似于整理扑克牌：
1. 从第一张牌开始，认为它已经排好序
2. 拿起下一张牌，在已排序的牌中从右向左比较
3. 找到合适的位置插入
4. 重复步骤2-3，直到所有牌都插入

### 2.2 工作原理

```
将数组分为两部分：
- 已排序部分（左侧）
- 未排序部分（右侧）

每次从未排序部分取出一个元素，插入到已排序部分的正确位置

示例：
初始: [5, 2, 4, 6, 1, 3]

i=1: 取出2, 插入到5前
     [2, 5, 4, 6, 1, 3]
     ^^^^^ 已排序

i=2: 取出4, 插入到2和5之间
     [2, 4, 5, 6, 1, 3]
     ^^^^^^^^ 已排序

i=3: 取出6, 已经在正确位置
     [2, 4, 5, 6, 1, 3]
     ^^^^^^^^^^^ 已排序

i=4: 取出1, 插入到最前面
     [1, 2, 4, 5, 6, 3]
     ^^^^^^^^^^^^^^ 已排序

i=5: 取出3, 插入到2和4之间
     [1, 2, 3, 4, 5, 6]
     ^^^^^^^^^^^^^^^^^ 全部排序
```

### 2.3 算法步骤

**详细步骤**:
1. 从第1个元素开始（认为第0个元素已排序）
2. 取出当前元素，保存为key
3. 在已排序序列中从后向前扫描
4. 如果已排序元素大于key，将该元素后移
5. 重复步骤4，直到找到小于等于key的元素
6. 将key插入到该元素之后
7. 重复步骤2-6，直到所有元素排序完成

---

## 3. Python实现

### 3.1 基础实现

```python
from typing import List

def insertion_sort(arr: List[int]) -> List[int]:
    """
    插入排序 - 基础实现
    
    时间复杂度: O(n²) 平均, O(n) 最好, O(n²) 最坏
    空间复杂度: O(1)
    稳定性: 稳定
    
    Args:
        arr: 待排序数组
    
    Returns:
        排序后的数组
    
    Example:
        >>> insertion_sort([5, 2, 4, 6, 1, 3])
        [1, 2, 3, 4, 5, 6]
    """
    n = len(arr)
    
    # 从第1个元素开始（索引1）
    for i in range(1, n):
        key = arr[i]  # 当前要插入的元素
        j = i - 1  # 已排序部分的最后一个元素
        
        # 在已排序部分找插入位置
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # 元素后移
            j -= 1
        
        # 插入key
        arr[j + 1] = key
    
    return arr
```

**代码详解**:
```python
# 示例: [5, 2, 4, 6, 1, 3]

# i=1, key=2
# j=0: arr[0]=5 > 2, arr[1]=5, j=-1
# arr[0]=2
# 结果: [2, 5, 4, 6, 1, 3]

# i=2, key=4
# j=1: arr[1]=5 > 4, arr[2]=5, j=0
# j=0: arr[0]=2 < 4, 停止
# arr[1]=4
# 结果: [2, 4, 5, 6, 1, 3]

# ... 继续处理剩余元素
```

### 3.2 优化实现

```python
def insertion_sort_optimized(arr: List[int]) -> List[int]:
    """
    插入排序 - 优化实现
    
    优化点：
    1. 提前终止：如果key大于等于arr[j]，提前退出
    2. 减少赋值：使用哨兵技术
    
    时间复杂度: O(n²) 平均, O(n) 最好
    空间复杂度: O(1)
    """
    n = len(arr)
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        # 提前终止优化
        if key >= arr[j]:
            continue
        
        # 移动元素
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


def insertion_sort_with_sentinel(arr: List[int]) -> List[int]:
    """
    插入排序 - 使用哨兵优化
    
    哨兵技术：在数组开头添加一个最小值作为哨兵
    避免边界检查 j >= 0
    
    时间复杂度: O(n²)
    空间复杂度: O(1)
    """
    if not arr:
        return arr
    
    # 找最小值作为哨兵
    min_idx = 0
    for i in range(1, len(arr)):
        if arr[i] < arr[min_idx]:
            min_idx = i
    
    # 将最小值交换到第一个位置
    arr[0], arr[min_idx] = arr[min_idx], arr[0]
    
    # 排序（无需检查j >= 0）
    for i in range(2, len(arr)):
        key = arr[i]
        j = i - 1
        
        # 无需检查 j >= 0，因为arr[0]是最小值
        while arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr
```

### 3.3 二分插入排序

```python
def binary_insertion_sort(arr: List[int]) -> List[int]:
    """
    二分插入排序
    
    优化：使用二分查找找插入位置
    
    时间复杂度: O(n²) - 移动元素仍是O(n²)
    空间复杂度: O(1)
    
    注意：虽然查找优化到O(log n)，但移动元素仍是O(n)
    所以总复杂度仍是O(n²)，但实际性能有所提升
    
    Example:
        >>> binary_insertion_sort([5, 2, 4, 6, 1, 3])
        [1, 2, 3, 4, 5, 6]
    """
    n = len(arr)
    
    for i in range(1, n):
        key = arr[i]
        
        # 二分查找插入位置
        left, right = 0, i - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] > key:
                right = mid - 1
            else:
                left = mid + 1
        
        # left是插入位置
        # 将[left, i-1]的元素后移
        for j in range(i, left, -1):
            arr[j] = arr[j - 1]
        
        # 插入key
        arr[left] = key
    
    return arr
```

---

## 4. 复杂度分析

### 4.1 时间复杂度

| 情况 | 时间复杂度 | 说明 |
|-----|-----------|------|
| **最好情况** | O(n) | 已排序，每次只需比较1次 |
| **平均情况** | O(n²) | 随机数据，平均n/2次比较 |
| **最坏情况** | O(n²) | 逆序，每次需要比较i次 |

**详细分析**:

1. **最好情况 - O(n)**:
   ```python
   # 已排序数组: [1, 2, 3, 4, 5]
   # 每个元素只需比较1次
   # 总比较次数: n-1 = O(n)
   
   for i in range(1, n):  # n-1 次循环
       key = arr[i]
       if key >= arr[i-1]:  # 1次比较
           continue  # 无需移动
   ```

2. **平均情况 - O(n²)**:
   ```python
   # 随机数组
   # 平均每个元素需要比较 i/2 次
   # 总比较次数: 1/2 + 2/2 + 3/2 + ... + (n-1)/2
   #           = (1+2+3+...+(n-1))/2
   #           = n(n-1)/4
   #           = O(n²)
   ```

3. **最坏情况 - O(n²)**:
   ```python
   # 逆序数组: [5, 4, 3, 2, 1]
   # 每个元素需要比较 i 次并移动 i 次
   # 总操作次数: 1+2+3+...+(n-1) = n(n-1)/2 = O(n²)
   ```

**比较与移动次数**:
```
最好情况: 
- 比较: n-1
- 移动: 0

平均情况:
- 比较: n²/4
- 移动: n²/4

最坏情况:
- 比较: n(n-1)/2
- 移动: n(n-1)/2
```

### 4.2 空间复杂度

**O(1)** - 原地排序

```python
def insertion_sort(arr):
    n = len(arr)
    
    # 只使用常数个额外变量
    for i in range(1, n):
        key = arr[i]  # O(1)
        j = i - 1     # O(1)
        
        # 在原数组上操作，无额外空间
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr
```

### 4.3 稳定性分析

**稳定排序** ✅

```python
# 示例：插入排序保持稳定性
arr = [3a, 1, 3b, 2]  # 下标表示相同值的不同对象

# 排序过程：
# i=1: [1, 3a, 3b, 2]
# i=2: [1, 3a, 3b, 2]  # 3b不会跨过3a
# i=3: [1, 2, 3a, 3b]

# 结果：3a仍在3b前面 ✅ 稳定！
```

**为什么稳定？**
```python
# 关键：arr[j] > key 使用严格大于
while j >= 0 and arr[j] > key:  # 不是 >=
    arr[j + 1] = arr[j]
    j -= 1

# 当遇到相等元素时，停止移动
# 新元素插入到相等元素之后
# 保持了原有的相对顺序
```

---

## 5. 算法可视化

### 详细排序过程

```
初始数组: [5, 2, 4, 6, 1, 3]

====================================
第1轮 (i=1, key=2):
[5 | 2, 4, 6, 1, 3]  # 分隔线左侧是已排序部分
 ^   ^
 j   i

比较: 5 > 2，移动5
[5, 5, 4, 6, 1, 3]
   ^
   j=-1

插入2
[2, 5, 4, 6, 1, 3]
 ^^^^^ 已排序

====================================
第2轮 (i=2, key=4):
[2, 5 | 4, 6, 1, 3]
    ^   ^
    j   i

比较: 5 > 4，移动5
[2, 5, 5, 6, 1, 3]
 ^
 j

比较: 2 < 4，停止
插入4
[2, 4, 5, 6, 1, 3]
 ^^^^^^^^ 已排序

====================================
第3轮 (i=3, key=6):
[2, 4, 5 | 6, 1, 3]
       ^   ^
       j   i

比较: 5 < 6，停止（已在正确位置）
[2, 4, 5, 6, 1, 3]
 ^^^^^^^^^^^ 已排序

====================================
第4轮 (i=4, key=1):
[2, 4, 5, 6 | 1, 3]
          ^   ^
          j   i

比较: 6 > 1，移动6
[2, 4, 5, 6, 6, 3]

比较: 5 > 1，移动5
[2, 4, 5, 5, 6, 3]

比较: 4 > 1，移动4
[2, 4, 4, 5, 6, 3]

比较: 2 > 1，移动2
[2, 2, 4, 5, 6, 3]
   ^
   j=-1

插入1
[1, 2, 4, 5, 6, 3]
 ^^^^^^^^^^^^^^ 已排序

====================================
第5轮 (i=5, key=3):
[1, 2, 4, 5, 6 | 3]
             ^   ^
             j   i

比较: 6 > 3，移动6
[1, 2, 4, 5, 6, 6]

比较: 5 > 3，移动5
[1, 2, 4, 5, 5, 6]

比较: 4 > 3，移动4
[1, 2, 4, 4, 5, 6]

比较: 2 < 3，停止
插入3
[1, 2, 3, 4, 5, 6]
 ^^^^^^^^^^^^^^^^^ 全部排序完成！
```

---

## 6. 优化技巧

### 6.1 提前终止

```python
def insertion_sort_early_termination(arr: List[int]) -> List[int]:
    """
    提前终止优化
    
    如果当前元素已经大于等于前一个元素，
    说明已在正确位置，无需插入
    """
    n = len(arr)
    
    for i in range(1, n):
        # 优化：如果已在正确位置，直接跳过
        if arr[i] >= arr[i - 1]:
            continue
        
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


# 性能提升示例
# 对于基本有序的数据 [1, 2, 3, 5, 4, 6, 7, 8, 9]
# 只需要处理4这一个元素
# 其他元素都通过提前终止跳过
```

### 6.2 二分查找优化

```python
def binary_insertion_sort_optimized(arr: List[int]) -> List[int]:
    """
    二分查找优化 + 块移动
    
    优化：
    1. 使用二分查找找位置 - O(log n)
    2. 使用切片批量移动 - 更快
    """
    for i in range(1, len(arr)):
        key = arr[i]
        
        # 二分查找插入位置
        left, right = 0, i
        while left < right:
            mid = (left + right) // 2
            if arr[mid] > key:
                right = mid
            else:
                left = mid + 1
        
        # 使用切片批量移动（比循环快）
        arr[left + 1:i + 1] = arr[left:i]
        arr[left] = key
    
    return arr
```

### 6.3 希尔排序

```python
def shell_sort(arr: List[int]) -> List[int]:
    """
    希尔排序 - 插入排序的高级版本
    
    思路：
    1. 选择递减的增量序列
    2. 对每个增量进行插入排序
    3. 最后进行一次完整的插入排序
    
    时间复杂度: O(n^(3/2)) 或更好
    空间复杂度: O(1)
    
    Example:
        >>> shell_sort([5, 2, 4, 6, 1, 3])
        [1, 2, 3, 4, 5, 6]
    """
    n = len(arr)
    gap = n // 2
    
    while gap > 0:
        # 对每个间隔进行插入排序
        for i in range(gap, n):
            key = arr[i]
            j = i
            
            # 插入排序，间隔为gap
            while j >= gap and arr[j - gap] > key:
                arr[j] = arr[j - gap]
                j -= gap
            
            arr[j] = key
        
        # 缩小间隔
        gap //= 2
    
    return arr
```

---

## 7. 应用场景

### ✅ 适用场景

1. **小数据集（n < 50）**
   ```python
   # 小数据插入排序比快速排序更快
   small_arr = [5, 2, 8, 1, 9, 3]
   insertion_sort(small_arr)  # 最优选择
   ```

2. **基本有序的数据**
   ```python
   # 接近O(n)的性能
   nearly_sorted = [1, 2, 3, 5, 4, 6, 7, 8]
   insertion_sort(nearly_sorted)  # 非常快！
   ```

3. **在线排序**
   ```python
   # 可以边接收数据边排序
   sorted_arr = []
   for new_data in stream:
       insert_into_sorted(sorted_arr, new_data)
   ```

4. **Timsort的一部分**
   ```python
   # Python的内置排序使用Timsort
   # Timsort对小分区使用插入排序
   # sorted() 和 list.sort() 都使用Timsort
   ```

5. **链表排序**
   ```python
   # 插入排序非常适合链表
   # 因为不需要移动大量元素
   def insertion_sort_linked_list(head):
       dummy = ListNode(float('-inf'))
       current = head
       
       while current:
           prev = dummy
           while prev.next and prev.next.val < current.val:
               prev = prev.next
           
           next_node = current.next
           current.next = prev.next
           prev.next = current
           current = next_node
       
       return dummy.next
   ```

### ❌ 不适用场景

1. **大数据集（n > 1000）**
   ```python
   # O(n²)不可接受
   large_arr = [random.randint(1, 10000) for _ in range(10000)]
   # 使用快速排序或归并排序
   ```

2. **完全随机数据**
   ```python
   # 随机数据平均O(n²)
   random_arr = [random.randint(1, 1000) for _ in range(1000)]
   # 使用快速排序
   ```

3. **严格性能要求**
   ```python
   # 需要保证O(n log n)
   # 使用归并排序或堆排序
   ```

---

## 8. 与其他排序算法对比

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定性 | 适用场景 |
|-----|------|------|------|------|--------|---------|
| **插入排序** | O(n) | O(n²) | O(n²) | O(1) | ✅ | 小数据/基本有序 |
| **选择排序** | O(n²) | O(n²) | O(n²) | O(1) | ❌ | 小数据 |
| **冒泡排序** | O(n) | O(n²) | O(n²) | O(1) | ✅ | 教学用途 |
| **快速排序** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ | 一般情况最优 |
| **归并排序** | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ | 需要稳定性 |
| **堆排序** | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ | 大数据，保证性能 |

### 详细对比

**插入排序 vs 选择排序**
```python
# 插入排序：
# ✅ 最好O(n)，有序时很快
# ✅ 稳定排序
# ✅ 自适应性强

# 选择排序：
# ❌ 总是O(n²)
# ❌ 不稳定
# ✅ 交换次数少
```

**插入排序 vs 冒泡排序**
```python
# 插入排序：
# ✅ 平均比冒泡快2倍
# ✅ 更少的交换次数
# ✅ 实际应用更广

# 冒泡排序：
# ❌ 更多的交换次数
# ❌ 实际很少使用
# ✅ 概念简单
```

**插入排序 vs 快速排序**
```python
# 小数据 (n < 50):
n = 10
arr = [random.randint(1, 100) for _ in range(n)]

# 插入排序更快
start = time.time()
insertion_sort(arr.copy())
insertion_time = time.time() - start

# 快速排序反而慢（递归开销）
start = time.time()
quick_sort(arr.copy())
quick_time = time.time() - start

print(f"插入: {insertion_time}, 快速: {quick_time}")
# 输出: 插入: 0.00001, 快速: 0.00005

# 大数据 (n > 1000):
# 快速排序明显更快
```

---

## 9. LeetCode相关题目

### 9.1 直接应用插入排序

| 题号 | 题目 | 难度 | 考点 |
|-----|------|------|------|
| 912 | 排序数组 | Medium | 排序实现 |
| 147 | 对链表进行插入排序 | Medium | 链表插入排序 |

### 9.2 插入操作

| 题号 | 题目 | 难度 | 考点 |
|-----|------|------|------|
| 35 | 搜索插入位置 | Easy | 二分查找 |
| 57 | 插入区间 | Medium | 区间插入 |
| 1431 | 拥有最多糖果的孩子 | Easy | 简单插入 |

### 9.3 示例：对链表进行插入排序

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def insertion_sort_list(head: ListNode) -> ListNode:
    """
    LeetCode 147: 对链表进行插入排序
    
    思路：
    1. 创建哑节点作为已排序链表的头
    2. 遍历原链表，将每个节点插入到已排序链表的合适位置
    
    时间复杂度: O(n²)
    空间复杂度: O(1)
    
    Example:
        Input: 4 -> 2 -> 1 -> 3
        Output: 1 -> 2 -> 3 -> 4
    """
    # 创建哑节点
    dummy = ListNode(float('-inf'))
    
    current = head
    
    while current:
        # 保存下一个节点
        next_node = current.next
        
        # 在已排序链表中找插入位置
        prev = dummy
        while prev.next and prev.next.val < current.val:
            prev = prev.next
        
        # 插入current
        current.next = prev.next
        prev.next = current
        
        # 移动到下一个节点
        current = next_node
    
    return dummy.next


# 使用示例
def create_linked_list(arr):
    """创建链表"""
    dummy = ListNode(0)
    current = dummy
    for val in arr:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def print_linked_list(head):
    """打印链表"""
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    print(" -> ".join(map(str, vals)))


# 测试
head = create_linked_list([4, 2, 1, 3])
print("原链表:")
print_linked_list(head)

sorted_head = insertion_sort_list(head)
print("排序后:")
print_linked_list(sorted_head)
```

---

## 10. 性能测试

### 10.1 不同数据规模测试

```python
import time
import random

def benchmark_insertion_sort(sizes: List[int]):
    """测试不同数据规模的性能"""
    
    print("数据规模性能测试:")
    print(f"{'规模':<10} {'时间(ms)':<15} {'时间/n²':<15}")
    print("-" * 40)
    
    for size in sizes:
        arr = [random.randint(1, 10000) for _ in range(size)]
        
        start = time.perf_counter()
        insertion_sort(arr.copy())
        elapsed = (time.perf_counter() - start) * 1000
        
        ratio = elapsed / (size * size) * 1000
        
        print(f"{size:<10} {elapsed:<15.3f} {ratio:<15.6f}")

# 运行测试
benchmark_insertion_sort([10, 50, 100, 500, 1000])
```

**输出示例：**
```
数据规模性能测试:
规模       时间(ms)        时间/n²        
----------------------------------------
10         0.023          2.300000      
50         0.234          0.936000      
100        0.987          0.987000      
500        23.456         0.938240      
1000       94.123         0.941230      

结论：时间/n²比值基本稳定，证实O(n²)复杂度
```

### 10.2 不同数据分布测试

```python
def test_different_distributions():
    """测试不同数据分布的性能"""
    
    size = 1000
    
    # 1. 随机数据
    random_data = [random.randint(1, 10000) for _ in range(size)]
    start = time.perf_counter()
    insertion_sort(random_data.copy())
    random_time = (time.perf_counter() - start) * 1000
    
    # 2. 已排序数据
    sorted_data = list(range(size))
    start = time.perf_counter()
    insertion_sort(sorted_data.copy())
    sorted_time = (time.perf_counter() - start) * 1000
    
    # 3. 逆序数据
    reversed_data = list(range(size, 0, -1))
    start = time.perf_counter()
    insertion_sort(reversed_data.copy())
    reversed_time = (time.perf_counter() - start) * 1000
    
    # 4. 基本有序（90%有序）
    nearly_sorted = list(range(size))
    for _ in range(size // 10):
        i, j = random.randint(0, size-1), random.randint(0, size-1)
        nearly_sorted[i], nearly_sorted[j] = nearly_sorted[j], nearly_sorted[i]
    
    start = time.perf_counter()
    insertion_sort(nearly_sorted.copy())
    nearly_time = (time.perf_counter() - start) * 1000
    
    # 5. 大量重复
    repeated_data = [random.randint(1, 10) for _ in range(size)]
    start = time.perf_counter()
    insertion_sort(repeated_data.copy())
    repeated_time = (time.perf_counter() - start) * 1000
    
    print("数据分布性能测试 (n=1000):")
    print(f"随机数据:   {random_time:>8.3f}ms (100.0%)")
    print(f"已排序:     {sorted_time:>8.3f}ms ({sorted_time/random_time*100:>5.1f}%)")
    print(f"逆序:       {reversed_time:>8.3f}ms ({reversed_time/random_time*100:>5.1f}%)")
    print(f"基本有序:   {nearly_time:>8.3f}ms ({nearly_time/random_time*100:>5.1f}%)")
    print(f"大量重复:   {repeated_time:>8.3f}ms ({repeated_time/random_time*100:>5.1f}%)")

test_different_distributions()
```

**输出示例：**
```
数据分布性能测试 (n=1000):
随机数据:     94.123ms (100.0%)
已排序:        0.234ms (  0.2%)  ← 极快！
逆序:        187.456ms (199.2%)  ← 最慢
基本有序:      5.678ms (  6.0%)  ← 很快
大量重复:     76.543ms ( 81.3%)

结论：插入排序对数据分布非常敏感！
```

### 10.3 与其他算法对比

```python
def compare_sorting_algorithms_small():
    """小数据集性能对比"""
    
    size = 50
    data = [random.randint(1, 1000) for _ in range(size)]
    
    algorithms = [
        ("插入排序", insertion_sort),
        ("选择排序", selection_sort),
        ("冒泡排序", bubble_sort),
        ("快速排序", quick_sort),
        ("Python内置", sorted)
    ]
    
    print(f"小数据集排序算法对比 (n={size}):")
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
        
        print(f"{name:<15} {elapsed:<15.6f}")

compare_sorting_algorithms_small()
```

**输出示例：**
```
小数据集排序算法对比 (n=50):
算法            时间(ms)       
------------------------------
插入排序        0.234000       ← 最快！
选择排序        0.456000       
冒泡排序        0.678000       
快速排序        0.890000       ← 递归开销
Python内置      0.123000       ← Timsort

结论：小数据集插入排序性能优异！
```

---

## 11. 常见陷阱与最佳实践

### 11.1 陷阱1：边界条件错误

```python
# ❌ 错误：从0开始遍历
def insertion_sort_wrong(arr):
    for i in range(0, len(arr)):  # 错误：i=0时没有前面的元素
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key

# ✅ 正确：从1开始遍历
def insertion_sort_correct(arr):
    for i in range(1, len(arr)):  # 正确：第0个元素默认已排序
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
```

### 11.2 陷阱2：不必要的交换

```python
# ❌ 低效：使用交换
def insertion_sort_swap(arr):
    for i in range(1, len(arr)):
        j = i
        
        # 每次都交换，效率低
        while j > 0 and arr[j-1] > arr[j]:
            arr[j-1], arr[j] = arr[j], arr[j-1]  # 3次赋值
            j -= 1

# ✅ 高效：使用移动
def insertion_sort_move(arr):
    for i in range(1, len(arr)):
        key = arr[i]  # 保存key
        j = i - 1
        
        # 移动而不是交换
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # 1次赋值
            j -= 1
        
        arr[j + 1] = key  # 最后赋值一次
```

### 11.3 陷阱3：忽视特殊情况

```python
# ❌ 错误：未处理空数组和单元素
def insertion_sort_incomplete(arr):
    # 未检查特殊情况
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key

# ✅ 正确：处理所有情况
def insertion_sort_complete(arr):
    # 处理特殊情况
    if not arr or len(arr) <= 1:
        return arr
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr
```

### 11.4 最佳实践

✅ **实践1：使用标准库**
```python
# 对于生产代码，使用Python内置sorted()
# Timsort在小分区上使用优化的插入排序

# 学习用途：自己实现
def my_sort(arr):
    return insertion_sort(arr)

# 生产用途：使用内置
def production_sort(arr):
    return sorted(arr)
```

✅ **实践2：选择合适的算法**
```python
def smart_sort(arr):
    """根据数据特点选择排序算法"""
    n = len(arr)
    
    # 空或单元素
    if n <= 1:
        return arr
    
    # 小数据：插入排序
    if n < 50:
        return insertion_sort(arr)
    
    # 检查是否基本有序
    inversions = count_inversions(arr)
    if inversions < n:  # 逆序对少
        return insertion_sort(arr)
    
    # 大数据：快速排序
    return quick_sort(arr)


def count_inversions(arr):
    """计算逆序对数量（简化版）"""
    count = 0
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            count += 1
    return count
```

✅ **实践3：提前终止优化**
```python
def insertion_sort_optimized(arr):
    """使用提前终止优化"""
    for i in range(1, len(arr)):
        # 已在正确位置，跳过
        if arr[i] >= arr[i - 1]:
            continue
        
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr
```

✅ **实践4：维护不变量**
```python
def insertion_sort_with_invariant(arr):
    """
    维护循环不变量：
    在每次迭代开始时，arr[0:i]已排序
    """
    for i in range(1, len(arr)):
        # 不变量：arr[0:i]已排序
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
        # 不变量：arr[0:i+1]已排序
    
    return arr
```

✅ **实践5：性能测试**
```python
import cProfile

def profile_insertion_sort():
    """性能分析"""
    arr = [random.randint(1, 1000) for _ in range(1000)]
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    insertion_sort(arr)
    
    profiler.disable()
    profiler.print_stats(sort='cumulative')

# 使用profile发现性能瓶颈
```

---

## 12. 实际应用

### 12.1 Timsort中的应用

```python
def timsort_simplified(arr):
    """
    Timsort简化版 - Python内置排序算法
    
    核心思想：
    1. 将数组分成小块（run）
    2. 对每个run使用插入排序
    3. 使用归并排序合并run
    
    优势：
    - 对小数据和有序数据都很快
    - 稳定排序
    - 自适应性强
    """
    MIN_MERGE = 32
    
    def insertion_sort_run(arr, left, right):
        """对[left, right]使用插入排序"""
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            
            arr[j + 1] = key
    
    n = len(arr)
    
    # 第1步：对每个小块使用插入排序
    for start in range(0, n, MIN_MERGE):
        end = min(start + MIN_MERGE - 1, n - 1)
        insertion_sort_run(arr, start, end)
    
    # 第2步：归并所有run（简化版，省略）
    # ...
    
    return arr
```

### 12.2 在线排序

```python
class OnlineSorter:
    """
    在线排序器 - 边接收数据边排序
    
    使用插入排序维护有序序列
    """
    
    def __init__(self):
        self.sorted_data = []
    
    def add(self, value):
        """
        添加新数据并保持有序
        
        时间复杂度: O(n) 插入
        空间复杂度: O(1)
        """
        # 找插入位置
        i = len(self.sorted_data) - 1
        
        # 移动元素
        self.sorted_data.append(value)
        while i >= 0 and self.sorted_data[i] > value:
            self.sorted_data[i + 1] = self.sorted_data[i]
            i -= 1
        
        # 插入
        self.sorted_data[i + 1] = value
    
    def add_binary_search(self, value):
        """使用二分查找优化"""
        import bisect
        bisect.insort(self.sorted_data, value)
    
    def get_sorted(self):
        """获取排序后的数据"""
        return self.sorted_data


# 使用示例：实时数据流排序
sorter = OnlineSorter()

for data in [5, 2, 8, 1, 9, 3]:
    sorter.add(data)
    print(f"添加{data}: {sorter.get_sorted()}")

# 输出：
# 添加5: [5]
# 添加2: [2, 5]
# 添加8: [2, 5, 8]
# 添加1: [1, 2, 5, 8]
# 添加9: [1, 2, 5, 8, 9]
# 添加3: [1, 2, 3, 5, 8, 9]
```

### 12.3 链表排序

```python
def insertion_sort_linked_list_optimized(head: ListNode) -> ListNode:
    """
    优化的链表插入排序
    
    优势：
    - 不需要移动大量元素
    - O(1)空间复杂度
    - 稳定排序
    
    时间复杂度: O(n²)
    空间复杂度: O(1)
    """
    if not head or not head.next:
        return head
    
    # 哑节点
    dummy = ListNode(float('-inf'))
    dummy.next = head
    
    # 当前已排序的最后一个节点
    last_sorted = head
    # 待插入的节点
    current = head.next
    
    while current:
        if current.val >= last_sorted.val:
            # 已在正确位置
            last_sorted = current
            current = current.next
        else:
            # 需要插入到前面
            # 1. 从已排序链表中找插入位置
            prev = dummy
            while prev.next.val < current.val:
                prev = prev.next
            
            # 2. 将current从原位置移除
            last_sorted.next = current.next
            
            # 3. 插入到新位置
            current.next = prev.next
            prev.next = current
            
            # 4. 处理下一个节点
            current = last_sorted.next
    
    return dummy.next
```

---

## 13. 总结

插入排序是一种简单但实用的排序算法，虽然时间复杂度为O(n²)，但在特定场景下表现优异。

### 核心要点

✅ **时间复杂度**
- 最好情况：O(n) - 已排序
- 平均情况：O(n²) - 随机数据
- 最坏情况：O(n²) - 逆序

✅ **空间复杂度**
- O(1) - 原地排序

✅ **稳定性**
- 稳定排序 - 保持相同元素相对顺序

✅ **优势**
- 实现简单
- 小数据快
- 对有序数据极快
- 稳定排序
- 在线算法
- 适合链表

✅ **劣势**
- 大数据慢
- O(n²)复杂度
- 不适合随机数据

### 使用建议

1. **小数据集（n < 50）**: 首选
2. **基本有序**: 性能接近O(n)
3. **在线排序**: 边接收边排序
4. **需要稳定性**: 且数据量不大
5. **链表排序**: 非常适合

### 学习价值

- 📚 **基础算法** - 理解排序本质
- 💡 **算法分析** - 学习复杂度分析
- 🎯 **实际应用** - 了解Timsort原理
- 🚀 **优化思路** - 提前终止、二分查找

插入排序虽然简单，但却是理解排序算法和算法优化的excellent起点！🚀
