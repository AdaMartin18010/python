# 多阶段构建 Dockerfile
# Python 监控示例应用

# ========== 阶段1: 构建阶段 ==========
FROM python:3.12-slim as builder

# 设置工作目录
WORKDIR /build

# 安装uv
RUN pip install --no-cache-dir uv==0.4.0

# 复制依赖文件
COPY requirements.txt .

# 安装依赖到虚拟环境
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache-dir -r requirements.txt

# ========== 阶段2: 运行阶段 ==========
FROM python:3.12-slim

# 安装必要的系统包
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1001 appuser

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 复制应用代码
COPY complete_monitoring_app.py .

# 修改所有权
RUN chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 设置环境变量
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "complete_monitoring_app:app", "--host", "0.0.0.0", "--port", "8000"]

