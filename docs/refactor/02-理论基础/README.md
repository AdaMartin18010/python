# 02. 理论基础层

## 概述

理论基础层是软件工程知识体系的计算机科学理论基础，建立在形式科学层之上，提供软件工程的核心理论支撑。

## 目录结构

```
02-理论基础/
├── 01-计算模型/
│   ├── 01-图灵机.md
│   ├── 02-λ演算.md
│   ├── 03-递归函数.md
│   ├── 04-寄存器机.md
│   └── 05-并行计算模型.md
├── 02-算法理论/
│   ├── 01-算法设计.md
│   ├── 02-算法分析.md
│   ├── 03-算法优化.md
│   ├── 04-随机算法.md
│   └── 05-近似算法.md
├── 03-数据结构/
│   ├── 01-基础数据结构.md
│   ├── 02-高级数据结构.md
│   ├── 03-抽象数据类型.md
│   ├── 04-持久化数据结构.md
│   └── 05-并发数据结构.md
├── 04-编程语言理论/
│   ├── 01-语法理论.md
│   ├── 02-语义理论.md
│   ├── 03-类型理论.md
│   ├── 04-程序分析.md
│   └── 05-程序变换.md
├── 05-并发理论/
│   ├── 01-进程代数.md
│   ├── 02-时序逻辑.md
│   ├── 03-死锁理论.md
│   ├── 04-一致性理论.md
│   └── 05-分布式算法.md
└── README.md
```

## 核心理念

### 1. 计算模型

不同的计算模型为软件工程提供理论基础：

- **图灵机**：通用计算模型
- **λ演算**：函数式编程基础
- **递归函数**：可计算性理论
- **寄存器机**：实际计算机模型
- **并行计算模型**：并发计算基础

### 2. 算法理论

算法是软件工程的核心：

- **算法设计**：问题求解方法
- **算法分析**：复杂度分析
- **算法优化**：性能改进
- **随机算法**：概率性算法
- **近似算法**：启发式方法

### 3. 数据结构

数据结构是算法的基础：

- **基础数据结构**：数组、链表、栈、队列
- **高级数据结构**：树、图、哈希表
- **抽象数据类型**：接口与实现分离
- **持久化数据结构**：不可变数据结构
- **并发数据结构**：线程安全的数据结构

## 计算模型

### 图灵机

**基本图灵机**

图灵机是计算理论的基础模型：

