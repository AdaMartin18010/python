# Python 代码审查检查清单

**Code Review完全指南**

---

## 📋 目录

- [代码审查原则](#代码审查原则)
- [检查清单](#检查清单)
- [常见问题](#常见问题)
- [审查流程](#审查流程)
- [工具支持](#工具支持)

---

## 代码审查原则

### 为什么需要代码审查

```python
"""
代码审查的价值
"""

# 价值:
# 1. 提高代码质量
# 2. 发现潜在bug
# 3. 知识共享
# 4. 统一编码风格
# 5. 团队协作
# 6. 技能提升

# 审查重点:
# ✅ 正确性: 代码是否正确实现功能
# ✅ 可读性: 代码是否易于理解
# ✅ 可维护性: 代码是否易于修改
# ✅ 性能: 是否有明显的性能问题
# ✅ 安全性: 是否有安全隐患
# ✅ 测试: 是否有足够的测试

# 审查态度:
# ✅ 建设性: 提供建设性反馈
# ✅ 尊重: 尊重作者的工作
# ✅ 学习: 相互学习提高
# ✅ 客观: 对事不对人
```

---

## 检查清单

### 1. 代码风格

```python
"""
代码风格检查
"""

# ☐ PEP 8符合性
# - 缩进: 4个空格
# - 行长度: 79-100字符
# - 空行: 函数间2行,方法间1行
# - 导入: 分组和排序

# ☐ 命名约定
# - 类名: CapWords
# - 函数/变量: lowercase_with_underscores
# - 常量: UPPERCASE
# - 私有: _leading_underscore

# ✅ Good
class UserService:
    MAX_RETRIES = 3
    
    def __init__(self):
        self._connection = None
    
    def get_user(self, user_id: int) -> User:
        pass
    
    def _internal_method(self):
        pass

# ❌ Bad
class user_service:  # 类名应该CapWords
    maxRetries = 3  # 常量应该UPPERCASE
    
    def GetUser(self, UserID):  # 方法应该lowercase
        pass
```

### 2. 类型注解

```python
"""
类型注解检查
"""

# ☐ 公开API有类型注解
# ☐ 复杂函数有类型注解
# ☐ 使用现代语法 (Python 3.10+)
# ☐ mypy/pyright检查通过

# ✅ Good
def process_users(
    users: list[dict[str, str]],
    filter_active: bool = True
) -> list[str]:
    """处理用户列表"""
    return [u["name"] for u in users if u.get("active", True)]

# ❌ Bad
def process_users(users, filter_active=True):
    """处理用户列表"""  # 缺少类型注解
    return [u["name"] for u in users if u.get("active", True)]

# ✅ Good - 使用新语法
def merge_dicts(d1: dict[str, int], d2: dict[str, int]) -> dict[str, int]:
    return d1 | d2

# ❌ Bad - 旧语法
from typing import Dict
def merge_dicts(d1: Dict[str, int], d2: Dict[str, int]) -> Dict[str, int]:
    return {**d1, **d2}
```

### 3. 文档和注释

```python
"""
文档检查
"""

# ☐ 公开API有docstring
# ☐ 复杂逻辑有注释
# ☐ TODO/FIXME标记清晰
# ☐ 文档与代码一致

# ✅ Good
def calculate_discount(
    price: float,
    discount_rate: float,
    membership_level: str
) -> float:
    """计算折扣后价格
    
    Args:
        price: 原价
        discount_rate: 基础折扣率 (0.0-1.0)
        membership_level: 会员等级 ("bronze", "silver", "gold")
    
    Returns:
        折扣后的价格
    
    Raises:
        ValueError: 如果discount_rate不在0-1之间
    
    Examples:
        >>> calculate_discount(100, 0.1, "gold")
        81.0  # 10% discount + 10% membership bonus
    """
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")
    
    # 会员额外折扣
    membership_bonus = {
        "bronze": 0.0,
        "silver": 0.05,
        "gold": 0.10,
    }.get(membership_level, 0.0)
    
    total_discount = discount_rate + membership_bonus
    return price * (1 - min(total_discount, 1.0))

# ❌ Bad - 缺少文档
def calculate_discount(price, discount_rate, membership_level):
    bonus = {"bronze": 0, "silver": 0.05, "gold": 0.10}.get(membership_level, 0)
    return price * (1 - min(discount_rate + bonus, 1.0))
```

### 4. 错误处理

```python
"""
错误处理检查
"""

# ☐ 捕获具体异常
# ☐ 不吞没异常
# ☐ 合适的异常类型
# ☐ 资源正确清理

# ✅ Good
def read_config(filename: str) -> dict:
    """读取配置文件"""
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {filename}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        raise ConfigError(f"Invalid config file: {filename}") from e

# ❌ Bad
def read_config(filename):
    try:
        f = open(filename)  # 没有with,资源可能泄漏
        return json.load(f)
    except:  # 裸except
        pass  # 吞没异常
```

### 5. 性能

```python
"""
性能检查
"""

# ☐ 避免不必要的计算
# ☐ 合适的数据结构
# ☐ 避免过早优化
# ☐ 明显的性能问题

# ✅ Good - 使用集合查找 O(1)
def has_duplicates(items: list[int]) -> bool:
    """检查是否有重复元素"""
    return len(items) != len(set(items))

# ❌ Bad - 嵌套循环 O(n²)
def has_duplicates(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False

# ✅ Good - 列表推导
squares = [x * x for x in range(100)]

# ❌ Bad - 显式循环
squares = []
for x in range(100):
    squares.append(x * x)

# ✅ Good - 生成器 (大数据)
def read_large_file(filename):
    with open(filename) as f:
        for line in f:  # 生成器,内存高效
            yield line.strip()

# ❌ Bad - 一次性读取
def read_large_file(filename):
    with open(filename) as f:
        return f.readlines()  # 可能耗尽内存
```

### 6. 安全性

```python
"""
安全性检查
"""

# ☐ 输入验证
# ☐ SQL注入防护
# ☐ XSS防护
# ☐ 密码加密
# ☐ 敏感数据处理

# ✅ Good - 参数化查询
def get_user(user_id: int) -> User:
    """安全的数据库查询"""
    query = "SELECT * FROM users WHERE id = ?"
    return db.execute(query, (user_id,)).fetchone()

# ❌ Bad - SQL注入风险
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # 危险!
    return db.execute(query).fetchone()

# ✅ Good - 密码哈希
from passlib.hash import bcrypt

def create_user(username: str, password: str):
    password_hash = bcrypt.hash(password)
    db.save_user(username, password_hash)

# ❌ Bad - 明文密码
def create_user(username, password):
    db.save_user(username, password)  # 明文存储!

# ✅ Good - 输入验证
from pydantic import BaseModel, EmailStr, Field

class UserInput(BaseModel):
    email: EmailStr
    age: int = Field(ge=0, le=150)

# ❌ Bad - 无验证
def create_user(email, age):
    # 直接使用,没有验证
    save_to_db(email, age)
```

### 7. 测试

```python
"""
测试检查
"""

# ☐ 单元测试覆盖
# ☐ 边界条件测试
# ☐ 异常情况测试
# ☐ 集成测试

# ✅ Good - 完整测试
def test_calculate_discount():
    """测试折扣计算"""
    
    # 正常情况
    assert calculate_discount(100, 0.1, "gold") == 81.0
    
    # 边界条件
    assert calculate_discount(100, 0.0, "bronze") == 100.0
    assert calculate_discount(100, 1.0, "gold") == 0.0
    
    # 异常情况
    with pytest.raises(ValueError):
        calculate_discount(100, -0.1, "gold")
    
    with pytest.raises(ValueError):
        calculate_discount(100, 1.5, "gold")

# ❌ Bad - 只测试正常情况
def test_calculate_discount():
    assert calculate_discount(100, 0.1, "gold") == 81.0
    # 缺少边界和异常测试
```

---

## 常见问题

### 代码坏味道

```python
"""
识别代码坏味道
"""

# 1. 神秘命名
# ❌ Bad
def calc(a, b, c):
    return a * b * c

# ✅ Good
def calculate_box_volume(length: float, width: float, height: float) -> float:
    return length * width * height

# 2. 过长函数
# ❌ Bad - 函数太长 (>50行)
def process_order(order):
    # 100+ lines of code
    pass

# ✅ Good - 拆分成小函数
def process_order(order: Order) -> OrderResult:
    validate_order(order)
    calculate_total(order)
    apply_discounts(order)
    process_payment(order)
    send_confirmation(order)
    return OrderResult(success=True)

# 3. 重复代码
# ❌ Bad
def send_email(to, subject, body):
    # 发送邮件代码
    pass

def send_sms(to, message):
    # 发送短信代码
    pass

# ✅ Good - 提取公共逻辑
def send_notification(to: str, message: str, channel: str):
    if channel == "email":
        send_via_email(to, message)
    elif channel == "sms":
        send_via_sms(to, message)

# 4. 过深嵌套
# ❌ Bad
def process(data):
    if data:
        if validate(data):
            if transform(data):
                if save(data):
                    return True
    return False

# ✅ Good - 早返回
def process(data: Data) -> bool:
    if not data:
        return False
    if not validate(data):
        return False
    if not transform(data):
        return False
    return save(data)

# 5. 魔法数字
# ❌ Bad
if age > 18:
    pass

if status == 1:
    pass

# ✅ Good
ADULT_AGE = 18
if age > ADULT_AGE:
    pass

class Status(Enum):
    PENDING = 1
    ACTIVE = 2

if status == Status.ACTIVE:
    pass
```

---

## 审查流程

### Pull Request检查清单

```markdown
## PR Description
- [ ] 清晰描述变更内容
- [ ] 关联相关Issue/Ticket
- [ ] 说明测试方法

## Code Quality
- [ ] 符合PEP 8代码风格
- [ ] 命名清晰有意义
- [ ] 有适当的类型注解
- [ ] 有必要的文档和注释

## Functionality
- [ ] 代码正确实现需求
- [ ] 边界条件处理正确
- [ ] 错误处理完善
- [ ] 无明显bug

## Testing
- [ ] 有单元测试
- [ ] 测试覆盖边界情况
- [ ] 测试覆盖异常情况
- [ ] 所有测试通过

## Performance
- [ ] 无明显性能问题
- [ ] 使用合适的数据结构
- [ ] 避免不必要的计算

## Security
- [ ] 输入验证完善
- [ ] 无SQL注入风险
- [ ] 敏感数据正确处理
- [ ] 权限检查完整

## Documentation
- [ ] README更新(如需要)
- [ ] API文档更新(如需要)
- [ ] Changelog更新(如需要)

## CI/CD
- [ ] 所有CI检查通过
- [ ] Linter检查通过
- [ ] 类型检查通过
- [ ] 测试覆盖率满足要求
```

### 审查反馈模板

```markdown
## Summary
<!-- 总体评价 -->
代码整体质量良好,建议进行以下改进...

## Critical Issues
<!-- 必须修改的问题 -->
- [ ] **安全**: SQL注入风险 (line 45)
- [ ] **Bug**: 空值未处理 (line 78)

## Suggestions
<!-- 建议改进的地方 -->
- 建议使用类型注解提高可读性 (line 12)
- 考虑提取重复代码 (line 34-56)
- 函数过长,建议拆分 (function_name)

## Nits
<!-- 小问题 -->
- 命名可以更清晰 (line 23)
- 缺少空行 (line 67)

## Positive Feedback
<!-- 好的地方 -->
- 测试覆盖很完整 ✨
- 错误处理很规范 👍
- 文档写得很清楚 📝

## Questions
<!-- 疑问 -->
- 为什么选择这种实现方式?(line 45)
- 这个性能优化是必要的吗?(line 89)
```

---

## 工具支持

### 自动化检查

```yaml
# .github/workflows/code-review.yml
name: Code Review

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install ruff mypy pytest pytest-cov
      
      - name: Run ruff
        run: ruff check src/
      
      - name: Run mypy
        run: mypy src/
      
      - name: Run tests
        run: pytest --cov=src tests/
      
      - name: Check coverage
        run: pytest --cov=src --cov-fail-under=80 tests/
```

### pre-commit配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.10.0
    hooks:
      - id: black
  
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.0
    hooks:
      - id: mypy
  
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

---

## 📚 核心要点

### 审查原则

- ✅ **建设性**: 提供建设性反馈
- ✅ **尊重**: 尊重作者工作
- ✅ **学习**: 相互学习提高
- ✅ **客观**: 对事不对人

### 检查重点

- ✅ **风格**: PEP 8, 命名
- ✅ **类型**: 类型注解
- ✅ **文档**: Docstring, 注释
- ✅ **错误**: 异常处理
- ✅ **性能**: 数据结构, 算法
- ✅ **安全**: 输入验证, SQL注入
- ✅ **测试**: 单元测试, 覆盖率

### 代码坏味道

- ❌ 神秘命名
- ❌ 过长函数
- ❌ 重复代码
- ❌ 过深嵌套
- ❌ 魔法数字

### 审查流程

- ✅ **PR描述**: 清晰说明
- ✅ **自动检查**: CI/CD
- ✅ **人工审查**: 逻辑正确性
- ✅ **反馈**: 建设性意见

### 工具支持

- ✅ **ruff**: Linter
- ✅ **mypy**: 类型检查
- ✅ **pytest**: 测试
- ✅ **pre-commit**: Git hooks
- ✅ **GitHub Actions**: CI/CD

---

**高质量代码审查提升团队水平！** 👥✨

**相关文档**:
- [01-pep8.md](01-pep8.md) - PEP 8代码风格
- [05-error-handling.md](05-error-handling.md) - 错误处理

**最后更新**: 2025年10月28日

