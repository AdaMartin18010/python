# httpx 现代HTTP客户端

**下一代HTTP客户端**

---

## 📋 概述

httpx是现代化的HTTP客户端，支持同步和异步，API类似requests但功能更强大。

### 核心特性

- 🔄 **同步/异步** - 统一的API
- 📡 **HTTP/2** - 原生支持
- ⚡ **高性能** - 连接池和持久连接
- 🎯 **类型提示** - 完整的类型注解

---

## 🚀 快速开始

### 安装

```bash
uv add httpx
```

### 同步使用

```python
import httpx

# GET请求
response = httpx.get('https://api.example.com/users')
print(response.json())

# POST请求
response = httpx.post('https://api.example.com/users', json={
    'name': 'Alice',
    'email': 'alice@example.com'
})
```

### 异步使用

```python
import httpx
import asyncio

async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.example.com/users')
        return response.json()

users = asyncio.run(fetch_users())
```

---

## 💻 核心功能

### 客户端会话

```python
# 同步
with httpx.Client() as client:
    r1 = client.get('https://example.com')
    r2 = client.get('https://example.org')

# 异步
async with httpx.AsyncClient() as client:
    r1 = await client.get('https://example.com')
    r2 = await client.get('https://example.org')
```

### 超时配置

```python
timeout = httpx.Timeout(10.0, connect=5.0)
response = httpx.get('https://example.com', timeout=timeout)
```

### 重试和错误处理

```python
from httpx import HTTPStatusError

try:
    response = httpx.get('https://api.example.com/data')
    response.raise_for_status()
except HTTPStatusError as exc:
    print(f"Error: {exc.response.status_code}")
```

---

## 🔄 HTTP/2支持

```python
# HTTP/2自动启用
async with httpx.AsyncClient(http2=True) as client:
    response = await client.get('https://http2.example.com')
    print(f"HTTP Version: {response.http_version}")
```

---

## 📚 最佳实践

### 连接池

```python
limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
async with httpx.AsyncClient(limits=limits) as client:
    # 自动管理连接池
    responses = await asyncio.gather(*[
        client.get(f'https://api.example.com/item/{i}')
        for i in range(100)
    ])
```

### 流式响应

```python
async with httpx.AsyncClient() as client:
    async with client.stream('GET', 'https://example.com/large-file') as response:
        async for chunk in response.aiter_bytes():
            process_chunk(chunk)
```

---

## 🆚 vs requests

| 特性 | httpx | requests |
|------|-------|----------|
| 异步 | ✅ | ❌ |
| HTTP/2 | ✅ | ❌ |
| 类型提示 | ✅ | ❌ |
| API相似性 | 高 | - |

---

## 🔗 相关资源

- [官方文档](https://www.python-httpx.org/)
- [GitHub](https://github.com/encode/httpx)

---

**最后更新**: 2025年10月28日

