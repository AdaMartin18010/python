"""
Merge Sort - 归并排序完整实现

提供5种实现方式：
1. 经典递归实现
2. 原地排序实现
3. 迭代实现（自底向上）
4. 优化实现
5. 泛型实现
"""

from typing import TypeVar, Callable, Any
from dataclasses import dataclass
import time

T = TypeVar('T')

# ============================================================================
# 1. 经典递归实现 ⭐⭐⭐⭐⭐
# ============================================================================


def merge_sort(arr: list[int]) -> list[int]:
    """
    归并排序 - 经典递归实现
    
    时间复杂度: O(n log n)
    空间复杂度: O(n)
    稳定性: 稳定
    
    Args:
        arr: 待排序数组
    
    Returns:
        排序后的新数组
    """
    if len(arr) <= 1:
        return arr
    
    # 分解
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # 合并
    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    """
    合并两个有序数组
    
    使用 <= 而不是 < 保证稳定性
    """
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


# ============================================================================
# 2. 原地排序实现
# ============================================================================


def merge_sort_inplace(arr: list[int]) -> None:
    """
    归并排序 - 原地排序入口
    
    修改原数组，不返回新数组
    """
    _merge_sort_inplace_helper(arr, 0, len(arr) - 1)


def _merge_sort_inplace_helper(arr: list[int], left: int, right: int) -> None:
    """原地归并排序辅助函数"""
    if left >= right:
        return
    
    mid = (left + right) // 2
    _merge_sort_inplace_helper(arr, left, mid)
    _merge_sort_inplace_helper(arr, mid + 1, right)
    _merge_inplace(arr, left, mid, right)


def _merge_inplace(arr: list[int], left: int, mid: int, right: int) -> None:
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


# ============================================================================
# 3. 迭代实现（自底向上）
# ============================================================================


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


# ============================================================================
# 4. 优化实现
# ============================================================================


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
        return _insertion_sort(arr)
    
    mid = len(arr) // 2
    left = merge_sort_optimized(arr[:mid], threshold)
    right = merge_sort_optimized(arr[mid:], threshold)
    
    # 优化2: 如果已经有序，直接返回
    if left[-1] <= right[0]:
        return left + right
    
    return merge(left, right)


def _insertion_sort(arr: list[int]) -> list[int]:
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


# ============================================================================
# 5. 泛型实现
# ============================================================================


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
    
    Returns:
        排序后的新数组
    
    Example:
        # 按长度排序字符串
        words = ["apple", "pie", "zoo", "elephant"]
        sorted_words = merge_sort_generic(words, key=len)
        # ["zoo", "pie", "apple", "elephant"]
        
        # 按第二个元素排序元组
        pairs = [(1, 5), (3, 2), (2, 8)]
        sorted_pairs = merge_sort_generic(pairs, key=lambda x: x[1])
        # [(3, 2), (1, 5), (2, 8)]
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_generic(arr[:mid], key, reverse)
    right = merge_sort_generic(arr[mid:], key, reverse)
    
    return _merge_generic(left, right, key, reverse)


def _merge_generic(
    left: list[T],
    right: list[T],
    key: Callable[[T], Any] | None,
    reverse: bool
) -> list[T]:
    """泛型合并"""
    result = []
    i = j = 0
    
    # 定义比较函数
    if key is None:
        if reverse:
            compare = lambda a, b: a >= b
        else:
            compare = lambda a, b: a <= b
    else:
        if reverse:
            compare = lambda a, b: key(a) >= key(b)
        else:
            compare = lambda a, b: key(a) <= key(b)
    
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


# ============================================================================
# 实战应用
# ============================================================================


def count_inversions(arr: list[int]) -> tuple[list[int], int]:
    """
    统计逆序对数量
    
    逆序对: (i, j) 满足 i < j 且 arr[i] > arr[j]
    
    Returns:
        (排序后的数组, 逆序对数量)
    
    Example:
        arr = [2, 4, 1, 3, 5]
        sorted_arr, count = count_inversions(arr)
        # sorted_arr = [1, 2, 3, 4, 5], count = 3
        # 逆序对: (2,1), (4,1), (4,3)
    """
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = count_inversions(arr[:mid])
    right, right_inv = count_inversions(arr[mid:])
    
    merged, split_inv = _merge_and_count(left, right)
    
    total_inversions = left_inv + right_inv + split_inv
    return merged, total_inversions