```python
from typing import Dict, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    """移动方向"""
    LEFT = "L"
    RIGHT = "R"
    STAY = "S"

@dataclass
class Transition:
    """状态转移"""
    current_state: str
    current_symbol: str
    new_state: str
    new_symbol: str
    direction: Direction

class TuringMachine:
    """图灵机"""
    
    def __init__(self, 
                 states: Set[str],
                 alphabet: Set[str],
                 blank_symbol: str,
                 initial_state: str,
                 accepting_states: Set[str],
                 transitions: Set[Transition]):
        self.states = states
        self.alphabet = alphabet
        self.blank_symbol = blank_symbol
        self.current_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = {t: t for t in transitions}
        
        # 磁带
        self.tape: Dict[int, str] = {}
        self.head_position = 0
        
        # 步数限制
        self.max_steps = 1000
        self.step_count = 0
    
    def write_tape(self, input_string: str) -> None:
        """写入输入到磁带"""
        self.tape.clear()
        for i, symbol in enumerate(input_string):
            self.tape[i] = symbol
    
    def read_symbol(self) -> str:
        """读取当前符号"""
        return self.tape.get(self.head_position, self.blank_symbol)
    
    def write_symbol(self, symbol: str) -> None:
        """写入符号到当前位置"""
        if symbol == self.blank_symbol:
            self.tape.pop(self.head_position, None)
        else:
            self.tape[self.head_position] = symbol
    
    def move_head(self, direction: Direction) -> None:
        """移动读写头"""
        if direction == Direction.LEFT:
            self.head_position -= 1
        elif direction == Direction.RIGHT:
            self.head_position += 1
        # STAY 不移动
    
    def step(self) -> bool:
        """执行一步"""
        if self.step_count >= self.max_steps:
            return False
        
        current_symbol = self.read_symbol()
        
        # 查找转移规则
        for transition in self.transitions.values():
            if (transition.current_state == self.current_state and 
                transition.current_symbol == current_symbol):
                
                # 执行转移
                self.write_symbol(transition.new_symbol)
                self.current_state = transition.new_state
                self.move_head(transition.direction)
                self.step_count += 1
                return True
        
        return False
    
    def run(self, input_string: str) -> bool:
        """运行图灵机"""
        self.write_tape(input_string)
        self.head_position = 0
        self.current_state = list(self.states)[0]  # 初始状态
        self.step_count = 0
        
        while self.step():
            if self.current_state in self.accepting_states:
                return True
        
        return self.current_state in self.accepting_states

# 使用示例：识别回文串的图灵机
def create_palindrome_tm() -> TuringMachine:
    """创建识别回文串的图灵机"""
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q_accept', 'q_reject'}
    alphabet = {'0', '1', 'X', 'Y', 'B'}
    blank_symbol = 'B'
    initial_state = 'q0'
    accepting_states = {'q_accept'}
    
    transitions = {
        # 初始状态：检查是否为空串
        Transition('q0', 'B', 'q_accept', 'B', Direction.STAY),
        Transition('q0', '0', 'q1', 'X', Direction.RIGHT),
        Transition('q0', '1', 'q1', 'Y', Direction.RIGHT),
        
        # 向右移动，标记已检查的符号
        Transition('q1', '0', 'q1', '0', Direction.RIGHT),
        Transition('q1', '1', 'q1', '1', Direction.RIGHT),
        Transition('q1', 'B', 'q2', 'B', Direction.LEFT),
        
        # 向左移动，检查对称性
        Transition('q2', '0', 'q3', 'X', Direction.LEFT),
        Transition('q2', '1', 'q3', 'Y', Direction.LEFT),
        Transition('q2', 'X', 'q_accept', 'X', Direction.STAY),
        Transition('q2', 'Y', 'q_accept', 'Y', Direction.STAY),
        
        # 继续向左移动
        Transition('q3', '0', 'q3', '0', Direction.LEFT),
        Transition('q3', '1', 'q3', '1', Direction.LEFT),
        Transition('q3', 'X', 'q4', 'X', Direction.RIGHT),
        Transition('q3', 'Y', 'q4', 'Y', Direction.RIGHT),
        
        # 向右移动，继续检查
        Transition('q4', '0', 'q1', 'X', Direction.RIGHT),
        Transition('q4', '1', 'q1', 'Y', Direction.RIGHT),
    }
    
    return TuringMachine(states, alphabet, blank_symbol, initial_state, 
                        accepting_states, transitions)

# 测试
tm = create_palindrome_tm()
test_strings = ['', '0', '1', '00', '11', '01', '010', '101', '0110']

for s in test_strings:
    result = tm.run(s)
    print(f"'{s}' 是回文: {result}")
```

### λ演算

**λ演算基础**

λ演算是函数式编程的理论基础：

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Dict
from dataclasses import dataclass

T = TypeVar('T')

class LambdaTerm(ABC):
    """λ项抽象基类"""
    
    @abstractmethod
    def free_variables(self) -> set[str]:
        """获取自由变量"""
        pass
    
    @abstractmethod
    def substitute(self, var: str, term: 'LambdaTerm') -> 'LambdaTerm':
        """变量替换"""
        pass
    
    @abstractmethod
    def reduce(self) -> Optional['LambdaTerm']:
        """β归约"""
        pass

class Variable(LambdaTerm):
    """变量"""
    
    def __init__(self, name: str):
        self.name = name
    
    def free_variables(self) -> set[str]:
        return {self.name}
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        if self.name == var:
            return term
        else:
            return self
    
    def reduce(self) -> Optional[LambdaTerm]:
        return None
    
    def __str__(self) -> str:
        return self.name

