"""
Python 2025 现代类型系统全面演示
涵盖泛型、协议、TypedDict、ParamSpec等高级特性
"""

from typing import (
    TypeVar,
    Generic,
    Protocol,
    TypedDict,
    ParamSpec,
    Concatenate,
    TypeGuard,
    Literal,
    Required,
    NotRequired,
    Self,
    Never,
    LiteralString,
    TypeAlias,
    Unpack,
    override,
)
from collections.abc import Callable, Sequence, Iterable, Iterator
from dataclasses import dataclass
from abc import ABC, abstractmethod

# ============================================================================
# 1. 泛型 (Generics) - PEP 695 新语法
# ============================================================================


# 传统泛型 (Python 3.11-)
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class ContainerOld(Generic[T]):
    """传统泛型容器"""

    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value


# 现代泛型 (Python 3.12+) ⭐⭐⭐⭐⭐
class Container[T]:
    """现代泛型容器 - 更简洁"""

    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value


# 泛型函数
def identity[T](value: T) -> T:
    """泛型身份函数"""
    return value


def map_values[K, V, R](mapping: dict[K, V], func: Callable[[V], R]) -> dict[K, R]:
    """映射字典值 - 多泛型参数"""
    return {k: func(v) for k, v in mapping.items()}


# 泛型类方法
class Stack[T]:
    """泛型栈"""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        return len(self._items) == 0


# ============================================================================
# 2. 协议 (Protocols) - 结构化子类型
# ============================================================================


class Drawable(Protocol):
    """可绘制协议 - 结构化类型"""

    def draw(self) -> str: ...


class Movable(Protocol):
    """可移动协议"""

    def move(self, x: float, y: float) -> None: ...


class Shape(Protocol):
    """形状协议 - 组合多个协议"""

    def area(self) -> float: ...
    def perimeter(self) -> float: ...


# 实现协议的类 (无需显式继承)
class Circle:
    """圆形 - 隐式实现 Shape 协议"""

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius**2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius

    def draw(self) -> str:
        return f"Drawing circle with radius {self.radius}"


class Rectangle:
    """矩形 - 隐式实现 Shape 协议"""

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


# 使用协议的函数
def print_shape_info(shape: Shape) -> None:
    """打印形状信息 - 接受任何实现 Shape 协议的对象"""
    print(f"Area: {shape.area():.2f}")
    print(f"Perimeter: {shape.perimeter():.2f}")


def draw_object(obj: Drawable) -> None:
    """绘制对象 - 结构化子类型"""
    print(obj.draw())


# ============================================================================
# 3. TypedDict - 结构化字典类型
# ============================================================================


class UserBase(TypedDict):
    """用户基础信息"""

    id: int
    name: str


class UserWithEmail(UserBase):
    """带邮箱的用户 - 继承 TypedDict"""

    email: str


# 可选字段 (Python 3.11+)
class UserProfile(TypedDict):
    """用户档案 - 必需和可选字段"""

    id: Required[int]  # 必需
    name: Required[str]  # 必需
    email: NotRequired[str]  # 可选
    age: NotRequired[int]  # 可选


# 使用 Unpack 解包 TypedDict
def create_user(**kwargs: Unpack[UserProfile]) -> UserProfile:
    """创建用户 - 类型安全的关键字参数"""
    return kwargs  # type: ignore[return-value]


# Total=False 表示所有字段可选
class PartialUser(TypedDict, total=False):
    """部分用户信息 - 所有字段可选"""

    id: int
    name: str
    email: str


# ============================================================================
# 4. ParamSpec - 保留函数签名
# ============================================================================

P = ParamSpec("P")
R = TypeVar("R")


def log_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """装饰器 - 保留函数签名"""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result

    return wrapper


@log_decorator
def add(a: int, b: int) -> int:
    """加法函数 - 装饰后类型保持不变"""
    return a + b


@log_decorator
def greet(name: str, greeting: str = "Hello") -> str:
    """问候函数 - 带默认参数"""
    return f"{greeting}, {name}!"


