# 02-理论基础 (Theoretical Foundation)

## 概述

理论基础层建立在形式科学层之上，涵盖了计算理论、算法理论、复杂性理论、形式语言理论和自动机理论等核心内容。这一层为软件工程提供了计算科学的基础理论支撑。

## 目录结构

```text
02-理论基础/
├── 01-计算理论/
│   ├── 01-图灵机理论.md
│   ├── 02-可计算性理论.md
│   ├── 03-递归函数理论.md
│   └── 04-λ演算理论.md
├── 02-算法理论/
│   ├── 01-算法设计.md
│   ├── 02-算法分析.md
│   ├── 03-算法正确性.md
│   └── 04-算法优化.md
├── 03-复杂性理论/
│   ├── 01-时间复杂度.md
│   ├── 02-空间复杂度.md
│   ├── 03-P与NP问题.md
│   └── 04-近似算法.md
├── 04-形式语言理论/
│   ├── 01-文法理论.md
│   ├── 02-语言层次.md
│   ├── 03-语法分析.md
│   └── 04-语义理论.md
└── 05-自动机理论/
    ├── 01-有限自动机.md
    ├── 02-下推自动机.md
    ├── 03-图灵机.md
    └── 04-自动机应用.md
```

## 核心理论

### 1. 计算理论 (Computability Theory)

```math
\text{计算理论框架:}

\text{图灵机} TM = (Q, \Sigma, \Gamma, \delta, q_0, B, F)

\text{其中:}
\begin{align}
Q &= \text{状态集合} \\
\Sigma &= \text{输入字母表} \\
\Gamma &= \text{带字母表} \\
\delta &= \text{转移函数} \\
q_0 &= \text{初始状态} \\
B &= \text{空白符号} \\
F &= \text{接受状态集合}
\end{align}
```

### 2. 算法理论 (Algorithm Theory)

```math
\text{算法定义:}

\text{算法} A = (I, P, O, T, C)

\text{其中:}
\begin{align}
I &= \text{输入集合} \\
P &= \text{处理步骤} \\
O &= \text{输出集合} \\
T &= \text{终止条件} \\
C &= \text{复杂度界限}
\end{align}
```

### 3. 复杂性理论 (Complexity Theory)

```math
\text{复杂度类:}

\begin{align}
P &= \{L : L \text{ 可在多项式时间内被确定性图灵机识别}\} \\
NP &= \{L : L \text{ 可在多项式时间内被非确定性图灵机识别}\} \\
PSPACE &= \{L : L \text{ 可在多项式空间内被图灵机识别}\} \\
EXP &= \{L : L \text{ 可在指数时间内被图灵机识别}\}
\end{align}
```

## Python实现

### 1. 图灵机实现

