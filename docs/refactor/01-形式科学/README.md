# 01. 形式科学层

## 概述

形式科学层是软件工程知识体系的数学和逻辑基础，提供形式化表达、数学建模和逻辑推理的理论支撑。本层建立从具体问题到抽象数学模型的桥梁。

## 目录结构

```
01-形式科学/
├── 01-数学基础/
│   ├── 01-集合论.md
│   ├── 02-关系理论.md
│   ├── 03-函数理论.md
│   ├── 04-代数结构.md
│   ├── 05-序理论.md
│   └── 06-图论基础.md
├── 02-逻辑理论/
│   ├── 01-命题逻辑.md
│   ├── 02-谓词逻辑.md
│   ├── 03-模态逻辑.md
│   ├── 04-时序逻辑.md
│   └── 05-直觉逻辑.md
├── 03-形式化方法/
│   ├── 01-形式化规约.md
│   ├── 02-形式化验证.md
│   ├── 03-模型检测.md
│   ├── 04-定理证明.md
│   └── 05-抽象解释.md
├── 04-计算理论/
│   ├── 01-自动机理论.md
│   ├── 02-形式语言.md
│   ├── 03-可计算性.md
│   ├── 04-复杂性理论.md
│   └── 05-算法分析.md
├── 05-概率统计/
│   ├── 01-概率论基础.md
│   ├── 02-随机过程.md
│   ├── 03-统计推断.md
│   ├── 04-信息论.md
│   └── 05-机器学习数学.md
└── README.md
```

## 核心理念

### 1. 形式化表达

将软件系统的概念、行为和性质用精确的数学语言表达：

- **精确性**：消除歧义，提供精确的定义
- **抽象性**：从具体实现中抽象出本质特征
- **通用性**：适用于多种具体场景
- **可推理性**：支持逻辑推理和证明

### 2. 数学建模

建立软件系统的数学模型：

- **状态模型**：系统状态的形式化描述
- **行为模型**：系统行为的形式化表达
- **结构模型**：系统结构的形式化表示
- **关系模型**：系统间关系的数学描述

### 3. 逻辑推理

基于形式化表达进行逻辑推理：

- **演绎推理**：从一般到特殊的推理
- **归纳推理**：从特殊到一般的推理
- **反证法**：通过否定结论来证明
- **构造性证明**：通过构造来证明存在性

## 数学基础

### 集合论基础

**集合的基本概念**

集合是数学的基础概念，在软件工程中有广泛应用：

$$\text{Set} = \{x \mid P(x)\}$$

其中 $P(x)$ 是谓词，定义集合中元素的性质。

```python
from typing import TypeVar, Generic, Set, Iterator
from abc import ABC, abstractmethod

T = TypeVar('T')

class Set(ABC, Generic[T]):
    """集合抽象基类"""
    
    @abstractmethod
    def contains(self, element: T) -> bool:
        """判断元素是否属于集合"""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """集合大小"""
        pass
    
    @abstractmethod
    def iterator(self) -> Iterator[T]:
        """集合迭代器"""
        pass
    
    def union(self, other: 'Set[T]') -> 'Set[T]':
        """并集"""
        return UnionSet(self, other)
    
    def intersection(self, other: 'Set[T]') -> 'Set[T]':
        """交集"""
        return IntersectionSet(self, other)
    
    def difference(self, other: 'Set[T]') -> 'Set[T]':
        """差集"""
        return DifferenceSet(self, other)

class FiniteSet(Set[T]):
    """有限集合"""
    
    def __init__(self, elements: Set[T]):
        self.elements = elements
    
    def contains(self, element: T) -> bool:
        return element in self.elements
    
    def size(self) -> int:
        return len(self.elements)
    
    def iterator(self) -> Iterator[T]:
        return iter(self.elements)

# 使用示例
set1 = FiniteSet({1, 2, 3})
set2 = FiniteSet({3, 4, 5})
print(f"1 in set1: {set1.contains(1)}")  # True
print(f"4 in set1: {set1.contains(4)}")  # False
```

