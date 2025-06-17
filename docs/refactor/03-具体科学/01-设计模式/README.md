# 01-设计模式

## 概述

设计模式是软件工程中解决常见问题的可重用解决方案。本章节使用Python实现GoF的23种经典设计模式，包括创建型、结构型和行为型模式。

## 目录结构

```text
01-设计模式/
├── README.md                    # 本文件
├── 01-创建型模式/               # 创建型设计模式
├── 02-结构型模式/               # 结构型设计模式
├── 03-行为型模式/               # 行为型设计模式
├── 04-并发模式/                 # 并发设计模式
└── 05-分布式模式/               # 分布式设计模式
```

## 1. 创建型模式 (Creational Patterns)

### 1.1 单例模式 (Singleton Pattern)

**定义**: 确保一个类只有一个实例，并提供全局访问点。

**Python实现**:

```python
import threading
from typing import Optional, Any
from abc import ABC, abstractmethod

class Singleton:
    """线程安全的单例模式"""
    
    _instance: Optional['Singleton'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'Singleton':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._data = {}
    
    def set_data(self, key: str, value: Any) -> None:
        """设置数据"""
        self._data[key] = value
    
    def get_data(self, key: str) -> Any:
        """获取数据"""
        return self._data.get(key)

class Logger(Singleton):
    """日志记录器单例"""
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._logs = []
    
    def log(self, message: str) -> None:
        """记录日志"""
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        self._logs.append(log_entry)
        print(log_entry)
    
    def get_logs(self) -> list:
        """获取所有日志"""
        return self._logs.copy()

# 单例模式示例
def singleton_example():
    """单例模式示例"""
    print("单例模式示例:")
    print("=" * 50)
    
    # 创建多个实例
    singleton1 = Singleton()
    singleton2 = Singleton()
    
    print(f"实例1 ID: {id(singleton1)}")
    print(f"实例2 ID: {id(singleton2)}")
    print(f"是否为同一实例: {singleton1 is singleton2}")
    
    # 测试数据共享
    singleton1.set_data("key1", "value1")
    print(f"从实例2获取数据: {singleton2.get_data('key1')}")
    
    # 日志记录器示例
    logger1 = Logger()
    logger2 = Logger()
    
    logger1.log("第一条日志")
    logger2.log("第二条日志")
    
    print(f"日志记录器是否为同一实例: {logger1 is logger2}")
    print(f"总日志数量: {len(logger1.get_logs())}")

if __name__ == "__main__":
    singleton_example()
```

### 1.2 工厂方法模式 (Factory Method Pattern)

**定义**: 定义一个创建对象的接口，让子类决定实例化哪一个类。

**Python实现**:

```python
from abc import ABC, abstractmethod
from typing import Dict, Type

class Product(ABC):
    """产品抽象基类"""
    
    @abstractmethod
    def operation(self) -> str:
        pass

class ConcreteProductA(Product):
    """具体产品A"""
    
    def operation(self) -> str:
        return "ConcreteProductA operation"

class ConcreteProductB(Product):
    """具体产品B"""
    
    def operation(self) -> str:
        return "ConcreteProductB operation"

class Creator(ABC):
    """创建者抽象基类"""
    
    @abstractmethod
    def factory_method(self) -> Product:
        pass
    
    def some_operation(self) -> str:
        """使用工厂方法创建产品"""
        product = self.factory_method()
        return f"Creator: {product.operation()}"

class ConcreteCreatorA(Creator):
    """具体创建者A"""
    
    def factory_method(self) -> Product:
        return ConcreteProductA()

class ConcreteCreatorB(Creator):
    """具体创建者B"""
    
    def factory_method(self) -> Product:
        return ConcreteProductB()

class ProductRegistry:
    """产品注册表"""
    
    def __init__(self):
        self._products: Dict[str, Type[Product]] = {}
    
    def register_product(self, name: str, product_class: Type[Product]) -> None:
        """注册产品"""
        self._products[name] = product_class
    
    def create_product(self, name: str) -> Product:
        """创建产品"""
        if name not in self._products:
            raise ValueError(f"Unknown product: {name}")
        return self._products[name]()

# 工厂方法模式示例
def factory_method_example():
    """工厂方法模式示例"""
    print("工厂方法模式示例:")
    print("=" * 50)
    
    # 使用具体创建者
    creator_a = ConcreteCreatorA()
    creator_b = ConcreteCreatorB()
    
    print(f"Creator A: {creator_a.some_operation()}")
    print(f"Creator B: {creator_b.some_operation()}")
    
    # 使用产品注册表
    registry = ProductRegistry()
    registry.register_product("A", ConcreteProductA)
    registry.register_product("B", ConcreteProductB)
    
    product_a = registry.create_product("A")
    product_b = registry.create_product("B")
    
    print(f"Product A: {product_a.operation()}")
    print(f"Product B: {product_b.operation()}")

if __name__ == "__main__":
    factory_method_example()
```

