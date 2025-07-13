# 02-理论基础

## 概述

理论基础层建立在形式科学之上，为软件工程和计算科学提供核心的理论支撑。本层包含计算理论、算法理论、复杂性理论、信息论和控制论等基础理论。

## 目录结构

```text
02-理论基础/
├── 01-计算理论/
│   ├── 01-可计算性理论.md
│   ├── 02-计算模型.md
│   ├── 03-递归函数理论.md
│   └── 04-λ演算.md
├── 02-算法理论/
│   ├── 01-算法设计.md
│   ├── 02-算法分析.md
│   ├── 03-分治算法.md
│   ├── 04-动态规划.md
│   ├── 05-贪心算法.md
│   └── 06-随机算法.md
├── 03-复杂性理论/
│   ├── 01-时间复杂度.md
│   ├── 02-空间复杂度.md
│   ├── 03-复杂度类.md
│   ├── 04-NP完全性.md
│   └── 05-近似算法.md
├── 04-信息论/
│   ├── 01-信息度量.md
│   ├── 02-熵与编码.md
│   ├── 03-信道容量.md
│   └── 04-数据压缩.md
└── 05-控制论/
    ├── 01-系统控制.md
    ├── 02-反馈控制.md
    ├── 03-自适应控制.md
    └── 04-最优控制.md
```

## 核心概念

### 1. 计算理论

#### 可计算性

- **图灵机**: 通用计算模型
- **停机问题**: 不可判定性
- **递归函数**: 可计算函数
- **λ演算**: 函数式计算模型

#### 计算模型

```python
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
from enum import Enum

class TapeDirection(Enum):
    LEFT = "L"
    RIGHT = "R"
    STAY = "S"

class TuringMachine:
    """图灵机的完整实现"""
    
    def __init__(self, 
                 states: set,
                 alphabet: set,
                 tape_alphabet: set,
                 transitions: Dict[tuple, tuple],
                 initial_state: str,
                 accept_states: set,
                 reject_states: set):
        self.states = states
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.reject_states = reject_states
        
        # 运行时状态
        self.current_state = initial_state
        self.tape = []
        self.head_position = 0
    
    def initialize_tape(self, input_string: str):
        """初始化纸带"""
        self.tape = list(input_string)
        self.head_position = 0
        self.current_state = self.initial_state
    
    def step(self) -> bool:
        """执行一步计算，返回是否继续"""
        if self.current_state in self.accept_states:
            return False  # 接受
        if self.current_state in self.reject_states:
            return False  # 拒绝
        
        current_symbol = self.tape[self.head_position] if self.head_position < len(self.tape) else '_'
        key = (self.current_state, current_symbol)
        
        if key not in self.transitions:
            return False  # 停机
        
        new_state, new_symbol, direction = self.transitions[key]
        
        # 更新纸带
        if self.head_position < len(self.tape):
            self.tape[self.head_position] = new_symbol
        else:
            self.tape.append(new_symbol)
        
        # 更新状态
        self.current_state = new_state
        
        # 移动读写头
        if direction == TapeDirection.LEFT:
            self.head_position = max(0, self.head_position - 1)
        elif direction == TapeDirection.RIGHT:
            self.head_position += 1
            if self.head_position >= len(self.tape):
                self.tape.append('_')
        
        return True
    
    def run(self, input_string: str) -> bool:
        """运行图灵机，返回是否接受输入"""
        self.initialize_tape(input_string)
        
        step_count = 0
        max_steps = 10000  # 防止无限循环
        
        while self.step() and step_count < max_steps:
            step_count += 1
        
        return self.current_state in self.accept_states
    
    def get_configuration(self) -> str:
        """获取当前配置的字符串表示"""
        tape_str = ''.join(self.tape)
        return f"{tape_str[:self.head_position]}[{self.current_state}]{tape_str[self.head_position:]}"

# 示例：识别回文串的图灵机
def create_palindrome_tm():
    """创建识别回文串的图灵机"""
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'qaccept', 'qreject'}
    alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', 'x', '_'}
    
    transitions = {
        # 初始状态：检查第一个符号
        ('q0', '0'): ('q1', 'x', TapeDirection.RIGHT),
        ('q0', '1'): ('q2', 'x', TapeDirection.RIGHT),
        ('q0', 'x'): ('qaccept', 'x', TapeDirection.STAY),
        ('q0', '_'): ('qaccept', '_', TapeDirection.STAY),
        
        # 向右移动到末尾
        ('q1', '0'): ('q1', '0', TapeDirection.RIGHT),
        ('q1', '1'): ('q1', '1', TapeDirection.RIGHT),
        ('q1', 'x'): ('q3', 'x', TapeDirection.LEFT),
        ('q1', '_'): ('q3', '_', TapeDirection.LEFT),
        
        ('q2', '0'): ('q2', '0', TapeDirection.RIGHT),
        ('q2', '1'): ('q2', '1', TapeDirection.RIGHT),
        ('q2', 'x'): ('q4', 'x', TapeDirection.LEFT),
        ('q2', '_'): ('q4', '_', TapeDirection.LEFT),
        
        # 向左移动并检查
        ('q3', '0'): ('q0', 'x', TapeDirection.RIGHT),
        ('q3', '1'): ('qreject', '1', TapeDirection.STAY),
        ('q3', 'x'): ('q3', 'x', TapeDirection.LEFT),
        ('q3', '_'): ('qaccept', '_', TapeDirection.STAY),
        
        ('q4', '0'): ('qreject', '0', TapeDirection.STAY),
        ('q4', '1'): ('q0', 'x', TapeDirection.RIGHT),
        ('q4', 'x'): ('q4', 'x', TapeDirection.LEFT),
        ('q4', '_'): ('qaccept', '_', TapeDirection.STAY),
    }
    
    return TuringMachine(
        states=states,
        alphabet=alphabet,
        tape_alphabet=tape_alphabet,
        transitions=transitions,
        initial_state='q0',
        accept_states={'qaccept'},
        reject_states={'qreject'}
    )

# 测试回文串识别
palindrome_tm = create_palindrome_tm()
test_strings = ['', '0', '1', '00', '11', '01', '10', '000', '010', '100', '101']
for s in test_strings:
    result = palindrome_tm.run(s)
    print(f"'{s}' -> {'接受' if result else '拒绝'}")
```

