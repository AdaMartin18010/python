# 01-语言与生态（2025）

聚焦语言新特性、生态与工具链的系统化实践。

## 1. 语言与版本

- 收敛到 2025 主流稳定版本
- 新特性综述与可迁移性评估
  - 本地副本：[迁移/01-语言新特性](./迁移/01-语言新特性.md)

> 版本基线：Python 3.12 为默认，关注 3.13 新特性（如更快的解释器、JIT 研究进展、性能与诊断改进）。确保示例与 CI 默认以 3.12 通过，兼容 3.11/3.13。

## 2. 工具链（uv/pip/venv）

- 安装、迁移策略与镜像源
- 项目级/工作区级依赖管理
  - 本地副本：
    - [迁移/06-uv工具综述](./迁移/06-uv工具综述.md)
    - [迁移/07-uv技术深度分析](./迁移/07-uv技术深度分析.md)
    - [迁移/08-uv生态系统解析](./迁移/08-uv生态系统解析.md)
    - [迁移/09-uv完成度总结](./迁移/09-uv完成度总结.md)
    - [迁移/10-uv技术深潜](./迁移/10-uv技术深潜.md)

### 2.1 快速开始（Windows / PowerShell）

```powershell
# 安装 uv（优先使用 pipx）
pipx install uv || pip install uv

# 创建与同步依赖（基于 pyproject.toml）
uv pip compile pyproject.toml -o uv.lock
uv pip sync uv.lock

# 创建并激活虚拟环境（如需）
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

### 2.2 常见任务对照

- 创建项目骨架：使用 `pyproject.toml` + `uv` 生成与同步；发布前锁定 `uv.lock`。
- 多工作区：在仓库根维护统一锁文件；子项目继承基础工具链（ruff/mypy/pytest）。
- 国内镜像：`uv pip --index-url <mirror> sync uv.lock`，或在 `pip.conf`/`uv config` 中设置。

## 3. 测试与质量

- pytest、类型、lint 体系
- 最小可运行样例与项目模板
  - 本地副本：
    - [../02-测试与质量/迁移/质量检查.md](../02-测试与质量/迁移/质量检查.md)
  - 推荐工具集：pytest + ruff + mypy（或 pyright）+ pre-commit

## 4. 性能与安全

- 性能剖析与优化策略
- 供应链与运行安全
  - 本地副本：
    - [迁移/05-性能优化指南](./迁移/05-性能优化指南.md)
    - [迁移/04-安全开发指南](./迁移/04-安全开发指南.md)

## 5. 工程与交付

- 打包/发布/部署流水线
- 多环境配置与运维接口

## 6. 生态综述

- 库与框架成熟度
  - 本地副本：[迁移/02-技术栈2025](./迁移/02-技术栈2025.md)

## 7. 最佳实践

- 团队与工程实践
  - 本地副本：[迁移/03-最佳实践2025](./迁移/03-最佳实践2025.md)

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 相关规范：[重构规范](../99-上下文与流程/03-重构规范.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)

## 来源与回链（docs → python）

- 新特性来源：`docs/model/Programming_Language/python_new_features.md` → 本地：[迁移/01-语言新特性](./迁移/01-语言新特性.md)
- 性能来源：`docs/model/Programming_Language/python_performance_optimization.md` → 本地：[迁移/05-性能优化指南](./迁移/05-性能优化指南.md)
