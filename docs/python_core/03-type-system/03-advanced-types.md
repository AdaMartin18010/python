# Python 高级类型特性

**类型系统高级主题**

---

## 📋 目录

- [递归类型](#递归类型)
- [Self类型](#Self类型)
- [NewType](#NewType)
- [类型别名高级用法](#类型别名高级用法)
- [类型变换](#类型变换)

---

## 递归类型

### JSON类型定义

```python
"""
递归类型定义
"""
from typing import TypeAlias

# JSON类型 - 递归定义
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

def parse_json(data: str) -> JSON:
    """解析JSON"""
    import json
    return json.loads(data)

def validate_json(obj: JSON) -> bool:
    """验证JSON对象"""
    if isinstance(obj, dict):
        return all(validate_json(v) for v in obj.values())
    elif isinstance(obj, list):
        return all(validate_json(item) for item in obj)
    return True

# 使用
data: JSON = {
    "name": "Alice",
    "age": 30,
    "children": [
        {"name": "Bob", "age": 5},
        {"name": "Charlie", "age": 3}
    ]
}
```

### 树结构

```python
"""
递归树结构
"""
from typing import Generic, TypeVar
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class TreeNode(Generic[T]):
    """二叉树节点"""
    value: T
    left: "TreeNode[T] | None" = None
    right: "TreeNode[T] | None" = None

def tree_height(node: TreeNode[T] | None) -> int:
    """计算树高度"""
    if node is None:
        return 0
    left_height = tree_height(node.left)
    right_height = tree_height(node.right)
    return 1 + max(left_height, right_height)

# 使用
root: TreeNode[int] = TreeNode(
    value=1,
    left=TreeNode(2, TreeNode(4), TreeNode(5)),
    right=TreeNode(3)
)

height = tree_height(root)  # 3

# 链表
@dataclass
class ListNode(Generic[T]):
    """链表节点"""
    value: T
    next: "ListNode[T] | None" = None

def list_length(node: ListNode[T] | None) -> int:
    """计算链表长度"""
    if node is None:
        return 0
    return 1 + list_length(node.next)
```

---

## Self类型

### Self类型基础 (Python 3.11+)

```python
"""
Self: 返回自身类型
"""
from typing import Self

class Builder:
    """建造者模式"""
    
    def __init__(self):
        self._config: dict[str, str] = {}
    
    def set_option(self, key: str, value: str) -> Self:
        """设置选项"""
        self._config[key] = value
        return self
    
    def build(self) -> dict[str, str]:
        """构建"""
        return self._config.copy()

# 链式调用
config = (Builder()
    .set_option("host", "localhost")
    .set_option("port", "8080")
    .build())

# 继承场景
class AdvancedBuilder(Builder):
    """高级建造者"""
    
    def set_advanced_option(self, key: str) -> Self:
        """高级选项"""
        self._config[key] = "advanced"
        return self

# Self自动推断为AdvancedBuilder
advanced = (AdvancedBuilder()
    .set_option("host", "localhost")
    .set_advanced_option("feature")
    .build())
```

### 类方法中的Self

```python
"""
类方法返回Self
"""
from typing import Self
from dataclasses import dataclass

@dataclass
class Point:
    """点"""
    x: float
    y: float
    
    @classmethod
    def origin(cls) -> Self:
        """原点"""
        return cls(0.0, 0.0)
    
    @classmethod
    def from_tuple(cls, coords: tuple[float, float]) -> Self:
        """从元组创建"""
        return cls(coords[0], coords[1])
    
    def translate(self, dx: float, dy: float) -> Self:
        """平移"""
        return type(self)(self.x + dx, self.y + dy)

# 使用
p1 = Point.origin()
p2 = Point.from_tuple((3.0, 4.0))
p3 = p2.translate(1.0, 1.0)

# 继承
class Point3D(Point):
    """3D点"""
    z: float = 0.0

# origin()返回Point3D类型
origin_3d = Point3D.origin()  # type: Point3D
```

---

## NewType

### NewType基础

```python
"""
NewType: 创建不同的类型
"""
from typing import NewType

# 创建新类型
UserId = NewType('UserId', int)
Username = NewType('Username', str)

def get_user_name(user_id: UserId) -> Username:
    """根据ID获取用户名"""
    # 实际实现
    return Username("Alice")

# 使用
user_id = UserId(12345)
name = get_user_name(user_id)

# 类型安全
# name = get_user_name(12345)  # ❌ mypy error: 需要UserId
# user_id2: UserId = 67890      # ❌ 需要显式转换

# 运行时: NewType只是identity函数
assert UserId(42) == 42  # True
assert type(UserId(42)) == int  # True
```

### NewType应用场景

```python
"""
NewType实际应用
"""
from typing import NewType

# 1. 区分语义相似的类型
Email = NewType('Email', str)
PhoneNumber = NewType('PhoneNumber', str)

def send_email(to: Email, subject: str) -> None:
    """发送邮件"""
    print(f"Sending email to {to}")

def send_sms(to: PhoneNumber, message: str) -> None:
    """发送短信"""
    print(f"Sending SMS to {to}")

# 类型安全
email = Email("alice@example.com")
phone = PhoneNumber("+1234567890")

send_email(email, "Hello")
send_sms(phone, "Hi")

# send_email(phone, "Hello")  # ❌ 类型错误

# 2. 增强类型安全
HTML = NewType('HTML', str)
SQL = NewType('SQL', str)

def render_html(html: HTML) -> str:
    """渲染HTML"""
    return f"<html>{html}</html>"

def execute_sql(query: SQL) -> list[dict]:
    """执行SQL"""
    # 实际执行
    return []

# 防止混淆
html = HTML("<p>Hello</p>")
sql = SQL("SELECT * FROM users")

render_html(html)  # ✅
execute_sql(sql)   # ✅
# render_html(sql)  # ❌ 类型错误

# 3. 验证过的类型
ValidatedEmail = NewType('ValidatedEmail', str)

def validate_email(email: str) -> ValidatedEmail | None:
    """验证邮箱"""
    if "@" in email and "." in email:
        return ValidatedEmail(email)
    return None

def send_validated_email(to: ValidatedEmail) -> None:
    """发送已验证的邮箱"""
    # 确保邮箱已验证
    print(f"Sending to {to}")

# 使用
email_str = "alice@example.com"
validated = validate_email(email_str)
if validated:
    send_validated_email(validated)  # ✅ 类型安全
```

---

## 类型别名高级用法

### 泛型类型别名

```python
"""
泛型类型别名
"""
from typing import TypeVar, TypeAlias, Generic

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# 泛型别名
Stack: TypeAlias = list[T]
Queue: TypeAlias = list[T]

def push(stack: Stack[int], item: int) -> None:
    """压栈"""
    stack.append(item)

# 多参数泛型别名
Pair: TypeAlias = tuple[T, T]
KeyValue: TypeAlias = tuple[K, V]

def create_pair(x: T, y: T) -> Pair[T]:
    """创建对"""
    return (x, y)

def create_kv(k: K, v: V) -> KeyValue[K, V]:
    """创建键值对"""
    return (k, v)

# Python 3.12+ 新语法
type Stack[T] = list[T]
type Pair[T] = tuple[T, T]
type KeyValue[K, V] = tuple[K, V]
```

### 条件类型别名

```python
"""
条件类型别名
"""
from typing import TypeAlias, Literal

# 字面量类型别名
HTTPMethod: TypeAlias = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
Status: TypeAlias = Literal["pending", "running", "success", "failed"]

def make_request(url: str, method: HTTPMethod) -> dict:
    """发送HTTP请求"""
    return {"url": url, "method": method}

# 复杂条件类型
ResponseData: TypeAlias = dict[str, str | int | bool | None]

def process_response(data: ResponseData) -> None:
    """处理响应"""
    for key, value in data.items():
        if isinstance(value, str):
            print(f"{key}: {value.upper()}")
        elif isinstance(value, int):
            print(f"{key}: {value * 2}")
```

---

## 类型变换

### Annotated类型

```python
"""
Annotated: 添加元数据 (Python 3.9+)
"""
from typing import Annotated, get_type_hints, get_args

# 添加元数据
UserId = Annotated[int, "User ID", "positive"]
Username = Annotated[str, "Username", "max_length:50"]

def create_user(user_id: UserId, username: Username) -> None:
    """创建用户"""
    print(f"Creating user {user_id}: {username}")

# 获取元数据
hints = get_type_hints(create_user, include_extras=True)
print(hints)  # {'user_id': Annotated[int, ...], ...}

user_id_meta = get_args(hints['user_id'])
print(user_id_meta)  # (int, 'User ID', 'positive')

# 与Pydantic结合
from pydantic import BaseModel, Field

class User(BaseModel):
    """用户模型"""
    id: Annotated[int, Field(gt=0, description="User ID")]
    name: Annotated[str, Field(max_length=50, description="Username")]
    email: Annotated[str, Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")]
```

### Required和NotRequired (Python 3.11+)

```python
"""
Required和NotRequired: TypedDict的必需/可选字段
"""
from typing import TypedDict, Required, NotRequired

# 默认所有字段必需
class User(TypedDict):
    """用户"""
    name: str
    age: int
    email: NotRequired[str]  # 可选

user1: User = {"name": "Alice", "age": 30}  # ✅
user2: User = {"name": "Bob", "age": 25, "email": "bob@example.com"}  # ✅

# 默认所有字段可选
class PartialUser(TypedDict, total=False):
    """部分用户"""
    name: str
    age: int
    email: Required[str]  # 必需

partial: PartialUser = {"email": "alice@example.com"}  # ✅
```

### ReadOnly (Python 3.13+)

```python
"""
ReadOnly: 只读字段 (Python 3.13+)
"""
from typing import TypedDict, ReadOnly

class Config(TypedDict):
    """配置"""
    host: ReadOnly[str]
    port: ReadOnly[int]
    debug: bool

config: Config = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}

# 类型检查器会警告修改只读字段
# config["host"] = "newhost"  # ❌ mypy warning
config["debug"] = False  # ✅ OK
```

---

## 📚 核心要点

### 递归类型

- ✅ **JSON类型**: 递归定义复杂结构
- ✅ **树结构**: 二叉树、N叉树
- ✅ **链表**: 单链表、双链表
- ✅ **字符串引用**: 使用引号

### Self类型

- ✅ **链式调用**: 返回self类型
- ✅ **类方法**: classmethod返回类型
- ✅ **继承**: 自动推断子类类型
- ✅ **Python 3.11+**: Self关键字

### NewType

- ✅ **类型区分**: 相同底层类型不同语义
- ✅ **零成本**: 运行时无开销
- ✅ **类型安全**: 编译时检查
- ✅ **应用**: Email, UserId, HTML等

### 类型别名

- ✅ **泛型别名**: TypeAlias + TypeVar
- ✅ **Python 3.12+**: type语句
- ✅ **条件类型**: Literal组合
- ✅ **可读性**: 简化复杂类型

### 类型变换

- ✅ **Annotated**: 添加元数据
- ✅ **Required/NotRequired**: 字段可选性
- ✅ **ReadOnly**: 只读字段
- ✅ **Pydantic**: 数据验证

---

**掌握高级类型，构建强大类型系统！** 🚀✨

**相关文档**:
- [01-type-hints-basics.md](01-type-hints-basics.md) - 类型注解基础
- [02-generics-protocols.md](02-generics-protocols.md) - 泛型与协议

**最后更新**: 2025年10月28日

