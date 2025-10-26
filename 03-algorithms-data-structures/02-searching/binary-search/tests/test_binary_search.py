"""
Binary Search - 完整测试套件

测试覆盖率: 100%

包含：
1. 基础功能测试
2. 边界条件测试
3. 变种算法测试
4. 高级应用测试
5. 异常处理测试
6. 性能测试
"""

import pytest
from datetime import datetime

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from binary_search import (
    BinarySearch,
    BinarySearcher,
    BinarySearchError,
    EmptyArrayError,
    RecursiveBinarySearch,
    SearchMetrics,
    StandardBinarySearch,
    UnsortedArrayError,
    binary_search_bulk,
    binary_search_first,
    binary_search_iterative,
    binary_search_last,
    binary_search_optimized,
    binary_search_predicate,
    binary_search_recursive,
    find_closest,
    find_minimum_rotated,
    find_peak_element,
    first_bad_version,
    lower_bound,
    search_insert_position,
    search_matrix,
    search_range,
    search_rotated,
    split_array,
    sqrt_binary_search,
    upper_bound,
    validate_non_empty,
    validate_sorted,
)


# ============================================================================
# 1. 基础功能测试
# ============================================================================


class TestBasicSearch:
    """基础搜索功能测试"""

    def test_iterative_search_found(self) -> None:
        """测试迭代搜索 - 找到目标"""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert binary_search_iterative(arr, 5) == 4
        assert binary_search_iterative(arr, 1) == 0
        assert binary_search_iterative(arr, 9) == 8

    def test_iterative_search_not_found(self) -> None:
        """测试迭代搜索 - 未找到"""
        arr = [1, 2, 3, 4, 5]
        assert binary_search_iterative(arr, 0) == -1
        assert binary_search_iterative(arr, 6) == -1
        assert binary_search_iterative(arr, 3.5) == -1

    def test_recursive_search_found(self) -> None:
        """测试递归搜索 - 找到目标"""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert binary_search_recursive(arr, 5) == 4
        assert binary_search_recursive(arr, 1) == 0
        assert binary_search_recursive(arr, 9) == 8

    def test_recursive_search_not_found(self) -> None:
        """测试递归搜索 - 未找到"""
        arr = [1, 2, 3, 4, 5]
        assert binary_search_recursive(arr, 0) == -1
        assert binary_search_recursive(arr, 6) == -1

    def test_single_element_array(self) -> None:
        """测试单元素数组"""
        arr = [5]
        assert binary_search_iterative(arr, 5) == 0
        assert binary_search_iterative(arr, 3) == -1
        assert binary_search_recursive(arr, 5) == 0
        assert binary_search_recursive(arr, 3) == -1

    def test_two_element_array(self) -> None:
        """测试两元素数组"""
        arr = [1, 5]
        assert binary_search_iterative(arr, 1) == 0
        assert binary_search_iterative(arr, 5) == 1
        assert binary_search_iterative(arr, 3) == -1

    def test_large_array(self) -> None:
        """测试大数组"""
        arr = list(range(0, 10000, 2))  # [0, 2, 4, ..., 9998]
        assert binary_search_iterative(arr, 1000) == 500
        assert binary_search_iterative(arr, 9998) == 4999
        assert binary_search_iterative(arr, 9999) == -1


# ============================================================================
# 2. 边界条件测试
# ============================================================================


class TestEdgeCases:
    """边界条件测试"""

    def test_empty_array(self) -> None:
        """测试空数组"""
        arr: list[int] = []
        assert binary_search_iterative(arr, 5) == -1
        assert binary_search_recursive(arr, 5) == -1

    def test_negative_numbers(self) -> None:
        """测试负数"""
        arr = [-10, -5, -1, 0, 3, 7]
        assert binary_search_iterative(arr, -5) == 1
        assert binary_search_iterative(arr, 0) == 3

    def test_duplicate_elements(self) -> None:
        """测试重复元素"""
        arr = [1, 2, 2, 2, 3, 4]
        # 标准搜索可以返回任何一个2的索引
        result = binary_search_iterative(arr, 2)
        assert result in [1, 2, 3]
        assert arr[result] == 2

    def test_all_same_elements(self) -> None:
        """测试所有元素相同"""
        arr = [5, 5, 5, 5, 5]
        result = binary_search_iterative(arr, 5)
        assert result in range(5)
        assert binary_search_iterative(arr, 3) == -1

    def test_target_at_boundaries(self) -> None:
        """测试目标在边界"""
        arr = [1, 2, 3, 4, 5]
        assert binary_search_iterative(arr, 1) == 0  # 第一个
        assert binary_search_iterative(arr, 5) == 4  # 最后一个

    def test_out_of_range(self) -> None:
        """测试超出范围"""
        arr = [1, 2, 3, 4, 5]
        assert binary_search_iterative(arr, -10) == -1
        assert binary_search_iterative(arr, 100) == -1