### 关系理论

**二元关系**

二元关系是集合论的重要概念，在软件工程中用于建模对象间的关系：

$$R \subseteq A \times B$$

其中 $A$ 和 $B$ 是集合，$R$ 是它们之间的二元关系。

```python
from typing import TypeVar, Generic, Set, Tuple
from dataclasses import dataclass

A = TypeVar('A')
B = TypeVar('B')

@dataclass
class BinaryRelation(Generic[A, B]):
    """二元关系"""
    domain: Set[A]
    codomain: Set[B]
    pairs: Set[Tuple[A, B]]
    
    def contains(self, a: A, b: B) -> bool:
        """判断关系是否包含对 (a, b)"""
        return (a, b) in self.pairs
    
    def is_function(self) -> bool:
        """判断是否为函数（每个域元素最多对应一个值域元素）"""
        for a in self.domain:
            codomain_elements = {b for (x, b) in self.pairs if x == a}
            if len(codomain_elements) > 1:
                return False
        return True

# 使用示例
domain = {1, 2, 3}
codomain = {'a', 'b', 'c'}
pairs = {(1, 'a'), (2, 'b'), (3, 'c')}

relation = BinaryRelation(domain, codomain, pairs)
print(f"是函数: {relation.is_function()}")  # True
```

### 函数理论

**函数的形式化定义**

函数是特殊的二元关系，在软件工程中用于建模计算过程：

$$f: A \rightarrow B$$

其中 $f$ 是函数，$A$ 是定义域，$B$ 是值域。

```python
from typing import TypeVar, Generic, Callable
from dataclasses import dataclass

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

@dataclass
class Function(Generic[A, B]):
    """函数"""
    domain: type[A]
    codomain: type[B]
    implementation: Callable[[A], B]
    
    def apply(self, a: A) -> B:
        """函数应用"""
        return self.implementation(a)
    
    def compose(self, other: 'Function[B, C]') -> 'Function[A, C]':
        """函数复合"""
        def composed(a: A) -> C:
            return other.apply(self.apply(a))
        return Function(self.domain, other.codomain, composed)

# 使用示例
def square(x: int) -> int:
    return x ** 2

def double(x: int) -> int:
    return x * 2

f = Function(int, int, square)
g = Function(int, int, double)

# 函数应用
print(f"f(3) = {f.apply(3)}")  # 9
print(f"g(3) = {g.apply(3)}")  # 6

# 函数复合
h = f.compose(g)
print(f"h(3) = {h.apply(3)}")  # 36
```

### 代数结构

**群论应用**

群论在软件工程中用于建模具有对称性的系统：

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Group(ABC, Generic[T]):
    """群抽象基类"""
    
    @abstractmethod
    def identity(self) -> T:
        """单位元"""
        pass
    
    @abstractmethod
    def operation(self, a: T, b: T) -> T:
        """群运算"""
        pass
    
    @abstractmethod
    def inverse(self, a: T) -> T:
        """逆元"""
        pass

class IntegerGroup(Group[int]):
    """整数加法群"""
    
    def identity(self) -> int:
        return 0
    
    def operation(self, a: int, b: int) -> int:
        return a + b
    
    def inverse(self, a: int) -> int:
        return -a

