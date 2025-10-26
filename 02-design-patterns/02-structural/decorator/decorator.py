"""
Decorator Pattern - 装饰器模式完整实现

提供6种Python装饰器实现方式：
1. 经典OOP装饰器
2. Python函数装饰器
3. 参数化装饰器
4. 类装饰器
5. 装饰类的装饰器
6. 方法装饰器
"""

from abc import ABC, abstractmethod
from functools import wraps, lru_cache
from typing import Callable, Any, TypeVar, ParamSpec, Type
import time
import logging
import threading
from dataclasses import dataclass
import statistics

# 类型变量
P = ParamSpec('P')
R = TypeVar('R')
T = TypeVar('T')

# ============================================================================
# 1. 经典OOP装饰器 - 遵循GoF设计模式
# ============================================================================


class Component(ABC):
    """组件接口"""
    
    @abstractmethod
    def operation(self) -> str:
        """组件的核心操作"""
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        """获取成本"""
        pass


class ConcreteComponent(Component):
    """具体组件"""
    
    def __init__(self, name: str):
        self.name = name
    
    def operation(self) -> str:
        return f"[{self.name}]"

    def get_cost(self) -> float:
        return 10.0


class Decorator(Component):
    """装饰器基类"""
    
    def __init__(self, component: Component):
        self._component = component
    
    def operation(self) -> str:
        return self._component.operation()

    def get_cost(self) -> float:
        return self._component.get_cost()


class ConcreteDecoratorA(Decorator):
    """具体装饰器A - 添加前缀"""
    
    def operation(self) -> str:
        return f"A({self._component.operation()})"

    def get_cost(self) -> float:
        return self._component.get_cost() + 5.0


class ConcreteDecoratorB(Decorator):
    """具体装饰器B - 添加后缀"""
    
    def operation(self) -> str:
        return f"{self._component.operation()}B"
    
    def get_cost(self) -> float:
        return self._component.get_cost() + 3.0


class ConcreteDecoratorC(Decorator):
    """具体装饰器C - 大写转换"""
    
    def operation(self) -> str:
        return self._component.operation().upper()
    
    def get_cost(self) -> float:
        return self._component.get_cost() + 2.0


# ============================================================================
# 2. Python函数装饰器
# ============================================================================


def simple_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """最简单的装饰器"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("执行前")
        result = func(*args, **kwargs)
        print("执行后")
        return result
    return wrapper


def timing_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱️  {func.__name__} 耗时: {elapsed*1000:.3f}ms")
        return result
    return wrapper


def logging_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """日志装饰器"""
    logger = logging.getLogger(func.__module__)
    
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info(f"调用 {func.__name__}")
        logger.debug(f"参数: args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"返回: {result}")
            return result
        except Exception as e:
            logger.error(f"异常: {e}")
            raise
    return wrapper


def exception_handler(func: Callable[P, R]) -> Callable[P, R]:
    """异常处理装饰器"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ 捕获异常: {type(e).__name__}: {e}")
            return None
    return wrapper


# ============================================================================
# 3. 参数化装饰器
# ============================================================================


def repeat(times: int):
    """重复执行装饰器"""
    def decorator(func: Callable[P, R]) -> Callable[P, list[R]]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> list[R]:
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,)
):
    """重试装饰器"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        break
                    
                    print(f"第 {attempt} 次尝试失败: {e}")
                    print(f"等待 {current_delay:.1f}秒后重试...")
                    
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            if last_exception:
                raise last_exception
            raise RuntimeError("重试失败")
        return wrapper
    return decorator


def rate_limit(calls: int, period: float):
    """限流装饰器"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        timestamps: list[float] = []
        lock = threading.Lock()
        
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with lock:
                current = time.time()
                
                # 移除过期的时间戳
                timestamps[:] = [t for t in timestamps if current - t < period]
                
                if len(timestamps) >= calls:
                    wait_time = period - (current - timestamps[0])
                    raise RuntimeError(
                        f"超过速率限制 ({calls} calls/{period}s). "
                        f"请等待 {wait_time:.1f}秒"
                    )
                
                timestamps.append(current)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def validate_args(**validators: Callable[[Any], bool]):
    """参数验证装饰器"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # 验证kwargs
            for key, validator in validators.items():
                if key in kwargs:
                    value = kwargs[key]
                    if not validator(value):
                        raise ValueError(
                            f"参数 '{key}' 验证失败: {value}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def timeout(seconds: float):
    """超时装饰器"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            import threading
            
            result: list[R | Exception] = []
            
            def target():
                try:
                    result.append(func(*args, **kwargs))
                except Exception as e:
                    result.append(e)
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(seconds)
            
            if thread.is_alive():
                raise TimeoutError(f"函数执行超时 ({seconds}s)")
            
            if not result:
                raise RuntimeError("函数执行失败")
            
            if isinstance(result[0], Exception):
                raise result[0]
            
            return result[0]
        return wrapper
    return decorator


