# uv - 极速 Python 包管理器

**基于 Rust 的下一代 Python 包管理工具 | 10-100x 速度提升**-

---

## 🚀 uv 简介

`uv` 是由 Astral 开发的**超高速 Python 包管理器和项目管理工具**，使用 Rust 编写，性能远超传统工具。

### 核心优势

- **🚄 极速**：比 pip 快 10-100 倍
- **🔒 可靠**：完整的依赖解析和锁定
- **🎯 现代**：支持 Python 3.12/3.13
- **📦 全面**：替代 pip, pip-tools, poetry, pyenv
- **🔧 简单**：零配置开箱即用

---

## 📦 安装 uv

### macOS/Linux

```bash
# 使用官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 homebrew
brew install uv
```

### Windows

```powershell
# 使用 PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 scoop
scoop install uv
```

### 通过 pip

```bash
pip install uv
```

### 验证安装

```bash
uv --version
# uv 0.5.0
```

---

## 🎯 快速开始

### 创建新项目

```bash
# 创建项目
uv init my-project
cd my-project

# 项目结构
my-project/
├── .python-version      # Python 版本
├── pyproject.toml       # 项目配置
├── README.md
└── src/
    └── my_project/
        └── __init__.py
```

### 安装 Python

```bash
# 安装 Python 3.12
uv python install 3.12

# 列出可用版本
uv python list

# 设置项目 Python 版本
uv python pin 3.12
```

### 添加依赖

```bash
# 添加运行时依赖
uv add fastapi uvicorn[standard]

# 添加开发依赖
uv add --dev pytest mypy ruff

# 从 requirements.txt 安装
uv pip install -r requirements.txt
```

### 运行项目

```bash
# 运行 Python 脚本
uv run python main.py

# 运行模块
uv run python -m myapp

# 激活虚拟环境
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
```

---

## 📋 核心命令

### 项目管理

```bash
# 初始化项目
uv init [project-name]

# 同步依赖（创建/更新虚拟环境）
uv sync

# 锁定依赖
uv lock

# 构建项目
uv build

# 发布到 PyPI
uv publish
```

### 依赖管理

```bash
# 添加依赖
uv add package-name

# 添加特定版本
uv add "package-name==1.2.3"

# 添加版本范围
uv add "package-name>=1.0,<2.0"

# 移除依赖
uv remove package-name

# 更新依赖
uv lock --upgrade

# 更新特定包
uv lock --upgrade-package package-name
```

### Python 版本管理

```bash
# 安装 Python
uv python install 3.12
uv python install 3.13

# 列出已安装版本
uv python list

# 设置项目版本
uv python pin 3.12

# 删除 Python 版本
uv python uninstall 3.12
```

### pip 兼容命令

```bash
# 安装包
uv pip install package-name

# 从 requirements.txt
uv pip install -r requirements.txt

# 卸载包
uv pip uninstall package-name

# 列出已安装包
uv pip list

# 显示包信息
uv pip show package-name

# 冻结依赖
uv pip freeze > requirements.txt
```

---

## ⚙️ 项目配置

### pyproject.toml 完整示例

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A modern Python project"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["python", "modern", "fast"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

# 运行时依赖
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.9.0",
    "sqlalchemy>=2.0.0",
]

# 可选依赖组
[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=5.0.0",
    "pytest-asyncio>=0.24.0",
    "mypy>=1.11.0",
    "ruff>=0.6.0",
]
docs = [
    "mkdocs>=1.6.0",
    "mkdocs-material>=9.5.0",
]
test = [
    "pytest>=8.3.0",
    "hypothesis>=6.112.0",
    "faker>=30.0.0",
]

# 项目入口点
[project.scripts]
my-cli = "my_project.cli:main"

[project.urls]
Homepage = "https://github.com/username/my-project"
Documentation = "https://my-project.readthedocs.io"
Repository = "https://github.com/username/my-project.git"
Issues = "https://github.com/username/my-project/issues"