class Abstraction(LambdaTerm):
    """抽象（λ抽象）"""
    
    def __init__(self, parameter: str, body: LambdaTerm):
        self.parameter = parameter
        self.body = body
    
    def free_variables(self) -> set[str]:
        return self.body.free_variables() - {self.parameter}
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        if var == self.parameter:
            return self
        else:
            # 避免变量捕获
            if term.free_variables() & {self.parameter}:
                # 需要α转换
                new_param = self._fresh_variable()
                new_body = self.body.substitute(self.parameter, Variable(new_param))
                return Abstraction(new_param, new_body.substitute(var, term))
            else:
                return Abstraction(self.parameter, self.body.substitute(var, term))
    
    def reduce(self) -> Optional[LambdaTerm]:
        return None
    
    def _fresh_variable(self) -> str:
        """生成新的变量名"""
        import random
        return f"x_{random.randint(1000, 9999)}"
    
    def __str__(self) -> str:
        return f"λ{self.parameter}.{self.body}"

class Application(LambdaTerm):
    """应用"""
    
    def __init__(self, function: LambdaTerm, argument: LambdaTerm):
        self.function = function
        self.argument = argument
    
    def free_variables(self) -> set[str]:
        return self.function.free_variables() | self.argument.free_variables()
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        return Application(
            self.function.substitute(var, term),
            self.argument.substitute(var, term)
        )
    
    def reduce(self) -> Optional[LambdaTerm]:
        # 尝试β归约
        if isinstance(self.function, Abstraction):
            return self.function.body.substitute(
                self.function.parameter, 
                self.argument
            )
        
        # 尝试归约函数部分
        reduced_function = self.function.reduce()
        if reduced_function:
            return Application(reduced_function, self.argument)
        
        # 尝试归约参数部分
        reduced_argument = self.argument.reduce()
        if reduced_argument:
            return Application(self.function, reduced_argument)
        
        return None
    
    def __str__(self) -> str:
        return f"({self.function} {self.argument})"

class LambdaEvaluator:
    """λ演算求值器"""
    
    def __init__(self, max_steps: int = 100):
        self.max_steps = max_steps
    
    def evaluate(self, term: LambdaTerm) -> LambdaTerm:
        """求值λ项"""
        current = term
        steps = 0
        
        while steps < self.max_steps:
            reduced = current.reduce()
            if reduced is None:
                break
            current = reduced
            steps += 1
        
        return current

# 使用示例
def create_identity_function() -> LambdaTerm:
    """创建恒等函数 λx.x"""
    return Abstraction('x', Variable('x'))

def create_constant_function() -> LambdaTerm:
    """创建常函数 λx.λy.x"""
    return Abstraction('x', Abstraction('y', Variable('x')))

def create_application(func: LambdaTerm, arg: LambdaTerm) -> LambdaTerm:
    """创建应用"""
    return Application(func, arg)

# 测试
evaluator = LambdaEvaluator()

# 恒等函数应用
identity = create_identity_function()
arg = Variable('y')
app = create_application(identity, arg)
result = evaluator.evaluate(app)
print(f"恒等函数: {identity}")
print(f"应用: {app}")
print(f"结果: {result}")

# 常函数
const = create_constant_function()
app2 = create_application(create_application(const, Variable('a')), Variable('b'))
result2 = evaluator.evaluate(app2)
print(f"常函数: {const}")
print(f"应用: {app2}")
print(f"结果: {result2}")
```

## 算法理论

### 算法设计

**分治算法**

```python
from typing import List, TypeVar, Callable
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class DivideAndConquer:
    """分治算法框架"""
    
    def divide(self, problem: List[T]) -> List[List[T]]:
        """分解问题"""
        n = len(problem)
        mid = n // 2
        return [problem[:mid], problem[mid:]]
    
    def conquer(self, subproblems: List[List[T]], 
                solve_func: Callable[[List[T]], T]) -> List[T]:
        """解决子问题"""
        return [solve_func(sub) for sub in subproblems]
    
    def combine(self, solutions: List[T]) -> T:
        """合并解"""
        raise NotImplementedError
    
    def solve(self, problem: List[T], 
              solve_func: Callable[[List[T]], T]) -> T:
        """分治求解"""
        if len(problem) <= 1:
            return solve_func(problem)
        
        # 分解
        subproblems = self.divide(problem)
        
        # 解决子问题
        solutions = self.conquer(subproblems, solve_func)
        
        # 合并
        return self.combine(solutions)

