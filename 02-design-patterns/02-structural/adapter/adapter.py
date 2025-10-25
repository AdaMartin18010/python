# Adapter Pattern - 适配器模式
# 核心实现

"""适配器模式的多种实现方式"""

from abc import ABC, abstractmethod

# 目标接口
class Target(ABC):
    @abstractmethod
    def request(self) -> str:
        pass

# 需要适配的类
class Adaptee:
    def specific_request(self) -> str:
        return "Adaptee的特殊请求"

# 类适配器（继承）
class ClassAdapter(Adaptee, Target):
    def request(self) -> str:
        return f"ClassAdapter: {self.specific_request()}"

# 对象适配器（组合）
class ObjectAdapter(Target):
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee
    
    def request(self) -> str:
        return f"ObjectAdapter: {self._adaptee.specific_request()}"

if __name__ == "__main__":
    print("类适配器:")
    adapter1 = ClassAdapter()
    print(adapter1.request())
    
    print("\n对象适配器:")
    adaptee = Adaptee()
    adapter2 = ObjectAdapter(adaptee)
    print(adapter2.request())
