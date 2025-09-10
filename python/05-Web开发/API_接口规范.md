# API 接口规范（团队约定）

## 1. 错误响应

- 统一格式：`{"detail": "..."}`
- 校验错误：HTTP 422，`detail` 为简明错误信息
- 业务错误：按语义返回 4xx/5xx，并保持统一结构

## 2. 认证与授权

- API Key（示例）：请求头 `X-API-Key`
  - 本地演示可复用应用名/环境变量；生产请使用安全密钥与轮换策略
- Bearer/JWT：
  - 获取：`POST /token` 返回 `{"access_token":"...","token_type":"bearer"}`
  - 使用：`Authorization: Bearer <access_token>` 访问受保护接口（如 `/me`）
  - 建议：`exp` 过期、`sub` 标识、密钥与算法约束（HS256/RS256），禁止在 JWT 放敏感信息

## 3. 版本化

- 路径：`/v1/...`，或
- Header：`X-API-Version: 1`
- 响应可加元数据：`{"_version": 1, "data": ...}`

## 4. 分页与排序

- 请求参数：
  - `limit`（1-100）、`offset`（>=0）
  - `sort=field`，`order=asc|desc`
- 响应结构：`Page{ total: int, items: [] }`

## 5. OpenAPI 与分组

- 在 OpenAPI 中通过 tags 组织接口：core/items/users/security/tasks/jobs
- 使用示例响应与安全方案声明（API Key / Bearer）

## 6. 参考实现

- 示例：`05-Web开发/examples/fastapi_min`
  - 统一错误：`ErrorResp`
  - 分页：`Page{ total, items }`
  - 安全：`X-API-Key`，`/protected`；Bearer：`/token`、`/me`
  - 调度：APScheduler，`/jobs`

---

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 上级主题：[05-Web开发/README](./README.md)
