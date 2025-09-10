# 发布材料包（变更清单 + 路线图 + 入口）

## 变更清单（摘要）

- 文档/规范：API 接口规范、部署与压测指引、SUMMARY 导航修复
- 工具与质量：根 pyproject、pre-commit；CI 增 fastapi_min 工作流
- FastAPI 示例：API Key/JWT、分页、任务与调度、指标、Docker/Compose、端到端测试、GHCR 推送、安全加固（CORS/体积限制/审计）

## 路线图（下一阶段）

- 监控：Grafana 看板与 Alertmanager 告警
- 安全：限流中间件、结构化日志与脱敏
- 性能：压测矩阵与自动报告
- 质量：覆盖率与 pre-commit 扩展

## 入口与操作

- 示例运行：`python/05-Web开发/examples/fastapi_min/README.md`
- 部署与压测：`python/05-Web开发/部署与压测指引.md`
- 规范约定：`python/05-Web开发/API_接口规范.md`
- 发布说明：`RELEASE_NOTES.md`，路线图：`ROADMAP_NEXT.md`
