# Makefile for Python 2025 Knowledge Base
# 提供便捷的命令来管理项目

.PHONY: help install dev test lint format clean docker-up docker-down k8s-deploy k8s-clean

# 默认目标
.DEFAULT_GOAL := help

# 颜色定义
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

## help: 显示帮助信息
help:
	@echo "$(BLUE)Python 2025 Knowledge Base - Makefile Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup Commands:$(NC)"
	@echo "  make install          - 安装所有依赖"
	@echo "  make dev              - 安装开发依赖"
	@echo "  make install-hooks    - 安装pre-commit hooks"
	@echo ""
	@echo "$(GREEN)Development Commands:$(NC)"
	@echo "  make format           - 格式化代码 (ruff format)"
	@echo "  make lint             - 检查代码质量 (ruff + mypy)"
	@echo "  make test             - 运行测试"
	@echo "  make test-cov         - 运行测试并生成覆盖率报告"
	@echo "  make security         - 运行安全扫描"
	@echo ""
	@echo "$(GREEN)Docker Commands:$(NC)"
	@echo "  make docker-build     - 构建Docker镜像"
	@echo "  make docker-up        - 启动监控栈"
	@echo "  make docker-down      - 停止监控栈"
	@echo "  make docker-logs      - 查看日志"
	@echo "  make docker-clean     - 清理Docker资源"
	@echo ""
	@echo "$(GREEN)Kubernetes Commands:$(NC)"
	@echo "  make k8s-deploy       - 部署到Kubernetes"
	@echo "  make k8s-status       - 查看部署状态"
	@echo "  make k8s-logs         - 查看Pod日志"
	@echo "  make k8s-clean        - 清理Kubernetes资源"
	@echo ""
	@echo "$(GREEN)Example Commands:$(NC)"
	@echo "  make run-monitoring   - 运行监控示例"
	@echo "  make run-security     - 运行安全示例"
	@echo "  make run-loadtest     - 运行压测示例"
	@echo "  make run-ai           - 运行AI示例"
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@echo "  make clean            - 清理缓存和临时文件"
	@echo "  make update           - 更新依赖"
	@echo "  make docs             - 生成文档"
	@echo "  make health-check     - 运行健康检查"
	@echo "  make benchmark        - 运行性能基准测试"
	@echo "  make init-project     - 初始化新项目"
	@echo ""

## install: 安装所有依赖
install:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install -r python/07-监控与可观测性/examples/requirements.txt; \
	else \
		pip install -r python/07-监控与可观测性/examples/requirements.txt; \
	fi
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

## dev: 安装开发依赖
dev:
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install ruff mypy pytest pytest-cov pytest-asyncio bandit pre-commit; \
	else \
		pip install ruff mypy pytest pytest-cov pytest-asyncio bandit pre-commit; \
	fi
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

## install-hooks: 安装pre-commit hooks
install-hooks:
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	@pre-commit install
	@echo "$(GREEN)✓ Pre-commit hooks installed$(NC)"

## format: 格式化代码
format:
	@echo "$(BLUE)Formatting code...$(NC)"
	@ruff format .
	@echo "$(GREEN)✓ Code formatted$(NC)"

## lint: 检查代码质量
lint:
	@echo "$(BLUE)Linting code...$(NC)"
	@ruff check . || true
	@echo ""
	@echo "$(BLUE)Type checking...$(NC)"
	@mypy python/ --ignore-missing-imports || true
	@echo "$(GREEN)✓ Linting complete$(NC)"

## test: 运行测试
test:
	@echo "$(BLUE)Running tests...$(NC)"
	@pytest python/08-安全与合规/examples/tests/ -v
	@echo "$(GREEN)✓ Tests complete$(NC)"

## test-cov: 运行测试并生成覆盖率报告
test-cov:
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	@pytest python/08-安全与合规/examples/tests/ --cov --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated$(NC)"
	@echo "$(YELLOW)Open htmlcov/index.html to view the report$(NC)"

## security: 运行安全扫描
security:
	@echo "$(BLUE)Running security scans...$(NC)"
	@echo "$(YELLOW)Bandit (code security)...$(NC)"
	@bandit -r python/ -f json -o bandit-report.json || true
	@echo "$(YELLOW)pip-audit (dependency vulnerabilities)...$(NC)"
	@pip-audit --format json --output pip-audit-report.json || true
	@echo "$(GREEN)✓ Security scans complete$(NC)"

## docker-build: 构建Docker镜像
docker-build:
	@echo "$(BLUE)Building Docker image...$(NC)"
	@cd python/07-监控与可观测性/examples && \
		docker build -t python-monitoring-app:latest .
	@echo "$(GREEN)✓ Docker image built$(NC)"