# 构建系统
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# uv 配置
[tool.uv]
dev-dependencies = [
    "pre-commit>=3.8.0",
    "black>=24.8.0",
]

# 包源
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cu121"
explicit = true

# pip 约束
[tool.uv.pip]
# 使用系统 Python
system = false
# 生成 uv.lock
generate-hashes = true

# 工作区配置
[tool.uv.workspace]
members = ["packages/*"]
```

---

## 🔒 依赖锁定

### uv.lock 文件

uv 自动生成 `uv.lock` 文件，确保依赖的可重现性：

```toml
# uv.lock (自动生成，不要手动编辑)
[[package]]
name = "fastapi"
version = "0.115.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "pydantic", version = "2.9.0" },
    { name = "starlette", version = "0.38.0" },
]
wheels = [
    { url = "...", hash = "sha256:..." },
]
```

### 锁定最佳实践

```bash
# 首次安装时自动创建 lock 文件
uv sync

# 更新所有依赖到最新版本
uv lock --upgrade

# 更新特定包
uv lock --upgrade-package fastapi

# 重新解析依赖（不升级）
uv lock

# 验证 lock 文件
uv sync --locked
```

---

## 🌍 工作区管理

### Monorepo 结构

```text
my-workspace/
├── pyproject.toml          # 根配置
├── uv.lock                 # 锁定文件
└── packages/
    ├── api/
    │   ├── pyproject.toml
    │   └── src/api/
    ├── core/
    │   ├── pyproject.toml
    │   └── src/core/
    └── cli/
        ├── pyproject.toml
        └── src/cli/
```

### 根 pyproject.toml

```toml
[tool.uv.workspace]
members = [
    "packages/api",
    "packages/core",
    "packages/cli",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "mypy>=1.11.0",
]
```

### 包间依赖

```toml
# packages/api/pyproject.toml
[project]
name = "my-api"
dependencies = [
    "my-core",  # 工作区内的包
    "fastapi>=0.115.0",
]
```

---

## ⚡ 性能对比

### 安装速度

```bash
# 测试环境：FastAPI + 所有依赖 (约 50 个包)

pip install fastapi[all]
# Time: ~45 seconds

poetry install
# Time: ~60 seconds

uv pip install fastapi[all]
# Time: ~2 seconds (25x faster!)

uv sync
# Time: ~1 second (45x faster!)
```

### 依赖解析

```bash
# 复杂依赖树（100+ 包）

pip install
# Time: ~120 seconds

poetry install
# Time: ~180 seconds

uv sync
# Time: ~3 seconds (40-60x faster!)
```

---

## 🎨 高级功能

### 1. 虚拟环境管理

```bash
# 创建虚拟环境
uv venv

# 指定 Python 版本
uv venv --python 3.12

# 指定路径
uv venv .custom-venv

# 使用系统 Python
uv venv --system-site-packages
```

### 2. 缓存管理

```bash
# 查看缓存信息
uv cache dir

# 清理缓存
uv cache clean

# 清理特定包缓存
uv cache clean fastapi
```

### 3. 工具运行

```bash
# 运行一次性工具（不安装）
uv run --with ruff ruff check .
uv run --with mypy mypy src/

# 运行特定版本
uv run --with "black==24.8.0" black .
```

### 4. 脚本执行

```bash
# inline script metadata
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests<3",
#     "rich",
# ]
# ///

import requests
from rich import print

response = requests.get("https://api.github.com")
print(response.json())
```

```bash
# 运行脚本（自动管理依赖）
uv run script.py
```

---

## 🔧 与其他工具集成

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
      
      - name: Set up Python
        run: uv python install 3.12
      
      - name: Install dependencies
        run: uv sync --all-extras --dev
      
      - name: Run tests
        run: uv run pytest
      
      - name: Run linters
        run: |
          uv run ruff check .
          uv run mypy src/
```