class MergeSort(DivideAndConquer[List[int]]):
    """归并排序"""
    
    def combine(self, solutions: List[List[int]]) -> List[int]:
        """合并两个有序数组"""
        if len(solutions) != 2:
            raise ValueError("Merge sort requires exactly 2 subproblems")
        
        left, right = solutions
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
    
    def solve(self, problem: List[int]) -> List[int]:
        """归并排序"""
        if len(problem) <= 1:
            return problem
        
        # 分解
        subproblems = self.divide(problem)
        
        # 递归解决子问题
        solutions = [self.solve(sub) for sub in subproblems]
        
        # 合并
        return self.combine(solutions)

# 使用示例
merge_sort = MergeSort()
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = merge_sort.solve(numbers)
print(f"原始数组: {numbers}")
print(f"排序后: {sorted_numbers}")
```

### 算法分析

**复杂度分析**

```python
import time
import math
from typing import Callable, List, Tuple
from dataclasses import dataclass

@dataclass
class ComplexityAnalysis:
    """算法复杂度分析"""
    
    def time_complexity(self, algorithm: Callable, 
                       input_sizes: List[int]) -> List[float]:
        """时间复杂度分析"""
        times = []
        
        for size in input_sizes:
            # 生成测试数据
            test_data = self._generate_test_data(size)
            
            # 测量时间
            start_time = time.time()
            algorithm(test_data)
            end_time = time.time()
            
            times.append(end_time - start_time)
        
        return times
    
    def space_complexity(self, algorithm: Callable, 
                        input_sizes: List[int]) -> List[int]:
        """空间复杂度分析（简化版）"""
        # 这里只是示例，实际的空间复杂度分析更复杂
        return [size for size in input_sizes]
    
    def _generate_test_data(self, size: int) -> List[int]:
        """生成测试数据"""
        import random
        return [random.randint(1, 1000) for _ in range(size)]
    
    def analyze_growth(self, sizes: List[int], times: List[float]) -> str:
        """分析增长趋势"""
        if len(sizes) < 2:
            return "数据不足"
        
        # 计算增长率
        growth_rates = []
        for i in range(1, len(sizes)):
            size_ratio = sizes[i] / sizes[i-1]
            time_ratio = times[i] / times[i-1]
            growth_rates.append(time_ratio / size_ratio)
        
        avg_growth = sum(growth_rates) / len(growth_rates)
        
        if avg_growth < 0.1:
            return "O(1) - 常数时间"
        elif avg_growth < 1.5:
            return "O(log n) - 对数时间"
        elif avg_growth < 2.5:
            return "O(n) - 线性时间"
        elif avg_growth < 4:
            return "O(n log n) - 线性对数时间"
        elif avg_growth < 8:
            return "O(n²) - 平方时间"
        else:
            return "O(n³) 或更高 - 多项式时间"

# 使用示例
def linear_search(arr: List[int], target: int) -> int:
    """线性搜索 O(n)"""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def binary_search(arr: List[int], target: int) -> int:
    """二分搜索 O(log n)"""
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

# 分析
analyzer = ComplexityAnalysis()
input_sizes = [100, 1000, 10000, 100000]

# 分析线性搜索
linear_times = analyzer.time_complexity(
    lambda arr: linear_search(arr, arr[-1]), 
    input_sizes
)

# 分析二分搜索（需要排序数组）
def sorted_binary_search(arr):
    sorted_arr = sorted(arr)
    return binary_search(sorted_arr, sorted_arr[-1])

binary_times = analyzer.time_complexity(sorted_binary_search, input_sizes)

print("线性搜索复杂度分析:")
for size, time_taken in zip(input_sizes, linear_times):
    print(f"  大小: {size}, 时间: {time_taken:.6f}秒")

print(f"增长趋势: {analyzer.analyze_growth(input_sizes, linear_times)}")

print("\n二分搜索复杂度分析:")
for size, time_taken in zip(input_sizes, binary_times):
    print(f"  大小: {size}, 时间: {time_taken:.6f}秒")

