# Python 实践案例

**实际应用案例和最佳实践模式**-

---

## 📚 目录

1. [项目结构模板](01-project-structure.md) - 标准项目组织
2. [常见设计模式](02-design-patterns.md) - 设计模式实现
3. [错误处理模式](03-error-handling-patterns.md) - 异常处理策略
4. [测试策略](04-testing-strategies.md) - 测试最佳实践
5. [性能优化案例](05-performance-cases.md) - 性能优化技巧

---

## 🏗️ 标准项目结构

### 现代 Python 项目布局

```text
my-project/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── docs/
│   ├── index.md
│   └── api.md
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── engine.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest 配置
│   ├── test_main.py
│   └── test_core/
│       └── test_engine.py
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml           # 项目配置
├── README.md
├── LICENSE
└── CHANGELOG.md
```

### pyproject.toml 完整配置

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "A modern Python project"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["python", "example"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

dependencies = [
    "pydantic>=2.9.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=5.0.0",
    "pytest-asyncio>=0.24.0",
    "mypy>=1.11.0",
    "ruff>=0.6.0",
]

[project.scripts]
myproject = "myproject.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pre-commit>=3.8.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

---

## 🎨 设计模式实现

### 1. 单例模式

```python
class Singleton(type):
    """线程安全的单例元类"""
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=Singleton):
    def __init__(self):
        self.connection = None
    
    def connect(self):
        if not self.connection:
            self.connection = create_connection()
        return self.connection

# 使用
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True
```

### 2. 工厂模式

```python
from abc import ABC, abstractmethod
from typing import Protocol

class Vehicle(Protocol):
    """车辆接口"""
    def drive(self) -> str: ...
    def stop(self) -> str: ...

class Car:
    def drive(self) -> str:
        return "Car is driving"
    
    def stop(self) -> str:
        return "Car stopped"

class Truck:
    def drive(self) -> str:
        return "Truck is driving"
    
    def stop(self) -> str:
        return "Truck stopped"

class VehicleFactory:
    """工厂类"""
    @staticmethod
    def create_vehicle(vehicle_type: str) -> Vehicle:
        match vehicle_type:
            case "car":
                return Car()
            case "truck":
                return Truck()
            case _:
                raise ValueError(f"Unknown vehicle type: {vehicle_type}")

# 使用
factory = VehicleFactory()
car = factory.create_vehicle("car")
print(car.drive())  # Car is driving
```

### 3. 观察者模式

```python
from typing import Protocol, Set

class Observer(Protocol):
    """观察者接口"""
    def update(self, message: str) -> None: ...

class Subject:
    """被观察者"""
    def __init__(self):
        self._observers: Set[Observer] = set()
    
    def attach(self, observer: Observer):
        self._observers.add(observer)
    
    def detach(self, observer: Observer):
        self._observers.discard(observer)
    
    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class ConcreteObserver:
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str):
        print(f"{self.name} received: {message}")

# 使用
subject = Subject()
obs1 = ConcreteObserver("Observer 1")
obs2 = ConcreteObserver("Observer 2")

subject.attach(obs1)
subject.attach(obs2)
subject.notify("Event occurred!")
```

### 4. 策略模式

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    """支付策略接口"""
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with credit card {self.card_number}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via PayPal account {self.email}"

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy: PaymentStrategy | None = None
    
    def add_item(self, item: str, price: float):
        self.items.append((item, price))
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
    
    def checkout(self) -> str:
        if not self.payment_strategy:
            raise ValueError("No payment strategy set")
        
        total = sum(price for _, price in self.items)
        return self.payment_strategy.pay(total)

# 使用
cart = ShoppingCart()
cart.add_item("Book", 29.99)
cart.add_item("Pen", 4.99)

cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456"))
print(cart.checkout())
```

### 5. 装饰器模式

```python
from abc import ABC, abstractmethod

class Component(ABC):
    """组件接口"""
    @abstractmethod
    def operation(self) -> str:
        pass

class ConcreteComponent(Component):
    """具体组件"""
    def operation(self) -> str:
        return "ConcreteComponent"

class Decorator(Component):
    """装饰器基类"""
    def __init__(self, component: Component):
        self._component = component
    
    def operation(self) -> str:
        return self._component.operation()

class ConcreteDecoratorA(Decorator):
    def operation(self) -> str:
        return f"DecoratorA({self._component.operation()})"

class ConcreteDecoratorB(Decorator):
    def operation(self) -> str:
        return f"DecoratorB({self._component.operation()})"

# 使用
component = ConcreteComponent()
decorated = ConcreteDecoratorB(ConcreteDecoratorA(component))
print(decorated.operation())
# 输出: DecoratorB(DecoratorA(ConcreteComponent))
```

---

## ⚠️ 错误处理模式

### 1. 自定义异常层次

```python
class ApplicationError(Exception):
    """应用基础异常"""
    pass

class ValidationError(ApplicationError):
    """验证错误"""
    pass

class DatabaseError(ApplicationError):
    """数据库错误"""
    pass

class NotFoundError(ApplicationError):
    """资源未找到"""
    pass

class PermissionError(ApplicationError):
    """权限错误"""
    pass

# 使用
def validate_user(user_data: dict):
    if "email" not in user_data:
        raise ValidationError("Email is required")
    
    if "@" not in user_data["email"]:
        raise ValidationError("Invalid email format")
```

### 2. 结果类型模式

```python
from typing import Generic, TypeVar, Union
from dataclasses import dataclass

T = TypeVar("T")
E = TypeVar("E")

@dataclass
class Ok(Generic[T]):
    """成功结果"""
    value: T
    
    def is_ok(self) -> bool:
        return True
    
    def is_err(self) -> bool:
        return False
    
    def unwrap(self) -> T:
        return self.value

@dataclass
class Err(Generic[E]):
    """错误结果"""
    error: E
    
    def is_ok(self) -> bool:
        return False
    
    def is_err(self) -> bool:
        return True
    
    def unwrap(self):
        raise ValueError(f"Called unwrap on Err: {self.error}")

Result = Union[Ok[T], Err[E]]

# 使用
def divide(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

result = divide(10, 2)
if result.is_ok():
    print(f"Result: {result.unwrap()}")
else:
    print(f"Error: {result.error}")
```

### 3. 上下文管理器错误处理

```python
from contextlib import contextmanager

@contextmanager
def error_handler(operation: str):
    """错误处理上下文管理器"""
    try:
        yield
    except ValueError as e:
        print(f"Validation error in {operation}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error in {operation}: {e}")
        raise
    finally:
        print(f"Completed {operation}")

# 使用
with error_handler("data processing"):
    process_data()
```

---

## 🧪 测试策略

### 1. 单元测试

```python
import pytest
from myproject.calculator import Calculator

class TestCalculator:
    @pytest.fixture
    def calc(self):
        """测试夹具"""
        return Calculator()
    
    def test_add(self, calc):
        """测试加法"""
        assert calc.add(2, 3) == 5
        assert calc.add(-1, 1) == 0
        assert calc.add(0, 0) == 0
    
    def test_divide(self, calc):
        """测试除法"""
        assert calc.divide(10, 2) == 5
        assert calc.divide(9, 3) == 3
    
    def test_divide_by_zero(self, calc):
        """测试除零异常"""
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, 2),
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
    ])
    def test_add_parametrized(self, calc, a, b, expected):
        """参数化测试"""
        assert calc.add(a, b) == expected
