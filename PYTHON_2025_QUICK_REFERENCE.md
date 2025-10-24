# Python 2025 快速参考卡 (Cheat Sheet)

**版本**: 1.0.0  
**日期**: 2025年10月24日  
**适用**: Python 3.12+ / uv 0.8+

---

## 🚀 快速开始

### 安装 uv (推荐包管理器)

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证安装
uv --version  # uv 0.8.17+
```

### 创建新项目 (30秒)

```bash
# 1. 创建项目
uv init my-project
cd my-project

# 2. 创建虚拟环境
uv venv

# 3. 激活环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 4. 添加依赖
uv add fastapi "uvicorn[standard]" sqlalchemy

# 5. 运行
uvicorn main:app --reload
```

---

## 📦 包管理速查

### uv 常用命令

```bash
# 项目管理
uv init [name]              # 创建新项目
uv venv                     # 创建虚拟环境
uv venv --python 3.13       # 指定Python版本

# 依赖管理
uv add package              # 添加依赖
uv add --dev pytest         # 添加开发依赖
uv remove package           # 移除依赖
uv sync                     # 同步依赖
uv sync --frozen            # CI/CD 锁定同步
uv lock                     # 生成锁文件
uv lock --upgrade           # 升级所有依赖

# Python 版本管理
uv python install 3.12      # 安装 Python 3.12
uv python install 3.13      # 安装 Python 3.13
uv python list              # 列出已安装版本
uv python pin 3.12          # 固定项目版本

# 运行脚本
uvx python script.py        # 运行脚本 (自动依赖)
uvx ruff check .            # 临时运行工具

# 缓存管理
uv cache clean              # 清理缓存
uv cache dir                # 显示缓存目录
```

### pyproject.toml 模板

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
readme = "README.md"
requires-python = ">=3.12"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = [
    "fastapi>=0.115.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.10.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "S", "B", "A"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q --cov=src --cov-report=html"
```

---

## 🔧 代码质量工具

### ruff (Linter + Formatter)

```bash
# 检查代码
ruff check .                # 检查所有文件
ruff check --fix .          # 自动修复

# 格式化代码
ruff format .               # 格式化所有文件
ruff format --check .       # 检查格式 (CI)

# 配置文件
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "ANN",  # flake8-annotations
    "S",    # flake8-bandit
    "B",    # flake8-bugbear
]
```

### mypy (类型检查)

```bash
# 检查类型
mypy src/

# 配置
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### pytest (测试)

```bash
# 运行测试
pytest                      # 运行所有测试
pytest -v                   # 详细输出
pytest -k "test_user"       # 运行特定测试
pytest --cov=src            # 代码覆盖率
pytest --cov-report=html    # HTML 报告

# 配置
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = "-ra -q --cov=src --cov-report=html"
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

---

## 🌐 Web 开发速查

### FastAPI 快速模板

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

app = FastAPI(
    title="My API",
    version="1.0.0",
    description="API Description"
)

# 数据模型
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    class Config:
        from_attributes = True

# 依赖注入
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# 路由
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """创建新用户"""
    # 业务逻辑
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """获取用户"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 启动
# uvicorn main:app --reload
```

### SQLAlchemy 2.0 异步模板

```python
# database.py
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

# 模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# 查询
from sqlalchemy import select

async def get_user(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_users(session: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(User).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()
```

---

## 📊 数据处理速查

### Polars (推荐)

```python
import polars as pl

# 读取数据
df = pl.read_csv("data.csv")
df = pl.scan_csv("large.csv")  # 懒加载

# 基本操作
df.head(10)                    # 前10行
df.shape                       # (行数, 列数)
df.columns                     # 列名
df.dtypes                      # 数据类型

# 筛选
df.filter(pl.col("age") > 18)
df.filter((pl.col("age") > 18) & (pl.col("city") == "NYC"))

# 选择列
df.select(["name", "age"])
df.select(pl.col("*").exclude("id"))

# 聚合
df.group_by("category").agg([
    pl.col("value").sum().alias("total"),
    pl.col("value").mean().alias("avg"),
    pl.col("id").count().alias("count"),
])

# 排序
df.sort("age", descending=True)

# Join
df1.join(df2, on="id", how="inner")

# 链式调用
result = (
    df
    .filter(pl.col("age") > 18)
    .group_by("city")
    .agg(pl.col("salary").mean())
    .sort("salary", descending=True)
)

# 写入
df.write_csv("output.csv")
df.write_parquet("output.parquet")
```

### DuckDB (SQL 查询)

```python
import duckdb

# 直接查询 CSV
result = duckdb.sql("""
    SELECT category, SUM(value) as total
    FROM 'data.csv'
    WHERE value > 100
    GROUP BY category
    ORDER BY total DESC
