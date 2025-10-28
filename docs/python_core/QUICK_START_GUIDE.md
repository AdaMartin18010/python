# Python Core 快速开始指南

**5分钟快速上手 Python Core 文档体系**

---

## 🎯 选择你的学习路径

### 我是初学者 👶

**推荐顺序**:
1. [数据模型与对象系统](01-language-core/01-data-model.md) - 理解Python一切皆对象
2. [类型注解基础](03-type-system/01-type-hints-basics.md) - 学习现代类型注解
3. [PEP 8代码风格](05-coding-standards/01-pep8.md) - 掌握编码规范
4. [pip包管理基础](04-package-management/01-pip-basics.md) - 管理依赖包
5. [表达式语义](02-syntax-semantics/03-expressions.md) - 理解Python表达式

**预计学习时间**: 2-3小时

---

### 我是进阶开发者 💻

**推荐顺序**:
1. [泛型与协议](03-type-system/02-generics-protocols.md) - 掌握泛型编程
2. [装饰器与元编程](02-syntax-semantics/07-decorators-metaprogramming.md) - 高级特性
3. [uv极速包管理器](04-package-management/03-uv.md) - 10-100x faster!
4. [错误处理最佳实践](05-coding-standards/05-error-handling.md) - 健壮代码
5. [Pydantic数据验证](03-type-system/06-pydantic.md) - 数据验证

**预计学习时间**: 3-4小时

---

### 我是专家级开发者 🚀

**推荐顺序**:
1. [执行模型与字节码](01-language-core/04-execution-model.md) - 深入理解Python
2. [高级类型特性](03-type-system/03-advanced-types.md) - Self, NewType等
3. [Poetry现代包管理](04-package-management/02-poetry.md) - 现代化工作流
4. [代码审查检查清单](05-coding-standards/06-code-review.md) - 提升代码质量
5. [内存模型与GC](01-language-core/03-memory-model.md) - 性能优化

**预计学习时间**: 4-5小时

---

## 📚 按主题学习

### 🔤 类型系统 (最推荐✨)

**为什么要学习类型系统**?
- ✅ 提前发现bug
- ✅ 更好的IDE支持
- ✅ 代码更易维护
- ✅ 文档化代码

**学习顺序**:
1. [类型注解基础](03-type-system/01-type-hints-basics.md) ⭐ 必读
2. [泛型与协议](03-type-system/02-generics-protocols.md) ⭐
3. [mypy静态检查](03-type-system/04-mypy.md)
4. [类型注解最佳实践](03-type-system/05-typing-best-practices.md) ⭐
5. [Pydantic数据验证](03-type-system/06-pydantic.md)
6. [Pyright类型检查器](03-type-system/07-pyright.md)

**预计时间**: 3-4小时  
**难度**: ⭐⭐⭐☆☆

---

### 📦 包管理工具 (极速体验⚡)

**为什么要学习包管理**?
- ⚡ uv比pip快10-100倍
- 📦 Poetry现代化工作流
- 🔒 依赖锁定保证可重现
- 🚀 提升开发效率

**学习顺序**:
1. [uv极速包管理器](04-package-management/03-uv.md) ⭐ 必读
2. [Poetry现代包管理](04-package-management/02-poetry.md) ⭐
3. [虚拟环境管理](04-package-management/04-virtual-env.md)
4. [Requirements依赖管理](04-package-management/05-requirements.md)
5. [包发布与分发](04-package-management/06-publishing.md)

**预计时间**: 2-3小时  
**难度**: ⭐⭐☆☆☆

---

### 📐 编码规范 (团队协作必备👥)

**为什么要学习编码规范**?
- 👥 团队协作更顺畅
- 📝 代码更易阅读
- 🔍 减少代码审查时间
- ✅ 自动化工具支持

**学习顺序**:
1. [PEP 8代码风格](05-coding-standards/01-pep8.md) ⭐ 必读
2. [命名约定与规范](05-coding-standards/02-naming.md) ⭐
3. [文档字符串与注释](05-coding-standards/03-documentation.md)
4. [导入规范与组织](05-coding-standards/04-imports.md)
5. [错误处理最佳实践](05-coding-standards/05-error-handling.md)
6. [代码审查检查清单](05-coding-standards/06-code-review.md) ⭐

**预计时间**: 3-4小时  
**难度**: ⭐⭐☆☆☆

---

## 🔥 热门话题

### 🚀 uv - 极速包管理器

```bash
# 安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 比pip快10-100倍！
uv pip install requests  # 0.3s vs pip 2.5s
uv pip compile requirements.in  # 0.5s vs 45s

# 完全兼容pip命令
uv pip install -r requirements.txt
uv pip list
uv pip show requests
```

**推荐阅读**: [uv极速包管理器](04-package-management/03-uv.md)

---

### 🔤 Python 3.12+ 新泛型语法