```python
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"
    STAY = "S"

@dataclass
class TuringMachine:
    """图灵机"""
    states: Set[str]
    input_alphabet: Set[str]
    tape_alphabet: Set[str]
    transition_function: Dict[Tuple[str, str], Tuple[str, str, Direction]]
    initial_state: str
    blank_symbol: str
    accept_states: Set[str]
    
    def __post_init__(self):
        self.current_state = self.initial_state
        self.tape = [self.blank_symbol]
        self.head_position = 0
    
    def step(self) -> bool:
        """执行一步"""
        if self.current_state in self.accept_states:
            return True
        
        current_symbol = self.tape[self.head_position]
        key = (self.current_state, current_symbol)
        
        if key not in self.transition_function:
            return False
        
        new_state, new_symbol, direction = self.transition_function[key]
        
        # 更新状态和带
        self.current_state = new_state
        self.tape[self.head_position] = new_symbol
        
        # 移动读写头
        if direction == Direction.LEFT:
            self.head_position -= 1
            if self.head_position < 0:
                self.tape.insert(0, self.blank_symbol)
                self.head_position = 0
        elif direction == Direction.RIGHT:
            self.head_position += 1
            if self.head_position >= len(self.tape):
                self.tape.append(self.blank_symbol)
        
        return True
    
    def run(self, input_string: str) -> bool:
        """运行图灵机"""
        # 初始化带
        self.tape = list(input_string) + [self.blank_symbol]
        self.head_position = 0
        self.current_state = self.initial_state
        
        # 执行步骤直到停机
        steps = 0
        max_steps = 1000  # 防止无限循环
        
        while steps < max_steps:
            if not self.step():
                return False
            steps += 1
        
        return self.current_state in self.accept_states

# 示例：识别回文串的图灵机
def create_palindrome_tm() -> TuringMachine:
    """创建识别回文串的图灵机"""
    states = {"q0", "q1", "q2", "q3", "q4", "qaccept", "qreject"}
    input_alphabet = {"0", "1"}
    tape_alphabet = {"0", "1", "X", "Y", "B"}
    blank_symbol = "B"
    initial_state = "q0"
    accept_states = {"qaccept"}
    
    # 转移函数
    transitions = {
        ("q0", "0"): ("q1", "X", Direction.RIGHT),
        ("q0", "1"): ("q2", "Y", Direction.RIGHT),
        ("q0", "X"): ("qaccept", "X", Direction.STAY),
        ("q0", "Y"): ("qaccept", "Y", Direction.STAY),
        ("q0", "B"): ("qaccept", "B", Direction.STAY),
        ("q1", "0"): ("q1", "0", Direction.RIGHT),
        ("q1", "1"): ("q1", "1", Direction.RIGHT),
        ("q1", "X"): ("q3", "X", Direction.LEFT),
        ("q1", "Y"): ("q3", "Y", Direction.LEFT),
        ("q1", "B"): ("q3", "B", Direction.LEFT),
        ("q2", "0"): ("q2", "0", Direction.RIGHT),
        ("q2", "1"): ("q2", "1", Direction.RIGHT),
        ("q2", "X"): ("q4", "X", Direction.LEFT),
        ("q2", "Y"): ("q4", "Y", Direction.LEFT),
        ("q2", "B"): ("q4", "B", Direction.LEFT),
        ("q3", "0"): ("qreject", "0", Direction.STAY),
        ("q3", "1"): ("qreject", "1", Direction.STAY),
        ("q3", "X"): ("q0", "X", Direction.RIGHT),
        ("q3", "Y"): ("qreject", "Y", Direction.STAY),
        ("q4", "0"): ("qreject", "0", Direction.STAY),
        ("q4", "1"): ("qreject", "1", Direction.STAY),
        ("q4", "X"): ("qreject", "X", Direction.STAY),
        ("q4", "Y"): ("q0", "Y", Direction.RIGHT),
    }
    
    return TuringMachine(
        states=states,
        input_alphabet=input_alphabet,
        tape_alphabet=tape_alphabet,
        transition_function=transitions,
        initial_state=initial_state,
        blank_symbol=blank_symbol,
        accept_states=accept_states
    )
```

### 2. 算法分析实现

```python
import time
from typing import Callable, List, Any, Dict
from dataclasses import dataclass

@dataclass
class AlgorithmAnalysis:
    """算法分析"""
    name: str
    function: Callable
    complexity: str
    description: str

class ComplexityAnalyzer:
    """复杂度分析器"""
    
    @staticmethod
    def measure_time(algorithm: Callable, inputs: List[Any]) -> Dict[str, float]:
        """测量执行时间"""
        times = []
        for input_data in inputs:
            start_time = time.time()
            algorithm(input_data)
            end_time = time.time()
            times.append(end_time - start_time)
        
        return {
            "times": times,
            "average": sum(times) / len(times),
            "min": min(times),
            "max": max(times)
        }
    
    @staticmethod
    def estimate_complexity(times: List[float], sizes: List[int]) -> str:
        """估计复杂度"""
        if len(times) < 2:
            return "O(1)"
        
        # 简单的复杂度估计
        time_ratio = times[-1] / times[0]
        size_ratio = sizes[-1] / sizes[0]
        
        if time_ratio < 2:
            return "O(1)"
        elif time_ratio < size_ratio:
            return "O(log n)"
        elif time_ratio < size_ratio * 2:
            return "O(n)"
        elif time_ratio < size_ratio ** 2:
            return "O(n log n)"
        else:
            return "O(n²)"

# 示例算法
def linear_search(arr: List[int], target: int) -> int:
    """线性搜索"""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def binary_search(arr: List[int], target: int) -> int:
    """二分搜索"""
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

def bubble_sort(arr: List[int]) -> List[int]:
    """冒泡排序"""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

### 3. 形式语言理论实现

```python
from typing import Set, List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Grammar:
    """文法"""
    non_terminals: Set[str]
    terminals: Set[str]
    productions: Dict[str, List[str]]
    start_symbol: str

