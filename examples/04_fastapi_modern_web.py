"""
FastAPI 2025现代Web开发实战
演示最新最佳实践
"""

from typing import Annotated
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

# FastAPI 相关
from fastapi import FastAPI, HTTPException, Depends, Query, Path, Body, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr

# ============================================================================
# 1. Pydantic V2 模型 (2025标准)
# ============================================================================


class UserBase(BaseModel):
    """用户基础模型 - Pydantic V2"""

    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自动去空格
        validate_assignment=True,  # 赋值时验证
        use_enum_values=True,  # 使用枚举值
        from_attributes=True,  # ORM模式
    )

    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    full_name: str | None = Field(None, max_length=100)
    age: int | None = Field(None, ge=0, le=150)

    @field_validator("username")
    @classmethod
    def username_must_be_valid(cls, v: str) -> str:
        """用户名验证"""
        if v.lower() in ["admin", "root", "system"]:
            raise ValueError("Reserved username")
        return v


class UserCreate(UserBase):
    """创建用户模型"""

    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """用户响应模型"""

    id: int
    is_active: bool = True
    created_at: str  # 简化为字符串,实际应使用 datetime


class UserUpdate(BaseModel):
    """更新用户模型 - 所有字段可选"""

    model_config = ConfigDict(str_strip_whitespace=True)

    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    age: int | None = Field(None, ge=0, le=150)


# ============================================================================
# 2. 依赖注入 (Dependency Injection)
# ============================================================================


async def get_current_user() -> UserResponse:
    """获取当前用户 - 依赖注入"""
    # 实际应该从token获取
    return UserResponse(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at="2025-01-01T00:00:00",
    )


async def get_db() -> AsyncIterator[dict]:
    """数据库连接 - 异步生成器依赖"""
    db = {"connected": True}  # 模拟数据库
    try:
        yield db
    finally:
        # 清理资源
        db["connected"] = False


# 类型化依赖 (Python 3.12+)
CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
Database = Annotated[dict, Depends(get_db)]


# ============================================================================
# 3. 生命周期管理 (Lifespan)
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """应用生命周期管理"""
    # 启动时执行
    print("🚀 Application startup")
    # 这里可以初始化数据库连接池、缓存等

    yield  # 应用运行期间

    # 关闭时执行
    print("🛑 Application shutdown")
    # 这里可以关闭数据库连接、清理资源等


# ============================================================================
# 4. FastAPI 应用实例
# ============================================================================

app = FastAPI(
    title="Modern FastAPI App 2025",
    description="基于 FastAPI 0.115+ 的现代 Web API",
    version="1.0.0",
    lifespan=lifespan,  # 使用生命周期管理
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)


# ============================================================================
# 5. 路由和端点
# ============================================================================


@app.get("/")
async def root() -> dict[str, str]:
    """根路径"""
    return {"message": "Welcome to Modern FastAPI 2025"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """健康检查"""
    return {"status": "healthy", "version": "1.0.0"}


# ============================================================================
# 6. 用户 CRUD API
# ============================================================================

# 模拟数据库
fake_users_db: dict[int, UserResponse] = {
    1: UserResponse(
        id=1,
        username="alice",
        email="alice@example.com",
        full_name="Alice Smith",
        age=30,
        created_at="2025-01-01T00:00:00",
    ),
    2: UserResponse(
        id=2,
        username="bob",
        email="bob@example.com",
        full_name="Bob Johnson",
        age=25,
        created_at="2025-01-02T00:00:00",
    ),
}


@app.get("/users", response_model=list[UserResponse], tags=["users"])
async def list_users(
    skip: Annotated[int, Query(ge=0, description="跳过的记录数")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="返回的记录数")] = 10,
    current_user: CurrentUser = None,
) -> list[UserResponse]:
    """获取用户列表"""
    users = list(fake_users_db.values())
    return users[skip : skip + limit]


@app.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(
    user_id: Annotated[int, Path(gt=0, description="用户ID")],
    db: Database = None,
) -> UserResponse:
    """获取单个用户"""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
        )
    return fake_users_db[user_id]


@app.post(
    "/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["users"]
)
async def create_user(
    user: Annotated[UserCreate, Body(description="用户信息")],
    current_user: CurrentUser = None,
) -> UserResponse:
    """创建用户"""
    # 检查用户名是否已存在
    for existing_user in fake_users_db.values():
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
            )

    # 创建新用户
    new_id = max(fake_users_db.keys()) + 1 if fake_users_db else 1
    new_user = UserResponse(
        id=new_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        age=user.age,
        created_at="2025-10-25T00:00:00",  # 应该用实际时间
    )

    fake_users_db[new_id] = new_user
    return new_user


@app.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(
    user_id: Annotated[int, Path(gt=0)],
    user_update: UserUpdate,
    current_user: CurrentUser = None,
) -> UserResponse:
    """更新用户"""
    if user_id not in fake_users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    existing_user = fake_users_db[user_id]

    # 只更新提供的字段
    update_data = user_update.model_dump(exclude_unset=True)
    updated_user = existing_user.model_copy(update=update_data)

    fake_users_db[user_id] = updated_user
    return updated_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(
    user_id: Annotated[int, Path(gt=0)], current_user: CurrentUser = None
) -> None:
    """删除用户"""
    if user_id not in fake_users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    del fake_users_db[user_id]


# ============================================================================
# 7. 错误处理
# ============================================================================


@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError) -> JSONResponse:
    """自定义错误处理"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


# ============================================================================
# 8. 中间件示例
# ============================================================================


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """添加处理时间header"""
    import time

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ============================================================================
# 主程序
# ============================================================================


if __name__ == "__main__":
    print("=" * 70)
    print("FastAPI 2025 现代Web开发实战")
    print("=" * 70)
    print("\n📖 API 文档: http://localhost:8000/docs")
    print("📖 ReDoc:    http://localhost:8000/redoc")
    print("\n启动服务器:")
    print("  uvicorn examples.04_fastapi_modern_web:app --reload")
    print("=" * 70)

