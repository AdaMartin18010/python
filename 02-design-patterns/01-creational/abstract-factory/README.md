# Abstract Factory Pattern (抽象工厂模式)

## 目录

- [1. 模式概述](#1-模式概述)
- [2. 核心概念](#2-核心概念)
- [3. Python实现方式](#3-python实现方式)
- [4. 使用场景](#4-使用场景)
- [5. 实现示例](#5-实现示例)
- [6. 最佳实践](#6-最佳实践)
- [7. 性能考量](#7-性能考量)
- [8. 相关模式](#8-相关模式)

---

## 1. 模式概述

### 1.1 定义

**抽象工厂模式**是一种创建型设计模式，它提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类。

### 1.2 意图

- 提供一个创建产品族的接口
- 将产品系列的创建与使用分离
- 保证产品族内部的一致性
- 隐藏具体产品的实现细节

### 1.3 别名

- Kit (工具箱)
- Product Family (产品族)

### 1.4 与工厂方法的区别

| 维度 | 工厂方法 | 抽象工厂 |
|-----|---------|---------|
| **创建对象** | 一个产品 | 一系列产品 |
| **产品层次** | 单一产品线 | 多个产品线（产品族） |
| **工厂层次** | 一个工厂方法 | 多个工厂方法 |
| **扩展方向** | 增加新产品类型 | 增加新产品族 |
| **使用场景** | 创建单一对象 | 创建相关对象组 |

---

## 2. 核心概念

### 2.1 角色组成

```text
AbstractFactory (抽象工厂)
├── create_product_a() -> AbstractProductA
└── create_product_b() -> AbstractProductB

ConcreteFactory1 (具体工厂1)
├── create_product_a() -> ProductA1
└── create_product_b() -> ProductB1

ConcreteFactory2 (具体工厂2)
├── create_product_a() -> ProductA2
└── create_product_b() -> ProductB2

AbstractProductA (抽象产品A)
└── operation_a()

AbstractProductB (抽象产品B)
└── operation_b()
└── another_operation_b(collaborator: AbstractProductA)

ProductA1, ProductA2 (具体产品A1, A2)
ProductB1, ProductB2 (具体产品B1, B2)
```

### 2.2 主要角色

1. **AbstractFactory (抽象工厂)**
   - 声明创建抽象产品对象的操作接口
   - 包含多个创建方法，每个对应一类产品

2. **ConcreteFactory (具体工厂)**
   - 实现创建具体产品对象的操作
   - 创建同一产品族的产品

3. **AbstractProduct (抽象产品)**
   - 为一类产品对象声明接口
   - 定义产品的共同行为

4. **ConcreteProduct (具体产品)**
   - 定义具体工厂创建的产品对象
   - 实现AbstractProduct接口

5. **Client (客户端)**
   - 仅使用AbstractFactory和AbstractProduct接口
   - 不关心具体实现

### 2.3 关键特性

- **产品族**: 一系列相关或相互依赖的产品对象
- **产品等级**: 产品的继承结构
- **一致性**: 同一工厂创建的产品属于同一产品族
- **封装性**: 隐藏具体产品的实现
- **可替换性**: 轻松切换整个产品族

---

## 3. Python实现方式

### 3.1 经典实现（抽象基类）

使用 `abc.ABC` 和 `@abstractmethod` 定义抽象工厂和产品接口。

```python
from abc import ABC, abstractmethod

class AbstractProductA(ABC):
    @abstractmethod
    def operation_a(self) -> str:
        pass

class AbstractProductB(ABC):
    @abstractmethod
    def operation_b(self) -> str:
        pass
    
    @abstractmethod
    def collaborate_with_a(self, collaborator: AbstractProductA) -> str:
        pass

class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass
    
    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass

class ConcreteFactory1(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()
    
    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()
```

**优点**:

- 类型安全，强制实现所有方法
- IDE支持好，自动补全完善
- 符合面向对象设计原则
- 编译时检查

**缺点**:

- 代码较冗长
- 需要定义多个类
- 添加新产品类型需要修改工厂接口

**适用场景**:

- 大型项目，需要严格的类型检查
- 多人协作开发
- 公共库和框架开发
- 产品族相对稳定

### 3.2 Protocol实现（结构化类型）

使用 `typing.Protocol` 定义接口，更灵活的鸭子类型。

```python
from typing import Protocol

class ProductA(Protocol):
    def operation_a(self) -> str: ...

class ProductB(Protocol):
    def operation_b(self) -> str: ...
    def collaborate_with_a(self, collaborator: ProductA) -> str: ...

class Factory(Protocol):
    def create_product_a(self) -> ProductA: ...
    def create_product_b(self) -> ProductB: ...
```

**优点**:

- 更Pythonic，鸭子类型
- 不需要显式继承
- 灵活，易于集成第三方代码
- 代码更简洁

**缺点**:

- 运行时不强制检查
- 可能导致错误延迟发现
- 需要配合mypy使用

**适用场景**:

- 需要灵活性的场景
- 集成第三方库
- 快速原型开发
- 鸭子类型风格的项目

### 3.3 函数式实现

使用函数和闭包实现抽象工厂。

```python
from typing import Callable, NamedTuple

class Products(NamedTuple):
    product_a: Any
    product_b: Any

def create_factory(family: str) -> Callable[[], Products]:
    """返回创建产品族的工厂函数"""
    factories = {
        "family1": lambda: Products(
            product_a=ConcreteProductA1(),
            product_b=ConcreteProductB1()
        ),
        "family2": lambda: Products(
            product_a=ConcreteProductA2(),
            product_b=ConcreteProductB2()
        ),
    }
    return factories.get(family, lambda: None)
```

**优点**:

- 代码最简洁
- 函数式编程风格
- 易于理解

**缺点**:

- 缺少面向对象的结构
- 难以管理复杂的产品族
- 类型检查较弱

**适用场景**:

- 简单的产品族
- 函数式编程风格项目
- 配置驱动的场景

### 3.4 注册表模式（推荐⭐）

使用装饰器和注册表管理工厂族。

```python
class FactoryRegistry:
    _factories: dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str):
        def decorator(factory_class):
            cls._factories[name] = factory_class
            return factory_class
        return decorator
    
    @classmethod
    def get_factory(cls, name: str) -> AbstractFactory:
        factory_class = cls._factories.get(name)
        if not factory_class:
            raise ValueError(f"Unknown factory: {name}")
        return factory_class()

@FactoryRegistry.register("modern")
class ModernFactory(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ModernProductA()
    
    def create_product_b(self) -> AbstractProductB:
        return ModernProductB()
```

**优点**:

- 自动注册，减少维护
- 支持插件式扩展
- 配置化管理
- 易于添加新工厂

**缺点**:

- 需要额外的注册机制
- 全局状态管理
- 增加了一层抽象

**适用场景**:

- 插件系统
- 多种产品族
- 动态工厂选择
- 配置驱动的应用

### 3.5 泛型实现（Python 3.12+）

使用新的泛型语法实现类型安全的抽象工厂。

```python
from typing import Generic, TypeVar, Protocol

PA = TypeVar('PA', bound='ProductA')
PB = TypeVar('PB', bound='ProductB')

class AbstractFactory(Protocol, Generic[PA, PB]):
    def create_product_a(self) -> PA: ...
    def create_product_b(self) -> PB: ...

class ConcreteFactory(AbstractFactory[ConcreteProductA, ConcreteProductB]):
    def create_product_a(self) -> ConcreteProductA:
        return ConcreteProductA()
    
    def create_product_b(self) -> ConcreteProductB:
        return ConcreteProductB()
```

**优点**:

- 强类型安全
- 编译时检查
- IDE支持好
- 类型推导准确

**缺点**:

- 需要Python 3.12+
- 语法相对复杂
- 学习曲线陡峭

**适用场景**:

- 现代Python项目
- 需要强类型保证
- 复杂的产品族关系
- 类型安全要求高

---

## 4. 使用场景

### 4.1 典型应用

1. **跨平台UI系统** 🖥️
   - Windows、macOS、Linux的UI组件
   - 同一平台的组件风格一致
   - 按钮、文本框、对话框等

2. **数据库访问层** 🗄️
   - 不同数据库的连接、命令、事务
   - MySQL、PostgreSQL、Oracle
   - 同一数据库的组件协作

3. **主题系统** 🎨
   - 亮色主题、暗色主题
   - 颜色、字体、图标等
   - 保证视觉一致性

4. **文档生成系统** 📄
   - HTML、PDF、Markdown
   - 标题、段落、图片等元素
   - 同一格式的元素配套

5. **游戏开发** 🎮
   - 不同地图的敌人、道具、场景
   - 同一地图的元素风格统一
   - 沙漠、森林、雪地等

6. **报表系统** 📊
   - Excel、CSV、JSON格式
   - 表头、数据行、汇总行
   - 同一格式的元素协作

### 4.2 适用条件

✅ **适合使用的情况**:

- 系统需要独立于产品的创建、组合和表示
- 系统要配置多个产品系列中的一个
- 一系列相关的产品对象被设计在一起使用
- 需要提供产品类库，只显示接口不显示实现
- 产品族相对稳定，但可能增加新的产品族

❌ **不适合使用的情况**:

- 产品族经常变化（增加新产品类型）
- 只有一个产品族
- 产品之间没有关联
- 系统复杂度不高
- 过度设计会增加维护成本

---

## 5. 实现示例

### 5.1 基础示例：跨平台UI

```python
from abc import ABC, abstractmethod

# 抽象产品：按钮
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def on_click(self) -> None:
        pass

# 抽象产品：复选框
class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def is_checked(self) -> bool:
        pass

# 具体产品：Windows按钮
class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Button]"
    
    def on_click(self) -> None:
        print("Windows button clicked")

# 具体产品：Windows复选框
class WindowsCheckbox(Checkbox):
    def __init__(self):
        self._checked = False
    
    def render(self) -> str:
        return "[X]" if self._checked else "[ ]"
    
    def is_checked(self) -> bool:
        return self._checked

# 抽象工厂
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

# 具体工厂：Windows工厂
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

# 客户端代码
def create_ui(factory: GUIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    
    print(button.render())
    print(checkbox.render())
    button.on_click()

# 使用
factory = WindowsFactory()
create_ui(factory)
```

### 5.2 进阶示例：数据库访问层

```python
from typing import Protocol

# 产品协议
class Connection(Protocol):
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def is_connected(self) -> bool: ...

class Command(Protocol):
    def execute(self, sql: str) -> list: ...
    def execute_scalar(self, sql: str) -> Any: ...

class Transaction(Protocol):
    def begin(self) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

# 抽象工厂
class DatabaseFactory(Protocol):
    def create_connection(self) -> Connection: ...
    def create_command(self, connection: Connection) -> Command: ...
    def create_transaction(self, connection: Connection) -> Transaction: ...

# MySQL具体产品
class MySQLConnection:
    def connect(self) -> None:
        print("Connected to MySQL")
        self._connected = True
    
    def disconnect(self) -> None:
        print("Disconnected from MySQL")
        self._connected = False
    
    def is_connected(self) -> bool:
        return self._connected

class MySQLCommand:
    def __init__(self, connection: MySQLConnection):
        self.connection = connection
    
    def execute(self, sql: str) -> list:
        print(f"Executing MySQL query: {sql}")
        return [{"id": 1, "name": "test"}]
    
    def execute_scalar(self, sql: str) -> Any:
        return 42

# MySQL工厂
class MySQLFactory:
    def create_connection(self) -> Connection:
        return MySQLConnection()
    
    def create_command(self, connection: Connection) -> Command:
        return MySQLCommand(connection)
    
    def create_transaction(self, connection: Connection) -> Transaction:
        return MySQLTransaction(connection)

# 客户端
def perform_database_operations(factory: DatabaseFactory):
    conn = factory.create_connection()
    conn.connect()
    
    cmd = factory.create_command(conn)
    results = cmd.execute("SELECT * FROM users")
    
    print(f"Results: {results}")
    
    conn.disconnect()

# 使用
factory = MySQLFactory()
perform_database_operations(factory)
```

### 5.3 实战示例：主题系统

```python
from dataclasses import dataclass
from enum import Enum

class ColorScheme(Enum):
    LIGHT = "light"
    DARK = "dark"

@dataclass
class Color:
    r: int
    g: int
    b: int
    
    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

# 抽象产品
class ThemeColors(ABC):
    @abstractmethod
    def get_background(self) -> Color:
        pass
    
    @abstractmethod
    def get_foreground(self) -> Color:
        pass
    
    @abstractmethod
    def get_accent(self) -> Color:
        pass

class ThemeFonts(ABC):
    @abstractmethod
    def get_title_font(self) -> str:
        pass
    
    @abstractmethod
    def get_body_font(self) -> str:
        pass

# 具体产品：亮色主题
class LightThemeColors(ThemeColors):
    def get_background(self) -> Color:
        return Color(255, 255, 255)  # 白色
    
    def get_foreground(self) -> Color:
        return Color(0, 0, 0)  # 黑色
    
    def get_accent(self) -> Color:
        return Color(0, 120, 215)  # 蓝色

class LightThemeFonts(ThemeFonts):
    def get_title_font(self) -> str:
        return "Arial Bold 24px"
    
    def get_body_font(self) -> str:
        return "Arial Regular 14px"

# 抽象工厂
class ThemeFactory(ABC):
    @abstractmethod
    def create_colors(self) -> ThemeColors:
        pass
    
    @abstractmethod
    def create_fonts(self) -> ThemeFonts:
        pass

# 具体工厂
class LightThemeFactory(ThemeFactory):
    def create_colors(self) -> ThemeColors:
        return LightThemeColors()
    
    def create_fonts(self) -> ThemeFonts:
        return LightThemeFonts()

# 应用主题
def apply_theme(factory: ThemeFactory):
    colors = factory.create_colors()
    fonts = factory.create_fonts()
    
    print(f"Background: {colors.get_background().to_hex()}")
    print(f"Foreground: {colors.get_foreground().to_hex()}")
    print(f"Title Font: {fonts.get_title_font()}")

# 使用
theme = LightThemeFactory()
apply_theme(theme)
```

---

## 6. 最佳实践

### 6.1 设计原则

1. **依赖倒置原则**

   ```python
   # ✅ 好的做法：依赖抽象
   def create_app(factory: AbstractFactory):
       product_a = factory.create_product_a()
       product_b = factory.create_product_b()
   
   # ❌ 避免：依赖具体类
   def create_app():
       product_a = ConcreteProductA1()
       product_b = ConcreteProductB1()
   ```

2. **开闭原则**

   ```python
   # ✅ 好的做法：通过扩展添加新产品族
   @FactoryRegistry.register("new_family")
   class NewFactory(AbstractFactory):
       pass
   
   # ❌ 避免：修改现有工厂代码
   class ExistingFactory:
       def create_product_a(self):
           if self.variant == "new":  # 修改了原有代码
               return NewProductA()
   ```

3. **单一职责原则**

   ```python
   # ✅ 好的做法：每个工厂负责一个产品族
   class WindowsFactory(AbstractFactory):
       def create_button(self) -> Button:
           return WindowsButton()
       
       def create_checkbox(self) -> Checkbox:
           return WindowsCheckbox()
   
   # ❌ 避免：一个工厂混合多个产品族
   class MixedFactory:
       def create_windows_button(self) -> Button: ...
       def create_mac_button(self) -> Button: ...
   ```

### 6.2 代码组织

1. **包结构推荐**

   ```text
   abstract_factory/
   ├── __init__.py
   ├── base.py           # 抽象类
   ├── products/
   │   ├── __init__.py
   │   ├── product_a.py
   │   └── product_b.py
   ├── factories/
   │   ├── __init__.py
   │   ├── factory1.py
   │   └── factory2.py
   └── registry.py       # 注册表（可选）
   ```

2. **命名规范**
   - 抽象工厂: `AbstractFactory`, `BaseFactory`
   - 具体工厂: `WindowsFactory`, `MacFactory`
   - 抽象产品: `AbstractButton`, `Button`
   - 具体产品: `WindowsButton`, `MacButton`

### 6.3 产品族一致性

```python
class ProductFamilyValidator:
    """验证产品族的一致性"""
    
    @staticmethod
    def validate(factory: AbstractFactory) -> bool:
        product_a = factory.create_product_a()
        product_b = factory.create_product_b()
        
        # 验证产品是否属于同一族
        return (
            product_a.get_family() == product_b.get_family()
        )
```

### 6.4 配置化工厂选择

```python
# config.py
FACTORY_CONFIG = {
    "development": "WindowsFactory",
    "production": "LinuxFactory",
    "testing": "MacFactory",
}

# main.py
import os

def get_factory() -> AbstractFactory:
    env = os.getenv("ENVIRONMENT", "development")
    factory_name = FACTORY_CONFIG.get(env)
    return FactoryRegistry.get_factory(factory_name)
```

---

## 7. 性能考量

### 7.1 性能对比

| 实现方式 | 创建速度 | 内存占用 | 类型安全 | 灵活性 | 推荐场景 |
|---------|---------|---------|---------|-------|---------|
| 直接实例化 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 简单场景 |
| ABC实现 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 大型项目 |
| Protocol实现 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 灵活场景 |
| 注册表模式 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 插件系统 |
| 泛型实现 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 类型安全 |

### 7.2 优化建议

1. **工厂缓存**

   ```python
   class CachedFactoryRegistry:
       _cache: dict[str, AbstractFactory] = {}
       
       @classmethod
       def get_factory(cls, name: str) -> AbstractFactory:
           if name not in cls._cache:
               cls._cache[name] = cls._create_factory(name)
           return cls._cache[name]
   ```

2. **延迟初始化**

   ```python
   class LazyFactory(AbstractFactory):
       def __init__(self):
           self._product_a = None
           self._product_b = None
       
       def create_product_a(self) -> ProductA:
           if self._product_a is None:
               self._product_a = ConcreteProductA()
           return self._product_a
   ```

3. **产品池**

   ```python
   class PooledFactory(AbstractFactory):
       def __init__(self, pool_size: int = 10):
           self._pool_a = [ConcreteProductA() for _ in range(pool_size)]
           self._pool_b = [ConcreteProductB() for _ in range(pool_size)]
       
       def create_product_a(self) -> ProductA:
           return self._pool_a.pop() if self._pool_a else ConcreteProductA()
   ```

---

## 8. 相关模式

### 8.1 模式对比

| 模式 | 关系 | 区别 |
|-----|------|------|
| **Factory Method** | 相似 | 工厂方法创建单个产品，抽象工厂创建产品族 |
| **Builder** | 互补 | Builder关注复杂对象构建，抽象工厂关注产品族创建 |
| **Prototype** | 可组合 | Prototype可作为抽象工厂的实现方式 |
| **Singleton** | 可组合 | 工厂可以是单例，确保全局唯一 |

### 8.2 组合使用

```python
# 抽象工厂 + 单例
class SingletonFactory(AbstractFactory, metaclass=SingletonMeta):
    pass

# 抽象工厂 + 原型
class PrototypeFactory(AbstractFactory):
    def __init__(self):
        self._prototypes = {
            "product_a": ConcreteProductA(),
            "product_b": ConcreteProductB(),
        }
    
    def create_product_a(self) -> ProductA:
        return copy.deepcopy(self._prototypes["product_a"])

# 抽象工厂 + 建造者
class FactoryWithBuilder(AbstractFactory):
    def create_product_a(self) -> ProductA:
        return (ProductABuilder()
                .set_property1("value1")
                .set_property2("value2")
                .build())
```

---

## 9. 总结

### 9.1 优点

✅ **产品族一致性**: 保证同一工厂创建的产品配套使用  
✅ **易于切换**: 轻松切换整个产品族  
✅ **解耦**: 隔离具体产品的创建  
✅ **扩展性**: 添加新产品族容易

### 9.2 缺点

❌ **复杂性**: 需要创建大量类  
❌ **难以扩展**: 添加新产品类型需要修改接口  
❌ **过度设计**: 简单场景使用会过度复杂

### 9.3 Python特色

🐍 **鸭子类型**: 使用Protocol实现更灵活  
🐍 **装饰器**: 用于工厂注册  
🐍 **类型提示**: 提供更好的IDE支持  
🐍 **数据类**: 简化产品定义

### 9.4 选择建议

| 场景 | 推荐方案 |
|-----|---------|
| 小项目、简单产品族 | 函数式实现 |
| 中型项目、多产品族 | Protocol + 注册表 |
| 大型项目、严格类型 | ABC + 泛型 |
| 插件系统 | 注册表模式 |
| 跨平台应用 | ABC实现 |

---

## 参考资源

- 《Design Patterns》Gang of Four
- 《Head First Design Patterns》
- Python官方文档: [abc模块](https://docs.python.org/3/library/abc.html)
- Python官方文档: [typing模块](https://docs.python.org/3/library/typing.html)
- PEP 544: Protocols
- PEP 695: Type Parameter Syntax

---

**版本**: 1.0.0  
**最后更新**: 2025-10-25  
**兼容Python版本**: 3.12+
