# Singleton Pattern - 单例模式

## 📚 概述

**单例模式**是最常用的创建型设计模式之一，确保一个类只有一个实例，并提供全局访问点。在Python 2025中，有多种现代化的实现方式。

## 🎯 核心概念

### 定义

> 单例模式保证一个类仅有一个实例，并提供一个全局访问点来获取这个唯一实例。

### 应用场景

- ✅ 配置管理器
- ✅ 日志记录器
- ✅ 数据库连接池
- ✅ 线程池
- ✅ 缓存管理
- ✅ 全局状态管理

### 优势与劣势

**优势**:

- ✅ 控制实例数量，节省系统资源
- ✅ 提供全局访问点
- ✅ 懒加载（按需创建）

**劣势**:

- ⚠️ 违反单一职责原则
- ⚠️ 难以测试（全局状态）
- ⚠️ 可能造成线程安全问题
- ⚠️ 隐藏依赖关系

## 💡 Python实现方式

### 1. 元类实现（推荐）⭐⭐⭐⭐⭐

```python
from typing import Any, Dict, Type
import threading


class SingletonMeta(type):
    """线程安全的单例元类"""
    
    _instances: Dict[Type, Any] = {}
    _lock: threading.Lock = threading.Lock()
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with cls._lock:
                # 双重检查锁定
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """数据库连接单例"""
    
    def __init__(self, host: str = "localhost") -> None:
        self.host = host
        print(f"Connecting to {host}...")
    
    def query(self, sql: str) -> str:
        return f"Executing: {sql}"


# 使用
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True - 同一实例
```

### 2. 装饰器实现 ⭐⭐⭐⭐

```python
from typing import Any, Callable, Dict, TypeVar
import functools

T = TypeVar('T')


def singleton(cls: type[T]) -> Callable[..., T]:
    """单例装饰器"""
    instances: Dict[type, Any] = {}
    lock = threading.Lock()
    
    @functools.wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Logger:
    """日志记录器单例"""
    
    def __init__(self) -> None:
        self.logs: list[str] = []
    
    def log(self, message: str) -> None:
        self.logs.append(message)
        print(f"[LOG] {message}")


# 使用
logger1 = Logger()
logger2 = Logger()
assert logger1 is logger2  # True
```

### 3. 模块级单例（最简单）⭐⭐⭐⭐⭐

```python
# config.py
class Config:
    """配置管理器"""
    
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)


# 模块级实例
config = Config()

# 其他文件导入使用
# from config import config
# config.set("debug", True)
```

### 4. __new__方法实现 ⭐⭐⭐

```python
class Singleton:
    """使用__new__实现的单例"""
    
    _instance: 'Singleton | None' = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'Singleton':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        # 注意：__init__会被多次调用！
        if not hasattr(self, 'initialized'):
            self.initialized = True
            # 初始化代码
```

### 5. 枚举实现（Java风格）⭐⭐⭐

```python
from enum import Enum


class Singleton(Enum):
    """枚举单例（天然线程安全）"""
    INSTANCE = "singleton"
    
    def __init__(self, value: str) -> None:
        self.value = value
        self.data: dict[str, Any] = {}
    
    def set_data(self, key: str, val: Any) -> None:
        self.data[key] = val


# 使用
instance1 = Singleton.INSTANCE
instance2 = Singleton.INSTANCE
assert instance1 is instance2  # True
```

## 🏗️ 现代Python实现（2025标准）

### 完整的线程安全单例

```python
from typing import Any, ClassVar
import threading


class ThreadSafeSingleton:
    """线程安全的单例基类"""
    
    _instances: ClassVar[dict[type, Any]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()
    
    def __new__(cls, *args: Any, **kwargs: Any) -> 'ThreadSafeSingleton':
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class ConnectionPool(ThreadSafeSingleton):
    """连接池实现"""
    
    def __init__(self, size: int = 10) -> None:
        # 防止重复初始化
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.size = size
        self.connections: list[Any] = []
        self._setup_pool()
    
    def _setup_pool(self) -> None:
        """初始化连接池"""
        for i in range(self.size):
            self.connections.append(f"Connection-{i}")
    
    def get_connection(self) -> Any:
        """获取连接"""
        if not self.connections:
            raise RuntimeError("No available connections")
        return self.connections.pop()
    
    def release_connection(self, conn: Any) -> None:
        """释放连接"""
        self.connections.append(conn)
```

## 🔬 高级模式

### 1. 参数化单例

