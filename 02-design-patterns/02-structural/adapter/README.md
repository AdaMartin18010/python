# Adapter Pattern - 适配器模式

## 📚 概述

**适配器模式**是一种结构型设计模式，它能使接口不兼容的对象能够相互合作。就像电源适配器将不同的插头转换为统一接口一样。

## 🎯 核心概念

### 定义

> 适配器模式将一个类的接口转换成客户希望的另外一个接口，使得原本由于接口不兼容而不能一起工作的类可以一起工作。

### 应用场景

- ✅ 集成第三方库
- ✅ 遗留系统兼容
- ✅ API版本兼容
- ✅ 数据格式转换
- ✅ 接口统一
- ✅ 多数据源适配

### 优势与劣势

**优势**:

- ✅ 单一职责原则（分离接口转换逻辑）
- ✅ 开闭原则（无需修改现有代码）
- ✅ 提高类的复用性
- ✅ 增加系统灵活性

**劣势**:

- ⚠️ 增加代码复杂度
- ⚠️ 可能影响性能
- ⚠️ 过多适配器难以维护

## 💡 Python实现方式

### 1. 类适配器（继承）⭐⭐⭐

```python
from abc import ABC, abstractmethod


class Target(ABC):
    """目标接口"""
    
    @abstractmethod
    def request(self) -> str:
        pass


class Adaptee:
    """需要适配的类"""
    
    def specific_request(self) -> str:
        return "Specific request from Adaptee"


class ClassAdapter(Adaptee, Target):
    """类适配器（多重继承）"""
    
    def request(self) -> str:
        # 调用父类方法并适配
        return f"Adapted: {self.specific_request()}"


# 使用
adapter = ClassAdapter()
print(adapter.request())
# 输出: Adapted: Specific request from Adaptee
```

### 2. 对象适配器（组合）⭐⭐⭐⭐⭐

```python
class ObjectAdapter(Target):
    """对象适配器（推荐）"""
    
    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee
    
    def request(self) -> str:
        # 委托给adaptee
        return f"Adapted: {self.adaptee.specific_request()}"


# 使用
adaptee = Adaptee()
adapter = ObjectAdapter(adaptee)
print(adapter.request())
```

### 3. 函数适配器 ⭐⭐⭐⭐

```python
from typing import Callable


def function_adapter(
    func: Callable[[int, int], int]
) -> Callable[[str, str], str]:
    """函数适配器"""
    
    def wrapper(a: str, b: str) -> str:
        # 转换参数类型
        result = func(int(a), int(b))
        # 转换返回值类型
        return str(result)
    
    return wrapper


# 原始函数
def add_numbers(a: int, b: int) -> int:
    return a + b


# 适配
add_strings = function_adapter(add_numbers)
result = add_strings("10", "20")  # "30"
```

## 🏗️ 现代Python实现（2025标准）

### 完整的数据源适配器

