#!/usr/bin/env python3
"""
高级异步编程示例
展示asyncio的高级功能，包括异步上下文管理、信号量、队列等
"""

import asyncio
import aiohttp
import aiofiles
import time
import json
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import signal
import sys
from contextlib import asynccontextmanager
from asyncio import Queue, Semaphore, Event, Lock
import random

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    status: str
    result: Any = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None

class AsyncTaskManager:
    """异步任务管理器"""
    
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.semaphore = Semaphore(max_concurrent)
        self.tasks: Dict[str, asyncio.Task] = {}
        self.results: Dict[str, TaskResult] = {}
        self.shutdown_event = Event()
        self.lock = Lock()
    
    async def add_task(self, task_id: str, coro) -> TaskResult:
        """添加任务"""
        async with self.semaphore:
            if self.shutdown_event.is_set():
                raise RuntimeError("任务管理器已关闭")
            
            async with self.lock:
                if task_id in self.tasks:
                    raise ValueError(f"任务 {task_id} 已存在")
                
                # 创建任务
                task = asyncio.create_task(self._execute_task(task_id, coro))
                self.tasks[task_id] = task
                
                # 等待任务完成
                result = await task
                return result
    
    async def _execute_task(self, task_id: str, coro) -> TaskResult:
        """执行任务"""
        start_time = datetime.now()
        result = TaskResult(
            task_id=task_id,
            status="running",
            start_time=start_time
        )
        
        try:
            logger.info(f"开始执行任务: {task_id}")
            task_result = await coro
            result.status = "completed"
            result.result = task_result
        except Exception as e:
            result.status = "failed"
            result.error = str(e)
            logger.error(f"任务 {task_id} 执行失败: {e}")
        finally:
            result.end_time = datetime.now()
            result.duration = (result.end_time - result.start_time).total_seconds()
            
            async with self.lock:
                self.results[task_id] = result
                if task_id in self.tasks:
                    del self.tasks[task_id]
            
            logger.info(f"任务 {task_id} 完成，耗时: {result.duration:.2f}秒")
        
        return result
    
    async def get_result(self, task_id: str) -> Optional[TaskResult]:
        """获取任务结果"""
        async with self.lock:
            return self.results.get(task_id)
    
    async def get_all_results(self) -> Dict[str, TaskResult]:
        """获取所有任务结果"""
        async with self.lock:
            return self.results.copy()
    
    async def shutdown(self):
        """关闭任务管理器"""
        logger.info("正在关闭任务管理器...")
        self.shutdown_event.set()
        
        # 等待所有任务完成
        if self.tasks:
            await asyncio.gather(*self.tasks.values(), return_exceptions=True)
        
        logger.info("任务管理器已关闭")

class AsyncDataProcessor:
    """异步数据处理器"""
    
    def __init__(self, input_queue: Queue, output_queue: Queue, 
                 max_workers: int = 5):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.max_workers = max_workers
        self.semaphore = Semaphore(max_workers)
        self.workers: List[asyncio.Task] = []
        self.shutdown_event = Event()
    
    async def start(self):
        """启动处理器"""
        logger.info(f"启动数据处理器，工作线程数: {self.max_workers}")
        
        # 创建工作线程
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)
    
    async def _worker(self, worker_id: str):
        """工作线程"""
        logger.info(f"工作线程 {worker_id} 启动")
        
        while not self.shutdown_event.is_set():
            try:
                # 获取数据
                data = await asyncio.wait_for(
                    self.input_queue.get(), timeout=1.0
                )
                
                async with self.semaphore:
                    # 处理数据
                    processed_data = await self._process_data(data, worker_id)
                    
                    # 输出结果
                    await self.output_queue.put(processed_data)
                    
                    # 标记任务完成
                    self.input_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"工作线程 {worker_id} 处理数据时出错: {e}")
        
        logger.info(f"工作线程 {worker_id} 停止")
    
    async def _process_data(self, data: Dict[str, Any], worker_id: str) -> Dict[str, Any]:
        """处理数据"""
        # 模拟数据处理
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        processed_data = data.copy()
        processed_data['processed_by'] = worker_id
        processed_data['processed_at'] = datetime.now().isoformat()
        processed_data['processed_value'] = data.get('value', 0) * 2
        
        return processed_data
    
    async def stop(self):
        """停止处理器"""
        logger.info("正在停止数据处理器...")
        self.shutdown_event.set()
        
        # 等待所有工作线程完成
        if self.workers:
            await asyncio.gather(*self.workers, return_exceptions=True)
        
        logger.info("数据处理器已停止")

