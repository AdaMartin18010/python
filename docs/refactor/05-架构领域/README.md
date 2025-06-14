# 05-架构领域 (Architecture Domain)

## 概述

架构领域层专注于软件系统的架构设计、模式应用和架构评估。这一层涵盖了软件架构模式、设计模式、微服务架构、事件驱动架构、领域驱动设计和工作流架构等核心内容。

## 目录结构

```text
05-架构领域/
├── 01-软件架构模式/
│   ├── 01-分层架构.md
│   ├── 02-客户端-服务器架构.md
│   ├── 03-管道-过滤器架构.md
│   ├── 04-事件驱动架构.md
│   └── 05-微服务架构.md
├── 02-设计模式/
│   ├── 01-创建型模式.md
│   ├── 02-结构型模式.md
│   ├── 03-行为型模式.md
│   ├── 04-并发模式.md
│   └── 05-架构模式.md
├── 03-微服务架构/
│   ├── 01-服务拆分.md
│   ├── 02-服务通信.md
│   ├── 03-服务发现.md
│   └── 04-服务治理.md
├── 04-事件驱动架构/
│   ├── 01-事件建模.md
│   ├── 02-事件流处理.md
│   ├── 03-事件溯源.md
│   └── 04-CQRS模式.md
├── 05-领域驱动设计/
│   ├── 01-领域建模.md
│   ├── 02-限界上下文.md
│   ├── 03-聚合设计.md
│   └── 04-领域服务.md
└── 06-工作流架构/
    ├── 01-工作流引擎.md
    ├── 02-状态机.md
    ├── 03-编排与编排.md
    └── 04-工作流优化.md
```

## 核心架构

### 1. 软件架构模式

```math
\text{架构模式定义:}

\text{模式} P = (C, R, I, Q)

\text{其中:}
\begin{align}
C &= \text{组件 (Components)} \\
R &= \text{关系 (Relationships)} \\
I &= \text{接口 (Interfaces)} \\
Q &= \text{质量属性 (Quality Attributes)}
\end{align}
```

### 2. 设计模式

```math
\text{设计模式结构:}

\text{模式} D = (P, S, C, A)

\text{其中:}
\begin{align}
P &= \text{问题 (Problem)} \\
S &= \text{解决方案 (Solution)} \\
C &= \text{后果 (Consequences)} \\
A &= \text{应用场景 (Applications)}
\end{align}
```

### 3. 微服务架构

```math
\text{微服务架构模型:}

\text{系统} M = (S, G, D, C)

\text{其中:}
\begin{align}
S &= \text{服务 (Services)} \\
G &= \text{网关 (Gateway)} \\
D &= \text{数据存储 (Data Storage)} \\
C &= \text{通信 (Communication)}
\end{align}
```

## Python实现

### 1. 架构模式实现

