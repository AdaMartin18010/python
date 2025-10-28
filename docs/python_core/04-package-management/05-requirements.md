# Python Requirements 依赖管理

**requirements.txt完全指南**

---

## 📋 目录

- [requirements.txt基础](#requirementstxt基础)
- [版本规范](#版本规范)
- [依赖分层](#依赖分层)
- [高级特性](#高级特性)
- [最佳实践](#最佳实践)

---

## requirements.txt基础

### 什么是requirements.txt

```bash
# requirements.txt: Python项目依赖列表文件
# 用于指定项目所需的包及其版本

# 生成requirements.txt
pip freeze > requirements.txt

# 安装requirements.txt
pip install -r requirements.txt

# 升级所有包
pip install -r requirements.txt --upgrade

# 基础示例
cat requirements.txt
# requests==2.31.0
# flask==3.0.0
# numpy>=1.24.0
```

### 基本语法

```txt
# requirements.txt 语法规则

# 1. 注释
# 这是注释

# 2. 固定版本
requests==2.31.0

# 3. 最小版本
requests>=2.28.0

# 4. 版本范围
requests>=2.28.0,<3.0.0

# 5. 排除版本
requests!=2.30.0

# 6. 兼容版本 (~=)
requests~=2.31.0
# 等价于 >=2.31.0,<2.32.0

# 7. 任意版本
requests

# 8. 包含额外依赖
requests[security,socks]

# 9. 环境标记
pywin32==305; platform_system == "Windows"
uvloop>=0.17.0; python_version >= "3.11"

# 10. 从URL安装
git+https://github.com/user/repo.git@v1.0.0#egg=package-name
https://github.com/user/repo/archive/main.zip

# 11. 本地路径
./packages/my-package
-e ./src  # editable模式

# 12. 包含其他requirements文件
-r requirements/base.txt
```

---

## 版本规范

### 版本运算符

```txt
# == 精确匹配
requests==2.31.0

# != 排除版本
requests!=2.30.0

# >= 大于等于
requests>=2.28.0

# <= 小于等于
requests<=3.0.0

# > 大于
requests>2.28.0

# < 小于
requests<3.0.0

# ~= 兼容版本
requests~=2.31.0
# 等价于 >=2.31.0,<2.32.0

requests~=2.31
# 等价于 >=2.31,<3.0

# 组合使用
requests>=2.28.0,<3.0.0,!=2.30.0

# 或运算 (很少使用)
requests==2.31.0 || ==2.30.0
```

### 语义化版本

```txt
# 语义化版本: MAJOR.MINOR.PATCH

# MAJOR: 不兼容的API变更
# MINOR: 向后兼容的功能新增
# PATCH: 向后兼容的问题修复

# 示例: requests 2.31.0
# MAJOR: 2
# MINOR: 31
# PATCH: 0

# 版本策略:

# 1. 固定MAJOR版本,允许MINOR和PATCH更新
requests>=2.0.0,<3.0.0

# 2. 固定MAJOR.MINOR,允许PATCH更新
requests>=2.31.0,<2.32.0
# 或使用 ~=
requests~=2.31.0

# 3. 完全固定版本 (生产环境推荐)
requests==2.31.0

# 4. 只指定MAJOR版本
requests>=2.0.0,<3.0.0

# 5. 开发中使用宽松版本
requests>=2.28.0
```

---

## 依赖分层

### 单文件结构

```txt
# requirements.txt
# 简单项目,所有依赖在一个文件

# 生产依赖
fastapi==0.104.0
pydantic==2.4.0
uvicorn==0.24.0
sqlalchemy==2.0.23

# 开发依赖
pytest==7.4.3
black==23.10.0
ruff==0.1.0
mypy==1.6.0

# 问题: 生产环境也会安装开发工具
```

### 分层结构

```bash
# 推荐: 分层管理依赖
requirements/
  ├── base.txt        # 基础依赖
  ├── dev.txt         # 开发依赖
  ├── test.txt        # 测试依赖
  └── prod.txt        # 生产依赖
```

```txt
# requirements/base.txt
# 基础依赖 - 所有环境都需要
fastapi==0.104.0
pydantic==2.4.0
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
python-dotenv==1.0.0
```

```txt
# requirements/dev.txt
# 开发依赖 - 包含基础依赖
-r base.txt

# 代码格式化
black==23.10.0
ruff==0.1.0
isort==5.12.0

# 类型检查
mypy==1.6.0

# 开发工具
ipython==8.17.2
```

```txt
# requirements/test.txt
# 测试依赖 - 包含基础依赖
-r base.txt

# 测试框架
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
pytest-mock==3.12.0

# 工厂数据
faker==20.0.0
```

```txt
# requirements/prod.txt
# 生产依赖 - 包含基础依赖
-r base.txt

# 生产服务器
gunicorn==21.2.0

# 监控
sentry-sdk==1.38.0
```

```bash
# 安装不同环境
pip install -r requirements/dev.txt   # 开发
pip install -r requirements/test.txt  # 测试
pip install -r requirements/prod.txt  # 生产
```

### 环境特定依赖

```txt
# requirements/base.txt
# 使用环境标记

# 所有平台
requests==2.31.0

# 仅Windows
pywin32==305; platform_system == "Windows"

# 仅Linux/macOS
uvloop>=0.17.0; platform_system != "Windows"

# Python版本相关
dataclasses==0.8; python_version < "3.7"
importlib-metadata>=4.0; python_version < "3.8"

# 特定Python版本
asyncio-backport==1.0.0; python_version == "3.6"

# 环境标记支持:
# - python_version
# - python_full_version
# - platform_system (Windows, Linux, Darwin)
# - platform_machine (x86_64, arm64)
# - platform_python_implementation (CPython, PyPy)
# - sys_platform (win32, linux, darwin)
```

---

## 高级特性

### 哈希验证

```bash
# 生成带哈希的requirements.txt
pip freeze --all | pip hash > requirements.txt

# 或使用pip-tools
pip-compile --generate-hashes requirements.in

# requirements.txt with hashes
cat requirements.txt
# requests==2.31.0 \
#     --hash=sha256:58cd2187c01e70e6e26505bca751777aa9f2ee0b7f4300988b709f44e013003f
# certifi==2023.7.22 \
#     --hash=sha256:539cc1d13202e33ca466e88b2807e29f4c13049d6d87031a3c110744495cb082

# 安装时验证哈希
pip install --require-hashes -r requirements.txt

# 优势:
# ✅ 防止中间人攻击
# ✅ 确保包未被篡改
# ✅ 提高安全性
```

### URL依赖

```txt
# 从Git仓库安装
git+https://github.com/django/django.git@stable/4.2.x#egg=Django

# 指定分支
git+https://github.com/user/repo.git@main#egg=package-name

# 指定标签
git+https://github.com/user/repo.git@v1.0.0#egg=package-name

# 指定提交
git+https://github.com/user/repo.git@abc123#egg=package-name

# SSH URL
git+ssh://git@github.com/user/repo.git@main#egg=package-name

# 从压缩包安装
https://github.com/user/repo/archive/main.zip

# 本地文件
file:///path/to/package.tar.gz

# 子目录
git+https://github.com/user/repo.git@main#egg=package-name&subdirectory=packages/my-pkg
```

### 可编辑安装

```txt
# 开发模式安装本地包
-e ./src
-e ./packages/core
-e git+https://github.com/user/repo.git#egg=package-name

# 优势:
# ✅ 修改代码立即生效
# ✅ 无需重新安装
# ✅ 便于开发调试
```

---

## 最佳实践

### pip-tools工作流

```bash
# 安装pip-tools
pip install pip-tools

# 1. 创建requirements.in (不固定版本)
cat > requirements.in << EOF
fastapi
pydantic
uvicorn[standard]
sqlalchemy
EOF

# 2. 编译生成requirements.txt (固定版本)
pip-compile requirements.in

# 输出 requirements.txt:
# fastapi==0.104.0
#     via -r requirements.in
# pydantic==2.4.0
#     via fastapi, -r requirements.in
# ...所有依赖及其子依赖都被固定

# 3. 同步安装 (移除不需要的包)
pip-sync requirements.txt

# 4. 升级特定包
pip-compile --upgrade-package fastapi requirements.in

# 5. 升级所有包
pip-compile --upgrade requirements.in

# 6. 生成哈希
pip-compile --generate-hashes requirements.in
```

### 分层pip-tools

```bash
# requirements/base.in
fastapi
pydantic
uvicorn[standard]

# requirements/dev.in
-c base.txt  # 使用base.txt作为约束
black
ruff
mypy

# 编译
pip-compile requirements/base.in
pip-compile requirements/dev.in

# 安装
pip-sync requirements/dev.txt
```

### 锁定依赖

```bash
# 方法1: pip freeze
pip freeze > requirements.txt

# 问题: 包含所有已安装的包,可能有多余

# 方法2: pipreqs (只包含项目实际使用的包)
pip install pipreqs
pipreqs . --force

# 方法3: pip-tools (推荐)
pip-compile requirements.in

# 方法4: poetry
poetry export -f requirements.txt -o requirements.txt

# 方法5: pipenv
pipenv requirements > requirements.txt
```

### CI/CD实践

```yaml
# GitHub Actions
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
        cache-dependency-path: 'requirements/*.txt'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements/test.txt
    
    - name: Check requirements
      run: |
        # 检查是否有未固定版本的包
        pip list --outdated
        
        # 验证依赖可安装
        pip check
    
    - name: Security audit
      run: |
        pip install pip-audit
        pip-audit -r requirements/prod.txt
```

---

## 📚 核心要点

### requirements.txt基础

- ✅ **生成**: pip freeze > requirements.txt
- ✅ **安装**: pip install -r requirements.txt
- ✅ **注释**: # 开头
- ✅ **包含**: -r other.txt

### 版本规范

- ✅ **==**: 精确版本
- ✅ **>=,<**: 版本范围
- ✅ **~=**: 兼容版本
- ✅ **!=**: 排除版本
- ✅ **组合**: 多个条件

### 依赖分层

- ✅ **base.txt**: 基础依赖
- ✅ **dev.txt**: 开发依赖
- ✅ **test.txt**: 测试依赖
- ✅ **prod.txt**: 生产依赖
- ✅ **环境标记**: 平台特定

### 高级特性

- ✅ **哈希验证**: 安全性
- ✅ **URL依赖**: Git, HTTP
- ✅ **可编辑**: -e ./src
- ✅ **extras**: [dev,test]

### 最佳实践

- ✅ 使用pip-tools管理
- ✅ 生产环境固定版本
- ✅ 分层管理依赖
- ✅ 定期更新和审计
- ✅ CI/CD自动化
- ✅ 哈希验证提高安全

---

**掌握requirements管理，项目依赖井井有条！** 📋✨

**相关文档**:
- [01-pip-basics.md](01-pip-basics.md) - pip基础
- [04-virtual-env.md](04-virtual-env.md) - 虚拟环境

**最后更新**: 2025年10月28日