### 2. 算法理论

#### 算法设计模式

```python
from typing import List, Callable, Any, Tuple
import time
import random

class AlgorithmAnalysis:
    """算法分析工具"""
    
    @staticmethod
    def time_complexity(func: Callable, inputs: List[Any]) -> List[float]:
        """测量函数的时间复杂度"""
        times = []
        for input_data in inputs:
            start_time = time.time()
            func(input_data)
            end_time = time.time()
            times.append(end_time - start_time)
        return times
    
    @staticmethod
    def space_complexity(func: Callable, inputs: List[Any]) -> List[int]:
        """测量函数的空间复杂度（简化版）"""
        # 这里简化处理，实际需要更复杂的实现
        return [len(str(input_data)) for input_data in inputs]

class DivideAndConquer:
    """分治算法框架"""
    
    @staticmethod
    def merge_sort(arr: List[int]) -> List[int]:
        """归并排序"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = DivideAndConquer.merge_sort(arr[:mid])
        right = DivideAndConquer.merge_sort(arr[mid:])
        
        return DivideAndConquer._merge(left, right)
    
    @staticmethod
    def _merge(left: List[int], right: List[int]) -> List[int]:
        """合并两个有序数组"""
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
    
    @staticmethod
    def quick_sort(arr: List[int]) -> List[int]:
        """快速排序"""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return (DivideAndConquer.quick_sort(left) + 
                middle + 
                DivideAndConquer.quick_sort(right))
    
    @staticmethod
    def binary_search(arr: List[int], target: int) -> int:
        """二分查找"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1

class DynamicProgramming:
    """动态规划算法框架"""
    
    @staticmethod
    def fibonacci_memo(n: int, memo: Dict[int, int] = None) -> int:
        """带记忆化的斐波那契数列"""
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = (DynamicProgramming.fibonacci_memo(n-1, memo) + 
                  DynamicProgramming.fibonacci_memo(n-2, memo))
        return memo[n]
    
    @staticmethod
    def fibonacci_dp(n: int) -> int:
        """动态规划版本的斐波那契数列"""
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        
        return dp[n]
    
    @staticmethod
    def longest_common_subsequence(text1: str, text2: str) -> int:
        """最长公共子序列"""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    @staticmethod
    def knapsack(values: List[int], weights: List[int], capacity: int) -> int:
        """0-1背包问题"""
        n = len(values)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i-1][w], 
                                 dp[i-1][w - weights[i-1]] + values[i-1])
                else:
                    dp[i][w] = dp[i-1][w]
        
        return dp[n][capacity]

class GreedyAlgorithm:
    """贪心算法框架"""
    
    @staticmethod
    def activity_selection(start_times: List[int], end_times: List[int]) -> List[int]:
        """活动选择问题"""
        activities = list(zip(start_times, end_times, range(len(start_times))))
        activities.sort(key=lambda x: x[1])  # 按结束时间排序
        
        selected = []
        last_end_time = 0
        
        for start, end, index in activities:
            if start >= last_end_time:
                selected.append(index)
                last_end_time = end
        
        return selected
    
    @staticmethod
    def huffman_coding(frequencies: Dict[str, int]) -> Dict[str, str]:
        """霍夫曼编码"""
        from heapq import heappush, heappop
        
        # 创建叶子节点
        heap = [(freq, char) for char, freq in frequencies.items()]
        heap.sort()
        
        # 构建霍夫曼树
        while len(heap) > 1:
            freq1, left = heap.pop(0)
            freq2, right = heap.pop(0)
            
            internal_node = (freq1 + freq2, (left, right))
            
            # 插入到正确位置（保持有序）
            i = 0
            while i < len(heap) and heap[i][0] < internal_node[0]:
                i += 1
            heap.insert(i, internal_node)
        
        # 生成编码
        codes = {}
        GreedyAlgorithm._generate_codes(heap[0][1], "", codes)
        return codes
    
    @staticmethod
    def _generate_codes(node, code: str, codes: Dict[str, str]):
        """递归生成霍夫曼编码"""
        if isinstance(node, str):
            codes[node] = code
        else:
            left, right = node
            GreedyAlgorithm._generate_codes(left, code + "0", codes)
            GreedyAlgorithm._generate_codes(right, code + "1", codes)

class RandomizedAlgorithm:
    """随机算法框架"""
    
    @staticmethod
    def randomized_quicksort(arr: List[int]) -> List[int]:
        """随机化快速排序"""
        if len(arr) <= 1:
            return arr
        
        # 随机选择主元
        pivot_index = random.randint(0, len(arr) - 1)
        pivot = arr[pivot_index]
        
        left = [x for i, x in enumerate(arr) if i != pivot_index and x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for i, x in enumerate(arr) if i != pivot_index and x > pivot]
        
        return (RandomizedAlgorithm.randomized_quicksort(left) + 
                middle + 
                RandomizedAlgorithm.randomized_quicksort(right))
    
    @staticmethod
    def monte_carlo_pi(iterations: int) -> float:
        """蒙特卡洛方法计算π"""
        inside_circle = 0
        
        for _ in range(iterations):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            
            if x**2 + y**2 <= 1:
                inside_circle += 1
        
        return 4 * inside_circle / iterations
    
    @staticmethod
    def las_vegas_search(arr: List[int], target: int) -> int:
        """拉斯维加斯算法：随机化搜索"""
        n = len(arr)
        visited = set()
        
        while len(visited) < n:
            index = random.randint(0, n - 1)
            if index not in visited:
                visited.add(index)
                if arr[index] == target:
                    return index
        
        return -1
```