# 使用示例
group = IntegerGroup()
print(f"单位元: {group.identity()}")  # 0
print(f"3 + 5 = {group.operation(3, 5)}")  # 8
print(f"3 的逆元: {group.inverse(3)}")  # -3
```

## 逻辑理论

### 命题逻辑

**命题逻辑基础**

命题逻辑是形式逻辑的基础，用于建模简单的逻辑关系：

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Proposition:
    """命题"""
    name: str
    value: bool
    
    def __str__(self) -> str:
        return f"{self.name} = {self.value}"

class LogicalOperator(ABC):
    """逻辑运算符抽象基类"""
    
    @abstractmethod
    def evaluate(self, *args: bool) -> bool:
        """计算逻辑值"""
        pass
    
    @abstractmethod
    def symbol(self) -> str:
        """运算符符号"""
        pass

class AndOperator(LogicalOperator):
    """与运算符"""
    
    def evaluate(self, *args: bool) -> bool:
        return all(args)
    
    def symbol(self) -> str:
        return "∧"

class OrOperator(LogicalOperator):
    """或运算符"""
    
    def evaluate(self, *args: bool) -> bool:
        return any(args)
    
    def symbol(self) -> str:
        return "∨"

class NotOperator(LogicalOperator):
    """非运算符"""
    
    def evaluate(self, *args: bool) -> bool:
        if len(args) != 1:
            raise ValueError("Not operator takes exactly one argument")
        return not args[0]
    
    def symbol(self) -> str:
        return "¬"

# 使用示例
p = Proposition("P", True)
q = Proposition("Q", False)

# 创建逻辑表达式: P ∧ ¬Q
not_q = LogicalExpression(NotOperator(), [q])
expression = LogicalExpression(AndOperator(), [p, not_q])

print(f"表达式: {expression}")
print(f"结果: {expression.evaluate()}")  # True
```

### 谓词逻辑

**谓词逻辑扩展**

谓词逻辑扩展了命题逻辑，能够表达更复杂的逻辑关系：

```python
from typing import TypeVar, Generic, Callable, Set
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class Predicate(Generic[T]):
    """谓词"""
    name: str
    function: Callable[[T], bool]
    
    def apply(self, x: T) -> bool:
        """应用谓词"""
        return self.function(x)

class Quantifier(ABC):
    """量词抽象基类"""
    
    @abstractmethod
    def evaluate(self, predicate: Predicate[T], domain: Set[T]) -> bool:
        """计算量词的值"""
        pass
    
    @abstractmethod
    def symbol(self) -> str:
        """量词符号"""
        pass

class UniversalQuantifier(Quantifier[T]):
    """全称量词 ∀"""
    
    def evaluate(self, predicate: Predicate[T], domain: Set[T]) -> bool:
        return all(predicate.apply(x) for x in domain)
    
    def symbol(self) -> str:
        return "∀"

class ExistentialQuantifier(Quantifier[T]):
    """存在量词 ∃"""
    
    def evaluate(self, predicate: Predicate[T], domain: Set[T]) -> bool:
        return any(predicate.apply(x) for x in domain)
    
    def symbol(self) -> str:
        return "∃"

# 使用示例
domain = {1, 2, 3, 4, 5}
is_even = Predicate("Even", lambda x: x % 2 == 0)
is_positive = Predicate("Positive", lambda x: x > 0)

# 全称量词：所有数都是正数
universal_expr = QuantifiedExpression(
    UniversalQuantifier(),
    "x",
    is_positive,
    domain
)

# 存在量词：存在偶数
existential_expr = QuantifiedExpression(
    ExistentialQuantifier(),
    "x",
    is_even,
    domain
)

print(f"{universal_expr} = {universal_expr.evaluate()}")  # True
print(f"{existential_expr} = {existential_expr.evaluate()}")  # True
```

## 形式化方法

### 形式化规约

**Z 记法示例**

Z 记法是一种形式化规约语言，用于精确描述软件系统的行为：

