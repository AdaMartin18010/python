# Python 异步编程完全指南 2025

**AsyncIO深度解析与最佳实践**

---

## 📊 异步编程体系

```mermaid
mindmap
  root((异步编程))
    核心概念
      协程Coroutine
      事件循环EventLoop
      任务Task
      Future对象
    
    语法特性
      async def
      await表达式
      async for
      async with
    
    并发模式
      gather并发执行
      TaskGroup任务组
      Semaphore限流
      Queue队列
    
    实战应用
      异步HTTP
      异步数据库
      异步文件IO
      WebSocket
    
    性能优化
      连接池
      批量操作
      超时控制
      错误处理
```

---

## 1️⃣ 异步编程基础

### 1.1 核心概念理解

```python
"""
异步编程核心概念
"""
import asyncio
from typing import Coroutine

# ============================================
# 1. 协程 (Coroutine)
# ============================================

async def simple_coroutine() -> str:
    """简单协程"""
    print("Coroutine started")
    await asyncio.sleep(1)  # 暂停,让出控制权
    print("Coroutine finished")
    return "Result"

# 协程对象 (不会立即执行)
coro = simple_coroutine()
print(type(coro))  # <class 'coroutine'>

# 运行协程
result = asyncio.run(coro)
print(result)  # "Result"

# ============================================
# 2. 事件循环 (Event Loop)
# ============================================

async def understand_event_loop():
    """理解事件循环"""
    # 获取当前事件循环
    loop = asyncio.get_running_loop()
    print(f"Running on: {loop}")
    
    # 事件循环调度任务
    task1 = asyncio.create_task(task("A", 2))
    task2 = asyncio.create_task(task("B", 1))
    
    # 等待任务完成
    await task1
    await task2

async def task(name: str, delay: float):
    """模拟异步任务"""
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")

# 运行
asyncio.run(understand_event_loop())

# ============================================
# 3. Task对象
# ============================================

async def understand_tasks():
    """理解Task对象"""
    
    # 创建Task
    task1 = asyncio.create_task(simple_coroutine())
    print(f"Task created: {task1}")
    print(f"Task done: {task1.done()}")  # False
    
    # 等待Task完成
    result = await task1
    print(f"Task done: {task1.done()}")  # True
    print(f"Result: {result}")
    
    # Task可以取消
    task2 = asyncio.create_task(asyncio.sleep(10))
    task2.cancel()  # 取消任务
    
    try:
        await task2
    except asyncio.CancelledError:
        print("Task was cancelled")

# ============================================
# 4. Future对象
# ============================================

async def understand_future():
    """理解Future对象"""
    loop = asyncio.get_running_loop()
    
    # 创建Future
    future = loop.create_future()
    
    async def set_future_result():
        await asyncio.sleep(1)
        future.set_result("Future result!")
    
    # 启动设置结果的任务
    asyncio.create_task(set_future_result())
    
    # 等待Future完成
    result = await future
    print(result)  # "Future result!"

# ============================================
# 协程 vs Task vs Future 对比
# ============================================

"""
Coroutine (协程):
- 使用 async def 定义
- 可await的对象
- 需要被调度执行

Task (任务):
- 包装协程的高级对象
- 自动调度执行
- 可以取消、查询状态

Future (未来对象):
- 最低级的awaitable
- 表示异步操作的结果
- 通常不直接使用
"""
```

### 1.2 async/await语法