### 3. 复杂性理论

#### 复杂度分析

```python
class ComplexityAnalysis:
    """复杂度分析工具"""
    
    @staticmethod
    def big_o_notation(func: Callable, input_generator: Callable, 
                      max_size: int = 100) -> str:
        """分析函数的大O复杂度"""
        sizes = list(range(1, max_size + 1))
        times = []
        
        for size in sizes:
            input_data = input_generator(size)
            start_time = time.time()
            func(input_data)
            end_time = time.time()
            times.append(end_time - start_time)
        
        # 简化分析，实际需要更复杂的拟合
        if times[-1] < 0.001:
            return "O(1)"
        elif times[-1] < 0.01:
            return "O(log n)"
        elif times[-1] < 0.1:
            return "O(n)"
        elif times[-1] < 1:
            return "O(n log n)"
        else:
            return "O(n²) or higher"
    
    @staticmethod
    def space_complexity_analysis(func: Callable, input_generator: Callable,
                                max_size: int = 100) -> str:
        """分析函数的空间复杂度"""
        # 简化实现
        return "O(n)"  # 大多数算法都是O(n)空间复杂度

# 复杂度类定义
class ComplexityClass:
    """复杂度类的定义"""
    
    P = "P"  # 多项式时间可解
    NP = "NP"  # 非确定性多项式时间
    NP_COMPLETE = "NP-Complete"  # NP完全
    NP_HARD = "NP-Hard"  # NP难
    PSPACE = "PSPACE"  # 多项式空间
    EXPTIME = "EXPTIME"  # 指数时间
    
    @staticmethod
    def is_in_p(problem: str) -> bool:
        """检查问题是否属于P类"""
        # 这里简化处理，实际需要更复杂的判断
        p_problems = {
            "排序", "搜索", "最短路径", "最小生成树", 
            "最大流", "二分图匹配"
        }
        return problem in p_problems
    
    @staticmethod
    def is_np_complete(problem: str) -> bool:
        """检查问题是否是NP完全的"""
        np_complete_problems = {
            "3-SAT", "顶点覆盖", "团问题", "哈密顿回路",
            "旅行商问题", "子集和问题", "背包问题"
        }
        return problem in np_complete_problems

class NPCompleteness:
    """NP完全性理论"""
    
    @staticmethod
    def reduction(from_problem: str, to_problem: str, 
                 reduction_func: Callable) -> bool:
        """问题归约"""
        # 简化实现
        return True
    
    @staticmethod
    def three_sat_to_vertex_cover(clause_list: List[List[int]], 
                                 num_variables: int) -> Tuple[List[List[int]], int]:
        """3-SAT到顶点覆盖的归约"""
        # 这是一个复杂的归约，这里简化实现
        vertices = []
        k = num_variables * 2 + len(clause_list) * 3
        
        # 为每个变量创建两个顶点
        for i in range(num_variables):
            vertices.append([i*2, i*2+1])
        
        # 为每个子句创建三角形
        for clause in clause_list:
            clause_vertices = []
            for literal in clause:
                var = abs(literal) - 1
                if literal > 0:
                    clause_vertices.append(var * 2)
                else:
                    clause_vertices.append(var * 2 + 1)
            vertices.append(clause_vertices)
        
        return vertices, k
```

