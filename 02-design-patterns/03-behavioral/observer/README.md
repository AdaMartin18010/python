# Observer Pattern - 观察者模式

## 📚 概述

**观察者模式**定义对象间的一对多依赖关系，当一个对象状态改变时，所有依赖者都会自动收到通知并更新。这是实现事件系统的基础模式。

## 🎯 核心概念

### 定义

> 观察者模式定义了对象之间的一对多依赖，当主题（Subject）状态改变时，所有观察者（Observer）都会收到通知。

### 应用场景

- ✅ 事件处理系统
- ✅ MVC架构
- ✅ 发布-订阅系统
- ✅ 数据绑定
- ✅ 实时更新
- ✅ 响应式编程

### 优势与劣势

**优势**:

- ✅ 松耦合
- ✅ 动态订阅/取消订阅
- ✅ 支持广播通信
- ✅ 符合开闭原则

**劣势**:

- ⚠️ 通知顺序不可控
- ⚠️ 可能导致意外更新
- ⚠️ 内存泄漏风险
- ⚠️ 性能开销

## 💡 Python实现方式

### 1. 经典实现 ⭐⭐⭐⭐

```python
from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    """观察者接口"""
    
    @abstractmethod
    def update(self, subject: 'Subject') -> None:
        """接收更新通知"""
        pass


class Subject:
    """主题/被观察者"""
    
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._state: Any = None
    
    def attach(self, observer: Observer) -> None:
        """添加观察者"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """移除观察者"""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self) -> None:
        """通知所有观察者"""
        for observer in self._observers:
            observer.update(self)
    
    @property
    def state(self) -> Any:
        return self._state
    
    @state.setter
    def state(self, value: Any) -> None:
        self._state = value
        self.notify()  # 状态改变时通知


class ConcreteObserver(Observer):
    """具体观察者"""
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def update(self, subject: Subject) -> None:
        print(f"{self.name} received update: {subject.state}")


# 使用
subject = Subject()
observer1 = ConcreteObserver("Observer1")
observer2 = ConcreteObserver("Observer2")

subject.attach(observer1)
subject.attach(observer2)

subject.state = "New State"  # 自动通知所有观察者
```

### 2. 基于信号（Signal）⭐⭐⭐⭐⭐

```python
from typing import Callable, Any
from weakref import WeakMethod, ref


class Signal:
    """信号类（类似Django signals）"""
    
    def __init__(self) -> None:
        self._receivers: list[Any] = []
    
    def connect(self, receiver: Callable) -> None:
        """连接接收器"""
        # 使用弱引用避免内存泄漏
        if hasattr(receiver, '__self__'):
            # 绑定方法
            self._receivers.append(WeakMethod(receiver))
        else:
            # 函数
            self._receivers.append(ref(receiver))
    
    def disconnect(self, receiver: Callable) -> None:
        """断开接收器"""
        for i, r in enumerate(self._receivers):
            if r() == receiver:
                del self._receivers[i]
                break
    
    def emit(self, *args: Any, **kwargs: Any) -> None:
        """发送信号"""
        # 清理已失效的弱引用
        self._receivers = [r for r in self._receivers if r() is not None]
        
        # 调用所有接收器
        for receiver_ref in self._receivers:
            receiver = receiver_ref()
            if receiver is not None:
                receiver(*args, **kwargs)


# 使用
user_logged_in = Signal()

def send_welcome_email(user: str) -> None:
    print(f"📧 Sending welcome email to {user}")

def log_login(user: str) -> None:
    print(f"📝 Logging login for {user}")

user_logged_in.connect(send_welcome_email)
user_logged_in.connect(log_login)

user_logged_in.emit("alice@example.com")
```

### 3. Event Bus模式 ⭐⭐⭐⭐⭐

```python
from typing import Callable, Any
from collections import defaultdict


class EventBus:
    """事件总线"""
    
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
    
    def subscribe(
        self, 
        event_type: str, 
        handler: Callable
    ) -> None:
        """订阅事件"""
        self._subscribers[event_type].append(handler)
    
    def unsubscribe(
        self, 
        event_type: str, 
        handler: Callable
    ) -> None:
        """取消订阅"""
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(handler)
            except ValueError:
                pass
    
    def publish(
        self, 
        event_type: str, 
        *args: Any, 
        **kwargs: Any
    ) -> None:
        """发布事件"""
        for handler in self._subscribers.get(event_type, []):
            handler(*args, **kwargs)


# 使用
bus = EventBus()

def on_order_created(order_id: int) -> None:
    print(f"📦 Order {order_id} created")

def send_notification(order_id: int) -> None:
    print(f"🔔 Notification sent for order {order_id}")

bus.subscribe("order_created", on_order_created)
bus.subscribe("order_created", send_notification)

bus.publish("order_created", 12345)
```

## 🏗️ 现代Python实现（2025标准）

### 类型安全的观察者模式

