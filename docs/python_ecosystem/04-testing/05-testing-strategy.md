# 测试策略与最佳实践

**Python测试完整指南**

---

## 📋 测试金字塔

```
           /\
          /  \  E2E Tests (5%)
         /----\
        /      \  Integration Tests (15%)
       /--------\
      /          \  Unit Tests (80%)
     /------------\
```

### 测试层级

1. **单元测试** (80%)
   - 测试单个函数/方法
   - 快速、独立、可重复
   
2. **集成测试** (15%)
   - 测试模块间交互
   - 数据库、API集成
   
3. **端到端测试** (5%)
   - 测试完整用户流程
   - UI、业务流程

---

## 🎯 测试策略

### 1. AAA模式

```python
def test_user_creation():
    # Arrange - 准备
    user_data = {'name': 'Alice', 'email': 'alice@example.com'}
    
    # Act - 执行
    user = create_user(user_data)
    
    # Assert - 断言
    assert user.name == 'Alice'
    assert user.email == 'alice@example.com'
```

### 2. Given-When-Then

```python
def test_shopping_cart():
    # Given - 给定初始状态
    cart = ShoppingCart()
    product = Product(name='Book', price=10.0)
    
    # When - 当执行操作
    cart.add(product, quantity=2)
    
    # Then - 那么期望结果
    assert cart.total == 20.0
    assert len(cart.items) == 1
```

---

## 🧪 单元测试最佳实践

### 1. 测试命名

```python
# ✅ 好 - 描述性命名
def test_create_user_with_valid_email_succeeds():
    pass

def test_create_user_with_invalid_email_raises_validation_error():
    pass

# ❌ 差 - 模糊命名
def test_user():
    pass

def test_case1():
    pass
```

### 2. 一个测试一个断言

```python
# ✅ 好 - 单一职责
def test_user_name_is_saved():
    user = create_user(name='Alice')
    assert user.name == 'Alice'

def test_user_email_is_saved():
    user = create_user(email='alice@example.com')
    assert user.email == 'alice@example.com'

# ❌ 差 - 多个断言
def test_user():
    user = create_user(name='Alice', email='alice@example.com')
    assert user.name == 'Alice'
    assert user.email == 'alice@example.com'
    assert user.is_active
```

### 3. 使用Fixtures

```python
import pytest

@pytest.fixture
def user():
    return User(name='Alice', email='alice@example.com')

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.close()

def test_user_save(user, db_session):
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
```

---

## 🔌 集成测试

### 数据库集成

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope='function')
def db():
    # 使用测试数据库
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()

def test_user_repository(db):
    repo = UserRepository(db)
    user = User(name='Alice')
    
    saved_user = repo.save(user)
    found_user = repo.find_by_id(saved_user.id)
    
    assert found_user.name == 'Alice'
```

### API集成

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_user():
    response = client.post(
        '/users/',
        json={'name': 'Alice', 'email': 'alice@example.com'}
    )
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Alice'

def test_get_user():
    response = client.get('/users/1')
    assert response.status_code == 200
```

---

## 🎭 测试替身 (Test Doubles)

### 1. Mock

```python
from unittest.mock import Mock, patch

def test_send_email():
    email_service = Mock()
    email_service.send.return_value = True
    
    result = send_welcome_email(email_service, 'user@example.com')
    
    email_service.send.assert_called_once_with(
        to='user@example.com',
        subject='Welcome'
    )
    assert result is True
```

### 2. Stub

```python
class StubDatabase:
    def get_user(self, user_id):
        return User(id=user_id, name='Test User')

def test_user_service():
    db = StubDatabase()
    service = UserService(db)
    
    user = service.get_user(1)
    assert user.name == 'Test User'
```

### 3. Spy

```python
class SpyEmailService:
    def __init__(self):
        self.sent_emails = []
    
    def send(self, to, subject, body):
        self.sent_emails.append({'to': to, 'subject': subject})
        return True

def test_notification():
    email_spy = SpyEmailService()
    notify_user(email_spy, 'user@example.com')
    
    assert len(email_spy.sent_emails) == 1
    assert email_spy.sent_emails[0]['to'] == 'user@example.com'
```

---

## 📊 测试覆盖率

### 使用Coverage.py

```bash
# 运行测试并生成覆盖率报告
pytest --cov=myapp --cov-report=html

# 查看报告
open htmlcov/index.html
```

### 覆盖率目标

```python
# pytest.ini 或 pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=myapp --cov-fail-under=80"
```

### 覆盖率不是越高越好

```python
# ✅ 关注关键路径
def critical_business_logic():
    # 必须100%覆盖
    pass

# ⚠️ 简单代码可以适当降低
def simple_getter():
    return self._value
```

---

## 🎯 测试驱动开发 (TDD)

### Red-Green-Refactor

```python
# 1. Red - 写失败的测试
def test_calculate_total():
    cart = ShoppingCart()
    cart.add(Product(price=10.0))
    assert cart.total() == 10.0  # 失败

# 2. Green - 最简实现
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add(self, product):
        self.items.append(product)
    
    def total(self):
        return sum(item.price for item in self.items)

# 3. Refactor - 重构优化
class ShoppingCart:
    def __init__(self):
        self._items: list[Product] = []
    
    def add(self, product: Product) -> None:
        self._items.append(product)
    
    def total(self) -> Decimal:
        return sum((item.price for item in self._items), Decimal('0'))
```

---

## 🚀 性能测试

### 使用pytest-benchmark

```python
import pytest

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def test_fibonacci_performance(benchmark):
    result = benchmark(fibonacci, 20)
    assert result == 6765
```

---

## 🔒 安全测试

```python
def test_sql_injection_prevention():
    # 测试是否防止SQL注入
    malicious_input = "'; DROP TABLE users; --"
    user = find_user_by_name(malicious_input)
    assert user is None

def test_xss_prevention():
    # 测试是否防止XSS
    malicious_script = "<script>alert('XSS')</script>"
    sanitized = sanitize_input(malicious_script)
    assert '<script>' not in sanitized
```

---

## 📚 最佳实践总结

### ✅ DO

1. **独立性** - 测试之间相互独立
2. **快速** - 单元测试应该快速运行
3. **可重复** - 每次运行结果一致
4. **自验证** - 自动判断成功或失败
5. **及时** - 代码写完立即测试

### ❌ DON'T

1. **依赖顺序** - 测试依赖执行顺序
2. **共享状态** - 测试间共享可变状态
3. **外部依赖** - 依赖外部服务
4. **测试实现** - 测试内部实现而非行为
5. **忽略失败** - 忽略偶尔失败的测试

---

## 🔗 相关资源

- [pytest文档](https://docs.pytest.org/)
- [测试驱动开发](https://www.obeythetestinggoat.com/)

---

**最后更新**: 2025年10月28日