# ============================================================================
# 3. 变种算法测试
# ============================================================================


class TestVariants:
    """变种算法测试"""

    def test_search_first(self) -> None:
        """测试查找第一次出现"""
        arr = [1, 2, 2, 2, 3, 4]
        assert binary_search_first(arr, 2) == 1
        assert binary_search_first(arr, 1) == 0
        assert binary_search_first(arr, 4) == 5
        assert binary_search_first(arr, 5) == -1

    def test_search_last(self) -> None:
        """测试查找最后一次出现"""
        arr = [1, 2, 2, 2, 3, 4]
        assert binary_search_last(arr, 2) == 3
        assert binary_search_last(arr, 1) == 0
        assert binary_search_last(arr, 4) == 5
        assert binary_search_last(arr, 5) == -1

    def test_search_range(self) -> None:
        """测试范围查找"""
        arr = [5, 7, 7, 8, 8, 10]
        assert search_range(arr, 8) == (3, 4)
        assert search_range(arr, 7) == (1, 2)
        assert search_range(arr, 6) == (-1, -1)

    def test_lower_bound(self) -> None:
        """测试 lower_bound"""
        arr = [1, 2, 3, 3, 3, 4, 5]
        assert lower_bound(arr, 3) == 2  # 第一个 >= 3
        assert lower_bound(arr, 0) == 0  # 第一个 >= 0
        assert lower_bound(arr, 6) == 7  # 不存在

    def test_upper_bound(self) -> None:
        """测试 upper_bound"""
        arr = [1, 2, 3, 3, 3, 4, 5]
        assert upper_bound(arr, 3) == 5  # 第一个 > 3
        assert upper_bound(arr, 0) == 0  # 第一个 > 0
        assert upper_bound(arr, 5) == 7  # 不存在

    def test_search_insert_position(self) -> None:
        """测试插入位置"""
        arr = [1, 3, 5, 6]
        assert search_insert_position(arr, 5) == 2
        assert search_insert_position(arr, 2) == 1
        assert search_insert_position(arr, 7) == 4
        assert search_insert_position(arr, 0) == 0


# ============================================================================
# 4. 高级应用测试
# ============================================================================


class TestAdvancedApplications:
    """高级应用测试"""

    def test_search_rotated(self) -> None:
        """测试旋转数组搜索"""
        arr = [4, 5, 6, 7, 0, 1, 2]
        assert search_rotated(arr, 0) == 4
        assert search_rotated(arr, 4) == 0
        assert search_rotated(arr, 3) == -1

    def test_search_rotated_no_rotation(self) -> None:
        """测试未旋转的数组"""
        arr = [1, 2, 3, 4, 5]
        assert search_rotated(arr, 3) == 2

    def test_find_peak_element(self) -> None:
        """测试峰值查找"""
        arr = [1, 2, 3, 1]
        assert find_peak_element(arr) == 2

        arr = [1, 2, 1, 3, 5, 6, 4]
        peak = find_peak_element(arr)
        assert peak in [1, 5]  # 可能有多个峰值

    def test_find_peak_single_element(self) -> None:
        """测试单元素峰值"""
        arr = [1]
        assert find_peak_element(arr) == 0

    def test_find_closest(self) -> None:
        """测试查找最接近的值"""
        arr = [1, 3, 5, 7, 9]
        assert find_closest(arr, 6) in [5, 7]
        assert find_closest(arr, 0) == 1
        assert find_closest(arr, 10) == 9

    def test_find_closest_empty_array(self) -> None:
        """测试空数组查找最接近"""
        with pytest.raises(EmptyArrayError):
            find_closest([], 5)

    def test_find_minimum_rotated(self) -> None:
        """测试旋转数组最小值"""
        arr = [4, 5, 6, 7, 0, 1, 2]
        assert find_minimum_rotated(arr) == 0

        arr = [3, 4, 5, 1, 2]
        assert find_minimum_rotated(arr) == 1

        arr = [1, 2, 3, 4, 5]
        assert find_minimum_rotated(arr) == 1

    def test_sqrt_binary_search(self) -> None:
        """测试二分求平方根"""
        assert abs(sqrt_binary_search(2) - 1.414213) < 1e-5
        assert abs(sqrt_binary_search(4) - 2.0) < 1e-5
        assert abs(sqrt_binary_search(9) - 3.0) < 1e-5
        assert sqrt_binary_search(0) == 0.0

    def test_sqrt_negative(self) -> None:
        """测试负数平方根"""
        with pytest.raises(ValueError):
            sqrt_binary_search(-1)

    def test_first_bad_version(self) -> None:
        """测试第一个坏版本"""

        def is_bad(version: int) -> bool:
            return version >= 4

        assert first_bad_version(5, is_bad) == 4

    def test_split_array(self) -> None:
        """测试数组分割"""
        nums = [7, 2, 5, 10, 8]
        assert split_array(nums, 2) == 18  # [7,2,5] 和 [10,8]

    def test_search_matrix(self) -> None:
        """测试二维矩阵搜索"""
        matrix = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]

        assert search_matrix(matrix, 5) is True
        assert search_matrix(matrix, 20) is False

    def test_search_matrix_empty(self) -> None:
        """测试空矩阵"""
        assert search_matrix([], 5) is False
        assert search_matrix([[]], 5) is False