```python
from typing import Dict
from dataclasses import dataclass

class BankAccount:
    """银行账户系统"""
    
    def __init__(self):
        self.accounts: Dict[str, int] = {}
        self.max_balance = 1000000
    
    def open_account(self, account_id: str, initial_balance: int) -> bool:
        """开户操作"""
        # 前置条件
        if account_id in self.accounts:
            return False  # 账户已存在
        
        if initial_balance < 0 or initial_balance > self.max_balance:
            return False  # 余额超出范围
        
        # 后置条件
        self.accounts[account_id] = initial_balance
        return True
    
    def deposit(self, account_id: str, amount: int) -> bool:
        """存款操作"""
        # 前置条件
        if account_id not in self.accounts:
            return False  # 账户不存在
        
        if amount <= 0:
            return False  # 存款金额必须为正
        
        current_balance = self.accounts[account_id]
        if current_balance + amount > self.max_balance:
            return False  # 余额超出上限
        
        # 后置条件
        self.accounts[account_id] = current_balance + amount
        return True
    
    def withdraw(self, account_id: str, amount: int) -> bool:
        """取款操作"""
        # 前置条件
        if account_id not in self.accounts:
            return False  # 账户不存在
        
        if amount <= 0:
            return False  # 取款金额必须为正
        
        current_balance = self.accounts[account_id]
        if current_balance < amount:
            return False  # 余额不足
        
        # 后置条件
        self.accounts[account_id] = current_balance - amount
        return True

# 使用示例
bank = BankAccount()

# 开户
print(f"开户成功: {bank.open_account('A001', 1000)}")  # True
print(f"开户成功: {bank.open_account('A002', 500)}")   # True

# 存款
print(f"存款成功: {bank.deposit('A001', 200)}")  # True

# 取款
print(f"取款成功: {bank.withdraw('A001', 300)}")  # True

# 违反前置条件
print(f"取款失败: {bank.withdraw('A001', 1000)}")  # False (余额不足)
print(f"存款失败: {bank.deposit('A003', 100)}")   # False (账户不存在)
```

### 模型检测

**状态机模型检测**

模型检测是一种自动化的形式化验证方法：

```python
from typing import Set, List, Optional
from dataclasses import dataclass
from enum import Enum

class State(Enum):
    """系统状态"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"

class Event(Enum):
    """系统事件"""
    START = "start"
    COMPLETE = "complete"
    FAIL = "fail"
    RESET = "reset"

@dataclass
class Transition:
    """状态转移"""
    from_state: State
    event: Event
    to_state: State
    condition: Optional[str] = None

class StateMachine:
    """状态机"""
    
    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.transitions: List[Transition] = []
        self.states: Set[State] = {initial_state}
    
    def add_transition(self, transition: Transition) -> None:
        """添加状态转移"""
        self.transitions.append(transition)
        self.states.add(transition.from_state)
        self.states.add(transition.to_state)
    
    def can_transition(self, event: Event) -> bool:
        """检查是否可以执行转移"""
        for transition in self.transitions:
            if (transition.from_state == self.current_state and 
                transition.event == event):
                return True
        return False
    
    def transition(self, event: Event) -> bool:
        """执行状态转移"""
        for transition in self.transitions:
            if (transition.from_state == self.current_state and 
                transition.event == event):
                self.current_state = transition.to_state
                return True
        return False
    
    def get_reachable_states(self) -> Set[State]:
        """获取可达状态"""
        reachable = {self.current_state}
        changed = True
        
        while changed:
            changed = False
            for transition in self.transitions:
                if transition.from_state in reachable:
                    if transition.to_state not in reachable:
                        reachable.add(transition.to_state)
                        changed = True
        
        return reachable

class ModelChecker:
    """模型检测器"""
    
    def __init__(self, state_machine: StateMachine):
        self.state_machine = state_machine
    
    def check_safety_property(self, bad_states: Set[State]) -> bool:
        """检查安全性质（永远不进入坏状态）"""
        reachable = self.state_machine.get_reachable_states()
        return reachable.isdisjoint(bad_states)
    
    def check_liveness_property(self, good_states: Set[State]) -> bool:
        """检查活性性质（最终会进入好状态）"""
        reachable = self.state_machine.get_reachable_states()
        return not reachable.isdisjoint(good_states)

# 使用示例
# 创建状态机
fsm = StateMachine(State.IDLE)

# 添加转移
fsm.add_transition(Transition(State.IDLE, Event.START, State.BUSY))
fsm.add_transition(Transition(State.BUSY, Event.COMPLETE, State.IDLE))
fsm.add_transition(Transition(State.BUSY, Event.FAIL, State.ERROR))
fsm.add_transition(Transition(State.ERROR, Event.RESET, State.IDLE))

# 创建模型检测器
checker = ModelChecker(fsm)

# 检查安全性质：永远不会进入错误状态
safety_result = checker.check_safety_property({State.ERROR})
print(f"安全性质检查: {safety_result}")  # False (可能进入错误状态)

# 检查活性性质：最终会回到空闲状态
liveness_result = checker.check_liveness_property({State.IDLE})
print(f"活性性质检查: {liveness_result}")  # True
```

