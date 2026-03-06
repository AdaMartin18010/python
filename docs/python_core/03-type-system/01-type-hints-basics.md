# Python 类型注解基础

**静态类型注解完全指南**

---

## 📋 目录

- [类型注解概述](#类型注解概述)
- [基础类型注解](#基础类型注解)
- [复合类型](#复合类型)
- [函数注解](#函数注解)
- [类型别名](#类型别名)

---

## 类型注解概述

### 为什么需要类型注解

```python
"""
类型注解的价值
"""

# 没有类型注解
def greet(name):
    return f"Hello, {name}"

# 有类型注解
def greet(name: str) -> str:
    return f"Hello, {name}"

# 类型注解的好处:
# 1. 文档作用: 代码更易读
# 2. 错误检测: 提前发现类型错误
# 3. IDE支持: 更好的代码补全
# 4. 重构支持: 更安全的重构

# 类型注解不影响运行时
result = greet(123)  # 运行时不会报错
print(result)        # Hello, 123

# 但mypy会报错:
# error: Argument 1 to "greet" has incompatible type "int"; expected "str"
```

### 类型注解的历史

```python
"""
类型注解演变史
"""

# Python 3.0+: 函数注解 (PEP 3107)
def func(x: int, y: int) -> int:
    return x + y

# Python 3.5: typing模块 (PEP 484)
from typing import List, Dict

def process(items: List[int]) -> Dict[str, int]:
    return {"count": len(items)}

# Python 3.6: 变量注解 (PEP 526)
name: str = "Alice"
age: int = 30

# Python 3.9: 内置类型泛型 (PEP 585)
def process(items: list[int]) -> dict[str, int]:
    return {"count": len(items)}

# Python 3.10: Union运算符 (PEP 604)
def func(x: int | str) -> int | None:
    pass

# Python 3.12: 泛型语法 (PEP 695)
class Stack[T]:
    def push(self, item: T) -> None:
        pass
```

---

## 基础类型注解

### 内置类型

```python
"""
基础内置类型注解
"""

# 数值类型
count: int = 42
price: float = 19.99
is_active: bool = True
value: complex = 3 + 4j

# 字符串和字节
name: str = "Alice"
data: bytes = b"binary data"
raw: bytearray = bytearray(b"data")

# None类型
result: None = None

# 任意类型 (避免使用)
from typing import Any
value: Any = "anything"

# 示例函数
def calculate_total(price: float, quantity: int) -> float:
    """计算总价"""
    return price * quantity

def is_valid(value: int) -> bool:
    """验证值"""
    return value > 0
```

### 容器类型

```python
"""
容器类型注解
"""

# Python 3.9+ 使用内置类型
from typing import List, Dict, Set, Tuple  # 3.9之前

# 列表
numbers: list[int] = [1, 2, 3, 4, 5]
names: list[str] = ["Alice", "Bob"]

# 字典
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
config: dict[str, str | int] = {"host": "localhost", "port": 8080}

# 集合
tags: set[str] = {"python", "typing", "mypy"}

# 元组 (固定长度)
point: tuple[int, int] = (10, 20)
point3d: tuple[int, int, int] = (10, 20, 30)

# 元组 (可变长度)
numbers: tuple[int, ...] = (1, 2, 3, 4, 5)

# 示例函数
def process_scores(scores: dict[str, int]) -> list[str]:
    """处理分数，返回及格的学生"""
    return [name for name, score in scores.items() if score >= 60]

def create_point(x: int, y: int) -> tuple[int, int]:
    """创建点"""
    return (x, y)
```

---

## 复合类型

### Optional和Union

```python
"""
Optional和Union类型
"""

from typing import Optional, Union

# Optional: 值或None
def find_user(user_id: int) -> Optional[str]:
    """查找用户，可能返回None"""
    if user_id == 1:
        return "Alice"
    return None

# 等价于 Union[str, None]
def find_user(user_id: int) -> Union[str, None]:
    pass

# Python 3.10+ 使用 | 运算符
def find_user(user_id: int) -> str | None:
    """更简洁的语法"""
    pass

# Union: 多种类型之一
def process(value: Union[int, str]) -> str:
    """处理整数或字符串"""
    return str(value)

# Python 3.10+
def process(value: int | str) -> str:
    """使用 | 运算符"""
    return str(value)

# 多个类型
def handle_input(value: int | str | float | None) -> str:
    """处理多种输入类型"""
    if value is None:
        return "empty"
    return str(value)

# 实际应用
def get_config(key: str) -> str | int | bool | None:
    """获取配置，可能是多种类型"""
    config = {
        "host": "localhost",
        "port": 8080,
        "debug": True
    }
    return config.get(key)
```

### Literal类型

```python
"""
Literal: 字面量类型
"""

from typing import Literal

# 限定特定值
Mode = Literal["r", "w", "a", "r+", "w+", "a+"]

def open_file(filename: str, mode: Mode) -> None:
    """打开文件，mode只能是特定值"""
    print(f"Opening {filename} in mode {mode}")

open_file("data.txt", "r")   # ✅ OK
# open_file("data.txt", "x")  # ❌ mypy error

# 布尔字面量
def set_flag(value: Literal[True]) -> None:
    """只接受True"""
    pass

set_flag(True)   # ✅ OK
# set_flag(False) # ❌ mypy error

# 数字字面量
def fibonacci(n: Literal[0, 1, 2, 3, 4, 5]) -> int:
    """小范围斐波那契"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 组合多个Literal
Status = Literal["pending", "running", "success", "failed"]

def update_status(status: Status) -> None:
    """更新状态"""
    print(f"Status: {status}")

# 实际应用: HTTP方法
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

def make_request(url: str, method: HttpMethod) -> dict:
    """发送HTTP请求"""
    return {"url": url, "method": method}
```

### Final类型

```python
"""
Final: 最终类型
"""

from typing import Final

# 常量
MAX_SIZE: Final = 100
API_KEY: Final[str] = "secret-key"

# 不能重新赋值
# MAX_SIZE = 200  # mypy error

# Final类属性
class Config:
    """配置类"""
    MAX_CONNECTIONS: Final = 100
    API_VERSION: Final[str] = "v1"

# Final方法参数
def process(data: Final[list[int]]) -> int:
    """data不应被修改"""
    # data.append(1)  # 可以修改，Final不阻止(仅类型检查)
    return sum(data)

# 实际应用
class Application:
    """应用程序类"""

    # 常量配置
    APP_NAME: Final[str] = "MyApp"
    VERSION: Final[tuple[int, int, int]] = (1, 0, 0)

    def __init__(self, debug: bool = False):
        # 实例常量
        self.debug: Final[bool] = debug
```

---

## 函数注解

### 参数和返回值注解

```python
"""
函数类型注解完整示例
"""

# 1. 基础函数注解
def add(x: int, y: int) -> int:
    """两数相加"""
    return x + y

# 2. 默认参数
def greet(name: str, prefix: str = "Hello") -> str:
    """问候函数"""
    return f"{prefix}, {name}"

# 3. 可变位置参数
def sum_all(*args: int) -> int:
    """求和"""
    return sum(args)

# 4. 可变关键字参数
def create_user(**kwargs: str) -> dict[str, str]:
    """创建用户"""
    return kwargs

# 5. 混合参数
def process(
    required: int,
    *args: int,
    optional: str = "default",
    **kwargs: str | int
) -> tuple[int, list[int], str, dict[str, str | int]]:
    """复杂参数函数"""
    return required, list(args), optional, kwargs

# 6. 仅位置参数 (Python 3.8+)
def func(a: int, b: int, /, c: int) -> int:
    """a, b仅位置; c位置或关键字"""
    return a + b + c

# 7. 仅关键字参数
def func(a: int, *, b: int, c: int) -> int:
    """b, c仅关键字"""
    return a + b + c

# 8. 无返回值
def log(message: str) -> None:
    """记录日志"""
    print(message)

# 9. 生成器函数
from typing import Iterator

def count_up(n: int) -> Iterator[int]:
    """生成器函数"""
    for i in range(n):
        yield i

# 10. 异步函数
from typing import Coroutine

async def fetch_data(url: str) -> str:
    """异步获取数据"""
    # await some_async_operation()
    return "data"
```

### Callable类型

```python
"""
Callable: 可调用对象类型
"""

from typing import Callable

# 基础Callable
def apply(func: Callable[[int], str], value: int) -> str:
    """应用函数"""
    return func(value)

result = apply(str, 42)  # "42"

# 多个参数
def process(
    func: Callable[[int, str], bool],
    x: int,
    y: str
) -> bool:
    """处理函数"""
    return func(x, y)

# 无参数
def execute(func: Callable[[], None]) -> None:
    """执行无参函数"""
    func()

# 可变参数
from typing import Any

def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
    """包装器，接受任意参数"""
    def inner(*args: Any, **kwargs: Any) -> Any:
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return inner

# 实际应用: 装饰器类型
from functools import wraps

def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function() -> None:
    import time
    time.sleep(1)
```

### TypeVar和泛型

```python
"""
TypeVar: 类型变量
"""

from typing import TypeVar

# 定义类型变量
T = TypeVar('T')

def first(items: list[T]) -> T:
    """返回列表第一个元素"""
    return items[0]

# 类型推断
x = first([1, 2, 3])      # x: int
y = first(["a", "b"])     # y: str

# 约束类型变量
T = TypeVar('T', int, float)

def add(x: T, y: T) -> T:
    """只接受int或float"""
    return x + y

add(1, 2)      # ✅ int
add(1.0, 2.0)  # ✅ float
# add("a", "b") # ❌ mypy error

# 有界类型变量
from typing import SupportsFloat

T = TypeVar('T', bound=SupportsFloat)

def double(x: T) -> float:
    """加倍，要求支持float转换"""
    return float(x) * 2

# 多个类型变量
K = TypeVar('K')
V = TypeVar('V')

def swap_dict(d: dict[K, V]) -> dict[V, K]:
    """交换字典的键值"""
    return {v: k for k, v in d.items()}

original = {"a": 1, "b": 2}
swapped = swap_dict(original)  # dict[int, str]
```

---

## 类型别名

### 简单别名

```python
"""
类型别名
"""

# 简单别名
Vector = list[float]
Matrix = list[Vector]

def dot_product(v1: Vector, v2: Vector) -> float:
    """向量点积"""
    return sum(x * y for x, y in zip(v1, v2))

def matrix_multiply(m1: Matrix, m2: Matrix) -> Matrix:
    """矩阵乘法"""
    # 实现...
    pass

# 复杂类型别名
JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

def parse_json(data: str) -> JSON:
    """解析JSON"""
    import json
    return json.loads(data)

# 联合类型别名
UserId = int | str
Username = str

def get_user(identifier: UserId) -> Username | None:
    """获取用户名"""
    # 实现...
    pass

# 回调类型别名
Callback = Callable[[str], None]

def register_callback(callback: Callback) -> None:
    """注册回调"""
    callback("event")
```

### TypeAlias (Python 3.10+)

```python
"""
显式类型别名
"""

from typing import TypeAlias

# 显式声明类型别名
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]

# 递归类型别名
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

# 与泛型结合
from typing import TypeVar

T = TypeVar('T')
Stack: TypeAlias = list[T]

def push(stack: Stack[int], item: int) -> None:
    """压栈"""
    stack.append(item)

# Python 3.12+ type语句
type Vector = list[float]
type Matrix = list[Vector]
type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None
```

---

## 📚 核心要点

### 类型注解基础

- ✅ **内置类型**: int, str, float, bool
- ✅ **容器类型**: list, dict, set, tuple
- ✅ **Optional**: 值或None
- ✅ **Union**: 多种类型之一 (用|)

### 高级类型

- ✅ **Literal**: 字面量类型
- ✅ **Final**: 常量类型
- ✅ **Callable**: 函数类型
- ✅ **TypeVar**: 泛型类型变量

### 类型别名

- ✅ **简单别名**: Type = OtherType
- ✅ **TypeAlias**: 显式类型别名
- ✅ **type语句**: Python 3.12+新语法

### 最佳实践

- ✅ 为公开API添加类型注解
- ✅ 使用Python 3.10+ | 语法
- ✅ 优先使用内置泛型 (list而非List)
- ✅ 合理使用TypeAlias提高可读性
- ✅ 避免过度使用Any

### 工具支持

- ✅ **mypy**: 静态类型检查器
- ✅ **pyright**: 微软类型检查器
- ✅ **IDE**: PyCharm, VSCode自动补全
- ✅ **运行时**: 类型注解不影响执行

---

**掌握类型注解，提升代码质量！** 📝✨

**相关文档**:

- [02-generics-protocols.md](02-generics-protocols.md) - 泛型与协议
- [04-mypy.md](04-mypy.md) - mypy类型检查

**最后更新**: 2025年10月28日
