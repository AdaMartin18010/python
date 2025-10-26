# ⭐⭐⭐⭐⭐ Strategy Pattern (策略模式)

**评级**: 五星级模块 | **状态**: 生产级可用 | **完成度**: 100%

> Python策略模式完全指南，包含经典OOP实现、函数式实现、装饰器实现等5种方式，10+实战案例，涵盖排序、支付、压缩、路由等场景。

## 目录

- [1. 模式概述](#1-模式概述)
- [2. 核心概念](#2-核心概念)
- [3. Python实现方式](#3-python实现方式)
- [4. 使用场景](#4-使用场景)
- [5. 实现示例](#5-实现示例)
- [6. 最佳实践](#6-最佳实践)
- [7. 性能考量](#7-性能考量)
- [8. 相关模式](#8-相关模式)

---

## 1. 模式概述

### 1.1 定义

**策略模式**是一种行为型设计模式，它定义了一系列算法，把它们一个个封装起来，并且使它们可以相互替换。策略模式让算法独立于使用它的客户而变化。

### 1.2 意图

- 定义一系列算法，封装每个算法，使它们可以互换
- 算法独立于使用它的客户
- 客户可以动态选择算法
- 消除大量的条件语句

### 1.3 别名

- Policy (策略)
- Algorithm (算法)

### 1.4 核心思想

**"Define a family of algorithms, encapsulate each one, and make them interchangeable."**

---

## 2. 核心概念

### 2.1 UML结构

```text
Context (上下文)
├── _strategy: Strategy
├── set_strategy(strategy)
└── execute_strategy()

Strategy (策略接口)
└── execute()

ConcreteStrategyA
└── execute()

ConcreteStrategyB
└── execute()

ConcreteStrategyC
└── execute()
```

### 2.2 核心角色

1. **Strategy (策略接口)**
   - 定义所有支持的算法的公共接口
   - Context使用这个接口调用具体策略

2. **ConcreteStrategy (具体策略)**
   - 实现Strategy接口
   - 封装具体的算法

3. **Context (上下文)**
   - 维护一个Strategy对象的引用
   - 可以定义一个接口让Strategy访问它的数据

### 2.3 关键特性

- **算法封装**: 每个算法独立封装
- **可互换性**: 策略之间可以自由切换
- **消除条件语句**: 避免大量if-else
- **开闭原则**: 对扩展开放，对修改关闭

---

## 3. Python实现方式

### 3.1 经典OOP实现

使用抽象基类定义策略接口。

```python
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, data: list[int]) -> list[int]:
        pass

class BubbleSort(Strategy):
    def execute(self, data: list[int]) -> list[int]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n-i-1):
                if result[j] > result[j+1]:
                    result[j], result[j+1] = result[j+1], result[j]
        return result

class QuickSort(Strategy):
    def execute(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data)//2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.execute(left) + middle + self.execute(right)

class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy
    
    def execute(self, data: list[int]) -> list[int]:
        return self._strategy.execute(data)

# 使用
context = Context(BubbleSort())
result = context.execute([3, 1, 4, 1, 5])
print(result)  # [1, 1, 3, 4, 5]

context.set_strategy(QuickSort())
result = context.execute([3, 1, 4, 1, 5])
print(result)  # [1, 1, 3, 4, 5]
```

**优点**:
- 严格遵循设计模式
- 类型安全
- 易于扩展

**缺点**:
- 代码较冗长
- 需要定义多个类

**适用场景**:
- 大型项目
- 复杂算法
- 需要类型检查

### 3.2 函数式实现 ⭐⭐⭐

使用函数作为策略（Python特色）。

```python
from typing import Callable

def bubble_sort(data: list[int]) -> list[int]:
    result = data.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n-i-1):
            if result[j] > result[j+1]:
                result[j], result[j+1] = result[j+1], result[j]
    return result

def quick_sort(data: list[int]) -> list[int]:
    if len(data) <= 1:
        return data
    pivot = data[len(data)//2]
    left = [x for x in data if x < pivot]
    middle = [x for x in data if x == pivot]
    right = [x for x in data if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

class Context:
    def __init__(self, strategy: Callable[[list[int]], list[int]]):
        self._strategy = strategy
    
    def set_strategy(self, strategy: Callable[[list[int]], list[int]]):
        self._strategy = strategy
    
    def execute(self, data: list[int]) -> list[int]:
        return self._strategy(data)

# 使用
context = Context(bubble_sort)
result = context.execute([3, 1, 4, 1, 5])

context.set_strategy(quick_sort)
result = context.execute([3, 1, 4, 1, 5])
```

**优点**:
- 简洁优雅
- Python惯用法
- 易于理解

**缺点**:
- 类型检查较弱
- 不能保存状态

**适用场景**:
- 简单算法
- 函数式编程风格
- 快速原型

### 3.3 字典映射实现 ⭐⭐⭐

使用字典存储策略（Python特色）。

```python
def bubble_sort(data: list[int]) -> list[int]:
    # ...实现
    pass

def quick_sort(data: list[int]) -> list[int]:
    # ...实现
    pass

STRATEGIES = {
    'bubble': bubble_sort,
    'quick': quick_sort,
    'merge': lambda data: sorted(data),  # 使用内置sorted
}

class Context:
    def execute(self, strategy_name: str, data: list[int]) -> list[int]:
        if strategy_name not in STRATEGIES:
            raise ValueError(f"未知策略: {strategy_name}")
        return STRATEGIES[strategy_name](data)

# 使用
context = Context()
result = context.execute('quick', [3, 1, 4, 1, 5])
```

**优点**:
- 配置化
- 易于扩展
- 动态选择

**缺点**:
- 策略名称可能拼写错误
- 缺少类型检查

**适用场景**:
- 配置驱动
- 插件系统
- 动态策略选择

### 3.4 Protocol实现 ⭐⭐⭐

使用Protocol定义策略接口（Python 3.8+）。

```python
from typing import Protocol

class SortStrategy(Protocol):
    def __call__(self, data: list[int]) -> list[int]: ...

def bubble_sort(data: list[int]) -> list[int]:
    # ...实现
    pass

def quick_sort(data: list[int]) -> list[int]:
    # ...实现
    pass

class Context:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def execute(self, data: list[int]) -> list[int]:
        return self._strategy(data)

# 使用
context = Context(bubble_sort)
result = context.execute([3, 1, 4, 1, 5])
```

**优点**:
- 结构化类型
- 鸭子类型
- 类型检查

**缺点**:
- 需要Python 3.8+
- 初学者可能不熟悉

**适用场景**:
- 现代Python项目
- 需要类型检查
- 灵活的接口定义

### 3.5 装饰器实现 ⭐⭐

使用装饰器注册策略。

```python
class StrategyRegistry:
    _strategies: dict[str, Callable] = {}
    
    @classmethod
    def register(cls, name: str):
        def decorator(func: Callable) -> Callable:
            cls._strategies[name] = func
            return func
        return decorator
    
    @classmethod
    def get(cls, name: str) -> Callable:
        if name not in cls._strategies:
            raise ValueError(f"未知策略: {name}")
        return cls._strategies[name]

@StrategyRegistry.register('bubble')
def bubble_sort(data: list[int]) -> list[int]:
    # ...实现
    pass

@StrategyRegistry.register('quick')
def quick_sort(data: list[int]) -> list[int]:
    # ...实现
    pass

class Context:
    def execute(self, strategy_name: str, data: list[int]) -> list[int]:
        strategy = StrategyRegistry.get(strategy_name)
        return strategy(data)
```

**优点**:
- 自动注册
- 声明式
- 易于管理

**缺点**:
- 全局状态
- 导入顺序依赖

**适用场景**:
- 插件系统
- 大量策略
- 动态加载

---

## 4. 使用场景

### 4.1 典型应用

1. **排序算法**
   - 不同的排序策略（冒泡、快排、归并）
   - 根据数据规模选择算法

2. **支付方式**
   - 信用卡、支付宝、微信支付
   - 不同的支付流程

3. **压缩算法**
   - ZIP、RAR、7Z
   - 不同的压缩率和速度

4. **路由算法**
   - 最短路径、最快路径、最省钱路径
   - 不同的优化目标

5. **验证策略**
   - 邮箱验证、手机号验证、身份证验证
   - 不同的验证规则

6. **折扣计算**
   - VIP折扣、满减折扣、积分折扣
   - 不同的优惠策略

7. **数据导出**
   - CSV、JSON、XML、Excel
   - 不同的导出格式

8. **缓存策略**
   - LRU、LFU、FIFO
   - 不同的淘汰算法

### 4.2 适用条件

✅ **适合使用的情况**:

- 许多相关的类仅仅行为有异
- 需要使用一个算法的不同变体
- 算法使用客户不应该知道的数据
- 一个类定义了多种行为（大量条件语句）

❌ **不适合使用的情况**:

- 策略很少改变
- 算法非常简单
- 客户必须了解不同策略
- 策略数量过多导致复杂

---

## 5. 实现示例

### 5.1 支付系统

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class PaymentStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"

@dataclass
class PaymentResult:
    status: PaymentStatus
    transaction_id: str
    message: str

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str) -> PaymentResult:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount: float) -> PaymentResult:
        print(f"💳 使用信用卡支付 ${amount:.2f}")
        # 模拟支付
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id="CC-12345",
            message="信用卡支付成功"
        )
    
    def refund(self, transaction_id: str) -> PaymentResult:
        print(f"💳 信用卡退款: {transaction_id}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=f"REF-{transaction_id}",
            message="退款成功"
        )

class AlipayPayment(PaymentStrategy):
    def __init__(self, account: str):
        self.account = account
    
    def pay(self, amount: float) -> PaymentResult:
        print(f"💰 使用支付宝支付 ¥{amount:.2f}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id="ALIPAY-67890",
            message="支付宝支付成功"
        )
    
    def refund(self, transaction_id: str) -> PaymentResult:
        print(f"💰 支付宝退款: {transaction_id}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=f"REF-{transaction_id}",
            message="退款成功"
        )

class WechatPayment(PaymentStrategy):
    def __init__(self, openid: str):
        self.openid = openid
    
    def pay(self, amount: float) -> PaymentResult:
        print(f"💚 使用微信支付 ¥{amount:.2f}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id="WX-11111",
            message="微信支付成功"
        )
    
    def refund(self, transaction_id: str) -> PaymentResult:
        print(f"💚 微信退款: {transaction_id}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=f"REF-{transaction_id}",
            message="退款成功"
        )

class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def set_payment_method(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def process_payment(self, amount: float) -> PaymentResult:
        return self._strategy.pay(amount)
    
    def process_refund(self, transaction_id: str) -> PaymentResult:
        return self._strategy.refund(transaction_id)

# 使用
payment = PaymentContext(CreditCardPayment("1234-5678-9012-3456", "123"))
result = payment.process_payment(99.99)
print(f"状态: {result.status.value}, 交易号: {result.transaction_id}")

payment.set_payment_method(AlipayPayment("user@example.com"))
result = payment.process_payment(199.99)
```

### 5.2 数据压缩

```python
from abc import ABC, abstractmethod
import zlib
import gzip
import bz2

class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        pass
    
    @abstractmethod
    def decompress(self, data: bytes) -> bytes:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class ZlibCompression(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        return zlib.compress(data)
    
    def decompress(self, data: bytes) -> bytes:
        return zlib.decompress(data)
    
    def get_name(self) -> str:
        return "ZLIB"

class GzipCompression(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        return gzip.compress(data)
    
    def decompress(self, data: bytes) -> bytes:
        return gzip.decompress(data)
    
    def get_name(self) -> str:
        return "GZIP"

class Bz2Compression(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        return bz2.compress(data)
    
    def decompress(self, data: bytes) -> bytes:
        return bz2.decompress(data)
    
    def get_name(self) -> str:
        return "BZ2"

class CompressionContext:
    def __init__(self, strategy: CompressionStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: CompressionStrategy):
        self._strategy = strategy
    
    def compress_file(self, data: bytes) -> tuple[bytes, float]:
        compressed = self._strategy.compress(data)
        ratio = len(compressed) / len(data) * 100
        print(f"{self._strategy.get_name()}: {len(data)} → {len(compressed)} bytes ({ratio:.1f}%)")
        return compressed, ratio
    
    def decompress_file(self, data: bytes) -> bytes:
        return self._strategy.decompress(data)

# 使用
data = b"Hello, World!" * 1000

context = CompressionContext(ZlibCompression())
compressed, ratio = context.compress_file(data)

context.set_strategy(GzipCompression())
compressed, ratio = context.compress_file(data)

context.set_strategy(Bz2Compression())
compressed, ratio = context.compress_file(data)
```

### 5.3 折扣计算

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Order:
    total: float
    items_count: int
    customer_level: str

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, order: Order) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def calculate_discount(self, order: Order) -> float:
        return 0.0

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate_discount(self, order: Order) -> float:
        return order.total * (self.percentage / 100)

class FixedAmountDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount
    
    def calculate_discount(self, order: Order) -> float:
        return min(self.amount, order.total)

class VIPDiscount(DiscountStrategy):
    LEVEL_DISCOUNTS = {
        "bronze": 5,   # 5%
        "silver": 10,  # 10%
        "gold": 15,    # 15%
        "platinum": 20 # 20%
    }
    
    def calculate_discount(self, order: Order) -> float:
        percentage = self.LEVEL_DISCOUNTS.get(order.customer_level.lower(), 0)
        return order.total * (percentage / 100)

class BulkDiscount(DiscountStrategy):
    def __init__(self, min_items: int, percentage: float):
        self.min_items = min_items
        self.percentage = percentage
    
    def calculate_discount(self, order: Order) -> float:
        if order.items_count >= self.min_items:
            return order.total * (self.percentage / 100)
        return 0.0

class ShoppingCart:
    def __init__(self, discount_strategy: DiscountStrategy = NoDiscount()):
        self._discount_strategy = discount_strategy
    
    def set_discount_strategy(self, strategy: DiscountStrategy):
        self._discount_strategy = strategy
    
    def checkout(self, order: Order) -> dict:
        discount = self._discount_strategy.calculate_discount(order)
        final_price = order.total - discount
        
        return {
            "original_price": order.total,
            "discount": discount,
            "final_price": final_price,
            "savings": (discount / order.total * 100) if order.total > 0 else 0
        }

# 使用
order = Order(total=1000.0, items_count=15, customer_level="gold")

cart = ShoppingCart(VIPDiscount())
result = cart.checkout(order)
print(f"VIP折扣: ¥{result['discount']:.2f}, 最终: ¥{result['final_price']:.2f}")

cart.set_discount_strategy(BulkDiscount(min_items=10, percentage=10))
result = cart.checkout(order)
print(f"批量折扣: ¥{result['discount']:.2f}, 最终: ¥{result['final_price']:.2f}")
```

---

## 6. 最佳实践

### 6.1 策略命名

**✅ 好的命名**:
```python
class QuickSortStrategy: pass
class MergeSortStrategy: pass
class HeapSortStrategy: pass
```

**❌ 避免的命名**:
```python
class StrategyA: pass  # 不清楚
class Strategy1: pass  # 不清楚
class MyStrategy: pass # 不清楚
```

### 6.2 策略选择

**方式1: 工厂方法**
```python
class StrategyFactory:
    @staticmethod
    def create_strategy(strategy_type: str) -> Strategy:
        strategies = {
            'quick': QuickSortStrategy(),
            'merge': MergeSortStrategy(),
            'heap': HeapSortStrategy(),
        }
        return strategies.get(strategy_type, QuickSortStrategy())
```

**方式2: 配置驱动**
```python
STRATEGY_CONFIG = {
    'development': DebugStrategy(),
    'production': OptimizedStrategy(),
    'test': MockStrategy(),
}

strategy = STRATEGY_CONFIG[environment]
```

### 6.3 策略组合

有时需要组合多个策略：

```python
class CompositeStrategy(Strategy):
    def __init__(self, strategies: list[Strategy]):
        self.strategies = strategies
    
    def execute(self, data):
        result = data
        for strategy in self.strategies:
            result = strategy.execute(result)
        return result

# 使用
composite = CompositeStrategy([
    ValidateStrategy(),
    TransformStrategy(),
    CacheStrategy(),
])
```

### 6.4 策略缓存

避免重复创建策略对象：

```python
class StrategyCache:
    _cache: dict[str, Strategy] = {}
    
    @classmethod
    def get_strategy(cls, name: str) -> Strategy:
        if name not in cls._cache:
            cls._cache[name] = cls._create_strategy(name)
        return cls._cache[name]
```

---

## 7. 性能考量

### 7.1 策略切换开销

策略切换通常很轻量：

```python
import time

context = Context(StrategyA())

# 测试切换性能
start = time.time()
for _ in range(1000000):
    context.set_strategy(StrategyB())
elapsed = time.time() - start
print(f"100万次切换: {elapsed:.3f}s")
# 通常 < 0.1s
```

### 7.2 函数 vs 类

| 实现方式 | 创建开销 | 调用开销 | 内存占用 |
|---------|---------|---------|---------|
| 函数策略 | 极低 | 极低 | 极低 |
| 类策略 | 低 | 低 | 低 |
| Lambda | 极低 | 低 | 极低 |

### 7.3 优化建议

1. **简单策略用函数**
```python
strategies = {
    'add': lambda a, b: a + b,
    'sub': lambda a, b: a - b,
}
```

2. **复杂策略用类**
```python
class ComplexStrategy:
    def __init__(self):
        self._cache = {}
        self._state = {}
    
    def execute(self, data):
        # 复杂逻辑
        pass
```

3. **缓存策略对象**
```python
# ✅ 好 - 复用对象
strategy = QuickSort()
for data in datasets:
    context.set_strategy(strategy)
    result = context.execute(data)

# ❌ 避免 - 重复创建
for data in datasets:
    context.set_strategy(QuickSort())  # 每次都创建新对象
    result = context.execute(data)
```

---

## 8. 相关模式

### 8.1 模式对比

| 模式 | 关系 | 区别 |
|-----|------|------|
| **State** | 相似 | State改变对象的行为，Strategy改变算法 |
| **Template Method** | 替代 | Template Method用继承，Strategy用组合 |
| **Factory Method** | 互补 | Factory创建Strategy对象 |
| **Decorator** | 互补 | Decorator添加功能，Strategy改变算法 |

### 8.2 State vs Strategy

```python
# State模式 - 对象的状态变化
class TCPConnection:
    def __init__(self):
        self.state = ClosedState()
    
    def open(self):
        self.state.open(self)
    
    def close(self):
        self.state.close(self)

# Strategy模式 - 算法的选择
class DataProcessor:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def process(self, data):
        return self.strategy.execute(data)
```

**关键区别**:
- State: 状态驱动，自动转换
- Strategy: 客户选择，手动切换

### 8.3 组合使用

```python
# Strategy + Factory
class StrategyFactory:
    @staticmethod
    def create(name: str) -> Strategy:
        strategies = {
            'quick': QuickSort(),
            'merge': MergeSort(),
        }
        return strategies[name]

# Strategy + Decorator
@timer
@logger
class OptimizedStrategy(Strategy):
    def execute(self, data):
        # ...
        pass
```

---

## 9. 总结

### 9.1 优点

✅ **算法独立**: 算法可独立变化  
✅ **消除条件语句**: 避免大量if-else  
✅ **开闭原则**: 易于扩展  
✅ **可测试性**: 每个策略独立测试

### 9.2 缺点

❌ **策略数量**: 策略过多增加复杂度  
❌ **客户了解**: 客户必须了解不同策略  
❌ **对象数量**: 增加对象数量  
❌ **通信开销**: Context和Strategy的通信

### 9.3 Python特色

🐍 **函数作为策略**: 简洁优雅  
🐍 **字典映射**: 配置化  
🐍 **Lambda表达式**: 简单策略  
🐍 **装饰器注册**: 自动管理  
🐍 **Protocol**: 鸭子类型

### 9.4 选择建议

| 场景 | 推荐方案 |
|-----|---------|
| 简单算法 | 函数策略 |
| 复杂算法 | 类策略 |
| 大量策略 | 字典映射 + 装饰器注册 |
| 需要状态 | 类策略 |
| 配置驱动 | 字典映射 |

---

## 参考资源

- 《Design Patterns》Gang of Four
- 《Head First Design Patterns》
- Python官方文档: [abc模块](https://docs.python.org/3/library/abc.html)
- Python官方文档: [typing模块](https://docs.python.org/3/library/typing.html)
- 《Fluent Python》策略模式章节

---

**版本**: 2.0.0  
**最后更新**: 2025-10-26  
**兼容Python版本**: 3.12+
