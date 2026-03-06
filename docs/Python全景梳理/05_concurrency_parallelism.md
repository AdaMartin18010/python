# Python 并发并行同步异步模式完全指南

> 本文档全面梳理Python中的并发、并行、同步和异步编程模式，包含概念定义、实现原理、完整代码示例、正例反例分析、性能对比和适用场景。

---

## 目录

- [Python 并发并行同步异步模式完全指南](#python-并发并行同步异步模式完全指南)
  - [目录](#目录)
  - [第一部分：线程模型](#第一部分线程模型)
    - [1.1 threading模块](#11-threading模块)
      - [概念定义](#概念定义)
      - [实现原理](#实现原理)
      - [基础示例：Thread类](#基础示例thread类)
      - [正例：正确创建和启动线程](#正例正确创建和启动线程)
      - [反例：错误使用线程](#反例错误使用线程)
    - [1.2 GIL的影响与绕过](#12-gil的影响与绕过)
      - [概念定义](#概念定义-1)
      - [实现原理](#实现原理-1)
      - [GIL影响的实验](#gil影响的实验)
      - [绕过GIL的方法](#绕过gil的方法)
      - [多线程适用场景](#多线程适用场景)
    - [1.3 线程安全](#13-线程安全)
      - [概念定义](#概念定义-2)
      - [原子操作](#原子操作)
      - [线程本地存储](#线程本地存储)
      - [线程安全的计数器实现](#线程安全的计数器实现)
  - [第二部分：进程模型](#第二部分进程模型)
    - [2.1 multiprocessing模块](#21-multiprocessing模块)
      - [概念定义](#概念定义-3)
      - [实现原理](#实现原理-2)
      - [Process类基础示例](#process类基础示例)
      - [进程池（Pool）](#进程池pool)
      - [进程间通信（Queue, Pipe）](#进程间通信queue-pipe)
      - [共享内存（Value, Array, Manager）](#共享内存value-array-manager)
    - [2.2 concurrent.futures](#22-concurrentfutures)
      - [概念定义](#概念定义-4)
      - [实现原理](#实现原理-3)
      - [ThreadPoolExecutor](#threadpoolexecutor)
      - [ProcessPoolExecutor](#processpoolexecutor)
      - [正例与反例对比](#正例与反例对比)
  - [第三部分：异步编程](#第三部分异步编程)
    - [3.1 asyncio核心概念](#31-asyncio核心概念)
      - [概念定义](#概念定义-5)
      - [实现原理](#实现原理-4)
      - [事件循环](#事件循环)
      - [协程（Coroutine）](#协程coroutine)
      - [Task和Future](#task和future)
    - [3.2 async/await语法](#32-asyncawait语法)
      - [异步函数定义](#异步函数定义)
      - [异步迭代器](#异步迭代器)
      - [异步上下文管理器](#异步上下文管理器)
    - [3.3 异步IO操作](#33-异步io操作)
      - [aiohttp](#aiohttp)
      - [asyncio同步原语](#asyncio同步原语)
      - [异步与同步代码交互](#异步与同步代码交互)
  - [第四部分：并发原语](#第四部分并发原语)
    - [4.1 锁机制](#41-锁机制)
      - [概念定义](#概念定义-6)
      - [Lock（互斥锁）](#lock互斥锁)
      - [RLock（可重入锁）](#rlock可重入锁)
      - [Semaphore（信号量）](#semaphore信号量)
      - [BoundedSemaphore](#boundedsemaphore)
    - [4.2 事件机制](#42-事件机制)
      - [Event](#event)
      - [Condition](#condition)
      - [Barrier](#barrier)
    - [4.3 队列](#43-队列)
      - [Queue](#queue)
      - [PriorityQueue](#priorityqueue)
      - [LifoQueue](#lifoqueue)
  - [第五部分：并发模式](#第五部分并发模式)
    - [5.1 生产者-消费者模式](#51-生产者-消费者模式)
      - [概念定义](#概念定义-7)
      - [实现原理](#实现原理-5)
      - [正例：正确实现](#正例正确实现)
      - [反例：错误实现](#反例错误实现)
    - [5.2 读者-写者模式](#52-读者-写者模式)
      - [概念定义](#概念定义-8)
      - [实现原理](#实现原理-6)
      - [正例：正确实现](#正例正确实现-1)
      - [写者优先实现](#写者优先实现)
    - [5.3 工作队列模式](#53-工作队列模式)
      - [概念定义](#概念定义-9)
      - [正例：正确实现](#正例正确实现-2)
    - [5.4 MapReduce模式](#54-mapreduce模式)
      - [概念定义](#概念定义-10)
      - [正例：正确实现](#正例正确实现-3)
    - [5.5 演员模型（Actor Model）](#55-演员模型actor-model)
      - [概念定义](#概念定义-11)
      - [正例：正确实现](#正例正确实现-4)
  - [第六部分：死锁与竞态条件](#第六部分死锁与竞态条件)
    - [6.1 死锁的四个条件](#61-死锁的四个条件)
      - [概念定义](#概念定义-12)
      - [死锁的四个必要条件](#死锁的四个必要条件)
      - [死锁示例代码](#死锁示例代码)
    - [6.2 死锁检测与避免](#62-死锁检测与避免)
      - [死锁避免策略](#死锁避免策略)
    - [6.3 竞态条件分析](#63-竞态条件分析)
      - [概念定义](#概念定义-13)
      - [竞态条件示例](#竞态条件示例)
      - [常见的竞态条件场景](#常见的竞态条件场景)
    - [6.4 线程转储分析](#64-线程转储分析)
      - [概念定义](#概念定义-14)
      - [获取线程转储](#获取线程转储)
      - [死锁检测代码](#死锁检测代码)
  - [总结](#总结)
    - [并发模型对比](#并发模型对比)
    - [选择指南](#选择指南)
    - [最佳实践](#最佳实践)

## 第一部分：线程模型

### 1.1 threading模块

#### 概念定义

`threading`模块是Python标准库中用于线程编程的核心模块。线程是操作系统能够进行运算调度的最小单位，它被包含在进程之中，是进程中的实际运作单位。同一进程中的多个线程共享该进程的资源（内存空间、文件描述符等），但拥有独立的执行栈和程序计数器。

#### 实现原理

Python的`threading`模块基于底层操作系统的原生线程实现：

- **Linux**: 基于POSIX线程（pthread）
- **Windows**: 基于Windows线程API
- **macOS**: 基于pthread

线程创建涉及系统调用，由操作系统内核进行调度。Python解释器通过GIL（全局解释器锁）来管理线程对Python对象的访问。

#### 基础示例：Thread类

```python
import threading
import time

def worker_function(name, delay):
    """工作线程函数"""
    print(f"[线程-{name}] 开始执行，线程ID: {threading.current_thread().ident}")
    time.sleep(delay)
    print(f"[线程-{name}] 执行完成，耗时 {delay} 秒")

# 创建并启动线程
print("=" * 50)
print("基础线程创建示例")
print("=" * 50)

threads = []
for i in range(3):
    t = threading.Thread(
        target=worker_function,
        args=(f"Worker-{i}", i + 1),
        name=f"MyThread-{i}"
    )
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print("所有线程执行完成")
```

#### 正例：正确创建和启动线程

```python
import threading
import time

class CorrectThreadUsage:
    """正确使用线程的示例"""

    def __init__(self):
        self.results = []
        self.lock = threading.Lock()

    def compute_task(self, n):
        """计算任务"""
        result = sum(i ** 2 for i in range(n))
        with self.lock:
            self.results.append((n, result))
        print(f"计算完成: sum of squares up to {n} = {result}")

    def run(self):
        """运行多线程任务"""
        threads = []
        numbers = [1000000, 2000000, 1500000, 3000000]

        start_time = time.time()

        # 创建线程
        for n in numbers:
            t = threading.Thread(target=self.compute_task, args=(n,))
            threads.append(t)
            t.start()

        # 等待所有线程完成
        for t in threads:
            t.join()

        elapsed = time.time() - start_time
        print(f"\n总耗时: {elapsed:.2f} 秒")
        print(f"结果数量: {len(self.results)}")

if __name__ == "__main__":
    demo = CorrectThreadUsage()
    demo.run()
```

#### 反例：错误使用线程

```python
import threading

class IncorrectThreadUsage:
    """错误使用线程的示例 - 竞态条件"""

    def __init__(self):
        self.counter = 0
        # 错误：没有使用锁保护共享变量

    def increment(self):
        """非线程安全的增量操作"""
        # 读取-修改-写入操作不是原子的
        current = self.counter      # 读取
        # 此处可能发生上下文切换！
        self.counter = current + 1  # 修改并写入

    def run(self):
        """演示竞态条件"""
        threads = []

        # 创建100个线程，每个增加1000次
        for _ in range(100):
            t = threading.Thread(target=lambda: [self.increment() for _ in range(1000)])
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f"期望结果: 100000")
        print(f"实际结果: {self.counter}")
        print(f"丢失更新: {100000 - self.counter}")

# 运行反例（可能每次结果都不同）
# demo = IncorrectThreadUsage()
# demo.run()
```

**问题分析**：

- `self.counter = self.counter + 1` 不是原子操作
- 包含三个步骤：读取、计算、写入
- 线程切换可能发生在任何步骤之间
- 导致更新丢失（Lost Update）问题

---

### 1.2 GIL的影响与绕过

#### 概念定义

**GIL（Global Interpreter Lock，全局解释器锁）** 是CPython解释器中的一个互斥锁，它确保任何时候只有一个线程在执行Python字节码。GIL的存在使得Python多线程在CPU密集型任务上无法真正实现并行执行。

#### 实现原理

```
┌─────────────────────────────────────────┐
│           Python 进程                    │
│  ┌─────────────────────────────────┐    │
│  │         GIL (互斥锁)              │    │
│  └─────────────────────────────────┘    │
│         │                               │
│    ┌────┴────┬────────┬────────┐       │
│    ▼         ▼        ▼        ▼       │
│  线程1     线程2    线程3    线程4      │
│  (执行中)  (等待)   (等待)   (等待)     │
└─────────────────────────────────────────┘
```

GIL的工作机制：

1. 线程获取GIL后才能执行Python字节码
2. 执行一定数量字节码或遇到IO操作时释放GIL
3. 其他等待的线程竞争获取GIL
4. 操作系统调度决定哪个线程获得GIL

#### GIL影响的实验

```python
import threading
import multiprocessing
import time

def cpu_bound_task(n):
    """CPU密集型任务"""
    count = 0
    for i in range(n):
        count += i ** 2
    return count

def io_bound_task(n):
    """IO密集型任务"""
    time.sleep(n)
    return f"Slept for {n} seconds"

def compare_execution():
    """对比单线程、多线程、多进程执行效率"""

    # CPU密集型任务参数
    cpu_task_size = 10_000_000
    num_tasks = 4

    print("=" * 60)
    print("CPU密集型任务对比")
    print("=" * 60)

    # 1. 单线程执行
    start = time.time()
    for _ in range(num_tasks):
        cpu_bound_task(cpu_task_size)
    single_thread_time = time.time() - start
    print(f"单线程耗时: {single_thread_time:.2f} 秒")

    # 2. 多线程执行（受GIL影响）
    start = time.time()
    threads = []
    for _ in range(num_tasks):
        t = threading.Thread(target=cpu_bound_task, args=(cpu_task_size,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    multi_thread_time = time.time() - start
    print(f"多线程耗时: {multi_thread_time:.2f} 秒")
    print(f"加速比: {single_thread_time / multi_thread_time:.2f}x")

    # 3. 多进程执行（绕过GIL）
    start = time.time()
    processes = []
    for _ in range(num_tasks):
        p = multiprocessing.Process(target=cpu_bound_task, args=(cpu_task_size,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    multi_process_time = time.time() - start
    print(f"多进程耗时: {multi_process_time:.2f} 秒")
    print(f"加速比: {single_thread_time / multi_process_time:.2f}x")

    print("\n" + "=" * 60)
    print("IO密集型任务对比")
    print("=" * 60)

    io_task_duration = 1

    # IO密集型 - 单线程
    start = time.time()
    for _ in range(num_tasks):
        io_bound_task(io_task_duration)
    single_io_time = time.time() - start
    print(f"单线程耗时: {single_io_time:.2f} 秒")

    # IO密集型 - 多线程（GIL在IO时释放）
    start = time.time()
    threads = []
    for _ in range(num_tasks):
        t = threading.Thread(target=io_bound_task, args=(io_task_duration,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    multi_io_thread_time = time.time() - start
    print(f"多线程耗时: {multi_io_thread_time:.2f} 秒")
    print(f"加速比: {single_io_time / multi_io_thread_time:.2f}x")

if __name__ == "__main__":
    compare_execution()
```

#### 绕过GIL的方法

```python
# 方法1: 使用多进程
import multiprocessing

def parallel_with_processes():
    """使用多进程绕过GIL"""
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(cpu_bound_task, [10_000_000] * 4)
    return results

# 方法2: 使用C扩展（如NumPy）
import numpy as np

def use_numpy():
    """NumPy在C层面释放GIL"""
    # NumPy的矩阵运算在C层面执行，不受GIL限制
    arr = np.random.rand(10000, 10000)
    result = np.dot(arr, arr.T)  # 矩阵乘法在C层面并行
    return result

# 方法3: 使用Cython并释放GIL
# Cython代码示例（需要保存为 .pyx 文件）:
cython_code = """
# example.pyx
from cython.parallel import prange

def parallel_sum(double[:] arr):
    cdef:
        double total = 0
        Py_ssize_t i

    with nogil:  # 释放GIL
        for i in prange(arr.shape[0], schedule='static'):
            total += arr[i]

    return total
"""

# 方法4: 使用子解释器（Python 3.12+）
import sys
if sys.version_info >= (3, 12):
    import _xxsubinterpreters as subinterpreters
    # 每个子解释器有自己的GIL
```

#### 多线程适用场景

| 场景 | 适用性 | 原因 |
|------|--------|------|
| IO密集型任务 | ⭐⭐⭐⭐⭐ | GIL在IO时释放，线程可并发 |
| 网络请求 | ⭐⭐⭐⭐⭐ | 等待响应时其他线程可执行 |
| 文件操作 | ⭐⭐⭐⭐ | 磁盘IO时释放GIL |
| GUI应用 | ⭐⭐⭐⭐⭐ | 保持界面响应，后台处理任务 |
| CPU密集型计算 | ⭐ | 受GIL限制，无法真正并行 |
| 数值计算 | ⭐⭐ | 使用NumPy等库可部分绕过 |

---

### 1.3 线程安全

#### 概念定义

**线程安全** 是指多线程环境下，代码能够正确处理多个线程同时访问共享数据的情况，保证数据的一致性和正确性。

#### 原子操作

```python
import threading
import dis

# 查看字节码，理解原子性
def check_atomicity():
    """检查操作的原子性"""

    print("=" * 60)
    print("操作原子性分析")
    print("=" * 60)

    # 原子操作（线程安全）
    print("\n1. 原子操作（线程安全）:")
    print("   - list.append(x)")
    print("   - list.pop()")
    print("   - dict[key] = value")
    print("   - set.add(x)")
    print("   - 变量赋值（简单类型）")

    # 非原子操作（需要锁保护）
    print("\n2. 非原子操作（需要锁保护）:")
    print("   - i += 1")
    print("   - dict[key] += 1")
    print("   - list[index] += 1")
    print("   - 复合赋值操作")

    # 字节码分析
    print("\n3. 字节码分析:")
    print("-" * 40)

    def simple_increment():
        x = 0
        x = x + 1

    print("代码: x = x + 1")
    print("字节码:")
    dis.dis(simple_increment)

    print("\n分析:")
    print("  LOAD_FAST    (读取x)")
    print("  LOAD_CONST   (加载1)")
    print("  BINARY_ADD   (加法)")
    print("  STORE_FAST   (存储结果)")
    print("  以上4步不是原子的，线程可能在任何步骤切换")

check_atomicity()
```

#### 线程本地存储

```python
import threading

# 线程本地存储示例
thread_local = threading.local()

def thread_worker(name):
    """每个线程有自己的独立存储"""
    # 设置线程本地变量
    thread_local.name = name
    thread_local.data = []

    # 模拟工作
    for i in range(3):
        thread_local.data.append(f"{name}-data-{i}")

    print(f"线程 {name}:")
    print(f"  thread_local.name = {thread_local.name}")
    print(f"  thread_local.data = {thread_local.data}")
    print(f"  id(thread_local) = {id(thread_local)}")

def demonstrate_thread_local():
    """演示线程本地存储"""
    print("=" * 60)
    print("线程本地存储 (threading.local)")
    print("=" * 60)

    threads = []
    for name in ["Alpha", "Beta", "Gamma"]:
        t = threading.Thread(target=thread_worker, args=(name,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n注意: 每个线程看到的thread_local是独立的")

demonstrate_thread_local()
```

#### 线程安全的计数器实现

```python
import threading
import time

class ThreadSafeCounter:
    """线程安全的计数器 - 正确使用锁"""

    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        """线程安全的增量"""
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self):
        """线程安全的减量"""
        with self._lock:
            self._value -= 1
            return self._value

    @property
    def value(self):
        """获取当前值（线程安全）"""
        with self._lock:
            return self._value

class UnsafeCounter:
    """非线程安全的计数器 - 反例"""

    def __init__(self):
        self._value = 0

    def increment(self):
        """非线程安全"""
        self._value += 1

    @property
    def value(self):
        return self._value

def test_counter(counter_class, name):
    """测试计数器"""
    print(f"\n测试 {name}:")
    counter = counter_class()

    def worker():
        for _ in range(100000):
            counter.increment()

    threads = [threading.Thread(target=worker) for _ in range(10)]

    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.time() - start

    expected = 100000 * 10
    actual = counter.value
    print(f"  期望: {expected}, 实际: {actual}, 丢失: {expected - actual}")
    print(f"  耗时: {elapsed:.3f} 秒")

# 运行测试
print("=" * 60)
print("线程安全计数器对比测试")
print("=" * 60)
test_counter(ThreadSafeCounter, "ThreadSafeCounter")
test_counter(UnsafeCounter, "UnsafeCounter")
```

---

## 第二部分：进程模型

### 2.1 multiprocessing模块

#### 概念定义

`multiprocessing`模块是Python标准库中用于进程编程的模块。与线程不同，进程拥有独立的内存空间，每个进程都有自己的Python解释器和GIL，因此可以实现真正的并行计算。

#### 实现原理

```
┌─────────────────────────────────────────────────────────┐
│                    操作系统                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   进程 P1    │  │   进程 P2    │  │   进程 P3    │     │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │     │
│  │ │  GIL    │ │  │ │  GIL    │ │  │ │  GIL    │ │     │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │     │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │     │
│  │ │ 内存空间 │ │  │ │ 内存空间 │ │  │ │ 内存空间 │ │     │
│  │ │(独立的) │ │  │ │(独立的) │ │  │ │(独立的) │ │     │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

进程创建方式：

- **spawn**（Windows/macOS默认）：启动全新的Python解释器进程
- **fork**（Linux默认）：复制父进程，共享代码段

#### Process类基础示例

```python
import multiprocessing
import time
import os

def worker_process(name, data):
    """工作进程函数"""
    pid = os.getpid()
    ppid = os.getppid()
    print(f"[进程-{name}] PID: {pid}, PPID: {ppid}")
    print(f"[进程-{name}] 接收数据: {data}")
    time.sleep(2)
    result = sum(data)
    print(f"[进程-{name}] 计算结果: {result}")
    return result

def basic_process_demo():
    """基础进程创建示例"""
    print("=" * 60)
    print("基础进程创建示例")
    print("=" * 60)

    # 创建进程
    p1 = multiprocessing.Process(
        target=worker_process,
        args=("Worker-1", [1, 2, 3, 4, 5]),
        name="MyProcess-1"
    )
    p2 = multiprocessing.Process(
        target=worker_process,
        args=("Worker-2", [10, 20, 30]),
        name="MyProcess-2"
    )

    # 启动进程
    p1.start()
    p2.start()

    # 等待进程完成
    p1.join()
    p2.join()

    print("所有进程执行完成")

if __name__ == "__main__":
    basic_process_demo()
```

#### 进程池（Pool）

```python
import multiprocessing
import time

def cpu_intensive_task(n):
    """CPU密集型任务"""
    return sum(i ** 2 for i in range(n))

def demonstrate_pool():
    """演示进程池的使用"""
    print("=" * 60)
    print("进程池 (Pool) 演示")
    print("=" * 60)

    # 任务列表
    tasks = [1_000_000, 2_000_000, 1_500_000, 3_000_000, 2_500_000]

    # 方法1: map - 阻塞式，保持顺序
    print("\n1. 使用 pool.map():")
    start = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(cpu_intensive_task, tasks)
    print(f"   结果: {results}")
    print(f"   耗时: {time.time() - start:.2f} 秒")

    # 方法2: imap - 惰性求值，保持顺序
    print("\n2. 使用 pool.imap():")
    start = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        for i, result in enumerate(pool.imap(cpu_intensive_task, tasks)):
            print(f"   任务 {i}: {result}")
    print(f"   耗时: {time.time() - start:.2f} 秒")

    # 方法3: imap_unordered - 最快完成先返回
    print("\n3. 使用 pool.imap_unordered():")
    start = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        for result in pool.imap_unordered(cpu_intensive_task, tasks):
            print(f"   结果: {result}")
    print(f"   耗时: {time.time() - start:.2f} 秒")

    # 方法4: apply_async - 异步提交
    print("\n4. 使用 pool.apply_async():")
    start = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        async_results = [pool.apply_async(cpu_intensive_task, (task,)) for task in tasks]
        results = [r.get() for r in async_results]
    print(f"   结果: {results}")
    print(f"   耗时: {time.time() - start:.2f} 秒")

demonstrate_pool()
```

#### 进程间通信（Queue, Pipe）

```python
import multiprocessing
import time

def producer(queue, items):
    """生产者进程"""
    for item in items:
        print(f"[生产者] 生产: {item}")
        queue.put(item)
        time.sleep(0.1)
    print("[生产者] 生产完成，发送结束信号")
    queue.put(None)  # 结束信号

def consumer(queue):
    """消费者进程"""
    while True:
        item = queue.get()
        if item is None:
            print("[消费者] 收到结束信号")
            break
        print(f"[消费者] 消费: {item}")
        time.sleep(0.2)

def demonstrate_queue():
    """演示Queue进程间通信"""
    print("=" * 60)
    print("进程间通信 - Queue")
    print("=" * 60)

    # 创建队列
    queue = multiprocessing.Queue(maxsize=10)

    # 创建生产者和消费者进程
    items = list(range(10))
    p_producer = multiprocessing.Process(target=producer, args=(queue, items))
    p_consumer = multiprocessing.Process(target=consumer, args=(queue,))

    # 启动进程
    p_consumer.start()
    p_producer.start()

    # 等待完成
    p_producer.join()
    p_consumer.join()

    print("通信完成")

# Pipe通信示例
def sender_pipe(conn, messages):
    """发送方"""
    for msg in messages:
        print(f"[发送方] 发送: {msg}")
        conn.send(msg)
        time.sleep(0.1)
    conn.close()

def receiver_pipe(conn):
    """接收方"""
    while True:
        try:
            msg = conn.recv()
            print(f"[接收方] 接收: {msg}")
        except EOFError:
            print("[接收方] 连接关闭")
            break

def demonstrate_pipe():
    """演示Pipe进程间通信"""
    print("\n" + "=" * 60)
    print("进程间通信 - Pipe")
    print("=" * 60)

    # 创建管道
    parent_conn, child_conn = multiprocessing.Pipe()

    # 创建进程
    messages = ["Hello", "World", "From", "Pipe"]
    p_sender = multiprocessing.Process(target=sender_pipe, args=(child_conn, messages))

    p_sender.start()
    receiver_pipe(parent_conn)
    p_sender.join()

demonstrate_queue()
demonstrate_pipe()
```

#### 共享内存（Value, Array, Manager）

```python
import multiprocessing
import time

def increment_shared_value(shared_val, lock, n):
    """增加共享值"""
    for _ in range(n):
        with lock:
            shared_val.value += 1

def modify_shared_array(shared_arr):
    """修改共享数组"""
    for i in range(len(shared_arr)):
        shared_arr[i] = i ** 2

def demonstrate_shared_memory():
    """演示共享内存"""
    print("=" * 60)
    print("共享内存 - Value 和 Array")
    print("=" * 60)

    # 使用 Value 共享单个值
    print("\n1. Value 共享示例:")
    shared_val = multiprocessing.Value('i', 0)  # 'i' 表示整数
    lock = multiprocessing.Lock()

    processes = [
        multiprocessing.Process(target=increment_shared_value,
                               args=(shared_val, lock, 10000))
        for _ in range(4)
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(f"   期望: 40000, 实际: {shared_val.value}")

    # 使用 Array 共享数组
    print("\n2. Array 共享示例:")
    shared_arr = multiprocessing.Array('i', [0] * 10)

    p = multiprocessing.Process(target=modify_shared_array, args=(shared_arr,))
    p.start()
    p.join()

    print(f"   数组内容: {list(shared_arr)}")

def manager_worker(d, l, n):
    """Manager工作函数"""
    d[n] = n ** 2
    l.append(n)

def demonstrate_manager():
    """演示Manager共享复杂数据"""
    print("\n" + "=" * 60)
    print("共享内存 - Manager")
    print("=" * 60)

    with multiprocessing.Manager() as manager:
        # 创建共享对象
        shared_dict = manager.dict()
        shared_list = manager.list()

        # 创建多个进程
        processes = [
            multiprocessing.Process(target=manager_worker,
                                   args=(shared_dict, shared_list, i))
            for i in range(5)
        ]

        for p in processes:
            p.start()
        for p in processes:
            p.join()

        print(f"   共享字典: {dict(shared_dict)}")
        print(f"   共享列表: {list(shared_list)}")

demonstrate_shared_memory()
demonstrate_manager()
```

---

### 2.2 concurrent.futures

#### 概念定义

`concurrent.futures`模块提供了高级接口用于异步执行可调用对象，抽象了线程池和进程池的实现细节，提供了统一的API。

#### 实现原理

```
┌─────────────────────────────────────────────────────────┐
│              concurrent.futures 架构                     │
│                                                         │
│  ┌─────────────────┐      ┌─────────────────────────┐  │
│  │   Executor      │      │       Future            │  │
│  │  (抽象接口)      |<-----│    (异步结果)            │  │
│  └────────┬────────┘      └─────────────────────────┘  │
│           │                                             │
│     ┌─────┴─────┐                                       │
│     ▼           ▼                                       │
│  ┌──────┐   ┌────────┐                                 │
│  │Thread│   │Process │                                 │
│  │Pool  │   │Pool    │                                 │
│  │Executor│  │Executor│                                 │
│  └──────┘   └────────┘                                 │
└─────────────────────────────────────────────────────────┘
```

#### ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests

def fetch_url(url):
    """获取URL内容（IO密集型）"""
    try:
        response = requests.get(url, timeout=10)
        return url, len(response.content)
    except Exception as e:
        return url, str(e)

def demonstrate_thread_pool():
    """演示ThreadPoolExecutor"""
    print("=" * 60)
    print("ThreadPoolExecutor 演示")
    print("=" * 60)

    urls = [
        "https://www.python.org",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.wikipedia.org",
    ]

    # 方法1: 使用 map
    print("\n1. 使用 executor.map():")
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(fetch_url, urls)
        for url, size in results:
            print(f"   {url}: {size} bytes")
    print(f"   耗时: {time.time() - start:.2f} 秒")

    # 方法2: 使用 submit + as_completed
    print("\n2. 使用 executor.submit() + as_completed():")
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交所有任务
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}

        # 按完成顺序处理结果
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                url, size = future.result()
                print(f"   {url}: {size} bytes")
            except Exception as e:
                print(f"   {url}: 错误 - {e}")
    print(f"   耗时: {time.time() - start:.2f} 秒")

def demonstrate_callback():
    """演示回调函数"""
    print("\n" + "=" * 60)
    print("Future 回调函数")
    print("=" * 60)

    def callback(future):
        """完成回调"""
        print(f"   任务完成，结果: {future.result()}")

    def task(n):
        time.sleep(1)
        return n ** 2

    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(task, 5)
        future2 = executor.submit(task, 10)

        # 添加回调
        future1.add_done_callback(callback)
        future2.add_done_callback(callback)

        # 等待完成
        print("等待任务完成...")
        time.sleep(2)

demonstrate_thread_pool()
demonstrate_callback()
```

#### ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import math

def is_prime(n):
    """判断是否为素数（CPU密集型）"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def count_primes(start, end):
    """计算范围内的素数数量"""
    count = 0
    for n in range(start, end):
        if is_prime(n):
            count += 1
    return count

def demonstrate_process_pool():
    """演示ProcessPoolExecutor"""
    print("=" * 60)
    print("ProcessPoolExecutor 演示")
    print("=" * 60)

    # 将任务分成4个区间
    ranges = [
        (2, 25000),
        (25000, 50000),
        (50000, 75000),
        (75000, 100000)
    ]

    # 单线程执行
    print("\n1. 单线程执行:")
    start = time.time()
    total = sum(count_primes(s, e) for s, e in ranges)
    single_time = time.time() - start
    print(f"   素数总数: {total}")
    print(f"   耗时: {single_time:.2f} 秒")

    # 使用ProcessPoolExecutor
    print("\n2. 使用 ProcessPoolExecutor:")
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda r: count_primes(*r), ranges))
        total = sum(results)
    multi_time = time.time() - start
    print(f"   素数总数: {total}")
    print(f"   耗时: {multi_time:.2f} 秒")
    print(f"   加速比: {single_time / multi_time:.2f}x")

def demonstrate_future_features():
    """演示Future的高级特性"""
    print("\n" + "=" * 60)
    print("Future 高级特性")
    print("=" * 60)

    def slow_task(n):
        time.sleep(n)
        return f"任务完成，耗时 {n} 秒"

    with ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(slow_task, 2)

        print(f"\n1. 任务状态:")
        print(f"   是否完成: {future.done()}")
        print(f"   是否取消: {future.cancelled()}")

        # 尝试取消（已开始执行的任务无法取消）
        print(f"\n2. 尝试取消: {future.cancel()}")

        # 等待结果（带超时）
        print(f"\n3. 等待结果...")
        try:
            result = future.result(timeout=3)
            print(f"   结果: {result}")
        except TimeoutError:
            print("   超时！")

        print(f"\n4. 最终状态:")
        print(f"   是否完成: {future.done()}")
        print(f"   是否取消: {future.cancelled()}")

demonstrate_process_pool()
demonstrate_future_features()
```

#### 正例与反例对比

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

# 正例：正确选择Executor类型
def correct_executor_choice():
    """正确选择Executor类型"""
    print("=" * 60)
    print("正确选择 Executor 类型")
    print("=" * 60)

    # IO密集型任务 - 使用ThreadPoolExecutor
    def io_task(url):
        import requests
        return requests.get(url, timeout=5).status_code

    # CPU密集型任务 - 使用ProcessPoolExecutor
    def cpu_task(n):
        return sum(i ** 2 for i in range(n))

    # IO密集型使用线程池
    print("\nIO密集型任务 - ThreadPoolExecutor:")
    urls = ["https://www.python.org"] * 4
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(io_task, urls))
    print(f"   结果: {results}")
    print(f"   耗时: {time.time() - start:.2f} 秒")

    # CPU密集型使用进程池
    print("\nCPU密集型任务 - ProcessPoolExecutor:")
    numbers = [1_000_000] * 4
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_task, numbers))
    print(f"   结果: {results[:2]}...")
    print(f"   耗时: {time.time() - start:.2f} 秒")

# 反例：错误选择Executor类型
def incorrect_executor_choice():
    """错误选择Executor类型 - 反例"""
    print("\n" + "=" * 60)
    print("错误选择 Executor 类型 - 反例")
    print("=" * 60)

    def cpu_task(n):
        return sum(i ** 2 for i in range(n))

    # 错误：CPU密集型任务使用ThreadPoolExecutor
    print("\n错误：CPU密集型任务使用 ThreadPoolExecutor:")
    numbers = [1_000_000] * 4
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_task, numbers))
    thread_time = time.time() - start
    print(f"   耗时: {thread_time:.2f} 秒")
    print(f"   问题：受GIL限制，无法真正并行")

    # 正确：CPU密集型任务使用ProcessPoolExecutor
    print("\n正确：CPU密集型任务使用 ProcessPoolExecutor:")
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_task, numbers))
    process_time = time.time() - start
    print(f"   耗时: {process_time:.2f} 秒")
    print(f"   加速比: {thread_time / process_time:.2f}x")

correct_executor_choice()
incorrect_executor_choice()
```

---

## 第三部分：异步编程

### 3.1 asyncio核心概念

#### 概念定义

`asyncio`是Python标准库中用于编写并发代码的模块，使用`async`/`await`语法。它基于事件循环（Event Loop）和协程（Coroutine）实现协作式多任务，特别适合IO密集型和高并发场景。

#### 实现原理

```
┌─────────────────────────────────────────────────────────┐
│                   asyncio 架构                           │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Event Loop (事件循环)                │   │
│  │                                                 │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐        │   │
│  │  │ Task 1  │  │ Task 2  │  │ Task 3  │  ...   │   │
│  │  │(等待IO) │  │(运行中) │  │(就绪)   │        │   │
│  │  └─────────┘  └─────────┘  └─────────┘        │   │
│  │                                                 │   │
│  │  ┌─────────────────────────────────────────┐   │   │
│  │  │         Selector (IO多路复用)            │   │   │
│  │  │    epoll(Linux) / kqueue(macOS)         │   │   │
│  │  │    / IOCP(Windows)                      │   │   │
│  │  └─────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

#### 事件循环

```python
import asyncio

# 获取和运行事件循环
def basic_event_loop():
    """基础事件循环操作"""
    print("=" * 60)
    print("事件循环基础")
    print("=" * 60)

    # 获取当前事件循环
    try:
        loop = asyncio.get_event_loop()
        print(f"当前事件循环: {loop}")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print(f"创建新事件循环: {loop}")

    # 检查循环是否运行
    print(f"循环是否运行: {loop.is_running()}")
    print(f"循环是否关闭: {loop.is_closed()}")

# 协程基础
async def simple_coroutine():
    """简单协程"""
    print("协程开始执行")
    await asyncio.sleep(1)
    print("协程执行完成")
    return "Hello from coroutine"

def run_coroutine():
    """运行协程"""
    print("\n" + "=" * 60)
    print("运行协程")
    print("=" * 60)

    # 方法1: 使用 asyncio.run() (Python 3.7+)
    print("\n方法1: asyncio.run()")
    result = asyncio.run(simple_coroutine())
    print(f"结果: {result}")

    # 方法2: 使用事件循环
    print("\n方法2: 使用事件循环")
    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(simple_coroutine())
        print(f"结果: {result}")
    finally:
        loop.close()

basic_event_loop()
run_coroutine()
```

#### 协程（Coroutine）

```python
import asyncio
import time

async def coroutine_demo():
    """协程完整演示"""
    print("=" * 60)
    print("协程 (Coroutine)")
    print("=" * 60)

    # 协程定义
    async def greet(name, delay):
        print(f"[协程-{name}] 开始")
        await asyncio.sleep(delay)
        print(f"[协程-{name}] 完成，耗时 {delay} 秒")
        return f"Hello, {name}!"

    # 协程是惰性执行的
    print("\n1. 协程是惰性执行的:")
    coro = greet("World", 1)
    print(f"   创建协程对象: {coro}")
    print(f"   类型: {type(coro)}")

    # 需要 await 或事件循环来执行
    print("\n2. 执行协程:")
    result = await coro
    print(f"   结果: {result}")

    # 并发执行多个协程
    print("\n3. 并发执行多个协程:")
    start = time.time()

    # 创建多个协程
    coroutines = [
        greet("A", 1),
        greet("B", 1),
        greet("C", 1)
    ]

    # 使用 asyncio.gather 并发执行
    results = await asyncio.gather(*coroutines)
    elapsed = time.time() - start

    print(f"   结果: {results}")
    print(f"   总耗时: {elapsed:.2f} 秒 (顺序执行需要 3 秒)")

asyncio.run(coroutine_demo())
```

#### Task和Future

```python
import asyncio

async def task_future_demo():
    """Task和Future演示"""
    print("=" * 60)
    print("Task 和 Future")
    print("=" * 60)

    async def worker(name, delay):
        print(f"[Task-{name}] 开始工作")
        await asyncio.sleep(delay)
        print(f"[Task-{name}] 工作完成")
        return f"{name} 的结果"

    # 创建Task
    print("\n1. 创建 Task:")
    task1 = asyncio.create_task(worker("Task1", 1))
    task2 = asyncio.create_task(worker("Task2", 2))

    print(f"   Task1: {task1}")
    print(f"   Task2: {task2}")

    # 等待Task完成
    print("\n2. 等待 Task 完成:")
    result1 = await task1
    result2 = await task2
    print(f"   Task1 结果: {result1}")
    print(f"   Task2 结果: {result2}")

    # Task状态检查
    print("\n3. Task 状态:")
    task3 = asyncio.create_task(worker("Task3", 1))
    print(f"   是否完成: {task3.done()}")
    print(f"   是否取消: {task3.cancelled()}")

    await task3
    print(f"   完成后 - 是否完成: {task3.done()}")

    # 取消Task
    print("\n4. 取消 Task:")
    task4 = asyncio.create_task(worker("Task4", 5))
    await asyncio.sleep(0.1)  # 让任务开始
    task4.cancel()

    try:
        await task4
    except asyncio.CancelledError:
        print("   Task4 已被取消")

    print(f"   是否取消: {task4.cancelled()}")

asyncio.run(task_future_demo())
```

---

### 3.2 async/await语法

#### 异步函数定义

```python
import asyncio
import aiohttp

# 基础异步函数
async def fetch_data(url):
    """异步获取数据"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# 异步生成器
async def async_range(n):
    """异步范围生成器"""
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

# 异步上下文管理器
class AsyncResource:
    """异步资源管理器"""

    async def __aenter__(self):
        print("异步获取资源...")
        await asyncio.sleep(0.5)
        print("资源已获取")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("异步释放资源...")
        await asyncio.sleep(0.5)
        print("资源已释放")

    async def do_something(self):
        await asyncio.sleep(0.5)
        return "操作完成"

async def async_syntax_demo():
    """async/await语法演示"""
    print("=" * 60)
    print("async/await 语法")
    print("=" * 60)

    # 1. 异步函数
    print("\n1. 异步函数:")
    async def say_hello():
        await asyncio.sleep(1)
        return "Hello, Async World!"

    result = await say_hello()
    print(f"   结果: {result}")

    # 2. 异步生成器
    print("\n2. 异步生成器:")
    async for i in async_range(5):
        print(f"   生成: {i}")

    # 3. 异步上下文管理器
    print("\n3. 异步上下文管理器:")
    async with AsyncResource() as resource:
        result = await resource.do_something()
        print(f"   {result}")

asyncio.run(async_syntax_demo())
```

#### 异步迭代器

```python
import asyncio

class AsyncCounter:
    """异步计数器 - 异步迭代器示例"""

    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.limit:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        value = self.current
        self.current += 1
        return value

async def async_iterator_demo():
    """异步迭代器演示"""
    print("=" * 60)
    print("异步迭代器")
    print("=" * 60)

    # 使用异步迭代器
    print("\n使用异步计数器:")
    counter = AsyncCounter(5)
    async for num in counter:
        print(f"   计数: {num}")

    # 异步推导式
    print("\n异步推导式:")
    async def async_generator():
        for i in range(5):
            await asyncio.sleep(0.1)
            yield i * 2

    result = []
    async for x in async_generator():
        result.append(x)
    print(f"   结果: {result}")

asyncio.run(async_iterator_demo())
```

#### 异步上下文管理器

```python
import asyncio
import time

class AsyncDatabase:
    """异步数据库连接示例"""

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None

    async def __aenter__(self):
        print(f"[DB] 连接到 {self.connection_string}")
        await asyncio.sleep(0.5)  # 模拟连接时间
        self.connection = f"Connection-{id(self)}"
        print(f"[DB] 连接成功: {self.connection}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"[DB] 关闭连接: {self.connection}")
        await asyncio.sleep(0.3)  # 模拟关闭时间
        self.connection = None
        print("[DB] 连接已关闭")

    async def query(self, sql):
        """异步查询"""
        print(f"[DB] 执行查询: {sql}")
        await asyncio.sleep(0.2)
        return [f"Row-{i}" for i in range(3)]

class AsyncLock:
    """自定义异步锁"""

    def __init__(self):
        self._locked = False
        self._waiters = []

    async def __aenter__(self):
        while self._locked:
            waiter = asyncio.Future()
            self._waiters.append(waiter)
            await waiter
        self._locked = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._locked = False
        if self._waiters:
            waiter = self._waiters.pop(0)
            waiter.set_result(None)

async def async_context_manager_demo():
    """异步上下文管理器演示"""
    print("=" * 60)
    print("异步上下文管理器")
    print("=" * 60)

    # 1. 异步数据库连接
    print("\n1. 异步数据库连接:")
    async with AsyncDatabase("postgresql://localhost/db") as db:
        result = await db.query("SELECT * FROM users")
        print(f"   查询结果: {result}")

    # 2. 嵌套异步上下文管理器
    print("\n2. 嵌套异步上下文管理器:")
    async with AsyncDatabase("db1") as db1:
        async with AsyncDatabase("db2") as db2:
            r1 = await db1.query("SELECT 1")
            r2 = await db2.query("SELECT 2")
            print(f"   DB1结果: {r1}")
            print(f"   DB2结果: {r2}")

    # 3. 并发使用异步上下文管理器
    print("\n3. 并发使用异步上下文管理器:")
    async def use_db(db_name):
        async with AsyncDatabase(db_name) as db:
            return await db.query(f"SELECT * FROM {db_name}")

    results = await asyncio.gather(
        use_db("db1"),
        use_db("db2"),
        use_db("db3")
    )
    print(f"   并发结果: {results}")

asyncio.run(async_context_manager_demo())
```

---

### 3.3 异步IO操作

#### aiohttp

```python
import asyncio
import aiohttp
import time

async def fetch_single(session, url):
    """获取单个URL"""
    async with session.get(url) as response:
        return url, response.status, len(await response.text())

async def fetch_all(urls):
    """并发获取多个URL"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_single(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def aiohttp_demo():
    """aiohttp演示"""
    print("=" * 60)
    print("aiohttp - 异步HTTP客户端")
    print("=" * 60)

    urls = [
        "https://www.python.org",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.wikipedia.org",
    ]

    # 异步并发请求
    print("\n异步并发请求:")
    start = time.time()
    results = await fetch_all(urls)
    elapsed = time.time() - start

    for url, status, size in results:
        print(f"   {url}: 状态={status}, 大小={size} bytes")
    print(f"   总耗时: {elapsed:.2f} 秒")

    # 对比：顺序请求
    print("\n顺序请求（对比）:")
    start = time.time()
    async with aiohttp.ClientSession() as session:
        for url in urls:
            result = await fetch_single(session, url)
            print(f"   {result[0]}: 状态={result[1]}, 大小={result[2]} bytes")
    elapsed = time.time() - start
    print(f"   总耗时: {elapsed:.2f} 秒")

# asyncio.run(aiohttp_demo())
```

#### asyncio同步原语

```python
import asyncio

async def asyncio_primitives_demo():
    """asyncio同步原语演示"""
    print("=" * 60)
    print("asyncio 同步原语")
    print("=" * 60)

    # 1. Lock
    print("\n1. asyncio.Lock:")
    lock = asyncio.Lock()
    counter = 0

    async def increment():
        nonlocal counter
        async with lock:
            current = counter
            await asyncio.sleep(0.01)
            counter = current + 1

    await asyncio.gather(*[increment() for _ in range(100)])
    print(f"   计数器结果: {counter} (期望: 100)")

    # 2. Semaphore
    print("\n2. asyncio.Semaphore:")
    semaphore = asyncio.Semaphore(3)  # 最多3个并发

    async def limited_task(name):
        async with semaphore:
            print(f"   [{name}] 获取信号量，开始执行")
            await asyncio.sleep(1)
            print(f"   [{name}] 释放信号量")

    start = time.time()
    await asyncio.gather(*[limited_task(f"Task-{i}") for i in range(6)])
    elapsed = time.time() - start
    print(f"   6个任务，限制3并发，耗时: {elapsed:.2f} 秒")

    # 3. Event
    print("\n3. asyncio.Event:")
    event = asyncio.Event()

    async def waiter(name):
        print(f"   [{name}] 等待事件...")
        await event.wait()
        print(f"   [{name}] 事件触发，继续执行")

    async def setter():
        await asyncio.sleep(1)
        print("   [Setter] 设置事件")
        event.set()

    await asyncio.gather(
        waiter("Waiter-1"),
        waiter("Waiter-2"),
        setter()
    )

    # 4. Condition
    print("\n4. asyncio.Condition:")
    condition = asyncio.Condition()
    data = []

    async def producer():
        for i in range(3):
            await asyncio.sleep(0.5)
            async with condition:
                data.append(f"item-{i}")
                print(f"   [Producer] 生产: item-{i}")
                condition.notify_all()

    async def consumer(name):
        for _ in range(3):
            async with condition:
                while not data:
                    await condition.wait()
                item = data.pop(0)
                print(f"   [{name}] 消费: {item}")

    await asyncio.gather(producer(), consumer("Consumer-1"), consumer("Consumer-2"))

    # 5. Queue
    print("\n5. asyncio.Queue:")
    queue = asyncio.Queue(maxsize=5)

    async def queue_producer():
        for i in range(5):
            await queue.put(f"item-{i}")
            print(f"   [Producer] 放入: item-{i}")
            await asyncio.sleep(0.3)

    async def queue_consumer():
        for _ in range(5):
            item = await queue.get()
            print(f"   [Consumer] 取出: {item}")
            queue.task_done()

    await asyncio.gather(queue_producer(), queue_consumer())

asyncio.run(asyncio_primitives_demo())
```

#### 异步与同步代码交互

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def blocking_io():
    """阻塞IO操作（同步函数）"""
    time.sleep(2)
    return "阻塞操作完成"

def cpu_bound(n):
    """CPU密集型操作（同步函数）"""
    return sum(i ** 2 for i in range(n))

async def run_in_thread(func, *args):
    """在线程池中运行同步函数"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, func, *args)

async def run_in_process(func, *args):
    """在进程池中运行同步函数"""
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, func, *args)

async def mixed_demo():
    """混合异步与同步代码"""
    print("=" * 60)
    print("异步与同步代码交互")
    print("=" * 60)

    # 1. 在线程池中运行阻塞IO
    print("\n1. 在线程池中运行阻塞IO:")
    start = time.time()
    result = await run_in_thread(blocking_io)
    print(f"   结果: {result}")
    print(f"   耗时: {time.time() - start:.2f} 秒")

    # 2. 并发运行多个阻塞操作
    print("\n2. 并发运行多个阻塞操作:")
    start = time.time()
    results = await asyncio.gather(
        run_in_thread(blocking_io),
        run_in_thread(blocking_io),
        run_in_thread(blocking_io)
    )
    print(f"   结果: {results}")
    print(f"   耗时: {time.time() - start:.2f} 秒 (顺序执行需要 6 秒)")

    # 3. 在进程池中运行CPU密集型任务
    print("\n3. 在进程池中运行CPU密集型任务:")
    start = time.time()
    results = await asyncio.gather(
        run_in_process(cpu_bound, 1_000_000),
        run_in_process(cpu_bound, 2_000_000),
        run_in_process(cpu_bound, 1_500_000)
    )
    print(f"   结果: {results}")
    print(f"   耗时: {time.time() - start:.2f} 秒")

asyncio.run(mixed_demo())
```

---

## 第四部分：并发原语

### 4.1 锁机制

#### 概念定义

锁（Lock）是最基本的同步原语，用于保护共享资源，确保同一时间只有一个线程/进程可以访问临界区。

#### Lock（互斥锁）

```python
import threading
import time

class LockDemo:
    """互斥锁演示"""

    def __init__(self):
        self.balance = 1000
        self.lock = threading.Lock()

    def deposit(self, amount):
        """存款 - 使用锁保护"""
        with self.lock:
            print(f"[存款] 当前余额: {self.balance}, 存入: {amount}")
            new_balance = self.balance + amount
            time.sleep(0.1)  # 模拟处理时间
            self.balance = new_balance
            print(f"[存款] 新余额: {self.balance}")

    def withdraw(self, amount):
        """取款 - 使用锁保护"""
        with self.lock:
            if self.balance >= amount:
                print(f"[取款] 当前余额: {self.balance}, 取出: {amount}")
                new_balance = self.balance - amount
                time.sleep(0.1)  # 模拟处理时间
                self.balance = new_balance
                print(f"[取款] 新余额: {self.balance}")
            else:
                print(f"[取款] 余额不足: {self.balance} < {amount}")

def demonstrate_lock():
    """演示互斥锁"""
    print("=" * 60)
    print("Lock (互斥锁)")
    print("=" * 60)

    account = LockDemo()

    # 创建多个线程操作账户
    threads = [
        threading.Thread(target=account.deposit, args=(500,)),
        threading.Thread(target=account.withdraw, args=(200,)),
        threading.Thread(target=account.deposit, args=(300,)),
        threading.Thread(target=account.withdraw, args=(800,)),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\n最终余额: {account.balance}")

demonstrate_lock()
```

#### RLock（可重入锁）

```python
import threading

class RLockDemo:
    """可重入锁演示"""

    def __init__(self):
        self.lock = threading.RLock()
        self.data = []

    def add_item(self, item):
        """添加项目"""
        with self.lock:
            self.data.append(item)
            print(f"添加: {item}, 数据: {self.data}")

    def add_multiple(self, items):
        """添加多个项目 - 内部调用add_item"""
        with self.lock:
            print(f"批量添加开始: {items}")
            for item in items:
                self.add_item(item)  # 递归获取锁，RLock允许
            print(f"批量添加完成")

class LockFailDemo:
    """普通锁会导致死锁 - 反例"""

    def __init__(self):
        self.lock = threading.Lock()  # 普通锁
        self.data = []

    def add_item(self, item):
        with self.lock:
            self.data.append(item)

    def add_multiple(self, items):
        with self.lock:
            for item in items:
                self.add_item(item)  # 死锁！同一线程无法再次获取锁

def demonstrate_rlock():
    """演示可重入锁"""
    print("\n" + "=" * 60)
    print("RLock (可重入锁)")
    print("=" * 60)

    print("\n1. RLock 允许同一线程多次获取锁:")
    demo = RLockDemo()
    demo.add_multiple([1, 2, 3])

    print("\n2. 普通 Lock 会导致死锁:")
    print("   代码: 同一线程在持有锁时再次获取锁")
    print("   结果: 死锁！")
    # 不要实际运行，会导致死锁
    # fail_demo = LockFailDemo()
    # fail_demo.add_multiple([1, 2, 3])  # 死锁！

demonstrate_rlock()
```

#### Semaphore（信号量）

```python
import threading
import time
import random

class SemaphoreDemo:
    """信号量演示 - 限制并发数"""

    def __init__(self, max_concurrent):
        self.semaphore = threading.Semaphore(max_concurrent)
        self.active_count = 0
        self.count_lock = threading.Lock()

    def access_resource(self, name):
        """访问受限资源"""
        print(f"[{name}] 请求访问...")

        with self.semaphore:
            with self.count_lock:
                self.active_count += 1
                current = self.active_count

            print(f"[{name}] 获得访问权，当前并发: {current}")
            time.sleep(random.uniform(1, 2))  # 模拟工作

            with self.count_lock:
                self.active_count -= 1

            print(f"[{name}] 释放访问权")

def demonstrate_semaphore():
    """演示信号量"""
    print("\n" + "=" * 60)
    print("Semaphore (信号量)")
    print("=" * 60)

    # 限制最多3个并发
    demo = SemaphoreDemo(3)

    threads = [
        threading.Thread(target=demo.access_resource, args=(f"Worker-{i}",))
        for i in range(8)
    ]

    for t in threads:
        t.start()
        time.sleep(0.1)  # 错开启动时间

    for t in threads:
        t.join()

demonstrate_semaphore()
```

#### BoundedSemaphore

```python
import threading

def demonstrate_bounded_semaphore():
    """演示有界信号量"""
    print("\n" + "=" * 60)
    print("BoundedSemaphore (有界信号量)")
    print("=" * 60)

    # 普通信号量
    sem = threading.Semaphore(2)
    print("\n1. 普通 Semaphore:")
    sem.release()  # 可以无限释放
    sem.release()
    sem.release()
    print(f"   释放3次后计数: {sem._value}")  # 可能超过初始值

    # 有界信号量
    bounded_sem = threading.BoundedSemaphore(2)
    print("\n2. BoundedSemaphore:")
    bounded_sem.acquire()
    bounded_sem.acquire()
    print(f"   获取2次后计数: {bounded_sem._value}")
    bounded_sem.release()
    bounded_sem.release()
    print(f"   释放2次后计数: {bounded_sem._value}")

    try:
        bounded_sem.release()  # 超过初始值会报错
    except ValueError as e:
        print(f"   错误: {e}")

demonstrate_bounded_semaphore()
```

---

### 4.2 事件机制

#### Event

```python
import threading
import time

class EventDemo:
    """事件演示"""

    def __init__(self):
        self.event = threading.Event()
        self.data = None

    def producer(self):
        """生产者线程"""
        print("[Producer] 开始生产数据...")
        time.sleep(2)
        self.data = "重要数据"
        print("[Producer] 数据准备完成，设置事件")
        self.event.set()

    def consumer(self):
        """消费者线程"""
        print("[Consumer] 等待数据...")
        self.event.wait()  # 阻塞等待事件
        print(f"[Consumer] 收到数据: {self.data}")

def demonstrate_event():
    """演示事件"""
    print("=" * 60)
    print("Event (事件)")
    print("=" * 60)

    demo = EventDemo()

    t1 = threading.Thread(target=demo.consumer)
    t2 = threading.Thread(target=demo.producer)

    t1.start()
    time.sleep(0.5)
    t2.start()

    t1.join()
    t2.join()

    print("\n事件状态:")
    print(f"   是否设置: {demo.event.is_set()}")

    # 清除事件
    demo.event.clear()
    print(f"   清除后: {demo.event.is_set()}")

demonstrate_event()
```

#### Condition

```python
import threading
import time
import random

class ConditionDemo:
    """条件变量演示 - 生产者消费者"""

    def __init__(self):
        self.condition = threading.Condition()
        self.queue = []
        self.max_size = 5

    def producer(self, name):
        """生产者"""
        for i in range(5):
            with self.condition:
                # 等待队列有空间
                while len(self.queue) >= self.max_size:
                    print(f"[{name}] 队列已满，等待...")
                    self.condition.wait()

                # 生产数据
                item = f"{name}-item-{i}"
                self.queue.append(item)
                print(f"[{name}] 生产: {item}, 队列长度: {len(self.queue)}")

                # 通知消费者
                self.condition.notify()

            time.sleep(random.uniform(0.1, 0.5))

    def consumer(self, name):
        """消费者"""
        for _ in range(5):
            with self.condition:
                # 等待队列有数据
                while not self.queue:
                    print(f"[{name}] 队列为空，等待...")
                    self.condition.wait()

                # 消费数据
                item = self.queue.pop(0)
                print(f"[{name}] 消费: {item}, 队列长度: {len(self.queue)}")

                # 通知生产者
                self.condition.notify()

            time.sleep(random.uniform(0.3, 0.7))

def demonstrate_condition():
    """演示条件变量"""
    print("\n" + "=" * 60)
    print("Condition (条件变量)")
    print("=" * 60)

    demo = ConditionDemo()

    # 创建生产者和消费者线程
    threads = [
        threading.Thread(target=demo.producer, args=("P1",)),
        threading.Thread(target=demo.producer, args=("P2",)),
        threading.Thread(target=demo.consumer, args=("C1",)),
        threading.Thread(target=demo.consumer, args=("C2",)),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

demonstrate_condition()
```

#### Barrier

```python
import threading
import time

class BarrierDemo:
    """屏障演示"""

    def __init__(self, num_parties):
        self.barrier = threading.Barrier(num_parties)

    def worker(self, name):
        """工作线程"""
        print(f"[{name}] 开始阶段1...")
        time.sleep(threading.current_thread().ident % 3)
        print(f"[{name}] 阶段1完成，等待其他线程...")

        self.barrier.wait()  # 等待所有线程到达

        print(f"[{name}] 所有线程到达，开始阶段2...")
        time.sleep(threading.current_thread().ident % 2)
        print(f"[{name}] 阶段2完成")

        self.barrier.wait()  # 再次等待

        print(f"[{name}] 所有线程到达，任务完成！")

def demonstrate_barrier():
    """演示屏障"""
    print("\n" + "=" * 60)
    print("Barrier (屏障)")
    print("=" * 60)

    num_threads = 4
    demo = BarrierDemo(num_threads)

    threads = [
        threading.Thread(target=demo.worker, args=(f"Worker-{i}",))
        for i in range(num_threads)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

demonstrate_barrier()
```

---

### 4.3 队列

#### Queue

```python
import threading
import queue
import time
import random

class QueueDemo:
    """队列演示"""

    def __init__(self):
        self.q = queue.Queue(maxsize=10)
        self.producer_done = threading.Event()

    def producer(self, name, items):
        """生产者"""
        for item in items:
            self.q.put(item)
            print(f"[{name}] 生产: {item}, 队列大小: {self.q.qsize()}")
            time.sleep(random.uniform(0.1, 0.3))
        print(f"[{name}] 生产完成")

    def consumer(self, name):
        """消费者"""
        while True:
            try:
                # 等待数据，超时检查是否结束
                item = self.q.get(timeout=2)

                # 处理数据
                print(f"[{name}] 消费: {item}, 队列大小: {self.q.qsize()}")

                self.q.task_done()
                time.sleep(random.uniform(0.2, 0.5))

            except queue.Empty:
                # 检查是否所有生产者都已完成
                if self.producer_done.is_set() and self.q.empty():
                    print(f"[{name}] 退出")
                    break

def demonstrate_queue():
    """演示队列"""
    print("=" * 60)
    print("Queue (队列)")
    print("=" * 60)

    demo = QueueDemo()

    # 生产数据
    items1 = [f"A-{i}" for i in range(5)]
    items2 = [f"B-{i}" for i in range(5)]

    threads = [
        threading.Thread(target=demo.producer, args=("P1", items1)),
        threading.Thread(target=demo.producer, args=("P2", items2)),
        threading.Thread(target=demo.consumer, args=("C1",)),
        threading.Thread(target=demo.consumer, args=("C2",)),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\n队列是否为空: {demo.q.empty()}")

demonstrate_queue()
```

#### PriorityQueue

```python
import threading
import queue
import time
import random

class PriorityQueueDemo:
    """优先队列演示"""

    def __init__(self):
        self.pq = queue.PriorityQueue()

    def add_task(self, name, priority, task):
        """添加任务"""
        # 优先级越小越优先
        self.pq.put((priority, name, task))
        print(f"[添加] 优先级:{priority}, 名称:{name}, 任务:{task}")

    def process_tasks(self):
        """处理任务"""
        while not self.pq.empty():
            priority, name, task = self.pq.get()
            print(f"[处理] 优先级:{priority}, 名称:{name}, 任务:{task}")
            time.sleep(0.5)
            self.pq.task_done()

def demonstrate_priority_queue():
    """演示优先队列"""
    print("\n" + "=" * 60)
    print("PriorityQueue (优先队列)")
    print("=" * 60)

    demo = PriorityQueueDemo()

    # 添加任务（优先级数字越小越优先）
    tasks = [
        (3, "任务A", "普通处理"),
        (1, "任务B", "紧急处理"),
        (2, "任务C", "重要处理"),
        (1, "任务D", "紧急处理2"),
        (4, "任务E", "低优先级"),
    ]

    for priority, name, task in tasks:
        demo.add_task(name, priority, task)

    print("\n按优先级处理:")
    demo.process_tasks()

demonstrate_priority_queue()
```

#### LifoQueue

```python
import threading
import queue
import time

class LifoQueueDemo:
    """LIFO队列演示 - 栈"""

    def __init__(self):
        self.lq = queue.LifoQueue(maxsize=10)

    def push_items(self, items):
        """压栈"""
        for item in items:
            self.lq.put(item)
            print(f"[压栈] {item}, 栈大小: {self.lq.qsize()}")

    def pop_items(self, count):
        """弹栈"""
        for _ in range(count):
            if not self.lq.empty():
                item = self.lq.get()
                print(f"[弹栈] {item}, 栈大小: {self.lq.qsize()}")
                self.lq.task_done()

def demonstrate_lifo_queue():
    """演示LIFO队列"""
    print("\n" + "=" * 60)
    print("LifoQueue (LIFO队列 / 栈)")
    print("=" * 60)

    demo = LifoQueueDemo()

    # 压栈
    items = ["第1个", "第2个", "第3个", "第4个", "第5个"]
    print("压栈顺序:", items)
    demo.push_items(items)

    # 弹栈（后进先出）
    print("\n弹栈顺序:")
    demo.pop_items(5)

demonstrate_lifo_queue()
```

---

## 第五部分：并发模式

### 5.1 生产者-消费者模式

#### 概念定义

生产者-消费者模式是一种经典的并发设计模式，用于解耦数据的生产和消费。生产者负责生成数据并放入缓冲区，消费者从缓冲区取出数据进行处理。

#### 实现原理

```
┌─────────────────────────────────────────────────────────┐
│              生产者-消费者模式                            │
│                                                         │
│  ┌─────────┐      ┌──────────┐      ┌─────────┐        │
│  │Producer1│──┐   │          │   ┌──│Consumer1│        │
│  ├─────────┤  │   │   Queue  │   │  ├─────────┤        │
│  │Producer2│──┼──►│ (Buffer) │───┼──►│Consumer2│        │
│  ├─────────┤  │   │          │   │  ├─────────┤        │
│  │Producer3│──┘   └──────────┘   └──│Consumer3│        │
│  └─────────┘                         └─────────┘        │
│                                                         │
│  特点：                                                  │
│  - 生产者和消费者解耦                                   │
│  - 缓冲区平衡生产和消费速度                              │
│  - 支持多生产者和多消费者                                │
└─────────────────────────────────────────────────────────┘
```

#### 正例：正确实现

```python
import threading
import queue
import time
import random

class ProducerConsumer:
    """生产者-消费者模式 - 正确实现"""

    def __init__(self, buffer_size=10):
        self.buffer = queue.Queue(maxsize=buffer_size)
        self.producer_done = threading.Event()
        self.lock = threading.Lock()
        self.items_produced = 0
        self.items_consumed = 0

    def producer(self, producer_id, num_items):
        """生产者"""
        for i in range(num_items):
            item = f"Item-{producer_id}-{i}"

            # 生产数据
            self.buffer.put(item)

            with self.lock:
                self.items_produced += 1

            print(f"[Producer-{producer_id}] 生产: {item}")
            time.sleep(random.uniform(0.1, 0.3))

        print(f"[Producer-{producer_id}] 完成生产")

    def consumer(self, consumer_id):
        """消费者"""
        while True:
            try:
                # 等待数据，超时检查是否结束
                item = self.buffer.get(timeout=2)

                # 处理数据
                print(f"[Consumer-{consumer_id}] 消费: {item}")

                with self.lock:
                    self.items_consumed += 1

                self.buffer.task_done()
                time.sleep(random.uniform(0.2, 0.5))

            except queue.Empty:
                # 检查是否所有生产者都已完成
                if self.producer_done.is_set() and self.buffer.empty():
                    print(f"[Consumer-{consumer_id}] 退出")
                    break

def run_producer_consumer():
    """运行生产者-消费者"""
    print("=" * 60)
    print("生产者-消费者模式")
    print("=" * 60)

    pc = ProducerConsumer(buffer_size=5)

    # 创建生产者线程
    producers = [
        threading.Thread(target=pc.producer, args=(i, 5))
        for i in range(2)
    ]

    # 创建消费者线程
    consumers = [
        threading.Thread(target=pc.consumer, args=(i,))
        for i in range(3)
    ]

    # 启动所有线程
    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    # 等待生产者完成
    for p in producers:
        p.join()

    print("\n所有生产者完成，设置完成标志")
    pc.producer_done.set()

    # 等待消费者完成
    for c in consumers:
        c.join()

    print(f"\n统计: 生产={pc.items_produced}, 消费={pc.items_consumed}")

run_producer_consumer()
```

#### 反例：错误实现

```python
import threading
import time

class BadProducerConsumer:
    """生产者-消费者模式 - 错误实现"""

    def __init__(self):
        self.buffer = []  # 错误：使用普通列表，没有大小限制
        self.lock = threading.Lock()
        self.has_data = threading.Event()

    def producer(self):
        """生产者 - 问题：没有缓冲区大小限制"""
        for i in range(100):
            with self.lock:
                self.buffer.append(f"Item-{i}")
            self.has_data.set()
            # 问题：生产速度过快，可能耗尽内存
            time.sleep(0.001)

    def consumer(self):
        """消费者 - 问题：忙等待"""
        while True:
            # 问题：忙等待，浪费CPU
            if self.buffer:
                with self.lock:
                    if self.buffer:  # 双重检查
                        item = self.buffer.pop(0)
                        print(f"消费: {item}")
            else:
                # 问题：忙等待，没有正确休眠
                pass

# 更好的实现使用 queue.Queue，它内部处理了：
# 1. 缓冲区大小限制（put 会阻塞）
# 2. 条件变量通知（避免忙等待）
# 3. 线程安全
```

---

### 5.2 读者-写者模式

#### 概念定义

读者-写者模式用于解决多线程对共享资源的读写冲突。允许多个读者同时读取，但写者独占访问。

#### 实现原理

```
┌─────────────────────────────────────────────────────────┐
│               读者-写者模式                              │
│                                                         │
│  规则：                                                  │
│  - 多个读者可以同时读取                                  │
│  - 写者独占访问（读写互斥，写写互斥）                     │
│                                                         │
│  ┌─────────┐  ┌─────────┐      ┌─────────┐             │
│  │ Reader1 │  │ Reader2 │──────│  Data   │             │
│  └─────────┘  └─────────┘      └────┬────┘             │
│                                     │                   │
│                              ┌──────┴──────┐           │
│                              │   Writer    │           │
│                              └─────────────┘           │
└─────────────────────────────────────────────────────────┘
```

#### 正例：正确实现

```python
import threading
import time
import random

class ReadWriteLock:
    """读写锁 - 读者优先实现"""

    def __init__(self):
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.read_count = 0

    def acquire_read(self):
        """获取读锁"""
        with self.read_lock:
            self.read_count += 1
            if self.read_count == 1:
                self.write_lock.acquire()

    def release_read(self):
        """释放读锁"""
        with self.read_lock:
            self.read_count -= 1
            if self.read_count == 0:
                self.write_lock.release()

    def acquire_write(self):
        """获取写锁"""
        self.write_lock.acquire()

    def release_write(self):
        """释放写锁"""
        self.write_lock.release()

    def __enter__(self):
        self.acquire_read()
        return self

    def __exit__(self, *args):
        self.release_read()

class ReaderWriterDemo:
    """读者-写者演示"""

    def __init__(self):
        self.data = "初始数据"
        self.rw_lock = ReadWriteLock()

    def reader(self, reader_id):
        """读者"""
        for _ in range(3):
            self.rw_lock.acquire_read()
            try:
                print(f"[Reader-{reader_id}] 读取: {self.data}")
                time.sleep(random.uniform(0.1, 0.3))
            finally:
                self.rw_lock.release_read()
            time.sleep(random.uniform(0.1, 0.2))

    def writer(self, writer_id):
        """写者"""
        for i in range(2):
            self.rw_lock.acquire_write()
            try:
                new_data = f"数据由Writer-{writer_id}修改-{i}"
                print(f"[Writer-{writer_id}] 写入: {new_data}")
                self.data = new_data
                time.sleep(random.uniform(0.2, 0.4))
            finally:
                self.rw_lock.release_write()
            time.sleep(random.uniform(0.3, 0.5))

def run_reader_writer():
    """运行读者-写者"""
    print("\n" + "=" * 60)
    print("读者-写者模式")
    print("=" * 60)

    demo = ReaderWriterDemo()

    # 创建读者线程
    readers = [
        threading.Thread(target=demo.reader, args=(i,))
        for i in range(3)
    ]

    # 创建写者线程
    writers = [
        threading.Thread(target=demo.writer, args=(i,))
        for i in range(2)
    ]

    # 启动所有线程
    for r in readers:
        r.start()
    for w in writers:
        w.start()

    # 等待完成
    for r in readers:
        r.join()
    for w in writers:
        w.join()

    print(f"\n最终数据: {demo.data}")

run_reader_writer()
```

#### 写者优先实现

```python
import threading

class WriterPriorityRWLock:
    """写者优先的读写锁"""

    def __init__(self):
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.read_count = 0
        self.write_waiting = 0
        self.condition = threading.Condition(self.read_lock)

    def acquire_read(self):
        """获取读锁"""
        with self.condition:
            # 如果有写者等待，读者等待
            while self.write_waiting > 0:
                self.condition.wait()

            self.read_count += 1
            if self.read_count == 1:
                self.write_lock.acquire()

    def release_read(self):
        """释放读锁"""
        with self.condition:
            self.read_count -= 1
            if self.read_count == 0:
                self.write_lock.release()
            self.condition.notify_all()

    def acquire_write(self):
        """获取写锁"""
        with self.read_lock:
            self.write_waiting += 1
        self.write_lock.acquire()

    def release_write(self):
        """释放写锁"""
        self.write_lock.release()
        with self.read_lock:
            self.write_waiting -= 1
            self.condition.notify_all()
```

---

### 5.3 工作队列模式

#### 概念定义

工作队列模式（Worker Queue Pattern）将任务提交到队列，由多个工作线程/进程从队列中获取任务并执行，实现负载均衡。

#### 正例：正确实现

```python
import threading
import queue
import time
import random

class WorkerPool:
    """工作队列模式 - 正确实现"""

    def __init__(self, num_workers):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.stop_event = threading.Event()

        # 创建工作线程
        for i in range(num_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                args=(i,),
                daemon=True
            )
            self.workers.append(worker)
            worker.start()

    def _worker_loop(self, worker_id):
        """工作线程主循环"""
        while not self.stop_event.is_set():
            try:
                # 获取任务（带超时以便检查停止事件）
                task = self.task_queue.get(timeout=1)

                if task is None:  # 停止信号
                    break

                task_id, func, args, kwargs = task

                try:
                    # 执行任务
                    print(f"[Worker-{worker_id}] 执行任务-{task_id}")
                    result = func(*args, **kwargs)
                    self.result_queue.put((task_id, True, result))
                except Exception as e:
                    self.result_queue.put((task_id, False, str(e)))

                self.task_queue.task_done()

            except queue.Empty:
                continue

    def submit(self, func, *args, **kwargs):
        """提交任务"""
        task_id = random.randint(1000, 9999)
        self.task_queue.put((task_id, func, args, kwargs))
        return task_id

    def shutdown(self):
        """关闭工作池"""
        self.stop_event.set()

        # 发送停止信号
        for _ in self.workers:
            self.task_queue.put(None)

        # 等待工作线程结束
        for worker in self.workers:
            worker.join()

    def get_results(self):
        """获取所有结果"""
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results

def worker_task(n):
    """示例任务"""
    time.sleep(random.uniform(0.5, 1.5))
    return n ** 2

def run_worker_pool():
    """运行工作队列"""
    print("\n" + "=" * 60)
    print("工作队列模式")
    print("=" * 60)

    # 创建工作池
    pool = WorkerPool(num_workers=3)

    # 提交任务
    print("\n提交任务:")
    task_ids = []
    for i in range(10):
        task_id = pool.submit(worker_task, i)
        task_ids.append(task_id)
        print(f"  提交任务-{task_id}: worker_task({i})")

    # 等待所有任务完成
    print("\n等待任务完成...")
    pool.task_queue.join()

    # 获取结果
    results = pool.get_results()
    print(f"\n获取到 {len(results)} 个结果:")
    for task_id, success, result in sorted(results):
        status = "成功" if success else "失败"
        print(f"  任务-{task_id}: {status}, 结果={result}")

    # 关闭工作池
    pool.shutdown()
    print("\n工作池已关闭")

run_worker_pool()
```

---

### 5.4 MapReduce模式

#### 概念定义

MapReduce是一种分布式计算模型，将大规模数据处理分解为Map（映射）和Reduce（归约）两个阶段。

#### 正例：正确实现

```python
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def map_word_count(text_chunk):
    """Map函数：统计单词出现次数"""
    word_counts = defaultdict(int)
    words = text_chunk.lower().split()
    for word in words:
        word = word.strip(".,!?;:\"\'()")
        if word:
            word_counts[word] += 1
    return list(word_counts.items())

def shuffle_word_counts(mapped_results):
    """Shuffle函数：按键分组"""
    grouped = defaultdict(list)
    for word, count in mapped_results:
        grouped[word].append(count)
    return grouped.items()

def reduce_word_count(word_counts):
    """Reduce函数：合并计数"""
    word, counts = word_counts
    return (word, sum(counts))

class MapReduce:
    """MapReduce实现"""

    def __init__(self, num_workers=None):
        self.num_workers = num_workers or multiprocessing.cpu_count()

    def run(self, data, map_func, reduce_func):
        """运行MapReduce"""
        print("\n" + "=" * 60)
        print("MapReduce 模式")
        print("=" * 60)

        # 1. Map阶段
        print(f"\n1. Map阶段（{self.num_workers}个worker）:")
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            mapped_results = list(executor.map(map_func, data))

        # 展平结果
        all_mapped = []
        for result in mapped_results:
            all_mapped.extend(result)
        print(f"   Map输出: {len(all_mapped)} 条记录")

        # 2. Shuffle阶段
        print("\n2. Shuffle阶段:")
        shuffled = shuffle_word_counts(all_mapped)
        print(f"   分组后: {len(shuffled)} 个key")

        # 3. Reduce阶段
        print(f"\n3. Reduce阶段（{self.num_workers}个worker）:")
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            results = list(executor.map(reduce_func, shuffled))

        return dict(results)

def run_mapreduce():
    """运行MapReduce示例"""
    # 示例数据
    texts = [
        "the quick brown fox jumps over the lazy dog",
        "the fox is quick and the dog is lazy",
        "brown fox jumps high over lazy dog",
        "quick brown fox quick lazy dog",
        "the dog sleeps while the fox jumps",
    ]

    mr = MapReduce(num_workers=4)
    result = mr.run(texts, map_word_count, reduce_word_count)

    # 显示结果
    print("\n4. 最终结果（Top 10）:")
    sorted_results = sorted(result.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_results[:10]:
        print(f"   {word}: {count}")

run_mapreduce()
```

---

### 5.5 演员模型（Actor Model）

#### 概念定义

演员模型是一种并发计算模型，将"演员"（Actor）作为并发计算的基本单元。每个演员有自己的状态和行为，通过异步消息传递进行通信。

#### 正例：正确实现

```python
import threading
import queue
import time
import uuid

class Actor:
    """演员基类"""

    def __init__(self):
        self.mailbox = queue.Queue()
        self.address = str(uuid.uuid4())
        self.running = False
        self.thread = None

    def start(self):
        """启动演员"""
        self.running = True
        self.thread = threading.Thread(target=self._process_messages)
        self.thread.start()

    def stop(self):
        """停止演员"""
        self.running = False
        self.send(None)  # 发送停止信号
        if self.thread:
            self.thread.join()

    def send(self, message):
        """发送消息"""
        self.mailbox.put(message)

    def _process_messages(self):
        """消息处理循环"""
        while self.running:
            try:
                message = self.mailbox.get(timeout=1)
                if message is None:
                    break
                self.receive(message)
            except queue.Empty:
                continue

    def receive(self, message):
        """接收消息（子类实现）"""
        raise NotImplementedError

class CounterActor(Actor):
    """计数器演员"""

    def __init__(self):
        super().__init__()
        self.count = 0

    def receive(self, message):
        action = message.get("action")
        sender = message.get("sender")

        if action == "increment":
            self.count += 1
            print(f"[Counter] 增加到 {self.count}")
        elif action == "decrement":
            self.count -= 1
            print(f"[Counter] 减少到 {self.count}")
        elif action == "get":
            if sender:
                sender.send({
                    "type": "result",
                    "value": self.count,
                    "from": self.address
                })

class PrinterActor(Actor):
    """打印机演员"""

    def receive(self, message):
        msg_type = message.get("type")

        if msg_type == "print":
            print(f"[Printer] {message.get('content')}")
        elif msg_type == "result":
            print(f"[Printer] 收到结果: {message.get('value')}")

def run_actor_model():
    """运行演员模型示例"""
    print("\n" + "=" * 60)
    print("演员模型 (Actor Model)")
    print("=" * 60)

    # 创建演员
    counter = CounterActor()
    printer = PrinterActor()

    # 启动演员
    counter.start()
    printer.start()

    print("\n发送消息:")

    # 发送增量消息
    for i in range(5):
        counter.send({"action": "increment"})
        time.sleep(0.1)

    # 发送减量消息
    for i in range(2):
        counter.send({"action": "decrement"})
        time.sleep(0.1)

    # 获取当前值
    counter.send({"action": "get", "sender": printer})

    time.sleep(1)

    # 停止演员
    counter.stop()
    printer.stop()
    print("\n演员已停止")

run_actor_model()
```

---

## 第六部分：死锁与竞态条件

### 6.1 死锁的四个条件

#### 概念定义

死锁（Deadlock）是指两个或多个线程/进程在执行过程中，因争夺资源而造成的一种互相等待的现象，若无外力作用，它们都将无法继续执行。

#### 死锁的四个必要条件

```
┌─────────────────────────────────────────────────────────┐
│                  死锁的四个必要条件                        │
│                                                         │
│  1. 互斥条件（Mutual Exclusion）                         │
│     └─> 资源一次只能被一个线程占用                       │
│                                                         │
│  2. 占有并等待（Hold and Wait）                          │
│     └─> 线程持有资源同时等待其他资源                     │
│                                                         │
│  3. 不可抢占（No Preemption）                            │
│     └─> 资源不能被强制释放                               │
│                                                         │
│  4. 循环等待（Circular Wait）                            │
│     └─> 线程之间形成循环等待链                          │
│                                                         │
│  ┌─────┐    等待    ┌─────┐                             │
│  │  A  │───────────>│  B  │                             │
│  └──┬──┘            └──┬──┘                             │
│     │                  │                                │
│     │    占有          │  占有                           │
│     │                  │                                │
│     │    ┌─────┐       │                                │
│     └────│Res1 │<──────┘                                │
│          └─────┘                                        │
│            ▲                                            │
│            │  等待                                      │
│          ┌─┴───┐                                        │
│          │Res2 │                                        │
│          └─────┘                                        │
└─────────────────────────────────────────────────────────┘
```

#### 死锁示例代码

```python
import threading
import time

class DeadlockDemo:
    """死锁演示"""

    def __init__(self):
        self.lock_a = threading.Lock()
        self.lock_b = threading.Lock()

    def thread_1(self):
        """线程1：先获取lock_a，再获取lock_b"""
        print("[Thread-1] 尝试获取 Lock A...")
        with self.lock_a:
            print("[Thread-1] 获得 Lock A")
            time.sleep(0.1)  # 确保线程2获取lock_b

            print("[Thread-1] 尝试获取 Lock B...")
            with self.lock_b:
                print("[Thread-1] 获得 Lock B")
                print("[Thread-1] 完成工作")

    def thread_2(self):
        """线程2：先获取lock_b，再获取lock_a"""
        print("[Thread-2] 尝试获取 Lock B...")
        with self.lock_b:
            print("[Thread-2] 获得 Lock B")
            time.sleep(0.1)  # 确保线程1获取lock_a

            print("[Thread-2] 尝试获取 Lock A...")
            with self.lock_a:
                print("[Thread-2] 获得 Lock A")
                print("[Thread-2] 完成工作")

def demonstrate_deadlock():
    """演示死锁"""
    print("=" * 60)
    print("死锁演示")
    print("=" * 60)
    print("警告: 这将导致死锁，程序会卡住！")
    print("按 Ctrl+C 终止程序")
    print("-" * 60)

    demo = DeadlockDemo()

    t1 = threading.Thread(target=demo.thread_1)
    t2 = threading.Thread(target=demo.thread_2)

    t1.start()
    t2.start()

    # 设置超时，避免真正卡住
    t1.join(timeout=3)
    t2.join(timeout=3)

    if t1.is_alive() or t2.is_alive():
        print("\n检测到死锁！线程仍在运行...")
    else:
        print("\n线程正常完成（没有死锁）")

# demonstrate_deadlock()  # 取消注释运行死锁演示
```

---

### 6.2 死锁检测与避免

#### 死锁避免策略

```python
import threading
import time

class DeadlockPrevention:
    """死锁预防策略"""

    def __init__(self):
        self.lock_a = threading.Lock()
        self.lock_b = threading.Lock()

    # 策略1: 统一获取顺序
    def strategy_1_ordered_locks(self):
        """策略1: 按固定顺序获取锁"""
        print("\n策略1: 按固定顺序获取锁")

        def worker_1():
            # 总是先获取A，再获取B
            with self.lock_a:
                print("[Worker-1] 获得 Lock A")
                time.sleep(0.1)
                with self.lock_b:
                    print("[Worker-1] 获得 Lock B")
                    print("[Worker-1] 完成")

        def worker_2():
            # 同样先获取A，再获取B
            with self.lock_a:
                print("[Worker-2] 获得 Lock A")
                time.sleep(0.1)
                with self.lock_b:
                    print("[Worker-2] 获得 Lock B")
                    print("[Worker-2] 完成")

        t1 = threading.Thread(target=worker_1)
        t2 = threading.Thread(target=worker_2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("策略1成功！")

    # 策略2: 使用RLock
    def strategy_2_rlock(self):
        """策略2: 使用可重入锁"""
        print("\n策略2: 使用可重入锁")

        rlock = threading.RLock()

        def worker():
            with rlock:
                print("[Worker] 第一次获取锁")
                with rlock:  # 同一线程可以再次获取
                    print("[Worker] 第二次获取锁")
                print("[Worker] 完成")

        t = threading.Thread(target=worker)
        t.start()
        t.join()
        print("策略2成功！")

    # 策略3: 使用超时
    def strategy_3_timeout(self):
        """策略3: 使用超时避免无限等待"""
        print("\n策略3: 使用超时")

        def worker_1():
            if self.lock_a.acquire(timeout=1):
                try:
                    print("[Worker-1] 获得 Lock A")
                    time.sleep(0.5)
                    if self.lock_b.acquire(timeout=1):
                        try:
                            print("[Worker-1] 获得 Lock B")
                        finally:
                            self.lock_b.release()
                    else:
                        print("[Worker-1] 获取 Lock B 超时")
                finally:
                    self.lock_a.release()
            else:
                print("[Worker-1] 获取 Lock A 超时")

        def worker_2():
            if self.lock_b.acquire(timeout=1):
                try:
                    print("[Worker-2] 获得 Lock B")
                    time.sleep(0.5)
                    if self.lock_a.acquire(timeout=1):
                        try:
                            print("[Worker-2] 获得 Lock A")
                        finally:
                            self.lock_a.release()
                    else:
                        print("[Worker-2] 获取 Lock A 超时")
                finally:
                    self.lock_b.release()
            else:
                print("[Worker-2] 获取 Lock B 超时")

        t1 = threading.Thread(target=worker_1)
        t2 = threading.Thread(target=worker_2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("策略3成功！")

    # 策略4: 使用上下文管理器同时获取多个锁
    def strategy_4_context_manager(self):
        """策略4: 使用上下文管理器"""
        print("\n策略4: 使用上下文管理器")

        from contextlib import contextmanager

        @contextmanager
        def acquire_locks(*locks):
            """同时获取多个锁"""
            for lock in sorted(locks, key=id):  # 按id排序确保顺序
                lock.acquire()
            try:
                yield
            finally:
                for lock in reversed(locks):
                    lock.release()

        def worker_1():
            with acquire_locks(self.lock_a, self.lock_b):
                print("[Worker-1] 获得两个锁")
                time.sleep(0.1)
                print("[Worker-1] 完成")

        def worker_2():
            with acquire_locks(self.lock_b, self.lock_a):  # 顺序不同但会被排序
                print("[Worker-2] 获得两个锁")
                time.sleep(0.1)
                print("[Worker-2] 完成")

        t1 = threading.Thread(target=worker_1)
        t2 = threading.Thread(target=worker_2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("策略4成功！")

def run_deadlock_prevention():
    """运行死锁预防演示"""
    print("=" * 60)
    print("死锁预防策略")
    print("=" * 60)

    demo = DeadlockPrevention()
    demo.strategy_1_ordered_locks()
    demo.strategy_2_rlock()
    demo.strategy_3_timeout()
    demo.strategy_4_context_manager()

    print("\n所有策略演示完成！")

run_deadlock_prevention()
```

---

### 6.3 竞态条件分析

#### 概念定义

竞态条件（Race Condition）是指多个线程访问共享数据时，最终结果依赖于线程执行的相对时序，导致结果不确定。

#### 竞态条件示例

```python
import threading
import time

class RaceConditionDemo:
    """竞态条件演示"""

    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()

    def unsafe_increment(self):
        """非线程安全的增量"""
        # 读取-修改-写入不是原子操作
        current = self.counter
        # 此处可能发生上下文切换！
        time.sleep(0.0001)  # 模拟其他操作
        self.counter = current + 1

    def safe_increment(self):
        """线程安全的增量"""
        with self.lock:
            current = self.counter
            time.sleep(0.0001)
            self.counter = current + 1

    def demonstrate(self):
        """演示竞态条件"""
        print("=" * 60)
        print("竞态条件演示")
        print("=" * 60)

        # 非线程安全版本
        print("\n1. 非线程安全版本:")
        self.counter = 0
        threads = [threading.Thread(target=self.unsafe_increment)
                   for _ in range(1000)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"   期望: 1000, 实际: {self.counter}")
        print(f"   丢失更新: {1000 - self.counter}")

        # 线程安全版本
        print("\n2. 线程安全版本:")
        self.counter = 0
        threads = [threading.Thread(target=self.safe_increment)
                   for _ in range(1000)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"   期望: 1000, 实际: {self.counter}")

race_demo = RaceConditionDemo()
race_demo.demonstrate()
```

#### 常见的竞态条件场景

```python
import threading

class CommonRaceConditions:
    """常见的竞态条件场景"""

    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    # 场景1: 检查-执行竞态
    def check_then_act_unsafe(self, key):
        """不安全的检查-执行"""
        if key not in self.data:  # 检查
            # 此处可能发生竞态！
            self.data[key] = []    # 执行
        self.data[key].append("value")

    def check_then_act_safe(self, key):
        """安全的检查-执行"""
        with self.lock:
            if key not in self.data:
                self.data[key] = []
            self.data[key].append("value")

    # 场景2: 读取-修改-写入竞态
    def read_modify_write_unsafe(self, key):
        """不安全的读取-修改-写入"""
        if key in self.data:
            value = self.data[key]  # 读取
            value += 1              # 修改
            # 此处可能发生竞态！
            self.data[key] = value  # 写入

    def read_modify_write_safe(self, key):
        """安全的读取-修改-写入"""
        with self.lock:
            if key in self.data:
                self.data[key] += 1

    # 场景3: 延迟初始化竞态
    _instance = None
    _instance_lock = threading.Lock()

    @classmethod
    def get_instance_unsafe(cls):
        """不安全的单例模式（可能创建多个实例）"""
        if cls._instance is None:
            # 此处可能发生竞态！
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_instance_safe(cls):
        """安全的单例模式（双检查锁）"""
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

print("\n" + "=" * 60)
print("常见竞态条件场景")
print("=" * 60)
print("""
场景1: 检查-执行竞态 (Check-Then-Act)
  if key not in dict:
      # 竞态窗口
      dict[key] = value

场景2: 读取-修改-写入竞态 (Read-Modify-Write)
  value = dict[key]
  value += 1
  # 竞态窗口
  dict[key] = value

场景3: 延迟初始化竞态 (Lazy Initialization)
  if instance is None:
      # 竞态窗口
      instance = create()

解决方案:
- 使用锁保护临界区
- 使用原子操作
- 使用线程安全的数据结构
""")
```

---

### 6.4 线程转储分析

#### 概念定义

线程转储（Thread Dump）是程序运行时所有线程状态的快照，用于诊断死锁、性能问题等。

#### 获取线程转储

```python
import threading
import sys
import traceback

def get_thread_dump():
    """获取线程转储"""
    print("=" * 60)
    print("线程转储分析")
    print("=" * 60)

    # 获取所有线程
    threads = threading.enumerate()
    print(f"\n当前活动线程数: {len(threads)}")
    print("-" * 60)

    for thread in threads:
        print(f"\n线程名: {thread.name}")
        print(f"线程ID: {thread.ident}")
        print(f"守护线程: {thread.daemon}")
        print(f"是否活动: {thread.is_alive()}")

        # 获取线程堆栈
        frame = sys._current_frames().get(thread.ident)
        if frame:
            print("堆栈跟踪:")
            traceback.print_stack(frame)
        print("-" * 60)

def simulate_threads():
    """模拟多个线程"""
    import time

    def worker_a():
        for i in range(10):
            time.sleep(1)

    def worker_b():
        for i in range(10):
            time.sleep(1)

    t1 = threading.Thread(target=worker_a, name="Worker-A")
    t2 = threading.Thread(target=worker_b, name="Worker-B")

    t1.start()
    t2.start()

    # 获取线程转储
    time.sleep(0.5)
    get_thread_dump()

    t1.join(timeout=1)
    t2.join(timeout=1)

# simulate_threads()
```

#### 死锁检测代码

```python
import threading

def detect_deadlock():
    """检测潜在的死锁"""
    print("\n" + "=" * 60)
    print("死锁检测")
    print("=" * 60)

    # 检查锁的获取顺序
    print("""
死锁检测方法:

1. 代码审查
   - 检查是否存在循环锁依赖
   - 确认所有线程按相同顺序获取锁

2. 运行时检测
   - 使用超时机制
   - 监控线程等待时间

3. 工具检测
   - Python: threading.enumerate() 查看线程状态
   - 使用 faulthandler 模块获取崩溃转储
   - 第三方工具: py-spy, manhole

4. 静态分析
   - 使用 pylint, mypy 检查代码
   - 专门的并发分析工具
""")

    # 演示如何检测长时间等待
    print("\n检测长时间等待的示例:")

    class TimeoutLock:
        """带超时的锁"""

        def __init__(self, name):
            self.lock = threading.Lock()
            self.name = name

        def acquire(self, timeout=5):
            if not self.lock.acquire(timeout=timeout):
                raise TimeoutError(
                    f"获取锁 {self.name} 超时，可能存在死锁！"
                )
            return True

        def release(self):
            self.lock.release()

        def __enter__(self):
            self.acquire()
            return self

        def __exit__(self, *args):
            self.release()

    lock_a = TimeoutLock("A")
    lock_b = TimeoutLock("B")

    def safe_worker_1():
        try:
            with lock_a:
                print("[Worker-1] 获得 Lock A")
                with lock_b:
                    print("[Worker-1] 获得 Lock B")
        except TimeoutError as e:
            print(f"[Worker-1] 错误: {e}")

    def safe_worker_2():
        try:
            with lock_b:
                print("[Worker-2] 获得 Lock B")
                with lock_a:
                    print("[Worker-2] 获得 Lock A")
        except TimeoutError as e:
            print(f"[Worker-2] 错误: {e}")

    # 注意：这里仍然可能死锁，但会超时
    # t1 = threading.Thread(target=safe_worker_1)
    # t2 = threading.Thread(target=safe_worker_2)
    # t1.start()
    # t2.start()

detect_deadlock()
```

---

## 总结

### 并发模型对比

| 特性 | 多线程 | 多进程 | 异步IO |
|------|--------|--------|--------|
| 适用场景 | IO密集型 | CPU密集型 | 高并发IO |
| GIL影响 | 是 | 否 | 否 |
| 内存共享 | 是 | 否（需IPC） | 是（单线程） |
| 切换开销 | 低 | 高 | 最低 |
| 编程复杂度 | 中 | 中 | 高 |
| 调试难度 | 高 | 中 | 中 |

### 选择指南

```
                    任务类型
                      │
        ┌─────────────┼─────────────┐
        │             │             │
    IO密集型      CPU密集型      混合类型
        │             │             │
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ asyncio │   │multipro-│   │ 组合使用 │
   │threading│   │cessing  │   │         │
   └─────────┘   └─────────┘   └─────────┘
```

### 最佳实践

1. **避免共享状态**：尽量使用消息传递而非共享内存
2. **最小化临界区**：锁保护的代码越少越好
3. **统一锁顺序**：多个锁时始终按相同顺序获取
4. **使用高级抽象**：优先使用线程池、进程池、asyncio
5. **超时机制**：所有等待操作都应设置超时
6. **测试并发**：使用压力测试发现竞态条件

---

*文档生成时间: 2024年*
*Python版本: 3.8+*
