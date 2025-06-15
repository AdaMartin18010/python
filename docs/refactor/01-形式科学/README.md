# 01-形式科学

## 概述

形式科学是软件工程和计算科学的理论基础，提供了严格的数学工具和逻辑框架。本层包含数学基础、逻辑学、集合论、范畴论和类型论等核心内容。

## 目录结构

```
01-形式科学/
├── 01-数学基础/
│   ├── 01-集合论.md
│   ├── 02-关系与函数.md
│   ├── 03-代数结构.md
│   └── 04-拓扑学基础.md
├── 02-逻辑学/
│   ├── 01-命题逻辑.md
│   ├── 02-谓词逻辑.md
│   ├── 03-模态逻辑.md
│   └── 04-直觉逻辑.md
├── 03-范畴论/
│   ├── 01-范畴基础.md
│   ├── 02-函子与自然变换.md
│   ├── 03-极限与余极限.md
│   └── 04-伴随函子.md
├── 04-类型论/
│   ├── 01-简单类型论.md
│   ├── 02-依赖类型论.md
│   ├── 03-同伦类型论.md
│   └── 04-线性类型论.md
└── 05-计算理论/
    ├── 01-可计算性理论.md
    ├── 02-计算复杂度.md
    ├── 03-形式语言理论.md
    └── 04-自动机理论.md
```

## 核心概念

### 1. 数学基础

#### 集合论
- **集合**: 基本概念和运算
- **关系**: 等价关系、偏序关系、全序关系
- **函数**: 单射、满射、双射
- **基数**: 可数集、不可数集

#### 代数结构
- **群**: 群的定义、子群、同态
- **环**: 环的定义、理想、商环
- **域**: 域的定义、扩域、有限域
- **格**: 格的定义、分配格、布尔代数

### 2. 逻辑学

#### 命题逻辑
```python
class PropositionalLogic:
    """命题逻辑形式化定义"""
    
    def __init__(self):
        self.variables = set()
        self.operators = {'¬', '∧', '∨', '→', '↔'}
    
    def evaluate(self, formula, assignment):
        """评估命题公式的真值"""
        if isinstance(formula, str):
            return assignment.get(formula, False)
        elif formula[0] == '¬':
            return not self.evaluate(formula[1], assignment)
        elif formula[0] == '∧':
            return (self.evaluate(formula[1], assignment) and 
                   self.evaluate(formula[2], assignment))
        # ... 其他操作符
```

#### 谓词逻辑
- **量词**: 全称量词 ∀、存在量词 ∃
- **谓词**: 一元谓词、多元谓词
- **推理规则**: 全称推广、存在推广

### 3. 范畴论

#### 基本概念
```python
from typing import TypeVar, Callable, List
from abc import ABC, abstractmethod

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

class Category(ABC):
    """范畴的抽象定义"""
    
    @abstractmethod
    def objects(self) -> List[object]:
        """范畴的对象"""
        pass
    
    @abstractmethod
    def morphisms(self, a: A, b: B) -> List[Callable[[A], B]]:
        """从对象a到对象b的态射"""
        pass
    
    @abstractmethod
    def compose(self, f: Callable[[A], B], g: Callable[[B], C]) -> Callable[[A], C]:
        """态射的复合"""
        pass
    
    @abstractmethod
    def identity(self, a: A) -> Callable[[A], A]:
        """恒等态射"""
        pass
```

#### 重要概念
- **函子**: 协变函子、逆变函子
- **自然变换**: 函子间的态射
- **极限**: 积、等化子、拉回
- **余极限**: 余积、余等化子、推出

### 4. 类型论

