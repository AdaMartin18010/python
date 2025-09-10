# FastAPI 最小应用

## 依赖

- 快速安装（推荐 uv）：
  - `uv pip install -e .[dev]`
- 或使用 pip：`pip install fastapi uvicorn sqlalchemy aiosqlite`

## 启动

- Windows PowerShell：`uvicorn app:app --reload --port 8000`
- *nix：`uvicorn app:app --reload --port 8000`

## 访问

- `http://127.0.0.1:8000`

## 进阶：依赖注入与中间件

- 依赖注入（示例）：

```python
from fastapi import Depends

class Settings:
    def __init__(self, env: str = "dev"):
        self.env = env

def get_settings() -> Settings:
    return Settings()

@app.get("/env")
def show_env(cfg: Settings = Depends(get_settings)) -> dict[str, str]:
    return {"env": cfg.env}
```

- 中间件（示例）：

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-App"] = "fastapi-min"
        return response

app.add_middleware(TraceMiddleware)
```

## 新端点与演示

- `/env`：查看环境
- `/items`（POST）：创建 Item，请求体为 `{name, price}`
- `/v1/ping`：路由分组（APIRouter）示例
- `/users`：异步 SQLite + SQLAlchemy（创建/列表）

```bash
# 查看健康
curl -s http://127.0.0.1:8000/health | jq .

# 查看环境
curl -s http://127.0.0.1:8000/env | jq .

# 创建 Item 成功
curl -s -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"book","price":9.9}' | jq .

# 路由分组 ping
curl -s http://127.0.0.1:8000/v1/ping | jq .

# 创建用户
curl -s -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"alice"}' | jq .

# 列表用户
curl -s http://127.0.0.1:8000/users | jq .
```

## 返回与相关

- 返回目录：[@SUMMARY](../../../SUMMARY.md)
- 上级主题：[05-Web开发/README](../../README.md)