```python
"""
async/await语法详解
"""

# ============================================
# 1. async def - 定义协程
# ============================================

async def fetch_data(url: str) -> dict:
    """异步获取数据"""
    # 模拟网络请求
    await asyncio.sleep(1)
    return {"url": url, "status": 200}

# ============================================
# 2. await - 等待协程
# ============================================

async def process_data():
    """处理数据"""
    # await只能在async def中使用
    data = await fetch_data("https://example.com")
    print(f"Received: {data}")
    return data

# ❌ 错误: await不能在普通函数中使用
# def wrong():
#     await asyncio.sleep(1)  # SyntaxError!

# ============================================
# 3. 多个await - 顺序执行
# ============================================

async def sequential_execution():
    """顺序执行 - 慢"""
    print("Starting...")
    
    # 顺序执行,总时间 = 1 + 2 + 3 = 6秒
    result1 = await fetch_data("url1")  # 1秒
    result2 = await fetch_data("url2")  # 2秒
    result3 = await fetch_data("url3")  # 3秒
    
    print("Finished!")
    return [result1, result2, result3]

# ============================================
# 4. 并发执行 - 使用gather
# ============================================

async def concurrent_execution():
    """并发执行 - 快"""
    print("Starting...")
    
    # 并发执行,总时间 = max(1, 2, 3) = 3秒
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3")
    )
    
    print("Finished!")
    return results

# 性能对比
# sequential_execution(): ~6秒
# concurrent_execution(): ~3秒 (2x faster!)

# ============================================
# 5. async for - 异步迭代
# ============================================

class AsyncIterator:
    """异步迭代器"""
    
    def __init__(self, max_count: int):
        self.max_count = max_count
        self.current = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.max_count:
            raise StopAsyncIteration
        
        self.current += 1
        await asyncio.sleep(0.1)  # 模拟异步操作
        return self.current

async def async_iteration():
    """使用async for"""
    async for number in AsyncIterator(5):
        print(f"Got: {number}")

# ============================================
# 6. async with - 异步上下文管理器
# ============================================

class AsyncResource:
    """异步资源"""
    
    async def __aenter__(self):
        print("Acquiring resource...")
        await asyncio.sleep(1)
        print("Resource acquired")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource...")
        await asyncio.sleep(1)
        print("Resource released")

async def use_async_context():
    """使用async with"""
    async with AsyncResource() as resource:
        print("Using resource...")
        await asyncio.sleep(1)

# ============================================
# 7. 异步生成器
# ============================================

async def async_generator(n: int):
    """异步生成器"""
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def consume_async_generator():
    """消费异步生成器"""
    async for value in async_generator(5):
        print(f"Generated: {value}")
```

---

## 2️⃣ 并发控制模式

### 2.1 并发执行

```python
"""
并发执行模式
"""
import asyncio
from typing import List, Any
import time

# ============================================
# 1. asyncio.gather - 并发执行多个协程
# ============================================

async def fetch_page(page: int, delay: float) -> dict:
    """模拟获取页面"""
    await asyncio.sleep(delay)
    return {"page": page, "data": f"Page {page} data"}

async def gather_example():
    """gather示例"""
    # 并发执行多个协程
    results = await asyncio.gather(
        fetch_page(1, 1.0),
        fetch_page(2, 0.5),
        fetch_page(3, 1.5),
        fetch_page(4, 0.8)
    )
    return results

# ============================================
# 2. asyncio.gather vs asyncio.wait
# ============================================

async def gather_vs_wait():
    """gather vs wait对比"""
    
    # gather: 返回结果列表,保持顺序
    results = await asyncio.gather(
        fetch_page(1, 1.0),
        fetch_page(2, 0.5)
    )
    print(f"Gather results: {results}")
    
    # wait: 返回完成和待处理的任务集合
    tasks = [
        asyncio.create_task(fetch_page(1, 1.0)),
        asyncio.create_task(fetch_page(2, 0.5))
    ]
    done, pending = await asyncio.wait(tasks)
    
    results = [task.result() for task in done]
    print(f"Wait results: {results}")

# ============================================
# 3. 错误处理
# ============================================

async def failing_task():
    """会失败的任务"""
    await asyncio.sleep(0.5)
    raise ValueError("Task failed!")

async def error_handling():
    """错误处理"""
    
    # gather默认: 遇到错误立即抛出
    try:
        results = await asyncio.gather(
            fetch_page(1, 0.5),
            failing_task(),
            fetch_page(2, 0.5)
        )
    except ValueError as e:
        print(f"Error caught: {e}")
    
    # gather with return_exceptions: 返回异常对象
    results = await asyncio.gather(
        fetch_page(1, 0.5),
        failing_task(),
        fetch_page(2, 0.5),
        return_exceptions=True  # 不抛出异常
    )
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} succeeded: {result}")

# ============================================
# 4. TaskGroup (Python 3.11+)
# ============================================

async def task_group_example():
    """TaskGroup示例"""
    async with asyncio.TaskGroup() as group:
        task1 = group.create_task(fetch_page(1, 1.0))
        task2 = group.create_task(fetch_page(2, 0.5))
        task3 = group.create_task(fetch_page(3, 1.5))
    
    # 离开上下文后,所有任务都已完成
    print(f"All tasks done!")
    print(f"Results: {task1.result()}, {task2.result()}, {task3.result()}")

# ============================================
# 5. 超时控制
# ============================================

async def with_timeout():
    """超时控制"""
    
    # 方式1: asyncio.wait_for
    try:
        result = await asyncio.wait_for(
            fetch_page(1, 5.0),  # 5秒
            timeout=2.0  # 超时2秒
        )
    except asyncio.TimeoutError:
        print("Operation timed out!")
    
    # 方式2: asyncio.timeout (Python 3.11+)
    try:
        async with asyncio.timeout(2.0):
            result = await fetch_page(1, 5.0)
    except asyncio.TimeoutError:
        print("Operation timed out!")
```

