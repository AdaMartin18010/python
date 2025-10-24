# Python 2025 知识库

> 面向2025年10月24日的Python最新最成熟版本的全面知识库，涵盖语言特性、生态系统、软件设计、架构设计和各行业领域的最佳实践。

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## 🎯 项目概述

本知识库是一个**生产就绪**的Python开发参考资源，包含：

- ✅ **10个核心章节** - 涵盖语言、测试、工程、并发、Web、数据科学、监控、安全、性能、AI集成
- ✅ **4个完整示例** - 监控应用、安全API、压测工具、AI聊天机器人
- ✅ **24个配置文件** - Docker、Kubernetes、监控栈（Prometheus、Grafana、Loki、Tempo）
- ✅ **生产级配置** - CI/CD、Pre-commit hooks、安全扫描、自动化测试
- ✅ **15,000+行代码** - 所有代码均可直接运行

---

## 🚀 快速开始

### 前置要求

- Python 3.12+ （推荐 3.13 以体验 Free-Threaded 模式）
- [uv](https://github.com/astral-sh/uv) （可选，推荐用于依赖管理）
- Docker & Docker Compose （用于运行示例）
- kubectl （可选，用于 Kubernetes 部署）

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/python-2025-kb.git
cd python-2025-kb

# 2. 安装依赖
make install

# 3. 安装开发依赖
make dev

# 4. 安装 pre-commit hooks
make install-hooks
```

### 运行示例

#### 方式1：使用 Makefile（推荐）

```bash
# 启动完整监控栈
make docker-up

# 运行监控示例
make run-monitoring

# 运行安全API示例
make run-security

# 运行压测
make run-loadtest

# 运行AI聊天机器人
make run-ai
```

#### 方式2：使用自动化脚本

```bash
# 一键安装开发环境
chmod +x scripts/setup_dev_env.sh
./scripts/setup_dev_env.sh

# 交互式运行示例
chmod +x scripts/run_examples.sh
./scripts/run_examples.sh
```

#### 方式3：手动运行

```bash
# 启动监控栈
cd python/07-监控与可观测性/examples
docker-compose -f docker-compose.monitoring.yml up -d

# 访问服务
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
# Alertmanager: http://localhost:9093
```

---

## 📚 目录结构

```
python-2025-kb/
│
├── python/                          # 核心章节
│   ├── 01-语言与生态/                # Python 3.12/3.13特性、现代工具链
│   ├── 02-测试与质量/                # pytest、覆盖率、测试策略
│   ├── 03-工程与交付/                # 打包、分发、CI/CD、Docker
│   ├── 04-并发与异步/                # Free-Threaded、asyncio、并发模式
│   ├── 05-Web开发/                  # FastAPI、Django、Litestar
│   ├── 06-数据科学/                  # Polars、Pandas 3.0、PyTorch
│   ├── 07-监控与可观测性/            # Prometheus、Grafana、OpenTelemetry
│   ├── 08-安全与合规/                # OWASP 2025、OAuth 2.1、SBOM
│   ├── 09-性能优化与压测/            # JIT、Locust、性能分析
│   └── 10-AI集成开发/                # LangChain 3.0、RAG、向量数据库
│
├── scripts/                         # 自动化脚本
│   ├── setup_dev_env.sh            # 开发环境安装
│   └── run_examples.sh             # 示例运行器
│
├── .github/workflows/              # CI/CD配置
│   └── python-ci.yml               # GitHub Actions
│
├── docker-compose.dev.yml          # 开发环境（PostgreSQL、Redis等）
├── .pre-commit-config.yaml         # Pre-commit hooks
├── Makefile                        # 便捷命令
├── pyproject.toml                  # 项目配置
│
├── INDEX_COMPREHENSIVE_2025.md     # 完整索引
├── QUICK_REFERENCE.md              # 快速参考
└── README.md                       # 本文件
```

---

## 🔥 核心特性

### 1. 完整的LGTM监控栈

```bash
# 一键启动企业级监控系统
make docker-up

# 包含：
✓ Loki (日志聚合)
✓ Grafana (可视化)
✓ Tempo (分布式追踪)
✓ Prometheus (指标采集)
✓ Alertmanager (告警管理)
✓ Pyroscope (性能分析)
```

### 2. 生产级Kubernetes配置

```yaml
✓ 高可用部署 (3-10副本)
✓ 自动扩缩容 (HPA)
✓ 滚动更新策略
✓ 健康检查 (Liveness/Readiness/Startup)
✓ 安全上下文 (非root、只读FS)
✓ Pod反亲和性
✓ PodDisruptionBudget
✓ Ingress (HTTPS + 速率限制)
```

### 3. 完整的CI/CD流水线

```yaml
✓ 代码质量检查 (Ruff + Mypy)
✓ 多平台测试 (Ubuntu, macOS, Windows)
✓ 安全扫描 (Bandit + pip-audit)
✓ SBOM生成 (CycloneDX)
✓ Docker构建和推送
✓ 容器安全扫描 (Trivy)
```

### 4. Pre-commit自动检查

```bash
# 安装hooks
make install-hooks

# 自动运行：
✓ Ruff (代码检查+格式化)
✓ Mypy (类型检查)
✓ Bandit (安全扫描)
✓ detect-secrets (密钥检测)
✓ Markdown检查
✓ YAML格式化
```

---

## 🎓 学习路径

### 初学者路径

1. **语言基础** - `python/01-语言与生态/README.md`
2. **测试入门** - `python/02-测试与质量/README.md`
3. **Web开发** - `python/05-Web开发/README.md`
4. **运行示例** - `make run-monitoring`

### 进阶路径

1. **并发编程** - `python/04-并发与异步/README.md`
2. **数据科学** - `python/06-数据科学/README.md`
3. **监控体系** - `python/07-监控与可观测性/README.md`
4. **性能优化** - `python/09-性能优化与压测/README.md`

### 专家路径

1. **架构设计** - `python/01-语言与生态/README.md#软件架构设计`
2. **安全合规** - `python/08-安全与合规/README.md`
3. **AI集成** - `python/10-AI集成开发/README.md`
4. **工程交付** - `python/03-工程与交付/README.md`

---

## 💡 Makefile命令

```bash
# Setup
make install          # 安装依赖
make dev              # 安装开发依赖
make install-hooks    # 安装pre-commit hooks

# Development
make format           # 格式化代码
make lint             # 代码检查
make test             # 运行测试
make test-cov         # 测试+覆盖率

# Docker
make docker-build     # 构建镜像
make docker-up        # 启动监控栈
make docker-down      # 停止监控栈
make docker-logs      # 查看日志

# Kubernetes
make k8s-deploy       # 部署到K8s
make k8s-status       # 查看状态
make k8s-clean        # 清理资源

# Examples
make run-monitoring   # 运行监控示例
make run-security     # 运行安全示例
make run-loadtest     # 运行压测
make run-ai           # 运行AI示例

# Utilities
make clean            # 清理缓存
make update           # 更新依赖
```

---

## 📊 统计数据

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
类型                  数量          行数
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
核心章节              10个          4,200+行
示例应用              4个           1,700+行
配置文件              24个          2,700+行
测试文件              1个           400+行
自动化脚本            2个           400+行
CI/CD配置             1个           250+行
K8s配置              1个           300+行
Pre-commit           1个           130+行
文档                  15+个         5,000+行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总计                  59+个文件      15,100+行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🛠️ 技术栈

### 核心技术

- **Python**: 3.12, 3.13 (Free-Threaded, JIT)
- **包管理**: uv (10-100x faster), pip, poetry
- **代码质量**: ruff, mypy, bandit
- **测试**: pytest, pytest-cov, hypothesis

### Web开发

- **框架**: FastAPI 0.115+, Django 5.1+, Litestar 2.0+
- **ASGI**: uvicorn, hypercorn
- **数据验证**: Pydantic 2.9+
- **ORM**: SQLAlchemy 2.0+, Tortoise ORM

### 数据科学

- **数据处理**: Polars 1.9+, Pandas 3.0+
- **ML**: PyTorch 2.5+, scikit-learn 1.5+
- **可视化**: Matplotlib 4.0, Seaborn 1.2

### 监控体系

- **LGTM栈**: Loki, Grafana, Tempo, Mimir
- **指标**: Prometheus 2.54+
- **追踪**: OpenTelemetry 1.27+
- **日志**: Structlog 24.4+

### AI/ML

- **框架**: LangChain 3.0+
- **向量DB**: Qdrant, Pinecone
- **LLM**: OpenAI, Anthropic

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📖 文档

- [完整索引](INDEX_COMPREHENSIVE_2025.md) - 所有章节导航
- [快速参考](QUICK_REFERENCE.md) - 常用命令和代码片段
- [更新日志](FINAL_UPDATE_2025_10_24_ROUND8.md) - 最新更新

---

## 📜 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

感谢所有贡献者和以下开源项目：

- [Python](https://www.python.org/)
- [Astral (uv, ruff)](https://astral.sh/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)

---

## 📧 联系方式

- **项目主页**: https://github.com/your-org/python-2025-kb
- **问题反馈**: https://github.com/your-org/python-2025-kb/issues
- **讨论**: https://github.com/your-org/python-2025-kb/discussions

---

**Python 2025 知识库** - 由 Python Knowledge Base Team 用 ❤️ 打造

**更新日期**: 2025年10月24日  
**版本**: 1.0.0  
**状态**: ✅ 生产就绪

