# 发布说明（本轮多任务推进）

## 概览

- 全链路完善：开发→规范→OpenAPI→安全（API Key/JWT+CORS/体积限制）→分页→任务/调度→指标→部署与压测→容器编排→端到端测试→CI→镜像推送
- 可一键运行，导航无死链，lint 全绿

## 关键变更

- 文档/规范：新增 `python/05-Web开发/API_接口规范.md`、`python/05-Web开发/部署与压测指引.md`；修订 `SUMMARY.md`
- 工具与质量：根 `pyproject.toml`（ruff/mypy/pytest）、`.pre-commit-config.yaml`
- FastAPI 示例：安全（API Key/JWT+CORS/体积限制）、分页 Page、后台任务、APScheduler 调度、Prometheus 指标、Docker/Compose、端到端测试、CI 与 GHCR 推送

## 运行入口

- 示例：`python/05-Web开发/examples/fastapi_min/README.md`
- 规范与部署：`python/05-Web开发/API_接口规范.md`、`python/05-Web开发/部署与压测指引.md`

## 已知事项

- 演示用密钥/配置仅用于本地示例，生产需替换并接入 Secret 管理
