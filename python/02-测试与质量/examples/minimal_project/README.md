# minimal_project 运行说明

## 环境准备（任选其一）

- 方案A：uv（推荐）
  - 安装：`pipx install uv` 或 `pip install uv`
  - 安装依赖：`uv pip install -r requirements.txt`（如无则使用 pyproject 直接安装）
- 方案B：venv
  - 创建：`python -m venv .venv`
  - 激活（Windows PowerShell）：`.venv/Scripts/Activate.ps1`
  - 安装：`pip install -e .[dev]`

## 运行

- 运行测试：`pytest -q`
- 代码检查：`ruff check .`
- 类型检查：`mypy src`

## 结构

- `pyproject.toml`：项目与工具配置
- `src/example/core.py`：核心示例代码
- `tests/test_core.py`：最小测试用例

## 返回与相关

- 返回目录：[@SUMMARY](../../../SUMMARY.md)
- 上级主题：[02-测试与质量/README](../../README.md)
