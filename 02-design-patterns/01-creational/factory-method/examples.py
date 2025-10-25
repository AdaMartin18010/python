"""
Factory Method Pattern - 实际应用示例

展示工厂方法模式在各种实际场景中的应用：
1. 数据库连接工厂
2. 日志处理器工厂
3. 文档解析器工厂
4. 消息队列工厂
5. UI组件工厂
6. 序列化器工厂
7. 支付方式工厂
8. 通知发送器工厂
9. 缓存策略工厂
"""

from abc import ABC, abstractmethod
from typing import Any, Protocol
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


# ============================================================================
# 示例1: 数据库连接工厂
# ============================================================================


class DatabaseConnection(ABC):
    """数据库连接抽象类"""

    @abstractmethod
    def connect(self) -> None:
        """建立连接"""
        pass

    @abstractmethod
    def execute(self, query: str) -> list[dict]:
        """执行查询"""
        pass

    @abstractmethod
    def close(self) -> None:
        """关闭连接"""
        pass


class MySQLConnection(DatabaseConnection):
    """MySQL连接实现"""

    def __init__(self, host: str, port: int = 3306, **kwargs: Any):
        self.host = host
        self.port = port
        self.config = kwargs
        self.connected = False

    def connect(self) -> None:
        print(f"🔗 连接到MySQL: {self.host}:{self.port}")
        self.connected = True

    def execute(self, query: str) -> list[dict]:
        if not self.connected:
            raise RuntimeError("数据库未连接")
        print(f"🔍 执行MySQL查询: {query}")
        return [{"id": 1, "name": "Test", "db": "mysql"}]

    def close(self) -> None:
        print("❌ 关闭MySQL连接")
        self.connected = False


class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL连接实现"""

    def __init__(self, host: str, port: int = 5432, **kwargs: Any):
        self.host = host
        self.port = port
        self.config = kwargs
        self.connected = False

    def connect(self) -> None:
        print(f"🔗 连接到PostgreSQL: {self.host}:{self.port}")
        self.connected = True

    def execute(self, query: str) -> list[dict]:
        if not self.connected:
            raise RuntimeError("数据库未连接")
        print(f"🔍 执行PostgreSQL查询: {query}")
        return [{"id": 1, "name": "Test", "db": "postgresql"}]

    def close(self) -> None:
        print("❌ 关闭PostgreSQL连接")
        self.connected = False


class MongoDBConnection(DatabaseConnection):
    """MongoDB连接实现"""

    def __init__(self, host: str, port: int = 27017, **kwargs: Any):
        self.host = host
        self.port = port
        self.config = kwargs
        self.connected = False

    def connect(self) -> None:
        print(f"🔗 连接到MongoDB: {self.host}:{self.port}")
        self.connected = True

    def execute(self, query: str) -> list[dict]:
        if not self.connected:
            raise RuntimeError("数据库未连接")
        print(f"🔍 执行MongoDB查询: {query}")
        return [{"_id": "1", "name": "Test", "db": "mongodb"}]

    def close(self) -> None:
        print("❌ 关闭MongoDB连接")
        self.connected = False


# 数据库工厂注册
from factory_method import FactoryRegistry

FactoryRegistry.register("mysql")(MySQLConnection)
FactoryRegistry.register("postgresql")(PostgreSQLConnection)
FactoryRegistry.register("mongodb")(MongoDBConnection)


def demo_database_factory() -> None:
    """演示数据库连接工厂"""
    print("\n" + "=" * 70)
    print("📦 示例1: 数据库连接工厂")
    print("=" * 70)

    # 创建不同类型的数据库连接
    for db_type in ["mysql", "postgresql", "mongodb"]:
        print(f"\n▶ 使用 {db_type.upper()}:")
        conn = FactoryRegistry.create(db_type, host="localhost")
        conn.connect()
        results = conn.execute("SELECT * FROM users")
        print(f"   结果: {results}")
        conn.close()


# ============================================================================
# 示例2: 日志处理器工厂
# ============================================================================


class LogLevel(Enum):
    """日志级别"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogHandler(ABC):
    """日志处理器抽象类"""

    @abstractmethod
    def log(self, level: LogLevel, message: str) -> None:
        """记录日志"""
        pass


