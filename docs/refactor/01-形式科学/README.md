# 01. 形式科学 - 数学、逻辑与形式化理论

## 目录结构

```text
01-形式科学/
├── README.md                    # 本文件
├── 01-数学基础/                 # 基础数学理论
│   ├── 01-集合论.md            # 集合、关系、函数
│   ├── 02-数论.md              # 数论基础
│   ├── 03-代数结构.md          # 群、环、域
│   └── 04-分析基础.md          # 微积分、极限、连续
├── 02-逻辑系统/                 # 逻辑推理系统
│   ├── 01-命题逻辑.md          # 命题逻辑基础
│   ├── 02-谓词逻辑.md          # 一阶谓词逻辑
│   ├── 03-模态逻辑.md          # 模态逻辑系统
│   └── 04-类型论.md            # 类型理论和构造逻辑
├── 03-形式化方法/               # 形式化建模方法
│   ├── 01-自动机理论.md        # 有限自动机、图灵机
│   ├── 02-形式语言.md          # 文法、语言理论
│   ├── 03-计算理论.md          # 可计算性、复杂性
│   └── 04-程序语义.md          # 操作语义、指称语义
└── 04-证明系统/                 # 形式化证明
    ├── 01-自然演绎.md          # 自然演绎系统
    ├── 02-公理化系统.md        # 公理化方法
    ├── 03-归纳证明.md          # 数学归纳法
    └── 04-构造性证明.md        # 构造性数学
```

## 核心理念

### 1. 数学基础

形式科学建立在严格的数学基础之上，为软件工程提供精确的数学工具和理论支撑。

**核心内容**:

- **集合论**: 数学的基础语言
- **数论**: 密码学和算法的基础
- **代数结构**: 抽象代数的应用
- **分析基础**: 连续数学的工具

### 2. 逻辑系统

逻辑是推理和证明的基础，为程序正确性提供形式化保证。

**逻辑体系**:

- **命题逻辑**: 基本推理规则
- **谓词逻辑**: 量化推理
- **模态逻辑**: 可能性和必然性
- **类型论**: 构造性逻辑

### 3. 形式化方法

形式化方法为软件系统的建模、分析和验证提供数学基础。

**方法体系**:

- **自动机理论**: 计算模型
- **形式语言**: 语言理论
- **计算理论**: 可计算性理论
- **程序语义**: 程序含义的数学描述

## 形式化表示

### 集合论基础

设 $U$ 为全集，$A, B \subseteq U$，则基本集合运算定义为：

**并集**: $A \cup B = \{x \in U \mid x \in A \lor x \in B\}$

**交集**: $A \cap B = \{x \in U \mid x \in A \land x \in B\}$

**差集**: $A \setminus B = \{x \in U \mid x \in A \land x \notin B\}$

**补集**: $A^c = U \setminus A = \{x \in U \mid x \notin A\}$

### 关系理论

**二元关系**: $R \subseteq A \times B$

**等价关系**: 关系 $R$ 是等价关系当且仅当：

1. **自反性**: $\forall x \in A, (x, x) \in R$
2. **对称性**: $\forall x, y \in A, (x, y) \in R \Rightarrow (y, x) \in R$
3. **传递性**: $\forall x, y, z \in A, (x, y) \in R \land (y, z) \in R \Rightarrow (x, z) \in R$

### 函数理论

**函数定义**: $f: A \rightarrow B$ 是函数当且仅当：

- $\forall x \in A, \exists! y \in B, f(x) = y$

**函数性质**:

- **单射**: $\forall x_1, x_2 \in A, f(x_1) = f(x_2) \Rightarrow x_1 = x_2$
- **满射**: $\forall y \in B, \exists x \in A, f(x) = y$
- **双射**: 既是单射又是满射

### 逻辑系统

**命题逻辑**:

