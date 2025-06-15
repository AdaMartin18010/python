# 02-理论基础层

## 概述

理论基础层是计算机科学的核心理论，包括算法理论、数据结构、计算复杂度、编程语言理论、软件工程理论和系统理论。这一层为具体的技术实现提供理论支撑。

## 目录结构

```
02-理论基础/
├── README.md                    # 本文件
├── 01-算法理论/                 # 算法设计与分析
├── 02-数据结构/                 # 数据结构理论
├── 03-计算复杂度/               # 计算复杂度理论
├── 04-编程语言理论/             # 编程语言理论基础
├── 05-软件工程理论/             # 软件工程理论
└── 06-系统理论/                 # 系统理论
```

## 核心理论

### 1. 算法理论 (Algorithm Theory)

**定义**: 算法理论研究算法的设计、分析和优化。

**算法设计范式**:
- **分治法**: 将问题分解为子问题
- **动态规划**: 通过子问题的最优解构造全局最优解
- **贪心算法**: 每步选择局部最优解
- **回溯法**: 通过试错寻找解

**Python实现**:
```python
from typing import List, Any, Callable, Tuple
import time

class AlgorithmTheory:
    """算法理论实现"""
    
    @staticmethod
    def divide_and_conquer(problem: List[Any], solve_small: Callable, 
                          combine: Callable, threshold: int = 1) -> Any:
        """分治法模板"""
        if len(problem) <= threshold:
            return solve_small(problem)
        
        mid = len(problem) // 2
        left = AlgorithmTheory.divide_and_conquer(problem[:mid], solve_small, combine, threshold)
        right = AlgorithmTheory.divide_and_conquer(problem[mid:], solve_small, combine, threshold)
        
        return combine(left, right)
    
    @staticmethod
    def dynamic_programming(problem_size: int, subproblem_solver: Callable) -> List[Any]:
        """动态规划模板"""
        dp = [None] * (problem_size + 1)
        dp[0] = subproblem_solver(0, dp)
        
        for i in range(1, problem_size + 1):
            dp[i] = subproblem_solver(i, dp)
        
        return dp
    
    @staticmethod
    def greedy_algorithm(choices: List[Any], 
                        selection_criteria: Callable,
                        is_feasible: Callable) -> List[Any]:
        """贪心算法模板"""
        solution = []
        remaining_choices = choices.copy()
        
        while remaining_choices:
            best_choice = max(remaining_choices, key=selection_criteria)
            if is_feasible(solution + [best_choice]):
                solution.append(best_choice)
            remaining_choices.remove(best_choice)
        
        return solution
    
    @staticmethod
    def backtracking(problem: List[Any], 
                    is_valid: Callable,
                    is_complete: Callable,
                    get_candidates: Callable) -> List[List[Any]]:
        """回溯法模板"""
        solutions = []
        
        def backtrack(partial_solution: List[Any]):
            if is_complete(partial_solution):
                solutions.append(partial_solution.copy())
                return
            
            for candidate in get_candidates(partial_solution):
                if is_valid(partial_solution + [candidate]):
                    partial_solution.append(candidate)
                    backtrack(partial_solution)
                    partial_solution.pop()
        
        backtrack([])
        return solutions

# 算法理论示例
def algorithm_theory_example():
    """算法理论示例"""
    
    # 分治法：归并排序
    def merge_sort_solve_small(arr):
        return arr
    
    def merge_sort_combine(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    # 动态规划：斐波那契数列
    def fibonacci_solver(n, dp):
        if n <= 1:
            return n
        return dp[n-1] + dp[n-2]
    
    # 贪心算法：活动选择
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10), (8, 11)]
    
    def activity_selection_criteria(activity):
        return activity[1]  # 按结束时间排序
    
    def activity_is_feasible(solution):
        if not solution:
            return True
        last_activity = solution[-1]
        return True  # 简化版本
    
    # 回溯法：N皇后问题
    def n_queens_is_valid(partial_solution):
        if not partial_solution:
            return True
        current_row = len(partial_solution)
        current_col = partial_solution[-1]
        
        for row, col in enumerate(partial_solution[:-1]):
            if col == current_col or abs(row - current_row) == abs(col - current_col):
                return False
        return True
    
    def n_queens_is_complete(partial_solution):
        return len(partial_solution) == 4  # 4皇后问题
    
    def n_queens_get_candidates(partial_solution):
        return [0, 1, 2, 3]
    
    print("算法理论示例:")
    print("=" * 50)
    
    # 测试分治法
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_arr = AlgorithmTheory.divide_and_conquer(arr, merge_sort_solve_small, merge_sort_combine)
    print(f"归并排序: {arr} -> {sorted_arr}")
    
    # 测试动态规划
    fib_dp = AlgorithmTheory.dynamic_programming(10, fibonacci_solver)
    print(f"斐波那契数列: {fib_dp}")
    
    # 测试贪心算法
    selected_activities = AlgorithmTheory.greedy_algorithm(
        activities, activity_selection_criteria, activity_is_feasible
    )
    print(f"活动选择: {selected_activities}")
    
    # 测试回溯法
    n_queens_solutions = AlgorithmTheory.backtracking(
        [], n_queens_is_valid, n_queens_is_complete, n_queens_get_candidates
    )
    print(f"4皇后问题解的数量: {len(n_queens_solutions)}")

if __name__ == "__main__":
    algorithm_theory_example()
```