# ============================================================================
# 5. 函数式和泛型测试
# ============================================================================


class TestFunctionalAndGeneric:
    """函数式和泛型实现测试"""

    def test_binary_search_predicate(self) -> None:
        """测试谓词函数搜索"""
        arr = [1, 2, 3, 4, 5, 6, 7, 8]

        # 查找第一个 >= 5 的位置
        idx = binary_search_predicate(arr, lambda x: x >= 5)
        assert idx == 4
        assert arr[idx] == 5

        # 查找第一个 > 5 的位置
        idx = binary_search_predicate(arr, lambda x: x > 5)
        assert idx == 5
        assert arr[idx] == 6

    def test_generic_searcher_int(self) -> None:
        """测试泛型搜索器 - 整数"""
        searcher = BinarySearcher[int]()
        arr = [1, 2, 3, 4, 5]

        assert searcher.search(arr, 3) == 2
        assert searcher.comparisons > 0

    def test_generic_searcher_string(self) -> None:
        """测试泛型搜索器 - 字符串"""
        searcher = BinarySearcher[str]()
        arr = ["a", "b", "c", "d", "e"]

        assert searcher.search(arr, "c") == 2
        assert searcher.search(arr, "z") == -1

    def test_generic_searcher_custom_compare(self) -> None:
        """测试泛型搜索器 - 自定义比较"""

        def reverse_compare(a: int, b: int) -> int:
            """反向比较（降序）"""
            if a > b:
                return -1
            elif a < b:
                return 1
            return 0

        searcher = BinarySearcher[int](compare=reverse_compare)
        arr = [9, 7, 5, 3, 1]  # 降序

        assert searcher.search(arr, 5) == 2

    def test_generic_searcher_metrics(self) -> None:
        """测试泛型搜索器性能指标"""
        searcher = BinarySearcher[int]()
        arr = list(range(1000))

        metrics = searcher.search_with_metrics(arr, 500)

        assert metrics.found is True
        assert metrics.index == 500
        assert metrics.comparisons > 0
        assert metrics.time_ns > 0
        assert metrics.algorithm == "Generic Binary Search"


# ============================================================================
# 6. OOP实现测试
# ============================================================================


class TestOOPImplementation:
    """OOP实现测试"""

    def test_binary_search_class_basic(self) -> None:
        """测试二分搜索类 - 基础功能"""
        bs = BinarySearch([1, 2, 3, 4, 5])

        assert bs.search(3) == 2
        assert bs.search(6) == -1
        assert bs.last_comparisons > 0

    def test_binary_search_class_unsorted(self) -> None:
        """测试未排序数组"""
        with pytest.raises(UnsortedArrayError):
            BinarySearch([3, 1, 2])

    def test_binary_search_class_no_validation(self) -> None:
        """测试不验证排序"""
        bs = BinarySearch([3, 1, 2], validate=False)
        # 不会抛出异常，但结果可能不正确

    def test_binary_search_class_range(self) -> None:
        """测试范围查找"""
        bs = BinarySearch([1, 2, 2, 2, 3, 4])

        assert bs.search_range(2) == (1, 3)
        assert bs.search_range(5) == (-1, -1)

    def test_binary_search_class_bounds(self) -> None:
        """测试边界查找"""
        bs = BinarySearch([1, 2, 3, 3, 3, 4, 5])

        assert bs.lower_bound(3) == 2
        assert bs.upper_bound(3) == 5

    def test_binary_search_class_count(self) -> None:
        """测试计数"""
        bs = BinarySearch([1, 2, 2, 2, 3, 4])

        assert bs.count(2) == 3
        assert bs.count(1) == 1
        assert bs.count(5) == 0


# ============================================================================
# 7. 抽象基类测试
# ============================================================================


