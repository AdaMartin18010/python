# 01-计算哲学

## 概述

计算哲学研究计算的本质、意义和价值，探讨计算作为一种思维方式和存在形式的哲学内涵。本章节从哲学角度深入分析计算的概念、原理和意义。

## 目录结构

```
01-计算哲学/
├── README.md                    # 本文件
├── 01-计算本质/                 # 计算的本质定义
├── 02-可计算性理论/             # 可计算性理论基础
├── 03-计算复杂性/               # 计算复杂性理论
├── 04-计算思维/                 # 计算思维方法
└── 05-计算伦理/                 # 计算伦理学
```

## 1. 计算本质 (Nature of Computation)

### 1.1 定义

**计算**是一个形式化的过程，通过有限步骤将输入转换为输出。

**形式化定义**:
设 $f: \Sigma^* \rightarrow \Sigma^*$ 是一个函数，其中 $\Sigma$ 是有限字母表。
如果存在一个算法 $A$，使得对于任意输入 $x \in \Sigma^*$，$A$ 在有限步内输出 $f(x)$，
则称 $f$ 是**可计算的**。

### 1.2 计算模型

#### 1.2.1 图灵机模型

**定义**: 图灵机是一个七元组 $M = (Q, \Sigma, \Gamma, \delta, q_0, q_{accept}, q_{reject})$，其中：

- $Q$ 是有限状态集
- $\Sigma$ 是输入字母表
- $\Gamma$ 是带字母表，$\Sigma \subseteq \Gamma$
- $\delta: Q \times \Gamma \rightarrow Q \times \Gamma \times \{L, R\}$ 是转移函数
- $q_0 \in Q$ 是初始状态
- $q_{accept}, q_{reject} \in Q$ 是接受和拒绝状态

**Python实现**:

```python
from enum import Enum
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass

class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"

@dataclass
class TuringMachine:
    """图灵机实现"""
    states: set
    input_alphabet: set
    tape_alphabet: set
    transition_function: Dict[Tuple, Tuple]
    initial_state: str
    accept_state: str
    reject_state: str
    
    def __init__(self):
        self.tape = []
        self.head_position = 0
        self.current_state = self.initial_state
    
    def step(self) -> bool:
        """执行一步计算"""
        if self.current_state in [self.accept_state, self.reject_state]:
            return False
        
        current_symbol = self.tape[self.head_position] if self.head_position < len(self.tape) else '_'
        key = (self.current_state, current_symbol)
        
        if key in self.transition_function:
            new_state, new_symbol, direction = self.transition_function[key]
            
            # 更新状态和带内容
            self.current_state = new_state
            if self.head_position < len(self.tape):
                self.tape[self.head_position] = new_symbol
            else:
                self.tape.append(new_symbol)
            
            # 移动读写头
            if direction == Direction.LEFT:
                self.head_position = max(0, self.head_position - 1)
            else:
                self.head_position += 1
                if self.head_position >= len(self.tape):
                    self.tape.append('_')
            
            return True
        else:
            self.current_state = self.reject_state
            return False
    
    def run(self, input_string: str) -> bool:
        """运行图灵机"""
        self.tape = list(input_string)
        self.head_position = 0
        self.current_state = self.initial_state
        
        while self.step():
            pass
        
        return self.current_state == self.accept_state

# 示例：识别回文串的图灵机
def create_palindrome_turing_machine() -> TuringMachine:
    """创建识别回文串的图灵机"""
    # 简化的回文识别算法
    states = {'q0', 'q1', 'q2', 'q3', 'qaccept', 'qreject'}
    input_alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', '_', 'X', 'Y'}
    
    # 转移函数（简化版本）
    transition_function = {
        # 初始状态：检查第一个字符
        ('q0', '0'): ('q1', 'X', Direction.RIGHT),
        ('q0', '1'): ('q2', 'Y', Direction.RIGHT),
        ('q0', '_'): ('qaccept', '_', Direction.RIGHT),
        
        # 寻找字符串末尾
        ('q1', '0'): ('q1', '0', Direction.RIGHT),
        ('q1', '1'): ('q1', '1', Direction.RIGHT),
        ('q1', '_'): ('q3', '_', Direction.LEFT),
        
        ('q2', '0'): ('q2', '0', Direction.RIGHT),
        ('q2', '1'): ('q2', '1', Direction.RIGHT),
        ('q2', '_'): ('q3', '_', Direction.LEFT),
        
        # 检查末尾字符
        ('q3', '0'): ('qaccept', 'X', Direction.LEFT),
        ('q3', '1'): ('qreject', '1', Direction.LEFT),
        ('q3', 'X'): ('qaccept', 'X', Direction.LEFT),
        ('q3', 'Y'): ('qaccept', 'Y', Direction.LEFT),
    }
    
    return TuringMachine()

def test_turing_machine():
    """测试图灵机"""
    tm = create_palindrome_turing_machine()
    
    test_cases = ['', '0', '1', '00', '11', '01', '10', '000', '010', '100']
    
    for test_input in test_cases:
        result = tm.run(test_input)
        is_palindrome = test_input == test_input[::-1]
        print(f"输入: '{test_input}' -> 图灵机结果: {result}, 实际: {is_palindrome}")

if __name__ == "__main__":
    test_turing_machine()
```

