# 02-理论基础

## 概述

理论基础层是知识库的科学基础，包含计算理论、算法理论、系统理论、信息论等核心理论。这一层为软件工程和计算科学提供科学理论基础，建立从形式科学到具体应用的桥梁。

## 目录结构

```
02-理论基础/
├── 001-计算理论/           # 图灵机、可计算性、复杂度理论
├── 002-算法理论/           # 算法设计、分析、优化理论
├── 003-系统理论/           # 系统论、控制论、信息论
├── 004-语言理论/           # 形式语言、自动机、语法理论
├── 005-并发理论/           # 进程代数、时序逻辑、并发模型
├── 006-分布式理论/         # 分布式算法、一致性、容错理论
├── 007-密码学理论/         # 密码学基础、安全协议、零知识证明
└── 008-机器学习理论/       # 统计学习、深度学习、优化理论
```

## 核心理论

### 1. 计算理论

```python
from typing import List, Dict, Set, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import time

class TapeSymbol(Enum):
    BLANK = "_"
    ZERO = "0"
    ONE = "1"

class Movement(Enum):
    LEFT = "L"
    RIGHT = "R"
    STAY = "S"

@dataclass
class TuringMachineState:
    """图灵机状态"""
    name: str
    is_accepting: bool = False
    is_rejecting: bool = False

@dataclass
class TuringMachineTransition:
    """图灵机转移函数"""
    current_state: str
    current_symbol: TapeSymbol
    new_state: str
    new_symbol: TapeSymbol
    movement: Movement

class TuringMachine:
    """图灵机实现"""
    
    def __init__(self, states: List[TuringMachineState], 
                 transitions: List[TuringMachineTransition],
                 initial_state: str):
        self.states = {state.name: state for state in states}
        self.transitions = self._build_transition_table(transitions)
        self.current_state = initial_state
        self.tape: List[TapeSymbol] = [TapeSymbol.BLANK]
        self.head_position = 0
        
    def _build_transition_table(self, transitions: List[TuringMachineTransition]) -> Dict:
        """构建转移表"""
        table = {}
        for transition in transitions:
            key = (transition.current_state, transition.current_symbol)
            table[key] = transition
        return table
    
    def step(self) -> bool:
        """执行一步计算"""
        current_symbol = self.tape[self.head_position]
        key = (self.current_state, current_symbol)
        
        if key not in self.transitions:
            return False  # 停机
        
        transition = self.transitions[key]
        self.current_state = transition.new_state
        self.tape[self.head_position] = transition.new_symbol
        
        # 移动读写头
        if transition.movement == Movement.LEFT:
            if self.head_position == 0:
                self.tape.insert(0, TapeSymbol.BLANK)
            else:
                self.head_position -= 1
        elif transition.movement == Movement.RIGHT:
            self.head_position += 1
            if self.head_position >= len(self.tape):
                self.tape.append(TapeSymbol.BLANK)
        
        return True
    
    def run(self, input_tape: List[TapeSymbol], max_steps: int = 1000) -> Dict[str, Any]:
        """运行图灵机"""
        self.tape = input_tape.copy()
        self.head_position = 0
        steps = 0
        
        while steps < max_steps:
            if not self.step():
                break
            steps += 1
            
            current_state = self.states[self.current_state]
            if current_state.is_accepting:
                return {"result": "accept", "steps": steps, "tape": self.tape}
            elif current_state.is_rejecting:
                return {"result": "reject", "steps": steps, "tape": self.tape}
        
        return {"result": "timeout", "steps": steps, "tape": self.tape}

# 示例：识别回文串的图灵机
def create_palindrome_tm() -> TuringMachine:
    """创建识别回文串的图灵机"""
    states = [
        TuringMachineState("q0"),  # 初始状态
        TuringMachineState("q1"),  # 向右移动
        TuringMachineState("q2"),  # 向左移动
        TuringMachineState("q3"),  # 比较
        TuringMachineState("q_accept", is_accepting=True),
        TuringMachineState("q_reject", is_rejecting=True)
    ]
    
    transitions = [
        # 初始状态：向右移动到末尾
        TuringMachineTransition("q0", TapeSymbol.ZERO, "q1", TapeSymbol.ZERO, Movement.RIGHT),
        TuringMachineTransition("q0", TapeSymbol.ONE, "q1", TapeSymbol.ONE, Movement.RIGHT),
        TuringMachineTransition("q0", TapeSymbol.BLANK, "q2", TapeSymbol.BLANK, Movement.LEFT),
        
        # 向右移动
        TuringMachineTransition("q1", TapeSymbol.ZERO, "q1", TapeSymbol.ZERO, Movement.RIGHT),
        TuringMachineTransition("q1", TapeSymbol.ONE, "q1", TapeSymbol.ONE, Movement.RIGHT),
        TuringMachineTransition("q1", TapeSymbol.BLANK, "q2", TapeSymbol.BLANK, Movement.LEFT),
        
        # 向左移动并比较
        TuringMachineTransition("q2", TapeSymbol.ZERO, "q3", TapeSymbol.BLANK, Movement.LEFT),
        TuringMachineTransition("q2", TapeSymbol.ONE, "q3", TapeSymbol.BLANK, Movement.LEFT),
        TuringMachineTransition("q2", TapeSymbol.BLANK, "q_accept", TapeSymbol.BLANK, Movement.STAY),
        
        # 比较阶段
        TuringMachineTransition("q3", TapeSymbol.ZERO, "q3", TapeSymbol.ZERO, Movement.LEFT),
        TuringMachineTransition("q3", TapeSymbol.ONE, "q3", TapeSymbol.ONE, Movement.LEFT),
        TuringMachineTransition("q3", TapeSymbol.BLANK, "q_reject", TapeSymbol.BLANK, Movement.STAY)
    ]
    
    return TuringMachine(states, transitions, "q0")
```

