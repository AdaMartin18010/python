# OpenTelemetry 可观测性

**云原生可观测性统一标准**

---

## 📋 概述

OpenTelemetry是CNCF的可观测性框架，提供统一的API、SDK和工具来收集、处理和导出遥测数据（追踪、指标、日志）。

### 核心特性

- 🔍 **分布式追踪** - 请求链路追踪
- 📊 **指标收集** - 性能指标
- 📝 **日志关联** - 日志与追踪关联
- 🌐 **厂商中立** - 不绑定特定后端
- 🔌 **自动注入** - 自动化instrumentation

---

## 🚀 快速开始

### 安装

```bash
uv add opentelemetry-api opentelemetry-sdk
uv add opentelemetry-instrumentation-fastapi
uv add opentelemetry-exporter-jaeger
```

### FastAPI集成

```python
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# 配置追踪
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# 创建应用
app = FastAPI()

# 自动注入
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

## 🔍 分布式追踪

### 手动Span

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user_id", user_id)
        
        # 数据库查询
        with tracer.start_as_current_span("db_query"):
            user = await db.get_user(user_id)
        
        # 缓存操作
        with tracer.start_as_current_span("cache_set"):
            await cache.set(f"user:{user_id}", user)
        
        return user
```

### 自动注入

```python
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# HTTP请求自动追踪
RequestsInstrumentor().instrument()

# SQLAlchemy自动追踪
SQLAlchemyInstrumentor().instrument(engine=engine)
```

---

## 📊 指标收集

```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    ConsoleMetricExporter,
)

# 配置指标
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))

# 创建指标
meter = metrics.get_meter(__name__)
request_counter = meter.create_counter(
    "requests",
    description="Number of requests",
)
request_duration = meter.create_histogram(
    "request_duration",
    description="Request duration",
    unit="ms",
)

# 使用指标
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    
    request_counter.add(1, {"method": request.method, "path": request.url.path})
    request_duration.record(duration, {"method": request.method})
    
    return response
```

---

## 📚 最佳实践

### 1. 上下文传播

```python
from opentelemetry import propagate

# HTTP头中传播追踪上下文
headers = {}
propagate.inject(headers)

response = requests.get("http://api.example.com", headers=headers)
```

### 2. 采样策略

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

# 10%采样率
sampler = TraceIdRatioBased(0.1)
provider = TracerProvider(sampler=sampler)
```

---

## 🔗 相关资源

- [官方文档](https://opentelemetry.io/)
- [Python SDK](https://opentelemetry-python.readthedocs.io/)

---

**最后更新**: 2025年10月28日