#### 1.2.2 Lambda演算模型

**定义**: Lambda演算是一个形式化系统，用于研究函数定义、函数应用和递归。

**语法**:

- 变量: $x, y, z, \ldots$
- 抽象: $\lambda x.M$ (函数定义)
- 应用: $(M N)$ (函数应用)

**公理**:

- $\alpha$-等价: $\lambda x.M = \lambda y.M[y/x]$ (变量重命名)
- $\beta$-归约: $(\lambda x.M) N = M[N/x]$ (函数应用)
- $\eta$-等价: $\lambda x.(M x) = M$ (外延性)

**Python实现**:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

class LambdaTerm(ABC):
    """Lambda项抽象基类"""
    
    @abstractmethod
    def free_variables(self) -> set:
        """获取自由变量"""
        pass
    
    @abstractmethod
    def substitute(self, var: str, term: 'LambdaTerm') -> 'LambdaTerm':
        """变量替换"""
        pass
    
    @abstractmethod
    def reduce(self) -> 'LambdaTerm':
        """归约"""
        pass

class Variable(LambdaTerm):
    """变量"""
    
    def __init__(self, name: str):
        self.name = name
    
    def free_variables(self) -> set:
        return {self.name}
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        if self.name == var:
            return term
        return self
    
    def reduce(self) -> LambdaTerm:
        return self
    
    def __str__(self) -> str:
        return self.name

class Abstraction(LambdaTerm):
    """抽象"""
    
    def __init__(self, parameter: str, body: LambdaTerm):
        self.parameter = parameter
        self.body = body
    
    def free_variables(self) -> set:
        return self.body.free_variables() - {self.parameter}
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        if var == self.parameter:
            return self
        if self.parameter in term.free_variables():
            # 需要alpha转换
            new_param = self._generate_fresh_variable()
            new_body = self.body.substitute(self.parameter, Variable(new_param))
            return Abstraction(new_param, new_body.substitute(var, term))
        return Abstraction(self.parameter, self.body.substitute(var, term))
    
    def reduce(self) -> LambdaTerm:
        return Abstraction(self.parameter, self.body.reduce())
    
    def _generate_fresh_variable(self) -> str:
        """生成新的变量名"""
        import string
        import random
        return ''.join(random.choices(string.ascii_lowercase, k=3))
    
    def __str__(self) -> str:
        return f"λ{self.parameter}.{self.body}"

class Application(LambdaTerm):
    """应用"""
    
    def __init__(self, function: LambdaTerm, argument: LambdaTerm):
        self.function = function
        self.argument = argument
    
    def free_variables(self) -> set:
        return self.function.free_variables() | self.argument.free_variables()
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        return Application(
            self.function.substitute(var, term),
            self.argument.substitute(var, term)
        )
    
    def reduce(self) -> LambdaTerm:
        # 先归约函数部分
        reduced_function = self.function.reduce()
        
        # 如果是抽象，进行beta归约
        if isinstance(reduced_function, Abstraction):
            return reduced_function.body.substitute(
                reduced_function.parameter, 
                self.argument
            ).reduce()
        
        # 否则归约参数部分
        return Application(reduced_function, self.argument.reduce())
    
    def __str__(self) -> str:
        return f"({self.function} {self.argument})"

