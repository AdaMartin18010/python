# CI/CD持续工作流与AI/ML工程实践全面指南

> 本文档系统性地梳理CI/CD持续集成/持续部署工作流以及AI/ML工程化实践，包含概念定义、最佳实践、完整代码示例、正例反例对比和工具选型指南。

---

## 目录

- [CI/CD持续工作流与AI/ML工程实践全面指南](#cicd持续工作流与aiml工程实践全面指南)
  - [目录](#目录)
  - [第一部分：CI/CD基础](#第一部分cicd基础)
    - [1. 持续集成（CI）](#1-持续集成ci)
      - [1.1 概念定义](#11-概念定义)
      - [1.2 核心实践](#12-核心实践)
      - [1.3 CI流程完整示例](#13-ci流程完整示例)
      - [1.4 正例 vs 反例](#14-正例-vs-反例)
    - [2. 持续交付/部署（CD）](#2-持续交付部署cd)
      - [2.1 概念定义](#21-概念定义)
      - [2.2 部署策略对比](#22-部署策略对比)
      - [2.3 蓝绿部署实现](#23-蓝绿部署实现)
      - [2.4 金丝雀发布实现](#24-金丝雀发布实现)
  - [第二部分：CI/CD工具](#第二部分cicd工具)
    - [1. GitHub Actions](#1-github-actions)
      - [1.1 Workflow语法详解](#11-workflow语法详解)
      - [1.2 Actions市场推荐](#12-actions市场推荐)
      - [1.3 自定义Action](#13-自定义action)
    - [2. GitLab CI](#2-gitlab-ci)
      - [2.1 .gitlab-ci.yml语法](#21-gitlab-ciyml语法)
      - [2.2 Runner配置](#22-runner配置)
    - [3. Jenkins](#3-jenkins)
      - [3.1 Pipeline语法](#31-pipeline语法)
      - [3.2 插件生态推荐](#32-插件生态推荐)
    - [4. ArgoCD](#4-argocd)
      - [4.1 GitOps概念](#41-gitops概念)
      - [4.2 ArgoCD配置示例](#42-argocd配置示例)
      - [4.3 ArgoCD CLI使用](#43-argocd-cli使用)
      - [4.4 工具对比](#44-工具对比)
  - [第三部分：CI/CD最佳实践](#第三部分cicd最佳实践)
    - [1. 自动化测试](#1-自动化测试)
      - [1.1 测试金字塔](#11-测试金字塔)
      - [1.2 单元测试最佳实践](#12-单元测试最佳实践)
      - [1.3 集成测试](#13-集成测试)
      - [1.4 端到端测试](#14-端到端测试)
      - [1.5 测试配置（pytest.ini）](#15-测试配置pytestini)
    - [2. 代码质量](#2-代码质量)
      - [2.1 静态分析工具配置](#21-静态分析工具配置)
      - [2.2 代码覆盖率配置](#22-代码覆盖率配置)
      - [2.3 预提交钩子配置](#23-预提交钩子配置)
      - [2.4 正例 vs 反例](#24-正例-vs-反例)
    - [3. 制品管理](#3-制品管理)
      - [3.1 Docker镜像构建](#31-docker镜像构建)
      - [3.2 版本管理策略](#32-版本管理策略)
    - [4. 部署策略详解](#4-部署策略详解)
      - [4.1 特性开关（Feature Flags）](#41-特性开关feature-flags)
      - [4.2 完整部署流水线](#42-完整部署流水线)
  - [第四部分：Python ML生态](#第四部分python-ml生态)
    - [1. 核心库](#1-核心库)
      - [1.1 NumPy基础](#11-numpy基础)
      - [1.2 Pandas数据处理](#12-pandas数据处理)
      - [1.3 Scikit-Learn机器学习](#13-scikit-learn机器学习)
      - [1.4 TensorFlow/PyTorch概述](#14-tensorflowpytorch概述)
    - [2. 模型训练流程](#2-模型训练流程)
  - [第五部分：MLOps](#第五部分mlops)
    - [1. 实验跟踪](#1-实验跟踪)
      - [1.1 MLflow实验跟踪](#11-mlflow实验跟踪)
      - [1.2 Weights \& Biases (W\&B)](#12-weights--biases-wb)
      - [1.3 TensorBoard](#13-tensorboard)
      - [1.4 实验跟踪工具对比](#14-实验跟踪工具对比)
    - [2. 模型版本管理](#2-模型版本管理)
      - [2.1 MLflow Model Registry](#21-mlflow-model-registry)
      - [2.2 DVC (Data Version Control)](#22-dvc-data-version-control)
    - [3. 模型服务](#3-模型服务)
      - [3.1 REST API (FastAPI + 模型)](#31-rest-api-fastapi--模型)
      - [3.2 批处理预测](#32-批处理预测)
      - [3.3 模型缓存](#33-模型缓存)
    - [4. 模型监控](#4-模型监控)
      - [4.1 性能监控](#41-性能监控)
      - [4.2 数据漂移检测](#42-数据漂移检测)
  - [第六部分：AI工程化](#第六部分ai工程化)
    - [1. LLM应用开发](#1-llm应用开发)
      - [1.1 OpenAI API](#11-openai-api)
      - [1.2 LangChain概述](#12-langchain概述)
      - [1.3 Prompt工程](#13-prompt工程)
    - [2. RAG（检索增强生成）](#2-rag检索增强生成)
      - [2.1 概念定义](#21-概念定义-1)
      - [2.2 Python实现](#22-python实现)
    - [3. AI Agent](#3-ai-agent)
      - [3.1 概念定义](#31-概念定义)
      - [3.2 实现模式](#32-实现模式)
  - [总结](#总结)
    - [CI/CD核心要点](#cicd核心要点)
    - [MLOps核心要点](#mlops核心要点)
    - [AI工程化核心要点](#ai工程化核心要点)

---

## 第一部分：CI/CD基础

### 1. 持续集成（CI）

#### 1.1 概念定义

**持续集成（Continuous Integration, CI）** 是一种软件开发实践，团队成员频繁地将代码变更合并到主干分支，每次合并都通过自动化构建和测试来验证，从而尽早发现问题。

```
┌─────────────────────────────────────────────────────────────┐
│                     持续集成流程图                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  开发者A ──► 代码提交 ──┐                                    │
│                        │                                    │
│  开发者B ──► 代码提交 ──┼──► 自动构建 ──► 自动测试 ──► 反馈   │
│                        │                                    │
│  开发者C ──► 代码提交 ──┘                                    │
│                                                             │
│  核心原则：频繁集成、自动化验证、快速反馈                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 1.2 核心实践

| 实践项 | 说明 | 频率要求 |
|--------|------|----------|
| **频繁提交** | 小批量、频繁地将代码提交到版本控制 | 每天至少1次 |
| **自动化构建** | 每次提交自动编译/打包代码 | 每次提交触发 |
| **自动化测试** | 运行单元测试、集成测试 | 每次构建触发 |
| **快速反馈** | 构建和测试在10分钟内完成 | < 10分钟 |
| **主干开发** | 直接在主干分支开发，避免长期分支 | 持续进行 |

#### 1.3 CI流程完整示例

```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
      # 1. 检出代码
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. 设置Python环境
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      # 3. 缓存依赖
      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

      # 4. 安装依赖
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      # 5. 代码质量检查
      - name: Lint with flake8
        run: |
          flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      # 6. 类型检查
      - name: Type check with mypy
        run: mypy src

      # 7. 运行单元测试
      - name: Run unit tests
        run: pytest tests/unit -v --cov=src --cov-report=xml

      # 8. 运行集成测试
      - name: Run integration tests
        run: pytest tests/integration -v

      # 9. 上传覆盖率报告
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

#### 1.4 正例 vs 反例

**✅ 正例：良好的CI实践**

```python
# 小而频繁的提交，每个提交都有明确目的
# commit 1: 添加用户认证功能
def authenticate_user(username: str, password: str) -> bool:
    """验证用户凭据."""
    user = get_user_by_username(username)
    if user and verify_password(password, user.password_hash):
        return True
    return False

# commit 2: 添加单元测试
class TestUserAuthentication(unittest.TestCase):
    def test_valid_credentials(self):
        self.assertTrue(authenticate_user("admin", "correct_password"))

    def test_invalid_credentials(self):
        self.assertFalse(authenticate_user("admin", "wrong_password"))
```

**❌ 反例：不良的CI实践**

```python
# 大而杂的提交，包含多个不相关的变更
# commit: "更新代码" (包含：新功能+bug修复+重构+配置变更)
def do_something():
    # 1000+ 行代码，混合了多个功能
    pass

# 没有自动化测试，手动验证
# 长期分支，很少合并到主干
```

---

### 2. 持续交付/部署（CD）

#### 2.1 概念定义

**持续交付（Continuous Delivery）** 是CI的延伸，确保代码变更可以自动部署到生产环境，但需要人工审批。

**持续部署（Continuous Deployment）** 更进一步，代码变更通过所有测试后自动部署到生产环境，无需人工干预。

```
┌─────────────────────────────────────────────────────────────────────┐
│                    持续交付/部署流程图                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  代码提交 ──► 构建 ──► 测试 ──►  staging部署 ──► 生产部署           │
│               │        │           │              │                 │
│               ▼        ▼           ▼              ▼                 │
│            制品库   测试报告    集成测试      持续交付(人工审批)      │
│                                                  │                  │
│                                                  ▼                  │
│                                           持续部署(全自动)           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 2.2 部署策略对比

| 策略 | 描述 | 风险 | 适用场景 |
|------|------|------|----------|
| **滚动部署** | 逐个替换实例 | 中 | 大多数Web应用 |
| **蓝绿部署** | 两套环境切换 | 低 | 需要零停机 |
| **金丝雀发布** | 小流量验证 | 低 | 高风险变更 |
| **A/B测试** | 流量分组对比 | 中 | 功能验证 |
| **特性开关** | 代码级控制 | 低 | 频繁发布 |

#### 2.3 蓝绿部署实现

```yaml
# kubernetes blue-green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  labels:
    app: myapp
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0.0
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: blue  # 切换到 green 进行流量切换
  ports:
  - port: 80
    targetPort: 8080
```

```python
# 蓝绿部署切换脚本
import subprocess
import sys

def switch_traffic(target_version: str):
    """切换流量到指定版本."""
    # 更新Service selector
    cmd = [
        "kubectl", "patch", "service", "myapp-service",
        "-p", f'{{"spec":{{"selector":{{"version":"{target_version}"}}}}}}'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ 流量已切换到 {target_version}")
        return True
    else:
        print(f"❌ 切换失败: {result.stderr}")
        return False

def rollback():
    """快速回滚到上一个版本."""
    current = get_current_version()
    previous = "green" if current == "blue" else "blue"
    return switch_traffic(previous)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <blue|green|rollback>")
        sys.exit(1)

    action = sys.argv[1]
    if action == "rollback":
        rollback()
    else:
        switch_traffic(action)
```

#### 2.4 金丝雀发布实现

```yaml
# kubernetes canary deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      track: stable
  template:
    metadata:
      labels:
        app: myapp
        track: stable
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0.0
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1  # 10% 流量
  selector:
    matchLabels:
      app: myapp
      track: canary
  template:
    metadata:
      labels:
        app: myapp
        track: canary
    spec:
      containers:
      - name: myapp
        image: myapp:v1.1.0  # 新版本
---
# Istio 流量分割
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp.example.com
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: myapp
        subset: canary
      weight: 100
  - route:
    - destination:
        host: myapp
        subset: stable
      weight: 90
    - destination:
        host: myapp
        subset: canary
      weight: 10
```

---

## 第二部分：CI/CD工具

### 1. GitHub Actions

#### 1.1 Workflow语法详解

```yaml
# .github/workflows/main.yml
name: Complete CI/CD Pipeline

# 触发条件
on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'tests/**'
      - 'requirements*.txt'
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
  schedule:
    - cron: '0 2 * * 1'  # 每周一凌晨2点
  workflow_dispatch:  # 手动触发
    inputs:
      environment:
        description: '部署环境'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

# 环境变量
env:
  PYTHON_VERSION: '3.11'
  REGISTRY: ghcr.io

# 权限控制
permissions:
  contents: read
  packages: write
  id-token: write

jobs:
  # Job 1: 代码质量检查
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install black flake8 mypy
      - run: black --check src
      - run: flake8 src
      - run: mypy src

  # Job 2: 测试
  test:
    runs-on: ubuntu-latest
    needs: lint  # 依赖lint job
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.9', '3.10', '3.11']
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  # Job 3: 构建Docker镜像
  build:
    runs-on: ubuntu-latest
    needs: test
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ${{ env.REGISTRY }}/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Job 4: 部署到Staging
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: staging
      url: https://staging.example.com
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Deploy to staging
        run: |
          echo "Deploying ${{ needs.build.outputs.image_tag }} to staging"
          # kubectl set image deployment/myapp myapp=${{ needs.build.outputs.image_tag }}

  # Job 5: 部署到生产
  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: production
      url: https://example.com
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying ${{ needs.build.outputs.image_tag }} to production"
```

#### 1.2 Actions市场推荐

| Action | 用途 | 示例 |
|--------|------|------|
| `actions/checkout` | 检出代码 | `uses: actions/checkout@v4` |
| `actions/setup-python` | 设置Python | `uses: actions/setup-python@v5` |
| `actions/cache` | 缓存依赖 | `uses: actions/cache@v4` |
| `docker/build-push-action` | 构建Docker | `uses: docker/build-push-action@v5` |
| `codecov/codecov-action` | 覆盖率报告 | `uses: codecov/codecov-action@v3` |
| `actions/github-script` | GitHub API | `uses: actions/github-script@v7` |

#### 1.3 自定义Action

```yaml
# .github/actions/setup-python-env/action.yml
name: 'Setup Python Environment'
description: 'Setup Python with caching and dependency installation'
inputs:
  python-version:
    description: 'Python version'
    required: true
    default: '3.11'
  requirements-file:
    description: 'Requirements file path'
    required: true
    default: 'requirements.txt'

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}

    - uses: actions/cache@v4
      with:
        path: |
          ~/.cache/pip
          ~/.local/share/virtualenvs
        key: ${{ runner.os }}-python-${{ inputs.python-version }}-${{ hashFiles(inputs.requirements-file) }}

    - run: pip install -r ${{ inputs.requirements-file }}
      shell: bash
```

---

### 2. GitLab CI

#### 2.1 .gitlab-ci.yml语法

```yaml
# .gitlab-ci.yml
# 全局变量
variables:
  PYTHON_VERSION: "3.11"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  DOCKER_REGISTRY: "$CI_REGISTRY"
  IMAGE_NAME: "$CI_REGISTRY_IMAGE"

# 缓存配置
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/pip/
    - venv/

# 阶段定义
stages:
  - lint
  - test
  - build
  - deploy

# 模板定义
.test_template: &test_template
  image: python:${PYTHON_VERSION}
  before_script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install --upgrade pip
    - pip install -r requirements.txt
    - pip install -r requirements-dev.txt

# Job 1: 代码格式检查
black:
  <<: *test_template
  stage: lint
  script:
    - black --check src tests
  allow_failure: true

# Job 2: 代码风格检查
flake8:
  <<: *test_template
  stage: lint
  script:
    - flake8 src tests --max-line-length=100 --extend-ignore=E203

# Job 3: 类型检查
mypy:
  <<: *test_template
  stage: lint
  script:
    - mypy src --ignore-missing-imports

# Job 4: 安全扫描
bandit:
  <<: *test_template
  stage: lint
  script:
    - bandit -r src -f json -o bandit-report.json || true
  artifacts:
    paths:
      - bandit-report.json
    expire_in: 1 week

# Job 5: 单元测试
unit_tests:
  <<: *test_template
  stage: test
  script:
    - pytest tests/unit -v --cov=src --cov-report=xml --cov-report=html
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - htmlcov/
    expire_in: 1 week

# Job 6: 集成测试
integration_tests:
  <<: *test_template
  stage: test
  services:
    - postgres:15-alpine
    - redis:7-alpine
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_pass
    DATABASE_URL: "postgresql://test_user:test_pass@postgres/test_db"
  script:
    - pytest tests/integration -v
  only:
    - merge_requests
    - main
    - develop

# Job 7: 构建Docker镜像
build_image:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_NAME:$CI_COMMIT_SHA -t $IMAGE_NAME:latest .
    - docker push $IMAGE_NAME:$CI_COMMIT_SHA
    - docker push $IMAGE_NAME:latest
  only:
    - main
    - tags

# Job 8: 部署到Staging
deploy_staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context staging
    - kubectl set image deployment/myapp app=$IMAGE_NAME:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# Job 9: 部署到生产
deploy_production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production
    - kubectl set image deployment/myapp app=$IMAGE_NAME:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
  environment:
    name: production
    url: https://example.com
  when: manual  # 需要手动触发
  only:
    - main

# Job 10: 性能测试
performance_test:
  stage: test
  image: loadimpact/k6:latest
  script:
    - k6 run --out json=performance.json tests/performance/load_test.js
  artifacts:
    paths:
      - performance.json
    expire_in: 30 days
  only:
    - schedules
```

#### 2.2 Runner配置

```toml
# /etc/gitlab-runner/config.toml
concurrent = 4
check_interval = 0
shutdown_timeout = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "docker-runner-01"
  url = "https://gitlab.com/"
  id = 12345
  token = "YOUR_RUNNER_TOKEN"
  token_obtained_at = 2024-01-01T00:00:00Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    tls_verify = false
    image = "docker:24-dind"
    privileged = true
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
    shm_size = 0
    network_mtu = 0
```

---

### 3. Jenkins

#### 3.1 Pipeline语法

```groovy
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: python
                    image: python:3.11-slim
                    command: ['cat']
                    tty: true
                  - name: docker
                    image: docker:24-dind
                    securityContext:
                      privileged: true
                  - name: kubectl
                    image: bitnami/kubectl:latest
                    command: ['cat']
                    tty: true
            '''
        }
    }

    environment {
        PYTHON_VERSION = '3.11'
        REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'myapp'
        DOCKER_CREDENTIALS = credentials('docker-registry-credentials')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }

    triggers {
        pollSCM('H/5 * * * *')  // 每5分钟检查代码变更
        cron('H 2 * * 1')        // 每周一凌晨2点执行
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.BUILD_VERSION = "${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
                }
            }
        }

        stage('Setup') {
            steps {
                container('python') {
                    sh '''
                        python -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install -r requirements-dev.txt
                    '''
                }
            }
        }

        stage('Lint') {
            parallel {
                stage('Black') {
                    steps {
                        container('python') {
                            sh '''
                                . venv/bin/activate
                                black --check src tests
                            '''
                        }
                    }
                }
                stage('Flake8') {
                    steps {
                        container('python') {
                            sh '''
                                . venv/bin/activate
                                flake8 src tests
                            '''
                        }
                    }
                }
                stage('MyPy') {
                    steps {
                        container('python') {
                            sh '''
                                . venv/bin/activate
                                mypy src
                            '''
                        }
                    }
                }
            }
        }

        stage('Test') {
            steps {
                container('python') {
                    sh '''
                        . venv/bin/activate
                        pytest tests/ -v --cov=src --cov-report=xml --cov-report=html
                    '''
                }
            }
            post {
                always {
                    junit 'test-results.xml'
                    cobertura coberturaReportFile: 'coverage.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        stage('Security Scan') {
            steps {
                container('python') {
                    sh '''
                        . venv/bin/activate
                        bandit -r src -f json -o bandit-report.json || true
                        safety check -r requirements.txt || true
                    '''
                }
            }
        }

        stage('Build') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    tag pattern: 'v\\d+\\.\\d+\\.\\d+', comparator: 'REGEXP'
                }
            }
            steps {
                container('docker') {
                    sh '''
                        docker build -t ${REGISTRY}/${IMAGE_NAME}:${BUILD_VERSION} .
                        docker build -t ${REGISTRY}/${IMAGE_NAME}:latest .
                        echo ${DOCKER_CREDENTIALS_PSW} | docker login ${REGISTRY} -u ${DOCKER_CREDENTIALS_USR} --password-stdin
                        docker push ${REGISTRY}/${IMAGE_NAME}:${BUILD_VERSION}
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                container('kubectl') {
                    sh '''
                        kubectl config use-context staging
                        kubectl set image deployment/myapp app=${REGISTRY}/${IMAGE_NAME}:${BUILD_VERSION}
                        kubectl rollout status deployment/myapp
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                container('kubectl') {
                    sh '''
                        kubectl config use-context production
                        kubectl set image deployment/myapp app=${REGISTRY}/${IMAGE_NAME}:${BUILD_VERSION}
                        kubectl rollout status deployment/myapp
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            slackSend(color: 'good', message: "Build succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
        failure {
            slackSend(color: 'danger', message: "Build failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
    }
}
```

#### 3.2 插件生态推荐

| 插件 | 用途 | 安装命令 |
|------|------|----------|
| Blue Ocean | 现代化UI | 在插件管理器中安装 |
| Pipeline | 流水线支持 | 内置 |
| Docker Pipeline | Docker集成 | `docker-workflow` |
| Kubernetes | K8s集成 | `kubernetes` |
| Slack Notification | Slack通知 | `slack` |
| Cobertura | 覆盖率报告 | `cobertura` |
| SonarQube Scanner | 代码质量 | `sonarqube-scanner` |

---

### 4. ArgoCD

#### 4.1 GitOps概念

**GitOps** 是一种运维模式，将Git仓库作为基础设施和应用配置的单一事实来源，通过自动化工具（如ArgoCD）持续同步Git仓库状态到集群。

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitOps 工作流                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                │
│  │  Git仓库  │────►│ ArgoCD   │────►│ K8s集群  │                │
│  │ (配置)   │     │ (同步)   │     │ (运行)   │                │
│  └──────────┘     └──────────┘     └──────────┘                │
│        ▲                                         │              │
│        │                                         │              │
│        └─────────────────────────────────────────┘              │
│              (监控和自动同步)                                     │
│                                                                 │
│  核心原则：                                                     │
│  1. 声明式配置 - 所有配置以声明式YAML存储                         │
│  2. 版本控制 - 所有变更通过Git管理                               │
│  3. 自动同步 - 自动应用Git中的配置                               │
│  4. 持续协调 - 持续确保集群状态与Git一致                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.2 ArgoCD配置示例

```yaml
# Application 定义
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/example/myapp-gitops.git
    targetRevision: HEAD
    path: overlays/production
    helm:
      valueFiles:
        - values-production.yaml
    kustomize:
      namePrefix: prod-
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true        # 自动删除Git中不存在的资源
      selfHeal: true     # 自动修复偏离配置的资源
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
```

```yaml
# ApplicationSet (多环境管理)
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-set
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - cluster: staging
            url: https://staging-cluster.example.com
            namespace: staging
          - cluster: production
            url: https://production-cluster.example.com
            namespace: production
  template:
    metadata:
      name: '{{cluster}}-myapp'
    spec:
      project: default
      source:
        repoURL: https://github.com/example/myapp-gitops.git
        targetRevision: HEAD
        path: overlays/{{cluster}}
      destination:
        server: '{{url}}'
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

```yaml
# App of Apps 模式
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-of-apps
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/example/gitops-repo.git
    targetRevision: HEAD
    path: apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

#### 4.3 ArgoCD CLI使用

```bash
# 登录ArgoCD
argocd login argocd.example.com --username admin --password <password>

# 列出应用
argocd app list

# 创建应用
argocd app create myapp \
  --repo https://github.com/example/myapp.git \
  --path k8s/overlays/production \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production \
  --sync-policy automated \
  --auto-prune \
  --self-heal

# 手动同步
argocd app sync myapp

# 查看应用状态
argocd app get myapp

# 查看差异
argocd app diff myapp

# 回滚到指定版本
argocd app rollback myapp 3

# 删除应用
argocd app delete myapp
```

#### 4.4 工具对比

| 特性 | GitHub Actions | GitLab CI | Jenkins | ArgoCD |
|------|---------------|-----------|---------|--------|
| **类型** | CI/CD平台 | CI/CD平台 | CI/CD平台 | GitOps工具 |
| **托管** | SaaS/自托管 | SaaS/自托管 | 自托管 | 自托管 |
| **配置** | YAML | YAML | Groovy/YAML | YAML |
| **GitOps** | 需配合 | 需配合 | 需配合 | 原生支持 |
| **K8s集成** | 良好 | 良好 | 良好 | 深度集成 |
| **学习曲线** | 低 | 低 | 高 | 中 |
| **社区** | 大 | 大 | 大 | 增长中 |
| **最佳场景** | GitHub项目 | GitLab项目 | 复杂企业 | K8s GitOps |

---

## 第三部分：CI/CD最佳实践

### 1. 自动化测试

#### 1.1 测试金字塔

```
                    ╱╲
                   ╱  ╲
                  ╱ E2E╲          # 端到端测试 (少量)
                 ╱──────╲
                ╱Integration╲     # 集成测试 (中等)
               ╱────────────╲
              ╱   Unit Tests   ╲  # 单元测试 (大量)
             ╱──────────────────╲

            数量: 多 ──────────────────► 少
            速度: 快 ──────────────────► 慢
            成本: 低 ──────────────────► 高
```

#### 1.2 单元测试最佳实践

```python
# tests/unit/test_calculator.py
"""单元测试示例 - 计算器模块."""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from src.calculator import Calculator, DatabaseCalculator


class TestCalculator(unittest.TestCase):
    """计算器单元测试类."""

    def setUp(self):
        """每个测试前的设置."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        """测试正数相加."""
        # Arrange
        a, b = 2, 3
        expected = 5

        # Act
        result = self.calc.add(a, b)

        # Assert
        self.assertEqual(result, expected)

    def test_add_negative_numbers(self):
        """测试负数相加."""
        self.assertEqual(self.calc.add(-2, -3), -5)

    def test_add_mixed_numbers(self):
        """测试正负数相加."""
        self.assertEqual(self.calc.add(-2, 3), 1)

    def test_divide_by_zero_raises_exception(self):
        """测试除以零抛出异常."""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertIn("Cannot divide by zero", str(context.exception))

    def test_divide_normal(self):
        """测试正常除法."""
        self.assertEqual(self.calc.divide(10, 2), 5.0)

    @patch('src.calculator.logger')
    def test_add_logs_operation(self, mock_logger):
        """测试加法操作记录日志."""
        self.calc.add(1, 2)
        mock_logger.info.assert_called_once_with("Adding 1 + 2")


# pytest 风格
class TestCalculatorPytest:
    """使用pytest风格的测试."""

    @pytest.fixture
    def calculator(self):
        """创建计算器fixture."""
        return Calculator()

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (-2, -3, -5),
        (-2, 3, 1),
        (0, 0, 0),
        (1.5, 2.5, 4.0),
    ])
    def test_add_parametrized(self, calculator, a, b, expected):
        """参数化测试加法."""
        assert calculator.add(a, b) == expected

    @pytest.mark.parametrize("input_val,expected", [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ])
    def test_factorial(self, calculator, input_val, expected):
        """测试阶乘计算."""
        assert calculator.factorial(input_val) == expected


# 使用Mock进行依赖隔离测试
class TestDatabaseCalculator(unittest.TestCase):
    """测试带数据库依赖的计算器."""

    @patch('src.calculator.Database')
    def test_save_result(self, mock_db_class):
        """测试保存结果到数据库."""
        # 设置mock
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_db.save.return_value = True

        # 执行测试
        calc = DatabaseCalculator(mock_db)
        result = calc.add_and_save(2, 3)

        # 验证
        self.assertEqual(result, 5)
        mock_db.save.assert_called_once_with(operation="add", result=5)


# src/calculator.py (被测试的代码)
"""计算器模块实现."""

import logging
from typing import Protocol

logger = logging.getLogger(__name__)


class Database(Protocol):
    """数据库接口."""
    def save(self, operation: str, result: float) -> bool: ...


class Calculator:
    """简单计算器类."""

    def add(self, a: float, b: float) -> float:
        """加法运算."""
        logger.info(f"Adding {a} + {b}")
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """减法运算."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """乘法运算."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """除法运算."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def factorial(self, n: int) -> int:
        """计算阶乘."""
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


class DatabaseCalculator:
    """带数据库持久化的计算器."""

    def __init__(self, db: Database):
        self.db = db

    def add_and_save(self, a: float, b: float) -> float:
        """加法并保存结果."""
        result = a + b
        self.db.save(operation="add", result=result)
        return result
```

#### 1.3 集成测试

```python
# tests/integration/test_api_integration.py
"""API集成测试示例."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db
from src.models import User


# 创建测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """覆盖数据库依赖."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """设置测试数据库."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestUserAPI:
    """用户API集成测试."""

    def test_create_user(self, setup_database):
        """测试创建用户."""
        response = client.post(
            "/users/",
            json={"username": "testuser", "email": "test@example.com", "password": "secret"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_get_user(self, setup_database):
        """测试获取用户."""
        # 先创建用户
        create_response = client.post(
            "/users/",
            json={"username": "testuser", "email": "test@example.com", "password": "secret"}
        )
        user_id = create_response.json()["id"]

        # 获取用户
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    def test_get_nonexistent_user(self, setup_database):
        """测试获取不存在的用户."""
        response = client.get("/users/999")
        assert response.status_code == 404

    def test_create_duplicate_user(self, setup_database):
        """测试创建重复用户."""
        user_data = {"username": "testuser", "email": "test@example.com", "password": "secret"}

        # 第一次创建
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == 201

        # 第二次创建（应该失败）
        response2 = client.post("/users/", json=user_data)
        assert response2.status_code == 400


# 使用pytest-docker进行容器化集成测试
@pytest.fixture(scope="session")
def docker_services():
    """启动Docker服务."""
    import docker
    client = docker.from_env()

    # 启动PostgreSQL
    container = client.containers.run(
        "postgres:15",
        environment={
            "POSTGRES_DB": "test_db",
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_pass"
        },
        ports={"5432/tcp": 5433},
        detach=True,
        remove=True
    )

    import time
    time.sleep(3)  # 等待数据库启动

    yield container

    container.stop()
```

#### 1.4 端到端测试

```python
# tests/e2e/test_user_journey.py
"""端到端测试示例 - 使用Playwright."""

import pytest
from playwright.sync_api import Page, expect


class TestUserJourney:
    """用户旅程端到端测试."""

    def test_user_registration_and_login(self, page: Page):
        """测试用户注册和登录流程."""
        # 访问首页
        page.goto("https://example.com")

        # 点击注册
        page.click("text=Sign Up")

        # 填写注册表单
        page.fill("[name='username']", "testuser123")
        page.fill("[name='email']", "test123@example.com")
        page.fill("[name='password']", "TestPass123!")
        page.fill("[name='confirm_password']", "TestPass123!")

        # 提交表单
        page.click("button[type='submit']")

        # 验证注册成功
        expect(page.locator("text=Registration successful")).to_be_visible()

        # 登录
        page.fill("[name='username']", "testuser123")
        page.fill("[name='password']", "TestPass123!")
        page.click("button[type='submit']")

        # 验证登录成功
        expect(page.locator("text=Welcome, testuser123")).to_be_visible()

    def test_shopping_cart_flow(self, page: Page):
        """测试购物车流程."""
        # 登录
        page.goto("https://example.com/login")
        page.fill("[name='username']", "testuser")
        page.fill("[name='password']", "password")
        page.click("button[type='submit']")

        # 浏览商品
        page.goto("https://example.com/products")

        # 添加商品到购物车
        page.click("text=Add to Cart", timeout=5000)

        # 验证购物车数量更新
        cart_count = page.locator(".cart-count")
        expect(cart_count).to_have_text("1")

        # 进入购物车
        page.click(".cart-icon")

        # 验证商品在购物车中
        expect(page.locator("text=Product Name")).to_be_visible()

        # 结账
        page.click("text=Checkout")

        # 填写地址
        page.fill("[name='address']", "123 Test St")
        page.fill("[name='city']", "Test City")
        page.fill("[name='zip']", "12345")

        # 完成订单
        page.click("text=Place Order")

        # 验证订单成功
        expect(page.locator("text=Order Confirmed")).to_be_visible()


# conftest.py
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """创建浏览器实例."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """创建新页面."""
    page = browser.new_page()
    yield page
    page.close()
```

#### 1.5 测试配置（pytest.ini）

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=xml:coverage.xml
    -ra
markers =
    unit: 单元测试
    integration: 集成测试
    e2e: 端到端测试
    slow: 慢速测试
    smoke: 冒烟测试
    skip_in_ci: CI环境跳过

filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

---

### 2. 代码质量

#### 2.1 静态分析工具配置

```ini
# .flake8
[flake8]
max-line-length = 100
extend-ignore =
    E203,  # whitespace before ':'
    E501,  # line too long (handled by black)
    W503,  # line break before binary operator
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist,
    *.egg-info,
    migrations
max-complexity = 10
per-file-ignores =
    __init__.py:F401
```

```toml
# pyproject.toml - Black配置
[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311']
include = '\.pyi?$'
extend-exclude = '''
/(
    migrations
  | \.venv
  | venv
  | build
  | dist
)/
'''
```

```toml
# pyproject.toml - MyPy配置
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = false
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
show_error_codes = true
show_column_numbers = true
show_error_context = true

[[tool.mypy.overrides]]
module = [
    "numpy.*",
    "pandas.*",
    "sklearn.*",
    "tensorflow.*",
    "torch.*",
]
ignore_missing_imports = true
```

```toml
# pyproject.toml - Pylint配置
[tool.pylint.messages_control]
disable = [
    "C0103",  # invalid-name
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
    "R0903",  # too-few-public-methods
    "R0913",  # too-many-arguments
]

[tool.pylint.format]
max-line-length = 100

[tool.pylint.design]
max-args = 8
max-attributes = 10
```

#### 2.2 代码覆盖率配置

```toml
# pyproject.toml - Coverage配置
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*",
    "*/migrations/*",
    "*/venv/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
show_missing = true
skip_covered = false
fail_under = 80

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

#### 2.3 预提交钩子配置

```yaml
# .pre-commit-config.yaml
repos:
  # 基础检查
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: debug-statements
      - id: check-docstring-first

  # Black代码格式化
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  # isort导入排序
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  # Flake8代码检查
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        additional_dependencies: [
          flake8-docstrings,
          flake8-bugbear,
          flake8-comprehensions,
          flake8-print,
        ]

  # MyPy类型检查
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  # Bandit安全扫描
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]

  # 提交信息规范
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

#### 2.4 正例 vs 反例

**✅ 正例：高质量代码**

```python
"""用户服务模块.

提供用户相关的业务逻辑处理.
"""

from typing import Optional, Protocol
from dataclasses import dataclass
from datetime import datetime
import hashlib


class UserRepository(Protocol):
    """用户仓库接口."""

    def get_by_id(self, user_id: int) -> Optional["User"]:
        """根据ID获取用户."""
        ...

    def save(self, user: "User") -> bool:
        """保存用户."""
        ...


@dataclass(frozen=True)
class User:
    """用户实体类."""

    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime

    def verify_password(self, password: str) -> bool:
        """验证密码."""
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed == self.password_hash


class UserService:
    """用户服务类."""

    def __init__(self, repository: UserRepository) -> None:
        """初始化用户服务.

        Args:
            repository: 用户数据仓库
        """
        self._repository = repository

    def get_user(self, user_id: int) -> Optional[User]:
        """获取用户信息.

        Args:
            user_id: 用户ID

        Returns:
            用户对象，如果不存在则返回None
        """
        if user_id <= 0:
            raise ValueError("User ID must be positive")
        return self._repository.get_by_id(user_id)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """用户认证.

        Args:
            username: 用户名
            password: 密码

        Returns:
            认证成功返回用户对象，否则返回None
        """
        # 实现认证逻辑
        pass
```

**❌ 反例：低质量代码**

```python
# 没有文档字符串
class user:
    def __init__(self, n, e, p):
        self.n = n  # 变量名不清晰
        self.e = e
        self.p = p

    def check(self, pw):
        if self.p == pw:  # 明文存储密码！
            return True
        return False

def do_stuff(x, y, z, a, b, c, d, e, f):  # 参数过多
    # 函数职责不单一
    # 没有类型注解
    # 复杂度过高
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z + a + b + c + d + e + f
    return 0

# 全局变量
users = []

def addUser(u):  # 命名不规范
    users.append(u)  # 修改全局状态
```

---

### 3. 制品管理

#### 3.1 Docker镜像构建

```dockerfile
# Dockerfile - 多阶段构建
# 阶段1: 构建
FROM python:3.11-slim as builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 创建虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 阶段2: 运行
FROM python:3.11-slim as runner

WORKDIR /app

# 创建非root用户
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从builder复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制应用代码
COPY --chown=appuser:appgroup src/ ./src/

# 切换到非root用户
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile - ML模型服务
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制模型文件
COPY models/ ./models/

# 复制应用代码
COPY src/ ./src/

# 环境变量
ENV MODEL_PATH=/app/models
ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["python", "-m", "src.serve"]
```

#### 3.2 版本管理策略

```python
# src/version.py
"""版本管理模块."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Version:
    """语义化版本."""

    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None

    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version

    @classmethod
    def parse(cls, version_str: str) -> "Version":
        """解析版本字符串."""
        # 简化实现，实际应使用semver库
        parts = version_str.split("+")
        build = parts[1] if len(parts) > 1 else None

        parts = parts[0].split("-")
        prerelease = parts[1] if len(parts) > 1 else None

        numbers = parts[0].split(".")
        return cls(
            major=int(numbers[0]),
            minor=int(numbers[1]),
            patch=int(numbers[2]),
            prerelease=prerelease,
            build=build
        )

    def bump_major(self) -> "Version":
        """主版本升级."""
        return Version(major=self.major + 1, minor=0, patch=0)

    def bump_minor(self) -> "Version":
        """次版本升级."""
        return Version(major=self.major, minor=self.minor + 1, patch=0)

    def bump_patch(self) -> "Version":
        """补丁版本升级."""
        return Version(
            major=self.major,
            minor=self.minor,
            patch=self.patch + 1
        )


def get_version() -> str:
    """获取当前版本."""
    # 优先从环境变量获取
    if version := os.getenv("APP_VERSION"):
        return version

    # 从版本文件读取
    try:
        with open("VERSION", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        pass

    # 默认版本
    return "0.0.0-dev"


# 当前版本
__version__ = get_version()
```

```toml
# pyproject.toml - 项目版本管理
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "myapp"
dynamic = ["version"]
description = "My Application"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.12.0",
    "flake8>=7.0.0",
    "mypy>=1.8.0",
]

[project.urls]
Homepage = "https://github.com/example/myapp"
Repository = "https://github.com/example/myapp.git"
Documentation = "https://myapp.readthedocs.io"

[tool.setuptools.dynamic]
version = {file = "VERSION"}

[tool.setuptools.packages.find]
where = ["src"]
```

---

### 4. 部署策略详解

#### 4.1 特性开关（Feature Flags）

```python
# src/feature_flags.py
"""特性开关模块."""

import os
from enum import Enum
from functools import wraps
from typing import Callable, Any, Dict, Optional
import json
import redis


class FeatureState(Enum):
    """特性状态."""
    OFF = "off"
    ON = "on"
    PERCENTAGE = "percentage"


class FeatureFlag:
    """特性开关类."""

    def __init__(
        self,
        name: str,
        state: FeatureState = FeatureState.OFF,
        percentage: int = 0,
        user_ids: Optional[list] = None
    ):
        self.name = name
        self.state = state
        self.percentage = percentage
        self.user_ids = set(user_ids or [])

    def is_enabled(self, user_id: Optional[str] = None) -> bool:
        """检查特性是否启用."""
        if self.state == FeatureState.ON:
            return True
        if self.state == FeatureState.OFF:
            return False
        if self.state == FeatureState.PERCENTAGE:
            if user_id:
                # 基于用户ID的哈希决定
                import hashlib
                hash_val = int(hashlib.md5(
                    f"{self.name}:{user_id}".encode()
                ).hexdigest(), 16)
                return (hash_val % 100) < self.percentage
            return False
        return False


class FeatureFlagManager:
    """特性开关管理器."""

    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self._flags: Dict[str, FeatureFlag] = {}
        self._redis = redis_client
        self._load_flags()

    def _load_flags(self) -> None:
        """加载特性开关配置."""
        # 从环境变量加载
        flags_env = os.getenv("FEATURE_FLAGS", "{}")
        try:
            flags_config = json.loads(flags_env)
            for name, config in flags_config.items():
                self._flags[name] = FeatureFlag(
                    name=name,
                    state=FeatureState(config.get("state", "off")),
                    percentage=config.get("percentage", 0),
                    user_ids=config.get("user_ids", [])
                )
        except json.JSONDecodeError:
            pass

        # 从Redis加载（如果可用）
        if self._redis:
            self._load_from_redis()

    def _load_from_redis(self) -> None:
        """从Redis加载特性开关."""
        flags_data = self._redis.hgetall("feature_flags")
        for name, config_json in flags_data.items():
            name = name.decode() if isinstance(name, bytes) else name
            config = json.loads(config_json)
            self._flags[name] = FeatureFlag(
                name=name,
                state=FeatureState(config["state"]),
                percentage=config.get("percentage", 0),
                user_ids=config.get("user_ids", [])
            )

    def is_enabled(self, flag_name: str, user_id: Optional[str] = None) -> bool:
        """检查特性开关状态."""
        flag = self._flags.get(flag_name)
        if not flag:
            return False
        return flag.is_enabled(user_id)

    def enable(self, flag_name: str) -> None:
        """启用特性."""
        if flag_name in self._flags:
            self._flags[flag_name].state = FeatureState.ON

    def disable(self, flag_name: str) -> None:
        """禁用特性."""
        if flag_name in self._flags:
            self._flags[flag_name].state = FeatureState.OFF

    def set_percentage(self, flag_name: str, percentage: int) -> None:
        """设置百分比发布."""
        if flag_name in self._flags:
            self._flags[flag_name].state = FeatureState.PERCENTAGE
            self._flags[flag_name].percentage = percentage


# 全局管理器实例
_feature_manager: Optional[FeatureFlagManager] = None


def get_feature_manager() -> FeatureFlagManager:
    """获取特性开关管理器."""
    global _feature_manager
    if _feature_manager is None:
        redis_client = None
        try:
            redis_client = redis.Redis.from_url(
                os.getenv("REDIS_URL", "redis://localhost:6379")
            )
        except redis.ConnectionError:
            pass
        _feature_manager = FeatureFlagManager(redis_client)
    return _feature_manager


def feature_flag(flag_name: str):
    """特性开关装饰器."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            manager = get_feature_manager()
            if manager.is_enabled(flag_name):
                return func(*args, **kwargs)
            else:
                # 返回默认行为或旧版本
                return kwargs.get("default_return", None)
        return wrapper
    return decorator


# 使用示例
@feature_flag("new_payment_flow")
def process_payment_new(order_id: str, amount: float) -> dict:
    """新支付流程."""
    return {"status": "success", "method": "new", "order_id": order_id}


def process_payment_old(order_id: str, amount: float) -> dict:
    """旧支付流程."""
    return {"status": "success", "method": "old", "order_id": order_id}


def process_payment(order_id: str, amount: float, user_id: str) -> dict:
    """根据特性开关选择支付流程."""
    manager = get_feature_manager()
    if manager.is_enabled("new_payment_flow", user_id):
        return process_payment_new(order_id, amount)
    return process_payment_old(order_id, amount)
```

#### 4.2 完整部署流水线

```yaml
# .github/workflows/deploy.yml
name: Deploy Pipeline

on:
  push:
    branches: [main, develop]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 阶段1: 代码质量
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install black flake8 mypy
      - run: black --check src
      - run: flake8 src
      - run: mypy src

  # 阶段2: 测试
  test:
    runs-on: ubuntu-latest
    needs: quality
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3

  # 阶段3: 安全扫描
  security:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install bandit safety
      - run: bandit -r src
      - run: safety check -r requirements.txt

  # 阶段4: 构建
  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
      image_digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,prefix={{branch}}-
      - uses: docker/build-push-action@v5
        id: build
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # 阶段5: 部署到Staging
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: staging
      url: https://staging.example.com
    if: github.ref == 'refs/heads/develop'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Staging
        run: |
          echo "${{ secrets.KUBECONFIG_STAGING }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
          kubectl set image deployment/myapp \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/myapp
          kubectl rollout history deployment/myapp

  # 阶段6: 部署到Production（金丝雀）
  deploy-production-canary:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: production-canary
      url: https://canary.example.com
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy Canary (10%)
        run: |
          echo "${{ secrets.KUBECONFIG_PROD }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
          # 部署金丝雀版本
          kubectl apply -f k8s/canary-deployment.yaml
          kubectl set image deployment/myapp-canary \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/myapp-canary

  # 阶段7: 金丝雀验证
  canary-analysis:
    runs-on: ubuntu-latest
    needs: deploy-production-canary
    environment:
      name: production-canary-analysis
    steps:
      - name: Run Canary Analysis
        run: |
          # 运行自动化验证
          echo "Running canary analysis..."
          # 检查错误率、延迟等指标
          sleep 300  # 5分钟观察期
          # 如果指标正常，继续全量部署

  # 阶段8: 全量部署
  deploy-production-full:
    runs-on: ubuntu-latest
    needs: canary-analysis
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v4
      - name: Full Production Deploy
        run: |
          echo "${{ secrets.KUBECONFIG_PROD }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
          kubectl set image deployment/myapp \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/myapp
          # 删除金丝雀
          kubectl delete deployment myapp-canary
```

---

## 第四部分：Python ML生态

### 1. 核心库

#### 1.1 NumPy基础

```python
"""NumPy核心操作示例."""

import numpy as np


# ==================== 数组创建 ====================
def create_arrays():
    """创建各种数组."""
    # 从列表创建
    arr1 = np.array([1, 2, 3, 4, 5])

    # 创建特定数组
    zeros = np.zeros((3, 4))          # 3x4 零矩阵
    ones = np.ones((2, 3))            # 2x3 全1矩阵
    identity = np.eye(3)              # 3x3 单位矩阵

    # 范围数组
    arange_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
    linspace_arr = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]

    # 随机数组
    random_arr = np.random.rand(3, 3)     # 均匀分布
    normal_arr = np.random.randn(3, 3)    # 标准正态分布
    randint_arr = np.random.randint(0, 10, (3, 3))  # 随机整数

    return {
        "arr1": arr1,
        "zeros": zeros,
        "ones": ones,
        "identity": identity,
        "arange": arange_arr,
        "linspace": linspace_arr,
        "random": random_arr,
        "normal": normal_arr,
        "randint": randint_arr
    }


# ==================== 数组操作 ====================
def array_operations():
    """数组基本操作."""
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    # 形状操作
    print(f"Shape: {arr.shape}")      # (3, 3)
    print(f"Size: {arr.size}")        # 9
    print(f"Dimensions: {arr.ndim}")  # 2

    # 重塑
    reshaped = arr.reshape(1, 9)      # 1x9
    flattened = arr.flatten()          # 一维

    # 转置
    transposed = arr.T

    # 索引和切片
    element = arr[1, 2]       # 6
    row = arr[1, :]           # [4, 5, 6]
    col = arr[:, 1]           # [2, 5, 8]
    subarray = arr[0:2, 1:3]  # [[2, 3], [5, 6]]

    # 布尔索引
    mask = arr > 5
    filtered = arr[mask]      # [6, 7, 8, 9]

    return {
        "reshaped": reshaped,
        "flattened": flattened,
        "transposed": transposed,
        "filtered": filtered
    }


# ==================== 数学运算 ====================
def mathematical_operations():
    """数学运算."""
    a = np.array([1, 2, 3, 4])
    b = np.array([5, 6, 7, 8])

    # 基本运算
    add = a + b              # [6, 8, 10, 12]
    subtract = a - b         # [-4, -4, -4, -4]
    multiply = a * b         # [5, 12, 21, 32]
    divide = a / b           # [0.2, 0.33, 0.43, 0.5]

    # 矩阵乘法
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    matmul = np.matmul(A, B)  # 或 A @ B

    # 统计运算
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    mean = np.mean(arr)           # 3.5
    mean_axis0 = np.mean(arr, axis=0)  # [2.5, 3.5, 4.5]
    mean_axis1 = np.mean(arr, axis=1)  # [2, 5]

    std = np.std(arr)             # 标准差
    var = np.var(arr)             # 方差
    min_val = np.min(arr)         # 最小值
    max_val = np.max(arr)         # 最大值
    sum_val = np.sum(arr)         # 求和

    # 线性代数
    det = np.linalg.det(A)        # 行列式
    inv = np.linalg.inv(A)        # 逆矩阵
    eigenvalues, eigenvectors = np.linalg.eig(A)  # 特征值和特征向量

    return {
        "matmul": matmul,
        "mean": mean,
        "std": std,
        "det": det,
        "inv": inv,
        "eigenvalues": eigenvalues
    }


# ==================== 广播机制 ====================
def broadcasting():
    """NumPy广播机制."""
    # 标量广播
    arr = np.array([1, 2, 3])
    result = arr + 10  # [11, 12, 13]

    # 一维数组广播到二维
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # 3x3
    b = np.array([1, 0, 1])                           # 1x3
    result = A + b  # 每行加上b

    # 列向量广播
    c = np.array([[1], [2], [3]])  # 3x1
    result = A + c  # 每列加上c

    return result
```

#### 1.2 Pandas数据处理

```python
"""Pandas核心操作示例."""

import pandas as pd
import numpy as np


# ==================== DataFrame创建 ====================
def create_dataframes():
    """创建DataFrame的各种方式."""
    # 从字典创建
    df1 = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Tokyo']
    })

    # 从列表创建
    df2 = pd.DataFrame([
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 30},
        {'name': 'Charlie', 'age': 35}
    ])

    # 从NumPy数组创建
    df3 = pd.DataFrame(
        np.random.randn(5, 3),
        columns=['A', 'B', 'C'],
        index=['a', 'b', 'c', 'd', 'e']
    )

    # 从CSV读取
    # df4 = pd.read_csv('data.csv')

    # 从数据库读取
    # import sqlite3
    # conn = sqlite3.connect('database.db')
    # df5 = pd.read_sql('SELECT * FROM users', conn)

    return df1, df2, df3


# ==================== 数据探索 ====================
def explore_data():
    """数据探索方法."""
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50],
        'C': ['a', 'b', 'c', 'd', 'e'],
        'D': [1.1, 2.2, np.nan, 4.4, 5.5]
    })

    # 基本信息
    print(df.head(3))        # 前3行
    print(df.tail(3))        # 后3行
    print(df.shape)          # (5, 4)
    print(df.columns)        # Index(['A', 'B', 'C', 'D'], dtype='object')
    print(df.dtypes)         # 数据类型
    print(df.info())         # 详细信息
    print(df.describe())     # 统计摘要

    # 统计信息
    print(df['A'].mean())    # 平均值
    print(df['A'].sum())     # 求和
    print(df['A'].std())     # 标准差
    print(df['A'].min())     # 最小值
    print(df['A'].max())     # 最大值

    # 唯一值
    print(df['C'].unique())  # ['a', 'b', 'c', 'd', 'e']
    print(df['C'].value_counts())  # 值计数

    return df


# ==================== 数据选择 ====================
def select_data():
    """数据选择方法."""
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50],
        'C': ['a', 'b', 'c', 'd', 'e']
    }, index=['row1', 'row2', 'row3', 'row4', 'row5'])

    # 列选择
    col_a = df['A']           # 单列 (Series)
    cols_ab = df[['A', 'B']]  # 多列 (DataFrame)

    # 行选择 (loc - 标签索引)
    row1 = df.loc['row1']           # 单行
    rows_1_3 = df.loc['row1':'row3']  # 多行
    specific = df.loc['row1', 'A']  # 特定值

    # 行选择 (iloc - 位置索引)
    row0 = df.iloc[0]           # 第一行
    rows_0_2 = df.iloc[0:3]     # 前3行
    specific = df.iloc[0, 0]    # 第一行第一列

    # 布尔索引
    filtered = df[df['A'] > 2]  # A > 2的行
    multi_condition = df[(df['A'] > 2) & (df['B'] < 50)]  # 多条件

    # isin
    in_list = df[df['C'].isin(['a', 'c', 'e'])]

    return {
        'col_a': col_a,
        'filtered': filtered,
        'multi_condition': multi_condition
    }


# ==================== 数据处理 ====================
def process_data():
    """数据处理方法."""
    df = pd.DataFrame({
        'A': [1, 2, np.nan, 4, 5],
        'B': ['a', 'b', 'c', 'd', 'e'],
        'C': [10, 20, 30, 40, 50],
        'date': pd.date_range('2024-01-01', periods=5)
    })

    # 处理缺失值
    df_filled = df.fillna(0)           # 填充0
    df_dropped = df.dropna()           # 删除含NaN的行
    df_interpolated = df.interpolate() # 插值

    # 删除重复值
    df_unique = df.drop_duplicates()

    # 类型转换
    df['C'] = df['C'].astype(float)
    df['date'] = pd.to_datetime(df['date'])

    # 新增列
    df['D'] = df['A'] + df['C']        # 基于现有列
    df['E'] = df['B'].str.upper()      # 字符串操作

    # 删除列
    df_dropped_col = df.drop('E', axis=1)

    # 重命名列
    df_renamed = df.rename(columns={'A': 'Column_A', 'B': 'Column_B'})

    # 排序
    df_sorted = df.sort_values('C', ascending=False)

    # 应用函数
    df['F'] = df['C'].apply(lambda x: x ** 2)

    return df


# ==================== 数据聚合 ====================
def aggregate_data():
    """数据聚合方法."""
    df = pd.DataFrame({
        'category': ['A', 'B', 'A', 'B', 'A', 'B'],
        'value1': [10, 20, 30, 40, 50, 60],
        'value2': [1, 2, 3, 4, 5, 6]
    })

    # groupby聚合
    grouped = df.groupby('category').agg({
        'value1': ['sum', 'mean', 'count'],
        'value2': ['min', 'max']
    })

    # 简单聚合
    sum_by_category = df.groupby('category')['value1'].sum()
    mean_by_category = df.groupby('category')['value1'].mean()

    # 透视表
    pivot = df.pivot_table(
        values='value1',
        index='category',
        aggfunc=['sum', 'mean', 'count']
    )

    # 交叉表
    crosstab = pd.crosstab(df['category'], df['value2'])

    return grouped, pivot


# ==================== 数据合并 ====================
def merge_data():
    """数据合并方法."""
    df1 = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'David']
    })

    df2 = pd.DataFrame({
        'id': [1, 2, 3, 5],
        'age': [25, 30, 35, 40]
    })

    # 内连接
    inner = pd.merge(df1, df2, on='id', how='inner')

    # 左连接
    left = pd.merge(df1, df2, on='id', how='left')

    # 右连接
    right = pd.merge(df1, df2, on='id', how='right')

    # 外连接
    outer = pd.merge(df1, df2, on='id', how='outer')

    # 纵向合并
    df3 = pd.DataFrame({
        'id': [5, 6],
        'name': ['Eve', 'Frank']
    })
    concatenated = pd.concat([df1, df3], ignore_index=True)

    return inner, left, outer, concatenated
```

#### 1.3 Scikit-Learn机器学习

```python
"""Scikit-Learn完整机器学习流程示例."""

import numpy as np
import pandas as pd
from sklearn.model_selection import (
    train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
)
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
import joblib
import warnings
warnings.filterwarnings('ignore')


# ==================== 数据准备 ====================
def prepare_data():
    """准备示例数据."""
    from sklearn.datasets import load_iris, make_classification

    # 使用Iris数据集
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target

    # 或者生成合成数据
    # X, y = make_classification(
    #     n_samples=1000,
    #     n_features=20,
    #     n_informative=10,
    #     n_redundant=5,
    #     n_classes=2,
    #     random_state=42
    # )

    return X, y


# ==================== 数据预处理Pipeline ====================
def create_preprocessing_pipeline(numeric_features, categorical_features):
    """创建预处理Pipeline."""

    # 数值特征处理
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # 分类特征处理
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # 组合预处理
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    return preprocessor


# ==================== 完整训练流程 ====================
class MLWorkflow:
    """机器学习工作流类."""

    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.pipeline = None
        self.best_params = None

    def load_data(self, X, y, test_size=0.2, random_state=42):
        """加载并分割数据."""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        print(f"训练集大小: {self.X_train.shape}")
        print(f"测试集大小: {self.X_test.shape}")
        return self

    def create_pipeline(self, model, numeric_features=None, categorical_features=None):
        """创建完整Pipeline."""
        if numeric_features is None:
            numeric_features = self.X_train.select_dtypes(
                include=[np.number]
            ).columns.tolist()

        if categorical_features is None:
            categorical_features = self.X_train.select_dtypes(
                include=['object', 'category']
            ).columns.tolist()

        self.preprocessor = create_preprocessing_pipeline(
            numeric_features, categorical_features
        )

        self.pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', model)
        ])

        return self

    def train(self):
        """训练模型."""
        print("开始训练...")
        self.pipeline.fit(self.X_train, self.y_train)
        print("训练完成!")
        return self

    def evaluate(self):
        """评估模型."""
        y_pred = self.pipeline.predict(self.X_test)
        y_prob = self.pipeline.predict_proba(self.X_test) if hasattr(
            self.pipeline.named_steps['classifier'], 'predict_proba'
        ) else None

        print("\n" + "="*50)
        print("模型评估结果")
        print("="*50)

        # 基本指标
        print(f"\n准确率 (Accuracy): {accuracy_score(self.y_test, y_pred):.4f}")
        print(f"精确率 (Precision): {precision_score(self.y_test, y_pred, average='weighted'):.4f}")
        print(f"召回率 (Recall): {recall_score(self.y_test, y_pred, average='weighted'):.4f}")
        print(f"F1分数 (F1-Score): {f1_score(self.y_test, y_pred, average='weighted'):.4f}")

        # 详细报告
        print("\n分类报告:")
        print(classification_report(self.y_test, y_pred))

        # 混淆矩阵
        print("混淆矩阵:")
        print(confusion_matrix(self.y_test, y_pred))

        # ROC-AUC (二分类)
        if y_prob is not None and len(np.unique(self.y_test)) == 2:
            auc = roc_auc_score(self.y_test, y_prob[:, 1])
            print(f"\nROC-AUC: {auc:.4f}")

        return self

    def cross_validate(self, cv=5):
        """交叉验证."""
        scores = cross_val_score(
            self.pipeline, self.X_train, self.y_train, cv=cv, scoring='accuracy'
        )
        print(f"\n交叉验证得分: {scores}")
        print(f"平均得分: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
        return self

    def hyperparameter_tuning(self, param_grid, cv=5):
        """超参数调优."""
        print("\n开始超参数调优...")

        grid_search = GridSearchCV(
            self.pipeline,
            param_grid,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(self.X_train, self.y_train)

        self.best_params = grid_search.best_params_
        self.pipeline = grid_search.best_estimator_

        print(f"\n最佳参数: {self.best_params}")
        print(f"最佳交叉验证得分: {grid_search.best_score_:.4f}")

        return self

    def save_model(self, filepath):
        """保存模型."""
        joblib.dump(self.pipeline, filepath)
        print(f"\n模型已保存到: {filepath}")
        return self

    def load_model(self, filepath):
        """加载模型."""
        self.pipeline = joblib.load(filepath)
        print(f"\n模型已从 {filepath} 加载")
        return self

    def predict(self, X):
        """预测."""
        return self.pipeline.predict(X)


# ==================== 使用示例 ====================
def main():
    """主函数 - 完整ML流程示例."""

    # 1. 准备数据
    X, y = prepare_data()

    # 2. 创建工作流
    workflow = MLWorkflow()

    # 3. 加载数据
    workflow.load_data(X, y)

    # 4. 创建模型Pipeline
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    workflow.create_pipeline(model)

    # 5. 交叉验证
    workflow.cross_validate(cv=5)

    # 6. 训练
    workflow.train()

    # 7. 评估
    workflow.evaluate()

    # 8. 超参数调优（可选）
    param_grid = {
        'classifier__n_estimators': [50, 100, 200],
        'classifier__max_depth': [3, 5, 7, None],
        'classifier__min_samples_split': [2, 5, 10]
    }
    # workflow.hyperparameter_tuning(param_grid)

    # 9. 保存模型
    workflow.save_model('model.pkl')

    # 10. 预测新数据
    new_data = X.iloc[:5]
    predictions = workflow.predict(new_data)
    print(f"\n新数据预测结果: {predictions}")


if __name__ == "__main__":
    main()
```

#### 1.4 TensorFlow/PyTorch概述

```python
"""TensorFlow和PyTorch基础对比示例."""

import numpy as np

# ==================== TensorFlow示例 ====================
def tensorflow_basics():
    """TensorFlow基础操作."""
    import tensorflow as tf

    print("="*50)
    print("TensorFlow 基础")
    print("="*50)

    # 张量创建
    tensor = tf.constant([[1, 2, 3], [4, 5, 6]])
    print(f"Tensor:\n{tensor}")
    print(f"Shape: {tensor.shape}")
    print(f"Dtype: {tensor.dtype}")

    # 随机张量
    random_tensor = tf.random.normal([3, 3], mean=0, stddev=1)
    print(f"\n随机正态分布张量:\n{random_tensor}")

    # 基本运算
    a = tf.constant([[1, 2], [3, 4]])
    b = tf.constant([[5, 6], [7, 8]])

    print(f"\n加法:\n{tf.add(a, b)}")
    print(f"乘法:\n{tf.matmul(a, b)}")

    # 自动微分
    x = tf.Variable(3.0)

    with tf.GradientTape() as tape:
        y = x ** 2

    dy_dx = tape.gradient(y, x)
    print(f"\n导数 dy/dx at x=3: {dy_dx}")  # 6.0

    # 简单神经网络
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    print(f"\n模型结构:")
    model.summary()

    return model


# ==================== PyTorch示例 ====================
def pytorch_basics():
    """PyTorch基础操作."""
    import torch
    import torch.nn as nn
    import torch.optim as optim

    print("\n" + "="*50)
    print("PyTorch 基础")
    print("="*50)

    # 张量创建
    tensor = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32)
    print(f"Tensor:\n{tensor}")
    print(f"Shape: {tensor.shape}")
    print(f"Device: {tensor.device}")

    # GPU支持
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor_gpu = tensor.to(device)
    print(f"\nGPU可用: {torch.cuda.is_available()}")

    # 随机张量
    random_tensor = torch.randn(3, 3)
    print(f"\n随机正态分布张量:\n{random_tensor}")

    # 基本运算
    a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
    b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)

    print(f"\n加法:\n{a + b}")
    print(f"矩阵乘法:\n{a @ b}")

    # 自动微分
    x = torch.tensor(3.0, requires_grad=True)
    y = x ** 2
    y.backward()
    print(f"\n导数 dy/dx at x=3: {x.grad}")  # 6.0

    # 简单神经网络
    class SimpleNet(nn.Module):
        def __init__(self):
            super(SimpleNet, self).__init__()
            self.fc1 = nn.Linear(10, 64)
            self.dropout = nn.Dropout(0.2)
            self.fc2 = nn.Linear(64, 32)
            self.fc3 = nn.Linear(32, 10)
            self.relu = nn.ReLU()

        def forward(self, x):
            x = self.relu(self.fc1(x))
            x = self.dropout(x)
            x = self.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    model = SimpleNet()
    print(f"\n模型结构:")
    print(model)

    # 统计参数数量
    total_params = sum(p.numel() for p in model.parameters())
    print(f"总参数数量: {total_params}")

    return model


# ==================== 框架对比 ====================
def framework_comparison():
    """TensorFlow vs PyTorch 对比."""
    comparison = {
        "特性": ["开发公司", "计算图", "调试", "部署", "学习曲线", "社区"],
        "TensorFlow": [
            "Google",
            "静态图(2.x支持动态)",
            "较复杂",
            "TF Serving, TF Lite",
            "较陡",
            "工业界主流"
        ],
        "PyTorch": [
            "Meta (Facebook)",
            "动态图",
            "简单(原生Python)",
            "TorchServe, ONNX",
            "平缓",
            "学术界主流"
        ]
    }

    import pandas as pd
    df = pd.DataFrame(comparison)
    print("\n" + "="*50)
    print("TensorFlow vs PyTorch 对比")
    print("="*50)
    print(df.to_string(index=False))


# ==================== JAX示例 ====================
def jax_basics():
    """JAX基础操作."""
    import jax
    import jax.numpy as jnp
    from jax import grad, jit, vmap

    print("\n" + "="*50)
    print("JAX 基础")
    print("="*50)

    # JAX NumPy
    x = jnp.array([1.0, 2.0, 3.0])
    print(f"JAX Array: {x}")
    print(f"Sin: {jnp.sin(x)}")

    # 自动微分
    def f(x):
        return x ** 2 + 3 * x + 1

    df = grad(f)
    print(f"\nf(x) = x² + 3x + 1")
    print(f"f'(2) = {df(2.0)}")  # 7.0

    # JIT编译加速
    @jit
    def fast_function(x):
        return jnp.sum(x ** 2)

    large_array = jnp.ones(1000000)
    result = fast_function(large_array)
    print(f"\nJIT编译求和结果: {result}")

    # 向量化映射
    @vmap
def batch_function(x):
        return x ** 2

    batch_x = jnp.array([1.0, 2.0, 3.0, 4.0, 5.0])
    batch_result = batch_function(batch_x)
    print(f"\n向量化结果: {batch_result}")
```

### 2. 模型训练流程

```python
"""完整的机器学习模型训练流程."""

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
from datetime import datetime
from pathlib import Path


class ModelTrainer:
    """模型训练器类."""

    def __init__(self, model_name: str = "model"):
        self.model_name = model_name
        self.model = None
        self.scaler = StandardScaler()
        self.metrics = {}
        self.training_info = {}

    def load_data(self) -> tuple:
        """加载数据."""
        # 使用乳腺癌数据集作为示例
        data = load_breast_cancer()
        X = pd.DataFrame(data.data, columns=data.feature_names)
        y = data.target

        print(f"数据形状: {X.shape}")
        print(f"类别分布:\n{pd.Series(y).value_counts()}")

        return X, y

    def preprocess(self, X: pd.DataFrame, y: np.ndarray, test_size: float = 0.2):
        """数据预处理."""
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # 标准化
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        print(f"训练集: {X_train_scaled.shape}")
        print(f"测试集: {X_test_scaled.shape}")

        return X_train_scaled, X_test_scaled, y_train, y_test

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """训练模型."""
        print("\n开始训练...")

        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        # 交叉验证
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
        print(f"交叉验证得分: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

        # 训练
        self.model.fit(X_train, y_train)

        # 记录训练信息
        self.training_info = {
            "model_type": "RandomForestClassifier",
            "n_estimators": 100,
            "max_depth": 10,
            "training_time": datetime.now().isoformat(),
            "cv_scores": cv_scores.tolist(),
            "cv_mean": float(cv_scores.mean()),
            "cv_std": float(cv_scores.std())
        }

        print("训练完成!")
        return self

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray):
        """评估模型."""
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)

        # 计算指标
        self.metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "report": classification_report(y_test, y_pred, output_dict=True)
        }

        print("\n评估结果:")
        print(f"准确率: {self.metrics['accuracy']:.4f}")
        print("\n分类报告:")
        print(classification_report(y_test, y_pred))

        return self

    def save(self, output_dir: str = "models"):
        """保存模型和相关信息."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_dir = output_path / f"{self.model_name}_{timestamp}"
        model_dir.mkdir(exist_ok=True)

        # 保存模型
        joblib.dump(self.model, model_dir / "model.pkl")
        joblib.dump(self.scaler, model_dir / "scaler.pkl")

        # 保存训练信息
        with open(model_dir / "training_info.json", "w") as f:
            json.dump(self.training_info, f, indent=2)

        # 保存评估指标
        with open(model_dir / "metrics.json", "w") as f:
            json.dump(self.metrics, f, indent=2)

        # 保存特征重要性
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = {
                "features": load_breast_cancer().feature_names.tolist(),
                "importance": self.model.feature_importances_.tolist()
            }
            with open(model_dir / "feature_importance.json", "w") as f:
                json.dump(feature_importance, f, indent=2)

        print(f"\n模型已保存到: {model_dir}")
        return model_dir

    def load(self, model_dir: str):
        """加载模型."""
        model_path = Path(model_dir)
        self.model = joblib.load(model_path / "model.pkl")
        self.scaler = joblib.load(model_path / "scaler.pkl")

        with open(model_path / "training_info.json") as f:
            self.training_info = json.load(f)

        print(f"模型已从 {model_dir} 加载")
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """预测."""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)


def main():
    """主函数."""
    # 创建训练器
    trainer = ModelTrainer(model_name="breast_cancer_classifier")

    # 加载数据
    X, y = trainer.load_data()

    # 预处理
    X_train, X_test, y_train, y_test = trainer.preprocess(X, y)

    # 训练
    trainer.train(X_train, y_train)

    # 评估
    trainer.evaluate(X_test, y_test)

    # 保存
    model_dir = trainer.save()

    # 加载并预测
    new_trainer = ModelTrainer()
    new_trainer.load(model_dir)
    predictions = new_trainer.predict(X_test[:5])
    print(f"\n预测结果: {predictions}")


if __name__ == "__main__":
    main()
```

---

## 第五部分：MLOps

### 1. 实验跟踪

#### 1.1 MLflow实验跟踪

```python
"""MLflow实验跟踪完整示例."""

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import json


class MLflowExperimentTracker:
    """MLflow实验跟踪器."""

    def __init__(self, experiment_name: str, tracking_uri: str = "http://localhost:5000"):
        """初始化实验跟踪器.

        Args:
            experiment_name: 实验名称
            tracking_uri: MLflow tracking服务器URI
        """
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name

    def start_run(self, run_name: str = None, nested: bool = False):
        """开始一个新的运行."""
        self.run = mlflow.start_run(run_name=run_name, nested=nested)
        return self

    def end_run(self):
        """结束当前运行."""
        mlflow.end_run()

    def log_params(self, params: dict):
        """记录参数."""
        for key, value in params.items():
            mlflow.log_param(key, value)

    def log_metrics(self, metrics: dict, step: int = None):
        """记录指标."""
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)

    def log_artifact(self, local_path: str, artifact_path: str = None):
        """记录文件."""
        mlflow.log_artifact(local_path, artifact_path)

    def log_model(self, model, artifact_path: str, registered_model_name: str = None):
        """记录模型."""
        mlflow.sklearn.log_model(
            model,
            artifact_path,
            registered_model_name=registered_model_name
        )

    def log_figure(self, figure, artifact_file: str):
        """记录图表."""
        mlflow.log_figure(figure, artifact_file)


def train_with_mlflow():
    """使用MLflow跟踪训练过程."""

    # 初始化跟踪器
    tracker = MLflowExperimentTracker("iris_classification")

    # 加载数据
    data = load_iris()
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 定义要尝试的超参数组合
    param_grid = [
        {"n_estimators": 50, "max_depth": 5},
        {"n_estimators": 100, "max_depth": 10},
        {"n_estimators": 200, "max_depth": None},
    ]

    for i, params in enumerate(param_grid):
        with tracker.start_run(run_name=f"run_{i+1}"):
            print(f"\n运行 {i+1}: {params}")

            # 记录参数
            tracker.log_params(params)
            tracker.log_param("dataset", "iris")
            tracker.log_param("test_size", 0.2)

            # 训练模型
            model = RandomForestClassifier(
                n_estimators=params["n_estimators"],
                max_depth=params["max_depth"],
                random_state=42
            )

            model.fit(X_train, y_train)

            # 交叉验证
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            tracker.log_metric("cv_mean", cv_scores.mean())
            tracker.log_metric("cv_std", cv_scores.std())

            # 测试集评估
            y_pred = model.predict(X_test)

            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average="weighted"),
                "recall": recall_score(y_test, y_pred, average="weighted"),
                "f1": f1_score(y_test, y_pred, average="weighted"),
            }
            tracker.log_metrics(metrics)

            # 记录特征重要性图
            fig, ax = plt.subplots(figsize=(10, 6))
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            ax.bar(range(len(importances)), importances[indices])
            ax.set_xticks(range(len(importances)))
            ax.set_xticklabels([data.feature_names[i] for i in indices], rotation=45)
            ax.set_title("Feature Importance")
            tracker.log_figure(fig, "feature_importance.png")
            plt.close()

            # 记录模型
            tracker.log_model(model, "model", registered_model_name="iris_rf")

            print(f"准确率: {metrics['accuracy']:.4f}")

        tracker.end_run()


# MLflow部署
def deploy_mlflow_server():
    """MLflow服务器部署配置."""

    # docker-compose.yml
    docker_compose = """
version: '3.8'

services:
  mlflow:
    image: python:3.11-slim
    ports:
      - "5000:5000"
    environment:
      - MLFLOW_TRACKING_URI=http://0.0.0.0:5000
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    volumes:
      - ./mlruns:/mlruns
      - ./artifacts:/artifacts
    command: >
      bash -c "pip install mlflow boto3 psycopg2-binary &&
               mlflow server
               --backend-store-uri postgresql://user:pass@postgres/mlflow
               --default-artifact-root s3://mlflow-bucket/artifacts
               --host 0.0.0.0
               --port 5000"

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mlflow
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""

    print("MLflow Docker Compose配置:")
    print(docker_compose)


# MLflow CLI命令
mlflow_cli_commands = """
# 启动MLflow Tracking服务器
mlflow server --host 0.0.0.0 --port 5000

# 运行实验
mlflow run . --experiment-name my_experiment

# 查看实验
mlflow experiments list

# 搜索运行
mlflow runs search --experiment-id 1

# 下载模型
mlflow artifacts download -r runs:/<run_id>/model -d ./downloaded_model

# 部署模型为REST API
mlflow models serve -m runs:/<run_id>/model -p 1234

# 构建Docker镜像
mlflow models build-docker -m runs:/<run_id>/model -n my-model-image
"""
```

#### 1.2 Weights & Biases (W&B)

```python
"""Weights & Biases实验跟踪示例."""

import wandb
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def train_with_wandb():
    """使用W&B跟踪训练过程."""

    # 初始化W&B
    wandb.init(
        project="iris-classification",
        entity="your-username",
        config={
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42,
            "dataset": "iris"
        }
    )

    # 获取配置
    config = wandb.config

    # 加载数据
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # 训练模型
    model = RandomForestClassifier(
        n_estimators=config.n_estimators,
        max_depth=config.max_depth,
        random_state=config.random_state
    )

    model.fit(X_train, y_train)

    # 评估
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # 记录指标
    wandb.log({"accuracy": accuracy})

    # 记录混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    wandb.log({"confusion_matrix": wandb.Image(plt)})
    plt.close()

    # 记录特征重要性
    feature_importance = dict(zip(
        data.feature_names,
        model.feature_importances_
    ))
    wandb.log({"feature_importance": wandb.Table(
        data=[[k, v] for k, v in feature_importance.items()],
        columns=["feature", "importance"]
    )})

    # 保存模型
    wandb.sklearn.plot_feature_importances(model, data.feature_names)

    # 结束运行
    wandb.finish()


# W&B Sweeps (超参数搜索)
def sweep_configuration():
    """W&B Sweep配置."""

    sweep_config = {
        "method": "bayes",  # 贝叶斯优化
        "metric": {
            "name": "accuracy",
            "goal": "maximize"
        },
        "parameters": {
            "n_estimators": {
                "values": [50, 100, 200, 500]
            },
            "max_depth": {
                "values": [5, 10, 15, 20, None]
            },
            "min_samples_split": {
                "distribution": "int_uniform",
                "min": 2,
                "max": 20
            },
            "max_features": {
                "values": ["sqrt", "log2", None]
            }
        },
        "early_terminate": {
            "type": "hyperband",
            "min_iter": 3
        }
    }

    # 创建sweep
    sweep_id = wandb.sweep(sweep_config, project="iris-classification")

    # 启动sweep agent
    wandb.agent(sweep_id, function=train_with_wandb, count=20)
```

#### 1.3 TensorBoard

```python
"""TensorBoard使用示例."""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from datetime import datetime


def train_with_tensorboard():
    """使用TensorBoard跟踪训练."""

    # 加载数据
    (X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
    X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
    X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0

    # 创建模型
    model = keras.Sequential([
        keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
        keras.layers.MaxPooling2D(),
        keras.layers.Conv2D(64, 3, activation='relu'),
        keras.layers.MaxPooling2D(),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # 创建TensorBoard回调
    log_dir = f"logs/fit/{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    tensorboard_callback = keras.callbacks.TensorBoard(
        log_dir=log_dir,
        histogram_freq=1,  # 每epoch记录直方图
        write_graph=True,   # 记录计算图
        write_images=True,  # 记录权重图像
        update_freq='epoch',
        profile_batch=2     # 性能分析
    )

    # 其他回调
    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    model_checkpoint = keras.callbacks.ModelCheckpoint(
        'best_model.h5',
        monitor='val_accuracy',
        save_best_only=True
    )

    # 训练
    history = model.fit(
        X_train, y_train,
        epochs=20,
        batch_size=128,
        validation_split=0.2,
        callbacks=[
            tensorboard_callback,
            early_stopping,
            model_checkpoint
        ]
    )

    # 启动TensorBoard
    # tensorboard --logdir logs/fit

    return model, history


# 自定义TensorBoard回调
class CustomTensorBoard(keras.callbacks.TensorBoard):
    """自定义TensorBoard回调."""

    def __init__(self, log_dir, **kwargs):
        super().__init__(log_dir, **kwargs)
        self.writer = tf.summary.create_file_writer(log_dir)

    def on_epoch_end(self, epoch, logs=None):
        super().on_epoch_end(epoch, logs)

        # 记录自定义指标
        with self.writer.as_default():
            # 学习率
            lr = self.model.optimizer.learning_rate.numpy()
            tf.summary.scalar('learning_rate', lr, step=epoch)

            # 权重统计
            for layer in self.model.layers:
                if hasattr(layer, 'kernel'):
                    weights = layer.kernel
                    tf.summary.histogram(
                        f'{layer.name}/weights',
                        weights,
                        step=epoch
                    )
```

#### 1.4 实验跟踪工具对比

| 特性 | MLflow | Weights & Biases | TensorBoard |
|------|--------|------------------|-------------|
| **托管方式** | 自托管/SaaS | SaaS | 自托管 |
| **价格** | 开源免费 | 免费额度+付费 | 开源免费 |
| **易用性** | 中 | 高 | 中 |
| **可视化** | 良好 | 优秀 | 良好 |
| **协作** | 中 | 优秀 | 弱 |
| **模型注册** | 原生支持 | 支持 | 需配合 |
| **最佳场景** | 企业自托管 | 团队协作 | TensorFlow |

---

### 2. 模型版本管理

#### 2.1 MLflow Model Registry

```python
"""MLflow模型注册中心使用示例."""

import mlflow
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import joblib


def model_registry_workflow():
    """模型注册完整工作流."""

    # 设置MLflow
    mlflow.set_tracking_uri("http://localhost:5000")
    client = MlflowClient()

    # 1. 训练并记录模型
    with mlflow.start_run(run_name="model_training") as run:
        # 训练模型
        data = load_iris()
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(data.data, data.target)

        # 记录模型到注册中心
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="iris_classifier"
        )

        run_id = run.info.run_id

    # 2. 获取模型版本
    model_version = client.get_latest_versions("iris_classifier")[0]
    print(f"模型版本: {model_version.version}")

    # 3. 转换模型阶段
    # 阶段: None -> Staging -> Production -> Archived
    client.transition_model_version_stage(
        name="iris_classifier",
        version=model_version.version,
        stage="Staging"
    )

    # 4. 添加模型标签
    client.set_model_version_tag(
        name="iris_classifier",
        version=model_version.version,
        key="validation_status",
        value="passed"
    )

    # 5. 添加模型描述
    client.update_model_version(
        name="iris_classifier",
        version=model_version.version,
        description="Iris分类模型，准确率95%"
    )

    # 6. 转换到生产环境
    client.transition_model_version_stage(
        name="iris_classifier",
        version=model_version.version,
        stage="Production"
    )

    # 7. 加载生产模型
    model_uri = "models:/iris_classifier/Production"
    production_model = mlflow.sklearn.load_model(model_uri)

    return production_model


def model_comparison():
    """模型比较和选择."""

    client = MlflowClient()

    # 获取所有版本
    versions = client.search_model_versions("name='iris_classifier'")

    # 比较指标
    results = []
    for version in versions:
        run = client.get_run(version.run_id)
        metrics = run.data.metrics
        results.append({
            "version": version.version,
            "stage": version.current_stage,
            "accuracy": metrics.get("accuracy", 0),
            "f1": metrics.get("f1", 0),
        })

    # 选择最佳模型
    best = max(results, key=lambda x: x["accuracy"])
    print(f"最佳模型: 版本{best['version']}, 准确率{best['accuracy']:.4f}")

    return best
```

#### 2.2 DVC (Data Version Control)

```yaml
# .dvc/config
[core]
    autostage = true
    remote = myremote
['remote "myremote"']
    url = s3://mybucket/dvcstore
    access_key_id = ${AWS_ACCESS_KEY_ID}
    secret_access_key = ${AWS_SECRET_ACCESS_KEY}
```

```bash
# DVC基本命令

# 初始化DVC
dvc init

# 跟踪数据文件
dvc add data/train.csv
dvc add data/test.csv

# 跟踪模型文件
dvc add models/model.pkl

# 推送数据到远程存储
dvc push

# 拉取数据
dvc pull

# 创建数据版本标签
git tag -a v1.0 -m "First model version"
git push origin v1.0

# 切换到特定版本
git checkout v1.0
dvc checkout

# 数据流水线
dvc run -n train \
    -d src/train.py \
    -d data/train.csv \
    -o models/model.pkl \
    python src/train.py

# 重现流水线
dvc repro

# 查看流水线
dvc dag
```

```python
# dvc_pipeline.py - DVC流水线Python接口
"""DVC流水线管理."""

import dvc.api
import pandas as pd
import joblib


def load_versioned_data(version: str = None):
    """加载版本化数据."""

    # 从特定版本加载数据
    with dvc.api.open(
        'data/train.csv',
        repo='https://github.com/user/repo',
        rev=version  # 可以是git标签、分支或commit
    ) as fd:
        df = pd.read_csv(fd)

    return df


def load_versioned_model(version: str = "v1.0"):
    """加载版本化模型."""

    # 下载模型文件
    model_path = dvc.api.get_url(
        'models/model.pkl',
        repo='.',
        rev=version
    )

    # 加载模型
    model = joblib.load(model_path)

    return model
```

---

### 3. 模型服务

#### 3.1 REST API (FastAPI + 模型)

```python
"""FastAPI模型服务完整示例."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import numpy as np
import joblib
import logging
from datetime import datetime
import asyncio
from contextlib import asynccontextmanager
import mlflow
import redis
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局模型存储
model_store = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理."""
    # 启动时加载模型
    logger.info("正在加载模型...")
    model_store["classifier"] = load_model()
    model_store["redis"] = redis.Redis.from_url(
        "redis://localhost:6379",
        decode_responses=True
    )
    logger.info("模型加载完成!")

    yield

    # 关闭时清理
    logger.info("正在关闭应用...")
    model_store.clear()


app = FastAPI(
    title="ML Model API",
    description="机器学习模型推理服务",
    version="1.0.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 数据模型 ====================

class PredictionRequest(BaseModel):
    """预测请求模型."""
    features: List[float] = Field(
        ...,
        min_items=4,
        max_items=4,
        description="特征向量"
    )
    model_version: Optional[str] = Field(
        default="latest",
        description="模型版本"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2],
                "model_version": "latest"
            }
        }


class BatchPredictionRequest(BaseModel):
    """批量预测请求模型."""
    instances: List[List[float]] = Field(
        ...,
        description="多个特征向量"
    )


class PredictionResponse(BaseModel):
    """预测响应模型."""
    prediction: int
    probability: List[float]
    model_version: str
    inference_time_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    """健康检查响应."""
    status: str
    model_loaded: bool
    timestamp: str


# ==================== 模型加载 ====================

def load_model(model_name: str = "iris_classifier", stage: str = "Production"):
    """加载MLflow模型."""
    mlflow.set_tracking_uri("http://localhost:5000")
    model_uri = f"models:/{model_name}/{stage}"
    model = mlflow.sklearn.load_model(model_uri)
    return model


# ==================== API端点 ====================

@app.get("/", response_model=Dict[str, str])
async def root():
    """根路径."""
    return {
        "message": "ML Model API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点."""
    return HealthResponse(
        status="healthy",
        model_loaded="classifier" in model_store,
        timestamp=datetime.now().isoformat()
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """单条预测端点."""
    start_time = datetime.now()

    try:
        model = model_store.get("classifier")
        if not model:
            raise HTTPException(status_code=503, detail="模型未加载")

        # 准备输入
        features = np.array(request.features).reshape(1, -1)

        # 预测
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()

        # 计算推理时间
        inference_time = (datetime.now() - start_time).total_seconds() * 1000

        # 记录到Redis
        redis_client = model_store.get("redis")
        if redis_client:
            redis_client.lpush(
                "predictions",
                json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    "prediction": int(prediction),
                    "inference_time_ms": inference_time
                })
            )

        return PredictionResponse(
            prediction=int(prediction),
            probability=probability,
            model_version=request.model_version,
            inference_time_ms=inference_time,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"预测错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    """批量预测端点."""
    start_time = datetime.now()

    try:
        model = model_store.get("classifier")
        if not model:
            raise HTTPException(status_code=503, detail="模型未加载")

        # 准备输入
        features = np.array(request.instances)

        # 批量预测
        predictions = model.predict(features).tolist()
        probabilities = model.predict_proba(features).tolist()

        inference_time = (datetime.now() - start_time).total_seconds() * 1000

        return {
            "predictions": predictions,
            "probabilities": probabilities,
            "count": len(predictions),
            "inference_time_ms": inference_time,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"批量预测错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model/info")
async def model_info():
    """获取模型信息."""
    model = model_store.get("classifier")
    if not model:
        raise HTTPException(status_code=503, detail="模型未加载")

    return {
        "model_type": type(model).__name__,
        "parameters": model.get_params(),
        "feature_importance": (
            model.feature_importances_.tolist()
            if hasattr(model, 'feature_importances_')
            else None
        )
    }


@app.post("/model/reload")
async def reload_model(background_tasks: BackgroundTasks):
    """重新加载模型."""
    background_tasks.add_task(_reload_model_task)
    return {"message": "模型重新加载中..."}


async def _reload_model_task():
    """后台重新加载模型任务."""
    try:
        model_store["classifier"] = load_model()
        logger.info("模型重新加载完成")
    except Exception as e:
        logger.error(f"模型重新加载失败: {str(e)}")


# ==================== 中间件 ====================

@app.middleware("http")
async def log_requests(request, call_next):
    """请求日志中间件."""
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()

    logger.info(
        f"{request.method} {request.url.path} - "
        f"{response.status_code} - {duration:.3f}s"
    )

    return response


# ==================== 启动 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 3.2 批处理预测

```python
"""批处理预测服务."""

import pandas as pd
import numpy as np
from typing import Iterator
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchPredictor:
    """批处理预测器."""

    def __init__(self, model, batch_size: int = 1000, n_workers: int = None):
        """
        初始化批处理预测器.

        Args:
            model: 训练好的模型
            batch_size: 批处理大小
            n_workers: 并行工作进程数
        """
        self.model = model
        self.batch_size = batch_size
        self.n_workers = n_workers or mp.cpu_count()

    def predict_dataframe(
        self,
        df: pd.DataFrame,
        feature_columns: list,
        output_column: str = "prediction"
    ) -> pd.DataFrame:
        """对DataFrame进行批量预测."""

        results = []
        total_rows = len(df)

        # 分批处理
        for i in range(0, total_rows, self.batch_size):
            batch = df.iloc[i:i + self.batch_size]
            features = batch[feature_columns].values

            predictions = self.model.predict(features)

            batch_result = batch.copy()
            batch_result[output_column] = predictions

            results.append(batch_result)

            if (i // self.batch_size) % 10 == 0:
                logger.info(f"已处理 {i}/{total_rows} 行")

        return pd.concat(results, ignore_index=True)

    def predict_file(
        self,
        input_path: str,
        output_path: str,
        feature_columns: list,
        chunksize: int = None
    ):
        """对大文件进行流式预测."""

        chunksize = chunksize or self.batch_size

        # 读取CSV分块
        reader = pd.read_csv(input_path, chunksize=chunksize)

        first_chunk = True
        for i, chunk in enumerate(reader):
            # 预测
            features = chunk[feature_columns].values
            predictions = self.model.predict(features)

            # 添加预测列
            chunk['prediction'] = predictions

            # 写入结果
            mode = 'w' if first_chunk else 'a'
            header = first_chunk

            chunk.to_csv(
                output_path,
                mode=mode,
                header=header,
                index=False
            )

            first_chunk = False
            logger.info(f"已处理第 {i+1} 块")

    def predict_parallel(
        self,
        data: np.ndarray,
        n_workers: int = None
    ) -> np.ndarray:
        """并行预测."""

        n_workers = n_workers or self.n_workers

        # 分割数据
        chunks = np.array_split(data, n_workers)

        # 并行处理
        with ProcessPoolExecutor(max_workers=n_workers) as executor:
            futures = {
                executor.submit(self._predict_chunk, chunk): i
                for i, chunk in enumerate(chunks)
            }

            results = [None] * n_workers
            for future in as_completed(futures):
                i = futures[future]
                results[i] = future.result()

        # 合并结果
        return np.concatenate(results)

    def _predict_chunk(self, chunk: np.ndarray) -> np.ndarray:
        """预测单个数据块."""
        return self.model.predict(chunk)


# 使用示例
def batch_prediction_example():
    """批处理预测示例."""
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier

    # 训练模型
    data = load_iris()
    model = RandomForestClassifier(n_estimators=100)
    model.fit(data.data, data.target)

    # 创建批处理预测器
    predictor = BatchPredictor(model, batch_size=100)

    # 创建测试数据
    test_df = pd.DataFrame(
        np.random.randn(10000, 4),
        columns=['f1', 'f2', 'f3', 'f4']
    )

    # 批量预测
    results = predictor.predict_dataframe(
        test_df,
        feature_columns=['f1', 'f2', 'f3', 'f4'],
        output_column='prediction'
    )

    print(f"预测结果:\n{results.head()}")

    return results
```

#### 3.3 模型缓存

```python
"""模型缓存管理."""

import functools
import hashlib
import pickle
import time
from typing import Any, Callable
import redis
import diskcache
from pathlib import Path


class ModelCache:
    """模型预测缓存管理器."""

    def __init__(
        self,
        redis_url: str = None,
        disk_cache_dir: str = "./cache",
        ttl: int = 3600
    ):
        """
        初始化缓存管理器.

        Args:
            redis_url: Redis连接URL
            disk_cache_dir: 磁盘缓存目录
            ttl: 缓存过期时间(秒)
        """
        self.ttl = ttl

        # Redis缓存
        self.redis_client = None
        if redis_url:
            try:
                self.redis_client = redis.Redis.from_url(redis_url)
                self.redis_client.ping()
            except redis.ConnectionError:
                pass

        # 磁盘缓存
        self.disk_cache = diskcache.Cache(disk_cache_dir)

    def _make_key(self, data: Any) -> str:
        """生成缓存键."""
        serialized = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        return hashlib.md5(serialized).hexdigest()

    def get(self, key: str) -> Any:
        """获取缓存."""
        # 先查Redis
        if self.redis_client:
            value = self.redis_client.get(key)
            if value:
                return pickle.loads(value)

        # 再查磁盘
        return self.disk_cache.get(key)

    def set(self, key: str, value: Any, ttl: int = None):
        """设置缓存."""
        ttl = ttl or self.ttl
        serialized = pickle.dumps(value)

        # 写入Redis
        if self.redis_client:
            self.redis_client.setex(key, ttl, serialized)

        # 写入磁盘
        self.disk_cache.set(key, value, expire=ttl)

    def cached_predict(
        self,
        predict_func: Callable,
        cache_key_prefix: str = "pred"
    ):
        """预测结果缓存装饰器."""

        @functools.wraps(predict_func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_data = {
                'args': args[1:],  # 排除self
                'kwargs': kwargs
            }
            key = f"{cache_key_prefix}:{self._make_key(cache_data)}"

            # 检查缓存
            cached = self.get(key)
            if cached is not None:
                return cached

            # 执行预测
            result = predict_func(*args, **kwargs)

            # 写入缓存
            self.set(key, result)

            return result

        return wrapper


# 使用示例
class CachedModel:
    """带缓存的模型类."""

    def __init__(self, model):
        self.model = model
        self.cache = ModelCache()

    @ModelCache.cached_predict
    def predict(self, features):
        """带缓存的预测."""
        time.sleep(0.1)  # 模拟耗时操作
        return self.model.predict([features])[0]


# LRU缓存装饰器
def lru_cached_predict(maxsize: int = 128):
    """LRU缓存装饰器."""

    def decorator(func: Callable) -> Callable:
        cached_func = functools.lru_cache(maxsize=maxsize)(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 将numpy数组转为元组以支持缓存
            cacheable_args = []
            for arg in args:
                if isinstance(arg, np.ndarray):
                    cacheable_args.append(tuple(arg.flatten()))
                else:
                    cacheable_args.append(arg)

            return cached_func(*cacheable_args, **kwargs)

        return wrapper

    return decorator
```

---

### 4. 模型监控

#### 4.1 性能监控

```python
"""模型性能监控系统."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import logging
from dataclasses import dataclass, asdict
from collections import deque
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PredictionMetrics:
    """预测指标."""
    timestamp: str
    latency_ms: float
    prediction: Any
    confidence: Optional[float] = None
    error: Optional[str] = None


class ModelMonitor:
    """模型监控器."""

    def __init__(self, window_size: int = 1000):
        """
        初始化监控器.

        Args:
            window_size: 滑动窗口大小
        """
        self.window_size = window_size
        self.predictions = deque(maxlen=window_size)
        self.latencies = deque(maxlen=window_size)
        self.errors = deque(maxlen=window_size)

    def log_prediction(
        self,
        latency_ms: float,
        prediction: Any,
        confidence: float = None,
        error: str = None
    ):
        """记录预测."""
        metric = PredictionMetrics(
            timestamp=datetime.now().isoformat(),
            latency_ms=latency_ms,
            prediction=prediction,
            confidence=confidence,
            error=error
        )

        self.predictions.append(metric)

        if error:
            self.errors.append(metric)
        else:
            self.latencies.append(latency_ms)

    def get_latency_stats(self) -> Dict:
        """获取延迟统计."""
        if not self.latencies:
            return {}

        latencies = list(self.latencies)

        return {
            "count": len(latencies),
            "mean_ms": statistics.mean(latencies),
            "median_ms": statistics.median(latencies),
            "std_ms": statistics.stdev(latencies) if len(latencies) > 1 else 0,
            "min_ms": min(latencies),
            "max_ms": max(latencies),
            "p95_ms": np.percentile(latencies, 95),
            "p99_ms": np.percentile(latencies, 99),
        }

    def get_error_stats(self) -> Dict:
        """获取错误统计."""
        total = len(self.predictions)
        errors = len(self.errors)

        return {
            "total_predictions": total,
            "error_count": errors,
            "error_rate": errors / total if total > 0 else 0,
            "recent_errors": [asdict(e) for e in list(self.errors)[-10:]]
        }

    def get_summary(self) -> Dict:
        """获取监控摘要."""
        return {
            "latency": self.get_latency_stats(),
            "errors": self.get_error_stats(),
            "window_size": self.window_size,
            "timestamp": datetime.now().isoformat()
        }

    def check_alerts(self) -> List[Dict]:
        """检查告警条件."""
        alerts = []

        latency_stats = self.get_latency_stats()
        if latency_stats.get("p95_ms", 0) > 1000:
            alerts.append({
                "level": "warning",
                "metric": "latency_p95",
                "message": f"P95延迟超过1000ms: {latency_stats['p95_ms']:.2f}ms",
                "timestamp": datetime.now().isoformat()
            })

        error_stats = self.get_error_stats()
        if error_stats.get("error_rate", 0) > 0.05:
            alerts.append({
                "level": "critical",
                "metric": "error_rate",
                "message": f"错误率超过5%: {error_stats['error_rate']:.2%}",
                "timestamp": datetime.now().isoformat()
            })

        return alerts


# Prometheus指标导出
class PrometheusExporter:
    """Prometheus指标导出器."""

    def __init__(self):
        try:
            from prometheus_client import Counter, Histogram, Gauge, start_http_server

            self.prediction_counter = Counter(
                'model_predictions_total',
                'Total predictions',
                ['model_version', 'status']
            )

            self.latency_histogram = Histogram(
                'model_prediction_latency_seconds',
                'Prediction latency',
                ['model_version']
            )

            self.confidence_gauge = Gauge(
                'model_prediction_confidence',
                'Prediction confidence',
                ['model_version']
            )

            # 启动指标服务器
            start_http_server(9090)

        except ImportError:
            logger.warning("prometheus_client not installed")
            self.prediction_counter = None

    def log_prediction(
        self,
        model_version: str,
        latency_s: float,
        confidence: float = None,
        success: bool = True
    ):
        """记录预测指标."""
        if self.prediction_counter is None:
            return

        status = "success" if success else "error"
        self.prediction_counter.labels(
            model_version=model_version,
            status=status
        ).inc()

        self.latency_histogram.labels(
            model_version=model_version
        ).observe(latency_s)

        if confidence is not None:
            self.confidence_gauge.labels(
                model_version=model_version
            ).set(confidence)
```

#### 4.2 数据漂移检测

```python
"""数据漂移检测系统."""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DriftDetector:
    """数据漂移检测器."""

    def __init__(self, reference_data: pd.DataFrame, threshold: float = 0.05):
        """
        初始化漂移检测器.

        Args:
            reference_data: 参考数据（训练数据）
            threshold: 统计检验阈值
        """
        self.reference_data = reference_data
        self.threshold = threshold
        self.reference_stats = self._compute_stats(reference_data)

    def _compute_stats(self, data: pd.DataFrame) -> Dict:
        """计算数据统计信息."""
        stats_dict = {}

        for column in data.select_dtypes(include=[np.number]).columns:
            stats_dict[column] = {
                'mean': data[column].mean(),
                'std': data[column].std(),
                'min': data[column].min(),
                'max': data[column].max(),
                'median': data[column].median(),
                'q25': data[column].quantile(0.25),
                'q75': data[column].quantile(0.75),
            }

        return stats_dict

    def ks_test(self, current_data: pd.DataFrame, column: str) -> Tuple[float, float]:
        """
        Kolmogorov-Smirnov检验.

        Returns:
            (统计量, p值)
        """
        reference = self.reference_data[column].dropna()
        current = current_data[column].dropna()

        statistic, p_value = stats.ks_2samp(reference, current)
        return statistic, p_value

    def chi2_test(self, current_data: pd.DataFrame, column: str) -> Tuple[float, float]:
        """
        卡方检验（分类变量）.

        Returns:
            (统计量, p值)
        """
        reference_counts = self.reference_data[column].value_counts()
        current_counts = current_data[column].value_counts()

        # 对齐类别
        all_categories = set(reference_counts.index) | set(current_counts.index)
        reference_freq = [reference_counts.get(cat, 0) for cat in all_categories]
        current_freq = [current_counts.get(cat, 0) for cat in all_categories]

        statistic, p_value = stats.chisquare(current_freq, reference_freq)
        return statistic, p_value

    def wasserstein_distance(
        self,
        current_data: pd.DataFrame,
        column: str
    ) -> float:
        """计算Wasserstein距离."""
        from scipy.stats import wasserstein_distance as wd

        reference = self.reference_data[column].dropna()
        current = current_data[column].dropna()

        return wd(reference, current)

    def detect_drift(self, current_data: pd.DataFrame) -> Dict:
        """
        检测数据漂移.

        Returns:
            漂移检测报告
        """
        drift_report = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'drift_detected': False,
            'features': {}
        }

        for column in self.reference_data.columns:
            if column not in current_data.columns:
                continue

            feature_report = {
                'drift_detected': False,
                'tests': {}
            }

            # 数值变量
            if self.reference_data[column].dtype in ['int64', 'float64']:
                # KS检验
                ks_stat, ks_p = self.ks_test(current_data, column)
                feature_report['tests']['ks_test'] = {
                    'statistic': float(ks_stat),
                    'p_value': float(ks_p),
                    'drift_detected': ks_p < self.threshold
                }

                # Wasserstein距离
                w_dist = self.wasserstein_distance(current_data, column)
                feature_report['tests']['wasserstein_distance'] = float(w_dist)

                if ks_p < self.threshold:
                    feature_report['drift_detected'] = True
                    drift_report['drift_detected'] = True

            # 分类变量
            else:
                chi2_stat, chi2_p = self.chi2_test(current_data, column)
                feature_report['tests']['chi2_test'] = {
                    'statistic': float(chi2_stat),
                    'p_value': float(chi2_p),
                    'drift_detected': chi2_p < self.threshold
                }

                if chi2_p < self.threshold:
                    feature_report['drift_detected'] = True
                    drift_report['drift_detected'] = True

            drift_report['features'][column] = feature_report

        return drift_report

    def get_drift_summary(self, drift_report: Dict) -> str:
        """获取漂移摘要."""
        lines = ["数据漂移检测报告", "=" * 50]

        if not drift_report['drift_detected']:
            lines.append("✅ 未检测到数据漂移")
        else:
            lines.append("⚠️ 检测到数据漂移!")
            lines.append("")

            for feature, report in drift_report['features'].items():
                if report['drift_detected']:
                    lines.append(f"特征: {feature}")
                    for test_name, test_result in report['tests'].items():
                        if 'p_value' in test_result:
                            lines.append(
                                f"  {test_name}: p={test_result['p_value']:.4f} "
                                f"({'漂移' if test_result['drift_detected'] else '正常'})"
                            )
                    lines.append("")

        return "\n".join(lines)


# 概念漂移检测
class ConceptDriftDetector:
    """概念漂移检测器（基于模型性能）."""

    def __init__(
        self,
        window_size: int = 100,
        warning_threshold: float = 0.05,
        drift_threshold: float = 0.1
    ):
        """
        初始化概念漂移检测器.

        Args:
            window_size: 滑动窗口大小
            warning_threshold: 警告阈值
            drift_threshold: 漂移阈值
        """
        self.window_size = window_size
        self.warning_threshold = warning_threshold
        self.drift_threshold = drift_threshold

        self.reference_accuracy = None
        self.accuracy_window = []

    def set_reference(self, accuracy: float):
        """设置参考准确率."""
        self.reference_accuracy = accuracy

    def update(self, accuracy: float) -> str:
        """
        更新并检测漂移.

        Returns:
            'normal', 'warning', 或 'drift'
        """
        self.accuracy_window.append(accuracy)

        if len(self.accuracy_window) > self.window_size:
            self.accuracy_window.pop(0)

        if self.reference_accuracy is None or len(self.accuracy_window) < 10:
            return 'normal'

        # 计算当前窗口平均准确率
        current_accuracy = np.mean(self.accuracy_window)
        accuracy_drop = self.reference_accuracy - current_accuracy

        if accuracy_drop > self.drift_threshold:
            return 'drift'
        elif accuracy_drop > self.warning_threshold:
            return 'warning'

        return 'normal'


# 使用示例
def drift_detection_example():
    """漂移检测示例."""
    from sklearn.datasets import load_iris

    # 加载数据
    data = load_iris()
    df = pd.DataFrame(data.data, columns=data.feature_names)

    # 创建漂移检测器
    detector = DriftDetector(df, threshold=0.05)

    # 模拟漂移数据（添加噪声）
    drifted_df = df.copy()
    for col in df.columns:
        drifted_df[col] = df[col] + np.random.normal(0, 0.5, len(df))

    # 检测漂移
    report = detector.detect_drift(drifted_df)

    # 打印摘要
    print(detector.get_drift_summary(report))

    return report
```

---

## 第六部分：AI工程化

### 1. LLM应用开发

#### 1.1 OpenAI API

```python
"""OpenAI API完整使用示例."""

import os
from typing import List, Dict, Optional, Generator
from dataclasses import dataclass
import openai
from openai import OpenAI
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@dataclass
class LLMResponse:
    """LLM响应数据结构."""
    content: str
    model: str
    usage: Dict
    finish_reason: str
    latency_ms: float


class OpenAIClient:
    """OpenAI客户端封装."""

    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        timeout: float = 30.0
    ):
        """
        初始化OpenAI客户端.

        Args:
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            timeout: 超时时间
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=timeout
        )

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> LLMResponse:
        """
        聊天完成.

        Args:
            messages: 消息列表
            tools: 工具定义
            **kwargs: 额外参数

        Returns:
            LLM响应
        """
        import time
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                tools=tools,
                **{k: v for k, v in kwargs.items() if k not in ['temperature', 'max_tokens']}
            )

            latency = (time.time() - start_time) * 1000

            return LLMResponse(
                content=response.choices[0].message.content or "",
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                finish_reason=response.choices[0].finish_reason,
                latency_ms=latency
            )

        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            raise

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Generator[str, None, None]:
        """
        流式聊天完成.

        Args:
            messages: 消息列表
            **kwargs: 额外参数

        Yields:
            内容片段
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"流式API调用失败: {str(e)}")
            raise

    def simple_chat(self, prompt: str, system_prompt: str = None) -> str:
        """简单聊天."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.chat(messages)
        return response.content

    def function_call(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict],
        tool_choice: str = "auto"
    ) -> Dict:
        """
        函数调用.

        Args:
            messages: 消息列表
            tools: 工具定义
            tool_choice: 工具选择策略

        Returns:
            函数调用结果
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice
        )

        message = response.choices[0].message

        if message.tool_calls:
            return {
                "type": "tool_call",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "function": {
                            "name": tc.function.name,
                            "arguments": json.loads(tc.function.arguments)
                        }
                    }
                    for tc in message.tool_calls
                ]
            }

        return {
            "type": "content",
            "content": message.content
        }


# 工具定义示例
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位"
                }
            },
            "required": ["city"]
        }
    }
}


def get_weather(city: str, unit: str = "celsius") -> Dict:
    """获取天气（模拟）."""
    # 实际实现会调用天气API
    return {
        "city": city,
        "temperature": 25 if unit == "celsius" else 77,
        "condition": "sunny",
        "unit": unit
    }


# 使用示例
def function_calling_example():
    """函数调用示例."""
    llm = OpenAIClient(model="gpt-4")

    messages = [
        {"role": "user", "content": "北京今天天气怎么样？"}
    ]

    result = llm.function_call(messages, [weather_tool])

    if result["type"] == "tool_call":
        for tool_call in result["tool_calls"]:
            if tool_call["function"]["name"] == "get_weather":
                args = tool_call["function"]["arguments"]
                weather = get_weather(args["city"], args.get("unit", "celsius"))
                print(f"天气结果: {weather}")


# 异步客户端
class AsyncOpenAIClient:
    """异步OpenAI客户端."""

    def __init__(self, model: str = "gpt-4"):
        from openai import AsyncOpenAI
        self.model = model
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """异步聊天完成."""
        import time
        start_time = time.time()

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )

        latency = (time.time() - start_time) * 1000

        return LLMResponse(
            content=response.choices[0].message.content or "",
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            finish_reason=response.choices[0].finish_reason,
            latency_ms=latency
        )
```

#### 1.2 LangChain概述

```python
"""LangChain核心概念示例."""

from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.schema import Document
import os


# ==================== 基础组件 ====================

def basic_components():
    """LangChain基础组件."""

    # 1. Prompt Template
    template = """
    你是一个{role}。请用{tone}的语气回答以下问题：

    问题：{question}

    回答：
    """

    prompt = PromptTemplate(
        input_variables=["role", "tone", "question"],
        template=template
    )

    formatted_prompt = prompt.format(
        role="技术专家",
        tone="专业",
        question="什么是机器学习？"
    )
    print(formatted_prompt)

    # 2. LLM
    llm = OpenAI(temperature=0.7)

    # 3. LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.predict(
        role="技术专家",
        tone="专业",
        question="什么是深度学习？"
    )
    print(result)


# ==================== 记忆组件 ====================

def memory_example():
    """记忆组件示例."""

    from langchain.chains import ConversationChain

    # 创建记忆
    memory = ConversationBufferMemory()

    # 创建对话链
    conversation = ConversationChain(
        llm=OpenAI(temperature=0.7),
        memory=memory,
        verbose=True
    )

    # 多轮对话
    print(conversation.predict(input="你好！我叫张三。"))
    print(conversation.predict(input="我叫什么名字？"))
    print(conversation.predict(input="今天天气不错。"))

    # 查看记忆
    print("\n对话历史:")
    print(memory.buffer)


# ==================== 文档处理 ====================

def document_processing():
    """文档处理示例."""

    # 1. 文本分割
    text = """
    这是第一段很长的文本。它包含了很多信息，需要被正确地分割成小块以便于处理。

    这是第二段文本。每段文本都应该被单独处理，以保持语义的完整性。

    这是第三段文本。分割策略对于RAG系统的性能至关重要。
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", " ", ""]
    )

    chunks = splitter.split_text(text)
    print(f"分割成 {len(chunks)} 块")
    for i, chunk in enumerate(chunks):
        print(f"块 {i+1}: {chunk[:50]}...")

    # 2. 文档加载
    # loader = TextLoader("document.txt")
    # documents = loader.load()

    # 3. 向量化
    embeddings = OpenAIEmbeddings()

    # 创建向量存储
    # db = Chroma.from_documents(documents, embeddings)

    # 相似性搜索
    # results = db.similarity_search("查询文本", k=3)


# ==================== Agent ====================

def agent_example():
    """Agent示例."""

    from langchain.tools import tool

    # 定义工具
    @tool
def search(query: str) -> str:
        """搜索信息."""
        return f"搜索结果: {query}"

    @tool
def calculator(expression: str) -> str:
        """计算表达式."""
        try:
            return str(eval(expression))
        except:
            return "计算错误"

    tools = [search, calculator]

    # 创建Agent
    prompt = """
    尽可能回答以下问题。你可以使用以下工具：

    {tools}

    使用以下格式：

    问题：你需要回答的问题
    思考：你应该如何思考
    行动：要采取的行动（应该是以下之一：{tool_names}）
    行动输入：行动的输入
    观察：行动的结果
    ...（这个思考/行动/行动输入/观察可以重复N次）
    思考：我现在知道最终答案
    最终答案：原始问题的最终答案

    开始！

    问题：{input}
    思考：{agent_scratchpad}
    """

    # agent = create_react_agent(OpenAI(temperature=0), tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # agent_executor.run("计算 25 * 4 + 10")


# ==================== 链式组合 ====================

def chain_composition():
    """链式组合示例."""

    from langchain.chains import SimpleSequentialChain, LLMChain

    # 第一个链：生成大纲
    outline_template = """
    为主题 "{topic}" 生成一个文章大纲。
    大纲：
    """
    outline_prompt = PromptTemplate(
        input_variables=["topic"],
        template=outline_template
    )
    outline_chain = LLMChain(
        llm=OpenAI(temperature=0.7),
        prompt=outline_prompt,
        output_key="outline"
    )

    # 第二个链：根据大纲写文章
    article_template = """
    根据以下大纲写一篇详细的文章：
    {outline}

    文章：
    """
    article_prompt = PromptTemplate(
        input_variables=["outline"],
        template=article_template
    )
    article_chain = LLMChain(
        llm=OpenAI(temperature=0.7),
        prompt=article_prompt,
        output_key="article"
    )

    # 组合链
    overall_chain = SimpleSequentialChain(
        chains=[outline_chain, article_chain],
        verbose=True
    )

    # 运行
    # result = overall_chain.run("人工智能的未来")
    # print(result)
```

#### 1.3 Prompt工程

```python
"""Prompt工程最佳实践."""

from dataclasses import dataclass
from typing import List, Dict, Optional
import json


@dataclass
class PromptTemplate:
    """Prompt模板."""
    system: str
    user: str
    examples: List[Dict[str, str]] = None

    def format(self, **kwargs) -> List[Dict[str, str]]:
        """格式化prompt."""
        messages = []

        # 系统提示
        if self.system:
            messages.append({
                "role": "system",
                "content": self.system.format(**kwargs)
            })

        # 示例
        if self.examples:
            for example in self.examples:
                messages.append({
                    "role": "user",
                    "content": example["input"]
                })
                messages.append({
                    "role": "assistant",
                    "content": example["output"]
                })

        # 用户提示
        messages.append({
            "role": "user",
            "content": self.user.format(**kwargs)
        })

        return messages


# ==================== Prompt模板库 ====================

class PromptLibrary:
    """Prompt模板库."""

    # 文本分类
    CLASSIFICATION = PromptTemplate(
        system="你是一个文本分类专家。请将文本分类到给定的类别中。",
        user="""请将以下文本分类到类别 [{categories}] 中：

文本：{text}

请以JSON格式输出：{{"category": "类别", "confidence": 0.95}}
""",
        examples=[
            {
                "input": "文本：这部电影太精彩了！演员表演出色，剧情扣人心弦。\n类别：[正面, 负面, 中性]",
                "output": '{"category": "正面", "confidence": 0.98}'
            }
        ]
    )

    # 信息提取
    EXTRACTION = PromptTemplate(
        system="你是一个信息提取专家。请从文本中提取结构化信息。",
        user="""请从以下文本中提取 {fields} 信息：

文本：{text}

请以JSON格式输出提取的信息。
"""
    )

    # 代码生成
    CODE_GENERATION = PromptTemplate(
        system="你是一个专业的程序员。请根据需求编写高质量、可维护的代码。",
        user="""请用 {language} 编写代码实现以下功能：

需求：{requirement}

要求：
{constraints}

请提供完整的代码，包括必要的注释和错误处理。
""",
        examples=[
            {
                "input": "请用Python编写一个函数，计算斐波那契数列的第n项。",
                "output": '''```python
def fibonacci(n: int) -> int:
    """计算斐波那契数列第n项."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```'''
            }
        ]
    )

    # 对话总结
    SUMMARIZATION = PromptTemplate(
        system="你是一个对话总结专家。请简洁地总结对话的关键信息。",
        user="""请总结以下对话：

{conversation}

请用2-3句话总结主要内容和结论。
"""
    )

    # 代码审查
    CODE_REVIEW = PromptTemplate(
        system="你是一个资深代码审查专家。请审查代码并提供建设性反馈。",
        user="""请审查以下 {language} 代码：

```

{code}

```

请从以下方面进行分析：
1. 代码质量和可读性
2. 潜在bug或问题
3. 性能优化建议
4. 最佳实践建议

请以结构化格式输出审查结果。
"""
    )


# ==================== Prompt优化技术 ====================

class PromptOptimizer:
    """Prompt优化器."""

    @staticmethod
    def add_context(prompt: str, context: str) -> str:
        """添加上下文."""
        return f"背景信息：\n{context}\n\n{prompt}"

    @staticmethod
    def add_constraints(prompt: str, constraints: List[str]) -> str:
        """添加约束条件."""
        constraint_text = "\n".join(f"- {c}" for c in constraints)
        return f"{prompt}\n\n约束条件：\n{constraint_text}"

    @staticmethod
    def add_output_format(prompt: str, format_spec: str) -> str:
        """添加输出格式要求."""
        return f"{prompt}\n\n输出格式：\n{format_spec}"

    @staticmethod
    def chain_of_thought(prompt: str) -> str:
        """添加思维链提示."""
        return f"{prompt}\n\n请逐步思考并解释你的推理过程。"

    @staticmethod
    def few_shot(prompt: str, examples: List[Dict[str, str]]) -> str:
        """添加少样本示例."""
        example_text = "\n\n".join(
            f"示例 {i+1}:\n输入：{ex['input']}\n输出：{ex['output']}"
            for i, ex in enumerate(examples)
        )
        return f"{example_text}\n\n现在请回答：\n{prompt}"


# ==================== 使用示例 ====================

def prompt_engineering_examples():
    """Prompt工程示例."""

    # 1. 文本分类
    classification_prompt = PromptLibrary.CLASSIFICATION.format(
        categories="正面, 负面, 中性",
        text="这家餐厅的服务太差了，等了一个小时才上菜。"
    )
    print("分类Prompt:")
    for msg in classification_prompt:
        print(f"{msg['role']}: {msg['content'][:100]}...")

    # 2. 代码生成
    code_prompt = PromptLibrary.CODE_GENERATION.format(
        language="Python",
        requirement="实现一个 LRU 缓存",
        constraints="- 使用字典和双向链表\n- 时间复杂度 O(1)\n- 支持泛型"
    )
    print("\n代码生成Prompt:")
    for msg in code_prompt:
        print(f"{msg['role']}: {msg['content'][:100]}...")


# ==================== Prompt测试框架 ====================

class PromptTester:
    """Prompt测试框架."""

    def __init__(self, llm_client):
        self.llm = llm_client
        self.results = []

    def test_prompt(
        self,
        name: str,
        prompt: List[Dict[str, str]],
        expected_keywords: List[str] = None,
        validate_json: bool = False
    ) -> Dict:
        """测试单个prompt."""

        response = self.llm.chat(prompt)
        content = response.content

        # 验证
        checks = {
            "has_content": len(content) > 0,
            "keyword_match": True,
            "valid_json": True
        }

        if expected_keywords:
            checks["keyword_match"] = all(
                kw.lower() in content.lower()
                for kw in expected_keywords
            )

        if validate_json:
            try:
                json.loads(content)
            except json.JSONDecodeError:
                checks["valid_json"] = False

        result = {
            "name": name,
            "passed": all(checks.values()),
            "checks": checks,
            "response": content[:200],
            "latency_ms": response.latency_ms
        }

        self.results.append(result)
        return result

    def get_report(self) -> str:
        """生成测试报告."""
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)

        lines = [
            "Prompt测试报告",
            "=" * 50,
            f"总计: {total}, 通过: {passed}, 失败: {total - passed}",
            ""
        ]

        for result in self.results:
            status = "✅" if result["passed"] else "❌"
            lines.append(f"{status} {result['name']}")
            if not result["passed"]:
                for check, passed in result["checks"].items():
                    if not passed:
                        lines.append(f"   - {check}: 失败")

        return "\n".join(lines)
```

---

### 2. RAG（检索增强生成）

#### 2.1 概念定义

**RAG (Retrieval-Augmented Generation)** 是一种结合信息检索和文本生成的技术。它通过从外部知识库检索相关信息，然后将其与原始查询一起提供给语言模型，从而生成更准确、更相关的回答。

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAG 架构图                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   用户查询   │───►│   检索模块   │───►│  相关文档   │         │
│  └─────────────┘    └──────┬──────┘    └──────┬──────┘         │
│                            │                   │               │
│                            │    ┌──────────────┘               │
│                            │    │                              │
│                            ▼    ▼                              │
│                     ┌─────────────────┐                        │
│                     │   上下文构建     │                        │
│                     │  [查询 + 文档]   │                        │
│                     └────────┬────────┘                        │
│                              │                                  │
│                              ▼                                  │
│                     ┌─────────────────┐                        │
│                     │   LLM 生成      │                        │
│                     │   最终回答      │                        │
│                     └─────────────────┘                        │
│                                                                 │
│  核心组件：                                                     │
│  1. 文档加载器 - 加载各种格式的文档                              │
│  2. 文本分割器 - 将长文档分割成小块                              │
│  3. 嵌入模型 - 将文本转换为向量                                  │
│  4. 向量数据库 - 存储和检索向量                                  │
│  5. 重排序器 - 对检索结果进行精排                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.2 Python实现

```python
"""RAG系统完整实现."""

import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from openai import OpenAI
import chromadb
from chromadb.config import Settings
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Document:
    """文档数据结构."""
    id: str
    content: str
    metadata: Dict
    embedding: Optional[List[float]] = None


@dataclass
class SearchResult:
    """搜索结果."""
    document: Document
    score: float


class EmbeddingModel:
    """嵌入模型封装."""

    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed(self, texts: List[str]) -> List[List[float]]:
        """生成文本嵌入."""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> List[float]:
        """生成查询嵌入."""
        return self.embed([text])[0]


class VectorStore:
    """向量存储封装."""

    def __init__(self, collection_name: str = "documents", persist_dir: str = "./chroma_db"):
        """初始化向量存储."""
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir
        ))

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Document]) -> None:
        """添加文档."""
        self.collection.add(
            ids=[doc.id for doc in documents],
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            embeddings=[doc.embedding for doc in documents if doc.embedding]
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Dict = None
    ) -> List[SearchResult]:
        """搜索相似文档."""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict
        )

        search_results = []
        for i in range(len(results['ids'][0])):
            doc = Document(
                id=results['ids'][0][i],
                content=results['documents'][0][i],
                metadata=results['metadatas'][0][i],
                embedding=None
            )
            search_results.append(SearchResult(
                document=doc,
                score=results['distances'][0][i]
            ))

        return search_results

    def delete(self, doc_id: str) -> None:
        """删除文档."""
        self.collection.delete(ids=[doc_id])


class TextSplitter:
    """文本分割器."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: List[str] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", "。", " ", ""]

    def split(self, text: str) -> List[str]:
        """分割文本."""
        chunks = []
        current_chunk = ""

        # 简单实现 - 按字符数分割
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i:i + self.chunk_size]
            if chunk:
                chunks.append(chunk)

        return chunks

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """分割文档."""
        split_docs = []

        for doc in documents:
            chunks = self.split(doc.content)
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc.id}_chunk_{i}"
                split_docs.append(Document(
                    id=chunk_id,
                    content=chunk,
                    metadata={**doc.metadata, "parent_id": doc.id, "chunk_index": i}
                ))

        return split_docs


class RAGSystem:
    """RAG系统主类."""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4",
        chunk_size: int = 500,
        top_k: int = 5
    ):
        """
        初始化RAG系统.

        Args:
            embedding_model: 嵌入模型名称
            llm_model: LLM模型名称
            chunk_size: 文本块大小
            top_k: 检索文档数
        """
        self.embedding_model = EmbeddingModel(embedding_model)
        self.vector_store = VectorStore()
        self.text_splitter = TextSplitter(chunk_size=chunk_size)
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.llm_model = llm_model
        self.top_k = top_k

    def add_documents(self, documents: List[Document]) -> None:
        """添加文档到知识库."""
        logger.info(f"正在处理 {len(documents)} 个文档...")

        # 分割文档
        split_docs = self.text_splitter.split_documents(documents)
        logger.info(f"分割为 {len(split_docs)} 个文本块")

        # 生成嵌入
        texts = [doc.content for doc in split_docs]
        embeddings = self.embedding_model.embed(texts)

        for doc, embedding in zip(split_docs, embeddings):
            doc.embedding = embedding

        # 存储到向量数据库
        self.vector_store.add_documents(split_docs)
        logger.info("文档添加完成")

    def query(
        self,
        query: str,
        system_prompt: str = None,
        filter_dict: Dict = None
    ) -> Dict:
        """
        查询RAG系统.

        Args:
            query: 用户查询
            system_prompt: 系统提示
            filter_dict: 过滤条件

        Returns:
            包含回答和来源的字典
        """
        # 1. 生成查询嵌入
        query_embedding = self.embedding_model.embed_query(query)

        # 2. 检索相关文档
        search_results = self.vector_store.search(
            query_embedding,
            top_k=self.top_k,
            filter_dict=filter_dict
        )

        # 3. 构建上下文
        context = self._build_context(search_results)

        # 4. 生成回答
        answer = self._generate_answer(query, context, system_prompt)

        return {
            "query": query,
            "answer": answer,
            "sources": [
                {
                    "content": r.document.content[:200],
                    "metadata": r.document.metadata,
                    "score": r.score
                }
                for r in search_results
            ]
        }

    def _build_context(self, search_results: List[SearchResult]) -> str:
        """构建上下文."""
        context_parts = []
        for i, result in enumerate(search_results):
            context_parts.append(
                f"[文档 {i+1}]\n{result.document.content}\n"
            )
        return "\n".join(context_parts)

    def _generate_answer(
        self,
        query: str,
        context: str,
        system_prompt: str = None
    ) -> str:
        """生成回答."""

        default_system = """你是一个 helpful 的AI助手。请基于提供的上下文信息回答用户的问题。
如果上下文信息不足以回答问题，请明确说明。"""

        messages = [
            {
                "role": "system",
                "content": system_prompt or default_system
            },
            {
                "role": "user",
                "content": f"""基于以下上下文回答问题：

上下文：
{context}

问题：{query}

请提供详细且准确的回答："""
            }
        ]

        response = self.llm.chat.completions.create(
            model=self.llm_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content


# ==================== 文档加载器 ====================

class DocumentLoader:
    """文档加载器."""

    @staticmethod
    def load_text(file_path: str, metadata: Dict = None) -> Document:
        """加载文本文件."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        doc_id = hashlib.md5(file_path.encode()).hexdigest()

        return Document(
            id=doc_id,
            content=content,
            metadata=metadata or {"source": file_path, "type": "text"}
        )

    @staticmethod
    def load_pdf(file_path: str, metadata: Dict = None) -> List[Document]:
        """加载PDF文件."""
        try:
            import PyPDF2

            documents = []
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)

                for i, page in enumerate(pdf.pages):
                    content = page.extract_text()
                    doc_id = f"{hashlib.md5(file_path.encode()).hexdigest()}_page_{i}"

                    documents.append(Document(
                        id=doc_id,
                        content=content,
                        metadata={
                            **(metadata or {}),
                            "source": file_path,
                            "type": "pdf",
                            "page": i + 1
                        }
                    ))

            return documents

        except ImportError:
            logger.error("PyPDF2 not installed")
            return []

    @staticmethod
    def load_web(url: str, metadata: Dict = None) -> Document:
        """加载网页内容."""
        try:
            import requests
            from bs4 import BeautifulSoup

            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 提取文本
            for script in soup(["script", "style"]):
                script.decompose()

            content = soup.get_text(separator='\n', strip=True)

            doc_id = hashlib.md5(url.encode()).hexdigest()

            return Document(
                id=doc_id,
                content=content,
                metadata={
                    **(metadata or {}),
                    "source": url,
                    "type": "web"
                }
            )

        except Exception as e:
            logger.error(f"Failed to load web page: {e}")
            return None


# ==================== 使用示例 ====================

def rag_example():
    """RAG系统使用示例."""

    # 初始化RAG系统
    rag = RAGSystem(
        embedding_model="text-embedding-3-small",
        llm_model="gpt-4",
        chunk_size=500,
        top_k=3
    )

    # 加载文档
    doc1 = DocumentLoader.load_text("document1.txt")
    doc2 = DocumentLoader.load_text("document2.txt")

    # 添加到知识库
    rag.add_documents([doc1, doc2])

    # 查询
    result = rag.query(
        query="什么是机器学习？",
        system_prompt="你是一个AI技术专家，请用通俗易懂的语言回答问题。"
    )

    print("回答:")
    print(result["answer"])
    print("\n来源:")
    for source in result["sources"]:
        print(f"- {source['metadata']['source']} (得分: {source['score']:.4f})")


# ==================== 高级RAG技术 ====================

class AdvancedRAG(RAGSystem):
    """高级RAG系统，包含重排序和查询扩展."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reranker = None  # 可以集成Cross-Encoder

    def query_expansion(self, query: str) -> List[str]:
        """查询扩展."""
        # 生成查询变体
        expansion_prompt = f"""为以下查询生成3个语义相似的变体：

查询：{query}

请以JSON数组格式输出：["变体1", "变体2", "变体3"]"""

        response = self.llm.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": expansion_prompt}]
        )

        try:
            import json
            variations = json.loads(response.choices[0].message.content)
            return [query] + variations
        except:
            return [query]

    def hybrid_search(
        self,
        query: str,
        top_k: int = 10
    ) -> List[SearchResult]:
        """混合搜索（向量 + 关键词）."""
        # 向量搜索
        query_embedding = self.embedding_model.embed_query(query)
        vector_results = self.vector_store.search(query_embedding, top_k=top_k)

        # 可以添加关键词搜索并融合结果

        return vector_results

    def rerank(
        self,
        query: str,
        results: List[SearchResult],
        top_k: int = 5
    ) -> List[SearchResult]:
        """重排序结果."""
        # 使用Cross-Encoder或LLM进行重排序
        # 这里使用简单的相关性评分

        scored_results = []
        for result in results:
            # 计算相关性分数
            relevance_prompt = f"""评估以下文档与查询的相关性（0-10分）：

查询：{query}

文档：{result.document.content[:200]}

请只输出数字分数。"""

            response = self.llm.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": relevance_prompt}],
                max_tokens=5
            )

            try:
                score = float(response.choices[0].message.content.strip())
            except:
                score = result.score

            scored_results.append((result, score))

        # 按分数排序
        scored_results.sort(key=lambda x: x[1], reverse=True)

        return [r for r, _ in scored_results[:top_k]]

    def query(self, query: str, **kwargs) -> Dict:
        """增强查询."""
        # 1. 查询扩展
        expanded_queries = self.query_expansion(query)

        # 2. 混合搜索
        all_results = []
        for q in expanded_queries:
            results = self.hybrid_search(q, top_k=5)
            all_results.extend(results)

        # 去重
        seen_ids = set()
        unique_results = []
        for r in all_results:
            if r.document.id not in seen_ids:
                seen_ids.add(r.document.id)
                unique_results.append(r)

        # 3. 重排序
        reranked_results = self.rerank(query, unique_results, top_k=self.top_k)

        # 4. 生成回答
        context = self._build_context(reranked_results)
        answer = self._generate_answer(query, context, kwargs.get('system_prompt'))

        return {
            "query": query,
            "expanded_queries": expanded_queries,
            "answer": answer,
            "sources": [
                {
                    "content": r.document.content[:200],
                    "metadata": r.document.metadata,
                    "score": r.score
                }
                for r in reranked_results
            ]
        }
```

---

### 3. AI Agent

#### 3.1 概念定义

**AI Agent** 是一种能够感知环境、做出决策并执行行动的自主系统。它结合了LLM的推理能力与工具使用能力，可以完成复杂的任务。

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI Agent 架构图                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      Agent Core                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │ Planning │  │ Memory   │  │ Tool Use │              │   │
│  │  │ 规划     │  │ 记忆     │  │ 工具调用 │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                         │
│         ┌─────────────┼─────────────┐                          │
│         │             │             │                          │
│         ▼             ▼             ▼                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│  │  Tools   │  │  Memory  │  │  LLM     │                     │
│  │ 工具集   │  │ 存储     │  │ 推理引擎 │                     │
│  └──────────┘  └──────────┘  └──────────┘                     │
│       │                                        │               │
│       └────────────────────────────────────────┘               │
│                       │                                         │
│                       ▼                                         │
│              ┌─────────────────┐                               │
│              │   Environment   │                               │
│              │   环境          │                               │
│              └─────────────────┘                               │
│                                                                 │
│  Agent类型：                                                    │
│  1. ReAct Agent - 推理+行动交替                                │
│  2. Plan-and-Execute - 先规划后执行                            │
│  3. Multi-Agent - 多Agent协作                                  │
│  4. AutoGPT - 自主目标导向                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.2 实现模式

```python
"""AI Agent完整实现."""

import os
import json
import re
from typing import List, Dict, Callable, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Agent状态."""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    FINISHED = "finished"
    ERROR = "error"


@dataclass
class Tool:
    """工具定义."""
    name: str
    description: str
    parameters: Dict
    func: Callable

    def to_dict(self) -> Dict:
        """转换为字典."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

    def execute(self, **kwargs) -> str:
        """执行工具."""
        try:
            result = self.func(**kwargs)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"


@dataclass
class Action:
    """行动."""
    tool: str
    input: Dict
    observation: str = ""

    def to_dict(self) -> Dict:
        return {
            "tool": self.tool,
            "input": self.input,
            "observation": self.observation
        }


@dataclass
class AgentMemory:
    """Agent记忆."""
    thoughts: List[str] = field(default_factory=list)
    actions: List[Action] = field(default_factory=list)
    max_history: int = 10

    def add_thought(self, thought: str):
        """添加思考."""
        self.thoughts.append(thought)
        if len(self.thoughts) > self.max_history:
            self.thoughts.pop(0)

    def add_action(self, action: Action):
        """添加行动."""
        self.actions.append(action)
        if len(self.actions) > self.max_history:
            self.actions.pop(0)

    def get_context(self) -> str:
        """获取记忆上下文."""
        context = []

        for thought, action in zip(self.thoughts, self.actions):
            context.append(f"思考: {thought}")
            context.append(f"行动: {action.tool}({json.dumps(action.input)})")
            context.append(f"观察: {action.observation}")

        return "\n".join(context)


class BaseAgent(ABC):
    """Agent基类."""

    def __init__(
        self,
        name: str,
        llm_model: str = "gpt-4",
        max_iterations: int = 10
    ):
        self.name = name
        self.llm_model = llm_model
        self.max_iterations = max_iterations
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tools: Dict[str, Tool] = {}
        self.memory = AgentMemory()
        self.state = AgentState.IDLE

    def add_tool(self, tool: Tool):
        """添加工具."""
        self.tools[tool.name] = tool

    @abstractmethod
    def run(self, task: str) -> str:
        """运行Agent."""
        pass

    def _get_tool_descriptions(self) -> str:
        """获取工具描述."""
        descriptions = []
        for tool in self.tools.values():
            descriptions.append(
                f"{tool.name}: {tool.description}\n"
                f"参数: {json.dumps(tool.parameters, indent=2)}"
            )
        return "\n\n".join(descriptions)


class ReActAgent(BaseAgent):
    """ReAct Agent实现."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.system_prompt = """你是一个智能助手，可以使用工具来完成任务。

你可以使用的工具：
{tools}

请按照以下格式回答：
思考：你对当前情况的思考
行动：工具名称
行动输入：工具的JSON格式输入
观察：工具执行结果
...（思考/行动/行动输入/观察可以重复多次）
思考：我现在知道最终答案
最终答案：对用户的回答

开始！"""

    def run(self, task: str) -> str:
        """运行ReAct Agent."""
        self.state = AgentState.THINKING

        messages = [
            {
                "role": "system",
                "content": self.system_prompt.format(
                    tools=self._get_tool_descriptions()
                )
            },
            {
                "role": "user",
                "content": f"任务：{task}\n\n{self.memory.get_context()}"
            }
        ]

        for iteration in range(self.max_iterations):
            logger.info(f"Iteration {iteration + 1}/{self.max_iterations}")

            # 获取LLM响应
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                temperature=0.7
            )

            content = response.choices[0].message.content
            logger.info(f"LLM Response:\n{content}")

            # 解析思考
            thought_match = re.search(r'思考：(.+?)(?=\n行动：|$)', content, re.DOTALL)
            if thought_match:
                thought = thought_match.group(1).strip()
                self.memory.add_thought(thought)

            # 检查是否有最终答案
            final_answer_match = re.search(r'最终答案：(.+)', content, re.DOTALL)
            if final_answer_match:
                self.state = AgentState.FINISHED
                return final_answer_match.group(1).strip()

            # 解析行动
            action_match = re.search(r'行动：(.+?)\n行动输入：(.+?)(?=\n观察：|$)', content, re.DOTALL)
            if action_match:
                tool_name = action_match.group(1).strip()
                tool_input_str = action_match.group(2).strip()

                try:
                    tool_input = json.loads(tool_input_str)
                except json.JSONDecodeError:
                    tool_input = {"input": tool_input_str}

                # 执行工具
                self.state = AgentState.ACTING

                if tool_name in self.tools:
                    observation = self.tools[tool_name].execute(**tool_input)
                else:
                    observation = f"错误：未知工具 '{tool_name}'"

                action = Action(
                    tool=tool_name,
                    input=tool_input,
                    observation=observation
                )
                self.memory.add_action(action)

                # 添加观察结果到消息
                messages.append({"role": "assistant", "content": content})
                messages.append({
                    "role": "user",
                    "content": f"观察：{observation}\n\n继续。"
                })

                self.state = AgentState.THINKING
            else:
                # 没有识别到行动格式
                messages.append({"role": "assistant", "content": content})
                messages.append({
                    "role": "user",
                    "content": "请按照指定格式回答：思考/行动/行动输入/观察"
                })

        self.state = AgentState.ERROR
        return "达到最大迭代次数，未能完成任务。"


class PlanAndExecuteAgent(BaseAgent):
    """Plan-and-Execute Agent."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _create_plan(self, task: str) -> List[str]:
        """创建执行计划."""
        prompt = f"""请为以下任务创建一个详细的执行计划，列出需要完成的步骤：

任务：{task}

可用工具：
{self._get_tool_descriptions()}

请以JSON数组格式输出步骤列表：
["步骤1", "步骤2", "步骤3"]"""

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            plan = json.loads(response.choices[0].message.content)
            return plan if isinstance(plan, list) else [task]
        except:
            return [task]

    def _execute_step(self, step: str, context: str) -> str:
        """执行单个步骤."""
        prompt = f"""执行以下步骤：

步骤：{step}

上下文：
{context}

可用工具：
{self._get_tool_descriptions()}

如果需要使用工具，请以JSON格式输出：
{{"tool": "工具名称", "input": {{"参数": "值"}}}}

否则直接输出结果。"""

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        # 尝试解析工具调用
        try:
            tool_call = json.loads(content)
            if "tool" in tool_call and tool_call["tool"] in self.tools:
                result = self.tools[tool_call["tool"]].execute(**tool_call.get("input", {}))
                return result
        except:
            pass

        return content

    def run(self, task: str) -> str:
        """运行Plan-and-Execute Agent."""
        # 1. 创建计划
        plan = self._create_plan(task)
        logger.info(f"执行计划：{plan}")

        # 2. 执行计划
        results = []
        context = f"原始任务：{task}"

        for i, step in enumerate(plan):
            logger.info(f"执行步骤 {i+1}/{len(plan)}: {step}")

            result = self._execute_step(step, context)
            results.append(f"步骤 {i+1} ({step}): {result}")

            context += f"\n步骤 {i+1} 结果：{result}"

        # 3. 生成最终答案
        final_prompt = f"""基于以下执行结果，生成最终答案：

原始任务：{task}

执行结果：
{chr(10).join(results)}

请提供清晰、完整的最终答案。"""

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": final_prompt}]
        )

        return response.choices[0].message.content


# ==================== 工具定义 ====================

def create_default_tools() -> List[Tool]:
    """创建默认工具集."""

    # 搜索工具
    def search(query: str) -> str:
        """模拟搜索."""
        return f"搜索结果：关于 '{query}' 的信息..."

    # 计算器
    def calculator(expression: str) -> str:
        """计算表达式."""
        try:
            # 安全计算
            allowed_names = {"abs": abs, "max": max, "min": min, "sum": sum}
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return str(result)
        except Exception as e:
            return f"计算错误: {str(e)}"

    # 天气查询
    def get_weather(city: str) -> str:
        """获取天气."""
        return f"{city} 今天天气晴朗，温度 25°C"

    # 文件读取
    def read_file(file_path: str) -> str:
        """读取文件."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"读取文件失败: {str(e)}"

    return [
        Tool(
            name="search",
            description="搜索信息",
            parameters={"query": {"type": "string", "description": "搜索查询"}},
            func=search
        ),
        Tool(
            name="calculator",
            description="计算数学表达式",
            parameters={"expression": {"type": "string", "description": "数学表达式"}},
            func=calculator
        ),
        Tool(
            name="get_weather",
            description="获取城市天气",
            parameters={"city": {"type": "string", "description": "城市名称"}},
            func=get_weather
        ),
        Tool(
            name="read_file",
            description="读取文件内容",
            parameters={"file_path": {"type": "string", "description": "文件路径"}},
            func=read_file
        )
    ]


# ==================== 使用示例 ====================

def agent_example():
    """Agent使用示例."""

    # 创建ReAct Agent
    agent = ReActAgent(
        name="Assistant",
        llm_model="gpt-4",
        max_iterations=5
    )

    # 添加工具
    for tool in create_default_tools():
        agent.add_tool(tool)

    # 运行任务
    result = agent.run("计算 25 * 4 + 100，然后告诉我北京的天气")
    print(f"\n最终结果：\n{result}")


def plan_execute_example():
    """Plan-and-Execute示例."""

    agent = PlanAndExecuteAgent(
        name="Planner",
        llm_model="gpt-4"
    )

    for tool in create_default_tools():
        agent.add_tool(tool)

    result = agent.run("帮我制定一个学习计划，先搜索Python学习资源，然后计算每天学习2小时需要多少天达到100小时")
    print(f"\n最终结果：\n{result}")


# ==================== 多Agent系统 ====================

class MultiAgentSystem:
    """多Agent协作系统."""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.communication_log: List[Dict] = []

    def add_agent(self, agent: BaseAgent):
        """添加Agent."""
        self.agents[agent.name] = agent

    def delegate(self, task: str, agent_name: str) -> str:
        """委派任务给特定Agent."""
        if agent_name not in self.agents:
            return f"错误：找不到Agent '{agent_name}'"

        result = self.agents[agent_name].run(task)

        self.communication_log.append({
            "from": "system",
            "to": agent_name,
            "task": task,
            "result": result
        })

        return result

    def collaborate(self, task: str, agent_names: List[str]) -> str:
        """多Agent协作完成任务."""
        results = []

        for name in agent_names:
            if name in self.agents:
                result = self.agents[name].run(task)
                results.append(f"{name}: {result}")

        # 综合结果
        return "\n\n".join(results)
```

---

## 总结

本文档全面梳理了CI/CD持续工作流和AI/ML工程实践的各个方面：

### CI/CD核心要点

1. **持续集成**：频繁集成、自动化测试、快速反馈
2. **持续部署**：蓝绿部署、金丝雀发布、特性开关
3. **工具选择**：GitHub Actions、GitLab CI、Jenkins、ArgoCD
4. **最佳实践**：自动化测试、代码质量、制品管理

### MLOps核心要点

1. **实验跟踪**：MLflow、W&B、TensorBoard
2. **模型管理**：版本控制、注册中心、DVC
3. **模型服务**：REST API、批处理、缓存
4. **模型监控**：性能监控、数据漂移检测

### AI工程化核心要点

1. **LLM应用**：OpenAI API、Prompt工程
2. **RAG系统**：检索增强生成、向量数据库
3. **AI Agent**：ReAct、Plan-and-Execute、多Agent协作

---

*文档版本: 1.0*
*最后更新: 2024*