- **原子命题**: $p, q, r, \ldots$
- **逻辑连接词**: $\neg, \land, \lor, \rightarrow, \leftrightarrow$
- **真值表**: 定义逻辑运算

**谓词逻辑**:

- **个体变量**: $x, y, z, \ldots$
- **谓词符号**: $P(x), Q(x, y), \ldots$
- **量词**: $\forall, \exists$

### 自动机理论

**有限自动机**: $M = (Q, \Sigma, \delta, q_0, F)$

- $Q$: 状态集合
- $\Sigma$: 输入字母表
- $\delta: Q \times \Sigma \rightarrow Q$: 转移函数
- $q_0 \in Q$: 初始状态
- $F \subseteq Q$: 接受状态集合

**图灵机**: $TM = (Q, \Sigma, \Gamma, \delta, q_0, q_{accept}, q_{reject})$

- $\Gamma$: 带字母表
- $\delta: Q \times \Gamma \rightarrow Q \times \Gamma \times \{L, R\}$: 转移函数

## Python 实现示例

### 集合论实现

```python
from typing import Set, TypeVar, Generic, Iterator
from abc import ABC, abstractmethod
import itertools

T = TypeVar('T')

class Set(Generic[T]):
    """集合抽象基类"""
    
    def __init__(self, elements: Set[T] = None):
        self._elements = elements or set()
    
    def __contains__(self, element: T) -> bool:
        """元素属于关系"""
        return element in self._elements
    
    def __iter__(self) -> Iterator[T]:
        """迭代器"""
        return iter(self._elements)
    
    def __len__(self) -> int:
        """集合大小"""
        return len(self._elements)
    
    def union(self, other: 'Set[T]') -> 'Set[T]':
        """并集"""
        return Set(self._elements | other._elements)
    
    def intersection(self, other: 'Set[T]') -> 'Set[T]':
        """交集"""
        return Set(self._elements & other._elements)
    
    def difference(self, other: 'Set[T]') -> 'Set[T]':
        """差集"""
        return Set(self._elements - other._elements)
    
    def complement(self, universe: 'Set[T]') -> 'Set[T]':
        """补集"""
        return universe.difference(self)
    
    def is_subset(self, other: 'Set[T]') -> bool:
        """子集关系"""
        return self._elements.issubset(other._elements)
    
    def is_superset(self, other: 'Set[T]') -> bool:
        """超集关系"""
        return self._elements.issuperset(other._elements)
    
    def __str__(self) -> str:
        return f"{{{', '.join(map(str, self._elements))}}}"

class Relation(Generic[T]):
    """二元关系"""
    
    def __init__(self, pairs: Set[tuple[T, T]] = None):
        self._pairs = pairs or set()
    
    def add_pair(self, a: T, b: T) -> None:
        """添加有序对"""
        self._pairs.add((a, b))
    
    def is_reflexive(self, domain: Set[T]) -> bool:
        """自反性检查"""
        return all((x, x) in self._pairs for x in domain)
    
    def is_symmetric(self) -> bool:
        """对称性检查"""
        return all((y, x) in self._pairs for (x, y) in self._pairs)
    
    def is_transitive(self) -> bool:
        """传递性检查"""
        for (x, y1) in self._pairs:
            for (y2, z) in self._pairs:
                if y1 == y2 and (x, z) not in self._pairs:
                    return False
        return True
    
    def is_equivalence(self, domain: Set[T]) -> bool:
        """等价关系检查"""
        return (self.is_reflexive(domain) and 
                self.is_symmetric() and 
                self.is_transitive())
    
    def equivalence_classes(self, domain: Set[T]) -> Set[Set[T]]:
        """等价类划分"""
        if not self.is_equivalence(domain):
            raise ValueError("关系必须是等价关系")
        
        classes = set()
        used = set()
        
        for x in domain:
            if x in used:
                continue
            
            # 找到x的等价类
            eq_class = {x}
            for y in domain:
                if (x, y) in self._pairs:
                    eq_class.add(y)
                    used.add(y)
            
            classes.add(Set(eq_class))
        
        return classes

class Function(Generic[T, U]):
    """函数抽象"""
    
    def __init__(self, mapping: dict[T, U]):
        self._mapping = mapping
    
    def __call__(self, x: T) -> U:
        """函数调用"""
        if x not in self._mapping:
            raise ValueError(f"函数在 {x} 处未定义")
        return self._mapping[x]
    
    def domain(self) -> Set[T]:
        """定义域"""
        return Set(set(self._mapping.keys()))
    
    def codomain(self) -> Set[U]:
        """陪域"""
        return Set(set(self._mapping.values()))
    
    def is_injective(self) -> bool:
        """单射检查"""
        values = list(self._mapping.values())
        return len(values) == len(set(values))
    
    def is_surjective(self, codomain: Set[U]) -> bool:
        """满射检查"""
        return codomain.is_subset(self.codomain())
    
    def is_bijective(self, codomain: Set[U]) -> bool:
        """双射检查"""
        return self.is_injective() and self.is_surjective(codomain)
    
    def inverse(self) -> 'Function[U, T]':
        """逆函数"""
        if not self.is_bijective(self.codomain()):
            raise ValueError("函数必须是双射才有逆函数")
        
        inverse_mapping = {v: k for k, v in self._mapping.items()}
        return Function(inverse_mapping)
```

