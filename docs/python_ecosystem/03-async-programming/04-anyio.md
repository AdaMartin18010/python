# AnyIO 异步兼容层

**统一的异步API**

---

## 📋 概述

AnyIO提供统一的异步API，兼容asyncio和trio，让代码可以在两个框架间无缝切换。

### 核心特性

- 🔄 **框架中立** - 支持asyncio和trio
- 🎯 **统一API** - 一套代码两个框架
- 🔧 **易于测试** - 简化异步测试
- 📦 **开箱即用** - 常用功能内置

---

## 🚀 快速开始

### 安装

```bash
uv add anyio
```

### 基本使用

```python
import anyio

async def main():
    print("Hello")
    await anyio.sleep(1)
    print("World")

# 使用asyncio运行
anyio.run(main, backend='asyncio')

# 或使用trio运行
anyio.run(main, backend='trio')
```

---

## 💻 核心功能

### 任务组

```python
async def task(name, delay):
    await anyio.sleep(delay)
    print(f"{name} done")

async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(task, "Task 1", 1)
        tg.start_soon(task, "Task 2", 2)

anyio.run(main)
```

### 取消和超时

```python
async def main():
    with anyio.move_on_after(1):
        await slow_operation()
        print("Completed")
```

### 文件I/O

```python
async def main():
    async with await anyio.open_file('data.txt', 'w') as f:
        await f.write('Hello, AnyIO!')
    
    async with await anyio.open_file('data.txt', 'r') as f:
        content = await f.read()
        print(content)
```

---

## 🌐 网络操作

```python
from anyio import connect_tcp

async def main():
    async with await connect_tcp('example.com', 80) as stream:
        await stream.send(b'GET / HTTP/1.0\r\n\r\n')
        response = await stream.receive()
        print(response)
```

---

## 📚 最佳实践

### 库开发

```python
# 使用AnyIO开发的库可以同时支持asyncio和trio
import anyio

async def my_async_library_function():
    async with anyio.create_task_group() as tg:
        tg.start_soon(background_task)
        result = await main_operation()
    return result
```

---

## 🔗 相关资源

- [官方文档](https://anyio.readthedocs.io/)

---

**最后更新**: 2025年10月28日

