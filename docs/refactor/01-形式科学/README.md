# 01-形式科学

## 概述

形式科学层提供软件工程和计算科学的数学和逻辑基础，包括集合论、逻辑学、代数结构、图论等核心数学工具。

## 目录结构

```
01-形式科学/
├── README.md                    # 本文件
├── 01-集合论/
│   ├── 01-基本概念.md          # 集合、元素、关系
│   ├── 02-集合运算.md          # 并、交、差、补
│   ├── 03-关系与函数.md        # 二元关系、函数
│   └── 04-基数与序数.md        # 无穷集合理论
├── 02-逻辑学/
│   ├── 01-命题逻辑.md          # 命题、联结词、真值表
│   ├── 02-谓词逻辑.md          # 量词、谓词、推理
│   ├── 03-模态逻辑.md          # 可能、必然、时间逻辑
│   └── 04-直觉逻辑.md          # 构造性逻辑
├── 03-代数结构/
│   ├── 01-群论.md              # 群、子群、同态
│   ├── 02-环与域.md            # 环、域、多项式
│   ├── 03-格论.md              # 偏序集、格、布尔代数
│   └── 04-范畴论.md            # 范畴、函子、自然变换
├── 04-图论/
│   ├── 01-基本概念.md          # 图、顶点、边
│   ├── 02-图的表示.md          # 邻接矩阵、邻接表
│   ├── 03-图算法.md            # 遍历、最短路径、最小生成树
│   └── 04-特殊图类.md          # 树、二分图、平面图
├── 05-组合数学/
│   ├── 01-排列组合.md          # 排列、组合、二项式定理
│   ├── 02-生成函数.md          # 普通生成函数、指数生成函数
│   ├── 03-递推关系.md          # 线性递推、非线性递推
│   └── 04-容斥原理.md          # 包含排除原理
└── 06-形式语言/
    ├── 01-语言与文法.md        # 字母表、字符串、文法
    ├── 02-自动机理论.md        # 有限自动机、下推自动机
    ├── 03-正则表达式.md        # 正则语言、正则表达式
    └── 04-上下文无关文法.md    # CFG、语法分析
```

## 核心概念

### 1. 集合论基础

**定义**: 集合是不同对象的无序聚集。

**形式化表示**:
- 集合 $A = \{x \mid P(x)\}$ 表示满足性质 $P$ 的所有元素 $x$
- 空集 $\emptyset = \{\}$
- 全集 $U$ 包含所有可能元素

**基本运算**:
- 并集: $A \cup B = \{x \mid x \in A \lor x \in B\}$
- 交集: $A \cap B = \{x \mid x \in A \land x \in B\}$
- 差集: $A \setminus B = \{x \mid x \in A \land x \notin B\}$
- 补集: $A^c = U \setminus A$

### 2. 逻辑学基础

**命题逻辑**:
- 原子命题: $p, q, r, ...$
- 逻辑联结词: $\neg, \land, \lor, \rightarrow, \leftrightarrow$
- 真值表: 定义每个联结词的语义

**谓词逻辑**:
- 个体变量: $x, y, z, ...$
- 谓词: $P(x), Q(x,y), ...$
- 量词: $\forall x, \exists x$

### 3. 代数结构

**群的定义**:
群 $(G, \cdot)$ 满足:
1. 封闭性: $\forall a,b \in G, a \cdot b \in G$
2. 结合律: $(a \cdot b) \cdot c = a \cdot (b \cdot c)$
3. 单位元: $\exists e \in G, \forall a \in G, e \cdot a = a \cdot e = a$
4. 逆元: $\forall a \in G, \exists a^{-1} \in G, a \cdot a^{-1} = a^{-1} \cdot a = e$

### 4. 图论基础

**图的定义**:
图 $G = (V, E)$ 由顶点集 $V$ 和边集 $E \subseteq V \times V$ 组成。

**基本概念**:
- 度: $deg(v) = |\{e \in E \mid v \in e\}|$
- 路径: 顶点序列 $v_1, v_2, ..., v_n$ 使得 $(v_i, v_{i+1}) \in E$
- 连通性: 任意两顶点间存在路径