# Lambda演算示例
def lambda_calculus_example():
    """Lambda演算示例"""
    
    # 定义恒等函数: λx.x
    identity = Abstraction('x', Variable('x'))
    print(f"恒等函数: {identity}")
    
    # 定义常量函数: λx.y
    const = Abstraction('x', Variable('y'))
    print(f"常量函数: {const}")
    
    # 应用恒等函数: (λx.x) y
    app = Application(identity, Variable('y'))
    print(f"应用: {app}")
    
    # 归约
    result = app.reduce()
    print(f"归约结果: {result}")
    
    # 自由变量
    print(f"应用的自由变量: {app.free_variables()}")

if __name__ == "__main__":
    lambda_calculus_example()
```

## 2. 可计算性理论 (Computability Theory)

### 2.1 丘奇-图灵论题

**丘奇-图灵论题**: 任何可计算的函数都可以由图灵机计算。

**形式化表述**: 对于任意函数 $f: \mathbb{N} \rightarrow \mathbb{N}$，如果存在算法计算 $f$，则存在图灵机 $M$ 使得 $M$ 计算 $f$。

### 2.2 停机问题

**停机问题**: 给定图灵机 $M$ 和输入 $w$，判断 $M$ 在输入 $w$ 上是否会停机。

**定理**: 停机问题是不可判定的。

**证明**:
假设存在图灵机 $H$ 可以判定停机问题。构造图灵机 $D$：

1. $D$ 接受输入 $M$（图灵机的编码）
2. $D$ 运行 $H(M, M)$
3. 如果 $H$ 输出"停机"，则 $D$ 进入无限循环
4. 如果 $H$ 输出"不停机"，则 $D$ 停机

现在考虑 $D(D)$：

- 如果 $D(D)$ 停机，则 $H(D, D)$ 输出"停机"，但 $D$ 会进入无限循环，矛盾
- 如果 $D(D)$ 不停机，则 $H(D, D)$ 输出"不停机"，但 $D$ 会停机，矛盾

因此，停机问题是不可判定的。

**Python实现**:

```python
from typing import Callable, Any
import time

class HaltingProblem:
    """停机问题演示"""
    
    @staticmethod
    def halts(program: Callable, input_data: Any) -> bool:
        """
        判断程序在给定输入上是否会停机
        注意：这是一个简化的演示，实际停机问题是不可判定的
        """
        try:
            # 设置超时来模拟停机检测
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("程序可能不会停机")
            
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(1)  # 1秒超时
            
            result = program(input_data)
            signal.alarm(0)  # 取消超时
            return True
            
        except TimeoutError:
            return False
        except Exception:
            return True  # 其他异常认为会停机
    
    @staticmethod
    def create_paradoxical_program():
        """创建导致悖论的程序"""
        def paradoxical_program(program_code):
            # 这是一个简化的悖论程序
            if HaltingProblem.halts(program_code, program_code):
                # 如果程序会停机，则进入无限循环
                while True:
                    pass
            else:
                # 如果程序不会停机，则停机
                return "停机"
        
        return paradoxical_program

def halting_problem_example():
    """停机问题示例"""
    
    # 会停机的程序
    def halting_program(n):
        return n * 2
    
    # 不会停机的程序
    def non_halting_program(n):
        while True:
            n += 1
    
    # 测试
    print("测试会停机的程序:")
    try:
        result = HaltingProblem.halts(halting_program, 5)
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n测试不会停机的程序:")
    try:
        result = HaltingProblem.halts(non_halting_program, 5)
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    halting_problem_example()
```

## 3. 计算复杂性 (Computational Complexity)

### 3.1 时间复杂度

**定义**: 算法的时间复杂度是算法执行时间随输入规模增长的变化规律。

**常见复杂度类**:

- $O(1)$: 常数时间
- $O(\log n)$: 对数时间
- $O(n)$: 线性时间
- $O(n \log n)$: 线性对数时间
- $O(n^2)$: 平方时间
- $O(2^n)$: 指数时间

**Python实现**:

```python
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, List, Tuple

