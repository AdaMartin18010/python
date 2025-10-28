# aiohttp 异步HTTP

**异步HTTP客户端/服务器框架**

---

## 📋 概述

aiohttp是功能完整的异步HTTP客户端/服务器框架，基于asyncio。

### 核心特性

- 🔄 **客户端/服务器** - 两者都支持
- ⚡ **异步** - 完全异步实现
- 🌐 **WebSocket** - 内置支持
- 📡 **HTTP/2** - 支持最新协议

---

## 🚀 快速开始

### 安装

```bash
uv add aiohttp
```

### HTTP客户端

```python
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    html = await fetch('https://example.com')
    print(html)

asyncio.run(main())
```

### HTTP服务器

```python
from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "World")
    return web.Response(text=f"Hello, {name}!")

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

web.run_app(app, port=8080)
```

---

## 💻 客户端功能

### 并发请求

```python
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.text() for r in responses]

urls = ['https://example.com', 'https://example.org']
results = await fetch_all(urls)
```

### POST请求

```python
async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

result = await post_data('https://api.example.com', {'key': 'value'})
```

### 超时和重试

```python
timeout = aiohttp.ClientTimeout(total=30)
async with aiohttp.ClientSession(timeout=timeout) as session:
    async with session.get(url) as response:
        return await response.text()
```

---

## 🌐 服务器功能

### 路由

```python
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
async def home(request):
    return web.json_response({'message': 'Home'})

@routes.post('/users')
async def create_user(request):
    data = await request.json()
    return web.json_response({'user': data}, status=201)

app = web.Application()
app.add_routes(routes)
```

### 中间件

```python
@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except Exception as ex:
        return web.json_response({'error': str(ex)}, status=500)

app = web.Application(middlewares=[error_middleware])
```

### WebSocket

```python
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            await ws.send_str(f"Echo: {msg.data}")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break
    
    return ws

app.add_routes([web.get('/ws', websocket_handler)])
```

---

## 📚 最佳实践

### 会话重用

```python
# ✅ 好 - 重用session
async with aiohttp.ClientSession() as session:
    for url in urls:
        async with session.get(url) as response:
            data = await response.text()

# ❌ 差 - 每次创建新session
for url in urls:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
```

---

## 🔗 相关资源

- [官方文档](https://docs.aiohttp.org/)
- [GitHub](https://github.com/aio-libs/aiohttp)

---

**最后更新**: 2025年10月28日