### 2. 数据结构理论 (Data Structure Theory)

**定义**: 数据结构理论研究数据的组织、存储和访问方式。

**基本数据结构**:
- **线性结构**: 数组、链表、栈、队列
- **树形结构**: 二叉树、B树、红黑树
- **图结构**: 邻接矩阵、邻接表
- **散列结构**: 散列表

**Python实现**:
```python
from typing import Any, Optional, List, Dict
from abc import ABC, abstractmethod

class DataStructure(ABC):
    """数据结构抽象基类"""
    
    @abstractmethod
    def insert(self, key: Any, value: Any) -> None:
        pass
    
    @abstractmethod
    def search(self, key: Any) -> Optional[Any]:
        pass
    
    @abstractmethod
    def delete(self, key: Any) -> bool:
        pass
    
    @abstractmethod
    def size(self) -> int:
        pass

class BinarySearchTree(DataStructure):
    """二叉搜索树"""
    
    class Node:
        def __init__(self, key: Any, value: Any):
            self.key = key
            self.value = value
            self.left: Optional[BinarySearchTree.Node] = None
            self.right: Optional[BinarySearchTree.Node] = None
    
    def __init__(self):
        self.root: Optional[BinarySearchTree.Node] = None
        self._size = 0
    
    def insert(self, key: Any, value: Any) -> None:
        self.root = self._insert_recursive(self.root, key, value)
        self._size += 1
    
    def _insert_recursive(self, node: Optional[Node], key: Any, value: Any) -> Node:
        if node is None:
            return BinarySearchTree.Node(key, value)
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            node.value = value
            self._size -= 1  # 重复键不增加大小
        
        return node
    
    def search(self, key: Any) -> Optional[Any]:
        node = self._search_recursive(self.root, key)
        return node.value if node else None
    
    def _search_recursive(self, node: Optional[Node], key: Any) -> Optional[Node]:
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    
    def delete(self, key: Any) -> bool:
        if self._delete_recursive(self.root, key):
            self._size -= 1
            return True
        return False
    
    def _delete_recursive(self, node: Optional[Node], key: Any) -> Optional[Node]:
        if node is None:
            return None
        
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # 找到要删除的节点
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # 有两个子节点，找到后继节点
                successor = self._find_min(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = self._delete_recursive(node.right, successor.key)
        
        return node
    
    def _find_min(self, node: Node) -> Node:
        while node.left:
            node = node.left
        return node
    
    def size(self) -> int:
        return self._size
    
    def inorder_traversal(self) -> List[Any]:
        """中序遍历"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[Node], result: List[Any]) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

class HashTable(DataStructure):
    """散列表"""
    
    def __init__(self, initial_size: int = 16, load_factor: float = 0.75):
        self.size = initial_size
        self.load_factor = load_factor
        self.table: List[List[tuple]] = [[] for _ in range(initial_size)]
        self._count = 0
    
    def _hash(self, key: Any) -> int:
        return hash(key) % self.size
    
    def insert(self, key: Any, value: Any) -> None:
        if self._count / self.size >= self.load_factor:
            self._resize()
        
        hash_value = self._hash(key)
        bucket = self.table[hash_value]
        
        # 检查是否已存在
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
        self._count += 1
    
    def search(self, key: Any) -> Optional[Any]:
        hash_value = self._hash(key)
        bucket = self.table[hash_value]
        
        for k, v in bucket:
            if k == key:
                return v
        return None
    
    def delete(self, key: Any) -> bool:
        hash_value = self._hash(key)
        bucket = self.table[hash_value]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._count -= 1
                return True
        return False
    
    def size(self) -> int:
        return self._count
    
    def _resize(self) -> None:
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self._count = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

# 数据结构理论示例
def data_structure_theory_example():
    """数据结构理论示例"""
    
    print("数据结构理论示例:")
    print("=" * 50)
    
    # 二叉搜索树示例
    print("二叉搜索树:")
    bst = BinarySearchTree()
    keys = [5, 3, 7, 2, 4, 6, 8]
    
    for key in keys:
        bst.insert(key, f"value_{key}")
    
    print(f"中序遍历: {bst.inorder_traversal()}")
    print(f"搜索键3: {bst.search(3)}")
    print(f"删除键3: {bst.delete(3)}")
    print(f"删除后中序遍历: {bst.inorder_traversal()}")
    
    # 散列表示例
    print("\n散列表:")
    ht = HashTable()
    test_data = [("apple", 1), ("banana", 2), ("cherry", 3), ("apple", 4)]
    
    for key, value in test_data:
        ht.insert(key, value)
    
    print(f"表大小: {ht.size()}")
    print(f"搜索'apple': {ht.search('apple')}")
    print(f"搜索'orange': {ht.search('orange')}")
    print(f"删除'banana': {ht.delete('banana')}")
    print(f"删除后搜索'banana': {ht.search('banana')}")

if __name__ == "__main__":
    data_structure_theory_example()
```