print(f"增长趋势: {analyzer.analyze_growth(input_sizes, binary_times)}")
```

## 数据结构

### 基础数据结构

**栈和队列**

```python
from typing import TypeVar, Generic, Optional
from abc import ABC, abstractmethod

T = TypeVar('T')

class Stack(ABC, Generic[T]):
    """栈抽象基类"""
    
    @abstractmethod
    def push(self, item: T) -> None:
        """入栈"""
        pass
    
    @abstractmethod
    def pop(self) -> Optional[T]:
        """出栈"""
        pass
    
    @abstractmethod
    def peek(self) -> Optional[T]:
        """查看栈顶"""
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """是否为空"""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """栈大小"""
        pass

class ArrayStack(Stack[T]):
    """基于数组的栈实现"""
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        if len(self.items) >= self.capacity:
            raise OverflowError("Stack is full")
        self.items.append(item)
    
    def pop(self) -> Optional[T]:
        if self.is_empty():
            return None
        return self.items.pop()
    
    def peek(self) -> Optional[T]:
        if self.is_empty():
            return None
        return self.items[-1]
    
    def is_empty(self) -> bool:
        return len(self.items) == 0
    
    def size(self) -> int:
        return len(self.items)

class Queue(ABC, Generic[T]):
    """队列抽象基类"""
    
    @abstractmethod
    def enqueue(self, item: T) -> None:
        """入队"""
        pass
    
    @abstractmethod
    def dequeue(self) -> Optional[T]:
        """出队"""
        pass
    
    @abstractmethod
    def front(self) -> Optional[T]:
        """查看队首"""
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """是否为空"""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """队列大小"""
        pass

class ArrayQueue(Queue[T]):
    """基于数组的队列实现"""
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.items: List[T] = []
    
    def enqueue(self, item: T) -> None:
        if len(self.items) >= self.capacity:
            raise OverflowError("Queue is full")
        self.items.append(item)
    
    def dequeue(self) -> Optional[T]:
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def front(self) -> Optional[T]:
        if self.is_empty():
            return None
        return self.items[0]
    
    def is_empty(self) -> bool:
        return len(self.items) == 0
    
    def size(self) -> int:
        return len(self.items)

# 使用示例
print("=== 栈操作 ===")
stack = ArrayStack[int](10)
stack.push(1)
stack.push(2)
stack.push(3)
print(f"栈大小: {stack.size()}")
print(f"栈顶: {stack.peek()}")
print(f"出栈: {stack.pop()}")
print(f"栈顶: {stack.peek()}")

