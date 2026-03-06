# PEP 705: TypedDict ReadOnly 标记

> Python 3.13 新特性 - 为 TypedDict 添加只读支持

---

## 概述

**PEP 705** 引入了 `typing.ReadOnly` 类型修饰符，允许将 `TypedDict` 的特定字段标记为只读。

**发布版本**: Python 3.13+
**PEP链接**: [PEP 705](https://peps.python.org/pep-0705/)

**核心优势**:

- ✅ 在类型层面防止意外修改
- ✅ 表达不可变数据结构
- ✅ 支持协变（covariant）类型检查
- ✅ 更好的 API 契约表达

---

## 基础概念

### 什么是 ReadOnly？

`ReadOnly` 是一个特殊的类型修饰符，用于标记 `TypedDict` 中的字段为只读：

```python
from typing import TypedDict, ReadOnly

class Config(TypedDict):
    # 普通字段 - 可读写
    debug: bool

    # 只读字段 - 只能读取
    version: ReadOnly[str]
    created_at: ReadOnly[str]

# 使用
config: Config = {
    "debug": True,
    "version": "1.0.0",
    "created_at": "2025-01-01"
}

# OK: 修改非只读字段
config["debug"] = False

# 类型错误: 不能修改只读字段
# config["version"] = "2.0.0"  # Error!
```

---

## 语法详解

### 基本用法

```python
from typing import TypedDict, ReadOnly

class User(TypedDict):
    # 可写字段
    name: str
    email: str

    # 只读字段
    id: ReadOnly[int]
    created_at: ReadOnly[str]
    is_verified: ReadOnly[bool]

# 创建时赋值
user: User = {
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com",
    "created_at": "2025-01-01",
    "is_verified": True
}

# 可以修改可写字段
user["name"] = "Alice Smith"
user["email"] = "alice.smith@example.com"

# 不能修改只读字段
# user["id"] = 456  # 类型错误！
# user["created_at"] = "2025-02-01"  # 类型错误！
```

### 嵌套结构

```python
from typing import TypedDict, ReadOnly

class Address(TypedDict):
    street: str
    city: str
    postal_code: ReadOnly[str]  # 邮编通常是固定的

class Person(TypedDict):
    name: str
    # 只读嵌套结构
    address: ReadOnly[Address]
    ssn: ReadOnly[str]  # 社会安全号码不可变

person: Person = {
    "name": "Bob",
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "postal_code": "10001"
    },
    "ssn": "123-45-6789"
}

# 可以修改 name
person["name"] = "Robert"

# 不能直接替换 address（因为它是 ReadOnly）
# person["address"] = {...}  # 错误！

# 但是可以修改 address 内部的非只读字段
person["address"]["street"] = "456 Oak Ave"  # OK
person["address"]["city"] = "Boston"  # OK

# 不能修改 address 内部的只读字段
# person["address"]["postal_code"] = "02101"  # 错误！
```

---

## 实战模式

### 模式 1: API 响应类型

```python
from typing import TypedDict, ReadOnly

class APIResponse(TypedDict):
    """API 响应 - 服务器返回的数据应该是只读的"""
    # 元数据 - 只读
    status_code: ReadOnly[int]
    request_id: ReadOnly[str]
    timestamp: ReadOnly[str]

    # 数据 - 只读
    data: ReadOnly[dict]

    # 客户端可以修改的缓存标记
    cached: bool

# 从服务器获取响应
def fetch_user(user_id: int) -> APIResponse:
    return {
        "status_code": 200,
        "request_id": "req-12345",
        "timestamp": "2025-01-15T10:30:00Z",
        "data": {"id": user_id, "name": "Alice"},
        "cached": False
    }

response = fetch_user(123)

# 可以修改缓存标记
response["cached"] = True

# 不能修改服务器返回的数据
# response["status_code"] = 404  # 类型错误！
# response["data"]["id"] = 456   # 如果 data 也是只读的，这会报错
```

### 模式 2: 配置对象

```python
from typing import TypedDict, ReadOnly, NotRequired

class AppConfig(TypedDict):
    """应用配置 - 某些项启动后不可更改"""

    # 运行时只读配置
    app_name: ReadOnly[str]
    version: ReadOnly[str]
    build_timestamp: ReadOnly[str]
    environment: ReadOnly[str]  # production, staging, development

    # 运行时动态配置（可修改）
    debug_mode: bool
    log_level: str
    max_connections: int

    # 可选配置
    custom_header: NotRequired[str]
    timeout_seconds: NotRequired[int]

# 加载配置
config: AppConfig = load_config_from_file("config.json")

# 可以修改运行时配置
config["debug_mode"] = True
config["log_level"] = "DEBUG"

# 不能修改只读配置
# config["app_name"] = "NewName"  # 类型错误！
# config["environment"] = "test"  # 类型错误！
```

### 模式 3: 数据库记录

```python
from typing import TypedDict, ReadOnly
from datetime import datetime

class UserRecord(TypedDict):
    """用户数据库记录 - 某些字段由数据库管理"""

    # 数据库管理的字段（只读）
    id: ReadOnly[int]
    created_at: ReadOnly[str]
    updated_at: ReadOnly[str]
    version: ReadOnly[int]  # 乐观锁版本号

    # 用户可修改的字段
    username: str
    email: str
    display_name: str
    bio: str
    is_active: bool

class UserRepository:
    def find_by_id(self, user_id: int) -> UserRecord:
        # 从数据库查询
        return {
            "id": user_id,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-15T10:30:00Z",
            "version": 1,
            "username": "alice",
            "email": "alice@example.com",
            "display_name": "Alice",
            "bio": "Software developer",
            "is_active": True
        }

    def update(self, user: UserRecord) -> None:
        """更新用户 - 数据库字段不应被修改"""
        # 实际实现会验证 version 字段进行乐观锁检查
        print(f"Updating user {user['id']} with version {user['version']}")
        # UPDATE users SET ... WHERE id = ? AND version = ?

# 使用
repo = UserRepository()
user = repo.find_by_id(123)

# 可以修改用户信息
user["display_name"] = "Alice Smith"
user["bio"] = "Senior Software Developer"

# 不能修改数据库管理的字段
# user["id"] = 456  # 类型错误！
# user["version"] = 2  # 类型错误！

repo.update(user)
```

### 模式 4: 不可变状态管理

```python
from typing import TypedDict, ReadOnly, TypeVar, Generic

T = TypeVar("T")

class StateSnapshot(TypedDict, Generic[T]):
    """状态快照 - 不可变的历史记录"""
    value: ReadOnly[T]
    timestamp: ReadOnly[str]
    action: ReadOnly[str]

class StateHistory(Generic[T]):
    """状态历史管理器"""

    def __init__(self, initial: T) -> None:
        self._snapshots: list[StateSnapshot[T]] = []
        self._current_value = initial

    def commit(self, action: str) -> None:
        """提交当前状态"""
        from datetime import datetime
        snapshot: StateSnapshot[T] = {
            "value": self._current_value,
            "timestamp": datetime.now().isoformat(),
            "action": action
        }
        self._snapshots.append(snapshot)

    def get_history(self) -> list[StateSnapshot[T]]:
        """获取只读的历史记录"""
        return self._snapshots.copy()

    @property
    def current(self) -> T:
        return self._current_value

    @current.setter
    def current(self, value: T) -> None:
        self._current_value = value

# 使用
history = StateHistory[int](0)

history.current = 10
history.commit("increment")

history.current = 20
history.commit("increment")

history.current = 15
history.commit("decrement")

# 查看历史 - 历史记录是只读的
for snapshot in history.get_history():
    print(f"{snapshot['timestamp']}: {snapshot['action']} → {snapshot['value']}")
    # 不能修改历史
    # snapshot["value"] = 999  # 类型错误！
```

---

## 高级用法

### 继承与覆盖

```python
from typing import TypedDict, ReadOnly

class BaseItem(TypedDict):
    id: ReadOnly[int]
    created_at: ReadOnly[str]

class EditableItem(BaseItem):
    """可编辑的项目 - 继承只读字段"""
    name: str
    description: str
    # id 和 created_at 仍然保持 ReadOnly

class FrozenItem(BaseItem):
    """完全冻结的项目 - 所有字段只读"""
    name: ReadOnly[str]
    description: ReadOnly[str]

# 使用
editable: EditableItem = {
    "id": 1,
    "created_at": "2025-01-01",
    "name": "Item 1",
    "description": "Description"
}

editable["name"] = "New Name"  # OK
# editable["id"] = 2  # 错误！

frozen: FrozenItem = {
    "id": 1,
    "created_at": "2025-01-01",
    "name": "Item 1",
    "description": "Description"
}

# frozen["name"] = "New Name"  # 错误！
# frozen["id"] = 2  # 错误！
```

### 与 NotRequired 结合

```python
from typing import TypedDict, ReadOnly, NotRequired

class Document(TypedDict):
    # 必需且只读
    id: ReadOnly[int]

    # 可选且只读（创建后可能不提供）
    original_filename: ReadOnly[NotRequired[str]]

    # 必需且可写
    title: str
    content: str

    # 可选且可写
    tags: NotRequired[list[str]]

    # 只读且可选 - 自动生成
    word_count: ReadOnly[NotRequired[int]]

# 创建文档
doc: Document = {
    "id": 1,
    "title": "My Document",
    "content": "Document content..."
}

# 可以添加可选字段
doc["tags"] = ["python", "typing"]

# 不能修改只读字段，即使它们是 NotRequired
# doc["original_filename"] = "doc.txt"  # 如果创建时没提供，之后也不能添加？
# 实际上可以添加，但不能修改
```

---

## 类型检查行为

### 协变（Covariance）

```python
from typing import TypedDict, ReadOnly

class Animal(TypedDict):
    name: ReadOnly[str]

class Dog(Animal):
    breed: ReadOnly[str]

class Cat(Animal):
    color: ReadOnly[str]

# ReadOnly 字段支持协变
def process_animal(animal: Animal) -> None:
    print(animal["name"])

dog: Dog = {"name": "Buddy", "breed": "Golden Retriever"}
cat: Cat = {"name": "Whiskers", "color": "orange"}

process_animal(dog)  # OK
process_animal(cat)  # OK
```

### 赋值兼容性

```python
from typing import TypedDict, ReadOnly

class MutablePoint(TypedDict):
    x: int
    y: int

class ImmutablePoint(TypedDict):
    x: ReadOnly[int]
    y: ReadOnly[int]

# 可变 → 不可变：OK
mutable: MutablePoint = {"x": 1, "y": 2}
immutable: ImmutablePoint = mutable  # OK

# 不可变 → 可变：错误
# mutable2: MutablePoint = immutable  # 类型错误！
# 因为 ReadOnly[int] 不是 int 的子类型
```

---

## 最佳实践

### ✅ 应该做的

1. **为标识符和元数据使用 ReadOnly**

   ```python
   class User(TypedDict):
       id: ReadOnly[int]
       uuid: ReadOnly[str]
       created_at: ReadOnly[str]
   ```

2. **为派生数据使用 ReadOnly**

   ```python
   class Order(TypedDict):
       items: list[OrderItem]
       total: ReadOnly[float]  # 从 items 计算得出
   ```

3. **为外部系统提供的数据使用 ReadOnly**

   ```python
   class DatabaseRecord(TypedDict):
       id: ReadOnly[int]
       version: ReadOnly[int]  # 乐观锁
   ```

### ❌ 不应该做的

1. **不要过度使用 ReadOnly**

   ```python
   # 不好：几乎所有字段都是 ReadOnly
   class TooRestrictive(TypedDict):
       field1: ReadOnly[str]
       field2: ReadOnly[int]
       field3: ReadOnly[bool]
   ```

2. **不要将可变集合标记为 ReadOnly 然后修改它们**

   ```python
   class BadExample(TypedDict):
       items: ReadOnly[list[int]]  # 列表本身可变！

   obj: BadExample = {"items": [1, 2, 3]}
   obj["items"].append(4)  # 这会成功！ReadOnly 只保护引用
   ```

---

## 兼容性

| Python 版本 | 支持情况 |
|-------------|----------|
| 3.13+ | ✅ 原生支持 `typing.ReadOnly` |
| 3.12 | ❌ 不支持 |
| <3.12 | ❌ 不支持 |

### 向后兼容方案

```python
import sys

if sys.version_info >= (3, 13):
    from typing import ReadOnly
else:
    # 对于旧版本，ReadOnly 是透明传递的
    T = TypeVar("T")
    ReadOnly = lambda x: x  # 类型: ignore

# 使用
class MyDict(TypedDict):
    field: ReadOnly[str]
```

---

## 与其他语言的对比

| 语言 | 只读字典/对象 |
|------|--------------|
| Python (3.13+) | `ReadOnly[T]` in `TypedDict` |
| TypeScript | `readonly` 修饰符 |
| Rust | 所有权和借用系统 |
| Swift | `let` vs `var` |

Python 的 `ReadOnly` 设计类似于 TypeScript 的 `readonly`，但仅适用于 `TypedDict`。

---

## 延伸阅读

- [PEP 705 - TypedDict ReadOnly](https://peps.python.org/pep-0705/)
- [PEP 692 - TypedDict with Unpack](https://peps.python.org/pep-0692/)
- [Python typing 文档](https://docs.python.org/3/library/typing.html)

---

**使用 ReadOnly，构建更清晰、更安全的数据模型！** 🔒📊
