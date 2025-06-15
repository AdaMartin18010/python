# 01. Python语言理论

## 1.1 Python语言基础理论

### 1.1.1 Python的设计哲学

**Python的设计原则**（The Zen of Python）：

```python
import this

# 核心原则：
# 1. 显式优于隐式 (Explicit is better than implicit)
# 2. 简单优于复杂 (Simple is better than complex)
# 3. 复杂优于复杂化 (Complex is better than complicated)
# 4. 可读性很重要 (Readability counts)
# 5. 实用性胜过纯粹性 (Practicality beats purity)
```

### 1.1.2 Python的类型系统

**动态类型系统**：

```python
from typing import Any, Union, Optional, TypeVar, Generic, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod

# 类型注解系统
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old"

# 联合类型
def process_data(data: Union[str, int, float]) -> str:
    return str(data)

# 可选类型
def find_user(user_id: Optional[int] = None) -> Optional[dict]:
    if user_id is None:
        return None
    return {"id": user_id, "name": "John"}

# 泛型
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()
    
    def is_empty(self) -> bool:
        return len(self.items) == 0

# 协议类型（结构化类型）
class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing a circle")

def draw_shape(shape: Drawable) -> None:
    shape.draw()
```

### 1.1.3 Python的对象模型

**对象系统**：

```python
class PythonObject:
    """Python对象的基础模型"""
    
    def __init__(self):
        self.__dict__ = {}  # 实例字典
        self.__class__ = type(self)  # 类型对象
    
    def __getattribute__(self, name: str) -> Any:
        """属性访问机制"""
        # 1. 检查描述符
        # 2. 检查实例字典
        # 3. 检查类字典
        # 4. 检查父类
        return super().__getattribute__(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """属性设置机制"""
        self.__dict__[name] = value

# 描述符协议
class Descriptor:
    """描述符基类"""
    
    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self
        return self._get_value(obj)
    
    def __set__(self, obj: Any, value: Any) -> None:
        self._set_value(obj, value)
    
    def __delete__(self, obj: Any) -> None:
        self._delete_value(obj)
    
    def _get_value(self, obj: Any) -> Any:
        raise NotImplementedError
    
    def _set_value(self, obj: Any, value: Any) -> None:
        raise NotImplementedError
    
    def _delete_value(self, obj: Any) -> None:
        raise NotImplementedError

class Property(Descriptor):
    """属性描述符"""
    
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc
    
    def _get_value(self, obj: Any) -> Any:
        if self.fget is None:
            raise AttributeError("can't get attribute")
        return self.fget(obj)
    
    def _set_value(self, obj: Any, value: Any) -> None:
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)
    
    def _delete_value(self, obj: Any) -> None:
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

# 元类系统
class MetaClass(type):
    """元类示例"""
    
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        # 在类创建时进行干预
        print(f"Creating class: {name}")
        return super().__new__(mcs, name, bases, namespace)
    
    def __init__(cls, name: str, bases: tuple, namespace: dict):
        # 在类初始化时进行干预
        super().__init__(name, bases, namespace)
        print(f"Initialized class: {name}")

class MyClass(metaclass=MetaClass):
    pass
```

## 1.2 函数式编程理论

### 1.2.1 函数作为一等公民

**高阶函数**：

```python
from typing import Callable, List, Iterator
from functools import reduce, partial
import operator

# 函数作为参数
def apply_operation(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# 函数作为返回值
def create_adder(n: int) -> Callable[[int], int]:
    def adder(x: int) -> int:
        return x + n
    return adder

# 装饰器模式
def timer(func: Callable) -> Callable:
    import time
    
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"

# 函数组合
def compose(*functions: Callable) -> Callable:
    def inner(arg):
        result = arg
        for f in reversed(functions):
            result = f(result)
        return result
    return inner

# 示例：组合函数
def add_one(x: int) -> int:
    return x + 1

def multiply_by_two(x: int) -> int:
    return x * 2

def square(x: int) -> int:
    return x ** 2

# 组合：square(multiply_by_two(add_one(x)))
combined = compose(square, multiply_by_two, add_one)
result = combined(5)  # ((5 + 1) * 2)² = 144
```