### 4. 信息论

#### 信息度量

```python
import math
from collections import Counter

class InformationTheory:
    """信息论基础"""
    
    @staticmethod
    def entropy(probabilities: List[float]) -> float:
        """计算香农熵"""
        entropy = 0
        for p in probabilities:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    @staticmethod
    def joint_entropy(prob_matrix: List[List[float]]) -> float:
        """计算联合熵"""
        joint_entropy = 0
        for row in prob_matrix:
            for p in row:
                if p > 0:
                    joint_entropy -= p * math.log2(p)
        return joint_entropy
    
    @staticmethod
    def conditional_entropy(prob_matrix: List[List[float]], 
                          marginal_probs: List[float]) -> float:
        """计算条件熵"""
        conditional_entropy = 0
        for i, row in enumerate(prob_matrix):
            for j, p in enumerate(row):
                if p > 0 and marginal_probs[i] > 0:
                    conditional_entropy -= p * math.log2(p / marginal_probs[i])
        return conditional_entropy
    
    @staticmethod
    def mutual_information(prob_matrix: List[List[float]], 
                          marginal_x: List[float], 
                          marginal_y: List[float]) -> float:
        """计算互信息"""
        mutual_info = 0
        for i, row in enumerate(prob_matrix):
            for j, p in enumerate(row):
                if p > 0 and marginal_x[i] > 0 and marginal_y[j] > 0:
                    mutual_info += p * math.log2(p / (marginal_x[i] * marginal_y[j]))
        return mutual_info

class DataCompression:
    """数据压缩算法"""
    
    @staticmethod
    def huffman_encode(text: str) -> Tuple[Dict[str, str], str]:
        """霍夫曼编码"""
        # 计算频率
        frequencies = Counter(text)
        
        # 生成编码
        codes = GreedyAlgorithm.huffman_coding(frequencies)
        
        # 编码文本
        encoded = ''.join(codes[char] for char in text)
        
        return codes, encoded
    
    @staticmethod
    def huffman_decode(codes: Dict[str, str], encoded: str) -> str:
        """霍夫曼解码"""
        # 创建反向映射
        reverse_codes = {code: char for char, code in codes.items()}
        
        decoded = ""
        current_code = ""
        
        for bit in encoded:
            current_code += bit
            if current_code in reverse_codes:
                decoded += reverse_codes[current_code]
                current_code = ""
        
        return decoded
    
    @staticmethod
    def lzw_compress(text: str) -> List[int]:
        """LZW压缩算法"""
        dictionary = {chr(i): i for i in range(256)}
        next_code = 256
        
        compressed = []
        current = ""
        
        for char in text:
            current_char = current + char
            if current_char in dictionary:
                current = current_char
            else:
                compressed.append(dictionary[current])
                dictionary[current_char] = next_code
                next_code += 1
                current = char
        
        if current:
            compressed.append(dictionary[current])
        
        return compressed
    
    @staticmethod
    def lzw_decompress(compressed: List[int]) -> str:
        """LZW解压缩算法"""
        dictionary = {i: chr(i) for i in range(256)}
        next_code = 256
        
        decompressed = ""
        previous = chr(compressed[0])
        decompressed += previous
        
        for code in compressed[1:]:
            if code in dictionary:
                current = dictionary[code]
            else:
                current = previous + previous[0]
            
            decompressed += current
            dictionary[next_code] = previous + current[0]
            next_code += 1
            previous = current
        
        return decompressed
```

