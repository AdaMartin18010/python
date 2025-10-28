# 缓存策略与实现

**Python缓存完整指南**

---

## 📋 概述

缓存是提升应用性能的关键技术，通过存储计算结果避免重复计算。

### 缓存层级

```
┌─────────────────────────────┐
│   内存缓存 (最快)            │  functools.lru_cache
├─────────────────────────────┤
│   进程缓存                   │  cachetools
├─────────────────────────────┤
│   分布式缓存                 │  Redis, Memcached
├─────────────────────────────┤
│   CDN缓存                    │  CloudFlare, AWS CloudFront
└─────────────────────────────┘
```

---

## 🚀 内存缓存

### functools.lru_cache

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """斐波那契数列（带缓存）"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 查看缓存信息
print(fibonacci.cache_info())
# CacheInfo(hits=8, misses=10, maxsize=128, currsize=10)

# 清除缓存
fibonacci.cache_clear()
```

### 自定义过期时间

```python
from functools import wraps
import time

def timed_lru_cache(seconds: int, maxsize: int = 128):
    """带过期时间的LRU缓存"""
    def decorator(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = seconds
        func.expiration = time.time() + seconds
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            if time.time() >= func.expiration:
                func.cache_clear()
                func.expiration = time.time() + func.lifetime
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

@timed_lru_cache(seconds=300)  # 5分钟过期
def expensive_operation(x: int) -> int:
    time.sleep(1)
    return x * 2
```

---

## 💾 Cachetools

### 多种缓存策略

```python
from cachetools import TTLCache, LRUCache, LFUCache
import time

# TTL缓存（基于时间）
ttl_cache = TTLCache(maxsize=100, ttl=300)  # 5分钟过期

@cached(ttl_cache)
def get_user(user_id: int):
    return database.query(f"SELECT * FROM users WHERE id = {user_id}")

# LRU缓存（最近最少使用）
lru_cache = LRUCache(maxsize=100)

# LFU缓存（最不经常使用）
lfu_cache = LFUCache(maxsize=100)
```

### 装饰器用法

```python
from cachetools import cached, TTLCache, keys

cache = TTLCache(maxsize=100, ttl=300)

@cached(cache, key=lambda user_id, include_deleted: keys.hashkey(user_id))
def get_user_by_id(user_id: int, include_deleted: bool = False):
    """根据ID获取用户"""
    return database.query(...)
```

---

## 🔴 Redis缓存

### 基本使用

```python
import redis
import json
from typing import Optional

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)
    
    def get(self, key: str) -> Optional[dict]:
        """获取缓存"""
        value = self.client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: dict, ttl: int = 300):
        """设置缓存"""
        self.client.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str):
        """删除缓存"""
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return bool(self.client.exists(key))

# 使用
cache = RedisCache()
cache.set('user:1', {'name': 'Alice', 'email': 'alice@example.com'})
user = cache.get('user:1')
```

### 装饰器模式

```python
from functools import wraps
import hashlib

def redis_cache(ttl: int = 300):
    """Redis缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key_parts = [func.__name__] + [str(arg) for arg in args]
            key = hashlib.md5(':'.join(key_parts).encode()).hexdigest()
            
            # 尝试从缓存获取
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存入缓存
            cache.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator

@redis_cache(ttl=600)
def get_user_profile(user_id: int):
    # 从数据库获取
    return database.get_user(user_id)
```

---

## ⚡ 缓存模式

### 1. Cache-Aside (旁路缓存)

```python
async def get_user(user_id: int):
    # 1. 先查缓存
    cache_key = f'user:{user_id}'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # 2. 缓存未命中，查数据库
    user = await database.get_user(user_id)
    
    # 3. 写入缓存
    await redis.setex(cache_key, 300, json.dumps(user))
    
    return user
```

### 2. Read-Through (读穿透)

```python
class UserRepository:
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database
    
    async def get(self, user_id: int):
        """读取时自动处理缓存"""
        key = f'user:{user_id}'
        
        # 尝试从缓存读取
        user = await self.cache.get(key)
        if user:
            return user
        
        # 从数据库读取
        user = await self.database.get_user(user_id)
        
        # 自动写入缓存
        await self.cache.set(key, user)
        
        return user