```python
from abc import ABC, abstractmethod
from typing import Any, Protocol
from dataclasses import dataclass


@dataclass
class DataRecord:
    """统一的数据记录"""
    id: int
    name: str
    value: float


class DataSource(Protocol):
    """数据源接口（使用Protocol）"""
    
    def fetch_data(self) -> list[DataRecord]:
        """获取数据"""
        ...


class JSONDataSource:
    """JSON数据源"""
    
    def get_json_data(self) -> list[dict[str, Any]]:
        """返回JSON格式数据"""
        return [
            {"id": 1, "name": "Alice", "value": 100.0},
            {"id": 2, "name": "Bob", "value": 200.0},
        ]


class XMLDataSource:
    """XML数据源"""
    
    def fetch_xml(self) -> str:
        """返回XML字符串"""
        return """
        <records>
            <record>
                <id>1</id>
                <name>Charlie</name>
                <value>300.0</value>
            </record>
        </records>
        """


class JSONAdapter:
    """JSON适配器"""
    
    def __init__(self, source: JSONDataSource) -> None:
        self.source = source
    
    def fetch_data(self) -> list[DataRecord]:
        """适配JSON数据为统一格式"""
        json_data = self.source.get_json_data()
        return [
            DataRecord(
                id=item["id"],
                name=item["name"],
                value=item["value"]
            )
            for item in json_data
        ]


class XMLAdapter:
    """XML适配器"""
    
    def __init__(self, source: XMLDataSource) -> None:
        self.source = source
    
    def fetch_data(self) -> list[DataRecord]:
        """适配XML数据为统一格式"""
        import xml.etree.ElementTree as ET
        
        xml_string = self.source.fetch_xml()
        root = ET.fromstring(xml_string)
        
        records = []
        for record in root.findall("record"):
            records.append(DataRecord(
                id=int(record.find("id").text),  # type: ignore
                name=record.find("name").text,  # type: ignore
                value=float(record.find("value").text)  # type: ignore
            ))
        
        return records


# 客户端代码
def process_data(source: DataSource) -> None:
    """处理数据（不关心数据源类型）"""
    data = source.fetch_data()
    for record in data:
        print(f"{record.id}: {record.name} = {record.value}")


# 使用不同数据源
json_source = JSONDataSource()
json_adapter = JSONAdapter(json_source)
process_data(json_adapter)

xml_source = XMLDataSource()
xml_adapter = XMLAdapter(xml_source)
process_data(xml_adapter)
```

## 🔬 高级模式

### 1. 双向适配器

```python
class TwoWayAdapter(Target):
    """双向适配器"""
    
    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee
    
    def request(self) -> str:
        """Target接口方法"""
        return f"Adapted: {self.adaptee.specific_request()}"
    
    def specific_request(self) -> str:
        """Adaptee接口方法"""
        return self.adaptee.specific_request()
```

### 2. 缓存适配器

```python
from functools import lru_cache


class CachingAdapter:
    """带缓存的适配器"""
    
    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee
    
    @lru_cache(maxsize=128)
    def request(self, key: str) -> str:
        """缓存适配结果"""
        return f"Cached: {self.adaptee.specific_request()}"
```

### 3. 链式适配器

```python
class ChainAdapter:
    """链式适配器"""
    
    def __init__(self, adapters: list[Target]) -> None:
        self.adapters = adapters
    
    def request(self) -> list[str]:
        """执行所有适配器"""
        return [adapter.request() for adapter in self.adapters]
```

## 📊 实战案例

### 1. 第三方支付集成

```python
from abc import ABC, abstractmethod
from typing import Protocol


class PaymentResult:
    """支付结果"""
    def __init__(self, success: bool, transaction_id: str) -> None:
        self.success = success
        self.transaction_id = transaction_id


class PaymentGateway(Protocol):
    """统一支付接口"""
    
    def pay(self, amount: float, currency: str = "USD") -> PaymentResult:
        """执行支付"""
        ...


class StripeAPI:
    """Stripe支付API"""
    
    def charge(
        self, 
        amount_cents: int, 
        currency_code: str
    ) -> dict[str, Any]:
        """Stripe的原始API"""
        return {
            "status": "succeeded",
            "id": "ch_stripe_123",
            "amount": amount_cents
        }


class PayPalAPI:
    """PayPal支付API"""
    
    def create_payment(
        self, 
        value: str, 
        currency: str
    ) -> dict[str, Any]:
        """PayPal的原始API"""
        return {
            "state": "approved",
            "transaction_id": "pp_456",
            "amount": {"total": value, "currency": currency}
        }


class StripeAdapter:
    """Stripe适配器"""
    
    def __init__(self, stripe: StripeAPI) -> None:
        self.stripe = stripe
    
    def pay(self, amount: float, currency: str = "USD") -> PaymentResult:
        """适配Stripe API"""
        # 转换金额（美元 → 美分）
        amount_cents = int(amount * 100)
        
        # 调用Stripe API
        result = self.stripe.charge(amount_cents, currency.lower())
        
        # 转换结果
        return PaymentResult(
            success=(result["status"] == "succeeded"),
            transaction_id=result["id"]
        )


class PayPalAdapter:
    """PayPal适配器"""
    
    def __init__(self, paypal: PayPalAPI) -> None:
        self.paypal = paypal
    
    def pay(self, amount: float, currency: str = "USD") -> PaymentResult:
        """适配PayPal API"""
        # 转换金额为字符串
        value = f"{amount:.2f}"
        
        # 调用PayPal API
        result = self.paypal.create_payment(value, currency)
        
        # 转换结果
        return PaymentResult(
            success=(result["state"] == "approved"),
            transaction_id=result["transaction_id"]
        )


# 客户端代码
def process_payment(gateway: PaymentGateway, amount: float) -> None:
    """处理支付（不关心具体支付方式）"""
    result = gateway.pay(amount)
    if result.success:
        print(f"✅ Payment successful: {result.transaction_id}")
    else:
        print("❌ Payment failed")


# 使用不同支付方式
stripe = StripeAPI()
stripe_adapter = StripeAdapter(stripe)
process_payment(stripe_adapter, 99.99)

paypal = PayPalAPI()
paypal_adapter = PayPalAdapter(paypal)
process_payment(paypal_adapter, 199.99)
```

