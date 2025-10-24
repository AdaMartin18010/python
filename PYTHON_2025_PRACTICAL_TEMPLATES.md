# Python 2025 实战模板集合

**版本**: 1.0.0  
**日期**: 2025年10月24日  
**用途**: 快速启动项目、生产级配置模板

---

## 📋 目录

- [Python 2025 实战模板集合](#python-2025-实战模板集合)
  - [📋 目录](#-目录)
  - [1. 项目初始化模板](#1-项目初始化模板)
    - [1.1 完整 pyproject.toml (生产级)](#11-完整-pyprojecttoml-生产级)
    - [1.2 项目目录结构](#12-项目目录结构)
    - [1.3 Makefile](#13-makefile)
  - [2. FastAPI 完整项目模板](#2-fastapi-完整项目模板)
    - [2.1 主应用文件 (src/my\_project/main.py)](#21-主应用文件-srcmy_projectmainpy)
    - [2.2 配置管理 (src/my\_project/config.py)](#22-配置管理-srcmy_projectconfigpy)
    - [2.3 数据库会话 (src/my\_project/db/session.py)](#23-数据库会话-srcmy_projectdbsessionpy)
    - [2.4 用户模型 (src/my\_project/models/user.py)](#24-用户模型-srcmy_projectmodelsuserpy)
    - [2.5 Pydantic 模式 (src/my\_project/schemas/user.py)](#25-pydantic-模式-srcmy_projectschemasuserpy)
    - [2.6 用户服务 (src/my\_project/services/user.py)](#26-用户服务-srcmy_projectservicesuserpy)
    - [2.7 用户路由 (src/my\_project/api/v1/users.py)](#27-用户路由-srcmy_projectapiv1userspy)
  - [3. 数据处理管道模板](#3-数据处理管道模板)
    - [3.1 Polars ETL 管道](#31-polars-etl-管道)
  - [4. AI/RAG 应用模板](#4-airag-应用模板)
    - [4.1 LangChain RAG 系统](#41-langchain-rag-系统)

---

## 1. 项目初始化模板

### 1.1 完整 pyproject.toml (生产级)

```toml
[project]
name = "my-awesome-project"
version = "0.1.0"
description = "Production-ready Python project"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["fastapi", "api", "backend"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

dependencies = [
    # Web框架
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    
    # 数据验证
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "email-validator>=2.2.0",
    
    # 数据库
    "sqlalchemy[asyncio]>=2.0.0",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    
    # 缓存
    "redis[hiredis]>=5.2.0",
    
    # HTTP客户端
    "httpx>=0.27.0",
    
    # 数据处理
    "polars>=1.10.0",
    
    # 认证
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    
    # 日志
    "structlog>=24.4.0",
    
    # 配置
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    # 测试
    "pytest>=8.3.0",
    "pytest-cov>=6.0.0",
    "pytest-asyncio>=0.24.0",
    "pytest-mock>=3.14.0",
    "faker>=30.0.0",
    "factory-boy>=3.3.0",
    
    # 代码质量
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "bandit>=1.8.0",
    
    # 类型存根
    "types-redis>=4.6.0",
    "types-passlib>=1.7.7",
    
    # 开发工具
    "ipython>=8.29.0",
    "ipdb>=0.13.13",
]

[project.scripts]
start = "my_project.main:start"
migrate = "my_project.db:migrate"

[project.urls]
Homepage = "https://github.com/yourusername/my-awesome-project"
Documentation = "https://my-awesome-project.readthedocs.io"
Repository = "https://github.com/yourusername/my-awesome-project"
Issues = "https://github.com/yourusername/my-awesome-project/issues"

[build-system]
requires = ["hatchling>=1.25.0"]
build-backend = "hatchling.build"

# ============================================
# Hatchling 配置
# ============================================
[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

# ============================================
# Ruff 配置
# ============================================
[tool.ruff]
line-length = 100
target-version = "py312"
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",     # pycodestyle errors
    "W",     # pycodestyle warnings
    "F",     # pyflakes
    "I",     # isort
    "N",     # pep8-naming
    "UP",    # pyupgrade
    "ANN",   # flake8-annotations
    "ASYNC", # flake8-async
    "S",     # flake8-bandit
    "B",     # flake8-bugbear
    "A",     # flake8-builtins
    "C4",    # flake8-comprehensions
    "DTZ",   # flake8-datetimez
    "T10",   # flake8-debugger
    "EM",    # flake8-errmsg
    "ISC",   # flake8-implicit-str-concat
    "ICN",   # flake8-import-conventions
    "PIE",   # flake8-pie
    "PYI",   # flake8-pyi
    "Q",     # flake8-quotes
    "RSE",   # flake8-raise
    "RET",   # flake8-return
    "SIM",   # flake8-simplify
    "TID",   # flake8-tidy-imports
    "TCH",   # flake8-type-checking
    "ARG",   # flake8-unused-arguments
    "PTH",   # flake8-use-pathlib
    "ERA",   # eradicate
    "PD",    # pandas-vet
    "PL",    # pylint
    "TRY",   # tryceratops
    "NPY",   # numpy
    "RUF",   # ruff-specific
]

ignore = [
    "ANN101",  # Missing type annotation for self
    "ANN102",  # Missing type annotation for cls
    "D",       # pydocstyle (根据团队决定)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",    # Use of assert
    "ARG",     # Unused arguments
    "PLR2004", # Magic values
]

[tool.ruff.lint.isort]
known-first-party = ["my_project"]

# ============================================
# Mypy 配置
# ============================================
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

# 插件
plugins = [
    "pydantic.mypy",
    "sqlalchemy.ext.mypy.plugin",
]

# 第三方库忽略
[[tool.mypy.overrides]]
module = [
    "redis.*",
    "uvicorn.*",
]
ignore_missing_imports = true

# ============================================
# Pytest 配置
# ============================================
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
pythonpath = ["src"]
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
    "--strict-config",
    "--cov=src/my_project",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-report=xml",
    "--cov-fail-under=80",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]
asyncio_mode = "auto"

# ============================================
# Coverage 配置
# ============================================
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]

# ============================================
# Bandit 配置
# ============================================
[tool.bandit]
skips = ["B101"]  # assert_used (测试中允许)
exclude_dirs = ["tests", "migrations"]
```

### 1.2 项目目录结构

```text
my-awesome-project/
├── .github/
│   └── workflows/
│       ├── ci.yml                  # CI 流水线
│       └── release.yml             # 发布流程
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py                 # 应用入口
│       ├── config.py               # 配置管理
│       ├── api/
│       │   ├── __init__.py
│       │   ├── deps.py             # 依赖注入
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── auth.py         # 认证路由
│       │       └── users.py        # 用户路由
│       ├── core/
│       │   ├── __init__.py
│       │   ├── security.py         # 安全工具
│       │   └── logging.py          # 日志配置
│       ├── db/
│       │   ├── __init__.py
│       │   ├── base.py             # 数据库基类
│       │   ├── session.py          # 会话管理
│       │   └── migrations/         # Alembic 迁移
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py             # 数据模型
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── user.py             # Pydantic 模式
│       ├── services/
│       │   ├── __init__.py
│       │   └── user.py             # 业务逻辑
│       └── utils/
│           ├── __init__.py
│           └── helpers.py          # 工具函数
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # pytest 配置
│   ├── unit/
│   │   └── test_users.py
│   └── integration/
│       └── test_api.py
├── migrations/                     # Alembic 迁移
│   └── versions/
├── docs/
│   ├── index.md
│   └── api.md
├── scripts/
│   ├── setup.sh                    # 环境设置
│   └── deploy.sh                   # 部署脚本
├── .env.example                    # 环境变量示例
├── .gitignore
├── .pre-commit-config.yaml         # Pre-commit hooks
├── docker-compose.yml              # 本地开发环境
├── Dockerfile                      # 生产镜像
├── Makefile                        # 常用命令
├── pyproject.toml                  # 项目配置
└── README.md
```

### 1.3 Makefile

```makefile
.PHONY: help install dev test lint format clean run docker-build docker-up

# 默认目标
help:
 @echo "可用命令:"
 @echo "  make install      - 安装依赖"
 @echo "  make dev          - 安装开发依赖"
 @echo "  make test         - 运行测试"
 @echo "  make lint         - 代码检查"
 @echo "  make format       - 代码格式化"
 @echo "  make clean        - 清理缓存"
 @echo "  make run          - 运行应用"
 @echo "  make docker-build - 构建 Docker 镜像"
 @echo "  make docker-up    - 启动 Docker 环境"

# 安装依赖
install:
 uv sync

# 安装开发依赖
dev:
 uv sync --all-extras

# 运行测试
test:
 pytest

# 代码检查
lint:
 ruff check .
 mypy src/
 bandit -r src/

# 代码格式化
format:
 ruff format .
 ruff check --fix .

# 清理缓存
clean:
 find . -type d -name "__pycache__" -exec rm -rf {} +
 find . -type d -name ".pytest_cache" -exec rm -rf {} +
 find . -type d -name ".mypy_cache" -exec rm -rf {} +
 find . -type d -name ".ruff_cache" -exec rm -rf {} +
 find . -type f -name "*.pyc" -delete
 rm -rf htmlcov/ .coverage coverage.xml

# 运行应用
run:
 uvicorn my_project.main:app --reload

# 数据库迁移
migrate:
 alembic upgrade head

# 创建迁移
migration:
 alembic revision --autogenerate -m "$(msg)"

# Docker 构建
docker-build:
 docker build -t my-project:latest .

# Docker 启动
docker-up:
 docker-compose up -d

# Docker 停止
docker-down:
 docker-compose down

# 安装 pre-commit hooks
install-hooks:
 pre-commit install
```

---

## 2. FastAPI 完整项目模板

### 2.1 主应用文件 (src/my_project/main.py)

```python
"""FastAPI 应用入口"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

from my_project.api.v1 import auth, users
from my_project.config import settings
from my_project.core.logging import configure_logging
from my_project.db.session import engine

# 配置日志
configure_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理"""
    logger.info("application_starting", version=settings.VERSION)
    
    # 启动时执行
    # 例如: 初始化数据库连接池、预加载模型等
    
    yield
    
    # 关闭时执行
    logger.info("application_shutdown")
    await engine.dispose()


# 创建应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-ready FastAPI application",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
    default_response_class=ORJSONResponse,  # 使用 orjson (5-10x 快)
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip 压缩
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/v1/users", tags=["用户"])


@app.get("/health")
async def health_check() -> dict[str, str]:
    """健康检查"""
    return {"status": "ok", "version": settings.VERSION}


@app.get("/")
async def root() -> dict[str, str]:
    """根路径"""
    return {
        "message": "Welcome to My Awesome API",
        "docs": "/api/docs",
        "version": settings.VERSION,
    }


# 启动函数 (供 uv run 使用)
def start() -> None:
    """启动应用"""
    import uvicorn
    
    uvicorn.run(
        "my_project.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,  # 使用自定义日志配置
    )


if __name__ == "__main__":
    start()
```

### 2.2 配置管理 (src/my_project/config.py)

```python
"""应用配置"""
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # 基础配置
    PROJECT_NAME: str = "My Awesome API"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: Literal["dev", "staging", "prod"] = "dev"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_HOSTS: list[str] = Field(default_factory=lambda: ["*"])
    
    # 数据库配置
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql+asyncpg://user:pass@localhost:5432/db"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False
    
    # Redis 配置
    REDIS_URL: RedisDsn = Field(default="redis://localhost:6379/0")
    REDIS_POOL_SIZE: int = 10
    
    # 安全配置
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_hosts(cls, v: str | list[str]) -> list[str]:
        """解析允许的主机"""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = True
    
    # Sentry (可选)
    SENTRY_DSN: str | None = None
    
    @property
    def database_url_sync(self) -> str:
        """同步数据库 URL (用于 Alembic)"""
        return str(self.DATABASE_URL).replace("+asyncpg", "")


# 创建全局配置实例
settings = Settings()
```

### 2.3 数据库会话 (src/my_project/db/session.py)

```python
"""数据库会话管理"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from my_project.config import settings

# 创建异步引擎
engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DB_ECHO,
    future=True,
)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# 声明基类
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话 (依赖注入)"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 2.4 用户模型 (src/my_project/models/user.py)

```python
"""用户数据模型"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from my_project.db.session import Base


class User(Base):
    """用户模型"""
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"
```

### 2.5 Pydantic 模式 (src/my_project/schemas/user.py)

```python
"""用户 Pydantic 模式"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """用户基础模式"""
    
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """创建用户"""
    
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """更新用户"""
    
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """用户响应"""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    """用户登录"""
    
    username: str
    password: str


class Token(BaseModel):
    """Token 响应"""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
```

### 2.6 用户服务 (src/my_project/services/user.py)

```python
"""用户业务逻辑"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from my_project.core.security import get_password_hash, verify_password
from my_project.models.user import User
from my_project.schemas.user import UserCreate, UserUpdate


class UserService:
    """用户服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> User | None:
        """根据 ID 获取用户"""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> User | None:
        """根据用户名获取用户"""
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        """根据邮箱获取用户"""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, user_create: UserCreate) -> User:
        """创建用户"""
        user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update(self, user: User, user_update: UserUpdate) -> User:
        """更新用户"""
        update_data = user_update.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user: User) -> None:
        """删除用户"""
        await self.db.delete(user)
        await self.db.flush()
    
    async def authenticate(self, username: str, password: str) -> User | None:
        """认证用户"""
        user = await self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
```

### 2.7 用户路由 (src/my_project/api/v1/users.py)

```python
"""用户路由"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from my_project.api.deps import get_current_active_user, get_db
from my_project.models.user import User
from my_project.schemas.user import UserCreate, UserResponse, UserUpdate
from my_project.services.user import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """创建新用户"""
    service = UserService(db)
    
    # 检查用户名是否存在
    if await service.get_by_username(user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    # 检查邮箱是否存在
    if await service.get_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    
    return await service.create(user_create)


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """获取当前用户信息"""
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """更新当前用户信息"""
    service = UserService(db)
    return await service.update(current_user, user_update)


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """获取用户信息"""
    service = UserService(db)
    user = await service.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user
```

---

## 3. 数据处理管道模板

### 3.1 Polars ETL 管道

```python
"""Polars ETL 数据管道"""
import polars as pl
from pathlib import Path
from datetime import datetime
import structlog

logger = structlog.get_logger()


class DataPipeline:
    """数据处理管道"""
    
    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
    
    def extract(self) -> pl.LazyFrame:
        """提取数据 (懒加载)"""
        logger.info("extracting_data", path=str(self.input_path))
        
        # 懒加载 CSV (不立即读取到内存)
        df = pl.scan_csv(
            self.input_path,
            try_parse_dates=True,
            null_values=["NA", "NULL", ""],
        )
        
        logger.info("data_extracted", rows=df.select(pl.len()).collect().item())
        return df
    
    def transform(self, df: pl.LazyFrame) -> pl.LazyFrame:
        """转换数据"""
        logger.info("transforming_data")
        
        # 链式转换
        df_transformed = (
            df
            # 1. 过滤无效数据
            .filter(
                (pl.col("age") > 0) & 
                (pl.col("age") < 120) &
                pl.col("email").is_not_null()
            )
            # 2. 数据清洗
            .with_columns([
                pl.col("email").str.to_lowercase().alias("email"),
                pl.col("name").str.strip_chars().alias("name"),
            ])
            # 3. 特征工程
            .with_columns([
                (pl.col("age") // 10 * 10).alias("age_group"),
                pl.when(pl.col("age") >= 18)
                  .then(True)
                  .otherwise(False)
                  .alias("is_adult"),
            ])
            # 4. 聚合统计
            .group_by("age_group")
            .agg([
                pl.col("user_id").count().alias("count"),
                pl.col("age").mean().alias("avg_age"),
                pl.col("email").n_unique().alias("unique_emails"),
            ])
            # 5. 排序
            .sort("age_group")
        )
        
        logger.info("data_transformed")
        return df_transformed
    
    def load(self, df: pl.LazyFrame) -> None:
        """加载数据"""
        logger.info("loading_data", path=str(self.output_path))
        
        # 收集并写入 (支持多种格式)
        df_collected = df.collect()
        
        # 写入 Parquet (推荐, 高效压缩)
        df_collected.write_parquet(
            self.output_path / "output.parquet",
            compression="zstd",  # 高压缩比
        )
        
        # 写入 CSV (可选)
        df_collected.write_csv(self.output_path / "output.csv")
        
        logger.info("data_loaded", rows=df_collected.height)
    
    def run(self) -> None:
        """运行完整管道"""
        start_time = datetime.now()
        logger.info("pipeline_started")
        
        try:
            # ETL 流程
            df = self.extract()
            df = self.transform(df)
            self.load(df)
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info("pipeline_completed", duration=f"{duration:.2f}s")
            
        except Exception as e:
            logger.error("pipeline_failed", error=str(e))
            raise


# 使用示例
if __name__ == "__main__":
    pipeline = DataPipeline(
        input_path=Path("data/input.csv"),
        output_path=Path("data/output/"),
    )
    pipeline.run()
```

---

## 4. AI/RAG 应用模板

### 4.1 LangChain RAG 系统

```python
"""LangChain RAG 系统"""
from pathlib import Path
from typing import List

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.prompts import PromptTemplate
import qdrant_client
import structlog

logger = structlog.get_logger()


class RAGSystem:
    """RAG 检索增强生成系统"""
    
    def __init__(
        self,
        docs_path: Path,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "docs",
        model: str = "gpt-4",
    ):
        self.docs_path = docs_path
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.model = model
        
        # 初始化组件
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.vectorstore = None
        self.qa_chain = None
    
    def load_documents(self) -> List:
        """加载文档"""
        logger.info("loading_documents", path=str(self.docs_path))
        
        loader = DirectoryLoader(
            str(self.docs_path),
            glob="**/*.md",
            show_progress=True,
        )
        documents = loader.load()
        
        logger.info("documents_loaded", count=len(documents))
        return documents
    
    def split_documents(self, documents: List) -> List:
        """分割文档"""
        logger.info("splitting_documents")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        texts = text_splitter.split_documents(documents)
        
        logger.info("documents_split", chunks=len(texts))
        return texts
    
    def create_vectorstore(self, texts: List) -> None:
        """创建向量存储"""
        logger.info("creating_vectorstore")
        
        client = qdrant_client.QdrantClient(url=self.qdrant_url)
        
        self.vectorstore = Qdrant.from_documents(
            texts,
            self.embeddings,
            url=self.qdrant_url,
            collection_name=self.collection_name,
            force_recreate=True,
        )
        
        logger.info("vectorstore_created")
    
    def create_qa_chain(self) -> None:
        """创建问答链"""
        logger.info("creating_qa_chain")
        
        # 自定义提示词
        prompt_template = """使用以下上下文回答问题。如果你不知道答案,就说不知道,不要试图编造答案。

上下文: {context}

问题: {question}

回答:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"],
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # 检索 top-3
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT},
        )
        
        logger.info("qa_chain_created")
    
    def setup(self) -> None:
        """设置 RAG 系统"""
        logger.info("setting_up_rag")
        
        # 加载并处理文档
        documents = self.load_documents()
        texts = self.split_documents(documents)
        
        # 创建向量存储
        self.create_vectorstore(texts)
        
        # 创建问答链
        self.create_qa_chain()
        
        logger.info("rag_setup_completed")
    
    def query(self, question: str) -> dict:
        """查询问题"""
        if not self.qa_chain:
            raise RuntimeError("RAG system not initialized. Call setup() first.")
        
        logger.info("querying", question=question)
        
        result = self.qa_chain({"query": question})
        
        logger.info(
            "query_completed",
            answer_length=len(result["result"]),
            sources=len(result["source_documents"]),
        )
        
        return {
            "answer": result["result"],
            "sources": [
                {
                    "content": doc.page_content[:200],
                    "metadata": doc.metadata,
                }
                for doc in result["source_documents"]
            ],
        }


# FastAPI 集成
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="RAG API")

# 全局 RAG 实例
rag = RAGSystem(docs_path=Path("docs/"))


@app.on_event("startup")
async def startup_event():
    """启动时初始化 RAG"""
    rag.setup()


class QueryRequest(BaseModel):
    """查询请求"""
    question: str


class QueryResponse(BaseModel):
    """查询响应"""
    answer: str
    sources: List[dict]


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """查询接口"""
    try:
        result = rag.query(request.question)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

**文档太长,分为两部分。下一部分继续...**

**当前进度**: ✅ 60%  
**剩余内容**: CI/CD、Docker、监控配置模板