### Docker

```dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy source code
COPY . .

# Run application
CMD ["uv", "run", "python", "-m", "myapp"]
```

### Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: uv-lock
        name: uv lock
        entry: uv lock
        language: system
        files: ^pyproject\.toml$
        pass_filenames: false
```

---

## 💡 最佳实践

### 1. 版本约束

```toml
# ✅ 推荐：使用语义化版本约束
dependencies = [
    "fastapi>=0.115.0,<1.0.0",  # 兼容性范围
    "pydantic>=2.9.0,<3.0.0",
]

# ❌ 避免：过于宽松或过于严格
dependencies = [
    "fastapi",           # 太宽松
    "pydantic==2.9.0",   # 太严格
]
```

### 2. 分离开发依赖

```toml
# 运行时依赖
dependencies = [
    "fastapi>=0.115.0",
    "sqlalchemy>=2.0.0",
]

# 开发依赖
[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "mypy>=1.11.0",
    "ruff>=0.6.0",
]
```

### 3. 使用 extras

```toml
[project.optional-dependencies]
# 数据库支持
db = [
    "sqlalchemy>=2.0.0",
    "psycopg2-binary>=2.9.0",
]
# Redis 支持
redis = [
    "redis>=5.0.0",
]
# 完整功能
all = [
    "my-project[db,redis]",
]
```

```bash
# 安装特定 extras
uv sync --extra db
uv sync --extra redis
uv sync --all-extras
```

### 4. 锁定文件管理

```bash
# 开发环境：保持依赖更新
uv lock --upgrade

# CI/CD：使用锁定版本
uv sync --frozen

# 库项目：不提交 uv.lock
echo "uv.lock" >> .gitignore

# 应用项目：提交 uv.lock 确保一致性
git add uv.lock
```

---

## 🔄 迁移指南

### 从 pip 迁移

```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 从 requirements.txt 迁移
uv add $(cat requirements.txt)

# 或使用 uv pip
uv pip install -r requirements.txt
uv pip freeze | uv add --requirements -
```

### 从 poetry 迁移

```bash
# 1. 导出依赖
poetry export -f requirements.txt --output requirements.txt

# 2. 创建 uv 项目
uv init .
uv add $(poetry show --no-dev | awk '{print $1}')
uv add --dev $(poetry show --only=dev | awk '{print $1}')
```

### 从 pipenv 迁移

```bash
# 1. 导出依赖
pipenv requirements > requirements.txt
pipenv requirements --dev > requirements-dev.txt

# 2. 迁移到 uv
uv add $(cat requirements.txt)
uv add --dev $(cat requirements-dev.txt)
```

---

## 📊 常见问题

### Q: uv 与 pip 有什么区别？

A: uv 是 pip 的替代品，但更快、更可靠：

- **速度**：10-100x 更快
- **依赖解析**：完整的 SAT 求解器
- **锁定文件**：确保可重现构建
- **Python 管理**：内置 Python 版本管理

### Q: 如何在 CI/CD 中使用 uv？

A: 推荐使用 `--frozen` 标志：

```bash
uv sync --frozen  # 使用精确的锁定版本
uv run pytest     # 运行测试
```

### Q: uv.lock 应该提交到版本控制吗？

A:

- **应用/服务**：应该提交（确保部署一致性）
- **库/包**：不应该提交（允许消费者选择版本）

### Q: 如何处理私有包仓库？

A:

```toml
[[tool.uv.index]]
name = "private"
url = "https://private-repo.example.com/simple"
```

---

## 🔗 相关资源

- [uv 官方文档](https://github.com/astral-sh/uv)
- [uv GitHub 仓库](https://github.com/astral-sh/uv)
- [Astral 官网](https://astral.sh/)
- [Python 打包用户指南](https://packaging.python.org/)

---

**使用 uv，让 Python 开发飞起来！** 🚀✨