```python
from typing import Generic, TypeVar, Protocol, Callable
from dataclasses import dataclass


T = TypeVar('T')


class Observable(Generic[T]):
    """类型安全的可观察对象"""
    
    def __init__(self, initial_value: T) -> None:
        self._value = initial_value
        self._observers: list[Callable[[T], None]] = []
    
    @property
    def value(self) -> T:
        return self._value
    
    @value.setter
    def value(self, new_value: T) -> None:
        if self._value != new_value:
            self._value = new_value
            self._notify()
    
    def subscribe(self, observer: Callable[[T], None]) -> Callable[[], None]:
        """订阅更新，返回取消订阅函数"""
        self._observers.append(observer)
        
        def unsubscribe() -> None:
            self._observers.remove(observer)
        
        return unsubscribe
    
    def _notify(self) -> None:
        """通知所有观察者"""
        for observer in self._observers:
            observer(self._value)


# 使用
count = Observable[int](0)

def on_count_changed(value: int) -> None:
    print(f"Count changed to: {value}")

# 订阅
unsubscribe = count.subscribe(on_count_changed)

count.value = 1  # 触发通知
count.value = 2  # 触发通知

# 取消订阅
unsubscribe()
count.value = 3  # 不再触发
```

### Property监听器

```python
from typing import Any, Callable


class PropertyObserver:
    """属性观察器（类似Vue.js reactive）"""
    
    def __init__(self, **kwargs: Any) -> None:
        self._data = kwargs
        self._watchers: dict[str, list[Callable]] = {}
    
    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            return super().__getattribute__(name)
        return self._data.get(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
            return
        
        old_value = self._data.get(name)
        self._data[name] = value
        
        # 触发监听器
        if name in self._watchers:
            for watcher in self._watchers[name]:
                watcher(value, old_value)
    
    def watch(
        self, 
        prop: str, 
        callback: Callable[[Any, Any], None]
    ) -> None:
        """监听属性变化"""
        if prop not in self._watchers:
            self._watchers[prop] = []
        self._watchers[prop].append(callback)


# 使用
@dataclass
class User:
    name: str
    age: int


user_data = PropertyObserver(name="Alice", age=25)

def on_age_changed(new_age: int, old_age: int) -> None:
    print(f"Age changed from {old_age} to {new_age}")

user_data.watch("age", on_age_changed)

user_data.age = 26  # 触发监听器
```

## 🔬 高级模式

### 1. 异步观察者

```python
import asyncio
from typing import Callable, Awaitable


class AsyncObservable:
    """异步观察者模式"""
    
    def __init__(self) -> None:
        self._observers: list[Callable[..., Awaitable[None]]] = []
    
    def subscribe(
        self, 
        observer: Callable[..., Awaitable[None]]
    ) -> None:
        """订阅（异步）"""
        self._observers.append(observer)
    
    async def notify(self, *args: Any, **kwargs: Any) -> None:
        """异步通知所有观察者"""
        tasks = [
            observer(*args, **kwargs) 
            for observer in self._observers
        ]
        await asyncio.gather(*tasks)


# 使用
async def async_handler_1(data: str) -> None:
    await asyncio.sleep(0.1)
    print(f"Handler 1: {data}")

async def async_handler_2(data: str) -> None:
    await asyncio.sleep(0.2)
    print(f"Handler 2: {data}")

async def main() -> None:
    observable = AsyncObservable()
    observable.subscribe(async_handler_1)
    observable.subscribe(async_handler_2)
    
    await observable.notify("Test data")

# asyncio.run(main())
```

### 2. 优先级观察者

```python
import heapq
from typing import Callable, Any


class PriorityObserver:
    """支持优先级的观察者"""
    
    def __init__(self) -> None:
        self._observers: list[tuple[int, int, Callable]] = []
        self._counter = 0  # 保证FIFO
    
    def subscribe(
        self, 
        observer: Callable, 
        priority: int = 0
    ) -> None:
        """订阅（priority越小越先执行）"""
        heapq.heappush(
            self._observers,
            (priority, self._counter, observer)
        )
        self._counter += 1
    
    def notify(self, *args: Any, **kwargs: Any) -> None:
        """按优先级通知"""
        # 创建副本避免修改原列表
        observers = sorted(self._observers)
        for _, _, observer in observers:
            observer(*args, **kwargs)
```

### 3. 过滤器观察者

```python
class FilteredObserver:
    """带过滤条件的观察者"""
    
    def __init__(self) -> None:
        self._observers: list[tuple[Callable, Callable[[Any], bool]]] = []
    
    def subscribe(
        self, 
        observer: Callable,
        filter_func: Callable[[Any], bool] | None = None
    ) -> None:
        """订阅（可选过滤器）"""
        if filter_func is None:
            filter_func = lambda x: True
        self._observers.append((observer, filter_func))
    
    def notify(self, data: Any) -> None:
        """只通知满足条件的观察者"""
        for observer, filter_func in self._observers:
            if filter_func(data):
                observer(data)


# 使用
filtered = FilteredObserver()

def on_high_value(value: int) -> None:
    print(f"High value: {value}")

def on_low_value(value: int) -> None:
    print(f"Low value: {value}")

filtered.subscribe(on_high_value, lambda x: x > 50)
filtered.subscribe(on_low_value, lambda x: x <= 50)

filtered.notify(75)  # 只触发on_high_value
filtered.notify(25)  # 只触发on_low_value
```

