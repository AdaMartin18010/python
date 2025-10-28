# CI/CD 持续集成与部署

**Python应用自动化流水线**

---

## 📋 概述

CI/CD是现代软件开发的核心实践，实现代码自动测试、构建和部署。

### 核心概念

- 🔄 **CI** - 持续集成：自动测试和构建
- 🚀 **CD** - 持续部署：自动发布到生产
- 🎯 **自动化** - 减少人工干预
- 📊 **可观测** - 实时反馈

---

## 🚀 GitHub Actions

### 基础工作流

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      
      - name: Lint with ruff
        run: uv run ruff check .
      
      - name: Type check with mypy
        run: uv run mypy .
      
      - name: Test with pytest
        run: |
          uv run pytest --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## 🐳 Docker构建和发布

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myregistry/myapp
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=myregistry/myapp:buildcache
          cache-to: type=registry,ref=myregistry/myapp:buildcache,mode=max
```

---

## 🔒 安全扫描

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # 每日扫描

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json
      
      - name: Run Safety
        run: |
          pip install safety
          safety check --json
      
      - name: Run Snyk
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
      
      - name: Upload results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: snyk.sarif
```

---

## 🚀 部署到Kubernetes

```yaml
# .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}
      
      - name: Deploy to cluster
        run: |
          kubectl set image deployment/myapp \
            myapp=myregistry/myapp:${{ github.ref_name }}
          
          kubectl rollout status deployment/myapp
      
      - name: Verify deployment
        run: |
          kubectl get pods
          kubectl get services
```

---

## 🎯 GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: registry.gitlab.com/$CI_PROJECT_PATH
  PYTHON_VERSION: "3.12"

# 测试阶段
test:
  stage: test
  image: python:$PYTHON_VERSION
  before_script:
    - pip install uv
    - uv sync
  script:
    - uv run ruff check .
    - uv run mypy .
    - uv run pytest --cov=. --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

# 构建阶段
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .
    - docker push $DOCKER_IMAGE:$CI_COMMIT_SHA
  only:
    - main
    - tags

# 部署阶段
deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context $KUBE_CONTEXT
    - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
  only:
    - main
  when: manual
```

---

## 🔄 多环境部署

```yaml
# .github/workflows/multi-env.yml
name: Multi-Environment Deploy

on:
  push:
    branches:
      - develop
      - staging
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Determine environment
        id: env
        run: |
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            echo "environment=production" >> $GITHUB_OUTPUT
            echo "url=https://api.example.com" >> $GITHUB_OUTPUT
          elif [[ "${{ github.ref }}" == "refs/heads/staging" ]]; then
            echo "environment=staging" >> $GITHUB_OUTPUT
            echo "url=https://staging-api.example.com" >> $GITHUB_OUTPUT
          else
            echo "environment=development" >> $GITHUB_OUTPUT
            echo "url=https://dev-api.example.com" >> $GITHUB_OUTPUT
          fi
      
      - name: Deploy to ${{ steps.env.outputs.environment }}
        uses: azure/webapps-deploy@v2
        with:
          app-name: myapp-${{ steps.env.outputs.environment }}
          publish-profile: ${{ secrets[format('AZURE_WEBAPP_PUBLISH_PROFILE_{0}', steps.env.outputs.environment)] }}
      
      - name: Run smoke tests
        run: |
          curl -f ${{ steps.env.outputs.url }}/health || exit 1
```

---

## 📊 性能测试

```yaml
# .github/workflows/performance.yml
name: Performance Test

on:
  pull_request:
    branches: [ main ]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Start application
        run: |
          docker-compose up -d
          sleep 10
      
      - name: Run Locust
        run: |
          pip install locust
          locust -f tests/locustfile.py \
            --headless \
            --users 100 \
            --spawn-rate 10 \
            --run-time 5m \
            --html locust-report.html
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: performance-report
          path: locust-report.html
```

---

## 🎯 蓝绿部署

```python
# deploy.py
import subprocess
import time

def blue_green_deploy(new_version: str):
    """蓝绿部署"""
    # 1. 部署新版本（绿色环境）
    print("部署绿色环境...")
    subprocess.run([
        'kubectl', 'apply', '-f', f'k8s/deployment-green-{new_version}.yaml'
    ])
    
    # 2. 等待新版本就绪
    print("等待绿色环境就绪...")
    subprocess.run([
        'kubectl', 'rollout', 'status', 'deployment/myapp-green'
    ])
    time.sleep(10)
    
    # 3. 健康检查
    print("健康检查...")
    result = subprocess.run([
        'kubectl', 'exec', 'deployment/myapp-green', '--',
        'curl', '-f', 'http://localhost:8000/health'
    ], capture_output=True)
    
    if result.returncode != 0:
        print("健康检查失败，回滚...")
        subprocess.run([
            'kubectl', 'delete', 'deployment', 'myapp-green'
        ])
        return False
    
    # 4. 切换流量
    print("切换流量到绿色环境...")
    subprocess.run([
        'kubectl', 'patch', 'service', 'myapp',
        '-p', '{"spec":{"selector":{"version":"green"}}}'
    ])
    
    # 5. 等待一段时间观察
    print("观察新版本...")
    time.sleep(60)
    
    # 6. 删除旧版本（蓝色环境）
    print("删除蓝色环境...")
    subprocess.run([
        'kubectl', 'delete', 'deployment', 'myapp-blue'
    ])
    
    return True

if __name__ == '__main__':
    import sys
    version = sys.argv[1] if len(sys.argv) > 1 else 'latest'
    success = blue_green_deploy(version)
    sys.exit(0 if success else 1)
```

---

## 🔄 金丝雀部署

```yaml
# k8s/canary-deployment.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 10    # 10%流量到新版本
        - pause: {duration: 5m}
        - setWeight: 25    # 25%流量
        - pause: {duration: 5m}
        - setWeight: 50    # 50%流量
        - pause: {duration: 5m}
        - setWeight: 75    # 75%流量
        - pause: {duration: 5m}
      trafficRouting:
        istio:
          virtualService:
            name: myapp-vsvc
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myregistry/myapp:latest
```

---

## 📚 最佳实践

### 1. 分支策略

```
main (生产)
  ↑
staging (预发布)
  ↑
develop (开发)
  ↑
feature/* (功能分支)
```

### 2. 版本管理

```bash
# 语义化版本
v1.2.3
  ↓
major.minor.patch

# 自动生成版本号
git tag v1.2.3
git push origin v1.2.3
```

### 3. 回滚策略

```yaml
# 自动回滚
- name: Deploy with rollback
  run: |
    kubectl apply -f deployment.yaml
    kubectl rollout status deployment/myapp --timeout=5m || \
    kubectl rollout undo deployment/myapp
```

---

## 🔗 相关资源

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [GitLab CI/CD文档](https://docs.gitlab.com/ee/ci/)

---

**最后更新**: 2025年10月28日

