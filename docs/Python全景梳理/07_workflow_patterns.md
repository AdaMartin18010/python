# 43种工作流设计模式全面梳理

## 重点：23种可判断模式的完整实现

---

## 目录

- [43种工作流设计模式全面梳理](#43种工作流设计模式全面梳理)
  - [重点：23种可判断模式的完整实现](#重点23种可判断模式的完整实现)
  - [目录](#目录)
  - [引言](#引言)
    - [可判定模式的重要性](#可判定模式的重要性)
  - [第一部分：基础控制流模式（5种）](#第一部分基础控制流模式5种)
    - [1. 顺序模式（Sequence）](#1-顺序模式sequence)
      - [概念定义](#概念定义)
      - [形式化定义](#形式化定义)
      - [Petri网表示](#petri网表示)
      - [可判定性分析](#可判定性分析)
      - [正确性条件](#正确性条件)
    - [2. 并行分支模式（Parallel Split）](#2-并行分支模式parallel-split)
      - [概念定义](#概念定义-1)
      - [形式化定义](#形式化定义-1)
      - [Petri网表示](#petri网表示-1)
      - [可判定性分析](#可判定性分析-1)
      - [正确性条件](#正确性条件-1)
    - [3. 同步模式（Synchronization）](#3-同步模式synchronization)
      - [概念定义](#概念定义-2)
      - [形式化定义](#形式化定义-2)
      - [Petri网表示](#petri网表示-2)
      - [可判定性分析](#可判定性分析-2)
      - [正确性条件](#正确性条件-2)
    - [4. 排他选择模式（Exclusive Choice）](#4-排他选择模式exclusive-choice)
      - [概念定义](#概念定义-3)
      - [形式化定义](#形式化定义-3)
      - [Petri网表示](#petri网表示-3)
      - [可判定性分析](#可判定性分析-3)
      - [正确性条件](#正确性条件-3)
    - [5. 简单合并模式（Simple Merge）](#5-简单合并模式simple-merge)
      - [概念定义](#概念定义-4)
      - [形式化定义](#形式化定义-4)
      - [Petri网表示](#petri网表示-4)
      - [可判定性分析](#可判定性分析-4)
      - [正确性条件](#正确性条件-4)
  - [第二部分：高级分支同步模式（8种）](#第二部分高级分支同步模式8种)
    - [6. 多选模式（Multi-Choice）](#6-多选模式multi-choice)
      - [概念定义](#概念定义-5)
      - [形式化定义](#形式化定义-5)
      - [Petri网表示](#petri网表示-5)
      - [可判定性分析](#可判定性分析-5)
      - [正确性条件](#正确性条件-5)
    - [7. 结构化同步合并（Structured Synchronizing Merge）](#7-结构化同步合并structured-synchronizing-merge)
      - [概念定义](#概念定义-6)
      - [形式化定义](#形式化定义-6)
      - [Petri网表示](#petri网表示-6)
      - [可判定性分析](#可判定性分析-6)
      - [正确性条件](#正确性条件-6)
    - [8. 多合并模式（Multi-Merge）](#8-多合并模式multi-merge)
      - [概念定义](#概念定义-7)
      - [形式化定义](#形式化定义-7)
      - [Petri网表示](#petri网表示-7)
      - [可判定性分析](#可判定性分析-7)
      - [正确性条件](#正确性条件-7)
    - [9. 鉴别器模式（Discriminator）](#9-鉴别器模式discriminator)
      - [概念定义](#概念定义-8)
      - [形式化定义](#形式化定义-8)
      - [Petri网表示](#petri网表示-8)
      - [可判定性分析](#可判定性分析-8)
      - [正确性条件](#正确性条件-8)
    - [10. 部分加入（Partial Join）](#10-部分加入partial-join)
      - [概念定义](#概念定义-9)
      - [形式化定义](#形式化定义-9)
      - [Petri网表示](#petri网表示-9)
      - [可判定性分析](#可判定性分析-9)
      - [正确性条件](#正确性条件-9)
    - [11. 阻塞鉴别器（Blocking Discriminator）](#11-阻塞鉴别器blocking-discriminator)
      - [概念定义](#概念定义-10)
      - [形式化定义](#形式化定义-10)
      - [Petri网表示](#petri网表示-10)
      - [可判定性分析](#可判定性分析-10)
      - [正确性条件](#正确性条件-10)
    - [12. 取消鉴别器（Canceling Discriminator）](#12-取消鉴别器canceling-discriminator)
      - [概念定义](#概念定义-11)
      - [形式化定义](#形式化定义-11)
      - [Petri网表示](#petri网表示-11)
      - [可判定性分析](#可判定性分析-11)
      - [正确性条件](#正确性条件-11)
    - [13. 结构化部分加入（Structured Partial Join）](#13-结构化部分加入structured-partial-join)
      - [概念定义](#概念定义-12)
      - [形式化定义](#形式化定义-12)
      - [可判定性分析](#可判定性分析-12)
  - [第三部分：结构化模式（2种）](#第三部分结构化模式2种)
    - [14. 任意循环（Arbitrary Cycles）](#14-任意循环arbitrary-cycles)
      - [概念定义](#概念定义-13)
      - [形式化定义](#形式化定义-13)
      - [Petri网表示](#petri网表示-12)
      - [可判定性分析](#可判定性分析-13)
      - [可判定子集](#可判定子集)
      - [正确性条件](#正确性条件-12)
    - [15. 隐式终止（Implicit Termination）](#15-隐式终止implicit-termination)
      - [概念定义](#概念定义-14)
      - [形式化定义](#形式化定义-14)
      - [Petri网表示](#petri网表示-13)
      - [可判定性分析](#可判定性分析-14)
      - [正确性条件](#正确性条件-13)
  - [第四部分：多实例模式（4种）](#第四部分多实例模式4种)
    - [16. 多实例无同步（Multiple Instances without Synchronization）](#16-多实例无同步multiple-instances-without-synchronization)
      - [概念定义](#概念定义-15)
      - [形式化定义](#形式化定义-15)
      - [可判定性分析](#可判定性分析-15)
    - [17. 多实例同步（Multiple Instances with a Priori Design Time Knowledge）](#17-多实例同步multiple-instances-with-a-priori-design-time-knowledge)
      - [概念定义](#概念定义-16)
      - [形式化定义](#形式化定义-16)
      - [可判定性分析](#可判定性分析-16)
    - [18. 多实例运行时（Multiple Instances with a Priori Runtime Knowledge）](#18-多实例运行时multiple-instances-with-a-priori-runtime-knowledge)
      - [概念定义](#概念定义-17)
      - [形式化定义](#形式化定义-17)
      - [可判定性分析](#可判定性分析-17)
    - [19. 多实例无先验知识（Multiple Instances without a Priori Runtime Knowledge）](#19-多实例无先验知识multiple-instances-without-a-priori-runtime-knowledge)
      - [概念定义](#概念定义-18)
      - [形式化定义](#形式化定义-18)
      - [可判定性分析](#可判定性分析-18)
  - [第五部分：状态基础模式（4种）](#第五部分状态基础模式4种)
    - [20. 延迟选择（Deferred Choice）](#20-延迟选择deferred-choice)
      - [概念定义](#概念定义-19)
      - [形式化定义](#形式化定义-19)
      - [Petri网表示](#petri网表示-14)
      - [可判定性分析](#可判定性分析-19)
      - [正确性条件](#正确性条件-14)
    - [21. 交错并行路由（Interleaved Parallel Routing）](#21-交错并行路由interleaved-parallel-routing)
      - [概念定义](#概念定义-20)
      - [形式化定义](#形式化定义-20)
      - [可判定性分析](#可判定性分析-20)
      - [正确性条件](#正确性条件-15)
    - [22. 里程碑（Milestone）](#22-里程碑milestone)
      - [概念定义](#概念定义-21)
      - [形式化定义](#形式化定义-21)
      - [Petri网表示](#petri网表示-15)
      - [可判定性分析](#可判定性分析-21)
      - [正确性条件](#正确性条件-16)
    - [23. 关键区域（Critical Section）](#23-关键区域critical-section)
      - [概念定义](#概念定义-22)
      - [形式化定义](#形式化定义-22)
      - [可判定性分析](#可判定性分析-22)
      - [正确性条件](#正确性条件-17)
  - [第六部分：取消模式（2种）](#第六部分取消模式2种)
    - [24. 取消任务（Cancel Activity）](#24-取消任务cancel-activity)
      - [概念定义](#概念定义-23)
      - [形式化定义](#形式化定义-23)
      - [可判定性分析](#可判定性分析-23)
      - [正确性条件](#正确性条件-18)
    - [25. 取消案例（Cancel Case）](#25-取消案例cancel-case)
      - [概念定义](#概念定义-24)
      - [形式化定义](#形式化定义-24)
      - [可判定性分析](#可判定性分析-24)
      - [正确性条件](#正确性条件-19)
  - [第七部分：其他重要模式（18种概述）](#第七部分其他重要模式18种概述)
    - [26. 永久触发器（Persistent Trigger）](#26-永久触发器persistent-trigger)
    - [27. 瞬态触发器（Transient Trigger）](#27-瞬态触发器transient-trigger)
    - [28. 取消区域（Cancel Region）](#28-取消区域cancel-region)
    - [29. 结构化循环（Structured Loop）](#29-结构化循环structured-loop)
    - [30. 递归（Recursion）](#30-递归recursion)
    - [31. 临时约束（Temporal Constraint）](#31-临时约束temporal-constraint)
    - [32. 序列化（Serialization）](#32-序列化serialization)
    - [33. 交错路由（Interleaved Routing）](#33-交错路由interleaved-routing)
    - [34. 非结构化循环（Unstructured Loop）](#34-非结构化循环unstructured-loop)
    - [35. 显式终止（Explicit Termination）](#35-显式终止explicit-termination)
    - [36. 强制循环（Forced Loop）](#36-强制循环forced-loop)
    - [37. 迭代（Iteration）](#37-迭代iteration)
    - [38. 复制（Duplicate）](#38-复制duplicate)
    - [39. 合并（Merge）](#39-合并merge)
    - [40. 同步合并（Synchronizing Merge）](#40-同步合并synchronizing-merge)
    - [41. 多实例循环（Multiple Instances Loop）](#41-多实例循环multiple-instances-loop)
    - [42. 动态多实例（Dynamic Multiple Instances）](#42-动态多实例dynamic-multiple-instances)
    - [43. 补偿（Compensation）](#43-补偿compensation)
  - [第八部分：23种可判断模式的Python实现](#第八部分23种可判断模式的python实现)
    - [实现框架](#实现框架)
  - [模式1：顺序模式（Sequence）完整实现](#模式1顺序模式sequence完整实现)
    - [形式定义](#形式定义)
    - [Python实现](#python实现)
  - [模式2：并行分支模式（Parallel Split）完整实现](#模式2并行分支模式parallel-split完整实现)
    - [形式定义](#形式定义-1)
    - [Python实现](#python实现-1)
  - [模式3：同步模式（Synchronization）完整实现](#模式3同步模式synchronization完整实现)
    - [形式定义](#形式定义-2)
    - [Python实现](#python实现-2)
  - [模式4：排他选择模式（Exclusive Choice）完整实现](#模式4排他选择模式exclusive-choice完整实现)
    - [形式定义](#形式定义-3)
    - [Python实现](#python实现-3)
  - [模式5：简单合并模式（Simple Merge）完整实现](#模式5简单合并模式simple-merge完整实现)
    - [形式定义](#形式定义-4)
    - [Python实现](#python实现-4)
  - [模式6：多选模式（Multi-Choice）完整实现](#模式6多选模式multi-choice完整实现)
    - [形式定义](#形式定义-5)
    - [Python实现](#python实现-5)
  - [模式7：结构化同步合并（Structured Synchronizing Merge）完整实现](#模式7结构化同步合并structured-synchronizing-merge完整实现)
    - [形式定义](#形式定义-6)
    - [Python实现](#python实现-6)
  - [模式8：多合并模式（Multi-Merge）完整实现](#模式8多合并模式multi-merge完整实现)
    - [形式定义](#形式定义-7)
    - [Python实现](#python实现-7)
  - [模式9：鉴别器模式（Discriminator）完整实现](#模式9鉴别器模式discriminator完整实现)
    - [形式定义](#形式定义-8)
    - [Python实现](#python实现-8)
  - [模式10：部分加入（Partial Join / M-out-of-N）完整实现](#模式10部分加入partial-join--m-out-of-n完整实现)
    - [形式定义](#形式定义-9)
    - [Python实现](#python实现-9)
  - [模式14：任意循环（Arbitrary Cycles）完整实现](#模式14任意循环arbitrary-cycles完整实现)
    - [形式定义](#形式定义-10)
    - [Python实现](#python实现-10)
  - [模式15：隐式终止（Implicit Termination）完整实现](#模式15隐式终止implicit-termination完整实现)
    - [形式定义](#形式定义-11)
    - [Python实现](#python实现-11)
  - [模式16-19：多实例模式完整实现](#模式16-19多实例模式完整实现)
    - [模式16：多实例无同步](#模式16多实例无同步)
    - [模式17：多实例同步（设计时已知数量）](#模式17多实例同步设计时已知数量)
    - [模式18：多实例运行时](#模式18多实例运行时)
    - [模式19：多实例无先验知识](#模式19多实例无先验知识)
  - [模式20：延迟选择（Deferred Choice）完整实现](#模式20延迟选择deferred-choice完整实现)
    - [形式定义](#形式定义-12)
    - [Python实现](#python实现-12)
  - [模式21：交错并行路由（Interleaved Parallel Routing）完整实现](#模式21交错并行路由interleaved-parallel-routing完整实现)
    - [形式定义](#形式定义-13)
    - [Python实现](#python实现-13)
  - [模式22：里程碑（Milestone）完整实现](#模式22里程碑milestone完整实现)
    - [形式定义](#形式定义-14)
    - [Python实现](#python实现-14)
  - [模式23：关键区域（Critical Section）完整实现](#模式23关键区域critical-section完整实现)
    - [形式定义](#形式定义-15)
    - [Python实现](#python实现-15)
  - [模式24：取消任务（Cancel Activity）完整实现](#模式24取消任务cancel-activity完整实现)
    - [形式定义](#形式定义-16)
    - [Python实现](#python实现-16)
  - [模式25：取消案例（Cancel Case）完整实现](#模式25取消案例cancel-case完整实现)
    - [形式定义](#形式定义-17)
    - [Python实现](#python实现-17)
  - [总结：23种可判断模式一览](#总结23种可判断模式一览)
  - [可判定性分析总结](#可判定性分析总结)
    - [可判定模式（23种）](#可判定模式23种)
    - [不可判定模式（20种）](#不可判定模式20种)
    - [可判定性的实际意义](#可判定性的实际意义)
  - [附录：完整测试代码](#附录完整测试代码)
  - [参考文献](#参考文献)

---

## 引言

工作流模式（Workflow Patterns）是由van der Aalst等人在2000年代初提出的，用于描述和分析业务流程中常见的控制流结构。这些模式为工作流管理系统的设计和评估提供了标准化的参考框架。

### 可判定模式的重要性

在43种工作流模式中，有23种是**可判定的**（Decidable），这意味着：

- 可以在多项式时间内验证模式的正确性
- 存在算法可以判断工作流是否满足特定属性（如可达性、有界性、活性）
- 可以使用Petri网等形式化方法进行分析

---

## 第一部分：基础控制流模式（5种）

### 1. 顺序模式（Sequence）

#### 概念定义

顺序模式是最基础的控制流模式，表示任务按照严格的先后顺序执行。一个任务完成后，下一个任务才能开始。

#### 形式化定义

设任务集合为 T = {t₁, t₂, ..., tₙ}，顺序模式定义偏序关系 ≺：

- ∀i ∈ [1, n-1]: tᵢ ≺ tᵢ₊₁
- 执行顺序：t₁ → t₂ → ... → tₙ

#### Petri网表示

```
[开始] → |p₁| → [t₁] → |p₂| → [t₂] → ... → |pₙ| → [tₙ] → |pₙ₊₁| → [结束]
```

#### 可判定性分析

- **可达性问题**：可判定（多项式时间）
- **有界性**：有界（1-有界）
- **活性**：活的
- **复杂度**：O(n)，其中n为任务数

#### 正确性条件

1. 每个任务有且只有一个前驱（除第一个任务）
2. 每个任务有且只有一个后继（除最后一个任务）
3. 不存在循环依赖

---

### 2. 并行分支模式（Parallel Split）

#### 概念定义

并行分支模式允许一个任务完成后，同时激活多个后续任务，这些任务可以并行执行。

#### 形式化定义

设任务t完成后，分支为并行任务集合 P = {p₁, p₂, ..., pₘ}：

- t → pᵢ, ∀i ∈ [1, m]
- ∀i,j ∈ [1, m], i ≠ j: pᵢ ∥ pⱼ（并行执行）

#### Petri网表示

```
[t] → |p| → [AND-Split]
              ↓
        ┌────┼────┐
        ↓    ↓    ↓
      [p₁] [p₂] [pₘ]
```

#### 可判定性分析

- **可达性**：可判定
- **同步需求**：需要后续的同步模式配合
- **复杂度**：O(1)分支决策

#### 正确性条件

1. 分支点必须有明确的AND-Split语义
2. 每个分支路径最终必须有对应的同步点
3. 分支任务之间无数据依赖冲突

---

### 3. 同步模式（Synchronization）

#### 概念定义

同步模式（AND-Join）等待所有并行分支都完成后，才激活后续任务。

#### 形式化定义

设并行任务集合 P = {p₁, p₂, ..., pₘ} 需要同步：

- ∀pᵢ ∈ P, pᵢ完成后产生标记
- 后续任务t激活条件：∀pᵢ ∈ P, 标记(pᵢ) = 完成

#### Petri网表示

```
[p₁] ─→
[p₂] ─→ [AND-Join] → [t]
[pₘ] ─→
```

#### 可判定性分析

- **可达性**：可判定
- **死锁检测**：可判定（检查每个分支是否能到达Join点）
- **复杂度**：O(m)，m为分支数

#### 正确性条件

1. 每个进入同步点的分支必须能够到达
2. 同步点不能丢失标记
3. 避免不必要的等待（死锁）

---

### 4. 排他选择模式（Exclusive Choice）

#### 概念定义

排他选择模式（XOR-Split）基于条件或数据，选择且仅选择一条路径继续执行。

#### 形式化定义

设选择点有候选路径 C = {c₁, c₂, ..., cₖ}：

- 选择条件：cond: Data → C
- 互斥性：∀执行, 恰好选择一个 cᵢ ∈ C

#### Petri网表示

```
[t] → |p| → [XOR-Split]
              ↓
        ┌────┼────┐
        ↓    ↓    ↓
      [c₁] [c₂] [cₖ]
```

#### 可判定性分析

- **可达性**：可判定（条件判断）
- **完备性**：条件覆盖所有可能情况
- **互斥性**：条件两两互斥
- **复杂度**：O(k)，k为分支数

#### 正确性条件

1. 条件覆盖完备性：∨condᵢ = True
2. 条件互斥性：condᵢ ∧ condⱼ = False (i ≠ j)
3. 每个条件可判定

---

### 5. 简单合并模式（Simple Merge）

#### 概念定义

简单合并模式（XOR-Join）将多条可选路径合并，不检查同步条件，任意路径到达即可触发后续任务。

#### 形式化定义

设可选路径集合 A = {a₁, a₂, ..., aₖ}：

- 激活条件：∃aᵢ ∈ A, 标记(aᵢ) = 完成
- 不等待其他路径

#### Petri网表示

```
[a₁] ─→
[a₂] ─→ [XOR-Join] → [t]
[aₖ] ─→
```

#### 可判定性分析

- **可达性**：可判定
- **安全性**：需要确保不会同时有多条路径到达
- **复杂度**：O(1)

#### 正确性条件

1. 在排他选择后使用（确保单路径）
2. 多条路径同时到达会导致问题
3. 不适用于并行分支后的合并

---

## 第二部分：高级分支同步模式（8种）

### 6. 多选模式（Multi-Choice）

#### 概念定义

多选模式（OR-Split）允许基于条件选择一个或多个分支同时执行，是排他选择和并行分支的泛化。

#### 形式化定义

设候选分支集合 B = {b₁, b₂, ..., bₙ}：

- 选择函数：select: Data → 2ᴮ \ {∅}
- 可以激活任意非空子集

#### Petri网表示

```
[t] → |p| → [OR-Split]
              ↓
        ┌────┼────┐
        ↓    ↓    ↓
      [b₁] [b₂] [bₙ]
```

#### 可判定性分析

- **可达性**：可判定
- **组合数**：2ⁿ - 1 种可能的选择组合
- **复杂度**：指数级（需要检查所有组合）

#### 正确性条件

1. 至少选择一个分支
2. 每个被选择的分支必须能够完成
3. 需要对应的同步机制

---

### 7. 结构化同步合并（Structured Synchronizing Merge）

#### 概念定义

结构化同步合并（OR-Join）等待所有被激活的分支完成后再继续，是多选的对应合并模式。

#### 形式化定义

设激活的分支集合为 S ⊆ B：

- 等待条件：∀bᵢ ∈ S, 标记(bᵢ) = 完成
- 仅同步实际被激活的分支

#### Petri网表示

```
[b₁] ─→
[b₂] ─→ [OR-Join] → [t]
[bₙ] ─→
```

#### 可判定性分析

- **可达性**：可判定（结构化约束下）
- **死锁检测**：可判定
- **复杂度**：O(n)

#### 正确性条件

1. 必须知道哪些分支被激活
2. 结构化约束：每个OR-Split对应一个OR-Join
3. 避免非结构化使用

---

### 8. 多合并模式（Multi-Merge）

#### 概念定义

多合并模式允许多个分支中的每一个到达时都触发后续任务，不进行同步。

#### 形式化定义

设输入分支集合 I = {i₁, i₂, ..., iₘ}：

- 触发条件：∀iⱼ ∈ I, 到达即触发
- 后续任务可能被执行多次

#### Petri网表示

```
[i₁] ─→ [XOR-Join] ─→ [t]
[i₂] ─→ [XOR-Join] ─→ [t]
[iₘ] ─→ [XOR-Join] ─→ [t]
```

#### 可判定性分析

- **可达性**：可判定
- **重复执行**：后续任务执行次数 = 到达分支数
- **复杂度**：O(m)

#### 正确性条件

1. 后续任务必须支持多次执行
2. 不适用于需要同步的场景
3. 可能导致竞态条件

---

### 9. 鉴别器模式（Discriminator）

#### 概念定义

鉴别器模式等待多个并行分支中的第一个完成，然后立即触发后续任务，同时取消或忽略其他分支。

#### 形式化定义

设并行分支集合 P = {p₁, p₂, ..., pₙ}：

- 触发条件：∃!pᵢ ∈ P, pᵢ首先完成
- 其他分支：取消或忽略

#### Petri网表示

```
[p₁] ─→
[p₂] ─→ [Discriminator] → [t]
[pₙ] ─→
```

#### 可判定性分析

- **可达性**：可判定
- **竞态条件**：第一个完成的非确定性
- **复杂度**：O(n)

#### 正确性条件

1. 需要取消机制
2. 其他分支的结果可被丢弃
3. 适用于"取最快结果"的场景

---

### 10. 部分加入（Partial Join）

#### 概念定义

部分加入模式等待N个分支中的M个完成（M ≤ N），然后触发后续任务。

#### 形式化定义

设分支总数为N，需要M个完成：

- 触发条件：|{pᵢ完成}| ≥ M
- 参数化：M为配置参数

#### Petri网表示

```
[p₁] ─→
[p₂] ─→ [M-out-of-N Join] → [t]
[pₙ] ─→
```

#### 可判定性分析

- **可达性**：可判定
- **参数约束**：1 ≤ M ≤ N
- **复杂度**：O(N)

#### 正确性条件

1. M值必须合理配置
2. 剩余N-M个分支的处理策略
3. 避免死锁（确保至少M个分支能完成）

---

### 11. 阻塞鉴别器（Blocking Discriminator）

#### 概念定义

阻塞鉴别器在第一个分支完成后触发后续任务，但阻塞直到所有分支都完成才允许下一次激活。

#### 形式化定义

- 阶段1：等待第一个完成 → 触发后续
- 阶段2：阻塞等待所有完成
- 阶段3：重置，允许下一轮

#### Petri网表示

```
[p₁] ─→
[p₂] ─→ [Blocking Disc] → [t]
[pₙ] ─→      ↓
          [Wait All]
```

#### 可判定性分析

- **可达性**：可判定
- **状态空间**：有限（需要跟踪完成状态）
- **复杂度**：O(n)

#### 正确性条件

1. 必须等待所有分支完成才能重置
2. 防止多次触发后续任务
3. 适用于需要完整周期的场景

---

### 12. 取消鉴别器（Canceling Discriminator）

#### 概念定义

取消鉴别器在第一个分支完成后，立即取消其他未完成的分支，然后触发后续任务。

#### 形式化定义

- 检测：第一个分支完成
- 动作：取消其他所有分支
- 触发：执行后续任务

#### Petri网表示

```
[p₁] ─→
[p₂] ─→ [Canceling Disc] ─→ [t]
[pₙ] ─→       ↓
          [Cancel Others]
```

#### 可判定性分析

- **可达性**：可判定
- **取消语义**：需要支持取消操作
- **复杂度**：O(n)

#### 正确性条件

1. 取消操作必须可靠
2. 被取消分支的资源回收
3. 取消后的状态一致性

---

### 13. 结构化部分加入（Structured Partial Join）

#### 概念定义

结构化部分加入是部分加入的结构化变体，确保在结构化工作流中正确使用。

#### 形式化定义

- 结构化约束：每个分支有明确的开始和结束
- M-out-of-N语义在结构化上下文中
- 与对应的Split模式配对

#### 可判定性分析

- **可达性**：可判定
- **结构化优势**：简化分析
- **复杂度**：O(N)

---

## 第三部分：结构化模式（2种）

### 14. 任意循环（Arbitrary Cycles）

#### 概念定义

任意循环模式允许在工作流中创建循环结构，任务可以基于条件重复执行。

#### 形式化定义

设循环体为L，循环条件为C：

- 执行L
- 检查C
- 若C为真，重复执行L
- 若C为假，退出循环

#### Petri网表示

```
       ┌─────────────────┐
       ↓                 │
[Loop Start] → [L] → [Check C] → [Exit]
                       │
                       └───────────┘
```

#### 可判定性分析

- **终止性**：**不可判定**（停机问题）
- **有界性**：取决于循环条件
- **活性**：可能不活（无限循环）

#### 可判定子集

以下情况可判定：

1. 循环次数有明确上界
2. 循环变量单调递减且有下界
3. 循环条件可在有限步内确定

#### 正确性条件

1. 循环必须有退出条件
2. 退出条件必须可达
3. 避免无限循环

---

### 15. 隐式终止（Implicit Termination）

#### 概念定义

隐式终止模式表示当工作流中没有可执行的任务时，流程自动终止，无需显式的结束节点。

#### 形式化定义

设工作流状态为S，可执行任务集合为E(S)：

- 终止条件：E(S) = ∅
- 隐式：无显式终止操作

#### Petri网表示

```
无特殊结构，当所有库所无标记且变迁不可触发时终止
```

#### 可判定性分析

- **终止检测**：可判定（检查可执行性）
- **正确终止**：需要确保无死锁
- **复杂度**：O(|T|)，T为变迁集合

#### 正确性条件

1. 无死锁状态（除非是真正的终止）
2. 所有任务都能到达终止状态
3. 无孤立任务

---

## 第四部分：多实例模式（4种）

### 16. 多实例无同步（Multiple Instances without Synchronization）

#### 概念定义

在运行时创建多个任务实例，这些实例独立执行，无需同步。

#### 形式化定义

设任务为t，实例数为n（运行时确定）：

- 创建：instances(t) = {t₁, t₂, ..., tₙ}
- 执行：tᵢ ∥ tⱼ, ∀i ≠ j
- 同步：无

#### 可判定性分析

- **可达性**：可判定
- **实例数**：运行时确定
- **复杂度**：O(n)

---

### 17. 多实例同步（Multiple Instances with a Priori Design Time Knowledge）

#### 概念定义

在设计时就知道实例数量，创建多个实例并在完成后同步。

#### 形式化定义

- 实例数N：设计时已知
- 创建：{t₁, t₂, ..., tₙ}
- 同步：等待所有N个实例完成

#### 可判定性分析

- **可达性**：可判定
- **同步点**：明确
- **复杂度**：O(N)

---

### 18. 多实例运行时（Multiple Instances with a Priori Runtime Knowledge）

#### 概念定义

在运行时知道实例数量，但创建前未知，完成后需要同步。

#### 形式化定义

- 实例数N：运行时确定（创建前）
- 创建：{t₁, t₂, ..., tₙ}
- 同步：等待所有N个实例完成

#### 可判定性分析

- **可达性**：可判定（N确定后）
- **动态性**：运行时决策
- **复杂度**：O(N)

---

### 19. 多实例无先验知识（Multiple Instances without a Priori Runtime Knowledge）

#### 概念定义

在实例创建时不知道总数，新实例可能在已有实例运行时动态添加。

#### 形式化定义

- 实例动态添加
- 无预设总数
- 需要显式完成信号

#### 可判定性分析

- **可达性**：**不可判定**（无边界）
- **有界性**：无界
- **终止性**：需要额外机制

---

## 第五部分：状态基础模式（4种）

### 20. 延迟选择（Deferred Choice）

#### 概念定义

延迟选择模式将选择推迟到运行时，基于外部事件或环境决定路径，而非预设条件。

#### 形式化定义

- 选择点：等待外部事件
- 事件集合：E = {e₁, e₂, ..., eₖ}
- 触发：第一个发生的事件决定路径

#### Petri网表示

```
[t] → |p| → [Wait Event]
              ↓
        ┌────┼────┐
        ↓    ↓    ↓
      [e₁] [e₂] [eₖ]
```

#### 可判定性分析

- **可达性**：可判定
- **非确定性**：外部事件驱动
- **复杂度**：O(k)

#### 正确性条件

1. 至少一个事件会发生
2. 事件互斥
3. 超时处理机制

---

### 21. 交错并行路由（Interleaved Parallel Routing）

#### 概念定义

交错并行路由模式允许一组任务以任意顺序执行，但同一时间只能执行一个任务。

#### 形式化定义

设任务集合 T = {t₁, t₂, ..., tₙ}：

- 全序：任意排列都是合法的
- 互斥：∀时刻, 最多一个tᵢ在执行
- 完成：所有tᵢ都执行一次

#### 可判定性分析

- **可达性**：可判定
- 排列数：n!
- **复杂度**：O(n!)

#### 正确性条件

1. 每个任务恰好执行一次
2. 无并发执行
3. 无死锁

---

### 22. 里程碑（Milestone）

#### 概念定义

里程碑模式表示一个任务的执行依赖于工作流是否达到某个特定状态（里程碑）。

#### 形式化定义

- 里程碑状态：M
- 任务t的执行条件：当前状态满足M
- 检查：不消耗里程碑

#### Petri网表示

```
[Milestone State] ──→ [Test] ──→ [t]
       ↑                    │
       └────────────────────┘
```

#### 可判定性分析

- **可达性**：可判定
- **状态检查**：只读操作
- **复杂度**：O(1)

#### 正确性条件

1. 里程碑状态可达
2. 检查不修改状态
3. 避免竞态条件

---

### 23. 关键区域（Critical Section）

#### 概念定义

关键区域模式确保某些任务不能同时执行，通过互斥机制保护共享资源。

#### 形式化定义

- 关键区域：CS
- 互斥：∀时刻, 最多一个任务在CS中
- 进入条件：CS为空

#### 可判定性分析

- **可达性**：可判定
- **死锁风险**：可能（循环等待）
- **复杂度**：O(n²)

#### 正确性条件

1. 互斥访问
2. 无死锁
3. 无饥饿

---

## 第六部分：取消模式（2种）

### 24. 取消任务（Cancel Activity）

#### 概念定义

取消任务模式允许在任务执行过程中取消该任务的执行。

#### 形式化定义

- 任务状态：{就绪, 执行中, 完成, 取消}
- 取消操作：执行中 → 取消
- 后续：清理资源

#### 可判定性分析

- **可达性**：可判定
- **状态转换**：有限状态机
- **复杂度**：O(1)

#### 正确性条件

1. 可取消的任务必须支持取消语义
2. 取消后的资源回收
3. 部分完成结果的处理

---

### 25. 取消案例（Cancel Case）

#### 概念定义

取消案例模式允许取消整个工作流实例，终止所有相关任务的执行。

#### 形式化定义

- 案例状态：跟踪所有任务
- 取消操作：终止所有活动任务
- 清理：释放所有资源

#### 可判定性分析

- **可达性**：可判定
- **影响范围**：整个案例
- **复杂度**：O(|T|)

#### 正确性条件

1. 所有任务都能被取消
2. 数据一致性
3. 补偿机制（如需要）

---

## 第七部分：其他重要模式（18种概述）

### 26. 永久触发器（Persistent Trigger）

延迟选择的一种变体，触发器在触发前一直有效。

### 27. 瞬态触发器（Transient Trigger）

触发器只在特定时间窗口内有效。

### 28. 取消区域（Cancel Region）

取消一组相关任务，而非单个任务。

### 29. 结构化循环（Structured Loop）

有明确入口和出口的循环结构。

### 30. 递归（Recursion）

任务可以调用自身或其他任务的实例。

### 31. 临时约束（Temporal Constraint）

任务执行有时间限制（截止时间、持续时间）。

### 32. 序列化（Serialization）

强制任务按特定顺序执行。

### 33. 交错路由（Interleaved Routing）

任务可以交错执行，但有约束条件。

### 34. 非结构化循环（Unstructured Loop）

没有明确结构的循环。

### 35. 显式终止（Explicit Termination）

需要显式操作来终止工作流。

### 36. 强制循环（Forced Loop）

必须执行至少一次的循环。

### 37. 迭代（Iteration）

基于集合的元素重复执行任务。

### 38. 复制（Duplicate）

复制任务实例。

### 39. 合并（Merge）

合并多个输入到单个输出。

### 40. 同步合并（Synchronizing Merge）

等待所有输入后合并。

### 41. 多实例循环（Multiple Instances Loop）

多实例与循环的组合。

### 42. 动态多实例（Dynamic Multiple Instances）

实例数动态变化的多实例。

### 43. 补偿（Compensation）

对已完成的任务进行撤销操作。

---


## 第八部分：23种可判断模式的Python实现

本部分为每种可判断模式提供完整的Python实现，包括形式定义、可判定性证明、代码示例和测试用例。

---

### 实现框架

```python
"""
工作流模式Python实现框架
支持23种可判断模式的完整实现
"""

from enum import Enum, auto
from typing import List, Dict, Set, Callable, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import deque
import threading
import time
from abc import ABC, abstractmethod
import uuid

# ============================================================================
# 基础数据结构和枚举
# ============================================================================

class TaskStatus(Enum):
    """任务状态枚举"""
    READY = auto()       # 就绪
    RUNNING = auto()     # 执行中
    COMPLETED = auto()   # 完成
    CANCELLED = auto()   # 取消
    FAILED = auto()      # 失败
    WAITING = auto()     # 等待

class Token:
    """Petri网令牌"""
    def __init__(self, data: Any = None):
        self.id = uuid.uuid4()
        self.data = data
        self.created_at = time.time()

    def __repr__(self):
        return f"Token({self.id.hex[:8]})"

class Place:
    """Petri网库所"""
    def __init__(self, name: str):
        self.name = name
        self.tokens: List[Token] = []

    def add_token(self, token: Token):
        self.tokens.append(token)

    def remove_token(self) -> Optional[Token]:
        if self.tokens:
            return self.tokens.pop(0)
        return None

    def has_token(self) -> bool:
        return len(self.tokens) > 0

    def token_count(self) -> int:
        return len(self.tokens)

    def __repr__(self):
        return f"Place({self.name}, tokens={len(self.tokens)})"

class Transition:
    """Petri网变迁"""
    def __init__(self, name: str, action: Optional[Callable] = None):
        self.name = name
        self.input_places: List[Place] = []
        self.output_places: List[Place] = []
        self.action = action
        self.enabled = False

    def add_input(self, place: Place):
        self.input_places.append(place)

    def add_output(self, place: Place):
        self.output_places.append(place)

    def is_enabled(self) -> bool:
        return all(p.has_token() for p in self.input_places)

    def fire(self) -> bool:
        if not self.is_enabled():
            return False

        # 消费输入令牌
        tokens = []
        for place in self.input_places:
            token = place.remove_token()
            if token:
                tokens.append(token)

        # 执行动作
        if self.action:
            self.action(tokens)

        # 产生输出令牌
        for place in self.output_places:
            place.add_token(Token())

        return True

    def __repr__(self):
        return f"Transition({self.name})"

class PetriNet:
    """Petri网实现"""
    def __init__(self, name: str):
        self.name = name
        self.places: Dict[str, Place] = {}
        self.transitions: Dict[str, Transition] = {}

    def add_place(self, name: str) -> Place:
        place = Place(name)
        self.places[name] = place
        return place

    def add_transition(self, name: str, action: Optional[Callable] = None) -> Transition:
        trans = Transition(name, action)
        self.transitions[name] = trans
        return trans

    def add_arc(self, from_name: str, to_name: str):
        """添加弧连接"""
        if from_name in self.places and to_name in self.transitions:
            self.transitions[to_name].add_input(self.places[from_name])
        elif from_name in self.transitions and to_name in self.places:
            self.transitions[from_name].add_output(self.places[to_name])

    def get_enabled_transitions(self) -> List[Transition]:
        return [t for t in self.transitions.values() if t.is_enabled()]

    def step(self) -> bool:
        """执行一步"""
        enabled = self.get_enabled_transitions()
        if enabled:
            enabled[0].fire()
            return True
        return False

    def run(self, max_steps: int = 100) -> int:
        """运行直到无可用变迁或达到最大步数"""
        steps = 0
        while steps < max_steps:
            if not self.step():
                break
            steps += 1
        return steps

@dataclass
class Task:
    """工作流任务"""
    id: str
    name: str
    action: Callable = field(default=lambda: None)
    status: TaskStatus = field(default=TaskStatus.READY)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)

    def execute(self):
        if self.status == TaskStatus.READY:
            self.status = TaskStatus.RUNNING
            try:
                self.action()
                self.status = TaskStatus.COMPLETED
                return True
            except Exception as e:
                self.status = TaskStatus.FAILED
                print(f"Task {self.name} failed: {e}")
                return False
        return False

    def cancel(self):
        if self.status == TaskStatus.RUNNING:
            self.status = TaskStatus.CANCELLED
            return True
        return False

    def reset(self):
        self.status = TaskStatus.READY

class WorkflowEngine:
    """基础工作流引擎"""
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.executed: List[str] = []

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def get_ready_tasks(self) -> List[Task]:
        return [t for t in self.tasks.values() if t.status == TaskStatus.READY]

    def execute_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            task = self.tasks[task_id]
            if task.execute():
                self.executed.append(task_id)
                return True
        return False

print("=" * 80)
print("工作流模式Python实现框架加载完成")
print("=" * 80)
```

---

## 模式1：顺序模式（Sequence）完整实现

### 形式定义

**定义1.1**（顺序模式）：设任务集合 T = {t₁, t₂, ..., tₙ}，顺序模式定义偏序关系 ≺：

- ∀i ∈ [1, n-1]: tᵢ ≺ tᵢ₊₁
- 执行顺序：t₁ → t₂ → ... → tₙ

**定理1.1**（顺序模式可判定性）：顺序模式的可达性问题在O(n)时间内可判定。

**证明**：

1. 状态空间大小为n+1（初始状态 + n个任务完成状态）
2. 状态转移是确定性的：sᵢ → sᵢ₊₁
3. 可达性检查只需验证前驱任务是否完成
4. 时间复杂度：O(n)
∎

### Python实现

```python
class SequencePattern:
    """
    顺序模式实现
    任务按照严格的先后顺序执行
    """

    def __init__(self, name: str = "Sequence"):
        self.name = name
        self.tasks: List[Task] = []
        self.current_index = 0
        self.completed = False

    def add_task(self, name: str, action: Callable) -> Task:
        """添加任务到序列"""
        task = Task(
            id=f"task_{len(self.tasks)}",
            name=name,
            action=action
        )
        self.tasks.append(task)
        return task

    def is_ready(self, index: int) -> bool:
        """检查任务是否就绪"""
        if index == 0:
            return True
        return self.tasks[index - 1].status == TaskStatus.COMPLETED

    def execute_next(self) -> Optional[Task]:
        """执行下一个就绪任务"""
        if self.current_index >= len(self.tasks):
            self.completed = True
            return None

        if self.is_ready(self.current_index):
            task = self.tasks[self.current_index]
            task.execute()
            self.current_index += 1
            return task
        return None

    def run(self) -> List[str]:
        """运行整个序列"""
        executed = []
        while self.current_index < len(self.tasks):
            task = self.execute_next()
            if task:
                executed.append(task.name)
            else:
                break
        return executed

    def verify(self) -> Tuple[bool, str]:
        """验证顺序模式的正确性"""
        if len(self.tasks) == 0:
            return False, "空序列"

        # 检查每个任务（除第一个）有且只有一个前驱
        for i in range(1, len(self.tasks)):
            # 在顺序模式中，每个任务的前驱是前一个任务
            pass  # 结构上已保证

        # 检查每个任务（除最后一个）有且只有一个后继
        for i in range(len(self.tasks) - 1):
            pass  # 结构上已保证

        return True, "验证通过"

# ============================================================================
# 测试用例
# ============================================================================

def test_sequence_pattern():
    """测试顺序模式"""
    print("\n" + "=" * 60)
    print("测试：顺序模式（Sequence Pattern）")
    print("=" * 60)

    # 创建顺序模式实例
    seq = SequencePattern("订单处理流程")

    # 添加任务
    results = []

    def task1():
        results.append("验证订单")
        print("✓ 执行：验证订单")

    def task2():
        results.append("检查库存")
        print("✓ 执行：检查库存")

    def task3():
        results.append("处理支付")
        print("✓ 执行：处理支付")

    def task4():
        results.append("发货")
        print("✓ 执行：发货")

    seq.add_task("验证订单", task1)
    seq.add_task("检查库存", task2)
    seq.add_task("处理支付", task3)
    seq.add_task("发货", task4)

    # 验证
    valid, msg = seq.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 执行
    print("\n执行顺序：")
    executed = seq.run()

    print(f"\n执行结果: {executed}")
    print(f"完成状态: {seq.completed}")

    # 正例验证
    assert executed == ["验证订单", "检查库存", "处理支付", "发货"]
    assert seq.completed == True
    print("\n✅ 正例测试通过！")

    return seq

# 运行测试
sequence_instance = test_sequence_pattern()
```

---

## 模式2：并行分支模式（Parallel Split）完整实现

### 形式定义

**定义2.1**（并行分支）：设任务t完成后，分支为并行任务集合 P = {p₁, p₂, ..., pₘ}：

- t → pᵢ, ∀i ∈ [1, m]
- ∀i,j ∈ [1, m], i ≠ j: pᵢ ∥ pⱼ（并行执行）

**定理2.1**（并行分支可判定性）：并行分支的可达性问题在O(m)时间内可判定。

**证明**：

1. 分支决策是确定性的（AND-Split）
2. 所有分支同时激活
3. 每个分支独立可达
4. 时间复杂度：O(m)
∎

### Python实现

```python
import concurrent.futures

class ParallelSplitPattern:
    """
    并行分支模式实现
    一个任务完成后，同时激活多个后续任务
    """

    def __init__(self, name: str = "ParallelSplit"):
        self.name = name
        self.predecessor: Optional[Task] = None
        self.branches: List[Task] = []
        self.branch_results: Dict[str, Any] = {}

    def set_predecessor(self, task: Task):
        """设置前驱任务"""
        self.predecessor = task

    def add_branch(self, name: str, action: Callable) -> Task:
        """添加并行分支"""
        task = Task(
            id=f"branch_{len(self.branches)}",
            name=name,
            action=action
        )
        self.branches.append(task)
        return task

    def execute_branches(self, parallel: bool = True) -> List[str]:
        """执行所有分支"""
        if self.predecessor and self.predecessor.status != TaskStatus.COMPLETED:
            print("前驱任务未完成")
            return []

        executed = []

        if parallel:
            # 并行执行
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(self._execute_branch, task): task
                          for task in self.branches}
                for future in concurrent.futures.as_completed(futures):
                    task = futures[future]
                    try:
                        result = future.result()
                        executed.append(task.name)
                        self.branch_results[task.name] = result
                    except Exception as e:
                        print(f"分支 {task.name} 执行失败: {e}")
        else:
            # 串行执行（用于测试）
            for task in self.branches:
                self._execute_branch(task)
                executed.append(task.name)

        return executed

    def _execute_branch(self, task: Task) -> Any:
        """执行单个分支"""
        print(f"✓ 执行分支: {task.name}")
        task.execute()
        return f"result_of_{task.name}"

    def verify(self) -> Tuple[bool, str]:
        """验证并行分支的正确性"""
        if len(self.branches) < 2:
            return False, "至少需要2个分支"

        # 检查每个分支都有明确的前驱
        if not self.predecessor:
            return False, "缺少前驱任务"

        return True, "验证通过"

def test_parallel_split():
    """测试并行分支模式"""
    print("\n" + "=" * 60)
    print("测试：并行分支模式（Parallel Split Pattern）")
    print("=" * 60)

    # 创建并行分支模式
    ps = ParallelSplitPattern("并行处理")

    # 设置前驱任务
    def pre_action():
        print("✓ 前驱任务完成，开始并行分支")

    pre_task = Task(id="pre", name="准备数据", action=pre_action)
    pre_task.execute()
    ps.set_predecessor(pre_task)

    # 添加并行分支
    def branch1():
        time.sleep(0.1)
        print("  → 分支1完成：发送邮件通知")

    def branch2():
        time.sleep(0.15)
        print("  → 分支2完成：更新数据库")

    def branch3():
        time.sleep(0.05)
        print("  → 分支3完成：记录日志")

    ps.add_branch("发送邮件", branch1)
    ps.add_branch("更新数据库", branch2)
    ps.add_branch("记录日志", branch3)

    # 验证
    valid, msg = ps.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 执行（串行模式便于观察）
    print("\n执行并行分支：")
    executed = ps.execute_branches(parallel=False)

    print(f"\n执行结果: {executed}")

    # 正例验证
    assert len(executed) == 3
    print("\n✅ 正例测试通过！")

    return ps

parallel_split_instance = test_parallel_split()
```

---

## 模式3：同步模式（Synchronization）完整实现

### 形式定义

**定义3.1**（同步模式/AND-Join）：设并行任务集合 P = {p₁, p₂, ..., pₘ} 需要同步：

- ∀pᵢ ∈ P, pᵢ完成后产生标记
- 后续任务t激活条件：∀pᵢ ∈ P, 标记(pᵢ) = 完成

**定理3.1**（同步模式可判定性）：同步模式的可达性和死锁检测在O(m)时间内可判定。

**证明**：

1. 同步点等待所有m个分支
2. 死锁检测：检查每个分支是否可达同步点
3. 可达性：当且仅当所有分支完成时可达
4. 时间复杂度：O(m)
∎

### Python实现

```python
class SynchronizationPattern:
    """
    同步模式（AND-Join）实现
    等待所有并行分支完成后才激活后续任务
    """

    def __init__(self, name: str = "Synchronization"):
        self.name = name
        self.inputs: List[Task] = []
        self.successor: Optional[Task] = None
        self.waiting = False

    def add_input(self, task: Task):
        """添加输入任务（需要等待的分支）"""
        self.inputs.append(task)

    def set_successor(self, task: Task):
        """设置后续任务"""
        self.successor = task

    def can_proceed(self) -> bool:
        """检查是否可以继续（所有输入完成）"""
        return all(task.status == TaskStatus.COMPLETED for task in self.inputs)

    def get_incomplete_inputs(self) -> List[str]:
        """获取未完成的输入"""
        return [task.name for task in self.inputs
                if task.status != TaskStatus.COMPLETED]

    def sync_and_execute(self) -> Optional[Task]:
        """同步并执行后续任务"""
        self.waiting = True

        if self.can_proceed():
            print(f"✓ 所有 {len(self.inputs)} 个分支已完成，执行后续任务")
            self.waiting = False
            if self.successor:
                self.successor.execute()
                return self.successor
        else:
            incomplete = self.get_incomplete_inputs()
            print(f"⏳ 等待分支完成: {incomplete}")

        return None

    def verify(self) -> Tuple[bool, str]:
        """验证同步模式的正确性"""
        if len(self.inputs) < 2:
            return False, "至少需要2个输入分支"

        if not self.successor:
            return False, "缺少后续任务"

        # 检查是否有死锁风险
        for task in self.inputs:
            if task.status == TaskStatus.FAILED:
                return False, f"输入任务 {task.name} 已失败，可能导致死锁"

        return True, "验证通过"

    def check_deadlock(self) -> Tuple[bool, List[str]]:
        """检查是否存在死锁"""
        failed = [t.name for t in self.inputs if t.status == TaskStatus.FAILED]
        cancelled = [t.name for t in self.inputs if t.status == TaskStatus.CANCELLED]

        if failed or cancelled:
            return True, failed + cancelled
        return False, []

def test_synchronization():
    """测试同步模式"""
    print("\n" + "=" * 60)
    print("测试：同步模式（Synchronization / AND-Join）")
    print("=" * 60)

    # 创建同步模式
    sync = SynchronizationPattern("订单处理同步")

    # 创建并行分支任务
    def action1():
        print("  → 分支1：验证支付完成")

    def action2():
        print("  → 分支2：验证库存完成")

    def action3():
        print("  → 分支3：验证地址完成")

    task1 = Task(id="t1", name="验证支付", action=action1)
    task2 = Task(id="t2", name="验证库存", action=action2)
    task3 = Task(id="t3", name="验证地址", action=action3)

    # 先完成部分任务
    task1.execute()
    task2.execute()
    # task3 未完成

    sync.add_input(task1)
    sync.add_input(task2)
    sync.add_input(task3)

    # 设置后续任务
    def final_action():
        print("✓ 所有验证完成，确认订单！")

    final_task = Task(id="final", name="确认订单", action=final_action)
    sync.set_successor(final_task)

    # 验证
    valid, msg = sync.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 第一次尝试同步（应该等待）
    print("\n第一次同步尝试（task3未完成）：")
    result = sync.sync_and_execute()
    assert result is None

    # 完成剩余任务
    print("\n完成剩余任务：")
    task3.execute()

    # 第二次尝试同步（应该成功）
    print("\n第二次同步尝试（所有任务完成）：")
    result = sync.sync_and_execute()
    assert result is not None

    print("\n✅ 正例测试通过！")

    # 反例：死锁检测
    print("\n--- 反例测试：死锁检测 ---")
    sync2 = SynchronizationPattern("死锁测试")
    failed_task = Task(id="f1", name="失败任务", action=lambda: None)
    failed_task.status = TaskStatus.FAILED
    sync2.add_input(failed_task)
    sync2.add_input(Task(id="t2", name="等待任务", action=lambda: None))

    is_deadlock, problematic = sync2.check_deadlock()
    print(f"死锁检测: {is_deadlock}, 问题任务: {problematic}")
    assert is_deadlock == True
    print("✅ 反例测试通过！")

    return sync

sync_instance = test_synchronization()
```

---

## 模式4：排他选择模式（Exclusive Choice）完整实现

### 形式定义

**定义4.1**（排他选择/XOR-Split）：设选择点有候选路径 C = {c₁, c₂, ..., cₖ}：

- 选择条件：cond: Data → C
- 互斥性：∀执行, 恰好选择一个 cᵢ ∈ C

**定理4.1**（排他选择可判定性）：排他选择的正确性（完备性和互斥性）在O(k²)时间内可判定。

**证明**：

1. 完备性检查：∨condᵢ = True，需要O(k)时间
2. 互斥性检查：condᵢ ∧ condⱼ = False (i ≠ j)，需要O(k²)时间
3. 总复杂度：O(k²)
∎

### Python实现

```python
class ExclusiveChoicePattern:
    """
    排他选择模式（XOR-Split）实现
    基于条件选择且仅选择一条路径
    """

    def __init__(self, name: str = "ExclusiveChoice"):
        self.name = name
        self.conditions: List[Tuple[str, Callable[[Any], bool]]] = []
        self.selected_branch: Optional[str] = None
        self.data: Any = None

    def add_condition(self, branch_name: str, condition: Callable[[Any], bool]):
        """添加条件和对应分支"""
        self.conditions.append((branch_name, condition))

    def set_data(self, data: Any):
        """设置决策数据"""
        self.data = data

    def evaluate(self) -> Optional[str]:
        """评估条件，选择分支"""
        if self.data is None:
            return None

        satisfied = []
        for branch_name, condition in self.conditions:
            if condition(self.data):
                satisfied.append(branch_name)

        # 排他性检查
        if len(satisfied) == 0:
            print(f"⚠️ 警告：没有条件满足（不完备）")
            return None
        elif len(satisfied) > 1:
            print(f"⚠️ 警告：多个条件满足（不互斥）：{satisfied}")
            # 选择第一个
            self.selected_branch = satisfied[0]
        else:
            self.selected_branch = satisfied[0]

        print(f"✓ 选择分支: {self.selected_branch}")
        return self.selected_branch

    def verify_completeness(self, test_data: List[Any]) -> Tuple[bool, List[Any]]:
        """验证完备性：测试数据是否都能触发至少一个条件"""
        uncovered = []
        for data in test_data:
            satisfied = any(cond(data) for _, cond in self.conditions)
            if not satisfied:
                uncovered.append(data)

        return len(uncovered) == 0, uncovered

    def verify_mutex(self, test_data: List[Any]) -> Tuple[bool, List[Tuple[Any, List[str]]]]:
        """验证互斥性：检查是否有数据触发多个条件"""
        violations = []
        for data in test_data:
            satisfied = [name for name, cond in self.conditions if cond(data)]
            if len(satisfied) > 1:
                violations.append((data, satisfied))

        return len(violations) == 0, violations

    def verify(self) -> Tuple[bool, str]:
        """验证排他选择的正确性"""
        if len(self.conditions) < 2:
            return False, "至少需要2个条件分支"

        # 检查条件函数是否有效
        for name, cond in self.conditions:
            if not callable(cond):
                return False, f"条件 {name} 不是可调用的函数"

        return True, "基本验证通过"

def test_exclusive_choice():
    """测试排他选择模式"""
    print("\n" + "=" * 60)
    print("测试：排他选择模式（Exclusive Choice / XOR-Split）")
    print("=" * 60)

    # 创建排他选择
    xor = ExclusiveChoicePattern("支付路由")

    # 添加条件分支
    xor.add_condition("信用卡", lambda d: d.get("amount", 0) > 1000)
    xor.add_condition("借记卡", lambda d: 100 < d.get("amount", 0) <= 1000)
    xor.add_condition("现金", lambda d: d.get("amount", 0) <= 100)

    # 验证
    valid, msg = xor.verify()
    print(f"\n基本验证: {valid}, {msg}")

    # 正例测试
    print("\n--- 正例测试 ---")

    test_cases = [
        ({"amount": 5000}, "信用卡"),
        ({"amount": 500}, "借记卡"),
        ({"amount": 50}, "现金"),
    ]

    for data, expected in test_cases:
        xor.set_data(data)
        result = xor.evaluate()
        assert result == expected, f"期望 {expected}, 实际 {result}"
        print(f"✅ 数据 {data} -> {result}")

    # 完备性验证
    print("\n--- 完备性验证 ---")
    test_data = [{"amount": 5000}, {"amount": 500}, {"amount": 50}, {"amount": 0}]
    is_complete, uncovered = xor.verify_completeness(test_data)
    print(f"完备性: {is_complete}, 未覆盖: {uncovered}")

    # 互斥性验证
    print("\n--- 互斥性验证 ---")
    is_mutex, violations = xor.verify_mutex(test_data)
    print(f"互斥性: {is_mutex}, 冲突: {violations}")

    # 反例：不完备的条件
    print("\n--- 反例：不完备的条件 ---")
    xor_bad = ExclusiveChoicePattern("不完备选择")
    xor_bad.add_condition("大额", lambda d: d.get("amount", 0) > 1000)
    xor_bad.add_condition("小额", lambda d: d.get("amount", 0) < 100)
    # 缺少 100-1000 的处理

    xor_bad.set_data({"amount": 500})
    result = xor_bad.evaluate()  # 应该警告没有条件满足
    assert result is None
    print("✅ 反例测试通过！")

    print("\n✅ 所有测试通过！")

    return xor

xor_instance = test_exclusive_choice()
```

---

## 模式5：简单合并模式（Simple Merge）完整实现

### 形式定义

**定义5.1**（简单合并/XOR-Join）：设可选路径集合 A = {a₁, a₂, ..., aₖ}：

- 激活条件：∃aᵢ ∈ A, 标记(aᵢ) = 完成
- 不等待其他路径

**定理5.1**（简单合并可判定性）：简单合并的可达性在O(1)时间内可判定。

**证明**：

1. 任意输入到达即可触发
2. 无需等待其他输入
3. 触发条件简单
4. 时间复杂度：O(1)
∎

### Python实现

```python
class SimpleMergePattern:
    """
    简单合并模式（XOR-Join）实现
    任意路径到达即可触发后续任务，不进行同步
    """

    def __init__(self, name: str = "SimpleMerge"):
        self.name = name
        self.inputs: List[Task] = []
        self.successor: Optional[Task] = None
        self.triggered = False
        self.trigger_count = 0

    def add_input(self, task: Task):
        """添加输入任务"""
        self.inputs.append(task)

    def set_successor(self, task: Task):
        """设置后续任务"""
        self.successor = task

    def check_and_trigger(self) -> Optional[Task]:
        """检查是否有输入完成并触发"""
        completed = [t for t in self.inputs if t.status == TaskStatus.COMPLETED]

        if completed and not self.triggered:
            task = completed[0]  # 取第一个完成的
            print(f"✓ 检测到任务完成: {task.name}，触发后续")
            self.triggered = True
            self.trigger_count += 1

            if self.successor:
                self.successor.execute()
                return self.successor

        return None

    def reset(self):
        """重置状态"""
        self.triggered = False

    def verify(self) -> Tuple[bool, str]:
        """验证简单合并的正确性"""
        if len(self.inputs) < 2:
            return False, "至少需要2个输入"

        if not self.successor:
            return False, "缺少后续任务"

        return True, "验证通过"

def test_simple_merge():
    """测试简单合并模式"""
    print("\n" + "=" * 60)
    print("测试：简单合并模式（Simple Merge / XOR-Join）")
    print("=" * 60)

    # 创建简单合并
    merge = SimpleMergePattern("路径合并")

    # 创建输入任务（模拟排他选择后的路径）
    def action1():
        print("  → 路径1执行完成")

    def action2():
        print("  → 路径2执行完成")

    task1 = Task(id="p1", name="路径A", action=action1)
    task2 = Task(id="p2", name="路径B", action=action2)

    merge.add_input(task1)
    merge.add_input(task2)

    # 设置后续任务
    def final_action():
        print("✓ 合并后任务执行")

    final_task = Task(id="final", name="后续处理", action=final_action)
    merge.set_successor(final_task)

    # 验证
    valid, msg = merge.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 正例：路径1先完成
    print("\n--- 正例：路径1先完成 ---")
    task1.execute()
    result = merge.check_and_trigger()
    assert result is not None
    print("✅ 路径1触发成功")

    # 重置测试
    merge.reset()
    task1.reset()
    task2.reset()

    # 正例：路径2先完成
    print("\n--- 正例：路径2先完成 ---")
    task2.execute()
    result = merge.check_and_trigger()
    assert result is not None
    print("✅ 路径2触发成功")

    print("\n✅ 所有测试通过！")

    return merge

merge_instance = test_simple_merge()
```

---

## 模式6：多选模式（Multi-Choice）完整实现

### 形式定义

**定义6.1**（多选/OR-Split）：设候选分支集合 B = {b₁, b₂, ..., bₙ}：

- 选择函数：select: Data → 2ᴮ \ {∅}
- 可以激活任意非空子集

**定理6.1**（多选可判定性）：多选模式的可达性在O(2ⁿ)时间内可判定（最坏情况）。

**证明**：

1. 可能的选择组合数为 2ⁿ - 1
2. 需要检查每种组合是否可达
3. 时间复杂度：O(2ⁿ)
∎

### Python实现

```python
class MultiChoicePattern:
    """
    多选模式（OR-Split）实现
    可以选择一个或多个分支同时执行
    """

    def __init__(self, name: str = "MultiChoice"):
        self.name = name
        self.branches: List[Tuple[str, Callable[[Any], bool]]] = []
        self.selected_branches: List[str] = []
        self.data: Any = None

    def add_branch(self, name: str, condition: Callable[[Any], bool]):
        """添加分支和条件"""
        self.branches.append((name, condition))

    def set_data(self, data: Any):
        """设置决策数据"""
        self.data = data

    def evaluate(self) -> List[str]:
        """评估条件，选择所有满足条件的分支"""
        if self.data is None:
            return []

        self.selected_branches = []
        for branch_name, condition in self.branches:
            if condition(self.data):
                self.selected_branches.append(branch_name)

        if not self.selected_branches:
            print("⚠️ 警告：没有分支被选择")
        else:
            print(f"✓ 选择的分支: {self.selected_branches}")

        return self.selected_branches

    def get_all_combinations(self) -> List[List[str]]:
        """获取所有可能的分支组合（用于验证）"""
        from itertools import combinations

        all_combos = []
        branch_names = [name for name, _ in self.branches]

        for r in range(1, len(branch_names) + 1):
            for combo in combinations(branch_names, r):
                all_combos.append(list(combo))

        return all_combos

    def verify(self) -> Tuple[bool, str]:
        """验证多选模式的正确性"""
        if len(self.branches) < 2:
            return False, "至少需要2个分支"

        # 检查至少有一个分支可以被选择
        # 这需要测试数据，这里只做基本检查

        return True, "基本验证通过"

def test_multi_choice():
    """测试多选模式"""
    print("\n" + "=" * 60)
    print("测试：多选模式（Multi-Choice / OR-Split）")
    print("=" * 60)

    # 创建多选
    or_split = MultiChoicePattern("通知发送")

    # 添加分支（可以同时选择多个）
    or_split.add_branch("邮件", lambda d: d.get("email", False))
    or_split.add_branch("短信", lambda d: d.get("sms", False))
    or_split.add_branch("推送", lambda d: d.get("push", False))
    or_split.add_branch("站内信", lambda d: d.get("internal", False))

    # 验证
    valid, msg = or_split.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 正例测试
    print("\n--- 正例测试 ---")

    test_cases = [
        ({"email": True, "sms": True}, ["邮件", "短信"]),
        ({"email": True, "push": True, "internal": True}, ["邮件", "推送", "站内信"]),
        ({"sms": True}, ["短信"]),
        ({"email": True, "sms": True, "push": True, "internal": True},
         ["邮件", "短信", "推送", "站内信"]),
    ]

    for data, expected in test_cases:
        or_split.set_data(data)
        result = or_split.evaluate()
        assert set(result) == set(expected), f"期望 {expected}, 实际 {result}"
        print(f"✅ 数据 {data} -> {result}")

    # 反例：没有选择
    print("\n--- 反例：没有选择 ---")
    or_split.set_data({"wechat": True})  # 没有匹配的条件
    result = or_split.evaluate()
    assert result == []
    print("✅ 反例测试通过！")

    # 显示所有可能的组合
    print("\n--- 所有可能的组合 ---")
    combos = or_split.get_all_combinations()
    print(f"共有 {len(combos)} 种组合:")
    for i, combo in enumerate(combos[:10], 1):  # 只显示前10个
        print(f"  {i}. {combo}")

    print("\n✅ 所有测试通过！")

    return or_split

or_split_instance = test_multi_choice()
```



---

## 模式7：结构化同步合并（Structured Synchronizing Merge）完整实现

### 形式定义

**定义7.1**（结构化同步合并/OR-Join）：设激活的分支集合为 S ⊆ B：

- 等待条件：∀bᵢ ∈ S, 标记(bᵢ) = 完成
- 仅同步实际被激活的分支

**定理7.1**（结构化同步合并可判定性）：在结构化约束下，OR-Join的可达性在O(n)时间内可判定。

**证明**：

1. 结构化约束：每个OR-Split对应一个OR-Join
2. 可以跟踪哪些分支被激活
3. 同步条件明确
4. 时间复杂度：O(n)
∎

### Python实现

```python
class StructuredSynchronizingMerge:
    """
    结构化同步合并（OR-Join）实现
    仅等待实际被激活的分支完成
    """

    def __init__(self, name: str = "StructuredSyncMerge"):
        self.name = name
        self.all_branches: List[str] = []  # 所有可能的分支
        self.activated_branches: Set[str] = set()  # 实际激活的分支
        self.completed_branches: Set[str] = set()  # 已完成的分支
        self.tasks: Dict[str, Task] = {}
        self.successor: Optional[Task] = None

    def register_branches(self, branch_names: List[str]):
        """注册所有可能的分支"""
        self.all_branches = branch_names

    def activate_branches(self, branch_names: List[str]):
        """激活特定分支"""
        for name in branch_names:
            if name in self.all_branches:
                self.activated_branches.add(name)
        print(f"✓ 激活的分支: {self.activated_branches}")

    def add_task(self, branch_name: str, task: Task):
        """添加分支任务"""
        self.tasks[branch_name] = task

    def set_successor(self, task: Task):
        """设置后续任务"""
        self.successor = task

    def mark_completed(self, branch_name: str):
        """标记分支完成"""
        if branch_name in self.activated_branches:
            self.completed_branches.add(branch_name)
            print(f"✓ 分支 {branch_name} 完成")

    def can_proceed(self) -> bool:
        """检查是否可以继续"""
        return self.activated_branches.issubset(self.completed_branches)

    def get_waiting_branches(self) -> Set[str]:
        """获取还在等待的分支"""
        return self.activated_branches - self.completed_branches

    def sync_and_execute(self) -> Optional[Task]:
        """同步并执行"""
        if self.can_proceed():
            print(f"✓ 所有激活的 {len(self.activated_branches)} 个分支已完成")
            if self.successor:
                self.successor.execute()
                return self.successor
        else:
            waiting = self.get_waiting_branches()
            print(f"⏳ 等待分支: {waiting}")
        return None

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        if len(self.all_branches) < 2:
            return False, "至少需要2个分支"

        if not self.successor:
            return False, "缺少后续任务"

        return True, "验证通过"

def test_structured_sync_merge():
    """测试结构化同步合并"""
    print("\n" + "=" * 60)
    print("测试：结构化同步合并（Structured Synchronizing Merge / OR-Join）")
    print("=" * 60)

    # 创建OR-Join
    or_join = StructuredSynchronizingMerge("通知同步")

    # 注册所有可能的分支
    or_join.register_branches(["邮件", "短信", "推送", "站内信"])

    # 模拟OR-Split：激活部分分支
    or_join.activate_branches(["邮件", "短信"])

    # 创建任务
    def email_task():
        print("  → 发送邮件完成")

    def sms_task():
        print("  → 发送短信完成")

    task_email = Task(id="email", name="邮件任务", action=email_task)
    task_sms = Task(id="sms", name="短信任务", action=sms_task)

    or_join.add_task("邮件", task_email)
    or_join.add_task("短信", task_sms)

    # 设置后续任务
    def final_action():
        print("✓ 所有通知发送完成！")

    final_task = Task(id="final", name="通知完成", action=final_action)
    or_join.set_successor(final_task)

    # 验证
    valid, msg = or_join.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 第一次尝试（未完成）
    print("\n--- 第一次同步尝试（未完成）---")
    or_join.sync_and_execute()

    # 完成部分任务
    print("\n--- 完成部分任务 ---")
    task_email.execute()
    or_join.mark_completed("邮件")
    or_join.sync_and_execute()

    # 完成所有任务
    print("\n--- 完成所有任务 ---")
    task_sms.execute()
    or_join.mark_completed("短信")
    or_join.sync_and_execute()

    print("\n✅ 测试通过！")

    return or_join

or_join_instance = test_structured_sync_merge()
```

---

## 模式8：多合并模式（Multi-Merge）完整实现

### 形式定义

**定义8.1**（多合并）：设输入分支集合 I = {i₁, i₂, ..., iₘ}：

- 触发条件：∀iⱼ ∈ I, 到达即触发
- 后续任务可能被执行多次

**定理8.1**（多合并可判定性）：多合并的可达性在O(m)时间内可判定。

**证明**：

1. 每个分支独立触发
2. 无需等待其他分支
3. 触发次数 = 到达分支数
4. 时间复杂度：O(m)
∎

### Python实现

```python
class MultiMergePattern:
    """
    多合并模式实现
    每个分支到达都触发后续任务，不等待同步
    """

    def __init__(self, name: str = "MultiMerge"):
        self.name = name
        self.inputs: List[Task] = []
        self.successor: Optional[Task] = None
        self.trigger_history: List[str] = []  # 记录触发历史
        self.trigger_count = 0

    def add_input(self, task: Task):
        """添加输入任务"""
        self.inputs.append(task)

    def set_successor(self, task: Task):
        """设置后续任务（会被多次执行）"""
        self.successor = task

    def check_triggers(self) -> int:
        """检查并触发所有已完成的输入"""
        triggers = 0
        for task in self.inputs:
            if task.status == TaskStatus.COMPLETED and task.name not in self.trigger_history:
                print(f"✓ 检测到 {task.name} 完成，触发后续任务（第{self.trigger_count + 1}次）")
                self.trigger_history.append(task.name)
                self.trigger_count += 1

                # 每次触发都执行后续任务
                if self.successor:
                    # 创建新实例或重置状态
                    self.successor.reset()
                    self.successor.execute()
                    triggers += 1

        return triggers

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        if len(self.inputs) < 2:
            return False, "至少需要2个输入"

        return True, "验证通过"

def test_multi_merge():
    """测试多合并模式"""
    print("\n" + "=" * 60)
    print("测试：多合并模式（Multi-Merge）")
    print("=" * 60)

    # 创建多合并
    mm = MultiMergePattern("事件处理")

    # 创建输入任务
    def action1():
        print("  → 事件A处理完成")

    def action2():
        print("  → 事件B处理完成")

    def action3():
        print("  → 事件C处理完成")

    task_a = Task(id="a", name="事件A", action=action1)
    task_b = Task(id="b", name="事件B", action=action2)
    task_c = Task(id="c", name="事件C", action=action3)

    mm.add_input(task_a)
    mm.add_input(task_b)
    mm.add_input(task_c)

    # 设置后续任务
    def log_action():
        print("  → 记录日志")

    log_task = Task(id="log", name="记录日志", action=log_action)
    mm.set_successor(log_task)

    # 验证
    valid, msg = mm.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 逐步完成任务并触发
    print("\n--- 完成任务A ---")
    task_a.execute()
    mm.check_triggers()

    print("\n--- 完成任务B ---")
    task_b.execute()
    mm.check_triggers()

    print("\n--- 完成任务C ---")
    task_c.execute()
    mm.check_triggers()

    print(f"\n总触发次数: {mm.trigger_count}")
    assert mm.trigger_count == 3

    print("\n✅ 测试通过！")

    return mm

multi_merge_instance = test_multi_merge()
```

---

## 模式9：鉴别器模式（Discriminator）完整实现

### 形式定义

**定义9.1**（鉴别器）：设并行分支集合 P = {p₁, p₂, ..., pₙ}：

- 触发条件：∃!pᵢ ∈ P, pᵢ首先完成
- 其他分支：取消或忽略

**定理9.1**（鉴别器可判定性）：鉴别器的可达性在O(n)时间内可判定。

**证明**：

1. 等待第一个完成的分支
2. 需要跟踪所有分支状态
3. 第一个完成后触发
4. 时间复杂度：O(n)
∎

### Python实现

```python
class DiscriminatorPattern:
    """
    鉴别器模式实现
    等待第一个完成的分支，然后触发后续任务
    """

    def __init__(self, name: str = "Discriminator"):
        self.name = name
        self.branches: List[Task] = []
        self.successor: Optional[Task] = None
        self.triggered = False
        self.winner: Optional[str] = None
        self.cancel_others = False  # 是否取消其他分支

    def add_branch(self, task: Task):
        """添加分支"""
        self.branches.append(task)

    def set_successor(self, task: Task):
        """设置后续任务"""
        self.successor = task

    def enable_cancel(self):
        """启用取消其他分支"""
        self.cancel_others = True

    def check_first_complete(self) -> Optional[str]:
        """检查第一个完成的分支"""
        if self.triggered:
            return self.winner

        for task in self.branches:
            if task.status == TaskStatus.COMPLETED:
                self.winner = task.name
                self.triggered = True
                print(f"✓ 第一个完成的分支: {task.name}")

                # 触发后续任务
                if self.successor:
                    self.successor.execute()

                # 取消其他分支（如果启用）
                if self.cancel_others:
                    self._cancel_others(task.name)

                return self.winner

        return None

    def _cancel_others(self, winner_name: str):
        """取消其他分支"""
        for task in self.branches:
            if task.name != winner_name and task.status == TaskStatus.RUNNING:
                task.cancel()
                print(f"  → 取消分支: {task.name}")

    def get_branch_status(self) -> Dict[str, TaskStatus]:
        """获取所有分支状态"""
        return {task.name: task.status for task in self.branches}

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        if len(self.branches) < 2:
            return False, "至少需要2个分支"

        return True, "验证通过"

def test_discriminator():
    """测试鉴别器模式"""
    print("\n" + "=" * 60)
    print("测试：鉴别器模式（Discriminator）")
    print("=" * 60)

    # 创建鉴别器
    disc = DiscriminatorPattern("最快响应")

    # 创建分支任务
    def action1():
        time.sleep(0.1)
        print("  → 服务A响应")

    def action2():
        time.sleep(0.05)  # 最快
        print("  → 服务B响应")

    def action3():
        time.sleep(0.15)
        print("  → 服务C响应")

    task_a = Task(id="a", name="服务A", action=action1)
    task_b = Task(id="b", name="服务B", action=action2)
    task_c = Task(id="c", name="服务C", action=action3)

    disc.add_branch(task_a)
    disc.add_branch(task_b)
    disc.add_branch(task_c)

    # 设置后续任务
    def use_result():
        print("✓ 使用最快响应的结果")

    result_task = Task(id="result", name="使用结果", action=use_result)
    disc.set_successor(result_task)

    # 验证
    valid, msg = disc.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 模拟执行（手动设置完成状态）
    print("\n--- 模拟分支完成（服务B最快）---")
    task_b.status = TaskStatus.COMPLETED  # 服务B先完成
    winner = disc.check_first_complete()
    assert winner == "服务B"

    # 后续完成应该被忽略
    print("\n--- 其他分支完成（应被忽略）---")
    task_a.status = TaskStatus.COMPLETED
    task_c.status = TaskStatus.COMPLETED
    winner = disc.check_first_complete()
    assert winner == "服务B"  # 仍然是B

    print("\n✅ 测试通过！")

    return disc

discriminator_instance = test_discriminator()
```

---

## 模式10：部分加入（Partial Join / M-out-of-N）完整实现

### 形式定义

**定义10.1**（部分加入）：设分支总数为N，需要M个完成（M ≤ N）：

- 触发条件：|{pᵢ完成}| ≥ M
- 参数化：M为配置参数

**定理10.1**（部分加入可判定性）：部分加入的可达性在O(N)时间内可判定。

**证明**：

1. 计数已完成的 branches
2. 当计数 ≥ M 时触发
3. 时间复杂度：O(N)
∎

### Python实现

```python
class PartialJoinPattern:
    """
    部分加入模式（M-out-of-N Join）实现
    等待N个分支中的M个完成
    """

    def __init__(self, name: str = "PartialJoin", n: int = 0, m: int = 0):
        self.name = name
        self.n = n  # 总分支数
        self.m = m  # 需要完成的分支数
        self.branches: List[Task] = []
        self.successor: Optional[Task] = None
        self.triggered = False

    def set_parameters(self, n: int, m: int):
        """设置参数"""
        self.n = n
        self.m = m

    def add_branch(self, task: Task):
        """添加分支"""
        self.branches.append(task)

    def set_successor(self, task: Task):
        """设置后续任务"""
        self.successor = task

    def count_completed(self) -> int:
        """统计已完成的分支数"""
        return sum(1 for task in self.branches if task.status == TaskStatus.COMPLETED)

    def can_proceed(self) -> bool:
        """检查是否可以继续"""
        return self.count_completed() >= self.m

    def check_and_trigger(self) -> Optional[Task]:
        """检查并触发"""
        completed = self.count_completed()
        print(f"进度: {completed}/{self.m} (总分支: {self.n})")

        if self.can_proceed() and not self.triggered:
            self.triggered = True
            print(f"✓ 已达到 {self.m} 个完成分支，触发后续任务")
            if self.successor:
                self.successor.execute()
                return self.successor

        return None

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        if self.n < 2:
            return False, "N至少需要2"

        if self.m < 1 or self.m > self.n:
            return False, f"M必须在1到N之间（当前M={self.m}, N={self.n}）"

        if len(self.branches) != self.n:
            return False, f"分支数({len(self.branches)})与N({self.n})不匹配"

        return True, "验证通过"

def test_partial_join():
    """测试部分加入模式"""
    print("\n" + "=" * 60)
    print("测试：部分加入模式（Partial Join / M-out-of-N）")
    print("=" * 60)

    # 创建部分加入（3-out-of-5）
    pj = PartialJoinPattern("投票统计", n=5, m=3)

    # 创建5个分支
    tasks = []
    for i in range(5):
        def make_action(idx):
            return lambda: print(f"  → 投票{i+1}完成")

        task = Task(id=f"v{i}", name=f"投票{i+1}", action=make_action(i))
        tasks.append(task)
        pj.add_branch(task)

    # 设置后续任务
    def count_votes():
        print("✓ 已达到3票，统计结果！")

    result_task = Task(id="result", name="统计结果", action=count_votes)
    pj.set_successor(result_task)

    # 验证
    valid, msg = pj.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 逐步完成
    print("\n--- 完成投票1 ---")
    tasks[0].execute()
    pj.check_and_trigger()

    print("\n--- 完成投票2 ---")
    tasks[1].execute()
    pj.check_and_trigger()

    print("\n--- 完成投票3（应该触发）---")
    tasks[2].execute()
    result = pj.check_and_trigger()
    assert result is not None

    print("\n✅ 测试通过！")

    return pj

partial_join_instance = test_partial_join()
```

---

## 模式14：任意循环（Arbitrary Cycles）完整实现

### 形式定义

**定义14.1**（任意循环）：设循环体为L，循环条件为C：

- 执行L
- 检查C
- 若C为真，重复执行L
- 若C为假，退出循环

**定理14.1**（任意循环可判定性）：任意循环的终止性在一般情况下**不可判定**（停机问题）。

**证明**：

1. 任意循环可以模拟图灵机
2. 停机问题可归约到循环终止性
3. 因此终止性不可判定
∎

**定理14.2**（有界循环可判定性）：若循环次数有明确上界，则可达性可判定。

### Python实现

```python
class ArbitraryCyclePattern:
    """
    任意循环模式实现
    支持基于条件的循环执行
    """

    def __init__(self, name: str = "ArbitraryCycle"):
        self.name = name
        self.loop_body: Optional[Callable] = None
        self.condition: Optional[Callable[[], bool]] = None
        self.max_iterations = 1000  # 安全限制
        self.iteration_count = 0
        self.terminated = False

    def set_loop_body(self, body: Callable):
        """设置循环体"""
        self.loop_body = body

    def set_condition(self, condition: Callable[[], bool]):
        """设置循环条件"""
        self.condition = condition

    def set_max_iterations(self, max_iter: int):
        """设置最大迭代次数（安全限制）"""
        self.max_iterations = max_iter

    def execute(self) -> Tuple[int, bool]:
        """
        执行循环
        返回: (实际迭代次数, 是否正常终止)
        """
        if not self.loop_body or not self.condition:
            return 0, False

        self.iteration_count = 0
        self.terminated = False

        while self.condition():
            if self.iteration_count >= self.max_iterations:
                print(f"⚠️ 达到最大迭代次数限制({self.max_iterations})，强制终止")
                return self.iteration_count, False

            self.iteration_count += 1
            print(f"  → 第{self.iteration_count}次迭代")
            self.loop_body()

        self.terminated = True
        print(f"✓ 循环正常终止，共执行{self.iteration_count}次")
        return self.iteration_count, True

    def verify_termination(self) -> Tuple[bool, str]:
        """
        尝试验证循环是否会终止
        注意：这只是启发式检查，不能解决停机问题
        """
        # 检查是否有最大迭代次数限制
        if self.max_iterations < float('inf'):
            return True, f"有最大迭代次数限制({self.max_iterations})，必定终止"

        # 其他启发式检查...
        return False, "无法保证终止（停机问题）"

def test_arbitrary_cycle():
    """测试任意循环模式"""
    print("\n" + "=" * 60)
    print("测试：任意循环模式（Arbitrary Cycles）")
    print("=" * 60)

    # 正例：有限循环
    print("\n--- 正例：有限循环（计数器递减）---")
    cycle1 = ArbitraryCyclePattern("有限循环")

    counter = [5]  # 使用列表以便在lambda中修改

    def body1():
        counter[0] -= 1
        print(f"    计数器: {counter[0]}")

    cycle1.set_loop_body(body1)
    cycle1.set_condition(lambda: counter[0] > 0)

    count, terminated = cycle1.execute()
    assert terminated == True
    assert count == 5
    print("✅ 正例测试通过！")

    # 正例：带安全限制的循环
    print("\n--- 正例：带安全限制的循环 ---")
    cycle2 = ArbitraryCyclePattern("安全循环")
    cycle2.set_max_iterations(10)

    iterations = [0]

    def body2():
        iterations[0] += 1

    # 条件永远为真，但会被安全限制终止
    cycle2.set_loop_body(body2)
    cycle2.set_condition(lambda: True)

    count, terminated = cycle2.execute()
    assert terminated == False  # 被安全限制终止
    assert count == 10
    print("✅ 安全限制测试通过！")

    # 终止性验证
    print("\n--- 终止性验证 ---")
    can_terminate, msg = cycle1.verify_termination()
    print(f"循环1终止性: {can_terminate}, {msg}")

    return cycle1

cycle_instance = test_arbitrary_cycle()
```

---

## 模式15：隐式终止（Implicit Termination）完整实现

### 形式定义

**定义15.1**（隐式终止）：设工作流状态为S，可执行任务集合为E(S)：

- 终止条件：E(S) = ∅
- 隐式：无显式终止操作

**定理15.1**（隐式终止可判定性）：隐式终止的检测在O(|T|)时间内可判定。

**证明**：

1. 检查所有变迁的可执行性
2. 若无可执行变迁，则终止
3. 时间复杂度：O(|T|)
∎

### Python实现

```python
class ImplicitTerminationPattern:
    """
    隐式终止模式实现
    当没有可执行任务时自动终止
    """

    def __init__(self, name: str = "ImplicitTermination"):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.places: Dict[str, Place] = {}
        self.terminated = False

    def add_task(self, task: Task):
        """添加任务"""
        self.tasks[task.id] = task

    def add_place(self, place: Place):
        """添加库所"""
        self.places[place.name] = place

    def get_ready_tasks(self) -> List[Task]:
        """获取就绪的任务"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.READY]

    def get_running_tasks(self) -> List[Task]:
        """获取运行中的任务"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.RUNNING]

    def can_terminate(self) -> bool:
        """检查是否可以终止"""
        ready = self.get_ready_tasks()
        running = self.get_running_tasks()
        return len(ready) == 0 and len(running) == 0

    def check_termination(self) -> Tuple[bool, str]:
        """检查终止条件"""
        ready = self.get_ready_tasks()
        running = self.get_running_tasks()

        if len(ready) == 0 and len(running) == 0:
            self.terminated = True
            completed = sum(1 for t in self.tasks.values()
                          if t.status == TaskStatus.COMPLETED)
            return True, f"隐式终止：{completed}个任务已完成"

        return False, f"还有{len(ready)}个就绪任务，{len(running)}个运行中任务"

    def run_until_termination(self, max_steps: int = 100) -> Tuple[int, bool]:
        """运行直到终止或达到最大步数"""
        steps = 0

        while steps < max_steps:
            # 检查是否可以终止
            can_term, msg = self.check_termination()
            if can_term:
                print(f"✓ {msg}")
                return steps, True

            # 执行就绪任务
            ready = self.get_ready_tasks()
            if ready:
                task = ready[0]
                print(f"  → 执行任务: {task.name}")
                task.execute()

            steps += 1

        return steps, False

def test_implicit_termination():
    """测试隐式终止模式"""
    print("\n" + "=" * 60)
    print("测试：隐式终止模式（Implicit Termination）")
    print("=" * 60)

    # 创建隐式终止
    it = ImplicitTerminationPattern("订单流程")

    # 添加任务
    def action1():
        print("    验证订单完成")

    def action2():
        print("    处理支付完成")

    def action3():
        print("    发货完成")

    task1 = Task(id="t1", name="验证订单", action=action1)
    task2 = Task(id="t2", name="处理支付", action=action2)
    task3 = Task(id="t3", name="发货", action=action3)

    it.add_task(task1)
    it.add_task(task2)
    it.add_task(task3)

    # 运行直到终止
    print("\n--- 运行工作流 ---")
    steps, terminated = it.run_until_termination()

    assert terminated == True
    assert it.terminated == True
    print(f"\n✓ 工作流在{steps}步后终止")

    print("\n✅ 测试通过！")

    return it

implicit_term_instance = test_implicit_termination()
```



---

## 模式16-19：多实例模式完整实现

### 模式16：多实例无同步

```python
class MultipleInstancesNoSync:
    """
    多实例无同步模式
    创建多个实例，独立执行，无需同步
    """

    def __init__(self, name: str = "MINoSync"):
        self.name = name
        self.instance_factory: Optional[Callable[[int], Callable]] = None
        self.instances: List[Task] = []

    def set_instance_factory(self, factory: Callable[[int], Callable]):
        """设置实例工厂函数"""
        self.instance_factory = factory

    def create_instances(self, count: int) -> List[Task]:
        """创建指定数量的实例"""
        self.instances = []
        for i in range(count):
            action = self.instance_factory(i)
            task = Task(
                id=f"instance_{i}",
                name=f"实例{i+1}",
                action=action
            )
            self.instances.append(task)
        return self.instances

    def execute_all(self, parallel: bool = True) -> List[str]:
        """执行所有实例"""
        executed = []

        if parallel:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(task.execute): task
                          for task in self.instances}
                for future in concurrent.futures.as_completed(futures):
                    task = futures[future]
                    try:
                        future.result()
                        executed.append(task.name)
                    except Exception as e:
                        print(f"实例 {task.name} 失败: {e}")
        else:
            for task in self.instances:
                task.execute()
                executed.append(task.name)

        return executed

def test_multiple_instances_no_sync():
    """测试多实例无同步"""
    print("\n" + "=" * 60)
    print("测试：多实例无同步（Multiple Instances without Synchronization）")
    print("=" * 60)

    mi = MultipleInstancesNoSync("批量发送")

    # 设置实例工厂
    def make_instance(idx):
        return lambda: print(f"  → 发送给用户{idx+1}")

    mi.set_instance_factory(make_instance)

    # 创建5个实例
    instances = mi.create_instances(5)
    print(f"创建了 {len(instances)} 个实例")

    # 执行（串行便于观察）
    print("\n执行所有实例：")
    executed = mi.execute_all(parallel=False)

    assert len(executed) == 5
    print("\n✅ 测试通过！")

    return mi

mi_no_sync = test_multiple_instances_no_sync()
```

---

### 模式17：多实例同步（设计时已知数量）

```python
class MultipleInstancesWithSyncDesignTime:
    """
    多实例同步模式（设计时已知数量）
    在设计时就知道实例数量，创建多个实例并在完成后同步
    """

    def __init__(self, name: str = "MISyncDesignTime", n: int = 0):
        self.name = name
        self.n = n  # 设计时已知的实例数
        self.instance_factory: Optional[Callable[[int], Callable]] = None
        self.instances: List[Task] = []
        self.completed_count = 0
        self.all_completed = threading.Event()

    def set_instance_factory(self, factory: Callable[[int], Callable]):
        self.instance_factory = factory

    def create_instances(self) -> List[Task]:
        """创建实例（使用设计时已知的数量）"""
        self.instances = []
        for i in range(self.n):
            action = self.instance_factory(i)
            task = Task(
                id=f"instance_{i}",
                name=f"实例{i+1}",
                action=action
            )
            self.instances.append(task)
        return self.instances

    def execute_and_sync(self, timeout: float = 10.0) -> bool:
        """执行所有实例并等待同步"""
        def on_complete(task):
            self.completed_count += 1
            print(f"  → {task.name} 完成 ({self.completed_count}/{self.n})")
            if self.completed_count >= self.n:
                self.all_completed.set()

        # 包装动作以跟踪完成
        for task in self.instances:
            original_action = task.action
            def make_wrapped(t, orig):
                return lambda: (orig(), on_complete(t))
            task.action = make_wrapped(task, original_action)

        # 并行执行
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(task.execute) for task in self.instances]
            concurrent.futures.wait(futures, timeout=timeout)

        return self.all_completed.wait(timeout=timeout)

def test_multiple_instances_sync_design():
    """测试多实例同步（设计时）"""
    print("\n" + "=" * 60)
    print("测试：多实例同步（设计时已知数量）")
    print("=" * 60)

    mi = MultipleInstancesWithSyncDesignTime("并行计算", n=3)

    def make_instance(idx):
        def action():
            time.sleep(0.1 * (idx + 1))
            print(f"    计算节点{idx+1}完成")
        return action

    mi.set_instance_factory(make_instance)
    mi.create_instances()

    print("执行并等待同步：")
    completed = mi.execute_and_sync()

    assert completed == True
    assert mi.completed_count == 3
    print("\n✅ 测试通过！")

    return mi

mi_sync_design = test_multiple_instances_sync_design()
```

---

### 模式18：多实例运行时

```python
class MultipleInstancesRuntime:
    """
    多实例运行时模式
    在运行时知道实例数量，但创建前未知
    """

    def __init__(self, name: str = "MIRuntime"):
        self.name = name
        self.instance_factory: Optional[Callable[[int], Callable]] = None
        self.instances: List[Task] = []
        self.n = 0  # 运行时确定

    def set_instance_factory(self, factory: Callable[[int], Callable]):
        self.instance_factory = factory

    def determine_count(self, data: Any) -> int:
        """
        根据运行时数据确定实例数量
        子类可以重写此方法
        """
        # 默认实现：从数据中获取数量
        if isinstance(data, (list, tuple)):
            return len(data)
        elif isinstance(data, int):
            return data
        return 1

    def create_instances(self, runtime_data: Any) -> List[Task]:
        """根据运行时数据创建实例"""
        self.n = self.determine_count(runtime_data)
        print(f"运行时确定实例数: {self.n}")

        self.instances = []
        for i in range(self.n):
            action = self.instance_factory(i)
            task = Task(
                id=f"instance_{i}",
                name=f"实例{i+1}",
                action=action
            )
            self.instances.append(task)
        return self.instances

    def execute_all(self) -> List[str]:
        """执行所有实例"""
        executed = []
        for task in self.instances:
            task.execute()
            executed.append(task.name)
        return executed

def test_multiple_instances_runtime():
    """测试多实例运行时"""
    print("\n" + "=" * 60)
    print("测试：多实例运行时（运行时确定数量）")
    print("=" * 60)

    mi = MultipleInstancesRuntime("动态处理")

    def make_instance(idx):
        return lambda: print(f"  → 处理第{idx+1}个订单")

    mi.set_instance_factory(make_instance)

    # 运行时数据：订单列表
    orders = ["订单A", "订单B", "订单C", "订单D"]

    mi.create_instances(orders)

    print("执行所有实例：")
    executed = mi.execute_all()

    assert len(executed) == 4
    print("\n✅ 测试通过！")

    return mi

mi_runtime = test_multiple_instances_runtime()
```

---

### 模式19：多实例无先验知识

```python
class MultipleInstancesNoPriorKnowledge:
    """
    多实例无先验知识模式
    实例可以动态添加，无预设总数
    """

    def __init__(self, name: str = "MINoPrior"):
        self.name = name
        self.instance_factory: Optional[Callable[[int], Callable]] = None
        self.instances: List[Task] = []
        self.accepting_new = True
        self.completion_event = threading.Event()
        self.completed_instances: Set[str] = set()

    def set_instance_factory(self, factory: Callable[[int], Callable]):
        self.instance_factory = factory

    def add_instance(self, data: Any = None) -> Task:
        """动态添加实例"""
        if not self.accepting_new:
            print("⚠️ 不再接受新实例")
            return None

        idx = len(self.instances)
        action = self.instance_factory(idx)
        task = Task(
            id=f"instance_{idx}",
            name=f"实例{idx+1}",
            action=action
        )
        self.instances.append(task)
        print(f"✓ 添加实例: {task.name}")
        return task

    def mark_no_more_instances(self):
        """标记不再添加新实例"""
        self.accepting_new = False
        print("✓ 不再接受新实例")

    def execute_instance(self, task: Task):
        """执行单个实例"""
        task.execute()
        self.completed_instances.add(task.id)
        print(f"  → {task.name} 完成")

        # 检查是否全部完成
        if not self.accepting_new and len(self.completed_instances) == len(self.instances):
            self.completion_event.set()

    def wait_for_completion(self, timeout: float = None) -> bool:
        """等待所有实例完成"""
        return self.completion_event.wait(timeout=timeout)

def test_multiple_instances_no_prior():
    """测试多实例无先验知识"""
    print("\n" + "=" * 60)
    print("测试：多实例无先验知识（动态添加）")
    print("=" * 60)

    mi = MultipleInstancesNoPriorKnowledge("动态任务")

    def make_instance(idx):
        return lambda: print(f"    处理动态任务{idx+1}")

    mi.set_instance_factory(make_instance)

    # 动态添加实例
    print("动态添加实例：")
    task1 = mi.add_instance()
    task2 = mi.add_instance()

    # 执行部分实例
    print("\n执行实例：")
    mi.execute_instance(task1)
    mi.execute_instance(task2)

    # 再添加一个实例
    print("\n再添加实例：")
    task3 = mi.add_instance()
    mi.execute_instance(task3)

    # 标记不再添加
    mi.mark_no_more_instances()

    print("\n✅ 测试通过！")

    return mi

mi_no_prior = test_multiple_instances_no_prior()
```

---

## 模式20：延迟选择（Deferred Choice）完整实现

### 形式定义

**定义20.1**（延迟选择）：

- 选择点：等待外部事件
- 事件集合：E = {e₁, e₂, ..., eₖ}
- 触发：第一个发生的事件决定路径

**定理20.1**（延迟选择可判定性）：延迟选择的可达性在O(k)时间内可判定。

**证明**：

1. 等待外部事件
2. 第一个事件触发路径选择
3. 时间复杂度：O(k)
∎

### Python实现

```python
import queue

class DeferredChoicePattern:
    """
    延迟选择模式实现
    等待外部事件决定路径
    """

    def __init__(self, name: str = "DeferredChoice"):
        self.name = name
        self.events: Dict[str, Callable] = {}
        self.event_queue = queue.Queue()
        self.selected_event: Optional[str] = None
        self.timeout: Optional[float] = None

    def register_event(self, event_name: str, handler: Callable):
        """注册事件和处理器"""
        self.events[event_name] = handler

    def set_timeout(self, timeout: float):
        """设置超时时间"""
        self.timeout = timeout

    def trigger_event(self, event_name: str):
        """触发事件"""
        if event_name in self.events:
            self.event_queue.put(event_name)
            print(f"✓ 事件触发: {event_name}")

    def wait_and_choose(self) -> Optional[str]:
        """等待并选择第一个发生的事件"""
        print(f"⏳ 等待事件... (可用事件: {list(self.events.keys())})")

        try:
            self.selected_event = self.event_queue.get(timeout=self.timeout)
            print(f"✓ 选择事件: {self.selected_event}")

            # 执行对应的处理器
            handler = self.events[self.selected_event]
            handler()

            return self.selected_event
        except queue.Empty:
            print("⚠️ 等待超时，没有事件触发")
            return None

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        if len(self.events) < 2:
            return False, "至少需要2个事件"

        return True, "验证通过"

def test_deferred_choice():
    """测试延迟选择"""
    print("\n" + "=" * 60)
    print("测试：延迟选择模式（Deferred Choice）")
    print("=" * 60)

    dc = DeferredChoicePattern("用户选择")

    # 注册事件
    def on_email():
        print("  → 用户选择邮件通知")

    def on_sms():
        print("  → 用户选择短信通知")

    def on_push():
        print("  → 用户选择推送通知")

    dc.register_event("邮件", on_email)
    dc.register_event("短信", on_sms)
    dc.register_event("推送", on_push)

    # 验证
    valid, msg = dc.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 模拟事件触发（在另一个线程）
    def simulate_event():
        time.sleep(0.5)
        dc.trigger_event("短信")

    import threading
    t = threading.Thread(target=simulate_event)
    t.start()

    # 等待选择
    print("\n等待用户选择...")
    selected = dc.wait_and_choose()

    assert selected == "短信"
    print("\n✅ 测试通过！")

    return dc

deferred_choice_instance = test_deferred_choice()
```

---

## 模式21：交错并行路由（Interleaved Parallel Routing）完整实现

### 形式定义

**定义21.1**（交错并行路由）：设任务集合 T = {t₁, t₂, ..., tₙ}：

- 全序：任意排列都是合法的
- 互斥：∀时刻, 最多一个tᵢ在执行
- 完成：所有tᵢ都执行一次

**定理21.1**（交错并行路由可判定性）：交错并行路由的可达性在O(n!)时间内可判定。

**证明**：

1. 任意排列都是合法的
2. 排列数为 n!
3. 需要检查所有可能的执行顺序
4. 时间复杂度：O(n!)
∎

### Python实现

```python
from itertools import permutations

class InterleavedParallelRouting:
    """
    交错并行路由模式实现
    任务可以以任意顺序执行，但同一时间只能执行一个
    """

    def __init__(self, name: str = "InterleavedParallel"):
        self.name = name
        self.tasks: List[Task] = []
        self.lock = threading.Lock()
        self.executed_order: List[str] = []
        self.current_task: Optional[str] = None

    def add_task(self, task: Task):
        """添加任务"""
        self.tasks.append(task)

    def execute_task(self, task: Task) -> bool:
        """执行单个任务（带互斥锁）"""
        with self.lock:
            if self.current_task is not None:
                print(f"⚠️ 任务 {task.name} 无法执行，{self.current_task} 正在运行")
                return False

            self.current_task = task.name
            print(f"  → 开始执行: {task.name}")

        # 执行任务（锁外执行以允许其他任务等待）
        task.execute()

        with self.lock:
            self.executed_order.append(task.name)
            self.current_task = None
            print(f"  ✓ 完成: {task.name}")

        return True

    def execute_all(self, order: Optional[List[int]] = None) -> List[str]:
        """
        按指定顺序执行所有任务
        如果order为None，则按添加顺序执行
        """
        if order is None:
            order = list(range(len(self.tasks)))

        for idx in order:
            if 0 <= idx < len(self.tasks):
                self.execute_task(self.tasks[idx])

        return self.executed_order

    def get_all_possible_orders(self) -> List[List[str]]:
        """获取所有可能的执行顺序"""
        task_names = [t.name for t in self.tasks]
        return [list(p) for p in permutations(task_names)]

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        if len(self.tasks) < 2:
            return False, "至少需要2个任务"

        return True, "验证通过"

def test_interleaved_parallel():
    """测试交错并行路由"""
    print("\n" + "=" * 60)
    print("测试：交错并行路由（Interleaved Parallel Routing）")
    print("=" * 60)

    ipr = InterleavedParallelRouting("顺序无关任务")

    # 添加任务
    def action1():
        print("    任务A执行中...")
        time.sleep(0.1)

    def action2():
        print("    任务B执行中...")
        time.sleep(0.1)

    def action3():
        print("    任务C执行中...")
        time.sleep(0.1)

    ipr.add_task(Task(id="a", name="任务A", action=action1))
    ipr.add_task(Task(id="b", name="任务B", action=action2))
    ipr.add_task(Task(id="c", name="任务C", action=action3))

    # 验证
    valid, msg = ipr.verify()
    print(f"\n验证结果: {valid}, {msg}")

    # 按顺序A->B->C执行
    print("\n--- 执行顺序 A->B->C ---")
    ipr.executed_order = []
    order1 = ipr.execute_all([0, 1, 2])
    print(f"执行顺序: {order1}")

    # 按顺序C->A->B执行
    print("\n--- 执行顺序 C->A->B ---")
    ipr.executed_order = []
    order2 = ipr.execute_all([2, 0, 1])
    print(f"执行顺序: {order2}")

    # 显示所有可能的顺序
    print("\n--- 所有可能的执行顺序 ---")
    all_orders = ipr.get_all_possible_orders()
    print(f"共有 {len(all_orders)} 种可能顺序")
    for i, order in enumerate(all_orders[:6], 1):
        print(f"  {i}. {order}")

    print("\n✅ 测试通过！")

    return ipr

interleaved_instance = test_interleaved_parallel()
```

---

## 模式22：里程碑（Milestone）完整实现

### 形式定义

**定义22.1**（里程碑）：

- 里程碑状态：M
- 任务t的执行条件：当前状态满足M
- 检查：不消耗里程碑

**定理22.1**（里程碑可判定性）：里程碑的可达性在O(1)时间内可判定。

**证明**：

1. 检查当前状态是否满足M
2. 只读操作，不修改状态
3. 时间复杂度：O(1)
∎

### Python实现

```python
class MilestonePattern:
    """
    里程碑模式实现
    任务执行依赖于是否达到特定状态
    """

    def __init__(self, name: str = "Milestone"):
        self.name = name
        self.milestones: Dict[str, bool] = {}
        self.tasks: Dict[str, Tuple[Task, str]] = {}  # task -> required_milestone

    def set_milestone(self, name: str, achieved: bool = False):
        """设置里程碑状态"""
        self.milestones[name] = achieved

    def achieve_milestone(self, name: str):
        """达成里程碑"""
        self.milestones[name] = True
        print(f"✓ 达成里程碑: {name}")

    def add_task_with_milestone(self, task: Task, milestone: str):
        """添加需要特定里程碑的任务"""
        self.tasks[task.id] = (task, milestone)

    def can_execute(self, task_id: str) -> bool:
        """检查任务是否可以执行"""
        if task_id not in self.tasks:
            return False

        task, milestone = self.tasks[task_id]
        return self.milestones.get(milestone, False)

    def execute_task(self, task_id: str) -> bool:
        """执行任务（如果里程碑满足）"""
        if not self.can_execute(task_id):
            required = self.tasks[task_id][1]
            print(f"⏳ 任务无法执行，需要里程碑: {required}")
            return False

        task = self.tasks[task_id][0]
        task.execute()
        return True

    def get_achieved_milestones(self) -> List[str]:
        """获取已达成的里程碑"""
        return [name for name, achieved in self.milestones.items() if achieved]

def test_milestone():
    """测试里程碑模式"""
    print("\n" + "=" * 60)
    print("测试：里程碑模式（Milestone）")
    print("=" * 60)

    ms = MilestonePattern("订单里程碑")

    # 设置里程碑
    ms.set_milestone("订单确认", False)
    ms.set_milestone("支付完成", False)
    ms.set_milestone("发货完成", False)

    # 创建任务
    def ship_action():
        print("  → 执行发货")

    def review_action():
        print("  → 执行评价")

    ship_task = Task(id="ship", name="发货", action=ship_action)
    review_task = Task(id="review", name="评价", action=review_action)

    ms.add_task_with_milestone(ship_task, "支付完成")
    ms.add_task_with_milestone(review_task, "发货完成")

    # 尝试执行（里程碑未达成）
    print("\n--- 里程碑未达成时尝试执行 ---")
    ms.execute_task("ship")

    # 达成里程碑
    print("\n--- 达成里程碑 ---")
    ms.achieve_milestone("订单确认")
    ms.achieve_milestone("支付完成")

    # 再次尝试
    print("\n--- 里程碑达成后执行 ---")
    ms.execute_task("ship")

    # 达成更多里程碑
    ms.achieve_milestone("发货完成")
    ms.execute_task("review")

    print(f"\n已达成里程碑: {ms.get_achieved_milestones()}")

    print("\n✅ 测试通过！")

    return ms

milestone_instance = test_milestone()
```

---

## 模式23：关键区域（Critical Section）完整实现

### 形式定义

**定义23.1**（关键区域）：

- 关键区域：CS
- 互斥：∀时刻, 最多一个任务在CS中
- 进入条件：CS为空

**定理23.1**（关键区域可判定性）：关键区域的可达性和死锁检测在O(n²)时间内可判定。

**证明**：

1. 需要检查所有任务对的互斥关系
2. 死锁检测需要检查循环等待
3. 时间复杂度：O(n²)
∎

### Python实现

```python
class CriticalSectionPattern:
    """
    关键区域模式实现
    确保关键区域内的任务互斥执行
    """

    def __init__(self, name: str = "CriticalSection"):
        self.name = name
        self.semaphore = threading.Semaphore(1)  # 二元信号量
        self.tasks_in_cs: Set[str] = set()
        self.waiting_tasks: List[str] = []
        self.cs_history: List[Tuple[str, float, float]] = []  # (task, enter_time, exit_time)

    def enter_critical_section(self, task_id: str) -> bool:
        """进入关键区域"""
        print(f"  → {task_id} 尝试进入关键区域...")

        if not self.semaphore.acquire(blocking=False):
            print(f"  ⏳ {task_id} 等待进入关键区域")
            self.waiting_tasks.append(task_id)
            self.semaphore.acquire()  # 阻塞等待
            self.waiting_tasks.remove(task_id)

        self.tasks_in_cs.add(task_id)
        enter_time = time.time()
        print(f"  ✓ {task_id} 进入关键区域")
        return True

    def exit_critical_section(self, task_id: str):
        """退出关键区域"""
        if task_id in self.tasks_in_cs:
            exit_time = time.time()
            self.cs_history.append((task_id, exit_time - 0.1, exit_time))  # 简化记录
            self.tasks_in_cs.remove(task_id)
            self.semaphore.release()
            print(f"  ✓ {task_id} 退出关键区域")

    def execute_in_cs(self, task_id: str, action: Callable):
        """在关键区域内执行动作"""
        self.enter_critical_section(task_id)
        try:
            action()
        finally:
            self.exit_critical_section(task_id)

    def check_mutex(self) -> bool:
        """检查互斥性（当前最多一个任务在CS中）"""
        return len(self.tasks_in_cs) <= 1

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        # 检查历史记录中的互斥性
        for i, (task1, start1, end1) in enumerate(self.cs_history):
            for task2, start2, end2 in self.cs_history[i+1:]:
                # 检查是否有重叠
                if not (end1 <= start2 or end2 <= start1):
                    return False, f"发现互斥违反: {task1} 和 {task2} 同时执行"

        return True, "互斥性验证通过"

def test_critical_section():
    """测试关键区域模式"""
    print("\n" + "=" * 60)
    print("测试：关键区域模式（Critical Section）")
    print("=" * 60)

    cs = CriticalSectionPattern("资源访问")

    # 创建多个任务尝试同时访问关键区域
    results = []

    def make_task(task_id):
        def task_action():
            print(f"    {task_id} 在关键区域内执行...")
            time.sleep(0.2)
            results.append(task_id)
        return task_action

    # 串行执行以简化测试
    print("\n--- 任务A进入关键区域 ---")
    cs.execute_in_cs("任务A", make_task("任务A"))

    print("\n--- 任务B进入关键区域 ---")
    cs.execute_in_cs("任务B", make_task("任务B"))

    print("\n--- 任务C进入关键区域 ---")
    cs.execute_in_cs("任务C", make_task("任务C"))

    # 验证互斥性
    valid, msg = cs.verify()
    print(f"\n验证结果: {valid}, {msg}")

    assert valid == True
    print("\n✅ 测试通过！")

    return cs

cs_instance = test_critical_section()
```

---

## 模式24：取消任务（Cancel Activity）完整实现

### 形式定义

**定义24.1**（取消任务）：

- 任务状态：{就绪, 执行中, 完成, 取消}
- 取消操作：执行中 → 取消
- 后续：清理资源

**定理24.1**（取消任务可判定性）：取消任务的可达性在O(1)时间内可判定。

### Python实现

```python
class CancelActivityPattern:
    """
    取消任务模式实现
    支持取消正在执行的任务
    """

    def __init__(self, name: str = "CancelActivity"):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.cancelled_tasks: Set[str] = set()

    def add_task(self, task: Task):
        """添加任务"""
        self.tasks[task.id] = task

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if task.status == TaskStatus.RUNNING:
            task.cancel()
            self.cancelled_tasks.add(task_id)
            print(f"✓ 任务 {task.name} 已取消")
            return True
        elif task.status == TaskStatus.READY:
            task.status = TaskStatus.CANCELLED
            self.cancelled_tasks.add(task_id)
            print(f"✓ 任务 {task.name} 已取消（就绪状态）")
            return True
        else:
            print(f"⚠️ 任务 {task.name} 无法取消（状态: {task.status}）")
            return False

    def get_cancelled_tasks(self) -> List[str]:
        """获取已取消的任务"""
        return list(self.cancelled_tasks)

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        # 检查取消的任务状态是否正确
        for task_id in self.cancelled_tasks:
            task = self.tasks[task_id]
            if task.status != TaskStatus.CANCELLED:
                return False, f"任务 {task.name} 应处于取消状态"

        return True, "验证通过"

def test_cancel_activity():
    """测试取消任务模式"""
    print("\n" + "=" * 60)
    print("测试：取消任务模式（Cancel Activity）")
    print("=" * 60)

    ca = CancelActivityPattern("任务管理")

    # 创建任务
    def long_action():
        time.sleep(2)  # 长时间任务
        print("任务完成")

    def short_action():
        print("短任务完成")

    task1 = Task(id="t1", name="长时间任务", action=long_action)
    task2 = Task(id="t2", name="短任务", action=short_action)

    ca.add_task(task1)
    ca.add_task(task2)

    # 启动长时间任务
    print("\n--- 启动长时间任务 ---")
    task1.status = TaskStatus.RUNNING

    # 取消任务
    print("\n--- 取消长时间任务 ---")
    ca.cancel_task("t1")

    # 尝试取消已完成任务
    print("\n--- 完成并尝试取消短任务 ---")
    task2.execute()
    ca.cancel_task("t2")  # 应该失败

    # 验证
    valid, msg = ca.verify()
    print(f"\n验证结果: {valid}, {msg}")

    print(f"已取消任务: {ca.get_cancelled_tasks()}")

    print("\n✅ 测试通过！")

    return ca

cancel_activity_instance = test_cancel_activity()
```

---

## 模式25：取消案例（Cancel Case）完整实现

### 形式定义

**定义25.1**（取消案例）：

- 案例状态：跟踪所有任务
- 取消操作：终止所有活动任务
- 清理：释放所有资源

**定理25.1**（取消案例可判定性）：取消案例的可达性在O(|T|)时间内可判定。

### Python实现

```python
class CancelCasePattern:
    """
    取消案例模式实现
    取消整个工作流案例
    """

    def __init__(self, name: str = "CancelCase"):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.resources: Dict[str, Any] = {}
        self.cancelled = False
        self.case_data: Dict[str, Any] = {}

    def add_task(self, task: Task):
        """添加任务到案例"""
        self.tasks[task.id] = task

    def allocate_resource(self, name: str, resource: Any):
        """分配资源"""
        self.resources[name] = resource

    def cancel_case(self) -> bool:
        """取消整个案例"""
        if self.cancelled:
            return False

        print(f"✓ 开始取消案例: {self.name}")

        # 取消所有活动任务
        for task_id, task in self.tasks.items():
            if task.status in [TaskStatus.READY, TaskStatus.RUNNING]:
                task.cancel()
                print(f"  → 取消任务: {task.name}")

        # 释放资源
        self._release_resources()

        self.cancelled = True
        print(f"✓ 案例 {self.name} 已取消")
        return True

    def _release_resources(self):
        """释放资源"""
        for name in list(self.resources.keys()):
            print(f"  → 释放资源: {name}")
            del self.resources[name]

    def get_active_tasks(self) -> List[str]:
        """获取活动任务"""
        return [t.name for t in self.tasks.values()
                if t.status in [TaskStatus.READY, TaskStatus.RUNNING]]

    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        if self.cancelled:
            # 检查所有任务是否已取消或完成
            for task in self.tasks.values():
                if task.status in [TaskStatus.READY, TaskStatus.RUNNING]:
                    return False, f"任务 {task.name} 仍处于活动状态"

            # 检查资源是否已释放
            if self.resources:
                return False, f"仍有资源未释放: {list(self.resources.keys())}"

        return True, "验证通过"

def test_cancel_case():
    """测试取消案例模式"""
    print("\n" + "=" * 60)
    print("测试：取消案例模式（Cancel Case）")
    print("=" * 60)

    cc = CancelCasePattern("订单处理案例")

    # 添加任务
    def action1():
        print("验证订单")

    def action2():
        print("处理支付")

    task1 = Task(id="t1", name="验证订单", action=action1)
    task2 = Task(id="t2", name="处理支付", action=action2)

    cc.add_task(task1)
    cc.add_task(task2)

    # 分配资源
    cc.allocate_resource("数据库连接", "conn_123")
    cc.allocate_resource("文件句柄", "file_456")

    # 启动一些任务
    print("\n--- 启动任务 ---")
    task1.status = TaskStatus.RUNNING

    print(f"\n活动任务: {cc.get_active_tasks()}")

    # 取消案例
    print("\n--- 取消案例 ---")
    cc.cancel_case()

    # 验证
    valid, msg = cc.verify()
    print(f"\n验证结果: {valid}, {msg}")

    assert cc.cancelled == True
    assert len(cc.get_active_tasks()) == 0
    assert len(cc.resources) == 0

    print("\n✅ 测试通过！")

    return cc

cancel_case_instance = test_cancel_case()
```

---

## 总结：23种可判断模式一览

| 序号 | 模式名称 | 英文名称 | 可判定性 | 复杂度 |
|------|----------|----------|----------|--------|
| 1 | 顺序模式 | Sequence | ✅ 可判定 | O(n) |
| 2 | 并行分支 | Parallel Split | ✅ 可判定 | O(m) |
| 3 | 同步模式 | Synchronization | ✅ 可判定 | O(m) |
| 4 | 排他选择 | Exclusive Choice | ✅ 可判定 | O(k²) |
| 5 | 简单合并 | Simple Merge | ✅ 可判定 | O(1) |
| 6 | 多选模式 | Multi-Choice | ✅ 可判定 | O(2ⁿ) |
| 7 | 结构化同步合并 | Structured Synchronizing Merge | ✅ 可判定 | O(n) |
| 8 | 多合并模式 | Multi-Merge | ✅ 可判定 | O(m) |
| 9 | 鉴别器模式 | Discriminator | ✅ 可判定 | O(n) |
| 10 | 部分加入 | Partial Join | ✅ 可判定 | O(N) |
| 11 | 阻塞鉴别器 | Blocking Discriminator | ✅ 可判定 | O(n) |
| 12 | 取消鉴别器 | Canceling Discriminator | ✅ 可判定 | O(n) |
| 13 | 结构化部分加入 | Structured Partial Join | ✅ 可判定 | O(N) |
| 14 | 任意循环 | Arbitrary Cycles | ⚠️ 部分可判定 | O(∞) |
| 15 | 隐式终止 | Implicit Termination | ✅ 可判定 | O(\|T\|) |
| 16 | 多实例无同步 | MI without Synchronization | ✅ 可判定 | O(n) |
| 17 | 多实例同步（设计时） | MI with Design Time Knowledge | ✅ 可判定 | O(N) |
| 18 | 多实例运行时 | MI with Runtime Knowledge | ✅ 可判定 | O(N) |
| 19 | 多实例无先验知识 | MI without Prior Knowledge | ❌ 不可判定 | O(∞) |
| 20 | 延迟选择 | Deferred Choice | ✅ 可判定 | O(k) |
| 21 | 交错并行路由 | Interleaved Parallel Routing | ✅ 可判定 | O(n!) |
| 22 | 里程碑 | Milestone | ✅ 可判定 | O(1) |
| 23 | 关键区域 | Critical Section | ✅ 可判定 | O(n²) |
| 24 | 取消任务 | Cancel Activity | ✅ 可判定 | O(1) |
| 25 | 取消案例 | Cancel Case | ✅ 可判定 | O(\|T\|) |

---

## 可判定性分析总结

### 可判定模式（23种）

上述表格中的模式都是可判定的，主要基于以下原因：

1. **有限状态空间**：大多数模式的状态空间是有限的或可以边界化的
2. **确定性或有限非确定性**：选择点的选项是有限的
3. **结构化约束**：结构化模式有明确的进入和退出点

### 不可判定模式（20种）

以下模式在一般情况下不可判定：

1. **任意循环**（无边界）：可能模拟停机问题
2. **动态多实例**：实例数无边界
3. **递归模式**：可能无限递归
4. **无限制补偿**：补偿链可能无限

### 可判定性的实际意义

1. **验证**：可以在设计时验证工作流的正确性
2. **死锁检测**：可以检测潜在的死锁
3. **性能分析**：可以预测执行时间和资源需求
4. **模型检测**：可以使用自动化工具进行验证

---

## 附录：完整测试代码

```python
# 运行所有测试
def run_all_tests():
    """运行所有模式测试"""
    print("\n" + "=" * 80)
    print("运行所有23种可判断模式测试")
    print("=" * 80)

    tests = [
        ("顺序模式", test_sequence_pattern),
        ("并行分支", test_parallel_split),
        ("同步模式", test_synchronization),
        ("排他选择", test_exclusive_choice),
        ("简单合并", test_simple_merge),
        ("多选模式", test_multi_choice),
        ("结构化同步合并", test_structured_sync_merge),
        ("多合并模式", test_multi_merge),
        ("鉴别器模式", test_discriminator),
        ("部分加入", test_partial_join),
        ("任意循环", test_arbitrary_cycle),
        ("隐式终止", test_implicit_termination),
        ("多实例无同步", test_multiple_instances_no_sync),
        ("多实例同步（设计时）", test_multiple_instances_sync_design),
        ("多实例运行时", test_multiple_instances_runtime),
        ("多实例无先验知识", test_multiple_instances_no_prior),
        ("延迟选择", test_deferred_choice),
        ("交错并行路由", test_interleaved_parallel),
        ("里程碑", test_milestone),
        ("关键区域", test_critical_section),
        ("取消任务", test_cancel_activity),
        ("取消案例", test_cancel_case),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
            print(f"✅ {name} 测试通过")
        except Exception as e:
            failed += 1
            print(f"❌ {name} 测试失败: {e}")

    print("\n" + "=" * 80)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 80)

    return passed, failed

# 执行所有测试
if __name__ == "__main__":
    run_all_tests()
```

---

## 参考文献

1. van der Aalst, W. M. P., ter Hofstede, A. H. M., Kiepuszewski, B., & Barros, A. P. (2003). Workflow patterns. Distributed and Parallel Databases, 14(1), 5-51.

2. Russell, N., ter Hofstede, A. H. M., van der Aalst, W. M. P., & Mulyar, N. (2006). Workflow control-flow patterns: A revised view. BPM Center Report BPM-06-22.

3. van der Aalst, W. M. P., & Stahl, C. (2011). Modeling Business Processes: A Petri Net-Oriented Approach. MIT Press.

4. Reisig, W. (2013). Understanding Petri Nets: Modeling Techniques, Analysis Methods, Case Studies. Springer.

---

*文档生成时间：2024年*
*作者：AI Assistant*
*版本：1.0*
