# Trio 结构化并发

**友好的异步I/O库**

---

## 📋 概述

Trio是一个现代异步I/O库，专注于可用性和正确性，引入了结构化并发概念。

### 核心特性

- 🎯 **结构化并发** - 任务层次结构
- 🔒 **取消作用域** - 安全的任务取消
- 🛡️ **易于测试** - 内置测试工具
- 📚 **简洁API** - 比asyncio更直观

---

## 🚀 快速开始

### 安装

```bash
uv add trio
```

### Hello Trio

```python
import trio

async def main():
    print("Hello")
    await trio.sleep(1)
    print("World")

trio.run(main)
```

---

## 💻 核心功能

### 并发任务

```python
import trio

async def task(name, delay):
    print(f"{name} started")
    await trio.sleep(delay)
    print(f"{name} done")

async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(task, "Task 1", 1)
        nursery.start_soon(task, "Task 2", 2)
        # 等待所有任务完成

trio.run(main)
```

### 取消作用域

```python
async def main():
    try:
        with trio.move_on_after(1):  # 1秒超时
            await slow_operation()
            print("Completed")
    except trio.TooSlowError:
        print("Timeout!")
```

---

## 🔄 通道

```python
async def producer(send_channel):
    async with send_channel:
        for i in range(10):
            await send_channel.send(i)

async def consumer(receive_channel):
    async with receive_channel:
        async for value in receive_channel:
            print(f"Received: {value}")

async def main():
    send_channel, receive_channel = trio.open_memory_channel(0)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(producer, send_channel)
        nursery.start_soon(consumer, receive_channel)
```

---

## 📚 最佳实践

### 错误处理

```python
async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(task1)
        nursery.start_soon(task2)
    # 如果任何任务出错，nursery会传播异常
```

---

## 🔗 相关资源

- [官方文档](https://trio.readthedocs.io/)
- [教程](https://trio.readthedocs.io/en/stable/tutorial.html)

---

**最后更新**: 2025年10月28日

