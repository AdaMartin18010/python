from fastapi import FastAPI, HTTPException, Request, Depends, Security, BackgroundTasks, Query
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .routers import router as v1_router
from .db import init_db, get_session, User
from .settings import get_settings
from .scheduler import get_scheduler, add_interval_job, list_jobs
from .jwt_auth import create_token, verify_token
from .metrics import prometheus_middleware, metrics_endpoint

app = FastAPI(
    title="FastAPI Minimal",
    version="0.5.0",
    description="最小可运行示例，涵盖配置/DB/安全/分页/任务/调度/OpenAPI/指标/安全加固",
    openapi_tags=[
        {"name": "core", "description": "核心与健康检查"},
        {"name": "items", "description": "示例资源：物品"},
        {"name": "users", "description": "用户管理（分页示例）"},
        {"name": "security", "description": "API Key 与 Bearer（JWT）"},
        {"name": "tasks", "description": "后台任务"},
        {"name": "jobs", "description": "APScheduler 调度"},
        {"name": "metrics", "description": "Prometheus 指标"},
    ],
)

# CORS（示例：仅本地与受信域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"]
    ,
    allow_headers=["*"]
)

# 审计日志与请求体大小限制
MAX_BODY = 1 * 1024 * 1024  # 1MB


@app.middleware("http")
async def audit_and_limit_middleware(request: Request, call_next):
    # 简要审计（方法、路径、远端）
    # 可替换为结构化日志
    if request.headers.get("content-length") and int(request.headers["content-length"]) > MAX_BODY:
        return JSONResponse(status_code=413, content={"detail": "request body too large"})
    response = await call_next(request)
    return response

app.middleware("http")(prometheus_middleware)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
http_bearer = HTTPBearer(auto_error=False)


class ErrorResp(BaseModel):
    detail: str


class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)


class UserIn(BaseModel):
    name: str = Field(min_length=1, max_length=64)


class Page(BaseModel):
    total: int
    items: list[dict[str, object]]


async def get_api_key(key: str | None = Security(api_key_header), settings = Depends(get_settings)) -> str:
    expected = settings.app_name
    if not key or key != expected:
        raise HTTPException(status_code=401, detail="invalid api key")
    return key


async def get_current_user(creds: HTTPAuthorizationCredentials | None = Security(http_bearer), settings = Depends(get_settings)) -> dict:
    if not creds or not creds.credentials:
        raise HTTPException(status_code=401, detail="missing bearer token")
    try:
        payload = verify_token(creds.credentials, settings.app_name)
    except Exception as e:  # jwt exceptions
        raise HTTPException(status_code=401, detail=f"invalid token: {e}")
    return payload


@app.on_event("startup")
async def _on_startup() -> None:
    await init_db()
    get_scheduler()


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=ErrorResp(detail=exc.detail).model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=ErrorResp(detail=str(exc)).model_dump())


@app.get("/metrics", tags=["metrics"])
async def metrics():
    return await metrics_endpoint(None)


@app.get("/health", response_model=dict[str, str], tags=["core"])
def health(settings = Depends(get_settings)) -> dict[str, str]:
    return {"status": "ok", "env": settings.env}


@app.post("/items", responses={400: {"model": ErrorResp}}, tags=["items"])
def create_item(item: Item) -> dict[str, object]:
    if item.price == 0:
        raise HTTPException(status_code=400, detail="price must be > 0")
    return {"ok": True, "item": item.model_dump()}


@app.post("/users", status_code=201, tags=["users"])
async def create_user(payload: UserIn, session: AsyncSession = Depends(get_session)) -> dict[str, object]:
    user = User(name=payload.name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"id": user.id, "name": user.name}


@app.get("/users", response_model=Page, tags=["users"])
async def list_users(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> Page:
    result = await session.execute(select(User))
    rows = result.scalars().all()
    sliced = rows[offset: offset + limit]
    return Page(total=len(rows), items=[{"id": u.id, "name": u.name} for u in sliced])


@app.get("/protected", tags=["security"], responses={401: {"model": ErrorResp}})
async def protected(_: APIKey = Depends(get_api_key)) -> dict[str, str]:
    return {"ok": "secured"}


@app.post("/token", tags=["security"])
async def issue_token(username: str = "alice", settings = Depends(get_settings)) -> dict[str, str]:
    token = create_token({"sub": username}, settings.app_name, expires_minutes=60)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", tags=["security"], responses={401: {"model": ErrorResp}})
async def me(claims: dict = Depends(get_current_user)) -> dict:
    return {"claims": claims}


@app.post("/tasks", tags=["tasks"])
async def run_task(tasks: BackgroundTasks, name: str = "job") -> dict[str, str]:
    tasks.add_task(lambda: None)
    return {"queued": name}


@app.post("/jobs", tags=["jobs"])  # 每 N 秒执行一次
async def add_job(seconds: int = 10, name: str = "world") -> dict[str, str]:
    job_id = add_interval_job(seconds=seconds, name=name)
    return {"job_id": job_id}


@app.get("/jobs", tags=["jobs"])  # 列表当前任务
async def jobs() -> list[dict[str, str]]:
    return list_jobs()


# 路由分组
app.include_router(v1_router)
