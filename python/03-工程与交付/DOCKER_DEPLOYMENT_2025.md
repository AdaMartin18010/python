# Docker 部署指南（2025年标准）

## 1. 多阶段Docker构建（2025最佳实践）

### 1.1 优化的Dockerfile

```dockerfile
# Dockerfile - 2025年Python项目标准
# 特点：多阶段构建、最小化镜像、安全性

# =============================================================================
# 阶段1：构建阶段
# =============================================================================
FROM python:3.12-slim AS builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv（超快包管理器）
RUN pip install --no-cache-dir uv

# 复制依赖文件
COPY pyproject.toml ./
COPY uv.lock* ./

# 创建虚拟环境并安装依赖
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv sync --frozen --no-dev

# 复制源代码
COPY src/ ./src/

# 构建wheel包
RUN uv build

# =============================================================================
# 阶段2：运行阶段
# =============================================================================
FROM python:3.12-slim

# 设置元数据
LABEL maintainer="your.email@example.com"
LABEL version="1.0.0"
LABEL description="Modern Python application 2025"

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/dist/*.whl /tmp/

# 安装应用
RUN /opt/venv/bin/pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*.whl

# 设置环境变量
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    # Python 3.12+ 优化
    PYTHONOPTIMIZE=1 \
    # 应用配置
    APP_ENV=production \
    APP_PORT=8000

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# 启动命令
CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 1.2 .dockerignore（2025标准）

```bash
# .dockerignore - 减小构建上下文

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# 虚拟环境
.venv/
venv/
ENV/

# 测试和覆盖率
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/

# IDE
.vscode/
.idea/
*.swp

# Git
.git/
.gitignore
.gitattributes

# CI/CD
.github/
.gitlab-ci.yml

# 文档
docs/
*.md
!README.md

# 开发工具
.pre-commit-config.yaml
.editorconfig

# 临时文件
*.log
*.tmp
.DS_Store
```

## 2. Docker Compose配置（2025标准）

### 2.1 开发环境

```yaml
# docker-compose.yml - 开发环境
version: '3.9'

services:
  # 应用服务
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder  # 使用构建阶段进行开发
    container_name: myapp-dev
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src:ro  # 挂载源代码（只读）
      - ./tests:/app/tests:ro
    environment:
      - APP_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s

  # PostgreSQL数据库
  db:
    image: postgres:16-alpine
    container_name: myapp-db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis缓存
  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Nginx反向代理
  nginx:
    image: nginx:1.27-alpine
    container_name: myapp-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### 2.2 生产环境

```yaml
# docker-compose.prod.yml - 生产环境
version: '3.9'

services:
  app:
    image: myapp:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
    environment:
      - APP_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    secrets:
      - db_password
      - api_key
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

secrets:
  db_password:
    external: true
  api_key:
    external: true
```

## 3. Kubernetes部署（2025标准）

### 3.1 Deployment配置

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.0.0
    spec:
      # 使用非root用户
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      # 镜像拉取密钥
      imagePullSecrets:
        - name: registry-secret

      containers:
      - name: myapp
        image: myregistry.io/myapp:1.0.0
        imagePullPolicy: Always
        
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP

        # 环境变量
        env:
        - name: APP_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: myapp-config
              key: redis-url

        # 资源限制
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # 存活探针
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3

        # 就绪探针
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        # 启动探针（Python 3.12+ 启动可能较慢）
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 0
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 30

        # 挂载卷
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true

      volumes:
      - name: config
        configMap:
          name: myapp-config

      # Pod反亲和性（高可用）
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp
              topologyKey: kubernetes.io/hostname
```

### 3.2 Service配置

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8000
    protocol: TCP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

### 3.3 Ingress配置

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

### 3.4 HPA自动扩缩容

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max
```

## 4. CI/CD流水线（2025标准）

### 4.1 GitHub Actions完整流程

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 构建和测试
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        run: uv run pytest --cov

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  # 构建Docker镜像
  build-image:
    needs: build-test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # 部署到Kubernetes
  deploy:
    needs: build-image
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f k8s/
          kubectl rollout status deployment/myapp -n production
```

## 5. 最佳实践清单

### ✅ Docker最佳实践
- ✅ 使用多阶段构建减小镜像大小
- ✅ 使用非root用户运行容器
- ✅ 添加健康检查
- ✅ 使用.dockerignore减小构建上下文
- ✅ 固定基础镜像版本
- ✅ 合并RUN命令减少层数
- ✅ 清理apt缓存

### ✅ Kubernetes最佳实践
- ✅ 设置资源请求和限制
- ✅ 配置存活探针和就绪探针
- ✅ 使用HPA自动扩缩容
- ✅ 配置Pod反亲和性
- ✅ 使用滚动更新策略
- ✅ 配置TLS/SSL
- ✅ 使用ConfigMap和Secret管理配置

### ✅ CI/CD最佳实践
- ✅ 自动化测试
- ✅ 代码质量检查
- ✅ 安全扫描
- ✅ 镜像缓存加速构建
- ✅ 多环境部署
- ✅ 回滚机制

---

**更新日期：** 2025年10月24日  
**适用版本：** Python 3.12+, Docker 27+, Kubernetes 1.30+

