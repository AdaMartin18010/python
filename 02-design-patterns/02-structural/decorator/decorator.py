# Decorator Pattern - 装饰器模式
# 核心实现

"""装饰器模式的多种实现方式"""

from abc import ABC, abstractmethod

# 组件接口
class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

# 具体组件
class ConcreteComponent(Component):
    def operation(self) -> str:
        return "ConcreteComponent"

# 装饰器基类
class Decorator(Component):
    def __init__(self, component: Component):
        self._component = component
    
    def operation(self) -> str:
        return self._component.operation()

# 具体装饰器A
class ConcreteDecoratorA(Decorator):
    def operation(self) -> str:
        return f"DecoratorA({super().operation()})"

# 具体装饰器B
class ConcreteDecoratorB(Decorator):
    def operation(self) -> str:
        return f"DecoratorB({super().operation()})"

if __name__ == "__main__":
    component = ConcreteComponent()
    print("基础组件:", component.operation())
    
    decorator1 = ConcreteDecoratorA(component)
    print("装饰器A:", decorator1.operation())
    
    decorator2 = ConcreteDecoratorB(decorator1)
    print("装饰器B:", decorator2.operation())
