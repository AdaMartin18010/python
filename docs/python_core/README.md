# Python 语言核心参考文档 2025

**基于 Python 3.12/3.13 | uv 包管理器 | 最新最佳实践**-

---

## 📚 文档目录

### 🎯 [01 - 语言核心特性](01-language-core/README.md)

Python 语言的核心特性和基础概念

- [1.1 数据模型与对象系统](01-language-core/01-data-model.md)
- [1.2 类型系统](01-language-core/02-type-system.md)
- [1.3 内存模型](01-language-core/03-memory-model.md)
- [1.4 执行模型](01-language-core/04-execution-model.md)
- [1.5 作用域与命名空间](01-language-core/05-scope-namespace.md)

### 📝 [02 - 语法与语义](02-syntax-semantics/README.md)

Python 语法规则和语义模型

- [2.1 词法分析](02-syntax-semantics/01-lexical.md)
- [2.2 语法结构](02-syntax-semantics/02-grammar.md)
- [2.3 表达式语义](02-syntax-semantics/03-expressions.md)
- [2.4 语句语义](02-syntax-semantics/04-statements.md)
- [2.5 函数与闭包](02-syntax-semantics/05-functions-closures.md)
- [2.6 类与继承](02-syntax-semantics/06-classes-inheritance.md)
- [2.7 装饰器与元编程](02-syntax-semantics/07-decorators-metaprogramming.md)

### 🔤 [03 - 类型系统深度解析](03-type-system/README.md)

现代 Python 类型系统全面指南

- [3.1 类型注解基础](03-type-system/01-type-hints-basics.md)
- [3.2 泛型与协议](03-type-system/02-generics-protocols.md)
- [3.3 类型推导](03-type-system/03-type-inference.md)
- [3.4 mypy 静态检查](03-type-system/04-mypy.md)
- [3.5 pyright 类型检查](03-type-system/05-pyright.md)
- [3.6 运行时类型检查](03-type-system/06-runtime-checking.md)
- [3.7 PEP 695 类型参数](03-type-system/07-pep695-type-parameters.md)

### 📦 [04 - 包管理与依赖](04-package-management/README.md)

现代 Python 包管理生态

- [4.1 uv 包管理器](04-package-management/01-uv-package-manager.md)
- [4.2 pip 使用指南](04-package-management/02-pip.md)
- [4.3 poetry 项目管理](04-package-management/03-poetry.md)
- [4.4 pipenv 环境管理](04-package-management/04-pipenv.md)
- [4.5 虚拟环境最佳实践](04-package-management/05-virtual-environments.md)
- [4.6 依赖解析与锁定](04-package-management/06-dependency-resolution.md)
- [4.7 pyproject.toml 配置](04-package-management/07-pyproject-toml.md)

### 📐 [05 - 编程规范](05-coding-standards/README.md)

Python 编程规范和最佳实践

- [5.1 PEP 8 代码风格](05-coding-standards/01-pep8.md)
- [5.2 PEP 257 文档字符串](05-coding-standards/02-pep257-docstrings.md)
- [5.3 命名约定](05-coding-standards/03-naming-conventions.md)
- [5.4 代码组织](05-coding-standards/04-code-organization.md)
- [5.5 注释与文档](05-coding-standards/05-comments-documentation.md)
- [5.6 错误处理](05-coding-standards/06-error-handling.md)
- [5.7 代码审查清单](05-coding-standards/07-code-review-checklist.md)

### 🐍 [06 - Pythonic 惯用法](06-pythonic-idioms/README.md)

Python 惯用法和优雅写法

- [6.1 基础惯用法](06-pythonic-idioms/01-basic-idioms.md)
- [6.2 集合与迭代](06-pythonic-idioms/02-collections-iteration.md)
- [6.3 函数式编程](06-pythonic-idioms/03-functional-programming.md)
- [6.4 上下文管理器](06-pythonic-idioms/04-context-managers.md)
- [6.5 生成器与迭代器](06-pythonic-idioms/05-generators-iterators.md)
- [6.6 异步编程模式](06-pythonic-idioms/06-async-patterns.md)
- [6.7 性能优化技巧](06-pythonic-idioms/07-performance-tips.md)

### 🚀 [07 - Python 3.12/3.13 新特性](07-new-features/README.md)

最新 Python 版本的新特性

- [7.1 Python 3.12 新特性](07-new-features/01-python-3.12.md)
- [7.2 Python 3.13 新特性](07-new-features/02-python-3.13.md)
- [7.3 Free-Threaded 模式](07-new-features/03-free-threaded.md)
- [7.4 JIT 编译器](07-new-features/04-jit-compiler.md)
- [7.5 性能改进总结](07-new-features/05-performance-improvements.md)

### 🔧 [08 - 开发工具链](08-toolchain/README.md)

现代 Python 开发工具