### 1.2.2 不可变数据结构

**不可变性**：

```python
from typing import Tuple, NamedTuple, FrozenSet
from dataclasses import dataclass, field
from collections import namedtuple

# 命名元组
Point = namedtuple('Point', ['x', 'y'])

# 数据类（不可变）
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float
    
    def distance_to(self, other: 'ImmutablePoint') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# 不可变集合
def create_immutable_set() -> FrozenSet[int]:
    return frozenset([1, 2, 3, 4, 5])

# 函数式列表操作
class FunctionalList:
    """函数式列表实现"""
    
    def __init__(self, items: List[Any]):
        self._items = items.copy()  # 创建副本
    
    def map(self, func: Callable[[Any], Any]) -> 'FunctionalList':
        """映射操作"""
        return FunctionalList([func(item) for item in self._items])
    
    def filter(self, predicate: Callable[[Any], bool]) -> 'FunctionalList':
        """过滤操作"""
        return FunctionalList([item for item in self._items if predicate(item)])
    
    def reduce(self, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
        """归约操作"""
        if initial is None:
            return reduce(func, self._items)
        return reduce(func, self._items, initial)
    
    def flat_map(self, func: Callable[[Any], List[Any]]) -> 'FunctionalList':
        """扁平映射"""
        result = []
        for item in self._items:
            result.extend(func(item))
        return FunctionalList(result)
    
    def __iter__(self) -> Iterator[Any]:
        return iter(self._items)
    
    def __str__(self) -> str:
        return str(self._items)

# 使用示例
numbers = FunctionalList([1, 2, 3, 4, 5])
result = (numbers
          .filter(lambda x: x % 2 == 0)  # 过滤偶数
          .map(lambda x: x * 2)          # 乘以2
          .reduce(lambda x, y: x + y, 0)) # 求和
print(result)  # 12 (2*2 + 4*2)
```

### 1.2.3 纯函数与副作用

**纯函数**：

```python
from typing import TypeVar, Callable
import random
import time

A = TypeVar('A')
B = TypeVar('B')

class PureFunction:
    """纯函数示例"""
    
    @staticmethod
    def add(a: int, b: int) -> int:
        """纯函数：相同输入总是产生相同输出，无副作用"""
        return a + b
    
    @staticmethod
    def multiply(a: int, b: int) -> int:
        """纯函数"""
        return a * b
    
    @staticmethod
    def compose(f: Callable[[A], B], g: Callable[[B], B]) -> Callable[[A], B]:
        """函数组合：纯函数"""
        return lambda x: g(f(x))

class ImpureFunction:
    """非纯函数示例"""
    
    def __init__(self):
        self.counter = 0
    
    def increment_counter(self) -> int:
        """非纯函数：有副作用"""
        self.counter += 1
        return self.counter
    
    def get_random_number(self) -> int:
        """非纯函数：相同输入可能产生不同输出"""
        return random.randint(1, 100)
    
    def get_current_time(self) -> float:
        """非纯函数：依赖外部状态"""
        return time.time()

# 副作用隔离
class SideEffectManager:
    """副作用管理器"""
    
    def __init__(self):
        self._effects: List[Callable[[], None]] = []
    
    def add_effect(self, effect: Callable[[], None]) -> None:
        """添加副作用"""
        self._effects.append(effect)
    
    def execute_effects(self) -> None:
        """执行所有副作用"""
        for effect in self._effects:
            effect()
        self._effects.clear()

# 函数式错误处理
from typing import Union, Optional
from dataclasses import dataclass

@dataclass
class Result(Generic[A]):
    """函数式结果类型"""
    value: Optional[A] = None
    error: Optional[str] = None
    
    @classmethod
    def success(cls, value: A) -> 'Result[A]':
        return cls(value=value)
    
    @classmethod
    def failure(cls, error: str) -> 'Result[A]':
        return cls(error=error)
    
    def is_success(self) -> bool:
        return self.error is None
    
    def is_failure(self) -> bool:
        return self.error is not None
    
    def map(self, func: Callable[[A], B]) -> 'Result[B]':
        """映射成功值"""
        if self.is_success():
            try:
                return Result.success(func(self.value))
            except Exception as e:
                return Result.failure(str(e))
        return Result.failure(self.error)
    
    def flat_map(self, func: Callable[[A], 'Result[B]']) -> 'Result[B]':
        """扁平映射"""
        if self.is_success():
            return func(self.value)
        return Result.failure(self.error)
    
    def get_or_else(self, default: A) -> A:
        """获取值或默认值"""
        return self.value if self.is_success() else default

# 使用示例
def safe_divide(a: float, b: float) -> Result[float]:
    """安全的除法操作"""
    if b == 0:
        return Result.failure("Division by zero")
    return Result.success(a / b)

def safe_sqrt(x: float) -> Result[float]:
    """安全的平方根操作"""
    if x < 0:
        return Result.failure("Cannot take square root of negative number")
    return Result.success(x ** 0.5)

# 链式操作
result = (safe_divide(10, 2)
          .flat_map(safe_sqrt)
          .map(lambda x: x * 2))
print(result)  # Result(value=6.324555320336759)
```