print("\n=== 队列操作 ===")
queue = ArrayQueue[int](10)
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(f"队列大小: {queue.size()}")
print(f"队首: {queue.front()}")
print(f"出队: {queue.dequeue()}")
print(f"队首: {queue.front()}")
```

## 编程语言理论

### 类型理论

**简单类型系统**

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, Optional
from dataclasses import dataclass

T = TypeVar('T')

class Type(ABC):
    """类型抽象基类"""
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass

class BasicType(Type):
    """基本类型"""
    
    def __init__(self, name: str):
        self.name = name
    
    def __eq__(self, other) -> bool:
        return isinstance(other, BasicType) and self.name == other.name
    
    def __str__(self) -> str:
        return self.name

class FunctionType(Type):
    """函数类型"""
    
    def __init__(self, domain: Type, codomain: Type):
        self.domain = domain
        self.codomain = codomain
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, FunctionType) and 
                self.domain == other.domain and 
                self.codomain == other.codomain)
    
    def __str__(self) -> str:
        return f"({self.domain} -> {self.codomain})"

class Expression(ABC):
    """表达式抽象基类"""
    
    @abstractmethod
    def type_check(self, context: Dict[str, Type]) -> Optional[Type]:
        """类型检查"""
        pass
    
    @abstractmethod
    def evaluate(self, context: Dict[str, T]) -> T:
        """求值"""
        pass

class Variable(Expression):
    """变量"""
    
    def __init__(self, name: str):
        self.name = name
    
    def type_check(self, context: Dict[str, Type]) -> Optional[Type]:
        return context.get(self.name)
    
    def evaluate(self, context: Dict[str, T]) -> T:
        return context[self.name]

class Lambda(Expression):
    """λ抽象"""
    
    def __init__(self, parameter: str, parameter_type: Type, body: Expression):
        self.parameter = parameter
        self.parameter_type = parameter_type
        self.body = body
    
    def type_check(self, context: Dict[str, Type]) -> Optional[Type]:
        new_context = context.copy()
        new_context[self.parameter] = self.parameter_type
        
        body_type = self.body.type_check(new_context)
        if body_type:
            return FunctionType(self.parameter_type, body_type)
        return None
    
    def evaluate(self, context: Dict[str, T]) -> T:
        # 返回一个函数
        def func(arg: T) -> T:
            new_context = context.copy()
            new_context[self.parameter] = arg
            return self.body.evaluate(new_context)
        return func

class Application(Expression):
    """函数应用"""
    
    def __init__(self, function: Expression, argument: Expression):
        self.function = function
        self.argument = argument
    
    def type_check(self, context: Dict[str, Type]) -> Optional[Type]:
        func_type = self.function.type_check(context)
        arg_type = self.argument.type_check(context)
        
        if (isinstance(func_type, FunctionType) and 
            func_type.domain == arg_type):
            return func_type.codomain
        return None
    
    def evaluate(self, context: Dict[str, T]) -> T:
        func = self.function.evaluate(context)
        arg = self.argument.evaluate(context)
        return func(arg)

class TypeChecker:
    """类型检查器"""
    
    def __init__(self):
        self.context: Dict[str, Type] = {}
    
    def add_variable(self, name: str, type_: Type) -> None:
        """添加变量到上下文"""
        self.context[name] = type_
    
    def check_expression(self, expr: Expression) -> Optional[Type]:
        """检查表达式类型"""
        return expr.type_check(self.context)
    
    def is_well_typed(self, expr: Expression) -> bool:
        """判断表达式是否类型正确"""
        return self.check_expression(expr) is not None

# 使用示例
# 定义基本类型
int_type = BasicType("Int")
bool_type = BasicType("Bool")

# 创建类型检查器
checker = TypeChecker()
checker.add_variable("x", int_type)
checker.add_variable("y", int_type)

# 创建表达式: λx:Int.x (恒等函数)
identity = Lambda("x", int_type, Variable("x"))
identity_type = checker.check_expression(identity)
print(f"恒等函数类型: {identity_type}")

# 创建表达式: (λx:Int.x) 5
application = Application(identity, Variable("x"))
application_type = checker.check_expression(application)
print(f"应用类型: {application_type}")

# 检查类型正确性
print(f"恒等函数类型正确: {checker.is_well_typed(identity)}")
print(f"应用类型正确: {checker.is_well_typed(application)}")
```

## 并发理论

### 进程代数

**CCS (Calculus of Communicating Systems)**

