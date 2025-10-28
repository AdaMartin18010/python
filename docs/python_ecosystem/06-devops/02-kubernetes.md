# Kubernetes Python应用部署

**Python应用容器编排指南**

---

## 📋 概述

Kubernetes (K8s) 是容器编排平台，用于自动化容器化应用的部署、扩展和管理。

### 核心概念

- 🏗️ **Pod** - 最小部署单元
- 🎯 **Service** - 服务发现和负载均衡
- 📊 **Deployment** - 声明式更新
- 🔧 **ConfigMap** - 配置管理
- 🔐 **Secret** - 敏感信息管理

---

## 🚀 快速开始

### 部署FastAPI应用

#### 1. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Deployment配置

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  labels:
    app: fastapi
spec:
  replicas: 3  # 3个副本
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: myregistry/fastapi-app:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 3. Service配置

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## 🔧 配置管理

### ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_NAME: "My FastAPI App"
  LOG_LEVEL: "info"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
```

```python
# Python中读取
import os

app_name = os.getenv('APP_NAME', 'Default App')
log_level = os.getenv('LOG_LEVEL', 'info')
```

### Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  # base64编码
  url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0BkYjo1NDMyL2RibmFtZQ==
  password: bXlzZWNyZXRwYXNzd29yZA==
```

---

## 📊 水平扩展

### Horizontal Pod Autoscaler (HPA)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 🔄 滚动更新

```bash
# 更新镜像
kubectl set image deployment/fastapi-app \
  fastapi=myregistry/fastapi-app:v1.1.0

# 查看滚动状态
kubectl rollout status deployment/fastapi-app

# 回滚
kubectl rollout undo deployment/fastapi-app
```

### 更新策略

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 最多多1个pod
      maxUnavailable: 0  # 不允许不可用pod
```

---

## 💾 持久化存储

### PersistentVolumeClaim

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

```yaml
# 在Deployment中使用
spec:
  template:
    spec:
      containers:
      - name: app
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: app-data-pvc
```

---

## 🔒 安全最佳实践

### 1. 非root用户运行

```dockerfile
FROM python:3.12-slim

# 创建非root用户
RUN useradd -m -u 1000 appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### 2. 资源限制

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "100m"
  limits:
    memory: "128Mi"
    cpu: "200m"
```

### 3. 安全上下文

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

---

## 📈 监控和日志

### 健康检查

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ready")
def readiness_check():
    # 检查数据库连接等
    if database.is_connected():
        return {"status": "ready"}
    return {"status": "not ready"}, 503
```

### Prometheus集成

```python
from prometheus_client import Counter, Histogram, make_asgi_app
from fastapi import FastAPI

app = FastAPI()

# 添加Prometheus指标端点
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# 定义指标
REQUEST_COUNT = Counter('requests_total', 'Total requests')
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    REQUEST_COUNT.inc()
    with REQUEST_DURATION.time():
        response = await call_next(request)
    return response
```

---

## 🔗 服务间通信

### Service Discovery

```python
import os
import httpx

# 使用Kubernetes Service DNS
redis_host = os.getenv('REDIS_HOST', 'redis-service')
database_host = os.getenv('DATABASE_HOST', 'postgres-service')

async with httpx.AsyncClient() as client:
    # 调用其他服务
    response = await client.get(f'http://user-service/api/users/1')
```

---

## 📚 常用命令

```bash
# 部署应用
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 查看状态
kubectl get pods
kubectl get services
kubectl get deployments

# 查看日志
kubectl logs -f <pod-name>

# 进入容器
kubectl exec -it <pod-name> -- /bin/bash

# 扩缩容
kubectl scale deployment/fastapi-app --replicas=5

# 删除资源
kubectl delete -f deployment.yaml
```

---

## 🔗 相关资源

- [Kubernetes官方文档](https://kubernetes.io/docs/)
- [FastAPI部署指南](https://fastapi.tiangolo.com/deployment/)

---

**最后更新**: 2025年10月28日

