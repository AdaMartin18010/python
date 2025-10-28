# API设计最佳实践

**RESTful API设计指南**

---

## 📋 设计原则

### REST原则

1. **资源导向** - URL代表资源
2. **无状态** - 每个请求独立
3. **统一接口** - 标准HTTP方法
4. **可缓存** - 支持HTTP缓存
5. **分层系统** - 客户端不知道中间层

---

## 🎯 URL设计

### 资源命名

```python
# ✅ 好 - 使用复数名词
GET  /users           # 获取用户列表
GET  /users/123       # 获取单个用户
POST /users           # 创建用户
PUT  /users/123       # 更新用户
DELETE /users/123     # 删除用户

# ❌ 差 - 使用动词
GET  /getUsers
POST /createUser
PUT  /updateUser
```

### 嵌套资源

```python
# ✅ 好 - 表达资源关系
GET  /users/123/posts          # 用户的文章
GET  /users/123/posts/456      # 用户的某篇文章
POST /users/123/posts          # 创建文章

# ⚠️ 避免过深嵌套（最多2-3层）
GET  /users/123/posts/456/comments/789/replies
# 可以简化为：
GET  /comments/789/replies
```

---

## 🔤 HTTP方法

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str

users_db: dict[int, User] = {}

# GET - 获取资源
@app.get("/users", response_model=List[User])
async def list_users():
    """获取用户列表"""
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """获取单个用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# POST - 创建资源
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """创建用户"""
    user.id = len(users_db) + 1
    users_db[user.id] = user
    return user

# PUT - 完整更新
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    """完整更新用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user.id = user_id
    users_db[user_id] = user
    return user

# PATCH - 部分更新
@app.patch("/users/{user_id}", response_model=User)
async def partial_update_user(user_id: int, updates: dict):
    """部分更新用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    for key, value in updates.items():
        setattr(user, key, value)
    
    return user

# DELETE - 删除资源
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """删除用户"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
```

---

## 📊 状态码规范

```python
from fastapi import status

# 2xx 成功
200  # OK - 请求成功
201  # Created - 资源创建成功
204  # No Content - 成功但无返回内容

# 3xx 重定向
301  # Moved Permanently - 永久重定向
302  # Found - 临时重定向

# 4xx 客户端错误
400  # Bad Request - 请求错误
401  # Unauthorized - 未认证
403  # Forbidden - 无权限
404  # Not Found - 资源不存在
409  # Conflict - 资源冲突
422  # Unprocessable Entity - 验证失败
429  # Too Many Requests - 请求过多

# 5xx 服务器错误
500  # Internal Server Error - 服务器错误
502  # Bad Gateway - 网关错误
503  # Service Unavailable - 服务不可用
```

---

## 🔍 查询和过滤

```python
from fastapi import Query
from typing import Optional

@app.get("/users")
async def list_users(
    # 分页
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    
    # 过滤
    name: Optional[str] = Query(None, description="按名字过滤"),
    email: Optional[str] = Query(None, description="按邮箱过滤"),
    is_active: Optional[bool] = Query(None, description="按状态过滤"),
    
    # 排序
    sort_by: str = Query("id", description="排序字段"),
    order: str = Query("asc", regex="^(asc|desc)$", description="排序顺序"),
    
    # 字段选择
    fields: Optional[str] = Query(None, description="返回字段，逗号分隔")
):
    """
    获取用户列表
    
    示例:
    - GET /users?page=1&page_size=20
    - GET /users?name=Alice&is_active=true
    - GET /users?sort_by=created_at&order=desc
    - GET /users?fields=id,name,email
    """
    # 实现查询逻辑
    pass
```

---

## 📦 响应格式

### 成功响应

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    items: List[T]
    total: int
    page: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size

@app.get("/users", response_model=PaginatedResponse[User])
async def list_users(page: int = 1, page_size: int = 20):
    # 查询数据
    items = get_users_from_db(page, page_size)
    total = count_users_in_db()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )

# 响应示例：
# {
#   "items": [{"id": 1, "name": "Alice"}, ...],
#   "total": 100,
#   "page": 1,
#   "page_size": 20,
#   "total_pages": 5
# }
```

### 错误响应

```python
class ErrorResponse(BaseModel):
    """错误响应"""
    error: str
    message: str
    details: Optional[dict] = None

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.status_code,
            message=exc.detail,
            details=getattr(exc, 'details', None)
        ).dict()
    )

# 错误响应示例：
# {
#   "error": 404,
#   "message": "User not found",
#   "details": {"user_id": 123}
# }
```

---

## 🔒 认证和授权

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

async def require_admin(user: User = Depends(get_current_user)):
    """要求管理员权限"""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    return user

# 使用
@app.post("/users", dependencies=[Depends(require_admin)])
async def create_user(user: User):
    """创建用户（需要管理员权限）"""
    return user
```

---

## 📈 版本控制

### URL版本

```python
from fastapi import APIRouter

# v1
v1_router = APIRouter(prefix="/v1")

@v1_router.get("/users")
async def list_users_v1():
    return {"version": "v1"}

# v2
v2_router = APIRouter(prefix="/v2")

@v2_router.get("/users")
async def list_users_v2():
    return {"version": "v2", "users": []}

app.include_router(v1_router)
app.include_router(v2_router)
```

### Header版本

```python
from fastapi import Header

@app.get("/users")
async def list_users(api_version: str = Header("1.0")):
    if api_version == "2.0":
        return {"version": "2.0"}
    return {"version": "1.0"}
```

---

## ⚡ 性能优化

### 1. 响应压缩

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 2. 缓存

```python
from fastapi import Response

@app.get("/users/{user_id}")
async def get_user(user_id: int, response: Response):
    user = get_user_from_db(user_id)
    
    # 设置缓存头
    response.headers["Cache-Control"] = "public, max-age=300"
    response.headers["ETag"] = f'"{user.updated_at.timestamp()}"'
    
    return user
```

### 3. 限流

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.get("/users")
@limiter.limit("10/minute")
async def list_users(request: Request):
    return []
```

---

## 📚 文档最佳实践

```python
@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="创建新用户",
    description="创建一个新用户账号",
    response_description="创建成功的用户对象",
    responses={
        201: {"description": "用户创建成功"},
        400: {"description": "请求参数错误"},
        409: {"description": "用户已存在"}
    }
)
async def create_user(user: User):
    """
    创建新用户：
    
    - **name**: 用户名（必填）
    - **email**: 邮箱地址（必填，唯一）
    - **password**: 密码（必填，至少8个字符）
    """
    return user
```

---

## 🔗 相关资源

- [REST API设计规范](https://restfulapi.net/)
- [HTTP状态码](https://httpstatuses.com/)

---

**最后更新**: 2025年10月28日

