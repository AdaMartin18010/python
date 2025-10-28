# Python Poetry 现代包管理

**Poetry完全使用指南**

---

## 📋 目录

- [Poetry简介](#Poetry简介)
- [项目管理](#项目管理)
- [依赖管理](#依赖管理)
- [发布包](#发布包)
- [高级特性](#高级特性)

---

## Poetry简介

### 什么是Poetry

```bash
# Poetry: 现代Python包管理和依赖管理工具

# 特点:
# 1. 依赖解析: 自动解决版本冲突
# 2. 虚拟环境: 自动创建和管理
# 3. 锁文件: poetry.lock确保可重现
# 4. pyproject.toml: 现代配置文件
# 5. 发布简单: 一键发布到PyPI

# 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 或使用pip (不推荐)
pip install poetry

# 或使用pipx (推荐)
pipx install poetry

# 检查版本
poetry --version
# Poetry (version 1.7.0)
```

### 配置Poetry

```bash
# 查看配置
poetry config --list

# 设置配置
poetry config virtualenvs.in-project true  # 在项目目录创建.venv
poetry config virtualenvs.create true      # 自动创建虚拟环境

# 国内镜像
poetry source add --priority=primary tsinghua https://pypi.tuna.tsinghua.edu.cn/simple/

# 配置文件位置:
# Linux/macOS: ~/.config/pypoetry/config.toml
# Windows: %APPDATA%\pypoetry\config.toml
```

---

## 项目管理

### 创建新项目

```bash
# 创建新项目
poetry new my-project

# 生成的结构:
# my-project/
#   ├── pyproject.toml
#   ├── README.md
#   ├── my_project/
#   │   └── __init__.py
#   └── tests/
#       └── __init__.py

# 创建项目 (不生成代码目录)
poetry new my-project --name my_app

# 在现有目录初始化
cd existing-project
poetry init
# 交互式配置pyproject.toml
```

### pyproject.toml

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "A modern Python project"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
license = "MIT"
homepage = "https://github.com/user/my-project"
repository = "https://github.com/user/my-project"
documentation = "https://my-project.readthedocs.io"
keywords = ["python", "example"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
]

# 依赖
[tool.poetry.dependencies]
python = "^3.12"
requests = "^2.31.0"
fastapi = "^0.104.0"

# 开发依赖
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.10.0"
ruff = "^0.1.0"
mypy = "^1.6.0"

# 可选依赖组
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.5.0"
mkdocs-material = "^9.4.0"

# 额外依赖 (extras)
[tool.poetry.extras]
mysql = ["pymysql", "cryptography"]
postgres = ["psycopg2-binary"]

# 脚本
[tool.poetry.scripts]
my-app = "my_project.cli:main"

# 构建系统
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## 依赖管理

### 添加依赖

```bash
# 1. 添加生产依赖
poetry add requests

# 2. 添加特定版本
poetry add requests@^2.31.0
poetry add "requests>=2.28.0,<3.0.0"

# 3. 添加最新版本
poetry add requests@latest

# 4. 添加开发依赖
poetry add --group dev pytest black ruff

# 5. 添加可选依赖
poetry add --optional pymysql

# 6. 从Git安装
poetry add git+https://github.com/user/repo.git

# 7. 从本地路径
poetry add ./packages/my-package

# 8. 添加多个包
poetry add requests flask numpy

# 9. 允许预发布版本
poetry add --allow-prereleases package-name
```

### 更新依赖

```bash
# 1. 更新所有依赖
poetry update

# 2. 更新特定包
poetry update requests

# 3. 更新多个包
poetry update requests flask

# 4. 只更新锁文件 (不安装)
poetry update --lock

# 5. 预览更新
poetry show --outdated
```

### 移除依赖

```bash
# 移除依赖
poetry remove requests

# 移除开发依赖
poetry remove --group dev pytest

# 移除多个依赖
poetry remove requests flask numpy
```

### 查看依赖

```bash
# 1. 列出所有依赖
poetry show

# 2. 查看依赖树
poetry show --tree

# 3. 查看特定包
poetry show requests

# 输出:
# name         : requests
# version      : 2.31.0
# description  : Python HTTP for Humans.
# dependencies
#  - certifi >=2017.4.17
#  - charset-normalizer >=2,<4
#  - idna >=2.5,<4
#  - urllib3 >=1.21.1,<3

# 4. 只显示生产依赖
poetry show --only main

# 5. 只显示开发依赖
poetry show --only dev

# 6. 显示过时的包
poetry show --outdated

# 7. 显示最新版本
poetry show --latest
```

---

## 虚拟环境

### 环境管理

```bash
# 1. 创建虚拟环境
poetry install

# 2. 激活虚拟环境
# Linux/macOS
source $(poetry env info --path)/bin/activate

# Windows
& ((poetry env info --path) + "\Scripts\activate.ps1")

# 3. 在虚拟环境中运行命令
poetry run python script.py
poetry run pytest
poetry run black .

# 4. 进入shell
poetry shell

# 5. 查看环境信息
poetry env info

# 输出:
# Virtualenv
# Python:         3.12.0
# Implementation: CPython
# Path:           /path/to/.venv
# Executable:     /path/to/.venv/bin/python

# 6. 列出环境
poetry env list

# 7. 移除环境
poetry env remove python3.12
poetry env remove --all

# 8. 使用特定Python版本
poetry env use python3.11
poetry env use /usr/bin/python3.12
```

### 安装选项

```bash
# 1. 只安装生产依赖
poetry install --only main

# 2. 不安装开发依赖
poetry install --without dev

# 3. 安装特定组
poetry install --with docs

# 4. 安装额外依赖
poetry install --extras "mysql postgres"

# 5. 同步环境 (移除不需要的包)
poetry install --sync

# 6. 不安装当前项目
poetry install --no-root

# 7. 编译安装 (开发模式)
poetry install
# 等价于 pip install -e .
```

---

## 发布包

### 构建

```bash
# 构建包
poetry build

# 输出:
# Building my-project (0.1.0)
#   - Building sdist
#   - Built my-project-0.1.0.tar.gz
#   - Building wheel
#   - Built my_project-0.1.0-py3-none-any.whl

# 生成的文件:
# dist/
#   ├── my-project-0.1.0.tar.gz
#   └── my_project-0.1.0-py3-none-any.whl

# 只构建wheel
poetry build --format wheel

# 只构建sdist
poetry build --format sdist
```

### 发布到PyPI

```bash
# 1. 配置PyPI凭证
poetry config pypi-token.pypi your-api-token

# 2. 发布
poetry publish

# 3. 构建并发布
poetry publish --build

# 4. 发布到测试PyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi your-test-token
poetry publish -r testpypi

# 5. 预览发布 (dry-run)
poetry publish --dry-run
```

### 版本管理

```bash
# 查看当前版本
poetry version

# 版本号规则
poetry version patch    # 0.1.0 -> 0.1.1
poetry version minor    # 0.1.0 -> 0.2.0
poetry version major    # 0.1.0 -> 1.0.0

# 预发布版本
poetry version prepatch # 0.1.0 -> 0.1.1a0
poetry version preminor # 0.1.0 -> 0.2.0a0
poetry version premajor # 0.1.0 -> 1.0.0a0

# 手动设置版本
poetry version 1.2.3
```

---

## 高级特性

### 依赖组

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.10.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.5.0"

[tool.poetry.group.test.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
```

```bash
# 安装特定组
poetry install --with docs
poetry install --with test

# 不安装特定组
poetry install --without dev

# 只安装特定组
poetry install --only docs
```

### 插件系统

```bash
# 安装插件
poetry self add poetry-plugin-export

# 使用插件导出requirements.txt
poetry export -f requirements.txt -o requirements.txt --without-hashes

# 导出包含开发依赖
poetry export -f requirements.txt -o requirements-dev.txt --with dev

# 其他常用插件:
# - poetry-dynamic-versioning: 动态版本
# - poetry-bumpversion: 版本管理
# - poetry-plugin-bundle: 打包工具
```

### Monorepo支持

```toml
# 项目A
[tool.poetry]
name = "project-a"

[tool.poetry.dependencies]
project-b = { path = "../project-b", develop = true }

# 项目B
[tool.poetry]
name = "project-b"
```

### 私有仓库

```toml
[[tool.poetry.source]]
name = "private"
url = "https://pypi.company.com/simple"
priority = "primary"
```

```bash
# 配置私有仓库凭证
poetry config http-basic.private username password

# 或使用环境变量
export POETRY_HTTP_BASIC_PRIVATE_USERNAME=username
export POETRY_HTTP_BASIC_PRIVATE_PASSWORD=password
```

---

## 📚 核心要点

### Poetry优势

- ✅ **依赖解析**: 自动解决版本冲突
- ✅ **锁文件**: 确保可重现构建
- ✅ **虚拟环境**: 自动创建管理
- ✅ **pyproject.toml**: 现代配置
- ✅ **发布简单**: 一键发布

### 项目管理

- ✅ **poetry new**: 创建新项目
- ✅ **poetry init**: 初始化现有项目
- ✅ **pyproject.toml**: 项目配置
- ✅ **版本管理**: poetry version

### 依赖管理

- ✅ **poetry add**: 添加依赖
- ✅ **poetry update**: 更新依赖
- ✅ **poetry remove**: 移除依赖
- ✅ **poetry show**: 查看依赖
- ✅ **依赖组**: 灵活组织

### 虚拟环境

- ✅ **poetry install**: 安装依赖
- ✅ **poetry run**: 运行命令
- ✅ **poetry shell**: 进入shell
- ✅ **poetry env**: 环境管理

### 发布

- ✅ **poetry build**: 构建包
- ✅ **poetry publish**: 发布到PyPI
- ✅ **poetry version**: 版本管理
- ✅ **插件**: 扩展功能

### 最佳实践

- ✅ 使用pyproject.toml统一配置
- ✅ 提交poetry.lock到版本控制
- ✅ 使用依赖组组织依赖
- ✅ 配置virtualenvs.in-project
- ✅ CI/CD缓存.venv目录

---

**掌握Poetry，现代化Python项目管理！** 🎨✨

**相关文档**:
- [01-pip-basics.md](01-pip-basics.md) - pip基础
- [03-uv.md](03-uv.md) - uv快速包管理器

**最后更新**: 2025年10月28日