## 1.3 并发编程理论

### 1.3.1 异步编程模型

**async/await模式**：

```python
import asyncio
from typing import AsyncIterator, AsyncGenerator
from contextlib import asynccontextmanager
import aiohttp
import time

class AsyncProgramming:
    """异步编程示例"""
    
    @staticmethod
    async def async_function() -> str:
        """异步函数"""
        await asyncio.sleep(1)  # 模拟I/O操作
        return "Async result"
    
    @staticmethod
    async def concurrent_tasks() -> List[str]:
        """并发任务"""
        tasks = [
            AsyncProgramming.async_function(),
            AsyncProgramming.async_function(),
            AsyncProgramming.async_function()
        ]
        results = await asyncio.gather(*tasks)
        return results
    
    @staticmethod
    async def async_generator() -> AsyncGenerator[int, None]:
        """异步生成器"""
        for i in range(5):
            await asyncio.sleep(0.1)
            yield i
    
    @staticmethod
    async def async_context_manager():
        """异步上下文管理器"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.github.com') as response:
                return await response.json()

# 异步迭代器
class AsyncIterator:
    """异步迭代器"""
    
    def __init__(self, items: List[Any]):
        self.items = items
        self.index = 0
    
    def __aiter__(self) -> 'AsyncIterator':
        return self
    
    async def __anext__(self) -> Any:
        if self.index >= len(self.items):
            raise StopAsyncIteration
        
        item = self.items[self.index]
        self.index += 1
        
        # 模拟异步操作
        await asyncio.sleep(0.1)
        return item

# 异步队列
class AsyncQueue:
    """异步队列"""
    
    def __init__(self, maxsize: int = 0):
        self._queue = asyncio.Queue(maxsize=maxsize)
    
    async def put(self, item: Any) -> None:
        """放入项目"""
        await self._queue.put(item)
    
    async def get(self) -> Any:
        """获取项目"""
        return await self._queue.get()
    
    async def join(self) -> None:
        """等待所有项目被处理"""
        await self._queue.join()
    
    def task_done(self) -> None:
        """标记任务完成"""
        self._queue.task_done()

# 生产者-消费者模式
async def producer(queue: AsyncQueue, items: List[Any]):
    """生产者"""
    for item in items:
        await queue.put(item)
        print(f"Produced: {item}")
        await asyncio.sleep(0.1)

async def consumer(queue: AsyncQueue, name: str):
    """消费者"""
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=1.0)
            print(f"Consumer {name} consumed: {item}")
            queue.task_done()
            await asyncio.sleep(0.2)
        except asyncio.TimeoutError:
            break

async def producer_consumer_example():
    """生产者-消费者示例"""
    queue = AsyncQueue(maxsize=5)
    items = list(range(10))
    
    # 创建任务
    producer_task = asyncio.create_task(producer(queue, items))
    consumer_tasks = [
        asyncio.create_task(consumer(queue, f"Worker-{i}"))
        for i in range(3)
    ]
    
    # 等待生产者完成
    await producer_task
    
    # 等待所有项目被消费
    await queue.join()
    
    # 取消消费者任务
    for task in consumer_tasks:
        task.cancel()
    
    await asyncio.gather(*consumer_tasks, return_exceptions=True)
```