# ============================================================================
# 4. 类装饰器
# ============================================================================


class CountCalls:
    """计数装饰器"""
    
    def __init__(self, func: Callable):
        self.func = func
        self.count = 0
        self.lock = threading.Lock()
    
    def __call__(self, *args, **kwargs):
        with self.lock:
            self.count += 1
            print(f"📞 第 {self.count} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)
    
    def get_count(self) -> int:
        """获取调用次数"""
        with self.lock:
            return self.count
    
    def reset(self) -> None:
        """重置计数"""
        with self.lock:
            self.count = 0


class Cache:
    """缓存装饰器"""
    
    def __init__(self, func: Callable):
        self.func = func
        self.cache: dict[tuple, Any] = {}
        self.hits = 0
        self.misses = 0
        self.lock = threading.Lock()
    
    def __call__(self, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        
        with self.lock:
            if key in self.cache:
                self.hits += 1
                return self.cache[key]
            
            self.misses += 1
        
        result = self.func(*args, **kwargs)
        
        with self.lock:
            self.cache[key] = result
        
        return result
    
    def clear(self) -> None:
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
    
    def stats(self) -> dict[str, int]:
        """获取统计信息"""
        with self.lock:
            total = self.hits + self.misses
            hit_rate = (self.hits / total * 100) if total > 0 else 0
            return {
                "hits": self.hits,
                "misses": self.misses,
                "total": total,
                "hit_rate": hit_rate,
                "cache_size": len(self.cache),
            }


class Timer:
    """计时器装饰器（保存统计信息）"""
    
    def __init__(self, func: Callable):
        self.func = func
        self.times: list[float] = []
        self.lock = threading.Lock()
    
    def __call__(self, *args, **kwargs):
        start = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        
        with self.lock:
            self.times.append(elapsed)
        
        return result
    
    def statistics(self) -> dict[str, float]:
        """获取统计信息"""
        with self.lock:
            if not self.times:
                return {}
            
            return {
                "count": len(self.times),
                "total": sum(self.times),
                "mean": statistics.mean(self.times),
                "median": statistics.median(self.times),
                "min": min(self.times),
                "max": max(self.times),
                "stdev": statistics.stdev(self.times) if len(self.times) > 1 else 0,
            }


# ============================================================================
# 5. 装饰类的装饰器
# ============================================================================


def singleton(cls: Type[T]) -> Type[T]:
    """单例装饰器"""
    instances: dict[Type, Any] = {}
    lock = threading.Lock()
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance  # type: ignore


def add_repr(cls: Type[T]) -> Type[T]:
    """添加__repr__方法"""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    
    cls.__repr__ = __repr__  # type: ignore
    return cls


def add_eq(cls: Type[T]) -> Type[T]:
    """添加__eq__方法"""
    def __eq__(self, other):
        if not isinstance(other, cls):
            return NotImplemented
        return self.__dict__ == other.__dict__
    
    cls.__eq__ = __eq__  # type: ignore
    return cls


def frozen(cls: Type[T]) -> Type[T]:
    """冻结类（不可变）"""
    original_setattr = cls.__setattr__
    original_delattr = cls.__delattr__
    
    def __setattr__(self, key, value):
        if hasattr(self, '_frozen'):
            raise AttributeError(f"Cannot modify frozen class {cls.__name__}")
        original_setattr(self, key, value)
    
    def __delattr__(self, key):
        if hasattr(self, '_frozen'):
            raise AttributeError(f"Cannot modify frozen class {cls.__name__}")
        original_delattr(self, key)
    
    cls.__setattr__ = __setattr__  # type: ignore
    cls.__delattr__ = __delattr__  # type: ignore
    
    original_init = cls.__init__
    
    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        object.__setattr__(self, '_frozen', True)
    
    cls.__init__ = __init__  # type: ignore
    
    return cls


# ============================================================================
# 6. 方法装饰器
# ============================================================================


def log_method(func: Callable) -> Callable:
    """记录方法调用"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        class_name = self.__class__.__name__
        print(f"📝 调用 {class_name}.{func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper


def cache_property(func: Callable) -> property:
    """缓存属性"""
    attr_name = f"_cached_{func.__name__}"
    
    @wraps(func)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    return property(wrapper)


def deprecated(message: str = ""):
    """标记方法为已废弃"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import warnings
            msg = message or f"{func.__name__} is deprecated"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# 实用工具装饰器
# ============================================================================


@dataclass
class MemoizeConfig:
    """缓存配置"""
    timeout: float | None = None  # 过期时间（秒）
    maxsize: int | None = None    # 最大缓存项数


def memoize(config: MemoizeConfig | None = None):
    """高级缓存装饰器"""
    if config is None:
        config = MemoizeConfig()
    
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: dict[tuple, tuple[R, float]] = {}
        lock = threading.Lock()
        
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (args, tuple(sorted(kwargs.items())))
            current_time = time.time()
            
            with lock:
                # 检查缓存
                if key in cache:
                    result, cached_time = cache[key]
                    if config.timeout is None or (current_time - cached_time) < config.timeout:
                        return result
                
                # 检查大小限制
                if config.maxsize and len(cache) >= config.maxsize:
                    # 删除最旧的项
                    oldest_key = min(cache.keys(), key=lambda k: cache[k][1])
                    del cache[oldest_key]
            
            # 计算结果
            result = func(*args, **kwargs)
            
            with lock:
                cache[key] = (result, current_time)
            
            return result
        
        def clear_cache():
            with lock:
                cache.clear()
        
        wrapper.clear_cache = clear_cache  # type: ignore
        return wrapper
    
    return decorator


def debug(func: Callable[P, R]) -> Callable[P, R]:
    """调试装饰器"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        print(f"🐛 调用 {func.__name__}({signature})")
        
        try:
            result = func(*args, **kwargs)
            print(f"🐛 {func.__name__} 返回 {result!r}")
            return result
        except Exception as e:
            print(f"🐛 {func.__name__} 抛出 {type(e).__name__}: {e}")
            raise
    
    return wrapper


# ============================================================================
# 对外接口
# ============================================================================

__all__ = [
    # 经典OOP装饰器
    "Component",
    "ConcreteComponent",
    "Decorator",
    "ConcreteDecoratorA",
    "ConcreteDecoratorB",
    "ConcreteDecoratorC",
    # 函数装饰器
    "simple_decorator",
    "timing_decorator",
    "logging_decorator",
    "exception_handler",
    # 参数化装饰器
    "repeat",
    "retry",
    "rate_limit",
    "validate_args",
    "timeout",
    # 类装饰器
    "CountCalls",
    "Cache",
    "Timer",
    # 装饰类
    "singleton",
    "add_repr",
    "add_eq",
    "frozen",
    # 方法装饰器
    "log_method",
    "cache_property",
    "deprecated",
    # 工具
    "memoize",
    "MemoizeConfig",
    "debug",
]


if __name__ == "__main__":
    print("=" * 70)
    print("Decorator Pattern - 演示")
    print("=" * 70)
    
    # 1. 经典OOP装饰器
    print("\n1️⃣  经典OOP装饰器:")
    component = ConcreteComponent("核心")
    decorated = ConcreteDecoratorA(ConcreteDecoratorB(component))
    print(f"   结果: {decorated.operation()}")
    print(f"   成本: ${decorated.get_cost()}")
    
    # 2. 函数装饰器
    print("\n2️⃣  Python函数装饰器:")
    
    @timing_decorator
    def calculate(n: int) -> int:
        return sum(range(n))
    
    result = calculate(1000000)
    print(f"   结果: {result}")
    
    # 3. 参数化装饰器
    print("\n3️⃣  参数化装饰器:")
    
    @retry(max_attempts=3, delay=0.1)
    def unreliable_function():
        import random
        if random.random() < 0.5:
            raise ValueError("随机失败")
        return "成功"
    
    try:
        result = unreliable_function()
        print(f"   结果: {result}")
    except ValueError as e:
        print(f"   最终失败: {e}")
    
    # 4. 类装饰器
    print("\n4️⃣  类装饰器:")
    
    @CountCalls
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    for name in ["Alice", "Bob", "Charlie"]:
        greet(name)
    
    print(f"   总调用次数: {greet.get_count()}")  # type: ignore
    
    print("\n" + "=" * 70)
    print("✅ 所有演示完成！")
    print("=" * 70)