## Python实现示例

```python
from abc import ABC, abstractmethod
from typing import Set, List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import math

# 集合论实现
class SetTheory:
    """集合论基本操作"""
    
    @staticmethod
    def union(a: Set, b: Set) -> Set:
        """集合并集"""
        return a | b
    
    @staticmethod
    def intersection(a: Set, b: Set) -> Set:
        """集合交集"""
        return a & b
    
    @staticmethod
    def difference(a: Set, b: Set) -> Set:
        """集合差集"""
        return a - b
    
    @staticmethod
    def complement(a: Set, universe: Set) -> Set:
        """集合补集"""
        return universe - a
    
    @staticmethod
    def cartesian_product(a: Set, b: Set) -> Set:
        """笛卡尔积"""
        return {(x, y) for x in a for y in b}

# 逻辑学实现
class PropositionalLogic:
    """命题逻辑"""
    
    @staticmethod
    def truth_table(proposition: str, variables: List[str]) -> Dict[Tuple, bool]:
        """生成真值表"""
        table = {}
        n = len(variables)
        
        for i in range(2**n):
            # 生成所有可能的真值组合
            values = []
            for j in range(n):
                values.append(bool((i >> j) & 1))
            
            # 计算命题的真值
            env = dict(zip(variables, values))
            result = PropositionalLogic._evaluate(proposition, env)
            table[tuple(values)] = result
        
        return table
    
    @staticmethod
    def _evaluate(expr: str, env: Dict[str, bool]) -> bool:
        """计算表达式的真值"""
        # 简化的表达式求值器
        expr = expr.replace('AND', 'and').replace('OR', 'or').replace('NOT', 'not')
        for var, value in env.items():
            expr = expr.replace(var, str(value))
        return eval(expr)

# 代数结构实现
class Group:
    """群的基本实现"""
    
    def __init__(self, elements: Set, operation: callable, identity: Any):
        self.elements = elements
        self.operation = operation
        self.identity = identity
        self._validate_group()
    
    def _validate_group(self):
        """验证群的性质"""
        # 检查封闭性
        for a in self.elements:
            for b in self.elements:
                if self.operation(a, b) not in self.elements:
                    raise ValueError("Group not closed under operation")
        
        # 检查单位元
        for a in self.elements:
            if self.operation(self.identity, a) != a or self.operation(a, self.identity) != a:
                raise ValueError("Invalid identity element")
        
        # 检查逆元
        for a in self.elements:
            has_inverse = False
            for b in self.elements:
                if self.operation(a, b) == self.identity and self.operation(b, a) == self.identity:
                    has_inverse = True
                    break
            if not has_inverse:
                raise ValueError(f"Element {a} has no inverse")
    
    def order(self) -> int:
        """群的阶"""
        return len(self.elements)
    
    def is_abelian(self) -> bool:
        """检查是否为阿贝尔群"""
        for a in self.elements:
            for b in self.elements:
                if self.operation(a, b) != self.operation(b, a):
                    return False
        return True

# 图论实现
@dataclass
class Graph:
    """图的基本实现"""
    vertices: Set[int]
    edges: Set[Tuple[int, int]]
    
    def __post_init__(self):
        # 验证边的有效性
        for edge in self.edges:
            if edge[0] not in self.vertices or edge[1] not in self.vertices:
                raise ValueError(f"Invalid edge {edge}")
    
    def degree(self, vertex: int) -> int:
        """计算顶点的度"""
        if vertex not in self.vertices:
            raise ValueError(f"Vertex {vertex} not in graph")
        
        count = 0
        for edge in self.edges:
            if vertex in edge:
                count += 1
        return count
    
    def neighbors(self, vertex: int) -> Set[int]:
        """获取顶点的邻居"""
        if vertex not in self.vertices:
            raise ValueError(f"Vertex {vertex} not in graph")
        
        neighbors = set()
        for edge in self.edges:
            if edge[0] == vertex:
                neighbors.add(edge[1])
            elif edge[1] == vertex:
                neighbors.add(edge[0])
        return neighbors
    
    def is_connected(self) -> bool:
        """检查图的连通性"""
        if not self.vertices:
            return True
        
        visited = set()
        start_vertex = next(iter(self.vertices))
        self._dfs(start_vertex, visited)
        
        return len(visited) == len(self.vertices)
    
    def _dfs(self, vertex: int, visited: Set[int]):
        """深度优先搜索"""
        visited.add(vertex)
        for neighbor in self.neighbors(vertex):
            if neighbor not in visited:
                self._dfs(neighbor, visited)
    
    def shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """使用BFS找最短路径"""
        if start not in self.vertices or end not in self.vertices:
            return None
        
        if start == end:
            return [start]
        
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            current, path = queue.pop(0)
            
            for neighbor in self.neighbors(current):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

# 组合数学实现
class Combinatorics:
    """组合数学工具"""
    
    @staticmethod
    def factorial(n: int) -> int:
        """阶乘"""
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n == 0:
            return 1
        return n * Combinatorics.factorial(n - 1)
    
    @staticmethod
    def combination(n: int, k: int) -> int:
        """组合数 C(n,k)"""
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1
        
        # 使用对称性优化
        if k > n // 2:
            k = n - k
        
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result
    
    @staticmethod
    def permutation(n: int, k: int) -> int:
        """排列数 P(n,k)"""
        if k > n or k < 0:
            return 0
        return Combinatorics.factorial(n) // Combinatorics.factorial(n - k)
    
    @staticmethod
    def generate_combinations(elements: List, k: int) -> List[Tuple]:
        """生成所有k组合"""
        if k == 0:
            return [()]
        if k > len(elements):
            return []
        
        result = []
        for i in range(len(elements) - k + 1):
            for combo in Combinatorics.generate_combinations(elements[i+1:], k-1):
                result.append((elements[i],) + combo)
        return result

# 使用示例
def main():
    # 集合论示例
    A = {1, 2, 3, 4}
    B = {3, 4, 5, 6}
    print(f"A ∪ B = {SetTheory.union(A, B)}")
    print(f"A ∩ B = {SetTheory.intersection(A, B)}")
    print(f"A - B = {SetTheory.difference(A, B)}")
    
    # 逻辑学示例
    variables = ['p', 'q']
    table = PropositionalLogic.truth_table('p AND q', variables)
    print("真值表:")
    for values, result in table.items():
        print(f"p={values[0]}, q={values[1]} -> {result}")
    
    # 群论示例
    def mod_add(a: int, b: int) -> int:
        return (a + b) % 4
    
    Z4 = Group({0, 1, 2, 3}, mod_add, 0)
    print(f"Z4的阶: {Z4.order()}")
    print(f"Z4是阿贝尔群: {Z4.is_abelian()}")
    
    # 图论示例
    vertices = {0, 1, 2, 3, 4}
    edges = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
    graph = Graph(vertices, edges)
    
    print(f"图是连通的: {graph.is_connected()}")
    print(f"顶点0的度: {graph.degree(0)}")
    print(f"顶点0的邻居: {graph.neighbors(0)}")
    
    path = graph.shortest_path(0, 3)
    print(f"从0到3的最短路径: {path}")
    
    # 组合数学示例
    n, k = 5, 3
    print(f"C({n},{k}) = {Combinatorics.combination(n, k)}")
    print(f"P({n},{k}) = {Combinatorics.permutation(n, k)}")
    
    elements = ['a', 'b', 'c', 'd']
    combinations = Combinatorics.generate_combinations(elements, 2)
    print(f"所有2组合: {combinations}")

if __name__ == "__main__":
    main()
```

## 关联链接

- **上一层**: [00-理念基础](../00-理念基础/README.md) - 哲学和认知基础
- **下一层**: [02-理论基础](../02-理论基础/README.md) - 计算机科学理论基础
- **相关主题**:
  - [算法分析](../02-理论基础/02-算法理论.md)
  - [数据结构](../03-具体科学/01-数据结构.md)
  - [形式化验证](../03-具体科学/03-形式化方法.md)

---

*形式科学层为整个知识体系提供了严格的数学和逻辑基础，确保所有理论都有坚实的数学支撑。*