### 1.3.2 多线程编程

**线程安全**：

```python
import threading
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, Future
import queue
import time

class ThreadSafeCounter:
    """线程安全计数器"""
    
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self) -> int:
        """增加计数器"""
        with self._lock:
            self._value += 1
            return self._value
    
    def decrement(self) -> int:
        """减少计数器"""
        with self._lock:
            self._value -= 1
            return self._value
    
    @property
    def value(self) -> int:
        """获取当前值"""
        with self._lock:
            return self._value

class ThreadSafeDict:
    """线程安全字典"""
    
    def __init__(self):
        self._dict: Dict[str, Any] = {}
        self._lock = threading.RLock()  # 可重入锁
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取值"""
        with self._lock:
            return self._dict.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置值"""
        with self._lock:
            self._dict[key] = value
    
    def delete(self, key: str) -> bool:
        """删除值"""
        with self._lock:
            if key in self._dict:
                del self._dict[key]
                return True
            return False

# 线程池
class ThreadPool:
    """线程池管理器"""
    
    def __init__(self, max_workers: int = None):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def submit(self, func: Callable, *args, **kwargs) -> Future:
        """提交任务"""
        return self.executor.submit(func, *args, **kwargs)
    
    def map(self, func: Callable, *iterables) -> Iterator:
        """映射任务"""
        return self.executor.map(func, *iterables)
    
    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池"""
        self.executor.shutdown(wait=wait)

# 条件变量
class BoundedBuffer:
    """有界缓冲区"""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer: List[Any] = []
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)
    
    def put(self, item: Any) -> None:
        """放入项目"""
        with self.lock:
            while len(self.buffer) >= self.capacity:
                self.not_full.wait()
            
            self.buffer.append(item)
            self.not_empty.notify()
    
    def get(self) -> Any:
        """获取项目"""
        with self.lock:
            while len(self.buffer) == 0:
                self.not_empty.wait()
            
            item = self.buffer.pop(0)
            self.not_full.notify()
            return item

# 使用示例
def worker_function(worker_id: int, counter: ThreadSafeCounter):
    """工作函数"""
    for _ in range(1000):
        counter.increment()
    print(f"Worker {worker_id} completed")

def thread_pool_example():
    """线程池示例"""
    counter = ThreadSafeCounter()
    pool = ThreadPool(max_workers=4)
    
    # 提交任务
    futures = []
    for i in range(4):
        future = pool.submit(worker_function, i, counter)
        futures.append(future)
    
    # 等待所有任务完成
    for future in futures:
        future.result()
    
    print(f"Final counter value: {counter.value}")
    pool.shutdown()
```

### 1.3.3 多进程编程

**进程间通信**：

