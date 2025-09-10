# FastAPI 最小应用

[部署与压测指引](../../部署与压测指引.md)

> CI: GitHub Actions 工作流 `fastapi_min_ci`（测试 + 构建镜像 + 可选推送 GHCR）

## 依赖

- 快速安装（推荐 uv）：
  - `uv pip install -e .[dev]`
- 或使用 pip：`pip install fastapi uvicorn sqlalchemy aiosqlite`

## 测试

```bash
pytest -q
```

## Docker 与 Compose

- 构建与启动：

```bash
docker compose up --build -d
```

- 访问：
  - 应用：`http://127.0.0.1:8000`
  - Nginx：`http://127.0.0.1/`
  - Prometheus：`http://127.0.0.1:9090`
  - Grafana：`http://127.0.0.1:3000`（默认 admin/admin）
  - Alertmanager：`http://127.0.0.1:9093`

## 安全加固

- CORS：仅允许 `http://127.0.0.1`、`http://localhost`
- 请求体限制：超过 1MB 返回 `413`
- 审计：简单中间件示例（可替换为结构化日志）

## 分环境配置与统一错误

- 通过环境变量加载：`APP_ENV=dev|stage|prod`、`APP_APP_NAME` 等（见 `settings.py`）
- 可复制 `ENV_EXAMPLE` 为 `.env` 并按需修改（如使用 `python-dotenv` 或部署平台自动注入）
- 统一错误响应：`{"detail": "..."}`（见 `ErrorResp` 模型）

## 启动（本地）

- Windows PowerShell：`$env:APP_ENV="dev"; uvicorn app:app --reload --port 8000`
- *nix：`APP_ENV=dev uvicorn app:app --reload --port 8000`

## OpenAPI 与授权

- 文档：`http://127.0.0.1:8000/docs`（Swagger UI），`/redoc`（ReDoc）
- 标签：core/items/users/security/tasks/jobs（见页面左侧 Tags）
- 受保护接口 `/protected`：在文档页右上角“Authorize”中，`X-API-Key` 设置为 `APP_APP_NAME`（默认 `fastapi-min`）即可调试
- Bearer/JWT：在文档中先调用 `/token` 获取 `access_token`，再在“Authorize”中选择 Bearer 输入 `access_token` 测试 `/me`

## 新端点与演示

- `/health`：返回 `status` 与 `env`
- `/items`（POST）：创建 Item，请求体为 `{name, price}`
- `/v1/ping`：路由分组（APIRouter）示例
- `/users`：异步 SQLite + SQLAlchemy（创建/分页列表）
- `/protected`：API Key 保护（请求头 `X-API-Key`，默认示例以 `APP_APP_NAME` 作为密钥）
- `/token` `/me`：Bearer/JWT 签发与校验
- `/tasks`：后台任务排队示例
- `/jobs`：APScheduler 调度（新增/列表）
- `/metrics`：Prometheus 指标

## CLI 演示（cli_demo.py）

- 运行：

```bash
python cli_demo.py  # 可选环境变量 BASE/X_API_KEY
```

## 响应模型版本化与分页/排序规范

- 版本化建议：路径 `/v1/...` 或 Header `X-API-Version: 1`
- 分页：请求 `limit/offset`，响应 `Page{ total, items }`
- 排序（可选）：`sort=field`，`order=asc|desc`

## 返回与相关

- 返回目录：[@SUMMARY](../../../SUMMARY.md)
- 上级主题：[05-Web开发/README](../../README.md)
