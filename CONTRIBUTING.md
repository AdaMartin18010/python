# 贡献指南

感谢您对 Python 2025 知识库的关注！我们欢迎所有形式的贡献。

---

## 🎯 贡献方式

### 1. 报告问题

如果您发现了bug或有功能建议：

1. 搜索 [Issues](https://github.com/your-org/python-2025-kb/issues) 确认问题未被报告
2. 创建新issue，使用清晰的标题和描述
3. 包含：
   - 重现步骤
   - 期望行为
   - 实际行为
   - 环境信息（OS、Python版本等）

### 2. 提交代码

#### 准备工作

```bash
# 1. Fork 仓库到您的账号

# 2. Clone 您的 fork
git clone https://github.com/YOUR_USERNAME/python-2025-kb.git
cd python-2025-kb

# 3. 添加上游仓库
git remote add upstream https://github.com/your-org/python-2025-kb.git

# 4. 安装开发依赖
make dev
make install-hooks
```

#### 开发流程

```bash
# 1. 创建新分支
git checkout -b feature/amazing-feature

# 2. 进行更改
# 编写代码...

# 3. 运行检查
make format          # 格式化代码
make lint            # 代码检查
make test            # 运行测试
make security        # 安全扫描

# 4. 提交更改
git add .
git commit -m "feat: add amazing feature"

# 5. 推送到您的 fork
git push origin feature/amazing-feature

# 6. 创建 Pull Request
```

---

## 📝 代码规范

### Python 代码风格

我们使用 **Ruff** 进行代码检查和格式化：

```python
# ✅ Good
def calculate_total(items: list[dict]) -> float:
    """Calculate total price of items.
    
    Args:
        items: List of item dictionaries with 'price' key
        
    Returns:
        Total price as float
    """
    return sum(item["price"] for item in items)


# ❌ Bad
def calculate_total(items):
    return sum([item["price"] for item in items])  # 使用列表推导式而非生成器
```

### 类型注解

**必须**使用类型注解：

```python
# ✅ Good
from typing import Optional

def process_user(user_id: int, name: str) -> dict[str, str | int]:
    """Process user data."""
    return {"id": user_id, "name": name}


# ❌ Bad
def process_user(user_id, name):
    return {"id": user_id, "name": name}
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def example_function(param1: int, param2: str) -> bool:
    """Brief description of function.
    
    More detailed explanation if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is negative
        
    Examples:
        >>> example_function(1, "test")
        True
    """
    if param1 < 0:
        raise ValueError("param1 must be non-negative")
    return param2 == "test"
```

### 测试

**所有新功能必须包含测试**：

```python
# tests/test_example.py
import pytest
from mymodule import example_function


def test_example_function_success():
    """Test example_function with valid input."""
    result = example_function(1, "test")
    assert result is True


def test_example_function_invalid_input():
    """Test example_function with invalid input."""
    with pytest.raises(ValueError, match="must be non-negative"):
        example_function(-1, "test")


@pytest.mark.parametrize("param1,param2,expected", [
    (1, "test", True),
    (2, "test", True),
    (1, "other", False),
])
def test_example_function_parametrized(param1, param2, expected):
    """Test example_function with various inputs."""
    result = example_function(param1, param2)
    assert result == expected
```

---

## 🔄 提交规范

我们使用 **Conventional Commits** 规范：

### 提交类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关
- `ci`: CI/CD相关

### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 示例

```bash
# 简单提交
git commit -m "feat: add user authentication"

# 详细提交
git commit -m "feat(auth): add OAuth2.1 support

- Implement OAuth2.1 authorization flow
- Add token refresh mechanism
- Update documentation

Closes #123"

# Breaking change
git commit -m "feat!: change API response format

BREAKING CHANGE: API responses now use snake_case instead of camelCase"
```

---

## 🧪 测试要求

### 测试覆盖率

- 所有新代码必须有测试
- 目标覆盖率：>80%
- 关键路径代码：100%

### 运行测试

```bash
# 运行所有测试
make test

# 运行特定测试
pytest tests/test_example.py

# 生成覆盖率报告
make test-cov

# 查看HTML报告
open htmlcov/index.html
```

### 测试类型

1. **单元测试** - 测试单个函数/类
2. **集成测试** - 测试模块间交互
3. **端到端测试** - 测试完整流程

---

## 📚 文档规范

### README更新

如果您的更改影响用户使用：

1. 更新相关README
2. 添加使用示例
3. 更新快速参考（如适用）

### 代码注释

```python
# ✅ Good - 解释"为什么"
# Use exponential backoff to handle rate limiting
retry_delay = 2 ** attempt

# ❌ Bad - 只说明"做什么"（代码已经很清楚）
# Multiply 2 by attempt
retry_delay = 2 ** attempt
```

---

## 🔒 安全

### 报告安全问题

**请勿**在公开issue中报告安全漏洞。

发送邮件至: security@example.com

### 安全最佳实践

1. 不要提交敏感信息（密钥、密码等）
2. 使用 `.env` 文件存储配置
3. 运行安全扫描：`make security`
4. 定期更新依赖

---

## ✅ Pull Request 检查清单

提交PR前，确保：

- [ ] 代码通过所有测试 (`make test`)
- [ ] 代码通过linting (`make lint`)
- [ ] 代码格式正确 (`make format`)
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 提交信息符合规范
- [ ] PR描述清晰
- [ ] 链接了相关issue（如有）

---

## 🎨 PR模板

创建PR时，请包含：

```markdown
## 描述
简要描述此PR的内容

## 类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 重构
- [ ] 其他

## 更改内容
- 添加了...
- 修复了...
- 更新了...

## 测试
描述如何测试这些更改

## 截图（如适用）
添加截图帮助说明

## 相关Issue
Closes #(issue编号)

## 检查清单
- [ ] 代码通过所有测试
- [ ] 代码通过linting
- [ ] 添加了测试
- [ ] 更新了文档
```

---

## 🌟 贡献者行为准则

### 我们的承诺

为了营造开放友好的环境，我们承诺：

- 使用包容性语言
- 尊重不同观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性暗示的语言或图像
- 侮辱性/贬损性评论，人身或政治攻击
- 公开或私下骚扰
- 未经许可发布他人私人信息
- 其他不道德或不专业的行为

---

## 📧 联系方式

- **GitHub Issues**: https://github.com/your-org/python-2025-kb/issues
- **Discussions**: https://github.com/your-org/python-2025-kb/discussions
- **Email**: team@example.com

---

## 🙏 致谢

感谢所有贡献者！您的贡献使这个项目变得更好。

---

**最后更新**: 2025年10月24日

