# 异步模式

**Python异步编程常见模式**

---

## 📋 概述

掌握异步编程的常见模式，能够编写高效、可维护的异步代码。

---

## 💻 核心模式

### 1. 并发限制

```python
import asyncio

async def fetch(url, semaphore):
    async with semaphore:
        # 限制并发数
        return await do_fetch(url)

async def main():
    semaphore = asyncio.Semaphore(10)  # 最多10个并发
    urls = [f"http://example.com/{i}" for i in range(100)]
    tasks = [fetch(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)
```

### 2. 超时控制

```python
async def with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=5.0)
        return result
    except asyncio.TimeoutError:
        return "Operation timed out"
```

### 3. 重试机制

```python
async def retry_async(func, max_retries=3, delay=1.0):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(delay * (2 ** attempt))  # 指数退避
```

---

## 🔄 高级模式

### 生产者-消费者

```python
async def producer(queue):
    for i in range(10):
        await asyncio.sleep(0.1)
        await queue.put(i)
    await queue.put(None)  # 结束信号

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        await process(item)

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(
        producer(queue),
        consumer(queue),
        consumer(queue),  # 多个消费者
    )
```

---

## 📚 最佳实践

### 1. 避免阻塞

```python
# ❌ 差
async def bad():
    time.sleep(1)  # 阻塞！

# ✅ 好
async def good():
    await asyncio.sleep(1)  # 异步
```

### 2. 取消处理

```python
async def cancellable_task():
    try:
        await long_running_operation()
    except asyncio.CancelledError:
        # 清理资源
        await cleanup()
        raise
```

---

**最后更新**: 2025年10月28日