class ComplexityAnalyzer:
    """复杂度分析器"""
    
    @staticmethod
    def measure_time(func: Callable, inputs: List) -> List[float]:
        """测量函数在不同输入规模下的执行时间"""
        times = []
        
        for input_data in inputs:
            start_time = time.time()
            func(input_data)
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
            return "O(n²) - 平方时间"
        else:
            return "O(2ⁿ) - 指数时间"

# 不同复杂度的算法示例
def constant_time_algorithm(n: int) -> int:
    """O(1) 算法"""
    return n * 2

def linear_time_algorithm(n: int) -> int:
    """O(n) 算法"""
    result = 0
    for i in range(n):
        result += i
    return result

def quadratic_time_algorithm(n: int) -> int:
    """O(n²) 算法"""
    result = 0
    for i in range(n):
        for j in range(n):
            result += i * j
    return result

def exponential_time_algorithm(n: int) -> int:
    """O(2ⁿ) 算法 - 斐波那契递归"""
    if n <= 1:
        return n
    return exponential_time_algorithm(n-1) + exponential_time_algorithm(n-2)

def complexity_analysis_example():
    """复杂度分析示例"""
    
    # 测试输入规模
    input_sizes = [100, 200, 400, 800, 1600]
    
    # 分析不同算法
    algorithms = [
        ("常数时间", constant_time_algorithm),
        ("线性时间", linear_time_algorithm),
        ("平方时间", quadratic_time_algorithm),
    ]
    
    for name, algorithm in algorithms:
        print(f"\n分析 {name} 算法:")
        
        # 测量执行时间
        execution_times = ComplexityAnalyzer.measure_time(algorithm, input_sizes)
        
        # 分析复杂度
        complexity = ComplexityAnalyzer.analyze_complexity(input_sizes, execution_times)
        
        print(f"复杂度: {complexity}")
        print("执行时间:")
        for size, time_taken in zip(input_sizes, execution_times):
            print(f"  输入规模 {size}: {time_taken:.6f} 秒")

if __name__ == "__main__":
    complexity_analysis_example()
```

## 4. 计算思维 (Computational Thinking)

### 4.1 定义

**计算思维**是一种解决问题的思维方式，包括：

- **分解**: 将复杂问题分解为简单子问题
- **模式识别**: 识别问题中的模式和规律
- **抽象**: 提取问题的本质特征
- **算法设计**: 设计解决问题的步骤

### 4.2 计算思维方法

**Python实现**:

```python
from abc import ABC, abstractmethod
from typing import List, Any, Callable
from dataclasses import dataclass

@dataclass
class Problem:
    """问题抽象"""
    description: str
    input_data: Any
    expected_output: Any
    complexity: str

class ComputationalThinking:
    """计算思维方法"""
    
    @staticmethod
    def decompose(problem: Problem) -> List[Problem]:
        """分解问题"""
        # 示例：将排序问题分解为比较和交换
        sub_problems = []
        
        if "排序" in problem.description:
            sub_problems.append(Problem(
                "比较两个元素",
                problem.input_data,
                None,
                "O(1)"
            ))
            sub_problems.append(Problem(
                "交换两个元素",
                problem.input_data,
                None,
                "O(1)"
            ))
        
        return sub_problems
    
    @staticmethod
    def recognize_patterns(data: List[Any]) -> List[Callable]:
        """识别模式"""
        patterns = []
        
        # 检查是否有序
        if all(data[i] <= data[i+1] for i in range(len(data)-1)):
            patterns.append(lambda x: "已排序")
        
        # 检查是否有重复
        if len(set(data)) < len(data):
            patterns.append(lambda x: "有重复元素")
        
        # 检查数值范围
        if all(isinstance(x, (int, float)) for x in data):
            patterns.append(lambda x: f"数值范围: {min(x)}-{max(x)}")
        
        return patterns
    
    @staticmethod
    def abstract(problem: Problem) -> str:
        """抽象问题"""
        # 提取问题的核心特征
        if "排序" in problem.description:
            return "比较排序问题"
        elif "搜索" in problem.description:
            return "查找问题"
        elif "计算" in problem.description:
            return "计算问题"
        else:
            return "一般问题"
    
    @staticmethod
    def design_algorithm(problem: Problem) -> Callable:
        """设计算法"""
        problem_type = ComputationalThinking.abstract(problem)
        
        if problem_type == "比较排序问题":
            return lambda x: sorted(x)
        elif problem_type == "查找问题":
            return lambda x: x.index if hasattr(x, 'index') else None
        else:
            return lambda x: x

