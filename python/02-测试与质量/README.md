# 02-测试与质量（2025年10月标准）

聚焦 pytest、类型检查、静态分析与CI 集成的现代化测试体系。

## 0. 2025年测试工具栈

### 0.1 核心工具（2025推荐）

| 工具 | 版本 | 用途 | 速度 | 推荐度 |
|------|------|------|------|--------|
| **pytest** | 8.3+ | 测试框架 | 快 | ⭐⭐⭐⭐⭐ |
| **pytest-cov** | 5.0+ | 覆盖率 | 快 | ⭐⭐⭐⭐⭐ |
| **pytest-asyncio** | 0.24+ | 异步测试 | 快 | ⭐⭐⭐⭐⭐ |
| **pytest-mock** | 3.14+ | Mock工具 | 快 | ⭐⭐⭐⭐⭐ |
| **hypothesis** | 6.112+ | 属性测试 | 中 | ⭐⭐⭐⭐ |
| **faker** | 30.0+ | 测试数据生成 | 快 | ⭐⭐⭐⭐ |
| **mypy** | 1.11+ | 类型检查 | 中 | ⭐⭐⭐⭐⭐ |
| **ruff** | 0.6+ | 代码质量 | 极快 | ⭐⭐⭐⭐⭐ |

### 0.2 快速配置（pyproject.toml）

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-ra",                          # 显示所有结果
    "--strict-markers",             # 严格标记
    "--strict-config",              # 严格配置
    "--cov=src",                    # 覆盖率源目录
    "--cov-report=term-missing",    # 终端覆盖率报告
    "--cov-report=html",            # HTML覆盖率报告
    "--cov-branch",                 # 分支覆盖
    "--asyncio-mode=auto",          # 自动异步模式
]
markers = [
    "slow: 慢速测试",
    "integration: 集成测试",
    "unit: 单元测试",
    "e2e: 端到端测试",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
precision = 2
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

### 0.3 安装测试工具

```bash
# 使用 uv（推荐）
uv add --dev pytest pytest-cov pytest-asyncio pytest-mock hypothesis faker

# 或使用 pip
pip install pytest pytest-cov pytest-asyncio pytest-mock hypothesis faker
```

## 1. 测试策略（2025最佳实践）

- 单元/集成/端到端分层
- 基线用例与回归集
- 属性测试（Property-based Testing）
- 快照测试（Snapshot Testing）
- 变异测试（Mutation Testing）

### 1.1 测试金字塔

```python
# 单元测试 - 基础层
def test_user_creation():
    """测试用户创建功能"""
    user = User(name="test", email="test@example.com", age=25)
    assert user.name == "test"
    assert user.email == "test@example.com"
    assert user.age == 25
    assert user.is_active is True

# 集成测试 - 中间层
def test_user_service_integration():
    """测试用户服务集成"""
    service = UserService()
    user_data = {"name": "test", "email": "test@example.com", "age": 25}
    user = service.create_user(user_data)
    assert user.id is not None
    assert user.name == "test"

# 端到端测试 - 顶层
def test_user_api_e2e():
    """测试用户API端到端"""
    client = TestClient(app)
    response = client.post("/users", json={
        "name": "test",
        "email": "test@example.com",
        "age": 25
    })
    assert response.status_code == 201
    assert response.json()["name"] == "test"
```

### 1.2 测试数据管理

```python
# 测试数据生成
class TestDataFactory:
    """测试数据工厂"""
    
    @staticmethod
    def create_user(**kwargs) -> User:
        """创建测试用户"""
        defaults = {
            "name": "test_user",
            "email": "test@example.com",
            "age": 25,
            "is_active": True
        }
        defaults.update(kwargs)
        return User(**defaults)
    
    @staticmethod
    def create_user_batch(count: int) -> list[User]:
        """批量创建测试用户"""
        return [TestDataFactory.create_user(name=f"user_{i}") for i in range(count)]

# 参数化测试
@pytest.mark.parametrize("name,email,age,expected", [
    ("Alice", "alice@example.com", 25, True),
    ("Bob", "bob@example.com", 17, False),
    ("Charlie", "charlie@example.com", 30, True),
])
def test_user_validation(name, email, age, expected):
    """参数化测试用户验证"""
    user = User(name=name, email=email, age=age)
    assert user.is_adult() == expected
```

## 2. 工具与配置

- pytest 基础配置、参数化、夹具
- 类型检查（mypy/pyright）
- Lint（ruff/flake8/pylint）
- 统一工具配置见仓库根 `pyproject.toml`

### 2.1 pytest 高级特性

```python
# pytest fixtures
@pytest.fixture
def sample_user():
    """用户测试夹具"""
    return User(name="test", email="test@example.com", age=25)

@pytest.fixture
def user_service():
    """用户服务测试夹具"""
    return UserService()

@pytest.fixture
def mock_database():
    """模拟数据库夹具"""
    with patch('app.database.get_connection') as mock:
        mock.return_value = MagicMock()
        yield mock

# 使用夹具的测试
def test_user_creation_with_fixture(sample_user, user_service):
    """使用夹具的测试"""
    user = user_service.create_user(sample_user)
    assert user.id is not None
    assert user.name == sample_user.name

# 异步测试
@pytest.mark.asyncio
async def test_async_user_creation():
    """异步用户创建测试"""
    service = AsyncUserService()
    user = await service.create_user_async({
        "name": "async_user",
        "email": "async@example.com",
        "age": 30
    })
    assert user.name == "async_user"

# 测试标记
@pytest.mark.slow
def test_expensive_operation():
    """慢速测试"""
    # 模拟耗时操作
    time.sleep(2)
    assert True

@pytest.mark.integration
def test_database_integration():
    """集成测试"""
    # 数据库集成测试
    pass
```

### 2.2 类型检查配置

```python
# mypy 配置示例
# pyproject.toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

# 类型检查示例
from typing import List, Dict, Optional, Union

def process_users(users: List[Dict[str, Union[str, int]]]) -> List[str]:
    """处理用户列表，返回用户名列表"""
    return [user["name"] for user in users if isinstance(user["name"], str)]

def get_user_by_id(user_id: int) -> Optional[Dict[str, Union[str, int]]]:
    """根据ID获取用户"""
    # 模拟数据库查询
    if user_id > 0:
        return {"id": user_id, "name": "test", "age": 25}
    return None
```

### 2.3 代码质量工具

```python
# ruff 配置示例
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py312"
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
]

# 代码质量检查示例
class CodeQualityExample:
    """代码质量示例"""
    
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value
    
    def process_data(self, data: List[int]) -> List[int]:
        """处理数据，返回处理后的列表"""
        # 使用列表推导式而不是循环
        return [x * 2 for x in data if x > 0]
    
    def get_user_info(self, user_id: int) -> Optional[Dict[str, str]]:
        """获取用户信息"""
        if user_id <= 0:
            return None
        return {"id": str(user_id), "name": self.name}
```

### 2.4 推荐最小组合（2025）

- 测试：`pytest`
- 代码风格与静态检查：`ruff`（含 `ruff format`）
- 类型：`mypy`（或 `pyright`）
- 提交钩子：`pre-commit`

### 2.5 安装与运行（uv 优先）

```powershell
pipx install uv || pip install uv
uv pip compile pyproject.toml -o uv.lock
uv pip sync uv.lock
pytest -q --maxfail=1 --disable-warnings
ruff check . && mypy src || true
```

## 3. 质量检查清单（本地副本）

- [迁移/质量检查](./迁移/质量检查.md)

## 4. CI 集成（示例骨架）

- GitHub Actions（最小示例）：

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install uv
        run: pipx install uv || pip install uv
      - name: Resolve
        run: |
          uv pip compile pyproject.toml -o uv.lock
          uv pip sync uv.lock
      - name: Lint & Type
        run: |
          ruff check .
          mypy src || true  # 如项目未准备完全，可先容忍为警告
      - name: Test
        run: pytest -q --maxfail=1 --disable-warnings
```

- GitLab CI（最小示例）：

```yaml
stages: [test]

image: python:3.11-slim

before_script:
  - pip install --no-cache-dir uv || pip install --no-cache-dir uv
  - uv pip compile pyproject.toml -o uv.lock
  - uv pip sync uv.lock

test:
  stage: test
  script:
    - ruff check .
    - mypy src || true
    - pytest -q --maxfail=1 --disable-warnings
```

- Azure Pipelines（最小示例）：

```yaml
trigger: [ main ]

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'
  - script: pipx install uv || pip install uv
    displayName: Install uv
  - script: |
      uv pip compile pyproject.toml -o uv.lock
      uv pip sync uv.lock
    displayName: Resolve deps
  - script: |
      ruff check .
      mypy src || true
      pytest -q --maxfail=1 --disable-warnings
    displayName: Lint & Test
```

## 5. 本地提交钩子（pre-commit）

- 安装：`pip install pre-commit` 或 `uv pip install pre-commit`
- 启用：`pre-commit install && pre-commit install --hook-type commit-msg`
- 配置：仓库根已提供 `.pre-commit-config.yaml`，包含 `ruff/ruff-format/mypy/commitizen`

## 6. 最小示例（可运行）

- 位置：`./examples/minimal_project`
  - 配置：`pyproject.toml`
  - 源码：`src/example/core.py`
  - 测试：`tests/test_core.py`
- 运行指引：
  1) 在示例目录下安装依赖（建议使用 uv/pipx 或 venv）
  2) 运行 `pytest`
  3) 运行 `ruff check .` 与 `mypy src`

> Windows PowerShell 提示：若使用 `uv`，需先通过 `pipx install uv` 或 `pip install uv` 安装；使用 venv 时先激活 `./.venv/Scripts/Activate.ps1`。

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 相关主题：
  - [01-语言与生态/README](../01-语言与生态/README.md)
  - [03-工程与交付/README](../03-工程与交付/README.md)
  - [04-并发与异步/README](../04-并发与异步/README.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)
- 相关规范：[重构规范](../99-上下文与流程/03-重构规范.md)

## 来源与回链（docs → python）

- 质量检查来源：`docs/python_ecosystem/02-高级特性/02-03-质量检查.md` → 本地：[迁移/质量检查](./迁移/质量检查.md)
- 测试策略来源：`docs/refactor/07-实践应用/07-04-测试策略/` → 本地：[迁移/测试策略与方法论](./迁移/测试策略与方法论.md)
