# Python pip 包管理基础

**pip完全使用指南**

---

## 📋 目录

- [pip简介](#pip简介)
- [基础命令](#基础命令)
- [依赖管理](#依赖管理)
- [高级特性](#高级特性)
- [最佳实践](#最佳实践)

---

## pip简介

### 什么是pip

```bash
# pip: Python Package Installer
# Python官方包管理器

# 检查pip版本
python -m pip --version
# pip 24.0 from ...

# 升级pip
python -m pip install --upgrade pip

# 为什么使用python -m pip:
# 1. 明确使用哪个Python解释器
# 2. 避免多Python版本冲突
# 3. 在虚拟环境中更可靠

# 直接使用pip (不推荐)
pip --version

# 推荐使用
python -m pip --version
python3 -m pip --version
```

### pip配置

```bash
# 查看配置
python -m pip config list

# 查看配置文件位置
python -m pip config list -v

# 设置配置
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 常用配置文件位置:
# Linux/macOS: ~/.pip/pip.conf
# Windows: %APPDATA%\pip\pip.ini
```

```ini
# pip.conf / pip.ini
[global]
# 国内镜像源
index-url = https://pypi.tuna.tsinghua.edu.cn/simple

# 信任主机
trusted-host = pypi.tuna.tsinghua.edu.cn

# 超时设置
timeout = 60

[install]
# 全局安装选项
# no-cache-dir = false
```

---

## 基础命令

### 安装包

```bash
# 1. 安装最新版本
python -m pip install requests

# 2. 安装指定版本
python -m pip install requests==2.31.0

# 3. 安装版本范围
python -m pip install "requests>=2.28.0,<3.0.0"

# 4. 安装多个包
python -m pip install requests flask numpy

# 5. 从requirements.txt安装
python -m pip install -r requirements.txt

# 6. 安装本地包
python -m pip install /path/to/package

# 7. 安装开发模式 (可编辑)
python -m pip install -e /path/to/package

# 8. 从GitHub安装
python -m pip install git+https://github.com/user/repo.git

# 9. 从特定分支/标签安装
python -m pip install git+https://github.com/user/repo.git@v1.0.0
python -m pip install git+https://github.com/user/repo.git@branch-name

# 10. 安装额外依赖
python -m pip install "fastapi[all]"  # 安装所有可选依赖
python -m pip install "requests[security,socks]"  # 安装特定可选依赖
```

### 卸载包

```bash
# 1. 卸载单个包
python -m pip uninstall requests

# 2. 卸载多个包
python -m pip uninstall requests flask numpy

# 3. 卸载所有包 (危险!)
python -m pip freeze | xargs python -m pip uninstall -y

# 4. 从requirements.txt卸载
python -m pip uninstall -r requirements.txt

# 5. 强制卸载 (不询问)
python -m pip uninstall -y requests
```

### 查看包信息

```bash
# 1. 列出已安装的包
python -m pip list

# 2. 查看包详情
python -m pip show requests

# 输出:
# Name: requests
# Version: 2.31.0
# Summary: Python HTTP for Humans.
# Home-page: https://requests.readthedocs.io
# Author: Kenneth Reitz
# License: Apache 2.0
# Location: /path/to/site-packages
# Requires: charset-normalizer, idna, urllib3, certifi
# Required-by: some-package

# 3. 查看过时的包
python -m pip list --outdated

# 4. 显示为JSON
python -m pip list --format=json

# 5. 列出用户安装的包 (非全局)
python -m pip list --user

# 6. 查看依赖树
python -m pip show --verbose requests
```

### 升级包

```bash
# 1. 升级单个包
python -m pip install --upgrade requests

# 2. 升级多个包
python -m pip install --upgrade requests flask numpy

# 3. 升级所有包 (不推荐)
python -m pip list --outdated --format=json | \
  python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | \
  xargs -n1 python -m pip install --upgrade

# 4. 升级到特定版本
python -m pip install --upgrade requests==2.31.0

# 5. 强制重新安装
python -m pip install --force-reinstall requests

# 6. 不升级依赖
python -m pip install --upgrade --no-deps requests
```

---

## 依赖管理

### requirements.txt

```bash
# 生成requirements.txt
python -m pip freeze > requirements.txt

# 安装requirements.txt
python -m pip install -r requirements.txt

# 升级requirements.txt中的所有包
python -m pip install -r requirements.txt --upgrade
```

```txt
# requirements.txt 语法

# 1. 固定版本
requests==2.31.0

# 2. 版本范围
requests>=2.28.0,<3.0.0

# 3. 兼容版本 (~=)
requests~=2.31.0  # 等价于 >=2.31.0,<2.32.0

# 4. 最小版本
requests>=2.28.0

# 5. 排除版本
requests!=2.30.0

# 6. 环境标记
requests==2.31.0 ; python_version >= "3.8"
pywin32==305 ; platform_system == "Windows"

# 7. 可选依赖
requests[security]==2.31.0

# 8. 从URL安装
git+https://github.com/user/repo.git@v1.0.0#egg=package-name

# 9. 本地包
./packages/my-package

# 10. 注释
# 开发依赖
pytest==7.4.0
black==23.7.0
```

### requirements分层

```bash
# 项目结构
requirements/
  ├── base.txt        # 基础依赖
  ├── dev.txt         # 开发依赖
  ├── prod.txt        # 生产依赖
  └── test.txt        # 测试依赖
```

```txt
# requirements/base.txt
# 基础依赖
fastapi==0.104.0
pydantic==2.4.0
uvicorn==0.24.0
```

```txt
# requirements/dev.txt
# 包含基础依赖
-r base.txt

# 开发工具
black==23.10.0
ruff==0.1.0
mypy==1.6.0
```

```txt
# requirements/prod.txt
# 生产依赖
-r base.txt

gunicorn==21.2.0
```

```txt
# requirements/test.txt
# 测试依赖
-r base.txt

pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
```

```bash
# 安装不同环境
python -m pip install -r requirements/dev.txt
python -m pip install -r requirements/prod.txt
python -m pip install -r requirements/test.txt
```

---

## 高级特性

### pip-tools

```bash
# 安装pip-tools
python -m pip install pip-tools

# 创建requirements.in (不固定版本)
# requirements.in
# requests
# flask

# 编译生成requirements.txt (固定版本)
pip-compile requirements.in

# 输出 requirements.txt:
# requests==2.31.0
#   via -r requirements.in
# flask==3.0.0
#   via -r requirements.in
# werkzeug==3.0.1
#   via flask
# ...

# 同步安装 (卸载不需要的包)
pip-sync requirements.txt

# 升级特定包
pip-compile --upgrade-package requests requirements.in

# 升级所有包
pip-compile --upgrade requirements.in
```

### pip缓存

```bash
# 查看缓存目录
python -m pip cache dir

# 查看缓存信息
python -m pip cache info

# 列出缓存文件
python -m pip cache list

# 清除缓存
python -m pip cache purge

# 不使用缓存安装
python -m pip install --no-cache-dir requests
```

### pip约束

```bash
# constraints.txt - 约束版本但不安装
# constraints.txt
requests==2.31.0
urllib3==2.0.7

# 使用约束安装
python -m pip install flask -c constraints.txt

# 会确保flask的依赖满足constraints.txt中的版本要求
```

---

## 最佳实践

### 版本固定策略

```txt
# 1. 开发依赖 - requirements-dev.in
# 宽松版本，允许自动升级
black
pytest
mypy

# 2. 生产依赖 - requirements.in
# 兼容版本
requests~=2.31.0
fastapi~=0.104.0

# 3. 编译生成 - requirements.txt
# 完全固定版本（用于生产部署）
requests==2.31.0
  via -r requirements.in
urllib3==2.0.7
  via requests
```

### 安全实践

```bash
# 1. 使用哈希验证
python -m pip install --require-hashes -r requirements.txt

# requirements.txt with hashes
# requests==2.31.0 \
#     --hash=sha256:58cd2187c01e70e6e26505bca751777aa9f2ee0b7f4300988b709f44e013003f

# 2. 生成哈希
python -m pip hash requests-2.31.0-py3-none-any.whl

# 3. 使用pip-audit检查安全漏洞
python -m pip install pip-audit
python -m pip-audit

# 4. 限制网络
python -m pip install --no-index --find-links=/local/packages requests
```

### 性能优化

```bash
# 1. 并行下载
python -m pip install --upgrade pip setuptools wheel
# pip 20.3+ 默认启用并行下载

# 2. 使用wheel
python -m pip install wheel
python -m pip wheel -r requirements.txt -w wheelhouse/
python -m pip install --no-index --find-links=wheelhouse/ -r requirements.txt

# 3. 预下载
python -m pip download -r requirements.txt -d packages/

# 4. 从本地安装
python -m pip install --no-index --find-links=packages/ -r requirements.txt
```

### CI/CD集成

```yaml
# GitHub Actions 示例
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        cache: 'pip'  # 缓存pip依赖
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install -r requirements/test.txt
    
    - name: Run tests
      run: pytest
```

---

## 📚 核心要点

### pip基础

- ✅ **使用python -m pip**: 明确Python版本
- ✅ **配置文件**: pip.conf/pip.ini
- ✅ **国内镜像**: 加速下载
- ✅ **版本管理**: ==, >=, ~=

### 命令

- ✅ **install**: 安装包
- ✅ **uninstall**: 卸载包
- ✅ **list**: 列出包
- ✅ **show**: 查看详情
- ✅ **freeze**: 导出依赖

### 依赖管理

- ✅ **requirements.txt**: 依赖列表
- ✅ **分层管理**: base/dev/prod/test
- ✅ **环境标记**: python_version, platform_system
- ✅ **pip-tools**: 依赖编译

### 高级特性

- ✅ **缓存**: 加速安装
- ✅ **约束**: constraints.txt
- ✅ **哈希验证**: 安全性
- ✅ **wheel**: 预编译包

### 最佳实践

- ✅ 生产环境固定版本
- ✅ 使用pip-tools管理依赖
- ✅ 定期检查安全漏洞
- ✅ CI/CD缓存依赖
- ✅ 虚拟环境隔离

---

**掌握pip，高效管理Python包！** 📦✨

**相关文档**:
- [02-poetry.md](02-poetry.md) - Poetry现代包管理
- [03-uv.md](03-uv.md) - uv快速包管理器
- [04-virtual-env.md](04-virtual-env.md) - 虚拟环境管理

**最后更新**: 2025年10月28日

