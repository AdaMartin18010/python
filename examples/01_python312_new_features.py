"""
Python 3.12 核心新特性演示
对标2025年语言标准
"""

# ============================================================================
# 1. PEP 695: 类型参数语法 (Type Parameter Syntax)
# ============================================================================

# 旧语法 (Python 3.11-)
from typing import TypeVar, Generic

T_old = TypeVar("T_old")


class StackOld(Generic[T_old]):
    """传统泛型语法"""

    def __init__(self) -> None:
        self.items: list[T_old] = []

    def push(self, item: T_old) -> None:
        self.items.append(item)

    def pop(self) -> T_old:
        return self.items.pop()


# 新语法 (Python 3.12+) ⭐⭐⭐⭐⭐
class Stack[T]:
    """现代泛型语法 - 更简洁直观"""

    def __init__(self) -> None:
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()


# 泛型函数
def first[T](items: list[T]) -> T | None:
    """返回列表第一个元素"""
    return items[0] if items else None


def swap[T](a: T, b: T) -> tuple[T, T]:
    """交换两个值"""
    return b, a


# ============================================================================
# 2. PEP 698: @override 装饰器
# ============================================================================

from typing import override


class Animal:
    """基类"""

    def make_sound(self) -> str:
        return "Some sound"

    def eat(self) -> str:
        return "Eating..."


class Dog(Animal):
    """子类使用 @override 确保正确重写"""

    @override
    def make_sound(self) -> str:
        return "Woof!"

    @override
    def eat(self) -> str:
        return "Dog is eating..."

    # 如果拼写错误,mypy会报错
    # @override
    # def make_sounds(self) -> str:  # 错误!父类没有这个方法
    #     return "Woof!"


# ============================================================================
# 3. PEP 701: f-string 增强
# ============================================================================


def demonstrate_fstring_enhancements() -> None:
    """演示 f-string 新特性"""

    # 3.1 支持嵌套引号 (不再需要混合引号)
    name = "Python"
    version = 3.12

    # 旧方法需要转义或混合引号
    old_way = f"Language: {name}, Info: {{'version': {version}}}"

    # 新方法: Python 3.12 改进了引号处理
    new_way = f'Language: {name}, Info: {{"version": {version}}}'

    # 3.2 支持反斜杠 (在某些上下文中)
    path = "C:\\Users\\Python"
    path_unix = path.replace("\\", "/")
    formatted = f"Path: {path_unix}"  # ✅ Python 3.12+

    # 3.3 支持多行表达式
    result = f"""
    User: {name}
    Version: {
        version if version >= 3.10
        else "Too old"
    }
    """

    # 3.4 表达式计算
    total = f"Sum: {10 + 20}"

    print(f"Old way: {old_way}")
    print(f"New way: {new_way}")
    print(f"Result: {result}")
    print(f"Total: {total}")


# ============================================================================
# 4. PEP 692: TypedDict with Unpack
# ============================================================================

from typing import TypedDict, Unpack


class UserInfo(TypedDict):
    """用户信息类型"""

    name: str
    age: int
    email: str


def create_user(**kwargs: Unpack[UserInfo]) -> UserInfo:
    """创建用户 - 类型安全的关键字参数"""
    return kwargs


# 类型安全的调用
user1 = create_user(name="Alice", age=30, email="alice@example.com")
# user2 = create_user(name="Bob", age=25)  # 错误!缺少 email


# ============================================================================
# 5. 性能优化: Comprehension 内联
# ============================================================================


def performance_improvements() -> None:
    """演示 Python 3.12 性能改进"""

    # 列表推导式现在更快 (PEP 709)
    # Python 3.12 内联了推导式,避免了额外的函数调用开销

    # 示例: 大数据集处理
    large_data = range(1_000_000)

    # 列表推导 (3.12 中优化)
    squares = [x * x for x in large_data if x % 2 == 0]

    # 字典推导 (同样优化)
    square_dict = {x: x * x for x in range(1000)}

    # 集合推导
    unique_squares = {x * x for x in range(100)}

    print(f"Generated {len(squares)} squares")
    print(f"Dictionary size: {len(square_dict)}")
    print(f"Set size: {len(unique_squares)}")