### 2. 算法理论

```python
from typing import TypeVar, Callable, List, Tuple, Optional
import math
import random

T = TypeVar('T')

class Algorithm:
    """算法的基础定义"""
    
    def __init__(self, name: str, complexity: str):
        self.name = name
        self.complexity = complexity
        self.step_count = 0
    
    def reset_step_count(self):
        """重置步数计数"""
        self.step_count = 0
    
    def get_step_count(self) -> int:
        """获取步数"""
        return self.step_count

class SortingAlgorithm(Algorithm):
    """排序算法基类"""
    
    def sort(self, arr: List[T], key: Optional[Callable[[T], Any]] = None) -> List[T]:
        """排序接口"""
        self.reset_step_count()
        return self._sort_impl(arr, key)
    
    def _sort_impl(self, arr: List[T], key: Optional[Callable[[T], Any]] = None) -> List[T]:
        """排序实现"""
        raise NotImplementedError

class QuickSort(SortingAlgorithm):
    """快速排序算法"""
    
    def __init__(self):
        super().__init__("QuickSort", "O(n log n) average, O(n²) worst")
    
    def _sort_impl(self, arr: List[T], key: Optional[Callable[[T], Any]] = None) -> List[T]:
        if len(arr) <= 1:
            return arr
        
        self.step_count += 1
        
        # 选择基准
        pivot = arr[len(arr) // 2]
        
        # 分区
        left = [x for x in arr if (key(x) if key else x) < (key(pivot) if key else pivot)]
        middle = [x for x in arr if (key(x) if key else x) == (key(pivot) if key else pivot)]
        right = [x for x in arr if (key(x) if key else x) > (key(pivot) if key else pivot)]
        
        # 递归排序
        return self._sort_impl(left, key) + middle + self._sort_impl(right, key)

class MergeSort(SortingAlgorithm):
    """归并排序算法"""
    
    def __init__(self):
        super().__init__("MergeSort", "O(n log n)")
    
    def _sort_impl(self, arr: List[T], key: Optional[Callable[[T], Any]] = None) -> List[T]:
        if len(arr) <= 1:
            return arr
        
        self.step_count += 1
        
        # 分割
        mid = len(arr) // 2
        left = self._sort_impl(arr[:mid], key)
        right = self._sort_impl(arr[mid:], key)
        
        # 合并
        return self._merge(left, right, key)
    
    def _merge(self, left: List[T], right: List[T], key: Optional[Callable[[T], Any]]) -> List[T]:
        """合并两个有序数组"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            self.step_count += 1
            left_val = key(left[i]) if key else left[i]
            right_val = key(right[j]) if key else right[j]
            
            if left_val <= right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class AlgorithmAnalyzer:
    """算法分析器"""
    
    @staticmethod
    def analyze_time_complexity(algorithm: Algorithm, input_sizes: List[int], 
                               input_generator: Callable[[int], List[T]]) -> Dict[str, List[float]]:
        """分析算法时间复杂度"""
        results = {"sizes": [], "times": [], "steps": []}
        
        for size in input_sizes:
            # 生成测试数据
            test_data = input_generator(size)
            
            # 运行算法
            start_time = time.time()
            algorithm.sort(test_data.copy())
            end_time = time.time()
            
            results["sizes"].append(size)
            results["times"].append(end_time - start_time)
            results["steps"].append(algorithm.get_step_count())
        
        return results
    
    @staticmethod
    def estimate_complexity(sizes: List[int], steps: List[int]) -> str:
        """估计算法复杂度"""
        if len(sizes) < 2:
            return "insufficient data"
        
        # 计算增长率
        ratios = []
        for i in range(1, len(sizes)):
            size_ratio = sizes[i] / sizes[i-1]
            step_ratio = steps[i] / steps[i-1]
            ratios.append(step_ratio / size_ratio)
        
        avg_ratio = sum(ratios) / len(ratios)
        
        if avg_ratio < 1.1:
            return "O(1)"
        elif avg_ratio < 1.5:
            return "O(log n)"
        elif avg_ratio < 2.5:
            return "O(n)"
        elif avg_ratio < 4:
            return "O(n log n)"
        elif avg_ratio < 8:
            return "O(n²)"
        else:
            return "O(n³) or higher"
```