## 📊 实战案例

### 1. GUI事件系统

```python
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """事件类型"""
    CLICK = "click"
    HOVER = "hover"
    KEY_PRESS = "key_press"


@dataclass
class Event:
    """事件对象"""
    type: EventType
    data: Any


class Widget:
    """UI组件"""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self._event_handlers: dict[EventType, list[Callable]] = {}
    
    def on(self, event_type: EventType, handler: Callable) -> None:
        """注册事件处理器"""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
    
    def emit(self, event: Event) -> None:
        """触发事件"""
        handlers = self._event_handlers.get(event.type, [])
        for handler in handlers:
            handler(event)


# 使用
button = Widget("submit_button")

def on_click(event: Event) -> None:
    print(f"Button {event.data['button_name']} clicked!")

def log_click(event: Event) -> None:
    print(f"Logging click event...")

button.on(EventType.CLICK, on_click)
button.on(EventType.CLICK, log_click)

button.emit(Event(
    type=EventType.CLICK,
    data={"button_name": "Submit"}
))
```

### 2. 股票价格监控

```python
from typing import Protocol
from dataclasses import dataclass


@dataclass
class Stock:
    """股票"""
    symbol: str
    price: float


class StockObserver(Protocol):
    """股票观察者接口"""
    
    def on_price_changed(self, stock: Stock) -> None:
        """价格变化回调"""
        ...


class StockMarket:
    """股票市场"""
    
    def __init__(self) -> None:
        self._stocks: dict[str, Stock] = {}
        self._observers: dict[str, list[StockObserver]] = {}
    
    def register_stock(self, symbol: str, initial_price: float) -> None:
        """注册股票"""
        self._stocks[symbol] = Stock(symbol, initial_price)
        self._observers[symbol] = []
    
    def subscribe(self, symbol: str, observer: StockObserver) -> None:
        """订阅股票"""
        if symbol in self._observers:
            self._observers[symbol].append(observer)
    
    def update_price(self, symbol: str, new_price: float) -> None:
        """更新股票价格"""
        if symbol in self._stocks:
            stock = self._stocks[symbol]
            stock.price = new_price
            
            # 通知观察者
            for observer in self._observers[symbol]:
                observer.on_price_changed(stock)


class PriceAlert:
    """价格警报"""
    
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
    
    def on_price_changed(self, stock: Stock) -> None:
        if stock.price > self.threshold:
            print(f"🚨 Alert: {stock.symbol} is now ${stock.price}")


class PriceLogger:
    """价格记录器"""
    
    def on_price_changed(self, stock: Stock) -> None:
        print(f"📊 {stock.symbol}: ${stock.price}")


# 使用
market = StockMarket()
market.register_stock("AAPL", 150.0)

alert = PriceAlert(160.0)
logger = PriceLogger()

market.subscribe("AAPL", alert)
market.subscribe("AAPL", logger)

market.update_price("AAPL", 155.0)  # 触发logger
market.update_price("AAPL", 165.0)  # 触发logger和alert
```

## 🎯 最佳实践

### 1. 防止内存泄漏

```python
from weakref import WeakSet


class SafeSubject:
    """使用弱引用避免内存泄漏"""
    
    def __init__(self) -> None:
        self._observers: WeakSet[Observer] = WeakSet()
    
    def attach(self, observer: Observer) -> None:
        self._observers.add(observer)
    
    def notify(self) -> None:
        # 弱引用会自动清理已删除的观察者
        for observer in self._observers:
            observer.update(self)
```

### 2. 错误处理

```python
class RobustSubject:
    """健壮的主题（错误隔离）"""
    
    def notify(self) -> None:
        """通知（错误不传播）"""
        for observer in self._observers:
            try:
                observer.update(self)
            except Exception as e:
                print(f"Error in observer: {e}")
                # 继续通知其他观察者
```

### 3. 性能优化

```python
class OptimizedSubject:
    """优化的主题"""
    
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._notifying = False
        self._pending_changes: list[Any] = []
    
    def notify(self) -> None:
        """批量通知（防止递归）"""
        if self._notifying:
            self._pending_changes.append(self._state)
            return
        
        self._notifying = True
        try:
            for observer in self._observers:
                observer.update(self)
        finally:
            self._notifying = False
            
            # 处理待处理的变化
            if self._pending_changes:
                self._pending_changes.clear()
```

## 🔗 相关模式

- **Mediator Pattern**: 中介者协调对象通信
- **Event Sourcing**: 事件溯源
- **Pub/Sub**: 发布-订阅
- **Reactor Pattern**: 反应器模式

## 📚 参考资源

- **Design Patterns** - Gang of Four
- **Reactive Programming**: <https://reactivex.io>
- **Python signals**: <https://docs.djangoproject.com/en/stable/topics/signals/>

---

**观察者模式：让对象之间优雅地通信！** 📡
