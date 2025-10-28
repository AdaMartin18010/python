# APM 应用性能监控

**Application Performance Monitoring**

---

## 📋 概述

APM（应用性能监控）是监控应用性能和用户体验的实践，帮助快速定位和解决性能问题。

### 核心指标

- 📊 **响应时间** - 请求处理时长
- 🔄 **吞吐量** - 每秒处理请求数
- ❌ **错误率** - 失败请求比例
- 🎯 **Apdex** - 用户满意度指标
- 📈 **资源使用** - CPU、内存、I/O

---

## 🚀 Elastic APM

### 安装和配置

```bash
uv add elastic-apm
```

```python
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from fastapi import FastAPI

app = FastAPI()

apm = make_apm_client({
    'SERVICE_NAME': 'my-fastapi-app',
    'SECRET_TOKEN': os.getenv('APM_SECRET_TOKEN'),
    'SERVER_URL': 'http://apm-server:8200',
    'ENVIRONMENT': 'production',
    'CAPTURE_BODY': 'all',
    'TRANSACTION_SAMPLE_RATE': 1.0
})

app.add_middleware(ElasticAPM, client=apm)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### 自定义跨度

```python
import elasticapm

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # 自定义跨度
    with elasticapm.capture_span('database_query'):
        user = await db.get_user(user_id)
    
    with elasticapm.capture_span('cache_lookup'):
        cached = await redis.get(f'user:{user_id}')
    
    return user
```

---

## 🎯 Datadog APM

### 集成

```bash
uv add ddtrace
```

```python
from ddtrace import tracer
from ddtrace.contrib.fastapi import patch

# 自动打补丁
patch()

app = FastAPI()

@app.get("/api/data")
async def get_data():
    # 自动跟踪
    with tracer.trace("custom.operation", service="api"):
        result = perform_operation()
    
    return result
```

### 自定义指标

```python
from ddtrace import tracer
from datadog import statsd

# 计数器
statsd.increment('api.requests', tags=['endpoint:/users'])

# 计时器
with statsd.timed('database.query.duration'):
    result = db.query()

# 仪表盘
statsd.gauge('active_connections', 42)

# 设置标签
span = tracer.current_span()
span.set_tag('user.id', user_id)
span.set_tag('user.tier', 'premium')
```

---

## 🔍 New Relic

### 配置

```bash
uv add newrelic
```

```python
import newrelic.agent

# 初始化（应在所有导入之前）
newrelic.agent.initialize('newrelic.ini')

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@newrelic.agent.function_trace()
async def root():
    return {"message": "Hello"}
```

```ini
# newrelic.ini
[newrelic]
license_key = YOUR_LICENSE_KEY
app_name = My FastAPI App
monitor_mode = true
log_level = info

[newrelic:production]
app_name = My FastAPI App (Production)
```

### 自定义事件

```python
import newrelic.agent

@app.post("/orders")
async def create_order(order: Order):
    # 记录自定义事件
    newrelic.agent.record_custom_event(
        'OrderCreated',
        {
            'order_id': order.id,
            'amount': order.total,
            'user_id': order.user_id
        }
    )
    
    return order
```

---

## 📊 Sentry性能监控

```bash
uv add sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[
        StarletteIntegration(),
        FastApiIntegration(),
    ],
    # 性能监控
    traces_sample_rate=1.0,
    # 错误采样
    sample_rate=1.0,
    environment="production",
)

app = FastAPI()

@app.get("/")
async def root():
    # 自动性能跟踪
    return {"message": "Hello"}
```

### 自定义性能追踪

```python
import sentry_sdk

@app.get("/complex-operation")
async def complex_operation():
    # 创建事务
    with sentry_sdk.start_transaction(op="task", name="complex_operation"):
        # 创建子跨度
        with sentry_sdk.start_span(op="db", description="fetch_users"):
            users = await db.get_users()
        
        with sentry_sdk.start_span(op="http", description="call_api"):
            data = await external_api.fetch()
        
        with sentry_sdk.start_span(op="process", description="transform_data"):
            result = transform(users, data)
    
    return result
```

---

## 🎨 自定义APM

### 基础追踪器

```python
from contextvars import ContextVar
from datetime import datetime
from typing import Optional
import uuid

# 上下文变量
trace_id_var: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
span_stack: ContextVar[list] = ContextVar('span_stack', default=[])

class Span:
    def __init__(self, name: str, operation: str):
        self.span_id = str(uuid.uuid4())
        self.name = name
        self.operation = operation
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.tags: dict = {}
        self.logs: list = []
    
    def finish(self):
        self.end_time = datetime.now()
    
    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0
    
    def set_tag(self, key: str, value: any):
        self.tags[key] = value
    
    def log(self, message: str):
        self.logs.append({
            'timestamp': datetime.now().isoformat(),
            'message': message
        })