### 2.2 限流和队列

```python
"""
限流和队列模式
"""

# ============================================
# 1. Semaphore - 限制并发数
# ============================================

async def fetch_with_semaphore(
    url: str,
    semaphore: asyncio.Semaphore
) -> dict:
    """带信号量的请求"""
    async with semaphore:  # 获取许可
        print(f"Fetching {url}...")
        await asyncio.sleep(1)
        print(f"Finished {url}")
        return {"url": url}

async def limited_concurrency():
    """限制并发数量"""
    # 最多3个并发
    semaphore = asyncio.Semaphore(3)
    
    # 创建10个任务
    tasks = [
        fetch_with_semaphore(f"url{i}", semaphore)
        for i in range(10)
    ]
    
    # 并发执行,但同时最多3个
    results = await asyncio.gather(*tasks)
    return results

# ============================================
# 2. Queue - 生产者消费者模式
# ============================================

async def producer(queue: asyncio.Queue, producer_id: int):
    """生产者"""
    for i in range(5):
        item = f"item-{producer_id}-{i}"
        await queue.put(item)
        print(f"Producer {producer_id} produced: {item}")
        await asyncio.sleep(0.1)

async def consumer(queue: asyncio.Queue, consumer_id: int):
    """消费者"""
    while True:
        item = await queue.get()
        
        if item is None:  # 结束信号
            break
        
        print(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(0.5)  # 处理时间
        queue.task_done()

async def producer_consumer_pattern():
    """生产者消费者模式"""
    queue = asyncio.Queue(maxsize=10)
    
    # 启动2个生产者
    producers = [
        asyncio.create_task(producer(queue, i))
        for i in range(2)
    ]
    
    # 启动3个消费者
    consumers = [
        asyncio.create_task(consumer(queue, i))
        for i in range(3)
    ]
    
    # 等待生产者完成
    await asyncio.gather(*producers)
    
    # 等待队列处理完成
    await queue.join()
    
    # 发送结束信号
    for _ in consumers:
        await queue.put(None)
    
    # 等待消费者结束
    await asyncio.gather(*consumers)

# ============================================
# 3. Lock - 互斥锁
# ============================================

class SharedResource:
    """共享资源"""
    
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()
    
    async def increment(self):
        """安全递增"""
        async with self.lock:
            # 临界区
            current = self.value
            await asyncio.sleep(0.01)  # 模拟操作
            self.value = current + 1

async def test_lock():
    """测试锁"""
    resource = SharedResource()
    
    # 100个并发递增
    tasks = [resource.increment() for _ in range(100)]
    await asyncio.gather(*tasks)
    
    print(f"Final value: {resource.value}")  # 应该是100

# ============================================
# 4. Event - 事件通知
# ============================================

async def waiter(event: asyncio.Event, name: str):
    """等待者"""
    print(f"{name} waiting...")
    await event.wait()  # 等待事件
    print(f"{name} triggered!")

async def setter(event: asyncio.Event):
    """设置者"""
    await asyncio.sleep(2)
    print("Setting event...")
    event.set()  # 触发事件

async def event_pattern():
    """事件模式"""
    event = asyncio.Event()
    
    # 多个等待者
    waiters = [
        asyncio.create_task(waiter(event, f"Waiter-{i}"))
        for i in range(3)
    ]
    
    # 设置事件
    setter_task = asyncio.create_task(setter(event))
    
    await asyncio.gather(*waiters, setter_task)
```

