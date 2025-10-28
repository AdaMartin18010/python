# Python Pyright 类型检查器

**Pyright vs mypy 对比指南**

---

## 📋 目录

- [Pyright简介](#Pyright简介)
- [Pyright配置](#Pyright配置)
- [Pyright vs mypy](#Pyright-vs-mypy)
- [VSCode集成](#VSCode集成)
- [高级特性](#高级特性)

---

## Pyright简介

### 什么是Pyright

```python
"""
Pyright: 微软开发的Python静态类型检查器
"""

# 安装
# npm install -g pyright
# 或
# uv add --dev pyright

# 基础使用
# pyright script.py
# pyright src/

# Pyright特点:
# 1. 快速 - TypeScript实现
# 2. 完整 - 支持所有PEP标准
# 3. 严格 - 默认更严格
# 4. VSCode集成 - Pylance

# 示例
def greet(name: str) -> str:
    return f"Hello, {name}"

# 类型错误
result = greet(123)  # pyright会报错
# Argument of type "Literal[123]" cannot be assigned to parameter "name" of type "str"
```

### 安装和使用

```bash
# 全局安装
npm install -g pyright

# 项目安装
uv add --dev pyright

# 运行检查
pyright

# 检查特定文件
pyright src/main.py

# 监视模式
pyright --watch

# 输出JSON
pyright --outputjson

# VSCode: 安装Pylance扩展
# Pylance = Pyright + 语言服务
```

---

## Pyright配置

### pyrightconfig.json

```json
{
  "include": [
    "src"
  ],
  "exclude": [
    "**/node_modules",
    "**/__pycache__",
    "build",
    "dist"
  ],
  "ignore": [
    "tests"
  ],
  
  "pythonVersion": "3.12",
  "pythonPlatform": "Linux",
  
  "typeCheckingMode": "strict",
  
  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "reportUnusedImport": "warning",
  "reportUnusedClass": "warning",
  "reportUnusedFunction": "warning",
  "reportUnusedVariable": "warning",
  "reportDuplicateImport": "warning",
  
  "reportOptionalSubscript": "error",
  "reportOptionalMemberAccess": "error",
  "reportOptionalCall": "error",
  "reportOptionalIterable": "error",
  "reportOptionalContextManager": "error",
  "reportOptionalOperand": "error",
  
  "reportUntypedFunctionDecorator": "warning",
  "reportUntypedClassDecorator": "warning",
  "reportUntypedBaseClass": "error",
  "reportUntypedNamedTuple": "error",
  
  "reportPrivateUsage": "warning",
  "reportConstantRedefinition": "error",
  "reportIncompatibleMethodOverride": "error",
  "reportIncompatibleVariableOverride": "error",
  
  "reportUnknownParameterType": "warning",
  "reportUnknownArgumentType": "warning",
  "reportUnknownLambdaType": "warning",
  "reportUnknownVariableType": "warning",
  "reportUnknownMemberType": "warning",
  
  "reportCallInDefaultInitializer": "warning",
  "reportUnnecessaryIsInstance": "warning",
  "reportUnnecessaryCast": "warning",
  "reportAssertAlwaysTrue": "warning",
  "reportSelfClsParameterName": "warning",
  "reportImplicitStringConcatenation": "warning",
  
  "venvPath": ".",
  "venv": ".venv",
  
  "executionEnvironments": [
    {
      "root": "src",
      "pythonVersion": "3.12",
      "pythonPlatform": "Linux",
      "extraPaths": []
    }
  ]
}
```

### pyproject.toml配置

```toml
[tool.pyright]
include = ["src"]
exclude = ["**/node_modules", "**/__pycache__"]
ignore = ["tests"]

pythonVersion = "3.12"
pythonPlatform = "Linux"

typeCheckingMode = "strict"

# 报告设置
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = "warning"
reportUnusedVariable = "warning"

# 虚拟环境
venvPath = "."
venv = ".venv"
```

---

## Pyright vs mypy

### 对比分析

```python
"""
Pyright与mypy对比
"""

# 1. 速度
# Pyright: 快 (TypeScript实现)
# mypy: 较慢 (Python实现)

# 2. 默认严格度
# Pyright: 默认更严格
# mypy: 默认较宽松

# 3. 错误信息
# Pyright:
# Argument of type "Literal[123]" cannot be assigned to parameter "name" of type "str"

# mypy:
# error: Argument 1 to "greet" has incompatible type "int"; expected "str"

# 4. PEP支持
# Pyright: 更快支持新PEP
# mypy: 稳定但较慢

# 5. IDE集成
# Pyright: VSCode (Pylance)
# mypy: PyCharm, VSCode (插件)

# 示例: 类型推断差异
def example():
    x = []  # Pyright推断为list[Unknown]
            # mypy推断为list[Any]
    
    x.append(1)  # Pyright: 此时细化为list[int]
                 # mypy: 仍是list[Any]
    
    x.append("hello")  # Pyright: 错误!
                       # mypy: OK (list[Any])
```

### 功能对比表

```python
"""
功能对比
"""

# | 功能 | Pyright | mypy |
# |------|---------|------|
# | 速度 | ★★★★★ | ★★★☆☆ |
# | 类型推断 | ★★★★★ | ★★★★☆ |
# | 错误信息 | ★★★★★ | ★★★★☆ |
# | PEP支持 | ★★★★★ | ★★★★☆ |
# | 配置灵活性 | ★★★★☆ | ★★★★★ |
# | 社区支持 | ★★★★☆ | ★★★★★ |
# | 文档 | ★★★★☆ | ★★★★★ |
# | CI/CD | ★★★★★ | ★★★★★ |

# 推荐使用场景:
# Pyright: VSCode开发, 追求速度, 新项目
# mypy: 成熟项目, 需要灵活配置, PyCharm

# 也可以两者都用:
# - 开发时: Pyright (VSCode)
# - CI: mypy (更稳定)
```

---

## VSCode集成

### Pylance设置

```json
// .vscode/settings.json
{
  // 启用Pylance
  "python.languageServer": "Pylance",
  
  // 类型检查模式
  "python.analysis.typeCheckingMode": "strict",
  // 可选: "off", "basic", "standard", "strict"
  
  // 自动导入补全
  "python.analysis.autoImportCompletions": true,
  
  // 导入格式
  "python.analysis.importFormat": "absolute",
  
  // 诊断模式
  "python.analysis.diagnosticMode": "workspace",
  // "openFilesOnly" - 只检查打开的文件
  
  // 额外路径
  "python.analysis.extraPaths": [],
  
  // 存根路径
  "python.analysis.stubPath": "typings",
  
  // 索引
  "python.analysis.indexing": true,
  
  // 内存限制
  "python.analysis.memory.keepLibraryAst": false,
  
  // 诊断严重性覆盖
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingImports": "error",
    "reportMissingTypeStubs": "warning",
    "reportUnusedImport": "information",
    "reportUnusedVariable": "warning",
    "reportGeneralTypeIssues": "error",
    "reportOptionalMemberAccess": "error",
    "reportOptionalSubscript": "error",
    "reportPrivateImportUsage": "warning"
  },
  
  // 类型检查时忽略的规则
  "python.analysis.ignore": ["**/node_modules", "**/__pycache__"],
  
  // Inlay hints
  "python.analysis.inlayHints.variableTypes": true,
  "python.analysis.inlayHints.functionReturnTypes": true,
  "python.analysis.inlayHints.parameterTypes": true
}
```

### 实时类型提示

```python
"""
VSCode中的实时类型检查
"""

# 1. 鼠标悬停显示类型
def greet(name: str) -> str:
    return f"Hello, {name}"

# 悬停在greet上: (name: str) -> str

# 2. 错误波浪线
result = greet(123)  # 红色波浪线

# 3. 自动补全
user = {"name": "Alice", "age": 30}
print(user["n"])  # 自动提示"name"

# 4. 类型推断
numbers = [1, 2, 3]
# 悬停在numbers上: list[int]

# 5. Inlay hints
def add(x: int, y: int):
    return x + y  # 显示: -> int

# 6. 问题面板
# Ctrl+Shift+M 查看所有类型错误

# 7. 快速修复
# 点击灯泡图标或Ctrl+.
```

---

## 高级特性

### 类型细化

```python
"""
Pyright的高级类型细化
"""

# 1. isinstance细化
def process(value: int | str | None) -> str:
    if isinstance(value, str):
        # Pyright知道这里value是str
        return value.upper()
    elif isinstance(value, int):
        # 这里value是int
        return str(value * 2)
    else:
        # 这里value是None
        return "empty"

# 2. is None细化
def handle(value: str | None) -> str:
    if value is None:
        return "default"
    # 这里value是str
    return value.upper()

# 3. assert细化
def func(value: str | None) -> str:
    assert value is not None
    # 这里value是str
    return value.upper()

# 4. 类型守卫
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process_list(items: list[object]) -> None:
    if is_str_list(items):
        # Pyright知道items是list[str]
        print(items[0].upper())

# 5. Literal细化
from typing import Literal

Mode = Literal["read", "write"]

def open_file(mode: Mode) -> None:
    if mode == "read":
        # 这里mode是Literal["read"]
        pass
    else:
        # 这里mode是Literal["write"]
        pass
```

### 注释指令

```python
"""
Pyright注释指令
"""

# 1. 忽略错误
result = some_untyped_function()  # type: ignore

# 2. 忽略特定错误
result = some_untyped_function()  # type: ignore[reportGeneralTypeIssues]

# 3. pyright注释 (推荐)
result = some_untyped_function()  # pyright: ignore

# 4. pyright特定规则
result = some_untyped_function()  # pyright: ignore[reportGeneralTypeIssues]

# 5. 文件级忽略
# pyright: basic
# 或
# pyright: strict

# 6. reveal_type
from typing import reveal_type

x = [1, 2, 3]
reveal_type(x)  # Type of "x" is "list[int]"

# 7. assert_type (Python 3.11+)
from typing import assert_type

def get_value() -> int:
    return 42

result = get_value()
assert_type(result, int)  # ✅ OK
```

### 性能优化

```python
"""
Pyright性能优化
"""

# 1. 限制检查范围
# pyrightconfig.json:
# {
#   "include": ["src"],
#   "exclude": ["tests", "build", "dist"]
# }

# 2. 使用基本模式
# pyrightconfig.json:
# {
#   "typeCheckingMode": "basic"  # 而非strict
# }

# 3. 禁用不需要的诊断
# pyrightconfig.json:
# {
#   "reportMissingTypeStubs": false,
#   "reportUnknownMemberType": false
# }

# 4. 使用.venv
# 避免扫描全局包

# 5. 增量检查
# VSCode会自动增量检查

# 6. 内存优化
# VSCode settings.json:
# {
#   "python.analysis.memory.keepLibraryAst": false
# }
```

---

## 📚 核心要点

### Pyright基础

- ✅ **快速**: TypeScript实现，速度快
- ✅ **严格**: 默认更严格的类型检查
- ✅ **完整**: 支持所有最新PEP
- ✅ **VSCode**: 完美集成(Pylance)

### 配置

- ✅ **pyrightconfig.json**: 项目配置
- ✅ **pyproject.toml**: 也支持
- ✅ **typeCheckingMode**: off/basic/standard/strict
- ✅ **灵活报告**: 精细控制诊断

### vs mypy

- ✅ **速度**: Pyright更快
- ✅ **类型推断**: Pyright更强
- ✅ **PEP支持**: Pyright更快
- ✅ **灵活性**: mypy更灵活
- ✅ **社区**: mypy更成熟

### VSCode集成

- ✅ **Pylance**: 语言服务器
- ✅ **实时检查**: 即时反馈
- ✅ **自动补全**: 智能提示
- ✅ **Inlay hints**: 类型提示

### 高级特性

- ✅ **类型细化**: 强大的类型推断
- ✅ **TypeGuard**: 自定义守卫
- ✅ **注释指令**: 灵活控制
- ✅ **性能优化**: 快速检查

### 最佳实践

- ✅ 开发用Pyright，CI用mypy
- ✅ 合理设置typeCheckingMode
- ✅ 限制检查范围提高性能
- ✅ 使用reveal_type调试
- ✅ 善用类型细化

---

**掌握Pyright，享受极速类型检查！** ⚡✨

**相关文档**:
- [04-mypy.md](04-mypy.md) - mypy类型检查器
- [05-typing-best-practices.md](05-typing-best-practices.md) - 类型最佳实践

**最后更新**: 2025年10月28日