#### 简单类型论
```python
from typing import Union, Tuple, Callable
from dataclasses import dataclass

@dataclass
class Type:
    """类型的基本定义"""
    name: str
    
    def __eq__(self, other):
        return isinstance(other, Type) and self.name == other.name

class SimpleTypeSystem:
    """简单类型系统"""
    
    def __init__(self):
        self.types = {
            'Bool': Type('Bool'),
            'Int': Type('Int'),
            'String': Type('String'),
            'Unit': Type('Unit')
        }
    
    def function_type(self, domain: Type, codomain: Type) -> Type:
        """函数类型构造"""
        return Type(f"{domain.name} -> {codomain.name}")
    
    def product_type(self, types: List[Type]) -> Type:
        """积类型构造"""
        return Type(f"({' × '.join(t.name for t in types)})")
    
    def sum_type(self, types: List[Type]) -> Type:
        """和类型构造"""
        return Type(f"({' + '.join(t.name for t in types)})")
```

#### 依赖类型论
- **依赖函数类型**: Π(x:A).B(x)
- **依赖积类型**: Σ(x:A).B(x)
- **宇宙**: 类型的类型
- **归纳类型**: 自然数、列表、树

### 5. 计算理论

#### 可计算性
```python
class TuringMachine:
    """图灵机的基本实现"""
    
    def __init__(self, states, alphabet, transitions, initial_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.current_state = initial_state
        self.accept_states = accept_states
        self.tape = []
        self.head_position = 0
    
    def step(self):
        """执行一步计算"""
        current_symbol = self.tape[self.head_position]
        key = (self.current_state, current_symbol)
        
        if key in self.transitions:
            new_state, new_symbol, direction = self.transitions[key]
            self.tape[self.head_position] = new_symbol
            self.current_state = new_state
            
            if direction == 'L':
                self.head_position = max(0, self.head_position - 1)
            elif direction == 'R':
                self.head_position = min(len(self.tape) - 1, self.head_position + 1)
    
    def run(self, input_string):
        """运行图灵机"""
        self.tape = list(input_string)
        self.head_position = 0
        
        while self.current_state not in self.accept_states:
            self.step()
        
        return self.current_state in self.accept_states
```

#### 计算复杂度
- **时间复杂度**: O(f(n)) 表示法
- **空间复杂度**: 内存使用分析
- **P vs NP**: 计算复杂性理论的核心问题
- **归约**: 问题间的复杂度关系

## 形式化方法

### 1. 公理化方法
```python
class AxiomaticSystem:
    """公理系统的基本框架"""
    
    def __init__(self, axioms, rules):
        self.axioms = axioms
        self.rules = rules
        self.theorems = set()
    
    def prove(self, statement):
        """证明一个陈述"""
        # 实现证明算法
        pass
    
    def is_consistent(self):
        """检查系统一致性"""
        # 实现一致性检查
        pass
```

### 2. 模型论方法
```python
class Model:
    """模型论中的模型概念"""
    
    def __init__(self, domain, interpretations):
        self.domain = domain
        self.interpretations = interpretations
    
    def satisfies(self, formula):
        """检查模型是否满足公式"""
        # 实现满足关系
        pass
```

## 应用领域

### 1. 程序验证
- **霍尔逻辑**: 程序正确性证明
- **类型系统**: 静态类型检查
- **模型检测**: 系统性质验证

### 2. 算法分析
- **渐近分析**: 算法效率分析
- **平摊分析**: 数据结构操作分析
- **概率分析**: 随机算法分析

### 3. 系统设计
- **形式化规约**: 系统需求形式化
- **抽象代数**: 数据结构设计
- **范畴论**: 软件架构设计

## 交叉引用

- **理论基础**: [02-理论基础](../02-理论基础/README.md)
- **具体科学**: [03-具体科学](../03-具体科学/README.md)
- **架构领域**: [05-架构领域](../05-架构领域/README.md)

## 参考文献

1. Enderton, H. B. (1977). Elements of Set Theory
2. Mendelson, E. (2015). Introduction to Mathematical Logic
3. Mac Lane, S. (1998). Categories for the Working Mathematician
4. Pierce, B. C. (2002). Types and Programming Languages
5. Sipser, M. (2012). Introduction to the Theory of Computation