class FiniteAutomaton:
    """有限自动机"""
    
    def __init__(self, states: Set[str], alphabet: Set[str], 
                 transitions: Dict[Tuple[str, str], str], 
                 initial_state: str, accept_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.current_state = initial_state
    
    def reset(self):
        """重置状态"""
        self.current_state = self.initial_state
    
    def step(self, symbol: str) -> bool:
        """执行一步"""
        key = (self.current_state, symbol)
        if key in self.transitions:
            self.current_state = self.transitions[key]
            return True
        return False
    
    def accept(self, string: str) -> bool:
        """接受字符串"""
        self.reset()
        for symbol in string:
            if not self.step(symbol):
                return False
        return self.current_state in self.accept_states

# 示例：识别偶数个0的自动机
def create_even_zeros_fa() -> FiniteAutomaton:
    """创建识别偶数个0的有限自动机"""
    states = {"q0", "q1"}
    alphabet = {"0", "1"}
    initial_state = "q0"
    accept_states = {"q0"}
    
    transitions = {
        ("q0", "0"): "q1",
        ("q0", "1"): "q0",
        ("q1", "0"): "q0",
        ("q1", "1"): "q1"
    }
    
    return FiniteAutomaton(states, alphabet, transitions, initial_state, accept_states)
```

## 应用示例

```python
def demonstrate_theoretical_foundations():
    """演示理论基础应用"""
    
    # 1. 图灵机示例
    print("=== 图灵机示例 ===")
    tm = create_palindrome_tm()
    test_strings = ["", "0", "1", "00", "11", "01", "010", "101"]
    
    for s in test_strings:
        result = tm.run(s)
        is_palindrome = s == s[::-1]
        print(f"'{s}' -> {result} (期望: {is_palindrome})")
    
    # 2. 算法分析示例
    print("\n=== 算法分析示例 ===")
    analyzer = ComplexityAnalyzer()
    
    # 测试线性搜索
    sizes = [100, 200, 400, 800]
    inputs = [list(range(size)) for size in sizes]
    
    for size, input_data in zip(sizes, inputs):
        times = analyzer.measure_time(lambda: linear_search(input_data, -1), [input_data])
        print(f"线性搜索 (n={size}): {times['average']:.6f}s")
    
    # 3. 有限自动机示例
    print("\n=== 有限自动机示例 ===")
    fa = create_even_zeros_fa()
    test_strings = ["", "0", "1", "00", "01", "10", "11", "000", "001"]
    
    for s in test_strings:
        result = fa.accept(s)
        zero_count = s.count('0')
        expected = zero_count % 2 == 0
        print(f"'{s}' -> {result} (0的个数: {zero_count}, 期望: {expected})")

if __name__ == "__main__":
    demonstrate_theoretical_foundations()
```

## 总结

理论基础层为软件工程提供了计算科学的核心理论支撑：

1. **计算理论**: 提供了计算的基本模型和可计算性理论
2. **算法理论**: 提供了算法设计和分析的理论基础
3. **复杂性理论**: 提供了计算复杂度的分析框架
4. **形式语言理论**: 提供了语言处理的理论基础
5. **自动机理论**: 提供了状态机建模的理论工具

这些理论为软件工程的其他层次提供了可靠的理论基础。

---

**相关链接**:

- [01-形式科学](../01-形式科学/README.md) - 数学和逻辑基础
- [03-具体科学](../03-具体科学/README.md) - 软件工程理论
- [04-行业领域](../04-行业领域/README.md) - 应用领域

**更新时间**: 2024年12月
**版本**: 1.0.0