```python
from abc import ABC, abstractmethod
from typing import Set, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class Action(Enum):
    """动作类型"""
    TAU = "τ"  # 内部动作

@dataclass
class Process(ABC):
    """进程抽象基类"""
    
    @abstractmethod
    def actions(self) -> Set[str]:
        """获取可能的动作"""
        pass
    
    @abstractmethod
    def can_perform(self, action: str) -> bool:
        """是否可以执行动作"""
        pass
    
    @abstractmethod
    def perform(self, action: str) -> Optional['Process']:
        """执行动作"""
        pass

class Nil(Process):
    """空进程"""
    
    def actions(self) -> Set[str]:
        return set()
    
    def can_perform(self, action: str) -> bool:
        return False
    
    def perform(self, action: str) -> Optional[Process]:
        return None
    
    def __str__(self) -> str:
        return "0"

class Prefix(Process):
    """前缀进程 a.P"""
    
    def __init__(self, action: str, continuation: Process):
        self.action = action
        self.continuation = continuation
    
    def actions(self) -> Set[str]:
        return {self.action}
    
    def can_perform(self, action: str) -> bool:
        return action == self.action
    
    def perform(self, action: str) -> Optional[Process]:
        if action == self.action:
            return self.continuation
        return None
    
    def __str__(self) -> str:
        return f"{self.action}.{self.continuation}"

class Choice(Process):
    """选择进程 P + Q"""
    
    def __init__(self, left: Process, right: Process):
        self.left = left
        self.right = right
    
    def actions(self) -> Set[str]:
        return self.left.actions() | self.right.actions()
    
    def can_perform(self, action: str) -> bool:
        return self.left.can_perform(action) or self.right.can_perform(action)
    
    def perform(self, action: str) -> Optional[Process]:
        if self.left.can_perform(action):
            return self.left.perform(action)
        elif self.right.can_perform(action):
            return self.right.perform(action)
        return None
    
    def __str__(self) -> str:
        return f"({self.left} + {self.right})"

class Parallel(Process):
    """并行进程 P | Q"""
    
    def __init__(self, left: Process, right: Process):
        self.left = left
        self.right = right
    
    def actions(self) -> Set[str]:
        return self.left.actions() | self.right.actions()
    
    def can_perform(self, action: str) -> bool:
        return self.left.can_perform(action) or self.right.can_perform(action)
    
    def perform(self, action: str) -> Optional[Process]:
        left_result = self.left.perform(action)
        right_result = self.right.perform(action)
        
        if left_result and right_result:
            return Parallel(left_result, right_result)
        elif left_result:
            return Parallel(left_result, self.right)
        elif right_result:
            return Parallel(self.left, right_result)
        return None
    
    def __str__(self) -> str:
        return f"({self.left} | {self.right})"

class ProcessSimulator:
    """进程模拟器"""
    
    def __init__(self, process: Process):
        self.process = process
    
    def simulate(self, actions: List[str]) -> bool:
        """模拟动作序列"""
        current = self.process
        
        for action in actions:
            if current.can_perform(action):
                result = current.perform(action)
                if result:
                    current = result
                else:
                    return False
            else:
                return False
        
        return True
    
    def get_trace(self) -> List[str]:
        """获取可能的执行轨迹"""
        # 简化实现，实际需要更复杂的算法
        return list(self.process.actions())

# 使用示例
# 创建进程: a.b.0 + c.0
process1 = Choice(
    Prefix("a", Prefix("b", Nil())),
    Prefix("c", Nil())
)

# 创建进程: a.0 | b.0
process2 = Parallel(
    Prefix("a", Nil()),
    Prefix("b", Nil())
)

# 模拟
simulator1 = ProcessSimulator(process1)
simulator2 = ProcessSimulator(process2)

print(f"进程1: {process1}")
print(f"进程2: {process2}")

print(f"进程1可以执行 ['a', 'b']: {simulator1.simulate(['a', 'b'])}")
print(f"进程1可以执行 ['c']: {simulator1.simulate(['c'])}")
print(f"进程1可以执行 ['a', 'c']: {simulator1.simulate(['a', 'c'])}")

print(f"进程2可以执行 ['a']: {simulator2.simulate(['a'])}")
print(f"进程2可以执行 ['b']: {simulator2.simulate(['b'])}")
print(f"进程2可以执行 ['a', 'b']: {simulator2.simulate(['a', 'b'])}")
```

## 总结

理论基础层为软件工程提供了坚实的计算机科学理论基础：

1. **计算模型**：图灵机、λ演算、递归函数等计算模型
2. **算法理论**：算法设计、分析、优化等核心理论
3. **数据结构**：基础数据结构、抽象数据类型等
4. **编程语言理论**：语法、语义、类型理论等
5. **并发理论**：进程代数、时序逻辑、死锁理论等

这些理论基础将指导后续各层的具体实现，确保软件系统的正确性、效率和可靠性。

---

**相关链接**:

- [01-形式科学](../01-形式科学/README.md) - 数学和逻辑基础
- [03-具体科学](../03-具体科学/README.md) - 软件工程理论
- [04-行业领域](../04-行业领域/README.md) - 应用领域

**更新时间**: 2024年12月
**版本**: 1.0.0
