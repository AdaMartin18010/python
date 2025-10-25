"""
Singleton Pattern (单例模式) 使用示例

本文件包含单例模式的实际使用场景示例,展示了5种不同实现方式的应用。

运行方式:
    python examples.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from singleton import (
    ConfigManager,
    Logger,
    SingletonDCL,
    SingletonMeta,
    SingletonNew,
    global_config,
    is_singleton,
    singleton,
)


# ============================================================================
# 示例1: 使用元类实现 - 配置管理器
# ============================================================================

def example_metaclass_config() -> None:
    """
    示例1: 使用元类实现单例 - 配置管理器
    
    展示如何使用SingletonMeta元类创建全局配置管理器。
    """
    print("=" * 60)
    print("示例1: 元类单例 - 配置管理器")
    print("=" * 60)
    
    # 创建第一个实例
    config1 = ConfigManager()
    config1.set("app_name", "Python2025")
    config1.set("version", "1.0.0")
    config1.set("debug", "true")
    
    print(f"\n配置管理器1: {config1}")
    print(f"app_name: {config1.get('app_name')}")
    print(f"version: {config1.get('version')}")
    
    # 创建第二个实例 - 应该是同一个对象
    config2 = ConfigManager()
    print(f"\n配置管理器2: {config2}")
    print(f"app_name: {config2.get('app_name')}")
    
    # 验证是同一个实例
    print(f"\n两个实例是否相同? {config1 is config2}")
    print(f"ID相同? config1={id(config1)}, config2={id(config2)}")
    
    # 修改配置
    config2.set("app_name", "Python2025-Updated")
    print(f"\n通过config2修改后,config1的值: {config1.get('app_name')}")


# ============================================================================
# 示例2: 使用装饰器实现 - 日志管理器
# ============================================================================

def example_decorator_logger() -> None:
    """
    示例2: 使用装饰器实现单例 - 日志管理器
    
    展示如何使用@singleton装饰器创建全局日志管理器。
    """
    print("\n\n" + "=" * 60)
    print("示例2: 装饰器单例 - 日志管理器")
    print("=" * 60)
    
    # 创建日志管理器
    logger1 = Logger()
    logger1.info("应用程序启动")
    logger1.info("正在加载配置...")
    
    # 在其他地方使用
    logger2 = Logger()
    logger2.warning("这是一个警告")
    logger2.error("发现一个错误")
    
    # 验证是同一个实例
    print(f"\n两个logger是否相同? {logger1 is logger2}")
    
    # 查看所有日志
    logs = logger1.get_logs()
    print(f"\n总共记录了 {len(logs)} 条日志:")
    for log in logs:
        print(f"  {log}")


# ============================================================================
# 示例3: 使用模块级单例 - 全局配置
# ============================================================================

def example_module_singleton() -> None:
    """
    示例3: 模块级单例 - 全局配置
    
    展示最Pythonic的单例实现方式 - 模块级单例。
    """
    print("\n\n" + "=" * 60)
    print("示例3: 模块级单例 - 全局配置")
    print("=" * 60)
    
    # 使用模块级单例
    print(f"\n应用名称: {global_config.app_name}")
    print(f"版本: {global_config.version}")
    print(f"调试模式: {global_config.debug}")
    
    # 修改配置
    global_config.app_name = "Python2025-Module"
    global_config.debug = True
    
    print(f"\n修改后:")
    print(f"应用名称: {global_config.app_name}")
    print(f"调试模式: {global_config.debug}")
    
    print("\n优点: 最简单,最Pythonic")
    print("缺点: 不支持参数化初始化,不支持继承")


# ============================================================================
# 示例4: 数据库连接池 (元类实现)
# ============================================================================

class DatabasePool(metaclass=SingletonMeta):
    """
    数据库连接池 (单例)
    
    确保整个应用只有一个连接池实例,所有地方共享连接。
    """
    
    def __init__(self) -> None:
        """初始化连接池"""
        if not hasattr(self, "_initialized"):
            self.max_connections = 10
            self.active_connections = 0
            self.total_requests = 0
            self._initialized = True
            print("  [连接池] 初始化完成")
    
    def acquire(self) -> str:
        """获取数据库连接"""
        self.total_requests += 1
        if self.active_connections < self.max_connections:
            self.active_connections += 1
            conn_id = f"Connection-{self.active_connections}"
            print(f"  [连接池] 分配连接: {conn_id}")
            return conn_id
        raise RuntimeError("连接池已满,无可用连接")
    
    def release(self, connection: str) -> None:
        """释放数据库连接"""
        if self.active_connections > 0:
            self.active_connections -= 1
            print(f"  [连接池] 释放连接: {connection}")
    
    def get_stats(self) -> dict[str, int]:
        """获取连接池统计信息"""
        return {
            "max_connections": self.max_connections,
            "active_connections": self.active_connections,
            "total_requests": self.total_requests,
        }


def example_database_pool() -> None:
    """
    示例4: 数据库连接池
    
    展示在实际应用中如何使用单例模式管理资源。
    """
    print("\n\n" + "=" * 60)
    print("示例4: 数据库连接池 (资源管理)")
    print("=" * 60)
    
    # 第一次获取连接池
    pool1 = DatabasePool()
    conn1 = pool1.acquire()
    conn2 = pool1.acquire()
    
    # 在其他模块中获取连接池
    pool2 = DatabasePool()
    conn3 = pool2.acquire()
    
    # 验证是同一个连接池
    print(f"\n两个pool是否相同? {pool1 is pool2}")
    
    # 查看连接池状态
    stats = pool1.get_stats()
    print(f"\n连接池状态:")
    print(f"  最大连接数: {stats['max_connections']}")
    print(f"  活跃连接数: {stats['active_connections']}")
    print(f"  总请求数: {stats['total_requests']}")
    
    # 释放连接
    pool1.release(conn1)
    pool2.release(conn2)
    
    stats = pool1.get_stats()
    print(f"\n释放2个连接后:")
    print(f"  活跃连接数: {stats['active_connections']}")


# ============================================================================
# 示例5: 应用上下文 (__new__ 方式)
# ============================================================================

class ApplicationContext(SingletonNew):
    """
    应用程序上下文 (单例)
    
    存储应用级别的全局状态和配置。
    """
    
    def __init__(self) -> None:
        """初始化应用上下文"""
        if not hasattr(self, "_initialized"):
            self.user: str | None = None
            self.session_id: str | None = None
            self.request_count = 0
            self._initialized = True
    
    def login(self, username: str) -> None:
        """用户登录"""
        self.user = username
        self.session_id = f"session_{id(self)}"
        print(f"  用户 {username} 登录成功")
    
    def logout(self) -> None:
        """用户登出"""
        if self.user:
            print(f"  用户 {self.user} 登出")
        self.user = None
        self.session_id = None
    
    def increment_request(self) -> None:
        """增加请求计数"""
        self.request_count += 1
    
    def get_status(self) -> dict[str, str | int | None]:
        """获取上下文状态"""
        return {
            "user": self.user,
            "session_id": self.session_id,
            "request_count": self.request_count,
        }


def example_application_context() -> None:
    """
    示例5: 应用程序上下文
    
    展示使用__new__方式实现的单例。
    """
    print("\n\n" + "=" * 60)
    print("示例5: 应用程序上下文 (__new__方式)")
    print("=" * 60)
    
    # 模拟应用流程
    ctx1 = ApplicationContext()
    ctx1.login("alice")
    ctx1.increment_request()
    
    # 在其他地方访问上下文
    ctx2 = ApplicationContext()
    ctx2.increment_request()
    ctx2.increment_request()
    
    print(f"\n两个上下文是否相同? {ctx1 is ctx2}")
    
    # 查看状态
    status = ctx1.get_status()
    print(f"\n应用状态:")
    print(f"  当前用户: {status['user']}")
    print(f"  会话ID: {status['session_id']}")
    print(f"  请求计数: {status['request_count']}")
    
    # 登出
    ctx2.logout()
    status = ctx1.get_status()
    print(f"\n登出后状态:")
    print(f"  当前用户: {status['user']}")


# ============================================================================
# 示例6: 自定义单例类 (DCL方式)
# ============================================================================

class CacheManager(SingletonDCL):
    """
    缓存管理器 (单例)
    
    使用双重检查锁定方式实现的单例。
    """
    
    def __init__(self) -> None:
        """初始化缓存管理器"""
        if not hasattr(self, "_initialized"):
            self._cache: dict[str, str] = {}
            self.hit_count = 0
            self.miss_count = 0
            self._initialized = True
    
    def get(self, key: str) -> str | None:
        """获取缓存"""
        value = self._cache.get(key)
        if value:
            self.hit_count += 1
            print(f"  [缓存] 命中: {key} = {value}")
        else:
            self.miss_count += 1
            print(f"  [缓存] 未命中: {key}")
        return value
    
    def set(self, key: str, value: str) -> None:
        """设置缓存"""
        self._cache[key] = value
        print(f"  [缓存] 存储: {key} = {value}")
    
    def get_stats(self) -> dict[str, int]:
        """获取缓存统计"""
        total = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total * 100) if total > 0 else 0
        return {
            "items": len(self._cache),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": round(hit_rate, 2),
        }


def example_cache_manager() -> None:
    """
    示例6: 缓存管理器
    
    展示使用双重检查锁定方式实现的单例。
    """
    print("\n\n" + "=" * 60)
    print("示例6: 缓存管理器 (DCL方式)")
    print("=" * 60)
    
    # 使用缓存
    cache1 = CacheManager()
    cache1.set("user:1", "Alice")
    cache1.set("user:2", "Bob")
    
    # 在其他地方访问缓存
    cache2 = CacheManager()
    cache2.get("user:1")  # 命中
    cache2.get("user:2")  # 命中
    cache2.get("user:3")  # 未命中
    
    print(f"\n两个缓存是否相同? {cache1 is cache2}")
    
    # 查看统计
    stats = cache1.get_stats()
    print(f"\n缓存统计:")
    print(f"  缓存项数: {stats['items']}")
    print(f"  命中次数: {stats['hit_count']}")
    print(f"  未命中次数: {stats['miss_count']}")
    print(f"  命中率: {stats['hit_rate']}%")


# ============================================================================
# 示例7: 验证单例特性
# ============================================================================

def example_singleton_verification() -> None:
    """
    示例7: 验证单例特性
    
    使用工具函数验证各种类是否为单例。
    """
    print("\n\n" + "=" * 60)
    print("示例7: 单例特性验证")
    print("=" * 60)
    
    # 测试各种单例实现
    print("\n验证结果:")
    print(f"  ConfigManager (元类): {is_singleton(ConfigManager)}")
    print(f"  Logger (装饰器): {is_singleton(Logger)}")
    print(f"  DatabasePool (元类): {is_singleton(DatabasePool)}")
    print(f"  ApplicationContext (__new__): {is_singleton(ApplicationContext)}")
    print(f"  CacheManager (DCL): {is_singleton(CacheManager)}")
    
    # 测试非单例类
    class RegularClass:
        pass
    
    print(f"  RegularClass (普通类): {is_singleton(RegularClass)}")


# ============================================================================
# 示例8: 线程安全演示 (简化版)
# ============================================================================

def example_thread_safety() -> None:
    """
    示例8: 线程安全演示
    
    展示单例模式在多线程环境下的行为。
    """
    print("\n\n" + "=" * 60)
    print("示例8: 线程安全特性")
    print("=" * 60)
    
    print("\n所有实现都使用了线程锁,确保线程安全:")
    print("  ✓ SingletonMeta: 使用 threading.Lock()")
    print("  ✓ @singleton: 使用 threading.Lock()")
    print("  ✓ SingletonNew: 使用类级 threading.Lock()")
    print("  ✓ SingletonDCL: 双重检查锁定 + threading.Lock()")
    print("  ✓ 模块级单例: Python解释器保证")
    
    print("\n在高并发场景下,所有实现都能保证:")
    print("  • 只创建一个实例")
    print("  • 线程之间共享同一个实例")
    print("  • 不会出现竞态条件")


# ============================================================================
# 示例9: 实际应用场景对比
# ============================================================================

def example_real_world_scenarios() -> None:
    """
    示例9: 实际应用场景对比
    
    展示不同单例实现方式的适用场景。
    """
    print("\n\n" + "=" * 60)
    print("示例9: 实际应用场景建议")
    print("=" * 60)
    
    scenarios = [
        ("配置管理", "元类 (SingletonMeta)", "需要继承,接口清晰"),
        ("日志系统", "装饰器 (@singleton)", "简单易用,快速实现"),
        ("全局常量", "模块级单例", "最Pythonic,性能最好"),
        ("连接池", "元类 (SingletonMeta)", "资源管理,需要复杂初始化"),
        ("缓存系统", "DCL (SingletonDCL)", "高性能要求,减少锁竞争"),
        ("应用上下文", "__new__方式", "标准实现,兼容性好"),
    ]
    
    print("\n场景推荐:")
    for scenario, method, reason in scenarios:
        print(f"\n  【{scenario}】")
        print(f"    推荐: {method}")
        print(f"    原因: {reason}")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    """运行所有示例"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Singleton Pattern 完整示例" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        # 运行所有示例
        example_metaclass_config()
        example_decorator_logger()
        example_module_singleton()
        example_database_pool()
        example_application_context()
        example_cache_manager()
        example_singleton_verification()
        example_thread_safety()
        example_real_world_scenarios()
        
        # 总结
        print("\n\n" + "=" * 60)
        print("✅ 所有示例运行完成!")
        print("=" * 60)
        print("\n关键要点:")
        print("  1. 单例模式确保一个类只有一个实例")
        print("  2. 所有实现都是线程安全的")
        print("  3. 推荐使用元类或装饰器方式")
        print("  4. 模块级单例最简单但灵活性较低")
        print("  5. 注意初始化陷阱 - 使用_initialized标志")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

