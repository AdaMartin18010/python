# 01-形式科学层

## 概述

形式科学层是知识体系的数学和逻辑基础，提供严格的形式化工具和方法。这一层包括集合论、逻辑学、代数结构、图论、计算理论和类型论等核心数学理论。

## 目录结构

```
01-形式科学/
├── README.md                    # 本文件
├── 01-集合论/                  # 集合论基础
├── 02-逻辑学/                  # 数理逻辑
├── 03-代数结构/                # 代数结构理论
├── 04-图论/                    # 图论基础
├── 05-计算理论/                # 计算理论基础
└── 06-类型论/                  # 类型论基础
```

## 核心理论

### 1. 集合论 (Set Theory)

**定义**: 集合论是研究集合及其性质的数学分支。

**公理系统**:

- **外延公理**: 两个集合相等当且仅当它们包含相同的元素
- **空集公理**: 存在一个不包含任何元素的集合
- **配对公理**: 对于任意两个集合，存在包含它们的集合
- **并集公理**: 对于任意集合族，存在包含所有成员的集合
- **幂集公理**: 对于任意集合，存在包含其所有子集的集合

**Python实现**:

```python
from typing import Set, List, Any, Callable
from abc import ABC, abstractmethod

class SetTheory:
    """集合论实现"""
    
    @staticmethod
    def empty_set() -> Set:
        """空集"""
        return set()
    
    @staticmethod
    def singleton(element: Any) -> Set:
        """单元素集"""
        return {element}
    
    @staticmethod
    def union(sets: List[Set]) -> Set:
        """并集"""
        result = set()
        for s in sets:
            result.update(s)
        return result
    
    @staticmethod
    def intersection(sets: List[Set]) -> Set:
        """交集"""
        if not sets:
            return set()
        result = sets[0].copy()
        for s in sets[1:]:
            result.intersection_update(s)
        return result
    
    @staticmethod
    def power_set(original_set: Set) -> Set:
        """幂集"""
        elements = list(original_set)
        power_set = {frozenset()}
        
        for i in range(1, 2**len(elements)):
            subset = set()
            for j in range(len(elements)):
                if i & (1 << j):
                    subset.add(elements[j])
            power_set.add(frozenset(subset))
        
        return {set(s) for s in power_set}
    
    @staticmethod
    def cartesian_product(set_a: Set, set_b: Set) -> Set:
        """笛卡尔积"""
        return {(a, b) for a in set_a for b in set_b}

# 集合论示例
def set_theory_example():
    """集合论示例"""
    A = {1, 2, 3}
    B = {3, 4, 5}
    
    print(f"集合 A: {A}")
    print(f"集合 B: {B}")
    print(f"并集 A ∪ B: {SetTheory.union([A, B])}")
    print(f"交集 A ∩ B: {SetTheory.intersection([A, B])}")
    print(f"A 的幂集: {SetTheory.power_set(A)}")
    print(f"A × B: {SetTheory.cartesian_product(A, B)}")

if __name__ == "__main__":
    set_theory_example()
```

### 2. 逻辑学 (Logic)

**定义**: 逻辑学是研究推理形式和有效性的学科。

**命题逻辑**:

- **原子命题**: 基本命题单元
- **逻辑连接词**: ¬, ∧, ∨, →, ↔
- **真值表**: 命题的真值组合

**Python实现**:

```python
from typing import Dict, List, Callable
from dataclasses import dataclass
from enum import Enum

class LogicalOperator(Enum):
    NOT = "¬"
    AND = "∧"
    OR = "∨"
    IMPLIES = "→"
    EQUIVALENT = "↔"

@dataclass
class Proposition:
    """命题"""
    name: str
    value: bool = False
    
    def __str__(self) -> str:
        return f"{self.name} = {self.value}"

class PropositionalLogic:
    """命题逻辑"""
    
    @staticmethod
    def negation(p: bool) -> bool:
        """否定 ¬p"""
        return not p
    
    @staticmethod
    def conjunction(p: bool, q: bool) -> bool:
        """合取 p ∧ q"""
        return p and q
    
    @staticmethod
    def disjunction(p: bool, q: bool) -> bool:
        """析取 p ∨ q"""
        return p or q
    
    @staticmethod
    def implication(p: bool, q: bool) -> bool:
        """蕴含 p → q"""
        return not p or q
    
    @staticmethod
    def equivalence(p: bool, q: bool) -> bool:
        """等价 p ↔ q"""
        return p == q
    
    @staticmethod
    def truth_table(propositions: List[str], formula: Callable) -> List[Dict]:
        """生成真值表"""
        n = len(propositions)
        truth_table = []
        
        for i in range(2**n):
            values = {}
            for j, prop in enumerate(propositions):
                values[prop] = bool(i & (1 << j))
            
            result = formula(values)
            values['result'] = result
            truth_table.append(values)
        
        return truth_table

# 逻辑学示例
def logic_example():
    """逻辑学示例"""
    # 德摩根定律: ¬(p ∧ q) ↔ (¬p ∨ ¬q)
    def demorgan_law(values: Dict[str, bool]) -> bool:
        p, q = values['p'], values['q']
        left = PropositionalLogic.negation(PropositionalLogic.conjunction(p, q))
        right = PropositionalLogic.disjunction(PropositionalLogic.negation(p), PropositionalLogic.negation(q))
        return PropositionalLogic.equivalence(left, right)
    
    truth_table = PropositionalLogic.truth_table(['p', 'q'], demorgan_law)
    
    print("德摩根定律真值表:")
    print("p\tq\t¬(p∧q)\t(¬p∨¬q)\t等价")
    for row in truth_table:
        p, q, result = row['p'], row['q'], row['result']
        left = PropositionalLogic.negation(PropositionalLogic.conjunction(p, q))
        right = PropositionalLogic.disjunction(PropositionalLogic.negation(p), PropositionalLogic.negation(q))
        print(f"{p}\t{q}\t{left}\t{right}\t{result}")

if __name__ == "__main__":
    logic_example()
```

