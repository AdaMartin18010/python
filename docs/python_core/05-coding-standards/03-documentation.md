# Python 文档字符串与注释

**Documentation完全指南**

---

## 📋 目录

- [文档字符串基础](#文档字符串基础)
- [文档风格](#文档风格)
- [注释最佳实践](#注释最佳实践)
- [文档生成](#文档生成)
- [示例](#示例)

---

## 文档字符串基础

### 什么是Docstring

```python
"""
Docstring (文档字符串) 是Python的官方文档方式
"""

def function():
    """这是一个文档字符串"""
    pass

# 访问docstring
print(function.__doc__)
# 输出: 这是一个文档字符串

# 特点:
# 1. 使用三引号 """..."""
# 2. 紧跟定义后的第一行
# 3. 可以被help()显示
# 4. 可以被工具提取
# 5. 支持多行

# ✅ 单行docstring
def greet(name: str) -> str:
    """返回问候语"""
    return f"Hello, {name}"

# ✅ 多行docstring
def calculate_total(items: list[int]) -> int:
    """
    计算列表项总和
    
    这是详细描述
    """
    return sum(items)
```

### PEP 257规范

```python
"""
PEP 257: Docstring Conventions
"""

# 规则1: 使用三双引号 """
def good():
    """Good docstring"""
    pass

def bad():
    '''Bad docstring'''  # 不推荐单引号
    pass

# 规则2: 单行docstring在同一行
def good():
    """Do something"""
    pass

def bad():
    """
    Do something
    """  # 单行不要换行
    pass

# 规则3: 多行docstring格式
def good():
    """
    Summary line.
    
    Detailed description starts here.
    """
    pass

# 规则4: 类的docstring
class MyClass:
    """
    Class summary.
    
    Detailed class description.
    """
    
    def method(self):
        """Method summary."""
        pass

# 规则5: 模块docstring
"""
Module docstring at the top of file.

This module does something useful.
"""

import os
import sys
```

---

## 文档风格

### Google风格

```python
"""
Google Style Docstrings (推荐)
"""

def function(arg1: int, arg2: str, arg3: bool = False) -> dict:
    """函数简短描述 (一行概括)
    
    可选的详细描述,解释函数做什么、为什么这样做。
    可以多行。
    
    Args:
        arg1: 第一个参数的描述
        arg2: 第二个参数的描述
        arg3: 第三个参数的描述. Defaults to False.
    
    Returns:
        返回值的描述,说明返回什么类型和含义
    
    Raises:
        ValueError: 当arg1为负数时抛出
        TypeError: 当arg2不是字符串时抛出
    
    Examples:
        >>> function(1, "hello")
        {'result': 'success'}
        
        >>> function(-1, "world")
        Traceback (most recent call last):
            ...
        ValueError: arg1 must be positive
    
    Note:
        这是一个注意事项
    
    Warning:
        这是一个警告
    """
    if arg1 < 0:
        raise ValueError("arg1 must be positive")
    return {'result': 'success'}

# Google风格 - 类
class User:
    """用户类
    
    管理用户数据和行为的类。
    
    Attributes:
        name: 用户名
        email: 用户邮箱
        age: 用户年龄
    
    Examples:
        >>> user = User("Alice", "alice@example.com", 30)
        >>> user.name
        'Alice'
    """
    
    def __init__(self, name: str, email: str, age: int):
        """初始化User实例
        
        Args:
            name: 用户名
            email: 用户邮箱
            age: 用户年龄
        """
        self.name = name
        self.email = email
        self.age = age
```

### NumPy风格

```python
"""
NumPy Style Docstrings
"""

def function(arg1, arg2, arg3=False):
    """
    函数简短描述
    
    详细描述段落,解释函数的行为和用途。
    可以包含多个段落。
    
    Parameters
    ----------
    arg1 : int
        第一个参数的描述
    arg2 : str
        第二个参数的描述
    arg3 : bool, optional
        第三个参数的描述 (default is False)
    
    Returns
    -------
    dict
        返回值描述
    
    Raises
    ------
    ValueError
        当arg1为负数时
    TypeError
        当arg2不是字符串时
    
    See Also
    --------
    other_function : 相关函数
    
    Notes
    -----
    这里是注释,可以包含算法说明、复杂度分析等。
    
    Examples
    --------
    >>> function(1, "hello")
    {'result': 'success'}
    
    >>> function(-1, "world")
    Traceback (most recent call last):
        ...
    ValueError: arg1 must be positive
    """
    pass
```

### Sphinx (reStructuredText)风格

```python
"""
Sphinx/reST Style Docstrings
"""

def function(arg1, arg2, arg3=False):
    """
    函数简短描述
    
    详细描述段落。
    
    :param arg1: 第一个参数描述
    :type arg1: int
    :param arg2: 第二个参数描述
    :type arg2: str
    :param arg3: 第三个参数描述
    :type arg3: bool, optional
    :returns: 返回值描述
    :rtype: dict
    :raises ValueError: 当arg1为负数时
    :raises TypeError: 当arg2不是字符串时
    
    .. note::
       这是一个注释
    
    .. warning::
       这是一个警告
    
    Example:
    
    .. code-block:: python
    
        >>> function(1, "hello")
        {'result': 'success'}
    """
    pass
```

---

## 注释最佳实践

### 何时写注释

```python
"""
何时写注释
"""

# ✅ 解释为什么 (Why)
# 使用二分查找因为数据已排序,O(log n)比线性查找更快
result = binary_search(sorted_list, target)

# ❌ 不要解释是什么 (What) - 代码本身就很清楚
# 设置x为1
x = 1  # 多余

# ✅ 复杂算法说明
def complex_algorithm(data):
    """
    使用动态规划求解最长公共子序列
    
    时间复杂度: O(m*n)
    空间复杂度: O(m*n)
    """
    # 初始化DP表
    dp = [[0] * (len(data[1]) + 1) for _ in range(len(data[0]) + 1)]
    
    # 填充DP表
    for i in range(1, len(data[0]) + 1):
        for j in range(1, len(data[1]) + 1):
            # 如果字符匹配,取左上角+1
            if data[0][i-1] == data[1][j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            # 否则取左边和上边的最大值
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[-1][-1]

# ✅ 警告和陷阱
# 注意: 这个函数会修改原列表!
def sort_in_place(items):
    items.sort()

# ✅ TODO和FIXME
# TODO(username): 实现缓存机制
# FIXME: 当输入为空时会崩溃
# XXX: 这里的实现很hacky,需要重构
```

### 注释风格

```python
"""
注释风格规范
"""

# ✅ 块注释: 完整句子,首字母大写,句号结尾
# This is a block comment explaining the following code section.
# It can span multiple lines.
def function():
    pass

# ✅ 行内注释: 至少两个空格分隔
x = x + 1  # Compensate for border

# ❌ 不要无意义的行内注释
x = x + 1  # Increment x  # 没有额外信息

# ✅ 段落注释: 用空行分隔
# First paragraph explaining something.
#
# Second paragraph explaining something else.

# ✅ 章节注释
# ============================================================================
# Section 1: Data Loading
# ============================================================================

# ============================================================================
# Section 2: Data Processing
# ============================================================================

# 或使用更简洁的风格
# --- Data Loading ---

# --- Data Processing ---
```

### 类型提示 vs 注释

```python
"""
类型提示优于注释
"""

# ❌ 旧方式: 用注释说明类型
def greet(name):
    # type: (str) -> str
    """
    Args:
        name (str): The name to greet
    
    Returns:
        str: The greeting message
    """
    return f"Hello, {name}"

# ✅ 新方式: 使用类型注解
def greet(name: str) -> str:
    """
    Args:
        name: The name to greet (类型已在签名中)
    
    Returns:
        The greeting message (类型已在签名中)
    """
    return f"Hello, {name}"

# ✅ 复杂类型也用注解
from typing import Optional, List, Dict

def process_users(
    users: List[Dict[str, str]],
    filter_active: bool = True
) -> Optional[List[str]]:
    """
    处理用户列表
    
    Args:
        users: 用户字典列表
        filter_active: 是否只返回活跃用户
    
    Returns:
        用户名列表,如果没有用户则返回None
    """
    pass
```

---

## 文档生成

### Sphinx文档

```bash
# 安装Sphinx
uv add --dev sphinx sphinx-rtd-theme

# 初始化Sphinx
mkdir docs
cd docs
sphinx-quickstart

# 配置 conf.py
# extensions = [
#     'sphinx.ext.autodoc',
#     'sphinx.ext.napoleon',  # 支持Google/NumPy风格
#     'sphinx.ext.viewcode',
# ]
# html_theme = 'sphinx_rtd_theme'

# 生成API文档
sphinx-apidoc -o source/ ../src/

# 构建HTML文档
make html

# 查看文档
# open build/html/index.html
```

### MkDocs文档

```bash
# 安装MkDocs
uv add --dev mkdocs mkdocs-material mkdocstrings[python]

# 创建配置 mkdocs.yml
cat > mkdocs.yml << EOF
site_name: My Project
theme:
  name: material
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
EOF

# 创建文档结构
mkdir -p docs
cat > docs/index.md << EOF
# Welcome

::: my_package.module
EOF

# 本地预览
mkdocs serve

# 构建
mkdocs build

# 部署到GitHub Pages
mkdocs gh-deploy
```

### pdoc文档

```bash
# 安装pdoc
uv add --dev pdoc

# 生成文档
pdoc --html --output-dir docs/ my_package

# 实时预览
pdoc --http : my_package
```

---

## 示例

### 完整模块示例

```python
"""
用户管理模块

这个模块提供用户管理的核心功能,包括用户创建、验证、查询等。

Examples:
    >>> from my_package import user_service
    >>> user = user_service.create_user("Alice", "alice@example.com")
    >>> user_service.authenticate(user.id, "password")
    True

Attributes:
    MAX_LOGIN_ATTEMPTS (int): 最大登录尝试次数
    SESSION_TIMEOUT (int): 会话超时时间(秒)

Note:
    这个模块依赖于database模块提供的连接。
"""

from typing import Optional
from dataclasses import dataclass

MAX_LOGIN_ATTEMPTS = 3
SESSION_TIMEOUT = 3600


@dataclass
class User:
    """用户数据类
    
    表示系统中的一个用户。
    
    Attributes:
        id: 用户唯一标识符
        username: 用户名
        email: 邮箱地址
        is_active: 用户是否激活
    
    Examples:
        >>> user = User(1, "alice", "alice@example.com", True)
        >>> user.username
        'alice'
    """
    
    id: int
    username: str
    email: str
    is_active: bool = True


def create_user(username: str, email: str) -> User:
    """创建新用户
    
    在数据库中创建一个新用户记录。
    
    Args:
        username: 用户名,必须唯一
        email: 邮箱地址,必须唯一且有效
    
    Returns:
        创建的User对象
    
    Raises:
        ValueError: 如果用户名或邮箱已存在
        ValidationError: 如果邮箱格式无效
    
    Examples:
        >>> user = create_user("alice", "alice@example.com")
        >>> user.username
        'alice'
        
        >>> create_user("", "invalid")
        Traceback (most recent call last):
            ...
        ValueError: Username cannot be empty
    
    Note:
        新创建的用户默认为激活状态。
    """
    if not username:
        raise ValueError("Username cannot be empty")
    
    # 创建用户逻辑
    user = User(
        id=1,  # 实际应从数据库生成
        username=username,
        email=email,
        is_active=True
    )
    
    return user


def authenticate(user_id: int, password: str) -> bool:
    """验证用户身份
    
    Args:
        user_id: 用户ID
        password: 密码
    
    Returns:
        验证是否成功
    
    Raises:
        UserNotFoundError: 如果用户不存在
        AccountLockedError: 如果账户被锁定
    
    Note:
        连续失败MAX_LOGIN_ATTEMPTS次后账户将被锁定。
    
    Warning:
        这个函数不应该暴露给公网API。
    """
    # 验证逻辑
    return True


class UserService:
    """用户服务类
    
    提供高级用户管理功能。
    
    Attributes:
        db_connection: 数据库连接
        cache: 缓存实例
    
    Examples:
        >>> service = UserService()
        >>> user = service.get_user_by_email("alice@example.com")
        >>> service.update_user(user.id, {"username": "alice_new"})
    """
    
    def __init__(self, db_connection=None):
        """初始化用户服务
        
        Args:
            db_connection: 数据库连接,如果为None则使用默认连接
        """
        self.db_connection = db_connection
        self.cache = {}
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """通过邮箱查找用户
        
        Args:
            email: 要查找的邮箱地址
        
        Returns:
            找到的User对象,如果不存在则返回None
        
        Examples:
            >>> service = UserService()
            >>> user = service.get_user_by_email("alice@example.com")
            >>> user.username if user else None
            'alice'
        """
        # 查找逻辑
        return None
```

---

## 📚 核心要点

### Docstring基础

- ✅ **三引号**: 使用"""
- ✅ **位置**: 紧跟定义
- ✅ **访问**: __doc__属性
- ✅ **工具**: help()函数

### 文档风格

- ✅ **Google**: 推荐,清晰简洁
- ✅ **NumPy**: 科学计算常用
- ✅ **Sphinx**: 传统,功能强大
- ✅ **一致性**: 项目统一风格

### 注释原则

- ✅ **Why not What**: 解释为什么
- ✅ **复杂算法**: 说明逻辑
- ✅ **警告**: 标注陷阱
- ✅ **TODO**: 标记待办
- ✅ **类型注解**: 优于注释

### 文档生成

- ✅ **Sphinx**: 传统强大
- ✅ **MkDocs**: 现代简洁
- ✅ **pdoc**: 快速简单
- ✅ **自动化**: CI/CD集成

### 最佳实践

- ✅ 公开API必须有docstring
- ✅ 类型注解替代类型文档
- ✅ 提供使用示例
- ✅ 说明异常情况
- ✅ 保持文档更新

---

**好的文档是代码的说明书！** 📚✨

**相关文档**:
- [01-pep8.md](01-pep8.md) - PEP 8代码风格
- [02-naming.md](02-naming.md) - 命名约定

**最后更新**: 2025年10月28日

