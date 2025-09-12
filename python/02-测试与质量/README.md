# 02-测试与质量

聚焦 pytest、类型检查、静态分析与CI 集成的最小可行体系。

## 1. 测试策略

- 单元/集成/端到端分层
- 基线用例与回归集

## 2. 工具与配置

- pytest 基础配置、参数化、夹具
- 类型检查（mypy/pyright）
- Lint（ruff/flake8/pylint）
- 统一工具配置见仓库根 `pyproject.toml`

### 2.1 推荐最小组合（2025）

- 测试：`pytest`
- 代码风格与静态检查：`ruff`（含 `ruff format`）
- 类型：`mypy`（或 `pyright`）
- 提交钩子：`pre-commit`

### 2.2 安装与运行（uv 优先）

```powershell
pipx install uv || pip install uv
uv pip compile pyproject.toml -o uv.lock
uv pip sync uv.lock
pytest -q --maxfail=1 --disable-warnings
ruff check . && mypy src || true
```

## 3. 质量检查清单（本地副本）

- [迁移/质量检查](./迁移/质量检查.md)

## 4. CI 集成（示例骨架）

- GitHub Actions（最小示例）：

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install uv
        run: pipx install uv || pip install uv
      - name: Resolve
        run: |
          uv pip compile pyproject.toml -o uv.lock
          uv pip sync uv.lock
      - name: Lint & Type
        run: |
          ruff check .
          mypy src || true  # 如项目未准备完全，可先容忍为警告
      - name: Test
        run: pytest -q --maxfail=1 --disable-warnings
```

- GitLab CI（最小示例）：

```yaml
stages: [test]

image: python:3.11-slim

before_script:
  - pip install --no-cache-dir uv || pip install --no-cache-dir uv
  - uv pip compile pyproject.toml -o uv.lock
  - uv pip sync uv.lock

test:
  stage: test
  script:
    - ruff check .
    - mypy src || true
    - pytest -q --maxfail=1 --disable-warnings
```

- Azure Pipelines（最小示例）：

```yaml
trigger: [ main ]

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'
  - script: pipx install uv || pip install uv
    displayName: Install uv
  - script: |
      uv pip compile pyproject.toml -o uv.lock
      uv pip sync uv.lock
    displayName: Resolve deps
  - script: |
      ruff check .
      mypy src || true
      pytest -q --maxfail=1 --disable-warnings
    displayName: Lint & Test
```

## 5. 本地提交钩子（pre-commit）

- 安装：`pip install pre-commit` 或 `uv pip install pre-commit`
- 启用：`pre-commit install && pre-commit install --hook-type commit-msg`
- 配置：仓库根已提供 `.pre-commit-config.yaml`，包含 `ruff/ruff-format/mypy/commitizen`

## 6. 最小示例（可运行）

- 位置：`./examples/minimal_project`
  - 配置：`pyproject.toml`
  - 源码：`src/example/core.py`
  - 测试：`tests/test_core.py`
- 运行指引：
  1) 在示例目录下安装依赖（建议使用 uv/pipx 或 venv）
  2) 运行 `pytest`
  3) 运行 `ruff check .` 与 `mypy src`

> Windows PowerShell 提示：若使用 `uv`，需先通过 `pipx install uv` 或 `pip install uv` 安装；使用 venv 时先激活 `./.venv/Scripts/Activate.ps1`。

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 相关主题：[01-语言与生态/README](../01-语言与生态/README.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)
