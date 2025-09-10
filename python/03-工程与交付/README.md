# 03-工程与交付

聚焦打包、分发、部署与运维接口的工程化流水线。

## 1. 构建与打包

- PEP 517/518、build、uv/pip 构建
- 版本与变更日志（SemVer / Conventional Commits）
- 最小示例：`./examples/minimal_build`
  - 配置：`pyproject.toml`
  - 包：`src/minbuild/__init__.py`
  - 构建命令（本地）：`uv build` 或 `python -m build`

### 基于 uv 的最小流水

```bash
uv pip compile pyproject.toml -o uv.lock
uv pip sync uv.lock
uv build
uv publish --repository pypi
```

## 2. 发布与分发

- PyPI/内部制品库
- 许可证与SBOM

### 私有制品库发布（示例）

- 配置 `~/.pypirc`：

```ini
[distutils]
index-servers =
    internal

[internal]
repository = https://repo.example.com/api/pypi/python/simple
username = __token__
password = ${PYPI_API_TOKEN}
```

- 使用 uv 发布到私有库：

```bash
# 通过名称选择仓库（与 .pypirc 对应）
uv publish --repository internal
```

- GitLab Package Registry（示例命令）：

```bash
uv publish --repository https://gitlab.example.com/api/v4/projects/<id>/packages/pypi
```

- JFrog Artifactory（示例命令）：

```bash
uv publish --repository https://artifactory.example.com/artifactory/api/pypi/python-local
```

> 建议：凭据通过 CI Secret 注入环境变量，避免写入仓库。

### SBOM 生成与签名

```bash
# 生成 SBOM（CycloneDX/Syft）
syft packages file:dist/*.whl -o cyclonedx-json > sbom.json

# 制品签名（Cosign），需事先配置密钥或 OIDC
cosign sign-blob --output-signature dist.sig dist/*.whl

# 验证
cosign verify-blob --signature dist.sig dist/*.whl
```

## 3. 运行与部署

- 容器化与镜像优化
- 配置与密钥管理

## 4. 观测与回滚

- 日志/指标/追踪
- 升级/回滚策略

## 5. 模板与参考

- 最小工程模板/部署脚本（预留）
- CI：GitHub Actions 示例

```yaml
# .github/workflows/release.yml（示例）
name: release
on:
  push:
    tags:
      - 'v*.*.*'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install uv
        run: pipx install uv || pip install uv
      - name: Resolve & build
        run: |
          uv pip compile pyproject.toml -o uv.lock
          uv pip sync uv.lock
          uv build
      - name: Publish
        env:
          PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
        run: uv publish --repository pypi
```

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 相关主题：[01-语言与生态/README](../01-语言与生态/README.md)
