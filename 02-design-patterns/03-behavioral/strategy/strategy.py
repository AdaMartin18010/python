"""
Strategy Pattern - 策略模式完整实现

提供5种Python策略模式实现方式：
1. 经典OOP实现
2. 函数式实现
3. 字典映射实现
4. Protocol实现
5. 装饰器注册实现
"""

from abc import ABC, abstractmethod
from typing import Callable, Protocol, Any, TypeVar
from dataclasses import dataclass
from enum import Enum
import time

T = TypeVar('T')

# ============================================================================
# 1. 经典OOP实现 - 遵循GoF设计模式
# ============================================================================


class Strategy(ABC):
    """策略接口"""
    
    @abstractmethod
    def execute(self, data: list[int]) -> list[int]:
        """执行策略算法"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取策略名称"""
        pass


class BubbleSortStrategy(Strategy):
    """冒泡排序策略"""
    
    def execute(self, data: list[int]) -> list[int]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n-i-1):
                if result[j] > result[j+1]:
                    result[j], result[j+1] = result[j+1], result[j]
        return result
    
    def get_name(self) -> str:
        return "Bubble Sort"


class QuickSortStrategy(Strategy):
    """快速排序策略"""
    
    def execute(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data)//2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.execute(left) + middle + self.execute(right)
    
    def get_name(self) -> str:
        return "Quick Sort"