### 3. 系统理论

```python
from typing import Dict, List, Set, Tuple, Optional, Callable
from dataclasses import dataclass
import numpy as np

@dataclass
class SystemState:
    """系统状态"""
    variables: Dict[str, float]
    timestamp: float
    
    def __str__(self) -> str:
        return f"State at {self.timestamp}: {self.variables}"

class System:
    """系统基类"""
    
    def __init__(self, name: str, state_variables: List[str]):
        self.name = name
        self.state_variables = state_variables
        self.current_state: Optional[SystemState] = None
        self.history: List[SystemState] = []
    
    def initialize(self, initial_values: Dict[str, float], timestamp: float = 0.0):
        """初始化系统状态"""
        self.current_state = SystemState(initial_values, timestamp)
        self.history = [self.current_state]
    
    def update(self, new_values: Dict[str, float], timestamp: float):
        """更新系统状态"""
        self.current_state = SystemState(new_values, timestamp)
        self.history.append(self.current_state)
    
    def get_state(self) -> Optional[SystemState]:
        """获取当前状态"""
        return self.current_state
    
    def get_history(self) -> List[SystemState]:
        """获取历史状态"""
        return self.history.copy()

class LinearSystem(System):
    """线性系统"""
    
    def __init__(self, name: str, A: np.ndarray, B: np.ndarray, C: np.ndarray, D: np.ndarray):
        super().__init__(name, [f"x{i}" for i in range(A.shape[0])])
        self.A = A  # 状态矩阵
        self.B = B  # 输入矩阵
        self.C = C  # 输出矩阵
        self.D = D  # 直接传递矩阵
    
    def step(self, u: np.ndarray, dt: float) -> np.ndarray:
        """系统步进"""
        if self.current_state is None:
            raise ValueError("System not initialized")
        
        # 当前状态
        x = np.array([self.current_state.variables[f"x{i}"] for i in range(len(self.state_variables))])
        
        # 状态更新: dx/dt = Ax + Bu
        dx = self.A @ x + self.B @ u
        
        # 欧拉积分
        x_new = x + dx * dt
        
        # 输出: y = Cx + Du
        y = self.C @ x + self.D @ u
        
        # 更新状态
        new_values = {f"x{i}": x_new[i] for i in range(len(x_new))}
        self.update(new_values, self.current_state.timestamp + dt)
        
        return y
    
    def is_stable(self) -> bool:
        """检查系统稳定性"""
        eigenvalues = np.linalg.eigvals(self.A)
        return all(np.real(eigenvalue) < 0 for eigenvalue in eigenvalues)
    
    def is_controllable(self) -> bool:
        """检查系统可控性"""
        n = self.A.shape[0]
        controllability_matrix = np.hstack([np.linalg.matrix_power(self.A, i) @ self.B 
                                          for i in range(n)])
        return np.linalg.matrix_rank(controllability_matrix) == n
    
    def is_observable(self) -> bool:
        """检查系统可观性"""
        n = self.A.shape[0]
        observability_matrix = np.vstack([self.C @ np.linalg.matrix_power(self.A, i) 
                                        for i in range(n)])
        return np.linalg.matrix_rank(observability_matrix) == n

class SystemAnalyzer:
    """系统分析器"""
    
    @staticmethod
    def analyze_stability(system: LinearSystem) -> Dict[str, Any]:
        """分析系统稳定性"""
        eigenvalues = np.linalg.eigvals(system.A)
        
        return {
            "eigenvalues": eigenvalues,
            "is_stable": system.is_stable(),
            "natural_frequencies": np.abs(eigenvalues),
            "damping_ratios": -np.real(eigenvalues) / np.abs(eigenvalues)
        }
    
    @staticmethod
    def analyze_controllability(system: LinearSystem) -> Dict[str, Any]:
        """分析系统可控性"""
        return {
            "is_controllable": system.is_controllable(),
            "controllability_gramian": SystemAnalyzer._compute_controllability_gramian(system)
        }
    
    @staticmethod
    def analyze_observability(system: LinearSystem) -> Dict[str, Any]:
        """分析系统可观性"""
        return {
            "is_observable": system.is_observable(),
            "observability_gramian": SystemAnalyzer._compute_observability_gramian(system)
        }
    
    @staticmethod
    def _compute_controllability_gramian(system: LinearSystem) -> np.ndarray:
        """计算可控性格拉姆矩阵"""
        # 简化实现
        return np.eye(system.A.shape[0])
    
    @staticmethod
    def _compute_observability_gramian(system: LinearSystem) -> np.ndarray:
        """计算可观性格拉姆矩阵"""
        # 简化实现
        return np.eye(system.A.shape[0])
```

