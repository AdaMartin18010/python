# Coverage 测试覆盖率

**代码覆盖率分析工具**

---

## 📋 概述

Coverage.py用于测量Python代码的测试覆盖率，帮助识别未测试的代码。

### 核心特性

- 📊 **详细报告** - HTML、XML、终端报告
- 🎯 **分支覆盖** - 检测分支逻辑
- 🔧 **pytest集成** - 无缝集成
- 📈 **趋势跟踪** - 追踪覆盖率变化

---

## 🚀 快速开始

### 安装

```bash
uv add coverage pytest-cov
```

### 基本使用

```bash
# 运行测试并收集覆盖率
coverage run -m pytest

# 查看报告
coverage report

# 生成HTML报告
coverage html
# 在浏览器中打开 htmlcov/index.html
```

---

## 💻 pytest集成

### 使用pytest-cov

```bash
# 运行测试并显示覆盖率
pytest --cov=myproject tests/

# 生成HTML报告
pytest --cov=myproject --cov-report=html tests/

# 只显示缺失的行
pytest --cov=myproject --cov-report=term-missing tests/
```

---

## ⚙️ 配置

### .coveragerc

```ini
[run]
source = myproject
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov
```

### pyproject.toml

```toml
[tool.coverage.run]
source = ["myproject"]
omit = ["*/tests/*", "*/venv/*"]

[tool.coverage.report]
precision = 2
show_missing = true
fail_under = 80
```

---

## 📊 报告格式

### 终端报告

```bash
$ coverage report
Name                 Stmts   Miss  Cover
----------------------------------------
myproject/core.py       20      2    90%
myproject/utils.py      15      0   100%
----------------------------------------
TOTAL                   35      2    94%
```

### 详细报告

```bash
$ coverage report -m
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
myproject/core.py       20      2    90%   5-6
myproject/utils.py      15      0   100%
--------------------------------------------------
TOTAL                   35      2    94%
```

---

## 🎯 CI/CD集成

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov
      
      - name: Run tests with coverage
        run: |
          pytest --cov=myproject --cov-report=xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
```

---

## 📚 最佳实践

### 1. 设置最低覆盖率

```bash
# 如果覆盖率低于90%，测试失败
pytest --cov=myproject --cov-fail-under=90
```

### 2. 忽略无需测试的代码

```python
def debug_only_function():  # pragma: no cover
    # 仅调试时使用，不需要测试
    print("Debug info")
```

### 3. 分支覆盖

```bash
# 启用分支覆盖
pytest --cov=myproject --cov-branch
```

---

## 🔗 相关资源

- [Coverage.py文档](https://coverage.readthedocs.io/)
- [pytest-cov文档](https://pytest-cov.readthedocs.io/)

---

**最后更新**: 2025年10月28日