class MergeSortStrategy(Strategy):
    """归并排序策略"""
    
    def execute(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self.execute(data[:mid])
        right = self.execute(data[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: list[int], right: list[int]) -> list[int]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def get_name(self) -> str:
        return "Merge Sort"


class SortContext:
    """排序上下文"""
    
    def __init__(self, strategy: Strategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: Strategy):
        """设置策略"""
        self._strategy = strategy
    
    def sort(self, data: list[int]) -> list[int]:
        """执行排序"""
        print(f"使用策略: {self._strategy.get_name()}")
        start = time.perf_counter()
        result = self._strategy.execute(data)
        elapsed = time.perf_counter() - start
        print(f"耗时: {elapsed*1000:.3f}ms")
        return result


# ============================================================================
# 2. 函数式实现 - Python特色
# ============================================================================


def bubble_sort(data: list[int]) -> list[int]:
    """冒泡排序"""
    result = data.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n-i-1):
            if result[j] > result[j+1]:
                result[j], result[j+1] = result[j+1], result[j]
    return result


def quick_sort(data: list[int]) -> list[int]:
    """快速排序"""
    if len(data) <= 1:
        return data
    pivot = data[len(data)//2]
    left = [x for x in data if x < pivot]
    middle = [x for x in data if x == pivot]
    right = [x for x in data if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def python_sort(data: list[int]) -> list[int]:
    """Python内置排序"""
    return sorted(data)


class FunctionalContext:
    """函数式策略上下文"""
    
    def __init__(self, strategy: Callable[[list[int]], list[int]]):
        self._strategy = strategy
    
    def set_strategy(self, strategy: Callable[[list[int]], list[int]]):
        self._strategy = strategy
    
    def sort(self, data: list[int]) -> list[int]:
        return self._strategy(data)


# ============================================================================
# 3. 字典映射实现 - 配置化
# ============================================================================


SORT_STRATEGIES = {
    'bubble': bubble_sort,
    'quick': quick_sort,
    'python': python_sort,
    'merge': lambda data: sorted(data),  # 使用内置sorted
}


class DictContext:
    """字典映射策略上下文"""
    
    def sort(self, strategy_name: str, data: list[int]) -> list[int]:
        if strategy_name not in SORT_STRATEGIES:
            raise ValueError(
                f"未知策略: {strategy_name}. "
                f"可用策略: {list(SORT_STRATEGIES.keys())}"
            )
        return SORT_STRATEGIES[strategy_name](data)


# ============================================================================
# 4. Protocol实现 - 结构化类型
# ============================================================================


class SortStrategyProtocol(Protocol):
    """排序策略协议"""
    def __call__(self, data: list[int]) -> list[int]: ...


class ProtocolContext:
    """Protocol策略上下文"""
    
    def __init__(self, strategy: SortStrategyProtocol):
        self._strategy = strategy
    
    def sort(self, data: list[int]) -> list[int]:
        return self._strategy(data)


# ============================================================================
# 5. 装饰器注册实现 - 自动管理
# ============================================================================


class StrategyRegistry:
    """策略注册表"""
    _strategies: dict[str, Callable] = {}
    
    @classmethod
    def register(cls, name: str):
        """注册策略装饰器"""
        def decorator(func: Callable) -> Callable:
            cls._strategies[name] = func
            return func
        return decorator
    
    @classmethod
    def get(cls, name: str) -> Callable:
        """获取策略"""
        if name not in cls._strategies:
            raise ValueError(
                f"未注册策略: {name}. "
                f"可用策略: {list(cls._strategies.keys())}"
            )
        return cls._strategies[name]
    
    @classmethod
    def list_strategies(cls) -> list[str]:
        """列出所有策略"""
        return list(cls._strategies.keys())


@StrategyRegistry.register('bubble')
def registry_bubble_sort(data: list[int]) -> list[int]:
    return bubble_sort(data)


@StrategyRegistry.register('quick')
def registry_quick_sort(data: list[int]) -> list[int]:
    return quick_sort(data)


@StrategyRegistry.register('python')
def registry_python_sort(data: list[int]) -> list[int]:
    return python_sort(data)


class RegistryContext:
    """注册表策略上下文"""
    
    def sort(self, strategy_name: str, data: list[int]) -> list[int]:
        strategy = StrategyRegistry.get(strategy_name)
        return strategy(data)


# ============================================================================
# 实战案例1: 支付系统
# ============================================================================


class PaymentStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


@dataclass
class PaymentResult:
    status: PaymentStatus
    transaction_id: str
    message: str
    amount: float


class PaymentStrategy(ABC):
    """支付策略接口"""
    
    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass


class CreditCardPayment(PaymentStrategy):
    """信用卡支付"""
    
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount: float) -> PaymentResult:
        print(f"💳 信用卡支付 ${amount:.2f}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id="CC-12345",
            message="信用卡支付成功",
            amount=amount
        )
    
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        print(f"💳 信用卡退款 ${amount:.2f}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=f"REF-{transaction_id}",
            message="退款成功",
            amount=amount
        )
    
    def get_name(self) -> str:
        return "信用卡"


class AlipayPayment(PaymentStrategy):
    """支付宝支付"""
    
    def __init__(self, account: str):
        self.account = account
    
    def pay(self, amount: float) -> PaymentResult:
        print(f"💰 支付宝支付 ¥{amount:.2f}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id="ALIPAY-67890",
            message="支付宝支付成功",
            amount=amount
        )
    
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        print(f"💰 支付宝退款 ¥{amount:.2f}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=f"REF-{transaction_id}",
            message="退款成功",
            amount=amount
        )
    
    def get_name(self) -> str:
        return "支付宝"


class WechatPayment(PaymentStrategy):
    """微信支付"""
    
    def __init__(self, openid: str):
        self.openid = openid
    
    def pay(self, amount: float) -> PaymentResult:
        print(f"💚 微信支付 ¥{amount:.2f}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id="WX-11111",
            message="微信支付成功",
            amount=amount
        )
    
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        print(f"💚 微信退款 ¥{amount:.2f}")
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=f"REF-{transaction_id}",
            message="退款成功",
            amount=amount
        )
    
    def get_name(self) -> str:
        return "微信支付"


class PaymentContext:
    """支付上下文"""
    
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def set_payment_method(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def process_payment(self, amount: float) -> PaymentResult:
        print(f"选择支付方式: {self._strategy.get_name()}")
        return self._strategy.pay(amount)
    
    def process_refund(self, transaction_id: str, amount: float) -> PaymentResult:
        return self._strategy.refund(transaction_id, amount)


# ============================================================================
# 实战案例2: 折扣计算
# ============================================================================


@dataclass
class Order:
    total: float
    items_count: int
    customer_level: str


class DiscountStrategy(ABC):
    """折扣策略接口"""
    
    @abstractmethod
    def calculate_discount(self, order: Order) -> float:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass


class NoDiscount(DiscountStrategy):
    """无折扣"""
    
    def calculate_discount(self, order: Order) -> float:
        return 0.0
    
    def get_name(self) -> str:
        return "无折扣"


class PercentageDiscount(DiscountStrategy):
    """百分比折扣"""
    
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate_discount(self, order: Order) -> float:
        return order.total * (self.percentage / 100)
    
    def get_name(self) -> str:
        return f"{self.percentage}%折扣"


class VIPDiscount(DiscountStrategy):
    """VIP折扣"""
    
    LEVEL_DISCOUNTS = {
        "bronze": 5,
        "silver": 10,
        "gold": 15,
        "platinum": 20
    }
    
    def calculate_discount(self, order: Order) -> float:
        percentage = self.LEVEL_DISCOUNTS.get(order.customer_level.lower(), 0)
        return order.total * (percentage / 100)
    
    def get_name(self) -> str:
        return "VIP折扣"


class BulkDiscount(DiscountStrategy):
    """批量折扣"""
    
    def __init__(self, min_items: int, percentage: float):
        self.min_items = min_items
        self.percentage = percentage
    
    def calculate_discount(self, order: Order) -> float:
        if order.items_count >= self.min_items:
            return order.total * (self.percentage / 100)
        return 0.0
    
    def get_name(self) -> str:
        return f"批量折扣({self.min_items}+件)"


class ShoppingCart:
    """购物车"""
    
    def __init__(self, discount_strategy: DiscountStrategy = None):
        self._discount_strategy = discount_strategy or NoDiscount()
    
    def set_discount_strategy(self, strategy: DiscountStrategy):
        self._discount_strategy = strategy
    
    def checkout(self, order: Order) -> dict[str, float]:
        discount = self._discount_strategy.calculate_discount(order)
        final_price = order.total - discount
        
        print(f"折扣策略: {self._discount_strategy.get_name()}")
        print(f"原价: ¥{order.total:.2f}")
        print(f"折扣: ¥{discount:.2f}")
        print(f"实付: ¥{final_price:.2f}")
        
        return {
            "original_price": order.total,
            "discount": discount,
            "final_price": final_price,
            "savings_percentage": (discount / order.total * 100) if order.total > 0 else 0
        }


# ============================================================================
# 对外接口
# ============================================================================

__all__ = [
    # 经典OOP
    "Strategy",
    "BubbleSortStrategy",
    "QuickSortStrategy",
    "MergeSortStrategy",
    "SortContext",
    # 函数式
    "bubble_sort",
    "quick_sort",
    "python_sort",
    "FunctionalContext",
    # 字典映射
    "SORT_STRATEGIES",
    "DictContext",
    # Protocol
    "SortStrategyProtocol",
    "ProtocolContext",
    # 注册表
    "StrategyRegistry",
    "RegistryContext",
    # 支付系统
    "PaymentStrategy",
    "CreditCardPayment",
    "AlipayPayment",
    "WechatPayment",
    "PaymentContext",
    "PaymentStatus",
    "PaymentResult",
    # 折扣计算
    "Order",
    "DiscountStrategy",
    "NoDiscount",
    "PercentageDiscount",
    "VIPDiscount",
    "BulkDiscount",
    "ShoppingCart",
]


if __name__ == "__main__":
    print("=" * 70)
    print("Strategy Pattern - 演示")
    print("=" * 70)
    
    # 1. 经典OOP实现
    print("\n1️⃣  经典OOP实现:")
    data = [64, 34, 25, 12, 22, 11, 90]
    context = SortContext(QuickSortStrategy())
    result = context.sort(data)
    print(f"   结果: {result}\n")
    
    # 2. 函数式实现
    print("2️⃣  函数式实现:")
    func_context = FunctionalContext(quick_sort)
    result = func_context.sort(data)
    print(f"   结果: {result}\n")
    
    # 3. 字典映射
    print("3️⃣  字典映射:")
    dict_context = DictContext()
    result = dict_context.sort('quick', data)
    print(f"   结果: {result}\n")
    
    # 4. 注册表
    print("4️⃣  注册表实现:")
    print(f"   可用策略: {StrategyRegistry.list_strategies()}")
    registry_context = RegistryContext()
    result = registry_context.sort('quick', data)
    print(f"   结果: {result}\n")
    
    # 5. 支付系统
    print("5️⃣  支付系统:")
    payment = PaymentContext(CreditCardPayment("1234-5678-9012-3456", "123"))
    result = payment.process_payment(99.99)
    print(f"   交易号: {result.transaction_id}\n")
    
    # 6. 折扣计算
    print("6️⃣  折扣计算:")
    order = Order(total=1000.0, items_count=15, customer_level="gold")
    cart = ShoppingCart(VIPDiscount())
    result = cart.checkout(order)
    
    print("\n" + "=" * 70)
    print("✅ 所有演示完成！")
    print("=" * 70)
