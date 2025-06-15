# 03.02-设计模式科学

## 概述

设计模式科学是软件工程中的核心理论，研究软件设计中反复出现的问题及其解决方案。本层将设计模式从经验总结提升为形式化科学，建立严格的理论基础和数学证明。

## 目录结构

### [03.02.01-创建型模式](./03.02.01-创建型模式.md)

- [03.02.01.01-单例模式](./03.02.01-创建型模式.md#单例模式)
- [03.02.01.02-工厂方法模式](./03.02.01-创建型模式.md#工厂方法模式)
- [03.02.01.03-抽象工厂模式](./03.02.01-创建型模式.md#抽象工厂模式)
- [03.02.01.04-建造者模式](./03.02.01-创建型模式.md#建造者模式)
- [03.02.01.05-原型模式](./03.02.01-创建型模式.md#原型模式)

### [03.02.02-结构型模式](./03.02.02-结构型模式.md)

- [03.02.02.01-适配器模式](./03.02.02-结构型模式.md#适配器模式)
- [03.02.02.02-桥接模式](./03.02.02-结构型模式.md#桥接模式)
- [03.02.02.03-组合模式](./03.02.02-结构型模式.md#组合模式)
- [03.02.02.04-装饰器模式](./03.02.02-结构型模式.md#装饰器模式)
- [03.02.02.05-外观模式](./03.02.02-结构型模式.md#外观模式)
- [03.02.02.06-享元模式](./03.02.02-结构型模式.md#享元模式)
- [03.02.02.07-代理模式](./03.02.02-结构型模式.md#代理模式)

### [03.02.03-行为型模式](./03.02.03-行为型模式.md)

- [03.02.03.01-责任链模式](./03.02.03-行为型模式.md#责任链模式)
- [03.02.03.02-命令模式](./03.02.03-行为型模式.md#命令模式)
- [03.02.03.03-解释器模式](./03.02.03-行为型模式.md#解释器模式)
- [03.02.03.04-迭代器模式](./03.02.03-行为型模式.md#迭代器模式)
- [03.02.03.05-中介者模式](./03.02.03-行为型模式.md#中介者模式)
- [03.02.03.06-备忘录模式](./03.02.03-行为型模式.md#备忘录模式)
- [03.02.03.07-观察者模式](./03.02.03-行为型模式.md#观察者模式)
- [03.02.03.08-状态模式](./03.02.03-行为型模式.md#状态模式)
- [03.02.03.09-策略模式](./03.02.03-行为型模式.md#策略模式)
- [03.02.03.10-模板方法模式](./03.02.03-行为型模式.md#模板方法模式)
- [03.02.03.11-访问者模式](./03.02.03-行为型模式.md#访问者模式)

### [03.02.04-并发模式](./03.02.04-并发模式.md)

- [03.02.04.01-活动对象模式](./03.02.04-并发模式.md#活动对象模式)
- [03.02.04.02-管程模式](./03.02.04-并发模式.md#管程模式)
- [03.02.04.03-线程池模式](./03.02.04-并发模式.md#线程池模式)
- [03.02.04.04-生产者-消费者模式](./03.02.04-并发模式.md#生产者-消费者模式)
- [03.02.04.05-读写锁模式](./03.02.04-并发模式.md#读写锁模式)
- [03.02.04.06-Future/Promise模式](./03.02.04-并发模式.md#futurepromise模式)
- [03.02.04.07-Actor模型](./03.02.04-并发模式.md#actor模型)

### [03.02.05-分布式模式](./03.02.05-分布式模式.md)

- [03.02.05.01-服务发现模式](./03.02.05-分布式模式.md#服务发现模式)
- [03.02.05.02-熔断器模式](./03.02.05-分布式模式.md#熔断器模式)
- [03.02.05.03-API网关模式](./03.02.05-分布式模式.md#api网关模式)
- [03.02.05.04-Saga模式](./03.02.05-分布式模式.md#saga模式)
- [03.02.05.05-领导者选举模式](./03.02.05-分布式模式.md#领导者选举模式)
- [03.02.05.06-分片/分区模式](./03.02.05-分布式模式.md#分片分区模式)
- [03.02.05.07-复制模式](./03.02.05-分布式模式.md#复制模式)
- [03.02.05.08-消息队列模式](./03.02.05-分布式模式.md#消息队列模式)

## 理论基础

### 1. 设计模式的形式化定义

设计模式可以形式化定义为：

$$\text{DesignPattern} = \langle \text{Problem}, \text{Solution}, \text{Consequences}, \text{Context} \rangle$$

其中：

- **Problem**: 描述在软件开发中反复出现的设计问题
- **Solution**: 描述解决该问题的抽象设计
- **Consequences**: 描述应用该模式的结果和权衡
- **Context**: 描述模式适用的情境

### 2. 模式分类理论

根据模式的目的和范围，可以建立分类理论：

$$\text{PatternClassification} = \{\text{Creational}, \text{Structural}, \text{Behavioral}, \text{Concurrency}, \text{Distributed}\}$$

每种类型都有其数学特征：

- **创建型**: $f: \text{Context} \rightarrow \text{Object}$
- **结构型**: $f: \text{Object} \times \text{Object} \rightarrow \text{Structure}$
- **行为型**: $f: \text{Object} \times \text{Event} \rightarrow \text{Behavior}$
- **并发型**: $f: \text{Thread} \times \text{Resource} \rightarrow \text{Synchronization}$
- **分布式**: $f: \text{Node} \times \text{Network} \rightarrow \text{Coordination}$

### 3. 模式组合理论

模式可以组合形成更复杂的解决方案：

$$\text{PatternComposition} = \text{Pattern}_1 \circ \text{Pattern}_2 \circ \cdots \circ \text{Pattern}_n$$

组合的数学性质：

- **结合律**: $(P_1 \circ P_2) \circ P_3 = P_1 \circ (P_2 \circ P_3)$
- **交换律**: 某些情况下 $P_1 \circ P_2 = P_2 \circ P_1$
- **单位元**: 存在单位模式 $I$，使得 $P \circ I = I \circ P = P$

## 与Python编程的关联

### 1. 设计模式在Python中的实现

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, List, Any, Protocol
from dataclasses import dataclass
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
from collections import defaultdict

T = TypeVar('T')
U = TypeVar('U')

class DesignPattern(ABC):
    """设计模式的抽象基类"""
    
    @abstractmethod
    def apply(self, context: Dict[str, Any]) -> Any:
        """应用模式"""
        pass
    
    @abstractmethod
    def get_consequences(self) -> List[str]:
        """获取模式的后果"""
        pass
    
    @abstractmethod
    def get_context(self) -> Dict[str, Any]:
        """获取适用上下文"""
        pass

class PatternRegistry:
    """模式注册表"""
    
    def __init__(self):
        self._patterns: Dict[str, type[DesignPattern]] = {}
        self._categories: Dict[str, List[str]] = defaultdict(list)
    
    def register(self, name: str, pattern_class: type[DesignPattern], 
                category: str) -> None:
        """注册模式"""
        self._patterns[name] = pattern_class
        self._categories[category].append(name)
    
    def get_pattern(self, name: str) -> type[DesignPattern]:
        """获取模式"""
        return self._patterns[name]
    
    def get_patterns_by_category(self, category: str) -> List[str]:
        """按类别获取模式"""
        return self._categories[category]
    
    def list_all_patterns(self) -> Dict[str, List[str]]:
        """列出所有模式"""
        return dict(self._categories)

# 全局模式注册表
pattern_registry = PatternRegistry()

def register_pattern(name: str, category: str):
    """模式注册装饰器"""
    def decorator(pattern_class: type[DesignPattern]):
        pattern_registry.register(name, pattern_class, category)
        return pattern_class
    return decorator
```

### 2. 创建型模式的形式化实现

```python
@register_pattern("Singleton", "Creational")
class SingletonPattern(DesignPattern):
    """单例模式"""
    
    def apply(self, context: Dict[str, Any]) -> Any:
        """应用单例模式"""
        class_name = context.get('class_name', 'Singleton')
        
        class Singleton:
            _instance = None
            _lock = threading.Lock()
            
            def __new__(cls):
                if cls._instance is None:
                    with cls._lock:
                        if cls._instance is None:
                            cls._instance = super().__new__(cls)
                return cls._instance
            
            def __init__(self):
                if not hasattr(self, '_initialized'):
                    self._initialized = True
                    self._data = {}
            
            def set_data(self, key: str, value: Any) -> None:
                """设置数据"""
                self._data[key] = value
            
            def get_data(self, key: str) -> Any:
                """获取数据"""
                return self._data.get(key)
        
        # 动态设置类名
        Singleton.__name__ = class_name
        return Singleton
    
    def get_consequences(self) -> List[str]:
        return [
            "确保一个类只有一个实例",
            "提供全局访问点",
            "可能违反单一职责原则",
            "在多线程环境下需要同步"
        ]
    
    def get_context(self) -> Dict[str, Any]:
        return {
            "problem": "需要确保一个类只有一个实例",
            "solution": "私有构造函数 + 静态实例",
            "when_to_use": ["全局配置", "日志记录器", "数据库连接"]
        }

@register_pattern("FactoryMethod", "Creational")
class FactoryMethodPattern(DesignPattern):
    """工厂方法模式"""
    
    def apply(self, context: Dict[str, Any]) -> Any:
        """应用工厂方法模式"""
        product_interface = context.get('product_interface')
        concrete_products = context.get('concrete_products', [])
        
        class Creator(ABC):
            @abstractmethod
            def factory_method(self) -> product_interface:
                pass
            
            def some_operation(self) -> str:
                product = self.factory_method()
                return f"Creator: {product.operation()}"
        
        # 动态创建具体创建者
        creators = {}
        for i, product_class in enumerate(concrete_products):
            creator_name = f"ConcreteCreator{i+1}"
            
            class ConcreteCreator(Creator):
                def factory_method(self) -> product_interface:
                    return product_class()
            
            ConcreteCreator.__name__ = creator_name
            creators[creator_name] = ConcreteCreator
        
        return creators
    
    def get_consequences(self) -> List[str]:
        return [
            "避免创建者与具体产品类耦合",
            "单一职责原则",
            "开闭原则",
            "可能产生大量小类"
        ]
    
    def get_context(self) -> Dict[str, Any]:
        return {
            "problem": "需要创建对象但不确定具体类型",
            "solution": "定义创建接口，让子类决定实例化",
            "when_to_use": ["框架设计", "插件系统", "配置驱动的创建"]
        }
```

### 3. 结构型模式的形式化实现

```python
@register_pattern("Adapter", "Structural")
class AdapterPattern(DesignPattern):
    """适配器模式"""
    
    def apply(self, context: Dict[str, Any]) -> Any:
        """应用适配器模式"""
        target_interface = context.get('target_interface')
        adaptee_class = context.get('adaptee_class')
        
        class Adapter(target_interface):
            def __init__(self, adaptee: adaptee_class):
                self._adaptee = adaptee
            
            def request(self) -> str:
                """适配目标接口的方法"""
                # 调用被适配对象的方法
                return self._adaptee.specific_request()
        
        return Adapter
    
    def get_consequences(self) -> List[str]:
        return [
            "使不兼容的接口可以一起工作",
            "提高类的复用性",
            "增加系统的灵活性",
            "可能增加系统复杂度"
        ]
    
    def get_context(self) -> Dict[str, Any]:
        return {
            "problem": "需要使用现有类但接口不匹配",
            "solution": "创建适配器类转换接口",
            "when_to_use": ["集成第三方库", "遗留系统改造", "接口标准化"]
        }

@register_pattern("Decorator", "Structural")
class DecoratorPattern(DesignPattern):
    """装饰器模式"""
    
    def apply(self, context: Dict[str, Any]) -> Any:
        """应用装饰器模式"""
        component_interface = context.get('component_interface')
        decorators = context.get('decorators', [])
        
        class Decorator(component_interface):
            def __init__(self, component: component_interface):
                self._component = component
            
            def operation(self) -> str:
                return self._component.operation()
        
        # 动态创建装饰器
        created_decorators = {}
        for i, decorator_func in enumerate(decorators):
            decorator_name = f"ConcreteDecorator{i+1}"
            
            class ConcreteDecorator(Decorator):
                def operation(self) -> str:
                    # 执行装饰器逻辑
                    result = decorator_func(self._component.operation())
                    return result
            
            ConcreteDecorator.__name__ = decorator_name
            created_decorators[decorator_name] = ConcreteDecorator
        
        return created_decorators
    
    def get_consequences(self) -> List[str]:
        return [
            "比继承更灵活",
            "避免类爆炸",
            "可以动态组合功能",
            "可能产生大量小对象"
        ]
    
    def get_context(self) -> Dict[str, Any]:
        return {
            "problem": "需要动态扩展对象功能",
            "solution": "组合优于继承",
            "when_to_use": ["日志记录", "性能监控", "权限控制", "缓存"]
        }
```

### 4. 行为型模式的形式化实现

```python
@register_pattern("Observer", "Behavioral")
class ObserverPattern(DesignPattern):
    """观察者模式"""
    
    def apply(self, context: Dict[str, Any]) -> Any:
        """应用观察者模式"""
        class Subject:
            def __init__(self):
                self._observers: List[Observer] = []
                self._state = None
            
            def attach(self, observer: 'Observer') -> None:
                """添加观察者"""
                if observer not in self._observers:
                    self._observers.append(observer)
            
            def detach(self, observer: 'Observer') -> None:
                """移除观察者"""
                self._observers.remove(observer)
            
            def notify(self) -> None:
                """通知所有观察者"""
                for observer in self._observers:
                    observer.update(self._state)
            
            @property
            def state(self):
                return self._state
            
            @state.setter
            def state(self, value):
                self._state = value
                self.notify()
        
        class Observer(ABC):
            @abstractmethod
            def update(self, state: Any) -> None:
                pass
        
        return Subject, Observer
    
    def get_consequences(self) -> List[str]:
        return [
            "支持广播通信",
            "松耦合设计",
            "可能产生意外的更新",
            "观察者不知道其他观察者的存在"
        ]
    
    def get_context(self) -> Dict[str, Any]:
        return {
            "problem": "对象状态变化需要通知其他对象",
            "solution": "定义一对多依赖关系",
            "when_to_use": ["事件处理", "MVC架构", "数据绑定", "消息系统"]
        }

@register_pattern("Strategy", "Behavioral")
class StrategyPattern(DesignPattern):
    """策略模式"""
    
    def apply(self, context: Dict[str, Any]) -> Any:
        """应用策略模式"""
        strategy_interface = context.get('strategy_interface')
        strategies = context.get('strategies', [])
        
        class Context:
            def __init__(self, strategy: strategy_interface):
                self._strategy = strategy
            
            def set_strategy(self, strategy: strategy_interface) -> None:
                """设置策略"""
                self._strategy = strategy
            
            def execute_strategy(self, data: Any) -> Any:
                """执行策略"""
                return self._strategy.execute(data)
        
        # 动态创建策略
        created_strategies = {}
        for i, strategy_func in enumerate(strategies):
            strategy_name = f"ConcreteStrategy{i+1}"
            
            class ConcreteStrategy(strategy_interface):
                def execute(self, data: Any) -> Any:
                    return strategy_func(data)
            
            ConcreteStrategy.__name__ = strategy_name
            created_strategies[strategy_name] = ConcreteStrategy
        
        return Context, created_strategies
    
    def get_consequences(self) -> List[str]:
        return [
            "算法可以独立变化",
            "避免条件语句",
            "客户端必须了解所有策略",
            "可能产生大量策略类"
        ]
    
    def get_context(self) -> Dict[str, Any]:
        return {
            "problem": "需要根据条件选择不同算法",
            "solution": "封装算法族，使它们可以互换",
            "when_to_use": ["排序算法", "压缩算法", "支付方式", "验证规则"]
        }
```

## 模式分析框架

### 1. 模式复杂度分析

```python
class PatternAnalyzer:
    """模式分析器"""
    
    def __init__(self):
        self.metrics = {}
    
    def analyze_complexity(self, pattern: DesignPattern) -> Dict[str, float]:
        """分析模式复杂度"""
        # 实现复杂度分析逻辑
        return {
            "cyclomatic_complexity": 0.0,
            "coupling": 0.0,
            "cohesion": 0.0,
            "maintainability": 0.0
        }
    
    def analyze_performance(self, pattern: DesignPattern) -> Dict[str, float]:
        """分析性能影响"""
        return {
            "memory_overhead": 0.0,
            "time_overhead": 0.0,
            "scalability": 0.0
        }
    
    def compare_patterns(self, pattern1: DesignPattern, 
                        pattern2: DesignPattern) -> Dict[str, Any]:
        """比较两个模式"""
        return {
            "complexity_diff": 0.0,
            "performance_diff": 0.0,
            "applicability_diff": 0.0
        }
```

### 2. 模式选择决策树

```python
class PatternDecisionTree:
    """模式选择决策树"""
    
    def __init__(self):
        self.decision_rules = []
    
    def add_rule(self, condition: callable, pattern: str) -> None:
        """添加决策规则"""
        self.decision_rules.append((condition, pattern))
    
    def select_pattern(self, context: Dict[str, Any]) -> str:
        """选择最适合的模式"""
        for condition, pattern in self.decision_rules:
            if condition(context):
                return pattern
        return "No suitable pattern found"
    
    def get_recommendations(self, context: Dict[str, Any]) -> List[str]:
        """获取模式推荐"""
        recommendations = []
        for condition, pattern in self.decision_rules:
            if condition(context):
                recommendations.append(pattern)
        return recommendations
```

## 学习路径

1. **创建型模式** → 理解对象创建机制
2. **结构型模式** → 掌握对象组合方法
3. **行为型模式** → 学习对象交互方式
4. **并发模式** → 理解并发编程模式
5. **分布式模式** → 掌握分布式系统模式

## 下一层：架构领域

设计模式科学为架构领域提供了微观层面的设计工具，架构领域层将在此基础上建立宏观层面的系统架构理论。

---

*设计模式科学将软件设计从经验总结提升为形式化理论，为软件工程提供了严格的设计方法论。*