---

## 3️⃣ 实战应用

### 3.1 异步HTTP客户端

```python
"""
异步HTTP最佳实践
"""
import aiohttp
from typing import List, Dict
import asyncio

# ============================================
# 1. 基础HTTP请求
# ============================================

async def fetch_url(url: str) -> str:
    """获取单个URL"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# ============================================
# 2. 复用Session
# ============================================

async def fetch_multiple_urls(urls: List[str]) -> List[str]:
    """复用Session"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch_one(
    session: aiohttp.ClientSession,
    url: str
) -> str:
    """使用共享Session"""
    async with session.get(url) as response:
        return await response.text()

# ============================================
# 3. 高级HTTP客户端
# ============================================

class AsyncHTTPClient:
    """异步HTTP客户端"""
    
    def __init__(
        self,
        base_url: str = "",
        timeout: int = 30,
        max_connections: int = 100
    ):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        
        # 连接池配置
        connector = aiohttp.TCPConnector(
            limit=max_connections,  # 最大连接数
            limit_per_host=10,  # 每个主机最大连接数
            ttl_dns_cache=300  # DNS缓存时间
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=self.timeout
        )
    
    async def get(
        self,
        path: str,
        **kwargs
    ) -> Dict:
        """GET请求"""
        url = f"{self.base_url}{path}"
        async with self.session.get(url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
    
    async def post(
        self,
        path: str,
        data: Dict,
        **kwargs
    ) -> Dict:
        """POST请求"""
        url = f"{self.base_url}{path}"
        async with self.session.post(url, json=data, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
    
    async def close(self):
        """关闭连接"""
        await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.close()

# 使用
async def use_client():
    """使用HTTP客户端"""
    async with AsyncHTTPClient("https://api.example.com") as client:
        # 并发请求
        results = await asyncio.gather(
            client.get("/users/1"),
            client.get("/users/2"),
            client.post("/users", {"name": "Alice"})
        )
        return results

# ============================================
# 4. 重试机制
# ============================================

from functools import wraps

def async_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0
):
    """异步重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    
                    print(f"Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {current_delay}s...")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
        
        return wrapper
    return decorator

@async_retry(max_attempts=3, delay=1.0)
async def unreliable_request(url: str) -> Dict:
    """可能失败的请求"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
```

### 3.2 异步数据库

