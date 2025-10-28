# Starlette ASGI框架

**轻量级高性能ASGI框架**

---

## 📋 概述

Starlette是一个轻量级的ASGI框架，FastAPI的底层框架。

### 核心特性

- ⚡ **高性能** - 异步原生支持
- 🪶 **轻量级** - 核心简洁
- 🔌 **ASGI** - 异步服务器网关接口
- 🎯 **灵活** - 可作为基础框架

---

## 🚀 快速开始

### 安装

```bash
uv add starlette uvicorn
```

### Hello World

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({'hello': 'world'})

app = Starlette(routes=[
    Route('/', homepage),
])
```

---

## 💻 核心功能

### 路由

```python
from starlette.routing import Route, Mount
from starlette.responses import PlainTextResponse

async def homepage(request):
    return PlainTextResponse('Hello, world!')

async def user_detail(request):
    user_id = request.path_params['user_id']
    return PlainTextResponse(f'User {user_id}')

routes = [
    Route('/', homepage),
    Route('/users/{user_id:int}', user_detail),
]

app = Starlette(routes=routes)
```

### 中间件

```python
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app = Starlette(routes=routes, middleware=middleware)
```

### WebSocket

```python
from starlette.websockets import WebSocket

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")

routes = [
    Route('/ws', websocket_endpoint, methods=['GET']),
]
```

---

## 📚 最佳实践

### 依赖注入

```python
from starlette.requests import Request

async def get_db(request: Request):
    return request.app.state.db

async def endpoint(request: Request):
    db = await get_db(request)
    users = await db.fetch_all("SELECT * FROM users")
    return JSONResponse([dict(u) for u in users])
```

---

## 🔗 相关资源

- [官方文档](https://www.starlette.io/)
- [GitHub](https://github.com/encode/starlette)

---

**最后更新**: 2025年10月28日

