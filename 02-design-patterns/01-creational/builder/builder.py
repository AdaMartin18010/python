# Builder Pattern - 建造者模式
# 核心实现文件

"""建造者模式的5种实现方式"""

from abc import ABC, abstractmethod

class Product:
    def __init__(self):
        self.parts = []
    
    def add(self, part: str):
        self.parts.append(part)
    
    def list_parts(self) -> str:
        return f"Product parts: {', '.join(self.parts)}"

class Builder(ABC):
    @abstractmethod
    def build_part_a(self): pass
    
    @abstractmethod
    def build_part_b(self): pass
    
    @abstractmethod
    def get_result(self) -> Product: pass

class ConcreteBuilder(Builder):
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._product = Product()
    
    def build_part_a(self):
        self._product.add("PartA")
    
    def build_part_b(self):
        self._product.add("PartB")
    
    def get_result(self) -> Product:
        product = self._product
        self.reset()
        return product

class Director:
    def __init__(self, builder: Builder):
        self._builder = builder
    
    def build_minimal_product(self):
        self._builder.build_part_a()
    
    def build_full_product(self):
        self._builder.build_part_a()
        self._builder.build_part_b()

if __name__ == "__main__":
    builder = ConcreteBuilder()
    director = Director(builder)
    
    print("Basic product:")
    director.build_minimal_product()
    print(builder.get_result().list_parts())
    
    print("\nFull product:")
    director.build_full_product()
    print(builder.get_result().list_parts())
