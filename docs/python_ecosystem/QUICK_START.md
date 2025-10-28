# Python 生态系统快速开始

**5分钟快速了解Python生态系统**

---

## 🎯 核心推荐

### 必备工具 ⭐⭐⭐⭐⭐

```bash
# 包管理器
uv                    # 10-100x faster than pip

# 代码质量
ruff                  # 90x faster than pylint
mypy                  # 静态类型检查

# Web框架
FastAPI               # 现代、快速、类型安全

# 数据处理
polars                # 比pandas快10-100倍

# 测试
pytest                # 现代测试框架

# 监控
opentelemetry         # 云原生可观测性
```

---

## 🚀 快速安装

### 使用 uv (推荐)

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建项目
uv init my-project
cd my-project

# 添加依赖
uv add fastapi uvicorn pydantic

# 运行
uv run python main.py
```

### 传统方式

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install fastapi uvicorn pydantic
```

---

## 📦 按场景选择

### 1️⃣ Web API 开发

**技术栈**:
```
FastAPI + Pydantic + SQLAlchemy + Redis
```

**安装**:
```bash
uv add fastapi uvicorn pydantic sqlalchemy redis
```

**Hello World**:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 运行: uvicorn main:app --reload
```

---

### 2️⃣ 数据分析

**技术栈**:
```
Polars + NumPy + Matplotlib
```

**安装**:
```bash
uv add polars numpy matplotlib
```

**示例**:
```python
import polars as pl

df = pl.read_csv("data.csv")
result = df.filter(pl.col("age") > 18).select(["name", "age"])
print(result)
```

---

### 3️⃣ 异步应用

**技术栈**:
```
AsyncIO + aiohttp + asyncpg
```

**安装**:
```bash
uv add aiohttp asyncpg
```

**示例**:
```python
import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

asyncio.run(fetch("https://api.example.com"))
```

---

### 4️⃣ 微服务

**技术栈**:
```
FastAPI + gRPC + OpenTelemetry + Docker
```

**安装**:
```bash
uv add fastapi grpcio opentelemetry-api
```

---

## 🎓 学习路径

### 第1周: 基础
- [ ] FastAPI基础
- [ ] Pydantic数据验证
- [ ] pytest测试

### 第2周: 数据库
- [ ] SQLAlchemy ORM
- [ ] asyncpg异步数据库
- [ ] Redis缓存

### 第3周: 高级
- [ ] 异步编程
- [ ] 微服务架构
- [ ] 性能优化

### 第4周: DevOps
- [ ] Docker容器化
- [ ] CI/CD流水线
- [ ] 监控告警

---

## 📚 推荐阅读顺序

1. **[Web框架](01-web-frameworks/README.md)** - 从FastAPI开始
2. **[API工具](07-api-tools/README.md)** - Pydantic数据验证
3. **[测试](04-testing/README.md)** - pytest测试框架
4. **[数据库](05-databases/README.md)** - SQLAlchemy
5. **[异步编程](03-async-programming/README.md)** - AsyncIO
6. **[DevOps](06-devops/README.md)** - Docker和CI/CD
7. **[监控](08-monitoring/README.md)** - OpenTelemetry

---

## 🔥 2025年热门技术

### 性能提升
- **uv**: 比pip快10-100倍 ⚡
- **ruff**: 比pylint快90倍 ⚡
- **Polars**: 比pandas快10-100倍 ⚡

### 新特性
- **Python 3.12/3.13**: 性能提升、新语法
- **Free-threaded mode**: 真正的并行
- **JIT编译器**: 进一步提速

### 云原生
- **OpenTelemetry**: 统一可观测性标准
- **FastAPI**: 云原生API框架
- **Kubernetes**: 容器编排

---

## 💡 最佳实践

### 项目结构
```
my-project/
├── pyproject.toml      # uv配置
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── api/
├── tests/
│   └── test_main.py
└── README.md
```

### pyproject.toml
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn>=0.27.0",
    "pydantic>=2.0.0",
]

[tool.ruff]
line-length = 100

[tool.mypy]
python_version = "3.12"
strict = true
```

---

## 🆘 快速帮助

### 常见问题

**Q: 如何选择Web框架？**
A: 新项目推荐FastAPI，大型项目考虑Django

**Q: 数据分析用什么？**
A: 新项目用Polars，现有项目可继续用Pandas

**Q: 如何提高性能？**
A: 1) 使用异步IO 2) 使用Polars 3) 优化算法

**Q: 如何监控应用？**
A: 使用OpenTelemetry + Prometheus + Grafana

---

## 🔗 有用链接

- [主文档](README.md)
- [Python官方文档](https://docs.python.org/)
- [PyPI包索引](https://pypi.org/)
- [Real Python教程](https://realpython.com/)

---

**开始你的Python之旅！** 🐍✨

**最后更新**: 2025年10月28日