```python
from typing import Dict, List, Set, Any, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

class ArchitectureType(Enum):
    """架构类型"""
    LAYERED = "layered"
    CLIENT_SERVER = "client_server"
    PIPE_FILTER = "pipe_filter"
    EVENT_DRIVEN = "event_driven"
    MICROSERVICES = "microservices"

@dataclass
class Component:
    """组件"""
    id: str
    name: str
    type: str
    responsibilities: List[str]
    interfaces: Dict[str, Any]
    dependencies: Set[str]

@dataclass
class ArchitecturePattern:
    """架构模式"""
    name: str
    type: ArchitectureType
    description: str
    components: List[Component]
    relationships: List[tuple]
    quality_attributes: Dict[str, float]

class LayeredArchitecture:
    """分层架构"""
    
    def __init__(self):
        self.layers: Dict[str, List[Component]] = {
            "presentation": [],
            "business": [],
            "data": []
        }
        self.current_layer = "presentation"
    
    def add_component(self, layer: str, component: Component) -> None:
        """添加组件到层"""
        if layer in self.layers:
            self.layers[layer].append(component)
    
    def get_layer_components(self, layer: str) -> List[Component]:
        """获取层的组件"""
        return self.layers.get(layer, [])
    
    def validate_dependencies(self) -> bool:
        """验证依赖关系"""
        # 检查层间依赖
        for layer_name, components in self.layers.items():
            for component in components:
                for dep in component.dependencies:
                    # 检查依赖是否在正确的层
                    if not self._is_valid_dependency(layer_name, dep):
                        return False
        return True
    
    def _is_valid_dependency(self, layer: str, dependency: str) -> bool:
        """检查依赖是否有效"""
        layer_order = ["presentation", "business", "data"]
        current_index = layer_order.index(layer)
        
        # 只能依赖下层
        for i in range(current_index + 1, len(layer_order)):
            if dependency in [comp.id for comp in self.layers[layer_order[i]]]:
                return True
        return False

class MicroservicesArchitecture:
    """微服务架构"""
    
    def __init__(self):
        self.services: Dict[str, Component] = {}
        self.gateway: Optional[Component] = None
        self.registry: Dict[str, str] = {}  # service_id -> endpoint
    
    def add_service(self, service: Component) -> None:
        """添加服务"""
        self.services[service.id] = service
        self.registry[service.id] = f"http://{service.id}.service"
    
    def set_gateway(self, gateway: Component) -> None:
        """设置网关"""
        self.gateway = gateway
    
    def route_request(self, service_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """路由请求"""
        if service_id not in self.services:
            return {"error": "Service not found"}
        
        service = self.services[service_id]
        endpoint = self.registry[service_id]
        
        # 简化的请求处理
        return {
            "service": service.name,
            "endpoint": endpoint,
            "request": request,
            "response": f"Response from {service.name}"
        }
    
    def discover_service(self, service_name: str) -> Optional[str]:
        """服务发现"""
        for service_id, service in self.services.items():
            if service.name == service_name:
                return self.registry[service_id]
        return None

class EventDrivenArchitecture:
    """事件驱动架构"""
    
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.handlers: Dict[str, List[callable]] = {}
        self.event_bus: List[Dict[str, Any]] = []
    
    def publish_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """发布事件"""
        event = {
            "id": str(uuid.uuid4()),
            "type": event_type,
            "data": data,
            "timestamp": datetime.now()
        }
        self.events.append(event)
        self.event_bus.append(event)
    
    def subscribe(self, event_type: str, handler: callable) -> None:
        """订阅事件"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def process_events(self) -> None:
        """处理事件"""
        while self.event_bus:
            event = self.event_bus.pop(0)
            event_type = event["type"]
            
            if event_type in self.handlers:
                for handler in self.handlers[event_type]:
                    handler(event)
```

### 2. 设计模式实现

```python
from typing import Dict, List, Any, Optional, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')

# 创建型模式
class Singleton:
    """单例模式"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class Factory:
    """工厂模式"""
    
    @staticmethod
    def create_product(product_type: str) -> Any:
        """创建产品"""
        if product_type == "A":
            return ProductA()
        elif product_type == "B":
            return ProductB()
        else:
            raise ValueError(f"Unknown product type: {product_type}")

class ProductA:
    def operation(self) -> str:
        return "ProductA operation"

class ProductB:
    def operation(self) -> str:
        return "ProductB operation"

# 结构型模式
class Adapter:
    """适配器模式"""
    
    def __init__(self, adaptee: Any):
        self.adaptee = adaptee
    
    def request(self) -> str:
        """适配请求"""
        return f"Adapter: {self.adaptee.specific_request()}"

class Decorator:
    """装饰器模式"""
    
    def __init__(self, component: Any):
        self.component = component
    
    def operation(self) -> str:
        return f"Decorator({self.component.operation()})"

# 行为型模式
class Observer:
    """观察者模式"""
    
    def __init__(self):
        self.observers: List[callable] = []
    
    def attach(self, observer: callable) -> None:
        """添加观察者"""
        self.observers.append(observer)
    
    def detach(self, observer: callable) -> None:
        """移除观察者"""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify(self, data: Any) -> None:
        """通知观察者"""
        for observer in self.observers:
            observer(data)

class Strategy:
    """策略模式"""
    
    def __init__(self, strategy: callable):
        self.strategy = strategy
    
    def execute(self, data: Any) -> Any:
        """执行策略"""
        return self.strategy(data)

# 并发模式
class ActiveObject:
    """主动对象模式"""
    
    def __init__(self):
        self.queue: List[tuple] = []
        self.running = True
        self.thread = threading.Thread(target=self._process_queue)
        self.thread.start()
    
    def enqueue(self, method: callable, *args, **kwargs) -> None:
        """入队方法调用"""
        self.queue.append((method, args, kwargs))
    
    def _process_queue(self) -> None:
        """处理队列"""
        while self.running:
            if self.queue:
                method, args, kwargs = self.queue.pop(0)
                method(*args, **kwargs)
            time.sleep(0.1)
    
    def stop(self) -> None:
        """停止处理"""
        self.running = False
        self.thread.join()
```