### 1.3 抽象工厂模式 (Abstract Factory Pattern)

**定义**: 提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们的具体类。

**Python实现**:

```python
from abc import ABC, abstractmethod
from typing import List

class AbstractProductA(ABC):
    """抽象产品A"""
    
    @abstractmethod
    def operation_a(self) -> str:
        pass

class AbstractProductB(ABC):
    """抽象产品B"""
    
    @abstractmethod
    def operation_b(self) -> str:
        pass

class ConcreteProductA1(AbstractProductA):
    """具体产品A1"""
    
    def operation_a(self) -> str:
        return "ConcreteProductA1 operation"

class ConcreteProductA2(AbstractProductA):
    """具体产品A2"""
    
    def operation_a(self) -> str:
        return "ConcreteProductA2 operation"

class ConcreteProductB1(AbstractProductB):
    """具体产品B1"""
    
    def operation_b(self) -> str:
        return "ConcreteProductB1 operation"

class ConcreteProductB2(AbstractProductB):
    """具体产品B2"""
    
    def operation_b(self) -> str:
        return "ConcreteProductB2 operation"

class AbstractFactory(ABC):
    """抽象工厂"""
    
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass
    
    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass

class ConcreteFactory1(AbstractFactory):
    """具体工厂1"""
    
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()
    
    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()

class ConcreteFactory2(AbstractFactory):
    """具体工厂2"""
    
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()
    
    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()

class Client:
    """客户端"""
    
    def __init__(self, factory: AbstractFactory):
        self.factory = factory
    
    def run(self) -> List[str]:
        """运行客户端"""
        product_a = self.factory.create_product_a()
        product_b = self.factory.create_product_b()
        
        return [
            product_a.operation_a(),
            product_b.operation_b()
        ]

# 抽象工厂模式示例
def abstract_factory_example():
    """抽象工厂模式示例"""
    print("抽象工厂模式示例:")
    print("=" * 50)
    
    # 使用工厂1
    factory1 = ConcreteFactory1()
    client1 = Client(factory1)
    results1 = client1.run()
    
    print("Factory 1 结果:")
    for result in results1:
        print(f"  {result}")
    
    # 使用工厂2
    factory2 = ConcreteFactory2()
    client2 = Client(factory2)
    results2 = client2.run()
    
    print("Factory 2 结果:")
    for result in results2:
        print(f"  {result}")

if __name__ == "__main__":
    abstract_factory_example()
```

### 1.4 建造者模式 (Builder Pattern)

**定义**: 将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。

**Python实现**:

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class Product:
    """产品类"""
    
    def __init__(self):
        self.parts: List[str] = []
    
    def add_part(self, part: str) -> None:
        """添加部件"""
        self.parts.append(part)
    
    def list_parts(self) -> str:
        """列出所有部件"""
        return f"Product parts: {', '.join(self.parts)}"

class Builder(ABC):
    """建造者抽象基类"""
    
    def __init__(self):
        self.reset()
    
    @abstractmethod
    def reset(self) -> None:
        pass
    
    @abstractmethod
    def build_part_a(self) -> None:
        pass
    
    @abstractmethod
    def build_part_b(self) -> None:
        pass
    
    @abstractmethod
    def build_part_c(self) -> None:
        pass