## 计算理论

### 自动机理论

**有限状态自动机**

```python
from typing import Set, Dict, Tuple, Optional, List
from dataclasses import dataclass

@dataclass
class FiniteStateAutomaton:
    """有限状态自动机"""
    states: Set[str]
    alphabet: Set[str]
    transitions: Dict[Tuple[str, str], Set[str]]
    initial_state: str
    accepting_states: Set[str]
    
    def transition(self, current_states: Set[str], symbol: str) -> Set[str]:
        """状态转移"""
        next_states = set()
        for state in current_states:
            key = (state, symbol)
            if key in self.transitions:
                next_states.update(self.transitions[key])
        return next_states
    
    def accepts(self, input_string: str) -> bool:
        """判断是否接受输入字符串"""
        current_states = {self.initial_state}
        
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            current_states = self.transition(current_states, symbol)
            if not current_states:
                return False
        
        return bool(current_states & self.accepting_states)
    
    def is_deterministic(self) -> bool:
        """判断是否为确定性自动机"""
        for (state, symbol), next_states in self.transitions.items():
            if len(next_states) > 1:
                return False
        return True

# 使用示例：识别以 'ab' 结尾的字符串
fsa = FiniteStateAutomaton(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        ('q0', 'a'): {'q1'},
        ('q0', 'b'): {'q0'},
        ('q1', 'a'): {'q1'},
        ('q1', 'b'): {'q2'},
        ('q2', 'a'): {'q1'},
        ('q2', 'b'): {'q0'}
    },
    initial_state='q0',
    accepting_states={'q2'}
)

# 测试
test_strings = ['ab', 'aab', 'abb', 'abab', 'ba']
for s in test_strings:
    result = fsa.accepts(s)
    print(f"'{s}' 被接受: {result}")
```

### 形式语言

**正则表达式引擎**

```python
from typing import Optional, Set, List
from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    """词法单元类型"""
    CHAR = "char"
    STAR = "*"
    PLUS = "+"
    QUESTION = "?"
    OR = "|"
    LPAREN = "("
    RPAREN = ")"

@dataclass
class Token:
    """词法单元"""
    type: TokenType
    value: str

class RegexParser:
    """正则表达式解析器"""
    
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.tokens = self.tokenize()
        self.pos = 0
    
    def tokenize(self) -> List[Token]:
        """词法分析"""
        tokens = []
        i = 0
        while i < len(self.pattern):
            char = self.pattern[i]
            if char == '*':
                tokens.append(Token(TokenType.STAR, char))
            elif char == '+':
                tokens.append(Token(TokenType.PLUS, char))
            elif char == '?':
                tokens.append(Token(TokenType.QUESTION, char))
            elif char == '|':
                tokens.append(Token(TokenType.OR, char))
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, char))
            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, char))
            else:
                tokens.append(Token(TokenType.CHAR, char))
            i += 1
        return tokens

class RegexEngine:
    """正则表达式引擎"""
    
    def __init__(self, pattern: str):
        parser = RegexParser(pattern)
        self.ast = parser.parse()
    
    def match(self, text: str) -> bool:
        """完全匹配"""
        matches = self.ast.matches(text, 0)
        return len(text) in matches
    
    def search(self, text: str) -> Optional[int]:
        """搜索匹配"""
        for i in range(len(text) + 1):
            matches = self.ast.matches(text, i)
            if matches:
                return i
        return None

# 使用示例
patterns = ['a*', 'a+', 'ab', 'a|b', '(ab)*']
test_strings = ['', 'a', 'aa', 'ab', 'aba', 'b']

for pattern in patterns:
    print(f"\n模式: {pattern}")
    engine = RegexEngine(pattern)
    for text in test_strings:
        result = engine.match(text)
        print(f"  '{text}' -> {result}")
```