### 3. 领域驱动设计实现

```python
from typing import Dict, List, Set, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class ValueObject:
    """值对象"""
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__

@dataclass
class Entity:
    """实体"""
    id: str
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id

@dataclass
class AggregateRoot(Entity):
    """聚合根"""
    version: int = 0
    
    def increment_version(self) -> None:
        """增加版本号"""
        self.version += 1

class BoundedContext:
    """限界上下文"""
    
    def __init__(self, name: str):
        self.name = name
        self.entities: Dict[str, Entity] = {}
        self.value_objects: Dict[str, ValueObject] = {}
        self.services: Dict[str, callable] = {}
    
    def add_entity(self, entity: Entity) -> None:
        """添加实体"""
        self.entities[entity.id] = entity
    
    def add_value_object(self, name: str, value_object: ValueObject) -> None:
        """添加值对象"""
        self.value_objects[name] = value_object
    
    def add_service(self, name: str, service: callable) -> None:
        """添加服务"""
        self.services[name] = service
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """获取实体"""
        return self.entities.get(entity_id)
    
    def execute_service(self, service_name: str, *args, **kwargs) -> Any:
        """执行服务"""
        if service_name in self.services:
            return self.services[service_name](*args, **kwargs)
        raise ValueError(f"Service {service_name} not found")

# 具体领域模型
@dataclass
class Money(ValueObject):
    """货币值对象"""
    amount: float
    currency: str
    
    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

@dataclass
class Order(AggregateRoot):
    """订单聚合根"""
    customer_id: str
    items: List[Dict[str, Any]]
    total: Money
    status: str = "pending"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def add_item(self, item: Dict[str, Any]) -> None:
        """添加商品"""
        self.items.append(item)
        self._recalculate_total()
        self.increment_version()
    
    def _recalculate_total(self) -> None:
        """重新计算总额"""
        total_amount = sum(item.get('price', 0) for item in self.items)
        self.total = Money(total_amount, "USD")
    
    def confirm(self) -> None:
        """确认订单"""
        if self.status == "pending":
            self.status = "confirmed"
            self.increment_version()

class OrderService:
    """订单领域服务"""
    
    def __init__(self, order_repository: Any):
        self.order_repository = order_repository
    
    def create_order(self, customer_id: str, items: List[Dict[str, Any]]) -> Order:
        """创建订单"""
        total = Money(sum(item.get('price', 0) for item in items), "USD")
        order = Order(
            id=str(uuid.uuid4()),
            customer_id=customer_id,
            items=items,
            total=total
        )
        
        # 业务规则验证
        if not self._validate_order(order):
            raise ValueError("Invalid order")
        
        return order
    
    def _validate_order(self, order: Order) -> bool:
        """验证订单"""
        return len(order.items) > 0 and order.total.amount > 0
```

### 4. 工作流架构实现

