# Radix Sort - 基数排序

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

**基数排序（Radix Sort）** 是一种非比较排序算法，通过按位排序来实现整体排序。

### 核心特点

- ⏱️ **时间复杂度**: O(d(n+k)) - d是位数
- 💾 **空间复杂度**: O(n+k)
- 🔄 **稳定性**: 稳定
- 📊 **适用场景**: 整数、字符串

### 算法优势

✅ **线性时间** - 位数固定时为O(n)  
✅ **稳定排序** - 保持相同元素相对顺序  
✅ **适合大数据** - 位数少时比比较排序快

### 算法劣势

❌ **空间消耗** - 需要额外空间  
❌ **位数影响** - 位数多时性能下降  
❌ **类型限制** - 主要用于整数和字符串

---

## 2. 算法原理

### 核心思想

```
从最低位到最高位，依次对每一位进行稳定排序

示例: [170, 45, 75, 90, 802, 24, 2, 66]

LSD (Least Significant Digit) 从个位开始:

个位排序:
170, 90, 802, 2, 24, 45, 75, 66

十位排序:
802, 2, 24, 45, 66, 170, 75, 90

百位排序:
2, 24, 45, 66, 75, 90, 170, 802

结果: [2, 24, 45, 66, 75, 90, 170, 802]
```

---

## 3. Python实现

### 3.1 基础实现（LSD）

```python
from typing import List

def radix_sort(arr: List[int]) -> List[int]:
    """
    基数排序 - LSD实现
    
    时间复杂度: O(d(n+k)) where d是最大数的位数
    空间复杂度: O(n+k)
    稳定性: 稳定
    
    Args:
        arr: 待排序数组（非负整数）
    
    Returns:
        排序后的数组
    
    Example:
        >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
        [2, 24, 45, 66, 75, 90, 170, 802]
    """
    if not arr:
        return arr
    
    # 找最大值，确定位数
    max_val = max(arr)
    
    # 从个位开始，对每一位进行计数排序
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr


def counting_sort_by_digit(arr: List[int], exp: int) -> None:
    """
    按指定位进行计数排序
    
    Args:
        arr: 数组
        exp: 位数（1=个位, 10=十位, 100=百位...）
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # 0-9
    
    # 统计当前位的数字出现次数
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1
    
    # 计算累计次数
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # 从后向前填充（保持稳定性）
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    # 复制回原数组
    for i in range(n):
        arr[i] = output[i]
```

### 3.2 字符串基数排序

```python
def radix_sort_strings(strings: List[str]) -> List[str]:
    """
    字符串基数排序
    
    假设所有字符串长度相同
    """
    if not strings or not strings[0]:
        return strings
    
    max_len = len(strings[0])
    
    # 从最后一个字符到第一个字符
    for pos in range(max_len - 1, -1, -1):
        # 按当前位置的字符排序
        strings = sorted(strings, key=lambda s: s[pos])
    
    return strings
```

---

## 4. 复杂度分析

### 时间复杂度

**O(d(n+k))** - 其中d是位数，k是基数（通常为10）

```python
# d = 最大数的位数
# n = 元素个数
# k = 基数（0-9）
#
# 每一位做一次计数排序: O(n+k)
# 总共d位: O(d(n+k))
#
# 当d是常数时，复杂度为O(n)
```

### 空间复杂度

**O(n+k)** - 需要额外数组

---

## 5. 应用场景

### ✅ 适用场景

1. **位数固定的整数**
   ```python
   # 电话号码、学号等
   phone_numbers = [13912345678, 13812345678, ...]
   radix_sort(phone_numbers)
   ```

2. **字符串排序**
   ```python
   # 等长字符串
   codes = ["ABC123", "XYZ456", "DEF789"]
   radix_sort_strings(codes)
   ```

### ❌ 不适用场景

1. **位数差异大**
   ```python
   # 效率低
   arr = [1, 10000000]
   ```

2. **浮点数**
   ```python
   # 不适用
   ```

---

## 6. 与其他排序算法对比

| 算法 | 时间 | 空间 | 稳定性 | 适用 |
|-----|------|------|--------|------|
| **基数排序** | O(d(n+k)) | O(n+k) | ✅ | 整数、字符串 |
| **计数排序** | O(n+k) | O(k) | ✅ | 整数、范围小 |
| **快速排序** | O(n log n) | O(log n) | ❌ | 通用 |

---

## 7. LeetCode相关题目

| 题号 | 题目 | 难度 | 考点 |
|-----|------|------|------|
| 164 | 最大间距 | Hard | 基数排序/桶排序 |
| 912 | 排序数组 | Medium | 排序实现 |

---

## 8. 性能测试

```python
def benchmark_radix_sort():
    """性能测试"""
    import time
    import random
    
    # 固定位数的大数据
    arr = [random.randint(0, 9999) for _ in range(10000)]
    
    start = time.perf_counter()
    radix_sort(arr.copy())
    radix_time = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    sorted(arr)
    python_time = (time.perf_counter() - start) * 1000
    
    print(f"基数排序: {radix_time:.3f}ms")
    print(f"Python内置: {python_time:.3f}ms")

benchmark_radix_sort()
```

---

## 9. 常见陷阱与最佳实践

### 陷阱1：未保持稳定性

```python
# ❌ 错误：不稳定的排序会破坏基数排序
# 必须使用稳定排序（如计数排序）

# ✅ 正确：使用稳定的计数排序
```

### 最佳实践

✅ **检查位数**
```python
def smart_radix_sort(arr):
    if not arr:
        return arr
    
    max_val = max(arr)
    digits = len(str(max_val))
    
    # 位数少：基数排序
    if digits <= 6:
        return radix_sort(arr)
    
    # 位数多：快速排序
    return sorted(arr)
```

---

## 10. 总结

基数排序是一种高效的非比较排序算法，特别适合位数固定的整数排序。

### 核心要点

✅ **时间复杂度**: O(d(n+k)) - 位数固定时为O(n)  
✅ **空间复杂度**: O(n+k)  
✅ **稳定性**: 稳定排序  
✅ **限制**: 适用于整数和字符串

### 使用建议

- ✅ 位数固定的整数
- ✅ 等长字符串
- ✅ 大数据量
- ❌ 位数差异大
- ❌ 浮点数

基数排序是处理大量整数的excellent选择！🚀
