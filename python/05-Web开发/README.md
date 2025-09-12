# 05-Web开发

聚焦现代 Python Web：FastAPI、Starlette、ASGI、中间件与部署。

## 1. 框架与协议

- ASGI 协议与服务器（uvicorn、hypercorn）
- FastAPI/Starlette 的关系与生态

## 2. 路由与依赖注入

- 路由/请求体/响应模型（pydantic）
- 依赖注入与生命周期

## 3. 中间件与安全

- 身份验证、授权、CORS、速率限制

## 4. 部署与运维

- 进程管理（uvicorn workers）
- 容器化与反向代理（Nginx/Caddy）

### 4.1 性能与部署建议（最小集合）

- 服务器：`uvicorn --workers (CPU核数) --loop uvloop --http h11`（如可用）
- 超时与连接：配置 `--timeout-keep-alive`，前置反代设置连接复用与压缩
- 观察性：启用结构化日志、请求ID、中间件级别的计时
- 压测基线：`wrk`/`bombardier` 对 `/health` 与典型业务路由进行RPS与P95
- 容器化：基于 `python:3.12-slim`，多阶段构建 + `uv` 同步依赖 + 非root用户

### 4.2 示例 Dockerfile 片段（简化）

```Dockerfile
FROM python:3.12-slim AS base
RUN pip install --no-cache-dir uv && useradd -m app
WORKDIR /app
COPY pyproject.toml .
RUN uv pip compile pyproject.toml -o uv.lock && uv pip sync uv.lock
COPY . .
USER app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 5. 示例（最小）

- 位置：`./examples/fastapi_min/app.py`
- 运行：`uvicorn app:app --reload --port 8000`
- 健康检查：`GET http://127.0.0.1:8000/health`
- 测试建议：使用 `httpx`/`pytest` 进行集成测试

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)
- 相关主题：[02-测试与质量/README](../02-测试与质量/README.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)