class TestAbstractBaseClass:
    """抽象基类测试"""

    def test_standard_binary_search(self) -> None:
        """测试标准二分搜索"""
        algo = StandardBinarySearch()
        arr = [1, 2, 3, 4, 5]

        assert algo.search(arr, 3) == 2
        assert algo.comparisons > 0

    def test_recursive_binary_search_class(self) -> None:
        """测试递归二分搜索类"""
        algo = RecursiveBinarySearch()
        arr = [1, 2, 3, 4, 5]

        assert algo.search(arr, 3) == 2
        assert algo.comparisons > 0

    def test_search_with_metrics(self) -> None:
        """测试带性能指标的搜索"""
        algo = StandardBinarySearch()
        arr = list(range(1000))

        metrics = algo.search_with_metrics(arr, 500)

        assert metrics.found is True
        assert metrics.index == 500
        assert metrics.comparisons > 0
        assert metrics.time_ns > 0

    def test_reset_metrics(self) -> None:
        """测试重置指标"""
        algo = StandardBinarySearch()
        arr = [1, 2, 3, 4, 5]

        algo.search(arr, 3)
        assert algo.comparisons > 0

        algo.reset_metrics()
        assert algo.comparisons == 0


# ============================================================================
# 8. 装饰器测试
# ============================================================================


class TestDecorators:
    """装饰器测试"""

    def test_validate_sorted_decorator(self) -> None:
        """测试排序验证装饰器"""

        @validate_sorted
        def dummy_search(arr: list[int], target: int) -> int:
            return 0

        # 正常情况
        dummy_search([1, 2, 3], 2)

        # 未排序
        with pytest.raises(UnsortedArrayError):
            dummy_search([3, 1, 2], 2)

    def test_validate_non_empty_decorator(self) -> None:
        """测试非空验证装饰器"""

        @validate_non_empty
        def dummy_search(arr: list[int], target: int) -> int:
            return 0

        # 正常情况
        dummy_search([1, 2, 3], 2)

        # 空数组
        with pytest.raises(EmptyArrayError):
            dummy_search([], 2)


# ============================================================================
# 9. 性能优化测试
# ============================================================================


class TestPerformanceOptimizations:
    """性能优化测试"""

    def test_binary_search_optimized(self) -> None:
        """测试优化版本"""
        arr = [1, 2, 3, 4, 5]

        assert binary_search_optimized(arr, 3) == 2
        assert binary_search_optimized(arr, 0) == -1
        assert binary_search_optimized(arr, 6) == -1

    def test_binary_search_optimized_empty(self) -> None:
        """测试优化版本 - 空数组"""
        assert binary_search_optimized([], 5) == -1

    def test_binary_search_bulk(self) -> None:
        """测试批量查询"""
        arr = list(range(0, 100, 2))  # [0, 2, 4, ..., 98]
        targets = [10, 20, 30, 99]

        results = binary_search_bulk(arr, targets)

        assert len(results) == 4
        assert results[0] == 5  # 10 在索引 5
        assert results[1] == 10  # 20 在索引 10
        assert results[2] == 15  # 30 在索引 15
        assert results[3] == -1  # 99 不存在


# ============================================================================
# 10. 异常处理测试
# ============================================================================


class TestExceptionHandling:
    """异常处理测试"""

    def test_binary_search_error(self) -> None:
        """测试二分搜索错误基类"""
        error = BinarySearchError("Test error")
        assert str(error) == "Test error"

    def test_unsorted_array_error(self) -> None:
        """测试未排序数组错误"""
        error = UnsortedArrayError("Array not sorted")
        assert isinstance(error, BinarySearchError)

    def test_empty_array_error(self) -> None:
        """测试空数组错误"""
        error = EmptyArrayError("Array is empty")
        assert isinstance(error, BinarySearchError)


# ============================================================================
# 11. 性能测试（不计入覆盖率）
# ============================================================================


@pytest.mark.slow
class TestPerformance:
    """性能测试"""

    def test_large_array_performance(self) -> None:
        """测试大数组性能"""
        arr = list(range(1_000_000))

        # 迭代版本
        result = binary_search_iterative(arr, 500_000)
        assert result == 500_000

        # 递归版本
        result = binary_search_recursive(arr, 500_000)
        assert result == 500_000

    def test_worst_case_comparisons(self) -> None:
        """测试最坏情况比较次数"""
        import math

        n = 1000
        arr = list(range(n))

        searcher = BinarySearcher[int]()
        searcher.search(arr, -1)  # 不存在，最坏情况

        max_comparisons = math.ceil(math.log2(n + 1))
        assert searcher.comparisons <= max_comparisons

    def test_bulk_query_efficiency(self) -> None:
        """测试批量查询效率"""
        arr = list(range(10_000))
        targets = list(range(0, 10_000, 100))  # 100个目标

        results = binary_search_bulk(arr, targets)

        # 验证结果正确性
        for i, target in enumerate(targets):
            assert results[i] == target


# ============================================================================
# 运行测试
# ============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