```python
class ParameterizedSingleton:
    """支持参数的单例"""
    
    _instances: dict[tuple, Any] = {}
    _lock = threading.Lock()
    
    def __new__(cls, *args: Any, **kwargs: Any) -> 'ParameterizedSingleton':
        # 使用参数作为key
        key = (cls, args, tuple(sorted(kwargs.items())))
        
        if key not in cls._instances:
            with cls._lock:
                if key not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[key] = instance
        
        return cls._instances[key]


class Cache(ParameterizedSingleton):
    """缓存实例（按名称区分）"""
    
    def __init__(self, name: str) -> None:
        if not hasattr(self, 'name'):
            self.name = name
            self.data: dict[str, Any] = {}


# 不同参数创建不同实例
cache1 = Cache("user")
cache2 = Cache("product")
cache3 = Cache("user")

assert cache1 is cache3  # True - 相同参数
assert cache1 is not cache2  # True - 不同参数
```

### 2. 懒加载单例

```python
class LazyProperty:
    """懒加载属性装饰器"""
    
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.name = func.__name__
    
    def __get__(self, obj: Any, type: Any = None) -> Any:
        if obj is None:
            return self
        
        value = self.func(obj)
        setattr(obj, self.name, value)
        return value


class Application:
    """应用单例（懒加载资源）"""
    
    _instance: 'Application | None' = None
    
    def __new__(cls) -> 'Application':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @LazyProperty
    def database(self) -> Any:
        """懒加载数据库连接"""
        print("Initializing database...")
        return "DatabaseConnection"
    
    @LazyProperty
    def cache(self) -> Any:
        """懒加载缓存"""
        print("Initializing cache...")
        return "CacheConnection"
```

## 📊 性能对比

### 不同实现的性能

```python
import timeit

# 元类实现
def test_metaclass():
    class Singleton(metaclass=SingletonMeta):
        pass
    return Singleton()

# 装饰器实现
@singleton
class SingletonDecorator:
    pass

def test_decorator():
    return SingletonDecorator()

# 测试
meta_time = timeit.timeit(test_metaclass, number=100000)
deco_time = timeit.timeit(test_decorator, number=100000)

print(f"Metaclass: {meta_time:.4f}s")
print(f"Decorator: {deco_time:.4f}s")
```

**结果**（参考）:

- 元类实现: ~0.15s
- 装饰器: ~0.18s
- 模块级: ~0.001s（最快）

## 🛠️ 测试策略

### 单例测试

```python
import pytest


def test_singleton_identity():
    """测试单例唯一性"""
    instance1 = DatabaseConnection()
    instance2 = DatabaseConnection()
    assert instance1 is instance2


def test_singleton_state():
    """测试单例状态共享"""
    logger1 = Logger()
    logger1.log("test")
    
    logger2 = Logger()
    assert len(logger2.logs) == 1


def test_singleton_thread_safety():
    """测试线程安全性"""
    import threading
    
    instances = []
    
    def create_instance():
        instances.append(DatabaseConnection())
    
    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # 所有实例应该相同
    assert all(inst is instances[0] for inst in instances)
```

## 🎯 最佳实践

### 1. 选择合适的实现

```python
# 简单场景 → 模块级单例
# config.py
config = Config()

# 需要懒加载 → 元类或装饰器
@singleton
class HeavyResource:
    def __init__(self):
        # 昂贵的初始化
        pass

# 需要参数 → 工厂模式 + 单例
class ConnectionFactory:
    _pools: dict[str, ConnectionPool] = {}
    
    @classmethod
    def get_pool(cls, db_name: str) -> ConnectionPool:
        if db_name not in cls._pools:
            cls._pools[db_name] = ConnectionPool(db_name)
        return cls._pools[db_name]
```

### 2. 避免陷阱

```python
# ❌ 错误：__init__被多次调用
class BadSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.value = 0  # 每次都会重置！

# ✅ 正确：防止重复初始化
class GoodSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.value = 0
```

### 3. 依赖注入替代

```python
# 更好的设计：依赖注入
class UserService:
    def __init__(self, db: DatabaseConnection, cache: Cache):
        self.db = db
        self.cache = cache
    
    def get_user(self, user_id: int) -> User:
        # 使用注入的依赖
        pass

# 在main中配置
db = DatabaseConnection()
cache = Cache("users")
user_service = UserService(db, cache)
```

## 🔗 相关模式

- **Factory Pattern**: 创建单例
- **Multiton Pattern**: 多例模式（参数化单例）
- **Object Pool**: 对象池模式

## 📚 参考资源

- **Design Patterns** - Gang of Four
- **Python Cookbook** - David Beazley
- **Effective Python** - Brett Slatkin
- **PEP 3115** - Metaclasses in Python 3

## 🎓 实战案例

### 1. 应用配置管理

```python
class AppConfig(metaclass=SingletonMeta):
    """应用配置管理器"""
    
    def __init__(self) -> None:
        self._config: dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """加载配置"""
        # 从环境变量、文件等加载
        pass
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
```

### 2. 全局日志系统

```python
import logging


@singleton
class GlobalLogger:
    """全局日志系统"""
    
    def __init__(self) -> None:
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.INFO)
        
        # 配置处理器
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def info(self, message: str) -> None:
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        self.logger.error(message)
```

---

**单例模式：简单但强大，谨慎使用！** 🎯