```

### 2. Mock 和 Stub

```python
from unittest.mock import Mock, patch
import pytest

def test_with_mock():
    """使用 Mock 对象"""
    # 创建 Mock
    mock_db = Mock()
    mock_db.get_user.return_value = {"id": 1, "name": "Alice"}
    
    # 测试
    user = mock_db.get_user(1)
    assert user["name"] == "Alice"
    
    # 验证调用
    mock_db.get_user.assert_called_once_with(1)

@patch('myproject.api.requests.get')
def test_with_patch(mock_get):
    """使用 patch 替换依赖"""
    # 配置 Mock 返回值
    mock_get.return_value.json.return_value = {"status": "ok"}
    mock_get.return_value.status_code = 200
    
    # 测试
    from myproject.api import fetch_data
    result = fetch_data("https://api.example.com")
    
    assert result["status"] == "ok"
    mock_get.assert_called_once()
```

### 3. 异步测试

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """异步函数测试"""
    async def fetch_data():
        await asyncio.sleep(0.1)
        return {"data": "value"}
    
    result = await fetch_data()
    assert result["data"] == "value"

@pytest.mark.asyncio
async def test_async_with_mock():
    """异步 Mock 测试"""
    from unittest.mock import AsyncMock
    
    mock_api = AsyncMock()
    mock_api.get_user.return_value = {"id": 1}
    
    user = await mock_api.get_user(1)
    assert user["id"] == 1
```

### 4. 集成测试

