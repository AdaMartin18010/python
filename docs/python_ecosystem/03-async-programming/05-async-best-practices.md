# 异步编程最佳实践

**Python异步编程指南**

---

## 📋 核心原则

### 1. 避免阻塞

```python
# ❌ 错误 - 阻塞事件循环
import time
async def bad():
    time.sleep(1)  # 阻塞！

# ✅ 正确 - 异步睡眠
import asyncio
async def good():
    await asyncio.sleep(1)
```

### 2. CPU密集型使用进程池

```python
from concurrent.futures import ProcessPoolExecutor

async def cpu_intensive():
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, heavy_computation)
    return result
```

### 3. 使用连接池

```python
# ✅ 好 - 重用连接
async with aiohttp.ClientSession() as session:
    for url in urls:
        async with session.get(url) as response:
            data = await response.text()

# ❌ 差 - 每次新建连接
for url in urls:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
```

---

## 🔒 并发控制

### 信号量限流

```python
async def limited_fetch(url, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

async def main():
    semaphore = asyncio.Semaphore(10)  # 限制10个并发
    tasks = [limited_fetch(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)
```

---

## ⚡ 性能优化

### 1. 使用asyncpg替代psycopg2

```python
# ✅ 快3-5倍
import asyncpg
conn = await asyncpg.connect(...)

# ❌ 较慢
import psycopg2
conn = psycopg2.connect(...)
```

### 2. 批量操作

```python
# ✅ 批量查询
results = await conn.fetch("SELECT * FROM users WHERE id = ANY($1)", user_ids)

# ❌ 逐个查询
results = [await conn.fetchrow("SELECT * FROM users WHERE id = $1", id) for id in user_ids]
```

---

## 🔧 错误处理

### 1. 捕获所有任务异常

```python
async def main():
    tasks = [task1(), task2(), task3()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
```

### 2. 超时保护

```python
try:
    result = await asyncio.wait_for(operation(), timeout=30.0)
except asyncio.TimeoutError:
    print("Operation timed out")
```

---

## 📚 资源管理

### 使用上下文管理器

```python
class AsyncResource:
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

async with AsyncResource() as resource:
    await resource.use()
```

---

## 🔗 相关资源

- [AsyncIO文档](https://docs.python.org/3/library/asyncio.html)

---

**最后更新**: 2025年10月28日