### 逻辑系统实现

```python
from typing import Dict, List, Set, Any
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

class TruthValue(Enum):
    """真值枚举"""
    TRUE = True
    FALSE = False

@dataclass
class Proposition:
    """命题"""
    name: str
    value: TruthValue = TruthValue.FALSE
    
    def __str__(self) -> str:
        return f"{self.name} = {self.value.value}"

class LogicalOperator(Enum):
    """逻辑运算符"""
    NOT = "¬"
    AND = "∧"
    OR = "∨"
    IMPLIES = "→"
    EQUIVALENT = "↔"

class LogicalExpression:
    """逻辑表达式"""
    
    def __init__(self, operator: LogicalOperator = None, 
                 operands: List['LogicalExpression'] = None,
                 proposition: Proposition = None):
        self.operator = operator
        self.operands = operands or []
        self.proposition = proposition
    
    def evaluate(self, interpretation: Dict[str, bool]) -> bool:
        """求值"""
        if self.proposition:
            return interpretation.get(self.proposition.name, False)
        
        if not self.operands:
            return False
        
        if self.operator == LogicalOperator.NOT:
            return not self.operands[0].evaluate(interpretation)
        elif self.operator == LogicalOperator.AND:
            return all(op.evaluate(interpretation) for op in self.operands)
        elif self.operator == LogicalOperator.OR:
            return any(op.evaluate(interpretation) for op in self.operands)
        elif self.operator == LogicalOperator.IMPLIES:
            return (not self.operands[0].evaluate(interpretation) or 
                    self.operands[1].evaluate(interpretation))
        elif self.operator == LogicalOperator.EQUIVALENT:
            return (self.operands[0].evaluate(interpretation) == 
                    self.operands[1].evaluate(interpretation))
        
        return False
    
    def get_variables(self) -> Set[str]:
        """获取变量集合"""
        if self.proposition:
            return {self.proposition.name}
        
        variables = set()
        for operand in self.operands:
            variables.update(operand.get_variables())
        return variables
    
    def __str__(self) -> str:
        if self.proposition:
            return self.proposition.name
        
        if self.operator == LogicalOperator.NOT:
            return f"¬({self.operands[0]})"
        elif self.operator == LogicalOperator.AND:
            return f"({' ∧ '.join(str(op) for op in self.operands)})"
        elif self.operator == LogicalOperator.OR:
            return f"({' ∨ '.join(str(op) for op in self.operands)})"
        elif self.operator == LogicalOperator.IMPLIES:
            return f"({self.operands[0]} → {self.operands[1]})"
        elif self.operator == LogicalOperator.EQUIVALENT:
            return f"({self.operands[0]} ↔ {self.operands[1]})"
        
        return ""

class TruthTable:
    """真值表"""
    
    def __init__(self, expression: LogicalExpression):
        self.expression = expression
        self.variables = sorted(list(expression.get_variables()))
    
    def generate_table(self) -> List[Dict[str, Any]]:
        """生成真值表"""
        table = []
        n_vars = len(self.variables)
        
        # 生成所有可能的真值组合
        for i in range(2 ** n_vars):
            interpretation = {}
            for j, var in enumerate(self.variables):
                interpretation[var] = bool((i >> j) & 1)
            
            result = self.expression.evaluate(interpretation)
            
            row = interpretation.copy()
            row['result'] = result
            table.append(row)
        
        return table
    
    def print_table(self) -> None:
        """打印真值表"""
        table = self.generate_table()
        
        # 打印表头
        header = " | ".join(self.variables + ["Result"])
        print(header)
        print("-" * len(header))
        
        # 打印每一行
        for row in table:
            values = [str(int(row[var])) for var in self.variables]
            values.append(str(int(row['result'])))
            print(" | ".join(values))
    
    def is_tautology(self) -> bool:
        """永真式检查"""
        return all(row['result'] for row in self.generate_table())
    
    def is_contradiction(self) -> bool:
        """永假式检查"""
        return not any(row['result'] for row in self.generate_table())
    
    def is_satisfiable(self) -> bool:
        """可满足性检查"""
        return any(row['result'] for row in self.generate_table())

class PredicateLogic:
    """谓词逻辑"""
    
    def __init__(self):
        self.predicates: Dict[str, List[int]] = {}  # 谓词名 -> 参数数量
        self.constants: Set[str] = set()
        self.variables: Set[str] = set()
    
    def add_predicate(self, name: str, arity: int) -> None:
        """添加谓词"""
        self.predicates[name] = arity
    
    def add_constant(self, name: str) -> None:
        """添加常元"""
        self.constants.add(name)
    
    def add_variable(self, name: str) -> None:
        """添加变元"""
        self.variables.add(name)
    
    def is_valid_formula(self, formula: str) -> bool:
        """检查公式有效性"""
        # 简化的语法检查
        try:
            # 检查括号匹配
            if formula.count('(') != formula.count(')'):
                return False
            
            # 检查量词使用
            if '∀' in formula or '∃' in formula:
                # 量词后必须跟变量
                pass
            
            return True
        except:
            return False
```