### 3. 代数结构 (Algebraic Structures)

**定义**: 代数结构是带有运算的集合。

**群论**:

- **群**: 满足结合律、单位元、逆元的代数结构
- **环**: 带有两种运算的代数结构
- **域**: 可除环

**Python实现**:

```python
from typing import Dict, Any, Callable
from abc import ABC, abstractmethod

class Group(ABC):
    """群抽象基类"""
    
    @abstractmethod
    def operation(self, a: Any, b: Any) -> Any:
        """群运算"""
        pass
    
    @abstractmethod
    def identity(self) -> Any:
        """单位元"""
        pass
    
    @abstractmethod
    def inverse(self, a: Any) -> Any:
        """逆元"""
        pass
    
    def is_associative(self, a: Any, b: Any, c: Any) -> bool:
        """检查结合律"""
        return self.operation(self.operation(a, b), c) == self.operation(a, self.operation(b, c))
    
    def is_identity(self, a: Any) -> bool:
        """检查是否为单位元"""
        return self.operation(a, self.identity()) == a and self.operation(self.identity(), a) == a
    
    def is_inverse(self, a: Any, b: Any) -> bool:
        """检查是否为逆元"""
        return self.operation(a, b) == self.identity() and self.operation(b, a) == self.identity()

class IntegerAdditionGroup(Group):
    """整数加法群"""
    
    def operation(self, a: int, b: int) -> int:
        return a + b
    
    def identity(self) -> int:
        return 0
    
    def inverse(self, a: int) -> int:
        return -a

# 代数结构示例
def algebraic_structure_example():
    """代数结构示例"""
    group = IntegerAdditionGroup()
    
    a, b, c = 3, 5, 7
    
    print(f"群运算: {a} + {b} = {group.operation(a, b)}")
    print(f"单位元: {group.identity()}")
    print(f"逆元: {a} 的逆元是 {group.inverse(a)}")
    print(f"结合律: ({a} + {b}) + {c} = {a} + ({b} + {c}) = {group.is_associative(a, b, c)}")
    print(f"单位元性质: {group.is_identity(group.identity())}")
    print(f"逆元性质: {group.is_inverse(a, group.inverse(a))}")

if __name__ == "__main__":
    algebraic_structure_example()
```

## 导航链接

- **上级目录**: [../README.md](../README.md)
- **同级目录**:
  - [00-理念基础/](../00-理念基础/)
  - [02-理论基础/](../02-理论基础/)
  - [03-具体科学/](../03-具体科学/)
  - [04-行业领域/](../04-行业领域/)
  - [05-架构领域/](../05-架构领域/)
  - [06-组件算法/](../06-组件算法/)
  - [07-实践应用/](../07-实践应用/)
  - [08-项目进度/](../08-项目进度/)
- **下级目录**:
  - [01-集合论/](01-集合论/)
  - [02-逻辑学/](02-逻辑学/)
  - [03-代数结构/](03-代数结构/)
  - [04-图论/](04-图论/)
  - [05-计算理论/](05-计算理论/)
  - [06-类型论/](06-类型论/)

## 参考文献

1. Halmos, P. R. (1974). Naive Set Theory. Springer-Verlag.
2. Enderton, H. B. (2001). A Mathematical Introduction to Logic. Academic Press.
3. Dummit, D. S., & Foote, R. M. (2004). Abstract Algebra. John Wiley & Sons.
4. Bondy, J. A., & Murty, U. S. R. (2008). Graph Theory. Springer.
5. Pierce, B. C. (2002). Types and Programming Languages. MIT Press.