class ConcreteBuilder1(Builder):
    """具体建造者1"""
    
    def reset(self) -> None:
        self._product = Product()
    
    def build_part_a(self) -> None:
        self._product.add_part("PartA1")
    
    def build_part_b(self) -> None:
        self._product.add_part("PartB1")
    
    def build_part_c(self) -> None:
        self._product.add_part("PartC1")
    
    def get_product(self) -> Product:
        """获取产品"""
        product = self._product
        self.reset()
        return product

class ConcreteBuilder2(Builder):
    """具体建造者2"""
    
    def reset(self) -> None:
        self._product = Product()
    
    def build_part_a(self) -> None:
        self._product.add_part("PartA2")
    
    def build_part_b(self) -> None:
        self._product.add_part("PartB2")
    
    def build_part_c(self) -> None:
        self._product.add_part("PartC2")
    
    def get_product(self) -> Product:
        """获取产品"""
        product = self._product
        self.reset()
        return product

class Director:
    """指挥者"""
    
    def __init__(self):
        self._builder: Optional[Builder] = None
    
    def set_builder(self, builder: Builder) -> None:
        """设置建造者"""
        self._builder = builder
    
    def build_minimal_viable_product(self) -> Product:
        """构建最小可行产品"""
        if self._builder is None:
            raise ValueError("Builder not set")
        
        self._builder.build_part_a()
        return self._builder.get_product()
    
    def build_full_featured_product(self) -> Product:
        """构建完整功能产品"""
        if self._builder is None:
            raise ValueError("Builder not set")
        
        self._builder.build_part_a()
        self._builder.build_part_b()
        self._builder.build_part_c()
        return self._builder.get_product()

# 建造者模式示例
def builder_example():
    """建造者模式示例"""
    print("建造者模式示例:")
    print("=" * 50)
    
    director = Director()
    
    # 使用建造者1
    builder1 = ConcreteBuilder1()
    director.set_builder(builder1)
    
    print("构建最小可行产品:")
    minimal_product = director.build_minimal_viable_product()
    print(f"  {minimal_product.list_parts()}")
    
    print("构建完整功能产品:")
    full_product = director.build_full_featured_product()
    print(f"  {full_product.list_parts()}")
    
    # 使用建造者2
    builder2 = ConcreteBuilder2()
    director.set_builder(builder2)
    
    print("使用建造者2构建完整产品:")
    full_product2 = director.build_full_featured_product()
    print(f"  {full_product2.list_parts()}")

if __name__ == "__main__":
    builder_example()
```

### 1.5 原型模式 (Prototype Pattern)

**定义**: 用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。

**Python实现**:

```python
import copy
from abc import ABC, abstractmethod
from typing import Dict, Any

class Prototype(ABC):
    """原型抽象基类"""
    
    @abstractmethod
    def clone(self) -> 'Prototype':
        pass

