# 🚀 Python 2025 快速开始指南

<div align="center">

**5分钟上手现代Python开发环境**-

</div>

---

## 📦 系统要求

- Windows 10/11, Linux, or macOS
- 互联网连接
- 500MB 磁盘空间

---

## ⚡ 快速安装

### 1. 安装 UV (包管理器)

**Windows (PowerShell)**:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Linux/macOS**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 安装 Python

```bash
# 安装 Python 3.12 (推荐)
uv python install 3.12

# 验证安装
uv python list
```

### 3. 创建项目

```bash
# 初始化项目
uv init my-project
cd my-project

# 创建虚拟环境
uv venv

# 激活虚拟环境 (Windows)
.venv\Scripts\activate

# 激活虚拟环境 (Linux/macOS)
source .venv/bin/activate
```

### 4. 安装工具

```bash
# 安装核心工具
uv pip install ruff mypy pytest

# 安装 Web 开发工具
uv pip install fastapi uvicorn pydantic

# 安装数据处理工具
uv pip install polars
```

---

## 🎯 第一个程序

### hello.py

```python
from typing import Protocol

class Greeter(Protocol):
    """问候协议"""
    def greet(self, name: str) -> str: ...

class FriendlyGreeter:
    """友好的问候者"""
    def greet(self, name: str) -> str:
        return f"Hello, {name}! Welcome to Python 2025!"

def main() -> None:
    greeter = FriendlyGreeter()
    print(greeter.greet("World"))

if __name__ == "__main__":
    main()
```

### 运行程序

```bash
# 运行
python hello.py

# 类型检查
mypy hello.py

# 代码检查
ruff check hello.py

# 格式化
ruff format hello.py
```

---

## 📚 下一步

### 学习路径

1. **运行示例** - 查看 `examples/` 目录
2. **阅读文档** - 查看 `PYTHON_2025_STANDARDS.md`
3. **配置项目** - 参考 `pyproject.toml`
4. **最佳实践** - 查看 `.cursorrules`

### 推荐阅读顺序

```text
1. README_PYTHON_2025.md          ← 项目概览
2. examples/01_python312_new_features.py  ← Python 3.12 特性
3. examples/03_modern_type_system.py      ← 类型系统
4. PYTHON_2025_STANDARDS.md       ← 完整标准
5. FINAL_REPORT_2025.md           ← 最终报告
```

---

## 🛠️ 常用命令

### UV 命令

```bash
# 添加依赖
uv add fastapi

# 添加开发依赖
uv add --dev pytest

# 同步依赖
uv sync

# 运行脚本
uv run python script.py

# 锁定依赖
uv lock
```

### Ruff 命令

```bash
# 检查代码
ruff check .

# 自动修复
ruff check --fix .

# 格式化代码
ruff format .

# 检查+格式化
ruff check --fix . && ruff format .
```

### Pytest 命令

```bash
# 运行测试
pytest

# 生成覆盖率报告
pytest --cov=src

# 详细输出
pytest -v

# 并行测试
pytest -n auto
```

---

## 💡 配置模板

### pyproject.toml (最小配置)

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

---

## 🎓 学习资源

- **官方文档**: <https://docs.python.org/3.12/>
- **UV 文档**: <https://docs.astral.sh/uv/>
- **Ruff 文档**: <https://docs.astral.sh/ruff/>
- **本项目**: 查看 `examples/` 和文档

---

## 🤝 获取帮助

1. 查看文档: `README_PYTHON_2025.md`
2. 运行示例: `examples/*.py`
3. 检查配置: `pyproject.toml`

---

<div align="center">

**开始你的现代Python之旅!** 🚀

</div>
