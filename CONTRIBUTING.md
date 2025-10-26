# 🤝 贡献指南 - Python 2025 Knowledge Base

感谢您对 **Python 2025 Ultimate Knowledge Base** 的关注！我们欢迎所有形式的贡献。

---

## 📋 目录

- [行为准则](#-行为准则)
- [如何贡献](#-如何贡献)
- [贡献类型](#-贡献类型)
- [开发流程](#-开发流程)
- [代码规范](#-代码规范)
- [提交指南](#-提交指南)
- [审查流程](#-审查流程)

---

## 📜 行为准则

### 我们的承诺

为了营造开放和友好的环境，我们承诺：

- ✅ 使用友好和包容的语言
- ✅ 尊重不同的观点和经验
- ✅ 优雅地接受建设性批评
- ✅ 关注对社区最有利的事情
- ✅ 对其他社区成员表示同理心

### 不可接受的行为

- ❌ 使用性化的语言或图像
- ❌ 人身攻击或侮辱性评论
- ❌ 公开或私下骚扰
- ❌ 未经许可发布他人私人信息
- ❌ 其他不道德或不专业的行为

---

## 🎯 如何贡献

### 快速开始

```bash
# 1. Fork 本仓库
# 在GitHub上点击 "Fork" 按钮

# 2. 克隆你的Fork
git clone https://github.com/YOUR_USERNAME/python-2025-knowledge-base.git
cd python-2025-knowledge-base

# 3. 添加上游仓库
git remote add upstream https://github.com/ORIGINAL_OWNER/python-2025-knowledge-base.git

# 4. 创建特性分支
git checkout -b feature/amazing-feature

# 5. 进行修改
# ... 编辑文件 ...

# 6. 提交更改
git add .
git commit -m "Add amazing feature"

# 7. 推送到你的Fork
git push origin feature/amazing-feature

# 8. 创建Pull Request
# 在GitHub上创建PR
```

---

## 🎨 贡献类型

### 1. 📝 文档改进

**适合所有人！**

- 修正拼写错误
- 改进说明文字
- 添加使用示例
- 翻译文档

**示例**:

```bash
# 编辑文档
vim README.md

# 提交
git commit -m "docs: fix typo in README"
```

### 2. 💻 代码示例

**提供更多实用示例**

- 添加新的代码示例
- 改进现有示例
- 优化实现方式

**示例**:

```bash
# 添加示例
touch 02-design-patterns/01-creational/singleton/examples/advanced_example.py

# 提交
git commit -m "feat: add advanced singleton example"
```

### 3. 🐛 Bug修复

**发现并修复问题**

- 修复代码错误
- 修复文档错误
- 修复配置问题

**示例**:

```bash
# 修复bug
vim 05-formal-methods/type-theory/type_theory.py

# 提交
git commit -m "fix: correct type annotation in Container class"
```

### 4. ✨ 新功能

**添加新模块或功能**

- 实现新的设计模式
- 添加新的算法
- 扩展技术栈覆盖

**示例**:

```bash
# 创建新模块
mkdir -p 02-design-patterns/new-pattern
touch 02-design-patterns/new-pattern/README.md

# 提交
git commit -m "feat: add new design pattern"
```

### 5. 🧪 测试

**提高代码质量**

- 添加单元测试
- 添加集成测试
- 提高测试覆盖率

**示例**:

```bash
# 添加测试
touch 02-design-patterns/01-creational/singleton/tests/test_advanced.py

# 提交
git commit -m "test: add advanced singleton tests"
```

### 6. 📊 基准测试

**性能优化**

- 添加性能测试
- 对比不同实现
- 优化算法性能

**示例**:

```bash
# 添加基准测试
touch 03-algorithms-data-structures/01-sorting/quick-sort/benchmarks/compare.py

# 提交
git commit -m "perf: add performance benchmarks for quick sort"
```

---

## 🔧 开发流程

### 环境配置

```bash
# 1. 安装UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建虚拟环境
uv venv --python 3.12

# 3. 激活环境
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 4. 安装依赖
uv sync --all-extras
```

### 开发工作流

```bash
# 1. 同步上游最新代码
git fetch upstream
git checkout main
git merge upstream/main

# 2. 创建特性分支
git checkout -b feature/my-feature

# 3. 进行开发
# ... 编辑文件 ...

# 4. 运行测试
uv run pytest

# 5. 代码格式化
uv run ruff format .

# 6. 代码检查
uv run ruff check .

# 7. 类型检查
uv run mypy src/

# 8. 提交代码
git add .
git commit -m "feat: add my feature"

# 9. 推送到Fork
git push origin feature/my-feature

# 10. 创建Pull Request
```

---

## 📏 代码规范

### Python代码规范

遵循 [PEP 8](https://pep8.org/) 和项目特定规范：

#### 1. 类型提示

```python
# ✅ 好
def process_data(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ❌ 差
def process_data(items):
    return {item: len(item) for item in items}
```

#### 2. 现代语法

```python
# ✅ 好：使用 | 而非 Optional
def get_value(key: str) -> str | None:
    return None

# ❌ 差：使用旧式Optional
from typing import Optional
def get_value(key: str) -> Optional[str]:
    return None
```

#### 3. Docstring

```python
# ✅ 好
def calculate_sum(numbers: list[int]) -> int:
    """
    Calculate the sum of a list of integers.
    
    Args:
        numbers: List of integers to sum
        
    Returns:
        Sum of all numbers
        
    Example:
        >>> calculate_sum([1, 2, 3])
        6
    """
    return sum(numbers)
```

#### 4. 命名规范

```python
# ✅ 好
class UserManager:
    def get_user_by_id(self, user_id: int) -> User | None:
        pass

MAX_RETRY_COUNT = 3
default_timeout = 30

# ❌ 差
class usermanager:
    def GetUserByID(self, userId: int):
        pass
```

### 文档规范

#### Markdown格式

```markdown
# ✅ 好的标题层次

## 主要章节

### 子章节

#### 详细说明

# ✅ 好的代码块

​```python
def example():
    return "Hello"
​```

# ✅ 好的列表

- 项目1
- 项目2
  - 子项目2.1
  - 子项目2.2
```

---

## 📝 提交指南

### Commit Message格式

遵循 [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型 (Type)

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例

```bash
# 好的提交消息
feat(singleton): add thread-safe implementation
fix(adapter): correct type annotation in PaymentGateway
docs(readme): update installation instructions
test(observer): add unit tests for event bus
perf(quicksort): optimize parallel sorting algorithm

# 详细的提交消息
feat(type-theory): add Result type implementation

- Implement Result[T, E] type similar to Rust
- Add ok() and err() factory methods
- Include map() and unwrap() operations
- Add comprehensive examples

Closes #123
```

---

## 🔍 审查流程

### Pull Request检查清单

提交PR前，请确保：

- [ ] **代码质量**
  - [ ] 通过所有测试
  - [ ] 通过代码检查 (ruff)
  - [ ] 通过类型检查 (mypy)
  - [ ] 代码已格式化

- [ ] **文档**
  - [ ] 添加/更新README
  - [ ] 添加/更新示例
  - [ ] 添加/更新测试
  - [ ] 更新CHANGELOG

- [ ] **提交**
  - [ ] Commit消息符合规范
  - [ ] PR描述清晰
  - [ ] 引用相关Issue

### PR模板

```markdown
## 描述
简要描述这个PR的目的

## 类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 性能优化
- [ ] 其他

## 更改内容
- 更改1
- 更改2

## 测试
描述如何测试这些更改

## 截图（如适用）
添加截图说明

## 相关Issue
Closes #123
```

### 审查标准

PR会根据以下标准审查：

1. **代码质量** (必须)
   - 符合代码规范
   - 通过所有检查
   - 无明显bug

2. **文档完整** (必须)
   - 有适当的文档
   - 示例清晰
   - 易于理解

3. **测试覆盖** (推荐)
   - 有单元测试
   - 测试覆盖关键路径

4. **性能影响** (如适用)
   - 无负面性能影响
   - 有性能提升证明

---

## 🎁 贡献者

感谢所有贡献者！

### 如何成为贡献者

1. 提交你的第一个PR
2. PR被合并后自动成为贡献者
3. 在README中列出

### 贡献者权益

- ✅ 名字出现在项目中
- ✅ 获得贡献者徽章
- ✅ 参与项目决策
- ✅ 优先的技术支持

---

## 💬 获取帮助

### 沟通渠道

- 📧 **Email**: <your.email@example.com>
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/python-2025-knowledge-base/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/python-2025-knowledge-base/issues)

### 常见问题

**Q: 我不知道从哪里开始？**
A: 查看标记为 `good first issue` 的Issue

**Q: 我的PR多久会被审查？**
A: 通常在3个工作日内

**Q: 如何报告安全问题？**
A: 请发送邮件到 <security@example.com>

---

## 📜 许可证

通过贡献，你同意你的贡献将在与本项目相同的 [MIT License](LICENSE) 下授权。

---

**感谢你的贡献！让我们一起让Python开发更美好！** 🚀

[← 返回主页](README.md)