```python
import multiprocessing as mp
from multiprocessing import Process, Queue, Pipe, Manager, Pool
from typing import Any, List
import os

class MultiprocessingExample:
    """多进程编程示例"""
    
    @staticmethod
    def cpu_bound_task(n: int) -> int:
        """CPU密集型任务"""
        result = 0
        for i in range(n):
            result += i * i
        return result
    
    @staticmethod
    def worker_with_queue(queue: Queue, task_id: int) -> None:
        """使用队列的工作进程"""
        result = MultiprocessingExample.cpu_bound_task(1000000)
        queue.put((task_id, result))
    
    @staticmethod
    def worker_with_pipe(conn: Pipe, task_id: int) -> None:
        """使用管道的工作进程"""
        result = MultiprocessingExample.cpu_bound_task(1000000)
        conn.send((task_id, result))
        conn.close()
    
    @staticmethod
    def shared_memory_worker(shared_dict: dict, key: str) -> None:
        """共享内存工作进程"""
        result = MultiprocessingExample.cpu_bound_task(100000)
        shared_dict[key] = result

# 进程池
class ProcessPool:
    """进程池管理器"""
    
    def __init__(self, processes: int = None):
        self.pool = Pool(processes=processes)
    
    def map(self, func: Callable, iterable: List[Any]) -> List[Any]:
        """映射任务到进程池"""
        return self.pool.map(func, iterable)
    
    def apply_async(self, func: Callable, args: tuple = ()) -> mp.pool.AsyncResult:
        """异步应用函数"""
        return self.pool.apply_async(func, args)
    
    def close(self) -> None:
        """关闭进程池"""
        self.pool.close()
    
    def join(self) -> None:
        """等待所有进程完成"""
        self.pool.join()

# 使用示例
def multiprocessing_example():
    """多进程示例"""
    # 1. 使用队列
    queue = Queue()
    processes = []
    
    for i in range(4):
        p = Process(target=MultiprocessingExample.worker_with_queue, args=(queue, i))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    # 收集结果
    results = []
    while not queue.empty():
        results.append(queue.get())
    
    print(f"Queue results: {results}")
    
    # 2. 使用管道
    parent_conn, child_conn = Pipe()
    p = Process(target=MultiprocessingExample.worker_with_pipe, args=(child_conn, 0))
    p.start()
    p.join()
    
    result = parent_conn.recv()
    print(f"Pipe result: {result}")
    
    # 3. 使用共享内存
    with Manager() as manager:
        shared_dict = manager.dict()
        processes = []
        
        for i in range(4):
            p = Process(target=MultiprocessingExample.shared_memory_worker, 
                       args=(shared_dict, f"worker_{i}"))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
        
        print(f"Shared memory results: {dict(shared_dict)}")
    
    # 4. 使用进程池
    pool = ProcessPool(processes=4)
    numbers = [1000000, 2000000, 3000000, 4000000]
    
    results = pool.map(MultiprocessingExample.cpu_bound_task, numbers)
    print(f"Process pool results: {results}")
    
    pool.close()
    pool.join()
```

## 1.4 元编程理论

### 1.4.1 装饰器模式

**装饰器系统**：

```python
from typing import TypeVar, Callable, Any
from functools import wraps
import time
import logging

F = TypeVar('F', bound=Callable[..., Any])

class DecoratorSystem:
    """装饰器系统"""
    
    @staticmethod
    def simple_decorator(func: F) -> F:
        """简单装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__}")
            result = func(*args, **kwargs)
            print(f"Finished {func.__name__}")
            return result
        return wrapper
    
    @staticmethod
    def parameterized_decorator(prefix: str = ""):
        """参数化装饰器"""
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"{prefix} Calling {func.__name__}")
                result = func(*args, **kwargs)
                print(f"{prefix} Finished {func.__name__}")
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def class_decorator(cls: type) -> type:
        """类装饰器"""
        # 添加新方法
        def new_method(self):
            return f"New method in {cls.__name__}"
        
        cls.new_method = new_method
        return cls
    
    @staticmethod
    def method_decorator(func: F) -> F:
        """方法装饰器"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"Method {func.__name__} called on {type(self).__name__}")
            return func(self, *args, **kwargs)
        return wrapper

# 实用装饰器
class UtilityDecorators:
    """实用装饰器集合"""
    
    @staticmethod
    def timer(func: F) -> F:
        """计时装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end - start:.4f} seconds")
            return result
        return wrapper
    
    @staticmethod
    def retry(max_attempts: int = 3, delay: float = 1.0):
        """重试装饰器"""
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            raise e
                        print(f"Attempt {attempt + 1} failed: {e}")
                        time.sleep(delay)
                return None
            return wrapper
        return decorator
    
    @staticmethod
    def cache(func: F) -> F:
        """缓存装饰器"""
        cache_dict = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key not in cache_dict:
                cache_dict[key] = func(*args, **kwargs)
            return cache_dict[key]
        return wrapper
    
    @staticmethod
    def validate_input(*validators: Callable[[Any], bool]):
        """输入验证装饰器"""
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 验证参数
                for i, validator in enumerate(validators):
                    if i < len(args) and not validator(args[i]):
                        raise ValueError(f"Argument {i} failed validation")
                return func(*args, **kwargs)
            return wrapper
        return decorator

# 使用示例
@UtilityDecorators.timer
@UtilityDecorators.retry(max_attempts=3)
def risky_function(x: int) -> int:
    """有风险的函数"""
    if x < 0:
        raise ValueError("Negative number")
    return x * 2

@UtilityDecorators.cache
def expensive_function(n: int) -> int:
    """昂贵的计算函数"""
    time.sleep(1)  # 模拟昂贵计算
    return n * n

@UtilityDecorators.validate_input(lambda x: x > 0, lambda x: isinstance(x, str))
def validated_function(number: int, text: str) -> str:
    """带验证的函数"""
    return f"{text}: {number}"
```