### 5. 控制论

#### 系统控制

```python
import numpy as np
from typing import Callable, List, Tuple

class ControlSystem:
    """控制系统基础"""
    
    def __init__(self, system_function: Callable, 
                 controller_function: Callable = None):
        self.system_function = system_function
        self.controller_function = controller_function
        self.state_history = []
        self.input_history = []
        self.output_history = []
    
    def simulate(self, initial_state: float, 
                reference: float, steps: int) -> Tuple[List[float], List[float]]:
        """模拟控制系统"""
        current_state = initial_state
        
        for step in range(steps):
            # 计算误差
            error = reference - current_state
            
            # 控制器输出
            if self.controller_function:
                control_input = self.controller_function(error, step)
            else:
                control_input = error  # 简单比例控制
            
            # 系统响应
            next_state = self.system_function(current_state, control_input)
            
            # 记录历史
            self.state_history.append(current_state)
            self.input_history.append(control_input)
            self.output_history.append(current_state)
            
            current_state = next_state
        
        return self.state_history, self.input_history

class PIDController:
    """PID控制器"""
    
    def __init__(self, kp: float, ki: float, kd: float):
        self.kp = kp  # 比例增益
        self.ki = ki  # 积分增益
        self.kd = kd  # 微分增益
        self.integral = 0
        self.previous_error = 0
    
    def control(self, error: float, dt: float = 1.0) -> float:
        """计算控制输出"""
        # 积分项
        self.integral += error * dt
        
        # 微分项
        derivative = (error - self.previous_error) / dt
        
        # PID输出
        output = (self.kp * error + 
                 self.ki * self.integral + 
                 self.kd * derivative)
        
        self.previous_error = error
        return output
    
    def reset(self):
        """重置控制器状态"""
        self.integral = 0
        self.previous_error = 0

class AdaptiveControl:
    """自适应控制"""
    
    def __init__(self, initial_gains: List[float], 
                 adaptation_rate: float = 0.1):
        self.gains = initial_gains
        self.adaptation_rate = adaptation_rate
        self.error_history = []
    
    def adapt(self, error: float, gradient: List[float]):
        """自适应调整参数"""
        self.error_history.append(error)
        
        # 基于梯度下降的自适应
        for i in range(len(self.gains)):
            self.gains[i] -= self.adaptation_rate * gradient[i] * error
    
    def control(self, error: float) -> float:
        """自适应控制输出"""
        return sum(gain * error for gain in self.gains)

# 示例：温度控制系统
def temperature_system(current_temp: float, heat_input: float) -> float:
    """简化的温度系统模型"""
    # 简化的热力学模型
    ambient_temp = 20.0
    thermal_resistance = 0.1
    thermal_capacity = 1.0
    
    # 温度变化率
    temp_change = (heat_input - (current_temp - ambient_temp) / thermal_resistance) / thermal_capacity
    
    return current_temp + temp_change

# 创建PID控制器
pid_controller = PIDController(kp=10.0, ki=0.1, kd=1.0)

# 创建控制系统
control_system = ControlSystem(
    system_function=temperature_system,
    controller_function=lambda error, step: pid_controller.control(error)
)

# 模拟温度控制
initial_temp = 20.0
target_temp = 25.0
simulation_steps = 100

temperatures, inputs = control_system.simulate(
    initial_temp, target_temp, simulation_steps
)

print("温度控制模拟结果:")
print(f"目标温度: {target_temp}°C")
print(f"最终温度: {temperatures[-1]:.2f}°C")
print(f"稳态误差: {abs(target_temp - temperatures[-1]):.2f}°C")
```