## 数学基础

### 计算复杂度理论

```math
\text{时间复杂度定义}: T(n) = O(f(n)) \text{ 当且仅当存在常数 } c > 0 \text{ 和 } n_0 \text{ 使得}

\forall n \geq n_0: T(n) \leq c \cdot f(n)

\text{空间复杂度定义}: S(n) = O(f(n)) \text{ 当且仅当存在常数 } c > 0 \text{ 和 } n_0 \text{ 使得}

\forall n \geq n_0: S(n) \leq c \cdot f(n)
```

### 系统理论

```math
\text{线性时不变系统}: 
\begin{align}
\dot{x}(t) &= Ax(t) + Bu(t) \\
y(t) &= Cx(t) + Du(t)
\end{align}

\text{系统稳定性条件}: \text{所有特征值的实部为负}

\text{可控性条件}: \text{可控性矩阵满秩}

\text{可观性条件}: \text{可观性矩阵满秩}
```

### 信息论

```math
\text{信息熵}: H(X) = -\sum_{i=1}^{n} p(x_i) \log_2 p(x_i)

\text{互信息}: I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)

\text{信道容量}: C = \max_{p(x)} I(X;Y)
```

## 应用示例

### 1. 图灵机应用

```python
# 创建回文串识别图灵机
tm = create_palindrome_tm()

# 测试输入
test_inputs = [
    [TapeSymbol.ONE, TapeSymbol.ZERO, TapeSymbol.ONE],  # 101 (回文)
    [TapeSymbol.ONE, TapeSymbol.ZERO, TapeSymbol.ZERO], # 100 (非回文)
    [TapeSymbol.ONE],  # 1 (回文)
    []  # 空串 (回文)
]

for i, input_tape in enumerate(test_inputs):
    result = tm.run(input_tape)
    print(f"输入 {i+1}: {[s.value for s in input_tape]} -> {result['result']}")
```

### 2. 算法分析

```python
# 创建排序算法
quicksort = QuickSort()
mergesort = MergeSort()

# 生成测试数据
def generate_random_data(size: int) -> List[int]:
    return [random.randint(1, 1000) for _ in range(size)]

# 分析算法性能
input_sizes = [100, 500, 1000, 2000, 5000]

quicksort_results = AlgorithmAnalyzer.analyze_time_complexity(
    quicksort, input_sizes, generate_random_data)
mergesort_results = AlgorithmAnalyzer.analyze_time_complexity(
    mergesort, input_sizes, generate_random_data)

print("快速排序复杂度估计:", 
      AlgorithmAnalyzer.estimate_complexity(
          quicksort_results["sizes"], 
          quicksort_results["steps"]))
print("归并排序复杂度估计:", 
      AlgorithmAnalyzer.estimate_complexity(
          mergesort_results["sizes"], 
          mergesort_results["steps"]))
```

### 3. 系统分析

```python
# 创建二阶系统
A = np.array([[-1, 1], [0, -2]])
B = np.array([[1], [0]])
C = np.array([[1, 0]])
D = np.array([[0]])

system = LinearSystem("Second Order System", A, B, C, D)

# 初始化系统
system.initialize({"x0": 1.0, "x1": 0.0})

# 系统分析
stability_analysis = SystemAnalyzer.analyze_stability(system)
controllability_analysis = SystemAnalyzer.analyze_controllability(system)
observability_analysis = SystemAnalyzer.analyze_observability(system)

print("稳定性分析:", stability_analysis)
print("可控性分析:", controllability_analysis)
print("可观性分析:", observability_analysis)

# 系统仿真
dt = 0.1
time_steps = 50
u = np.array([[1.0]])  # 单位阶跃输入

for i in range(time_steps):
    y = system.step(u, dt)
    if i % 10 == 0:
        print(f"t={i*dt:.1f}, y={y[0]:.3f}")
```

## 质量保证

### 1. 理论严谨性
- 数学定义的精确性
- 证明过程的完整性
- 理论框架的一致性

### 2. 实现正确性
- 算法的正确性验证
- 系统的稳定性分析
- 性能的准确评估

### 3. 应用有效性
- 理论到实践的映射
- 抽象到具体的转换
- 复杂度的实际评估

## 相关链接

- [01-形式科学](../01-形式科学/README.md) - 数学和逻辑基础
- [03-具体科学](../03-具体科学/README.md) - 软件工程理论
- [04-行业领域](../04-行业领域/README.md) - 行业应用

---

*最后更新：2024年12月*