""").to_df()

# 连接数据库
con = duckdb.connect("database.duckdb")

# 查询
df = con.execute("""
    SELECT * FROM users
    WHERE age > 18
""").fetch_df()

# Polars 集成
import polars as pl
df_polars = pl.read_csv("data.csv")
result = duckdb.sql("""
    SELECT * FROM df_polars WHERE age > 18
""").pl()  # 返回 Polars DataFrame
```

---

## 🤖 AI/ML 速查

### PyTorch 模型模板

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 定义模型
class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# 初始化
model = SimpleNet(input_size=784, hidden_size=128, num_classes=10)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练
for epoch in range(num_epochs):
    for images, labels in train_loader:
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 保存模型
torch.save(model.state_dict(), 'model.pth')

# 加载模型
model.load_state_dict(torch.load('model.pth'))
model.eval()
```

### LangChain RAG 模板

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader

# 1. 加载文档
loader = DirectoryLoader("docs/", glob="**/*.md")
documents = loader.load()

# 2. 分割文本
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_documents(documents)

# 3. 创建向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Qdrant.from_documents(
    texts,
    embeddings,
    url="http://localhost:6333",
    collection_name="docs"
)

# 4. 创建检索链
llm = ChatOpenAI(model="gpt-4", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# 5. 查询
result = qa_chain({"query": "What is Python?"})
print(result["result"])
print(f"\n来源: {result['source_documents']}")
```

---

## 🧪 异步编程速查

### asyncio 基础

```python
import asyncio
import aiohttp

# 基本异步函数
async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# 运行单个协程
result = await fetch_url("https://api.example.com")

# 并发多个协程
urls = ["https://api.example.com/1", "https://api.example.com/2"]
tasks = [fetch_url(url) for url in urls]
results = await asyncio.gather(*tasks)

# 主函数
async def main():
    result = await fetch_url("https://api.example.com")
    print(result)

# 运行
asyncio.run(main())

# 超时控制
try:
    result = await asyncio.wait_for(fetch_url(url), timeout=5.0)
except asyncio.TimeoutError:
    print("请求超时")

# 并发控制
semaphore = asyncio.Semaphore(10)  # 最多10个并发

async def fetch_with_limit(url: str):
    async with semaphore:
        return await fetch_url(url)
```

### httpx (同步+异步)

```python
import httpx

# 同步
response = httpx.get("https://api.example.com")
print(response.json())

# 异步
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")
    print(response.json())

# 配置
client = httpx.AsyncClient(
    timeout=httpx.Timeout(10.0),
    limits=httpx.Limits(max_keepalive_connections=5),
    headers={"User-Agent": "MyApp/1.0"}
)
```

---

## 🎨 类型注解速查

### Python 3.12+ 类型注解

```python
from typing import (
    List, Dict, Set, Tuple, Optional, Union,
    Any, Callable, Literal, TypeVar, Generic,
    Protocol, TypedDict, NotRequired
)
from collections.abc import Sequence, Iterable

# 基础类型
def greet(name: str) -> str:
    return f"Hello, {name}"

# 集合类型 (Python 3.9+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# 可选类型 (Python 3.10+)
def find_user(user_id: int) -> User | None:
    pass

# 联合类型
def process(value: str | int | float) -> str:
    return str(value)

# 泛型 (Python 3.12+)
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

class Stack[T]:
    def __init__(self) -> None:
        self.items: list[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()

# Protocol (结构化类型)
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()

# TypedDict
class UserDict(TypedDict):
    name: str
    age: int
    email: NotRequired[str]  # 可选字段

# Literal
Mode = Literal["r", "w", "a"]

def open_file(path: str, mode: Mode) -> None:
    pass

# Callable
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)
```

---

## 🔒 安全最佳实践

```python
# 1. 密码哈希 (bcrypt)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# 2. JWT Token
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # 从环境变量读取!
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise

# 3. SQL 防注入 (参数化查询)
# ✅ 安全
stmt = select(User).where(User.username == username)

# ❌ 危险 (永远不要这样做!)
# query = f"SELECT * FROM users WHERE username = '{username}'"

# 4. 环境变量
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    api_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 📈 性能优化技巧

```python
# 1. 列表推导 vs for 循环
# ✅ 快 20-30%
result = [x * 2 for x in range(1000)]

# ⚠️ 慢
result = []
for x in range(1000):
    result.append(x * 2)

# 2. 生成器 (节省内存)
# ✅ 内存高效
gen = (x * 2 for x in range(1_000_000))

# ⚠️ 内存占用大
lst = [x * 2 for x in range(1_000_000)]

# 3. __slots__ (减少内存)
class User:
    __slots__ = ['name', 'email', 'age']  # 节省 40% 内存
    
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age

# 4. lru_cache (缓存)
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 5. orjson (JSON 快 5-10x)
import orjson

# 序列化
json_bytes = orjson.dumps(data)

# 反序列化
data = orjson.loads(json_bytes)

# 6. uvloop (asyncio 快 2-4x)
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 7. NumPy 向量化
import numpy as np

# ✅ 快 10-100x
arr = np.array([1, 2, 3, 4, 5])
result = arr * 2

# ⚠️ 慢
result = [x * 2 for x in [1, 2, 3, 4, 5]]
```

---

## 🐛 调试技巧

```python
# 1. 断点调试
import pdb

def buggy_function():
    x = 10
    pdb.set_trace()  # 设置断点
    y = x * 2
    return y

# 2. 打印调试
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")

# 3. 结构化日志 (推荐)
import structlog

log = structlog.get_logger()

log.info("user_created", user_id=123, username="john")

# 4. 性能分析
import cProfile
import pstats

cProfile.run('my_function()', 'profile.stats')
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumulative').print_stats(10)

# 5. 内存分析
from memory_profiler import profile

@profile
def my_function():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a
```

---

## 📚 推荐资源

### 官方文档
- [Python 官方文档](https://docs.python.org/3/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Polars 文档](https://pola-rs.github.io/polars/)
- [uv 文档](https://docs.astral.sh/uv/)

### 书籍推荐
- **Fluent Python** (2nd Edition, 2022) - Python 进阶必读
- **Python Concurrency with asyncio** (2022) - 异步编程
- **High Performance Python** (3rd Edition, 2025) - 性能优化

### 在线资源
- [Real Python](https://realpython.com/) - 高质量教程
- [Python Weekly](https://www.pythonweekly.com/) - 周刊
- [Awesome Python](https://awesome-python.com/) - 库索引

---

## 🎯 常见问题

### Q: Python 3.12 vs 3.13, 应该用哪个?
**A**: 
- **生产环境**: Python 3.12 (LTS, 稳定)
- **新项目**: Python 3.13 (稳定, 性能更好)
- **实验**: Python 3.14-dev

### Q: uv vs poetry, 选哪个?
**A**: 
- **新项目**: uv (10-100x 性能提升)
- **遗留项目**: 继续用 poetry (生态成熟)
- **迁移**: poetry → uv (简单)

### Q: Pandas vs Polars, 怎么选?
**A**:
- **数据 < 1GB**: Pandas (生态丰富)
- **数据 > 1GB**: Polars (10-100x 性能)
- **新项目**: Polars (现代化)

### Q: FastAPI vs Django?
**A**:
- **API/微服务**: FastAPI (性能+类型安全)
- **全栈应用**: Django (功能完整)
- **轻量级**: Flask

---

**更新日期**: 2025年10月24日  
**下次更新**: 2026年1月  
**反馈**: 欢迎提交 Issue!