class Tracer:
    def __init__(self):
        self.spans: dict[str, list[Span]] = {}
    
    def start_span(self, name: str, operation: str = "custom") -> Span:
        # 获取或创建trace_id
        trace_id = trace_id_var.get()
        if not trace_id:
            trace_id = str(uuid.uuid4())
            trace_id_var.set(trace_id)
        
        # 创建span
        span = Span(name, operation)
        
        # 添加到栈
        stack = span_stack.get([])
        stack.append(span)
        span_stack.set(stack)
        
        return span
    
    def finish_span(self, span: Span):
        span.finish()
        
        # 从栈中移除
        stack = span_stack.get([])
        if stack and stack[-1] == span:
            stack.pop()
        
        # 保存span
        trace_id = trace_id_var.get()
        if trace_id not in self.spans:
            self.spans[trace_id] = []
        self.spans[trace_id].append(span)
    
    def get_trace(self, trace_id: str) -> list[Span]:
        return self.spans.get(trace_id, [])

# 全局追踪器
tracer = Tracer()

# 上下文管理器
class trace_span:
    def __init__(self, name: str, operation: str = "custom"):
        self.name = name
        self.operation = operation
        self.span: Optional[Span] = None
    
    def __enter__(self):
        self.span = tracer.start_span(self.name, self.operation)
        return self.span
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            if exc_type:
                self.span.set_tag('error', True)
                self.span.log(f'Exception: {exc_val}')
            tracer.finish_span(self.span)

# 使用
@app.get("/api/data")
async def get_data():
    with trace_span("database_query", "db"):
        data = await db.query()
    
    with trace_span("transform_data", "process"):
        result = transform(data)
    
    return result
```

---

## 📈 性能优化实践

### 1. N+1查询检测

```python
from collections import defaultdict

class QueryMonitor:
    def __init__(self):
        self.queries: defaultdict[str, int] = defaultdict(int)
    
    def record_query(self, query: str):
        self.queries[query] += 1
    
    def check_n_plus_one(self, threshold: int = 10):
        for query, count in self.queries.items():
            if count > threshold:
                sentry_sdk.capture_message(
                    f"Potential N+1 query detected: {query} executed {count} times",
                    level='warning'
                )

monitor = QueryMonitor()

@app.get("/users")
async def list_users():
    with monitor:
        users = await db.get_users()
        # 如果这里有N+1查询，会被检测到
        for user in users:
            user.posts = await db.get_user_posts(user.id)
    
    return users
```

### 2. 慢查询日志

```python
import logging
from functools import wraps
import time

slow_query_logger = logging.getLogger('slow_queries')

def log_slow_query(threshold_ms: float = 100):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            
            if duration > threshold_ms:
                slow_query_logger.warning(
                    f"Slow query: {func.__name__} took {duration:.2f}ms"
                )
            
            return result
        return wrapper
    return decorator

@log_slow_query(threshold_ms=200)
async def complex_query():
    return await db.execute_complex_query()
```

---

## 🎯 SLA监控

```python
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class SLAMetrics:
    """SLA指标"""
    availability: float  # 可用性 %
    response_time_p95: float  # P95响应时间 ms
    error_rate: float  # 错误率 %

class SLAMonitor:
    def __init__(self, target_availability: float = 99.9):
        self.target_availability = target_availability
        self.requests: list = []
    
    def record_request(self, success: bool, duration_ms: float):
        self.requests.append({
            'timestamp': datetime.now(),
            'success': success,
            'duration_ms': duration_ms
        })
    
    def calculate_sla(self, window: timedelta = timedelta(hours=1)) -> SLAMetrics:
        cutoff = datetime.now() - window
        recent = [r for r in self.requests if r['timestamp'] > cutoff]
        
        if not recent:
            return SLAMetrics(100.0, 0.0, 0.0)
        
        # 可用性
        successful = sum(1 for r in recent if r['success'])
        availability = (successful / len(recent)) * 100
        
        # P95响应时间
        durations = sorted([r['duration_ms'] for r in recent])
        p95_index = int(len(durations) * 0.95)
        p95 = durations[p95_index] if durations else 0.0
        
        # 错误率
        error_rate = ((len(recent) - successful) / len(recent)) * 100
        
        return SLAMetrics(availability, p95, error_rate)
```

---

## 📚 最佳实践

### 1. 采样策略

```python
import random

def should_trace() -> bool:
    """10%采样率"""
    return random.random() < 0.1

@app.get("/api/data")
async def get_data():
    if should_trace():
        with tracer.trace("get_data"):
            return await fetch_data()
    else:
        return await fetch_data()
```

### 2. 关键事务优先

```python
# 始终追踪关键事务
CRITICAL_ENDPOINTS = ['/checkout', '/payment', '/login']

@app.middleware("http")
async def apm_middleware(request, call_next):
    should_trace = (
        request.url.path in CRITICAL_ENDPOINTS or
        random.random() < 0.1  # 其他10%采样
    )
    
    if should_trace:
        with tracer.trace(request.url.path):
            response = await call_next(request)
    else:
        response = await call_next(request)
    
    return response
```

---

## 🔗 相关资源

- [Elastic APM文档](https://www.elastic.co/guide/en/apm/get-started/current/overview.html)
- [Datadog APM](https://docs.datadoghq.com/tracing/)
- [New Relic APM](https://docs.newrelic.com/docs/apm/)

---

**最后更新**: 2025年10月28日

