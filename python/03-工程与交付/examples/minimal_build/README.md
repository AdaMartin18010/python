# minimal_build 运行与验证

## 本地构建

- 使用 uv：`uv build`
- 或使用 build：`python -m build`

## 本地安装与导入验证

- 安装生成的 wheel（版本以实际为准）：
  - Windows PowerShell：`pip install .\dist\minbuild-0.1.0-py3-none-any.whl`
- 交互式验证：
  - `python -c "import minbuild; print(minbuild.__version__)"`

## 结构

- `pyproject.toml`
- `src/minbuild/__init__.py`

## 返回与相关

- 返回目录：[@SUMMARY](../../../SUMMARY.md)
- 上级主题：[03-工程与交付/README](../../README.md)