def computational_thinking_example():
    """计算思维示例"""
    
    # 创建问题
    problem = Problem(
        "对整数列表进行排序",
        [3, 1, 4, 1, 5, 9, 2, 6],
        [1, 1, 2, 3, 4, 5, 6, 9],
        "O(n log n)"
    )
    
    print("原始问题:", problem.description)
    print("输入数据:", problem.input_data)
    
    # 应用计算思维方法
    print("\n1. 分解问题:")
    sub_problems = ComputationalThinking.decompose(problem)
    for i, sub_problem in enumerate(sub_problems, 1):
        print(f"   {i}. {sub_problem.description}")
    
    print("\n2. 识别模式:")
    patterns = ComputationalThinking.recognize_patterns(problem.input_data)
    for pattern in patterns:
        print(f"   - {pattern(problem.input_data)}")
    
    print("\n3. 抽象问题:")
    abstraction = ComputationalThinking.abstract(problem)
    print(f"   问题类型: {abstraction}")
    
    print("\n4. 设计算法:")
    algorithm = ComputationalThinking.design_algorithm(problem)
    result = algorithm(problem.input_data)
    print(f"   算法结果: {result}")
    print(f"   期望结果: {problem.expected_output}")
    print(f"   结果正确: {result == problem.expected_output}")

if __name__ == "__main__":
    computational_thinking_example()
```

## 5. 计算伦理 (Computational Ethics)

### 5.1 定义

**计算伦理**研究计算技术应用中的道德问题和伦理原则，包括隐私保护、算法公平性、人工智能伦理等。

### 5.2 核心原则

1. **隐私保护**: 保护个人数据和隐私
2. **算法公平性**: 确保算法不产生歧视
3. **透明度**: 算法决策过程可解释
4. **责任性**: 明确算法使用者的责任

**Python实现**:

```python
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import random

class EthicalPrinciple(Enum):
    PRIVACY = "privacy"
    FAIRNESS = "fairness"
    TRANSPARENCY = "transparency"
    ACCOUNTABILITY = "accountability"

@dataclass
class EthicalViolation:
    """伦理违规"""
    principle: EthicalPrinciple
    description: str
    severity: float  # 0-1, 1为最严重
    impact: str

class EthicalAlgorithm:
    """伦理算法基类"""
    
    def __init__(self):
        self.violations: List[EthicalViolation] = []
        self.privacy_level = 1.0  # 0-1, 1为最高隐私保护
        self.fairness_score = 1.0  # 0-1, 1为最公平
        self.transparency_score = 1.0  # 0-1, 1为最透明
    
    def check_privacy(self, data: Any) -> bool:
        """检查隐私保护"""
        # 简化的隐私检查
        if isinstance(data, dict) and 'personal_info' in data:
            self.violations.append(EthicalViolation(
                EthicalPrinciple.PRIVACY,
                "包含个人信息",
                0.8,
                "高"
            ))
            return False
        return True
    
    def check_fairness(self, decisions: List[Any], groups: List[str]) -> bool:
        """检查算法公平性"""
        if len(set(groups)) < 2:
            return True
        
        # 计算各组的决策分布
        group_decisions = {}
        for decision, group in zip(decisions, groups):
            if group not in group_decisions:
                group_decisions[group] = []
            group_decisions[group].append(decision)
        
        # 检查是否存在显著差异
        positive_rates = {}
        for group, group_decisions_list in group_decisions.items():
            positive_rates[group] = sum(1 for d in group_decisions_list if d) / len(group_decisions_list)
        
        # 如果差异过大，认为不公平
        max_rate = max(positive_rates.values())
        min_rate = min(positive_rates.values())
        
        if max_rate - min_rate > 0.3:  # 30%的差异阈值
            self.violations.append(EthicalViolation(
                EthicalPrinciple.FAIRNESS,
                f"决策在不同组间差异过大: {positive_rates}",
                0.9,
                "高"
            ))
            return False
        
        return True
    
    def explain_decision(self, input_data: Any, decision: Any) -> str:
        """解释决策过程"""
        return f"基于输入 {input_data} 的特征，算法做出决策 {decision}"
    
    def get_ethical_report(self) -> Dict[str, Any]:
        """获取伦理报告"""
        return {
            "privacy_score": self.privacy_level,
            "fairness_score": self.fairness_score,
            "transparency_score": self.transparency_score,
            "violations": self.violations,
            "overall_ethical_score": (self.privacy_level + self.fairness_score + self.transparency_score) / 3
        }