```python
from typing import Dict, List, Set, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio

class WorkflowState(Enum):
    """工作流状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowStep:
    """工作流步骤"""
    id: str
    name: str
    action: Callable
    dependencies: Set[str]
    timeout: int = 30
    retry_count: int = 3

@dataclass
class WorkflowInstance:
    """工作流实例"""
    id: str
    workflow_id: str
    state: WorkflowState
    current_step: Optional[str]
    completed_steps: Set[str]
    failed_steps: Set[str]
    data: Dict[str, Any]

class WorkflowEngine:
    """工作流引擎"""
    
    def __init__(self):
        self.workflows: Dict[str, List[WorkflowStep]] = {}
        self.instances: Dict[str, WorkflowInstance] = {}
        self.step_results: Dict[str, Any] = {}
    
    def register_workflow(self, workflow_id: str, steps: List[WorkflowStep]) -> None:
        """注册工作流"""
        self.workflows[workflow_id] = steps
    
    def start_workflow(self, workflow_id: str, initial_data: Dict[str, Any]) -> str:
        """启动工作流"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        instance_id = str(uuid.uuid4())
        instance = WorkflowInstance(
            id=instance_id,
            workflow_id=workflow_id,
            state=WorkflowState.PENDING,
            current_step=None,
            completed_steps=set(),
            failed_steps=set(),
            data=initial_data
        )
        
        self.instances[instance_id] = instance
        return instance_id
    
    async def execute_workflow(self, instance_id: str) -> None:
        """执行工作流"""
        instance = self.instances[instance_id]
        workflow = self.workflows[instance.workflow_id]
        
        instance.state = WorkflowState.RUNNING
        
        while instance.state == WorkflowState.RUNNING:
            # 找到可执行的步骤
            executable_steps = self._find_executable_steps(instance, workflow)
            
            if not executable_steps:
                if len(instance.completed_steps) == len(workflow):
                    instance.state = WorkflowState.COMPLETED
                else:
                    instance.state = WorkflowState.FAILED
                break
            
            # 并行执行可执行的步骤
            tasks = []
            for step in executable_steps:
                task = asyncio.create_task(self._execute_step(instance, step))
                tasks.append(task)
            
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def _find_executable_steps(self, instance: WorkflowInstance, 
                              workflow: List[WorkflowStep]) -> List[WorkflowStep]:
        """找到可执行的步骤"""
        executable = []
        
        for step in workflow:
            if (step.id not in instance.completed_steps and 
                step.id not in instance.failed_steps and
                step.dependencies.issubset(instance.completed_steps)):
                executable.append(step)
        
        return executable
    
    async def _execute_step(self, instance: WorkflowInstance, step: WorkflowStep) -> None:
        """执行步骤"""
        try:
            instance.current_step = step.id
            
            # 执行步骤
            result = await asyncio.wait_for(
                asyncio.to_thread(step.action, instance.data),
                timeout=step.timeout
            )
            
            # 存储结果
            self.step_results[f"{instance.id}_{step.id}"] = result
            instance.completed_steps.add(step.id)
            instance.data.update(result)
            
        except Exception as e:
            instance.failed_steps.add(step.id)
            print(f"Step {step.id} failed: {e}")
    
    def get_workflow_status(self, instance_id: str) -> Dict[str, Any]:
        """获取工作流状态"""
        if instance_id not in self.instances:
            return {"error": "Instance not found"}
        
        instance = self.instances[instance_id]
        return {
            "instance_id": instance_id,
            "state": instance.state.value,
            "current_step": instance.current_step,
            "completed_steps": list(instance.completed_steps),
            "failed_steps": list(instance.failed_steps),
            "progress": len(instance.completed_steps) / len(self.workflows[instance.workflow_id])
        }
```

## 应用示例

