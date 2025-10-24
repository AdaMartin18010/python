# 05-Web开发（2025年10月标准）

聚焦现代 Python Web：FastAPI、Django 5.1、ASGI、异步优先与生产部署。

## 0. 2025年Web开发技术栈

### 0.1 框架选择（2025推荐）

| 框架 | 版本 | 类型 | 性能 | 适用场景 | 推荐度 |
|------|------|------|------|----------|--------|
| **FastAPI** | 0.115+ | 异步API | 极高 | 微服务、API | ⭐⭐⭐⭐⭐ |
| **Django** | 5.1+ | 全栈 | 高 | 企业应用、CMS | ⭐⭐⭐⭐⭐ |
| **Litestar** | 2.0+ | 异步API | 极高 | 高性能API | ⭐⭐⭐⭐ |
| **Flask** | 3.0+ | 同步Web | 中 | 简单应用 | ⭐⭐⭐ |

### 0.2 技术栈组合（2025标准）

**现代API技术栈：**

```text
FastAPI 0.115+ (Web框架)
├── Pydantic 2.9+ (数据验证)
├── SQLAlchemy 2.0+ (ORM)
├── Alembic 1.13+ (数据库迁移)
├── uvicorn 0.30+ (ASGI服务器)
├── httpx 0.27+ (HTTP客户端)
├── Redis 5.0+ (缓存)
└── PostgreSQL 16+ (数据库)
```

**企业级Web技术栈：**

```text
Django 5.1+ (Web框架)
├── Django REST framework 3.15+ (API)
├── Celery 5.4+ (任务队列)
├── Channels 4.1+ (WebSocket)
├── PostgreSQL 16+ (数据库)
└── Redis 5.0+ (缓存/Celery broker)
```

### 0.3 性能对比（2025实测）

| 框架 | RPS (请求/秒) | 延迟 (P95) | 内存占用 |
|------|-------------|-----------|---------|
| FastAPI (异步) | 15,000 | 15ms | 120MB |
| Django 5.1 (异步) | 12,000 | 20ms | 180MB |
| Flask (同步) | 3,000 | 80ms | 100MB |

## 1. FastAPI 完整指南（2025最佳实践）

### 1.1 现代FastAPI应用结构

```python
# FastAPI 2025标准项目结构
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional
from datetime import datetime
import asyncio

app = FastAPI(
    title="Modern API 2025",
    description="FastAPI with all 2025 best practices",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# 数据模型（Pydantic 2.x）
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    
    model_config = {"json_schema_extra": {
        "examples": [{
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }]
    }}

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

# 依赖注入
async def get_db():
    """数据库会话依赖"""
    db = AsyncSession()
    try:
        yield db
    finally:
        await db.close()

# 路由处理器
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """创建用户（异步 + 后台任务）"""
    # 创建用户
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # 添加后台任务
    background_tasks.add_task(send_welcome_email, user.email)
    
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """获取用户"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### 1.2 ASGI 协议与服务器

**ASGI（Asynchronous Server Gateway Interface）**是Python异步Web应用的标准接口。

**推荐服务器：**

- **uvicorn** - 最流行，性能优秀
- **hypercorn** - 支持HTTP/2和HTTP/3
- **daphne** - Django官方支持

```bash
# uvicorn 生产配置（2025推荐）
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --loop uvloop \
    --http h11 \
    --timeout-keep-alive 30 \
    --access-log \
    --log-level info
```

## 2. 路由与依赖注入

- 路由/请求体/响应模型（pydantic）
- 依赖注入与生命周期

## 3. 中间件与安全

- 身份验证、授权、CORS、速率限制

## 4. 部署与运维

- 进程管理（uvicorn workers）
- 容器化与反向代理（Nginx/Caddy）

### 4.1 性能与部署建议（最小集合）

- 服务器：`uvicorn --workers (CPU核数) --loop uvloop --http h11`（如可用）
- 超时与连接：配置 `--timeout-keep-alive`，前置反代设置连接复用与压缩
- 观察性：启用结构化日志、请求ID、中间件级别的计时
- 压测基线：`wrk`/`bombardier` 对 `/health` 与典型业务路由进行RPS与P95
- 容器化：基于 `python:3.12-slim`，多阶段构建 + `uv` 同步依赖 + 非root用户

### 4.2 示例 Dockerfile 片段（简化）

```Dockerfile
FROM python:3.12-slim AS base
RUN pip install --no-cache-dir uv && useradd -m app
WORKDIR /app
COPY pyproject.toml .
RUN uv pip compile pyproject.toml -o uv.lock && uv pip sync uv.lock
COPY . .
USER app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 5. 示例（最小）

- 位置：`./examples/fastapi_min/app.py`
- 运行：`uvicorn app:app --reload --port 8000`
- 健康检查：`GET http://127.0.0.1:8000/health`
- 测试建议：使用 `httpx`/`pytest` 进行集成测试

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)
- 相关主题：
  - [01-语言与生态/README](../01-语言与生态/README.md)
  - [02-测试与质量/README](../02-测试与质量/README.md)
  - [03-工程与交付/README](../03-工程与交付/README.md)
  - [04-并发与异步/README](../04-并发与异步/README.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)
- 相关规范：[重构规范](../99-上下文与流程/03-重构规范.md)

## 来源与回链（docs → python）

- Web开发来源：`docs/python_ecosystem/08-Web开发/` → 本地：[迁移/现代Web框架](./迁移/现代Web框架.md)
- API设计来源：`docs/refactor/04-行业领域/04-01-Web开发/` → 本地：[API_接口规范.md](./API_接口规范.md)
