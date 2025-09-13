# 03-工程与交付

聚焦打包、分发、部署与运维接口的工程化流水线。

## 1. 构建与打包

- PEP 517/518、build、uv/pip 构建
- 版本与变更日志（SemVer / Conventional Commits）
- 最小示例：`./examples/minimal_build`
  - 配置：`pyproject.toml`
  - 包：`src/minbuild/__init__.py`
  - 构建命令（本地）：`uv build` 或 `python -m build`

### 1.1 现代项目结构

```python
# 标准项目结构
my-project/
├── pyproject.toml          # 项目配置
├── requirements.txt        # 生产依赖
├── requirements-dev.txt    # 开发依赖
├── .venv/                 # 虚拟环境
├── src/                   # 源代码
│   └── myproject/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/                 # 测试代码
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── docs/                  # 文档
├── .github/               # GitHub Actions
│   └── workflows/
├── .pre-commit-config.yaml # 预提交钩子
└── README.md

# pyproject.toml 配置示例
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-project"
version = "0.1.0"
description = "A modern Python project"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
    "uvicorn[standard]>=0.23.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
    "pre-commit>=3.0.0",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
```

### 1.2 版本管理策略

```python
# 语义化版本控制
# 主版本号.次版本号.修订号
# 1.0.0 -> 1.0.1 (bug修复)
# 1.0.1 -> 1.1.0 (新功能)
# 1.1.0 -> 2.0.0 (破坏性变更)

# 版本管理工具
import tomllib
from pathlib import Path

class VersionManager:
    """版本管理工具"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.pyproject_path = project_path / "pyproject.toml"
    
    def get_current_version(self) -> str:
        """获取当前版本"""
        with open(self.pyproject_path, "rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    
    def bump_version(self, bump_type: str) -> str:
        """版本号递增"""
        current = self.get_current_version()
        major, minor, patch = map(int, current.split("."))
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        new_version = f"{major}.{minor}.{patch}"
        return new_version
```

### 基于 uv 的最小流水

```bash
uv pip compile pyproject.toml -o uv.lock
uv pip sync uv.lock
uv build
uv publish --repository pypi
```

## 2. 发布与分发

- PyPI/内部制品库
- 许可证与SBOM

### 2.1 自动化发布流程

```python
# 发布自动化脚本
import subprocess
import sys
from pathlib import Path

class ReleaseManager:
    """发布管理工具"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
    
    def run_command(self, command: str) -> subprocess.CompletedProcess:
        """运行命令"""
        return subprocess.run(
            command.split(),
            cwd=self.project_path,
            check=True,
            capture_output=True,
            text=True
        )
    
    def build_package(self) -> None:
        """构建包"""
        print("Building package...")
        self.run_command("uv build")
        print("Package built successfully!")
    
    def run_tests(self) -> None:
        """运行测试"""
        print("Running tests...")
        self.run_command("pytest")
        print("Tests passed!")
    
    def run_linting(self) -> None:
        """运行代码检查"""
        print("Running linting...")
        self.run_command("ruff check .")
        self.run_command("mypy src")
        print("Linting passed!")
    
    def publish_to_pypi(self) -> None:
        """发布到PyPI"""
        print("Publishing to PyPI...")
        self.run_command("uv publish --repository pypi")
        print("Published successfully!")
    
    def full_release(self) -> None:
        """完整发布流程"""
        try:
            self.run_tests()
            self.run_linting()
            self.build_package()
            self.publish_to_pypi()
            print("Release completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Release failed: {e}")
            sys.exit(1)
```

### 2.2 多环境部署策略

```python
# 环境配置管理
from pydantic import BaseSettings
from typing import Optional

class DatabaseSettings(BaseSettings):
    """数据库配置"""
    host: str = "localhost"
    port: int = 5432
    database: str
    username: str
    password: str
    pool_size: int = 10
    
    class Config:
        env_prefix = "DB_"

class APISettings(BaseSettings):
    """API配置"""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    workers: int = 1
    
    class Config:
        env_prefix = "API_"

class RedisSettings(BaseSettings):
    """Redis配置"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    
    class Config:
        env_prefix = "REDIS_"

# 环境特定配置
class EnvironmentConfig:
    """环境配置管理"""
    
    @staticmethod
    def get_database_config(env: str) -> DatabaseSettings:
        """获取数据库配置"""
        if env == "development":
            return DatabaseSettings(
                database="myapp_dev",
                username="dev_user",
                password="dev_password"
            )
        elif env == "staging":
            return DatabaseSettings(
                database="myapp_staging",
                username="staging_user",
                password="staging_password"
            )
        elif env == "production":
            return DatabaseSettings(
                database="myapp_prod",
                username="prod_user",
                password="prod_password"
            )
        else:
            raise ValueError(f"Unknown environment: {env}")
```

### 私有制品库发布（示例）

- 配置 `~/.pypirc`：

```ini
[distutils]
index-servers =
    internal

[internal]
repository = https://repo.example.com/api/pypi/python/simple
username = __token__
password = ${PYPI_API_TOKEN}
```

- 使用 uv 发布到私有库：

```bash
# 通过名称选择仓库（与 .pypirc 对应）
uv publish --repository internal
```

- GitLab Package Registry（示例命令）：

```bash
uv publish --repository https://gitlab.example.com/api/v4/projects/<id>/packages/pypi
```

- JFrog Artifactory（示例命令）：

```bash
uv publish --repository https://artifactory.example.com/artifactory/api/pypi/python-local
```

> 建议：凭据通过 CI Secret 注入环境变量，避免写入仓库。

### SBOM 生成与签名

```bash
# 生成 SBOM（CycloneDX/Syft）
syft packages file:dist/*.whl -o cyclonedx-json > sbom.json

# 制品签名（Cosign），需事先配置密钥或 OIDC
cosign sign-blob --output-signature dist.sig dist/*.whl

# 验证
cosign verify-blob --signature dist.sig dist/*.whl
```

## 3. 运行与部署

- 容器化与镜像优化
- 配置与密钥管理

## 4. 观测与回滚

- 日志/指标/追踪
- 升级/回滚策略

## 5. 模板与参考

- 最小工程模板/部署脚本（预留）
- CI：GitHub Actions 示例

```yaml
# .github/workflows/release.yml（示例）
name: release
on:
  push:
    tags:
      - 'v*.*.*'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install uv
        run: pipx install uv || pip install uv
      - name: Resolve & build
        run: |
          uv pip compile pyproject.toml -o uv.lock
          uv pip sync uv.lock
          uv build
      - name: Publish
        env:
          PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
        run: uv publish --repository pypi
```

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 相关主题：
  - [01-语言与生态/README](../01-语言与生态/README.md)
  - [02-测试与质量/README](../02-测试与质量/README.md)
  - [04-并发与异步/README](../04-并发与异步/README.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)
- 相关规范：[重构规范](../99-上下文与流程/03-重构规范.md)

## 来源与回链（docs → python）

- 项目管理来源：`docs/model/Programming_Language/python_project_management.md` → 本地：[迁移/项目管理](./迁移/项目管理.md)
- 构建打包来源：`docs/refactor/07-实践应用/07-05-部署运维/` → 本地：[迁移/构建与打包](./迁移/构建与打包.md)