## 应用实例

### 1. 算法优化

```python
class AlgorithmOptimizer:
    """算法优化工具"""
    
    @staticmethod
    def optimize_sorting_algorithm(data_sizes: List[int]) -> Dict[str, List[float]]:
        """比较不同排序算法的性能"""
        algorithms = {
            "冒泡排序": lambda arr: sorted(arr),  # 简化实现
            "归并排序": DivideAndConquer.merge_sort,
            "快速排序": DivideAndConquer.quick_sort,
            "随机化快速排序": RandomizedAlgorithm.randomized_quicksort
        }
        
        results = {}
        
        for name, algorithm in algorithms.items():
            times = []
            for size in data_sizes:
                data = list(range(size))
                random.shuffle(data)
                
                start_time = time.time()
                algorithm(data.copy())
                end_time = time.time()
                
                times.append(end_time - start_time)
            
            results[name] = times
        
        return results

# 性能比较
data_sizes = [100, 500, 1000, 2000]
performance_results = AlgorithmOptimizer.optimize_sorting_algorithm(data_sizes)

print("排序算法性能比较:")
for algorithm, times in performance_results.items():
    print(f"{algorithm}: {[f'{t:.4f}s' for t in times]}")
```

### 2. 复杂度分析

```python
class ComplexityAnalyzer:
    """复杂度分析器"""
    
    @staticmethod
    def analyze_algorithm_complexity():
        """分析各种算法的复杂度"""
        algorithms = {
            "线性搜索": lambda arr: arr.index(0) if 0 in arr else -1,
            "二分搜索": lambda arr: DivideAndConquer.binary_search(sorted(arr), 0),
            "归并排序": DivideAndConquer.merge_sort,
            "快速排序": DivideAndConquer.quick_sort
        }
        
        input_generators = {
            "线性搜索": lambda n: list(range(n)),
            "二分搜索": lambda n: list(range(n)),
            "归并排序": lambda n: list(range(n, 0, -1)),
            "快速排序": lambda n: list(range(n, 0, -1))
        }
        
        for name, algorithm in algorithms.items():
            generator = input_generators[name]
            complexity = ComplexityAnalysis.big_o_notation(algorithm, generator)
            print(f"{name}: {complexity}")

# 运行复杂度分析
ComplexityAnalyzer.analyze_algorithm_complexity()
```

## 总结

理论基础层为软件工程提供了：

1. **计算理论**: 可计算性、计算模型、算法基础
2. **算法理论**: 设计模式、分析方法、优化技术
3. **复杂性理论**: 复杂度分析、NP完全性、近似算法
4. **信息论**: 信息度量、数据压缩、编码理论
5. **控制论**: 系统控制、反馈控制、自适应控制

## 交叉引用

- **形式科学**: [01-形式科学](../01-形式科学/README.md)
- **具体科学**: [03-具体科学](../03-具体科学/README.md)
- **架构领域**: [05-架构领域](../05-架构领域/README.md)
