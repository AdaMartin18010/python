# Dockerfile - 2025年Python项目标准
# 多阶段构建，优化镜像大小

# =============================================================================
# 构建阶段
# =============================================================================
FROM python:3.12-slim as builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv（推荐）
RUN pip install --no-cache-dir uv

# 复制依赖文件
COPY pyproject.toml ./

# 创建虚拟环境并安装依赖
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install -e .

# =============================================================================
# 运行阶段
# =============================================================================
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 设置环境变量
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    # Python 3.13 优化
    PYTHONOPTIMIZE=1

# 复制应用代码
COPY --chown=appuser:appuser . .

# 切换到非root用户
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# 默认命令
CMD ["python", "-m", "my_modern_project"]

# 暴露端口（如果是Web应用）
# EXPOSE 8000