## 概率统计

### 概率论基础

**概率分布**

```python
from typing import TypeVar, Generic, Dict, List, Callable
from abc import ABC, abstractmethod
import random
import math

T = TypeVar('T')

class ProbabilityDistribution(ABC, Generic[T]):
    """概率分布抽象基类"""
    
    @abstractmethod
    def probability(self, value: T) -> float:
        """计算概率"""
        pass
    
    @abstractmethod
    def sample(self) -> T:
        """采样"""
        pass
    
    @abstractmethod
    def expectation(self) -> float:
        """期望"""
        pass
    
    @abstractmethod
    def variance(self) -> float:
        """方差"""
        pass

class DiscreteDistribution(ProbabilityDistribution[T]):
    """离散分布"""
    
    def __init__(self, probabilities: Dict[T, float]):
        self.probabilities = probabilities
        self._validate()
    
    def _validate(self) -> None:
        """验证概率分布"""
        total = sum(self.probabilities.values())
        if not math.isclose(total, 1.0, abs_tol=1e-6):
            raise ValueError(f"Probabilities must sum to 1, got {total}")
    
    def probability(self, value: T) -> float:
        return self.probabilities.get(value, 0.0)
    
    def sample(self) -> T:
        r = random.random()
        cumulative = 0.0
        
        for value, prob in self.probabilities.items():
            cumulative += prob
            if r <= cumulative:
                return value
        
        # 处理浮点误差
        return list(self.probabilities.keys())[-1]
    
    def expectation(self) -> float:
        if not all(isinstance(k, (int, float)) for k in self.probabilities.keys()):
            raise ValueError("Expectation only defined for numeric values")
        return sum(value * prob for value, prob in self.probabilities.items())
    
    def variance(self) -> float:
        if not all(isinstance(k, (int, float)) for k in self.probabilities.keys()):
            raise ValueError("Variance only defined for numeric values")
        mean = self.expectation()
        return sum(prob * (value - mean) ** 2 for value, prob in self.probabilities.items())

class BernoulliDistribution(DiscreteDistribution[int]):
    """伯努利分布"""
    
    def __init__(self, p: float):
        super().__init__({0: 1 - p, 1: p})
        self.p = p
    
    def expectation(self) -> float:
        return self.p
    
    def variance(self) -> float:
        return self.p * (1 - self.p)

# 使用示例
print("=== 伯努利分布 ===")
bernoulli = BernoulliDistribution(0.3)
print(f"期望: {bernoulli.expectation()}")
print(f"方差: {bernoulli.variance()}")
samples = [bernoulli.sample() for _ in range(10)]
print(f"样本: {samples}")
```

## 总结

形式科学层为软件工程提供了坚实的数学和逻辑基础：

1. **数学基础**：集合论、关系理论、函数理论、代数结构
2. **逻辑理论**：命题逻辑、谓词逻辑、形式化推理
3. **形式化方法**：形式化规约、模型检测、定理证明
4. **计算理论**：自动机理论、形式语言、可计算性
5. **概率统计**：概率分布、随机过程、统计推断

这些理论基础将指导后续各层的具体实现，确保软件系统的正确性、可靠性和可验证性。

---

**相关链接**:

- [00-理念基础](../00-理念基础/README.md) - 软件工程哲学基础
- [02-理论基础](../02-理论基础/README.md) - 计算理论基础
- [03-具体科学](../03-具体科学/README.md) - 软件工程理论

**更新时间**: 2024年12月
**版本**: 1.0.0
