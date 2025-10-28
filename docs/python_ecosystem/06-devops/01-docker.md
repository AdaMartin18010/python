# Docker 容器化

**容器化应用的标准工具**

---

## 📋 概述

Docker是一个开源的容器化平台，允许开发者将应用及其依赖打包到轻量级、可移植的容器中。

### 核心特性

- 📦 **容器化** - 应用和依赖打包
- 🚀 **快速部署** - 秒级启动
- 🔄 **一致环境** - 开发/生产一致
- 💾 **资源高效** - 比虚拟机轻量
- 🔧 **易于管理** - 简单的CLI工具

---

## 🚀 快速开始

### Python应用Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t myapp:latest .

# 运行容器
docker run -p 8000:8000 myapp:latest

# 后台运行
docker run -d -p 8000:8000 --name myapp myapp:latest
```

---

## 💻 核心命令

### 镜像管理

```bash
# 列出镜像
docker images

# 拉取镜像
docker pull python:3.12

# 删除镜像
docker rmi myapp:latest

# 清理未使用镜像
docker image prune -a
```

### 容器管理

```bash
# 列出运行中容器
docker ps

# 列出所有容器
docker ps -a

# 停止容器
docker stop myapp

# 启动容器
docker start myapp

# 删除容器
docker rm myapp

# 查看日志
docker logs myapp
docker logs -f myapp  # 实时日志

# 进入容器
docker exec -it myapp bash
```

---

## 🏗️ 多阶段构建

### 优化镜像大小

```dockerfile
# 构建阶段
FROM python:3.12 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 运行阶段
FROM python:3.12-slim

WORKDIR /app

# 只复制必需文件
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

---

## 🔧 Docker Compose

### 多容器应用

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
    command: uvicorn main:app --host 0.0.0.0 --reload

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Compose命令

```bash
# 启动所有服务
docker-compose up

# 后台启动
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看日志
docker-compose logs -f web

# 重建并启动
docker-compose up --build
```

---

## 📚 最佳实践

### 1. 使用.dockerignore

```
# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.git
.gitignore
.pytest_cache
.vscode
*.md
```

### 2. 优化层缓存

```dockerfile
# ✅ 好 - 依赖先复制
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ 差 - 每次都重新安装
COPY . .
RUN pip install -r requirements.txt
```

### 3. 使用非root用户

```dockerfile
FROM python:3.12-slim

RUN useradd -m -u 1000 appuser
USER appuser

WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . .

CMD ["python", "app.py"]
```

---

## 🔗 相关资源

- [官方文档](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [最佳实践](https://docs.docker.com/develop/dev-best-practices/)

---

**最后更新**: 2025年10月28日