### 自动机理论实现

```python
from typing import Dict, Set, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    """移动方向"""
    LEFT = "L"
    RIGHT = "R"
    STAY = "S"

@dataclass
class Transition:
    """转移规则"""
    current_state: str
    current_symbol: str
    next_state: str
    write_symbol: str
    direction: Direction

class FiniteAutomaton:
    """有限自动机"""
    
    def __init__(self, states: Set[str], alphabet: Set[str], 
                 transitions: Dict[Tuple[str, str], str],
                 initial_state: str, accepting_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.current_state = initial_state
    
    def reset(self) -> None:
        """重置到初始状态"""
        self.current_state = self.initial_state
    
    def step(self, symbol: str) -> bool:
        """执行一步转移"""
        if symbol not in self.alphabet:
            return False
        
        key = (self.current_state, symbol)
        if key not in self.transitions:
            return False
        
        self.current_state = self.transitions[key]
        return True
    
    def accept(self, input_string: str) -> bool:
        """接受输入字符串"""
        self.reset()
        
        for symbol in input_string:
            if not self.step(symbol):
                return False
        
        return self.current_state in self.accepting_states
    
    def is_deterministic(self) -> bool:
        """检查是否为确定有限自动机"""
        for state in self.states:
            for symbol in self.alphabet:
                key = (state, symbol)
                if key in self.transitions:
                    # 检查是否有多个转移
                    count = sum(1 for k in self.transitions.keys() if k == key)
                    if count > 1:
                        return False
        return True

class TuringMachine:
    """图灵机"""
    
    def __init__(self, states: Set[str], input_alphabet: Set[str], 
                 tape_alphabet: Set[str], transitions: List[Transition],
                 initial_state: str, accept_state: str, reject_state: str):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        
        # 运行时状态
        self.current_state = initial_state
        self.tape: List[str] = []
        self.head_position = 0
    
    def reset(self, input_string: str) -> None:
        """重置图灵机"""
        self.current_state = self.initial_state
        self.tape = list(input_string)
        self.head_position = 0
    
    def get_current_symbol(self) -> str:
        """获取当前符号"""
        if 0 <= self.head_position < len(self.tape):
            return self.tape[self.head_position]
        return '_'  # 空白符号
    
    def write_symbol(self, symbol: str) -> None:
        """写入符号"""
        if 0 <= self.head_position < len(self.tape):
            self.tape[self.head_position] = symbol
        else:
            # 扩展磁带
            if self.head_position < 0:
                self.tape.insert(0, symbol)
                self.head_position = 0
            else:
                self.tape.append(symbol)
    
    def move_head(self, direction: Direction) -> None:
        """移动读写头"""
        if direction == Direction.LEFT:
            self.head_position -= 1
        elif direction == Direction.RIGHT:
            self.head_position += 1
        # STAY 不移动
    
    def find_transition(self) -> Optional[Transition]:
        """查找适用的转移规则"""
        current_symbol = self.get_current_symbol()
        
        for transition in self.transitions:
            if (transition.current_state == self.current_state and 
                transition.current_symbol == current_symbol):
                return transition
        
        return None
    
    def step(self) -> bool:
        """执行一步计算"""
        transition = self.find_transition()
        
        if transition is None:
            return False
        
        # 执行转移
        self.current_state = transition.next_state
        self.write_symbol(transition.write_symbol)
        self.move_head(transition.direction)
        
        return True
    
    def run(self, input_string: str, max_steps: int = 1000) -> str:
        """运行图灵机"""
        self.reset(input_string)
        steps = 0
        
        while steps < max_steps:
            if self.current_state == self.accept_state:
                return "ACCEPT"
            elif self.current_state == self.reject_state:
                return "REJECT"
            
            if not self.step():
                return "HALT"
            
            steps += 1
        
        return "TIMEOUT"
    
    def get_tape_content(self) -> str:
        """获取磁带内容"""
        return ''.join(self.tape)

# 使用示例
def create_dfa_example() -> FiniteAutomaton:
    """创建DFA示例：接受包含偶数个1的二进制串"""
    states = {'q0', 'q1'}
    alphabet = {'0', '1'}
    transitions = {
        ('q0', '0'): 'q0',
        ('q0', '1'): 'q1',
        ('q1', '0'): 'q1',
        ('q1', '1'): 'q0'
    }
    initial_state = 'q0'
    accepting_states = {'q0'}
    
    return FiniteAutomaton(states, alphabet, transitions, initial_state, accepting_states)

def create_tm_example() -> TuringMachine:
    """创建图灵机示例：复制输入"""
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'qaccept', 'qreject'}
    input_alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', '_', 'X', 'Y'}
    
    transitions = [
        # 初始状态：读取第一个符号
        Transition('q0', '0', 'q1', 'X', Direction.RIGHT),
        Transition('q0', '1', 'q2', 'Y', Direction.RIGHT),
        Transition('q0', '_', 'qaccept', '_', Direction.STAY),
        
        # 处理0：移动到右端
        Transition('q1', '0', 'q1', '0', Direction.RIGHT),
        Transition('q1', '1', 'q1', '1', Direction.RIGHT),
        Transition('q1', '_', 'q3', '_', Direction.LEFT),
        
        # 处理1：移动到右端
        Transition('q2', '0', 'q2', '0', Direction.RIGHT),
        Transition('q2', '1', 'q2', '1', Direction.RIGHT),
        Transition('q2', '_', 'q4', '_', Direction.LEFT),
        
        # 写0并返回
        Transition('q3', '0', 'q3', '0', Direction.LEFT),
        Transition('q3', '1', 'q3', '1', Direction.LEFT),
        Transition('q3', 'X', 'q0', 'X', Direction.RIGHT),
        
        # 写1并返回
        Transition('q4', '0', 'q4', '0', Direction.LEFT),
        Transition('q4', '1', 'q4', '1', Direction.LEFT),
        Transition('q4', 'Y', 'q0', 'Y', Direction.RIGHT),
    ]
    
    return TuringMachine(states, input_alphabet, tape_alphabet, transitions,
                        'q0', 'qaccept', 'qreject')

# 测试
if __name__ == "__main__":
    # 测试DFA
    print("=== DFA测试 ===")
    dfa = create_dfa_example()
    test_strings = ['', '0', '1', '00', '01', '10', '11', '000', '001', '010', '011']
    
    for s in test_strings:
        result = dfa.accept(s)
        ones_count = s.count('1')
        expected = ones_count % 2 == 0
        print(f"'{s}' -> {result} (期望: {expected})")
    
    # 测试图灵机
    print("\n=== 图灵机测试 ===")
    tm = create_tm_example()
    test_inputs = ['', '0', '1', '01', '10', '001']
    
    for inp in test_inputs:
        result = tm.run(inp)
        print(f"输入: '{inp}' -> {result}")
        if result == "ACCEPT":
            print(f"磁带内容: {tm.get_tape_content()}")
```

