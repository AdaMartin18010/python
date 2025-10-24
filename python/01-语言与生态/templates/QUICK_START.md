# Python 2025 快速启动指南

> 5分钟快速上手2025年Python现代开发

## 🚀 快速开始（最少步骤）

### 1. 安装Python 3.12+

```bash
# Windows (使用 winget)
winget install Python.Python.3.12

# macOS (使用 Homebrew)
brew install python@3.12

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3.12 python3.12-venv
```

### 2. 安装 uv (推荐的包管理器)

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv
```

### 3. 创建新项目

#### 方法1：使用模板（推荐）

```bash
# 复制模板
cp -r templates/modern-project-2025 my-project
cd my-project

# 初始化 git
git init
git add .
git commit -m "Initial commit from 2025 template"
```

#### 方法2：从零开始

```bash
# 创建项目目录
mkdir my-project && cd my-project

# 使用 uv 初始化
uv init

# 创建虚拟环境
uv venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 4. 安装开发工具

```bash
# 安装核心工具
uv add --dev ruff mypy pytest pre-commit

# 设置 pre-commit
pre-commit install
```

## 📝 创建第一个文件

### pyproject.toml（最小配置）

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = [
    "ruff>=0.6.0",
    "mypy>=1.11.0",
    "pytest>=8.3.0",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.mypy]
python_version = "3.12"
strict = true
```

### 第一个Python文件

```python
# src/main.py
"""主模块"""


def greet(name: str) -> str:
    """
    生成问候语

    Args:
        name: 要问候的名字

    Returns:
        问候字符串
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("World"))
```

### 第一个测试文件

```python
# tests/test_main.py
"""测试主模块"""

from src.main import greet


def test_greet() -> None:
    """测试 greet 函数"""
    assert greet("World") == "Hello, World!"
```

## 🔍 运行检查

```bash
# 格式化代码
ruff format .

# 检查代码质量
ruff check --fix .

# 类型检查
mypy .

# 运行测试
pytest
```

## 📦 常用命令速查

### uv 命令

```bash
# 添加依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 安装所有依赖
uv sync

# 运行脚本
uv run python script.py

# 更新依赖
uv lock --upgrade
```

### 开发工作流

```bash
# 1. 创建功能分支
git checkout -b feature/my-feature

# 2. 编写代码
# 3. 格式化和检查
ruff format . && ruff check --fix . && mypy .

# 4. 运行测试
pytest

# 5. 提交（自动运行 pre-commit）
git add .
git commit -m "feat: add new feature"

# 6. 推送
git push origin feature/my-feature
```

## 🎯 Web应用快速开始（FastAPI）

```bash
# 安装 FastAPI
uv add fastapi uvicorn[standard]
```

```python
# src/app.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    """根路径"""
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# 运行
uv run python src/app.py

# 访问
# http://localhost:8000
# http://localhost:8000/docs (自动生成的API文档)
```

## 📊 数据科学快速开始

```bash
# 安装数据科学库
uv add polars pandas numpy matplotlib
```

```python
# analysis.py
import polars as pl

# 读取CSV（Polars比Pandas快10-100倍）
df = pl.read_csv("data.csv")

# 数据处理
result = (
    df
    .filter(pl.col("age") > 18)
    .group_by("city")
    .agg(pl.col("income").mean())
)

print(result)
```

## 🤖 AI/ML快速开始

```bash
# 安装AI库
uv add openai langchain
```

```python
# ai_app.py
from openai import OpenAI

client = OpenAI(api_key="your-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## 🐳 Docker快速开始

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install uv
COPY . .
RUN uv sync
CMD ["uv", "run", "python", "src/main.py"]
```

```bash
# 构建和运行
docker build -t my-project .
docker run my-project
```

## 📚 下一步

1. **阅读完整文档**：`python/01-语言与生态/README.md`
2. **查看示例项目**：`templates/modern-project-2025/`
3. **学习最佳实践**：各章节README
4. **配置IDE**：VSCode/PyCharm设置

## 🆘 常见问题

### Q: uv和pip的区别？
A: uv比pip快10-100倍，是2025年推荐的包管理器。完全兼容pip。

### Q: 为什么使用Python 3.12？
A: Python 3.12是当前最稳定的版本，性能比3.10提升25%。

### Q: ruff是什么？
A: ruff是超快的Python linter，替代black+isort+flake8。

### Q: 必须使用类型注解吗？
A: 强烈推荐。类型注解提高代码质量，是2025年最佳实践。

## 🔗 资源链接

- [Python 3.12 官方文档](https://docs.python.org/3.12/)
- [uv 官方文档](https://github.com/astral-sh/uv)
- [ruff 官方文档](https://docs.astral.sh/ruff/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)

---

**现在开始你的Python 2025之旅吧！** 🚀

