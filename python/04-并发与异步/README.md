# 04-并发与异步

聚焦多线程、多进程、异步（asyncio/Trio）与并行化模式。

## 1. 并发模型

- 线程、进程、协程对比与适用性
- I/O 密集 vs CPU 密集

## 2. asyncio 实践

- 任务、事件循环、超时与取消
- 限流、重试与背压
- 示例：`./examples/asyncio_rate_limit/main.py`
  - 运行：`python main.py`

## 3. Trio/其他运行时（占位）

- 结构化并发思想

## 4. 并行与性能

- 进程池/线程池
- GIL 影响与规避策略

## 5. 示例与模式（占位）

- 最小 asyncio 示例与测试建议