## 理论证明

### 定理 1.1: 德摩根律

**陈述**: 对于任意集合 $A, B$，有：

1. $(A \cup B)^c = A^c \cap B^c$
2. $(A \cap B)^c = A^c \cup B^c$

**证明**:

1. 对于任意 $x \in (A \cup B)^c$，有 $x \notin A \cup B$
2. 因此 $x \notin A$ 且 $x \notin B$
3. 所以 $x \in A^c$ 且 $x \in B^c$
4. 因此 $x \in A^c \cap B^c$
5. 反之亦然，故 $(A \cup B)^c = A^c \cap B^c$

### 定理 1.2: 函数复合的结合律

**陈述**: 对于函数 $f: A \rightarrow B$, $g: B \rightarrow C$, $h: C \rightarrow D$，有：
$(h \circ g) \circ f = h \circ (g \circ f)$

**证明**:
对于任意 $x \in A$：

1. $((h \circ g) \circ f)(x) = (h \circ g)(f(x)) = h(g(f(x)))$
2. $(h \circ (g \circ f))(x) = h((g \circ f)(x)) = h(g(f(x)))$
3. 因此 $(h \circ g) \circ f = h \circ (g \circ f)$

### 引理 1.1: 等价关系的划分性质

**陈述**: 等价关系将集合划分为不相交的等价类。

**证明**:

1. 自反性保证每个元素至少属于一个等价类
2. 对称性和传递性保证等价类的不相交性
3. 因此等价关系产生集合的划分

## 总结

形式科学层为软件工程提供了严格的数学和逻辑基础。通过集合论、逻辑系统、形式化方法和证明系统，我们建立了理解和分析软件系统的数学工具。这些理论基础将指导后续各层的具体应用和实现。

---

**相关链接**:

- [00-理念基础](../00-理念基础/README.md) - 哲学理念和基础概念
- [02-理论基础](../02-理论基础/README.md) - 计算机科学理论
- [03-具体科学](../03-具体科学/README.md) - 具体技术领域