def _merge_and_count(left: list[int], right: list[int]) -> tuple[list[int], int]:
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
            inversions += len(left) - i  # 统计逆序对
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result, inversions


class ListNode:
    """链表节点"""
    def __init__(self, val: int = 0, next: 'ListNode | None' = None):
        self.val = val
        self.next = next


def merge_sort_linked_list(head: ListNode | None) -> ListNode | None:
    """
    链表归并排序
    
    时间复杂度: O(n log n)
    空间复杂度: O(log n) - 只有递归栈
    
    这是链表排序的最佳选择！
    """
    if not head or not head.next:
        return head
    
    # 找到中点（快慢指针）
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
    return _merge_linked_lists(left, right)


def _merge_linked_lists(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
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


# ============================================================================
# 工具函数
# ============================================================================


@dataclass
class SortStats:
    """排序统计信息"""
    algorithm: str
    size: int
    time_ms: float
    comparisons: int
    is_sorted: bool


def benchmark_merge_sort(arr: list[int], algorithm: str = "classic") -> SortStats:
    """
    测试归并排序性能
    
    Args:
        arr: 待排序数组
        algorithm: 算法类型 ("classic", "iterative", "optimized")
    """
    algorithms = {
        "classic": merge_sort,
        "iterative": merge_sort_iterative,
        "optimized": merge_sort_optimized,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    sort_func = algorithms[algorithm]
    
    start = time.perf_counter()
    result = sort_func(arr.copy())
    elapsed = (time.perf_counter() - start) * 1000  # ms
    
    is_sorted = all(result[i] <= result[i+1] for i in range(len(result)-1))
    
    return SortStats(
        algorithm=algorithm,
        size=len(arr),
        time_ms=elapsed,
        comparisons=-1,  # 难以精确统计
        is_sorted=is_sorted
    )


# ============================================================================
# 对外接口
# ============================================================================

__all__ = [
    # 基本实现
    "merge_sort",
    "merge",
    "merge_sort_inplace",
    "merge_sort_iterative",
    "merge_sort_optimized",
    "merge_sort_generic",
    # 应用
    "count_inversions",
    "merge_sort_linked_list",
    "ListNode",
    # 工具
    "benchmark_merge_sort",
    "SortStats",
]


if __name__ == "__main__":
    print("=" * 70)
    print("Merge Sort - 演示")
    print("=" * 70)
    
    # 测试数据
    test_data = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 33, 17, 10, 55, 77]
    
    # 1. 经典递归实现
    print("\n1️⃣  经典递归实现:")
    result = merge_sort(test_data)
    print(f"   原始: {test_data}")
    print(f"   排序: {result}")
    
    # 2. 原地排序
    print("\n2️⃣  原地排序:")
    arr = test_data.copy()
    merge_sort_inplace(arr)
    print(f"   结果: {arr}")
    
    # 3. 迭代实现
    print("\n3️⃣  迭代实现:")
    result = merge_sort_iterative(test_data)
    print(f"   结果: {result}")
    
    # 4. 优化实现
    print("\n4️⃣  优化实现:")
    result = merge_sort_optimized(test_data)
    print(f"   结果: {result}")
    
    # 5. 泛型实现
    print("\n5️⃣  泛型实现:")
    words = ["apple", "pie", "zoo", "elephant", "cat"]
    result = merge_sort_generic(words, key=len)
    print(f"   按长度排序: {result}")
    
    # 6. 逆序对统计
    print("\n6️⃣  逆序对统计:")
    arr = [2, 4, 1, 3, 5]
    sorted_arr, count = count_inversions(arr)
    print(f"   原始: {arr}")
    print(f"   逆序对数量: {count}")
    
    # 7. 性能测试
    print("\n7️⃣  性能测试:")
    import random
    test_arr = [random.randint(1, 1000) for _ in range(1000)]
    
    for algo in ["classic", "iterative", "optimized"]:
        stats = benchmark_merge_sort(test_arr, algo)
        print(f"   {algo:12s}: {stats.time_ms:.3f}ms (正确: {stats.is_sorted})")
    
    print("\n" + "=" * 70)
    print("✅ 所有演示完成！")
    print("=" * 70)
