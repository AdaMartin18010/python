# Grafana 可视化

**Prometheus数据可视化平台**

---

## 📋 概述

Grafana是开源的数据可视化和监控平台，支持多种数据源，提供美观的仪表板。

### 核心特性

- 📊 **多数据源** - Prometheus、InfluxDB、Elasticsearch等
- 🎨 **丰富图表** - 折线图、柱状图、热力图等
- 🔔 **告警** - 灵活的告警规则
- 👥 **团队协作** - 仪表板共享
- 📱 **移动端** - 响应式设计

---

## 🚀 快速开始

### Docker部署

```yaml
# docker-compose.yml
version: '3'
services:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-storage:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

volumes:
  grafana-storage:
```

### 访问

```bash
# 启动服务
docker-compose up -d

# 访问Grafana
http://localhost:3000
# 默认账号: admin / admin
```

---

## 📊 配置Prometheus数据源

### 手动配置

1. 登录Grafana
2. Configuration → Data Sources
3. Add data source → Prometheus
4. URL: `http://prometheus:9090`
5. Save & Test

### 代码配置

```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

---

## 🎨 创建仪表板

### Python应用仪表板

```json
{
  "dashboard": {
    "title": "FastAPI应用监控",
    "tags": ["python", "fastapi"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "请求速率",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ],
        "yaxes": [
          {"format": "reqps", "label": "请求/秒"},
          {"format": "short"}
        ]
      },
      {
        "id": 2,
        "title": "P95延迟",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "P95延迟"
          }
        ],
        "yaxes": [
          {"format": "s", "label": "延迟"},
          {"format": "short"}
        ]
      },
      {
        "id": 3,
        "title": "错误率",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "错误率"
          }
        ],
        "yaxes": [
          {"format": "percentunit", "label": "错误率"},
          {"format": "short"}
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [0.05], "type": "gt"},
              "query": {"params": ["A", "5m", "now"]}
            }
          ],
          "executionErrorState": "alerting",
          "frequency": "1m",
          "message": "错误率超过5%",
          "name": "高错误率告警"
        }
      },
      {
        "id": 4,
        "title": "活跃连接",
        "type": "stat",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "http_requests_active",
            "legendFormat": "活跃请求"
          }
        ],
        "options": {
          "colorMode": "value",
          "graphMode": "area",
          "orientation": "auto"
        }
      }
    ]
  }
}
```

---

## 📈 常用面板类型

### 1. 时间序列图

```json
{
  "type": "timeseries",
  "title": "CPU使用率",
  "targets": [
    {
      "expr": "rate(process_cpu_seconds_total[5m]) * 100",
      "legendFormat": "CPU %"
    }
  ]
}
```

### 2. Stat面板

```json
{
  "type": "stat",
  "title": "当前在线用户",
  "targets": [
    {
      "expr": "active_users"
    }
  ],
  "options": {
    "colorMode": "background",
    "graphMode": "none",
    "textMode": "value_and_name"
  }
}
```

### 3. 热力图

```json
{
  "type": "heatmap",
  "title": "请求延迟分布",
  "targets": [
    {
      "expr": "rate(http_request_duration_seconds_bucket[5m])"
    }
  ]
}
```

### 4. 表格

```json
{
  "type": "table",
  "title": "慢查询Top 10",
  "targets": [
    {
      "expr": "topk(10, rate(query_duration_seconds_sum[5m]) / rate(query_duration_seconds_count[5m]))",
      "format": "table"
    }
  ]
}
```

---

## 🔔 告警配置

### 配置告警通道

```yaml
# grafana/provisioning/alerting/notification-channels.yml
notifiers:
  - name: Email
    type: email
    uid: email1
    settings:
      addresses: "team@example.com"
  
  - name: Slack
    type: slack
    uid: slack1
    settings:
      url: "https://hooks.slack.com/services/..."
      recipient: "#alerts"
```

### 创建告警规则

```python
# Python脚本创建告警
import requests
import json

grafana_url = "http://localhost:3000"
api_key = "your-api-key"

alert_rule = {
    "name": "High Error Rate",
    "conditions": [
        {
            "evaluator": {"type": "gt", "params": [0.05]},
            "query": {
                "model": {
                    "expr": 'rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])'
                }
            }
        }
    ],
    "frequency": "1m",
    "message": "错误率超过5%",
    "notifications": [{"uid": "slack1"}]
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(
    f"{grafana_url}/api/alerts",
    headers=headers,
    data=json.dumps(alert_rule)
)
```

---

## 🎯 最佳实践

### 1. 仪表板组织

```
项目/
├── Overview Dashboard          # 总览
├── Application Performance     # 应用性能
│   ├── API Performance
│   ├── Database Performance
│   └── Cache Performance
├── Infrastructure              # 基础设施
│   ├── CPU & Memory
│   ├── Network
│   └── Disk I/O
└── Business Metrics            # 业务指标
    ├── User Activity
    ├── Revenue
    └── Conversion
```

### 2. 变量使用

```json
{
  "templating": {
    "list": [
      {
        "name": "environment",
        "type": "custom",
        "options": [
          {"text": "Production", "value": "prod"},
          {"text": "Staging", "value": "staging"}
        ]
      },
      {
        "name": "instance",
        "type": "query",
        "query": "label_values(up, instance)"
      }
    ]
  }
}
```

在查询中使用：
```
rate(http_requests_total{instance="$instance", env="$environment"}[5m])
```

### 3. 时间范围

```json
{
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "refresh": "1m"
}
```

---

## 📊 Python自动化

### 使用grafana-api

```python
from grafana_api.grafana_face import GrafanaFace

# 连接Grafana
grafana = GrafanaFace(
    auth=('admin', 'admin'),
    host='localhost',
    port=3000
)

# 创建仪表板
dashboard = {
    "dashboard": {
        "title": "My Dashboard",
        "panels": [...]
    },
    "overwrite": True
}

grafana.dashboard.update_dashboard(dashboard)

# 获取仪表板列表
dashboards = grafana.search.search_dashboards()

# 导出仪表板
dashboard_json = grafana.dashboard.get_dashboard("my-dashboard")
```

---

## 🔗 集成Python应用

### 导出指标到Grafana

```python
from prometheus_client import Counter, Histogram, Gauge
from prometheus_client import start_http_server
from fastapi import FastAPI

app = FastAPI()

# 定义指标
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

ACTIVE_USERS = Gauge('active_users', 'Number of active users')

# 在Grafana中可视化
# - 请求速率: rate(http_requests_total[5m])
# - P95延迟: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
# - 活跃用户: active_users
```

---

## 📚 常用PromQL查询

```promql
# QPS
rate(http_requests_total[5m])

# P95延迟
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# 错误率
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# 内存使用率
process_resident_memory_bytes / node_memory_MemTotal_bytes * 100

# CPU使用率
rate(process_cpu_seconds_total[5m]) * 100

# 按端点分组的请求数
sum(rate(http_requests_total[5m])) by (endpoint)
```

---

## 🔗 相关资源

- [Grafana官方文档](https://grafana.com/docs/)
- [仪表板示例](https://grafana.com/grafana/dashboards/)

---

**最后更新**: 2025年10月28日