### 1.4.2 元类编程

**元类系统**：

```python
from typing import Dict, Any, Type
from abc import ABCMeta

class MetaClass(type):
    """自定义元类"""
    
    def __new__(mcs, name: str, bases: tuple, namespace: Dict[str, Any]) -> type:
        """创建类时调用"""
        print(f"Creating class: {name}")
        
        # 添加类属性
        namespace['_created_by_metaclass'] = True
        
        # 验证类定义
        if 'required_method' not in namespace:
            raise TypeError(f"Class {name} must define 'required_method'")
        
        return super().__new__(mcs, name, bases, namespace)
    
    def __init__(cls, name: str, bases: tuple, namespace: Dict[str, Any]) -> None:
        """初始化类时调用"""
        super().__init__(name, bases, namespace)
        print(f"Initialized class: {name}")
    
    def __call__(cls, *args, **kwargs) -> Any:
        """创建实例时调用"""
        print(f"Creating instance of {cls.__name__}")
        instance = super().__call__(*args, **kwargs)
        print(f"Created instance: {instance}")
        return instance

class AutoRegisterMeta(type):
    """自动注册元类"""
    
    _registry: Dict[str, type] = {}
    
    def __new__(mcs, name: str, bases: tuple, namespace: Dict[str, Any]) -> type:
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 自动注册类
        if 'auto_register' in namespace and namespace['auto_register']:
            mcs._registry[name] = cls
        
        return cls
    
    @classmethod
    def get_registered_classes(cls) -> Dict[str, type]:
        """获取注册的类"""
        return cls._registry.copy()

# 使用元类
class MyClass(metaclass=MetaClass):
    """使用自定义元类的类"""
    
    def required_method(self):
        return "Required method implemented"

class AutoRegisteredClass(metaclass=AutoRegisterMeta):
    """自动注册的类"""
    auto_register = True

# 描述符元类
class DescriptorMeta(type):
    """描述符元类"""
    
    def __new__(mcs, name: str, bases: tuple, namespace: Dict[str, Any]) -> type:
        # 处理描述符
        for key, value in namespace.items():
            if hasattr(value, '__get__'):
                # 这是一个描述符
                print(f"Found descriptor: {key}")
        
        return super().__new__(mcs, name, bases, namespace)

# 单例元类
class SingletonMeta(type):
    """单例元类"""
    
    _instances: Dict[type, Any] = {}
    
    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    """单例类"""
    pass

# 抽象基类元类
class AbstractMeta(ABCMeta):
    """抽象基类元类"""
    
    def __new__(mcs, name: str, bases: tuple, namespace: Dict[str, Any]) -> type:
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 检查抽象方法
        abstract_methods = set()
        for base in bases:
            if hasattr(base, '__abstractmethods__'):
                abstract_methods.update(base.__abstractmethods__)
        
        for name, value in namespace.items():
            if getattr(value, '__isabstractmethod__', False):
                abstract_methods.add(name)
        
        cls.__abstractmethods__ = frozenset(abstract_methods)
        return cls

class AbstractBase(metaclass=AbstractMeta):
    """抽象基类"""
    
    @abstractmethod
    def abstract_method(self) -> str:
        """抽象方法"""
        pass
```

## 1.5 总结

Python语言理论为软件工程提供了**强大的编程范式**：

1. **动态类型系统**: 提供灵活的类型注解和类型检查
2. **函数式编程**: 支持高阶函数、不可变数据和纯函数
3. **并发编程**: 提供异步、多线程、多进程编程模型
4. **元编程**: 支持装饰器、元类等高级编程技术

这些理论特性使Python成为现代软件开发的强大工具，特别适合快速原型开发、数据科学、Web开发等领域。
