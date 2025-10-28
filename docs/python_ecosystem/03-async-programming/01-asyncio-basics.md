# AsyncIO 基础

**Python异步编程完全指南**

---

## 📋 概述

AsyncIO是Python标准库中的异步I/O框架，提供了编写并发代码的工具。
使用async/await语法，可以高效处理I/O密集型任务。

### 核心概念

- **协程 (Coroutine)**: 使用async def定义的函数
- **事件循环 (Event Loop)**: 管理和调度协程执行
- **任务 (Task)**: 封装的协程，可以并发执行
- **Future**: 表示异步操作的最终结果

---

## 🚀 快速开始

### Hello AsyncIO

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Python 3.7+
asyncio.run(main())
```

---

## 💻 核心功能

### 1. 基本协程

```python
import asyncio

async def fetch_data(id: int) -> str:
    print(f"开始获取数据 {id}")
    await asyncio.sleep(1)  # 模拟I/O操作
    print(f"完成获取数据 {id}")
    return f"数据 {id}"

async def main():
    result = await fetch_data(1)
    print(result)

asyncio.run(main())
```

### 2. 并发执行

```python
import asyncio
import time

async def task(name: str, delay: int):
    print(f"{name} 开始")
    await asyncio.sleep(delay)
    print(f"{name} 完成")
    return f"{name} 结果"

async def main():
    start = time.time()
    
    # ✅ 并发执行 - 快
    results = await asyncio.gather(
        task("任务1", 1),
        task("任务2", 2),
        task("任务3", 1)
    )
    
    print(f"耗时: {time.time() - start:.2f}秒")  # ~2秒
    print(results)

asyncio.run(main())
```

### 3. 创建任务

```python
import asyncio

async def background_task():
    while True:
        print("后台任务运行中...")
        await asyncio.sleep(1)

async def main():
    # 创建后台任务
    task = asyncio.create_task(background_task())
    
    # 主任务
    await asyncio.sleep(3)
    
    # 取消后台任务
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("任务已取消")

asyncio.run(main())
```

---

## 🔄 常见模式

### 1. 超时控制

```python
import asyncio

async def long_running_task():
    await asyncio.sleep(10)
    return "完成"

async def main():
    try:
        result = await asyncio.wait_for(long_running_task(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("超时!")

asyncio.run(main())
```

### 2. 并发限制

```python
import asyncio

async def fetch_url(url: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        print(f"开始获取 {url}")
        await asyncio.sleep(1)
        print(f"完成获取 {url}")
        return url

async def main():
    # 限制同时只有3个任务
    semaphore = asyncio.Semaphore(3)
    
    urls = [f"http://example.com/{i}" for i in range(10)]
    tasks = [fetch_url(url, semaphore) for url in urls]
    
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

### 3. 任务队列

```python
import asyncio

async def producer(queue: asyncio.Queue):
    for i in range(5):
        await asyncio.sleep(0.5)
        await queue.put(i)
        print(f"生产: {i}")
    await queue.put(None)  # 结束信号

async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        await asyncio.sleep(1)
        print(f"消费: {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    
    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )

asyncio.run(main())
```

---

## 🌐 异步HTTP

### 使用aiohttp

```python
import asyncio
import aiohttp

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, "https://example.com")
        print(f"获取了 {len(html)} 字节")

asyncio.run(main())
```

### 并发HTTP请求

```python
import asyncio
import aiohttp

async def fetch_all(urls: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def main():
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    results = await fetch_all(urls)
    print(f"获取了 {len(results)} 个页面")

asyncio.run(main())
```

---

## 📚 最佳实践

### 1. 避免阻塞操作

```python
import asyncio
import time

# ❌ 错误 - 阻塞事件循环
async def bad_example():
    time.sleep(1)  # 阻塞!
    return "完成"

# ✅ 正确 - 使用异步
async def good_example():
    await asyncio.sleep(1)  # 不阻塞
    return "完成"

# ✅ CPU密集型任务使用线程池
async def cpu_intensive():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, heavy_computation)
    return result
```

### 2. 异常处理

```python
import asyncio

async def risky_task(id: int):
    if id == 2:
        raise ValueError("错误!")
    await asyncio.sleep(1)
    return f"任务 {id}"

async def main():
    tasks = [risky_task(i) for i in range(5)]
    
    # gather with return_exceptions=True
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"任务 {i} 失败: {result}")
        else:
            print(f"任务 {i} 成功: {result}")

asyncio.run(main())
```

### 3. 资源清理

```python
import asyncio

class AsyncResource:
    async def __aenter__(self):
        print("打开资源")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("关闭资源")
        await asyncio.sleep(0.1)
    
    async def operation(self):
        print("执行操作")
        await asyncio.sleep(0.1)

async def main():
    async with AsyncResource() as resource:
        await resource.operation()

asyncio.run(main())
```

---

## ⚡ 性能对比

### 同步 vs 异步

```python
import asyncio
import time
import requests
import aiohttp

# 同步版本
def sync_fetch(urls: list[str]):
    start = time.time()
    results = [requests.get(url) for url in urls]
    return time.time() - start

# 异步版本
async def async_fetch(urls: list[str]):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        results = await asyncio.gather(*tasks)
    return time.time() - start

# 测试
urls = ["https://example.com"] * 10

sync_time = sync_fetch(urls)
async_time = asyncio.run(async_fetch(urls))

print(f"同步: {sync_time:.2f}秒")
print(f"异步: {async_time:.2f}秒")
print(f"提速: {sync_time/async_time:.1f}x")
```

---

## 🔗 相关资源

- [官方文档](https://docs.python.org/3/library/asyncio.html)
- [aiohttp文档](https://docs.aiohttp.org/)
- [Real Python AsyncIO教程](https://realpython.com/async-io-python/)

---

**最后更新**: 2025年10月28日