class ConcretePrototype1(Prototype):
    """具体原型1"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
    
    def clone(self) -> 'ConcretePrototype1':
        """浅拷贝"""
        return copy.copy(self)
    
    def deep_clone(self) -> 'ConcretePrototype1':
        """深拷贝"""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return f"ConcretePrototype1(data={self.data})"

class ConcretePrototype2(Prototype):
    """具体原型2"""
    
    def __init__(self, value: int, text: str):
        self.value = value
        self.text = text
    
    def clone(self) -> 'ConcretePrototype2':
        """浅拷贝"""
        return copy.copy(self)
    
    def deep_clone(self) -> 'ConcretePrototype2':
        """深拷贝"""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return f"ConcretePrototype2(value={self.value}, text='{self.text}')"

class PrototypeRegistry:
    """原型注册表"""
    
    def __init__(self):
        self._prototypes: Dict[str, Prototype] = {}
    
    def register_prototype(self, name: str, prototype: Prototype) -> None:
        """注册原型"""
        self._prototypes[name] = prototype
    
    def create_prototype(self, name: str) -> Prototype:
        """创建原型副本"""
        if name not in self._prototypes:
            raise ValueError(f"Unknown prototype: {name}")
        return self._prototypes[name].clone()

# 原型模式示例
def prototype_example():
    """原型模式示例"""
    print("原型模式示例:")
    print("=" * 50)
    
    # 创建原型
    prototype1 = ConcretePrototype1({"key1": "value1", "key2": [1, 2, 3]})
    prototype2 = ConcretePrototype2(42, "Hello, Prototype!")
    
    print("原始原型:")
    print(f"  {prototype1}")
    print(f"  {prototype2}")
    
    # 浅拷贝
    clone1 = prototype1.clone()
    clone2 = prototype2.clone()
    
    print("\n浅拷贝:")
    print(f"  {clone1}")
    print(f"  {clone2}")
    
    # 修改原始对象
    prototype1.data["key1"] = "modified"
    prototype1.data["key2"].append(4)
    prototype2.value = 100
    
    print("\n修改原始对象后:")
    print(f"  原始: {prototype1}")
    print(f"  浅拷贝: {clone1}")
    print(f"  原始: {prototype2}")
    print(f"  浅拷贝: {clone2}")
    
    # 深拷贝
    deep_clone1 = prototype1.deep_clone()
    deep_clone2 = prototype2.deep_clone()
    
    print("\n深拷贝:")
    print(f"  {deep_clone1}")
    print(f"  {deep_clone2}")
    
    # 原型注册表
    registry = PrototypeRegistry()
    registry.register_prototype("prototype1", prototype1)
    registry.register_prototype("prototype2", prototype2)
    
    print("\n使用原型注册表:")
    new_prototype1 = registry.create_prototype("prototype1")
    new_prototype2 = registry.create_prototype("prototype2")
    
    print(f"  {new_prototype1}")
    print(f"  {new_prototype2}")

if __name__ == "__main__":
    prototype_example()
```

## 2. 结构型模式 (Structural Patterns)

### 2.1 适配器模式 (Adapter Pattern)

**定义**: 将一个类的接口转换成客户希望的另外一个接口。

**Python实现**:

```python
from abc import ABC, abstractmethod
from typing import List

class Target(ABC):
    """目标接口"""
    
    @abstractmethod
    def request(self) -> str:
        pass

class Adaptee:
    """需要适配的类"""
    
    def specific_request(self) -> str:
        return "Adaptee's specific request"

class Adapter(Target):
    """适配器"""
    
    def __init__(self, adaptee: Adaptee):
        self.adaptee = adaptee
    
    def request(self) -> str:
        return f"Adapter: {self.adaptee.specific_request()}"

class ObjectAdapter(Target):
    """对象适配器"""
    
    def __init__(self, adaptee: Adaptee):
        self.adaptee = adaptee
    
    def request(self) -> str:
        return f"Object Adapter: {self.adaptee.specific_request()}"

class ClassAdapter(Adaptee, Target):
    """类适配器"""
    
    def request(self) -> str:
        return f"Class Adapter: {self.specific_request()}"

# 适配器模式示例
def adapter_example():
    """适配器模式示例"""
    print("适配器模式示例:")
    print("=" * 50)
    
    adaptee = Adaptee()
    
    # 对象适配器
    object_adapter = ObjectAdapter(adaptee)
    print(f"对象适配器: {object_adapter.request()}")
    
    # 类适配器
    class_adapter = ClassAdapter()
    print(f"类适配器: {class_adapter.request()}")

if __name__ == "__main__":
    adapter_example()
```

## 导航链接

- **上级目录**: [../README.md](../README.md)
- **同级目录**:
  - [02-架构模式/](02-架构模式/)
  - [03-并发编程/](03-并发编程/)
  - [04-分布式系统/](04-分布式系统/)
  - [05-网络编程/](05-网络编程/)
  - [06-安全编程/](06-安全编程/)
- **下级目录**:
  - [01-创建型模式/](01-创建型模式/)
  - [02-结构型模式/](02-结构型模式/)
  - [03-行为型模式/](03-行为型模式/)
  - [04-并发模式/](04-并发模式/)
  - [05-分布式模式/](05-分布式模式/)

## 参考文献

1. Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.
2. Freeman, E., Robson, E., Sierra, K., & Bates, B. (2004). Head First Design Patterns. O'Reilly Media.
3. Larman, C. (2004). Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development. Prentice Hall.