```python
# 旧语法 (Python 3.11-)
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def push(self, item: T) -> None: ...

# 新语法 (Python 3.12+)
class Stack[T]:
    def push(self, item: T) -> None: ...

# type语句
type Vector = list[float]
type Matrix = list[Vector]
```

**推荐阅读**: [泛型与协议](03-type-system/02-generics-protocols.md)

---

### 📊 Pydantic数据验证

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

# 自动验证
user = User(id=1, name="Alice", email="alice@example.com")

# 验证失败自动报错
try:
    invalid = User(id=-1, name="", email="invalid")
except ValidationError as e:
    print(e)
```

**推荐阅读**: [Pydantic数据验证](03-type-system/06-pydantic.md)

---

## 🎓 学习技巧

### 1. 边学边练

**不要只看文档，一定要实践！**

```bash
# 创建练习项目
mkdir python-practice
cd python-practice
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装工具
pip install ruff black mypy

# 写代码练习
vim practice.py
```

### 2. 使用自动化工具

**让工具帮你学习规范！**

```bash
# 自动格式化
black practice.py

# 检查代码
ruff check practice.py

# 类型检查
mypy practice.py
```

### 3. 参考真实项目

**看看开源项目怎么做的**:
- FastAPI: https://github.com/tiangolo/fastapi
- httpx: https://github.com/encode/httpx
- rich: https://github.com/Textualize/rich

### 4. 循序渐进

**不要一次学太多！**

- 📅 Day 1: 类型注解基础
- 📅 Day 2: PEP 8代码风格
- 📅 Day 3: uv包管理器
- 📅 Day 4: 错误处理
- 📅 Day 5: 代码审查

---

## 🔗 快速链接

### 必读文档 ⭐⭐⭐⭐⭐

1. [类型注解基础](03-type-system/01-type-hints-basics.md)
2. [PEP 8代码风格](05-coding-standards/01-pep8.md)
3. [uv极速包管理器](04-package-management/03-uv.md)
4. [类型注解最佳实践](03-type-system/05-typing-best-practices.md)
5. [命名约定与规范](05-coding-standards/02-naming.md)

### 进阶必读 ⭐⭐⭐⭐☆

1. [泛型与协议](03-type-system/02-generics-protocols.md)
2. [装饰器与元编程](02-syntax-semantics/07-decorators-metaprogramming.md)
3. [Pydantic数据验证](03-type-system/06-pydantic.md)
4. [错误处理最佳实践](05-coding-standards/05-error-handling.md)
5. [代码审查检查清单](05-coding-standards/06-code-review.md)

### 深度理解 ⭐⭐⭐⭐⭐

1. [数据模型与对象系统](01-language-core/01-data-model.md)
2. [内存模型与GC](01-language-core/03-memory-model.md)
3. [执行模型与字节码](01-language-core/04-execution-model.md)
4. [高级类型特性](03-type-system/03-advanced-types.md)

---

## 💡 常见问题

### Q1: 我应该先学什么？

**A**: 如果你是：
- 🆕 **新手**: 从[数据模型](01-language-core/01-data-model.md)开始
- 💻 **有经验**: 从[类型系统](03-type-system/01-type-hints-basics.md)开始
- 🚀 **专家**: 直接看[高级特性](03-type-system/03-advanced-types.md)

### Q2: 需要多长时间学完？

**A**: 根据你的目标：
- ⏱️ **快速入门**: 5-6小时 (必读文档)
- ⏱️ **全面掌握**: 20-30小时 (所有文档)
- ⏱️ **精通**: 持续实践

### Q3: 文档会更新吗？

**A**: 
- ✅ 是的！我们会持续更新
- ✅ 跟进Python新版本
- ✅ 添加更多实战案例
- ✅ 优化现有内容

### Q4: 如何获得帮助？

**A**:
- 📖 查看[主README](README.md)
- 🔍 使用文档内搜索
- 💬 提交Issue
- 👥 加入社区讨论

---

## 🎯 学习目标检查

完成学习后，你应该能够：

### 基础级 ✅

- [ ] 理解Python对象模型
- [ ] 使用类型注解
- [ ] 遵循PEP 8规范
- [ ] 使用pip/uv管理包
- [ ] 编写清晰的代码

### 进阶级 ✅

- [ ] 掌握泛型编程
- [ ] 使用装饰器和元编程
- [ ] 配置Poetry/uv工作流
- [ ] 实现正确的错误处理
- [ ] 进行代码审查

### 专家级 ✅

- [ ] 深入理解Python执行模型
- [ ] 掌握高级类型特性
- [ ] 优化代码性能
- [ ] 发布Python包
- [ ] 指导团队开发

---

## 🚀 开始学习

**准备好了吗？选择你的路径，开始学习吧！**

1. 📚 [查看完整目录](README.md)
2. 🎯 [选择学习路径](#选择你的学习路径)
3. 💻 动手实践
4. 🎓 持续进步

---

**祝你学习愉快！** 🐍✨

**最后更新**: 2025年10月28日