```python
"""
异步数据库操作
"""
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy import select, update, delete
from contextlib import asynccontextmanager

# ============================================
# 1. 数据库连接配置
# ============================================

class AsyncDatabase:
    """异步数据库管理"""
    
    def __init__(self, database_url: str):
        # 创建异步引擎
        self.engine = create_async_engine(
            database_url,
            echo=False,
            pool_size=20,  # 连接池大小
            max_overflow=10,  # 最大溢出连接
            pool_pre_ping=True  # 连接健康检查
        )
        
        # 创建会话工厂
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    @asynccontextmanager
    async def session(self):
        """获取会话"""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    
    async def close(self):
        """关闭连接"""
        await self.engine.dispose()

# ============================================
# 2. 异步查询
# ============================================

class UserRepository:
    """用户仓储"""
    
    def __init__(self, db: AsyncDatabase):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> User | None:
        """根据ID获取用户"""
        async with self.db.session() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
    
    async def get_all(self, limit: int = 100) -> List[User]:
        """获取所有用户"""
        async with self.db.session() as session:
            stmt = select(User).limit(limit)
            result = await session.execute(stmt)
            return list(result.scalars().all())
    
    async def create(self, user_data: Dict) -> User:
        """创建用户"""
        async with self.db.session() as session:
            user = User(**user_data)
            session.add(user)
            await session.flush()  # 获取ID
            return user
    
    async def update(self, user_id: int, data: Dict) -> User:
        """更新用户"""
        async with self.db.session() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(**data)
                .returning(User)
            )
            result = await session.execute(stmt)
            return result.scalar_one()
    
    async def delete(self, user_id: int) -> bool:
        """删除用户"""
        async with self.db.session() as session:
            stmt = delete(User).where(User.id == user_id)
            result = await session.execute(stmt)
            return result.rowcount > 0

# ============================================
# 3. 批量操作
# ============================================

async def bulk_insert(db: AsyncDatabase, users: List[Dict]):
    """批量插入"""
    async with db.session() as session:
        user_objects = [User(**data) for data in users]
        session.add_all(user_objects)
    # 自动提交

async def bulk_update(db: AsyncDatabase, updates: List[Dict]):
    """批量更新"""
    async with db.session() as session:
        for update_data in updates:
            stmt = (
                update(User)
                .where(User.id == update_data["id"])
                .values(**update_data["data"])
            )
            await session.execute(stmt)
```

---

## 4️⃣ 性能优化

### 4.1 连接池管理

```python
"""
连接池优化
"""

# ============================================
# 1. HTTP连接池
# ============================================

class OptimizedHTTPClient:
    """优化的HTTP客户端"""
    
    def __init__(self):
        # 配置连接池
        connector = aiohttp.TCPConnector(
            limit=100,  # 总连接数
            limit_per_host=30,  # 每个主机连接数
            ttl_dns_cache=300,  # DNS缓存300秒
            enable_cleanup_closed=True  # 清理关闭的连接
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
    
    async def fetch_batch(self, urls: List[str]) -> List[str]:
        """批量获取"""
        tasks = [self.fetch_one(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def fetch_one(self, url: str) -> str:
        """获取单个URL"""
        try:
            async with self.session.get(url) as response:
                return await response.text()
        except Exception as e:
            return f"Error: {e}"

# ============================================
# 2. 数据库连接池
# ============================================

# 推荐配置
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,  # 常驻连接数
    max_overflow=10,  # 最大溢出连接
    pool_timeout=30,  # 获取连接超时
    pool_recycle=3600,  # 连接回收时间(秒)
    pool_pre_ping=True,  # 连接健康检查
    echo_pool=True  # 连接池日志
)
```

### 4.2 批量操作优化

```python
"""
批量操作优化
"""

# ============================================
# 1. 分批处理
# ============================================

async def process_in_batches(
    items: List[Any],
    batch_size: int = 100
):
    """分批处理"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        await process_batch(batch)

async def process_batch(batch: List[Any]):
    """处理一批"""
    tasks = [process_item(item) for item in batch]
    await asyncio.gather(*tasks)

# ============================================
# 2. 限流处理
# ============================================

async def process_with_rate_limit(
    items: List[Any],
    rate_limit: int = 10  # 每秒10个
):
    """限流处理"""
    semaphore = asyncio.Semaphore(rate_limit)
    
    async def process_with_semaphore(item):
        async with semaphore:
            await process_item(item)
            await asyncio.sleep(1 / rate_limit)
    
    tasks = [process_with_semaphore(item) for item in items]
    await asyncio.gather(*tasks)
```

---

## 📚 最佳实践清单

### 异步编程检查清单

- [ ] 使用`async def`定义协程函数
- [ ] 在协程中使用`await`等待异步操作
- [ ] 使用`asyncio.gather()`并发执行
- [ ] 合理使用`Semaphore`限制并发
- [ ] 为长时间操作设置超时
- [ ] 复用`Session`和连接池
- [ ] 正确处理异常和取消
- [ ] 使用`async with`管理资源
- [ ] 避免在协程中使用阻塞IO
- [ ] 使用`TaskGroup`管理任务生命周期

---

**掌握异步编程，构建高性能应用！** ⚡✨

**最后更新**: 2025年10月28日

