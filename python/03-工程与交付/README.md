# 03-工程与交付（2025年10月标准）

聚焦打包、分发、部署与运维接口的现代化工程流水线。

## 0. 2025年工程工具栈

### 0.1 核心工具（2025推荐）

| 工具 | 版本 | 用途 | 速度 | 推荐度 |
|------|------|------|------|--------|
| **uv** | 0.4+ | 包管理&构建 | 极快 | ⭐⭐⭐⭐⭐ |
| **hatchling** | 1.25+ | 构建后端 | 快 | ⭐⭐⭐⭐⭐ |
| **twine** | 5.1+ | PyPI发布 | 中 | ⭐⭐⭐⭐⭐ |
| **docker** | 27+ | 容器化 | 中 | ⭐⭐⭐⭐⭐ |
| **kubernetes** | 1.30+ | 容器编排 | 中 | ⭐⭐⭐⭐⭐ |
| **GitHub Actions** | - | CI/CD | 快 | ⭐⭐⭐⭐⭐ |

### 0.2 构建工具对比（2025）

| 特性 | uv | poetry | setuptools | hatch |
|------|-----|--------|-----------|-------|
| 速度 | ⚡⚡⚡ | ⚡⚡ | ⚡ | ⚡⚡ |
| 依赖解析 | 极快 | 快 | 慢 | 快 |
| 虚拟环境 | ✅ | ✅ | ❌ | ✅ |
| 锁文件 | ✅ | ✅ | ❌ | ✅ |
| PEP 517支持 | ✅ | ✅ | ✅ | ✅ |
| 推荐指数 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### 0.3 快速开始

```bash
# 安装 uv（推荐）
pip install uv

# 创建新项目
uv init my-project
cd my-project

# 构建项目
uv build

# 发布到 PyPI
uv publish
```

## 1. 构建与打包（2025最佳实践）

- PEP 517/518、PEP 621 现代化打包
- uv/hatchling 构建工具链
- 版本与变更日志（SemVer / Conventional Commits）
- 多平台构建（wheels）
- 源码分发（sdist）
- 最小示例：`./examples/minimal_build`
  - 配置：`pyproject.toml`
  - 包：`src/minbuild/__init__.py`
  - 构建命令：`uv build` (推荐) 或 `python -m build`

### 1.1 现代项目结构（2025标准）

```bash
# 2025年推荐项目结构
my-project/
├── pyproject.toml          # 统一配置文件（PEP 621）
├── uv.lock                 # uv依赖锁文件（可选）
├── README.md               # 项目说明
├── LICENSE                 # 许可证
├── .gitignore              # Git忽略文件
├── .pre-commit-config.yaml # pre-commit配置
├── Dockerfile              # Docker镜像
├── docker-compose.yml      # Docker Compose
├── .github/                # GitHub配置
│   └── workflows/
│       ├── ci.yml          # CI流水线
│       └── release.yml     # 发布流水线
├── src/                    # 源代码（PEP 420）
│   └── myproject/
│       ├── __init__.py     # 包初始化
│       ├── __main__.py     # CLI入口
│       ├── core.py         # 核心功能
│       ├── api.py          # API路由
│       └── config.py       # 配置管理
├── tests/                  # 测试代码
│   ├── conftest.py         # pytest配置
│   ├── test_core.py        # 单元测试
│   ├── test_api.py         # API测试
│   └── test_integration.py # 集成测试
├── docs/                   # 文档
│   ├── index.md
│   ├── api.md
│   └── deployment.md
├── scripts/                # 辅助脚本
│   ├── setup.sh
│   └── deploy.sh
└── examples/               # 示例代码
    └── basic_usage.py

# pyproject.toml 配置示例（2025标准）
[build-system]
requires = ["hatchling>=1.25.0"]
build-backend = "hatchling.build"

[project]
name = "my-project"
version = "1.0.0"
description = "A modern Python project following 2025 best practices"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.12"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["python", "modern", "2025"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]

dependencies = [
    "fastapi>=0.115.0",
    "pydantic>=2.9.0",
    "uvicorn[standard]>=0.30.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=5.0.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.6.0",
    "mypy>=1.11.0",
    "pre-commit>=3.8.0",
]

[project.urls]
Homepage = "https://github.com/username/my-project"
Documentation = "https://my-project.readthedocs.io"
Repository = "https://github.com/username/my-project"
Issues = "https://github.com/username/my-project/issues"
Changelog = "https://github.com/username/my-project/blob/main/CHANGELOG.md"

[project.scripts]
my-project = "myproject.__main__:main"

[tool.hatchling.build.targets.wheel]
packages = ["src/myproject"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.mypy]
python_version = "3.12"
strict = true

[tool.uv]
managed = true
dev-dependencies = [
    "pytest>=8.3.0",
    "ruff>=0.6.0",
    "mypy>=1.11.0",
]
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

### 1.3 基于 uv 的现代化构建流水线（2025推荐）

```bash
#!/bin/bash
# build.sh - 现代化构建脚本

set -e  # 遇到错误立即退出

echo "🚀 开始构建流程..."

# 1. 代码质量检查
echo "📝 运行代码质量检查..."
uv run ruff check .
uv run ruff format --check .
uv run mypy .

# 2. 运行测试
echo "🧪 运行测试..."
uv run pytest --cov --cov-report=term-missing

# 3. 构建包
echo "📦 构建包..."
uv build

# 4. 检查包
echo "✅ 检查包..."
uv run twine check dist/*

# 5. 列出构建产物
echo "📋 构建产物:"
ls -lh dist/

echo "✅ 构建完成!"
```

### 1.4 完整发布流程（2025标准）

```bash
# 发布到 PyPI
#!/bin/bash
# release.sh - 发布脚本

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh <version>"
    exit 1
fi

echo "🚀 开始发布 v$VERSION..."

# 1. 更新版本号
echo "📝 更新版本号..."
# 使用 sed 或 Python 脚本更新 pyproject.toml 中的版本

# 2. 生成变更日志
echo "📋 生成变更日志..."
git cliff --tag v$VERSION > CHANGELOG.md

# 3. 提交版本更新
git add pyproject.toml CHANGELOG.md
git commit -m "chore: release v$VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"

# 4. 运行完整构建
./build.sh

# 5. 发布到 PyPI
echo "📤 发布到 PyPI..."
uv publish

# 6. 推送到远程
git push origin main --tags

echo "✅ 发布完成! 🎉"
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