```

### 3. Write-Through (写穿透)

```python
class UserRepository:
    async def update(self, user_id: int, data: dict):
        """更新时同时更新缓存"""
        # 1. 更新数据库
        user = await self.database.update_user(user_id, data)
        
        # 2. 更新缓存
        key = f'user:{user_id}'
        await self.cache.set(key, user)
        
        return user
```

### 4. Write-Behind (写回)

```python
import asyncio
from collections import deque

class WriteBehindCache:
    def __init__(self, database):
        self.database = database
        self.write_queue = deque()
        self.cache = {}
        
        # 启动后台写入任务
        asyncio.create_task(self._background_writer())
    
    async def update(self, key: str, value: dict):
        """更新缓存，异步写入数据库"""
        # 立即更新缓存
        self.cache[key] = value
        
        # 添加到写入队列
        self.write_queue.append((key, value))
    
    async def _background_writer(self):
        """后台批量写入数据库"""
        while True:
            await asyncio.sleep(5)  # 每5秒写一次
            
            if self.write_queue:
                # 批量写入
                batch = []
                while self.write_queue:
                    batch.append(self.write_queue.popleft())
                
                await self.database.batch_update(batch)
```

---

## 🎯 FastAPI缓存

### aiocache集成

```python
from fastapi import FastAPI
from aiocache import Cache
from aiocache.decorators import cached

app = FastAPI()
cache = Cache(Cache.REDIS, endpoint="localhost", port=6379)

@app.get("/users/{user_id}")
@cached(ttl=300, key_builder=lambda *args, **kwargs: f"user:{kwargs['user_id']}")
async def get_user(user_id: int):
    # 自动缓存
    user = await database.get_user(user_id)
    return user
```

### 自定义缓存中间件

```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class CacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 只缓存GET请求
        if request.method != "GET":
            return await call_next(request)
        
        # 生成缓存键
        cache_key = f"http:{request.url.path}:{request.query_params}"
        
        # 尝试从缓存获取
        cached_response = await cache.get(cache_key)
        if cached_response:
            return Response(
                content=cached_response,
                media_type="application/json"
            )
        
        # 执行请求
        response = await call_next(request)
        
        # 缓存响应
        if response.status_code == 200:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            await cache.set(cache_key, body, ttl=60)
            return Response(content=body, media_type="application/json")
        
        return response

app.add_middleware(CacheMiddleware)
```

---

## 📊 缓存最佳实践

### 1. 缓存键设计

```python
# ✅ 好 - 清晰的命名空间
cache_key = f"user:profile:{user_id}:v1"

# ❌ 差 - 模糊的键名
cache_key = f"u{user_id}"

# ✅ 好 - 包含版本号
cache_key = f"api:response:v2:{endpoint}"
```

### 2. 缓存预热

```python
async def warm_cache():
    """预热缓存"""
    # 热门用户
    popular_users = await database.get_popular_users(limit=100)
    for user in popular_users:
        await cache.set(f'user:{user.id}', user, ttl=3600)
    
    # 热门文章
    popular_posts = await database.get_popular_posts(limit=50)
    for post in popular_posts:
        await cache.set(f'post:{post.id}', post, ttl=1800)
```

### 3. 缓存失效策略

```python
async def update_user(user_id: int, data: dict):
    """更新用户并使缓存失效"""
    # 更新数据库
    user = await database.update_user(user_id, data)
    
    # 删除相关缓存
    await cache.delete(f'user:{user_id}')
    await cache.delete(f'user:profile:{user_id}')
    await cache.delete(f'user:posts:{user_id}')
    
    return user
```

---

## 🔗 相关资源

- [Redis文档](https://redis.io/docs/)
- [cachetools文档](https://cachetools.readthedocs.io/)

---

**最后更新**: 2025年10月28日