class FairClassifier(EthicalAlgorithm):
    """公平分类器"""
    
    def __init__(self):
        super().__init__()
        self.decision_threshold = 0.5
    
    def classify(self, features: List[float], group: str) -> bool:
        """分类决策"""
        # 简化的分类逻辑
        score = sum(features) / len(features)
        
        # 检查隐私
        if not self.check_privacy({"features": features}):
            return False
        
        decision = score > self.decision_threshold
        
        # 检查公平性（需要累积数据）
        if not hasattr(self, 'all_decisions'):
            self.all_decisions = []
            self.all_groups = []
        
        self.all_decisions.append(decision)
        self.all_groups.append(group)
        
        if len(self.all_decisions) > 10:
            self.check_fairness(self.all_decisions, self.all_groups)
        
        return decision
    
    def explain_decision(self, features: List[float], decision: bool) -> str:
        """解释分类决策"""
        score = sum(features) / len(features)
        return f"特征平均分: {score:.2f}, 阈值: {self.decision_threshold}, 决策: {decision}"

def computational_ethics_example():
    """计算伦理示例"""
    
    # 创建公平分类器
    classifier = FairClassifier()
    
    # 模拟不同群体的数据
    groups = ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    features_list = [
        [0.8, 0.9, 0.7],  # A组，高分
        [0.3, 0.4, 0.2],  # B组，低分
        [0.7, 0.8, 0.6],  # A组，高分
        [0.2, 0.3, 0.1],  # B组，低分
        [0.9, 0.8, 0.9],  # A组，高分
        [0.1, 0.2, 0.1],  # B组，低分
        [0.6, 0.7, 0.5],  # A组，中等分
        [0.4, 0.5, 0.3],  # B组，中等分
        [0.8, 0.9, 0.8],  # A组，高分
        [0.2, 0.1, 0.2],  # B组，低分
    ]
    
    print("公平分类器测试:")
    print("=" * 50)
    
    for i, (features, group) in enumerate(zip(features_list, groups)):
        decision = classifier.classify(features, group)
        explanation = classifier.explain_decision(features, decision)
        print(f"样本 {i+1} (组{group}): {explanation}")
    
    print("\n伦理评估报告:")
    print("=" * 50)
    report = classifier.get_ethical_report()
    
    for key, value in report.items():
        if key == "violations":
            print(f"{key}:")
            for violation in value:
                print(f"  - {violation.principle.value}: {violation.description} (严重性: {violation.severity})")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    computational_ethics_example()
```

## 导航链接

- **上级目录**: [../README.md](../README.md)
- **同级目录**:
  - [02-软件工程哲学/](../02-软件工程哲学/)
  - [03-形式化思维/](../03-形式化思维/)
  - [04-系统思维/](../04-系统思维/)
  - [05-抽象思维/](../05-抽象思维/)
- **下级目录**:
  - [01-计算本质/](01-计算本质/)
  - [02-可计算性理论/](02-可计算性理论/)
  - [03-计算复杂性/](03-计算复杂性/)
  - [04-计算思维/](04-计算思维/)
  - [05-计算伦理/](05-计算伦理/)

## 参考文献

1. Church, A. (1936). An unsolvable problem of elementary number theory. American Journal of Mathematics, 58(2), 345-363.
2. Turing, A. M. (1937). On computable numbers, with an application to the Entscheidungsproblem. Proceedings of the London Mathematical Society, 42(1), 230-265.
3. Sipser, M. (2012). Introduction to the Theory of Computation. Cengage Learning.
4. Wing, J. M. (2006). Computational thinking. Communications of the ACM, 49(3), 33-35.
5. Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., Chazerand, P., Dignum, V., ... & Vayena, E. (2018). AI4People—An ethical framework for a good AI society: opportunities, risks, principles, and recommendations. Minds and Machines, 28(4), 689-707.
