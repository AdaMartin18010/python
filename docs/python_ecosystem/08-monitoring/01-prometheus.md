# Prometheus 监控

**Python应用指标监控**

---

## 📋 概述

Prometheus是开源的监控和告警系统，用于收集和存储时间序列数据。

### 核心特性

- 📊 **多维数据** - 基于标签的时间序列
- 🔍 **强大查询** - PromQL查询语言
- 📈 **可视化** - 集成Grafana
- 🔔 **告警** - AlertManager告警
- 🎯 **Pull模型** - 主动拉取指标

---

## 🚀 快速开始

### 安装客户端

```bash
uv add prometheus-client
```

### 基本示例

```python
from prometheus_client import Counter, Gauge, Histogram, Summary
from prometheus_client import start_http_server
import time

# 定义指标
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# 使用指标
REQUEST_COUNT.labels(method='GET', endpoint='/api/users', status='200').inc()
ACTIVE_USERS.set(42)

with REQUEST_DURATION.time():
    # 处理请求
    time.sleep(0.5)

# 启动指标服务器
start_http_server(8000)
```

---

## 🎯 指标类型

### 1. Counter (计数器)

```python
from prometheus_client import Counter

# 只能增加
http_requests = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'status']
)

http_requests.labels(method='GET', status='200').inc()
http_requests.labels(method='POST', status='201').inc(5)
```

### 2. Gauge (仪表盘)

```python
from prometheus_client import Gauge

# 可增可减
temperature = Gauge('room_temperature_celsius', 'Room temperature')

temperature.set(23.5)
temperature.inc(1.2)  # 增加
temperature.dec(0.5)  # 减少

# 使用函数设置值
def get_cpu_usage():
    import psutil
    return psutil.cpu_percent()

cpu_gauge = Gauge('cpu_usage_percent', 'CPU usage')
cpu_gauge.set_function(get_cpu_usage)
```

### 3. Histogram (直方图)

```python
from prometheus_client import Histogram

# 用于测量分布
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# 记录观测值
with request_duration.time():
    # 处理请求
    process_request()

# 或手动记录
request_duration.observe(0.75)
```

### 4. Summary (摘要)

```python
from prometheus_client import Summary

# 类似Histogram，但计算分位数
request_latency = Summary(
    'request_latency_seconds',
    'Request latency'
)

with request_latency.time():
    process_request()
```

---

## 🔌 FastAPI集成

### 完整集成

```python
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, make_asgi_app
import time

app = FastAPI()

# 定义指标
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active requests'
)

# 中间件
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    ACTIVE_REQUESTS.inc()
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    ACTIVE_REQUESTS.dec()
    
    return response

# 暴露指标端点
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

## 📊 业务指标

### 自定义业务指标

```python
from prometheus_client import Counter, Gauge, Histogram

# 订单指标
orders_created = Counter(
    'orders_created_total',
    'Total orders created',
    ['product_category']
)

orders_value = Histogram(
    'order_value_dollars',
    'Order value distribution',
    buckets=[10, 50, 100, 500, 1000, 5000]
)

inventory_stock = Gauge(
    'inventory_stock_items',
    'Current inventory stock',
    ['product_id']
)

# 使用
def create_order(product_category: str, value: float):
    orders_created.labels(product_category=product_category).inc()
    orders_value.observe(value)

def update_inventory(product_id: str, stock: int):
    inventory_stock.labels(product_id=product_id).set(stock)
```

---

## 🔍 PromQL查询

### 基本查询

```promql
# 请求总数
http_requests_total

# 过滤标签
http_requests_total{method="GET", status="200"}

# 速率（每秒）
rate(http_requests_total[5m])

# 求和
sum(rate(http_requests_total[5m])) by (endpoint)

# P95延迟
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# 错误率
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])
```

---

## 🎨 Grafana可视化

### Dashboard JSON

```json
{
  "dashboard": {
    "title": "FastAPI监控",
    "panels": [
      {
        "title": "请求速率",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "P95延迟",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

---

## 📈 最佳实践

### 1. 命名规范

```python
# ✅ 好的命名
http_requests_total          # 计数器加_total后缀
http_request_duration_seconds # 带单位
active_connections           # 当前状态用现在时

# ❌ 差的命名
requests                     # 太模糊
request_time                 # 缺少单位
total_requests               # total应该是后缀
```

### 2. 标签使用

```python
# ✅ 好 - 适度使用标签
http_requests_total{method="GET", status="200", endpoint="/api/users"}

# ❌ 差 - 高基数标签（user_id会有很多值）
http_requests_total{user_id="12345"}

# ❌ 差 - 时间戳作为标签
http_requests_total{timestamp="2025-10-28"}
```

### 3. 指标导出

```python
from prometheus_client import CollectorRegistry, write_to_textfile

# 批量作业指标
registry = CollectorRegistry()
g = Gauge('batch_job_last_success', 'Last successful batch job', registry=registry)
g.set_to_current_time()

write_to_textfile('/var/lib/prometheus/batch_job.prom', registry)
```

---

## 🐳 Docker部署

### docker-compose.yml

```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "8000:8000"
  
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### prometheus.yml

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['app:8000']
```

---

## 🔗 相关资源

- [Prometheus官方文档](https://prometheus.io/docs/)
- [PromQL查询指南](https://prometheus.io/docs/prometheus/latest/querying/basics/)

---

**最后更新**: 2025年10月28日

