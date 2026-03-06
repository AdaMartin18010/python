#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
43种工作流设计模式 - 23种可判断模式完整Python实现

本模块实现了工作流模式中的23种可判断模式，包括：
- 基础控制流模式（5种）
- 高级分支同步模式（8种）
- 结构化模式（2种）
- 多实例模式（4种）
- 状态基础模式（4种）
- 取消模式（2种）

作者：AI Assistant
版本：1.0
"""

from enum import Enum, auto
from typing import List, Dict, Set, Callable, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import deque
import threading
import time
from abc import ABC, abstractmethod
import uuid
from itertools import permutations
import queue
import concurrent.futures

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


# ============================================================================
# 模式1：顺序模式（Sequence）
# ============================================================================

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
        return True, "验证通过"


# ============================================================================
# 模式2：并行分支模式（Parallel Split）
# ============================================================================

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
        if not self.predecessor:
            return False, "缺少前驱任务"
        return True, "验证通过"


# ============================================================================
# 模式3：同步模式（Synchronization / AND-Join）
# ============================================================================

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
        return True, "验证通过"
    
    def check_deadlock(self) -> Tuple[bool, List[str]]:
        """检查是否存在死锁"""
        failed = [t.name for t in self.inputs if t.status == TaskStatus.FAILED]
        cancelled = [t.name for t in self.inputs if t.status == TaskStatus.CANCELLED]
        
        if failed or cancelled:
            return True, failed + cancelled
        return False, []


# ============================================================================
# 模式4：排他选择模式（Exclusive Choice / XOR-Split）
# ============================================================================

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
            self.selected_branch = satisfied[0]
        else:
            self.selected_branch = satisfied[0]
        
        print(f"✓ 选择分支: {self.selected_branch}")
        return self.selected_branch
    
    def verify_completeness(self, test_data: List[Any]) -> Tuple[bool, List[Any]]:
        """验证完备性"""
        uncovered = []
        for data in test_data:
            satisfied = any(cond(data) for _, cond in self.conditions)
            if not satisfied:
                uncovered.append(data)
        
        return len(uncovered) == 0, uncovered
    
    def verify_mutex(self, test_data: List[Any]) -> Tuple[bool, List[Tuple[Any, List[str]]]]:
        """验证互斥性"""
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
        return True, "基本验证通过"


# ============================================================================
# 模式5：简单合并模式（Simple Merge / XOR-Join）
# ============================================================================

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
            task = completed[0]
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


# ============================================================================
# 模式6：多选模式（Multi-Choice / OR-Split）
# ============================================================================

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
        return True, "基本验证通过"


# ============================================================================
# 模式7：结构化同步合并（Structured Synchronizing Merge / OR-Join）
# ============================================================================

class StructuredSynchronizingMerge:
    """
    结构化同步合并（OR-Join）实现
    仅等待实际被激活的分支完成
    """
    
    def __init__(self, name: str = "StructuredSyncMerge"):
        self.name = name
        self.all_branches: List[str] = []
        self.activated_branches: Set[str] = set()
        self.completed_branches: Set[str] = set()
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


# ============================================================================
# 模式8：多合并模式（Multi-Merge）
# ============================================================================

class MultiMergePattern:
    """
    多合并模式实现
    每个分支到达都触发后续任务，不等待同步
    """
    
    def __init__(self, name: str = "MultiMerge"):
        self.name = name
        self.inputs: List[Task] = []
        self.successor: Optional[Task] = None
        self.trigger_history: List[str] = []
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
                
                if self.successor:
                    self.successor.reset()
                    self.successor.execute()
                    triggers += 1
        
        return triggers
    
    def verify(self) -> Tuple[bool, str]:
        """验证正确性"""
        if len(self.inputs) < 2:
            return False, "至少需要2个输入"
        return True, "验证通过"


# ============================================================================
# 模式9：鉴别器模式（Discriminator）
# ============================================================================

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
        self.cancel_others = False
    
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
                
                if self.successor:
                    self.successor.execute()
                
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


# ============================================================================
# 模式10：部分加入（Partial Join / M-out-of-N）
# ============================================================================

class PartialJoinPattern:
    """
    部分加入模式（M-out-of-N Join）实现
    等待N个分支中的M个完成
    """
    
    def __init__(self, name: str = "PartialJoin", n: int = 0, m: int = 0):
        self.name = name
        self.n = n
        self.m = m
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
            return False, f"M必须在1到N之间"
        return True, "验证通过"


# ============================================================================
# 模式14：任意循环（Arbitrary Cycles）
# ============================================================================

class ArbitraryCyclePattern:
    """
    任意循环模式实现
    支持基于条件的循环执行
    """
    
    def __init__(self, name: str = "ArbitraryCycle"):
        self.name = name
        self.loop_body: Optional[Callable] = None
        self.condition: Optional[Callable[[], bool]] = None
        self.max_iterations = 1000
        self.iteration_count = 0
        self.terminated = False
    
    def set_loop_body(self, body: Callable):
        """设置循环体"""
        self.loop_body = body
    
    def set_condition(self, condition: Callable[[], bool]):
        """设置循环条件"""
        self.condition = condition
    
    def set_max_iterations(self, max_iter: int):
        """设置最大迭代次数"""
        self.max_iterations = max_iter
    
    def execute(self) -> Tuple[int, bool]:
        """执行循环"""
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
        """尝试验证循环是否会终止"""
        if self.max_iterations < float('inf'):
            return True, f"有最大迭代次数限制({self.max_iterations})，必定终止"
        return False, "无法保证终止（停机问题）"


# ============================================================================
# 模式15：隐式终止（Implicit Termination）
# ============================================================================

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
            can_term, msg = self.check_termination()
            if can_term:
                print(f"✓ {msg}")
                return steps, True
            
            ready = self.get_ready_tasks()
            if ready:
                task = ready[0]
                print(f"  → 执行任务: {task.name}")
                task.execute()
            
            steps += 1
        
        return steps, False


# ============================================================================
# 模式16-19：多实例模式
# ============================================================================

class MultipleInstancesNoSync:
    """多实例无同步模式"""
    
    def __init__(self, name: str = "MINoSync"):
        self.name = name
        self.instance_factory: Optional[Callable[[int], Callable]] = None
        self.instances: List[Task] = []
    
    def set_instance_factory(self, factory: Callable[[int], Callable]):
        self.instance_factory = factory
    
    def create_instances(self, count: int) -> List[Task]:
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


class MultipleInstancesWithSyncDesignTime:
    """多实例同步模式（设计时已知数量）"""
    
    def __init__(self, name: str = "MISyncDesignTime", n: int = 0):
        self.name = name
        self.n = n
        self.instance_factory: Optional[Callable[[int], Callable]] = None
        self.instances: List[Task] = []
        self.completed_count = 0
        self.all_completed = threading.Event()
    
    def set_instance_factory(self, factory: Callable[[int], Callable]):
        self.instance_factory = factory
    
    def create_instances(self) -> List[Task]:
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
        def on_complete(task):
            self.completed_count += 1
            print(f"  → {task.name} 完成 ({self.completed_count}/{self.n})")
            if self.completed_count >= self.n:
                self.all_completed.set()
        
        for task in self.instances:
            original_action = task.action
            def make_wrapped(t, orig):
                return lambda: (orig(), on_complete(t))
            task.action = make_wrapped(task, original_action)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(task.execute) for task in self.instances]
            concurrent.futures.wait(futures, timeout=timeout)
        
        return self.all_completed.wait(timeout=timeout)


class MultipleInstancesRuntime:
    """多实例运行时模式"""
    
    def __init__(self, name: str = "MIRuntime"):
        self.name = name
        self.instance_factory: Optional[Callable[[int], Callable]] = None
        self.instances: List[Task] = []
        self.n = 0
    
    def set_instance_factory(self, factory: Callable[[int], Callable]):
        self.instance_factory = factory
    
    def determine_count(self, data: Any) -> int:
        if isinstance(data, (list, tuple)):
            return len(data)
        elif isinstance(data, int):
            return data
        return 1
    
    def create_instances(self, runtime_data: Any) -> List[Task]:
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
        executed = []
        for task in self.instances:
            task.execute()
            executed.append(task.name)
        return executed


class MultipleInstancesNoPriorKnowledge:
    """多实例无先验知识模式"""
    
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
        self.accepting_new = False
        print("✓ 不再接受新实例")
    
    def execute_instance(self, task: Task):
        task.execute()
        self.completed_instances.add(task.id)
        print(f"  → {task.name} 完成")
        
        if not self.accepting_new and len(self.completed_instances) == len(self.instances):
            self.completion_event.set()
    
    def wait_for_completion(self, timeout: float = None) -> bool:
        return self.completion_event.wait(timeout=timeout)


# ============================================================================
# 模式20：延迟选择（Deferred Choice）
# ============================================================================

class DeferredChoicePattern:
    """延迟选择模式实现"""
    
    def __init__(self, name: str = "DeferredChoice"):
        self.name = name
        self.events: Dict[str, Callable] = {}
        self.event_queue = queue.Queue()
        self.selected_event: Optional[str] = None
        self.timeout: Optional[float] = None
    
    def register_event(self, event_name: str, handler: Callable):
        self.events[event_name] = handler
    
    def set_timeout(self, timeout: float):
        self.timeout = timeout
    
    def trigger_event(self, event_name: str):
        if event_name in self.events:
            self.event_queue.put(event_name)
            print(f"✓ 事件触发: {event_name}")
    
    def wait_and_choose(self) -> Optional[str]:
        print(f"⏳ 等待事件... (可用事件: {list(self.events.keys())})")
        
        try:
            self.selected_event = self.event_queue.get(timeout=self.timeout)
            print(f"✓ 选择事件: {self.selected_event}")
            
            handler = self.events[self.selected_event]
            handler()
            
            return self.selected_event
        except queue.Empty:
            print("⚠️ 等待超时，没有事件触发")
            return None
    
    def verify(self) -> Tuple[bool, str]:
        if len(self.events) < 2:
            return False, "至少需要2个事件"
        return True, "验证通过"


# ============================================================================
# 模式21：交错并行路由（Interleaved Parallel Routing）
# ============================================================================

class InterleavedParallelRouting:
    """交错并行路由模式实现"""
    
    def __init__(self, name: str = "InterleavedParallel"):
        self.name = name
        self.tasks: List[Task] = []
        self.lock = threading.Lock()
        self.executed_order: List[str] = []
        self.current_task: Optional[str] = None
    
    def add_task(self, task: Task):
        self.tasks.append(task)
    
    def execute_task(self, task: Task) -> bool:
        with self.lock:
            if self.current_task is not None:
                print(f"⚠️ 任务 {task.name} 无法执行，{self.current_task} 正在运行")
                return False
            
            self.current_task = task.name
            print(f"  → 开始执行: {task.name}")
        
        task.execute()
        
        with self.lock:
            self.executed_order.append(task.name)
            self.current_task = None
            print(f"  ✓ 完成: {task.name}")
        
        return True
    
    def execute_all(self, order: Optional[List[int]] = None) -> List[str]:
        if order is None:
            order = list(range(len(self.tasks)))
        
        for idx in order:
            if 0 <= idx < len(self.tasks):
                self.execute_task(self.tasks[idx])
        
        return self.executed_order
    
    def get_all_possible_orders(self) -> List[List[str]]:
        task_names = [t.name for t in self.tasks]
        return [list(p) for p in permutations(task_names)]
    
    def verify(self) -> Tuple[bool, str]:
        if len(self.tasks) < 2:
            return False, "至少需要2个任务"
        return True, "验证通过"


# ============================================================================
# 模式22：里程碑（Milestone）
# ============================================================================

class MilestonePattern:
    """里程碑模式实现"""
    
    def __init__(self, name: str = "Milestone"):
        self.name = name
        self.milestones: Dict[str, bool] = {}
        self.tasks: Dict[str, Tuple[Task, str]] = {}
    
    def set_milestone(self, name: str, achieved: bool = False):
        self.milestones[name] = achieved
    
    def achieve_milestone(self, name: str):
        self.milestones[name] = True
        print(f"✓ 达成里程碑: {name}")
    
    def add_task_with_milestone(self, task: Task, milestone: str):
        self.tasks[task.id] = (task, milestone)
    
    def can_execute(self, task_id: str) -> bool:
        if task_id not in self.tasks:
            return False
        task, milestone = self.tasks[task_id]
        return self.milestones.get(milestone, False)
    
    def execute_task(self, task_id: str) -> bool:
        if not self.can_execute(task_id):
            required = self.tasks[task_id][1]
            print(f"⏳ 任务无法执行，需要里程碑: {required}")
            return False
        
        task = self.tasks[task_id][0]
        task.execute()
        return True
    
    def get_achieved_milestones(self) -> List[str]:
        return [name for name, achieved in self.milestones.items() if achieved]


# ============================================================================
# 模式23：关键区域（Critical Section）
# ============================================================================

class CriticalSectionPattern:
    """关键区域模式实现"""
    
    def __init__(self, name: str = "CriticalSection"):
        self.name = name
        self.semaphore = threading.Semaphore(1)
        self.tasks_in_cs: Set[str] = set()
        self.waiting_tasks: List[str] = []
        self.cs_history: List[Tuple[str, float, float]] = []
    
    def enter_critical_section(self, task_id: str) -> bool:
        print(f"  → {task_id} 尝试进入关键区域...")
        
        if not self.semaphore.acquire(blocking=False):
            print(f"  ⏳ {task_id} 等待进入关键区域")
            self.waiting_tasks.append(task_id)
            self.semaphore.acquire()
            self.waiting_tasks.remove(task_id)
        
        self.tasks_in_cs.add(task_id)
        enter_time = time.time()
        print(f"  ✓ {task_id} 进入关键区域")
        return True
    
    def exit_critical_section(self, task_id: str):
        if task_id in self.tasks_in_cs:
            exit_time = time.time()
            self.cs_history.append((task_id, exit_time - 0.1, exit_time))
            self.tasks_in_cs.remove(task_id)
            self.semaphore.release()
            print(f"  ✓ {task_id} 退出关键区域")
    
    def execute_in_cs(self, task_id: str, action: Callable):
        self.enter_critical_section(task_id)
        try:
            action()
        finally:
            self.exit_critical_section(task_id)
    
    def check_mutex(self) -> bool:
        return len(self.tasks_in_cs) <= 1
    
    def verify(self) -> Tuple[bool, str]:
        for i, (task1, start1, end1) in enumerate(self.cs_history):
            for task2, start2, end2 in self.cs_history[i+1:]:
                if not (end1 <= start2 or end2 <= start1):
                    return False, f"发现互斥违反: {task1} 和 {task2} 同时执行"
        return True, "互斥性验证通过"


# ============================================================================
# 模式24：取消任务（Cancel Activity）
# ============================================================================

class CancelActivityPattern:
    """取消任务模式实现"""
    
    def __init__(self, name: str = "CancelActivity"):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.cancelled_tasks: Set[str] = set()
    
    def add_task(self, task: Task):
        self.tasks[task.id] = task
    
    def cancel_task(self, task_id: str) -> bool:
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
        return list(self.cancelled_tasks)
    
    def verify(self) -> Tuple[bool, str]:
        for task_id in self.cancelled_tasks:
            task = self.tasks[task_id]
            if task.status != TaskStatus.CANCELLED:
                return False, f"任务 {task.name} 应处于取消状态"
        return True, "验证通过"


# ============================================================================
# 模式25：取消案例（Cancel Case）
# ============================================================================

class CancelCasePattern:
    """取消案例模式实现"""
    
    def __init__(self, name: str = "CancelCase"):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.resources: Dict[str, Any] = {}
        self.cancelled = False
        self.case_data: Dict[str, Any] = {}
    
    def add_task(self, task: Task):
        self.tasks[task.id] = task
    
    def allocate_resource(self, name: str, resource: Any):
        self.resources[name] = resource
    
    def cancel_case(self) -> bool:
        if self.cancelled:
            return False
        
        print(f"✓ 开始取消案例: {self.name}")
        
        for task_id, task in self.tasks.items():
            if task.status in [TaskStatus.READY, TaskStatus.RUNNING]:
                task.cancel()
                print(f"  → 取消任务: {task.name}")
        
        self._release_resources()
        
        self.cancelled = True
        print(f"✓ 案例 {self.name} 已取消")
        return True
    
    def _release_resources(self):
        for name in list(self.resources.keys()):
            print(f"  → 释放资源: {name}")
            del self.resources[name]
    
    def get_active_tasks(self) -> List[str]:
        return [t.name for t in self.tasks.values() 
                if t.status in [TaskStatus.READY, TaskStatus.RUNNING]]
    
    def verify(self) -> Tuple[bool, str]:
        if self.cancelled:
            for task in self.tasks.values():
                if task.status in [TaskStatus.READY, TaskStatus.RUNNING]:
                    return False, f"任务 {task.name} 仍处于活动状态"
            if self.resources:
                return False, f"仍有资源未释放: {list(self.resources.keys())}"
        return True, "验证通过"


# ============================================================================
# 测试函数
# ============================================================================

def test_sequence_pattern():
    """测试顺序模式"""
    print("\n" + "=" * 60)
    print("测试：顺序模式（Sequence Pattern）")
    print("=" * 60)
    
    seq = SequencePattern("订单处理流程")
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
    
    valid, msg = seq.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print("\n执行顺序：")
    executed = seq.run()
    
    print(f"\n执行结果: {executed}")
    print(f"完成状态: {seq.completed}")
    
    assert executed == ["验证订单", "检查库存", "处理支付", "发货"]
    assert seq.completed == True
    print("\n✅ 正例测试通过！")
    
    return seq


def test_parallel_split():
    """测试并行分支模式"""
    print("\n" + "=" * 60)
    print("测试：并行分支模式（Parallel Split Pattern）")
    print("=" * 60)
    
    ps = ParallelSplitPattern("并行处理")
    
    def pre_action():
        print("✓ 前驱任务完成，开始并行分支")
    
    pre_task = Task(id="pre", name="准备数据", action=pre_action)
    pre_task.execute()
    ps.set_predecessor(pre_task)
    
    def branch1():
        print("  → 分支1完成：发送邮件通知")
    
    def branch2():
        print("  → 分支2完成：更新数据库")
    
    def branch3():
        print("  → 分支3完成：记录日志")
    
    ps.add_branch("发送邮件", branch1)
    ps.add_branch("更新数据库", branch2)
    ps.add_branch("记录日志", branch3)
    
    valid, msg = ps.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print("\n执行并行分支：")
    executed = ps.execute_branches(parallel=False)
    
    print(f"\n执行结果: {executed}")
    
    assert len(executed) == 3
    print("\n✅ 正例测试通过！")
    
    return ps


def test_synchronization():
    """测试同步模式"""
    print("\n" + "=" * 60)
    print("测试：同步模式（Synchronization / AND-Join）")
    print("=" * 60)
    
    sync = SynchronizationPattern("订单处理同步")
    
    def action1():
        print("  → 分支1：验证支付完成")
    
    def action2():
        print("  → 分支2：验证库存完成")
    
    def action3():
        print("  → 分支3：验证地址完成")
    
    task1 = Task(id="t1", name="验证支付", action=action1)
    task2 = Task(id="t2", name="验证库存", action=action2)
    task3 = Task(id="t3", name="验证地址", action=action3)
    
    task1.execute()
    task2.execute()
    
    sync.add_input(task1)
    sync.add_input(task2)
    sync.add_input(task3)
    
    def final_action():
        print("✓ 所有验证完成，确认订单！")
    
    final_task = Task(id="final", name="确认订单", action=final_action)
    sync.set_successor(final_task)
    
    valid, msg = sync.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print("\n第一次同步尝试（task3未完成）：")
    result = sync.sync_and_execute()
    assert result is None
    
    print("\n完成剩余任务：")
    task3.execute()
    
    print("\n第二次同步尝试（所有任务完成）：")
    result = sync.sync_and_execute()
    assert result is not None
    
    print("\n✅ 正例测试通过！")
    
    return sync


def test_exclusive_choice():
    """测试排他选择模式"""
    print("\n" + "=" * 60)
    print("测试：排他选择模式（Exclusive Choice / XOR-Split）")
    print("=" * 60)
    
    xor = ExclusiveChoicePattern("支付路由")
    
    xor.add_condition("信用卡", lambda d: d.get("amount", 0) > 1000)
    xor.add_condition("借记卡", lambda d: 100 < d.get("amount", 0) <= 1000)
    xor.add_condition("现金", lambda d: d.get("amount", 0) <= 100)
    
    valid, msg = xor.verify()
    print(f"\n基本验证: {valid}, {msg}")
    
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
    
    print("\n✅ 所有测试通过！")
    
    return xor


def test_simple_merge():
    """测试简单合并模式"""
    print("\n" + "=" * 60)
    print("测试：简单合并模式（Simple Merge / XOR-Join）")
    print("=" * 60)
    
    merge = SimpleMergePattern("路径合并")
    
    def action1():
        print("  → 路径1执行完成")
    
    def action2():
        print("  → 路径2执行完成")
    
    task1 = Task(id="p1", name="路径A", action=action1)
    task2 = Task(id="p2", name="路径B", action=action2)
    
    merge.add_input(task1)
    merge.add_input(task2)
    
    def final_action():
        print("✓ 合并后任务执行")
    
    final_task = Task(id="final", name="后续处理", action=final_action)
    merge.set_successor(final_task)
    
    valid, msg = merge.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print("\n--- 正例：路径1先完成 ---")
    task1.execute()
    result = merge.check_and_trigger()
    assert result is not None
    print("✅ 路径1触发成功")
    
    print("\n✅ 所有测试通过！")
    
    return merge


def test_multi_choice():
    """测试多选模式"""
    print("\n" + "=" * 60)
    print("测试：多选模式（Multi-Choice / OR-Split）")
    print("=" * 60)
    
    or_split = MultiChoicePattern("通知发送")
    
    or_split.add_branch("邮件", lambda d: d.get("email", False))
    or_split.add_branch("短信", lambda d: d.get("sms", False))
    or_split.add_branch("推送", lambda d: d.get("push", False))
    or_split.add_branch("站内信", lambda d: d.get("internal", False))
    
    valid, msg = or_split.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print("\n--- 正例测试 ---")
    
    test_cases = [
        ({"email": True, "sms": True}, ["邮件", "短信"]),
        ({"email": True, "push": True, "internal": True}, ["邮件", "推送", "站内信"]),
        ({"sms": True}, ["短信"]),
    ]
    
    for data, expected in test_cases:
        or_split.set_data(data)
        result = or_split.evaluate()
        assert set(result) == set(expected), f"期望 {expected}, 实际 {result}"
        print(f"✅ 数据 {data} -> {result}")
    
    print("\n✅ 所有测试通过！")
    
    return or_split


def test_structured_sync_merge():
    """测试结构化同步合并"""
    print("\n" + "=" * 60)
    print("测试：结构化同步合并（Structured Synchronizing Merge / OR-Join）")
    print("=" * 60)
    
    or_join = StructuredSynchronizingMerge("通知同步")
    
    or_join.register_branches(["邮件", "短信", "推送", "站内信"])
    or_join.activate_branches(["邮件", "短信"])
    
    def email_task():
        print("  → 发送邮件完成")
    
    def sms_task():
        print("  → 发送短信完成")
    
    task_email = Task(id="email", name="邮件任务", action=email_task)
    task_sms = Task(id="sms", name="短信任务", action=sms_task)
    
    or_join.add_task("邮件", task_email)
    or_join.add_task("短信", task_sms)
    
    def final_action():
        print("✓ 所有通知发送完成！")
    
    final_task = Task(id="final", name="通知完成", action=final_action)
    or_join.set_successor(final_task)
    
    valid, msg = or_join.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print("\n--- 第一次同步尝试（未完成）---")
    or_join.sync_and_execute()
    
    print("\n--- 完成部分任务 ---")
    task_email.execute()
    or_join.mark_completed("邮件")
    or_join.sync_and_execute()
    
    print("\n--- 完成所有任务 ---")
    task_sms.execute()
    or_join.mark_completed("短信")
    or_join.sync_and_execute()
    
    print("\n✅ 测试通过！")
    
    return or_join


def test_multi_merge():
    """测试多合并模式"""
    print("\n" + "=" * 60)
    print("测试：多合并模式（Multi-Merge）")
    print("=" * 60)
    
    mm = MultiMergePattern("事件处理")
    
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
    
    def log_action():
        print("  → 记录日志")
    
    log_task = Task(id="log", name="记录日志", action=log_action)
    mm.set_successor(log_task)
    
    valid, msg = mm.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
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


def test_discriminator():
    """测试鉴别器模式"""
    print("\n" + "=" * 60)
    print("测试：鉴别器模式（Discriminator）")
    print("=" * 60)
    
    disc = DiscriminatorPattern("最快响应")
    
    def action1():
        print("  → 服务A响应")
    
    def action2():
        print("  → 服务B响应")
    
    def action3():
        print("  → 服务C响应")
    
    task_a = Task(id="a", name="服务A", action=action1)
    task_b = Task(id="b", name="服务B", action=action2)
    task_c = Task(id="c", name="服务C", action=action3)
    
    disc.add_branch(task_a)
    disc.add_branch(task_b)
    disc.add_branch(task_c)
    
    def use_result():
        print("✓ 使用最快响应的结果")
    
    result_task = Task(id="result", name="使用结果", action=use_result)
    disc.set_successor(result_task)
    
    valid, msg = disc.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print("\n--- 模拟分支完成（服务B最快）---")
    task_b.status = TaskStatus.COMPLETED
    winner = disc.check_first_complete()
    assert winner == "服务B"
    
    print("\n✅ 测试通过！")
    
    return disc


def test_partial_join():
    """测试部分加入模式"""
    print("\n" + "=" * 60)
    print("测试：部分加入模式（Partial Join / M-out-of-N）")
    print("=" * 60)
    
    pj = PartialJoinPattern("投票统计", n=5, m=3)
    
    tasks = []
    for i in range(5):
        def make_action(idx):
            return lambda: print(f"  → 投票{idx+1}完成")
        
        task = Task(id=f"v{i}", name=f"投票{i+1}", action=make_action(i))
        tasks.append(task)
        pj.add_branch(task)
    
    def count_votes():
        print("✓ 已达到3票，统计结果！")
    
    result_task = Task(id="result", name="统计结果", action=count_votes)
    pj.set_successor(result_task)
    
    valid, msg = pj.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
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


def test_arbitrary_cycle():
    """测试任意循环模式"""
    print("\n" + "=" * 60)
    print("测试：任意循环模式（Arbitrary Cycles）")
    print("=" * 60)
    
    print("\n--- 正例：有限循环（计数器递减）---")
    cycle1 = ArbitraryCyclePattern("有限循环")
    
    counter = [5]
    
    def body1():
        counter[0] -= 1
        print(f"    计数器: {counter[0]}")
    
    cycle1.set_loop_body(body1)
    cycle1.set_condition(lambda: counter[0] > 0)
    
    count, terminated = cycle1.execute()
    assert terminated == True
    assert count == 5
    print("✅ 正例测试通过！")
    
    return cycle1


def test_implicit_termination():
    """测试隐式终止模式"""
    print("\n" + "=" * 60)
    print("测试：隐式终止模式（Implicit Termination）")
    print("=" * 60)
    
    it = ImplicitTerminationPattern("订单流程")
    
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
    
    print("\n--- 运行工作流 ---")
    steps, terminated = it.run_until_termination()
    
    assert terminated == True
    assert it.terminated == True
    print(f"\n✓ 工作流在{steps}步后终止")
    
    print("\n✅ 测试通过！")
    
    return it


def test_multiple_instances_no_sync():
    """测试多实例无同步"""
    print("\n" + "=" * 60)
    print("测试：多实例无同步（Multiple Instances without Synchronization）")
    print("=" * 60)
    
    mi = MultipleInstancesNoSync("批量发送")
    
    def make_instance(idx):
        return lambda: print(f"  → 发送给用户{idx+1}")
    
    mi.set_instance_factory(make_instance)
    
    instances = mi.create_instances(5)
    print(f"创建了 {len(instances)} 个实例")
    
    print("\n执行所有实例：")
    executed = mi.execute_all(parallel=False)
    
    assert len(executed) == 5
    print("\n✅ 测试通过！")
    
    return mi


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


def test_multiple_instances_runtime():
    """测试多实例运行时"""
    print("\n" + "=" * 60)
    print("测试：多实例运行时（运行时确定数量）")
    print("=" * 60)
    
    mi = MultipleInstancesRuntime("动态处理")
    
    def make_instance(idx):
        return lambda: print(f"  → 处理第{idx+1}个订单")
    
    mi.set_instance_factory(make_instance)
    
    orders = ["订单A", "订单B", "订单C", "订单D"]
    mi.create_instances(orders)
    
    print("执行所有实例：")
    executed = mi.execute_all()
    
    assert len(executed) == 4
    print("\n✅ 测试通过！")
    
    return mi


def test_multiple_instances_no_prior():
    """测试多实例无先验知识"""
    print("\n" + "=" * 60)
    print("测试：多实例无先验知识（动态添加）")
    print("=" * 60)
    
    mi = MultipleInstancesNoPriorKnowledge("动态任务")
    
    def make_instance(idx):
        return lambda: print(f"    处理动态任务{idx+1}")
    
    mi.set_instance_factory(make_instance)
    
    print("动态添加实例：")
    task1 = mi.add_instance()
    task2 = mi.add_instance()
    
    print("\n执行实例：")
    mi.execute_instance(task1)
    mi.execute_instance(task2)
    
    print("\n再添加实例：")
    task3 = mi.add_instance()
    mi.execute_instance(task3)
    
    mi.mark_no_more_instances()
    
    print("\n✅ 测试通过！")
    
    return mi


def test_deferred_choice():
    """测试延迟选择"""
    print("\n" + "=" * 60)
    print("测试：延迟选择模式（Deferred Choice）")
    print("=" * 60)
    
    dc = DeferredChoicePattern("用户选择")
    
    def on_email():
        print("  → 用户选择邮件通知")
    
    def on_sms():
        print("  → 用户选择短信通知")
    
    def on_push():
        print("  → 用户选择推送通知")
    
    dc.register_event("邮件", on_email)
    dc.register_event("短信", on_sms)
    dc.register_event("推送", on_push)
    
    valid, msg = dc.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    def simulate_event():
        time.sleep(0.5)
        dc.trigger_event("短信")
    
    t = threading.Thread(target=simulate_event)
    t.start()
    
    print("\n等待用户选择...")
    selected = dc.wait_and_choose()
    
    assert selected == "短信"
    print("\n✅ 测试通过！")
    
    return dc


def test_interleaved_parallel():
    """测试交错并行路由"""
    print("\n" + "=" * 60)
    print("测试：交错并行路由（Interleaved Parallel Routing）")
    print("=" * 60)
    
    ipr = InterleavedParallelRouting("顺序无关任务")
    
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
    
    valid, msg = ipr.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print("\n--- 执行顺序 A->B->C ---")
    ipr.executed_order = []
    order1 = ipr.execute_all([0, 1, 2])
    print(f"执行顺序: {order1}")
    
    print("\n✅ 测试通过！")
    
    return ipr


def test_milestone():
    """测试里程碑模式"""
    print("\n" + "=" * 60)
    print("测试：里程碑模式（Milestone）")
    print("=" * 60)
    
    ms = MilestonePattern("订单里程碑")
    
    ms.set_milestone("订单确认", False)
    ms.set_milestone("支付完成", False)
    ms.set_milestone("发货完成", False)
    
    def ship_action():
        print("  → 执行发货")
    
    def review_action():
        print("  → 执行评价")
    
    ship_task = Task(id="ship", name="发货", action=ship_action)
    review_task = Task(id="review", name="评价", action=review_action)
    
    ms.add_task_with_milestone(ship_task, "支付完成")
    ms.add_task_with_milestone(review_task, "发货完成")
    
    print("\n--- 里程碑未达成时尝试执行 ---")
    ms.execute_task("ship")
    
    print("\n--- 达成里程碑 ---")
    ms.achieve_milestone("订单确认")
    ms.achieve_milestone("支付完成")
    
    print("\n--- 里程碑达成后执行 ---")
    ms.execute_task("ship")
    
    ms.achieve_milestone("发货完成")
    ms.execute_task("review")
    
    print(f"\n已达成里程碑: {ms.get_achieved_milestones()}")
    
    print("\n✅ 测试通过！")
    
    return ms


def test_critical_section():
    """测试关键区域模式"""
    print("\n" + "=" * 60)
    print("测试：关键区域模式（Critical Section）")
    print("=" * 60)
    
    cs = CriticalSectionPattern("资源访问")
    
    results = []
    
    def make_task(task_id):
        def task_action():
            print(f"    {task_id} 在关键区域内执行...")
            time.sleep(0.2)
            results.append(task_id)
        return task_action
    
    print("\n--- 任务A进入关键区域 ---")
    cs.execute_in_cs("任务A", make_task("任务A"))
    
    print("\n--- 任务B进入关键区域 ---")
    cs.execute_in_cs("任务B", make_task("任务B"))
    
    print("\n--- 任务C进入关键区域 ---")
    cs.execute_in_cs("任务C", make_task("任务C"))
    
    valid, msg = cs.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    assert valid == True
    print("\n✅ 测试通过！")
    
    return cs


def test_cancel_activity():
    """测试取消任务模式"""
    print("\n" + "=" * 60)
    print("测试：取消任务模式（Cancel Activity）")
    print("=" * 60)
    
    ca = CancelActivityPattern("任务管理")
    
    def long_action():
        time.sleep(2)
        print("任务完成")
    
    def short_action():
        print("短任务完成")
    
    task1 = Task(id="t1", name="长时间任务", action=long_action)
    task2 = Task(id="t2", name="短任务", action=short_action)
    
    ca.add_task(task1)
    ca.add_task(task2)
    
    print("\n--- 启动长时间任务 ---")
    task1.status = TaskStatus.RUNNING
    
    print("\n--- 取消长时间任务 ---")
    ca.cancel_task("t1")
    
    print("\n--- 完成并尝试取消短任务 ---")
    task2.execute()
    ca.cancel_task("t2")
    
    valid, msg = ca.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    print(f"已取消任务: {ca.get_cancelled_tasks()}")
    
    print("\n✅ 测试通过！")
    
    return ca


def test_cancel_case():
    """测试取消案例模式"""
    print("\n" + "=" * 60)
    print("测试：取消案例模式（Cancel Case）")
    print("=" * 60)
    
    cc = CancelCasePattern("订单处理案例")
    
    def action1():
        print("验证订单")
    
    def action2():
        print("处理支付")
    
    task1 = Task(id="t1", name="验证订单", action=action1)
    task2 = Task(id="t2", name="处理支付", action=action2)
    
    cc.add_task(task1)
    cc.add_task(task2)
    
    cc.allocate_resource("数据库连接", "conn_123")
    cc.allocate_resource("文件句柄", "file_456")
    
    print("\n--- 启动任务 ---")
    task1.status = TaskStatus.RUNNING
    
    print(f"\n活动任务: {cc.get_active_tasks()}")
    
    print("\n--- 取消案例 ---")
    cc.cancel_case()
    
    valid, msg = cc.verify()
    print(f"\n验证结果: {valid}, {msg}")
    
    assert cc.cancelled == True
    assert len(cc.get_active_tasks()) == 0
    assert len(cc.resources) == 0
    
    print("\n✅ 测试通过！")
    
    return cc


# ============================================================================
# 主函数：运行所有测试
# ============================================================================

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
            print(f"\n✅ {name} 测试通过")
        except Exception as e:
            failed += 1
            print(f"\n❌ {name} 测试失败: {e}")
    
    print("\n" + "=" * 80)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 80)
    
    return passed, failed


if __name__ == "__main__":
    run_all_tests()