## docker-up: 启动监控栈
docker-up:
	@echo "$(BLUE)Starting monitoring stack...$(NC)"
	@cd python/07-监控与可观测性/examples && \
		docker-compose -f docker-compose.monitoring.yml up -d
	@echo "$(GREEN)✓ Monitoring stack started$(NC)"
	@echo ""
	@echo "$(YELLOW)Access URLs:$(NC)"
	@echo "  Grafana:     http://localhost:3000 (admin/admin)"
	@echo "  Prometheus:  http://localhost:9090"
	@echo "  Alertmanager: http://localhost:9093"
	@echo "  Application: http://localhost:8000"

## docker-down: 停止监控栈
docker-down:
	@echo "$(BLUE)Stopping monitoring stack...$(NC)"
	@cd python/07-监控与可观测性/examples && \
		docker-compose -f docker-compose.monitoring.yml down
	@echo "$(GREEN)✓ Monitoring stack stopped$(NC)"

## docker-logs: 查看日志
docker-logs:
	@cd python/07-监控与可观测性/examples && \
		docker-compose -f docker-compose.monitoring.yml logs -f

## docker-clean: 清理Docker资源
docker-clean:
	@echo "$(BLUE)Cleaning Docker resources...$(NC)"
	@cd python/07-监控与可观测性/examples && \
		docker-compose -f docker-compose.monitoring.yml down -v
	@docker system prune -f
	@echo "$(GREEN)✓ Docker resources cleaned$(NC)"

## k8s-deploy: 部署到Kubernetes
k8s-deploy:
	@echo "$(BLUE)Deploying to Kubernetes...$(NC)"
	@kubectl apply -f python/07-监控与可观测性/examples/k8s/deployment.yaml
	@echo "$(GREEN)✓ Deployed to Kubernetes$(NC)"

## k8s-status: 查看部署状态
k8s-status:
	@echo "$(BLUE)Kubernetes Status:$(NC)"
	@kubectl get all -n python-app
	@echo ""
	@echo "$(BLUE)HPA Status:$(NC)"
	@kubectl get hpa -n python-app

## k8s-logs: 查看Pod日志
k8s-logs:
	@kubectl logs -f deployment/python-app -n python-app

## k8s-clean: 清理Kubernetes资源
k8s-clean:
	@echo "$(BLUE)Cleaning Kubernetes resources...$(NC)"
	@kubectl delete namespace python-app
	@echo "$(GREEN)✓ Kubernetes resources cleaned$(NC)"

## run-monitoring: 运行监控示例
run-monitoring:
	@echo "$(BLUE)Starting monitoring example...$(NC)"
	@cd python/07-监控与可观测性/examples && \
		uvicorn complete_monitoring_app:app --reload

## run-security: 运行安全示例
run-security:
	@echo "$(BLUE)Starting security example...$(NC)"
	@cd python/08-安全与合规/examples && \
		uvicorn secure_api_example:app --reload

## run-loadtest: 运行压测示例
run-loadtest:
	@echo "$(BLUE)Starting load test...$(NC)"
	@cd python/09-性能优化与压测/examples && \
		locust -f locustfile.py --host=http://localhost:8000

## run-ai: 运行AI示例
run-ai:
	@echo "$(BLUE)Starting AI chatbot...$(NC)"
	@cd python/10-AI集成开发/examples && \
		uvicorn rag_chatbot:app --reload

## clean: 清理缓存和临时文件
clean:
	@echo "$(BLUE)Cleaning cache and temporary files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned$(NC)"

## update: 更新依赖
update:
	@echo "$(BLUE)Updating dependencies...$(NC)"
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install --upgrade -r python/07-监控与可观测性/examples/requirements.txt; \
	else \
		pip install --upgrade -r python/07-监控与可观测性/examples/requirements.txt; \
	fi
	@pre-commit autoupdate
	@echo "$(GREEN)✓ Dependencies updated$(NC)"

## docs: 生成文档
docs:
	@echo "$(BLUE)Generating documentation...$(NC)"
	@echo "Documentation files:"
	@echo "  - INDEX_COMPREHENSIVE_2025.md"
	@echo "  - QUICK_REFERENCE.md"
	@echo "  - FINAL_UPDATE_2025_10_24_ROUND8.md"
	@echo "$(GREEN)✓ Documentation available$(NC)"

# 检查工具是否安装
check-tool-%:
	@which $* > /dev/null || (echo "$(RED)Error: $* not installed$(NC)" && exit 1)

## health-check: 运行健康检查
health-check:
	@echo "$(BLUE)Running health check...$(NC)"
	@python scripts/health_check.py
	@echo "$(GREEN)✓ Health check complete$(NC)"

## benchmark: 运行性能基准测试
benchmark:
	@echo "$(BLUE)Running performance benchmarks...$(NC)"
	@python scripts/benchmark.py
	@echo "$(GREEN)✓ Benchmarks complete$(NC)"

## init-project: 初始化新项目
init-project:
	@echo "$(BLUE)Initialize new project$(NC)"
	@echo "$(YELLOW)Usage: python scripts/init_project.py <project-name>$(NC)"
	@echo "$(YELLOW)Example: python scripts/init_project.py my-awesome-project$(NC)"