- [8.1 uv 工具链](08-toolchain/01-uv-toolchain.md)
- [8.2 ruff 代码检查](08-toolchain/02-ruff.md)
- [8.3 mypy 类型检查](08-toolchain/03-mypy.md)
- [8.4 pytest 测试框架](08-toolchain/04-pytest.md)
- [8.5 black 代码格式化](08-toolchain/05-black.md)
- [8.6 pre-commit 钩子](08-toolchain/06-pre-commit.md)
- [8.7 IDE 集成](08-toolchain/07-ide-integration.md)

### 📊 [09 - 语义模型](09-semantic-models/README.md)

Python 语义模型和形式化

- [9.1 操作语义](09-semantic-models/01-operational-semantics.md)
- [9.2 指称语义](09-semantic-models/02-denotational-semantics.md)
- [9.3 类型语义](09-semantic-models/03-type-semantics.md)
- [9.4 并发语义](09-semantic-models/04-concurrency-semantics.md)
- [9.5 异常语义](09-semantic-models/05-exception-semantics.md)

### 💡 [10 - 实践案例](10-practical-examples/README.md)

实际应用案例和模式

- [10.1 项目结构模板](10-practical-examples/01-project-structure.md)
- [10.2 常见设计模式](10-practical-examples/02-design-patterns.md)
- [10.3 错误处理模式](10-practical-examples/03-error-handling-patterns.md)
- [10.4 测试策略](10-practical-examples/04-testing-strategies.md)
- [10.5 性能优化案例](10-practical-examples/05-performance-cases.md)

---

## 🎯 快速开始

### 环境准备

```bash
# 安装 uv (推荐)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv

# 创建项目
uv init my-project
cd my-project

# 添加依赖
uv add fastapi uvicorn

# 运行项目
uv run python main.py
```

### Python 版本选择

```bash
# 安装 Python 3.12
uv python install 3.12

# 安装 Python 3.13 (实验性)
uv python install 3.13

# 列出可用版本
uv python list

# 设置项目 Python 版本
uv python pin 3.12
```

---

## 🌟 核心概念速查

### 数据模型

```python
# 一切皆对象
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2  # Point(4, 6)
```

### 类型注解

```python
from typing import TypeVar, Generic, Protocol

T = TypeVar("T")

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
    
    def get(self) -> T:
        return self.value

# Protocol (结构化子类型)
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()
```

### 现代包管理

```toml
# pyproject.toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "mypy>=1.11.0",
    "ruff>=0.6.0",
]
```

---

## 📖 学习路径

### 初学者

1. [数据模型与对象系统](01-language-core/01-data-model.md)
2. [语法结构](02-syntax-semantics/02-grammar.md)
3. [基础惯用法](06-pythonic-idioms/01-basic-idioms.md)
4. [PEP 8 代码风格](05-coding-standards/01-pep8.md)
5. [uv 包管理器](04-package-management/01-uv-package-manager.md)

### 进阶开发者

1. [类型系统深度解析](03-type-system/README.md)
2. [装饰器与元编程](02-syntax-semantics/07-decorators-metaprogramming.md)
3. [生成器与迭代器](06-pythonic-idioms/05-generators-iterators.md)
4. [异步编程模式](06-pythonic-idioms/06-async-patterns.md)
5. [性能优化技巧](06-pythonic-idioms/07-performance-tips.md)

### 专家级

1. [语义模型](09-semantic-models/README.md)
2. [Python 3.13 新特性](07-new-features/02-python-3.13.md)
3. [Free-Threaded 模式](07-new-features/03-free-threaded.md)
4. [JIT 编译器](07-new-features/04-jit-compiler.md)
5. [高级类型系统](03-type-system/07-pep695-type-parameters.md)

---

## 🔗 相关资源

### 官方文档

- [Python 官方文档](https://docs.python.org/3/)
- [PEP 索引](https://peps.python.org/)
- [Python Enhancement Proposals](https://github.com/python/peps)

### 工具文档

- [uv 文档](https://github.com/astral-sh/uv)
- [ruff 文档](https://docs.astral.sh/ruff/)
- [mypy 文档](https://mypy.readthedocs.io/)
- [pytest 文档](https://docs.pytest.org/)

### 社区资源

- [Real Python](https://realpython.com/)
- [Python Weekly](https://www.pythonweekly.com/)
- [Talk Python](https://talkpython.fm/)

---

## 🤝 贡献指南

欢迎贡献！请查看 [贡献指南](../../CONTRIBUTING.md)

### 文档标准

- 使用 Markdown 格式
- 代码示例必须可运行
- 包含类型注解
- 遵循 PEP 8 风格
- 提供实际用例

---

## 📝 更新日志

- **2025-10-24**: 初始版本，覆盖 Python 3.12/3.13
- 基于 uv 包管理器
- 完整的类型系统文档
- 现代化的开发工具链

---

**让我们一起掌握 Python 的精髓！** 🐍✨