# ============================================================================
# 6. 错误消息改进
# ============================================================================


def demonstrate_error_improvements() -> None:
    """演示改进的错误消息"""

    # Python 3.12 的错误消息更精确,指出具体位置

    data = {"name": "Python", "version": 3.12}

    try:
        # 这会产生更清晰的错误消息
        result = data["name"].upper() + data["versions"]  # 拼写错误
    except KeyError as e:
        print(f"Error: {e}")
        # Python 3.12 会精确指出是 'versions' 键不存在


# ============================================================================
# 7. 现代类型注解最佳实践
# ============================================================================


class ModernTyping:
    """2025年类型注解标准"""

    # 使用 | 而不是 Union
    def get_value(self) -> str | int | None:
        return None

    # 使用 list[T] 而不是 List[T]
    def process_items(self, items: list[str]) -> dict[str, int]:
        return {item: len(item) for item in items}

    # 使用 tuple 而不是 Tuple
    def get_coordinates(self) -> tuple[float, float]:
        return 0.0, 0.0

    # 使用 type 别名
    type UserId = int
    type UserName = str
    type UserMapping = dict[UserId, UserName]

    def get_users(self) -> UserMapping:
        return {1: "Alice", 2: "Bob"}


# ============================================================================
# 8. 异常组 (Exception Groups) - Python 3.11+, 3.12优化
# ============================================================================


async def demonstrate_exception_groups() -> None:
    """演示异常组处理"""
    import asyncio

    async def task_that_fails(n: int) -> int:
        if n % 2 == 0:
            raise ValueError(f"Task {n} failed with ValueError")
        if n % 3 == 0:
            raise TypeError(f"Task {n} failed with TypeError")
        return n

    try:
        # 并发执行多个任务
        results = await asyncio.gather(
            task_that_fails(1), task_that_fails(2), task_that_fails(3), return_exceptions=True
        )

        # 收集异常
        exceptions = [r for r in results if isinstance(r, Exception)]
        if exceptions:
            raise ExceptionGroup("Multiple tasks failed", exceptions)

    except* ValueError as eg:
        # 只捕获 ValueError
        print(f"Caught {len(eg.exceptions)} ValueError(s)")

    except* TypeError as eg:
        # 只捕获 TypeError
        print(f"Caught {len(eg.exceptions)} TypeError(s)")


# ============================================================================
# 主程序
# ============================================================================


def main() -> None:
    """主函数"""
    print("=" * 70)
    print("Python 3.12 核心新特性演示")
    print("=" * 70)

    # 测试新泛型语法
    stack = Stack[int]()
    stack.push(1)
    stack.push(2)
    print(f"✅ 泛型语法: Stack popped {stack.pop()}")

    # 测试泛型函数
    numbers = [1, 2, 3, 4, 5]
    print(f"✅ 泛型函数: First element is {first(numbers)}")

    # 测试 override
    dog = Dog()
    print(f"✅ @override: Dog says {dog.make_sound()}")

    # 测试 f-string
    print("\n✅ f-string 增强:")
    demonstrate_fstring_enhancements()

    # 测试 TypedDict
    user = create_user(name="Alice", age=30, email="alice@example.com")
    print(f"\n✅ TypedDict: Created user {user['name']}")

    # 性能改进
    print("\n✅ 性能优化:")
    performance_improvements()

    # 现代类型注解
    typing_demo = ModernTyping()
    users = typing_demo.get_users()
    print(f"\n✅ 现代类型注解: {len(users)} users")

    print("\n" + "=" * 70)
    print("✅ 所有特性演示完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()