### 3. 计算复杂度理论 (Computational Complexity Theory)

**定义**: 计算复杂度理论研究算法和问题的计算资源需求。

**复杂度类**:
- **P**: 多项式时间可解问题
- **NP**: 非确定性多项式时间可验证问题
- **NP-完全**: NP中最难的问题
- **PSPACE**: 多项式空间可解问题

**Python实现**:
```python
from typing import List, Tuple, Set, Callable
import time
import random

class ComplexityTheory:
    """计算复杂度理论"""
    
    @staticmethod
    def polynomial_time_algorithm(n: int) -> int:
        """多项式时间算法 O(n²)"""
        result = 0
        for i in range(n):
            for j in range(n):
                result += i * j
        return result
    
    @staticmethod
    def exponential_time_algorithm(n: int) -> int:
        """指数时间算法 O(2ⁿ)"""
        if n <= 1:
            return n
        return (ComplexityTheory.exponential_time_algorithm(n-1) + 
                ComplexityTheory.exponential_time_algorithm(n-2))
    
    @staticmethod
    def np_verification_solution(problem_instance: List[int], 
                                certificate: List[int], 
                                verification_function: Callable) -> bool:
        """NP问题验证"""
        return verification_function(problem_instance, certificate)
    
    @staticmethod
    def subset_sum_verification(numbers: List[int], target: int, 
                               subset: List[int]) -> bool:
        """子集和问题验证"""
        return sum(subset) == target and all(x in numbers for x in subset)
    
    @staticmethod
    def measure_complexity(algorithm: Callable, inputs: List[int]) -> List[float]:
        """测量算法复杂度"""
        times = []
        for n in inputs:
            start_time = time.time()
            algorithm(n)
            end_time = time.time()
            times.append(end_time - start_time)
        return times
    
    @staticmethod
    def analyze_complexity(input_sizes: List[int], execution_times: List[float]) -> str:
        """分析复杂度类型"""
        if len(input_sizes) < 2:
            return "数据不足"
        
        # 计算增长率
        ratios = []
        for i in range(1, len(input_sizes)):
            time_ratio = execution_times[i] / execution_times[i-1]
            size_ratio = input_sizes[i] / input_sizes[i-1]
            ratios.append(time_ratio / size_ratio)
        
        avg_ratio = sum(ratios) / len(ratios)
        
        if avg_ratio < 0.1:
            return "O(1) - 常数时间"
        elif avg_ratio < 0.5:
            return "O(log n) - 对数时间"
        elif avg_ratio < 2:
            return "O(n) - 线性时间"
        elif avg_ratio < 5:
            return "O(n log n) - 线性对数时间"
        elif avg_ratio < 10:
            return "O(n²) - 多项式时间"
        else:
            return "O(2ⁿ) - 指数时间"

# 计算复杂度理论示例
def complexity_theory_example():
    """计算复杂度理论示例"""
    
    print("计算复杂度理论示例:")
    print("=" * 50)
    
    # 测量多项式时间算法
    print("多项式时间算法 (O(n²)):")
    poly_inputs = [10, 20, 40, 80]
    poly_times = ComplexityTheory.measure_complexity(
        ComplexityTheory.polynomial_time_algorithm, poly_inputs
    )
    
    for n, t in zip(poly_inputs, poly_times):
        print(f"  输入规模 {n}: {t:.6f} 秒")
    
    poly_complexity = ComplexityTheory.analyze_complexity(poly_inputs, poly_times)
    print(f"  复杂度分析: {poly_complexity}")
    
    # NP问题验证示例
    print("\nNP问题验证 (子集和问题):")
    numbers = [1, 2, 3, 4, 5]
    target = 7
    
    # 正确的证书
    correct_certificate = [2, 5]
    is_correct = ComplexityTheory.subset_sum_verification(numbers, target, correct_certificate)
    print(f"  证书 {correct_certificate} 验证结果: {is_correct}")
    
    # 错误的证书
    wrong_certificate = [1, 2, 3]
    is_wrong = ComplexityTheory.subset_sum_verification(numbers, target, wrong_certificate)
    print(f"  证书 {wrong_certificate} 验证结果: {is_wrong}")
    
    # 指数时间算法（小规模测试）
    print("\n指数时间算法 (O(2ⁿ)):")
    exp_inputs = [10, 15, 20, 25]
    exp_times = ComplexityTheory.measure_complexity(
        ComplexityTheory.exponential_time_algorithm, exp_inputs
    )
    
    for n, t in zip(exp_inputs, exp_times):
        print(f"  输入规模 {n}: {t:.6f} 秒")
    
    exp_complexity = ComplexityTheory.analyze_complexity(exp_inputs, exp_times)
    print(f"  复杂度分析: {exp_complexity}")

if __name__ == "__main__":
    complexity_theory_example()
```

