# OpenAPI 规范与文档

**API设计与文档标准**

---

## 📋 概述

OpenAPI (原Swagger) 是RESTful API的行业标准规范，用于描述、生成和可视化API。

### 核心特性

- 📝 **标准化** - 统一的API描述格式
- 🔄 **自动生成** - 从代码生成文档
- 🎨 **可视化** - Swagger UI交互界面
- 🔧 **代码生成** - 自动生成客户端SDK

---

## 🚀 FastAPI集成

### 自动生成OpenAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="我的API",
    description="这是一个示例API",
    version="1.0.0",
    openapi_tags=[
        {"name": "users", "description": "用户操作"},
        {"name": "items", "description": "商品操作"}
    ]
)

class User(BaseModel):
    """用户模型"""
    id: int
    name: str
    email: str

@app.post("/users/", tags=["users"], response_model=User)
async def create_user(user: User):
    """
    创建新用户
    
    - **id**: 用户ID
    - **name**: 用户名
    - **email**: 邮箱地址
    """
    return user

@app.get("/users/{user_id}", tags=["users"])
async def get_user(user_id: int):
    """根据ID获取用户"""
    return {"id": user_id, "name": "Alice"}

# 访问文档
# http://localhost:8000/docs  (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
# http://localhost:8000/openapi.json (OpenAPI JSON)
```

---

## 📝 OpenAPI规范

### 基本结构

```yaml
openapi: 3.1.0
info:
  title: 我的API
  description: API描述
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: 生产环境
  - url: https://staging.api.example.com/v1
    description: 测试环境

paths:
  /users:
    get:
      summary: 获取用户列表
      tags:
        - users
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    
    post:
      summary: 创建用户
      tags:
        - users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      responses:
        '201':
          description: 创建成功
        '400':
          description: 请求错误

components:
  schemas:
    User:
      type: object
      required:
        - name
        - email
      properties:
        id:
          type: integer
          example: 1
        name:
          type: string
          example: "Alice"
        email:
          type: string
          format: email
          example: "alice@example.com"
  
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## 🎨 自定义文档

### 添加示例

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., example=1, description="用户ID")
    name: str = Field(..., example="Alice", description="用户名")
    email: str = Field(..., example="alice@example.com", description="邮箱")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com"
            }
        }

@app.post("/users/", response_model=User)
async def create_user(user: User):
    """创建用户"""
    return user
```

### 添加响应示例

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

@app.get(
    "/users/{user_id}",
    responses={
        200: {
            "description": "成功获取用户",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "Alice"}
                }
            }
        },
        404: {
            "description": "用户不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
async def get_user(user_id: int):
    return {"id": user_id, "name": "Alice"}
```

---

## 🔧 高级配置

### 自定义Swagger UI

```python
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
```

### 自定义OpenAPI Schema

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Custom API",
        version="2.5.0",
        description="This is a custom OpenAPI schema",
        routes=app.routes,
    )
    
    # 添加自定义内容
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

---

## 🔒 安全定义

### JWT Bearer认证

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

app = FastAPI()

@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """受保护的路由"""
    token = credentials.credentials
    # 验证token
    return {"message": "Success"}
```

### OAuth2

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

---

## 📚 使用Spectral验证

```bash
# 安装Spectral
npm install -g @stoplight/spectral-cli

# 验证OpenAPI规范
spectral lint openapi.yaml
```

```yaml
# .spectral.yaml
extends: spectral:oas
rules:
  operation-description: error
  operation-tags: error
  info-contact: error
  info-description: error
```

---

## 🔄 从OpenAPI生成代码

### 生成Python客户端

```bash
# 使用openapi-generator
pip install openapi-generator-cli

openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./client
```

### 使用生成的客户端

```python
from client import ApiClient, Configuration, UsersApi

config = Configuration()
config.host = "https://api.example.com"

with ApiClient(config) as api_client:
    api = UsersApi(api_client)
    users = api.list_users()
```

---

## 📊 最佳实践

### 1. 版本控制

```python
from fastapi import FastAPI

app_v1 = FastAPI()
app_v2 = FastAPI()

@app_v1.get("/users")
async def get_users_v1():
    return {"version": "v1"}

@app_v2.get("/users")
async def get_users_v2():
    return {"version": "v2"}

# 主应用
app = FastAPI()
app.mount("/v1", app_v1)
app.mount("/v2", app_v2)
```

### 2. 分组路由

```python
from fastapi import APIRouter

users_router = APIRouter(prefix="/users", tags=["users"])
items_router = APIRouter(prefix="/items", tags=["items"])

@users_router.get("/")
async def list_users():
    return []

@items_router.get("/")
async def list_items():
    return []

app.include_router(users_router)
app.include_router(items_router)
```

### 3. 错误响应

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    获取用户
    
    Raises:
        HTTPException: 用户不存在时返回404
    """
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]
```

---

## 🔗 相关资源

- [OpenAPI规范](https://spec.openapis.org/oas/latest.html)
- [Swagger Editor](https://editor.swagger.io/)
- [FastAPI文档](https://fastapi.tiangolo.com/)

---

**最后更新**: 2025年10月28日