class AsyncFileManager:
    """异步文件管理器"""
    
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.lock = Lock()
    
    @asynccontextmanager
    async def open_file(self, file_path: str, mode: str = 'r'):
        """异步文件上下文管理器"""
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with self.lock:
            async with aiofiles.open(full_path, mode) as f:
                yield f
    
    async def read_json(self, file_path: str) -> Dict[str, Any]:
        """读取JSON文件"""
        async with self.open_file(file_path, 'r') as f:
            content = await f.read()
            return json.loads(content)
    
    async def write_json(self, file_path: str, data: Dict[str, Any]):
        """写入JSON文件"""
        async with self.open_file(file_path, 'w') as f:
            content = json.dumps(data, indent=2, ensure_ascii=False)
            await f.write(content)
    
    async def read_lines(self, file_path: str) -> List[str]:
        """读取文件行"""
        async with self.open_file(file_path, 'r') as f:
            return await f.readlines()
    
    async def write_lines(self, file_path: str, lines: List[str]):
        """写入文件行"""
        async with self.open_file(file_path, 'w') as f:
            await f.writelines(lines)

class AsyncWebClient:
    """异步Web客户端"""
    
    def __init__(self, timeout: int = 30, max_connections: int = 100):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.connector = aiohttp.TCPConnector(limit=max_connections)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=self.timeout,
            connector=self.connector
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """GET请求"""
        if not self.session:
            raise RuntimeError("Web客户端未初始化")
        
        async with self.session.get(url, **kwargs) as response:
            return {
                'url': url,
                'status': response.status,
                'headers': dict(response.headers),
                'content': await response.text()
            }
    
    async def post(self, url: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """POST请求"""
        if not self.session:
            raise RuntimeError("Web客户端未初始化")
        
        async with self.session.post(url, json=data, **kwargs) as response:
            return {
                'url': url,
                'status': response.status,
                'headers': dict(response.headers),
                'content': await response.text()
            }
    
    async def fetch_multiple(self, urls: List[str]) -> List[Dict[str, Any]]:
        """并发获取多个URL"""
        if not self.session:
            raise RuntimeError("Web客户端未初始化")
        
        tasks = [self.get(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

class AsyncRateLimiter:
    """异步限流器"""
    
    def __init__(self, rate: int, per: float):
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
        self.lock = Lock()
    
    async def acquire(self):
        """获取许可"""
        async with self.lock:
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current
            
            self.allowance += time_passed * (self.rate / self.per)
            if self.allowance > self.rate:
                self.allowance = self.rate
            
            if self.allowance < 1.0:
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                await asyncio.sleep(sleep_time)
                self.allowance = 0.0
            else:
                self.allowance -= 1.0

class AsyncCache:
    """异步缓存"""
    
    def __init__(self, ttl: float = 3600):
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        async with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                if time.time() - entry['timestamp'] < self.ttl:
                    return entry['value']
                else:
                    del self.cache[key]
            return None
    
    async def set(self, key: str, value: Any):
        """设置缓存值"""
        async with self.lock:
            self.cache[key] = {
                'value': value,
                'timestamp': time.time()
            }
    
    async def delete(self, key: str):
        """删除缓存值"""
        async with self.lock:
            if key in self.cache:
                del self.cache[key]
    
    async def clear(self):
        """清空缓存"""
        async with self.lock:
            self.cache.clear()

# 示例函数
async def simulate_work(task_id: str, duration: float) -> str:
    """模拟工作"""
    await asyncio.sleep(duration)
    return f"任务 {task_id} 完成，耗时 {duration:.2f}秒"

async def fetch_url_data(url: str) -> Dict[str, Any]:
    """获取URL数据"""
    async with AsyncWebClient() as client:
        try:
            result = await client.get(url)
            return {
                'url': url,
                'success': True,
                'status': result['status'],
                'content_length': len(result['content'])
            }
        except Exception as e:
            return {
                'url': url,
                'success': False,
                'error': str(e)
            }

async def process_data_batch(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """批量处理数据"""
    input_queue = Queue()
    output_queue = Queue()
    
    # 添加数据到输入队列
    for data in data_list:
        await input_queue.put(data)
    
    # 创建数据处理器
    processor = AsyncDataProcessor(input_queue, output_queue, max_workers=3)
    
    # 启动处理器
    await processor.start()
    
    # 收集结果
    results = []
    for _ in range(len(data_list)):
        result = await output_queue.get()
        results.append(result)
    
    # 停止处理器
    await processor.stop()
    
    return results

async def demonstrate_async_features():
    """演示异步功能"""
    logger.info("开始演示异步功能")
    
    # 1. 异步任务管理器
    logger.info("=== 异步任务管理器演示 ===")
    task_manager = AsyncTaskManager(max_concurrent=3)
    
    # 添加任务
    tasks = [
        ("task-1", simulate_work("task-1", 1.0)),
        ("task-2", simulate_work("task-2", 2.0)),
        ("task-3", simulate_work("task-3", 0.5)),
        ("task-4", simulate_work("task-4", 1.5)),
    ]
    
    for task_id, coro in tasks:
        result = await task_manager.add_task(task_id, coro)
        logger.info(f"任务结果: {result.status} - {result.result}")
    
    # 2. 异步Web客户端
    logger.info("=== 异步Web客户端演示 ===")
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/json",
    ]
    
    async with AsyncWebClient() as client:
        results = await client.fetch_multiple(urls)
        for result in results:
            if isinstance(result, dict):
                logger.info(f"请求结果: {result['url']} - {result['status']}")
            else:
                logger.error(f"请求失败: {result}")
    
    # 3. 异步文件管理
    logger.info("=== 异步文件管理演示 ===")
    file_manager = AsyncFileManager(Path("temp"))
    
    # 写入JSON文件
    test_data = {
        "name": "测试数据",
        "timestamp": datetime.now().isoformat(),
        "values": [1, 2, 3, 4, 5]
    }
    await file_manager.write_json("test.json", test_data)
    
    # 读取JSON文件
    loaded_data = await file_manager.read_json("test.json")
    logger.info(f"读取的数据: {loaded_data['name']}")
    
    # 4. 异步限流器
    logger.info("=== 异步限流器演示 ===")
    rate_limiter = AsyncRateLimiter(rate=2, per=1.0)  # 每秒2个请求
    
    start_time = time.time()
    for i in range(5):
        await rate_limiter.acquire()
        logger.info(f"限流请求 {i+1} 完成")
    end_time = time.time()
    logger.info(f"限流测试完成，总耗时: {end_time - start_time:.2f}秒")
    
    # 5. 异步缓存
    logger.info("=== 异步缓存演示 ===")
    cache = AsyncCache(ttl=5.0)
    
    # 设置缓存
    await cache.set("key1", "value1")
    await cache.set("key2", {"data": "value2"})
    
    # 获取缓存
    value1 = await cache.get("key1")
    value2 = await cache.get("key2")
    logger.info(f"缓存值1: {value1}")
    logger.info(f"缓存值2: {value2}")
    
    # 6. 数据批量处理
    logger.info("=== 数据批量处理演示 ===")
    test_data_list = [
        {"id": i, "value": i * 10, "name": f"item-{i}"}
        for i in range(10)
    ]
    
    processed_results = await process_data_batch(test_data_list)
    logger.info(f"处理了 {len(processed_results)} 条数据")
    
    # 关闭任务管理器
    await task_manager.shutdown()
    
    logger.info("异步功能演示完成")

async def signal_handler():
    """信号处理器"""
    logger.info("收到关闭信号，正在清理资源...")
    
    # 这里可以添加清理逻辑
    await asyncio.sleep(1)
    
    logger.info("资源清理完成")
    sys.exit(0)

async def main():
    """主函数"""
    # 设置信号处理
    loop = asyncio.get_event_loop()
    for sig in [signal.SIGTERM, signal.SIGINT]:
        loop.add_signal_handler(sig, lambda: asyncio.create_task(signal_handler()))
    
    try:
        await demonstrate_async_features()
    except KeyboardInterrupt:
        logger.info("收到中断信号")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
    finally:
        logger.info("程序结束")

if __name__ == "__main__":
    asyncio.run(main())