```python
import pytest
from fastapi.testclient import TestClient
from myproject.main import app

@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)

def test_create_user(client):
    """集成测试：创建用户"""
    response = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data

def test_get_user(client):
    """集成测试：获取用户"""
    # 先创建
    create_response = client.post(
        "/users",
        json={"name": "Bob", "email": "bob@example.com"}
    )
    user_id = create_response.json()["id"]
    
    # 再获取
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Bob"
```

---

## ⚡ 性能优化案例

### 1. 列表推导式 vs 循环

```python
import timeit

# ❌ 慢：使用循环
def squares_loop(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# ✅ 快：使用列表推导式
def squares_comprehension(n):
    return [i ** 2 for i in range(n)]

# 性能测试
n = 100000
time_loop = timeit.timeit(lambda: squares_loop(n), number=100)
time_comp = timeit.timeit(lambda: squares_comprehension(n), number=100)

print(f"Loop: {time_loop:.4f}s")
print(f"Comprehension: {time_comp:.4f}s")
print(f"Speedup: {time_loop / time_comp:.2f}x")
```

### 2. 生成器节省内存

```python
import sys

# ❌ 占用大量内存
def get_numbers_list(n):
    return [i for i in range(n)]

# ✅ 节省内存
def get_numbers_generator(n):
    return (i for i in range(n))

# 内存对比
n = 1000000
list_obj = get_numbers_list(n)
gen_obj = get_numbers_generator(n)

print(f"List size: {sys.getsizeof(list_obj)} bytes")
print(f"Generator size: {sys.getsizeof(gen_obj)} bytes")
# List size: ~8MB
# Generator size: ~128 bytes
```

### 3. 字典查找 vs 列表查找

```python
import timeit

# 测试数据
items = list(range(10000))
search_dict = {i: i for i in items}
search_list = list(items)

# 字典查找 O(1)
def dict_lookup():
    return 9999 in search_dict

# 列表查找 O(n)
def list_lookup():
    return 9999 in search_list

# 性能对比
time_dict = timeit.timeit(dict_lookup, number=100000)
time_list = timeit.timeit(list_lookup, number=100000)

print(f"Dict lookup: {time_dict:.4f}s")
print(f"List lookup: {time_list:.4f}s")
print(f"Speedup: {time_list / time_dict:.2f}x")
```

### 4. 缓存优化

```python
from functools import lru_cache

# ❌ 无缓存：慢
def fibonacci_slow(n):
    if n < 2:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

# ✅ 有缓存：快
@lru_cache(maxsize=None)
def fibonacci_fast(n):
    if n < 2:
        return n
    return fibonacci_fast(n-1) + fibonacci_fast(n-2)

# 性能对比
import time

n = 35

start = time.time()
result1 = fibonacci_slow(n)
time_slow = time.time() - start

start = time.time()
result2 = fibonacci_fast(n)
time_fast = time.time() - start

print(f"Without cache: {time_slow:.4f}s")
print(f"With cache: {time_fast:.4f}s")
print(f"Speedup: {time_slow / time_fast:.0f}x")
```

### 5. 批量操作优化

```python
# ❌ 慢：逐个处理
def process_items_slow(items):
    results = []
    for item in items:
        result = expensive_operation(item)
        results.append(result)
    return results

# ✅ 快：批量处理
def process_items_fast(items, batch_size=100):
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = expensive_batch_operation(batch)
        results.extend(batch_results)
    return results

# ✅ 更快：并行处理
from concurrent.futures import ThreadPoolExecutor

def process_items_parallel(items, workers=4):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(expensive_operation, items))
    return results
```

---

## 📚 完整项目示例

### Web API 项目

```python
# src/myproject/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI(title="My API", version="1.0.0")

class User(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

# 模拟数据库
users_db: dict[int, User] = {}
next_id = 1

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """创建用户"""
    global next_id
    new_user = User(id=next_id, **user.dict())
    users_db[next_id] = new_user
    next_id += 1
    return new_user

@app.get("/users", response_model=List[User])
async def list_users():
    """列出所有用户"""
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """获取用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    """更新用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = User(id=user_id, **user.dict())
    users_db[user_id] = updated_user
    return updated_user

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """删除用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 📖 延伸阅读

- [Python Patterns](https://python-patterns.guide/)
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns/python)
- [Real Python - Testing](https://realpython.com/python-testing/)
- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)

---

**通过实践掌握 Python，构建优秀的应用！** 🚀✨
