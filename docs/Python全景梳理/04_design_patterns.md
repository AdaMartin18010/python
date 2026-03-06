# GoF 23种设计模式 Python实现完全指南

> **版本**: 1.0
> **目标读者**: Python开发者、架构师
> **适用范围**: Python 3.8+

---

## 目录

- [GoF 23种设计模式 Python实现完全指南](#gof-23种设计模式-python实现完全指南)
  - [目录](#目录)
  - [第一部分：创建型模式（5种）](#第一部分创建型模式5种)
    - [1.1 单例模式（Singleton）](#11-单例模式singleton)
      - [意图](#意图)
      - [适用场景](#适用场景)
      - [UML结构图](#uml结构图)
      - [Python实现](#python实现)
        - [方式1：使用 `__new__` 方法（基础版）](#方式1使用-__new__-方法基础版)
        - [方式2：线程安全版本（使用锁）](#方式2线程安全版本使用锁)
        - [方式3：使用装饰器](#方式3使用装饰器)
        - [方式4：使用元类](#方式4使用元类)
      - [正例：配置管理器](#正例配置管理器)
      - [反例：滥用单例](#反例滥用单例)
      - [优缺点分析](#优缺点分析)
      - [与其他模式的关系](#与其他模式的关系)
    - [1.2 工厂方法模式（Factory Method）](#12-工厂方法模式factory-method)
      - [意图](#意图-1)
      - [适用场景](#适用场景-1)
      - [UML结构图](#uml结构图-1)
      - [Python实现](#python实现-1)
      - [正例：动态工厂注册](#正例动态工厂注册)
      - [反例：简单工厂误用](#反例简单工厂误用)
      - [优缺点分析](#优缺点分析-1)
    - [1.3 抽象工厂模式（Abstract Factory）](#13-抽象工厂模式abstract-factory)
      - [意图](#意图-2)
      - [适用场景](#适用场景-2)
      - [UML结构图](#uml结构图-2)
      - [Python实现](#python实现-2)
      - [正例：数据库访问层](#正例数据库访问层)
      - [反例：工厂方法误用](#反例工厂方法误用)
      - [优缺点分析](#优缺点分析-2)
    - [1.4 建造者模式（Builder）](#14-建造者模式builder)
      - [意图](#意图-3)
      - [适用场景](#适用场景-3)
      - [UML结构图](#uml结构图-3)
      - [Python实现](#python实现-3)
      - [Pythonic变体：链式调用建造者](#pythonic变体链式调用建造者)
      - [正例：HTTP请求构建器](#正例http请求构建器)
      - [反例：巨型构造函数](#反例巨型构造函数)
      - [优缺点分析](#优缺点分析-3)
    - [1.5 原型模式（Prototype）](#15-原型模式prototype)
      - [意图](#意图-4)
      - [适用场景](#适用场景-4)
      - [UML结构图](#uml结构图-4)
      - [Python实现](#python实现-4)
      - [正例：Python的copy模块](#正例python的copy模块)
      - [反例：直接实例化](#反例直接实例化)
      - [优缺点分析](#优缺点分析-4)
  - [第二部分：结构型模式（7种）](#第二部分结构型模式7种)
    - [2.1 适配器模式（Adapter）](#21-适配器模式adapter)
      - [意图](#意图-5)
      - [适用场景](#适用场景-5)
      - [UML结构图](#uml结构图-5)
      - [Python实现](#python实现-5)
      - [正例：第三方库适配](#正例第三方库适配)
      - [反例：直接依赖具体类](#反例直接依赖具体类)
      - [优缺点分析](#优缺点分析-5)
    - [2.2 桥接模式（Bridge）](#22-桥接模式bridge)
      - [意图](#意图-6)
      - [适用场景](#适用场景-6)
      - [UML结构图](#uml结构图-6)
      - [Python实现](#python实现-6)
      - [正例：消息发送系统](#正例消息发送系统)
      - [反例：类爆炸](#反例类爆炸)
      - [优缺点分析](#优缺点分析-6)
    - [2.3 组合模式（Composite）](#23-组合模式composite)
      - [意图](#意图-7)
      - [适用场景](#适用场景-7)
      - [UML结构图](#uml结构图-7)
      - [Python实现](#python实现-7)
      - [正例：UI组件树](#正例ui组件树)
      - [反例：区别对待叶节点和组合](#反例区别对待叶节点和组合)
      - [优缺点分析](#优缺点分析-7)
    - [2.4 装饰器模式（Decorator）](#24-装饰器模式decorator)
      - [意图](#意图-8)
      - [适用场景](#适用场景-8)
      - [UML结构图](#uml结构图-8)
      - [Python实现](#python实现-8)
      - [Python装饰器 vs 装饰器模式](#python装饰器-vs-装饰器模式)
      - [正例：IO流装饰](#正例io流装饰)
      - [反例：子类爆炸](#反例子类爆炸)
      - [优缺点分析](#优缺点分析-8)
    - [2.5 外观模式（Facade）](#25-外观模式facade)
      - [意图](#意图-9)
      - [适用场景](#适用场景-9)
      - [UML结构图](#uml结构图-9)
      - [Python实现](#python实现-9)
      - [正例：API网关](#正例api网关)
      - [反例：外观过于庞大](#反例外观过于庞大)
      - [优缺点分析](#优缺点分析-9)
    - [2.6 享元模式（Flyweight）](#26-享元模式flyweight)
      - [意图](#意图-10)
      - [适用场景](#适用场景-10)
      - [UML结构图](#uml结构图-10)
      - [Python实现](#python实现-10)
      - [正例：字符渲染](#正例字符渲染)
      - [反例：过度优化](#反例过度优化)
      - [优缺点分析](#优缺点分析-10)
    - [2.7 代理模式（Proxy）](#27-代理模式proxy)
      - [意图](#意图-11)
      - [适用场景](#适用场景-11)
      - [UML结构图](#uml结构图-11)
      - [Python实现](#python实现-11)
      - [正例：数据库连接池](#正例数据库连接池)
      - [反例：过度代理](#反例过度代理)
      - [优缺点分析](#优缺点分析-11)
  - [第三部分：行为型模式（11种）](#第三部分行为型模式11种)
    - [3.1 责任链模式（Chain of Responsibility）](#31-责任链模式chain-of-responsibility)
      - [意图](#意图-12)
      - [适用场景](#适用场景-12)
      - [UML结构图](#uml结构图-12)
      - [Python实现](#python实现-12)
      - [正例：中间件链](#正例中间件链)
      - [反例：硬编码条件判断](#反例硬编码条件判断)
      - [优缺点分析](#优缺点分析-12)
    - [3.2 命令模式（Command）](#32-命令模式command)
      - [意图](#意图-13)
      - [适用场景](#适用场景-13)
      - [UML结构图](#uml结构图-13)
      - [Python实现](#python实现-13)
      - [正例：任务队列](#正例任务队列)
      - [反例：直接调用](#反例直接调用)
      - [优缺点分析](#优缺点分析-13)
    - [3.3 解释器模式（Interpreter）](#33-解释器模式interpreter)
      - [意图](#意图-14)
      - [适用场景](#适用场景-14)
      - [UML结构图](#uml结构图-14)
      - [Python实现](#python实现-14)
      - [正例：SQL查询构建器](#正例sql查询构建器)
      - [反例：复杂文法](#反例复杂文法)
      - [优缺点分析](#优缺点分析-14)
    - [3.4 迭代器模式（Iterator）](#34-迭代器模式iterator)
      - [意图](#意图-15)
      - [适用场景](#适用场景-15)
      - [Python实现](#python实现-15)
      - [Python迭代器协议](#python迭代器协议)
      - [正例：二叉树迭代器](#正例二叉树迭代器)
      - [优缺点分析](#优缺点分析-15)
    - [3.5 中介者模式（Mediator）](#35-中介者模式mediator)
      - [意图](#意图-16)
      - [适用场景](#适用场景-16)
      - [UML结构图](#uml结构图-15)
      - [Python实现](#python实现-16)
      - [正例：MVC控制器](#正例mvc控制器)
      - [反例：上帝中介者](#反例上帝中介者)
      - [优缺点分析](#优缺点分析-16)
    - [3.6 备忘录模式（Memento）](#36-备忘录模式memento)
      - [意图](#意图-17)
      - [适用场景](#适用场景-17)
      - [Python实现](#python实现-17)
      - [正例：游戏存档系统](#正例游戏存档系统)
      - [反例：破坏封装](#反例破坏封装)
      - [优缺点分析](#优缺点分析-17)
    - [3.7 观察者模式（Observer）](#37-观察者模式observer)
      - [意图](#意图-18)
      - [适用场景](#适用场景-18)
      - [Python实现](#python实现-18)
      - [Pythonic实现：使用内置功能](#pythonic实现使用内置功能)
      - [反例：紧耦合通知](#反例紧耦合通知)
      - [优缺点分析](#优缺点分析-18)
    - [3.8 状态模式（State）](#38-状态模式state)
      - [意图](#意图-19)
      - [适用场景](#适用场景-19)
      - [Python实现](#python实现-19)
      - [正例：游戏角色状态](#正例游戏角色状态)
      - [反例：巨型条件语句](#反例巨型条件语句)
      - [优缺点分析](#优缺点分析-19)
    - [3.9 策略模式（Strategy）](#39-策略模式strategy)
      - [意图](#意图-20)
      - [适用场景](#适用场景-20)
      - [Python实现](#python实现-20)
      - [正例：支付策略](#正例支付策略)
      - [Pythonic实现：使用函数](#pythonic实现使用函数)
      - [反例：条件选择算法](#反例条件选择算法)
      - [优缺点分析](#优缺点分析-20)
    - [3.10 模板方法模式（Template Method）](#310-模板方法模式template-method)
      - [意图](#意图-21)
      - [适用场景](#适用场景-21)
      - [Python实现](#python实现-21)
      - [正例：测试框架](#正例测试框架)
      - [反例：重复代码](#反例重复代码)
      - [优缺点分析](#优缺点分析-21)
    - [3.11 访问者模式（Visitor）](#311-访问者模式visitor)
      - [意图](#意图-22)
      - [适用场景](#适用场景-22)
      - [Python实现](#python实现-22)
      - [正例：AST遍历](#正例ast遍历)
      - [反例：违反开闭原则](#反例违反开闭原则)
      - [优缺点分析](#优缺点分析-22)
  - [第四部分：Pythonic设计模式变体](#第四部分pythonic设计模式变体)
    - [4.1 Borg模式（单例变体）](#41-borg模式单例变体)
      - [意图](#意图-23)
      - [与单例模式的区别](#与单例模式的区别)
      - [Python实现](#python实现-23)
    - [4.2 注册表模式](#42-注册表模式)
      - [意图](#意图-24)
      - [Python实现](#python实现-24)
    - [4.3 混入模式（Mixin）](#43-混入模式mixin)
      - [意图](#意图-25)
      - [Python实现](#python实现-25)
  - [第五部分：反模式](#第五部分反模式)
    - [5.1 上帝对象（God Object）](#51-上帝对象god-object)
      - [问题描述](#问题描述)
      - [反例](#反例)
      - [正确设计](#正确设计)
    - [5.2 循环依赖](#52-循环依赖)
      - [问题描述](#问题描述-1)
      - [反例](#反例-1)
      - [解决方案](#解决方案)
    - [5.3 过度设计](#53-过度设计)
      - [问题描述](#问题描述-2)
      - [反例](#反例-2)
      - [正确设计](#正确设计-1)
    - [5.4 重复代码](#54-重复代码)
      - [问题描述](#问题描述-3)
      - [反例](#反例-3)
      - [解决方案](#解决方案-1)
  - [附录：设计模式速查表](#附录设计模式速查表)
    - [创建型模式](#创建型模式)
    - [结构型模式](#结构型模式)
    - [行为型模式](#行为型模式)
  - [总结](#总结)
    - [设计原则](#设计原则)
    - [模式选择指南](#模式选择指南)

---

## 第一部分：创建型模式（5种）

创建型模式关注对象的创建机制，试图在创建对象的同时隐藏创建逻辑，而非直接使用 new 运算符实例化对象。

---

### 1.1 单例模式（Singleton）

#### 意图

确保一个类只有一个实例，并提供一个全局访问点。

#### 适用场景

- 需要控制共享资源访问（数据库连接池、线程池）
- 需要全局状态管理（配置管理器、日志记录器）
- 需要唯一实例协调系统行为

#### UML结构图

```
┌─────────────────┐
│    Singleton    │
├─────────────────┤
│ - _instance     │
├─────────────────┤
│ + get_instance()│
│ + business_method│
└─────────────────┘
```

#### Python实现

##### 方式1：使用 `__new__` 方法（基础版）

```python
class Singleton:
    """使用__new__实现的单例模式（非线程安全）"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        # 注意：每次获取实例都会调用__init__
        if value is not None:
            self.value = value


# 测试
s1 = Singleton("first")
s2 = Singleton("second")
print(s1 is s2)  # True
print(s1.value)  # second（被覆盖了）
```

##### 方式2：线程安全版本（使用锁）

```python
import threading


class ThreadSafeSingleton:
    """线程安全的单例模式"""
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                # 双重检查锁定
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        # 确保__init__只执行一次
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self.value = value
                    self._initialized = True


# 多线程测试
def test_singleton(value):
    instance = ThreadSafeSingleton(value)
    print(f"Instance value: {instance.value}")


threads = []
for i in range(10):
    t = threading.Thread(target=test_singleton, args=(f"thread-{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

##### 方式3：使用装饰器

```python
from functools import wraps


def singleton(cls):
    """单例装饰器"""
    instances = {}
    lock = threading.Lock()

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class DatabaseConnection:
    """数据库连接单例"""
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = f"Connected to {self.connection_string}"
        return self.connection


# 测试
db1 = DatabaseConnection("postgresql://localhost/db")
db2 = DatabaseConnection("mysql://localhost/db")  # 参数被忽略
print(db1 is db2)  # True
print(db1.connection_string)  # postgresql://localhost/db
```

##### 方式4：使用元类

```python
class SingletonMeta(type):
    """单例元类"""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    """日志记录器单例"""
    def __init__(self):
        self.logs = []

    def log(self, message):
        self.logs.append(message)
        print(f"[LOG] {message}")


# 测试
logger1 = Logger()
logger2 = Logger()
logger1.log("Message 1")
logger2.log("Message 2")
print(logger1 is logger2)  # True
print(logger1.logs)  # ['Message 1', 'Message 2']
```

#### 正例：配置管理器

```python
import json
from pathlib import Path


class AppConfig(metaclass=SingletonMeta):
    """应用配置单例 - 正确使用示例"""

    def __init__(self):
        self._config = {}
        self._config_file = Path("config.json")
        self._load_config()

    def _load_config(self):
        """从文件加载配置"""
        if self._config_file.exists():
            with open(self._config_file, 'r') as f:
                self._config = json.load(f)

    def get(self, key, default=None):
        """获取配置项"""
        return self._config.get(key, default)

    def set(self, key, value):
        """设置配置项"""
        self._config[key] = value
        self._save_config()

    def _save_config(self):
        """保存配置到文件"""
        with open(self._config_file, 'w') as f:
            json.dump(self._config, f, indent=2)


# 使用示例
def module_a():
    config = AppConfig()
    config.set("database_url", "postgresql://localhost/mydb")

def module_b():
    config = AppConfig()
    print(config.get("database_url"))  # 获取module_a设置的值

module_a()
module_b()  # 输出: postgresql://localhost/mydb
```

#### 反例：滥用单例

```python
# ❌ 错误：将业务对象设计为单例
class UserService(metaclass=SingletonMeta):
    """用户服务 - 错误设计"""
    def __init__(self):
        self.current_user = None

    def login(self, user):
        self.current_user = user

# 问题：
# 1. 无法支持多用户并发
# 2. 测试困难，状态难以隔离
# 3. 违反单一职责原则

# ✅ 正确设计：依赖注入
class UserService:
    """用户服务 - 正确设计"""
    def __init__(self, user_repository, session_manager):
        self.user_repository = user_repository
        self.session_manager = session_manager

    def login(self, username, password):
        user = self.user_repository.find_by_username(username)
        if user and user.verify_password(password):
            return self.session_manager.create_session(user)
        return None
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 全局唯一访问点 | 违反单一职责原则 |
| 节省资源 | 隐藏依赖关系，难以测试 |
| 控制共享资源 | 多线程环境下需要额外处理 |
| 懒加载可能 | 扩展困难（继承问题） |

#### 与其他模式的关系

- **外观模式**：外观类通常设计为单例
- **抽象工厂**：工厂本身可以是单例
- **享元模式**：享元工厂通常是单例

---

### 1.2 工厂方法模式（Factory Method）

#### 意图

定义一个创建对象的接口，让子类决定实例化哪个类。

#### 适用场景

- 不知道确切类型时需要创建对象
- 希望由子类决定创建哪种对象
- 需要解耦对象创建与使用

#### UML结构图

```
┌──────────────────┐         ┌──────────────────┐
│   Creator        │<>───────│   Product        │
├──────────────────┤         ├──────────────────┤
│ + factory_method │         │ + operation()    │
│ + operation()    │         └──────────────────┘
└──────────────────┘                  △
         △                            │
         │                  ┌─────────┴─────────┐
┌────────┴────────┐         │                   │
│ ConcreteCreatorA│         │  ConcreteProductA │
│ ConcreteCreatorB│         │  ConcreteProductB │
└─────────────────┘         └───────────────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from enum import Enum


# 产品接口
class Notification(ABC):
    """通知接口"""

    @abstractmethod
    def send(self, message: str, recipient: str) -> None:
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        pass


# 具体产品
class EmailNotification(Notification):
    """邮件通知"""

    def send(self, message: str, recipient: str) -> None:
        print(f"[Email] To: {recipient}")
        print(f"[Email] Message: {message}")

    def get_channel_name(self) -> str:
        return "Email"


class SMSNotification(Notification):
    """短信通知"""

    def send(self, message: str, recipient: str) -> None:
        print(f"[SMS] To: {recipient}")
        print(f"[SMS] Message: {message[:100]}...")  # 短信截断

    def get_channel_name(self) -> str:
        return "SMS"


class PushNotification(Notification):
    """推送通知"""

    def send(self, message: str, recipient: str) -> None:
        print(f"[Push] To device: {recipient}")
        print(f"[Push] Message: {message}")

    def get_channel_name(self) -> str:
        return "Push"


# 创建者抽象类
class NotificationFactory(ABC):
    """通知工厂抽象类"""

    @abstractmethod
    def create_notification(self) -> Notification:
        """工厂方法 - 由子类实现"""
        pass

    def notify(self, message: str, recipient: str) -> None:
        """使用工厂方法创建产品并执行操作"""
        notification = self.create_notification()
        print(f"Using channel: {notification.get_channel_name()}")
        notification.send(message, recipient)


# 具体创建者
class EmailNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return EmailNotification()


class SMSNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return SMSNotification()


class PushNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return PushNotification()


# 使用示例
def client_code(factory: NotificationFactory):
    """客户端代码 - 只依赖抽象"""
    factory.notify(
        message="Your order has been shipped!",
        recipient="user@example.com"
    )


# 测试
print("=== Email Notification ===")
client_code(EmailNotificationFactory())

print("\n=== SMS Notification ===")
client_code(SMSNotificationFactory())

print("\n=== Push Notification ===")
client_code(PushNotificationFactory())
```

#### 正例：动态工厂注册

```python
class NotificationRegistry:
    """通知工厂注册表 - 扩展性更好"""
    _factories = {}

    @classmethod
    def register(cls, channel_type: str, factory_class):
        cls._factories[channel_type] = factory_class

    @classmethod
    def create(cls, channel_type: str) -> Notification:
        if channel_type not in cls._factories:
            raise ValueError(f"Unknown channel type: {channel_type}")
        return cls._factories[channel_type]()


# 注册工厂
NotificationRegistry.register("email", EmailNotification)
NotificationRegistry.register("sms", SMSNotification)
NotificationRegistry.register("push", PushNotification)


# 动态创建
def send_notification(channel_type: str, message: str, recipient: str):
    notification = NotificationRegistry.create(channel_type)
    notification.send(message, recipient)


# 使用
send_notification("email", "Hello!", "user@example.com")
send_notification("sms", "Hello!", "+1234567890")
```

#### 反例：简单工厂误用

```python
# ❌ 错误：简单工厂违反开闭原则
class BadNotificationFactory:
    """简单工厂 - 新增类型需要修改此类"""

    @staticmethod
    def create(channel_type: str) -> Notification:
        if channel_type == "email":
            return EmailNotification()
        elif channel_type == "sms":
            return SMSNotification()
        elif channel_type == "push":
            return PushNotification()
        else:
            raise ValueError(f"Unknown type: {channel_type}")

# 问题：
# 1. 新增通知类型需要修改工厂类
# 2. 违反开闭原则
# 3. 工厂类会变得臃肿

# ✅ 正确：使用工厂方法或注册表模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 符合开闭原则 | 代码复杂度增加 |
| 解耦创建与使用 | 需要更多类 |
| 易于扩展新产品 | 每个产品需要对应创建者 |
| 单一职责原则 | 小型项目可能过度设计 |

---

### 1.3 抽象工厂模式（Abstract Factory）

#### 意图

创建相关或依赖对象的家族，而不需要明确指定具体类。

#### 适用场景

- 需要创建一系列相关产品
- 系统需要独立于产品创建方式
- 需要保证产品家族的一致性

#### UML结构图

```
┌─────────────────────┐
│   AbstractFactory   │
├─────────────────────┤
│ + create_product_a()│
│ + create_product_b()│
└─────────────────────┘
          △
          │
    ┌─────┴─────┐
    │           │
┌───┴───┐   ┌───┴────┐
│Factory1│   │Factory2│
└────────┘   └────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod


# ============ 抽象产品接口 ============

class Button(ABC):
    """按钮抽象类"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_click(self) -> None:
        pass


class Checkbox(ABC):
    """复选框抽象类"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def toggle(self) -> None:
        pass


class TextField(ABC):
    """文本框抽象类"""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def set_text(self, text: str) -> None:
        pass


# ============ 具体产品：Windows风格 ============

class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Style Button]"

    def on_click(self) -> None:
        print("Windows button clicked!")


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[Windows Style Checkbox]"

    def toggle(self) -> None:
        print("Windows checkbox toggled!")


class WindowsTextField(TextField):
    def render(self) -> str:
        return "[Windows Style TextField]"

    def set_text(self, text: str) -> None:
        print(f"Windows text field set to: {text}")


# ============ 具体产品：MacOS风格 ============

class MacButton(Button):
    def render(self) -> str:
        return "[MacOS Style Button]"

    def on_click(self) -> None:
        print("Mac button clicked!")


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "[MacOS Style Checkbox]"

    def toggle(self) -> None:
        print("Mac checkbox toggled!")


class MacTextField(TextField):
    def render(self) -> str:
        return "[MacOS Style TextField]"

    def set_text(self, text: str) -> None:
        print(f"Mac text field set to: {text}")


# ============ 抽象工厂 ============

class GUIFactory(ABC):
    """GUI工厂抽象类"""

    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

    @abstractmethod
    def create_text_field(self) -> TextField:
        pass


# ============ 具体工厂 ============

class WindowsFactory(GUIFactory):
    """Windows GUI工厂"""

    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

    def create_text_field(self) -> TextField:
        return WindowsTextField()


class MacFactory(GUIFactory):
    """MacOS GUI工厂"""

    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

    def create_text_field(self) -> TextField:
        return MacTextField()


# ============ 客户端代码 ============

class Application:
    """应用程序 - 只依赖抽象"""

    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()
        self.text_field = factory.create_text_field()

    def render_ui(self):
        """渲染UI"""
        print("Rendering UI components:")
        print(f"  {self.button.render()}")
        print(f"  {self.checkbox.render()}")
        print(f"  {self.text_field.render()}")

    def interact(self):
        """交互"""
        self.button.on_click()
        self.checkbox.toggle()
        self.text_field.set_text("Hello, World!")


def get_factory(os_type: str) -> GUIFactory:
    """根据操作系统类型获取对应工厂"""
    factories = {
        "windows": WindowsFactory,
        "mac": MacFactory,
    }
    return factories.get(os_type.lower(), WindowsFactory)()


# 测试
print("=== Windows Application ===")
windows_app = Application(get_factory("windows"))
windows_app.render_ui()
windows_app.interact()

print("\n=== MacOS Application ===")
mac_app = Application(get_factory("mac"))
mac_app.render_ui()
mac_app.interact()
```

#### 正例：数据库访问层

```python
# 抽象产品
class Connection(ABC):
    @abstractmethod
    def execute(self, query: str): pass

class Transaction(ABC):
    @abstractmethod
    def commit(self): pass

class ResultSet(ABC):
    @abstractmethod
    def fetch_all(self): pass


# 抽象工厂
class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection: pass

    @abstractmethod
    def create_transaction(self) -> Transaction: pass


# PostgreSQL实现
class PostgreSQLConnection(Connection):
    def execute(self, query: str):
        print(f"PostgreSQL executing: {query}")
        return []

class PostgreSQLTransaction(Transaction):
    def commit(self):
        print("PostgreSQL transaction committed")

class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return PostgreSQLConnection()

    def create_transaction(self) -> Transaction:
        return PostgreSQLTransaction()


# MySQL实现
class MySQLConnection(Connection):
    def execute(self, query: str):
        print(f"MySQL executing: {query}")
        return []

class MySQLTransaction(Transaction):
    def commit(self):
        print("MySQL transaction committed")

class MySQLFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return MySQLConnection()

    def create_transaction(self) -> Transaction:
        return MySQLTransaction()


# DAO层 - 完全独立于具体数据库
class UserDAO:
    def __init__(self, factory: DatabaseFactory):
        self.connection = factory.create_connection()
        self.transaction = factory.create_transaction()

    def find_by_id(self, user_id: int):
        self.connection.execute(f"SELECT * FROM users WHERE id = {user_id}")

    def save(self, user):
        self.connection.execute(f"INSERT INTO users ...")
        self.transaction.commit()
```

#### 反例：工厂方法误用

```python
# ❌ 错误：当需要产品家族时使用工厂方法
class BadApplication:
    """错误设计：混用不同风格的产品"""

    def __init__(self):
        # 混用了不同工厂的产品！
        self.button = WindowsButton()  # Windows风格
        self.checkbox = MacCheckbox()  # Mac风格 - 不一致！

# 问题：
# 1. UI风格不一致
# 2. 难以保证产品兼容性
# 3. 客户端需要了解所有具体类

# ✅ 正确：使用抽象工厂保证产品家族一致性
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 保证产品家族一致性 | 增加代码复杂度 |
| 易于切换产品家族 | 难以支持新产品类型 |
| 符合开闭原则 | 需要大量接口和类 |
| 隔离具体类 | 工厂和产品等级结构复杂 |

---

### 1.4 建造者模式（Builder）

#### 意图

将复杂对象的构建与其表示分离，使同样的构建过程可以创建不同的表示。

#### 适用场景

- 对象构建过程复杂（多步骤）
- 需要创建不同表示的相同类型对象
- 需要控制对象构建顺序

#### UML结构图

```
┌─────────────┐         ┌─────────────┐
│   Director  │────────>│   Builder   │
└─────────────┘         ├─────────────┤
                        │ + build_part│
                        └─────────────┘
                                △
                        ┌───────┴───────┐
                        │               │
                   ┌────┴────┐     ┌────┴────┐
                   │Concrete1│     │Concrete2│
                   └─────────┘     └─────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass


# ============ 产品 ============

@dataclass
class Computer:
    """电脑产品"""
    cpu: str = ""
    memory: str = ""
    storage: str = ""
    gpu: str = ""
    motherboard: str = ""
    power_supply: str = ""
    case: str = ""

    def __str__(self):
        return f"""Computer Configuration:
  CPU: {self.cpu}
  Memory: {self.memory}
  Storage: {self.storage}
  GPU: {self.gpu}
  Motherboard: {self.motherboard}
  Power Supply: {self.power_supply}
  Case: {self.case}"""


# ============ 抽象建造者 ============

class ComputerBuilder(ABC):
    """电脑建造者抽象类"""

    def __init__(self):
        self.computer = Computer()

    @abstractmethod
    def build_cpu(self) -> 'ComputerBuilder':
        pass

    @abstractmethod
    def build_memory(self) -> 'ComputerBuilder':
        pass

    @abstractmethod
    def build_storage(self) -> 'ComputerBuilder':
        pass

    @abstractmethod
    def build_gpu(self) -> 'ComputerBuilder':
        pass

    @abstractmethod
    def build_motherboard(self) -> 'ComputerBuilder':
        pass

    @abstractmethod
    def build_power_supply(self) -> 'ComputerBuilder':
        pass

    @abstractmethod
    def build_case(self) -> 'ComputerBuilder':
        pass

    def get_result(self) -> Computer:
        return self.computer


# ============ 具体建造者 ============

class GamingComputerBuilder(ComputerBuilder):
    """游戏电脑建造者"""

    def build_cpu(self) -> 'ComputerBuilder':
        self.computer.cpu = "Intel Core i9-13900K"
        return self

    def build_memory(self) -> 'ComputerBuilder':
        self.computer.memory = "64GB DDR5-6000 RGB"
        return self

    def build_storage(self) -> 'ComputerBuilder':
        self.computer.storage = "2TB NVMe SSD Gen4"
        return self

    def build_gpu(self) -> 'ComputerBuilder':
        self.computer.gpu = "NVIDIA RTX 4090 24GB"
        return self

    def build_motherboard(self) -> 'ComputerBuilder':
        self.computer.motherboard = "ASUS ROG Maximus Z790"
        return self

    def build_power_supply(self) -> 'ComputerBuilder':
        self.computer.power_supply = "1000W 80 Plus Gold"
        return self

    def build_case(self) -> 'ComputerBuilder':
        self.computer.case = "Lian Li O11 Dynamic EVO"
        return self


class OfficeComputerBuilder(ComputerBuilder):
    """办公电脑建造者"""

    def build_cpu(self) -> 'ComputerBuilder':
        self.computer.cpu = "Intel Core i5-13400"
        return self

    def build_memory(self) -> 'ComputerBuilder':
        self.computer.memory = "16GB DDR4-3200"
        return self

    def build_storage(self) -> 'ComputerBuilder':
        self.computer.storage = "512GB SATA SSD"
        return self

    def build_gpu(self) -> 'ComputerBuilder':
        self.computer.gpu = "Integrated Graphics"
        return self

    def build_motherboard(self) -> 'ComputerBuilder':
        self.computer.motherboard = "ASUS Prime B760M"
        return self

    def build_power_supply(self) -> 'ComputerBuilder':
        self.computer.power_supply = "450W 80 Plus Bronze"
        return self

    def build_case(self) -> 'ComputerBuilder':
        self.computer.case = "Cooler Master MasterBox"
        return self


class BudgetComputerBuilder(ComputerBuilder):
    """经济型电脑建造者"""

    def build_cpu(self) -> 'ComputerBuilder':
        self.computer.cpu = "AMD Ryzen 5 5600G"
        return self

    def build_memory(self) -> 'ComputerBuilder':
        self.computer.memory = "8GB DDR4-2666"
        return self

    def build_storage(self) -> 'ComputerBuilder':
        self.computer.storage = "256GB NVMe SSD"
        return self

    def build_gpu(self) -> 'ComputerBuilder':
        self.computer.gpu = "Integrated Vega Graphics"
        return self

    def build_motherboard(self) -> 'ComputerBuilder':
        self.computer.motherboard = "MSI B550M PRO-VDH"
        return self

    def build_power_supply(self) -> 'ComputerBuilder':
        self.computer.power_supply = "350W Standard"
        return self

    def build_case(self) -> 'ComputerBuilder':
        self.computer.case = "Generic Micro ATX Case"
        return self


# ============ 指挥者 ============

class ComputerDirector:
    """电脑组装指挥者"""

    def __init__(self, builder: ComputerBuilder):
        self.builder = builder

    def construct(self) -> Computer:
        """按顺序构建电脑"""
        return (self.builder
                .build_case()
                .build_power_supply()
                .build_motherboard()
                .build_cpu()
                .build_memory()
                .build_gpu()
                .build_storage()
                .get_result())

    def construct_minimal(self) -> Computer:
        """构建最小配置"""
        return (self.builder
                .build_case()
                .build_motherboard()
                .build_cpu()
                .build_memory()
                .get_result())


# ============ 使用示例 ============

print("=== Gaming Computer ===")
gaming_builder = GamingComputerBuilder()
director = ComputerDirector(gaming_builder)
gaming_pc = director.construct()
print(gaming_pc)

print("\n=== Office Computer ===")
office_builder = OfficeComputerBuilder()
director = ComputerDirector(office_builder)
office_pc = director.construct()
print(office_pc)

print("\n=== Budget Computer (Minimal) ===")
budget_builder = BudgetComputerBuilder()
director = ComputerDirector(budget_builder)
budget_pc = director.construct_minimal()
print(budget_pc)
```

#### Pythonic变体：链式调用建造者

```python
class FluentComputerBuilder:
    """流畅接口风格的建造者"""

    def __init__(self):
        self.computer = Computer()

    def with_cpu(self, cpu: str) -> 'FluentComputerBuilder':
        self.computer.cpu = cpu
        return self

    def with_memory(self, memory: str) -> 'FluentComputerBuilder':
        self.computer.memory = memory
        return self

    def with_storage(self, storage: str) -> 'FluentComputerBuilder':
        self.computer.storage = storage
        return self

    def with_gpu(self, gpu: str) -> 'FluentComputerBuilder':
        self.computer.gpu = gpu
        return self

    def build(self) -> Computer:
        return self.computer


# 使用流畅接口
custom_pc = (FluentComputerBuilder()
    .with_cpu("AMD Ryzen 9 7950X")
    .with_memory("32GB DDR5-5600")
    .with_storage("1TB NVMe SSD")
    .with_gpu("AMD RX 7900 XTX")
    .build())

print("\n=== Custom Computer ===")
print(custom_pc)
```

#### 正例：HTTP请求构建器

```python
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class HTTPRequest:
    """HTTP请求"""
    method: str = "GET"
    url: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    timeout: int = 30
    retries: int = 3


class HTTPRequestBuilder:
    """HTTP请求建造者"""

    def __init__(self):
        self._request = HTTPRequest()

    def get(self, url: str) -> 'HTTPRequestBuilder':
        self._request.method = "GET"
        self._request.url = url
        return self

    def post(self, url: str) -> 'HTTPRequestBuilder':
        self._request.method = "POST"
        self._request.url = url
        return self

    def with_header(self, key: str, value: str) -> 'HTTPRequestBuilder':
        self._request.headers[key] = value
        return self

    def with_auth_token(self, token: str) -> 'HTTPRequestBuilder':
        self._request.headers["Authorization"] = f"Bearer {token}"
        return self

    def with_json_body(self, data: dict) -> 'HTTPRequestBuilder':
        import json
        self._request.headers["Content-Type"] = "application/json"
        self._request.body = json.dumps(data)
        return self

    def with_timeout(self, seconds: int) -> 'HTTPRequestBuilder':
        self._request.timeout = seconds
        return self

    def build(self) -> HTTPRequest:
        return self._request


# 使用
request = (HTTPRequestBuilder()
    .post("https://api.example.com/users")
    .with_auth_token("my-secret-token")
    .with_header("X-Request-ID", "12345")
    .with_json_body({"name": "John", "email": "john@example.com"})
    .with_timeout(10)
    .build())

print(f"\n{request.method} {request.url}")
print(f"Headers: {request.headers}")
print(f"Body: {request.body}")
```

#### 反例：巨型构造函数

```python
# ❌ 错误：使用巨型构造函数
class BadComputer:
    def __init__(self, cpu, memory, storage, gpu, motherboard,
                 power_supply, case, cooling, fans, rgb, wifi, bluetooth):
        self.cpu = cpu
        self.memory = memory
        # ... 更多参数

# 问题：
# 1. 参数过多，难以理解和使用
# 2. 参数顺序容易出错
# 3. 可选参数处理困难
# 4. 可读性差

# 创建时痛苦
pc = BadComputer("i9", "64GB", None, None, None, None, None, None, None, None, None, None)

# ✅ 正确：使用建造者模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 分步构建复杂对象 | 代码量增加 |
| 复用相同构建代码 | 需要创建多个类 |
| 隔离复杂构建逻辑 | 产品必须共有接口 |
| 精细控制构建过程 | 变化产品困难 |

---

### 1.5 原型模式（Prototype）

#### 意图

通过复制现有对象来创建新对象，而非新建实例。

#### 适用场景

- 对象创建成本高
- 需要避免与具体类耦合
- 需要保存和恢复对象状态
- 需要创建相似对象

#### UML结构图

```
┌─────────────────┐
│   Prototype     │
├─────────────────┤
│ + clone()       │
└─────────────────┘
         △
         │
┌────────┴────────┐
│ ConcretePrototype│
├─────────────────┤
│ + clone()       │
└─────────────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict
import json


# ============ 抽象原型 ============

class Prototype(ABC):
    """原型抽象类"""

    @abstractmethod
    def clone(self) -> 'Prototype':
        """创建对象的深拷贝"""
        pass

    @abstractmethod
    def shallow_clone(self) -> 'Prototype':
        """创建对象的浅拷贝"""
        pass


# ============ 具体原型 ============

class Document(Prototype):
    """文档原型"""

    def __init__(self, title: str = "", content: str = "",
                 author: str = "", metadata: Dict[str, Any] = None):
        self.title = title
        self.content = content
        self.author = author
        self.metadata = metadata or {}
        self.comments = []

    def clone(self) -> 'Document':
        """深拷贝 - 完全独立的副本"""
        new_doc = Document()
        new_doc.title = self.title
        new_doc.content = self.content
        new_doc.author = self.author
        new_doc.metadata = deepcopy(self.metadata)
        new_doc.comments = deepcopy(self.comments)
        return new_doc

    def shallow_clone(self) -> 'Document':
        """浅拷贝 - 共享可变对象"""
        import copy
        return copy.copy(self)

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def __str__(self):
        return f"Document(title='{self.title}', author='{self.author}', comments={len(self.comments)})"


class Shape(Prototype):
    """形状原型"""

    def __init__(self, x: int = 0, y: int = 0, color: str = "black"):
        self.x = x
        self.y = y
        self.color = color

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        return self

    def clone(self) -> 'Shape':
        return Shape(self.x, self.y, self.color)

    def shallow_clone(self) -> 'Shape':
        return self.clone()  # Shape没有可变对象，浅拷贝=深拷贝

    def __str__(self):
        return f"Shape(x={self.x}, y={self.y}, color='{self.color}')"


class Circle(Shape):
    """圆形原型"""

    def __init__(self, x: int = 0, y: int = 0, color: str = "black", radius: int = 1):
        super().__init__(x, y, color)
        self.radius = radius

    def clone(self) -> 'Circle':
        return Circle(self.x, self.y, self.color, self.radius)

    def __str__(self):
        return f"Circle(x={self.x}, y={self.y}, radius={self.radius}, color='{self.color}')"


class Rectangle(Shape):
    """矩形原型"""

    def __init__(self, x: int = 0, y: int = 0, color: str = "black",
                 width: int = 1, height: int = 1):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def clone(self) -> 'Rectangle':
        return Rectangle(self.x, self.y, self.color, self.width, self.height)

    def __str__(self):
        return f"Rectangle(x={self.x}, y={self.y}, w={self.width}, h={self.height})"


# ============ 原型注册表 ============

class PrototypeRegistry:
    """原型注册表 - 管理原型实例"""

    _prototypes: Dict[str, Prototype] = {}

    @classmethod
    def register(cls, name: str, prototype: Prototype):
        """注册原型"""
        cls._prototypes[name] = prototype

    @classmethod
    def create(cls, name: str) -> Prototype:
        """通过名称创建克隆"""
        if name not in cls._prototypes:
            raise ValueError(f"Unknown prototype: {name}")
        return cls._prototypes[name].clone()

    @classmethod
    def list_prototypes(cls) -> list:
        return list(cls._prototypes.keys())


# ============ 使用示例 ============

print("=== Document Prototype ===")
# 创建基础文档
template = Document(
    title="Project Report Template",
    content="# Project Report\n\n## Executive Summary\n\n## Details",
    author="Template System",
    metadata={"department": "Engineering", "confidentiality": "Internal"}
)

# 克隆并定制
doc1 = template.clone()
doc1.title = "Q1 Report"
doc1.author = "Alice"
doc1.add_comment("Draft version")

doc2 = template.clone()
doc2.title = "Q2 Report"
doc2.author = "Bob"
doc2.metadata["confidentiality"] = "Public"  # 不影响template

print(f"Template: {template}")
print(f"Doc1: {doc1}")
print(f"Doc2: {doc2}")
print(f"Template metadata: {template.metadata}")
print(f"Doc2 metadata: {doc2.metadata}")

print("\n=== Shape Prototype ===")
# 注册原型
PrototypeRegistry.register("small_circle", Circle(radius=5, color="red"))
PrototypeRegistry.register("large_circle", Circle(radius=50, color="blue"))
PrototypeRegistry.register("square", Rectangle(width=10, height=10, color="green"))

# 使用原型创建对象
shape1 = PrototypeRegistry.create("small_circle")
shape1.move(10, 20)
print(f"Shape1: {shape1}")

shape2 = PrototypeRegistry.create("small_circle")  # 新的独立实例
shape2.move(100, 200)
print(f"Shape2: {shape2}")

print(f"\nAvailable prototypes: {PrototypeRegistry.list_prototypes()}")

print("\n=== Deep vs Shallow Copy ===")
# 深拷贝 vs 浅拷贝对比
doc = Document(metadata={"tags": ["important"]})
doc.add_comment("Original comment")

shallow = doc.shallow_clone()
deep = doc.clone()

# 修改原文档
doc.metadata["tags"].append("urgent")
doc.add_comment("New comment")

print(f"Original comments: {doc.comments}")
print(f"Shallow comments: {shallow.comments}")  # 共享列表
print(f"Deep comments: {deep.comments}")  # 独立列表

print(f"Original metadata: {doc.metadata}")
print(f"Shallow metadata: {shallow.metadata}")  # 共享dict
print(f"Deep metadata: {deep.metadata}")  # 独立dict
```

#### 正例：Python的copy模块

```python
import copy

class GameCharacter:
    """游戏角色 - 使用Python copy模块"""

    def __init__(self, name: str, level: int, inventory: list = None):
        self.name = name
        self.level = level
        self.inventory = inventory or []
        self.stats = {"hp": 100, "mp": 50}

    def __copy__(self):
        """自定义浅拷贝"""
        new_obj = GameCharacter(self.name, self.level)
        new_obj.inventory = self.inventory  # 共享
        new_obj.stats = self.stats.copy()  # 复制
        return new_obj

    def __deepcopy__(self, memo):
        """自定义深拷贝"""
        new_obj = GameCharacter(
            copy.deepcopy(self.name, memo),
            copy.deepcopy(self.level, memo),
            copy.deepcopy(self.inventory, memo)
        )
        new_obj.stats = copy.deepcopy(self.stats, memo)
        return new_obj

    def __str__(self):
        return f"{self.name}(Lv.{self.level}, inventory={self.inventory})"


# 使用
hero = GameCharacter("Hero", 10, ["sword", "shield"])
hero.stats["hp"] = 150

# 浅拷贝
ally = copy.copy(hero)
ally.name = "Ally"

# 深拷贝
enemy = copy.deepcopy(hero)
enemy.name = "Enemy"
enemy.inventory.append("poison")  # 不影响hero

print(f"Hero: {hero}")
print(f"Ally: {ally}")
print(f"Enemy: {enemy}")
```

#### 反例：直接实例化

```python
# ❌ 错误：重复创建相似对象
class GameLevel:
    def create_enemies(self):
        enemies = []
        # 重复创建10个相似的敌人
        for i in range(10):
            enemy = Enemy()  # 每次都从头创建
            enemy.health = 100
            enemy.damage = 10
            enemy.ai = BasicAI()
            enemy.sprite = load_sprite("enemy.png")  # 昂贵的资源加载
            enemies.append(enemy)
        return enemies

# 问题：
# 1. 重复昂贵的初始化操作
# 2. 代码重复
# 3. 难以维护

# ✅ 正确：使用原型模式
class GameLevel:
    def __init__(self):
        self.enemy_prototype = Enemy()
        self.enemy_prototype.health = 100
        self.enemy_prototype.damage = 10
        self.enemy_prototype.ai = BasicAI()
        self.enemy_prototype.sprite = load_sprite("enemy.png")

    def create_enemies(self, count: int):
        return [self.enemy_prototype.clone() for _ in range(count)]
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 避免子类化 | 克隆复杂对象困难 |
| 运行时添加/删除产品 | 循环引用处理复杂 |
| 减少子类数量 | 需要实现clone方法 |
| 保存和恢复状态 | 深拷贝可能很慢 |

---

## 第二部分：结构型模式（7种）

结构型模式关注如何组合类和对象以形成更大的结构。

---

### 2.1 适配器模式（Adapter）

#### 意图

将一个类的接口转换成客户希望的另一个接口。

#### 适用场景

- 使用现有类但接口不兼容
- 需要复用不相关类
- 需要统一多个类的接口

#### UML结构图

```
┌─────────────┐         ┌─────────────┐
│   Client    │────────>│    Target   │
└─────────────┘         ├─────────────┤
                        │ + request() │
                        └─────────────┘
                                △
                                │
                        ┌───────┴───────┐
                        │    Adapter    │
                        ├───────────────┤
                        │ - adaptee     │
                        │ + request()   │
                        └───────────────┘
                                │
                        ┌───────┴───────┐
                        │    Adaptee    │
                        ├───────────────┤
                        │ + specific_req│
                        └───────────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod


# ============ 目标接口 ============

class MediaPlayer(ABC):
    """媒体播放器接口（目标接口）"""

    @abstractmethod
    def play(self, filename: str) -> None:
        pass


# ============ 被适配者 ============

class AdvancedMediaPlayer:
    """高级媒体播放器（被适配者）"""

    def play_vlc(self, filename: str) -> None:
        print(f"Playing vlc file: {filename}")

    def play_mp4(self, filename: str) -> None:
        print(f"Playing mp4 file: {filename}")


class OldAudioPlayer:
    """旧版音频播放器（被适配者）"""

    def play_audio(self, filepath: str, format_type: str) -> None:
        print(f"Playing {format_type} audio: {filepath}")


# ============ 适配器 ============

class MediaAdapter(MediaPlayer):
    """媒体适配器 - 对象适配器"""

    def __init__(self, adaptee):
        self.adaptee = adaptee

    def play(self, filename: str) -> None:
        if isinstance(self.adaptee, AdvancedMediaPlayer):
            if filename.endswith(".vlc"):
                self.adaptee.play_vlc(filename)
            elif filename.endswith(".mp4"):
                self.adaptee.play_mp4(filename)
        elif isinstance(self.adaptee, OldAudioPlayer):
            format_type = filename.split(".")[-1]
            self.adaptee.play_audio(filename, format_type)


# ============ 类适配器（使用多重继承） ============

class ClassAdapter(MediaPlayer, AdvancedMediaPlayer):
    """类适配器 - 使用多重继承"""

    def play(self, filename: str) -> None:
        if filename.endswith(".vlc"):
            self.play_vlc(filename)
        elif filename.endswith(".mp4"):
            self.play_mp4(filename)


# ============ 客户端 ============

class AudioPlayer(MediaPlayer):
    """音频播放器 - 客户端"""

    def __init__(self):
        self.adapters = {}

    def register_adapter(self, extension: str, adapter: MediaAdapter):
        """注册适配器"""
        self.adapters[extension] = adapter

    def play(self, filename: str) -> None:
        """播放文件"""
        extension = filename.split(".")[-1].lower()

        if extension in ["mp3", "wav", "aac"]:
            print(f"Playing native audio: {filename}")
        elif f".{extension}" in self.adapters:
            self.adapters[f".{extension}"].play(filename)
        else:
            print(f"Unsupported format: {extension}")


# ============ 使用示例 ============

print("=== Object Adapter ===")
player = AudioPlayer()

# 注册适配器
player.register_adapter(".vlc", MediaAdapter(AdvancedMediaPlayer()))
player.register_adapter(".mp4", MediaAdapter(AdvancedMediaPlayer()))
player.register_adapter(".ogg", MediaAdapter(OldAudioPlayer()))

# 播放各种格式
player.play("song.mp3")
player.play("movie.vlc")
player.play("clip.mp4")
player.play("music.ogg")
player.play("unknown.xyz")

print("\n=== Class Adapter ===")
class_adapter = ClassAdapter()
class_adapter.play("video.vlc")
class_adapter.play("film.mp4")
```

#### 正例：第三方库适配

```python
# 适配不同支付网关的接口

class PaymentGateway(ABC):
    """统一支付接口"""

    @abstractmethod
    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> dict:
        pass


# Stripe SDK（第三方库）
class StripeSDK:
    """Stripe支付SDK"""

    def create_charge(self, params: dict) -> dict:
        print(f"Stripe: Charging ${params['amount']} {params['currency']}")
        return {"id": "stripe_123", "status": "succeeded"}

    def create_refund(self, charge_id: str, amount: int) -> dict:
        print(f"Stripe: Refunding ${amount/100} for {charge_id}")
        return {"id": "refund_123", "status": "succeeded"}


# PayPal SDK（第三方库）
class PayPalSDK:
    """PayPal支付SDK"""

    def do_payment(self, total: str, currency_code: str, credit_card: dict) -> dict:
        print(f"PayPal: Charging {total} {currency_code}")
        return {"TRANSACTIONID": "paypal_123", "ACK": "Success"}

    def do_void(self, transaction_id: str, amount: str) -> dict:
        print(f"PayPal: Voiding {amount} for {transaction_id}")
        return {"ACK": "Success"}


# 适配器
class StripeAdapter(PaymentGateway):
    """Stripe适配器"""

    def __init__(self, api_key: str):
        self.stripe = StripeSDK()
        self.api_key = api_key

    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        # 转换参数格式
        params = {
            "amount": int(amount * 100),  # Stripe使用分
            "currency": currency.lower(),
            "source": card_token
        }
        result = self.stripe.create_charge(params)
        return {
            "transaction_id": result["id"],
            "status": result["status"],
            "gateway": "stripe"
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        result = self.stripe.create_refund(transaction_id, int(amount * 100))
        return {
            "refund_id": result["id"],
            "status": result["status"]
        }


class PayPalAdapter(PaymentGateway):
    """PayPal适配器"""

    def __init__(self, client_id: str, client_secret: str):
        self.paypal = PayPalSDK()
        self.client_id = client_id
        self.client_secret = client_secret

    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        result = self.paypal.do_payment(
            total=f"{amount:.2f}",
            currency_code=currency,
            credit_card={"token": card_token}
        )
        return {
            "transaction_id": result["TRANSACTIONID"],
            "status": "succeeded" if result["ACK"] == "Success" else "failed",
            "gateway": "paypal"
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        result = self.paypal.do_void(transaction_id, f"{amount:.2f}")
        return {
            "status": "succeeded" if result["ACK"] == "Success" else "failed"
        }


# 支付服务 - 完全解耦
class PaymentService:
    """支付服务 - 使用统一接口"""

    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def process_payment(self, amount: float, currency: str, card_token: str):
        return self.gateway.charge(amount, currency, card_token)

    def process_refund(self, transaction_id: str, amount: float):
        return self.gateway.refund(transaction_id, amount)


# 使用 - 可以轻松切换支付网关
stripe_service = PaymentService(StripeAdapter("sk_test_xxx"))
paypal_service = PaymentService(PayPalAdapter("client_id", "secret"))

print("\n=== Payment Adapters ===")
stripe_service.process_payment(99.99, "USD", "tok_visa")
paypal_service.process_payment(49.99, "EUR", "paypal_token")
```

#### 反例：直接依赖具体类

```python
# ❌ 错误：直接依赖具体类
class OrderService:
    def __init__(self):
        self.stripe = StripeSDK()  # 直接依赖

    def process_order(self, order):
        # 硬编码Stripe特定逻辑
        params = {
            "amount": int(order.total * 100),
            "currency": order.currency.lower(),
            "source": order.card_token
        }
        return self.stripe.create_charge(params)

# 问题：
# 1. 无法更换支付网关
# 2. 测试困难
# 3. 代码重复

# ✅ 正确：使用适配器模式解耦
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 解耦客户端与适配者 | 增加代码复杂度 |
| 复用现有类 | 可能需要多个适配器 |
| 符合开闭原则 | 过度使用导致混乱 |

---

### 2.2 桥接模式（Bridge）

#### 意图

将抽象部分与实现部分分离，使它们可以独立变化。

#### 适用场景

- 需要避免抽象和实现之间的永久绑定
- 抽象和实现都需要扩展
- 实现细节对客户隐藏

#### UML结构图

```
┌───────────────┐         ┌───────────────┐
│  Abstraction  │────────>│ Implementation│
├───────────────┤         ├───────────────┤
│ + operation() │         │ + operation() │
└───────────────┘         └───────────────┘
         △                          △
         │                          │
┌────────┴────────┐        ┌────────┴────────┐
│RefinedAbstraction│       │ConcreteImplA    │
└─────────────────┘        │ConcreteImplB    │
                           └─────────────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod


# ============ 实现部分 ============

class DrawingAPI(ABC):
    """绘图API接口（实现部分）"""

    @abstractmethod
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        pass

    @abstractmethod
    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        pass


class DrawingAPI1(DrawingAPI):
    """绘图API实现1"""

    def draw_circle(self, x: float, y: float, radius: float) -> None:
        print(f"API1.circle at ({x}, {y}) radius {radius}")

    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        print(f"API1.rectangle at ({x}, {y}) size {width}x{height}")


class DrawingAPI2(DrawingAPI):
    """绘图API实现2"""

    def draw_circle(self, x: float, y: float, radius: float) -> None:
        print(f"API2: Drawing circle @({x:.1f}, {y:.1f}) r={radius:.1f}")

    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        print(f"API2: Drawing rect @({x:.1f}, {y:.1f}) {width:.1f}x{height:.1f}")


class SVGDrawingAPI(DrawingAPI):
    """SVG绘图实现"""

    def __init__(self):
        self.elements = []

    def draw_circle(self, x: float, y: float, radius: float) -> None:
        self.elements.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" />'
        )

    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        self.elements.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" />'
        )

    def get_svg(self) -> str:
        return f'<svg>\n  ' + '\n  '.join(self.elements) + '\n</svg>'


# ============ 抽象部分 ============

class Shape(ABC):
    """形状抽象类（抽象部分）"""

    def __init__(self, drawing_api: DrawingAPI):
        self.drawing_api = drawing_api

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def resize(self, factor: float) -> None:
        pass


class CircleShape(Shape):
    """圆形 - 细化抽象"""

    def __init__(self, x: float, y: float, radius: float, drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self) -> None:
        self.drawing_api.draw_circle(self.x, self.y, self.radius)

    def resize(self, factor: float) -> None:
        self.radius *= factor


class RectangleShape(Shape):
    """矩形 - 细化抽象"""

    def __init__(self, x: float, y: float, width: float, height: float,
                 drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self) -> None:
        self.drawing_api.draw_rectangle(self.x, self.y, self.width, self.height)

    def resize(self, factor: float) -> None:
        self.width *= factor
        self.height *= factor


# ============ 使用示例 ============

print("=== Bridge Pattern ===")

# 使用API1绘制
circle1 = CircleShape(1, 2, 3, DrawingAPI1())
circle1.draw()
circle1.resize(2)
circle1.draw()

# 使用API2绘制相同的形状
circle2 = CircleShape(1, 2, 3, DrawingAPI2())
circle2.draw()

# 使用SVG绘制
svg_api = SVGDrawingAPI()
rect = RectangleShape(10, 20, 100, 50, svg_api)
rect.draw()
circle = CircleShape(50, 50, 30, svg_api)
circle.draw()
print("\nSVG Output:")
print(svg_api.get_svg())

# 动态切换实现
print("\n=== Dynamic Switching ===")
shapes = [
    CircleShape(1, 2, 3, DrawingAPI1()),
    CircleShape(5, 7, 11, DrawingAPI2()),
    RectangleShape(0, 0, 10, 20, DrawingAPI1()),
]

for shape in shapes:
    shape.draw()
```

#### 正例：消息发送系统

```python
# 抽象：消息类型
# 实现：发送渠道

class MessageSender(ABC):
    """消息发送器（实现）"""

    @abstractmethod
    def send(self, recipient: str, content: str) -> bool:
        pass


class EmailSender(MessageSender):
    def send(self, recipient: str, content: str) -> bool:
        print(f"[Email] To: {recipient}\nContent: {content[:50]}...")
        return True


class SMSSender(MessageSender):
    def send(self, recipient: str, content: str) -> bool:
        print(f"[SMS] To: {recipient}\nContent: {content[:100]}...")
        return True


class PushSender(MessageSender):
    def send(self, recipient: str, content: str) -> bool:
        print(f"[Push] To device: {recipient}\nContent: {content}")
        return True


class Message(ABC):
    """消息（抽象）"""

    def __init__(self, sender: MessageSender):
        self.sender = sender

    @abstractmethod
    def format_content(self, raw_content: str) -> str:
        pass

    def send(self, recipient: str, content: str) -> bool:
        formatted = self.format_content(content)
        return self.sender.send(recipient, formatted)


class TextMessage(Message):
    """纯文本消息"""

    def format_content(self, raw_content: str) -> str:
        return raw_content


class HTMLMessage(Message):
    """HTML消息"""

    def format_content(self, raw_content: str) -> str:
        return f"<html><body><p>{raw_content}</p></body></html>"


class EncryptedMessage(Message):
    """加密消息"""

    def format_content(self, raw_content: str) -> str:
        # 简单模拟加密
        return f"[ENCRYPTED]{raw_content[::-1]}[/ENCRYPTED]"


# 使用 - 可以独立组合
print("\n=== Message Bridge ===")

# 纯文本邮件
text_email = TextMessage(EmailSender())
text_email.send("user@example.com", "Hello, World!")

# HTML邮件
html_email = HTMLMessage(EmailSender())
html_email.send("user@example.com", "Hello, World!")

# 加密短信
encrypted_sms = EncryptedMessage(SMSSender())
encrypted_sms.send("+1234567890", "Secret message")

# 推送通知
push = TextMessage(PushSender())
push.send("device_token_123", "You have a new notification!")
```

#### 反例：类爆炸

```python
# ❌ 错误：继承导致类爆炸
class EmailTextMessage: pass
class EmailHTMLMessage: pass
class EmailEncryptedMessage: pass
class SMSTextMessage: pass
class SMSHTMLMessage: pass
# ... 2个维度 x 3个类型 = 6个类，且不断增加

# 问题：
# 1. 类数量爆炸
# 2. 代码重复
# 3. 难以维护

# ✅ 正确：使用桥接模式，2 + 3 = 5个类
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 分离抽象与实现 | 增加设计复杂度 |
| 独立扩展两个维度 | 需要识别两个维度 |
| 隐藏实现细节 | 对简单系统过度设计 |

---

### 2.3 组合模式（Composite）

#### 意图

将对象组合成树形结构以表示"部分-整体"的层次结构。

#### 适用场景

- 需要表示对象的部分-整体层次
- 希望客户端统一处理单个对象和组合对象
- 需要递归结构

#### UML结构图

```
┌─────────────────┐
│   Component     │
├─────────────────┤
│ + operation()   │
│ + add()         │
│ + remove()      │
│ + getChild()    │
└─────────────────┘
         △
    ┌────┴────┐
    │         │
┌───┴───┐ ┌───┴────┐
│ Leaf  │ │Composite│
└───────┘ ├─────────┤
          │ - children│
          │ + operation()│
          └─────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import List


# ============ 组件接口 ============

class FileSystemComponent(ABC):
    """文件系统组件接口"""

    def __init__(self, name: str):
        self.name = name
        self.parent = None

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        pass

    def get_path(self) -> str:
        """获取完整路径"""
        if self.parent is None:
            return self.name
        return f"{self.parent.get_path()}/{self.name}"


# ============ 叶节点 ============

class File(FileSystemComponent):
    """文件 - 叶节点"""

    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def get_size(self) -> int:
        return self._size

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}📄 {self.name} ({self._size} bytes)"


# ============ 组合节点 ============

class Directory(FileSystemComponent):
    """目录 - 组合节点"""

    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> 'Directory':
        """添加子组件"""
        component.parent = self
        self._children.append(component)
        return self

    def remove(self, component: FileSystemComponent) -> None:
        """移除子组件"""
        self._children.remove(component)
        component.parent = None

    def get_children(self) -> List[FileSystemComponent]:
        return self._children.copy()

    def get_size(self) -> int:
        """递归计算总大小"""
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}📁 {self.name}/ ({self.get_size()} bytes)"]
        for child in self._children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)

    def find(self, name: str) -> List[FileSystemComponent]:
        """递归查找"""
        results = []
        for child in self._children:
            if child.name == name:
                results.append(child)
            if isinstance(child, Directory):
                results.extend(child.find(name))
        return results


# ============ 使用示例 ============

print("=== Composite Pattern: File System ===")

# 创建文件系统结构
root = Directory("root")

# 添加文件和目录
documents = Directory("documents")
documents.add(File("resume.pdf", 1024))
documents.add(File("cover_letter.docx", 512))

projects = Directory("projects")
python_proj = Directory("python_app")
python_proj.add(File("main.py", 256))
python_proj.add(File("utils.py", 128))
python_proj.add(File("README.md", 64))

projects.add(python_proj)
projects.add(File("todo.txt", 32))

root.add(documents)
root.add(projects)
root.add(File("notes.txt", 128))

# 显示结构
print(root.display())

# 统一操作
print(f"\nTotal size: {root.get_size()} bytes")
print(f"Path to main.py: {python_proj.get_children()[0].get_path()}")

# 递归查找
found = root.find("README.md")
print(f"\nFound {len(found)} file(s) named 'README.md'")
for f in found:
    print(f"  - {f.get_path()}")
```

#### 正例：UI组件树

```python
class UIComponent(ABC):
    """UI组件接口"""

    def __init__(self, name: str):
        self.name = name
        self.visible = True
        self.parent = None

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def get_bounds(self) -> dict:
        pass


class UIWidget(UIComponent):
    """UI控件 - 叶节点"""

    def __init__(self, name: str, width: int, height: int):
        super().__init__(name)
        self.width = width
        self.height = height

    def render(self) -> str:
        if not self.visible:
            return ""
        return f"<{self.name} width={self.width} height={self.height}/>"

    def get_bounds(self) -> dict:
        return {"width": self.width, "height": self.height}


class UIContainer(UIComponent):
    """UI容器 - 组合节点"""

    def __init__(self, name: str, layout: str = "vertical"):
        super().__init__(name)
        self.layout = layout
        self.children: List[UIComponent] = []
        self.padding = 10
        self.spacing = 5

    def add(self, component: UIComponent) -> 'UIContainer':
        component.parent = self
        self.children.append(component)
        return self

    def remove(self, component: UIComponent) -> None:
        self.children.remove(component)
        component.parent = None

    def render(self) -> str:
        if not self.visible:
            return ""

        children_html = "\n".join(
            "  " + line
            for child in self.children
            for line in child.render().split("\n")
        )
        return f"<{self.name} layout='{self.layout}'>\n{children_html}\n</{self.name}>"

    def get_bounds(self) -> dict:
        """计算容器边界"""
        if not self.children:
            return {"width": 0, "height": 0}

        if self.layout == "vertical":
            width = max(c.get_bounds()["width"] for c in self.children)
            height = sum(c.get_bounds()["height"] for c in self.children)
            height += self.spacing * (len(self.children) - 1)
        else:  # horizontal
            width = sum(c.get_bounds()["width"] for c in self.children)
            width += self.spacing * (len(self.children) - 1)
            height = max(c.get_bounds()["height"] for c in self.children)

        return {
            "width": width + 2 * self.padding,
            "height": height + 2 * self.padding
        }

    def show_all(self) -> None:
        """显示所有子组件"""
        self.visible = True
        for child in self.children:
            if isinstance(child, UIContainer):
                child.show_all()
            else:
                child.visible = True

    def hide_all(self) -> None:
        """隐藏所有子组件"""
        self.visible = False
        for child in self.children:
            if isinstance(child, UIContainer):
                child.hide_all()
            else:
                child.visible = False


# 构建UI
print("\n=== Composite Pattern: UI Components ===")

form = UIContainer("form", layout="vertical")
form.add(UIWidget("label", 200, 20))
form.add(UIWidget("input", 200, 30))

button_row = UIContainer("div", layout="horizontal")
button_row.add(UIWidget("button", 80, 30))
button_row.add(UIWidget("button", 80, 30))

form.add(button_row)

print(form.render())
print(f"\nForm bounds: {form.get_bounds()}")
```

#### 反例：区别对待叶节点和组合

```python
# ❌ 错误：客户端需要区分叶节点和组合
class BadFileSystem:
    def calculate_total_size(self, items):
        total = 0
        for item in items:
            if isinstance(item, File):  # 特殊处理叶节点
                total += item.size
            elif isinstance(item, Directory):  # 特殊处理组合
                total += self.calculate_total_size(item.children)
        return total

# 问题：
# 1. 客户端代码复杂
# 2. 违反开闭原则
# 3. 类型检查脆弱

# ✅ 正确：使用组合模式统一接口
class GoodFileSystem:
    def calculate_total_size(self, root):
        return root.get_size()  # 统一调用，无需类型检查
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 统一处理单个和组合对象 | 设计更抽象 |
| 易于添加新组件类型 | 可能限制组件行为 |
| 简化客户端代码 | 类型检查困难 |

---

### 2.4 装饰器模式（Decorator）

#### 意图

动态地给对象添加额外职责，比子类更灵活。

#### 适用场景

- 需要在不修改类的情况下添加功能
- 需要动态添加/移除职责
- 功能组合导致类爆炸

#### UML结构图

```
┌───────────────┐         ┌───────────────┐
│   Component   │<────────│  Decorator    │
├───────────────┤         ├───────────────┤
│ + operation() │         │ - component   │
└───────────────┘         │ + operation() │
         △                └───────────────┘
         │                        △
    ┌────┴────┐            ┌──────┴──────┐
    │         │            │             │
┌───┴───┐ ┌───┴────┐  ┌────┴────┐  ┌────┴────┐
│Concrete ││Concrete│  │ConcreteA│  │ConcreteB│
│Component││Component│  │Decorator│  │Decorator│
└─────────┘└─────────┘  └─────────┘  └─────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod


# ============ 组件接口 ============

class Coffee(ABC):
    """咖啡接口"""

    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def ingredients(self) -> list:
        pass


# ============ 具体组件 ============

class SimpleCoffee(Coffee):
    """简单咖啡"""

    def cost(self) -> float:
        return 10.0

    def description(self) -> str:
        return "Simple coffee"

    def ingredients(self) -> list:
        return ["coffee", "water"]


# ============ 装饰器基类 ============

class CoffeeDecorator(Coffee):
    """咖啡装饰器基类"""

    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()

    def ingredients(self) -> list:
        return self._coffee.ingredients()


# ============ 具体装饰器 ============

class Milk(CoffeeDecorator):
    """牛奶装饰器"""

    def cost(self) -> float:
        return self._coffee.cost() + 2.0

    def description(self) -> str:
        return f"{self._coffee.description()}, milk"

    def ingredients(self) -> list:
        return self._coffee.ingredients() + ["milk"]


class Sugar(CoffeeDecorator):
    """糖装饰器"""

    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return f"{self._coffee.description()}, sugar"

    def ingredients(self) -> list:
        return self._coffee.ingredients() + ["sugar"]


class Whip(CoffeeDecorator):
    """奶泡装饰器"""

    def cost(self) -> float:
        return self._coffee.cost() + 3.0

    def description(self) -> str:
        return f"{self._coffee.description()}, whip"

    def ingredients(self) -> list:
        return self._coffee.ingredients() + ["whip"]


class Vanilla(CoffeeDecorator):
    """香草装饰器"""

    def cost(self) -> float:
        return self._coffee.cost() + 1.5

    def description(self) -> str:
        return f"{self._coffee.description()}, vanilla"

    def ingredients(self) -> list:
        return self._coffee.ingredients() + ["vanilla"]


# ============ 使用示例 ============

print("=== Decorator Pattern: Coffee Shop ===")

# 简单咖啡
coffee = SimpleCoffee()
print(f"{coffee.description()}: ${coffee.cost()}")

# 加牛奶
coffee_with_milk = Milk(SimpleCoffee())
print(f"{coffee_with_milk.description()}: ${coffee_with_milk.cost()}")

# 加牛奶和糖
coffee_with_milk_sugar = Sugar(Milk(SimpleCoffee()))
print(f"{coffee_with_milk_sugar.description()}: ${coffee_with_milk_sugar.cost()}")

# 复杂组合
fancy_coffee = Vanilla(Whip(Sugar(Milk(SimpleCoffee()))))
print(f"{fancy_coffee.description()}: ${fancy_coffee.cost()}")
print(f"Ingredients: {fancy_coffee.ingredients()}")

# 另一种组合方式
another_coffee = Milk(Sugar(Whip(SimpleCoffee())))
print(f"\n{another_coffee.description()}: ${another_coffee.cost()}")
```

#### Python装饰器 vs 装饰器模式

```python
# ============ Python函数装饰器 ============

def timing_decorator(func):
    """Python函数装饰器 - 语法糖"""
    import time
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


@timing_decorator
def slow_function():
    import time
    time.sleep(0.1)
    return "Done"


# ============ 类装饰器（更接近装饰器模式） ============

class TimingDecorator:
    """类装饰器 - 实现装饰器模式"""

    def __init__(self, component):
        self._component = component

    def __getattr__(self, name):
        """代理所有属性访问"""
        import time
        attr = getattr(self._component, name)

        if callable(attr):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = attr(*args, **kwargs)
                elapsed = time.time() - start
                print(f"{name} took {elapsed:.4f}s")
                return result
            return wrapper
        return attr


# 使用类装饰器
class DataProcessor:
    def process(self, data):
        import time
        time.sleep(0.05)
        return f"Processed: {data}"

    def save(self, data):
        print(f"Saved: {data}")


timed_processor = TimingDecorator(DataProcessor())
timed_processor.process("test data")


# ============ 对比总结 ============
print("\n=== Python Decorator vs Decorator Pattern ===")
print("""
Python装饰器（语法糖）:
- 用于函数/方法
- 编译时应用
- 语法: @decorator
- 用途: 日志、缓存、权限检查等

装饰器模式（设计模式）:
- 用于对象
- 运行时动态组合
- 通过构造函数包装
- 用途: 动态添加职责、避免子类爆炸
""")
```

#### 正例：IO流装饰

```python
# 模拟Java IO流的装饰器模式

class DataSource(ABC):
    """数据源接口"""

    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, data: str) -> None:
        pass


class FileDataSource(DataSource):
    """文件数据源"""

    def __init__(self, filename: str):
        self.filename = filename
        self._data = ""

    def read(self) -> str:
        print(f"Reading from {self.filename}")
        return self._data

    def write(self, data: str) -> None:
        print(f"Writing to {self.filename}")
        self._data = data


class DataSourceDecorator(DataSource):
    """数据源装饰器基类"""

    def __init__(self, source: DataSource):
        self._source = source

    def read(self) -> str:
        return self._source.read()

    def write(self, data: str) -> None:
        self._source.write(data)


class EncryptionDecorator(DataSourceDecorator):
    """加密装饰器"""

    def read(self) -> str:
        encrypted = self._source.read()
        return self._decrypt(encrypted)

    def write(self, data: str) -> None:
        encrypted = self._encrypt(data)
        self._source.write(encrypted)

    def _encrypt(self, data: str) -> str:
        # 简单模拟加密
        return f"[ENCRYPTED]{data[::-1]}"

    def _decrypt(self, data: str) -> str:
        if data.startswith("[ENCRYPTED]"):
            return data[11:][::-1]
        return data


class CompressionDecorator(DataSourceDecorator):
    """压缩装饰器"""

    def read(self) -> str:
        compressed = self._source.read()
        return self._decompress(compressed)

    def write(self, data: str) -> None:
        compressed = self._compress(data)
        self._source.write(compressed)

    def _compress(self, data: str) -> str:
        # 简单模拟压缩
        return f"[COMPRESSED:{len(data)}]{data[:10]}..."

    def _decompress(self, data: str) -> str:
        if data.startswith("[COMPRESSED:"):
            # 实际应该解压
            return "<decompressed data>"
        return data


class LoggingDecorator(DataSourceDecorator):
    """日志装饰器"""

    def read(self) -> str:
        print(f"[LOG] Reading from data source")
        result = self._source.read()
        print(f"[LOG] Read {len(result)} characters")
        return result

    def write(self, data: str) -> None:
        print(f"[LOG] Writing {len(data)} characters to data source")
        self._source.write(data)
        print(f"[LOG] Write completed")


# 使用 - 可以任意组合
print("\n=== IO Stream Decorators ===")

# 简单文件
datasource = FileDataSource("data.txt")
datasource.write("Hello, World!")
print(f"Read: {datasource.read()}\n")

# 加密+压缩+日志
datasource = LoggingDecorator(
    CompressionDecorator(
        EncryptionDecorator(
            FileDataSource("secure.dat")
        )
    )
)
datasource.write("Secret message")
print(f"Read: {datasource.read()}")
```

#### 反例：子类爆炸

```python
# ❌ 错误：使用继承导致类爆炸
class CoffeeWithMilk(SimpleCoffee):
    def cost(self): return super().cost() + 2.0

class CoffeeWithSugar(SimpleCoffee):
    def cost(self): return super().cost() + 0.5

class CoffeeWithMilkAndSugar(SimpleCoffee):
    def cost(self): return super().cost() + 2.5

class CoffeeWithWhip(SimpleCoffee):
    def cost(self): return super().cost() + 3.0

# 问题：
# 1. 类数量爆炸（2^n种组合）
# 2. 代码重复
# 3. 无法运行时组合

# ✅ 正确：使用装饰器模式动态组合
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 比继承更灵活 | 可能产生很多小对象 |
| 运行时添加职责 | 调试困难 |
| 符合单一职责 | 装饰顺序重要 |

---

### 2.5 外观模式（Facade）

#### 意图

为子系统中的一组接口提供一个统一的高层接口。

#### 适用场景

- 需要简化复杂子系统
- 需要分层系统
- 需要解耦客户端与子系统

#### UML结构图

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────┐
│   Facade    │
├─────────────┤
│ + operation()│
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│SubA │ │SubB │
└─────┘ └─────┘
```

#### Python实现

```python
# ============ 复杂子系统 ============

class CPU:
    """CPU子系统"""

    def freeze(self) -> None:
        print("CPU: Freezing processor")

    def jump(self, position: int) -> None:
        print(f"CPU: Jumping to position {position}")

    def execute(self) -> None:
        print("CPU: Executing instructions")


class Memory:
    """内存子系统"""

    def load(self, position: int, data: str) -> None:
        print(f"Memory: Loading '{data}' at position {position}")

    def read(self, position: int) -> str:
        print(f"Memory: Reading from position {position}")
        return "<data>"


class HardDrive:
    """硬盘子系统"""

    def read(self, lba: int, size: int) -> str:
        print(f"HardDrive: Reading {size} bytes from LBA {lba}")
        return "<boot sector>"

    def write(self, lba: int, data: str) -> None:
        print(f"HardDrive: Writing to LBA {lba}")


class GPU:
    """GPU子系统"""

    def initialize(self) -> None:
        print("GPU: Initializing graphics")

    def render(self) -> None:
        print("GPU: Rendering frame")


class NetworkInterface:
    """网络接口子系统"""

    def connect(self) -> None:
        print("Network: Connecting")

    def disconnect(self) -> None:
        print("Network: Disconnecting")


# ============ 外观类 ============

class ComputerFacade:
    """计算机外观 - 简化复杂子系统"""

    BOOT_ADDRESS = 0x0000
    BOOT_SECTOR = 0x0000
    SECTOR_SIZE = 512

    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
        self.gpu = GPU()
        self.network = NetworkInterface()

    def start(self) -> None:
        """启动计算机 - 简化复杂流程"""
        print("=== Starting Computer ===")
        self.cpu.freeze()
        boot_data = self.hard_drive.read(self.BOOT_SECTOR, self.SECTOR_SIZE)
        self.memory.load(self.BOOT_ADDRESS, boot_data)
        self.cpu.jump(self.BOOT_ADDRESS)
        self.cpu.execute()
        self.gpu.initialize()
        self.network.connect()
        print("=== Computer Started ===\n")

    def shutdown(self) -> None:
        """关闭计算机"""
        print("=== Shutting Down ===")
        self.network.disconnect()
        print("=== Computer Shut Down ===\n")

    def run_program(self, program: str) -> None:
        """运行程序"""
        print(f"=== Running {program} ===")
        self.gpu.render()
        print(f"=== {program} Completed ===\n")


# ============ 使用示例 ============

print("=== Facade Pattern: Computer ===")

# 使用外观 - 简单
computer = ComputerFacade()
computer.start()
computer.run_program("Application")
computer.shutdown()

# 不使用外观 - 复杂
print("=== Without Facade ===")
cpu = CPU()
memory = Memory()
hard_drive = HardDrive()
gpu = GPU()
network = NetworkInterface()

cpu.freeze()
boot_data = hard_drive.read(0x0000, 512)
memory.load(0x0000, boot_data)
cpu.jump(0x0000)
cpu.execute()
gpu.initialize()
network.connect()
```

#### 正例：API网关

```python
# 外观模式在微服务中的应用

class UserService:
    def get_user(self, user_id: str) -> dict:
        return {"id": user_id, "name": "John", "email": "john@example.com"}

class OrderService:
    def get_orders(self, user_id: str) -> list:
        return [{"id": "1", "total": 100}, {"id": "2", "total": 200}]

class InventoryService:
    def check_stock(self, product_id: str) -> int:
        return 10

class PaymentService:
    def process_payment(self, order_id: str, amount: float) -> bool:
        return True

class NotificationService:
    def send_notification(self, user_id: str, message: str) -> None:
        print(f"Notification to {user_id}: {message}")


class OrderFacade:
    """订单外观 - 协调多个服务"""

    def __init__(self):
        self.user_service = UserService()
        self.order_service = OrderService()
        self.inventory_service = InventoryService()
        self.payment_service = PaymentService()
        self.notification_service = NotificationService()

    def place_order(self, user_id: str, items: list) -> dict:
        """下单 - 协调多个服务"""
        # 1. 获取用户信息
        user = self.user_service.get_user(user_id)

        # 2. 检查库存
        for item in items:
            stock = self.inventory_service.check_stock(item["product_id"])
            if stock < item["quantity"]:
                raise ValueError(f"Insufficient stock for {item['product_id']}")

        # 3. 计算总价
        total = sum(item["price"] * item["quantity"] for item in items)

        # 4. 处理支付
        order_id = "order_123"
        if not self.payment_service.process_payment(order_id, total):
            raise ValueError("Payment failed")

        # 5. 发送通知
        self.notification_service.send_notification(
            user_id,
            f"Order {order_id} placed successfully!"
        )

        return {
            "order_id": order_id,
            "user": user,
            "items": items,
            "total": total,
            "status": "confirmed"
        }

    def get_user_dashboard(self, user_id: str) -> dict:
        """获取用户仪表盘数据"""
        user = self.user_service.get_user(user_id)
        orders = self.order_service.get_orders(user_id)

        return {
            "user": user,
            "orders": orders,
            "order_count": len(orders),
            "total_spent": sum(o["total"] for o in orders)
        }


# 使用
print("\n=== Order Facade ===")
facade = OrderFacade()

result = facade.place_order("user_123", [
    {"product_id": "p1", "quantity": 2, "price": 50},
    {"product_id": "p2", "quantity": 1, "price": 100}
])
print(f"Order placed: {result['order_id']}")

dashboard = facade.get_user_dashboard("user_123")
print(f"Dashboard: {dashboard}")
```

#### 反例：外观过于庞大

```python
# ❌ 错误：外观类过于庞大
class BadFacade:
    def method1(self): pass
    def method2(self): pass
    # ... 100+ 方法
    def method100(self): pass

# 问题：
# 1. 违反单一职责原则
# 2. 成为上帝对象
# 3. 难以维护

# ✅ 正确：按功能拆分外观
class OrderFacade: pass
class UserFacade: pass
class InventoryFacade: pass
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 简化接口 | 可能成为上帝对象 |
| 解耦子系统 | 限制低级功能访问 |
| 分层架构 | 需要额外维护 |

---

### 2.6 享元模式（Flyweight）

#### 意图

运用共享技术有效地支持大量细粒度对象。

#### 适用场景

- 需要大量相似对象
- 对象状态可分离为内部和外部
- 内存是瓶颈

#### UML结构图

```
┌─────────────┐         ┌─────────────┐
│   Client    │────────>│  Flyweight  │
└─────────────┘         ├─────────────┤
                        │ + operation │
                        │   (extrinsic)│
                        └─────────────┘
                                △
                        ┌───────┴───────┐
                        │               │
                   ┌────┴────┐     ┌────┴────┐
                   │Concrete │     │Concrete │
                   │Flyweight│     │Flyweight│
                   │(intrinsic)    │(intrinsic)│
                   └─────────┘     └─────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import Dict, Tuple


# ============ 享元接口 ============

class TreeType(ABC):
    """树木类型 - 享元"""

    def __init__(self, name: str, color: str, texture: str):
        self.name = name      # 内部状态
        self.color = color    # 内部状态
        self.texture = texture  # 内部状态

    @abstractmethod
    def draw(self, x: int, y: int, size: int) -> None:
        """绘制 - 使用外部状态"""
        pass

    def __str__(self):
        return f"TreeType({self.name}, {self.color})"


# ============ 具体享元 ============

class ConcreteTreeType(TreeType):
    """具体树木类型"""

    def draw(self, x: int, y: int, size: int) -> None:
        """绘制树木 - 外部状态作为参数"""
        print(f"Drawing {self.name} tree at ({x}, {y}) size={size}")
        print(f"  Color: {self.color}, Texture: {self.texture}")


# ============ 享元工厂 ============

class TreeFactory:
    """树木工厂 - 管理享元对象"""

    _tree_types: Dict[Tuple[str, str, str], TreeType] = {}
    _instance_count = 0

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        """获取或创建享元"""
        key = (name, color, texture)

        if key not in cls._tree_types:
            print(f"  [Factory] Creating new tree type: {key}")
            cls._tree_types[key] = ConcreteTreeType(name, color, texture)
            cls._instance_count += 1
        else:
            print(f"  [Factory] Reusing existing tree type: {key}")

        return cls._tree_types[key]

    @classmethod
    def get_instance_count(cls) -> int:
        return cls._instance_count

    @classmethod
    def list_types(cls) -> list:
        return list(cls._tree_types.keys())


# ============ 上下文 ============

class Tree:
    """树木 - 包含外部状态"""

    def __init__(self, x: int, y: int, size: int, tree_type: TreeType):
        self.x = x              # 外部状态
        self.y = y              # 外部状态
        self.size = size        # 外部状态
        self.tree_type = tree_type  # 享元引用

    def draw(self) -> None:
        """绘制树木"""
        self.tree_type.draw(self.x, self.y, self.size)


# ============ 森林管理器 ============

class Forest:
    """森林 - 管理大量树木"""

    def __init__(self):
        self.trees: list = []

    def plant_tree(self, x: int, y: int, size: int,
                   name: str, color: str, texture: str) -> None:
        """种植树木"""
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, size, tree_type)
        self.trees.append(tree)

    def draw(self) -> None:
        """绘制整个森林"""
        for tree in self.trees:
            tree.draw()

    def get_tree_count(self) -> int:
        return len(self.trees)


# ============ 使用示例 ============

print("=== Flyweight Pattern: Forest ===")

forest = Forest()

# 种植大量树木 - 但只有几种类型
print("\n--- Planting trees ---")
tree_types = [
    ("Oak", "Green", "Rough"),
    ("Pine", "Dark Green", "Smooth"),
    ("Birch", "White", "Smooth"),
    ("Maple", "Red", "Rough"),
]

import random
random.seed(42)

for i in range(20):  # 种植20棵树
    tree_type = random.choice(tree_types)
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    size = random.randint(5, 20)
    forest.plant_tree(x, y, size, *tree_type)

print(f"\n--- Statistics ---")
print(f"Total trees planted: {forest.get_tree_count()}")
print(f"Unique tree types created: {TreeFactory.get_instance_count()}")
print(f"Memory saved: {forest.get_tree_count() - TreeFactory.get_instance_count()} objects")

print(f"\n--- Tree Types ---")
for tree_type in TreeFactory.list_types():
    print(f"  {tree_type}")
```

#### 正例：字符渲染

```python
class CharacterStyle:
    """字符样式 - 享元"""

    def __init__(self, font: str, size: int, color: str, bold: bool = False):
        self.font = font
        self.size = size
        self.color = color
        self.bold = bold

    def __eq__(self, other):
        return (self.font == other.font and
                self.size == other.size and
                self.color == other.color and
                self.bold == other.bold)

    def __hash__(self):
        return hash((self.font, self.size, self.color, self.bold))

    def __str__(self):
        return f"Style({self.font}, {self.size}pt, {self.color})"


class StyleFactory:
    """样式工厂"""

    _styles: Dict[CharacterStyle, CharacterStyle] = {}

    @classmethod
    def get_style(cls, font: str, size: int, color: str, bold: bool = False) -> CharacterStyle:
        style = CharacterStyle(font, size, color, bold)
        if style not in cls._styles:
            cls._styles[style] = style
            print(f"  [StyleFactory] Created: {style}")
        return cls._styles[style]

    @classmethod
    def get_style_count(cls) -> int:
        return len(cls._styles)


class Character:
    """字符 - 包含外部状态"""

    def __init__(self, char: str, x: int, y: int, style: CharacterStyle):
        self.char = char
        self.x = x
        self.y = y
        self.style = style

    def render(self):
        weight = "bold" if self.style.bold else "normal"
        print(f"  '{self.char}' at ({self.x}, {self.y}) - {self.style} [{weight}]")


class TextDocument:
    """文本文档"""

    def __init__(self):
        self.characters: list = []

    def add_text(self, text: str, x: int, y: int,
                 font: str, size: int, color: str, bold: bool = False):
        style = StyleFactory.get_style(font, size, color, bold)
        for i, char in enumerate(text):
            self.characters.append(Character(char, x + i * size, y, style))

    def render(self):
        print("Rendering document:")
        for char in self.characters:
            char.render()


# 使用
print("\n=== Flyweight Pattern: Text Rendering ===")
doc = TextDocument()

# 添加文本 - 相同样式共享
doc.add_text("Hello", 0, 0, "Arial", 12, "black")
doc.add_text("World", 60, 0, "Arial", 12, "black")  # 复用样式
doc.add_text("Bold", 0, 20, "Arial", 12, "black", bold=True)
doc.add_text("Title", 0, 40, "Times", 24, "blue")
doc.add_text("Normal", 0, 70, "Arial", 12, "black")  # 复用样式

doc.render()

print(f"\nTotal characters: {len(doc.characters)}")
print(f"Unique styles: {StyleFactory.get_style_count()}")
```

#### 反例：过度优化

```python
# ❌ 错误：对少量对象使用享元
class BadFlyweight:
    pass

# 只有几个对象时使用享元，增加复杂度而没有收益

# ✅ 正确：在大量相似对象时使用
# 通常 > 1000 个对象且有大量重复状态时才考虑
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 大量节省内存 | 代码复杂度增加 |
| 提高性能 | 需要分离状态 |
| 集中管理共享对象 | CPU时间换内存 |

---

### 2.7 代理模式（Proxy）

#### 意图

为其他对象提供一种代理以控制对这个对象的访问。

#### 适用场景

- 延迟加载（虚拟代理）
- 访问控制（保护代理）
- 远程访问（远程代理）
- 记录日志（日志代理）

#### UML结构图

```
┌─────────────┐         ┌─────────────┐
│   Client    │────────>│   Subject   │
└─────────────┘         ├─────────────┤
                        │ + request() │
                        └─────────────┘
                                △
                         ┌──────┴──────┐
                         │             │
                    ┌────┴────┐   ┌────┴────┐
                    │  Real   │   │  Proxy  │
                    │ Subject │   ├─────────┤
                    └─────────┘   │- real   │
                                  │+ request│
                                  └─────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import Optional
import time


# ============ 主题接口 ============

class Image(ABC):
    """图像接口"""

    @abstractmethod
    def display(self) -> None:
        pass

    @abstractmethod
    def get_size(self) -> tuple:
        pass


# ============ 真实主题 ============

class RealImage(Image):
    """真实图像 - 加载成本高"""

    def __init__(self, filename: str):
        self.filename = filename
        self._width = 0
        self._height = 0
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """从磁盘加载 - 昂贵操作"""
        print(f"Loading image from disk: {self.filename}")
        time.sleep(1)  # 模拟加载时间
        self._width = 1920
        self._height = 1080

    def display(self) -> None:
        print(f"Displaying: {self.filename} ({self._width}x{self._height})")

    def get_size(self) -> tuple:
        return (self._width, self._height)


# ============ 代理 ============

class ProxyImage(Image):
    """图像代理 - 虚拟代理"""

    def __init__(self, filename: str):
        self.filename = filename
        self._real_image: Optional[RealImage] = None

    def display(self) -> None:
        """延迟加载真实图像"""
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()

    def get_size(self) -> tuple:
        """获取尺寸 - 可能不需要加载完整图像"""
        if self._real_image is None:
            # 可以从元数据读取，无需加载完整图像
            print(f"Reading metadata for: {self.filename}")
            return (1920, 1080)  # 模拟从元数据读取
        return self._real_image.get_size()


class CachingProxyImage(Image):
    """缓存代理 - 缓存结果"""

    _cache: dict = {}

    def __init__(self, filename: str):
        self.filename = filename

    def display(self) -> None:
        if self.filename not in self._cache:
            self._cache[self.filename] = RealImage(self.filename)
        self._cache[self.filename].display()

    def get_size(self) -> tuple:
        if self.filename not in self._cache:
            self._cache[self.filename] = RealImage(self.filename)
        return self._cache[self.filename].get_size()


# ============ 保护代理 ============

class ProtectedImage(Image):
    """保护代理 - 访问控制"""

    def __init__(self, filename: str, user_role: str):
        self.filename = filename
        self.user_role = user_role
        self._real_image: Optional[RealImage] = None

    def _check_access(self) -> bool:
        """检查访问权限"""
        return self.user_role in ["admin", "premium"]

    def display(self) -> None:
        if not self._check_access():
            print(f"Access denied: {self.user_role} cannot view {self.filename}")
            return

        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()

    def get_size(self) -> tuple:
        if not self._check_access():
            return (0, 0)

        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        return self._real_image.get_size()


# ============ 日志代理 ============

class LoggingProxyImage(Image):
    """日志代理 - 记录操作"""

    def __init__(self, filename: str):
        self.filename = filename
        self._real_image: Optional[RealImage] = None
        self.access_count = 0

    def display(self) -> None:
        self.access_count += 1
        print(f"[LOG] Access #{self.access_count}: display({self.filename})")

        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()

    def get_size(self) -> tuple:
        self.access_count += 1
        print(f"[LOG] Access #{self.access_count}: get_size({self.filename})")

        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        return self._real_image.get_size()


# ============ 使用示例 ============

print("=== Proxy Pattern ===")

print("\n--- Virtual Proxy (Lazy Loading) ---")
# 虚拟代理 - 延迟加载
images = [ProxyImage(f"photo_{i}.jpg") for i in range(3)]
print("Images created (not loaded yet)")

# 只有显示时才加载
images[0].display()
images[0].display()  # 第二次不重新加载

print("\n--- Caching Proxy ---")
# 缓存代理
cached = CachingProxyImage("cached_photo.jpg")
cached.display()  # 加载
cached.display()  # 从缓存读取

print("\n--- Protection Proxy ---")
# 保护代理
admin_image = ProtectedImage("premium.jpg", "admin")
guest_image = ProtectedImage("premium.jpg", "guest")
admin_image.display()
guest_image.display()

print("\n--- Logging Proxy ---")
# 日志代理
logged = LoggingProxyImage("logged.jpg")
logged.display()
logged.get_size()
print(f"Total accesses: {logged.access_count}")
```

#### 正例：数据库连接池

```python
from contextlib import contextmanager
import threading


class DatabaseConnection:
    """数据库连接 - 昂贵资源"""

    _id_counter = 0
    _lock = threading.Lock()

    def __init__(self):
        with self._lock:
            DatabaseConnection._id_counter += 1
            self.id = DatabaseConnection._id_counter
        print(f"  [DB] Creating connection #{self.id}")
        self.in_use = False

    def execute(self, query: str):
        print(f"  [DB] Connection #{self.id} executing: {query}")
        return f"Result of: {query}"

    def close(self):
        print(f"  [DB] Connection #{self.id} closed")


class ConnectionPool:
    """连接池 - 代理模式"""

    def __init__(self, max_connections: int = 5):
        self.max_connections = max_connections
        self._available: list = []
        self._in_use: list = []
        self._lock = threading.Lock()

        # 预创建连接
        for _ in range(max_connections):
            self._available.append(DatabaseConnection())

    def acquire(self) -> DatabaseConnection:
        """获取连接"""
        with self._lock:
            if not self._available:
                raise Exception("No connections available")

            conn = self._available.pop()
            conn.in_use = True
            self._in_use.append(conn)
            print(f"[Pool] Acquired connection #{conn.id} "
                  f"(available: {len(self._available)}, in use: {len(self._in_use)})")
            return conn

    def release(self, conn: DatabaseConnection):
        """释放连接"""
        with self._lock:
            conn.in_use = False
            self._in_use.remove(conn)
            self._available.append(conn)
            print(f"[Pool] Released connection #{conn.id} "
                  f"(available: {len(self._available)}, in use: {len(self._in_use)})")

    @contextmanager
    def get_connection(self):
        """上下文管理器获取连接"""
        conn = self.acquire()
        try:
            yield conn
        finally:
            self.release(conn)

    def get_stats(self):
        return {
            "available": len(self._available),
            "in_use": len(self._in_use),
            "total": self.max_connections
        }


# 使用
print("\n=== Connection Pool Proxy ===")
pool = ConnectionPool(max_connections=3)

# 使用上下文管理器
with pool.get_connection() as conn1:
    conn1.execute("SELECT * FROM users")

    with pool.get_connection() as conn2:
        conn2.execute("SELECT * FROM orders")

        with pool.get_connection() as conn3:
            conn3.execute("SELECT * FROM products")

print(f"\nPool stats: {pool.get_stats()}")
```

#### 反例：过度代理

```python
# ❌ 错误：不必要的代理
class SimpleProxy:
    def __init__(self, real_object):
        self.real = real_object

    def method(self):
        return self.real.method()  # 纯转发，无附加功能

# 问题：
# 1. 增加复杂度
# 2. 性能开销
# 3. 无实际价值

# ✅ 正确：代理应提供附加功能
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 控制访问 | 增加响应时间 |
| 延迟加载 | 代码复杂度增加 |
| 附加功能透明 | 可能隐藏问题 |

---

## 第三部分：行为型模式（11种）

行为型模式关注对象之间的通信和职责分配。

---

### 3.1 责任链模式（Chain of Responsibility）

#### 意图

使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系。

#### 适用场景

- 多个对象可以处理同一请求
- 需要动态指定处理者
- 希望在不明确指定接收者的情况下提交请求

#### UML结构图

```
┌─────────────┐
│   Handler   │
├─────────────┤
│ - successor │
│ + handle()  │
│ + set_next()│
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
┌─┴─┐    ┌──┴──┐
│A  │    │  B  │
└───┘    └─────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from enum import Enum


# ============ 请求类 ============

class RequestType(Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    SALES = "sales"
    GENERAL = "general"


@dataclass
class SupportRequest:
    """支持请求"""
    type: RequestType
    description: str
    priority: int  # 1-5, 5为最高


# ============ 处理者接口 ============

class SupportHandler(ABC):
    """支持处理者"""

    def __init__(self):
        self._next_handler: Optional[SupportHandler] = None

    def set_next(self, handler: 'SupportHandler') -> 'SupportHandler':
        """设置下一个处理者"""
        self._next_handler = handler
        return handler  # 支持链式调用

    @abstractmethod
    def can_handle(self, request: SupportRequest) -> bool:
        pass

    @abstractmethod
    def handle_request(self, request: SupportRequest) -> str:
        pass

    def handle(self, request: SupportRequest) -> str:
        """处理请求或传递给下一个"""
        if self.can_handle(request):
            return self.handle_request(request)
        elif self._next_handler:
            return self._next_handler.handle(request)
        else:
            return f"No handler available for {request.type.value} request"


# ============ 具体处理者 ============

class TechnicalSupportHandler(SupportHandler):
    """技术支持处理者"""

    def can_handle(self, request: SupportRequest) -> bool:
        return request.type == RequestType.TECHNICAL and request.priority <= 3

    def handle_request(self, request: SupportRequest) -> str:
        return f"[Technical Support] Handling: {request.description}"


class SeniorTechnicalHandler(SupportHandler):
    """高级技术支持"""

    def can_handle(self, request: SupportRequest) -> bool:
        return request.type == RequestType.TECHNICAL and request.priority > 3

    def handle_request(self, request: SupportRequest) -> str:
        return f"[Senior Technical] Handling high priority: {request.description}"


class BillingSupportHandler(SupportHandler):
    """账单支持处理者"""

    def can_handle(self, request: SupportRequest) -> bool:
        return request.type == RequestType.BILLING

    def handle_request(self, request: SupportRequest) -> str:
        return f"[Billing Support] Processing: {request.description}"


class SalesSupportHandler(SupportHandler):
    """销售支持处理者"""

    def can_handle(self, request: SupportRequest) -> bool:
        return request.type == RequestType.SALES

    def handle_request(self, request: SupportRequest) -> str:
        return f"[Sales Support] Assisting with: {request.description}"


class GeneralSupportHandler(SupportHandler):
    """通用支持处理者（默认）"""

    def can_handle(self, request: SupportRequest) -> bool:
        return True  # 处理所有未被处理的请求

    def handle_request(self, request: SupportRequest) -> str:
        return f"[General Support] Redirecting: {request.description}"


# ============ 使用示例 ============

print("=== Chain of Responsibility Pattern ===")

# 构建责任链
chain = TechnicalSupportHandler()
chain.set_next(SeniorTechnicalHandler()) \
     .set_next(BillingSupportHandler()) \
     .set_next(SalesSupportHandler()) \
     .set_next(GeneralSupportHandler())

# 测试各种请求
requests = [
    SupportRequest(RequestType.TECHNICAL, "Can't login", 2),
    SupportRequest(RequestType.TECHNICAL, "Server crashed", 5),
    SupportRequest(RequestType.BILLING, "Refund request", 3),
    SupportRequest(RequestType.SALES, "Product inquiry", 2),
    SupportRequest(RequestType.GENERAL, "Feedback", 1),
]

for req in requests:
    result = chain.handle(req)
    print(f"Request: {req.type.value} (P{req.priority})")
    print(f"Result: {result}\n")
```

#### 正例：中间件链

```python
from typing import Callable, Any


class Middleware:
    """中间件基类"""

    def __init__(self):
        self._next: Optional[Callable] = None

    def set_next(self, next_handler: Callable) -> 'Middleware':
        self._next = next_handler
        return self

    def handle(self, request: dict) -> Any:
        if self._next:
            return self._next(request)
        return request


class AuthenticationMiddleware(Middleware):
    """认证中间件"""

    def handle(self, request: dict) -> Any:
        print("[Auth] Checking authentication...")
        if not request.get("token"):
            raise Exception("Unauthorized")
        print("[Auth] Authentication passed")
        return super().handle(request)


class LoggingMiddleware(Middleware):
    """日志中间件"""

    def handle(self, request: dict) -> Any:
        print(f"[Log] Request: {request.get('path')}")
        result = super().handle(request)
        print(f"[Log] Response: {result}")
        return result


class RateLimitMiddleware(Middleware):
    """限流中间件"""

    _requests = {}

    def handle(self, request: dict) -> Any:
        client_ip = request.get("ip", "unknown")
        count = self._requests.get(client_ip, 0)

        if count > 100:
            raise Exception("Rate limit exceeded")

        self._requests[client_ip] = count + 1
        print(f"[RateLimit] Request count for {client_ip}: {count + 1}")
        return super().handle(request)


class ValidationMiddleware(Middleware):
    """验证中间件"""

    def handle(self, request: dict) -> Any:
        print("[Validation] Validating request...")
        if request.get("method") == "POST" and not request.get("body"):
            raise Exception("Invalid request body")
        return super().handle(request)


def final_handler(request: dict) -> dict:
    """最终处理函数"""
    return {"status": 200, "data": "Success"}


# 构建中间件链
print("\n=== Middleware Chain ===")
handler = AuthenticationMiddleware()
handler.set_next(LoggingMiddleware()) \
       .set_next(RateLimitMiddleware()) \
       .set_next(ValidationMiddleware()) \
       .set_next(final_handler)

# 测试请求
try:
    request = {
        "path": "/api/users",
        "method": "POST",
        "token": "valid_token",
        "ip": "192.168.1.1",
        "body": {"name": "John"}
    }
    result = handler.handle(request)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
```

#### 反例：硬编码条件判断

```python
# ❌ 错误：硬编码条件判断
def handle_request(request):
    if request.type == "technical":
        if request.priority <= 3:
            return technical_handler.handle(request)
        else:
            return senior_handler.handle(request)
    elif request.type == "billing":
        return billing_handler.handle(request)
    # ... 更多条件

# 问题：
# 1. 违反开闭原则
# 2. 难以扩展
# 3. 条件复杂时难以维护

# ✅ 正确：使用责任链模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 解耦发送者和接收者 | 请求可能未被处理 |
| 动态指定处理者 | 调试困难 |
| 符合单一职责 | 可能影响性能 |

---

### 3.2 命令模式（Command）

#### 意图

将请求封装为对象，从而可以用不同的请求、队列或日志来参数化其他对象。

#### 适用场景

- 需要参数化对象
- 需要队列或日志请求
- 需要支持撤销操作

#### UML结构图

```
┌─────────────┐         ┌─────────────┐
│   Invoker   │────────>│   Command   │
├─────────────┤         ├─────────────┤
│ + set_cmd() │         │ + execute() │
│ + invoke()  │         │ + undo()    │
└─────────────┘         └──────┬──────┘
                               │
                          ┌────┴────┐
                          │         │
                     ┌────┴────┐ ┌──┴─────┐
                     │Concrete │ │Concrete│
                     │CommandA │ │CommandB│
                     └────┬────┘ └────┬───┘
                          │           │
                     ┌────┴───────────┴───┐
                     │      Receiver      │
                     └────────────────────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
from datetime import datetime


# ============ 接收者 ============

class TextEditor:
    """文本编辑器 - 接收者"""

    def __init__(self):
        self.content = ""
        self.clipboard = ""
        self.selection = ""

    def insert(self, text: str, position: int = None) -> None:
        """插入文本"""
        if position is None:
            position = len(self.content)
        self.content = self.content[:position] + text + self.content[position:]

    def delete(self, start: int, length: int) -> str:
        """删除文本"""
        deleted = self.content[start:start + length]
        self.content = self.content[:start] + self.content[start + length:]
        return deleted

    def select(self, start: int, length: int) -> str:
        """选择文本"""
        self.selection = self.content[start:start + length]
        return self.selection

    def copy(self) -> None:
        """复制"""
        self.clipboard = self.selection

    def paste(self, position: int = None) -> None:
        """粘贴"""
        self.insert(self.clipboard, position)

    def get_content(self) -> str:
        return self.content


# ============ 命令接口 ============

class Command(ABC):
    """命令接口"""

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    def get_name(self) -> str:
        return self.__class__.__name__


# ============ 具体命令 ============

class InsertCommand(Command):
    """插入命令"""

    def __init__(self, editor: TextEditor, text: str, position: int = None):
        self.editor = editor
        self.text = text
        self.position = position
        self._executed_position = None

    def execute(self) -> None:
        self._executed_position = self.position or len(self.editor.content)
        self.editor.insert(self.text, self._executed_position)
        print(f"Inserted '{self.text}' at position {self._executed_position}")

    def undo(self) -> None:
        self.editor.delete(self._executed_position, len(self.text))
        print(f"Undone insert of '{self.text}'")


class DeleteCommand(Command):
    """删除命令"""

    def __init__(self, editor: TextEditor, start: int, length: int):
        self.editor = editor
        self.start = start
        self.length = length
        self._deleted_text = ""

    def execute(self) -> None:
        self._deleted_text = self.editor.delete(self.start, self.length)
        print(f"Deleted '{self._deleted_text}' from position {self.start}")

    def undo(self) -> None:
        self.editor.insert(self._deleted_text, self.start)
        print(f"Restored '{self._deleted_text}'")


class CopyCommand(Command):
    """复制命令"""

    def __init__(self, editor: TextEditor, start: int, length: int):
        self.editor = editor
        self.start = start
        self.length = length
        self._previous_clipboard = ""

    def execute(self) -> None:
        self._previous_clipboard = self.editor.clipboard
        self.editor.select(self.start, self.length)
        self.editor.copy()
        print(f"Copied '{self.editor.clipboard}'")

    def undo(self) -> None:
        self.editor.clipboard = self._previous_clipboard
        print(f"Restored clipboard to '{self._previous_clipboard}'")


class PasteCommand(Command):
    """粘贴命令"""

    def __init__(self, editor: TextEditor, position: int = None):
        self.editor = editor
        self.position = position
        self._pasted_length = 0

    def execute(self) -> None:
        pos = self.position or len(self.editor.content)
        self.editor.paste(pos)
        self._pasted_length = len(self.editor.clipboard)
        print(f"Pasted '{self.editor.clipboard}' at position {pos}")

    def undo(self) -> None:
        pos = self.position or (len(self.editor.content) - self._pasted_length)
        self.editor.delete(pos, self._pasted_length)
        print(f"Undone paste")


# ============ 调用者 ============

class CommandHistory:
    """命令历史 - 支持撤销/重做"""

    def __init__(self):
        self._history: List[Command] = []
        self._current_index = -1

    def push(self, command: Command) -> None:
        """添加命令"""
        # 删除当前位置之后的所有命令（重做历史）
        self._history = self._history[:self._current_index + 1]
        self._history.append(command)
        self._current_index += 1

    def undo(self) -> bool:
        """撤销"""
        if self._current_index >= 0:
            command = self._history[self._current_index]
            command.undo()
            self._current_index -= 1
            return True
        print("Nothing to undo")
        return False

    def redo(self) -> bool:
        """重做"""
        if self._current_index < len(self._history) - 1:
            self._current_index += 1
            command = self._history[self._current_index]
            command.execute()
            return True
        print("Nothing to redo")
        return False

    def get_history(self) -> List[str]:
        return [cmd.get_name() for cmd in self._history]


class EditorInvoker:
    """编辑器调用者"""

    def __init__(self, editor: TextEditor):
        self.editor = editor
        self.history = CommandHistory()

    def execute(self, command: Command) -> None:
        """执行命令"""
        command.execute()
        self.history.push(command)

    def undo(self) -> None:
        self.history.undo()

    def redo(self) -> None:
        self.history.redo()

    def get_content(self) -> str:
        return self.editor.get_content()


# ============ 使用示例 ============

print("=== Command Pattern: Text Editor ===")

editor = TextEditor()
invoker = EditorInvoker(editor)

# 执行一系列命令
print("\n--- Executing commands ---")
invoker.execute(InsertCommand(editor, "Hello "))
invoker.execute(InsertCommand(editor, "World"))
invoker.execute(InsertCommand(editor, "!"))

print(f"\nContent: '{invoker.get_content()}'")

# 撤销
print("\n--- Undoing ---")
invoker.undo()
print(f"Content: '{invoker.get_content()}'")

invoker.undo()
print(f"Content: '{invoker.get_content()}'")

# 重做
print("\n--- Redoing ---")
invoker.redo()
print(f"Content: '{invoker.get_content()}'")

# 新命令会清除重做历史
print("\n--- New command (clears redo history) ---")
invoker.execute(InsertCommand(editor, " Python"))
print(f"Content: '{invoker.get_content()}'")

print(f"\nHistory: {invoker.history.get_history()}")
```

#### 正例：任务队列

```python
import queue
import threading
import time


class TaskCommand(Command):
    """任务命令"""

    def __init__(self, name: str, action: Callable, *args, **kwargs):
        self.name = name
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.executed_at = None

    def execute(self) -> None:
        self.executed_at = datetime.now()
        self.result = self.action(*self.args, **self.kwargs)
        print(f"[Task] {self.name} completed with result: {self.result}")

    def undo(self) -> None:
        print(f"[Task] {self.name} undo not supported")


class TaskQueue:
    """任务队列"""

    def __init__(self, num_workers: int = 2):
        self.queue = queue.Queue()
        self.workers = []
        self.running = False

        for i in range(num_workers):
            worker = threading.Thread(target=self._worker_loop, args=(i,))
            self.workers.append(worker)

    def start(self):
        self.running = True
        for worker in self.workers:
            worker.start()

    def stop(self):
        self.running = False
        for worker in self.workers:
            worker.join()

    def submit(self, command: TaskCommand) -> None:
        self.queue.put(command)

    def _worker_loop(self, worker_id: int):
        while self.running:
            try:
                command = self.queue.get(timeout=1)
                print(f"[Worker {worker_id}] Processing: {command.name}")
                command.execute()
                self.queue.task_done()
            except queue.Empty:
                continue


# 使用
print("\n=== Task Queue ===")

def send_email(to: str, subject: str) -> str:
    time.sleep(0.5)
    return f"Email sent to {to}"

def process_payment(order_id: str, amount: float) -> str:
    time.sleep(0.3)
    return f"Payment processed for order {order_id}"

def generate_report(report_type: str) -> str:
    time.sleep(0.4)
    return f"{report_type} report generated"

task_queue = TaskQueue(num_workers=2)
task_queue.start()

task_queue.submit(TaskCommand("email_task", send_email, "user@example.com", "Welcome"))
task_queue.submit(TaskCommand("payment_task", process_payment, "ORD-123", 99.99))
task_queue.submit(TaskCommand("report_task", generate_report, "monthly"))

time.sleep(2)
task_queue.stop()
```

#### 反例：直接调用

```python
# ❌ 错误：直接调用，无法撤销
class BadEditor:
    def insert(self, text):
        self.content += text  # 无法撤销

    def delete(self, start, length):
        self.content = self.content[:start] + self.content[start+length:]
        # 删除的内容丢失，无法恢复

# 问题：
# 1. 无法撤销
# 2. 无法记录操作
# 3. 无法队列化

# ✅ 正确：使用命令模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 支持撤销/重做 | 类数量增加 |
| 支持队列和日志 | 代码复杂度增加 |
| 解耦调用者和接收者 | 每个命令需要新类 |

---

### 3.3 解释器模式（Interpreter）

#### 意图

给定一个语言，定义它的文法表示，并定义一个解释器来解释语言中的句子。

#### 适用场景

- 需要解释特定领域语言
- 文法简单且稳定
- 效率不是关键

#### UML结构图

```
┌─────────────┐
│  Expression │
├─────────────┤
│ + interpret │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
┌─┴─┐    ┌──┴──┐
│Terminal│Non- │
│Expr    │Terminal
└────────┴─────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import Dict, List
import re


# ============ 抽象表达式 ============

class Expression(ABC):
    """表达式接口"""

    @abstractmethod
    def interpret(self, context: Dict) -> bool:
        pass


# ============ 终结符表达式 ============

class VariableExpression(Expression):
    """变量表达式"""

    def __init__(self, name: str):
        self.name = name

    def interpret(self, context: Dict) -> bool:
        return context.get(self.name, False)


class ConstantExpression(Expression):
    """常量表达式"""

    def __init__(self, value: bool):
        self.value = value

    def interpret(self, context: Dict) -> bool:
        return self.value


# ============ 非终结符表达式 ============

class AndExpression(Expression):
    """与表达式"""

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: Dict) -> bool:
        return self.left.interpret(context) and self.right.interpret(context)


class OrExpression(Expression):
    """或表达式"""

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: Dict) -> bool:
        return self.left.interpret(context) or self.right.interpret(context)


class NotExpression(Expression):
    """非表达式"""

    def __init__(self, expression: Expression):
        self.expression = expression

    def interpret(self, context: Dict) -> bool:
        return not self.expression.interpret(context)


# ============ 规则解析器 ============

class RuleParser:
    """规则解析器"""

    def __init__(self):
        self.tokens = []
        self.position = 0

    def parse(self, rule: str) -> Expression:
        """解析规则字符串"""
        # 简单的词法分析
        self.tokens = re.findall(r'\(|\)|AND|OR|NOT|[a-zA-Z_][a-zA-Z0-9_]*', rule)
        self.position = 0
        return self._parse_expression()

    def _parse_expression(self) -> Expression:
        """解析表达式"""
        token = self._current_token()

        if token == "NOT":
            self._consume("NOT")
            return NotExpression(self._parse_expression())

        if token == "(":
            self._consume("(")
            expr = self._parse_or_expression()
            self._consume(")")
            return expr

        # 变量
        self._consume(token)
        return VariableExpression(token)

    def _parse_or_expression(self) -> Expression:
        """解析或表达式"""
        left = self._parse_and_expression()

        while self._current_token() == "OR":
            self._consume("OR")
            right = self._parse_and_expression()
            left = OrExpression(left, right)

        return left

    def _parse_and_expression(self) -> Expression:
        """解析与表达式"""
        left = self._parse_expression()

        while self._current_token() == "AND":
            self._consume("AND")
            right = self._parse_expression()
            left = AndExpression(left, right)

        return left

    def _current_token(self) -> str:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ""

    def _consume(self, expected: str):
        if self._current_token() != expected:
            raise ValueError(f"Expected {expected}, got {self._current_token()}")
        self.position += 1


# ============ 使用示例 ============

print("=== Interpreter Pattern ===")

# 构建表达式树
# (is_premium AND has_good_credit) OR (is_vip AND NOT is_blacklisted)
expression = OrExpression(
    AndExpression(
        VariableExpression("is_premium"),
        VariableExpression("has_good_credit")
    ),
    AndExpression(
        VariableExpression("is_vip"),
        NotExpression(VariableExpression("is_blacklisted"))
    )
)

# 测试不同上下文
test_cases = [
    {"is_premium": True, "has_good_credit": True, "is_vip": False, "is_blacklisted": False},
    {"is_premium": True, "has_good_credit": False, "is_vip": True, "is_blacklisted": False},
    {"is_premium": False, "has_good_credit": False, "is_vip": True, "is_blacklisted": True},
    {"is_premium": False, "has_good_credit": False, "is_vip": True, "is_blacklisted": False},
]

for i, context in enumerate(test_cases):
    result = expression.interpret(context)
    print(f"Case {i+1}: {context}")
    print(f"  Result: {result}\n")

# 使用解析器
print("--- Using Rule Parser ---")
parser = RuleParser()
rule = "(is_member AND has_subscription) OR is_admin"
parsed = parser.parse(rule)

context = {"is_member": True, "has_subscription": False, "is_admin": True}
print(f"Rule: {rule}")
print(f"Context: {context}")
print(f"Result: {parsed.interpret(context)}")
```

#### 正例：SQL查询构建器

```python
class QueryExpression(ABC):
    """查询表达式"""

    @abstractmethod
    def to_sql(self) -> str:
        pass


class FieldExpression(QueryExpression):
    """字段表达式"""

    def __init__(self, name: str, value: any, operator: str = "="):
        self.name = name
        self.value = value
        self.operator = operator

    def to_sql(self) -> str:
        if isinstance(self.value, str):
            return f"{self.name} {self.operator} '{self.value}'"
        return f"{self.name} {self.operator} {self.value}"


class AndCondition(QueryExpression):
    """AND条件"""

    def __init__(self, *conditions: QueryExpression):
        self.conditions = conditions

    def to_sql(self) -> str:
        return " AND ".join(f"({c.to_sql()})" for c in self.conditions)


class OrCondition(QueryExpression):
    """OR条件"""

    def __init__(self, *conditions: QueryExpression):
        self.conditions = conditions

    def to_sql(self) -> str:
        return " OR ".join(f"({c.to_sql()})" for c in self.conditions)


class QueryBuilder:
    """查询构建器"""

    def __init__(self):
        self.table = ""
        self.fields = ["*"]
        self.where = None

    def select(self, *fields: str) -> 'QueryBuilder':
        self.fields = list(fields) if fields else ["*"]
        return self

    def from_table(self, table: str) -> 'QueryBuilder':
        self.table = table
        return self

    def where(self, condition: QueryExpression) -> 'QueryBuilder':
        self.where = condition
        return self

    def build(self) -> str:
        query = f"SELECT {', '.join(self.fields)} FROM {self.table}"
        if self.where:
            query += f" WHERE {self.where.to_sql()}"
        return query


# 使用
print("\n=== Query Builder ===")

query = (QueryBuilder()
    .select("id", "name", "email")
    .from_table("users")
    .where(OrCondition(
        AndCondition(
            FieldExpression("age", 18, ">="),
            FieldExpression("status", "active")
        ),
        FieldExpression("role", "admin")
    ))
    .build())

print(f"SQL: {query}")
```

#### 反例：复杂文法

```python
# ❌ 错误：对复杂文法使用解释器模式
# 复杂文法应该使用解析器生成器（如ANTLR）

# 问题：
# 1. 复杂文法导致类爆炸
# 2. 难以维护
# 3. 性能问题

# ✅ 正确：简单文法使用解释器，复杂文法使用专业工具
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 易于改变和扩展文法 | 复杂文法难以维护 |
| 易于实现 | 性能问题 |
| 符合开闭原则 | 不适合复杂文法 |

---

### 3.4 迭代器模式（Iterator）

#### 意图

提供一种方法顺序访问聚合对象中的各个元素，而又不暴露其内部表示。

#### 适用场景

- 需要遍历聚合对象
- 需要多种遍历方式
- 需要统一遍历接口

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import Any, List, Optional


# ============ 迭代器接口 ============

class Iterator(ABC):
    """迭代器接口"""

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Any:
        pass

    @abstractmethod
    def current(self) -> Any:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass


# ============ 聚合接口 ============

class IterableCollection(ABC):
    """可迭代集合接口"""

    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass


# ============ 具体迭代器 ============

class BookIterator(Iterator):
    """书籍迭代器"""

    def __init__(self, books: List[Any]):
        self._books = books
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._books)

    def next(self) -> Any:
        if not self.has_next():
            raise StopIteration()
        book = self._books[self._position]
        self._position += 1
        return book

    def current(self) -> Any:
        if self._position >= len(self._books):
            return None
        return self._books[self._position]

    def reset(self) -> None:
        self._position = 0


class ReverseBookIterator(Iterator):
    """反向书籍迭代器"""

    def __init__(self, books: List[Any]):
        self._books = books
        self._position = len(books) - 1

    def has_next(self) -> bool:
        return self._position >= 0

    def next(self) -> Any:
        if not self.has_next():
            raise StopIteration()
        book = self._books[self._position]
        self._position -= 1
        return book

    def current(self) -> Any:
        if self._position < 0:
            return None
        return self._books[self._position]

    def reset(self) -> None:
        self._position = len(self._books) - 1


class FilteredBookIterator(Iterator):
    """过滤迭代器"""

    def __init__(self, books: List[Any], predicate):
        self._books = books
        self._predicate = predicate
        self._position = 0
        self._find_next()

    def _find_next(self):
        """找到下一个符合条件的元素"""
        while (self._position < len(self._books) and
               not self._predicate(self._books[self._position])):
            self._position += 1

    def has_next(self) -> bool:
        return self._position < len(self._books)

    def next(self) -> Any:
        if not self.has_next():
            raise StopIteration()
        book = self._books[self._position]
        self._position += 1
        self._find_next()
        return book

    def current(self) -> Any:
        if self._position >= len(self._books):
            return None
        return self._books[self._position]

    def reset(self) -> None:
        self._position = 0
        self._find_next()


# ============ 具体集合 ============

class Book:
    """书籍"""

    def __init__(self, title: str, author: str, year: int, genre: str):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"


class Library(IterableCollection):
    """图书馆 - 聚合对象"""

    def __init__(self):
        self._books: List[Book] = []

    def add_book(self, book: Book) -> 'Library':
        self._books.append(book)
        return self

    def create_iterator(self) -> Iterator:
        return BookIterator(self._books)

    def create_reverse_iterator(self) -> Iterator:
        return ReverseBookIterator(self._books)

    def create_genre_iterator(self, genre: str) -> Iterator:
        return FilteredBookIterator(
            self._books,
            lambda book: book.genre == genre
        )

    def create_year_range_iterator(self, start: int, end: int) -> Iterator:
        return FilteredBookIterator(
            self._books,
            lambda book: start <= book.year <= end
        )


# ============ 使用示例 ============

print("=== Iterator Pattern ===")

library = Library()
library.add_book(Book("Python Design Patterns", "John Smith", 2020, "Tech"))
library.add_book(Book("Clean Code", "Robert Martin", 2008, "Tech"))
library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction"))
library.add_book(Book("1984", "George Orwell", 1949, "Fiction"))
library.add_book(Book("Python Cookbook", "David Beazley", 2013, "Tech"))

print("\n--- Forward Iteration ---")
iterator = library.create_iterator()
while iterator.has_next():
    print(f"  {iterator.next()}")

print("\n--- Reverse Iteration ---")
reverse = library.create_reverse_iterator()
while reverse.has_next():
    print(f"  {reverse.next()}")

print("\n--- Tech Books Only ---")
tech_iterator = library.create_genre_iterator("Tech")
while tech_iterator.has_next():
    print(f"  {tech_iterator.next()}")

print("\n--- Books from 2000-2020 ---")
recent_iterator = library.create_year_range_iterator(2000, 2020)
while recent_iterator.has_next():
    print(f"  {recent_iterator.next()}")
```

#### Python迭代器协议

```python
# ============ Python内置迭代器协议 ============

class CustomCollection:
    """自定义集合 - 实现Python迭代器协议"""

    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def __iter__(self):
        """返回迭代器对象"""
        return CustomIterator(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        """支持索引访问"""
        return self._items[index]


class CustomIterator:
    """自定义迭代器"""

    def __init__(self, items):
        self._items = items
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item


# 使用Python迭代器协议
print("\n=== Python Iterator Protocol ===")

collection = CustomCollection()
collection.add("Item 1")
collection.add("Item 2")
collection.add("Item 3")

# for循环使用__iter__
print("For loop:")
for item in collection:
    print(f"  {item}")

# 列表推导
print("\nList comprehension:")
squared = [x + "!" for x in collection]
print(f"  {squared}")

# 生成器表达式
print("\nGenerator expression:")
upper = list(x.upper() for x in collection)
print(f"  {upper}")


# ============ 使用生成器简化 ============

class SimpleCollection:
    """使用生成器简化迭代器"""

    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def __iter__(self):
        """使用生成器简化迭代器实现"""
        for item in self._items:
            yield item

    def filtered_iter(self, predicate):
        """过滤迭代器"""
        for item in self._items:
            if predicate(item):
                yield item


# 使用
print("\n=== Generator-based Iterator ===")
simple = SimpleCollection()
simple.add(1)
simple.add(2)
simple.add(3)
simple.add(4)
simple.add(5)

print("All items:")
for item in simple:
    print(f"  {item}")

print("\nEven items only:")
for item in simple.filtered_iter(lambda x: x % 2 == 0):
    print(f"  {item}")
```

#### 正例：二叉树迭代器

```python
class TreeNode:
    """树节点"""

    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value: int):
        if value < self.value:
            if self.left is None:
                self.left = TreeNode(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = TreeNode(value)
            else:
                self.right.insert(value)


class BinaryTree:
    """二叉树 - 多种遍历方式"""

    def __init__(self):
        self.root = None

    def insert(self, value: int):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self.root.insert(value)

    def inorder(self):
        """中序遍历"""
        return InorderIterator(self.root)

    def preorder(self):
        """前序遍历"""
        return PreorderIterator(self.root)

    def postorder(self):
        """后序遍历"""
        return PostorderIterator(self.root)


class InorderIterator:
    """中序遍历迭代器"""

    def __init__(self, root: TreeNode):
        self._stack = []
        self._current = root
        self._advance()

    def _advance(self):
        """移动到下一个节点"""
        while self._current:
            self._stack.append(self._current)
            self._current = self._current.left

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if not self._stack:
            raise StopIteration

        node = self._stack.pop()
        value = node.value

        # 处理右子树
        self._current = node.right
        self._advance()

        return value


class PreorderIterator:
    """前序遍历迭代器"""

    def __init__(self, root: TreeNode):
        self._stack = [root] if root else []

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if not self._stack:
            raise StopIteration

        node = self._stack.pop()

        # 右子树先入栈（后出）
        if node.right:
            self._stack.append(node.right)
        if node.left:
            self._stack.append(node.left)

        return node.value


class PostorderIterator:
    """后序遍历迭代器"""

    def __init__(self, root: TreeNode):
        self._stack = []
        self._output = []
        if root:
            self._stack.append(root)

        # 使用两个栈实现后序遍历
        while self._stack:
            node = self._stack.pop()
            self._output.append(node.value)

            if node.left:
                self._stack.append(node.left)
            if node.right:
                self._stack.append(node.right)

        self._output.reverse()
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self._index >= len(self._output):
            raise StopIteration

        value = self._output[self._index]
        self._index += 1
        return value


# 使用
print("\n=== Binary Tree Iterators ===")

tree = BinaryTree()
for value in [5, 3, 7, 1, 4, 6, 8]:
    tree.insert(value)

print("Inorder (sorted):")
for value in tree.inorder():
    print(f"  {value}", end=" ")

print("\nPreorder:")
for value in tree.preorder():
    print(f"  {value}", end=" ")

print("\nPostorder:")
for value in tree.postorder():
    print(f"  {value}", end=" ")
print()
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 统一遍历接口 | 增加代码复杂度 |
| 多种遍历方式 | 对于简单集合可能过度设计 |
| 解耦遍历与集合 | |

---

### 3.5 中介者模式（Mediator）

#### 意图

定义一个对象来封装一组对象之间的交互，使对象之间不需要显式相互引用。

#### 适用场景

- 对象间有复杂引用关系
- 需要改变对象间交互
- 需要复用对象但交互复杂

#### UML结构图

```
┌─────────────┐
│   Mediator  │
├─────────────┤
│ + notify()  │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
┌─┴─┐    ┌──┴──┐
│ A │    │  B  │
└───┘    └─────┘
```

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import Dict, List
from enum import Enum


# ============ 中介者接口 ============

class ChatMediator(ABC):
    """聊天中介者"""

    @abstractmethod
    def send_message(self, message: str, sender: 'User') -> None:
        pass

    @abstractmethod
    def send_private_message(self, message: str, sender: 'User', receiver: 'User') -> None:
        pass

    @abstractmethod
    def add_user(self, user: 'User') -> None:
        pass

    @abstractmethod
    def remove_user(self, user: 'User') -> None:
        pass


# ============ 具体中介者 ============

class ChatRoom(ChatMediator):
    """聊天室 - 具体中介者"""

    def __init__(self, name: str):
        self.name = name
        self._users: Dict[str, 'User'] = {}
        self._message_history: List[str] = []

    def add_user(self, user: 'User') -> None:
        self._users[user.name] = user
        user.mediator = self
        self._broadcast(f"{user.name} joined the room", system=True)

    def remove_user(self, user: 'User') -> None:
        if user.name in self._users:
            del self._users[user.name]
            self._broadcast(f"{user.name} left the room", system=True)

    def send_message(self, message: str, sender: 'User') -> None:
        self._broadcast(f"[{sender.name}]: {message}")

    def send_private_message(self, message: str, sender: 'User', receiver: 'User') -> None:
        if receiver.name in self._users:
            private_msg = f"[Private from {sender.name}]: {message}"
            receiver.receive(private_msg)
            sender.receive(f"[Private to {receiver.name}]: {message}")

    def _broadcast(self, message: str, system: bool = False) -> None:
        prefix = "[System] " if system else ""
        full_message = prefix + message
        self._message_history.append(full_message)

        for user in self._users.values():
            user.receive(full_message)

    def get_history(self) -> List[str]:
        return self._message_history.copy()


# ============ 同事类 ============

class User:
    """用户 - 同事类"""

    def __init__(self, name: str):
        self.name = name
        self.mediator: ChatMediator = None
        self._messages: List[str] = []

    def send(self, message: str) -> None:
        """发送消息"""
        if self.mediator:
            self.mediator.send_message(message, self)

    def send_private(self, message: str, receiver_name: str) -> None:
        """发送私信"""
        if self.mediator and isinstance(self.mediator, ChatRoom):
            receiver = self.mediator._users.get(receiver_name)
            if receiver:
                self.mediator.send_private_message(message, self, receiver)

    def receive(self, message: str) -> None:
        """接收消息"""
        self._messages.append(message)
        print(f"{self.name} received: {message}")

    def get_messages(self) -> List[str]:
        return self._messages.copy()


# ============ 使用示例 ============

print("=== Mediator Pattern: Chat Room ===")

# 创建聊天室
room = ChatRoom("Python Developers")

# 创建用户
alice = User("Alice")
bob = User("Bob")
charlie = User("Charlie")

# 用户加入聊天室
room.add_user(alice)
room.add_user(bob)
room.add_user(charlie)

print("\n--- Public Messages ---")
alice.send("Hello everyone!")
bob.send("Hi Alice!")

print("\n--- Private Message ---")
alice.send_private("Hey Bob, how are you?", "Bob")

print("\n--- User Leaves ---")
room.remove_user(charlie)
bob.send("Charlie left...")

print(f"\n--- Chat History ---")
for msg in room.get_history():
    print(f"  {msg}")
```

#### 正例：MVC控制器

```python
class Component(ABC):
    """组件基类"""

    def __init__(self, mediator: 'FormMediator' = None):
        self.mediator = mediator

    def changed(self):
        """通知中介者状态改变"""
        if self.mediator:
            self.mediator.notify(self, "changed")


class FormMediator:
    """表单中介者"""

    def __init__(self):
        self.username = None
        self.password = None
        self.confirm_password = None
        self.submit_button = None
        self.error_label = None

    def register_component(self, name: str, component: Component):
        setattr(self, name, component)
        component.mediator = self

    def notify(self, sender: Component, event: str):
        """处理组件通知"""
        if event == "changed":
            self._validate_form()

    def _validate_form(self):
        """验证表单"""
        errors = []

        if self.username and not self.username.value:
            errors.append("Username is required")

        if self.password and self.confirm_password:
            if self.password.value != self.confirm_password.value:
                errors.append("Passwords do not match")

        # 更新提交按钮状态
        if self.submit_button:
            self.submit_button.enabled = len(errors) == 0

        # 更新错误信息
        if self.error_label:
            self.error_label.text = "\n".join(errors) if errors else ""


class TextField(Component):
    """文本框组件"""

    def __init__(self, mediator: FormMediator = None):
        super().__init__(mediator)
        self._value = ""

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self.changed()


class Button(Component):
    """按钮组件"""

    def __init__(self, mediator: FormMediator = None):
        super().__init__(mediator)
        self.enabled = False


class Label(Component):
    """标签组件"""

    def __init__(self, mediator: FormMediator = None):
        super().__init__(mediator)
        self.text = ""


# 使用
print("\n=== Form Mediator ===")

mediator = FormMediator()

username = TextField()
password = TextField()
confirm = TextField()
submit = Button()
error = Label()

mediator.register_component("username", username)
mediator.register_component("password", password)
mediator.register_component("confirm_password", confirm)
mediator.register_component("submit_button", submit)
mediator.register_component("error_label", error)

print("Setting username...")
username.value = "john_doe"
print(f"Submit enabled: {submit.enabled}")

print("\nSetting passwords (mismatch)...")
password.value = "secret123"
confirm.value = "secret456"
print(f"Submit enabled: {submit.enabled}")
print(f"Error: {error.text}")

print("\nFixing passwords...")
confirm.value = "secret123"
print(f"Submit enabled: {submit.enabled}")
print(f"Error: {error.text}")
```

#### 反例：上帝中介者

```python
# ❌ 错误：中介者成为上帝对象
class BadMediator:
    def method1(self): pass
    def method2(self): pass
    # ... 100+ 方法

# 问题：
# 1. 违反单一职责
# 2. 难以维护
# 3. 成为瓶颈

# ✅ 正确：按功能拆分或使用观察者模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 解耦同事类 | 中介者可能变得复杂 |
| 集中控制交互 | 可能成为瓶颈 |
| 简化对象协议 | 难以维护 |

---

### 3.6 备忘录模式（Memento）

#### 意图

在不破坏封装性的情况下，捕获对象的内部状态，并在对象之外保存这个状态。

#### 适用场景

- 需要保存和恢复对象状态
- 需要实现撤销功能
- 需要检查点功能

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from copy import deepcopy
import json


# ============ 备忘录 ============

@dataclass
class EditorMemento:
    """编辑器备忘录"""
    content: str
    cursor_position: int
    selection: str
    timestamp: str

    def get_state(self) -> Dict:
        return {
            "content": self.content,
            "cursor_position": self.cursor_position,
            "selection": self.selection,
            "timestamp": self.timestamp
        }


# ============ 原发器 ============

class TextEditor:
    """文本编辑器 - 原发器"""

    def __init__(self):
        self._content = ""
        self._cursor_position = 0
        self._selection = ""

    # 业务方法
    def type_text(self, text: str) -> None:
        """输入文本"""
        self._content = (
            self._content[:self._cursor_position] +
            text +
            self._content[self._cursor_position:]
        )
        self._cursor_position += len(text)

    def delete_text(self, length: int) -> str:
        """删除文本"""
        deleted = self._content[self._cursor_position:self._cursor_position + length]
        self._content = (
            self._content[:self._cursor_position] +
            self._content[self._cursor_position + length:]
        )
        return deleted

    def select_text(self, start: int, length: int) -> None:
        """选择文本"""
        self._selection = self._content[start:start + length]

    # 备忘录方法
    def save(self) -> EditorMemento:
        """创建备忘录"""
        from datetime import datetime
        return EditorMemento(
            content=self._content,
            cursor_position=self._cursor_position,
            selection=self._selection,
            timestamp=datetime.now().isoformat()
        )

    def restore(self, memento: EditorMemento) -> None:
        """从备忘录恢复"""
        self._content = memento.content
        self._cursor_position = memento.cursor_position
        self._selection = memento.selection

    def get_state(self) -> Dict:
        """获取当前状态"""
        return {
            "content": self._content,
            "cursor": self._cursor_position,
            "selection": self._selection
        }


# ============ 负责人 ============

class HistoryManager:
    """历史管理器 - 负责人"""

    def __init__(self, editor: TextEditor):
        self._editor = editor
        self._history: List[EditorMemento] = []
        self._current_index = -1
        self._max_history = 50

    def backup(self) -> None:
        """备份当前状态"""
        # 删除当前位置之后的所有历史
        self._history = self._history[:self._current_index + 1]

        # 添加新备份
        self._history.append(self._editor.save())
        self._current_index += 1

        # 限制历史大小
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._current_index -= 1

    def undo(self) -> bool:
        """撤销"""
        if self._current_index > 0:
            self._current_index -= 1
            self._editor.restore(self._history[self._current_index])
            return True
        return False

    def redo(self) -> bool:
        """重做"""
        if self._current_index < len(self._history) - 1:
            self._current_index += 1
            self._editor.restore(self._history[self._current_index])
            return True
        return False

    def get_history_list(self) -> List[str]:
        """获取历史列表"""
        return [m.timestamp for m in self._history]


# ============ 使用示例 ============

print("=== Memento Pattern ===")

editor = TextEditor()
history = HistoryManager(editor)

# 初始备份
history.backup()

# 编辑操作
print("\n--- Editing ---")
editor.type_text("Hello")
history.backup()
print(f"State: {editor.get_state()}")

editor.type_text(" World")
history.backup()
print(f"State: {editor.get_state()}")

editor.type_text("!")
history.backup()
print(f"State: {editor.get_state()}")

# 撤销
print("\n--- Undo ---")
history.undo()
print(f"After undo: {editor.get_state()}")

history.undo()
print(f"After undo: {editor.get_state()}")

# 重做
print("\n--- Redo ---")
history.redo()
print(f"After redo: {editor.get_state()}")

# 新操作会清除重做历史
print("\n--- New Operation ---")
editor.type_text(" Python")
history.backup()
print(f"State: {editor.get_state()}")

print(f"\nHistory: {history.get_history_list()}")
```

#### 正例：游戏存档系统

```python
@dataclass
class GameState:
    """游戏状态"""
    level: int
    health: int
    score: int
    inventory: List[str]
    position: tuple
    timestamp: str


class GameCharacter:
    """游戏角色"""

    def __init__(self, name: str):
        self.name = name
        self.level = 1
        self.health = 100
        self.score = 0
        self.inventory = []
        self.position = (0, 0)

    def level_up(self):
        self.level += 1
        self.health = 100

    def take_damage(self, damage: int):
        self.health = max(0, self.health - damage)

    def add_item(self, item: str):
        self.inventory.append(item)

    def move(self, x: int, y: int):
        self.position = (self.position[0] + x, self.position[1] + y)

    def save(self) -> GameState:
        from datetime import datetime
        return GameState(
            level=self.level,
            health=self.health,
            score=self.score,
            inventory=deepcopy(self.inventory),
            position=self.position,
            timestamp=datetime.now().isoformat()
        )

    def load(self, state: GameState):
        self.level = state.level
        self.health = state.health
        self.score = state.score
        self.inventory = deepcopy(state.inventory)
        self.position = state.position

    def __str__(self):
        return (f"{self.name}: Lv.{self.level}, HP:{self.health}, "
                f"Score:{self.score}, Pos:{self.position}")


class SaveManager:
    """存档管理器"""

    def __init__(self):
        self._saves: Dict[str, GameState] = {}

    def save(self, name: str, character: GameCharacter):
        """保存游戏"""
        self._saves[name] = character.save()
        print(f"Game saved: {name}")

    def load(self, name: str, character: GameCharacter):
        """加载游戏"""
        if name not in self._saves:
            raise ValueError(f"Save not found: {name}")
        character.load(self._saves[name])
        print(f"Game loaded: {name}")

    def list_saves(self) -> List[str]:
        return list(self._saves.keys())

    def delete_save(self, name: str):
        if name in self._saves:
            del self._saves[name]


# 使用
print("\n=== Game Save System ===")

player = GameCharacter("Hero")
save_manager = SaveManager()

# 游戏过程
player.move(10, 20)
player.add_item("Sword")
player.add_item("Shield")
player.level_up()
print(f"After playing: {player}")

# 保存
save_manager.save("level2_checkpoint", player)

# 继续游戏
player.take_damage(30)
player.move(5, 5)
print(f"After more playing: {player}")

# 加载存档
save_manager.load("level2_checkpoint", player)
print(f"After load: {player}")
```

#### 反例：破坏封装

```python
# ❌ 错误：备忘录暴露内部状态
class BadMemento:
    def __init__(self, editor):
        self.content = editor._content  # 直接访问私有属性
        self.cursor = editor._cursor

# 问题：
# 1. 破坏封装
# 2. 违反迪米特法则
# 3. 难以维护

# ✅ 正确：通过原发器创建备忘录，保持封装
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 保持封装 | 内存消耗 |
| 简化原发器 | 维护成本 |
| 支持撤销 | 历史管理复杂 |

---

### 3.7 观察者模式（Observer）

#### 意图

定义对象间的一对多依赖关系，当一个对象状态改变时，所有依赖者都会收到通知。

#### 适用场景

- 一个对象改变需要改变其他对象
- 需要事件订阅机制
- 需要松耦合通信

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import List, Set
from dataclasses import dataclass
from datetime import datetime


# ============ 主题接口 ============

class Subject(ABC):
    """主题接口"""

    def __init__(self):
        self._observers: List['Observer'] = []

    def attach(self, observer: 'Observer') -> None:
        """添加观察者"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        """移除观察者"""
        self._observers.remove(observer)

    def notify(self) -> None:
        """通知所有观察者"""
        for observer in self._observers:
            observer.update(self)


# ============ 观察者接口 ============

class Observer(ABC):
    """观察者接口"""

    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass


# ============ 具体主题 ============

@dataclass
class NewsArticle:
    """新闻文章"""
    title: str
    content: str
    category: str
    published_at: datetime


class NewsPublisher(Subject):
    """新闻发布者"""

    def __init__(self):
        super().__init__()
        self._latest_article: NewsArticle = None
        self._articles: List[NewsArticle] = []

    def publish(self, article: NewsArticle) -> None:
        """发布新闻"""
        self._articles.append(article)
        self._latest_article = article
        print(f"\n[Publisher] New article published: {article.title}")
        self.notify()

    def get_latest_article(self) -> NewsArticle:
        return self._latest_article

    def get_articles_by_category(self, category: str) -> List[NewsArticle]:
        return [a for a in self._articles if a.category == category]


# ============ 具体观察者 ============

class EmailSubscriber(Observer):
    """邮件订阅者"""

    def __init__(self, email: str, preferred_categories: List[str] = None):
        self.email = email
        self.preferred_categories = preferred_categories or []
        self.notifications = []

    def update(self, subject: NewsPublisher) -> None:
        article = subject.get_latest_article()

        # 检查是否感兴趣
        if (not self.preferred_categories or
            article.category in self.preferred_categories):

            notification = f"Email to {self.email}: {article.title}"
            self.notifications.append(notification)
            print(f"  [Email] {notification}")


class SMSSubscriber(Observer):
    """短信订阅者"""

    def __init__(self, phone: str, urgent_only: bool = False):
        self.phone = phone
        self.urgent_only = urgent_only
        self.notifications = []

    def update(self, subject: NewsPublisher) -> None:
        article = subject.get_latest_article()

        if self.urgent_only and article.category != "Urgent":
            return

        notification = f"SMS to {self.phone}: {article.title[:30]}..."
        self.notifications.append(notification)
        print(f"  [SMS] {notification}")


class PushSubscriber(Observer):
    """推送订阅者"""

    def __init__(self, device_id: str):
        self.device_id = device_id
        self.notifications = []

    def update(self, subject: NewsPublisher) -> None:
        article = subject.get_latest_article()
        notification = f"Push to {self.device_id}: {article.title}"
        self.notifications.append(notification)
        print(f"  [Push] {notification}")


class AnalyticsObserver(Observer):
    """分析观察者"""

    def __init__(self):
        self.article_views = {}

    def update(self, subject: NewsPublisher) -> None:
        article = subject.get_latest_article()
        self.article_views[article.title] = 0
        print(f"  [Analytics] Tracking article: {article.title}")


# ============ 使用示例 ============

print("=== Observer Pattern ===")

# 创建发布者
publisher = NewsPublisher()

# 创建订阅者
email_sub = EmailSubscriber("user@example.com", ["Tech", "Science"])
sms_sub = SMSSubscriber("+1234567890")
push_sub = PushSubscriber("device_123")
analytics = AnalyticsObserver()

# 订阅
publisher.attach(email_sub)
publisher.attach(sms_sub)
publisher.attach(push_sub)
publisher.attach(analytics)

# 发布新闻
publisher.publish(NewsArticle(
    "Python 3.12 Released",
    "New features include...",
    "Tech",
    datetime.now()
))

publisher.publish(NewsArticle(
    "Breaking: Major Discovery",
    "Scientists have found...",
    "Science",
    datetime.now()
))

# 取消订阅
publisher.detach(sms_sub)

publisher.publish(NewsArticle(
    "Sports Update",
    "Latest match results...",
    "Sports",
    datetime.now()
))

print(f"\nEmail notifications: {len(email_sub.notifications)}")
print(f"SMS notifications: {len(sms_sub.notifications)}")
```

#### Pythonic实现：使用内置功能

```python
# ============ 使用property和回调 ============

class ObservableProperty:
    """可观察属性"""

    def __init__(self, initial_value=None):
        self._value = initial_value
        self._callbacks = []

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        self._callbacks.remove(callback)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        old_value = self._value
        self._value = new_value
        for callback in self._callbacks:
            callback(old_value, new_value)


class TemperatureSensor:
    """温度传感器"""

    def __init__(self):
        self.temperature = ObservableProperty(20.0)

    def set_temperature(self, value: float):
        self.temperature.value = value


# 使用
print("\n=== Observable Property ===")

sensor = TemperatureSensor()

def on_temperature_change(old, new):
    print(f"Temperature changed: {old}°C -> {new}°C")

def alert_on_high_temp(old, new):
    if new > 30:
        print(f"⚠️  ALERT: High temperature! {new}°C")

sensor.temperature.add_callback(on_temperature_change)
sensor.temperature.add_callback(alert_on_high_temp)

sensor.set_temperature(25)
sensor.set_temperature(35)


# ============ 使用事件系统 ============

class Event:
    """事件类"""

    def __init__(self):
        self._handlers = []

    def subscribe(self, handler):
        self._handlers.append(handler)
        return self

    def unsubscribe(self, handler):
        self._handlers.remove(handler)

    def emit(self, *args, **kwargs):
        for handler in self._handlers:
            handler(*args, **kwargs)


class Button:
    """按钮 - 使用事件"""

    def __init__(self, name: str):
        self.name = name
        self.on_click = Event()
        self.on_hover = Event()

    def click(self):
        print(f"Button '{self.name}' clicked")
        self.on_click.emit(self)

    def hover(self):
        self.on_hover.emit(self)


# 使用
print("\n=== Event System ===")

button = Button("Submit")

button.on_click.subscribe(lambda btn: print(f"  Handler 1: {btn.name} clicked"))
button.on_click.subscribe(lambda btn: print(f"  Handler 2: Processing {btn.name}"))

button.click()
```

#### 反例：紧耦合通知

```python
# ❌ 错误：紧耦合的通知
class BadPublisher:
    def __init__(self):
        self.subscriber1 = None
        self.subscriber2 = None

    def notify(self):
        if self.subscriber1:
            self.subscriber1.update()  # 直接依赖具体类
        if self.subscriber2:
            self.subscriber2.update()

# 问题：
# 1. 紧耦合
# 2. 难以扩展
# 3. 违反开闭原则

# ✅ 正确：使用观察者模式解耦
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 松耦合 | 可能导致循环依赖 |
| 支持广播 | 通知顺序不确定 |
| 符合开闭原则 | 内存泄漏风险 |

---

### 3.8 状态模式（State）

#### 意图

允许对象在内部状态改变时改变它的行为。

#### 适用场景

- 对象行为依赖于状态
- 需要大量条件语句处理状态
- 状态转换复杂

#### Python实现

```python
from abc import ABC, abstractmethod
from enum import Enum, auto


# ============ 状态接口 ============

class OrderState(ABC):
    """订单状态接口"""

    def __init__(self, order: 'Order'):
        self.order = order

    @abstractmethod
    def pay(self) -> None:
        pass

    @abstractmethod
    def ship(self) -> None:
        pass

    @abstractmethod
    def deliver(self) -> None:
        pass

    @abstractmethod
    def cancel(self) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


# ============ 具体状态 ============

class PendingState(OrderState):
    """待支付状态"""

    def pay(self) -> None:
        print("Processing payment...")
        self.order.set_state(PaidState(self.order))

    def ship(self) -> None:
        print("Cannot ship: Order not paid yet")

    def deliver(self) -> None:
        print("Cannot deliver: Order not shipped yet")

    def cancel(self) -> None:
        print("Cancelling order...")
        self.order.set_state(CancelledState(self.order))

    def get_name(self) -> str:
        return "Pending"


class PaidState(OrderState):
    """已支付状态"""

    def pay(self) -> None:
        print("Order already paid")

    def ship(self) -> None:
        print("Shipping order...")
        self.order.set_state(ShippedState(self.order))

    def deliver(self) -> None:
        print("Cannot deliver: Order not shipped yet")

    def cancel(self) -> None:
        print("Processing refund...")
        self.order.set_state(CancelledState(self.order))

    def get_name(self) -> str:
        return "Paid"


class ShippedState(OrderState):
    """已发货状态"""

    def pay(self) -> None:
        print("Order already paid")

    def ship(self) -> None:
        print("Order already shipped")

    def deliver(self) -> None:
        print("Delivering order...")
        self.order.set_state(DeliveredState(self.order))

    def cancel(self) -> None:
        print("Cannot cancel: Order already shipped")

    def get_name(self) -> str:
        return "Shipped"


class DeliveredState(OrderState):
    """已送达状态"""

    def pay(self) -> None:
        print("Order already paid")

    def ship(self) -> None:
        print("Order already shipped")

    def deliver(self) -> None:
        print("Order already delivered")

    def cancel(self) -> None:
        print("Cannot cancel: Order already delivered")

    def get_name(self) -> str:
        return "Delivered"


class CancelledState(OrderState):
    """已取消状态"""

    def pay(self) -> None:
        print("Cannot pay: Order cancelled")

    def ship(self) -> None:
        print("Cannot ship: Order cancelled")

    def deliver(self) -> None:
        print("Cannot deliver: Order cancelled")

    def cancel(self) -> None:
        print("Order already cancelled")

    def get_name(self) -> str:
        return "Cancelled"


# ============ 上下文 ============

class Order:
    """订单 - 上下文"""

    def __init__(self, order_id: str):
        self.order_id = order_id
        self._state: OrderState = PendingState(self)

    def set_state(self, state: OrderState) -> None:
        """设置状态（状态类调用）"""
        old_state = self._state.get_name()
        self._state = state
        print(f"  State changed: {old_state} -> {state.get_name()}")

    def pay(self) -> None:
        print(f"\n[Order {self.order_id}] Attempting to pay...")
        self._state.pay()

    def ship(self) -> None:
        print(f"\n[Order {self.order_id}] Attempting to ship...")
        self._state.ship()

    def deliver(self) -> None:
        print(f"\n[Order {self.order_id}] Attempting to deliver...")
        self._state.deliver()

    def cancel(self) -> None:
        print(f"\n[Order {self.order_id}] Attempting to cancel...")
        self._state.cancel()

    def get_status(self) -> str:
        return self._state.get_name()


# ============ 使用示例 ============

print("=== State Pattern ===")

order = Order("ORD-12345")
print(f"Initial status: {order.get_status()}")

# 正常流程
order.pay()
order.ship()
order.deliver()

# 尝试无效操作
print("\n--- Invalid operations ---")
order.pay()  # 已支付
order.cancel()  # 已送达，不能取消

# 取消流程
print("\n--- Cancellation flow ---")
order2 = Order("ORD-67890")
order2.pay()
order2.cancel()
order2.ship()  # 已取消，不能发货
```

#### 正例：游戏角色状态

```python
class CharacterState(ABC):
    """角色状态"""

    def __init__(self, character: 'GameCharacter'):
        self.character = character

    @abstractmethod
    def move(self) -> None:
        pass

    @abstractmethod
    def attack(self) -> None:
        pass

    @abstractmethod
    def take_damage(self, damage: int) -> None:
        pass


class NormalState(CharacterState):
    """正常状态"""

    def move(self) -> None:
        print(f"{self.character.name} moves normally")

    def attack(self) -> None:
        damage = self.character.base_damage
        print(f"{self.character.name} attacks for {damage} damage")

    def take_damage(self, damage: int) -> None:
        self.character.health -= damage
        print(f"{self.character.name} takes {damage} damage")
        if self.character.health <= 0:
            self.character.set_state(DeadState(self.character))
        elif self.character.health < 30:
            self.character.set_state(WoundedState(self.character))


class WoundedState(CharacterState):
    """受伤状态"""

    def move(self) -> None:
        print(f"{self.character.name} moves slowly (wounded)")

    def attack(self) -> None:
        damage = self.character.base_damage * 0.5
        print(f"{self.character.name} weakly attacks for {damage} damage")

    def take_damage(self, damage: int) -> None:
        self.character.health -= damage * 1.5  # 受伤时受到更多伤害
        print(f"{self.character.name} takes {damage * 1.5} damage (vulnerable)")
        if self.character.health <= 0:
            self.character.set_state(DeadState(self.character))


class DeadState(CharacterState):
    """死亡状态"""

    def move(self) -> None:
        print(f"{self.character.name} cannot move (dead)")

    def attack(self) -> None:
        print(f"{self.character.name} cannot attack (dead)")

    def take_damage(self, damage: int) -> None:
        print(f"{self.character.name} is already dead")


class GameCharacter:
    """游戏角色"""

    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.base_damage = 20
        self._state: CharacterState = NormalState(self)

    def set_state(self, state: CharacterState):
        self._state = state
        print(f"  >> {self.name} is now {state.__class__.__name__}")

    def move(self):
        self._state.move()

    def attack(self):
        self._state.attack()

    def take_damage(self, damage: int):
        self._state.take_damage(damage)


# 使用
print("\n=== Character State ===")

hero = GameCharacter("Hero")
hero.move()
hero.attack()

hero.take_damage(40)  # 健康
hero.move()

hero.take_damage(35)  # 受伤
hero.move()
hero.attack()

hero.take_damage(50)  # 死亡
hero.move()
hero.attack()
```

#### 反例：巨型条件语句

```python
# ❌ 错误：使用大量条件语句
class BadOrder:
    def pay(self):
        if self.state == "pending":
            self.state = "paid"
        elif self.state == "paid":
            print("Already paid")
        elif self.state == "shipped":
            print("Cannot pay")
        # ... 更多条件

# 问题：
# 1. 代码复杂
# 2. 难以维护
# 3. 违反开闭原则

# ✅ 正确：使用状态模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 消除条件语句 | 类数量增加 |
| 状态转换明确 | 可能状态过多 |
| 易于扩展 | |

---

### 3.9 策略模式（Strategy）

#### 意图

定义一系列算法，把它们一个个封装起来，并且使它们可以互相替换。

#### 适用场景

- 多种算法解决同一问题
- 需要动态选择算法
- 避免大量条件语句

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass


# ============ 策略接口 ============

class SortStrategy(ABC):
    """排序策略接口"""

    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


# ============ 具体策略 ============

class BubbleSortStrategy(SortStrategy):
    """冒泡排序"""

    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def get_name(self) -> str:
        return "Bubble Sort"


class QuickSortStrategy(SortStrategy):
    """快速排序"""

    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        self._quick_sort(arr, 0, len(arr) - 1)
        return arr

    def _quick_sort(self, arr: List[int], low: int, high: int) -> None:
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick_sort(arr, low, pi - 1)
            self._quick_sort(arr, pi + 1, high)

    def _partition(self, arr: List[int], low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def get_name(self) -> str:
        return "Quick Sort"


class MergeSortStrategy(SortStrategy):
    """归并排序"""

    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data.copy()
        return self._merge_sort(data.copy())

    def _merge_sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])

        return self._merge(left, right)

    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def get_name(self) -> str:
        return "Merge Sort"


# ============ 上下文 ============

class Sorter:
    """排序器 - 上下文"""

    def __init__(self, strategy: SortStrategy = None):
        self._strategy = strategy or QuickSortStrategy()

    def set_strategy(self, strategy: SortStrategy) -> None:
        """动态切换策略"""
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        """使用当前策略排序"""
        print(f"Using {self._strategy.get_name()}")
        return self._strategy.sort(data)


# ============ 使用示例 ============

print("=== Strategy Pattern ===")

data = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {data}")

sorter = Sorter()

# 使用快速排序
sorter.set_strategy(QuickSortStrategy())
result = sorter.sort(data)
print(f"Result: {result}\n")

# 切换到归并排序
sorter.set_strategy(MergeSortStrategy())
result = sorter.sort(data)
print(f"Result: {result}\n")

# 切换到冒泡排序
sorter.set_strategy(BubbleSortStrategy())
result = sorter.sort(data)
print(f"Result: {result}")
```

#### 正例：支付策略

```python
class PaymentStrategy(ABC):
    """支付策略"""

    @abstractmethod
    def pay(self, amount: float) -> dict:
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass


class CreditCardStrategy(PaymentStrategy):
    """信用卡支付"""

    def __init__(self, card_number: str, cvv: str, expiry: str):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def validate(self) -> bool:
        return len(self.card_number) == 16 and len(self.cvv) == 3

    def pay(self, amount: float) -> dict:
        if not self.validate():
            return {"success": False, "error": "Invalid card"}

        print(f"Processing ${amount} via Credit Card ending in {self.card_number[-4:]}")
        return {
            "success": True,
            "method": "credit_card",
            "amount": amount,
            "transaction_id": "CC123456"
        }


class PayPalStrategy(PaymentStrategy):
    """PayPal支付"""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def validate(self) -> bool:
        return "@" in self.email

    def pay(self, amount: float) -> dict:
        if not self.validate():
            return {"success": False, "error": "Invalid email"}

        print(f"Processing ${amount} via PayPal ({self.email})")
        return {
            "success": True,
            "method": "paypal",
            "amount": amount,
            "transaction_id": "PP789012"
        }


class CryptoStrategy(PaymentStrategy):
    """加密货币支付"""

    def __init__(self, wallet_address: str, currency: str = "BTC"):
        self.wallet_address = wallet_address
        self.currency = currency

    def validate(self) -> bool:
        return len(self.wallet_address) > 20

    def pay(self, amount: float) -> dict:
        if not self.validate():
            return {"success": False, "error": "Invalid wallet"}

        print(f"Processing ${amount} via {self.currency} ({self.wallet_address[:10]}...)")
        return {
            "success": True,
            "method": "crypto",
            "currency": self.currency,
            "amount": amount,
            "transaction_id": "CR345678"
        }


class ShoppingCart:
    """购物车"""

    def __init__(self):
        self.items = []
        self._payment_strategy = None

    def add_item(self, name: str, price: float):
        self.items.append({"name": name, "price": price})

    def get_total(self) -> float:
        return sum(item["price"] for item in self.items)

    def set_payment_strategy(self, strategy: PaymentStrategy):
        self._payment_strategy = strategy

    def checkout(self) -> dict:
        if not self._payment_strategy:
            return {"success": False, "error": "No payment method selected"}

        total = self.get_total()
        return self._payment_strategy.pay(total)


# 使用
print("\n=== Payment Strategy ===")

cart = ShoppingCart()
cart.add_item("Laptop", 999.99)
cart.add_item("Mouse", 29.99)

print(f"Total: ${cart.get_total()}")

# 使用信用卡支付
cart.set_payment_strategy(CreditCardStrategy("1234567890123456", "123", "12/25"))
result = cart.checkout()
print(f"Result: {result}\n")

# 切换到PayPal
cart.set_payment_strategy(PayPalStrategy("user@example.com", "password"))
result = cart.checkout()
print(f"Result: {result}")
```

#### Pythonic实现：使用函数

```python
# Python中可以用函数代替策略类

# 策略函数
def bubble_sort(data: List[int]) -> List[int]:
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(data: List[int]) -> List[int]:
    if len(data) <= 1:
        return data.copy()

    pivot = data[len(data) // 2]
    left = [x for x in data if x < pivot]
    middle = [x for x in data if x == pivot]
    right = [x for x in data if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


class FunctionalSorter:
    """函数式排序器"""

    def __init__(self, strategy=None):
        self._strategy = strategy or quick_sort

    def set_strategy(self, strategy):
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        return self._strategy(data)


# 使用
print("\n=== Functional Strategy ===")

sorter = FunctionalSorter()
print(f"Quick: {sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])}")

sorter.set_strategy(bubble_sort)
print(f"Bubble: {sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])}")

# 使用lambda
sorter.set_strategy(lambda d: sorted(d, reverse=True))
print(f"Reverse: {sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])}")
```

#### 反例：条件选择算法

```python
# ❌ 错误：使用条件语句选择算法
def bad_sort(data, algorithm):
    if algorithm == "bubble":
        # 冒泡排序实现
        pass
    elif algorithm == "quick":
        # 快速排序实现
        pass
    elif algorithm == "merge":
        # 归并排序实现
        pass

# 问题：
# 1. 违反开闭原则
# 2. 难以扩展
# 3. 代码重复

# ✅ 正确：使用策略模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 消除条件语句 | 客户端需要了解策略 |
| 易于扩展 | 类数量增加 |
| 运行时切换 | |

---

### 3.10 模板方法模式（Template Method）

#### 意图

定义一个操作中的算法骨架，将一些步骤延迟到子类中实现。

#### 适用场景

- 算法有固定步骤
- 需要复用算法结构
- 需要钩子方法

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import List


# ============ 抽象类 ============

class DataMiner(ABC):
    """数据挖掘器 - 抽象类"""

    def mine(self, path: str) -> dict:
        """
        模板方法 - 定义算法骨架
        """
        file = self._open_file(path)
        raw_data = self._extract_data(file)
        data = self._parse_data(raw_data)
        analysis = self._analyze_data(data)
        self._send_report(analysis)
        self._close_file(file)
        return analysis

    # 抽象方法 - 子类必须实现
    @abstractmethod
    def _open_file(self, path: str):
        pass

    @abstractmethod
    def _extract_data(self, file):
        pass

    @abstractmethod
    def _parse_data(self, raw_data: str) -> List[dict]:
        pass

    # 具体方法 - 默认实现
    def _analyze_data(self, data: List[dict]) -> dict:
        """分析数据 - 可有默认实现"""
        print("Analyzing data...")
        return {
            "count": len(data),
            "summary": f"Processed {len(data)} records"
        }

    def _send_report(self, analysis: dict) -> None:
        """发送报告 - 钩子方法"""
        print(f"Report: {analysis}")

    def _close_file(self, file) -> None:
        """关闭文件 - 可有默认实现"""
        print("Closing file")


# ============ 具体类 ============

class PDFDataMiner(DataMiner):
    """PDF数据挖掘器"""

    def _open_file(self, path: str):
        print(f"Opening PDF: {path}")
        return {"type": "pdf", "path": path}

    def _extract_data(self, file):
        print("Extracting text from PDF...")
        return "PDF raw data"

    def _parse_data(self, raw_data: str) -> List[dict]:
        print("Parsing PDF data...")
        return [{"type": "pdf_record", "content": raw_data}]


class CSVDataMiner(DataMiner):
    """CSV数据挖掘器"""

    def _open_file(self, path: str):
        print(f"Opening CSV: {path}")
        return {"type": "csv", "path": path}

    def _extract_data(self, file):
        print("Reading CSV rows...")
        return "col1,col2,col3\n1,2,3\n4,5,6"

    def _parse_data(self, raw_data: str) -> List[dict]:
        print("Parsing CSV data...")
        lines = raw_data.strip().split("\n")
        headers = lines[0].split(",")
        records = []
        for line in lines[1:]:
            values = line.split(",")
            records.append(dict(zip(headers, values)))
        return records

    def _analyze_data(self, data: List[dict]) -> dict:
        """自定义分析"""
        print("Custom CSV analysis...")
        return {
            "count": len(data),
            "columns": list(data[0].keys()) if data else [],
            "summary": f"CSV with {len(data)} rows"
        }


class DatabaseDataMiner(DataMiner):
    """数据库数据挖掘器"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def _open_file(self, path: str):
        print(f"Connecting to database: {self.connection_string}")
        return {"type": "db", "connection": self.connection_string}

    def _extract_data(self, file):
        print(f"Executing query: {file['connection']}")
        return "DB query results"

    def _parse_data(self, raw_data: str) -> List[dict]:
        print("Parsing database results...")
        return [{"type": "db_record", "data": raw_data}]

    def _send_report(self, analysis: dict) -> None:
        """自定义报告 - 钩子"""
        print(f"[Database Report] {analysis}")
        print("  Sending to DBA team...")


# ============ 使用示例 ============

print("=== Template Method Pattern ===")

print("\n--- PDF Mining ---")
pdf_miner = PDFDataMiner()
pdf_miner.mine("document.pdf")

print("\n--- CSV Mining ---")
csv_miner = CSVDataMiner()
csv_miner.mine("data.csv")

print("\n--- Database Mining ---")
db_miner = DatabaseDataMiner("postgresql://localhost/db")
db_miner.mine("SELECT * FROM users")
```

#### 正例：测试框架

```python
class TestCase(ABC):
    """测试用例基类"""

    def run(self) -> dict:
        """测试模板方法"""
        result = {"name": self.__class__.__name__, "passed": False}

        try:
            self.setUp()
            self.execute()
            result["passed"] = True
        except AssertionError as e:
            result["error"] = str(e)
        except Exception as e:
            result["error"] = f"Unexpected: {e}"
        finally:
            self.tearDown()

        return result

    def setUp(self) -> None:
        """测试前准备 - 钩子"""
        pass

    @abstractmethod
    def execute(self) -> None:
        """执行测试 - 必须实现"""
        pass

    def tearDown(self) -> None:
        """测试后清理 - 钩子"""
        pass

    def assertEqual(self, a, b):
        if a != b:
            raise AssertionError(f"{a} != {b}")

    def assertTrue(self, condition):
        if not condition:
            raise AssertionError("Expected True, got False")


class UserServiceTest(TestCase):
    """用户服务测试"""

    def setUp(self):
        print("  Setting up test database...")
        self.users = []

    def execute(self):
        print("  Running tests...")
        # 测试创建用户
        self.users.append({"id": 1, "name": "John"})
        self.assertEqual(len(self.users), 1)

        # 测试查找用户
        user = next((u for u in self.users if u["id"] == 1), None)
        self.assertTrue(user is not None)
        self.assertEqual(user["name"], "John")

    def tearDown(self):
        print("  Cleaning up...")
        self.users.clear()


class CalculatorTest(TestCase):
    """计算器测试"""

    def execute(self):
        print("  Testing calculator...")
        self.assertEqual(2 + 2, 4)
        self.assertEqual(10 - 5, 5)
        self.assertTrue(5 > 3)


# 运行测试
print("\n=== Test Framework ===")

tests = [UserServiceTest(), CalculatorTest()]
for test in tests:
    result = test.run()
    status = "✓ PASS" if result["passed"] else "✗ FAIL"
    print(f"{status}: {result['name']}")
    if "error" in result:
        print(f"  Error: {result['error']}")
```

#### 反例：重复代码

```python
# ❌ 错误：重复的算法结构
class PDFMiner:
    def mine(self, path):
        file = self.open_pdf(path)
        data = self.extract(file)
        analysis = self.analyze(data)
        self.report(analysis)
        self.close(file)

class CSVMinder:
    def mine(self, path):
        file = self.open_csv(path)
        data = self.extract(file)
        analysis = self.analyze(data)
        self.report(analysis)
        self.close(file)

# 问题：
# 1. 重复代码
# 2. 难以维护
# 3. 算法改变需要多处修改

# ✅ 正确：使用模板方法模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 复用算法结构 | 子类可能过多 |
| 易于扩展 | 限制灵活性 |
| 钩子方法提供扩展点 | |

---

### 3.11 访问者模式（Visitor）

#### 意图

表示一个作用于某对象结构中的各元素的操作，使你可以在不改变各元素类的前提下定义新操作。

#### 适用场景

- 需要对对象结构执行多种操作
- 类层次结构稳定但操作经常变化
- 需要分离操作与对象结构

#### Python实现

```python
from abc import ABC, abstractmethod
from typing import List


# ============ 元素接口 ============

class Shape(ABC):
    """形状接口"""

    @abstractmethod
    def accept(self, visitor: 'ShapeVisitor') -> None:
        pass


# ============ 具体元素 ============

class Circle(Shape):
    """圆形"""

    def __init__(self, radius: float, x: float = 0, y: float = 0):
        self.radius = radius
        self.x = x
        self.y = y

    def accept(self, visitor: 'ShapeVisitor') -> None:
        visitor.visit_circle(self)


class Rectangle(Shape):
    """矩形"""

    def __init__(self, width: float, height: float, x: float = 0, y: float = 0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def accept(self, visitor: 'ShapeVisitor') -> None:
        visitor.visit_rectangle(self)


class Triangle(Shape):
    """三角形"""

    def __init__(self, base: float, height: float, x: float = 0, y: float = 0):
        self.base = base
        self.height = height
        self.x = x
        self.y = y

    def accept(self, visitor: 'ShapeVisitor') -> None:
        visitor.visit_triangle(self)


# ============ 访问者接口 ============

class ShapeVisitor(ABC):
    """形状访问者"""

    @abstractmethod
    def visit_circle(self, circle: Circle) -> None:
        pass

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> None:
        pass

    @abstractmethod
    def visit_triangle(self, triangle: Triangle) -> None:
        pass


# ============ 具体访问者 ============

class AreaCalculator(ShapeVisitor):
    """面积计算器"""

    def __init__(self):
        self.total_area = 0.0
        self.areas = []

    def visit_circle(self, circle: Circle) -> None:
        import math
        area = math.pi * circle.radius ** 2
        self.areas.append(("Circle", area))
        self.total_area += area

    def visit_rectangle(self, rectangle: Rectangle) -> None:
        area = rectangle.width * rectangle.height
        self.areas.append(("Rectangle", area))
        self.total_area += area

    def visit_triangle(self, triangle: Triangle) -> None:
        area = 0.5 * triangle.base * triangle.height
        self.areas.append(("Triangle", area))
        self.total_area += area


class PerimeterCalculator(ShapeVisitor):
    """周长计算器"""

    def __init__(self):
        self.total_perimeter = 0.0
        self.perimeters = []

    def visit_circle(self, circle: Circle) -> None:
        import math
        perimeter = 2 * math.pi * circle.radius
        self.perimeters.append(("Circle", perimeter))
        self.total_perimeter += perimeter

    def visit_rectangle(self, rectangle: Rectangle) -> None:
        perimeter = 2 * (rectangle.width + rectangle.height)
        self.perimeters.append(("Rectangle", perimeter))
        self.total_perimeter += perimeter

    def visit_triangle(self, triangle: Triangle) -> None:
        # 简化计算（假设等腰三角形）
        side = ((triangle.base / 2) ** 2 + triangle.height ** 2) ** 0.5
        perimeter = triangle.base + 2 * side
        self.perimeters.append(("Triangle", perimeter))
        self.total_perimeter += perimeter


class XMLExporter(ShapeVisitor):
    """XML导出器"""

    def __init__(self):
        self.xml = ["<shapes>"]

    def visit_circle(self, circle: Circle) -> None:
        self.xml.append(f'  <circle x="{circle.x}" y="{circle.y}" r="{circle.radius}"/>')

    def visit_rectangle(self, rectangle: Rectangle) -> None:
        self.xml.append(f'  <rectangle x="{rectangle.x}" y="{rectangle.y}" '
                       f'w="{rectangle.width}" h="{rectangle.height}"/>')

    def visit_triangle(self, triangle: Triangle) -> None:
        self.xml.append(f'  <triangle x="{triangle.x}" y="{triangle.y}" '
                       f'base="{triangle.base}" h="{triangle.height}"/>')

    def get_xml(self) -> str:
        return "\n".join(self.xml) + "\n</shapes>"


class Renderer(ShapeVisitor):
    """渲染器"""

    def __init__(self):
        self.rendered = []

    def visit_circle(self, circle: Circle) -> None:
        self.rendered.append(f"Drawing circle at ({circle.x}, {circle.y}) "
                            f"with radius {circle.radius}")

    def visit_rectangle(self, rectangle: Rectangle) -> None:
        self.rendered.append(f"Drawing rectangle at ({rectangle.x}, {rectangle.y}) "
                            f"size {rectangle.width}x{rectangle.height}")

    def visit_triangle(self, triangle: Triangle) -> None:
        self.rendered.append(f"Drawing triangle at ({triangle.x}, {triangle.y}) "
                            f"base {triangle.base} height {triangle.height}")


# ============ 对象结构 ============

class Drawing:
    """绘图 - 对象结构"""

    def __init__(self):
        self.shapes: List[Shape] = []

    def add(self, shape: Shape) -> 'Drawing':
        self.shapes.append(shape)
        return self

    def accept(self, visitor: ShapeVisitor) -> None:
        """接受访问者"""
        for shape in self.shapes:
            shape.accept(visitor)


# ============ 使用示例 ============

print("=== Visitor Pattern ===")

drawing = Drawing()
drawing.add(Circle(5, 0, 0))
drawing.add(Rectangle(10, 20, 5, 5))
drawing.add(Triangle(8, 12, 10, 10))
drawing.add(Circle(3, 15, 15))

print("\n--- Area Calculation ---")
area_calc = AreaCalculator()
drawing.accept(area_calc)
for shape, area in area_calc.areas:
    print(f"  {shape}: {area:.2f}")
print(f"  Total: {area_calc.total_area:.2f}")

print("\n--- Perimeter Calculation ---")
perimeter_calc = PerimeterCalculator()
drawing.accept(perimeter_calc)
for shape, perimeter in perimeter_calc.perimeters:
    print(f"  {shape}: {perimeter:.2f}")
print(f"  Total: {perimeter_calc.total_perimeter:.2f}")

print("\n--- XML Export ---")
xml_exporter = XMLExporter()
drawing.accept(xml_exporter)
print(xml_exporter.get_xml())

print("--- Rendering ---")
renderer = Renderer()
drawing.accept(renderer)
for line in renderer.rendered:
    print(f"  {line}")
```

#### 正例：AST遍历

```python
class ASTNode(ABC):
    """AST节点"""

    @abstractmethod
    def accept(self, visitor: 'ASTVisitor'):
        pass


class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_number(self)


class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_binary_op(self)


class ASTVisitor(ABC):
    """AST访问者"""

    @abstractmethod
    def visit_number(self, node: NumberNode):
        pass

    @abstractmethod
    def visit_binary_op(self, node: BinaryOpNode):
        pass


class Evaluator(ASTVisitor):
    """求值器"""

    def visit_number(self, node: NumberNode):
        return node.value

    def visit_binary_op(self, node: BinaryOpNode):
        left = node.left.accept(self)
        right = node.right.accept(self)

        if node.op == "+":
            return left + right
        elif node.op == "-":
            return left - right
        elif node.op == "*":
            return left * right
        elif node.op == "/":
            return left / right


class Printer(ASTVisitor):
    """打印器"""

    def visit_number(self, node: NumberNode):
        return str(node.value)

    def visit_binary_op(self, node: BinaryOpNode):
        left = node.left.accept(self)
        right = node.right.accept(self)
        return f"({left} {node.op} {right})"


# 使用
print("\n=== AST Visitor ===")

# 构建AST: (1 + 2) * 3
ast = BinaryOpNode(
    BinaryOpNode(NumberNode(1), "+", NumberNode(2)),
    "*",
    NumberNode(3)
)

evaluator = Evaluator()
result = ast.accept(evaluator)
print(f"Result: {result}")

printer = Printer()
expression = ast.accept(printer)
print(f"Expression: {expression}")
```

#### 反例：违反开闭原则

```python
# ❌ 错误：在元素类中添加新操作
class BadShape:
    def calculate_area(self): pass
    def calculate_perimeter(self): pass
    def export_xml(self): pass
    def render(self): pass
    # 每增加操作都需要修改所有类

# 问题：
# 1. 违反开闭原则
# 2. 类变得臃肿
# 3. 难以维护

# ✅ 正确：使用访问者模式
```

#### 优缺点分析

| 优点 | 缺点 |
|------|------|
| 易于添加新操作 | 难以添加新元素 |
| 集中相关操作 | 破坏封装 |
| 符合单一职责 | 代码复杂 |

---

## 第四部分：Pythonic设计模式变体

Python的动态特性和语法糖提供了一些独特的模式实现方式。

---

### 4.1 Borg模式（单例变体）

#### 意图

让所有实例共享相同的状态，而非相同的身份。

#### 与单例模式的区别

- **单例模式**：所有实例是同一个对象（`is`判断为True）
- **Borg模式**：所有实例是不同的对象，但共享状态

#### Python实现

```python
# ============ Borg模式 ============

class Borg:
    """Borg模式 - 共享状态"""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class AppConfig(Borg):
    """应用配置 - Borg实现"""

    def __init__(self):
        super().__init__()
        # 只在第一次初始化时设置默认值
        if not hasattr(self, '_initialized'):
            self.database_url = "localhost"
            self.debug_mode = False
            self.max_connections = 10
            self._initialized = True

    def set(self, key: str, value):
        setattr(self, key, value)

    def get(self, key: str, default=None):
        return getattr(self, key, default)


# 测试Borg模式
print("=== Borg Pattern ===")

config1 = AppConfig()
config2 = AppConfig()

print(f"Same object? {config1 is config2}")  # False
print(f"Same state? {config1.__dict__ is config2.__dict__}")  # True

config1.database_url = "postgresql://prod-server/db"
print(f"Config2 sees: {config2.database_url}")  # 共享状态

# 可以添加新属性
config1.new_setting = "value"
print(f"Config2 has new_setting: {config2.new_setting}")


# ============ 对比：单例模式 ============

class Singleton:
    """传统单例"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


print("\n=== Singleton vs Borg ===")

s1 = Singleton()
s2 = Singleton()
print(f"Singleton same object? {s1 is s2}")  # True

b1 = Borg()
b2 = Borg()
print(f"Borg same object? {b1 is b2}")  # False
print(f"Borg same state? {b1.__dict__ is b2.__dict__}")  # True


# ============ 使用场景对比 ============

print("""
=== 选择建议 ===

使用单例模式：
- 需要严格的唯一实例（如数据库连接池）
- 需要重写 __eq__ 等魔术方法
- 实例身份很重要

使用Borg模式：
- 只需要共享状态
- 希望实例可以独立垃圾回收
- 继承关系复杂时
- 需要多个"单例"类共享相同模式
""")
```

---

### 4.2 注册表模式

#### 意图

提供一个中心化的注册机制，用于管理和查找组件。

#### Python实现

```python
from typing import Dict, Type, Callable, Any
from functools import wraps


# ============ 基础注册表 ============

class PluginRegistry:
    """插件注册表"""

    _plugins: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: str):
        """注册装饰器"""
        def decorator(plugin_class: Type) -> Type:
            cls._plugins[name] = plugin_class
            plugin_class._plugin_name = name
            return plugin_class
        return decorator

    @classmethod
    def get(cls, name: str) -> Type:
        if name not in cls._plugins:
            raise ValueError(f"Plugin '{name}' not found")
        return cls._plugins[name]

    @classmethod
    def create(cls, name: str, *args, **kwargs) -> Any:
        """创建插件实例"""
        plugin_class = cls.get(name)
        return plugin_class(*args, **kwargs)

    @classmethod
    def list_plugins(cls) -> list:
        return list(cls._plugins.keys())

    @classmethod
    def unregister(cls, name: str) -> None:
        if name in cls._plugins:
            del cls._plugins[name]


# 使用注册表
@PluginRegistry.register("email")
class EmailNotifier:
    def __init__(self, config: dict = None):
        self.config = config or {}

    def send(self, message: str, recipient: str):
        print(f"[Email] To {recipient}: {message}")


@PluginRegistry.register("sms")
class SMSNotifier:
    def __init__(self, config: dict = None):
        self.config = config or {}

    def send(self, message: str, recipient: str):
        print(f"[SMS] To {recipient}: {message[:20]}...")


@PluginRegistry.register("push")
class PushNotifier:
    def __init__(self, config: dict = None):
        self.config = config or {}

    def send(self, message: str, recipient: str):
        print(f"[Push] To device {recipient}: {message}")


# 测试注册表
print("=== Registry Pattern ===")

print(f"Registered plugins: {PluginRegistry.list_plugins()}")

# 动态创建
email_notifier = PluginRegistry.create("email", {"smtp": "smtp.example.com"})
email_notifier.send("Hello!", "user@example.com")

sms_notifier = PluginRegistry.create("sms", {"provider": "twilio"})
sms_notifier.send("Hello World!", "+1234567890")


# ============ 函数注册表 ============

class CommandRegistry:
    """命令注册表"""

    _commands: Dict[str, Callable] = {}

    @classmethod
    def command(cls, name: str):
        """命令装饰器"""
        def decorator(func: Callable) -> Callable:
            cls._commands[name] = func
            func._command_name = name
            return func
        return decorator

    @classmethod
    def execute(cls, name: str, *args, **kwargs):
        if name not in cls._commands:
            raise ValueError(f"Command '{name}' not found")
        return cls._commands[name](*args, **kwargs)

    @classmethod
    def list_commands(cls) -> list:
        return list(cls._commands.keys())


# 注册命令
@CommandRegistry.command("greet")
def greet_command(name: str):
    return f"Hello, {name}!"

@CommandRegistry.command("add")
def add_command(a: int, b: int):
    return a + b

@CommandRegistry.command("help")
def help_command():
    return f"Available commands: {CommandRegistry.list_commands()}"


print("\n=== Command Registry ===")
print(CommandRegistry.execute("greet", "World"))
print(CommandRegistry.execute("add", 5, 3))
print(CommandRegistry.execute("help"))


# ============ 序列化注册表 ============

class SerializerRegistry:
    """序列化器注册表"""

    _serializers: Dict[str, Callable[[Any], str]] = {}
    _deserializers: Dict[str, Callable[[str], Any]] = {}

    @classmethod
    def register(cls, format: str):
        def decorator(func_pair: tuple):
            serializer, deserializer = func_pair
            cls._serializers[format] = serializer
            cls._deserializers[format] = deserializer
            return func_pair
        return decorator

    @classmethod
    def serialize(cls, format: str, data: Any) -> str:
        if format not in cls._serializers:
            raise ValueError(f"Format '{format}' not supported")
        return cls._serializers[format](data)

    @classmethod
    def deserialize(cls, format: str, data: str) -> Any:
        if format not in cls._deserializers:
            raise ValueError(f"Format '{format}' not supported")
        return cls._deserializers[format](data)


import json

@SerializerRegistry.register("json")
def json_handlers():
    return (json.dumps, json.loads)


@SerializerRegistry.register("yaml")
def yaml_handlers():
    # 模拟YAML处理
    def yaml_dump(data):
        return f"yaml: {data}"
    def yaml_load(data):
        return data.replace("yaml: ", "")
    return (yaml_dump, yaml_load)


print("\n=== Serializer Registry ===")
data = {"name": "John", "age": 30}
print(f"JSON: {SerializerRegistry.serialize('json', data)}")
```

---

### 4.3 混入模式（Mixin）

#### 意图

通过多重继承为类提供可选功能，而不需要深度继承层次。

#### Python实现

```python
import json
from datetime import datetime
from typing import Dict, Any


# ============ Mixin基类 ============

class JSONSerializableMixin:
    """JSON序列化Mixin"""

    def to_json(self) -> str:
        """转换为JSON"""
        return json.dumps(self.to_dict(), default=str, indent=2)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 - 子类可覆盖"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

    @classmethod
    def from_json(cls, json_str: str) -> 'JSONSerializableMixin':
        """从JSON创建"""
        data = json.loads(json_str)
        return cls(**data)


class ComparableMixin:
    """可比较Mixin"""

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._compare_key() == other._compare_key()

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._compare_key() < other._compare_key()

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def _compare_key(self):
        """返回比较键 - 子类必须实现"""
        raise NotImplementedError


class TimestampMixin:
    """时间戳Mixin"""

    def __init__(self, *args, **kwargs):
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        super().__init__(*args, **kwargs)

    def touch(self):
        """更新时间戳"""
        self.updated_at = datetime.now()


class LoggerMixin:
    """日志Mixin"""

    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] [{level}] {self.__class__.__name__}: {message}")

    def log_debug(self, message: str):
        self.log(message, "DEBUG")

    def log_error(self, message: str):
        self.log(message, "ERROR")


# ============ 使用Mixin的类 ============

class User(JSONSerializableMixin, ComparableMixin, TimestampMixin, LoggerMixin):
    """用户类 - 使用多个Mixin"""

    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        super().__init__()  # 调用Mixin的__init__

    def _compare_key(self):
        """实现ComparableMixin的要求"""
        return self.id

    def update_email(self, new_email: str):
        """更新邮箱"""
        old_email = self.email
        self.email = new_email
        self.touch()  # 来自TimestampMixin
        self.log(f"Email changed from {old_email} to {new_email}")  # 来自LoggerMixin


class Product(JSONSerializableMixin, ComparableMixin, LoggerMixin):
    """产品类"""

    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price
        super().__init__()

    def _compare_key(self):
        return self.sku

    def apply_discount(self, percent: float):
        old_price = self.price
        self.price *= (1 - percent / 100)
        self.log(f"Price changed from ${old_price} to ${self.price}")


# 测试Mixin
print("=== Mixin Pattern ===")

user1 = User(1, "Alice", "alice@example.com")
user2 = User(2, "Bob", "bob@example.com")

# ComparableMixin
print(f"user1 < user2: {user1 < user2}")

# TimestampMixin
print(f"Created at: {user1.created_at}")
user1.update_email("alice.new@example.com")
print(f"Updated at: {user1.updated_at}")

# JSONSerializableMixin
print(f"\nUser JSON:\n{user1.to_json()}")


# ============ 上下文管理器Mixin ============

class ContextManagerMixin:
    """上下文管理器Mixin"""

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.teardown()
        return False

    def setup(self):
        """设置 - 子类覆盖"""
        pass

    def teardown(self):
        """清理 - 子类覆盖"""
        pass


class DatabaseConnection(ContextManagerMixin, LoggerMixin):
    """数据库连接"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    def setup(self):
        self.log("Opening database connection...")
        self.connection = f"Connection to {self.connection_string}"

    def teardown(self):
        self.log("Closing database connection...")
        self.connection = None

    def execute(self, query: str):
        self.log(f"Executing: {query}")
        return f"Result of: {query}"


# 使用上下文管理器
print("\n=== Context Manager Mixin ===")
with DatabaseConnection("postgresql://localhost/db") as db:
    result = db.execute("SELECT * FROM users")
    print(f"Result: {result}")


# ============ 验证Mixin ============

class ValidatableMixin:
    """可验证Mixin"""

    _validators = {}

    @classmethod
    def add_validator(cls, field: str, validator: Callable):
        if field not in cls._validators:
            cls._validators[field] = []
        cls._validators[field].append(validator)

    def validate(self) -> Dict[str, list]:
        errors = {}
        for field, validators in self._validators.items():
            value = getattr(self, field, None)
            for validator in validators:
                error = validator(value)
                if error:
                    if field not in errors:
                        errors[field] = []
                    errors[field].append(error)
        return errors

    def is_valid(self) -> bool:
        return len(self.validate()) == 0


class Customer(ValidatableMixin, LoggerMixin):
    """客户类 - 带验证"""

    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age
        super().__init__()


# 添加验证器
Customer.add_validator("name", lambda v: "Name required" if not v else None)
Customer.add_validator("email", lambda v: "Invalid email" if v and "@" not in v else None)
Customer.add_validator("age", lambda v: "Age must be positive" if v and v < 0 else None)


print("\n=== Validation Mixin ===")
customer = Customer("", "invalid-email", -5)
errors = customer.validate()
print(f"Validation errors: {errors}")

customer2 = Customer("John", "john@example.com", 30)
print(f"Is valid: {customer2.is_valid()}")
```

---

## 第五部分：反模式

反模式是常见的、看似合理但实际上会导致问题的解决方案。

---

### 5.1 上帝对象（God Object）

#### 问题描述

一个类承担了过多的职责，知道太多、做太多。

#### 反例

```python
# ❌ 上帝对象 - 承担了太多职责
class GodApplication:
    """上帝对象 - 反模式"""

    def __init__(self):
        # 数据库
        self.db_connection = None
        self.db_config = {}

        # 用户管理
        self.users = []
        self.current_user = None

        # 订单管理
        self.orders = []
        self.order_counter = 0

        # 库存管理
        self.inventory = {}
        self.stock_alerts = []

        # 支付处理
        self.payment_gateway = None
        self.transactions = []

        # 邮件服务
        self.email_config = {}
        self.email_queue = []

        # 日志
        self.log_entries = []

        # 配置
        self.config = {}

        # 缓存
        self.cache = {}

    # 数据库方法
    def connect_db(self): pass
    def query_db(self, sql): pass
    def close_db(self): pass

    # 用户方法
    def create_user(self, data): pass
    def delete_user(self, user_id): pass
    def authenticate_user(self, credentials): pass
    def update_user_profile(self, user_id, data): pass

    # 订单方法
    def create_order(self, items): pass
    def cancel_order(self, order_id): pass
    def process_refund(self, order_id): pass
    def get_order_history(self, user_id): pass

    # 库存方法
    def check_stock(self, product_id): pass
    def update_stock(self, product_id, quantity): pass
    def reorder_product(self, product_id): pass

    # 支付方法
    def process_payment(self, order_id, amount): pass
    def verify_payment(self, transaction_id): pass
    def handle_chargeback(self, transaction_id): pass

    # 邮件方法
    def send_email(self, to, subject, body): pass
    def send_bulk_email(self, recipients, template): pass

    # 日志方法
    def log(self, message, level): pass
    def get_logs(self, filters): pass

    # 配置方法
    def load_config(self, path): pass
    def save_config(self): pass
    def get_config(self, key): pass

    # 缓存方法
    def cache_get(self, key): pass
    def cache_set(self, key, value, ttl): pass
    def cache_clear(self): pass


# 问题：
# 1. 违反单一职责原则
# 2. 难以测试
# 3. 难以维护
# 4. 难以团队协作
# 5. 代码重复风险
```

#### 正确设计

```python
# ✅ 正确：职责分离

class DatabaseService:
    """数据库服务"""
    def connect(self): pass
    def query(self, sql): pass
    def close(self): pass


class UserService:
    """用户服务"""
    def __init__(self, db: DatabaseService):
        self.db = db

    def create(self, data): pass
    def delete(self, user_id): pass
    def authenticate(self, credentials): pass


class OrderService:
    """订单服务"""
    def __init__(self, db: DatabaseService, payment: 'PaymentService'):
        self.db = db
        self.payment = payment

    def create(self, items): pass
    def cancel(self, order_id): pass


class PaymentService:
    """支付服务"""
    def process(self, order_id, amount): pass
    def verify(self, transaction_id): pass


class EmailService:
    """邮件服务"""
    def send(self, to, subject, body): pass


class ConfigService:
    """配置服务"""
    def get(self, key): pass
    def set(self, key, value): pass


class CacheService:
    """缓存服务"""
    def get(self, key): pass
    def set(self, key, value, ttl): pass


# 依赖注入组合
class Application:
    """应用程序 - 正确设计"""

    def __init__(self):
        self.config = ConfigService()
        self.cache = CacheService()
        self.db = DatabaseService()
        self.email = EmailService()
        self.payment = PaymentService()
        self.users = UserService(self.db)
        self.orders = OrderService(self.db, self.payment)
```

---

### 5.2 循环依赖

#### 问题描述

两个或多个模块相互依赖，形成循环。

#### 反例

```python
# ❌ 循环依赖 - module_a.py
# from module_b import B  # 循环导入

class A:
    def __init__(self):
        self.b = None  # 稍后设置

    def do_something(self):
        return self.b.help()


# ❌ 循环依赖 - module_b.py
# from module_a import A  # 循环导入

class B:
    def __init__(self):
        self.a = None  # 稍后设置

    def help(self):
        return "Help from B"

    def use_a(self):
        return self.a.do_something()


# 问题：
# 1. 导入错误
# 2. 难以测试
# 3. 难以理解
# 4. 构建困难
```

#### 解决方案

```python
# ✅ 方案1：依赖注入

# module_a.py
class A:
    def __init__(self, b=None):
        self._b = b

    def set_b(self, b):
        self._b = b

    def do_something(self):
        if self._b:
            return self._b.help()
        return "No B available"


# module_b.py
class B:
    def __init__(self, a=None):
        self._a = a

    def set_a(self, a):
        self._a = a

    def help(self):
        return "Help from B"


# main.py
from module_a import A
from module_b import B

a = A()
b = B()
a.set_b(b)
b.set_a(a)


# ✅ 方案2：接口抽象

from abc import ABC, abstractmethod

class IB(ABC):
    """B的接口"""
    @abstractmethod
    def help(self): pass


class A:
    def __init__(self, b: IB = None):
        self._b = b

    def do_something(self):
        if self._b:
            return self._b.help()
        return "No B available"


class B(IB):
    def help(self):
        return "Help from B"


# ✅ 方案3：事件驱动

class EventBus:
    """事件总线 - 解耦"""

    _handlers = {}

    @classmethod
    def subscribe(cls, event: str, handler):
        if event not in cls._handlers:
            cls._handlers[event] = []
        cls._handlers[event].append(handler)

    @classmethod
    def publish(cls, event: str, data):
        for handler in cls._handlers.get(event, []):
            handler(data)


class ModuleA:
    def __init__(self):
        EventBus.subscribe("help_needed", self.on_help_needed)

    def on_help_needed(self, data):
        print(f"A received help request: {data}")

    def request_help(self):
        EventBus.publish("need_help", "from A")


class ModuleB:
    def __init__(self):
        EventBus.subscribe("need_help", self.on_need_help)

    def on_need_help(self, data):
        print(f"B received request: {data}")
        EventBus.publish("help_needed", "Help from B")


# 使用
print("=== Event-Driven Decoupling ===")
a = ModuleA()
b = ModuleB()
a.request_help()
```

---

### 5.3 过度设计

#### 问题描述

为简单问题设计复杂的解决方案，增加不必要的抽象。

#### 反例

```python
# ❌ 过度设计 - 简单问题复杂化

from abc import ABC, abstractmethod
from typing import List

# 只需要一个简单的函数，却设计了复杂的类层次

class DataProcessor(ABC):
    """数据处理器抽象类"""

    @abstractmethod
    def process(self, data: List[int]) -> List[int]:
        pass


class DataValidator(ABC):
    """数据验证器抽象类"""

    @abstractmethod
    def validate(self, data: List[int]) -> bool:
        pass


class DataTransformer(ABC):
    """数据转换器抽象类"""

    @abstractmethod
    def transform(self, data: List[int]) -> List[int]:
        pass


class IntegerValidator(DataValidator):
    def validate(self, data: List[int]) -> bool:
        return all(isinstance(x, int) for x in data)


class DoubleTransformer(DataTransformer):
    def transform(self, data: List[int]) -> List[int]:
        return [x * 2 for x in data]


class DoublingProcessor(DataProcessor):
    """加倍处理器"""

    def __init__(self, validator: DataValidator, transformer: DataTransformer):
        self.validator = validator
        self.transformer = transformer

    def process(self, data: List[int]) -> List[int]:
        if not self.validator.validate(data):
            raise ValueError("Invalid data")
        return self.transformer.transform(data)


# 使用
validator = IntegerValidator()
transformer = DoubleTransformer()
processor = DoublingProcessor(validator, transformer)
result = processor.process([1, 2, 3, 4, 5])

# 问题：
# 1. 7个类 vs 1个函数
# 2. 难以理解和维护
# 3. 过度抽象
```

#### 正确设计

```python
# ✅ 正确：简单直接

def double_values(data: List[int]) -> List[int]:
    """将列表中的每个值加倍"""
    return [x * 2 for x in data]


# 使用
result = double_values([1, 2, 3, 4, 5])


# 当需要扩展时，逐步增加复杂性

class DataPipeline:
    """数据处理管道 - 适度设计"""

    def __init__(self):
        self.steps = []

    def add_step(self, func):
        self.steps.append(func)
        return self

    def process(self, data):
        for step in self.steps:
            data = step(data)
        return data


# 使用
pipeline = (DataPipeline()
    .add_step(lambda x: [i for i in x if i > 0])  # 过滤
    .add_step(lambda x: [i * 2 for i in x])        # 加倍
    .add_step(lambda x: [i for i in x if i < 100]) # 再次过滤
)

result = pipeline.process([1, -2, 3, 4, 100])
```

---

### 5.4 重复代码

#### 问题描述

相同的代码出现在多个地方，违反DRY原则。

#### 反例

```python
# ❌ 重复代码

class UserService:
    def create_user(self, data):
        # 验证
        if not data.get("email"):
            raise ValueError("Email required")
        if "@" not in data["email"]:
            raise ValueError("Invalid email")

        # 保存
        print(f"Creating user: {data}")
        return {"id": 1, **data}

    def update_user(self, user_id, data):
        # 验证 - 重复！
        if not data.get("email"):
            raise ValueError("Email required")
        if "@" not in data["email"]:
            raise ValueError("Invalid email")

        # 更新
        print(f"Updating user {user_id}: {data}")
        return {"id": user_id, **data}


class OrderService:
    def create_order(self, data):
        # 验证 - 又重复！
        if not data.get("email"):
            raise ValueError("Email required")
        if "@" not in data["email"]:
            raise ValueError("Invalid email")

        # 创建订单
        print(f"Creating order: {data}")
        return {"order_id": 1, **data}


# 问题：
# 1. 代码重复
# 2. 修改困难
# 3. 容易遗漏
# 4. 测试困难
```

#### 解决方案

```python
# ✅ 方案1：提取函数

def validate_email(email: str) -> None:
    """验证邮箱"""
    if not email:
        raise ValueError("Email required")
    if "@" not in email:
        raise ValueError("Invalid email")


class UserService:
    def create_user(self, data):
        validate_email(data.get("email"))
        print(f"Creating user: {data}")
        return {"id": 1, **data}

    def update_user(self, user_id, data):
        validate_email(data.get("email"))
        print(f"Updating user {user_id}: {data}")
        return {"id": user_id, **data}


# ✅ 方案2：装饰器

from functools import wraps

def validate_email_field(field_name: str):
    """验证邮箱字段装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 从args或kwargs中找到data
            data = kwargs.get('data') or args[1] if len(args) > 1 else None
            if data:
                email = data.get(field_name)
                if not email or "@" not in email:
                    raise ValueError(f"Invalid {field_name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


class OrderService:
    @validate_email_field("email")
    def create_order(self, data):
        print(f"Creating order: {data}")
        return {"order_id": 1, **data}


# ✅ 方案3：Mixin

class ValidationMixin:
    """验证Mixin"""

    def validate_email(self, email: str) -> None:
        if not email or "@" not in email:
            raise ValueError("Invalid email")

    def validate_required(self, data: dict, fields: list) -> None:
        for field in fields:
            if not data.get(field):
                raise ValueError(f"{field} is required")


class ProductService(ValidationMixin):
    def create_product(self, data):
        self.validate_required(data, ["name", "price"])
        print(f"Creating product: {data}")
        return {"product_id": 1, **data}


# ✅ 方案4：继承

class BaseService:
    """基础服务"""

    def validate_email(self, email: str) -> None:
        if not email or "@" not in email:
            raise ValueError("Invalid email")

    def log_operation(self, operation: str, data: dict) -> None:
        print(f"[LOG] {operation}: {data}")


class CustomerService(BaseService):
    def create_customer(self, data):
        self.validate_email(data.get("email"))
        self.log_operation("CREATE_CUSTOMER", data)
        return {"customer_id": 1, **data}


# 测试
print("=== DRY Solutions ===")

try:
    user_service = UserService()
    user_service.create_user({"email": "test@example.com"})
except ValueError as e:
    print(f"Error: {e}")

order_service = OrderService()
order_service.create_order({"email": "order@example.com"})
```

---

## 附录：设计模式速查表

### 创建型模式

| 模式 | 意图 | 使用场景 |
|------|------|----------|
| 单例 | 确保唯一实例 | 配置、连接池 |
| 工厂方法 | 子类决定实例化 | 需要扩展产品 |
| 抽象工厂 | 创建产品家族 | UI主题、数据库 |
| 建造者 | 分步构建复杂对象 | 配置对象、查询 |
| 原型 | 复制创建对象 | 对象创建成本高 |

### 结构型模式

| 模式 | 意图 | 使用场景 |
|------|------|----------|
| 适配器 | 转换接口 | 集成第三方库 |
| 桥接 | 分离抽象与实现 | 多维度扩展 |
| 组合 | 统一树形结构 | UI组件、文件系统 |
| 装饰器 | 动态添加职责 | IO流、中间件 |
| 外观 | 简化接口 | 复杂子系统 |
| 享元 | 共享细粒度对象 | 大量相似对象 |
| 代理 | 控制访问 | 延迟加载、权限 |

### 行为型模式

| 模式 | 意图 | 使用场景 |
|------|------|----------|
| 责任链 | 多个对象处理请求 | 中间件、审批流 |
| 命令 | 封装请求 | 撤销、队列 |
| 解释器 | 定义文法 | 简单DSL |
| 迭代器 | 顺序访问 | 自定义遍历 |
| 中介者 | 封装交互 | 聊天室、MVC |
| 备忘录 | 保存状态 | 撤销、存档 |
| 观察者 | 状态变化通知 | 事件系统 |
| 状态 | 状态改变行为 | 订单状态、游戏 |
| 策略 | 封装算法 | 排序、支付 |
| 模板方法 | 定义算法骨架 | 框架、测试 |
| 访问者 | 分离操作 | AST遍历 |

---

## 总结

### 设计原则

1. **SOLID原则**
   - S: 单一职责原则
   - O: 开闭原则
   - L: 里氏替换原则
   - I: 接口隔离原则
   - D: 依赖倒置原则

2. **DRY原则**: Don't Repeat Yourself

3. **KISS原则**: Keep It Simple, Stupid

4. **YAGNI原则**: You Aren't Gonna Need It

### 模式选择指南

```
需要创建对象？
├── 需要唯一实例 → 单例
├── 需要产品家族 → 抽象工厂
├── 子类决定实例 → 工厂方法
├── 分步构建 → 建造者
└── 复制创建 → 原型

需要组织类结构？
├── 接口不兼容 → 适配器
├── 多维度扩展 → 桥接
├── 树形结构 → 组合
├── 动态添加功能 → 装饰器
├── 简化复杂系统 → 外观
├── 大量相似对象 → 享元
└── 控制访问 → 代理

需要处理行为？
├── 多个对象可处理 → 责任链
├── 需要撤销 → 命令
├── 遍历集合 → 迭代器
├── 对象间通信 → 中介者/观察者
├── 状态改变行为 → 状态
├── 算法可变 → 策略
├── 复用算法结构 → 模板方法
└── 操作与结构分离 → 访问者
```

---

*文档版本: 1.0*
*最后更新: 2024*
