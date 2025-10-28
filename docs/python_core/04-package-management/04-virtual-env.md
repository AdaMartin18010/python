# Python 虚拟环境管理

**虚拟环境完全指南**

---

## 📋 目录

- [虚拟环境简介](#虚拟环境简介)
- [venv模块](#venv模块)
- [virtualenv工具](#virtualenv工具)
- [环境管理最佳实践](#环境管理最佳实践)
- [高级技巧](#高级技巧)

---

## 虚拟环境简介

### 为什么需要虚拟环境

```python
"""
虚拟环境解决的问题
"""

# 问题1: 版本冲突
# 项目A需要 requests==2.25.0
# 项目B需要 requests==2.31.0
# 全局安装只能有一个版本

# 问题2: 系统污染
# 全局安装包可能影响系统Python
# 可能破坏系统依赖

# 问题3: 依赖管理
# 难以追踪项目实际依赖
# 部署时难以重现环境

# 解决方案: 虚拟环境
# ✅ 每个项目独立环境
# ✅ 不同Python版本
# ✅ 隔离依赖
# ✅ 易于管理和部署
```

### 虚拟环境原理

```bash
# 虚拟环境的本质:
# 1. 复制/链接Python解释器
# 2. 创建独立的site-packages目录
# 3. 修改PATH环境变量
# 4. 隔离pip安装的包

# 目录结构:
# .venv/
#   ├── bin/              # Linux/macOS可执行文件
#   │   ├── python -> python3.12
#   │   ├── pip
#   │   └── activate
#   ├── Scripts/          # Windows可执行文件
#   │   ├── python.exe
#   │   ├── pip.exe
#   │   └── activate.bat
#   ├── lib/
#   │   └── python3.12/
#   │       └── site-packages/  # 包安装目录
#   └── pyvenv.cfg        # 配置文件
```

---

## venv模块

### 创建虚拟环境

```bash
# venv - Python 3.3+内置模块

# 1. 创建虚拟环境
python -m venv .venv

# 2. 指定Python版本
python3.12 -m venv .venv

# 3. 使用系统site-packages
python -m venv --system-site-packages .venv

# 4. 不包含pip
python -m venv --without-pip .venv

# 5. 升级核心包
python -m venv --upgrade .venv

# 6. 清空并重建
python -m venv --clear .venv

# 7. 创建多个环境
python -m venv env1
python -m venv env2
```

### 激活和停用

```bash
# Linux/macOS 激活
source .venv/bin/activate

# Windows CMD
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows Git Bash
source .venv/Scripts/activate

# 激活后:
# (venv) user@host:~/project$

# 检查Python路径
which python  # Linux/macOS
where python  # Windows
# 输出: /path/to/project/.venv/bin/python

# 检查pip
which pip
# 输出: /path/to/project/.venv/bin/pip

# 停用虚拟环境
deactivate
```

### 使用虚拟环境

```bash
# 激活后正常使用Python和pip
python script.py
pip install requests
pip list

# 不激活直接使用
.venv/bin/python script.py
.venv/bin/pip install requests

# 在虚拟环境中运行命令
.venv/bin/python -m pip list
.venv/bin/python -m pytest
```

---

## virtualenv工具

### virtualenv vs venv

```bash
# virtualenv - 第三方工具

# 安装
pip install virtualenv

# 优势:
# ✅ 更快
# ✅ 更多功能
# ✅ 支持更多Python版本
# ✅ 更灵活的配置

# venv vs virtualenv:
# venv:        内置, 简单, 够用
# virtualenv:  功能更强, 更快, 更灵活
```

### 创建virtualenv

```bash
# 1. 创建环境
virtualenv .venv

# 2. 指定Python版本
virtualenv -p python3.12 .venv
virtualenv --python=/usr/bin/python3.11 .venv

# 3. 使用系统site-packages
virtualenv --system-site-packages .venv

# 4. 不安装wheel和setuptools
virtualenv --no-wheel --no-setuptools .venv

# 5. 不下载pip
virtualenv --no-download .venv

# 6. 指定额外的搜索路径
virtualenv --extra-search-dir=/path/to/packages .venv

# 7. 使用符号链接而非复制
virtualenv --always-copy .venv  # 复制(默认)
virtualenv --symlinks .venv     # 符号链接
```

### virtualenv配置

```ini
# virtualenv.ini / virtualenv.conf
[virtualenv]
# 额外搜索路径
extra-search-dir = /path/to/packages

# 不下载
no-download = true

# 使用符号链接
symlinks = true

# 配置文件位置:
# Linux/macOS: ~/.virtualenvrc
# Windows: %APPDATA%\virtualenv\virtualenv.ini
```

---

## 环境管理最佳实践

### 项目结构

```bash
# 推荐项目结构
my-project/
  ├── .venv/              # 虚拟环境
  ├── .venv/              # 也可以用venv/或env/
  ├── src/
  │   └── my_project/
  ├── tests/
  ├── requirements.txt
  ├── requirements-dev.txt
  ├── .gitignore
  ├── README.md
  └── pyproject.toml

# .gitignore
.venv/
venv/
env/
*.pyc
__pycache__/
.pytest_cache/
```

### 环境变量

```bash
# 设置虚拟环境相关环境变量

# VIRTUAL_ENV - 激活时自动设置
echo $VIRTUAL_ENV
# /path/to/project/.venv

# VIRTUAL_ENV_PROMPT - 自定义提示符
export VIRTUAL_ENV_PROMPT="(myproject)"

# PYTHONPATH - 模块搜索路径
export PYTHONPATH="${PYTHONPATH}:/path/to/project/src"

# PIP_REQUIRE_VIRTUALENV - 强制使用虚拟环境
export PIP_REQUIRE_VIRTUALENV=true
# 这样在全局使用pip会报错

# .env文件
cat > .env << EOF
PYTHONPATH=\${PYTHONPATH}:./src
DATABASE_URL=postgresql://localhost/mydb
DEBUG=True
EOF

# 加载.env
pip install python-dotenv
python -c "from dotenv import load_dotenv; load_dotenv()"
```

### 多环境管理

```bash
# 开发、测试、生产不同环境

# 1. 使用不同的requirements文件
requirements/
  ├── base.txt          # 基础依赖
  ├── dev.txt           # 开发依赖
  ├── test.txt          # 测试依赖
  └── prod.txt          # 生产依赖

# 2. 创建对应的虚拟环境
python -m venv .venv-dev
python -m venv .venv-test
python -m venv .venv-prod

# 3. 安装对应依赖
source .venv-dev/bin/activate
pip install -r requirements/dev.txt

source .venv-test/bin/activate
pip install -r requirements/test.txt

source .venv-prod/bin/activate
pip install -r requirements/prod.txt

# 4. 或使用环境变量
export ENV=dev
source .venv-${ENV}/bin/activate
```

---

## 高级技巧

### 脚本中使用虚拟环境

```bash
#!/bin/bash
# run_in_venv.sh

# 方法1: 激活虚拟环境
source .venv/bin/activate
python script.py
deactivate

# 方法2: 直接使用虚拟环境的Python
.venv/bin/python script.py

# 方法3: 自动检测和激活
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "No virtual environment found"
    exit 1
fi

python script.py
```

```python
#!/usr/bin/env python
"""
Python脚本中确保使用虚拟环境
"""
import sys
import os

# 检查是否在虚拟环境中
if not hasattr(sys, 'real_prefix') and not (
    hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
):
    print("Please run this script in a virtual environment")
    sys.exit(1)

# 检查特定包
try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    sys.exit(1)

# 主逻辑
def main():
    print(f"Python: {sys.executable}")
    print(f"Virtual environment: {sys.prefix}")

if __name__ == "__main__":
    main()
```

### IDE集成

```json
// VSCode settings.json
{
  // 自动检测虚拟环境
  "python.venvPath": "${workspaceFolder}",
  
  // 选择Python解释器
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  
  // 激活虚拟环境时运行
  "python.terminal.activateEnvironment": true,
  
  // 终端中使用虚拟环境
  "terminal.integrated.env.linux": {
    "VIRTUAL_ENV": "${workspaceFolder}/.venv"
  }
}
```

```xml
<!-- PyCharm -->
<!-- Settings -> Project -> Python Interpreter -->
<!-- Add Interpreter -> Virtualenv Environment -->
<!-- Location: /path/to/project/.venv -->
```

### 自动化工具

```bash
# direnv - 自动激活虚拟环境
# 安装direnv
# macOS: brew install direnv
# Linux: apt install direnv

# 配置.envrc
echo 'source .venv/bin/activate' > .envrc
direnv allow

# 进入目录自动激活
cd my-project  # 自动激活.venv

# pyenv - Python版本管理
curl https://pyenv.run | bash

# 安装Python版本
pyenv install 3.12.0
pyenv install 3.11.0

# 设置项目Python版本
cd my-project
pyenv local 3.12.0  # 创建.python-version

# 创建虚拟环境
pyenv virtualenv 3.12.0 myproject-3.12
pyenv activate myproject-3.12
```

---

## 📚 核心要点

### 虚拟环境基础

- ✅ **隔离**: 每个项目独立环境
- ✅ **版本**: 不同Python和包版本
- ✅ **清洁**: 不污染系统Python
- ✅ **可重现**: 易于部署

### venv模块

- ✅ **内置**: Python 3.3+自带
- ✅ **简单**: 创建和使用简单
- ✅ **轻量**: 符号链接节省空间
- ✅ **够用**: 满足基本需求

### virtualenv工具

- ✅ **功能强**: 更多配置选项
- ✅ **快速**: 创建速度更快
- ✅ **兼容**: 支持更多Python版本
- ✅ **灵活**: 高级功能

### 最佳实践

- ✅ 每个项目创建独立环境
- ✅ 环境目录加入.gitignore
- ✅ 使用requirements.txt管理依赖
- ✅ 分层管理不同环境
- ✅ IDE配置虚拟环境

### 高级技巧

- ✅ 脚本中检查虚拟环境
- ✅ direnv自动激活
- ✅ pyenv管理Python版本
- ✅ IDE集成
- ✅ CI/CD自动化

---

**掌握虚拟环境，管理Python项目更轻松！** 🔧✨

**相关文档**:
- [01-pip-basics.md](01-pip-basics.md) - pip基础
- [05-requirements.md](05-requirements.md) - 依赖管理

**最后更新**: 2025年10月28日

