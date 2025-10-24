# Modern Python Project 2025

> 基于2025年10月最新技术栈和最佳实践的Python项目模板

## 🚀 特性

- ✅ **Python 3.12+** - 使用最新稳定Python版本
- ⚡ **uv** - 超快的包管理器（10-100倍提升）
- 🔥 **ruff** - 超快的代码质量工具（替代black/isort/flake8）
- 🎯 **mypy** - 严格的类型检查
- 🧪 **pytest** - 现代测试框架
- 📦 **pre-commit** - 自动化代码质量检查
- 🐳 **Docker** - 容器化部署
- 🔄 **GitHub Actions** - CI/CD自动化

## 📋 系统要求

- Python 3.12 或更高版本
- uv (推荐) 或 pip
- Git

## 🛠️ 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/my-modern-project.git
cd my-modern-project
```

### 2. 设置开发环境

#### 使用 uv (推荐)

```bash
# 安装 uv
pip install uv

# 创建虚拟环境
uv venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
uv sync --all-extras
```

#### 使用 pip

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -e ".[dev]"
```

### 3. 设置 pre-commit 钩子

```bash
pre-commit install
```

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并显示覆盖率
pytest --cov

# 运行特定测试
pytest tests/test_module.py

# 运行标记的测试
pytest -m unit
```

## 🔍 代码质量检查

```bash
# 运行 ruff 检查
ruff check .

# 自动修复问题
ruff check --fix .

# 格式化代码
ruff format .

# 运行类型检查
mypy .

# 运行所有检查（pre-commit）
pre-commit run --all-files
```

## 📦 项目结构

```
my-modern-project/
├── src/
│   └── my_modern_project/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── conftest.py
├── docs/
│   └── index.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
├── Dockerfile
└── docker-compose.yml
```

## 🐳 Docker部署

```bash
# 构建镜像
docker build -t my-modern-project:latest .

# 运行容器
docker run -p 8000:8000 my-modern-project:latest

# 使用 docker-compose
docker-compose up -d
```

## 📝 开发工作流

1. **创建新分支**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **编写代码**
   - 遵循类型注解
   - 编写测试
   - 添加文档字符串

3. **运行检查**
   ```bash
   ruff check --fix .
   ruff format .
   mypy .
   pytest
   ```

4. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   # pre-commit 钩子会自动运行
   ```

5. **推送并创建PR**
   ```bash
   git push origin feature/my-feature
   ```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🔗 相关资源

- [Python 3.12 文档](https://docs.python.org/3.12/)
- [uv 文档](https://github.com/astral-sh/uv)
- [ruff 文档](https://docs.astral.sh/ruff/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [pytest 文档](https://docs.pytest.org/)

## 📧 联系方式

- 作者: Your Name
- 邮箱: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

⭐ 如果这个项目对你有帮助，请给个星标！

