# Python 包发布与分发

**PyPI发布完全指南**

---

## 📋 目录

- [包发布流程](#包发布流程)
- [项目配置](#项目配置)
- [构建包](#构建包)
- [发布到PyPI](#发布到PyPI)
- [最佳实践](#最佳实践)

---

## 包发布流程

### 发布概览

```bash
# Python包发布流程:
# 1. 准备项目结构
# 2. 配置pyproject.toml
# 3. 构建包 (sdist + wheel)
# 4. 测试安装
# 5. 发布到Test PyPI
# 6. 验证测试
# 7. 发布到PyPI
# 8. 验证发布

# 工具选择:
# - setuptools (传统)
# - poetry (现代,推荐)
# - flit (简单)
# - hatch (新兴)
```

### 项目结构

```bash
# 标准Python包结构
my-package/
  ├── src/
  │   └── my_package/
  │       ├── __init__.py
  │       ├── core.py
  │       └── utils.py
  ├── tests/
  │   ├── __init__.py
  │   └── test_core.py
  ├── docs/
  │   └── index.md
  ├── pyproject.toml       # 项目配置
  ├── README.md            # 项目说明
  ├── LICENSE              # 许可证
  ├── CHANGELOG.md         # 变更日志
  └── .gitignore

# __init__.py
"""My Package

A simple example package.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "you@example.com"

from .core import main_function

__all__ = ["main_function"]
```

---

## 项目配置

### pyproject.toml (现代方式)

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description of the package"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
keywords = ["example", "package"]
authors = [
  {name = "Your Name", email = "you@example.com"}
]
maintainers = [
  {name = "Your Name", email = "you@example.com"}
]
classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "Topic :: Software Development :: Libraries :: Python Modules",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.8",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
]

dependencies = [
  "requests>=2.28.0,<3.0.0",
  "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=7.4.0",
  "black>=23.10.0",
  "ruff>=0.1.0",
  "mypy>=1.6.0",
]
docs = [
  "mkdocs>=1.5.0",
  "mkdocs-material>=9.4.0",
]
all = ["my-package[dev,docs]"]

[project.urls]
Homepage = "https://github.com/user/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/user/my-package"
"Bug Tracker" = "https://github.com/user/my-package/issues"
Changelog = "https://github.com/user/my-package/blob/main/CHANGELOG.md"

[project.scripts]
my-cli = "my_package.cli:main"

[project.entry-points."my_package.plugins"]
plugin1 = "my_package.plugins:plugin1"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
my_package = ["data/*.json", "templates/*.html"]
```

### Poetry配置

```toml
[tool.poetry]
name = "my-package"
version = "0.1.0"
description = "A short description"
authors = ["Your Name <you@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/user/my-package"
repository = "https://github.com/user/my-package"
documentation = "https://my-package.readthedocs.io"
keywords = ["example", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.0"
pydantic = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.10.0"
ruff = "^0.1.0"
mypy = "^1.6.0"

[tool.poetry.scripts]
my-cli = "my_package.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## 构建包

### 使用build构建

```bash
# 安装build
pip install build

# 构建包
python -m build

# 输出:
# dist/
#   ├── my_package-0.1.0.tar.gz        # source distribution
#   └── my_package-0.1.0-py3-none-any.whl  # wheel

# 只构建wheel
python -m build --wheel

# 只构建sdist
python -m build --sdist

# 指定输出目录
python -m build --outdir custom_dist/
```

### 使用setuptools构建

```bash
# 传统方式 (不推荐)
python setup.py sdist bdist_wheel

# 清理构建文件
python setup.py clean --all
rm -rf build/ dist/ *.egg-info
```

### 使用Poetry构建

```bash
# Poetry构建
poetry build

# 输出:
# dist/
#   ├── my-package-0.1.0.tar.gz
#   └── my_package-0.1.0-py3-none-any.whl

# 只构建wheel
poetry build --format wheel

# 只构建sdist
poetry build --format sdist
```

### 测试本地安装

```bash
# 从本地wheel安装
pip install dist/my_package-0.1.0-py3-none-any.whl

# 从本地sdist安装
pip install dist/my_package-0.1.0.tar.gz

# 可编辑模式安装
pip install -e .

# 测试包功能
python -c "import my_package; print(my_package.__version__)"

# 测试命令行工具
my-cli --help
```

---

## 发布到PyPI

### 配置账号

```bash
# 1. 注册PyPI账号
# https://pypi.org/account/register/

# 2. 注册Test PyPI账号 (用于测试)
# https://test.pypi.org/account/register/

# 3. 生成API Token
# PyPI -> Account Settings -> API tokens
# 创建token,范围选择"Entire account"或特定项目

# 4. 配置~/.pypirc
cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-...your-token...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-...your-test-token...
EOF

chmod 600 ~/.pypirc
```

### 使用twine上传

```bash
# 安装twine
pip install twine

# 1. 检查包
twine check dist/*

# 2. 上传到Test PyPI
twine upload --repository testpypi dist/*

# 3. 从Test PyPI安装测试
pip install --index-url https://test.pypi.org/simple/ my-package

# 4. 测试功能
python -c "import my_package; print(my_package.__version__)"

# 5. 上传到PyPI
twine upload dist/*

# 6. 从PyPI安装验证
pip install my-package

# 只上传特定版本
twine upload dist/my_package-0.1.0*
```

### 使用Poetry发布

```bash
# 配置Poetry token
poetry config pypi-token.pypi pypi-...your-token...
poetry config pypi-token.testpypi pypi-...your-test-token...

# 配置Test PyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/

# 构建并上传到Test PyPI
poetry publish -r testpypi --build

# 构建并上传到PyPI
poetry publish --build

# 或分步操作
poetry build
poetry publish

# 预览发布 (dry-run)
poetry publish --dry-run
```

---

## 最佳实践

### 版本管理

```python
"""
版本管理策略
"""

# 1. 语义化版本
# MAJOR.MINOR.PATCH
# 0.1.0 -> 0.1.1 (patch: bug修复)
# 0.1.1 -> 0.2.0 (minor: 新功能)
# 0.2.0 -> 1.0.0 (major: 破坏性变更)

# 2. 版本号存储位置

# 方法1: __init__.py
# src/my_package/__init__.py
__version__ = "0.1.0"

# 方法2: pyproject.toml
# [project]
# version = "0.1.0"

# 方法3: 单独的version.py
# src/my_package/version.py
VERSION = "0.1.0"

# 方法4: 动态版本 (poetry-dynamic-versioning)
# 从Git标签自动生成

# 3. 更新版本
# poetry version patch  # 0.1.0 -> 0.1.1
# poetry version minor  # 0.1.0 -> 0.2.0
# poetry version major  # 0.1.0 -> 1.0.0

# 4. 预发布版本
# 0.1.0a1 (alpha)
# 0.1.0b1 (beta)
# 0.1.0rc1 (release candidate)
```

### 文档

```markdown
# README.md

# My Package

[![PyPI version](https://badge.fury.io/py/my-package.svg)](https://badge.fury.io/py/my-package)
[![Python versions](https://img.shields.io/pypi/pyversions/my-package.svg)](https://pypi.org/project/my-package/)
[![License](https://img.shields.io/pypi/l/my-package.svg)](https://github.com/user/my-package/blob/main/LICENSE)

A short description of the package.

## Installation

```bash
pip install my-package
```

## Quick Start

```python
from my_package import main_function

result = main_function()
print(result)
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Documentation

Full documentation: https://my-package.readthedocs.io

## Development

```bash
# Clone repository
git clone https://github.com/user/my-package.git
cd my-package

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
ruff check .
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).
```

### CI/CD自动发布

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Check package
      run: twine check dist/*
    
    - name: Publish to Test PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.TEST_PYPI_API_TOKEN }}
      run: |
        twine upload --repository testpypi dist/*
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*
```

### 包清单

```txt
# MANIFEST.in
# 包含额外文件到sdist

include README.md
include LICENSE
include CHANGELOG.md
include pyproject.toml

recursive-include src/my_package/data *.json
recursive-include src/my_package/templates *.html

global-exclude __pycache__
global-exclude *.py[co]
```

---

## 📚 核心要点

### 发布流程

- ✅ **配置**: pyproject.toml
- ✅ **构建**: python -m build
- ✅ **测试**: Test PyPI
- ✅ **发布**: twine upload
- ✅ **验证**: pip install测试

### 项目配置

- ✅ **pyproject.toml**: 现代配置
- ✅ **dependencies**: 依赖列表
- ✅ **classifiers**: 包分类
- ✅ **scripts**: 命令行工具
- ✅ **urls**: 项目链接

### 构建

- ✅ **sdist**: 源码分发
- ✅ **wheel**: 预构建包
- ✅ **python -m build**: 推荐工具
- ✅ **poetry build**: Poetry方式

### 发布

- ✅ **PyPI**: 正式发布
- ✅ **Test PyPI**: 测试发布
- ✅ **twine**: 上传工具
- ✅ **API Token**: 安全认证

### 最佳实践

- ✅ 语义化版本
- ✅ 完善的README
- ✅ MIT/Apache等开源协议
- ✅ CHANGELOG记录变更
- ✅ CI/CD自动发布
- ✅ 测试后再正式发布

---

**掌握包发布，分享你的Python代码！** 📦🚀

**相关文档**:
- [01-pip-basics.md](01-pip-basics.md) - pip基础
- [02-poetry.md](02-poetry.md) - Poetry包管理

**最后更新**: 2025年10月28日