## 导航链接

- **上级目录**: [../README.md](../README.md)
- **同级目录**: 
  - [00-理念基础/](../00-理念基础/)
  - [01-形式科学/](../01-形式科学/)
  - [03-具体科学/](../03-具体科学/)
  - [04-行业领域/](../04-行业领域/)
  - [05-架构领域/](../05-架构领域/)
  - [06-组件算法/](../06-组件算法/)
  - [07-实践应用/](../07-实践应用/)
  - [08-项目进度/](../08-项目进度/)
- **下级目录**:
  - [01-算法理论/](01-算法理论/)
  - [02-数据结构/](02-数据结构/)
  - [03-计算复杂度/](03-计算复杂度/)
  - [04-编程语言理论/](04-编程语言理论/)
  - [05-软件工程理论/](05-软件工程理论/)
  - [06-系统理论/](06-系统理论/)

## 参考文献

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms. MIT Press.
2. Aho, A. V., Hopcroft, J. E., & Ullman, J. D. (1974). The Design and Analysis of Computer Algorithms. Addison-Wesley.
3. Sipser, M. (2012). Introduction to the Theory of Computation. Cengage Learning.
4. Pierce, B. C. (2002). Types and Programming Languages. MIT Press.
5. Sommerville, I. (2011). Software Engineering. Pearson Education.
6. Bertsekas, D. P., & Tsitsiklis, J. N. (2002). Introduction to Probability. Athena Scientific.
