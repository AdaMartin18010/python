# Python包管理与标准库核心机制权威指南

> 本文档全面梳理Python生态系统的包管理机制、导入系统和标准库核心模块，提供权威的使用方法、最佳实践和常见陷阱。

---

## 目录

- [Python包管理与标准库核心机制权威指南](#python包管理与标准库核心机制权威指南)
  - [目录](#目录)
  - [第一部分：包管理机制](#第一部分包管理机制)
    - [1.1 pip工具详解](#11-pip工具详解)
      - [核心原理](#核心原理)
      - [权威使用方法](#权威使用方法)
      - [requirements.txt格式详解](#requirementstxt格式详解)
      - [依赖解析算法](#依赖解析算法)
      - [最佳实践](#最佳实践)
      - [常见陷阱](#常见陷阱)
    - [1.2 现代包管理工具对比](#12-现代包管理工具对比)
      - [Poetry详解](#poetry详解)
      - [PDM详解](#pdm详解)
      - [uv详解（Rust实现，极速）](#uv详解rust实现极速)
      - [Conda详解](#conda详解)
      - [工具对比表格](#工具对比表格)
      - [选择建议](#选择建议)
    - [1.3 虚拟环境](#13-虚拟环境)
      - [venv模块（标准库）](#venv模块标准库)
      - [virtualenv](#virtualenv)
      - [Conda环境](#conda环境)
      - [pyenv（Python版本管理）](#pyenvpython版本管理)
      - [虚拟环境对比](#虚拟环境对比)
    - [1.4 打包与分发](#14-打包与分发)
      - [setuptools配置](#setuptools配置)
      - [flit](#flit)
      - [hatch](#hatch)
      - [build模块（PEP 517构建）](#build模块pep-517构建)
      - [打包工具对比](#打包工具对比)
  - [第二部分：导入系统](#第二部分导入系统)
    - [2.1 sys.path机制](#21-syspath机制)
    - [2.2 PYTHONPATH环境变量](#22-pythonpath环境变量)
    - [2.3 命名空间包（Namespace Packages）](#23-命名空间包namespace-packages)
    - [2.4 相对导入与绝对导入](#24-相对导入与绝对导入)
    - [2.5 导入钩子（Import Hooks）](#25-导入钩子import-hooks)
  - [第三部分：标准库核心模块详解](#第三部分标准库核心模块详解)
    - [3.1 系统与文件模块](#31-系统与文件模块)
      - [os模块](#os模块)
      - [sys模块](#sys模块)
      - [pathlib模块](#pathlib模块)
      - [shutil模块](#shutil模块)
      - [glob模块](#glob模块)
      - [tempfile模块](#tempfile模块)
    - [3.2 数据结构模块](#32-数据结构模块)
      - [collections模块](#collections模块)
      - [dataclasses模块](#dataclasses模块)
      - [enum模块](#enum模块)
      - [typing模块](#typing模块)
    - [3.3 函数式编程模块](#33-函数式编程模块)
      - [itertools模块](#itertools模块)
      - [functools模块](#functools模块)
      - [operator模块](#operator模块)
    - [3.4 并发与异步模块](#34-并发与异步模块)
      - [threading模块](#threading模块)
      - [multiprocessing模块](#multiprocessing模块)
      - [asyncio模块](#asyncio模块)
      - [concurrent.futures模块](#concurrentfutures模块)
      - [queue模块](#queue模块)
    - [3.5 网络与IO模块](#35-网络与io模块)
      - [socket模块](#socket模块)
      - [urllib模块](#urllib模块)
      - [http模块](#http模块)
      - [json模块](#json模块)
      - [csv模块](#csv模块)
      - [xml模块](#xml模块)
    - [3.6 测试与调试模块](#36-测试与调试模块)
      - [unittest模块](#unittest模块)
      - [pytest（第三方但重要）](#pytest第三方但重要)
      - [logging模块](#logging模块)
      - [pdb模块](#pdb模块)
    - [3.7 其他重要模块](#37-其他重要模块)
      - [re模块（正则表达式）](#re模块正则表达式)
      - [datetime模块](#datetime模块)
      - [decimal和fractions模块](#decimal和fractions模块)
      - [hashlib和secrets模块](#hashlib和secrets模块)
      - [argparse模块](#argparse模块)
      - [configparser模块](#configparser模块)
  - [附录：快速参考](#附录快速参考)
    - [包管理工具选择速查表](#包管理工具选择速查表)
    - [标准库模块分类速查](#标准库模块分类速查)
    - [常见陷阱速查](#常见陷阱速查)

---

## 第一部分：包管理机制

### 1.1 pip工具详解

#### 核心原理

pip是Python的官方包管理工具，负责从PyPI（Python Package Index）下载、安装、升级和卸载Python包。其核心工作流程：

1. **解析依赖**：分析包的依赖关系
2. **下载包**：从PyPI或指定索引下载wheel或源码包
3. **构建**（如需要）：对源码包执行构建过程
4. **安装**：将包安装到site-packages目录
5. **记录元数据**：在dist-info目录记录安装信息

#### 权威使用方法

```bash
# ========== 基础安装 ==========
# 安装最新版本
pip install requests

# 安装指定版本
pip install requests==2.28.1

# 安装最低版本
pip install 'requests>=2.28.0'

# 安装兼容版本（语义化版本）
pip install 'requests~=2.28.0'  # >=2.28.0, <2.29.0

# 安装范围版本
pip install 'requests>=2.27.0,<2.29.0'

# ========== 升级与卸载 ==========
# 升级包
pip install --upgrade requests
pip install -U requests

# 卸载包
pip uninstall requests

# 卸载并清除所有依赖（手动）
pip uninstall requests -y

# ========== 从其他源安装 ==========
# 从Git仓库安装
pip install git+https://github.com/psf/requests.git
pip install git+https://github.com/psf/requests.git@v2.28.1

# 从本地路径安装
pip install /path/to/package
pip install -e /path/to/package  # 可编辑模式

# 从wheel文件安装
pip install ./requests-2.28.1-py3-none-any.whl

# ========== 批量安装 ==========
# 从requirements.txt安装
pip install -r requirements.txt

# 指定镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

# ========== 查看与查询 ==========
# 列出已安装包
pip list

# 显示包详情
pip show requests

# 检查过时包
pip list --outdated

# 导出当前环境
pip freeze > requirements.txt

# ========== 缓存管理 ==========
pip cache list          # 列出缓存
pip cache remove requests  # 移除特定缓存
pip cache purge         # 清除所有缓存

# ========== 配置 ==========
# 配置默认镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 配置信任主机
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
```

#### requirements.txt格式详解

```txt
# ========== 基础格式 ==========
# 精确版本
requests==2.28.1
numpy==1.23.0

# 最小版本
requests>=2.28.0

# 版本范围
requests>=2.27.0,<2.29.0

# 兼容版本
requests~=2.28.0

# ========== 环境标记 ==========
# 平台特定
pywin32>=227; platform_system=="Windows"

# Python版本特定
dataclasses>=0.6; python_version<"3.7"

# 系统架构特定
numpy>=1.21.0; platform_machine=='arm64'

# 多条件组合
requests>=2.28.0; python_version>="3.8" and platform_system!="Windows"

# ========== 额外依赖 ==========
# 安装包的特定extra
requests[security]>=2.28.0
fastapi[all]>=0.85.0

# ========== 注释与空行 ==========
# 这是注释
requests>=2.28.0  # 内联注释

# ========== 从其他源指定 ==========
# 指定索引源
--index-url https://pypi.tuna.tsinghua.edu.cn/simple
--trusted-host pypi.tuna.tsinghua.edu.cn

# 额外索引源
--extra-index-url https://download.pytorch.org/whl/cu118

# 指定查找链接
--find-links https://example.com/packages/

# ========== 完整示例 ==========
# requirements/production.txt
--index-url https://pypi.tuna.tsinghua.edu.cn/simple
--trusted-host pypi.tuna.tsinghua.edu.cn

# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0

# 数据库
sqlalchemy==2.0.23
alembic==1.12.1
asyncpg==0.29.0; python_version>="3.8"

# 缓存
redis==5.0.1

# 任务队列
celery==5.3.4

# 监控
prometheus-client==0.19.0

# 开发依赖（单独文件 requirements/dev.txt）
-r production.txt  # 包含生产依赖
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
mypy==1.7.1
```

#### 依赖解析算法

```python
"""
pip的依赖解析经历了两个主要阶段：

1. pip < 20.3: 使用"递归安装"策略
   - 遇到依赖冲突时，使用"先到先服务"原则
   - 可能导致不一致的依赖树

2. pip >= 20.3: 使用resolvelib库
   - 基于PubGrub算法的回溯求解器
   - 找到满足所有约束的解决方案
   - 冲突时提供清晰的错误信息
"""

# 依赖冲突示例
"""
包A依赖: requests>=2.25.0
包B依赖: requests<2.28.0

resolvelib会尝试找到满足两者的版本：
- requests 2.27.1 满足 >=2.25.0 且 <2.28.0 ✓
- requests 2.28.0 不满足 <2.28.0 ✗
"""

# 查看依赖树
# pip install pipdeptree
# pipdeptree

# 依赖冲突诊断
"""
当遇到依赖冲突时，使用以下命令诊断：

1. pip check                    # 检查依赖一致性
2. pipdeptree --reverse --packages requests  # 查看谁依赖了requests
3. pip install -v package       # 详细输出查看解析过程
"""
```

#### 最佳实践

```bash
# 1. 始终使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. 使用约束文件确保一致性
pip install -c constraints.txt -r requirements.txt

# 3. 锁定依赖版本
pip install pip-tools
pip-compile requirements.in  # 生成锁定文件
pip-sync                     # 同步环境

# 4. 分层管理依赖
# requirements/
#   ├── base.txt      # 核心依赖
#   ├── dev.txt       # 开发依赖
#   ├── test.txt      # 测试依赖
#   └── prod.txt      # 生产依赖

# 5. 使用哈希验证安全性
# requirements.txt 中添加 --hash=sha256:...

# 6. 定期更新依赖
pip list --outdated
pip-review --local --interactive  # 使用pip-review工具
```

#### 常见陷阱

```python
"""
陷阱1: 全局安装污染系统Python
❌ sudo pip install package        # 危险！
✅ python -m venv venv && source venv/bin/activate

陷阱2: 不使用版本约束
❌ requests                        # 安装最新版，可能不兼容
✅ requests>=2.28.0,<3.0.0        # 明确版本范围

陷阱3: 混合使用pip和系统包管理器
❌ apt install python-requests && pip install requests
✅ 只使用一种方式管理

陷阱4: 忽略依赖冲突警告
❌ pip install package  # 忽略警告
✅ pip check  # 安装后检查

陷阱5: requirements.txt过于宽松
❌ requests  # 无版本约束
✅ requests==2.28.1  # 精确版本或明确范围

陷阱6: 不区分开发和生产依赖
❌ 所有依赖放在一个文件
✅ 分离 requirements-dev.txt 和 requirements-prod.txt
"""
```

---

### 1.2 现代包管理工具对比

#### Poetry详解

```toml
# pyproject.toml - Poetry配置
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "项目描述"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
license = "MIT"
homepage = "https://example.com"
repository = "https://github.com/user/repo"
keywords = ["python", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
]
packages = [{include = "my_package"}]

[tool.poetry.dependencies]
python = "^3.9"  # 要求Python >=3.9,<4.0
requests = "^2.28.0"
pydantic = ">=2.0.0"
numpy = {version = ">=1.24.0", optional = true}

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.0.0"
mypy = "^1.5.0"

[tool.poetry.group.test.dependencies]
pytest-cov = "^4.1.0"

[tool.poetry.extras]
science = ["numpy"]  # pip install package[science]

[tool.poetry.scripts]
my-cli = "my_package.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# Poetry版本约束语义
# ^1.2.3  := >=1.2.3, <2.0.0
# ~1.2.3  := >=1.2.3, <1.3.0
# >=1.2.0 := 1.2.0及以上
# *       := 任意版本
# 1.2.*   := >=1.2.0, <1.3.0
```

```bash
# Poetry常用命令
# ========== 项目初始化 ==========
poetry new my-project          # 创建新项目
poetry init                    # 在现有项目初始化

# ========== 依赖管理 ==========
poetry add requests            # 添加依赖
poetry add requests@^2.28.0    # 指定版本
poetry add --group dev pytest  # 添加到dev组
poetry add --optional numpy    # 可选依赖

poetry remove requests         # 移除依赖
poetry update                  # 更新所有依赖
poetry update requests         # 更新特定包

# ========== 环境管理 ==========
poetry install                 # 安装所有依赖
poetry install --no-dev        # 不安装开发依赖
poetry install --with test     # 包含test组
poetry install --extras science # 安装可选依赖

# ========== 虚拟环境 ==========
poetry env info                # 环境信息
poetry env list                # 列出环境
poetry env remove python3.9    # 删除环境
poetry env use python3.11      # 切换Python版本

# ========== 运行与构建 ==========
poetry run python script.py    # 在环境中运行
poetry shell                   # 进入虚拟环境shell
poetry build                   # 构建包
poetry publish                 # 发布到PyPI

# ========== 锁定文件 ==========
poetry lock                    # 生成poetry.lock
poetry lock --no-update        # 不更新只验证
```

#### PDM详解

```toml
# pyproject.toml - PDM配置
[project]
name = "my-project"
version = "0.1.0"
description = "项目描述"
authors = [{name = "Your Name", email = "you@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"
keywords = ["python", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
]
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
web = ["fastapi>=0.100.0", "uvicorn>=0.23.0"]
data = ["pandas>=2.0.0", "numpy>=1.24.0"]
all = ["my-project[web,data]"]

[project.scripts]
my-cli = "my_package.cli:main"

[project.urls]
Homepage = "https://example.com"
Repository = "https://github.com/user/repo"

[tool.pdm.dev-dependencies]
test = ["pytest>=7.4.0", "pytest-cov>=4.1.0"]
lint = ["black>=23.0.0", "ruff>=0.1.0", "mypy>=1.5.0"]
doc = ["mkdocs>=1.5.0", "mkdocs-material>=9.0.0"]

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

# PDM配置
[tool.pdm]
version = {source = "scm"}  # 从git标签获取版本
```

```bash
# PDM常用命令
# ========== 项目初始化 ==========
pdm init                       # 初始化项目

# ========== 依赖管理 ==========
pdm add requests               # 添加依赖
pdm add -dG test pytest        # 添加到test组
dev依赖
pdm add -G web fastapi         # 添加到web组

pdm remove requests            # 移除依赖
pdm update                     # 更新所有
pdm update --update-reuse requests  # 保守更新

# ========== 安装与同步 ==========
pdm install                    # 安装依赖
pdm install --prod             # 仅生产依赖
pdm install --no-lock          # 不检查锁定文件
pdm sync                       # 严格同步到锁定文件

# ========== 虚拟环境 ==========
pdm venv create                # 创建环境
pdm venv list                  # 列出环境
pdm venv remove                # 删除环境
pdm use python3.11             # 切换Python版本

# ========== 运行与构建 ==========
pdm run python script.py       # 运行脚本
pdm run pytest                 # 运行测试
pdm shell                      # 进入shell
pdm build                      # 构建
pdm publish                    # 发布

# ========== 锁定文件 ==========
pdm lock                       # 生成pdm.lock
pdm lock --update-reuse        # 最小化更新
pdm lock --refresh             # 重新生成
```

#### uv详解（Rust实现，极速）

```bash
# uv是Astral公司开发的极速Python包管理器
# 使用Rust编写，比pip快10-100倍

# ========== 安装 ==========
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或
pip install uv

# ========== pip替代命令 ==========
# 所有pip命令都可以用uv pip前缀
uv pip install requests        # 安装
uv pip install -r requirements.txt  # 批量安装
uv pip uninstall requests      # 卸载
uv pip list                    # 列出
uv pip freeze                  # 导出
uv pip compile requirements.in -o requirements.txt  # 编译锁定
uv pip sync requirements.txt   # 同步环境

# ========== 虚拟环境 ==========
uv venv                        # 创建虚拟环境
uv venv --python python3.11    # 指定Python版本
source .venv/bin/activate      # 激活（标准方式）

# ========== Python版本管理 ==========
uv python install 3.11         # 安装Python
uv python list                 # 列出可用版本
uv python find                 # 查找Python

# ========== 项目管理（实验性） ==========
uv init                        # 初始化项目
uv add requests                # 添加依赖
uv remove requests             # 移除依赖
uv run python script.py        # 运行脚本
uv run pytest                  # 运行测试
uv lock                        # 锁定依赖
uv sync                        # 同步环境
uv build                       # 构建
uv publish                     # 发布

# ========== 工具运行 ==========
uvx ruff check .               # 运行ruff（无需安装）
uvx black file.py              # 运行black
uvx --python 3.11 pytest       # 指定Python版本运行
```

#### Conda详解

```yaml
# environment.yml
name: my-project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy=1.24
  - pandas>=2.0
  - pip
  - pip:
    - requests>=2.28.0
    - fastapi>=0.100.0
```

```bash
# ========== 环境管理 ==========
conda create -n myenv python=3.11  # 创建环境
conda create -f environment.yml    # 从文件创建
conda activate myenv               # 激活环境
conda deactivate                   # 退出环境
conda env list                     # 列出环境
conda remove -n myenv --all        # 删除环境

# ========== 包管理 ==========
conda install numpy                # 安装包
conda install numpy=1.24           # 指定版本
conda install -c conda-forge flask # 指定channel
conda update numpy                 # 更新
conda remove numpy                 # 卸载
conda list                         # 列出包

# ========== 环境导出与复现 ==========
conda env export > environment.yml           # 导出（含版本）
conda env export --no-builds > environment.yml  # 导出（不含build）
conda env create -f environment.yml          # 从文件创建

# ========== 清理与维护 ==========
conda clean -p                     # 清理包缓存
conda clean -a                     # 清理所有缓存
conda update conda                 # 更新conda本身
```

#### 工具对比表格

| 特性 | pip + venv | Poetry | PDM | uv | Conda |
|------|-----------|--------|-----|-----|-------|
| **核心定位** | 基础工具 | 全功能管理 | 符合PEP标准 | 极速替代 | 科学计算生态 |
| **配置文件** | requirements.txt | pyproject.toml | pyproject.toml | pyproject.toml | environment.yml |
| **锁定文件** | 需pip-tools | poetry.lock | pdm.lock | uv.lock | conda-lock |
| **虚拟环境** | 需venv | 内置 | 可选 | 内置 | 内置 |
| **依赖解析** | resolvelib | 自定义 | 自定义 | 自定义 | SAT求解器 |
| **构建后端** | 需配置 | poetry-core | pdm-backend | 内置 | conda-build |
| **Python版本管理** | pyenv | 部分支持 | 部分支持 | 内置 | 内置 |
| **安装速度** | 基准 | 中等 | 中等 | **极快** | 慢 |
| **PEP 621支持** | N/A | 部分 | **完全** | **完全** | N/A |
| **PEP 660支持** | 是 | 是 | 是 | 是 | N/A |
| **二进制包** | wheel | wheel | wheel | wheel | conda包 |
| **非Python依赖** | 否 | 否 | 否 | 否 | **是** |
| **学习曲线** | 低 | 中等 | 中等 | 低 | 中等 |
| **社区活跃度** | 极高 | 高 | 中高 | **快速上升** | 高 |

#### 选择建议

```python
"""
场景选择指南：

1. 小型项目/快速原型
   推荐: uv
   理由: 极速安装，低学习成本

2. 中型Web项目（Django/FastAPI）
   推荐: Poetry 或 PDM
   理由: 完善的依赖管理，清晰的锁定文件

3. 数据科学/ML项目
   推荐: Conda 或 Conda + pip
   理由: 管理非Python依赖（CUDA等）

4. 企业级/严格合规项目
   推荐: PDM
   理由: 完全符合PEP标准，未来兼容性好

5. CI/CD环境
   推荐: uv
   理由: 极速安装，节省CI时间

6. 库开发（发布到PyPI）
   推荐: Poetry 或 PDM 或 hatch
   理由: 完善的构建和发布流程

7. 遗留项目维护
   推荐: pip + venv
   理由: 无需迁移，兼容性最好
"""
```

---

### 1.3 虚拟环境

#### venv模块（标准库）

```bash
# ========== 创建虚拟环境 ==========
# 基本创建
python -m venv venv

# 指定Python版本
python3.11 -m venv venv

# 包含系统site-packages（不推荐）
python -m venv venv --system-site-packages

# 不安装pip（特殊场景）
python -m venv venv --without-pip

# 使用symlink而非copy（Linux/Mac更快）
python -m venv venv --symlinks

# ========== 激活与退出 ==========
# Linux/Mac
source venv/bin/activate

# Windows CMD
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1

# 退出
 deactivate

# ========== 删除环境 ==========
# 直接删除目录即可
rm -rf venv

# Windows
rmdir /s venv
```

```python
# venv的Python API
import venv

# 创建环境
builder = venv.EnvBuilder(
    system_site_packages=False,  # 不包含系统包
    clear=False,                  # 不清除现有目录
    symlinks=True,               # 使用符号链接
    upgrade=False,               # 不升级核心文件
    with_pip=True,               # 安装pip
    prompt='myenv'               # 提示符前缀
)
builder.create('/path/to/venv')

# 自定义创建器
class CustomEnvBuilder(venv.EnvBuilder):
    def post_setup(self, context):
        """创建后执行自定义操作"""
        # context.env_dir: 环境目录
        # context.env_name: 环境名称
        # context.prompt: 提示符
        # context.executable: Python解释器路径
        # context.bin_path: bin/scripts目录

        # 例如：安装基础包
        import subprocess
        subprocess.check_call([
            context.executable, '-m', 'pip', 'install', 'wheel'
        ])

builder = CustomEnvBuilder(with_pip=True)
builder.create('/path/to/venv')
```

#### virtualenv

```bash
# virtualenv比venv提供更多功能
pip install virtualenv

# 创建环境
virtualenv venv

# 指定Python版本
virtualenv -p python3.11 venv
virtualenv -p /usr/bin/python3.9 venv

# 使用特定版本的pip
virtualenv --pip 23.0 venv

# 使用特定版本的setuptools
virtualenv --setuptools 67.0 venv

# 使用特定版本的wheel
virtualenv --wheel 0.38 venv

# 不安装任何包
virtualenv --no-pip --no-setuptools --no-wheel venv

# 使用副本而非symlink
virtualenv --always-copy venv

# 使用app-data种子（更快）
virtualenv --seeder app-data venv
```

#### Conda环境

```bash
# ========== 环境管理 ==========
# 创建基础环境
conda create -n myenv python=3.11

# 创建并安装包
conda create -n myenv python=3.11 numpy pandas

# 克隆环境
conda create -n newenv --clone oldenv

# 导出环境
conda env export -n myenv > environment.yml

# 从文件创建
conda env create -f environment.yml

# ========== 环境操作 ==========
conda activate myenv
conda deactivate
conda env list
conda info --envs

# 重命名环境（conda 4.14+）
conda rename -n oldname newname

# 删除环境
conda remove -n myenv --all

# ========== 包管理 ==========
conda install numpy
conda install numpy=1.24
conda install -c conda-forge flask
conda update numpy
conda remove numpy
conda list

# ========== 高级用法 ==========
# 指定精确版本
conda install numpy=1.24.3=py311h...  # 包含build string

# 锁定环境
conda list --explicit > spec-file.txt  # 精确规格
conda create -n myenv --file spec-file.txt
```

#### pyenv（Python版本管理）

```bash
# ========== 安装pyenv ==========
# Linux/Mac
curl https://pyenv.run | bash

# 添加到~/.bashrc或~/.zshrc
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# ========== Python版本管理 ==========
# 列出可安装版本
pyenv install --list

# 安装Python
pyenv install 3.11.6
pyenv install 3.10.13
pyenv install 3.12.0

# 卸载版本
pyenv uninstall 3.11.6

# 列出已安装
pyenv versions

# ========== 版本切换 ==========
# 全局默认
pyenv global 3.11.6

# 当前目录（写入.python-version）
pyenv local 3.10.13

# 当前shell会话
pyenv shell 3.12.0

# 取消设置
pyenv local --unset
pyenv shell --unset

# ========== 虚拟环境 ==========
# 创建基于pyenv的虚拟环境
pyenv virtualenv 3.11.6 myproject

# 激活
pyenv activate myproject
pyenv deactivate

# 列出虚拟环境
pyenv virtualenvs

# 删除虚拟环境
pyenv virtualenv-delete myproject

# 自动激活（目录进入时）
# 在项目目录执行：
pyenv local myproject
```

#### 虚拟环境对比

| 特性 | venv | virtualenv | Conda | pyenv |
|------|------|-----------|-------|-------|
| **Python版本管理** | 否 | 否 | 是 | **是** |
| **创建速度** | 快 | 快 | 慢 | N/A |
| **隔离性** | 好 | 好 | 好 | 好 |
| **跨平台** | 是 | 是 | 是 | 部分 |
| **非Python依赖** | 否 | 否 | **是** | 否 |
| **学习成本** | 低 | 低 | 中 | 中 |
| **推荐场景** | 标准开发 | 高级需求 | 数据科学 | 多版本管理 |

---

### 1.4 打包与分发

#### setuptools配置

```toml
# pyproject.toml - 现代setuptools配置
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
requires-python = ">=3.9"
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=23.0"]
test = ["pytest-cov>=4.0"]

[project.urls]
Homepage = "https://github.com/user/repo"
Documentation = "https://docs.example.com"
Repository = "https://github.com/user/repo"
Issues = "https://github.com/user/repo/issues"

[project.scripts]
my-cli = "my_package.cli:main"

[project.gui-scripts]
my-gui = "my_package.gui:main"

[project.entry-points."pytest11"]
myplugin = "my_package.pytest_plugin"

# setuptools特定配置
[tool.setuptools]
packages = ["my_package"]
zip-safe = false
include-package-data = true

[tool.setuptools.package-data]
my_package = ["data/*.json", "templates/*.html"]

[tool.setuptools.exclude-package-data]
my_package = ["tests/*", "docs/*"]

[tool.setuptools.dynamic]
version = {attr = "my_package.__version__"}
```

```python
# setup.py - 仅在需要动态配置时使用
from setuptools import setup, find_packages

setup(
    name="my-package",
    use_scm_version=True,  # 从git标签获取版本
    setup_requires=['setuptools_scm'],
    packages=find_packages(
        where="src",
        exclude=["tests", "tests.*"]
    ),
    package_dir={"": "src"},
    # 其他配置...
)
```

#### flit

```toml
# pyproject.toml - flit配置
[build-system]
requires = ["flit_core>=3.4"]
build-backend = "flit_core.buildapi"

[project]
name = "my_package"
version = "0.1.0"
description = "A short description"
readme = "README.md"
license = {file = "LICENSE"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]
requires-python = ">=3.9"
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
test = ["pytest>=7.0"]
doc = ["sphinx>=5.0"]

[project.scripts]
my-cli = "my_package:main"

[project.urls]
Homepage = "https://github.com/user/repo"
```

```bash
# flit命令
flit build              # 构建
flit publish            # 发布
flit install            # 安装到环境
flit install --symlink  # 可编辑安装（开发模式）
```

#### hatch

```toml
# pyproject.toml - hatch配置
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
dynamic = ["version"]
description = "A short description"
readme = "README.md"
license = "MIT"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.9",
]
requires-python = ">=3.9"
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
test = ["pytest>=7.0"]

[project.scripts]
my-cli = "my_package.cli:main"

[project.urls]
Documentation = "https://github.com/user/repo#readme"
Issues = "https://github.com/user/repo/issues"
Source = "https://github.com/user/repo"

# hatch版本管理
[tool.hatch.version]
path = "src/my_package/__init__.py"

# hatch构建配置
[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/tests",
    "/README.md",
    "/LICENSE",
]
exclude = [
    "/.github",
    "/docs/_build",
]

# hatch环境管理
[tool.hatch.envs.default]
dependencies = [
    "pytest>=7.0",
    "black>=23.0",
]
[tool.hatch.envs.default.scripts]
test = "pytest {args:tests}"
lint = "black src tests"

[tool.hatch.envs.docs]
dependencies = ["mkdocs>=1.5"]
[tool.hatch.envs.docs.scripts]
build = "mkdocs build"
serve = "mkdocs serve"
```

```bash
# hatch命令
hatch build                    # 构建
hatch publish                  # 发布
hatch env create               # 创建环境
hatch env remove               # 删除环境
hatch run test                 # 运行测试
hatch run lint                 # 运行lint
hatch shell                    # 进入环境
hatch version                  # 查看/设置版本
hatch version patch            # 增加patch版本
```

#### build模块（PEP 517构建）

```bash
# build是PEP 517标准的构建前端
pip install build

# 构建wheel和sdist
python -m build

# 只构建wheel
python -m build --wheel

# 只构建sdist
python -m build --sdist

# 指定输出目录
python -m build --outdir dist/

# 不隔离构建（使用当前环境）
python -m build --no-isolation

# 详细输出
python -m build -v
```

```python
# 程序化使用build
from build import ProjectBuilder
from build.env import IsolatedEnv

# 创建构建器
builder = ProjectBuilder('.')

# 获取元数据
metadata = builder.metadata
print(metadata.version)
print(metadata.name)

# 构建
builder.build('wheel', 'dist/')
builder.build('sdist', 'dist/')
```

#### 打包工具对比

| 特性 | setuptools | flit | hatch | poetry-core | pdm-backend |
|------|-----------|------|-------|-------------|-------------|
| **配置复杂度** | 高 | 低 | 中 | 中 | 中 |
| **构建速度** | 中 | **快** | 中 | 中 | 中 |
| **版本管理** | 手动 | 手动 | **自动** | 自动 | 自动 |
| **环境管理** | 否 | 否 | **是** | 是 | 是 |
| **插件扩展** | 是 | 否 | **是** | 否 | 否 |
| **PEP 621** | 是 | 是 | 是 | 部分 | 是 |
| **适用场景** | 复杂项目 | 简单项目 | 复杂项目 | 应用开发 | 库开发 |

---

## 第二部分：导入系统

### 2.1 sys.path机制

```python
"""
sys.path是Python导入系统的搜索路径列表。
导入模块时，Python按顺序在sys.path中查找。
"""

import sys

# 查看当前搜索路径
print("Python导入搜索路径:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

"""
sys.path的初始化顺序（从高优先级到低）：

1. 运行脚本所在目录（或空字符串表示当前目录）
2. PYTHONPATH环境变量中的目录
3. 标准库目录（安装时的prefix/lib/pythonX.Y）
4. site-packages目录（第三方包）
5. 路径配置文件（.pth文件）
"""

# 动态修改sys.path
# ========== 临时添加路径 ==========
# 添加到开头（最高优先级）
sys.path.insert(0, '/path/to/module')

# 添加到末尾（最低优先级）
sys.path.append('/path/to/module')

# ========== 使用pathlib ==========
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# ========== 更好的方式：使用site模块 ==========
import site
site.addsitedir('/path/to/module')  # 同时处理.pth文件

# ========== 使用PYTHONPATH环境变量（推荐） ==========
"""
# Linux/Mac
export PYTHONPATH="/path/to/module:$PYTHONPATH"

# Windows
set PYTHONPATH=C:\path\to\module;%PYTHONPATH%
"""

# ========== 路径钩子 ==========
# sys.path_hooks: 处理特殊路径的钩子
# sys.path_importer_cache: 缓存的查找器

print("\n路径钩子:")
for hook in sys.path_hooks:
    print(f"  {hook}")

# ========== 元路径查找器 ==========
# sys.meta_path: 最高级别的导入钩子
print("\n元路径查找器:")
for finder in sys.meta_path:
    print(f"  {finder}")
```

### 2.2 PYTHONPATH环境变量

```bash
# ========== 设置PYTHONPATH ==========
# Linux/Mac - 临时（当前终端）
export PYTHONPATH="/home/user/myproject/src:$PYTHONPATH"

# Linux/Mac - 永久（添加到~/.bashrc或~/.zshrc）
echo 'export PYTHONPATH="/home/user/myproject/src:$PYTHONPATH"' >> ~/.bashrc

# Windows CMD - 临时
set PYTHONPATH=C:\Users\user\myproject\src;%PYTHONPATH%

# Windows PowerShell - 临时
$env:PYTHONPATH = "C:\Users\user\myproject\src;$env:PYTHONPATH"

# Windows - 永久（系统属性->环境变量）
# 或使用PowerShell
[Environment]::SetEnvironmentVariable("PYTHONPATH", "C:\Users\user\myproject\src", "User")
```

```python
# PYTHONPATH最佳实践
"""
1. 开发时使用，生产环境避免
2. 优先使用虚拟环境
3. 使用相对路径要小心
4. 考虑使用 -m 运行模块
"""

# 替代方案：使用 -m 运行
# 代替: python /path/to/script.py
# 使用: python -m package.module

# 项目结构示例
"""
myproject/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
"""

# 在tests/test_module.py中
# 不推荐: sys.path.insert(0, '../src')
# 推荐: 安装为可编辑模式 pip install -e .
# 或使用 pytest 的pythonpath配置

# pytest.ini
"""
[pytest]
pythonpath = src
"""
```

### 2.3 命名空间包（Namespace Packages）

```python
"""
命名空间包允许将一个大包分割到多个目录中。

两种类型：
1. 隐式命名空间包（PEP 420，Python 3.3+）
2. 显式命名空间包（pkgutil，兼容旧版本）
"""

# ========== 隐式命名空间包（推荐） ==========
"""
目录结构：
/project1
    /company
        /package1
            __init__.py
            module1.py

/project2
    /company
        /package2
            __init__.py
            module2.py

注意：company目录下没有__init__.py
"""

# 使用
import sys
sys.path.insert(0, '/project1')
sys.path.insert(0, '/project2')

import company.package1  # 来自/project1
import company.package2  # 来自/project2

# ========== 显式命名空间包（兼容旧版） ==========
"""
/project1
    /company
        __init__.py  # 包含: __import__('pkgutil').extend_path(__path__, __name__)
        /package1
            __init__.py

/project2
    /company
        __init__.py  # 同样内容
        /package2
            __init__.py
"""

# company/__init__.py
__import__('pkgutil').extend_path(__path__, __name__)

# ========== 检查命名空间包 ==========
import company
print(type(company.__path__))  # <class '_namespace_path'>
print(company.__path__)  # 显示所有路径
print(company.__file__)  # None（命名空间包没有__file__）

# ========== 实际应用：插件系统 ==========
"""
应用结构：
/myapp
    /core
        __init__.py
        app.py
    /plugins
        /plugin_a
            __init__.py
        /plugin_b
            __init__.py

插件可以安装在独立的包中：
/myapp_plugins_extra
    /myapp
        /plugins
            /plugin_c
                __init__.py
"""

# core/app.py
import myapp.plugins
print(myapp.plugins.__path__)  # 包含所有插件路径
```

### 2.4 相对导入与绝对导入

```python
"""
绝对导入：从项目根目录开始的完整路径
相对导入：相对于当前模块的路径
"""

# ========== 绝对导入 ==========
# 项目结构
"""
myproject/
├── package/
│   ├── __init__.py
│   ├── module_a.py
│   └── subpackage/
│       ├── __init__.py
│       └── module_b.py
└── main.py
"""

# package/subpackage/module_b.py 中使用
from package.module_a import MyClass      # 绝对导入
from package.subpackage import something  # 绝对导入

# ========== 相对导入 ==========
# .  当前包
# .. 父包
# ... 祖父包

# package/subpackage/module_b.py 中使用
from . import something           # 从当前包导入
from ..module_a import MyClass    # 从父包导入
from .. import module_a           # 导入父包的module_a

# ========== 对比示例 ==========
"""
package/
    __init__.py
    utils.py
    models.py
    api/
        __init__.py
        routes.py
        handlers.py
"""

# package/api/routes.py
# 绝对导入
from package.utils import helper
from package.models import User
from package.api.handlers import handle_request

# 相对导入
from ..utils import helper
from ..models import User
from .handlers import handle_request

# ========== 选择指南 ==========
"""
相对导入优点：
- 包重命名时无需修改导入
- 清晰表达模块关系
- 适合大型项目内部

相对导入缺点：
- 不能直接运行模块（python module.py会失败）
- 必须使用 python -m package.module 运行

绝对导入优点：
- 清晰完整
- 可以直接运行模块
- 适合小型项目

绝对导入缺点：
- 包重命名需要修改所有导入
- 可能很长
"""

# ========== 运行相对导入的模块 ==========
# ❌ 错误：直接运行
# python package/api/routes.py
# ImportError: attempted relative import with no known parent package

# ✅ 正确：使用 -m 运行
# python -m package.api.routes

# 从项目根目录运行
# python -m package.module
```

### 2.5 导入钩子（Import Hooks）

```python
"""
Python导入系统提供三个层次的钩子：

1. sys.meta_path: 最高级别，在导入开始时调用
2. sys.path_hooks: 处理sys.path中的特殊路径
3. 路径导入器: 实际的模块加载
"""

import sys
import importlib.abc
import importlib.machinery
import importlib.util

# ========== 元路径查找器 ==========
class DebugMetaPathFinder(importlib.abc.MetaPathFinder):
    """调试用的元路径查找器"""

    def find_spec(self, fullname, path, target=None):
        print(f"[Debug] 查找模块: {fullname}")
        print(f"[Debug] 路径: {path}")
        return None  # 不处理，让其他查找器处理

# 注册到sys.meta_path（插入到最前面）
debug_finder = DebugMetaPathFinder()
sys.meta_meta.insert(0, debug_finder)

# ========== 自定义模块加载器 ==========
class StringModuleLoader(importlib.abc.Loader):
    """从字符串加载模块"""

    def __init__(self, code_string):
        self.code_string = code_string

    def create_module(self, spec):
        return None  # 使用默认模块创建

    def exec_module(self, module):
        exec(self.code_string, module.__dict__)

class StringModuleFinder(importlib.abc.MetaPathFinder):
    """查找字符串定义的模块"""

    def __init__(self, modules):
        self.modules = modules  # {name: code_string}

    def find_spec(self, fullname, path, target=None):
        if fullname in self.modules:
            spec = importlib.machinery.ModuleSpec(
                fullname,
                StringModuleLoader(self.modules[fullname]),
                origin="<string>"
            )
            return spec
        return None

# 使用示例
modules = {
    'dynamic_module': '''
def hello():
    return "Hello from dynamic module!"

x = 42
'''
}

finder = StringModuleFinder(modules)
sys.meta_path.insert(0, finder)

import dynamic_module
print(dynamic_module.hello())  # Hello from dynamic module!
print(dynamic_module.x)        # 42

# ========== 路径钩子 ==========
class RemotePathFinder(importlib.abc.PathEntryFinder):
    """从远程URL加载模块"""

    def __init__(self, base_url):
        self.base_url = base_url

    def find_spec(self, fullname, target=None):
        # 实现远程模块查找逻辑
        pass

def remote_path_hook(path):
    """处理http://或https://开头的路径"""
    if path.startswith(('http://', 'https://')):
        return RemotePathFinder(path)
    raise ImportError

# 注册路径钩子
sys.path_hooks.append(remote_path_hook)
sys.path.insert(0, 'https://example.com/modules')

# ========== 导入后钩子 ==========
# 使用importlib的post-import钩子
import importlib

class ImportMonitor:
    """监控模块导入"""

    def find_module(self, fullname, path=None):
        return self

    def load_module(self, fullname):
        # 记录导入
        print(f"[Monitor] 导入模块: {fullname}")
        # 委托给真正的加载器
        return importlib.import_module(fullname)

# ========== 实际应用：热重载 ==========
import importlib
import time
import threading

class HotReloader:
    """开发时热重载模块"""

    def __init__(self):
        self._modules = {}
        self._timestamps = {}
        self._lock = threading.Lock()

    def watch(self, module_name):
        """开始监视模块"""
        module = importlib.import_module(module_name)
        with self._lock:
            self._modules[module_name] = module
            self._timestamps[module_name] = self._get_mtime(module)

    def _get_mtime(self, module):
        """获取模块文件修改时间"""
        if hasattr(module, '__file__'):
            import os
            return os.path.getmtime(module.__file__)
        return 0

    def check_and_reload(self):
        """检查并重载修改的模块"""
        with self._lock:
            for name, module in self._modules.items():
                current_mtime = self._get_mtime(module)
                if current_mtime > self._timestamps[name]:
                    print(f"[HotReload] 重载: {name}")
                    importlib.reload(module)
                    self._timestamps[name] = current_mtime
                    return module
        return None

    def start_watching(self, interval=1.0):
        """启动监视线程"""
        def watch_loop():
            while True:
                self.check_and_reload()
                time.sleep(interval)

        thread = threading.Thread(target=watch_loop, daemon=True)
        thread.start()

# 使用
reloader = HotReloader()
reloader.watch('my_module')
reloader.start_watching()
```

---

## 第三部分：标准库核心模块详解

### 3.1 系统与文件模块

#### os模块

```python
"""
os模块提供与操作系统交互的功能。
核心功能：文件/目录操作、进程管理、环境变量、路径操作。
"""

import os

# ========== 环境变量 ==========
# 获取环境变量
path = os.environ.get('PATH')
home = os.environ.get('HOME') or os.environ.get('USERPROFILE')

# 设置环境变量（当前进程有效）
os.environ['MY_VAR'] = 'value'

# 带默认值
api_key = os.environ.get('API_KEY', 'default_key')

# 必需环境变量（不存在则抛出异常）
# api_key = os.environ['API_KEY']  # KeyError如果不存在

# ========== 进程信息 ==========
print(f"进程ID: {os.getpid()}")
print(f"父进程ID: {os.getppid()}")
print(f"当前工作目录: {os.getcwd()}")
print(f"当前用户: {os.getlogin()}")

# ========== 目录操作 ==========
# 创建目录
os.mkdir('new_dir')                    # 创建单级目录
os.makedirs('a/b/c', exist_ok=True)    # 递归创建

# 删除目录
os.rmdir('empty_dir')                  # 删除空目录
os.removedirs('a/b/c')                 # 递归删除空目录

# 列出目录
entries = os.listdir('.')

# 更改工作目录
os.chdir('/tmp')

# ========== 文件操作 ==========
# 重命名
os.rename('old.txt', 'new.txt')
os.replace('src.txt', 'dst.txt')       # 原子操作，覆盖目标

# 删除文件
os.remove('file.txt')
os.unlink('file.txt')                  # 同remove

# 符号链接
os.symlink('target.txt', 'link.txt')
os.readlink('link.txt')                # 读取链接目标

# 文件状态
stat = os.stat('file.txt')
print(f"大小: {stat.st_size}")
print(f"修改时间: {stat.st_mtime}")
print(f"权限: {oct(stat.st_mode)}")

# ========== 路径操作（已弃用，使用pathlib或os.path） ==========
# os.path.join - 智能拼接路径
path = os.path.join('dir', 'subdir', 'file.txt')

# os.path.exists - 检查存在
exists = os.path.exists('file.txt')

# os.path.isfile/os.path.isdir - 类型检查
is_file = os.path.isfile('file.txt')
is_dir = os.path.isdir('directory')

# os.path.abspath - 绝对路径
abs_path = os.path.abspath('relative/path')

# os.path.dirname/os.path.basename - 拆分路径
dirname = os.path.dirname('/a/b/c.txt')    # /a/b
basename = os.path.basename('/a/b/c.txt')  # c.txt

# os.path.splitext - 分离扩展名
root, ext = os.path.splitext('file.txt')   # ('file', '.txt')

# ========== 进程管理 ==========
# 执行系统命令（推荐使用subprocess）
# os.system('ls -la')  # 简单但功能有限

# 创建子进程
pid = os.fork()  # Unix only
if pid == 0:
    print("子进程")
else:
    print(f"父进程，子进程PID: {pid}")

# 等待子进程
pid, status = os.wait()

# 执行新程序（替换当前进程）
# os.execl('/bin/ls', 'ls', '-la')

# ========== 文件描述符 ==========
# 打开文件（低级别）
fd = os.open('file.txt', os.O_RDONLY)

# 读取
data = os.read(fd, 1024)

# 关闭
os.close(fd)

# 管道
r, w = os.pipe()
os.write(w, b'hello')
os.read(r, 1024)

# ========== 最佳实践 ==========
"""
1. 文件路径使用pathlib而非os.path
2. 执行命令使用subprocess而非os.system
3. 使用exist_ok避免竞争条件
4. 使用上下文管理器确保资源释放
"""

# 好的实践
from pathlib import Path
import subprocess

# 创建目录
Path('mydir').mkdir(parents=True, exist_ok=True)

# 执行命令
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)
```

#### sys模块

```python
"""
sys模块提供与Python解释器交互的功能。
核心功能：命令行参数、路径管理、模块信息、解释器控制。
"""

import sys

# ========== 命令行参数 ==========
# sys.argv[0] 是脚本名
# sys.argv[1:] 是传递给脚本的参数
print(f"脚本名: {sys.argv[0]}")
print(f"参数: {sys.argv[1:]}")

# 示例: python script.py arg1 arg2
# sys.argv = ['script.py', 'arg1', 'arg2']

# ========== 路径管理 ==========
# sys.path - 模块搜索路径
print("模块搜索路径:")
for p in sys.path:
    print(f"  {p}")

# 动态添加路径
sys.path.insert(0, '/my/modules')

# ========== 模块信息 ==========
# 已加载模块
print(f"已加载模块数: {len(sys.modules)}")
print(f"是否有os模块: 'os' in sys.modules")

# 获取模块信息
if 'os' in sys.modules:
    print(f"os模块路径: {sys.modules['os'].__file__}")

# ========== 解释器信息 ==========
print(f"Python版本: {sys.version}")
print(f"版本信息: {sys.version_info}")  # (major, minor, micro, releaselevel, serial)
print(f"平台: {sys.platform}")  # 'linux', 'darwin', 'win32'
print(f"可执行文件: {sys.executable}")
print(f"前缀: {sys.prefix}")  # 安装前缀
print(f"字节序: {sys.byteorder}")  # 'little' 或 'big'

# ========== 标准流 ==========
# sys.stdin - 标准输入
# sys.stdout - 标准输出
# sys.stderr - 标准错误

# 重定向输出
original_stdout = sys.stdout
with open('output.txt', 'w') as f:
    sys.stdout = f
    print("这会被写入文件")
sys.stdout = original_stdout

# 更好的方式使用上下文管理器
from contextlib import redirect_stdout
with open('output.txt', 'w') as f:
    with redirect_stdout(f):
        print("这会被写入文件")

# ========== 退出与异常 ==========
# 正常退出
# sys.exit(0)  # 或 sys.exit()

# 异常退出
# sys.exit(1)  # 非零表示错误

# 带消息的退出
# sys.exit("Error: invalid input")

# 获取当前异常信息（在except块中）
try:
    1 / 0
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f"异常类型: {exc_type}")
    print(f"异常值: {exc_value}")

# ========== 递归限制 ==========
print(f"默认递归限制: {sys.getrecursionlimit()}")
sys.setrecursionlimit(2000)  # 谨慎修改

# ========== 垃圾回收 ==========
import gc
print(f"引用计数: {sys.getrefcount('hello')}")

# ========== 性能分析 ==========
# 获取对象大小
print(f"int大小: {sys.getsizeof(42)} bytes")
print(f"list大小: {sys.getsizeof([1, 2, 3])} bytes")
print(f"str大小: {sys.getsizeof('hello')} bytes")

# ========== 导入钩子 ==========
# sys.meta_path - 元路径查找器
print(f"元路径查找器: {sys.meta_path}")

# sys.path_hooks - 路径钩子
print(f"路径钩子: {sys.path_hooks}")

# sys.path_importer_cache - 导入器缓存
print(f"导入器缓存: {list(sys.path_importer_cache.keys())}")

# ========== 最佳实践 ==========
"""
1. 使用argparse而非直接解析sys.argv
2. 谨慎修改sys.path，优先使用PYTHONPATH
3. 使用logging而非直接写sys.stderr
4. 避免修改递归限制，重构代码更好
"""

# 好的命令行参数处理
import argparse

parser = argparse.ArgumentParser(description='示例程序')
parser.add_argument('input', help='输入文件')
parser.add_argument('-o', '--output', help='输出文件')
parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
args = parser.parse_args()

print(f"输入: {args.input}")
print(f"输出: {args.output}")
print(f"详细: {args.verbose}")
```


#### pathlib模块

```python
"""
pathlib是Python 3.4+引入的面向对象路径操作模块。
相比os.path，它更直观、功能更丰富、跨平台更好。
"""

from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath

# ========== 创建路径 ==========
# 当前目录
p = Path('.')

# 绝对路径
p = Path('/usr/bin/python')
p = Path('C:/Windows/System32')

# 从字符串构造
p = Path('dir', 'subdir', 'file.txt')

# 用户主目录
home = Path.home()

# 当前工作目录
cwd = Path.cwd()

# ========== 路径属性 ==========
p = Path('/usr/bin/python3')

print(f"字符串表示: {str(p)}")
print(f"组成部分: {p.parts}")          # ('/', 'usr', 'bin', 'python3')
print(f"驱动器: {p.drive}")             # '' (Unix) 或 'C:' (Windows)
print(f"根目录: {p.root}")              # '/' 或 '\\'
print(f"锚点: {p.anchor}")              # '/' 或 'C:\\'
print(f"父目录: {p.parent}")            # /usr/bin
print(f"所有父目录: {list(p.parents)}") # [Path('/usr/bin'), Path('/usr'), Path('/')]
print(f"名称: {p.name}")                # python3
print(f"后缀: {p.suffix}")              # '' (无后缀)
print(f"所有后缀: {p.suffixes}")        # []
print(f"纯名称: {p.stem}")              # python3

p = Path('archive.tar.gz')
print(f"名称: {p.name}")                # archive.tar.gz
print(f"后缀: {p.suffix}")              # .gz
print(f"所有后缀: {p.suffixes}")        # ['.tar', '.gz']
print(f"纯名称: {p.stem}")              # archive.tar

# ========== 路径操作 ==========
# 拼接路径
p = Path('/etc')
new_path = p / 'nginx' / 'nginx.conf'  # /etc/nginx/nginx.conf

# 使用joinpath
new_path = p.joinpath('nginx', 'nginx.conf')

# 相对路径计算
p1 = Path('/etc/nginx/nginx.conf')
p2 = Path('/etc/ssl')
rel = p1.relative_to(p2.parent)  # ssl/../nginx/nginx.conf

# 解析相对路径
p = Path('/etc/nginx/../ssl/nginx.conf').resolve()  # /etc/ssl/nginx.conf

# ========== 文件系统操作 ==========
p = Path('example.txt')

# 检查存在
if p.exists():
    print("文件存在")

# 检查类型
if p.is_file():
    print("是普通文件")
if p.is_dir():
    print("是目录")
if p.is_symlink():
    print("是符号链接")

# 检查权限
if p.is_readable():
    print("可读")
if p.is_writable():
    print("可写")
if p.is_absolute():
    print("是绝对路径")

# ========== 目录操作 ==========
# 创建目录
Path('new_dir').mkdir()                          # 创建单级
Path('a/b/c').mkdir(parents=True)                # 递归创建
Path('new_dir').mkdir(exist_ok=True)             # 存在不报错

# 创建文件
Path('new_file.txt').touch()                     # 创建空文件
Path('new_file.txt').touch(exist_ok=True)        # 存在不报错

# 删除
Path('file.txt').unlink()                        # 删除文件
Path('file.txt').unlink(missing_ok=True)         # 不存在不报错
Path('empty_dir').rmdir()                        # 删除空目录

# 重命名/移动
Path('old.txt').rename('new.txt')
Path('src.txt').replace('dst.txt')               # 覆盖目标

# 符号链接
Path('link.txt').symlink_to('target.txt')
Path('link.txt').hardlink_to('target.txt')

# 读取链接
print(Path('link.txt').readlink())

# ========== 文件读写 ==========
p = Path('data.txt')

# 文本读写
p.write_text('Hello, World!', encoding='utf-8')
content = p.read_text(encoding='utf-8')

# 二进制读写
p.write_bytes(b'\x00\x01\x02\x03')
data = p.read_bytes()

# 打开文件（返回文件对象）
with p.open('r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())

# ========== 遍历目录 ==========
# 列出目录内容
for entry in Path('.').iterdir():
    print(entry)

# 递归遍历
for path in Path('.').rglob('*.py'):  # 递归查找所有.py文件
    print(path)

# 非递归通配
for path in Path('.').glob('*.txt'):  # 当前目录的.txt文件
    print(path)

# 模式匹配
for path in Path('.').glob('**/*.py'):  # 同rglob
    print(path)

# 遍历并筛选
for path in Path('.').rglob('*'):
    if path.is_file() and path.stat().st_size > 1024:
        print(f"大文件: {path} ({path.stat().st_size} bytes)")

# ========== 文件信息 ==========
p = Path('example.txt')
stat = p.stat()
print(f"大小: {stat.st_size}")
print(f"修改时间: {stat.st_mtime}")
print(f"访问时间: {stat.st_atime}")
print(f"创建时间: {stat.st_ctime}")

# 修改时间戳
import time
p.touch()  # 更新访问和修改时间

# ========== 纯路径（不访问文件系统） ==========
# PurePath用于路径操作而不实际访问文件

# 跨平台路径表示
posix_path = PurePosixPath('/usr/bin/python')
windows_path = PureWindowsPath('C:/Windows/System32')

# 路径比较
print(PurePosixPath('/etc') == PurePosixPath('/etc/'))  # True
print(PurePosixPath('/etc') < PurePosixPath('/usr'))     # True

# 路径匹配
print(Path('src/main.py').match('src/*.py'))      # True
print(Path('src/main.py').match('**/*.py'))       # True

# ========== 最佳实践 ==========
"""
1. 新项目优先使用pathlib而非os.path
2. 使用/运算符拼接路径，比字符串拼接更安全
3. 使用resolve()获取规范化的绝对路径
4. 使用rglob()替代os.walk()进行递归遍历
5. 使用with_suffix()和with_stem()修改路径
"""

# 好的实践示例

def find_python_files(directory: Path) -> list[Path]:
    """查找目录下所有Python文件"""
    return list(directory.rglob('*.py'))

def backup_file(file_path: Path) -> Path:
    """创建文件备份"""
    backup = file_path.with_suffix(file_path.suffix + '.bak')
    backup.write_bytes(file_path.read_bytes())
    return backup

def ensure_dir(path: Path) -> Path:
    """确保目录存在，不存在则创建"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_project_root() -> Path:
    """获取项目根目录（假设当前文件在src/下）"""
    return Path(__file__).parent.parent

# 使用示例
project_root = get_project_root()
data_dir = ensure_dir(project_root / 'data')
config_file = project_root / 'config' / 'app.yaml'
```

#### shutil模块

```python
"""
shutil提供高级文件操作功能。
核心功能：复制、移动、删除、归档、磁盘操作。
"""

import shutil
from pathlib import Path

# ========== 复制操作 ==========
# 复制文件
shutil.copy('src.txt', 'dst.txt')           # 复制文件，保留权限
shutil.copy2('src.txt', 'dst.txt')          # 复制文件，保留更多元数据

# 复制到目录
shutil.copy('file.txt', '/tmp/')            # 复制到/tmp/file.txt

# 复制文件对象
with open('src.txt', 'rb') as fsrc:
    with open('dst.txt', 'wb') as fdst:
        shutil.copyfileobj(fsrc, fdst)

# 仅复制文件内容（不复制权限）
shutil.copyfile('src.txt', 'dst.txt')

# 复制目录树
shutil.copytree('src_dir', 'dst_dir')                    # 复制整个目录
shutil.copytree('src_dir', 'dst_dir', dirs_exist_ok=True)  # 目标存在也继续

# 复制时忽略某些文件
shutil.copytree(
    'src_dir', 'dst_dir',
    ignore=shutil.ignore_patterns('*.pyc', '__pycache__')
)

# 自定义忽略函数
def ignore_git(dir, files):
    return {f for f in files if f == '.git'}

shutil.copytree('src_dir', 'dst_dir', ignore=ignore_git)

# ========== 移动操作 ==========
shutil.move('src.txt', 'dst.txt')           # 移动文件
shutil.move('src_dir', 'dst_dir')           # 移动目录
shutil.move('file.txt', '/tmp/')            # 移动到目录

# ========== 删除操作 ==========
# 删除整个目录树（危险！）
shutil.rmtree('dir_to_remove')

# 安全删除（忽略错误）
shutil.rmtree('dir', ignore_errors=True)

# 删除时处理错误
def onerror(func, path, exc_info):
    import stat
    # 修改权限后重试
    os.chmod(path, stat.S_IWRITE)
    func(path)

shutil.rmtree('dir', onerror=onerror)

# ========== 磁盘操作 ==========
# 获取磁盘使用情况
total, used, free = shutil.disk_usage('/')
print(f"总空间: {total // (2**30)} GB")
print(f"已用: {used // (2**30)} GB")
print(f"可用: {free // (2**30)} GB")

# ========== 归档操作 ==========
# 创建压缩包
shutil.make_archive('backup', 'zip', 'data_dir')        # 创建backup.zip
shutil.make_archive('backup', 'tar', 'data_dir')        # 创建backup.tar
shutil.make_archive('backup', 'gztar', 'data_dir')      # 创建backup.tar.gz
shutil.make_archive('backup', 'bztar', 'data_dir')      # 创建backup.tar.bz2
shutil.make_archive('backup', 'xztar', 'data_dir')      # 创建backup.tar.xz

# 解压缩
shutil.unpack_archive('backup.zip', 'extract_dir')
shutil.unpack_archive('backup.tar.gz', 'extract_dir')

# 获取支持的格式
print(shutil.get_archive_formats())      # 创建格式
print(shutil.get_unpack_formats())       # 解压格式

# ========== 查询操作 ==========
# 获取终端大小
columns, lines = shutil.get_terminal_size()
print(f"终端: {columns}x{lines}")

# 获取哪个程序打开某种文件
print(shutil.which('python'))            # /usr/bin/python
print(shutil.which('python.exe'))        # Windows

# ========== 最佳实践 ==========
"""
1. 复制目录使用copytree，文件使用copy2
2. 删除前确认路径，避免误删
3. 使用pathlib配合shutil更直观
4. 大文件复制考虑使用copyfileobj控制缓冲区
"""

# 好的实践：安全复制
def safe_copy(src: Path, dst: Path, overwrite: bool = False) -> Path:
    """安全复制文件"""
    if not src.exists():
        raise FileNotFoundError(f"源文件不存在: {src}")
    if dst.exists() and not overwrite:
        raise FileExistsError(f"目标已存在: {dst}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst

# 好的实践：带进度的大文件复制
def copy_with_progress(src: Path, dst: Path, chunk_size: int = 1024*1024):
    """带进度显示的文件复制"""
    size = src.stat().st_size
    copied = 0

    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        while True:
            chunk = fsrc.read(chunk_size)
            if not chunk:
                break
            fdst.write(chunk)
            copied += len(chunk)
            print(f"\r进度: {copied/size*100:.1f}%", end='')
    print()
```

#### glob模块

```python
"""
glob模块使用Unix shell风格的通配符查找文件。
注意：pathlib的glob方法更现代，推荐优先使用。
"""

import glob
from pathlib import Path

# ========== 基本匹配 ==========
# 当前目录所有py文件
py_files = glob.glob('*.py')

# 递归匹配（**匹配任意目录）
all_py = glob.glob('**/*.py', recursive=True)

# 特定目录
config_files = glob.glob('/etc/*.conf')

# ========== 通配符规则 ==========
# *      匹配任意非空字符串（不含/）
# **     匹配任意字符串（含/），需要recursive=True
# ?      匹配单个字符
# [seq]  匹配seq中的任意字符
# [!seq] 匹配不在seq中的字符

# 示例
glob.glob('file?.txt')        # file1.txt, fileA.txt
glob.glob('file[0-9].txt')    # file0.txt, file1.txt, ...
glob.glob('file[!0-9].txt')   # fileA.txt, file_.txt, ...

# ========== 转义特殊字符 ==========
glob.glob('file\*.txt')       # 匹配字面量file*.txt
glob.glob('file[[]1[]].txt')  # 匹配file[1].txt

# ========== 返回Path对象 ==========
py_paths = glob.glob('*.py', root_dir='/home/user')

# ========== iglob（迭代器，节省内存） ==========
for path in glob.iglob('**/*.py', recursive=True):
    print(path)

# ========== 与pathlib对比 ==========
# glob方式
import glob
files = glob.glob('src/**/*.py', recursive=True)

# pathlib方式（推荐）
from pathlib import Path
files = list(Path('src').rglob('*.py'))

# pathlib优势：
# 1. 返回Path对象而非字符串
# 2. 可以直接调用文件操作方法
# 3. 更面向对象
```

#### tempfile模块

```python
"""
tempfile模块创建临时文件和目录。
核心功能：安全创建、自动清理、跨平台。
"""

import tempfile
from pathlib import Path

# ========== 临时文件 ==========
# 最基本的临时文件
with tempfile.TemporaryFile() as f:
    f.write(b'Hello, World!')
    f.seek(0)
    data = f.read()
# 退出with块自动删除

# 文本模式
with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as f:
    f.write('Hello, World!')
    f.seek(0)
    text = f.read()

# 命名临时文件（有文件名）
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=True) as f:
    f.write('content')
    print(f"临时文件: {f.name}")
# 默认delete=True，退出时删除

# 不自动删除的命名临时文件
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write('content')
    temp_path = f.name
# 需要手动删除
import os
os.unlink(temp_path)

# ========== 临时目录 ==========
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"临时目录: {tmpdir}")
    # 在目录中创建文件
    path = Path(tmpdir) / 'file.txt'
    path.write_text('content')
# 退出with块自动删除整个目录

# ========== 低级函数 ==========
# 生成临时文件名（不创建文件）
name = tempfile.mktemp(suffix='.tmp', prefix='tmp')
print(f"生成的名称: {name}")  # 不推荐，有竞争条件风险

# 创建临时文件（低级）
fd, path = tempfile.mkstemp(suffix='.txt', text=True)
os.write(fd, b'content')
os.close(fd)
os.unlink(path)

# 创建临时目录（低级）
tmpdir = tempfile.mkdtemp(prefix='myapp_')
print(f"临时目录: {tmpdir}")
# 需要手动清理
import shutil
shutil.rmtree(tmpdir)

# ========== 配置 ==========
# 指定临时文件目录
tempfile.tempdir = '/my/temp/dir'

# 获取临时目录
tmp_dir = tempfile.gettempdir()
print(f"系统临时目录: {tmp_dir}")

# 获取临时文件名前缀
tmp_prefix = tempfile.gettempprefix()
print(f"默认前缀: {tmp_prefix}")  # tmp

# ========== 最佳实践 ==========
"""
1. 优先使用上下文管理器（with语句）
2. 需要文件名时用NamedTemporaryFile
3. 多文件操作时用TemporaryDirectory
4. 不要依赖临时文件长期存在
5. 敏感数据确保正确删除
"""

# 好的实践：处理大文件的临时目录
def process_large_file(input_path: Path) -> Path:
    """处理大文件，使用临时目录存储中间结果"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # 分块处理
        chunk_path = tmp_path / 'chunk'
        with open(input_path, 'rb') as src:
            while chunk := src.read(1024 * 1024):  # 1MB chunks
                chunk_path.write_bytes(chunk)
                process_chunk(chunk_path)

        # 合并结果
        result_path = tmp_path / 'result'
        merge_results(tmp_path, result_path)

        # 返回结果（复制到持久位置）
        final_path = Path('/output/result.dat')
        shutil.copy(result_path, final_path)
        return final_path

def process_chunk(path: Path):
    pass

def merge_results(tmpdir: Path, output: Path):
    pass
```

---

### 3.2 数据结构模块

#### collections模块

```python
"""
collections模块提供额外的专用容器数据类型。
核心类型：Counter, defaultdict, OrderedDict, deque, namedtuple, ChainMap
"""

from collections import (
    Counter, defaultdict, OrderedDict, deque,
    namedtuple, ChainMap, UserDict, UserList, UserString
)

# ========== Counter：计数器 ==========
"""
Counter是dict的子类，用于计数可哈希对象。
"""

# 创建
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
counter = Counter(words)
print(counter)  # Counter({'apple': 3, 'banana': 2, 'orange': 1})

# 从字符串创建
c = Counter('abracadabra')
print(c)  # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# 常用方法
print(counter.most_common(2))  # [('apple', 3), ('banana', 2)]
print(counter.elements())       # 迭代所有元素（按计数重复）
print(list(counter.elements())) # ['apple', 'apple', 'apple', 'banana', 'banana', 'orange']

# 数学运算
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})  相加
print(c1 - c2)  # Counter({'a': 2})  相减（结果为正）
print(c1 & c2)  # Counter({'a': 1, 'b': 1})  取最小值
print(c1 | c2)  # Counter({'a': 3, 'b': 2})  取最大值

# 更新计数
counter.update(['apple', 'cherry'])  # 增加
counter.subtract(['apple'])          # 减少

# ========== defaultdict：默认字典 ==========
"""
defdict为不存在的键提供默认值，避免KeyError。
"""

# 基本用法
dd = defaultdict(int)      # 默认值为0
dd = defaultdict(list)     # 默认值为[]
dd = defaultdict(set)      # 默认值为set()
dd = defaultdict(dict)     # 默认值为{}

# 分组示例
groups = defaultdict(list)
for key, value in [('a', 1), ('b', 2), ('a', 3)]:
    groups[key].append(value)
print(groups)  # defaultdict({'a': [1, 3], 'b': [2]})

# 自定义默认值函数
def default_value():
    return "N/A"

dd = defaultdict(default_value)
print(dd['missing'])  # N/A

# 使用lambda
dd = defaultdict(lambda: 0)
dd['x'] += 1
print(dd['x'])  # 1

# 计数示例（替代Counter）
counts = defaultdict(int)
for word in ['a', 'b', 'a', 'c', 'a']:
    counts[word] += 1

# ========== OrderedDict：有序字典 ==========
"""
OrderedDict保持键的插入顺序。
注意：Python 3.7+普通dict也保持顺序，OrderedDict仍有特殊用途。
"""

od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3

# 移动到末尾/开头
od.move_to_end('a')       # 移动到最后
od.move_to_end('b', last=False)  # 移动到开头

# 反转
reversed_od = OrderedDict(reversed(od.items()))

# 相等性比较（顺序敏感）
od1 = OrderedDict([('a', 1), ('b', 2)])
od2 = OrderedDict([('b', 2), ('a', 1)])
print(od1 == od2)  # False（顺序不同）

d1 = {'a': 1, 'b': 2}
d2 = {'b': 2, 'a': 1}
print(d1 == d2)    # True（普通dict不考虑顺序）

# 实际用途：LRU缓存实现
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# ========== deque：双端队列 ==========
"""
deque（double-ended queue）支持O(1)的两端操作。
"""

# 创建
d = deque()
d = deque([1, 2, 3])
d = deque('abc', maxlen=5)  # 限制最大长度

# 两端操作
d.append(4)         # 右端添加
d.appendleft(0)     # 左端添加
d.pop()             # 右端移除
d.popleft()         # 左端移除

# 批量添加
d.extend([5, 6, 7])
d.extendleft([-1, -2, -3])  # 注意顺序：-3, -2, -1

# 旋转
d = deque([1, 2, 3, 4, 5])
d.rotate(2)         # 右旋：deque([4, 5, 1, 2, 3])
d.rotate(-2)        # 左旋：deque([1, 2, 3, 4, 5])

# 其他操作
d.clear()           # 清空
d.copy()            # 浅拷贝
d.count(3)          # 计数
d.index(3)          # 查找索引
d.insert(2, 99)     # 插入
d.remove(3)         # 移除第一个匹配项

# 限制长度（环形缓冲区）
d = deque(maxlen=3)
d.extend([1, 2, 3])
d.append(4)         # 自动移除最老的元素1
d.appendleft(0)     # 自动移除最老的元素3
print(list(d))      # [0, 2, 4]

# 实际用途：滑动窗口
def moving_average(iterable, n=3):
    it = iter(iterable)
    d = deque(maxlen=n)
    for x in it:
        d.append(x)
        if len(d) == n:
            yield sum(d) / n

print(list(moving_average([1, 2, 3, 4, 5, 6], 3)))  # [2.0, 3.0, 4.0, 5.0]

# ========== namedtuple：命名元组 ==========
"""
namedtuple创建带有命名字段的元组子类。
"""

from typing import NamedTuple

# 传统方式
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)     # 1 2
print(p[0], p[1])   # 1 2（仍是元组）

# 字符串定义字段
Person = namedtuple('Person', 'name age city')

# 默认值（Python 3.7+）
Person = namedtuple('Person', 'name age city', defaults=['Unknown'])
p = Person('Alice', 30)
print(p)  # Person(name='Alice', age=30, city='Unknown')

# 类型提示方式（Python 3.6+）
class Point(NamedTuple):
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

p = Point(3, 4)
print(p.distance_from_origin())  # 5.0

# 转换
d = {'x': 1, 'y': 2}
p = Point(**d)      # 从字典创建

# 替换（创建新实例）
p2 = p._replace(x=10)

# 转换为字典
d = p._asdict()

# ========== ChainMap：链式映射 ==========
"""
ChainMap将多个字典逻辑上合并，不创建新字典。
"""

d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
cm = ChainMap(d1, d2)

print(cm['a'])  # 1（来自d1）
print(cm['b'])  # 2（来自d1，d1优先）
print(cm['c'])  # 4（来自d2）

# 添加新字典到链
d3 = {'d': 5}
cm = cm.new_child(d3)

# 修改
cm['a'] = 10      # 修改d1中的'a'
cm['e'] = 6       # 添加到第一个字典

# 实际用途：配置层级
import argparse
import os

def get_config():
    defaults = {'theme': 'default', 'debug': False}
    env_vars = {k.lower(): v for k, v in os.environ.items() if k.startswith('APP_')}

    parser = argparse.ArgumentParser()
    parser.add_argument('--theme')
    parser.add_argument('--debug', action='store_true')
    args = vars(parser.parse_args())
    args = {k: v for k, v in args.items() if v is not None}

    # 优先级：命令行 > 环境变量 > 默认值
    return ChainMap(args, env_vars, defaults)

# ========== 最佳实践 ==========
"""
1. 计数用Counter，比手动dict更简洁
2. 分组用defaultdict(list/set)
3. 需要顺序敏感的操作用OrderedDict
4. 双端操作用deque，比list快
5. 结构化数据用namedtuple或dataclass
6. 配置层级用ChainMap
"""
```

#### dataclasses模块

```python
"""
dataclasses模块（Python 3.7+）自动为类生成特殊方法。
核心功能：自动生成__init__, __repr__, __eq__等。
"""

from dataclasses import dataclass, field, asdict, astuple, replace
from typing import List, Optional
from datetime import datetime

# ========== 基础用法 ==========
@dataclass
class Person:
    name: str
    age: int

p = Person('Alice', 30)
print(p)  # Person(name='Alice', age=30)
print(p.name)  # Alice

# ========== 参数详解 ==========
@dataclass(
    init=True,      # 生成__init__
    repr=True,      # 生成__repr__
    eq=True,        # 生成__eq__
    order=False,    # 生成__lt__, __le__, __gt__, __ge__
    unsafe_hash=False,  # 生成__hash__
    frozen=False,   # 不可变实例
    match_args=True,
    kw_only=False,
    slots=False,
    weakref_slot=False,
)
class Config:
    pass

# ========== 不可变数据类 ==========
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1, 2)
# p.x = 3  # FrozenInstanceError

# ========== 默认值 ==========
@dataclass
class Book:
    title: str
    author: str
    published: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)  # 可变默认值必须用field

# 错误示范：不要这样做
# tags: List[str] = []  # 所有实例共享同一个列表！

# ========== field函数 ==========
@dataclass
class Product:
    name: str
    price: float = field(
        default=0.0,
        repr=True,           # 包含在__repr__中
        compare=True,        # 包含在比较中
        hash=None,           # 包含在__hash__中（None表示跟随compare）
        metadata={'unit': 'USD'}  # 元数据
    )
    quantity: int = field(default=0, compare=False)  # 不参与比较

    # 使用metadata
    def get_metadata(self, field_name):
        return self.__dataclass_fields__[field_name].metadata

# ========== __post_init__ ==========
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # 不在__init__中

    def __post_init__(self):
        self.area = self.width * self.height

r = Rectangle(3, 4)
print(r.area)  # 12

# ========== 继承 ==========
@dataclass
class Employee(Person):
    employee_id: int
    department: str = 'Engineering'

# 子类字段排在父类字段之后
e = Employee('Bob', 25, 1001)
print(e)  # Employee(name='Bob', age=25, employee_id=1001, department='Engineering')

# ========== 实用函数 ==========
p = Person('Alice', 30)

# 转字典
d = asdict(p)  # {'name': 'Alice', 'age': 30}

# 转元组
t = astuple(p)  # ('Alice', 30)

# 创建副本并修改
p2 = replace(p, age=31)  # Person(name='Alice', age=31)

# ========== 与typing.NamedTuple对比 ==========
"""
dataclass vs NamedTuple:

1. 可变性：dataclass默认可变，NamedTuple不可变
2. 继承：dataclass支持更好
3. 性能：NamedTuple略快（基于元组）
4. 功能：dataclass更灵活（__post_init__等）
5. 选择：需要可变或复杂逻辑用dataclass
"""

# ========== 高级用法：slots ==========
@dataclass(slots=True)
class CompactPoint:
    x: float
    y: float

# slots节省内存，禁止动态添加属性
# p = CompactPoint(1, 2)
# p.z = 3  # AttributeError

# ========== 最佳实践 ==========
"""
1. 优先使用dataclass而非手写类
2. 可变默认值用field(default_factory=...)
3. 需要不可变性用frozen=True
4. 需要计算字段用__post_init__
5. 大量实例考虑slots=True节省内存
6. 简单不可变数据考虑NamedTuple
"""
```

#### enum模块

```python
"""
enum模块支持创建枚举类型。
核心功能：定义具名常量集合。
"""

from enum import Enum, IntEnum, Flag, IntFlag, auto, unique

# ========== 基础枚举 ==========
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# 访问
print(Color.RED)        # Color.RED
print(Color.RED.name)   # RED
print(Color.RED.value)  # 1

# 迭代
for color in Color:
    print(color)

# 成员检查
print(Color.RED in Color)  # True

# 获取成员
print(Color(1))         # Color.RED
print(Color['RED'])     # Color.RED

# ========== 自动值 ==========
class Status(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()

# 自动分配1, 2, 3, 4

# 自定义auto行为
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

class Status(AutoName):
    PENDING = auto()    # pending
    RUNNING = auto()    # running

# ========== 唯一值装饰器 ==========
@unique
class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    # URGENT = 1  # ValueError: duplicate values

# ========== IntEnum ==========
class HttpStatus(IntEnum):
    OK = 200
    NOT_FOUND = 404
    ERROR = 500

# 可以像整数一样比较
print(HttpStatus.OK == 200)  # True
print(HttpStatus.OK < 300)   # True

# ========== Flag ==========
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

# 组合权限
perms = Permission.READ | Permission.WRITE
print(perms)  # Permission.READ|WRITE

# 检查权限
print(Permission.READ in perms)  # True
print(perms & Permission.READ)   # Permission.READ

# 所有权限
print(Permission(0))  # Permission(0)
print(~Permission(0))  # Permission.READ|WRITE|EXECUTE

# ========== 带方法的枚举 ==========
class Planet(Enum):
    MERCURY = (3.303e+23, 2.4397e6)
    VENUS   = (4.869e+24, 6.0518e6)
    EARTH   = (5.976e+24, 6.37814e6)

    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius

    @property
    def surface_gravity(self):
        G = 6.673e-11
        return G * self.mass / (self.radius ** 2)

print(Planet.EARTH.surface_gravity)

# ========== 最佳实践 ==========
"""
1. 用枚举替代魔法数字和字符串常量
2. 使用@unique确保值唯一
3. 需要整数行为用IntEnum
4. 权限/选项用Flag
5. 复杂枚举可添加方法和属性
"""
```

#### typing模块

```python
"""
typing模块提供类型提示支持。
核心功能：静态类型检查、代码提示、文档。
"""

from typing import (
    List, Dict, Set, Tuple, Optional, Union, Any, Callable,
    TypeVar, Generic, Protocol, NamedTuple, TypedDict,
    Iterator, Iterable, Sequence, Mapping, MutableMapping,
    Final, Literal, NewType, NoReturn, ClassVar
)
from dataclasses import dataclass

# ========== 基础类型 ==========
# 列表
def process_list(items: List[int]) -> int:
    return sum(items)

# 字典
def get_config() -> Dict[str, str]:
    return {'key': 'value'}

# 集合
def unique_items(items: Set[str]) -> List[str]:
    return list(items)

# 元组（固定长度）
def get_point() -> Tuple[float, float]:
    return (1.0, 2.0)

# 元组（变长，同类型）
def get_numbers() -> Tuple[int, ...]:
    return (1, 2, 3, 4)

# ========== Optional和Union ==========
# Optional[X] 等价于 Union[X, None]
def find_user(user_id: int) -> Optional[str]:
    if user_id > 0:
        return f"User {user_id}"
    return None

# Union
def parse_value(value: str) -> Union[int, float, str]:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

# Python 3.10+ 可用 | 替代Union
# def parse_value(value: str) -> int | float | str:

# ========== Callable ==========
# 函数类型
def apply_operation(
    x: int,
    y: int,
    operation: Callable[[int, int], int]
) -> int:
    return operation(x, y)

# 任意参数
def log_call(func: Callable[..., Any]) -> None:
    print(f"Calling {func.__name__}")
    func()

# ========== 泛型 ==========
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# 泛型函数
def first(items: List[T]) -> Optional[T]:
    return items[0] if items else None

# 泛型类
@dataclass
class Stack(Generic[T]):
    items: List[T] = None

    def __post_init__(self):
        if self.items is None:
            self.items = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> Optional[T]:
        return self.items.pop() if self.items else None

# 使用
int_stack: Stack[int] = Stack()
int_stack.push(1)

# 泛型约束
Number = TypeVar('Number', int, float)

def add(x: Number, y: Number) -> Number:
    return x + y

# ========== Protocol（结构子类型） ==========
class Drawable(Protocol):
    def draw(self) -> None:
        ...

def render(item: Drawable) -> None:
    item.draw()

# 任何有draw方法的类都符合Drawable
class Circle:
    def draw(self) -> None:
        print("Drawing circle")

render(Circle())  # OK

# ========== TypedDict ==========
class Movie(TypedDict):
    name: str
    year: int
    rating: float

movie: Movie = {
    'name': 'Inception',
    'year': 2010,
    'rating': 8.8
}

# 可选字段
class User(TypedDict, total=False):
    name: str
    age: int
    email: str

# ========== Final和Literal ==========
# Final：不可重新赋值
MAX_SIZE: Final[int] = 100

# Literal：限定具体值
def set_level(level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR']) -> None:
    pass

set_level('DEBUG')  # OK
# set_level('UNKNOWN')  # 类型错误

# ========== NewType ==========
# 创建语义化类型
UserId = NewType('UserId', int)
AccountId = NewType('AccountId', int)

def get_user(user_id: UserId) -> str:
    return f"User {user_id}"

user_id = UserId(123)
# account_id = AccountId(456)
# get_user(account_id)  # 类型警告

# ========== 最佳实践 ==========
"""
1. 为函数参数和返回值添加类型
2. 复杂类型使用TypeAlias（Python 3.10+）
3. 泛型提高代码复用性
4. Protocol实现鸭子类型
5. 使用mypy或pyright进行静态检查
6. 渐进式添加类型，不必一次完成
"""

# 类型别名
from typing import TypeAlias  # Python 3.10+

JsonDict: TypeAlias = Dict[str, Any]
Vector: TypeAlias = List[float]
Matrix: TypeAlias = List[Vector]
```


---

### 3.3 函数式编程模块

#### itertools模块

```python
"""
itertools提供高效的迭代器工具，用于创建和操作迭代器。
核心功能：无限迭代器、组合生成器、分组工具。
"""

import itertools
from typing import Iterable, Iterator, TypeVar

T = TypeVar('T')

# ========== 无限迭代器 ==========

# count(start=0, step=1) - 无限计数
for i in itertools.count(10, 2):
    if i > 20:
        break
    print(i)  # 10, 12, 14, 16, 18, 20

# cycle(iterable) - 无限循环
counter = 0
for item in itertools.cycle(['A', 'B', 'C']):
    print(item)
    counter += 1
    if counter >= 6:
        break  # A, B, C, A, B, C

# repeat(elem [,n]) - 重复元素
for x in itertools.repeat('Hello', 3):
    print(x)  # Hello, Hello, Hello

# 与map结合
squares = list(map(pow, range(10), itertools.repeat(2)))
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# ========== 有限迭代器 ==========

# accumulate(iterable[, func, *, initial=None]) - 累积
data = [1, 2, 3, 4, 5]
print(list(itertools.accumulate(data)))  # [1, 3, 6, 10, 15]

# 自定义函数
import operator
print(list(itertools.accumulate(data, operator.mul)))  # [1, 2, 6, 24, 120]

# 最大值累积
print(list(itertools.accumulate([3, 1, 4, 1, 5], max)))  # [3, 3, 4, 4, 5]

# chain(*iterables) - 连接迭代器
print(list(itertools.chain([1, 2], [3, 4], [5, 6])))  # [1, 2, 3, 4, 5, 6]

# chain.from_iterable(iterable) - 展平一层
print(list(itertools.chain.from_iterable([[1, 2], [3, 4]])))  # [1, 2, 3, 4]

# compress(data, selectors) - 选择性过滤
data = ['A', 'B', 'C', 'D', 'E']
selectors = [1, 0, 1, 0, 1]
print(list(itertools.compress(data, selectors)))  # ['A', 'C', 'E']

# dropwhile(predicate, iterable) - 跳过直到条件不满足
print(list(itertools.dropwhile(lambda x: x < 5, [1, 3, 5, 2, 4])))  # [5, 2, 4]

# takewhile(predicate, iterable) - 取直到条件不满足
print(list(itertools.takewhile(lambda x: x < 5, [1, 3, 5, 2, 4])))  # [1, 3]

# filterfalse(predicate, iterable) - 取不满足条件的
print(list(itertools.filterfalse(lambda x: x % 2, range(10))))  # [0, 2, 4, 6, 8]

# groupby(iterable, key=None) - 分组（需要已排序）
data = [('A', 1), ('A', 2), ('B', 3), ('B', 4), ('A', 5)]
data.sort(key=lambda x: x[0])  # 必须先排序！
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]
# A: [('A', 5)]

# islice(iterable, start, stop[, step]) - 切片
print(list(itertools.islice(range(10), 2, 8, 2)))  # [2, 4, 6]

# starmap(function, iterable) - 解包参数
print(list(itertools.starmap(pow, [(2, 5), (3, 2), (10, 3)])))  # [32, 9, 1000]

# tee(iterable, n=2) - 复制迭代器
iter1, iter2 = itertools.tee(range(3), 2)
print(list(iter1))  # [0, 1, 2]
print(list(iter2))  # [0, 1, 2]

# zip_longest(*iterables, fillvalue=None) - 不等长zip
print(list(itertools.zip_longest('ABC', 'xy', fillvalue='-')))  # [('A', 'x'), ('B', 'y'), ('C', '-')]

# ========== 组合生成器 ==========

# product(*iterables, repeat=1) - 笛卡尔积
print(list(itertools.product('AB', '12')))  # [('A', '1'), ('A', '2'), ('B', '1'), ('B', '2')]
print(list(itertools.product('AB', repeat=2)))  # [('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]

# permutations(iterable, r=None) - 排列
print(list(itertools.permutations('ABC', 2)))  # [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

# combinations(iterable, r) - 组合（无序）
print(list(itertools.combinations('ABC', 2)))  # [('A', 'B'), ('A', 'C'), ('B', 'C')]

# combinations_with_replacement(iterable, r) - 可重复组合
print(list(itertools.combinations_with_replacement('ABC', 2)))  # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]

# ========== 实用函数 ==========

def batched(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    """将迭代器分批（Python 3.12+有内置）"""
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator, n)):
        yield batch

# 使用
for batch in batched(range(10), 3):
    print(batch)  # (0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)

def pairwise(iterable: Iterable[T]) -> Iterator[tuple[T, T]]:
    """成对迭代（Python 3.10+有内置）"""
    iterator = iter(iterable)
    try:
        a = next(iterator)
    except StopIteration:
        return
    for b in iterator:
        yield a, b
        a = b

# 使用
print(list(pairwise('ABCDEFG')))  # [('A', 'B'), ('B', 'C'), ('C', 'D'), ...]

# ========== 最佳实践 ==========
"""
1. 无限序列用count, cycle, repeat
2. 展平列表用chain.from_iterable
3. 分组前务必排序
4. 笛卡尔积用product
5. 排列组合用permutations/combinations
6. 大迭代器用islice限制大小
"""
```

#### functools模块

```python
"""
functools提供高阶函数和可调用对象操作。
核心功能：缓存、偏函数、 reduce、装饰器。
"""

import functools
from typing import Callable

# ========== lru_cache - 缓存装饰器 ==========
@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """带缓存的斐波那契"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 查看缓存信息
print(fibonacci.cache_info())  # CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)

# 清除缓存
fibonacci.cache_clear()

# 无限制缓存
@functools.lru_cache(maxsize=None)
def expensive_function(x):
    pass

# 带类型的缓存（Python 3.9+）
@functools.cache  # 等价于 lru_cache(maxsize=None)
def cached_func(x):
    pass

# ========== partial - 偏函数 ==========
# 固定部分参数
basetwo = functools.partial(int, base=2)
print(basetwo('1010'))  # 10

# 关键字参数
print(basetwo('1010', base=10))  # 可以覆盖

# 实际应用：回调函数
def send_email(to: str, subject: str, body: str) -> None:
    print(f"To: {to}\nSubject: {subject}\nBody: {body}")

# 创建偏函数
send_to_admin = functools.partial(send_email, to='admin@example.com')
send_to_admin(subject='Alert', body='Something happened!')

# ========== reduce - 累积计算 ==========
from functools import reduce
import operator

# 求积
print(reduce(operator.mul, [1, 2, 3, 4, 5]))  # 120

# 找最大值
print(reduce(lambda x, y: x if x > y else y, [3, 1, 4, 1, 5]))  # 5

# 字符串连接
print(reduce(operator.add, ['a', 'b', 'c']))  # abc

# 扁平化列表（一层）
lists = [[1, 2], [3, 4], [5, 6]]
print(reduce(operator.add, lists))  # [1, 2, 3, 4, 5, 6]

# ========== wraps - 保留元数据 ==========
def my_decorator(func: Callable) -> Callable:
    @functools.wraps(func)  # 保留__name__, __doc__等
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"

print(greet.__name__)  # greet（不是wrapper）
print(greet.__doc__)   # Greet someone.

# ========== singledispatch - 函数重载 ==========
@functools.singledispatch
def process(arg):
    """默认实现"""
    raise NotImplementedError(f"Cannot process {type(arg)}")

@process.register(int)
def _(arg: int):
    return f"Integer: {arg}"

@process.register(str)
def _(arg: str):
    return f"String: {arg}"

@process.register(list)
def _(arg: list):
    return f"List with {len(arg)} items"

print(process(42))       # Integer: 42
print(process("hello"))  # String: hello
print(process([1, 2]))   # List with 2 items

# 类型组合（Python 3.7+）
@functools.singledispatchmethod
class Processor:
    @process.register
    def _(self, arg: dict):
        return f"Dict with {len(arg)} keys"

# ========== cmp_to_key - 比较函数转key ==========
# 旧式比较函数（返回-1, 0, 1）
def compare_length(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return -1
    elif len(s1) > len(s2):
        return 1
    return 0

# 转换后使用
words = ['apple', 'pie', 'banana', 'kiwi']
sorted_words = sorted(words, key=functools.cmp_to_key(compare_length))
print(sorted_words)  # ['pie', 'kiwi', 'apple', 'banana']

# ========== total_ordering - 自动生成比较方法 ==========
@functools.total_ordering
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

# 自动生成 __le__, __gt__, __ge__
p1 = Point(1, 2)
p2 = Point(2, 3)
print(p1 < p2)   # True
print(p1 <= p2)  # True
print(p1 > p2)   # False
print(p1 >= p2)  # False

# ========== 最佳实践 ==========
"""
1. 递归函数用lru_cache优化
2. 固定参数用partial创建特化函数
3. 累积操作用reduce
4. 装饰器用wraps保留元数据
5. 不同类型处理用singledispatch
6. 只需实现__eq__和__lt__，用total_ordering生成其他
"""
```

#### operator模块

```python
"""
operator模块提供与Python内置运算符对应的函数。
核心功能：函数式编程、高阶函数操作。
"""

import operator

# ========== 算术运算符 ==========
print(operator.add(1, 2))      # 3
print(operator.sub(5, 3))      # 2
print(operator.mul(4, 5))      # 20
print(operator.truediv(7, 2))  # 3.5
print(operator.floordiv(7, 2)) # 3
print(operator.mod(7, 4))      # 3
print(operator.pow(2, 3))      # 8
print(operator.neg(5))         # -5
print(operator.abs(-5))        # 5

# ========== 比较运算符 ==========
print(operator.eq(1, 1))   # True
print(operator.ne(1, 2))   # True
print(operator.lt(1, 2))   # True
print(operator.le(1, 1))   # True
print(operator.gt(2, 1))   # True
print(operator.ge(2, 2))   # True

# ========== 位运算符 ==========
print(operator.and_(0b1100, 0b1010))  # 0b1000 (8)
print(operator.or_(0b1100, 0b1010))   # 0b1110 (14)
print(operator.xor(0b1100, 0b1010))   # 0b0110 (6)
print(operator.invert(0b1100))        # -13
print(operator.lshift(1, 3))          # 8
print(operator.rshift(8, 2))          # 2

# ========== 序列操作 ==========
# 索引
data = [1, 2, 3, 4, 5]
print(operator.getitem(data, 2))  # 3

# 切片
print(operator.getitem(data, slice(1, 4)))  # [2, 3, 4]

# 设置值
operator.setitem(data, 2, 10)
print(data)  # [1, 2, 10, 4, 5]

# 删除
del data[2]
# operator.delitem(data, 2)

# 包含检查
print(operator.contains(data, 4))  # True

# 长度
print(operator.length_hint(data))  # 4

# 连接
print(operator.concat([1, 2], [3, 4]))  # [1, 2, 3, 4]

# 重复
print(operator.repeat([1, 2], 3))  # [1, 2, 1, 2, 1, 2]

# ========== 属性获取和调用 ==========
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"

p = Person('Alice', 30)

# 获取属性
print(operator.attrgetter('name')(p))  # Alice

# 获取多个属性
get_info = operator.attrgetter('name', 'age')
print(get_info(p))  # ('Alice', 30)

# 嵌套属性
# operator.attrgetter('address.city')

# 调用方法
call_greet = operator.methodcaller('greet')
print(call_greet(p))  # Hello, I'm Alice

# 带参数的方法调用
class Calculator:
    def add(self, x, y):
        return x + y

calc = Calculator()
add_five = operator.methodcaller('add', 5)
print(add_five(calc, 3))  # 8

# ========== 实际应用 ==========

# 1. 排序
students = [
    ('Alice', 25, 'A'),
    ('Bob', 20, 'B'),
    ('Charlie', 23, 'A'),
]

# 按年龄排序
sorted_by_age = sorted(students, key=operator.itemgetter(1))
print(sorted_by_age)

# 按成绩然后年龄排序
sorted_by_grade_age = sorted(students, key=operator.itemgetter(2, 1))
print(sorted_by_grade_age)

# 2. 对象列表排序
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

products = [Product('Apple', 1.5), Product('Banana', 0.8), Product('Cherry', 2.0)]
sorted_products = sorted(products, key=operator.attrgetter('price'))
print([p.name for p in sorted_products])  # ['Banana', 'Apple', 'Cherry']

# 3. 分组
data = [('A', 1), ('B', 2), ('A', 3), ('B', 4)]
from itertools import groupby
data.sort(key=operator.itemgetter(0))
for key, group in groupby(data, key=operator.itemgetter(0)):
    print(f"{key}: {list(group)}")

# 4. reduce操作
from functools import reduce
numbers = [1, 2, 3, 4, 5]
print(reduce(operator.add, numbers))  # 15
print(reduce(operator.mul, numbers))  # 120

# ========== 最佳实践 ==========
"""
1. 排序key用itemgetter/attrgetter比lambda快
2. reduce配合operator函数更简洁
3. 动态属性访问用attrgetter
4. 方法调用用methodcaller
"""
```

---

### 3.4 并发与异步模块

#### threading模块

```python
"""
threading提供基于线程的并行执行。
注意：由于GIL，线程适合IO密集型，不适合CPU密集型。
"""

import threading
import time
from queue import Queue

# ========== 基础线程 ==========
def worker(name: str) -> None:
    print(f"{name} 开始")
    time.sleep(1)
    print(f"{name} 结束")

# 创建并启动线程
thread = threading.Thread(target=worker, args=('Worker-1',))
thread.start()
thread.join()  # 等待完成

# ========== 线程类 ==========
class MyThread(threading.Thread):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def run(self) -> None:
        print(f"{self.name} 运行中")
        time.sleep(1)

thread = MyThread('Thread-1')
thread.start()
thread.join()

# ========== 线程同步 ==========

# Lock - 互斥锁
lock = threading.Lock()
counter = 0

def increment():
    global counter
    for _ in range(1000):
        with lock:  # 自动获取和释放
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"Counter: {counter}")  # 10000

# RLock - 可重入锁（同一线程可多次获取）
rlock = threading.RLock()
def recursive_function(n):
    with rlock:
        if n > 0:
            recursive_function(n - 1)

# Semaphore - 信号量（限制并发数）
semaphore = threading.Semaphore(3)  # 最多3个并发

def limited_worker():
    with semaphore:
        print(f"{threading.current_thread().name} 工作中")
        time.sleep(1)

# Event - 事件（线程间信号）
event = threading.Event()

def waiter():
    print("等待事件...")
    event.wait()  # 阻塞直到事件被设置
    print("事件已触发！")

def trigger():
    time.sleep(2)
    event.set()
    print("事件已设置")

threading.Thread(target=waiter).start()
threading.Thread(target=trigger).start()

# Condition - 条件变量
condition = threading.Condition()
shared_data = []

def producer():
    with condition:
        shared_data.append('item')
        print("生产了item")
        condition.notify()  # 通知消费者

def consumer():
    with condition:
        while not shared_data:
            condition.wait()  # 等待通知
        item = shared_data.pop()
        print(f"消费了{item}")

# Barrier - 屏障（等待所有线程到达）
barrier = threading.Barrier(3)

def barrier_worker():
    print(f"{threading.current_thread().name} 到达屏障")
    barrier.wait()  # 等待所有线程
    print(f"{threading.current_thread().name} 通过屏障")

# ========== 线程本地存储 ==========
local_data = threading.local()

def thread_function(value):
    local_data.value = value
    print(f"线程 {threading.current_thread().name}: {local_data.value}")

# ========== 线程池 ==========
from concurrent.futures import ThreadPoolExecutor

def fetch_url(url: str) -> str:
    time.sleep(1)
    return f"Data from {url}"

urls = ['http://a.com', 'http://b.com', 'http://c.com']

with ThreadPoolExecutor(max_workers=3) as executor:
    # 提交单个任务
    future = executor.submit(fetch_url, urls[0])
    result = future.result()

    # 批量提交
    results = list(executor.map(fetch_url, urls))
    print(results)

# ========== 守护线程 ==========
def daemon_worker():
    while True:
        print("守护线程工作中...")
        time.sleep(1)

daemon = threading.Thread(target=daemon_worker, daemon=True)
daemon.start()

# 主线程结束时，守护线程自动终止
time.sleep(3)
print("主线程结束")

# ========== 最佳实践 ==========
"""
1. 优先使用ThreadPoolExecutor而非手动管理线程
2. 始终使用锁保护共享数据
3. 避免死锁：按固定顺序获取多个锁
4. 使用Queue进行线程间通信
5. 守护线程用于后台任务
6. 注意GIL限制，CPU密集型用多进程
"""
```

#### multiprocessing模块

```python
"""
multiprocessing提供基于进程的并行执行。
绕过GIL，适合CPU密集型任务。
"""

import multiprocessing as mp
import time
import os

# ========== 基础进程 ==========
def worker(name: str) -> None:
    print(f"进程 {name} (PID: {os.getpid()}) 开始")
    time.sleep(1)
    print(f"进程 {name} 结束")

if __name__ == '__main__':
    process = mp.Process(target=worker, args=('Worker-1',))
    process.start()
    process.join()

# ========== 进程池 ==========
def square(n: int) -> int:
    return n * n

if __name__ == '__main__':
    with mp.Pool(processes=4) as pool:
        # map
        results = pool.map(square, range(10))
        print(results)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

        # apply_async
        result = pool.apply_async(square, (5,))
        print(result.get())  # 25

        # imap（惰性求值）
        for result in pool.imap(square, range(5)):
            print(result)

        # imap_unordered（无序返回）
        for result in pool.imap_unordered(square, range(5)):
            print(result)

# ========== 进程间通信 ==========

# Queue - 队列
if __name__ == '__main__':
    def producer(queue):
        for i in range(5):
            queue.put(i)
            print(f"生产: {i}")

    def consumer(queue):
        while True:
            item = queue.get()
            if item is None:  # 结束信号
                break
            print(f"消费: {item}")

    queue = mp.Queue()
    p1 = mp.Process(target=producer, args=(queue,))
    p2 = mp.Process(target=consumer, args=(queue,))

    p1.start()
    p2.start()
    p1.join()
    queue.put(None)  # 发送结束信号
    p2.join()

# Pipe - 管道（双向通信）
if __name__ == '__main__':
    def sender(conn):
        conn.send('Hello')
        conn.close()

    def receiver(conn):
        msg = conn.recv()
        print(f"收到: {msg}")

    parent_conn, child_conn = mp.Pipe()
    p1 = mp.Process(target=sender, args=(child_conn,))
    p2 = mp.Process(target=receiver, args=(parent_conn,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

# ========== 共享内存 ==========
if __name__ == '__main__':
    # Value - 共享单个值
    counter = mp.Value('i', 0)  # 'i' = 整数

    # Array - 共享数组
    shared_array = mp.Array('d', [1.0, 2.0, 3.0])  # 'd' = 双精度浮点

    def increment(counter):
        for _ in range(1000):
            with counter.get_lock():  # 需要锁保护
                counter.value += 1

    processes = [mp.Process(target=increment, args=(counter,)) for _ in range(10)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(f"Counter: {counter.value}")

# ========== Manager - 高级共享 ==========
if __name__ == '__main__':
    with mp.Manager() as manager:
        # 共享列表
        shared_list = manager.list([1, 2, 3])

        # 共享字典
        shared_dict = manager.dict({'key': 'value'})

        # 共享命名空间
        namespace = manager.Namespace()
        namespace.x = 10
        namespace.y = 20

        def worker(ns):
            ns.x += 1

        p = mp.Process(target=worker, args=(namespace,))
        p.start()
        p.join()

        print(f"namespace.x = {namespace.x}")  # 11

# ========== 进程同步 ==========
if __name__ == '__main__':
    # Lock
    lock = mp.Lock()

    # Semaphore
    semaphore = mp.Semaphore(2)

    # Event
    event = mp.Event()

    # Barrier
    barrier = mp.Barrier(3)

# ========== CPU密集型示例 ==========
def cpu_intensive(n: int) -> int:
    """CPU密集型计算"""
    count = 0
    for i in range(n):
        count += i * i
    return count

if __name__ == '__main__':
    numbers = [10_000_000] * 4

    # 串行
    start = time.time()
    results = [cpu_intensive(n) for n in numbers]
    print(f"串行: {time.time() - start:.2f}s")

    # 并行
    start = time.time()
    with mp.Pool() as pool:
        results = pool.map(cpu_intensive, numbers)
    print(f"并行: {time.time() - start:.2f}s")

# ========== 最佳实践 ==========
"""
1. CPU密集型用multiprocessing，IO密集型用threading
2. 始终使用if __name__ == '__main__'保护
3. 优先使用Pool简化进程管理
4. 大量数据交换考虑共享内存
5. 注意进程启动开销，小任务可能更慢
6. 进程数通常设为CPU核心数
"""
```


#### asyncio模块

```python
"""
asyncio提供异步IO、事件循环、协程和任务。
核心优势：单线程处理大量并发IO操作。
"""

import asyncio
import aiohttp  # 需要: pip install aiohttp
from typing import List

# ========== 基础协程 ==========
async def say_hello():
    print("Hello")
    await asyncio.sleep(1)  # 非阻塞等待
    print("World")

# 运行协程
asyncio.run(say_hello())

# ========== async/await ==========
async def fetch_data(url: str) -> str:
    print(f"Fetching {url}")
    await asyncio.sleep(1)  # 模拟IO
    return f"Data from {url}"

async def main():
    # 顺序执行
    result1 = await fetch_data('url1')
    result2 = await fetch_data('url2')
    print(result1, result2)

# ========== 并发执行 ==========
async def main_concurrent():
    # 方式1: gather
    results = await asyncio.gather(
        fetch_data('url1'),
        fetch_data('url2'),
        fetch_data('url3')
    )
    print(results)

    # 方式2: 创建任务
    task1 = asyncio.create_task(fetch_data('url1'))
    task2 = asyncio.create_task(fetch_data('url2'))
    result1 = await task1
    result2 = await task2

    # 方式3: wait
    tasks = [asyncio.create_task(fetch_data(f'url{i}')) for i in range(3)]
    done, pending = await asyncio.wait(tasks)
    for task in done:
        print(task.result())

# ========== 任务管理 ==========
async def task_management():
    # 创建任务
    task = asyncio.create_task(
        fetch_data('url'),
        name='fetch_task'
    )

    # 取消任务
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("任务已取消")

    # 超时
    try:
        result = await asyncio.wait_for(fetch_data('url'), timeout=5.0)
    except asyncio.TimeoutError:
        print("超时")

    # 屏蔽取消
    task = asyncio.create_task(fetch_data('url'))
    try:
        result = await asyncio.shield(task)
    except asyncio.CancelledError:
        await task  # 等待任务完成
        raise

# ========== 事件循环 ==========
# 获取当前循环
loop = asyncio.get_event_loop()

# 创建新循环
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 运行直到完成
result = loop.run_until_complete(say_hello())

# 运行 forever
# loop.run_forever()

# 关闭循环
loop.close()

# ========== 同步代码调用异步 ==========
def sync_main():
    # 在同步代码中运行异步
    result = asyncio.run(fetch_data('url'))

    # 或在已有循环中
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_data('url'))

# ========== 异步迭代器 ==========
class AsyncRange:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)  # 模拟异步操作
        value = self.i
        self.i += 1
        return value

async def use_async_iter():
    async for i in AsyncRange(5):
        print(i)

# ========== 异步上下文管理器 ==========
class AsyncConnection:
    async def __aenter__(self):
        print("Connecting...")
        await asyncio.sleep(0.5)
        print("Connected")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("Disconnecting...")
        await asyncio.sleep(0.5)
        print("Disconnected")

    async def send(self, data):
        print(f"Sending: {data}")

async def use_async_context():
    async with AsyncConnection() as conn:
        await conn.send("Hello")

# ========== 实际应用：并发HTTP请求 ==========
async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls: List[str]) -> List[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# 使用
urls = [
    'https://api.github.com',
    'https://httpbin.org/get',
    'https://jsonplaceholder.typicode.com/posts/1'
]
# results = asyncio.run(fetch_all(urls))

# ========== 信号量限制并发 ==========
async def bounded_fetch(urls: List[str], max_concurrent: int = 5) -> List[str]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_with_limit(session, url):
        async with semaphore:
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# ========== 队列 ==========
async def producer(queue: asyncio.Queue, n: int):
    for i in range(n):
        await queue.put(i)
        print(f"生产: {i}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # 结束信号

async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"消费: {item}")
        queue.task_done()

async def queue_example():
    queue = asyncio.Queue(maxsize=10)
    await asyncio.gather(
        producer(queue, 5),
        consumer(queue)
    )

# ========== 最佳实践 ==========
"""
1. IO密集型用asyncio，CPU密集型用多进程
2. 不要在协程中调用阻塞操作（用run_in_executor）
3. 使用gather并发执行独立任务
4. 使用wait处理部分完成的任务
5. 始终处理CancelledError
6. 使用async上下文管理器管理资源
7. 限制并发数使用Semaphore
"""

# 在协程中调用阻塞代码
async def call_blocking():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_function)

def blocking_function():
    import time
    time.sleep(1)
    return "result"
```

#### concurrent.futures模块

```python
"""
concurrent.futures提供高级异步执行接口。
核心功能：ThreadPoolExecutor, ProcessPoolExecutor。
"""

from concurrent.futures import (
    ThreadPoolExecutor, ProcessPoolExecutor,
    as_completed, wait, FIRST_COMPLETED, ALL_COMPLETED
)
import time
from typing import List

# ========== ThreadPoolExecutor ==========
def fetch_url(url: str) -> str:
    time.sleep(1)  # 模拟IO
    return f"Data from {url}"

urls = ['url1', 'url2', 'url3', 'url4', 'url5']

# 基本使用
with ThreadPoolExecutor(max_workers=3) as executor:
    # submit - 提交单个任务
    future = executor.submit(fetch_url, 'url1')
    result = future.result()
    print(result)

    # map - 批量提交，保持顺序
    results = list(executor.map(fetch_url, urls))
    print(results)

# ========== ProcessPoolExecutor ==========
def cpu_intensive(n: int) -> int:
    """CPU密集型任务"""
    return sum(i * i for i in range(n))

numbers = [1_000_000, 2_000_000, 3_000_000]

with ProcessPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(cpu_intensive, numbers))
    print(results)

# ========== Future对象 ==========
with ThreadPoolExecutor() as executor:
    future = executor.submit(fetch_url, 'url')

    # 检查状态
    print(future.done())    # False
    print(future.running()) # True

    # 获取结果（阻塞）
    result = future.result()

    # 获取异常
    # exception = future.exception()

    # 添加回调
    def callback(fut):
        print(f"Callback: {fut.result()}")

    future.add_done_callback(callback)

# ========== as_completed ==========
with ThreadPoolExecutor() as executor:
    # 提交所有任务
    futures = {executor.submit(fetch_url, url): url for url in urls}

    # 按完成顺序处理
    for future in as_completed(futures):
        url = futures[future]
        try:
            result = future.result()
            print(f"{url}: {result}")
        except Exception as e:
            print(f"{url}: {e}")

# ========== wait ==========
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(fetch_url, url) for url in urls]

    # 等待所有完成
    done, not_done = wait(futures, return_when=ALL_COMPLETED)

    # 等待第一个完成
    done, not_done = wait(futures, return_when=FIRST_COMPLETED)

    # 带超时等待
    done, not_done = wait(futures, timeout=5)

# ========== 取消任务 ==========
with ThreadPoolExecutor() as executor:
    future = executor.submit(time.sleep, 10)

    # 尝试取消
    cancelled = future.cancel()  # 只有在未开始执行时才能取消
    print(f"Cancelled: {cancelled}")

# ========== 实际应用：并行处理 ==========
def process_item(item: dict) -> dict:
    """处理单个项目"""
    time.sleep(0.1)
    item['processed'] = True
    return item

def parallel_process(items: List[dict], max_workers: int = 4) -> List[dict]:
    """并行处理列表"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_item, items))
    return results

# 带进度报告
def parallel_process_with_progress(items: List[dict], max_workers: int = 4) -> List[dict]:
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_item, item): item for item in items}

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(f"进度: {i}/{len(items)}")

    return results

# ========== 最佳实践 ==========
"""
1. IO密集型用ThreadPoolExecutor
2. CPU密集型用ProcessPoolExecutor
3. 使用上下文管理器确保资源释放
4. 大量任务用as_completed处理结果
5. 设置合理的max_workers（通常CPU核心数）
6. 注意ProcessPoolExecutor的序列化开销
"""
```

#### queue模块

```python
"""
queue提供线程安全的FIFO队列实现。
核心类型：Queue, LifoQueue, PriorityQueue。
"""

import queue
import threading
import time

# ========== FIFO队列 ==========
q = queue.Queue(maxsize=10)  # 限制大小

# 放入元素
q.put('item1')      # 阻塞直到有空位
q.put('item2', block=False)  # 非阻塞，满时抛Full
q.put('item3', timeout=1)    # 带超时

# 获取元素
item = q.get()              # 阻塞直到有元素
item = q.get(block=False)   # 非阻塞，空时抛Empty
item = q.get(timeout=1)     # 带超时

# 标记任务完成
q.task_done()

# 等待所有任务完成
q.join()

# 检查状态
print(q.empty())   # True/False
print(q.full())    # True/False
print(q.qsize())   # 当前大小（近似值）

# ========== LIFO队列（栈） ==========
stack = queue.LifoQueue()
stack.put('a')
stack.put('b')
print(stack.get())  # b（后进先出）

# ========== 优先队列 ==========
pq = queue.PriorityQueue()

# 放入元组 (优先级, 数据)，数字越小优先级越高
pq.put((2, 'medium priority'))
pq.put((1, 'high priority'))
pq.put((3, 'low priority'))

print(pq.get())  # (1, 'high priority')
print(pq.get())  # (2, 'medium priority')

# 使用自定义类
class Task:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Task({self.priority}, {self.description})"

pq = queue.PriorityQueue()
pq.put(Task(2, 'task2'))
pq.put(Task(1, 'task1'))
print(pq.get())  # Task(1, task1)

# ========== 简单队列（无大小限制） ==========
sq = queue.SimpleQueue()  # Python 3.7+
sq.put('item')
print(sq.get())

# ========== 生产者-消费者模式 ==========
def producer(q: queue.Queue, items: list):
    for item in items:
        q.put(item)
        print(f"生产: {item}")
        time.sleep(0.1)
    q.put(None)  # 结束信号

def consumer(q: queue.Queue):
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        print(f"消费: {item}")
        q.task_done()

# 使用
q = queue.Queue()
items = list(range(10))

p = threading.Thread(target=producer, args=(q, items))
c = threading.Thread(target=consumer, args=(q,))

p.start()
c.start()
p.join()
q.join()

# ========== 多生产者多消费者 ==========
def multi_producer(q: queue.Queue, name: str, items: list):
    for item in items:
        q.put((name, item))
    q.put((name, None))  # 结束信号

def multi_consumer(q: queue.Queue, num_producers: int):
    finished = 0
    while finished < num_producers:
        name, item = q.get()
        if item is None:
            finished += 1
        else:
            print(f"消费者处理 {name}: {item}")
        q.task_done()

# ========== 最佳实践 ==========
"""
1. 线程通信用Queue，避免手动锁
2. 使用task_done和join跟踪任务
3. 优先队列用于任务调度
4. 设置合理的队列大小防止内存溢出
5. 使用None或其他信号值表示结束
6. 处理Empty和Full异常
"""
```

---

### 3.5 网络与IO模块

#### socket模块

```python
"""
socket提供底层网络接口。
核心功能：TCP/UDP通信、网络编程基础。
"""

import socket
import threading

# ========== TCP客户端 ==========
def tcp_client():
    # 创建socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接服务器
        client.connect(('localhost', 8080))

        # 发送数据
        client.sendall(b'Hello, Server!')

        # 接收数据
        data = client.recv(1024)
        print(f"收到: {data.decode()}")
    finally:
        client.close()

# ========== TCP服务器 ==========
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind(('0.0.0.0', 8080))
        server.listen(5)
        print("服务器启动，等待连接...")

        while True:
            client, addr = server.accept()
            print(f"连接来自: {addr}")

            # 处理客户端（多线程）
            threading.Thread(target=handle_client, args=(client,)).start()
    finally:
        server.close()

def handle_client(client: socket.socket):
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            print(f"收到: {data.decode()}")
            client.sendall(b'Echo: ' + data)
    finally:
        client.close()

# ========== UDP ==========
def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 8080))

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"来自 {addr}: {data.decode()}")
        sock.sendto(b'ACK', addr)

def udp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'Hello', ('localhost', 8080))
    data, addr = sock.recvfrom(1024)
    print(f"收到: {data.decode()}")

# ========== 非阻塞socket ==========
def non_blocking_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setblocking(False)  # 非阻塞模式

    try:
        client.connect(('localhost', 8080))
    except BlockingIOError:
        pass  # 连接中

    # 使用select检查可读/可写
    import select
    ready = select.select([], [client], [], 5)
    if ready[1]:
        print("连接成功")

# ========== 获取地址信息 ==========
# 获取主机名
print(socket.gethostname())

# 获取IP地址
print(socket.gethostbyname('localhost'))
print(socket.gethostbyname_ex('localhost'))

# 获取地址信息
addr_info = socket.getaddrinfo('www.example.com', 80)
for info in addr_info:
    print(info)

# ========== 最佳实践 ==========
"""
1. 始终使用try-finally确保socket关闭
2. 服务器使用SO_REUSEADDR避免端口占用
3. 多客户端用多线程或多进程处理
4. 大量连接考虑select/poll/epoll
5. 生产环境使用高级框架（asyncio, Twisted）
"""
```

#### urllib模块

```python
"""
urllib提供URL处理功能。
注意：推荐使用requests库进行HTTP请求。
"""

import urllib.request
import urllib.parse
import urllib.error

# ========== 简单请求 ==========
# GET请求
response = urllib.request.urlopen('https://www.example.com')
print(response.status)      # 200
print(response.getheaders()) # 响应头列表
print(response.read().decode())  # 响应体

# ========== 带参数的GET ==========
params = urllib.parse.urlencode({'key': 'value', 'foo': 'bar'})
url = f'https://httpbin.org/get?{params}'
response = urllib.request.urlopen(url)

# ========== POST请求 ==========
data = urllib.parse.urlencode({'key': 'value'}).encode()
response = urllib.request.urlopen(
    'https://httpbin.org/post',
    data=data
)

# ========== 自定义请求 ==========
req = urllib.request.Request(
    'https://api.example.com/data',
    data=b'{"key": "value"}',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token'
    },
    method='POST'
)
response = urllib.request.urlopen(req)

# ========== URL解析 ==========
url = 'https://user:pass@example.com:8080/path?query=1#fragment'
parsed = urllib.parse.urlparse(url)
print(parsed.scheme)    # https
print(parsed.netloc)    # user:pass@example.com:8080
print(parsed.path)      # /path
print(parsed.query)     # query=1
print(parsed.fragment)  # fragment

# 解析查询字符串
query = 'key1=value1&key2=value2&key1=value3'
params = urllib.parse.parse_qs(query)
print(params)  # {'key1': ['value1', 'value3'], 'key2': ['value2']}

# 构建URL
parts = urllib.parse.ParseResult(
    scheme='https',
    netloc='example.com',
    path='/path',
    params='',
    query='key=value',
    fragment=''
)
print(urllib.parse.urlunparse(parts))

# URL编码/解码
encoded = urllib.parse.quote('hello world!')  # hello%20world%21
decoded = urllib.parse.unquote(encoded)       # hello world!

# ========== 错误处理 ==========
try:
    response = urllib.request.urlopen('https://example.com/notfound')
except urllib.error.HTTPError as e:
    print(f"HTTP错误: {e.code}")
except urllib.error.URLError as e:
    print(f"URL错误: {e.reason}")

# ========== 最佳实践 ==========
"""
1. 简单请求用urllib.request
2. 复杂HTTP操作用requests库
3. 始终处理HTTPError和URLError
4. 使用Request对象自定义请求
5. URL操作使用urllib.parse
"""
```

#### http模块

```python
"""
http模块提供HTTP协议相关功能。
核心功能：HTTP状态码、HTTP服务器、Cookie处理。
"""

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie

# ========== HTTP状态码 ==========
print(HTTPStatus.OK)                    # HTTPStatus.OK
print(HTTPStatus.OK.value)              # 200
print(HTTPStatus.OK.phrase)             # OK
print(HTTPStatus.OK.description)        # Request fulfilled, document follows

# 常用状态码
# 200 OK
# 201 Created
# 400 Bad Request
# 401 Unauthorized
# 403 Forbidden
# 404 Not Found
# 500 Internal Server Error

# 检查状态码类别
print(HTTPStatus.OK.is_success)         # True (2xx)
print(HTTPStatus.NOT_FOUND.is_error)    # True (4xx or 5xx)

# ========== 简单HTTP服务器 ==========
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Hello, World!</h1>')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        self.send_response(HTTPStatus.CREATED)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "created"}')

    def log_message(self, format, *args):
        # 自定义日志
        print(f"[{self.date_time_string()}] {args[0]}")

def run_server():
    server = HTTPServer(('localhost', 8080), SimpleHandler)
    print("服务器启动在 http://localhost:8080")
    server.serve_forever()

# ========== Cookie处理 ==========
# 创建Cookie
cookie = SimpleCookie()
cookie['session'] = 'abc123'
cookie['session']['expires'] = 3600  # 1小时

# 输出HTTP头
print(cookie.output())  # Set-Cookie: session=abc123; expires=...

# 解析Cookie
cookie_str = 'session=abc123; user=john'
cookie.load(cookie_str)
print(cookie['session'].value)  # abc123

# ========== 最佳实践 ==========
"""
1. 使用HTTPStatus提高代码可读性
2. 简单测试用http.server
3. 生产环境使用专业框架（Flask, FastAPI）
4. Cookie处理注意安全性
"""
```

#### json模块

```python
"""
json模块提供JSON数据的编码和解码。
核心功能：序列化、反序列化、自定义编码器。
"""

import json
from datetime import datetime
from decimal import Decimal

# ========== 基本操作 ==========
data = {
    'name': 'Alice',
    'age': 30,
    'is_student': False,
    'courses': ['Math', 'Science'],
    'address': None
}

# 编码（Python -> JSON）
json_str = json.dumps(data)
print(json_str)

# 美化输出
pretty = json.dumps(data, indent=2, ensure_ascii=False)
print(pretty)

# 排序键
sorted_json = json.dumps(data, sort_keys=True)

# 解码（JSON -> Python）
parsed = json.loads(json_str)
print(parsed['name'])

# 文件操作
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('data.json', 'r') as f:
    loaded = json.load(f)

# ========== 自定义编码 ==========
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            '_type': 'User'
        }

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.to_dict()
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

user = User('Alice', 30)
json_str = json.dumps(user, cls=CustomEncoder)
print(json_str)

# 或使用default参数
json_str = json.dumps(
    {'user': user, 'time': datetime.now()},
    default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else str(o)
)

# ========== 自定义解码 ==========
def custom_decoder(dct):
    if '_type' in dct and dct['_type'] == 'User':
        return User(dct['name'], dct['age'])
    return dct

parsed = json.loads(json_str, object_hook=custom_decoder)

# ========== 流式处理 ==========
# 处理大型JSON
from json import JSONDecoder

def extract_objects(json_str):
    decoder = JSONDecoder()
    idx = 0
    while idx < len(json_str):
        try:
            obj, end = decoder.raw_decode(json_str, idx)
            yield obj
            idx += end
        except json.JSONDecodeError:
            break

# ========== 最佳实践 ==========
"""
1. 始终使用ensure_ascii=False处理中文
2. 复杂对象使用自定义Encoder
3. 浮点数精度问题用Decimal
4. 日期时间转为ISO格式
5. 大型JSON考虑流式处理
6. 不信任的输入用try-except
"""

# 安全加载（避免执行恶意代码）
def safe_loads(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
```


#### csv模块

```python
"""
csv模块提供CSV文件的读写功能。
核心功能：读写CSV、处理不同格式、方言支持。
"""

import csv
from io import StringIO

# ========== 读取CSV ==========
# 基本读取
with open('data.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # 每行是列表

# 读取为字典
with open('data.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'])  # 通过列名访问

# ========== 写入CSV ==========
# 基本写入
with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'age', 'city'])
    writer.writerow(['Alice', 30, 'NYC'])
    writer.writerows([
        ['Bob', 25, 'LA'],
        ['Charlie', 35, 'SF']
    ])

# 从字典写入
with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['name', 'age', 'city']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'name': 'Alice', 'age': 30, 'city': 'NYC'})

# ========== 方言（处理不同格式） ==========
# 注册自定义方言
csv.register_dialect('excel-semicolon', delimiter=';', lineterminator='\n')

# 使用方言
with open('european.csv', 'r', newline='') as f:
    reader = csv.reader(f, dialect='excel-semicolon')
    for row in reader:
        print(row)

# 方言参数
# delimiter: 分隔符（默认,）
# quotechar: 引号字符（默认"）
# escapechar: 转义字符
# doublequote: 双引号处理
# skipinitialspace: 跳过分隔符后空格
# lineterminator: 行结束符
# quoting: 引用规则

# ========== 引用规则 ==========
# csv.QUOTE_ALL - 所有字段加引号
# csv.QUOTE_MINIMAL - 需要时加引号（默认）
# csv.QUOTE_NONNUMERIC - 非数字加引号
# csv.QUOTE_NONE - 不加引号

with open('quoted.csv', 'w', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(['hello', 'world'])
# 输出: "hello","world"

# ========== 处理特殊字符 ==========
data = [['value with, comma', 'value with "quotes"', 'normal']]

with open('special.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)

# 内存中处理
csv_file = StringIO()
writer = csv.writer(csv_file)
writer.writerow(['a', 'b', 'c'])
csv_content = csv_file.getvalue()
print(csv_content)

# ========== 最佳实践 ==========
"""
1. 始终使用newline=''打开CSV文件
2. 明确指定encoding（推荐utf-8）
3. 使用DictReader/DictWriter处理表头
4. 处理欧洲CSV注意分隔符可能是分号
5. 特殊字符使用适当引用规则
6. 大文件使用迭代器逐行处理
"""

# 安全的CSV读取（防止注入）
def safe_csv_read(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # 清理每行数据
            cleaned = [cell.strip() for cell in row]
            yield cleaned
```

#### xml模块

```python
"""
xml模块提供XML处理功能。
核心功能：ElementTree解析、DOM操作、SAX流式处理。
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import xml.sax

# ========== ElementTree解析 ==========
xml_data = '''<?xml version="1.0"?>
<library>
    <book id="1">
        <title>Python Guide</title>
        <author>John Doe</author>
        <price>29.99</price>
    </book>
    <book id="2">
        <title>Learning XML</title>
        <author>Jane Smith</author>
        <price>39.99</price>
    </book>
</library>
'''

# 从字符串解析
root = ET.fromstring(xml_data)

# 从文件解析
tree = ET.parse('library.xml')
root = tree.getroot()

# ========== 遍历XML ==========
# 遍历所有book
for book in root.findall('book'):
    book_id = book.get('id')
    title = book.find('title').text
    author = book.find('author').text
    price = float(book.find('price').text)
    print(f"{book_id}: {title} by {author} (${price})")

# XPath查询
book = root.find('.//book[@id="1"]')
all_titles = root.findall('.//title')

# ========== 创建XML ==========
# 创建根元素
root = ET.Element('library')

# 添加子元素
book = ET.SubElement(root, 'book', {'id': '3'})
title = ET.SubElement(book, 'title')
title.text = 'New Book'
author = ET.SubElement(book, 'author')
author.text = 'New Author'
price = ET.SubElement(book, 'price')
price.text = '19.99'

# 美化输出
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

print(prettify(root))

# 写入文件
tree = ET.ElementTree(root)
tree.write('output.xml', encoding='utf-8', xml_declaration=True)

# ========== 修改XML ==========
# 修改文本
book.find('price').text = '24.99'

# 修改属性
book.set('id', '4')

# 删除元素
root.remove(book)

# ========== SAX解析（流式，内存友好） ==========
class BookHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current = ''
        self.title = ''
        self.author = ''

    def startElement(self, name, attrs):
        self.current = name
        if name == 'book':
            print(f"Book ID: {attrs.get('id')}")

    def characters(self, content):
        if self.current == 'title':
            self.title = content
        elif self.current == 'author':
            self.author = content

    def endElement(self, name):
        if name == 'title':
            print(f"Title: {self.title}")
        elif name == 'author':
            print(f"Author: {self.author}")
        self.current = ''

# 使用SAX解析
parser = xml.sax.make_parser()
parser.setContentHandler(BookHandler())
# parser.parse('library.xml')

# ========== 命名空间处理 ==========
namespaces = {'ns': 'http://example.com/books'}

# 带命名空间的查询
for book in root.findall('ns:book', namespaces):
    pass

# ========== 最佳实践 ==========
"""
1. 小型XML用ElementTree
2. 大型XML用SAX流式处理
3. 注意命名空间处理
4. 始终指定encoding
5. 不信任的XML注意XXE攻击
6. 考虑使用lxml库获得更好性能
"""

# 安全解析（防止XXE）
from xml.etree.ElementTree import XMLParser

class SafeXMLParser(XMLParser):
    def __init__(self):
        super().__init__()
        # 禁用外部实体
        self.parser.UseForeignDTD(False)
```

---

### 3.6 测试与调试模块

#### unittest模块

```python
"""
unittest是Python的标准单元测试框架。
核心功能：测试用例、测试套件、断言、夹具。
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
from typing import List

# ========== 基础测试类 ==========
class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class TestCalculator(unittest.TestCase):
    """Calculator测试类"""

    # ========== 夹具（Fixture） ==========
    @classmethod
    def setUpClass(cls):
        """类级别：所有测试前执行一次"""
        print("setUpClass")
        cls.calculator = Calculator()

    @classmethod
    def tearDownClass(cls):
        """类级别：所有测试后执行一次"""
        print("tearDownClass")

    def setUp(self):
        """方法级别：每个测试前执行"""
        print("setUp")

    def tearDown(self):
        """方法级别：每个测试后执行"""
        print("tearDown")

    # ========== 测试方法 ==========
    def test_add(self):
        """测试加法"""
        result = self.calculator.add(2, 3)
        self.assertEqual(result, 5)

    def test_add_negative(self):
        """测试负数加法"""
        result = self.calculator.add(-2, -3)
        self.assertEqual(result, -5)

    def test_divide(self):
        """测试除法"""
        result = self.calculator.divide(10, 2)
        self.assertEqual(result, 5)

    def test_divide_by_zero(self):
        """测试除零异常"""
        with self.assertRaises(ValueError) as context:
            self.calculator.divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")

    # ========== 常用断言 ==========
    def test_assertions(self):
        # 相等
        self.assertEqual(1 + 1, 2)
        self.assertNotEqual(1 + 1, 3)

        # 真值
        self.assertTrue(1 == 1)
        self.assertFalse(1 == 2)

        # None
        self.assertIsNone(None)
        self.assertIsNotNone('value')

        # 身份
        a = b = [1, 2, 3]
        self.assertIs(a, b)

        # 包含
        self.assertIn(2, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])

        # 比较
        self.assertGreater(5, 3)
        self.assertGreaterEqual(5, 5)
        self.assertLess(3, 5)
        self.assertLessEqual(3, 3)

        # 近似相等（浮点数）
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)

        # 列表
        self.assertListEqual([1, 2, 3], [1, 2, 3])
        self.assertCountEqual([1, 2, 3], [3, 2, 1])  # 忽略顺序

        # 字典
        self.assertDictEqual({'a': 1}, {'a': 1})

        # 正则
        self.assertRegex('hello world', r'hello')
        self.assertNotRegex('hello world', r'foo')

        # 异常
        with self.assertRaises(TypeError):
            len(42)

        # 警告
        import warnings
        with self.assertWarns(UserWarning):
            warnings.warn('warning', UserWarning)

# ========== Mock测试 ==========
class TestWithMock(unittest.TestCase):

    def test_mock_object(self):
        """测试Mock对象"""
        mock = Mock()
        mock.return_value = 42

        result = mock()
        self.assertEqual(result, 42)
        mock.assert_called_once()

    def test_mock_method(self):
        """测试Mock方法"""
        mock = Mock()
        mock.some_method.return_value = 'result'

        result = mock.some_method('arg1', key='value')
        self.assertEqual(result, 'result')
        mock.some_method.assert_called_once_with('arg1', key='value')

    @patch('builtins.open')
    def test_patch_builtin(self, mock_open):
        """测试patch内置函数"""
        mock_open.return_value.__enter__.return_value.read.return_value = 'content'

        with open('file.txt') as f:
            content = f.read()

        self.assertEqual(content, 'content')

    @patch('requests.get')
    def test_patch_external(self, mock_get):
        """测试patch外部库"""
        mock_response = Mock()
        mock_response.json.return_value = {'key': 'value'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        import requests
        response = requests.get('https://api.example.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'key': 'value'})

    def test_mock_side_effect(self):
        """测试side_effect"""
        mock = Mock()
        mock.side_effect = [1, 2, 3]  # 依次返回值

        self.assertEqual(mock(), 1)
        self.assertEqual(mock(), 2)
        self.assertEqual(mock(), 3)

    def test_mock_side_effect_exception(self):
        """测试side_effect抛出异常"""
        mock = Mock()
        mock.side_effect = ValueError('error')

        with self.assertRaises(ValueError):
            mock()

# ========== 参数化测试 ==========
class TestParameterized(unittest.TestCase):

    def test_add_multiple(self):
        """多组参数测试"""
        test_cases = [
            (2, 3, 5),
            (-1, 1, 0),
            (0, 0, 0),
            (-2, -3, -5),
        ]
        calc = Calculator()

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result = calc.add(a, b)
                self.assertEqual(result, expected)

# ========== 跳过和预期失败 ==========
class TestSkipAndExpectedFailure(unittest.TestCase):

    @unittest.skip("暂时跳过")
    def test_skipped(self):
        pass

    @unittest.skipIf(True, "条件为真时跳过")
    def test_skipped_if(self):
        pass

    @unittest.skipUnless(False, "条件为假时跳过")
    def test_skipped_unless(self):
        pass

    @unittest.expectedFailure
    def test_expected_failure(self):
        """预期失败的测试"""
        self.assertEqual(1, 2)

# ========== 运行测试 ==========
if __name__ == '__main__':
    # 运行所有测试
    unittest.main()

    # 或者
    # python -m unittest test_module
    # python -m unittest test_module.TestClass
    # python -m unittest test_module.TestClass.test_method

    # 发现测试
    # python -m unittest discover -s tests -p "test_*.py"

# ========== 测试套件 ==========
def suite():
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTests(loader.loadTestsFromTestCase(TestCalculator))
    test_suite.addTests(loader.loadTestsFromTestCase(TestWithMock))
    return test_suite

# 运行套件
# runner = unittest.TextTestRunner(verbosity=2)
# runner.run(suite())

# ========== 最佳实践 ==========
"""
1. 测试方法名以test_开头
2. 每个测试只测试一个概念
3. 使用setUp/tearDown管理资源
4. 外部依赖用Mock替代
5. 使用subTest进行参数化测试
6. 保持测试独立，不依赖执行顺序
7. 测试覆盖率目标80%以上
"""
```

#### pytest（第三方但重要）

```python
"""
pytest是Python最流行的测试框架。
核心优势：简洁语法、强大fixture、丰富插件。
安装: pip install pytest
"""

# ========== 基础测试 ==========
# 测试函数（无需类）
def add(x, y):
    return x + y

def test_add():
    """测试加法"""
    assert add(2, 3) == 5

def test_add_negative():
    """测试负数"""
    assert add(-2, -3) == -5

# ========== Fixture ==========
import pytest

@pytest.fixture
def sample_data():
    """提供测试数据"""
    return {'name': 'test', 'value': 42}

def test_with_fixture(sample_data):
    """使用fixture"""
    assert sample_data['value'] == 42

# 作用域
@pytest.fixture(scope='function')   # 每个测试函数（默认）
def func_fixture():
    pass

@pytest.fixture(scope='class')      # 每个测试类
def class_fixture():
    pass

@pytest.fixture(scope='module')     # 每个模块
def module_fixture():
    pass

@pytest.fixture(scope='session')    # 整个测试会话
def session_fixture():
    pass

# Fixture依赖
@pytest.fixture
def db():
    """数据库连接"""
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture
def user(db):
    """依赖db fixture"""
    return db.create_user('test')

# ========== 参数化测试 ==========
@pytest.mark.parametrize("x,y,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add_parametrized(x, y, expected):
    assert add(x, y) == expected

# 多参数
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [4, 5])
def test_combinations(x, y):
    """生成6组测试 (1,4), (1,5), (2,4), (2,5), (3,4), (3,5)"""
    pass

# ========== Mock（使用pytest-mock） ==========
# pip install pytest-mock

def test_with_mock(mocker):
    """使用mocker fixture"""
    # Mock函数
    mock = mocker.patch('module.function')
    mock.return_value = 42

    result = module.function()
    assert result == 42
    mock.assert_called_once()

# ========== 标记和跳过 ==========
@pytest.mark.skip(reason="暂时跳过")
def test_skipped():
    pass

@pytest.mark.skipif(True, reason="条件为真跳过")
def test_skipped_if():
    pass

@pytest.mark.xfail(reason="预期失败")
def test_expected_failure():
    assert 1 == 2

@pytest.mark.slow  # 自定义标记
def test_slow():
    pass

# 运行特定标记: pytest -m slow

# ========== 异常测试 ==========
def test_raises():
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("error message")

    assert str(exc_info.value) == "error message"

# ========== 近似比较 ==========
def test_approx():
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert [0.1, 0.2] == pytest.approx([0.1, 0.2])

# ========== 类和模块 ==========
class TestCalculator:
    """测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """自动使用的fixture"""
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5

# ========== 常用命令 ==========
"""
pytest                          # 运行所有测试
pytest test_module.py           # 运行特定模块
pytest test_module.py::test_func # 运行特定函数
pytest test_module.py::TestClass # 运行特定类
pytest -v                       # 详细输出
pytest -s                       # 显示print输出
pytest -x                       # 第一次失败停止
pytest --maxfail=3              # 3次失败停止
pytest -k "test_add"            # 匹配名称
pytest -m slow                  # 运行标记的测试
pytest --cov=module             # 覆盖率（需pytest-cov）
pytest --cov-report=html        # HTML覆盖率报告
"""

# ========== 最佳实践 ==========
"""
1. 测试函数以test_开头
2. 使用assert而非self.assertEqual
3. 用fixture管理测试依赖
4. 参数化测试减少重复
5. 使用conftest.py共享fixture
6. 保持测试快速和独立
7. 使用pytest-xdist并行测试
"""
```

#### logging模块

```python
"""
logging提供灵活的日志记录功能。
核心组件：Logger, Handler, Formatter, Filter。
"""

import logging
import logging.handlers
import sys
from pathlib import Path

# ========== 基础使用 ==========
# 简单配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.debug('调试信息')
logger.info('普通信息')
logger.warning('警告')
logger.error('错误')
logger.critical('严重错误')

# ========== 日志级别 ==========
# DEBUG (10) - 详细信息，诊断问题
# INFO (20) - 确认程序按预期运行
# WARNING (30) - 意外情况，但程序继续运行
# ERROR (40) - 严重问题，某些功能无法工作
# CRITICAL (50) - 严重错误，程序可能无法继续

# ========== 完整配置 ==========
def setup_logging():
    """配置日志系统"""

    # 创建logger
    logger = logging.getLogger('myapp')
    logger.setLevel(logging.DEBUG)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)

    # 文件处理器
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_format)

    # 错误文件处理器
    error_handler = logging.FileHandler(log_dir / 'error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    return logger

# ========== 常用处理器 ==========
"""
StreamHandler - 输出到流（如sys.stdout）
FileHandler - 输出到文件
RotatingFileHandler - 自动轮转文件
TimedRotatingFileHandler - 按时间轮转
SocketHandler - 发送到网络socket
SMTPHandler - 发送邮件
SysLogHandler - 发送到syslog
HTTPHandler - 发送到HTTP服务器
"""

# ========== 格式化字符串 ==========
"""
%(asctime)s - 时间
%(name)s - logger名称
%(levelname)s - 日志级别
%(message)s - 日志消息
%(filename)s - 文件名
%(lineno)d - 行号
%(funcName)s - 函数名
%(module)s - 模块名
%(process)d - 进程ID
%(thread)d - 线程ID
"""

# ========== 日志配置字典 ==========
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
    },
    'loggers': {
        'myapp': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    },
}

# 应用配置
# logging.config.dictConfig(LOGGING_CONFIG)

# ========== 日志过滤 ==========
class LevelFilter(logging.Filter):
    """只允许特定级别的日志"""

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

# 使用
handler = logging.StreamHandler()
handler.addFilter(LevelFilter(logging.ERROR))

# ========== 上下文信息 ==========
# 使用extra添加额外信息
logger.info('用户登录', extra={'user_id': 123, 'ip': '192.168.1.1'})

# 使用LoggerAdapter
class ContextAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[{self.extra['request_id']}] {msg}", kwargs

adapter = ContextAdapter(logger, {'request_id': 'abc123'})
adapter.info('处理请求')

# ========== 异常信息 ==========
try:
    1 / 0
except ZeroDivisionError:
    logger.exception('发生除零错误')  # 自动包含堆栈
    # 或
    logger.error('错误', exc_info=True)

# ========== 最佳实践 ==========
"""
1. 使用__name__作为logger名称
2. 不要频繁创建logger实例
3. 使用RotatingFileHandler避免日志过大
4. 生产环境日志级别设为INFO或WARNING
5. 敏感信息不要记录到日志
6. 使用结构化日志（JSON格式）便于分析
7. 异常使用logger.exception记录堆栈
"""
```

#### pdb模块

```python
"""
pdb是Python的交互式源代码调试器。
核心功能：断点、单步执行、检查变量。
"""

import pdb

# ========== 启动调试器 ==========
# 方式1: 在代码中插入
# pdb.set_trace()  # Python 3.7前
# breakpoint()     # Python 3.7+ 推荐

def buggy_function(x, y):
    result = x + y
    # breakpoint()  # 会在这里暂停
    result = result * 2
    return result

# 方式2: 命令行启动
# python -m pdb script.py

# 方式3: 事后调试
# python -m pdb -c continue script.py

# ========== 常用命令 ==========
"""
命令            简写    说明
help            h       显示帮助
where           w       显示堆栈
next            n       执行下一行（不进入函数）
step            s       执行下一行（进入函数）
continue        c       继续执行直到下一个断点
return          r       执行到当前函数返回
quit            q       退出调试器
break           b       设置断点
clear           cl      清除断点
list            l       显示源代码
print           p       打印表达式
pp              pp      美化打印
args            a       显示当前函数参数
up              u       上移堆栈帧
down            d       下移堆栈帧
until           unt     执行到指定行号
"""

# ========== 断点设置 ==========
# 代码中设置
# pdb.set_trace()

# 条件断点
# 在pdb中: break 10, x > 5

# 使用breakpoint()的高级用法
# PYTHONBREAKPOINT=0 禁用所有断点
# PYTHONBREAKPOINT=pdb.set_trace 使用pdb
# PYTHONBREAKPOINT=ipdb.set_trace 使用ipdb

# ========== 程序示例 ==========
def calculate(a, b, operation):
    if operation == 'add':
        result = a + b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        result = a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

    # 可以在这里设置断点检查result
    # breakpoint()

    return result

# ========== 事后调试 ==========
import sys

def post_mortem_debug(exc_type, exc_value, traceback):
    """异常发生后进入调试器"""
    import pdb
    pdb.post_mortem(traceback)

# 设置为异常钩子
# sys.excepthook = post_mortem_debug

# ========== 远程调试 ==========
# 使用rpdb或远程pdb
# import rpdb; rpdb.set_trace("0.0.0.0", 4444)

# ========== 最佳实践 ==========
"""
1. 使用breakpoint()而非pdb.set_trace()
2. 学习常用命令提高效率
3. 使用w命令查看调用堆栈
4. 使用pp命令查看复杂数据结构
5. 条件断点减少不必要的中断
6. 生产环境禁用断点（PYTHONBREAKPOINT=0）
7. 复杂场景考虑使用IDE调试器
"""
```

---

### 3.7 其他重要模块

#### re模块（正则表达式）

```python
"""
re模块提供正则表达式匹配操作。
核心功能：模式匹配、搜索、替换、分割。
"""

import re

# ========== 基础匹配 ==========
# search - 搜索第一个匹配
match = re.search(r'\d+', 'abc123def')
print(match.group())  # 123

# match - 从字符串开头匹配
match = re.match(r'\d+', '123abc')
print(match.group())  # 123

# fullmatch - 整个字符串匹配
match = re.fullmatch(r'\d+', '123')
print(match.group())  # 123

# findall - 查找所有匹配
matches = re.findall(r'\d+', 'abc123def456')
print(matches)  # ['123', '456']

# finditer - 返回迭代器
for match in re.finditer(r'\d+', 'abc123def456'):
    print(f"Found {match.group()} at {match.start()}-{match.end()}")

# ========== 编译正则 ==========
# 频繁使用的正则应该编译
pattern = re.compile(r'\d+')
matches = pattern.findall('abc123def456')

# 编译选项
pattern = re.compile(
    r'hello world',
    re.IGNORECASE | re.MULTILINE  # 忽略大小写，多行模式
)

# ========== 分组和捕获 ==========
# 基本分组
text = 'John Doe, 30'
pattern = re.compile(r'(\w+) (\w+), (\d+)')
match = pattern.match(text)
print(match.group(0))  # John Doe, 30（整个匹配）
print(match.group(1))  # John
print(match.group(2))  # Doe
print(match.group(3))  # 30
print(match.groups())  # ('John', 'Doe', '30')

# 命名分组
text = '2023-12-25'
pattern = re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})')
match = pattern.match(text)
print(match.group('year'))   # 2023
print(match.groupdict())     # {'year': '2023', 'month': '12', 'day': '25'}

# 非捕获分组
pattern = re.compile(r'(?:abc)+')  # (?:...) 不捕获

# 前瞻后顾
# 正向前瞻 (?=...)
re.findall(r'\w+(?=\.)', 'hello.txt world.py')  # ['hello', 'world']

# 负向前瞻 (?!...)
re.findall(r'\b\w+(?!\.)\b', 'hello.txt world')  # ['world']

# 正向后顾 (?<=...)
re.findall(r'(?<=\$)\d+', 'Price: $100')  # ['100']

# 负向后顾 (?<!...)
re.findall(r'\b\w+\b(?<!\.)', 'hello. world')  # ['world']

# ========== 替换 ==========
# sub - 替换
text = 'Hello 123 World 456'
result = re.sub(r'\d+', 'XXX', text)
print(result)  # Hello XXX World XXX

# 使用函数替换
def double(match):
    return str(int(match.group()) * 2)

result = re.sub(r'\d+', double, '1 2 3')
print(result)  # 2 4 6

# subn - 替换并返回次数
result, count = re.subn(r'\d+', 'X', 'a1b2c3')
print(result, count)  # aXbXcX 3

# ========== 分割 ==========
# split - 正则分割
text = 'apple, banana; orange|grape'
parts = re.split(r'[,;|]\s*', text)
print(parts)  # ['apple', 'banana', 'orange', 'grape']

# ========== 常用模式 ==========
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

PHONE_PATTERN = re.compile(
    r'^(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'
)

URL_PATTERN = re.compile(
    r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(/[^\s]*)?$'
)

IPV4_PATTERN = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
    r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
)

# ========== 最佳实践 ==========
"""
1. 频繁使用的正则编译后使用
2. 使用原始字符串r'...'定义模式
3. 复杂模式使用re.VERBOSE添加注释
4. 使用命名分组提高可读性
5. 注意贪婪vs非贪婪匹配
6. 优先使用字符串方法（简单场景）
"""

# 使用VERBOSE添加注释
pattern = re.compile(r'''
    ^                   # 字符串开头
    (?P<username>\w+)   # 用户名
    @                   # @符号
    (?P<domain>\w+)     # 域名
    \.                  # 点
    (?P<tld>\w{2,})     # 顶级域名
    $                   # 字符串结尾
''', re.VERBOSE)
```

#### datetime模块

```python
"""
datetime提供日期和时间处理功能。
核心类型：date, time, datetime, timedelta, tzinfo。
"""

from datetime import datetime, date, time, timedelta, timezone
from dateutil import tz  # 需要: pip install python-dateutil
import time as time_module

# ========== 创建日期时间 ==========
# 当前日期时间
now = datetime.now()
today = date.today()

# 指定值创建
dt = datetime(2023, 12, 25, 10, 30, 0)
d = date(2023, 12, 25)
t = time(10, 30, 0)

# 从字符串解析
dt = datetime.fromisoformat('2023-12-25T10:30:00')
dt = datetime.strptime('25/12/2023 10:30', '%d/%m/%Y %H:%M')

# 从时间戳
dt = datetime.fromtimestamp(1703502600)
ts = datetime.now().timestamp()

# ========== 格式化输出 ==========
dt = datetime(2023, 12, 25, 10, 30, 0)
print(dt.isoformat())           # 2023-12-25T10:30:00
print(dt.strftime('%Y-%m-%d'))  # 2023-12-25
print(dt.strftime('%d/%m/%Y %H:%M'))  # 25/12/2023 10:30

# 常用格式码
"""
%Y - 四位年份 (2023)
%y - 两位年份 (23)
%m - 月份 (01-12)
%d - 日期 (01-31)
%H - 小时 (00-23)
%M - 分钟 (00-59)
%S - 秒 (00-59)
%f - 微秒 (000000-999999)
%A - 星期几 (Monday)
%a - 星期几缩写 (Mon)
%B - 月份名称 (December)
%b - 月份缩写 (Dec)
%p - AM/PM
%z - 时区偏移 (+0000)
%Z - 时区名称 (UTC)
"""

# ========== 时间计算 ==========
dt = datetime(2023, 12, 25, 10, 0)

# 加减时间
tomorrow = dt + timedelta(days=1)
last_week = dt - timedelta(weeks=1)
future = dt + timedelta(days=2, hours=3)

# 时间差
diff = datetime(2023, 12, 25) - datetime(2023, 12, 20)
print(diff.days)  # 5

# ========== 时区处理 ==========
# Python 3.9+ 推荐方式
from zoneinfo import ZoneInfo

# 创建带时区的datetime
utc = datetime.now(timezone.utc)
nyc = datetime.now(ZoneInfo('America/New_York'))
tokyo = datetime.now(ZoneInfo('Asia/Tokyo'))

# 时区转换
utc_time = datetime.now(timezone.utc)
nyc_time = utc_time.astimezone(ZoneInfo('America/New_York'))

# 无时区转有时区（假设为本地时间）
naive = datetime(2023, 12, 25, 10, 0)
aware = naive.replace(tzinfo=ZoneInfo('Asia/Shanghai'))

# ========== 日期时间属性 ==========
dt = datetime(2023, 12, 25, 10, 30, 45, 123456)
print(dt.year)        # 2023
print(dt.month)       # 12
print(dt.day)         # 25
print(dt.hour)        # 10
print(dt.minute)      # 30
print(dt.second)      # 45
print(dt.microsecond) # 123456
print(dt.weekday())   # 0=Monday, 6=Sunday
print(dt.isoweekday())  # 1=Monday, 7=Sunday
print(dt.isocalendar())  # (year, week, weekday)

# ========== 实用函数 ==========
def days_until(target_date: date) -> int:
    """计算距离目标日期还有多少天"""
    return (target_date - date.today()).days

def is_weekend(d: date) -> bool:
    """检查是否是周末"""
    return d.weekday() >= 5

def get_month_range(year: int, month: int) -> tuple[date, date]:
    """获取某月的起始和结束日期"""
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start, end

# ========== 最佳实践 ==========
"""
1. 始终使用时区感知datetime处理跨时区
2. 存储使用UTC，显示时转换
3. 使用fromisoformat/strptime解析
4. 使用strftime格式化输出
5. 时间计算使用timedelta
6. 考虑使用pendulum或arrow库简化
"""

# 存储最佳实践
# 存储: datetime.now(timezone.utc).isoformat()
# 解析: datetime.fromisoformat(stored_string)
```

#### decimal和fractions模块

```python
"""
decimal提供十进制浮点运算，fractions提供有理数运算。
核心用途：精确计算（货币、科学计算）。
"""

from decimal import Decimal, ROUND_UP, ROUND_DOWN, ROUND_HALF_UP, getcontext
from fractions import Fraction

# ========== Decimal ==========
# 创建Decimal
a = Decimal('0.1')  # 推荐：从字符串创建
b = Decimal(0.1)    # 不推荐：先转float会丢失精度

# 基本运算
print(Decimal('0.1') + Decimal('0.2'))  # 0.3（精确）
print(0.1 + 0.2)  # 0.30000000000000004（不精确）

# 设置精度
getcontext().prec = 6
print(Decimal('1') / Decimal('7'))  # 0.142857

# 舍入模式
getcontext().rounding = ROUND_HALF_UP
print(Decimal('2.5').quantize(Decimal('1')))  # 3

# 货币计算
def calculate_total(price: str, quantity: int, tax_rate: str) -> Decimal:
    """计算含税总价"""
    price_dec = Decimal(price)
    tax_dec = Decimal(tax_rate)

    subtotal = price_dec * quantity
    tax = (subtotal * tax_dec).quantize(Decimal('0.01'))
    total = subtotal + tax

    return total.quantize(Decimal('0.01'))

print(calculate_total('19.99', 3, '0.08'))  # 64.77

# ========== Fraction ==========
# 创建分数
f1 = Fraction(1, 3)    # 1/3
f2 = Fraction('0.5')   # 1/2
f3 = Fraction(0.25)    # 1/4

# 运算
print(f1 + f2)  # 5/6
print(f1 * f2)  # 1/6
print(f1 / f2)  # 2/3

# 属性
print(f1.numerator)    # 1
print(f1.denominator)  # 3

# 转float
print(float(f1))  # 0.3333333333333333

# 限制分母
from math import pi
print(Fraction(pi).limit_denominator(100))  # 22/7

# ========== 最佳实践 ==========
"""
1. 货币计算用Decimal，不要用float
2. Decimal从字符串创建，避免float污染
3. 设置合适的精度和舍入模式
4. 分数运算用Fraction保持精确
5. 最终显示时再转换为float
"""

# 货币计算最佳实践
class Money:
    def __init__(self, amount: str, currency: str = 'USD'):
        self.amount = Decimal(amount).quantize(Decimal('0.01'))
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(str(self.amount + other.amount), self.currency)

    def __repr__(self):
        return f"{self.currency} {self.amount}"

price = Money('19.99')
tax = Money('1.60')
total = price + tax
print(total)  # USD 21.59
```

#### hashlib和secrets模块

```python
"""
hashlib提供安全哈希算法，secrets提供加密安全随机数。
核心用途：密码哈希、数据完整性、安全令牌。
"""

import hashlib
import secrets
import hmac

# ========== 哈希算法 ==========
# MD5（不推荐用于安全场景）
md5 = hashlib.md5(b'hello').hexdigest()

# SHA-256（推荐）
sha256 = hashlib.sha256(b'hello').hexdigest()

# SHA-512
sha512 = hashlib.sha512(b'hello').hexdigest()

# 分块哈希（大文件）
sha256 = hashlib.sha256()
with open('file.txt', 'rb') as f:
    while chunk := f.read(8192):
        sha256.update(chunk)
file_hash = sha256.hexdigest()

# ========== 密码哈希 ==========
# 使用hashlib.pbkdf2_hmac（简单场景）
def hash_password(password: str, salt: bytes = None) -> tuple[str, bytes]:
    """使用PBKDF2哈希密码"""
    if salt is None:
        salt = secrets.token_bytes(16)

    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        iterations=100000  # 迭代次数
    )
    return key.hex(), salt

# 验证密码
def verify_password(password: str, hash_str: str, salt: bytes) -> bool:
    new_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(new_hash, hash_str)

# 生产环境推荐使用bcrypt或argon2
# pip install bcrypt
# import bcrypt
# hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# bcrypt.checkpw(password.encode(), hashed)

# ========== secrets模块 ==========
# 安全随机数（用于密码学）

# 随机整数
secure_int = secrets.randbelow(100)  # 0-99
secure_bits = secrets.randbits(16)   # 16位随机数

# 随机选择
choices = ['a', 'b', 'c']
secure_choice = secrets.choice(choices)

# 安全令牌
token = secrets.token_bytes(16)      # 16字节随机字节
token_hex = secrets.token_hex(16)    # 32字符十六进制
token_urlsafe = secrets.token_urlsafe(16)  # URL安全字符串

# 应用场景
def generate_api_key() -> str:
    """生成API密钥"""
    return secrets.token_urlsafe(32)

def generate_password(length: int = 12) -> str:
    """生成随机密码"""
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_reset_token() -> str:
    """生成密码重置令牌"""
    return secrets.token_urlsafe(32)

# ========== HMAC ==========
# 消息认证码
def generate_signature(message: str, key: bytes) -> str:
    """生成HMAC签名"""
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

def verify_signature(message: str, signature: str, key: bytes) -> bool:
    """验证HMAC签名"""
    expected = generate_signature(message, key)
    return hmac.compare_digest(expected, signature)

# ========== 最佳实践 ==========
"""
1. 密码哈希用bcrypt/argon2，不要用MD5/SHA1
2. 安全随机数用secrets，不要用random
3. 比较密文用hmac.compare_digest防时序攻击
4. API密钥用token_urlsafe生成
5. 迭代次数至少100000
6. 每个密码用独立salt
"""
```

#### argparse模块

```python
"""
argparse提供命令行参数解析功能。
核心功能：位置参数、可选参数、子命令、帮助生成。
"""

import argparse
from pathlib import Path

# ========== 基础解析器 ==========
parser = argparse.ArgumentParser(
    description='示例程序',
    epilog='更多信息访问: https://example.com'
)

# 位置参数
parser.add_argument('input', help='输入文件路径')
parser.add_argument('output', nargs='?', default='output.txt', help='输出文件路径')

# 可选参数
parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
parser.add_argument('-n', '--number', type=int, default=1, help='重复次数')
parser.add_argument('-l', '--level', choices=['debug', 'info', 'warning'], default='info')

# 解析
args = parser.parse_args()
print(args.input)
print(args.verbose)

# ========== 参数类型 ==========
parser = argparse.ArgumentParser()

# 基本类型
parser.add_argument('--count', type=int, help='整数')
parser.add_argument('--ratio', type=float, help='浮点数')
parser.add_argument('--name', type=str, help='字符串')

# 自定义类型
def valid_file(path):
    if not Path(path).exists():
        raise argparse.ArgumentTypeError(f"文件不存在: {path}")
    return path

parser.add_argument('--config', type=valid_file, help='配置文件')

# 列表类型
parser.add_argument('--tags', nargs='+', help='多个标签')
parser.add_argument('--values', nargs='*', default=[], help='零个或多个值')
parser.add_argument('--pair', nargs=2, help='恰好两个值')

# ========== 动作类型 ==========
parser = argparse.ArgumentParser()

# store_true/store_false
parser.add_argument('--debug', action='store_true', help='启用调试')
parser.add_argument('--no-cache', action='store_false', dest='cache', help='禁用缓存')

# append
parser.add_argument('-I', '--include', action='append', help='添加包含路径')

# append_const
parser.add_argument('-a', action='append_const', const='a', dest='letters')
parser.add_argument('-b', action='append_const', const='b', dest='letters')

# count
parser.add_argument('-v', '--verbose', action='count', default=0, help='详细级别')

# version
parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# ========== 互斥参数 ==========
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--quiet', action='store_true', help='安静模式')
group.add_argument('--verbose', action='store_true', help='详细模式')

# ========== 参数组 ==========
parser = argparse.ArgumentParser()

input_group = parser.add_argument_group('输入选项')
input_group.add_argument('--input', required=True, help='输入文件')
input_group.add_argument('--format', choices=['json', 'xml'], default='json')

output_group = parser.add_argument_group('输出选项')
output_group.add_argument('--output', help='输出文件')
output_group.add_argument('--compress', action='store_true')

# ========== 子命令 ==========
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', help='可用命令')

# init子命令
init_parser = subparsers.add_parser('init', help='初始化项目')
init_parser.add_argument('name', help='项目名称')
init_parser.add_argument('--template', default='basic')

# run子命令
run_parser = subparsers.add_parser('run', help='运行项目')
run_parser.add_argument('--port', type=int, default=8080)
run_parser.add_argument('--host', default='localhost')

# 使用
# python script.py init myproject --template advanced
# python script.py run --port 3000

# ========== 完整示例 ==========
def create_parser():
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog='fileprocessor',
        description='处理文件的命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s input.txt output.txt
  %(prog)s input.txt -v --format json
  %(prog)s input.txt --compress --level 9
        '''
    )

    # 位置参数
    parser.add_argument('input', type=Path, help='输入文件')
    parser.add_argument('output', nargs='?', type=Path, default=Path('output.txt'),
                       help='输出文件 (默认: output.txt)')

    # 处理选项
    processing = parser.add_argument_group('处理选项')
    processing.add_argument('-f', '--format', choices=['text', 'json', 'xml'],
                           default='text', help='输出格式')
    processing.add_argument('--encoding', default='utf-8', help='文件编码')

    # 压缩选项
    compression = parser.add_argument_group('压缩选项')
    compression.add_argument('-c', '--compress', action='store_true',
                            help='启用压缩')
    compression.add_argument('-l', '--level', type=int, choices=range(1, 10),
                            default=6, help='压缩级别 (1-9)')

    # 其他选项
    parser.add_argument('-v', '--verbose', action='count', default=0,
                       help='增加详细程度')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='安静模式')
    parser.add_argument('--dry-run', action='store_true',
                       help='模拟运行，不实际执行')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    # 处理参数
    if args.quiet:
        verbose_level = 0
    else:
        verbose_level = args.verbose

    if verbose_level > 0:
        print(f"输入: {args.input}")
        print(f"输出: {args.output}")
        print(f"格式: {args.format}")

# if __name__ == '__main__':
#     main()

# ========== 最佳实践 ==========
"""
1. 使用argparse而非sys.argv
2. 提供清晰的help文本
3. 使用类型转换和验证
4. 合理使用默认值
5. 复杂工具使用子命令
6. 提供--version选项
7. 使用formatter美化帮助
"""
```

#### configparser模块

```python
"""
configparser提供INI格式配置文件解析。
核心功能：读写配置、默认值、插值。
"""

import configparser
from pathlib import Path

# ========== 读取配置 ==========
config = configparser.ConfigParser()
config.read('config.ini')

# 访问配置
host = config['database']['host']
port = config.getint('database', 'port')
enabled = config.getboolean('features', 'debug')

# 检查存在
if 'database' in config:
    pass

if config.has_option('database', 'password'):
    pass

# 获取所有节
print(config.sections())

# 获取节内所有项
for key in config['database']:
    print(f"{key} = {config['database'][key]}")

# ========== 写入配置 ==========
config = configparser.ConfigParser()

config['DEFAULT'] = {
    'debug': 'False',
    'log_level': 'INFO'
}

config['database'] = {
    'host': 'localhost',
    'port': '5432',
    'name': 'mydb',
    'user': 'admin',
    'password': 'secret'
}

config['api'] = {
    'host': '0.0.0.0',
    'port': '8080',
    'workers': '4'
}

# 写入文件
with open('config.ini', 'w') as f:
    config.write(f)

# ========== 配置示例 ==========
"""
; config.ini
[DEFAULT]
debug = False
log_level = INFO

[database]
host = localhost
port = 5432
name = mydb
user = admin
password = secret

[api]
host = 0.0.0.0
port = 8080
workers = 4

[cache]
enabled = True
ttl = 3600
"""

# ========== 高级用法 ==========
# 插值（变量替换）
config = configparser.ConfigParser()
config.read_string('''
[paths]
base = /var/app
logs = %(base)s/logs
data = %(base)s/data
''')

print(config['paths']['logs'])  # /var/app/logs

# 自定义插值
class EnvInterpolation(configparser.BasicInterpolation):
    """从环境变量插值"""
    def before_get(self, parser, section, option, value, defaults):
        import os
        return os.path.expandvars(value)

config = configparser.ConfigParser(interpolation=EnvInterpolation())

# 不区分大小写
config = configparser.ConfigParser()
config.optionxform = str  # 保持键的大小写

# 允许多值
config = configparser.ConfigParser()
config.read_string('''
[tags]
values = tag1
    tag2
    tag3
''')

# ========== 类型转换 ==========
config = configparser.ConfigParser()
config.read_string('''
[settings]
count = 42
enabled = true
ratio = 3.14
items = 1, 2, 3
''')

# 内置转换
config.getint('settings', 'count')
config.getfloat('settings', 'ratio')
config.getboolean('settings', 'enabled')

# 自定义转换
def getlist(config, section, option):
    value = config.get(section, option)
    return [x.strip() for x in value.split(',')]

items = getlist(config, 'settings', 'items')  # ['1', '2', '3']

# ========== 配置类封装 ==========
class AppConfig:
    """应用配置类"""

    def __init__(self, config_file: str = 'config.ini'):
        self._config = configparser.ConfigParser()
        self._config.read(config_file)

    @property
    def database_host(self) -> str:
        return self._config.get('database', 'host', fallback='localhost')

    @property
    def database_port(self) -> int:
        return self._config.getint('database', 'port', fallback=5432)

    @property
    def debug(self) -> bool:
        return self._config.getboolean('DEFAULT', 'debug', fallback=False)

    def get(self, section: str, option: str, fallback=None):
        return self._config.get(section, option, fallback=fallback)

# 使用
# config = AppConfig()
# print(config.database_host)

# ========== 最佳实践 ==========
"""
1. 使用类封装配置访问
2. 提供合理的默认值
3. 使用类型转换获取正确类型
4. 敏感配置考虑环境变量
5. 配置文件加入版本控制模板
6. 实际配置加入.gitignore
"""
```

---

## 附录：快速参考

### 包管理工具选择速查表

| 场景 | 推荐工具 | 理由 |
|------|---------|------|
| 快速原型 | uv | 极速安装 |
| Web开发 | Poetry/PDM | 依赖锁定完善 |
| 数据科学 | Conda | 非Python依赖 |
| CI/CD | uv | 节省时间 |
| 库开发 | Poetry/hatch | 发布流程完善 |
| 遗留项目 | pip | 无需迁移 |

### 标准库模块分类速查

| 类别 | 核心模块 |
|------|---------|
| 系统文件 | os, sys, pathlib, shutil, glob, tempfile |
| 数据结构 | collections, dataclasses, enum, typing |
| 函数式 | itertools, functools, operator |
| 并发 | threading, multiprocessing, asyncio, concurrent.futures |
| 网络 | socket, urllib, http |
| 数据格式 | json, csv, xml |
| 测试 | unittest, pytest(第三方) |
| 调试 | logging, pdb |
| 其他 | re, datetime, decimal, hashlib, argparse, configparser |

### 常见陷阱速查

| 模块 | 陷阱 | 解决方案 |
|------|------|---------|
| pip | 全局安装 | 使用虚拟环境 |
| dict | 可变默认参数 | 用None或factory |
| datetime | 时区问题 | 使用timezone |
| float | 精度问题 | 用Decimal |
| random | 安全随机 | 用secrets |
| json | datetime序列化 | 自定义encoder |
| re | 贪婪匹配 | 用非贪婪.*? |
| threading | GIL限制 | CPU密集用多进程 |

---

> **文档版本**: 1.0
> **最后更新**: 2024年
> **适用范围**: Python 3.9+
