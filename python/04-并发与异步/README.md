# 04-并发与异步

聚焦多线程、多进程、异步（asyncio/Trio）与并行化模式。

## 1. 并发模型

- 线程、进程、协程对比与适用性
- I/O 密集 vs CPU 密集

### 1.1 并发模型对比

```python
import asyncio
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

# 1. 线程模型 - 适合I/O密集型任务
def io_intensive_task(url: str) -> str:
    """模拟I/O密集型任务"""
    time.sleep(0.1)  # 模拟网络请求
    return f"Response from {url}"

def thread_example():
    """线程示例"""
    with ThreadPoolExecutor(max_workers=5) as executor:
        urls = [f"url_{i}" for i in range(10)]
        results = list(executor.map(io_intensive_task, urls))
    return results

# 2. 进程模型 - 适合CPU密集型任务
def cpu_intensive_task(n: int) -> int:
    """模拟CPU密集型任务"""
    result = 0
    for i in range(n):
        result += i ** 2
    return result

def process_example():
    """进程示例"""
    with ProcessPoolExecutor(max_workers=4) as executor:
        numbers = [1000000, 2000000, 3000000, 4000000]
        results = list(executor.map(cpu_intensive_task, numbers))
    return results

# 3. 协程模型 - 适合高并发I/O任务
async def async_io_task(url: str) -> str:
    """异步I/O任务"""
    await asyncio.sleep(0.1)  # 模拟异步网络请求
    return f"Async response from {url}"

async def async_example():
    """异步示例"""
    urls = [f"url_{i}" for i in range(10)]
    tasks = [async_io_task(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
```

### 1.2 选择指南

| 模型 | 适用场景 | 优势 | 劣势 |
|------|----------|------|------|
| 线程 | I/O密集型，简单并发 | 简单易用，共享内存 | GIL限制，上下文切换开销 |
| 进程 | CPU密集型，计算密集 | 真正并行，无GIL限制 | 内存开销大，通信复杂 |
| 协程 | 高并发I/O，网络服务 | 高并发，低开销 | 单线程，CPU密集型任务不适用 |

## 2. asyncio 实践

- 任务、事件循环、超时与取消
- 限流、重试与背压
- 示例：`./examples/asyncio_rate_limit/main.py`
  - 运行：`python main.py`

### 2.1 现代asyncio特性

```python
import asyncio
from typing import List, Any
from contextlib import asynccontextmanager

# 任务组（Python 3.11+）
async def task_group_example():
    """任务组示例"""
    async def worker(name: str, delay: float) -> str:
        await asyncio.sleep(delay)
        return f"Worker {name} completed"
    
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(worker("A", 1.0))
            task2 = tg.create_task(worker("B", 0.5))
            task3 = tg.create_task(worker("C", 1.5))
        
        print("All tasks completed successfully")
        return [task1.result(), task2.result(), task3.result()]
    except* Exception as eg:
        print(f"Some tasks failed: {eg.exceptions}")
        raise

# 异常组处理（Python 3.11+）
async def exception_group_example():
    """异常组处理示例"""
    async def failing_task(name: str, should_fail: bool) -> str:
        if should_fail:
            raise ValueError(f"Task {name} failed")
        return f"Task {name} succeeded"
    
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(failing_task("A", False))
            tg.create_task(failing_task("B", True))
            tg.create_task(failing_task("C", True))
    except* ValueError as eg:
        print(f"ValueError in {len(eg.exceptions)} tasks")
        for exc in eg.exceptions:
            print(f"  - {exc}")
    except* TypeError as eg:
        print(f"TypeError in {len(eg.exceptions)} tasks")
```

### 2.2 限流与重试机制

```python
import asyncio
import aiohttp
from typing import Optional, Callable, Any
from dataclasses import dataclass

@dataclass
class RateLimiter:
    """速率限制器"""
    max_requests: int
    time_window: float
    _requests: List[float] = None
    
    def __post_init__(self):
        self._requests = []
    
    async def acquire(self) -> None:
        """获取请求许可"""
        now = asyncio.get_event_loop().time()
        
        # 清理过期的请求记录
        self._requests = [req_time for req_time in self._requests 
                         if now - req_time < self.time_window]
        
        # 如果达到限制，等待
        if len(self._requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self._requests[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                return await self.acquire()
        
        self._requests.append(now)

class RetryConfig:
    """重试配置"""
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, 
                 max_delay: float = 60.0, exponential_base: float = 2.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base

async def retry_async(func: Callable, config: RetryConfig, *args, **kwargs) -> Any:
    """异步重试装饰器"""
    last_exception = None
    
    for attempt in range(config.max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt == config.max_retries:
                break
            
            # 指数退避
            delay = min(
                config.base_delay * (config.exponential_base ** attempt),
                config.max_delay
            )
            await asyncio.sleep(delay)
    
    raise last_exception

# 使用示例
async def fetch_with_retry_and_rate_limit(url: str) -> dict:
    """带重试和限流的请求"""
    rate_limiter = RateLimiter(max_requests=10, time_window=1.0)
    retry_config = RetryConfig(max_retries=3, base_delay=1.0)
    
    async def _fetch():
        await rate_limiter.acquire()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise aiohttp.ClientError(f"HTTP {response.status}")
    
    return await retry_async(_fetch, retry_config)
```

## 3. Trio/其他运行时（占位）

- 结构化并发思想

## 4. 并行与性能

- 进程池/线程池
- GIL 影响与规避策略

## 5. 示例与模式（占位）

- 最小 asyncio 示例与测试建议

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 相关主题：
  - [01-语言与生态/README](../01-语言与生态/README.md)
  - [02-测试与质量/README](../02-测试与质量/README.md)
  - [03-工程与交付/README](../03-工程与交付/README.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)
- 相关规范：[重构规范](../99-上下文与流程/03-重构规范.md)

## 来源与回链（docs → python）

- 异步编程模式来源：`docs/python_ecosystem/02-高级特性/02-3.Behavioral_rust_async.md` → 本地：[迁移/异步编程模式](./迁移/异步编程模式.md)
- 并发模式来源：`docs/python_ecosystem/02-高级特性/02-2.Structural_rust_threads.md` → 本地：[迁移/并发模式与最佳实践](./迁移/并发模式与最佳实践.md)