# Concatenate - 添加额外参数
def add_logging[**P, R](func: Callable[P, R]) -> Callable[Concatenate[str, P], R]:
    """添加日志参数的装饰器"""

    def wrapper(log_level: str, *args: P.args, **kwargs: P.kwargs) -> R:
        print(f"[{log_level}] Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# ============================================================================
# 5. 类型守卫 (TypeGuard)
# ============================================================================


def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    """类型守卫 - 检查是否为字符串列表"""
    return all(isinstance(x, str) for x in val)


def process_data(items: list[object]) -> None:
    """处理数据 - 使用类型守卫"""
    if is_str_list(items):
        # mypy 知道这里 items 是 list[str]
        for item in items:
            print(item.upper())
    else:
        print("Not a string list")


# 更复杂的类型守卫
def is_user_dict(val: dict[str, object]) -> TypeGuard[UserProfile]:
    """检查是否为有效的用户字典"""
    return (
        isinstance(val.get("id"), int)
        and isinstance(val.get("name"), str)
        and ("email" not in val or isinstance(val["email"], str))
    )


# ============================================================================
# 6. Literal Types - 字面量类型
# ============================================================================

# 字面量类型
type Mode = Literal["read", "write", "append"]
type Status = Literal["pending", "running", "completed", "failed"]


class FileHandler:
    """文件处理器 - 使用字面量类型"""

    def __init__(self, filename: str, mode: Mode) -> None:
        self.filename = filename
        self.mode = mode

    def get_mode(self) -> Mode:
        return self.mode


class Task:
    """任务 - 使用状态字面量"""

    def __init__(self, name: str) -> None:
        self.name = name
        self._status: Status = "pending"

    def get_status(self) -> Status:
        return self._status

    def set_status(self, status: Status) -> None:
        self._status = status


# ============================================================================
# 7. Self Type - 返回自身类型
# ============================================================================


class Builder:
    """构建器模式 - 使用 Self 类型"""

    def __init__(self) -> None:
        self._value = 0

    def add(self, n: int) -> Self:
        """链式调用 - 返回 Self"""
        self._value += n
        return self

    def multiply(self, n: int) -> Self:
        """链式调用"""
        self._value *= n
        return self

    def build(self) -> int:
        return self._value


class ExtendedBuilder(Builder):
    """扩展构建器 - Self 自动适应"""

    def subtract(self, n: int) -> Self:
        """新方法 - 返回 Self"""
        self._value -= n
        return self


# ============================================================================
# 8. @override 装饰器 - 确保正确重写
# ============================================================================


class Animal(ABC):
    """动物基类"""

    @abstractmethod
    def make_sound(self) -> str:
        """发出声音"""
        ...

    def eat(self) -> str:
        """吃东西"""
        return "Eating..."


class Dog(Animal):
    """狗 - 使用 @override"""

    @override
    def make_sound(self) -> str:
        return "Woof!"

    @override
    def eat(self) -> str:
        return "Dog is eating..."

    # @override
    # def make_sounds(self) -> str:  # 错误! 父类没有这个方法
    #     return "Woof!"


# ============================================================================
# 9. Type Aliases - 类型别名 (Python 3.12+)
# ============================================================================

# 简单类型别名
type UserId = int
type UserName = str
type Email = str

# 泛型类型别名
type Point[T] = tuple[T, T]
type Matrix[T] = list[list[T]]

# 复杂类型别名
type UserMapping[K, V] = dict[K, V]
type Result[T, E] = tuple[Literal["ok"], T] | tuple[Literal["error"], E]


# 使用类型别名
def get_user(user_id: UserId) -> UserName:
    """获取用户名"""
    return f"User_{user_id}"


def process_matrix(matrix: Matrix[float]) -> float:
    """处理矩阵"""
    return sum(sum(row) for row in matrix)


# Result 类型示例
def divide(a: float, b: float) -> Result[float, str]:
    """除法 - 返回 Result 类型"""
    if b == 0:
        return ("error", "Division by zero")
    return ("ok", a / b)


# ============================================================================
# 10. Never Type - 永不返回
# ============================================================================


def assert_never(value: Never) -> Never:
    """穷尽性检查"""
    raise AssertionError(f"Unexpected value: {value}")


type Color = Literal["red", "green", "blue"]


def get_color_code(color: Color) -> str:
    """获取颜色代码 - 穷尽性检查"""
    if color == "red":
        return "#FF0000"
    elif color == "green":
        return "#00FF00"
    elif color == "blue":
        return "#0000FF"
    else:
        # 如果添加新颜色但忘记处理,mypy 会报错
        assert_never(color)


# ============================================================================
# 11. 实战综合示例
# ============================================================================


class Repository[T]:
    """泛型仓储模式"""

    def __init__(self) -> None:
        self._storage: dict[int, T] = {}
        self._next_id = 1

    def add(self, item: T) -> int:
        """添加项目"""
        item_id = self._next_id
        self._storage[item_id] = item
        self._next_id += 1
        return item_id

    def get(self, item_id: int) -> T | None:
        """获取项目"""
        return self._storage.get(item_id)

    def all(self) -> list[T]:
        """获取所有项目"""
        return list(self._storage.values())


@dataclass
class Product:
    """产品数据类"""

    name: str
    price: float
    stock: int

    def is_available(self) -> bool:
        return self.stock > 0


# 使用泛型仓储
product_repo = Repository[Product]()


# ============================================================================
# 主程序
# ============================================================================


def main() -> None:
    """主函数"""
    print("=" * 70)
    print("Python 2025 现代类型系统全面演示")
    print("=" * 70)

    # 1. 泛型
    print("\n1️⃣ 泛型 (Generics)")
    stack = Stack[int]()
    stack.push(1)
    stack.push(2)
    print(f"✅ Stack peek: {stack.peek()}")

    # 2. 协议
    print("\n2️⃣ 协议 (Protocols)")
    circle = Circle(5)
    print_shape_info(circle)
    draw_object(circle)

    # 3. TypedDict
    print("\n3️⃣ TypedDict")
    user = create_user(id=1, name="Alice", email="alice@example.com")
    print(f"✅ User created: {user['name']}")

    # 4. ParamSpec
    print("\n4️⃣ ParamSpec")
    result = add(5, 3)
    greeting = greet("Bob")

    # 5. 类型守卫
    print("\n5️⃣ 类型守卫 (TypeGuard)")
    items: list[object] = ["hello", "world"]
    process_data(items)

    # 6. Literal Types
    print("\n6️⃣ 字面量类型 (Literal)")
    handler = FileHandler("data.txt", "read")
    print(f"✅ File mode: {handler.get_mode()}")

    # 7. Self Type
    print("\n7️⃣ Self 类型")
    builder = Builder().add(5).multiply(2).add(3)
    print(f"✅ Builder result: {builder.build()}")

    # 8. @override
    print("\n8️⃣ @override 装饰器")
    dog = Dog()
    print(f"✅ Dog sound: {dog.make_sound()}")

    # 9. Type Aliases
    print("\n9️⃣ 类型别名")
    user_name = get_user(123)
    print(f"✅ User name: {user_name}")

    ok_result = divide(10, 2)
    print(f"✅ Division result: {ok_result}")

    # 10. Result 类型
    err_result = divide(10, 0)
    if err_result[0] == "error":
        print(f"✅ Error handled: {err_result[1]}")

    # 11. 泛型仓储
    print("\n🔟 泛型仓储模式")
    product1 = Product("Laptop", 999.99, 10)
    product2 = Product("Mouse", 29.99, 50)

    id1 = product_repo.add(product1)
    id2 = product_repo.add(product2)

    print(f"✅ Added {len(product_repo.all())} products")

    print("\n" + "=" * 70)
    print("✅ 类型系统演示完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()