class ConsoleLogHandler(LogHandler):
    """控制台日志处理器"""

    def __init__(self, colored: bool = True):
        self.colored = colored

    def log(self, level: LogLevel, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.colored:
            colors = {
                LogLevel.DEBUG: "🔵",
                LogLevel.INFO: "🟢",
                LogLevel.WARNING: "🟡",
                LogLevel.ERROR: "🔴",
                LogLevel.CRITICAL: "🔥",
            }
            icon = colors.get(level, "⚪")
            print(f"{icon} [{timestamp}] {level.value}: {message}")
        else:
            print(f"[{timestamp}] {level.value}: {message}")


class FileLogHandler(LogHandler):
    """文件日志处理器"""

    def __init__(self, filename: str):
        self.filename = filename

    def log(self, level: LogLevel, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level.value}: {message}"
        print(f"📝 写入日志文件 {self.filename}: {log_entry}")


class RemoteLogHandler(LogHandler):
    """远程日志处理器"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def log(self, level: LogLevel, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_data = {"timestamp": timestamp, "level": level.value, "message": message}
        print(f"📡 发送日志到 {self.endpoint}: {log_data}")


# 注册日志处理器
FactoryRegistry.register("console_log")(ConsoleLogHandler)
FactoryRegistry.register("file_log")(FileLogHandler)
FactoryRegistry.register("remote_log")(RemoteLogHandler)


def demo_log_handler_factory() -> None:
    """演示日志处理器工厂"""
    print("\n" + "=" * 70)
    print("📦 示例2: 日志处理器工厂")
    print("=" * 70)

    # 创建不同类型的日志处理器
    console_handler = FactoryRegistry.create("console_log", colored=True)
    console_handler.log(LogLevel.INFO, "应用程序启动")
    console_handler.log(LogLevel.ERROR, "发生错误")

    file_handler = FactoryRegistry.create("file_log", filename="app.log")
    file_handler.log(LogLevel.WARNING, "警告信息")

    remote_handler = FactoryRegistry.create("remote_log", endpoint="https://logs.example.com")
    remote_handler.log(LogLevel.CRITICAL, "严重错误")


# ============================================================================
# 示例3: 文档解析器工厂
# ============================================================================


@dataclass
class Document:
    """文档数据类"""

    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


class DocumentParser(ABC):
    """文档解析器抽象类"""

    @abstractmethod
    def parse(self, data: str) -> Document:
        """解析文档"""
        pass

    @abstractmethod
    def validate(self, data: str) -> bool:
        """验证文档格式"""
        pass


class PDFParser(DocumentParser):
    """PDF解析器"""

    def parse(self, data: str) -> Document:
        print("📄 解析PDF文档...")
        return Document(
            title="PDF文档",
            content=data,
            metadata={"format": "pdf", "pages": 10},
        )

    def validate(self, data: str) -> bool:
        return data.startswith("%PDF")


class WordParser(DocumentParser):
    """Word文档解析器"""

    def parse(self, data: str) -> Document:
        print("📝 解析Word文档...")
        return Document(
            title="Word文档",
            content=data,
            metadata={"format": "docx", "author": "User"},
        )

    def validate(self, data: str) -> bool:
        return data.startswith("PK")  # DOCX是ZIP格式


class MarkdownParser(DocumentParser):
    """Markdown解析器"""

    def parse(self, data: str) -> Document:
        print("📋 解析Markdown文档...")
        lines = data.split("\n")
        title = lines[0].lstrip("#").strip() if lines else "Untitled"
        return Document(
            title=title,
            content=data,
            metadata={"format": "markdown", "lines": len(lines)},
        )

    def validate(self, data: str) -> bool:
        return "#" in data or "*" in data


# 注册文档解析器
FactoryRegistry.register("pdf_parser")(PDFParser)
FactoryRegistry.register("word_parser")(WordParser)
FactoryRegistry.register("markdown_parser")(MarkdownParser)


def demo_document_parser_factory() -> None:
    """演示文档解析器工厂"""
    print("\n" + "=" * 70)
    print("📦 示例3: 文档解析器工厂")
    print("=" * 70)

    # 解析不同格式的文档
    pdf_data = "%PDF-1.4 Sample PDF content"
    pdf_parser = FactoryRegistry.create("pdf_parser")
    pdf_doc = pdf_parser.parse(pdf_data)
    print(f"   解析结果: {pdf_doc.title}, 元数据: {pdf_doc.metadata}")

    md_data = "# Markdown Document\n\nContent here..."
    md_parser = FactoryRegistry.create("markdown_parser")
    md_doc = md_parser.parse(md_data)
    print(f"   解析结果: {md_doc.title}, 元数据: {md_doc.metadata}")


# ============================================================================
# 示例4: 消息队列工厂
# ============================================================================


class MessageQueue(Protocol):
    """消息队列协议"""

    def send(self, message: dict[str, Any]) -> None: ...

    def receive(self) -> dict[str, Any] | None: ...

    def connect(self) -> None: ...

    def disconnect(self) -> None: ...


class RabbitMQQueue:
    """RabbitMQ队列实现"""

    def __init__(self, host: str, port: int = 5672):
        self.host = host
        self.port = port
        self.connected = False

    def connect(self) -> None:
        print(f"🔗 连接到RabbitMQ: {self.host}:{self.port}")
        self.connected = True

    def send(self, message: dict[str, Any]) -> None:
        if not self.connected:
            raise RuntimeError("未连接到消息队列")
        print(f"📤 发送消息到RabbitMQ: {message}")

    def receive(self) -> dict[str, Any] | None:
        if not self.connected:
            raise RuntimeError("未连接到消息队列")
        print("📥 从RabbitMQ接收消息")
        return {"id": "123", "data": "test"}

    def disconnect(self) -> None:
        print("❌ 断开RabbitMQ连接")
        self.connected = False


class KafkaQueue:
    """Kafka队列实现"""

    def __init__(self, brokers: list[str]):
        self.brokers = brokers
        self.connected = False

    def connect(self) -> None:
        print(f"🔗 连接到Kafka: {', '.join(self.brokers)}")
        self.connected = True

    def send(self, message: dict[str, Any]) -> None:
        if not self.connected:
            raise RuntimeError("未连接到消息队列")
        print(f"📤 发送消息到Kafka: {message}")

    def receive(self) -> dict[str, Any] | None:
        if not self.connected:
            raise RuntimeError("未连接到消息队列")
        print("📥 从Kafka接收消息")
        return {"offset": 42, "data": "test"}

    def disconnect(self) -> None:
        print("❌ 断开Kafka连接")
        self.connected = False


class RedisQueue:
    """Redis队列实现"""

    def __init__(self, host: str, port: int = 6379):
        self.host = host
        self.port = port
        self.connected = False

    def connect(self) -> None:
        print(f"🔗 连接到Redis: {self.host}:{self.port}")
        self.connected = True

    def send(self, message: dict[str, Any]) -> None:
        if not self.connected:
            raise RuntimeError("未连接到消息队列")
        print(f"📤 推送消息到Redis: {message}")

    def receive(self) -> dict[str, Any] | None:
        if not self.connected:
            raise RuntimeError("未连接到消息队列")
        print("📥 从Redis弹出消息")
        return {"key": "msg:1", "data": "test"}

    def disconnect(self) -> None:
        print("❌ 断开Redis连接")
        self.connected = False


# 注册消息队列
FactoryRegistry.register("rabbitmq")(RabbitMQQueue)
FactoryRegistry.register("kafka")(KafkaQueue)
FactoryRegistry.register("redis_queue")(RedisQueue)


def demo_message_queue_factory() -> None:
    """演示消息队列工厂"""
    print("\n" + "=" * 70)
    print("📦 示例4: 消息队列工厂")
    print("=" * 70)

    # RabbitMQ
    print("\n▶ RabbitMQ:")
    rabbitmq = FactoryRegistry.create("rabbitmq", host="localhost")
    rabbitmq.connect()
    rabbitmq.send({"event": "user.created", "user_id": 123})
    rabbitmq.disconnect()

    # Kafka
    print("\n▶ Kafka:")
    kafka = FactoryRegistry.create("kafka", brokers=["broker1:9092", "broker2:9092"])
    kafka.connect()
    kafka.send({"topic": "events", "message": "test"})
    kafka.disconnect()


# ============================================================================
# 示例5: UI组件工厂
# ============================================================================


class Button(ABC):
    """按钮组件抽象类"""

    @abstractmethod
    def render(self) -> str:
        """渲染按钮"""
        pass

    @abstractmethod
    def click(self) -> None:
        """点击事件"""
        pass


class WindowsButton(Button):
    """Windows风格按钮"""

    def __init__(self, text: str):
        self.text = text

    def render(self) -> str:
        return f"[Windows按钮: {self.text}]"

    def click(self) -> None:
        print(f"🖱️  点击Windows按钮: {self.text}")


class MacOSButton(Button):
    """macOS风格按钮"""

    def __init__(self, text: str):
        self.text = text

    def render(self) -> str:
        return f"(macOS按钮: {self.text})"

    def click(self) -> None:
        print(f"🖱️  点击macOS按钮: {self.text}")


class LinuxButton(Button):
    """Linux风格按钮"""

    def __init__(self, text: str):
        self.text = text

    def render(self) -> str:
        return f"<Linux按钮: {self.text}>"

    def click(self) -> None:
        print(f"🖱️  点击Linux按钮: {self.text}")


# 注册UI组件
FactoryRegistry.register("windows_button")(WindowsButton)
FactoryRegistry.register("macos_button")(MacOSButton)
FactoryRegistry.register("linux_button")(LinuxButton)


def demo_ui_component_factory() -> None:
    """演示UI组件工厂"""
    print("\n" + "=" * 70)
    print("📦 示例5: UI组件工厂")
    print("=" * 70)

    import platform

    # 根据操作系统创建对应的按钮
    os_name = platform.system().lower()
    button_map = {
        "windows": "windows_button",
        "darwin": "macos_button",  # macOS
        "linux": "linux_button",
    }

    button_type = button_map.get(os_name, "linux_button")
    button = FactoryRegistry.create(button_type, text="确定")

    print(f"   当前系统: {os_name}")
    print(f"   渲染结果: {button.render()}")
    button.click()


# ============================================================================
# 示例6: 序列化器工厂
# ============================================================================


class Serializer(ABC):
    """序列化器抽象类"""

    @abstractmethod
    def serialize(self, data: Any) -> str:
        """序列化数据"""
        pass

    @abstractmethod
    def deserialize(self, data: str) -> Any:
        """反序列化数据"""
        pass


class JSONSerializer(Serializer):
    """JSON序列化器"""

    def serialize(self, data: Any) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    def deserialize(self, data: str) -> Any:
        return json.loads(data)


class XMLSerializer(Serializer):
    """XML序列化器"""

    def serialize(self, data: Any) -> str:
        # 简化的XML序列化
        if isinstance(data, dict):
            items = "".join(f"<{k}>{v}</{k}>" for k, v in data.items())
            return f"<root>{items}</root>"
        return f"<value>{data}</value>"

    def deserialize(self, data: str) -> Any:
        # 简化的XML反序列化
        return {"xml": "parsed data"}


class YAMLSerializer(Serializer):
    """YAML序列化器"""

    def serialize(self, data: Any) -> str:
        # 简化的YAML序列化
        if isinstance(data, dict):
            lines = [f"{k}: {v}" for k, v in data.items()]
            return "\n".join(lines)
        return str(data)

    def deserialize(self, data: str) -> Any:
        # 简化的YAML反序列化
        return {"yaml": "parsed data"}


# 注册序列化器
FactoryRegistry.register("json_serializer")(JSONSerializer)
FactoryRegistry.register("xml_serializer")(XMLSerializer)
FactoryRegistry.register("yaml_serializer")(YAMLSerializer)


def demo_serializer_factory() -> None:
    """演示序列化器工厂"""
    print("\n" + "=" * 70)
    print("📦 示例6: 序列化器工厂")
    print("=" * 70)

    data = {"name": "Alice", "age": 30, "city": "Beijing"}

    for serializer_type in ["json_serializer", "xml_serializer", "yaml_serializer"]:
        print(f"\n▶ 使用 {serializer_type}:")
        serializer = FactoryRegistry.create(serializer_type)
        serialized = serializer.serialize(data)
        print(f"   序列化结果:\n{serialized}")


# ============================================================================
# 主程序
# ============================================================================


def main() -> None:
    """运行所有示例"""
    print("\n" + "=" * 70)
    print("🎯 Factory Method Pattern - 实际应用示例")
    print("=" * 70)

    try:
        demo_database_factory()
        demo_log_handler_factory()
        demo_document_parser_factory()
        demo_message_queue_factory()
        demo_ui_component_factory()
        demo_serializer_factory()

        print("\n" + "=" * 70)
        print("✅ 所有示例运行完成！")
        print("=" * 70)
        print(f"\n📊 已注册的产品类型总数: {len(FactoryRegistry.list_products())}")
        print(f"📋 产品列表: {', '.join(sorted(FactoryRegistry.list_products()))}")

    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

