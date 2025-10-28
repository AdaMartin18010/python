# pytest 现代测试框架

**Python测试的最佳选择**

---

## 📋 概述

pytest是Python中最流行的测试框架，提供简洁的语法、强大的功能和丰富的插件生态。

### 核心特性

- ✅ **简洁语法** - 使用assert语句
- 🔧 **Fixtures** - 强大的测试准备机制
- 🎯 **参数化** - 轻松测试多组数据
- 🔌 **插件丰富** - 大量实用插件
- 📊 **详细报告** - 清晰的失败信息

---

## 🚀 快速开始

### 安装

```bash
uv add pytest
```

### 第一个测试

```python
# test_sample.py
def test_addition():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"
```

运行测试:
```bash
pytest
pytest test_sample.py
pytest -v  # 详细输出
```

---

## 💻 核心功能

### 1. 基本测试

```python
# test_math.py
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_floats():
    result = add(0.1, 0.2)
    assert abs(result - 0.3) < 1e-10  # 浮点数比较
```

### 2. 异常测试

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_normal():
    assert divide(10, 2) == 5
```

### 3. 测试类

```python
class TestCalculator:
    def test_add(self):
        assert 1 + 1 == 2
    
    def test_subtract(self):
        assert 5 - 3 == 2
    
    def test_multiply(self):
        assert 3 * 4 == 12
```

---

## 🔧 Fixtures

### 基本Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    """提供测试数据"""
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_length(sample_data):
    assert len(sample_data) == 5
```

### 设置和清理

```python
@pytest.fixture
def database():
    # 设置
    db = create_database()
    db.connect()
    
    yield db  # 提供给测试
    
    # 清理
    db.disconnect()
    db.drop()

def test_insert(database):
    database.insert("test data")
    assert database.count() == 1
```

### Fixture作用域

```python
@pytest.fixture(scope="function")  # 每个测试函数
def func_fixture():
    return "function scope"

@pytest.fixture(scope="class")  # 每个测试类
def class_fixture():
    return "class scope"

@pytest.fixture(scope="module")  # 每个模块
def module_fixture():
    return "module scope"

@pytest.fixture(scope="session")  # 整个测试会话
def session_fixture():
    return "session scope"
```

### Fixture参数化

```python
@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param

def test_square(number):
    assert number ** 2 >= 0
# 这个测试会运行3次，每次使用不同的参数
```

---

## 🎯 参数化测试

### 基本参数化

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### 多参数

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (5, 5, 10),
    (10, -5, 5),
])
def test_add(a, b, expected):
    assert a + b == expected
```

### 组合参数

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_multiply(x, y):
    assert x * y > 0
# 运行4次: (1,3), (1,4), (2,3), (2,4)
```

---

## 🏷️ 标记 (Markers)

### 内置标记

```python
import pytest

@pytest.mark.skip(reason="暂时跳过")
def test_skip():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="需要Python 3.10+")
def test_skipif():
    pass

@pytest.mark.xfail(reason="已知bug")
def test_xfail():
    assert 1 == 2  # 预期失败
```

### 自定义标记

```python
# 定义标记
@pytest.mark.slow
def test_slow_operation():
    time.sleep(1)
    assert True

@pytest.mark.unit
def test_unit():
    assert True

@pytest.mark.integration
def test_integration():
    assert True
```

运行特定标记的测试:
```bash
pytest -m slow          # 只运行slow测试
pytest -m "not slow"    # 跳过slow测试
pytest -m "unit or integration"  # 运行unit或integration测试
```

---

## 🔌 常用插件

### pytest-cov (覆盖率)

```bash
uv add pytest-cov

# 运行
pytest --cov=myapp tests/
pytest --cov=myapp --cov-report=html
```

### pytest-mock (Mock)

```python
def test_with_mock(mocker):
    mock_func = mocker.patch('module.function')
    mock_func.return_value = 42
    
    result = call_function()
    assert result == 42
    mock_func.assert_called_once()
```

### pytest-asyncio (异步测试)

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == "expected"
```

### pytest-xdist (并行测试)

```bash
uv add pytest-xdist

# 运行
pytest -n 4  # 使用4个进程
pytest -n auto  # 自动检测CPU核心数
```

---

## 🏗️ 项目结构

### 推荐结构

```
myproject/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # 共享fixtures
│   ├── test_core.py
│   └── test_utils.py
├── pytest.ini           # pytest配置
└── pyproject.toml
```

### conftest.py

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def app():
    """创建应用实例"""
    from myapp import create_app
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def db(app):
    """创建数据库"""
    from myapp import db
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
```

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
markers =
    slow: 慢速测试
    unit: 单元测试
    integration: 集成测试
```

---

## 📝 最佳实践

### 1. 测试命名

```python
# ✅ 好 - 清晰的测试名称
def test_user_registration_with_valid_email():
    pass

def test_user_registration_fails_with_invalid_email():
    pass

# ❌ 差 - 模糊的测试名称
def test_registration():
    pass
```

### 2. 单一职责

```python
# ✅ 好 - 每个测试只测试一件事
def test_add_returns_sum():
    assert add(1, 2) == 3

def test_add_handles_negative_numbers():
    assert add(-1, -2) == -3

# ❌ 差 - 测试太多内容
def test_add():
    assert add(1, 2) == 3
    assert add(-1, -2) == -3
    assert add(0, 0) == 0
    # ...
```

### 3. 使用Fixtures避免重复

```python
# ✅ 好 - 使用fixture
@pytest.fixture
def user():
    return User(name="Alice", email="alice@example.com")

def test_user_name(user):
    assert user.name == "Alice"

def test_user_email(user):
    assert user.email == "alice@example.com"
```

### 4. 参数化减少重复

```python
# ✅ 好 - 参数化
@pytest.mark.parametrize("value,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("Python", "PYTHON"),
])
def test_upper(value, expected):
    assert value.upper() == expected

# ❌ 差 - 重复代码
def test_upper_hello():
    assert "hello".upper() == "HELLO"

def test_upper_world():
    assert "world".upper() == "WORLD"
```

---

## 🧪 实战示例

### API测试

```python
import pytest
from fastapi.testclient import TestClient
from myapp import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"

def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert "username" in response.json()
```

### 数据库测试

```python
@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()
    session.close()

def test_create_user(db_session):
    user = User(username="test", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert db_session.query(User).count() == 1
```

---

## 🔗 相关资源

- [官方文档](https://docs.pytest.org/)
- [pytest插件列表](https://docs.pytest.org/en/latest/reference/plugin_list.html)
- [Real Python pytest教程](https://realpython.com/pytest-python-testing/)

---

**最后更新**: 2025年10月28日