```python
def demonstrate_architecture_domains():
    """演示架构领域应用"""
    
    # 1. 分层架构
    print("=== 分层架构 ===")
    layered_arch = LayeredArchitecture()
    
    # 添加组件
    ui_component = Component("ui_001", "UserInterface", "presentation", 
                           ["显示数据", "处理用户输入"], {}, set())
    business_component = Component("biz_001", "BusinessLogic", "business",
                                 ["处理业务逻辑"], {}, {"ui_001"})
    data_component = Component("data_001", "DataAccess", "data",
                             ["数据访问"], {}, {"biz_001"})
    
    layered_arch.add_component("presentation", ui_component)
    layered_arch.add_component("business", business_component)
    layered_arch.add_component("data", data_component)
    
    is_valid = layered_arch.validate_dependencies()
    print(f"分层架构依赖验证: {is_valid}")
    
    # 2. 微服务架构
    print("\n=== 微服务架构 ===")
    microservices = MicroservicesArchitecture()
    
    # 添加服务
    user_service = Component("user_svc", "UserService", "service",
                           ["用户管理"], {}, set())
    order_service = Component("order_svc", "OrderService", "service",
                            ["订单管理"], {}, {"user_svc"})
    
    microservices.add_service(user_service)
    microservices.add_service(order_service)
    
    # 设置网关
    gateway = Component("gateway", "APIGateway", "gateway",
                      ["路由", "认证"], {}, set())
    microservices.set_gateway(gateway)
    
    # 路由请求
    response = microservices.route_request("user_svc", {"action": "get_user"})
    print(f"微服务响应: {response}")
    
    # 3. 事件驱动架构
    print("\n=== 事件驱动架构 ===")
    event_arch = EventDrivenArchitecture()
    
    # 订阅事件
    def order_handler(event):
        print(f"处理订单事件: {event['data']}")
    
    def inventory_handler(event):
        print(f"处理库存事件: {event['data']}")
    
    event_arch.subscribe("order_created", order_handler)
    event_arch.subscribe("inventory_updated", inventory_handler)
    
    # 发布事件
    event_arch.publish_event("order_created", {"order_id": "123", "amount": 100})
    event_arch.publish_event("inventory_updated", {"product_id": "456", "quantity": 10})
    
    # 处理事件
    event_arch.process_events()
    
    # 4. 领域驱动设计
    print("\n=== 领域驱动设计 ===")
    order_context = BoundedContext("Order")
    
    # 创建订单
    order_service = OrderService(None)
    items = [{"name": "Product A", "price": 50}, {"name": "Product B", "price": 30}]
    order = order_service.create_order("customer_001", items)
    
    order_context.add_entity(order)
    
    # 添加值对象
    money = Money(100, "USD")
    order_context.add_value_object("total", money)
    
    print(f"订单ID: {order.id}")
    print(f"订单总额: {order.total.amount} {order.total.currency}")
    print(f"订单状态: {order.status}")
    
    # 5. 工作流架构
    print("\n=== 工作流架构 ===")
    workflow_engine = WorkflowEngine()
    
    # 定义工作流步骤
    def step1(data):
        print("执行步骤1")
        return {"step1_result": "completed"}
    
    def step2(data):
        print("执行步骤2")
        return {"step2_result": "completed"}
    
    def step3(data):
        print("执行步骤3")
        return {"step3_result": "completed"}
    
    steps = [
        WorkflowStep("step1", "步骤1", step1, set()),
        WorkflowStep("step2", "步骤2", step2, {"step1"}),
        WorkflowStep("step3", "步骤3", step3, {"step1", "step2"})
    ]
    
    workflow_engine.register_workflow("simple_workflow", steps)
    
    # 启动工作流
    instance_id = workflow_engine.start_workflow("simple_workflow", {"initial": "data"})
    
    # 执行工作流
    asyncio.run(workflow_engine.execute_workflow(instance_id))
    
    # 获取状态
    status = workflow_engine.get_workflow_status(instance_id)
    print(f"工作流状态: {status}")

if __name__ == "__main__":
    demonstrate_architecture_domains()
```

## 总结

架构领域层提供了软件系统设计的核心理论和方法：

1. **软件架构模式**: 提供了系统级的设计模式
2. **设计模式**: 提供了组件级的设计模式
3. **微服务架构**: 提供了分布式系统的架构方法
4. **事件驱动架构**: 提供了松耦合的系统设计方法
5. **领域驱动设计**: 提供了业务驱动的设计方法
6. **工作流架构**: 提供了流程驱动的系统设计方法

这些架构方法为构建高质量、可维护、可扩展的软件系统提供了理论基础和实践指导。

---

**相关链接**:

- [03-具体科学](../03-具体科学/README.md) - 软件工程理论
- [04-行业领域](../04-行业领域/README.md) - 行业应用
- [06-组件算法](../06-组件算法/README.md) - 组件算法

**更新时间**: 2024年12月
**版本**: 1.0.0
