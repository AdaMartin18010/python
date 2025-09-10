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

## 5. 示例（最小）

- 位置：`./examples/fastapi_min/app.py`
- 运行：`uvicorn app:app --reload --port 8000`
- 健康检查：`GET http://127.0.0.1:8000/health`
- 测试建议：使用 `httpx`/`pytest` 进行集成测试