### 2. 数据库驱动适配

```python
from typing import Any


class Database(Protocol):
    """统一数据库接口"""
    
    def execute(self, query: str) -> list[dict[str, Any]]:
        """执行查询"""
        ...


class MySQLDriver:
    """MySQL驱动"""
    
    def query(self, sql: str) -> list[tuple]:
        """MySQL特定API"""
        # 模拟查询
        return [(1, "Alice"), (2, "Bob")]


class PostgreSQLDriver:
    """PostgreSQL驱动"""
    
    def exec_sql(self, statement: str) -> list[dict]:
        """PostgreSQL特定API"""
        # 模拟查询
        return [{"id": 1, "name": "Charlie"}]


class MySQLAdapter:
    """MySQL适配器"""
    
    def __init__(self, driver: MySQLDriver) -> None:
        self.driver = driver
    
    def execute(self, query: str) -> list[dict[str, Any]]:
        """适配MySQL结果"""
        rows = self.driver.query(query)
        # 转换为统一格式
        return [
            {"id": row[0], "name": row[1]}
            for row in rows
        ]


class PostgreSQLAdapter:
    """PostgreSQL适配器"""
    
    def __init__(self, driver: PostgreSQLDriver) -> None:
        self.driver = driver
    
    def execute(self, query: str) -> list[dict[str, Any]]:
        """适配PostgreSQL结果（无需转换）"""
        return self.driver.exec_sql(query)
```

## 🎯 最佳实践

### 1. 使用Protocol而非ABC

```python
# ✅ 推荐：使用Protocol（结构子类型）
class DataSource(Protocol):
    def fetch_data(self) -> list[DataRecord]:
        ...

# ❌ 避免：强制继承ABC
class DataSource(ABC):
    @abstractmethod
    def fetch_data(self) -> list[DataRecord]:
        pass
```

### 2. 适配器应轻量

```python
# ✅ 好：只做接口转换
class GoodAdapter:
    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee
    
    def request(self) -> str:
        return self.adaptee.specific_request()

# ❌ 差：包含业务逻辑
class BadAdapter:
    def request(self) -> str:
        result = self.adaptee.specific_request()
        # 复杂的业务处理...
        return process_business_logic(result)
```

### 3. 考虑性能

```python
# 对高频调用使用缓存
class OptimizedAdapter:
    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee
        self._cache: dict[str, Any] = {}
    
    def request(self, key: str) -> Any:
        if key not in self._cache:
            self._cache[key] = self._transform(
                self.adaptee.get_data(key)
            )
        return self._cache[key]
```

## 🔗 相关模式

- **Bridge Pattern**: 分离抽象和实现
- **Decorator Pattern**: 动态添加功能
- **Proxy Pattern**: 控制访问
- **Facade Pattern**: 简化接口

## 📚 参考资源

- **Design Patterns** - Gang of Four
- **Head First Design Patterns**
- **Python Design Patterns** - Brandon Rhodes
- **Refactoring Guru**: <https://refactoring.guru/design-patterns/adapter>

---

**适配器模式：让不兼容变得兼容！** 🔌
