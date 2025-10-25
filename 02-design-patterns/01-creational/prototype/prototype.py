# Prototype Pattern - 原型模式
# 核心实现

"""原型模式的5种实现方式"""

import copy
from abc import ABC, abstractmethod

class Prototype(ABC):
    @abstractmethod
    def clone(self): pass

class ConcretePrototype(Prototype):
    def __init__(self, value: str):
        self.value = value
        self.data = []
    
    def clone(self):
        return copy.deepcopy(self)

class PrototypeRegistry:
    _prototypes = {}
    
    @classmethod
    def register(cls, name: str, prototype):
        cls._prototypes[name] = prototype
    
    @classmethod
    def clone(cls, name: str):
        return copy.deepcopy(cls._prototypes[name])

if __name__ == "__main__":
    original = ConcretePrototype("Original")
    original.data = [1, 2, 3]
    
    cloned = original.clone()
    cloned.value = "Cloned"
    cloned.data.append(4)
    
    print(f"Original: {original.value}, {original.data}")
    print(f"Cloned: {cloned.value}, {cloned.data}")
