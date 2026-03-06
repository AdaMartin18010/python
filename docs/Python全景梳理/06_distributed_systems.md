# Python分布式系统设计模型全面指南

> 本文档系统性地梳理Python分布式系统设计中的核心概念、架构模式和实现方案。

---

## 目录

- [Python分布式系统设计模型全面指南](#python分布式系统设计模型全面指南)
  - [目录](#目录)
  - [第一部分：分布式通信](#第一部分分布式通信)
    - [1.1 RPC框架](#11-rpc框架)
      - [1.1.1 gRPC（Protocol Buffers）](#111-grpcprotocol-buffers)
      - [1.1.2 Pyro4/Pyro5](#112-pyro4pyro5)
      - [1.1.3 RPyC](#113-rpyc)
    - [1.2 RESTful API设计](#12-restful-api设计)
      - [1.2.1 Flask/FastAPI实现](#121-flaskfastapi实现)
    - [1.3 消息队列](#13-消息队列)
      - [1.3.1 RabbitMQ（pika）](#131-rabbitmqpika)
      - [1.3.2 Kafka（kafka-python）](#132-kafkakafka-python)
      - [1.3.3 Redis Pub/Sub](#133-redis-pubsub)
  - [第二部分：分布式一致性](#第二部分分布式一致性)
    - [2.1 CAP定理](#21-cap定理)
      - [2.1.1 形式定义和证明](#211-形式定义和证明)
      - [2.1.2 实际系统中的权衡](#212-实际系统中的权衡)
    - [2.2 BASE理论](#22-base理论)
    - [2.3 一致性协议](#23-一致性协议)
      - [2.3.1 Raft（理解层面）](#231-raft理解层面)
      - [2.3.2 Paxos（理解层面）](#232-paxos理解层面)
  - [第三部分：服务发现与注册](#第三部分服务发现与注册)
    - [3.1 服务注册中心](#31-服务注册中心)
      - [3.1.1 Consul](#311-consul)
      - [3.1.2 etcd](#312-etcd)
      - [3.1.3 ZooKeeper（kazoo）](#313-zookeeperkazoo)
  - [第五部分：分布式事务](#第五部分分布式事务)
    - [5.1 两阶段提交（2PC）](#51-两阶段提交2pc)
    - [5.2 TCC（Try-Confirm-Cancel）](#52-tcctry-confirm-cancel)
    - [5.3 Saga模式](#53-saga模式)
    - [5.4 本地消息表](#54-本地消息表)
  - [第六部分：分布式缓存](#第六部分分布式缓存)
    - [6.1 Redis集群](#61-redis集群)
    - [6.2 缓存策略](#62-缓存策略)
      - [6.2.1 缓存穿透、击穿、雪崩](#621-缓存穿透击穿雪崩)
  - [第七部分：数据分片](#第七部分数据分片)
    - [7.1 水平分片](#71-水平分片)
    - [7.2 垂直分片](#72-垂直分片)
    - [7.3 分片策略](#73-分片策略)
  - [第八部分：微服务架构](#第八部分微服务架构)
    - [8.1 服务拆分原则](#81-服务拆分原则)
    - [8.2 API网关](#82-api网关)
    - [8.3 服务网格概念](#83-服务网格概念)
  - [总结](#总结)
    - [关键知识点回顾](#关键知识点回顾)
    - [最佳实践建议](#最佳实践建议)

---

## 第一部分：分布式通信

### 1.1 RPC框架

#### 1.1.1 gRPC（Protocol Buffers）

**概念定义**

gRPC是由Google开发的高性能、开源、通用的RPC框架，基于HTTP/2协议传输，使用Protocol Buffers作为接口定义语言(IDL)和序列化工具。

**核心特性：**

- 基于HTTP/2，支持双向流、头部压缩、多路复用
- 使用Protocol Buffers进行高效的二进制序列化
- 支持四种服务类型：Unary、Server Streaming、Client Streaming、Bidirectional Streaming
- 跨语言支持（Python、Java、Go、C++等）

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                        gRPC 通信架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐      .proto定义      ┌─────────────┐           │
│  │   Client    │◄────────────────────►│   Server    │           │
│  │  (Stub)     │    Protocol Buffers  │  (Service)  │           │
│  └──────┬──────┘                      └──────┬──────┘           │
│         │                                     │                  │
│         │         HTTP/2 + TLS                │                  │
│         │◄───────────────────────────────────►│                  │
│         │                                     │                  │
│  ┌──────▼──────┐                      ┌──────▼──────┐           │
│  │  序列化     │                      │   反序列化  │           │
│  │  Protobuf   │                      │   Protobuf  │           │
│  └─────────────┘                      └─────────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

首先安装依赖：

```bash
pip install grpcio grpcio-tools
```

定义服务（`calculator.proto`）：

```protobuf
syntax = "proto3";

package calculator;

// 定义服务
service Calculator {
    // 一元RPC
    rpc Add (AddRequest) returns (AddResponse);
    rpc Subtract (SubtractRequest) returns (SubtractResponse);

    // 服务端流式RPC
    rpc GenerateNumbers (NumberRange) returns (stream Number);

    // 客户端流式RPC
    rpc SumNumbers (stream Number) returns (SumResponse);

    // 双向流式RPC
    rpc Chat (stream Message) returns (stream Message);
}

// 消息定义
message AddRequest {
    int32 a = 1;
    int32 b = 2;
}

message AddResponse {
    int32 result = 1;
}

message SubtractRequest {
    int32 a = 1;
    int32 b = 2;
}

message SubtractResponse {
    int32 result = 1;
}

message NumberRange {
    int32 start = 1;
    int32 end = 2;
}

message Number {
    int32 value = 1;
}

message SumResponse {
    int32 sum = 1;
}

message Message {
    string sender = 1;
    string content = 2;
    int64 timestamp = 3;
}
```

生成Python代码：

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

服务端实现（`grpc_server.py`）：

```python
"""
gRPC服务端实现 - 计算器服务
"""
from concurrent import futures
import time
import grpc
import calculator_pb2
import calculator_pb2_grpc
from datetime import datetime


class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    """计算器服务实现"""

    def Add(self, request, context):
        """加法运算 - 一元RPC"""
        result = request.a + request.b
        print(f"[Add] {request.a} + {request.b} = {result}")
        return calculator_pb2.AddResponse(result=result)

    def Subtract(self, request, context):
        """减法运算 - 一元RPC"""
        result = request.a - request.b
        print(f"[Subtract] {request.a} - {request.b} = {result}")
        return calculator_pb2.SubtractResponse(result=result)

    def GenerateNumbers(self, request, context):
        """生成数字序列 - 服务端流式RPC"""
        print(f"[GenerateNumbers] Range: {request.start} to {request.end}")
        for i in range(request.start, request.end + 1):
            yield calculator_pb2.Number(value=i)
            time.sleep(0.1)  # 模拟处理延迟

    def SumNumbers(self, request_iterator, context):
        """求和 - 客户端流式RPC"""
        total = 0
        count = 0
        for number in request_iterator:
            total += number.value
            count += 1
            print(f"[SumNumbers] Received: {number.value}")
        print(f"[SumNumbers] Total sum of {count} numbers: {total}")
        return calculator_pb2.SumResponse(sum=total)

    def Chat(self, request_iterator, context):
        """聊天 - 双向流式RPC"""
        print("[Chat] Chat session started")
        for message in request_iterator:
            print(f"[Chat] {message.sender}: {message.content}")
            # 回复消息
            reply = calculator_pb2.Message(
                sender="Server",
                content=f"Echo: {message.content}",
                timestamp=int(datetime.now().timestamp())
            )
            yield reply


def serve(port=50051):
    """启动gRPC服务器"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"gRPC Server started on port {port}")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        print("\nServer stopped")


if __name__ == '__main__':
    serve()
```

客户端实现（`grpc_client.py`）：

```python
"""
gRPC客户端实现 - 计算器服务
"""
import grpc
import calculator_pb2
import calculator_pb2_grpc
from datetime import datetime


class CalculatorClient:
    """gRPC计算器客户端"""

    def __init__(self, target='localhost:50051'):
        self.channel = grpc.insecure_channel(target)
        self.stub = calculator_pb2_grpc.CalculatorStub(self.channel)

    def add(self, a, b):
        """调用加法服务"""
        request = calculator_pb2.AddRequest(a=a, b=b)
        response = self.stub.Add(request)
        return response.result

    def subtract(self, a, b):
        """调用减法服务"""
        request = calculator_pb2.SubtractRequest(a=a, b=b)
        response = self.stub.Subtract(request)
        return response.result

    def generate_numbers(self, start, end):
        """调用服务端流式RPC"""
        request = calculator_pb2.NumberRange(start=start, end=end)
        numbers = []
        for number in self.stub.GenerateNumbers(request):
            numbers.append(number.value)
            print(f"Received: {number.value}")
        return numbers

    def sum_numbers(self, numbers):
        """调用客户端流式RPC"""
        def number_generator():
            for n in numbers:
                yield calculator_pb2.Number(value=n)

        response = self.stub.SumNumbers(number_generator())
        return response.sum

    def chat(self, messages):
        """调用双向流式RPC"""
        def message_generator():
            for msg in messages:
                yield calculator_pb2.Message(
                    sender="Client",
                    content=msg,
                    timestamp=int(datetime.now().timestamp())
                )

        responses = []
        for response in self.stub.Chat(message_generator()):
            responses.append(response)
            print(f"Server: {response.content}")
        return responses

    def close(self):
        """关闭连接"""
        self.channel.close()


def demo():
    """演示gRPC客户端调用"""
    client = CalculatorClient()

    print("=" * 50)
    print("1. 一元RPC - 加法")
    print("=" * 50)
    result = client.add(10, 20)
    print(f"10 + 20 = {result}")

    print("\n" + "=" * 50)
    print("2. 一元RPC - 减法")
    print("=" * 50)
    result = client.subtract(50, 15)
    print(f"50 - 15 = {result}")

    print("\n" + "=" * 50)
    print("3. 服务端流式RPC - 生成数字")
    print("=" * 50)
    numbers = client.generate_numbers(1, 5)
    print(f"Generated numbers: {numbers}")

    print("\n" + "=" * 50)
    print("4. 客户端流式RPC - 求和")
    print("=" * 50)
    total = client.sum_numbers([1, 2, 3, 4, 5])
    print(f"Sum of [1,2,3,4,5] = {total}")

    print("\n" + "=" * 50)
    print("5. 双向流式RPC - 聊天")
    print("=" * 50)
    client.chat(["Hello", "How are you?", "Goodbye"])

    client.close()


if __name__ == '__main__':
    demo()
```

**正例（正确使用）**

```python
"""
gRPC正确使用示例
"""
import grpc
from grpc import RpcError

# ✅ 正确使用连接池和超时设置
channel = grpc.insecure_channel(
    'localhost:50051',
    options=[
        ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50MB
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),
        ('grpc.keepalive_time_ms', 10000),
        ('grpc.keepalive_timeout_ms', 5000),
    ]
)

stub = calculator_pb2_grpc.CalculatorStub(channel)

# ✅ 使用超时和错误处理
try:
    response = stub.Add(
        calculator_pb2.AddRequest(a=10, b=20),
        timeout=5.0,  # 5秒超时
        metadata=(('authorization', 'Bearer token123'),)
    )
except RpcError as e:
    if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        print("请求超时")
    elif e.code() == grpc.StatusCode.UNAVAILABLE:
        print("服务不可用")
    else:
        print(f"RPC错误: {e.details()}")

# ✅ 使用上下文管理器确保资源释放
with grpc.insecure_channel('localhost:50051') as channel:
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    response = stub.Add(calculator_pb2.AddRequest(a=1, b=2))

# ✅ 流式处理大数据集（避免内存问题）
def process_large_dataset():
    """正确处理大数据集的流式传输"""
    for chunk in stub.GenerateNumbers(calculator_pb2.NumberRange(start=1, end=1000000)):
        process_chunk(chunk)  # 立即处理每个块，不缓存所有数据
```

**反例（错误使用）**

```python
"""
gRPC错误使用示例
"""
import grpc

# ❌ 不设置超时，可能导致无限等待
response = stub.Add(calculator_pb2.AddRequest(a=10, b=20))  # 危险！

# ❌ 不处理异常，程序可能崩溃
def bad_call():
    response = stub.Add(calculator_pb2.AddRequest(a=10, b=20))
    return response.result  # 如果RPC失败，这里会抛出异常

# ❌ 创建大量短连接，不重用channel
for i in range(1000):
    channel = grpc.insecure_channel('localhost:50051')  # 每次循环都创建新连接
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    stub.Add(calculator_pb2.AddRequest(a=i, b=i))
    # 没有关闭channel，造成资源泄漏

# ❌ 在流式RPC中缓存所有数据
def bad_streaming():
    all_numbers = list(stub.GenerateNumbers(
        calculator_pb2.NumberRange(start=1, end=10000000)
    ))  # ❌ 内存爆炸！
    return sum(n.value for n in all_numbers)

# ❌ 忽略元数据和上下文信息
def bad_metadata():
    # 没有传递认证信息
    response = stub.ProtectedMethod(calculator_pb2.Request())
    # 应该传递认证token
```

**分布式挑战分析**

| 挑战 | 解决方案 |
|------|----------|
| 服务发现 | 使用Consul/etcd进行服务注册与发现 |
| 负载均衡 | gRPC内置负载均衡器或使用Envoy代理 |
| 熔断降级 | 实现客户端熔断器，失败时快速返回 |
| 链路追踪 | 集成OpenTelemetry/Jaeger |
| 认证授权 | 使用TLS + JWT/OAuth2 |
| 超时控制 | 设置合理的deadline和重试策略 |

---

#### 1.1.2 Pyro4/Pyro5

**概念定义**

Pyro（Python Remote Objects）是Python专用的RPC库，允许Python对象像本地对象一样被远程调用。Pyro5是Pyro4的继任者，使用更现代的Python特性。

**核心特性：**

- 纯Python实现，无需IDL定义
- 支持对象序列化（pickle）
- 内置名称服务（Name Server）
- 支持异步调用和回调
- 自动重新连接和故障转移

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                     Pyro 通信架构                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐         ┌─────────────┐    ┌─────────────┐    │
│  │   Client    │         │ Name Server │    │   Server    │    │
│  │             │         │             │    │             │    │
│  │  Proxy      │◄───────►│  注册表      │◄───│  Daemon     │    │
│  │  (代理)      │  查询   │  名称→URI   │    │  (守护进程)  │    │
│  └──────┬──────┘         └─────────────┘    └──────┬──────┘    │
│         │                                          │            │
│         │              直接通信                     │            │
│         │◄────────────────────────────────────────►│            │
│         │                                          │            │
│  ┌──────▼──────┐                            ┌──────▼──────┐    │
│  │  pickle     │                            │  pickle     │    │
│  │  序列化     │                            │  反序列化   │    │
│  └─────────────┘                            └─────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

安装依赖：

```bash
pip install Pyro5
```

服务端实现（`pyro_server.py`）：

```python
"""
Pyro5服务端实现 - 远程对象服务
"""
import Pyro5.api
import Pyro5.server
import threading
import time
from datetime import datetime


@Pyro5.api.expose
class Calculator(object):
    """远程计算器服务"""

    def __init__(self):
        self._call_count = 0
        self._lock = threading.Lock()

    def add(self, a, b):
        """加法运算"""
        with self._lock:
            self._call_count += 1
        result = a + b
        print(f"[{datetime.now()}] add({a}, {b}) = {result}")
        return result

    def subtract(self, a, b):
        """减法运算"""
        with self._lock:
            self._call_count += 1
        result = a - b
        print(f"[{datetime.now()}] subtract({a}, {b}) = {result}")
        return result

    def multiply(self, a, b):
        """乘法运算"""
        with self._lock:
            self._call_count += 1
        result = a * b
        print(f"[{datetime.now()}] multiply({a}, {b}) = {result}")
        return result

    def divide(self, a, b):
        """除法运算"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        with self._lock:
            self._call_count += 1
        result = a / b
        print(f"[{datetime.now()}] divide({a}, {b}) = {result}")
        return result

    def get_stats(self):
        """获取统计信息"""
        with self._lock:
            return {"call_count": self._call_count}

    @property
    def call_count(self):
        """调用次数属性"""
        with self._lock:
            return self._call_count


@Pyro5.api.expose
class FileService(object):
    """远程文件服务"""

    def __init__(self, base_path="/tmp/pyro_files"):
        import os
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def list_files(self):
        """列出文件"""
        import os
        return os.listdir(self.base_path)

    def read_file(self, filename):
        """读取文件"""
        import os
        filepath = os.path.join(self.base_path, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filename}")
        with open(filepath, 'r') as f:
            return f.read()

    def write_file(self, filename, content):
        """写入文件"""
        import os
        filepath = os.path.join(self.base_path, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return True


def start_server():
    """启动Pyro5服务器"""
    # 启动名称服务器（通常在单独进程中运行）
    # Pyro5.nameserver.start_ns_loop()  # 用于独立启动

    # 创建守护进程
    daemon = Pyro5.server.Daemon()

    # 查找或启动名称服务器
    ns = Pyro5.api.locate_ns()

    # 注册对象
    calculator = Calculator()
    file_service = FileService()

    calculator_uri = daemon.register(calculator)
    file_uri = daemon.register(file_service)

    # 注册到名称服务器
    ns.register("example.calculator", calculator_uri)
    ns.register("example.fileservice", file_uri)

    print(f"Calculator URI: {calculator_uri}")
    print(f"FileService URI: {file_uri}")
    print("Pyro5 Server is ready.")

    # 启动事件循环
    daemon.requestLoop()


if __name__ == "__main__":
    start_server()
```

客户端实现（`pyro_client.py`）：

```python
"""
Pyro5客户端实现
"""
import Pyro5.api
import sys


class PyroClient:
    """Pyro5客户端"""

    def __init__(self, nameserver_host="localhost", nameserver_port=None):
        self.ns = Pyro5.api.locate_ns(nameserver_host, nameserver_port)

    def get_calculator(self):
        """获取计算器代理"""
        uri = self.ns.lookup("example.calculator")
        return Pyro5.api.Proxy(uri)

    def get_file_service(self):
        """获取文件服务代理"""
        uri = self.ns.lookup("example.fileservice")
        return Pyro5.api.Proxy(uri)


def demo_calculator():
    """演示计算器服务"""
    print("=" * 50)
    print("Pyro5 Calculator Demo")
    print("=" * 50)

    client = PyroClient()
    calc = client.get_calculator()

    # 基本运算
    print(f"10 + 20 = {calc.add(10, 20)}")
    print(f"50 - 15 = {calc.subtract(50, 15)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"100 / 4 = {calc.divide(100, 4)}")

    # 获取统计信息
    stats = calc.get_stats()
    print(f"Call count: {stats['call_count']}")
    print(f"Property call_count: {calc.call_count}")

    # 错误处理
    try:
        calc.divide(10, 0)
    except Exception as e:
        print(f"Expected error: {e}")


def demo_file_service():
    """演示文件服务"""
    print("\n" + "=" * 50)
    print("Pyro5 FileService Demo")
    print("=" * 50)

    client = PyroClient()
    fs = client.get_file_service()

    # 写入文件
    fs.write_file("test.txt", "Hello from Pyro5 client!")
    print("File written successfully")

    # 列出文件
    files = fs.list_files()
    print(f"Files: {files}")

    # 读取文件
    content = fs.read_file("test.txt")
    print(f"File content: {content}")


def demo_batch_calls():
    """演示批量调用"""
    print("\n" + "=" * 50)
    print("Pyro5 Batch Calls Demo")
    print("=" * 50)

    client = PyroClient()
    calc = client.get_calculator()

    # 使用_oneway进行异步调用
    print("Making async calls...")
    calc._pyroOneway.add(1, 2)  # 不等待结果
    calc._pyroOneway.multiply(3, 4)

    # 批量调用
    with calc._pyroBatch() as batch:
        batch.add(1, 2)
        batch.add(3, 4)
        batch.multiply(5, 6)

    results = batch()  # 执行批量调用
    print(f"Batch results: {results}")


if __name__ == "__main__":
    demo_calculator()
    demo_file_service()
    demo_batch_calls()
```

**正例（正确使用）**

```python
"""
Pyro5正确使用示例
"""
import Pyro5.api

# ✅ 使用上下文管理器自动管理代理生命周期
with Pyro5.api.Proxy("PYRONAME:example.calculator") as calc:
    result = calc.add(10, 20)
    # 自动关闭连接

# ✅ 使用名称服务而不是硬编码URI
def good_practice():
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("example.calculator")
    with Pyro5.api.Proxy(uri) as calc:
        return calc.add(1, 2)

# ✅ 正确处理异常
with Pyro5.api.Proxy("PYRONAME:example.calculator") as calc:
    try:
        result = calc.divide(10, 0)
    except ValueError as e:
        print(f"Business error: {e}")
    except Pyro5.errors.CommunicationError as e:
        print(f"Communication error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# ✅ 使用异步调用提高性能
calc._pyroOneway.long_running_operation()  # 不阻塞

# ✅ 设置超时
import Pyro5.config
Pyro5.config.COMMTIMEOUT = 5.0  # 5秒超时
```

**反例（错误使用）**

```python
"""
Pyro5错误使用示例
"""
import Pyro5.api

# ❌ 不使用上下文管理器，可能泄漏连接
calc = Pyro5.api.Proxy("PYRONAME:example.calculator")
result = calc.add(1, 2)
# 忘记调用 calc._pyroRelease() 或关闭

# ❌ 硬编码URI，不利于服务发现
calc = Pyro5.api.Proxy("PYRO:obj_abc123@localhost:9090")

# ❌ 不处理异常
def bad_call():
    calc = Pyro5.api.Proxy("PYRONAME:example.calculator")
    return calc.risky_operation()  # 可能抛出异常

# ❌ 在循环中重复创建代理
for i in range(100):
    calc = Pyro5.api.Proxy("PYRONAME:example.calculator")  # 每次循环都创建
    calc.add(i, i)
    # 没有释放

# ❌ 传递不可序列化的对象
def bad_serialization():
    calc = Pyro5.api.Proxy("PYRONAME:example.calculator")
    # 传递lambda或本地函数会失败
    result = calc.process(lambda x: x * 2)  # ❌ pickle错误
```

---

#### 1.1.3 RPyC

**概念定义**

RPyC（Remote Python Call）是一个透明、对称的Python RPC库，允许在远程Python解释器中执行代码，就像本地执行一样。

**核心特性：**

- 透明远程调用，语法与本地调用完全一致
- 支持双向通信（客户端和服务器可以互相调用）
- 支持netref（网络引用），可以传递复杂对象
- 内置服务发现和认证
- 支持SSL/TLS加密

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                     RPyC 通信架构                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐                      ┌─────────────┐           │
│  │   Client    │                      │   Server    │           │
│  │             │                      │             │           │
│  │  conn.root  │◄────────────────────►│  Service    │           │
│  │  (透明访问)  │    brine序列化        │  (暴露对象)  │           │
│  └──────┬──────┘                      └──────┬──────┘           │
│         │                                     │                  │
│         │         TCP/SSL                     │                  │
│         │◄───────────────────────────────────►│                  │
│         │                                     │                  │
│  ┌──────▼──────┐                      ┌──────▼──────┐           │
│  │  netref     │                      │  远程执行   │           │
│  │  网络引用   │                      │  代码执行   │           │
│  └─────────────┘                      └─────────────┘           │
│                                                                  │
│  特点: 透明代理，支持双向调用，可以传递任意Python对象            │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

安装依赖：

```bash
pip install rpyc
```

服务端实现（`rpyc_server.py`）：

```python
"""
RPyC服务端实现
"""
import rpyc
from rpyc.utils.server import ThreadedServer
from datetime import datetime
import threading


class CalculatorService(rpyc.Service):
    """计算器服务"""

    def __init__(self):
        self._call_count = 0
        self._lock = threading.Lock()

    def on_connect(self, conn):
        """客户端连接时调用"""
        print(f"[{datetime.now()}] Client connected: {conn}")

    def on_disconnect(self, conn):
        """客户端断开时调用"""
        print(f"[{datetime.now()}] Client disconnected: {conn}")

    def exposed_add(self, a, b):
        """暴露的加法方法"""
        with self._lock:
            self._call_count += 1
        result = a + b
        print(f"[{datetime.now()}] add({a}, {b}) = {result}")
        return result

    def exposed_subtract(self, a, b):
        """暴露的减法方法"""
        with self._lock:
            self._call_count += 1
        return a - b

    def exposed_multiply(self, a, b):
        """暴露的乘法方法"""
        with self._lock:
            self._call_count += 1
        return a * b

    def exposed_divide(self, a, b):
        """暴露的除法方法"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        with self._lock:
            self._call_count += 1
        return a / b

    def exposed_get_stats(self):
        """获取统计信息"""
        with self._lock:
            return {"call_count": self._call_count}

    def exposed_execute(self, code):
        """执行Python代码（危险！仅用于演示）"""
        # 注意：生产环境不应该暴露此方法
        return eval(code)


class FileSystemService(rpyc.Service):
    """文件系统服务"""

    def __init__(self, root_dir="/tmp/rpyc_fs"):
        import os
        self.root_dir = root_dir
        os.makedirs(root_dir, exist_ok=True)

    def exposed_list_dir(self, path=""):
        """列出目录"""
        import os
        full_path = os.path.join(self.root_dir, path)
        return os.listdir(full_path)

    def exposed_read_file(self, filename):
        """读取文件"""
        import os
        filepath = os.path.join(self.root_dir, filename)
        with open(filepath, 'r') as f:
            return f.read()

    def exposed_write_file(self, filename, content):
        """写入文件"""
        import os
        filepath = os.path.join(self.root_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return True


class SecureService(rpyc.Service):
    """带认证的服务"""

    def __init__(self, valid_token="secret123"):
        self.valid_token = valid_token
        self._authenticated = False

    def exposed_authenticate(self, token):
        """认证"""
        if token == self.valid_token:
            self._authenticated = True
            return True
        return False

    def exposed_secure_operation(self):
        """安全操作"""
        if not self._authenticated:
            raise PermissionError("Not authenticated")
        return "Secret data"


def start_server(port=18861):
    """启动RPyC服务器"""
    server = ThreadedServer(
        CalculatorService,
        port=port,
        protocol_config={
            'allow_public_attrs': True,
            'allow_pickle': True,
        }
    )
    print(f"RPyC Server started on port {port}")
    server.start()


if __name__ == "__main__":
    start_server()
```

客户端实现（`rpyc_client.py`）：

```python
"""
RPyC客户端实现
"""
import rpyc
from contextlib import contextmanager


@contextmanager
def rpyc_connection(host="localhost", port=18861):
    """RPyC连接上下文管理器"""
    conn = rpyc.connect(host, port)
    try:
        yield conn
    finally:
        conn.close()


class RPyCClient:
    """RPyC客户端"""

    def __init__(self, host="localhost", port=18861):
        self.host = host
        self.port = port

    def call(self, method_name, *args, **kwargs):
        """通用调用方法"""
        with rpyc_connection(self.host, self.port) as conn:
            method = getattr(conn.root, method_name)
            return method(*args, **kwargs)


def demo_basic():
    """基本调用演示"""
    print("=" * 50)
    print("RPyC Basic Demo")
    print("=" * 50)

    with rpyc_connection() as conn:
        calc = conn.root

        # 基本运算
        print(f"10 + 20 = {calc.exposed_add(10, 20)}")
        print(f"50 - 15 = {calc.exposed_subtract(50, 15)}")
        print(f"6 * 7 = {calc.exposed_multiply(6, 7)}")
        print(f"100 / 4 = {calc.exposed_divide(100, 4)}")

        # 获取统计
        stats = calc.exposed_get_stats()
        print(f"Stats: {stats}")


def demo_advanced():
    """高级功能演示"""
    print("\n" + "=" * 50)
    print("RPyC Advanced Demo")
    print("=" * 50)

    with rpyc_connection() as conn:
        calc = conn.root

        # 执行代码
        result = calc.exposed_execute("2 + 2")
        print(f"execute('2 + 2') = {result}")

        # 使用内置模块
        import rpyc.utils.helpers
        # RPyC允许访问远程的Python内置函数


def demo_async():
    """异步调用演示"""
    print("\n" + "=" * 50)
    print("RPyC Async Demo")
    print("=" * 50)

    with rpyc_connection() as conn:
        calc = conn.root

        # 异步调用
        async_result = rpyc.async_(calc.exposed_add)(10, 20)
        print(f"Async call sent, waiting...")
        result = async_result.value  # 阻塞等待结果
        print(f"Async result: {result}")


def demo_callback():
    """回调演示 - RPyC支持双向调用"""
    print("\n" + "=" * 50)
    print("RPyC Callback Demo")
    print("=" * 50)

    # 创建一个可以被远程调用的回调对象
    class Callback:
        def __init__(self):
            self.results = []

        def notify(self, message):
            print(f"Callback received: {message}")
            self.results.append(message)
            return f"Ack: {message}"

    # 注意：这需要服务器支持回调
    print("Callback pattern requires bidirectional communication setup")


def demo_error_handling():
    """错误处理演示"""
    print("\n" + "=" * 50)
    print("RPyC Error Handling Demo")
    print("=" * 50)

    with rpyc_connection() as conn:
        calc = conn.root

        try:
            result = calc.exposed_divide(10, 0)
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
        except Exception as e:
            print(f"Caught exception: {type(e).__name__}: {e}")


if __name__ == "__main__":
    demo_basic()
    demo_advanced()
    demo_async()
    demo_callback()
    demo_error_handling()
```

**正例（正确使用）**

```python
"""
RPyC正确使用示例
"""
import rpyc

# ✅ 使用上下文管理器确保连接关闭
with rpyc.connect("localhost", 18861) as conn:
    result = conn.root.exposed_add(10, 20)

# ✅ 异步调用避免阻塞
async_result = rpyc.async_(conn.root.long_operation)()
# 做其他事情...
result = async_result.value  # 获取结果

# ✅ 使用回调进行双向通信
class MyCallback:
    def notify(self, msg):
        print(f"Received: {msg}")

callback = MyCallback()
conn.root.register_callback(callback)

# ✅ 配置安全选项
conn = rpyc.connect(
    "localhost", 18861,
    config={'allow_pickle': False}  # 禁用pickle防止反序列化攻击
)

# ✅ 使用SSL加密
import ssl
context = ssl.create_default_context()
conn = rpyc.ssl_connect("localhost", 18862, ssl_ctx=context)
```

**反例（错误使用）**

```python
"""
RPyC错误使用示例
"""
import rpyc

# ❌ 不关闭连接
conn = rpyc.connect("localhost", 18861)
result = conn.root.add(1, 2)
# 忘记 conn.close()

# ❌ 暴露危险方法（如eval）
class BadService(rpyc.Service):
    def exposed_run_any_code(self, code):
        return eval(code)  # 严重安全风险！

# ❌ 不验证输入
result = conn.root.process(user_input)  # 可能包含恶意代码

# ❌ 在循环中重复创建连接
for i in range(100):
    conn = rpyc.connect("localhost", 18861)  # 每次都新建连接
    conn.root.add(i, i)
    conn.close()

# ❌ 不处理网络异常
def bad_network_call():
    conn = rpyc.connect("localhost", 18861)
    return conn.root.operation()  # 网络失败时会抛出异常
```

---

### 1.2 RESTful API设计

#### 1.2.1 Flask/FastAPI实现

**概念定义**

REST（Representational State Transfer）是一种软件架构风格，用于设计网络应用程序。RESTful API使用HTTP协议的标准方法（GET、POST、PUT、DELETE等）来操作资源。

**RESTful设计原则：**

- 资源识别：每个资源有唯一的URI标识
- 统一接口：使用标准HTTP方法
- 无状态：每个请求包含所有必要信息
- 可缓存：响应可以被客户端缓存
- 分层系统：客户端不需要知道是否直接连接到服务器

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                   RESTful API 架构                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐         HTTP/HTTPS        ┌─────────────┐      │
│  │   Client    │◄─────────────────────────►│   Server    │      │
│  │             │                           │             │      │
│  │  GET        │                           │  Router     │      │
│  │  POST       │                           │  Controller │      │
│  │  PUT        │                           │  Service    │      │
│  │  DELETE     │                           │  Model      │      │
│  └─────────────┘                           └──────┬──────┘      │
│                                                    │             │
│                                           ┌───────▼───────┐     │
│                                           │   Database    │     │
│                                           │  (持久化层)    │     │
│                                           └───────────────┘     │
│                                                                  │
│  URL设计示例:                                                    │
│  GET    /api/v1/users          - 获取用户列表                    │
│  GET    /api/v1/users/123      - 获取用户详情                    │
│  POST   /api/v1/users          - 创建用户                        │
│  PUT    /api/v1/users/123      - 更新用户                        │
│  DELETE /api/v1/users/123      - 删除用户                        │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现 - Flask版本**

安装依赖：

```bash
pip install flask flask-restful flask-jwt-extended
```

Flask RESTful API实现（`flask_api.py`）：

```python
"""
Flask RESTful API实现
"""
from flask import Flask, request, jsonify, g
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps
from datetime import datetime, timedelta
import uuid
import hashlib


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

api = Api(app)
jwt = JWTManager(app)

# 模拟数据库
users_db = {}
posts_db = {}


# ==================== 数据模型 ====================

class User:
    """用户模型"""
    def __init__(self, username, email, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.now().isoformat()
        self.is_active = True

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash_password(password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'is_active': self.is_active
        }


class Post:
    """文章模型"""
    def __init__(self, title, content, author_id):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# ==================== 认证装饰器 ====================

def admin_required(fn):
    """管理员权限装饰器"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = users_db.get(current_user_id)
        if not user or not getattr(user, 'is_admin', False):
            return {'error': 'Admin permission required'}, 403
        return fn(*args, **kwargs)
    return wrapper


# ==================== API资源 ====================

class UserListResource(Resource):
    """用户列表资源"""

    def get(self):
        """获取用户列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # 分页
        all_users = list(users_db.values())
        start = (page - 1) * per_page
        end = start + per_page
        users = all_users[start:end]

        return {
            'users': [u.to_dict() for u in users],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(all_users),
                'pages': (len(all_users) + per_page - 1) // per_page
            }
        }, 200

    def post(self):
        """创建用户"""
        data = request.get_json()

        # 验证
        if not data or 'username' not in data or 'password' not in data:
            return {'error': 'Username and password are required'}, 400

        # 检查用户名是否已存在
        if any(u.username == data['username'] for u in users_db.values()):
            return {'error': 'Username already exists'}, 409

        # 创建用户
        user = User(
            username=data['username'],
            email=data.get('email', ''),
            password=data['password']
        )
        users_db[user.id] = user

        return user.to_dict(), 201


class UserResource(Resource):
    """单个用户资源"""

    def get(self, user_id):
        """获取用户详情"""
        user = users_db.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    def put(self, user_id):
        """更新用户"""
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return {'error': 'Permission denied'}, 403

        user = users_db.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()
        if 'email' in data:
            user.email = data['email']

        return user.to_dict(), 200

    @jwt_required()
    def delete(self, user_id):
        """删除用户"""
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return {'error': 'Permission denied'}, 403

        if user_id not in users_db:
            return {'error': 'User not found'}, 404

        del users_db[user_id]
        return {'message': 'User deleted'}, 200


class PostListResource(Resource):
    """文章列表资源"""

    def get(self):
        """获取文章列表"""
        posts = list(posts_db.values())
        return {'posts': [p.to_dict() for p in posts]}, 200

    @jwt_required()
    def post(self):
        """创建文章"""
        data = request.get_json()

        if not data or 'title' not in data:
            return {'error': 'Title is required'}, 400

        current_user_id = get_jwt_identity()
        post = Post(
            title=data['title'],
            content=data.get('content', ''),
            author_id=current_user_id
        )
        posts_db[post.id] = post

        return post.to_dict(), 201


class PostResource(Resource):
    """单个文章资源"""

    def get(self, post_id):
        """获取文章详情"""
        post = posts_db.get(post_id)
        if not post:
            return {'error': 'Post not found'}, 404
        return post.to_dict(), 200

    @jwt_required()
    def put(self, post_id):
        """更新文章"""
        post = posts_db.get(post_id)
        if not post:
            return {'error': 'Post not found'}, 404

        current_user_id = get_jwt_identity()
        if post.author_id != current_user_id:
            return {'error': 'Permission denied'}, 403

        data = request.get_json()
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        post.updated_at = datetime.now().isoformat()

        return post.to_dict(), 200

    @jwt_required()
    def delete(self, post_id):
        """删除文章"""
        post = posts_db.get(post_id)
        if not post:
            return {'error': 'Post not found'}, 404

        current_user_id = get_jwt_identity()
        if post.author_id != current_user_id:
            return {'error': 'Permission denied'}, 403

        del posts_db[post_id]
        return {'message': 'Post deleted'}, 200


class AuthResource(Resource):
    """认证资源"""

    def post(self):
        """用户登录"""
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return {'error': 'Username and password are required'}, 400

        # 查找用户
        user = None
        for u in users_db.values():
            if u.username == data['username']:
                user = u
                break

        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401

        # 创建JWT令牌
        access_token = create_access_token(identity=user.id)

        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'user': user.to_dict()
        }, 200


class HealthResource(Resource):
    """健康检查资源"""

    def get(self):
        """健康检查"""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }, 200


# 注册路由
api.add_resource(HealthResource, '/api/v1/health')
api.add_resource(AuthResource, '/api/v1/auth/login')
api.add_resource(UserListResource, '/api/v1/users')
api.add_resource(UserResource, '/api/v1/users/<string:user_id>')
api.add_resource(PostListResource, '/api/v1/posts')
api.add_resource(PostResource, '/api/v1/posts/<string:post_id>')


# 错误处理
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Resource not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500


# 初始化测试数据
@app.before_first_request
def init_data():
    """初始化测试数据"""
    # 创建测试用户
    test_user = User('admin', 'admin@example.com', 'admin123')
    test_user.is_admin = True
    users_db[test_user.id] = test_user
    print(f"Created test user: {test_user.username} (ID: {test_user.id})")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Python实现 - FastAPI版本**

安装依赖：

```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]
```

FastAPI实现（`fastapi_app.py`）：

```python
"""
FastAPI RESTful API实现
"""
from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import uuid


# ==================== 配置 ====================

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


# ==================== Pydantic模型 ====================

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """用户更新模型"""
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """用户响应模型"""
    id: str
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    """文章基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = ""


class PostCreate(PostBase):
    """文章创建模型"""
    pass


class PostUpdate(BaseModel):
    """文章更新模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None


class PostResponse(PostBase):
    """文章响应模型"""
    id: str
    author_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    """令牌模型"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """令牌数据模型"""
    user_id: Optional[str] = None


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Query(1, ge=1)
    per_page: int = Query(10, ge=1, le=100)


# ==================== 模拟数据库 ====================

users_db = {}
posts_db = {}


# ==================== 工具函数 ====================

def verify_password(plain_password, hashed_password):
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """获取密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = users_db.get(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


# ==================== FastAPI应用 ====================

app = FastAPI(
    title="Distributed Systems API",
    description="A RESTful API built with FastAPI",
    version="1.0.0"
)


# ==================== 用户API ====================

@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """创建用户"""
    # 检查用户名是否已存在
    if any(u['username'] == user.username for u in users_db.values()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    user_id = str(uuid.uuid4())
    user_data = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
        "created_at": datetime.now(),
        "is_active": True,
        "is_admin": False
    }
    users_db[user_id] = user_data

    return UserResponse(
        id=user_id,
        username=user.username,
        email=user.email,
        created_at=user_data["created_at"],
        is_active=True
    )


@app.get("/api/v1/users", response_model=dict)
async def list_users(
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user)
):
    """获取用户列表"""
    all_users = list(users_db.values())
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page
    users = all_users[start:end]

    return {
        "users": [
            UserResponse(
                id=u["id"],
                username=u["username"],
                email=u["email"],
                created_at=u["created_at"],
                is_active=u["is_active"]
            ) for u in users
        ],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": len(all_users),
            "pages": (len(all_users) + pagination.per_page - 1) // pagination.per_page
        }
    }


@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """获取用户详情"""
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        created_at=user["created_at"],
        is_active=user["is_active"]
    )


@app.put("/api/v1/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新用户"""
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    user = users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_update.email is not None:
        user["email"] = user_update.email

    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        created_at=user["created_at"],
        is_active=user["is_active"]
    )


@app.delete("/api/v1/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除用户"""
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    del users_db[user_id]
    return {"message": "User deleted successfully"}


# ==================== 文章API ====================

@app.post("/api/v1/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建文章"""
    post_id = str(uuid.uuid4())
    now = datetime.now()
    post_data = {
        "id": post_id,
        "title": post.title,
        "content": post.content,
        "author_id": current_user["id"],
        "created_at": now,
        "updated_at": now
    }
    posts_db[post_id] = post_data

    return PostResponse(
        id=post_id,
        title=post.title,
        content=post.content,
        author_id=current_user["id"],
        created_at=now,
        updated_at=now
    )


@app.get("/api/v1/posts", response_model=dict)
async def list_posts(pagination: PaginationParams = Depends()):
    """获取文章列表"""
    all_posts = list(posts_db.values())
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page
    posts = all_posts[start:end]

    return {
        "posts": [
            PostResponse(
                id=p["id"],
                title=p["title"],
                content=p["content"],
                author_id=p["author_id"],
                created_at=p["created_at"],
                updated_at=p["updated_at"]
            ) for p in posts
        ],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": len(all_posts),
            "pages": (len(all_posts) + pagination.per_page - 1) // pagination.per_page
        }
    }


@app.get("/api/v1/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    """获取文章详情"""
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return PostResponse(
        id=post["id"],
        title=post["title"],
        content=post["content"],
        author_id=post["author_id"],
        created_at=post["created_at"],
        updated_at=post["updated_at"]
    )


@app.put("/api/v1/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_update: PostUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新文章"""
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post["author_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    if post_update.title is not None:
        post["title"] = post_update.title
    if post_update.content is not None:
        post["content"] = post_update.content
    post["updated_at"] = datetime.now()

    return PostResponse(
        id=post["id"],
        title=post["title"],
        content=post["content"],
        author_id=post["author_id"],
        created_at=post["created_at"],
        updated_at=post["updated_at"]
    )


@app.delete("/api/v1/posts/{post_id}")
async def delete_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除文章"""
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post["author_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    del posts_db[post_id]
    return {"message": "Post deleted successfully"}


# ==================== 认证API ====================

@app.post("/api/v1/auth/login", response_model=Token)
async def login(credentials: dict):
    """用户登录"""
    username = credentials.get("username")
    password = credentials.get("password")

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required"
        )

    # 查找用户
    user = None
    for u in users_db.values():
        if u["username"] == username:
            user = u
            break

    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ==================== 健康检查 ====================

@app.get("/api/v1/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


# ==================== 启动事件 ====================

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    # 创建测试用户
    test_user_id = str(uuid.uuid4())
    users_db[test_user_id] = {
        "id": test_user_id,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("admin123"),
        "created_at": datetime.now(),
        "is_active": True,
        "is_admin": True
    }
    print(f"Created test user: admin (ID: {test_user_id})")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**正例（正确使用）**

```python
"""
RESTful API正确使用示例
"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import httpx

# ✅ 使用正确的HTTP状态码
@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: str):
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ✅ 使用Pydantic进行输入验证
class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

@app.post("/api/v1/users", status_code=201)
async def create_user(request: CreateUserRequest):
    # 输入已自动验证
    return await create_user_service(request)

# ✅ 使用依赖注入进行认证
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

@app.get("/api/v1/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hello {user.username}"}

# ✅ 实现幂等操作
@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: str, data: UserUpdate):
    # PUT应该是幂等的，多次调用结果相同
    return await update_or_create_user(user_id, data)

# ✅ 使用异步HTTP客户端
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# ✅ 实现适当的错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

**反例（错误使用）**

```python
"""
RESTful API错误使用示例
"""
from flask import Flask, request, jsonify

# ❌ 不使用HTTP状态码
@app.route('/api/users', methods=['POST'])
def create_user():
    user = create_user_logic(request.json)
    return jsonify(user)  # 总是返回200，应该返回201

# ❌ 不使用输入验证
@app.route('/api/users', methods=['POST'])
def create_user_bad():
    data = request.json
    # 没有验证data是否包含必要字段
    user = User(username=data['username'])  # 可能KeyError
    return jsonify(user.to_dict())

# ❌ 在URL中使用动词
@app.route('/api/users/create', methods=['POST'])  # 应该是 /api/users
def create_user_verb():
    pass

# ❌ 不使用复数名词
@app.route('/api/user/<id>')  # 应该是 /api/users/<id>
def get_user_bad(id):
    pass

# ❌ 混合业务逻辑在路由中
@app.route('/api/orders', methods=['POST'])
def create_order():
    # 太多业务逻辑在路由中
    data = request.json
    user = db.query(User).get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    product = db.query(Product).get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    if product.stock < data['quantity']:
        return jsonify({'error': 'Insufficient stock'}), 400
    # ... 更多逻辑
    return jsonify(order.to_dict())

# ❌ 不使用HTTPS
app.run(ssl_context=None)  # 生产环境应该使用SSL

# ❌ 暴露敏感信息在错误中
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'error': str(error),  # 可能暴露内部实现细节
        'traceback': traceback.format_exc()  # 严重安全风险！
    }), 500
```

---

### 1.3 消息队列

#### 1.3.1 RabbitMQ（pika）

**概念定义**

RabbitMQ是一个开源的消息代理软件（消息队列），实现了高级消息队列协议（AMQP）。它支持多种消息模式，包括点对点、发布/订阅、路由和主题。

**核心概念：**

- **Exchange（交换机）**：接收消息并根据路由规则转发到队列
- **Queue（队列）**：存储消息的缓冲区
- **Binding（绑定）**：交换机和队列之间的关联规则
- **Routing Key（路由键）**：用于消息路由的标识

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                    RabbitMQ 消息队列架构                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │  Producer   │      │   Exchange  │      │   Queue     │     │
│  │   (生产者)   │─────►│  (交换机)    │─────►│   (队列)    │     │
│  └─────────────┘      └──────┬──────┘      └──────┬──────┘     │
│                              │                    │             │
│                    ┌─────────┴─────────┐         │             │
│                    │  Routing Rules    │         │             │
│                    │  direct/topic/    │         │             │
│                    │  fanout/headers   │         │             │
│                    └─────────┬─────────┘         │             │
│                              │                    │             │
│  ┌─────────────┐      ┌──────▼──────┐      ┌─────▼─────┐       │
│  │  Consumer   │◄─────│   Queue     │◄─────│  Queue    │       │
│  │   (消费者)   │      │   (队列)    │      │  (队列)   │       │
│  └─────────────┘      └─────────────┘      └───────────┘       │
│                                                                  │
│  消息模式:                                                       │
│  1. Direct: 精确匹配路由键                                       │
│  2. Topic: 模式匹配路由键 (order.*, order.create)               │
│  3. Fanout: 广播到所有绑定队列                                   │
│  4. Headers: 根据消息头属性匹配                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

安装依赖：

```bash
pip install pika
```

生产者实现（`rabbitmq_producer.py`）：

```python
"""
RabbitMQ生产者实现
"""
import pika
import json
import uuid
from datetime import datetime
from contextlib import contextmanager


class RabbitMQConnection:
    """RabbitMQ连接管理"""

    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = None
        self.channel = None

    def connect(self):
        """建立连接"""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=self.credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            self.channel = self.connection.channel()
        return self

    def close(self):
        """关闭连接"""
        if self.channel and not self.channel.is_closed:
            self.channel.close()
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class MessageProducer:
    """消息生产者"""

    EXCHANGE_TYPES = ['direct', 'topic', 'fanout', 'headers']

    def __init__(self, connection: RabbitMQConnection):
        self.connection = connection

    def declare_exchange(self, exchange_name, exchange_type='direct', durable=True):
        """声明交换机"""
        if exchange_type not in self.EXCHANGE_TYPES:
            raise ValueError(f"Invalid exchange type: {exchange_type}")

        self.connection.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            durable=durable
        )
        print(f"Exchange '{exchange_name}' declared ({exchange_type})")

    def declare_queue(self, queue_name, durable=True, exclusive=False, auto_delete=False):
        """声明队列"""
        result = self.connection.channel.queue_declare(
            queue=queue_name,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete
        )
        print(f"Queue '{queue_name}' declared, message count: {result.method.message_count}")
        return result

    def bind_queue(self, queue_name, exchange_name, routing_key=''):
        """绑定队列到交换机"""
        self.connection.channel.queue_bind(
            queue=queue_name,
            exchange=exchange_name,
            routing_key=routing_key
        )
        print(f"Queue '{queue_name}' bound to exchange '{exchange_name}' with key '{routing_key}'")

    def publish(self, exchange_name, routing_key, message, headers=None, priority=None):
        """发布消息"""
        message_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        properties = pika.BasicProperties(
            message_id=message_id,
            timestamp=int(datetime.now().timestamp()),
            content_type='application/json',
            delivery_mode=2,  # 持久化
            headers=headers,
            priority=priority
        )

        body = json.dumps({
            'message_id': message_id,
            'timestamp': timestamp,
            'data': message
        })

        self.connection.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=body.encode('utf-8'),
            properties=properties
        )

        print(f"Message published: {message_id}")
        return message_id

    def send_rpc_request(self, queue_name, message, timeout=30):
        """发送RPC请求"""
        # 创建临时回调队列
        result = self.connection.channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue

        corr_id = str(uuid.uuid4())
        response = None

        def on_response(ch, method, props, body):
            nonlocal response
            if corr_id == props.correlation_id:
                response = json.loads(body)

        self.connection.channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_response,
            auto_ack=True
        )

        self.connection.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=corr_id,
                content_type='application/json'
            ),
            body=json.dumps(message).encode('utf-8')
        )

        # 等待响应
        start_time = datetime.now()
        while response is None:
            self.connection.connection.process_data_events(time_limit=0.1)
            if (datetime.now() - start_time).seconds > timeout:
                raise TimeoutError("RPC request timeout")

        return response


# ==================== 使用示例 ====================

def demo_direct_exchange():
    """Direct Exchange示例"""
    print("\n" + "=" * 50)
    print("Direct Exchange Demo")
    print("=" * 50)

    with RabbitMQConnection() as conn:
        producer = MessageProducer(conn)

        # 声明交换机和队列
        producer.declare_exchange('orders_direct', 'direct')
        producer.declare_queue('orders_created')
        producer.declare_queue('orders_cancelled')

        # 绑定队列
        producer.bind_queue('orders_created', 'orders_direct', 'order.created')
        producer.bind_queue('orders_cancelled', 'orders_direct', 'order.cancelled')

        # 发送消息
        producer.publish('orders_direct', 'order.created', {
            'order_id': 'ORD-001',
            'user_id': 'USER-001',
            'amount': 100.00
        })

        producer.publish('orders_direct', 'order.cancelled', {
            'order_id': 'ORD-002',
            'user_id': 'USER-002',
            'reason': 'Customer request'
        })


def demo_topic_exchange():
    """Topic Exchange示例"""
    print("\n" + "=" * 50)
    print("Topic Exchange Demo")
    print("=" * 50)

    with RabbitMQConnection() as conn:
        producer = MessageProducer(conn)

        # 声明Topic交换机
        producer.declare_exchange('logs_topic', 'topic')
        producer.declare_queue('all_logs')
        producer.declare_queue('error_logs')
        producer.declare_queue('kernel_logs')

        # 绑定队列（使用通配符）
        producer.bind_queue('all_logs', 'logs_topic', '#')  # 所有消息
        producer.bind_queue('error_logs', 'logs_topic', '*.error')  # 所有error级别
        producer.bind_queue('kernel_logs', 'logs_topic', 'kernel.*')  # 所有kernel相关

        # 发送消息
        producer.publish('logs_topic', 'kernel.error', {
            'level': 'ERROR',
            'message': 'Kernel panic!',
            'timestamp': datetime.now().isoformat()
        })

        producer.publish('logs_topic', 'app.info', {
            'level': 'INFO',
            'message': 'Application started',
            'timestamp': datetime.now().isoformat()
        })


def demo_fanout_exchange():
    """Fanout Exchange示例（广播）"""
    print("\n" + "=" * 50)
    print("Fanout Exchange Demo")
    print("=" * 50)

    with RabbitMQConnection() as conn:
        producer = MessageProducer(conn)

        # 声明Fanout交换机（广播模式）
        producer.declare_exchange('notifications_fanout', 'fanout')
        producer.declare_queue('email_notifications')
        producer.declare_queue('sms_notifications')
        producer.declare_queue('push_notifications')

        # 绑定队列（Fanout忽略routing_key）
        producer.bind_queue('email_notifications', 'notifications_fanout')
        producer.bind_queue('sms_notifications', 'notifications_fanout')
        producer.bind_queue('push_notifications', 'notifications_fanout')

        # 发送广播消息
        producer.publish('notifications_fanout', '', {
            'type': 'system_alert',
            'message': 'System maintenance scheduled',
            'time': '2024-01-01 02:00:00'
        })


def demo_delayed_message():
    """延迟消息示例（使用死信队列）"""
    print("\n" + "=" * 50)
    print("Delayed Message Demo")
    print("=" * 50)

    with RabbitMQConnection() as conn:
        producer = MessageProducer(conn)

        # 声明主队列和死信队列
        producer.declare_queue('tasks_delayed', arguments={
            'x-message-ttl': 60000,  # 60秒TTL
            'x-dead-letter-exchange': '',
            'x-dead-letter-routing-key': 'tasks_main'
        })

        producer.declare_queue('tasks_main')

        # 发送延迟消息
        producer.publish('', 'tasks_delayed', {
            'task_id': 'TASK-001',
            'action': 'send_reminder',
            'delay_seconds': 60
        })

        print("Delayed message sent (will be processed after 60s)")


if __name__ == '__main__':
    demo_direct_exchange()
    demo_topic_exchange()
    demo_fanout_exchange()
    demo_delayed_message()
```

消费者实现（`rabbitmq_consumer.py`）：

```python
"""
RabbitMQ消费者实现
"""
import pika
import json
import threading
import signal
import sys
from datetime import datetime
from typing import Callable, Dict, Any


class MessageConsumer:
    """消息消费者"""

    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = None
        self.channel = None
        self.consuming = False
        self.message_count = 0
        self.error_count = 0

    def connect(self):
        """建立连接"""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=self.credentials,
                heartbeat=600
            )
        )
        self.channel = self.connection.channel()

        # 设置QoS，每次只接收一条消息
        self.channel.basic_qos(prefetch_count=1)
        return self

    def close(self):
        """关闭连接"""
        self.consuming = False
        if self.channel and not self.channel.is_closed:
            self.channel.close()
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def create_message_handler(self, processor: Callable[[Dict], Any]):
        """创建消息处理器"""
        def handler(ch, method, properties, body):
            try:
                # 解析消息
                message = json.loads(body.decode('utf-8'))
                message_id = message.get('message_id', 'unknown')

                print(f"[{datetime.now()}] Received message: {message_id}")
                print(f"  Exchange: {method.exchange}")
                print(f"  Routing Key: {method.routing_key}")
                print(f"  Data: {message.get('data')}")

                # 处理消息
                result = processor(message.get('data', {}))

                # 确认消息
                ch.basic_ack(delivery_tag=method.delivery_tag)
                self.message_count += 1

                print(f"  ✓ Message processed successfully")

            except Exception as e:
                print(f"  ✗ Error processing message: {e}")
                self.error_count += 1

                # 拒绝消息，重新入队
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        return handler

    def consume(self, queue_name: str, processor: Callable[[Dict], Any], auto_ack=False):
        """消费消息"""
        self.connect()

        handler = self.create_message_handler(processor)

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=handler,
            auto_ack=auto_ack
        )

        print(f"[*] Waiting for messages from queue: {queue_name}")
        print(f"[*] Press Ctrl+C to exit")

        self.consuming = True

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
        finally:
            self.close()
            print(f"[*] Total messages processed: {self.message_count}")
            print(f"[*] Total errors: {self.error_count}")

    def consume_multiple(self, queue_processors: Dict[str, Callable[[Dict], Any]]):
        """从多个队列消费消息"""
        self.connect()

        for queue_name, processor in queue_processors.items():
            handler = self.create_message_handler(processor)
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=handler,
                auto_ack=False
            )
            print(f"[*] Registered consumer for queue: {queue_name}")

        print(f"[*] Waiting for messages from {len(queue_processors)} queues")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
        finally:
            self.close()


class RPCServer:
    """RPC服务器"""

    def __init__(self, queue_name: str, host='localhost', port=5672):
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None
        self.handlers = {}

    def register_handler(self, method_name: str, handler: Callable):
        """注册RPC处理器"""
        self.handlers[method_name] = handler

    def connect(self):
        """建立连接"""
        credentials = pika.PlainCredentials('guest', 'guest')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

        return self

    def on_request(self, ch, method, props, body):
        """处理RPC请求"""
        request = json.loads(body)
        method_name = request.get('method')
        params = request.get('params', {})

        print(f"[RPC] Received request: {method_name}")

        handler = self.handlers.get(method_name)
        if handler:
            try:
                result = handler(**params)
                response = {'status': 'success', 'result': result}
            except Exception as e:
                response = {'status': 'error', 'message': str(e)}
        else:
            response = {'status': 'error', 'message': f'Method not found: {method_name}'}

        # 发送响应
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body=json.dumps(response).encode('utf-8')
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[RPC] Response sent")

    def start(self):
        """启动RPC服务器"""
        self.connect()

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_request
        )

        print(f"[RPC] Server started on queue: {self.queue_name}")
        print(f"[RPC] Registered methods: {list(self.handlers.keys())}")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("\n[RPC] Server stopped")
        finally:
            self.connection.close()


# ==================== 处理器示例 ====================

def process_order(data: Dict) -> Any:
    """处理订单"""
    order_id = data.get('order_id')
    user_id = data.get('user_id')
    amount = data.get('amount')

    print(f"  Processing order: {order_id}")
    print(f"    User: {user_id}")
    print(f"    Amount: ${amount}")

    # 模拟处理
    import time
    time.sleep(1)

    return {'order_id': order_id, 'status': 'processed'}


def process_log(data: Dict) -> Any:
    """处理日志"""
    level = data.get('level')
    message = data.get('message')

    print(f"  [{level}] {message}")

    # 存储到数据库或发送到日志服务
    return {'logged': True}


def process_notification(data: Dict) -> Any:
    """处理通知"""
    notif_type = data.get('type')
    message = data.get('message')

    print(f"  Sending {notif_type} notification: {message}")

    return {'sent': True}


# ==================== RPC处理器 ====================

def add(a: int, b: int) -> int:
    """加法运算"""
    return a + b


def subtract(a: int, b: int) -> int:
    """减法运算"""
    return a - b


def multiply(a: int, b: int) -> int:
    """乘法运算"""
    return a * b


# ==================== 使用示例 ====================

def run_consumer():
    """运行消费者"""
    consumer = MessageConsumer()

    # 从单个队列消费
    consumer.consume('orders_created', process_order)


def run_multiple_consumers():
    """运行多队列消费者"""
    consumer = MessageConsumer()

    queue_processors = {
        'orders_created': process_order,
        'orders_cancelled': lambda d: print(f"Order cancelled: {d}"),
        'all_logs': process_log,
    }

    consumer.consume_multiple(queue_processors)


def run_rpc_server():
    """运行RPC服务器"""
    server = RPCServer('rpc_queue')

    server.register_handler('add', add)
    server.register_handler('subtract', subtract)
    server.register_handler('multiply', multiply)

    server.start()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python rabbitmq_consumer.py [consumer|multi|rpc]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'consumer':
        run_consumer()
    elif command == 'multi':
        run_multiple_consumers()
    elif command == 'rpc':
        run_rpc_server()
    else:
        print(f"Unknown command: {command}")
```

**正例（正确使用）**

```python
"""
RabbitMQ正确使用示例
"""
import pika

# ✅ 使用连接池和持久化
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        heartbeat=600,
        blocked_connection_timeout=300
    )
)

# ✅ 声明持久化队列和交换机
channel.queue_declare(queue='tasks', durable=True)
channel.exchange_declare(exchange='tasks_exchange', exchange_type='direct', durable=True)

# ✅ 发送持久化消息
channel.basic_publish(
    exchange='tasks_exchange',
    routing_key='task_queue',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2,  # 持久化
        content_type='application/json'
    )
)

# ✅ 使用手动确认确保消息不丢失
def callback(ch, method, properties, body):
    try:
        process_message(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 确认
    except Exception as e:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # 重新入队

channel.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=False)

# ✅ 设置QoS控制消费速率
channel.basic_qos(prefetch_count=10)  # 每次最多10条未确认消息

# ✅ 使用死信队列处理失败消息
channel.queue_declare(
    queue='main_queue',
    arguments={
        'x-dead-letter-exchange': 'dlx',
        'x-dead-letter-routing-key': 'failed',
        'x-message-ttl': 30000  # 30秒TTL
    }
)
```

**反例（错误使用）**

```python
"""
RabbitMQ错误使用示例
"""
import pika

# ❌ 不使用连接池，频繁创建连接
for i in range(100):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    ch.basic_publish(exchange='', routing_key='queue', body=b'message')
    conn.close()

# ❌ 使用自动确认，消息可能丢失
channel.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=True)

# ❌ 不设置消息持久化
channel.basic_publish(
    exchange='',
    routing_key='queue',
    body=b'important message'  # 如果RabbitMQ重启，消息丢失
)

# ❌ 不处理连接异常
def bad_publish(message):
    channel.basic_publish(exchange='', routing_key='queue', body=message)
    # 如果连接断开，会抛出异常

# ❌ 不设置心跳，可能导致僵尸连接
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')  # 没有heartbeat
)

# ❌ 不限制消费速率，可能导致内存问题
channel.basic_consume(queue='tasks', on_message_callback=callback)
# 没有basic_qos，消费者会一次性接收所有消息
```

---

#### 1.3.2 Kafka（kafka-python）

**概念定义**

Apache Kafka是一个分布式流处理平台，主要用于构建实时数据管道和流式应用程序。它以高吞吐量、低延迟和可扩展性著称。

**核心概念：**

- **Topic（主题）**：消息的分类名，生产者发送消息到Topic，消费者从Topic订阅消息
- **Partition（分区）**：Topic的物理分片，每个分区是有序的、不可变的消息序列
- **Producer（生产者）**：向Topic发送消息的客户端
- **Consumer（消费者）**：从Topic读取消息的客户端
- **Consumer Group（消费者组）**：一组消费者共同消费一个Topic
- **Offset（偏移量）**：消息在分区中的唯一标识

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Kafka 架构                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐                                                │
│  │  Producer   │                                                │
│  │   (生产者)   │                                                │
│  └──────┬──────┘                                                │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      Kafka Cluster                       │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │    │
│  │  │ Broker 1│  │ Broker 2│  │ Broker 3│                  │    │
│  │  │(Leader) │  │(Follower│  │(Follower│                  │    │
│  │  └────┬────┘  └────┬────┘  └────┬────┘                  │    │
│  │       │            │            │                        │    │
│  │       └────────────┴────────────┘                        │    │
│  │                    │                                     │    │
│  │  Topic: orders     │                                     │    │
│  │  ┌─────────────────┴─────────────────┐                   │    │
│  │  │  Partition 0  │  Partition 1      │  Partition 2      │    │
│  │  │  ┌─────┐     │  ┌─────┐          │  ┌─────┐          │    │
│  │  │  │msg1 │     │  │msg1 │          │  │msg1 │          │    │
│  │  │  │msg2 │     │  │msg2 │          │  │msg2 │          │    │
│  │  │  │msg3 │     │  │msg3 │          │  │msg3 │          │    │
│  │  │  └─────┘     │  └─────┘          │  └─────┘          │    │
│  │  └──────────────┴───────────────────┴───────────────────┘    │
│  └─────────────────────────────────────────────────────────┘    │
│         │                                                        │
│         │  Consumer Group: order-processors                      │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │    │
│  │  │ Consumer 1  │  │ Consumer 2  │  │ Consumer 3  │      │    │
│  │  │ (Partition 0)│  │(Partition 1)│  │(Partition 2)│      │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  特点:                                                           │
│  - 分区并行处理，提高吞吐量                                       │
│  - 消费者组内每个分区只被一个消费者消费                           │
│  - 消息持久化，支持回溯消费                                       │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

安装依赖：

```bash
pip install kafka-python
```

生产者实现（`kafka_producer.py`）：

```python
"""
Kafka生产者实现
"""
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import threading
import time


class KafkaMessageProducer:
    """Kafka消息生产者"""

    def __init__(
        self,
        bootstrap_servers='localhost:9092',
        client_id=None,
        acks='all',  # '0', '1', 'all'
        retries=3,
        batch_size=16384,
        linger_ms=5,
        compression_type='gzip'  # 'gzip', 'snappy', 'lz4', None
    ):
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id or f"producer-{uuid.uuid4().hex[:8]}"

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            client_id=self.client_id,
            acks=acks,
            retries=retries,
            batch_size=batch_size,
            linger_ms=linger_ms,
            compression_type=compression_type,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            max_in_flight_requests_per_connection=5
        )

        self.sent_count = 0
        self.error_count = 0

    def send(
        self,
        topic: str,
        value: Dict[str, Any],
        key: Optional[str] = None,
        partition: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        timestamp_ms: Optional[int] = None
    ):
        """发送消息"""
        message = {
            'message_id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'data': value
        }

        try:
            future = self.producer.send(
                topic=topic,
                value=message,
                key=key,
                partition=partition,
                headers=[(k, v.encode('utf-8')) for k, v in (headers or {}).items()],
                timestamp_ms=timestamp_ms
            )

            # 异步发送，添加回调
            future.add_callback(self._on_send_success)
            future.add_errback(self._on_send_error)

            return future

        except KafkaError as e:
            print(f"Failed to send message: {e}")
            self.error_count += 1
            raise

    def _on_send_success(self, record_metadata):
        """发送成功回调"""
        self.sent_count += 1
        print(f"Message sent to {record_metadata.topic} "
              f"partition {record_metadata.partition} "
              f"offset {record_metadata.offset}")

    def _on_send_error(self, excp):
        """发送失败回调"""
        self.error_count += 1
        print(f"Message delivery failed: {excp}")

    def send_sync(
        self,
        topic: str,
        value: Dict[str, Any],
        key: Optional[str] = None,
        timeout=10
    ):
        """同步发送消息"""
        future = self.send(topic, value, key)
        try:
            record_metadata = future.get(timeout=timeout)
            return record_metadata
        except KafkaError as e:
            print(f"Sync send failed: {e}")
            raise

    def flush(self, timeout=30):
        """刷新缓冲区"""
        self.producer.flush(timeout=timeout)

    def close(self, timeout=30):
        """关闭生产者"""
        self.producer.close(timeout=timeout)
        print(f"Producer closed. Sent: {self.sent_count}, Errors: {self.error_count}")

    def metrics(self):
        """获取指标"""
        return {
            'sent_count': self.sent_count,
            'error_count': self.error_count,
            'kafka_metrics': self.producer.metrics()
        }


class OrderProducer:
    """订单生产者示例"""

    TOPIC_ORDERS = 'orders'
    TOPIC_ORDER_EVENTS = 'order-events'

    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaMessageProducer(bootstrap_servers)

    def create_order(self, user_id: str, items: list, total_amount: float):
        """创建订单"""
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        order_data = {
            'order_id': order_id,
            'user_id': user_id,
            'items': items,
            'total_amount': total_amount,
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }

        # 发送订单消息
        self.producer.send(
            topic=self.TOPIC_ORDERS,
            value=order_data,
            key=user_id,  # 使用user_id作为key，确保同一用户的订单进入同一分区
            headers={'event-type': 'order-created'}
        )

        # 发送订单事件
        self.producer.send(
            topic=self.TOPIC_ORDER_EVENTS,
            value={
                'event': 'ORDER_CREATED',
                'order_id': order_id,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            }
        )

        return order_id

    def update_order_status(self, order_id: str, status: str):
        """更新订单状态"""
        self.producer.send(
            topic=self.TOPIC_ORDER_EVENTS,
            value={
                'event': 'ORDER_STATUS_CHANGED',
                'order_id': order_id,
                'new_status': status,
                'timestamp': datetime.now().isoformat()
            }
        )

    def close(self):
        """关闭生产者"""
        self.producer.close()


class LogProducer:
    """日志生产者示例"""

    TOPIC_LOGS = 'application-logs'

    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaMessageProducer(
            bootstrap_servers=bootstrap_servers,
            acks='1',  # 日志可以容忍少量丢失
            batch_size=32768,  # 更大的批处理
            linger_ms=100  # 更长的等待时间
        )

    def log(self, level: str, message: str, extra: Dict = None):
        """发送日志"""
        log_data = {
            'level': level,
            'message': message,
            'service': 'my-service',
            'hostname': 'server-01',
            'extra': extra or {}
        }

        self.producer.send(
            topic=self.TOPIC_LOGS,
            value=log_data,
            key=level  # 按日志级别分区
        )

    def info(self, message: str, extra: Dict = None):
        self.log('INFO', message, extra)

    def error(self, message: str, extra: Dict = None):
        self.log('ERROR', message, extra)

    def close(self):
        self.producer.close()


# ==================== 使用示例 ====================

def demo_basic_producer():
    """基本生产者示例"""
    print("=" * 50)
    print("Kafka Basic Producer Demo")
    print("=" * 50)

    producer = KafkaMessageProducer()

    # 发送多条消息
    for i in range(10):
        producer.send(
            topic='test-topic',
            value={'message': f'Hello Kafka {i}', 'index': i},
            key=f'key-{i % 3}'  # 3个分区
        )

    # 等待所有消息发送完成
    producer.flush()
    producer.close()


def demo_order_producer():
    """订单生产者示例"""
    print("\n" + "=" * 50)
    print("Kafka Order Producer Demo")
    print("=" * 50)

    producer = OrderProducer()

    # 创建订单
    order_id = producer.create_order(
        user_id='user-123',
        items=[
            {'product_id': 'PROD-001', 'quantity': 2, 'price': 29.99},
            {'product_id': 'PROD-002', 'quantity': 1, 'price': 49.99}
        ],
        total_amount=109.97
    )
    print(f"Created order: {order_id}")

    # 更新订单状态
    producer.update_order_status(order_id, 'paid')
    producer.update_order_status(order_id, 'shipped')

    producer.close()


def demo_log_producer():
    """日志生产者示例"""
    print("\n" + "=" * 50)
    print("Kafka Log Producer Demo")
    print("=" * 50)

    producer = LogProducer()

    producer.info('Application started', {'version': '1.0.0'})
    producer.info('User logged in', {'user_id': 'user-123'})
    producer.error('Database connection failed', {'retry_count': 3})

    producer.close()


def demo_high_throughput():
    """高吞吐量示例"""
    print("\n" + "=" * 50)
    print("Kafka High Throughput Demo")
    print("=" * 50)

    producer = KafkaMessageProducer(
        batch_size=65536,
        linger_ms=100,
        compression_type='snappy'
    )

    start_time = time.time()

    # 发送10000条消息
    for i in range(10000):
        producer.send(
            topic='high-throughput-topic',
            value={'data': f'message-{i}', 'timestamp': time.time()},
            key=str(i % 10)
        )

    producer.flush()
    elapsed = time.time() - start_time

    print(f"Sent 10000 messages in {elapsed:.2f} seconds")
    print(f"Throughput: {10000/elapsed:.0f} messages/second")

    producer.close()


if __name__ == '__main__':
    demo_basic_producer()
    demo_order_producer()
    demo_log_producer()
    demo_high_throughput()
```

消费者实现（`kafka_consumer.py`）：

```python
"""
Kafka消费者实现
"""
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
import json
import signal
import sys
from datetime import datetime
from typing import Callable, Dict, Any, List, Optional
import threading
import time


class KafkaMessageConsumer:
    """Kafka消息消费者"""

    def __init__(
        self,
        topics: List[str],
        bootstrap_servers='localhost:9092',
        group_id='default-group',
        client_id=None,
        auto_offset_reset='earliest',  # 'earliest', 'latest', 'none'
        enable_auto_commit=True,
        auto_commit_interval_ms=5000,
        max_poll_records=500,
        session_timeout_ms=10000,
        heartbeat_interval_ms=3000
    ):
        self.topics = topics if isinstance(topics, list) else [topics]
        self.group_id = group_id
        self.running = False
        self.message_count = 0
        self.error_count = 0

        self.consumer = KafkaConsumer(
            *self.topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            client_id=client_id or f"consumer-{group_id}",
            auto_offset_reset=auto_offset_reset,
            enable_auto_commit=enable_auto_commit,
            auto_commit_interval_ms=auto_commit_interval_ms,
            max_poll_records=max_poll_records,
            session_timeout_ms=session_timeout_ms,
            heartbeat_interval_ms=heartbeat_interval_ms,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda m: m.decode('utf-8') if m else None
        )

        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """设置信号处理器"""
        def signal_handler(sig, frame):
            print("\n[!] Shutdown signal received")
            self.stop()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def consume(self, processor: Callable[[Any], None]):
        """消费消息"""
        self.running = True
        print(f"[*] Starting consumer for topics: {self.topics}")
        print(f"[*] Group ID: {self.group_id}")
        print(f"[*] Press Ctrl+C to exit")

        try:
            while self.running:
                # 轮询消息
                messages = self.consumer.poll(timeout_ms=1000)

                for topic_partition, records in messages.items():
                    for record in records:
                        try:
                            self._process_record(record, processor)
                        except Exception as e:
                            print(f"Error processing message: {e}")
                            self.error_count += 1

        except KafkaError as e:
            print(f"Kafka error: {e}")
        finally:
            self.close()

    def _process_record(self, record, processor):
        """处理单条记录"""
        self.message_count += 1

        print(f"\n[{datetime.now()}] Received message #{self.message_count}")
        print(f"  Topic: {record.topic}")
        print(f"  Partition: {record.partition}")
        print(f"  Offset: {record.offset}")
        print(f"  Key: {record.key}")
        print(f"  Value: {record.value}")

        # 调用处理器
        processor(record)

    def stop(self):
        """停止消费"""
        self.running = False

    def close(self):
        """关闭消费者"""
        print(f"\n[*] Closing consumer...")
        print(f"[*] Total messages processed: {self.message_count}")
        print(f"[*] Total errors: {self.error_count}")
        self.consumer.close()

    def commit_sync(self):
        """同步提交偏移量"""
        self.consumer.commit_sync()

    def seek_to_beginning(self):
        """重置到开头"""
        self.consumer.seek_to_beginning()

    def seek_to_end(self):
        """跳转到末尾"""
        self.consumer.seek_to_end()

    def get_offsets(self) -> Dict[str, Dict[int, int]]:
        """获取当前偏移量"""
        offsets = {}
        for topic in self.topics:
            partitions = self.consumer.partitions_for_topic(topic)
            if partitions:
                offsets[topic] = {}
                for partition in partitions:
                    tp = TopicPartition(topic, partition)
                    position = self.consumer.position(tp)
                    offsets[topic][partition] = position
        return offsets


class OrderConsumer:
    """订单消费者示例"""

    def __init__(self, bootstrap_servers='localhost:9092'):
        self.consumer = KafkaMessageConsumer(
            topics=['orders', 'order-events'],
            group_id='order-processors',
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest'
        )
        self.orders_processed = 0

    def process_order(self, record):
        """处理订单"""
        value = record.value

        if record.topic == 'orders':
            print(f"Processing order: {value['data']['order_id']}")
            # 订单处理逻辑
            self._handle_order_created(value['data'])

        elif record.topic == 'order-events':
            print(f"Processing event: {value['data']['event']}")
            # 事件处理逻辑
            self._handle_order_event(value['data'])

    def _handle_order_created(self, order_data):
        """处理订单创建"""
        print(f"  Order created: {order_data['order_id']}")
        print(f"    User: {order_data['user_id']}")
        print(f"    Amount: ${order_data['total_amount']}")
        self.orders_processed += 1

    def _handle_order_event(self, event_data):
        """处理订单事件"""
        print(f"  Event: {event_data['event']}")
        print(f"    Order: {event_data.get('order_id')}")

    def start(self):
        """启动消费者"""
        self.consumer.consume(self.process_order)


class LogConsumer:
    """日志消费者示例"""

    def __init__(self, bootstrap_servers='localhost:9092'):
        self.consumer = KafkaMessageConsumer(
            topics=['application-logs'],
            group_id='log-analyzers',
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',  # 只消费新消息
            max_poll_records=1000
        )
        self.log_counts = {'INFO': 0, 'WARN': 0, 'ERROR': 0}

    def process_log(self, record):
        """处理日志"""
        log_data = record.value['data']
        level = log_data['level']

        self.log_counts[level] = self.log_counts.get(level, 0) + 1

        if level == 'ERROR':
            print(f"⚠️  ERROR: {log_data['message']}")
            # 发送告警
            self._send_alert(log_data)

    def _send_alert(self, log_data):
        """发送告警"""
        print(f"  🚨 Sending alert for: {log_data['message']}")

    def start(self):
        """启动消费者"""
        self.consumer.consume(self.process_log)

    def print_stats(self):
        """打印统计"""
        print("\nLog Statistics:")
        for level, count in self.log_counts.items():
            print(f"  {level}: {count}")


class MultiThreadedConsumer:
    """多线程消费者"""

    def __init__(
        self,
        topics: List[str],
        num_workers: int = 4,
        bootstrap_servers='localhost:9092',
        group_id='multi-threaded-group'
    ):
        self.topics = topics
        self.num_workers = num_workers
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.workers = []
        self.running = False

    def _worker(self, worker_id: int):
        """工作线程"""
        consumer = KafkaMessageConsumer(
            topics=self.topics,
            group_id=self.group_id,
            bootstrap_servers=self.bootstrap_servers
        )

        def processor(record):
            print(f"[Worker {worker_id}] Processing: {record.value['message_id']}")
            # 模拟处理
            time.sleep(0.1)

        consumer.consume(processor)

    def start(self):
        """启动多线程消费者"""
        self.running = True

        for i in range(self.num_workers):
            thread = threading.Thread(target=self._worker, args=(i,))
            thread.daemon = True
            thread.start()
            self.workers.append(thread)

        print(f"[*] Started {self.num_workers} consumer workers")

        # 等待所有线程
        for worker in self.workers:
            worker.join()


# ==================== 使用示例 ====================

def run_basic_consumer():
    """运行基本消费者"""
    consumer = KafkaMessageConsumer(
        topics=['test-topic'],
        group_id='test-group'
    )

    def processor(record):
        print(f"Processed: {record.value}")

    consumer.consume(processor)


def run_order_consumer():
    """运行订单消费者"""
    consumer = OrderConsumer()
    consumer.start()


def run_log_consumer():
    """运行日志消费者"""
    consumer = LogConsumer()
    consumer.start()


def run_multi_threaded_consumer():
    """运行多线程消费者"""
    consumer = MultiThreadedConsumer(
        topics=['high-throughput-topic'],
        num_workers=4
    )
    consumer.start()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python kafka_consumer.py [basic|order|log|multi]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'basic':
        run_basic_consumer()
    elif command == 'order':
        run_order_consumer()
    elif command == 'log':
        run_log_consumer()
    elif command == 'multi':
        run_multi_threaded_consumer()
    else:
        print(f"Unknown command: {command}")
```

**正例（正确使用）**

```python
"""
Kafka正确使用示例
"""
from kafka import KafkaProducer, KafkaConsumer

# ✅ 使用合适的acks配置
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    acks='all',  # 等待所有副本确认
    retries=3,   # 失败重试
    retry_backoff_ms=1000
)

# ✅ 使用消费者组实现负载均衡
consumer = KafkaConsumer(
    'orders',
    bootstrap_servers='localhost:9092',
    group_id='order-processors',  # 同一组内消费者分担分区
    auto_offset_reset='earliest',
    enable_auto_commit=False  # 手动提交偏移量
)

# ✅ 手动提交偏移量确保不丢失消息
for message in consumer:
    try:
        process_message(message)
        consumer.commit_sync()  # 处理成功后提交
    except Exception as e:
        # 不提交，消息会被重新消费
        logger.error(f"Failed to process: {e}")

# ✅ 使用key确保消息顺序
producer.send('orders', key=user_id, value=order_data)
# 同一key的消息进入同一分区，保证顺序

# ✅ 批量处理提高吞吐量
consumer = KafkaConsumer(
    'logs',
    max_poll_records=500,  # 每次拉取500条
    max_poll_interval_ms=300000
)

# ✅ 使用压缩减少网络传输
producer = KafkaProducer(
    compression_type='snappy',  # gzip, snappy, lz4
    batch_size=65536,
    linger_ms=100
)
```

**反例（错误使用）**

```python
"""
Kafka错误使用示例
"""
from kafka import KafkaProducer, KafkaConsumer

# ❌ 不使用消费者组，无法负载均衡
consumer = KafkaConsumer('orders')  # 没有group_id

# ❌ 自动提交偏移量可能导致消息丢失
consumer = KafkaConsumer(
    'orders',
    group_id='processors',
    enable_auto_commit=True  # 可能在处理前提交
)

# ❌ 不使用key，消息随机分布
for order in orders:
    producer.send('orders', value=order)  # 没有key，顺序无法保证

# ❌ 不处理异常，导致消费者停止
for message in consumer:
    process_message(message)  # 如果抛出异常，消费者会停止

# ❌ 创建过多连接
for message in messages:
    producer = KafkaProducer()  # 每次都创建新生产者
    producer.send('topic', message)

# ❌ 不关闭生产者，资源泄漏
producer = KafkaProducer()
producer.send('topic', message)
# 忘记 producer.close()

# ❌ 使用同步发送处理高吞吐场景
for i in range(100000):
    future = producer.send('topic', message)
    future.get()  # 同步等待，性能极差
```

---

#### 1.3.3 Redis Pub/Sub

**概念定义**

Redis Pub/Sub（发布/订阅）是Redis提供的消息通信模式，允许发送者（发布者）发送消息到频道，而接收者（订阅者）接收感兴趣频道的消息。

**核心特性：**

- 实时消息推送
- 无持久化，消息不保存
- 支持模式匹配订阅
- 轻量级，适合实时通知场景

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                   Redis Pub/Sub 架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐                                                │
│  │  Publisher  │                                                │
│  │   (发布者)   │                                                │
│  └──────┬──────┘                                                │
│         │  PUBLISH channel message                               │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Redis Server                          │    │
│  │                                                          │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │              Channel (频道)                      │    │    │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐         │    │    │
│  │  │  │Sub 1    │  │Sub 2    │  │Sub 3    │         │    │    │
│  │  │  │(client1)│  │(client2)│  │(client3)│         │    │    │
│  │  │  └────┬────┘  └────┬────┘  └────┬────┘         │    │    │
│  │  └───────┼────────────┼────────────┼──────────────┘    │    │
│  │          │            │            │                    │    │
│  └──────────┼────────────┼────────────┼────────────────────┘    │
│             │            │            │                          │
│  ┌──────────▼──┐  ┌──────▼────┐  ┌───▼─────┐                   │
│  │ Subscriber 1│  │Subscriber 2│  │Subscriber 3│                │
│  │  (订阅者)    │  │ (订阅者)   │  │ (订阅者)   │                │
│  └─────────────┘  └───────────┘  └──────────┘                   │
│                                                                  │
│  特点:                                                           │
│  - 消息不持久化，订阅者必须在线才能接收                          │
│  - 支持模式订阅: PSUBSCRIBE order.*                              │
│  - 适合实时通知、聊天、实时数据推送                              │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

安装依赖：

```bash
pip install redis
```

Redis Pub/Sub实现（`redis_pubsub.py`）：

```python
"""
Redis Pub/Sub实现
"""
import redis
import json
import threading
import time
from datetime import datetime
from typing import Callable, List, Optional, Dict, Any
import signal


class RedisPubSub:
    """Redis Pub/Sub客户端"""

    def __init__(
        self,
        host='localhost',
        port=6379,
        db=0,
        password=None,
        decode_responses=True
    ):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses
        )
        self.pubsub = None
        self.subscriptions = []
        self.running = False

    def publish(self, channel: str, message: Dict[str, Any]) -> int:
        """发布消息到频道"""
        message_with_meta = {
            'message_id': f"msg-{int(time.time() * 1000)}",
            'timestamp': datetime.now().isoformat(),
            'data': message
        }

        result = self.redis_client.publish(
            channel,
            json.dumps(message_with_meta)
        )
        print(f"Published to {channel}: {result} subscribers received")
        return result

    def subscribe(
        self,
        channels: List[str],
        message_handler: Callable[[str, Dict], None],
        pattern: bool = False
    ):
        """订阅频道"""
        self.pubsub = self.redis_client.pubsub()

        if pattern:
            # 模式订阅
            for channel in channels:
                self.pubsub.psubscribe(channel)
                print(f"Pattern subscribed to: {channel}")
        else:
            # 精确订阅
            for channel in channels:
                self.pubsub.subscribe(channel)
                print(f"Subscribed to: {channel}")

        self.subscriptions = channels
        self.running = True

        print(f"[*] Listening for messages...")
        print(f"[*] Press Ctrl+C to exit")

        try:
            for message in self.pubsub.listen():
                if not self.running:
                    break

                if message['type'] in ('message', 'pmessage'):
                    try:
                        channel = message['channel']
                        data = json.loads(message['data'])
                        message_handler(channel, data)
                    except json.JSONDecodeError:
                        print(f"Failed to decode message: {message['data']}")
                    except Exception as e:
                        print(f"Error handling message: {e}")

        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
        finally:
            self.unsubscribe()

    def unsubscribe(self):
        """取消订阅"""
        if self.pubsub:
            self.pubsub.unsubscribe()
            self.pubsub.punsubscribe()
            self.pubsub.close()
            print("[*] Unsubscribed from all channels")

    def get_subscriber_count(self, channel: str) -> int:
        """获取频道的订阅者数量"""
        return self.redis_client.pubsub_numsub(channel)[0][1]

    def list_channels(self, pattern: str = '*') -> List[str]:
        """列出匹配的频道"""
        return self.redis_client.pubsub_channels(pattern)


class NotificationService:
    """通知服务示例"""

    CHANNEL_USER_NOTIFICATIONS = 'user:notifications'
    CHANNEL_SYSTEM_ALERTS = 'system:alerts'
    CHANNEL_ORDER_UPDATES = 'order:updates'

    def __init__(self, redis_host='localhost'):
        self.redis_pubsub = RedisPubSub(host=redis_host)

    def notify_user(self, user_id: str, notification: Dict):
        """发送用户通知"""
        channel = f"user:{user_id}:notifications"
        self.redis_pubsub.publish(channel, {
            'type': 'notification',
            'user_id': user_id,
            'content': notification,
            'sent_at': datetime.now().isoformat()
        })

    def broadcast_alert(self, alert: Dict):
        """广播系统告警"""
        self.redis_pubsub.publish(self.CHANNEL_SYSTEM_ALERTS, {
            'type': 'alert',
            'severity': alert.get('severity', 'info'),
            'message': alert.get('message'),
            'timestamp': datetime.now().isoformat()
        })

    def order_status_update(self, order_id: str, status: str, details: Dict = None):
        """订单状态更新"""
        self.redis_pubsub.publish(self.CHANNEL_ORDER_UPDATES, {
            'type': 'order_status',
            'order_id': order_id,
            'status': status,
            'details': details or {},
            'updated_at': datetime.now().isoformat()
        })


class ChatService:
    """聊天服务示例"""

    def __init__(self, redis_host='localhost'):
        self.redis_pubsub = RedisPubSub(host=redis_host)
        self.active_users = {}

    def join_room(self, room_id: str, user_id: str, username: str):
        """用户加入聊天室"""
        channel = f"chat:room:{room_id}"

        # 通知其他用户
        self.redis_pubsub.publish(channel, {
            'type': 'user_joined',
            'user_id': user_id,
            'username': username,
            'timestamp': datetime.now().isoformat()
        })

        self.active_users[user_id] = {
            'room_id': room_id,
            'username': username
        }

        return channel

    def send_message(self, room_id: str, user_id: str, username: str, content: str):
        """发送聊天消息"""
        channel = f"chat:room:{room_id}"

        self.redis_pubsub.publish(channel, {
            'type': 'message',
            'user_id': user_id,
            'username': username,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })

    def leave_room(self, room_id: str, user_id: str, username: str):
        """用户离开聊天室"""
        channel = f"chat:room:{room_id}"

        self.redis_pubsub.publish(channel, {
            'type': 'user_left',
            'user_id': user_id,
            'username': username,
            'timestamp': datetime.now().isoformat()
        })

        if user_id in self.active_users:
            del self.active_users[user_id]


class RealtimeDataService:
    """实时数据服务示例"""

    def __init__(self, redis_host='localhost'):
        self.redis_pubsub = RedisPubSub(host=redis_host)

    def publish_metrics(self, metrics: Dict):
        """发布系统指标"""
        self.redis_pubsub.publish('metrics:system', {
            'cpu_percent': metrics.get('cpu_percent'),
            'memory_percent': metrics.get('memory_percent'),
            'disk_usage': metrics.get('disk_usage'),
            'timestamp': datetime.now().isoformat()
        })

    def publish_stock_price(self, symbol: str, price: float, change: float):
        """发布股票价格"""
        channel = f"stock:{symbol}"
        self.redis_pubsub.publish(channel, {
            'symbol': symbol,
            'price': price,
            'change': change,
            'change_percent': (change / (price - change)) * 100 if price != change else 0,
            'timestamp': datetime.now().isoformat()
        })


# ==================== 消费者示例 ====================

class NotificationConsumer:
    """通知消费者"""

    def __init__(self, redis_host='localhost'):
        self.redis_pubsub = RedisPubSub(host=redis_host)
        self.notification_count = 0

    def handle_message(self, channel: str, message: Dict):
        """处理消息"""
        self.notification_count += 1

        print(f"\n[{datetime.now()}] Notification #{self.notification_count}")
        print(f"  Channel: {channel}")
        print(f"  Message ID: {message.get('message_id')}")
        print(f"  Data: {message.get('data')}")

        # 根据消息类型处理
        data = message.get('data', {})
        msg_type = data.get('type')

        if msg_type == 'alert':
            self._handle_alert(data)
        elif msg_type == 'notification':
            self._handle_notification(data)
        elif msg_type == 'order_status':
            self._handle_order_update(data)

    def _handle_alert(self, data: Dict):
        """处理告警"""
        severity = data.get('severity', 'info')
        message = data.get('message')

        if severity == 'critical':
            print(f"  🚨 CRITICAL ALERT: {message}")
            # 发送紧急通知
        else:
            print(f"  ℹ️  Alert: {message}")

    def _handle_notification(self, data: Dict):
        """处理通知"""
        user_id = data.get('user_id')
        content = data.get('content', {})
        print(f"  📧 Notification to {user_id}: {content.get('title')}")

    def _handle_order_update(self, data: Dict):
        """处理订单更新"""
        order_id = data.get('order_id')
        status = data.get('status')
        print(f"  📦 Order {order_id} status: {status}")

    def start(self, channels: List[str]):
        """启动消费者"""
        self.redis_pubsub.subscribe(channels, self.handle_message)


class ChatConsumer:
    """聊天消费者"""

    def __init__(self, redis_host='localhost'):
        self.redis_pubsub = RedisPubSub(host=redis_host)
        self.username = None

    def handle_message(self, channel: str, message: Dict):
        """处理聊天消息"""
        data = message.get('data', {})
        msg_type = data.get('type')

        if msg_type == 'message':
            sender = data.get('username')
            content = data.get('content')
            if sender != self.username:
                print(f"[{sender}]: {content}")
        elif msg_type == 'user_joined':
            print(f"*** {data.get('username')} joined the room ***")
        elif msg_type == 'user_left':
            print(f"*** {data.get('username')} left the room ***")

    def join_chat(self, room_id: str, username: str):
        """加入聊天室"""
        self.username = username
        channel = f"chat:room:{room_id}"

        print(f"Joined room {room_id} as {username}")
        print("Type messages and press Enter to send. Type 'quit' to exit.")

        # 在后台启动订阅
        def subscribe_in_background():
            self.redis_pubsub.subscribe([channel], self.handle_message)

        thread = threading.Thread(target=subscribe_in_background)
        thread.daemon = True
        thread.start()

        # 发送加入消息
        chat_service = ChatService()
        chat_service.join_room(room_id, f"user-{int(time.time())}", username)

        # 交互式发送消息
        while True:
            try:
                content = input()
                if content.lower() == 'quit':
                    chat_service.leave_room(room_id, f"user-{int(time.time())}", username)
                    break
                chat_service.send_message(room_id, f"user-{int(time.time())}", username, content)
            except EOFError:
                break


# ==================== 使用示例 ====================

def demo_basic_pubsub():
    """基本Pub/Sub示例"""
    print("=" * 50)
    print("Redis Pub/Sub Basic Demo")
    print("=" * 50)

    pubsub = RedisPubSub()

    # 发布消息
    pubsub.publish('news', {'title': 'Breaking News', 'content': 'Something happened!'})
    pubsub.publish('updates', {'version': '1.0.1', 'changes': ['bug fix', 'performance improvement']})


def demo_notification_service():
    """通知服务示例"""
    print("\n" + "=" * 50)
    print("Notification Service Demo")
    print("=" * 50)

    service = NotificationService()

    # 发送用户通知
    service.notify_user('user-123', {
        'title': 'New Message',
        'body': 'You have a new message from John'
    })

    # 广播系统告警
    service.broadcast_alert({
        'severity': 'warning',
        'message': 'High CPU usage detected'
    })

    # 订单状态更新
    service.order_status_update('ORD-001', 'shipped', {
        'tracking_number': 'TRK123456',
        'carrier': 'UPS'
    })


def demo_realtime_data():
    """实时数据示例"""
    print("\n" + "=" * 50)
    print("Realtime Data Demo")
    print("=" * 50)

    service = RealtimeDataService()

    # 发布系统指标
    service.publish_metrics({
        'cpu_percent': 45.2,
        'memory_percent': 62.5,
        'disk_usage': 78.0
    })

    # 发布股票价格
    service.publish_stock_price('AAPL', 175.50, 2.30)
    service.publish_stock_price('GOOGL', 142.80, -1.20)


def run_notification_consumer():
    """运行通知消费者"""
    consumer = NotificationConsumer()
    consumer.start([
        'user:notifications',
        'system:alerts',
        'order:updates'
    ])


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        demo_basic_pubsub()
        demo_notification_service()
        demo_realtime_data()
    elif sys.argv[1] == 'consumer':
        run_notification_consumer()
    elif sys.argv[1] == 'chat':
        if len(sys.argv) < 4:
            print("Usage: python redis_pubsub.py chat <room_id> <username>")
        else:
            consumer = ChatConsumer()
            consumer.join_chat(sys.argv[2], sys.argv[3])
```

**正例（正确使用）**

```python
"""
Redis Pub/Sub正确使用示例
"""
import redis

# ✅ 使用连接池
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_client = redis.Redis(connection_pool=pool)

# ✅ 正确处理订阅循环
pubsub = redis_client.pubsub()
pubsub.subscribe('channel')

for message in pubsub.listen():
    if message['type'] == 'message':
        process_message(message['data'])

# ✅ 使用模式订阅处理多个频道
pubsub.psubscribe('user:*:notifications')  # 匹配所有用户通知频道

# ✅ 优雅关闭
pubsub.unsubscribe()
pubsub.close()

# ✅ 使用线程处理订阅（非阻塞）
import threading

def subscribe_handler():
    for message in pubsub.listen():
        if message['type'] == 'message':
            process_message(message['data'])

thread = threading.Thread(target=subscribe_handler)
thread.start()

# 主线程可以继续执行其他任务
```

**反例（错误使用）**

```python
"""
Redis Pub/Sub错误使用示例
"""
import redis

# ❌ 不使用连接池
redis_client = redis.Redis(host='localhost', port=6379)  # 每次创建新连接

# ❌ 不处理连接断开
pubsub = redis_client.pubsub()
pubsub.subscribe('channel')
for message in pubsub.listen():
    process_message(message['data'])  # 如果连接断开，会抛出异常

# ❌ 不关闭订阅
pubsub = redis_client.pubsub()
pubsub.subscribe('channel')
# 程序结束时没有调用 pubsub.close()

# ❌ 期望消息持久化
pubsub.subscribe('orders')
# 如果消费者离线，消息会丢失

# ❌ 在订阅循环中执行耗时操作
for message in pubsub.listen():
    if message['type'] == 'message':
        process_message(message['data'])  # 如果处理耗时，会阻塞其他消息

# ❌ 不处理消息格式错误
for message in pubsub.listen():
    data = json.loads(message['data'])  # 如果格式错误，会抛出异常
```

---

## 第二部分：分布式一致性

### 2.1 CAP定理

#### 2.1.1 形式定义和证明

**概念定义**

CAP定理（也称为Brewer定理）指出，在分布式数据存储系统中，不可能同时满足以下三个特性：

- **C - Consistency（一致性）**：所有节点在同一时间看到相同的数据
- **A - Availability（可用性）**：每个请求都能在有限时间内得到响应（成功或失败）
- **P - Partition Tolerance（分区容错性）**：系统在网络分区的情况下仍能继续运行

**CAP定理的正式表述：**

对于任何分布式数据存储系统，在网络分区发生时，必须在一致性和可用性之间做出选择。

**形式化证明：**

```
假设：存在一个分布式系统同时满足C、A、P

场景：
1. 系统有两个节点N1和N2
2. 客户端向N1写入数据V1
3. 在数据同步到N2之前，网络分区发生（N1和N2之间无法通信）

情况分析：

如果系统选择一致性（C）：
- N2必须拒绝读取请求，直到收到N1的同步
- 这违反了可用性（A），因为N2无法响应请求

如果系统选择可用性（A）：
- N2必须响应读取请求
- 但N2还没有收到V1，只能返回旧值V0
- 这违反了一致性（C），因为N1和N2看到不同的数据

结论：在网络分区时，无法同时满足C和A
因此：CAP定理成立，最多只能满足其中两个
```

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                      CAP 定理图解                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────┐                              │
│                    │   CAP定理   │                              │
│                    │  (不可能三角) │                              │
│                    └──────┬──────┘                              │
│                           │                                      │
│              ┌────────────┼────────────┐                        │
│              │            │            │                        │
│              ▼            ▼            ▼                        │
│         ┌───────┐   ┌────────┐   ┌──────────┐                 │
│         │   C   │   │   A    │   │    P     │                 │
│         │一致性 │   │ 可用性  │   │ 分区容错  │                 │
│         └───┬───┘   └───┬────┘   └────┬─────┘                 │
│             │           │             │                        │
│             └───────────┴─────────────┘                        │
│                         │                                      │
│                         ▼                                      │
│              最多只能选择两个                                   │
│                                                                  │
│  组合选择:                                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  CP系统: 一致+分区容错  │  AP系统: 可用+分区容错        │    │
│  │  - HBase, MongoDB       │  - Cassandra, DynamoDB        │    │
│  │  - 牺牲可用性保证数据一致 │  - 牺牲一致性保证服务可用     │    │
│  │  - 适合金融交易          │  - 适合社交网络               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  注意: CA系统(一致+可用)在网络分区时无法保证分区容错            │
│        因此CA系统实际上不是真正的分布式系统                      │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现 - CAP演示**

```python
"""
CAP定理演示 - 分布式系统行为模拟
"""
import threading
import time
import random
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, List
import uuid


class ConsistencyLevel(Enum):
    """一致性级别"""
    STRONG = "strong"      # 强一致性
    EVENTUAL = "eventual"  # 最终一致性
    CAUSAL = "causal"      # 因果一致性


class SystemMode(Enum):
    """系统模式"""
    CP = "CP"  # 一致+分区容错
    AP = "AP"  # 可用+分区容错
    CA = "CA"  # 一致+可用（无分区容错）


@dataclass
class Node:
    """分布式节点"""
    node_id: str
    data: Dict[str, any]
    is_available: bool = True
    is_partitioned: bool = False
    last_update: float = 0


class DistributedSystem:
    """分布式系统模拟"""

    def __init__(self, mode: SystemMode, num_nodes: int = 3):
        self.mode = mode
        self.nodes: Dict[str, Node] = {}
        self.lock = threading.RLock()
        self.network_partitioned = False

        # 初始化节点
        for i in range(num_nodes):
            node_id = f"node-{i}"
            self.nodes[node_id] = Node(
                node_id=node_id,
                data={},
                last_update=time.time()
            )

    def write(self, key: str, value: any) -> bool:
        """
        写入数据

        CP模式：必须同步到所有节点才返回成功
        AP模式：写入本地节点立即返回，异步同步
        """
        with self.lock:
            if self.mode == SystemMode.CP:
                return self._write_cp(key, value)
            elif self.mode == SystemMode.AP:
                return self._write_ap(key, value)
            else:
                return self._write_ca(key, value)

    def _write_cp(self, key: str, value: any) -> bool:
        """CP模式写入 - 强一致性"""
        print(f"[CP] Writing {key}={value}")

        # 如果有网络分区，检查是否所有可达节点都能写入
        available_nodes = [n for n in self.nodes.values()
                          if n.is_available and not n.is_partitioned]

        if len(available_nodes) < len(self.nodes):
            print(f"  ✗ Network partition detected, write rejected (CP)")
            return False

        # 同步写入所有节点
        timestamp = time.time()
        for node in self.nodes.values():
            node.data[key] = {
                'value': value,
                'timestamp': timestamp,
                'version': self._get_version(key) + 1
            }
            node.last_update = timestamp

        print(f"  ✓ Written to all {len(self.nodes)} nodes")
        return True

    def _write_ap(self, key: str, value: any) -> bool:
        """AP模式写入 - 高可用"""
        print(f"[AP] Writing {key}={value}")

        # 写入任意可用节点
        written = False
        timestamp = time.time()

        for node in self.nodes.values():
            if node.is_available:
                node.data[key] = {
                    'value': value,
                    'timestamp': timestamp,
                    'version': self._get_version(key) + 1
                }
                node.last_update = timestamp
                written = True
                print(f"  ✓ Written to {node.node_id}")

        # 异步同步（模拟）
        if written:
            threading.Thread(target=self._async_sync, args=(key,)).start()

        return written

    def _write_ca(self, key: str, value: any) -> bool:
        """CA模式写入 - 无分区容错"""
        print(f"[CA] Writing {key}={value}")

        if self.network_partitioned:
            print(f"  ✗ Network partition, CA system cannot operate")
            return False

        timestamp = time.time()
        for node in self.nodes.values():
            node.data[key] = {
                'value': value,
                'timestamp': timestamp,
                'version': self._get_version(key) + 1
            }

        print(f"  ✓ Written to all nodes (no partition tolerance)")
        return True

    def read(self, key: str, node_id: Optional[str] = None) -> Optional[any]:
        """
        读取数据

        CP模式：如果存在分区，可能无法读取
        AP模式：总是可以读取，但可能读到旧数据
        """
        with self.lock:
            if self.mode == SystemMode.CP:
                return self._read_cp(key, node_id)
            elif self.mode == SystemMode.AP:
                return self._read_ap(key, node_id)
            else:
                return self._read_ca(key, node_id)

    def _read_cp(self, key: str, node_id: Optional[str] = None) -> Optional[any]:
        """CP模式读取"""
        print(f"[CP] Reading {key}")

        # 检查所有节点是否一致
        values = []
        for node in self.nodes.values():
            if node.is_available and not node.is_partitioned:
                if key in node.data:
                    values.append(node.data[key])

        if len(values) < len([n for n in self.nodes.values()
                              if n.is_available and not n.is_partitioned]):
            print(f"  ✗ Not all nodes have the data (inconsistent)")
            return None

        # 检查版本是否一致
        if values:
            versions = set(v['version'] for v in values)
            if len(versions) > 1:
                print(f"  ✗ Version mismatch: {versions}")
                return None

        result = values[0]['value'] if values else None
        print(f"  ✓ Read consistent value: {result}")
        return result

    def _read_ap(self, key: str, node_id: Optional[str] = None) -> Optional[any]:
        """AP模式读取"""
        print(f"[AP] Reading {key}")

        # 从任意可用节点读取
        target_node = node_id or random.choice(list(self.nodes.keys()))
        node = self.nodes.get(target_node)

        if node and node.is_available:
            if key in node.data:
                value = node.data[key]['value']
                version = node.data[key]['version']
                print(f"  ✓ Read from {target_node}: {value} (v{version})")
                return value

        print(f"  ✗ Key not found")
        return None

    def _read_ca(self, key: str, node_id: Optional[str] = None) -> Optional[any]:
        """CA模式读取"""
        print(f"[CA] Reading {key}")

        if self.network_partitioned:
            print(f"  ✗ Network partition, CA system cannot operate")
            return None

        # 从任意节点读取（所有节点应该一致）
        for node in self.nodes.values():
            if key in node.data:
                value = node.data[key]['value']
                print(f"  ✓ Read: {value}")
                return value

        return None

    def _async_sync(self, key: str):
        """异步同步（AP模式）"""
        time.sleep(0.5)  # 模拟网络延迟
        with self.lock:
            # 找到最新版本
            latest_version = 0
            latest_value = None

            for node in self.nodes.values():
                if key in node.data:
                    if node.data[key]['version'] > latest_version:
                        latest_version = node.data[key]['version']
                        latest_value = node.data[key]['value']

            # 同步到所有节点
            if latest_value is not None:
                for node in self.nodes.values():
                    if node.is_available:
                        node.data[key] = {
                            'value': latest_value,
                            'timestamp': time.time(),
                            'version': latest_version
                        }
                print(f"[AP] Async sync completed for {key}")

    def _get_version(self, key: str) -> int:
        """获取当前版本号"""
        max_version = 0
        for node in self.nodes.values():
            if key in node.data:
                max_version = max(max_version, node.data[key]['version'])
        return max_version

    def simulate_partition(self, node_ids: List[str]):
        """模拟网络分区"""
        print(f"\n[!] Simulating network partition: {node_ids}")
        self.network_partitioned = True
        for node_id in node_ids:
            if node_id in self.nodes:
                self.nodes[node_id].is_partitioned = True
                print(f"  - {node_id} is now partitioned")

    def heal_partition(self):
        """恢复网络分区"""
        print(f"\n[!] Healing network partition")
        self.network_partitioned = False
        for node in self.nodes.values():
            node.is_partitioned = False
        print(f"  - All nodes reconnected")

    def print_state(self):
        """打印系统状态"""
        print(f"\n{'='*50}")
        print(f"System State ({self.mode.value} mode)")
        print(f"{'='*50}")
        for node_id, node in self.nodes.items():
            status = "✓" if node.is_available and not node.is_partitioned else "✗"
            print(f"{status} {node_id}: {node.data}")


def demo_cap_theorem():
    """CAP定理演示"""
    print("\n" + "="*60)
    print("CAP THEOREM DEMONSTRATION")
    print("="*60)

    # 1. CP系统演示
    print("\n" + "-"*60)
    print("1. CP SYSTEM (Consistency + Partition Tolerance)")
    print("-"*60)

    cp_system = DistributedSystem(SystemMode.CP, num_nodes=3)

    # 正常写入
    cp_system.write("balance", 1000)
    cp_system.print_state()

    # 模拟分区
    cp_system.simulate_partition(["node-2"])

    # 分区后尝试写入（应该失败）
    success = cp_system.write("balance", 2000)
    print(f"Write during partition: {'Success' if success else 'Failed'}")

    # 读取（应该失败因为不一致）
    value = cp_system.read("balance")
    print(f"Read during partition: {value}")

    # 恢复分区
    cp_system.heal_partition()
    cp_system.write("balance", 2000)
    cp_system.print_state()

    # 2. AP系统演示
    print("\n" + "-"*60)
    print("2. AP SYSTEM (Availability + Partition Tolerance)")
    print("-"*60)

    ap_system = DistributedSystem(SystemMode.AP, num_nodes=3)

    # 正常写入
    ap_system.write("username", "alice")
    ap_system.print_state()

    # 模拟分区
    ap_system.simulate_partition(["node-2"])

    # 分区后尝试写入（应该成功）
    success = ap_system.write("username", "bob")
    print(f"Write during partition: {'Success' if success else 'Failed'}")

    # 从不同节点读取（可能读到不同值）
    value1 = ap_system.read("username", "node-0")
    value2 = ap_system.read("username", "node-2")
    print(f"Read from node-0: {value1}")
    print(f"Read from node-2: {value2}")
    print("Note: Inconsistent values due to eventual consistency!")

    # 等待同步
    time.sleep(1)
    ap_system.heal_partition()
    time.sleep(0.5)
    ap_system.print_state()

    # 3. CA系统演示
    print("\n" + "-"*60)
    print("3. CA SYSTEM (Consistency + Availability)")
    print("-"*60)
    print("Note: CA systems cannot tolerate network partitions!")

    ca_system = DistributedSystem(SystemMode.CA, num_nodes=3)

    # 正常操作
    ca_system.write("data", "value1")
    ca_system.print_state()

    # 模拟分区（CA系统无法工作）
    ca_system.simulate_partition(["node-2"])
    success = ca_system.write("data", "value2")
    print(f"Write during partition: {'Success' if success else 'Failed'}")
    print("CA system cannot operate during partition!")


if __name__ == '__main__':
    demo_cap_theorem()
```

#### 2.1.2 实际系统中的权衡

**不同场景的选择：**

| 场景 | 推荐选择 | 代表系统 | 原因 |
|------|----------|----------|------|
| 金融交易 | CP | HBase, Spanner | 数据一致性至关重要 |
| 社交网络 | AP | Cassandra, DynamoDB | 可用性优先，可接受短暂不一致 |
| 电商购物车 | AP | Redis | 用户体验优先 |
| 库存管理 | CP | PostgreSQL | 超卖会造成严重问题 |
| 日志收集 | AP | Kafka | 高吞吐优先 |
| 配置中心 | CP | etcd, ZooKeeper | 配置必须一致 |

---

### 2.2 BASE理论

**概念定义**

BASE是Basically Available（基本可用）、Soft state（软状态）、Eventually consistent（最终一致性）的缩写，是对CAP定理中一致性和可用性权衡的结果。

**BASE的核心思想：**

- 放弃强一致性，追求最终一致性
- 允许系统在一段时间内不一致
- 优先保证系统的可用性和性能

**BASE三要素：**

1. **Basically Available（基本可用）**
   - 系统在出现故障时，允许损失部分可用性
   - 例如：响应时间变长、部分功能降级

2. **Soft State（软状态）**
   - 允许系统中的数据存在中间状态
   - 不同节点的数据副本可能不一致

3. **Eventually Consistent（最终一致性）**
   - 不保证实时一致性
   - 保证在没有新的更新操作后，最终所有副本会一致

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                      BASE 理论架构                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    BASE Principles                       │    │
│  │                                                          │    │
│  │  ┌─────────────────┐  ┌─────────────────┐              │    │
│  │  │  B - Basically  │  │  A - Available  │              │    │
│  │  │     Available   │  │                 │              │    │
│  │  │                 │  │  允许响应时间延长 │              │    │
│  │  │  允许功能降级    │  │  允许部分不可用  │              │    │
│  │  │  允许限流熔断    │  │  核心功能可用    │              │    │
│  │  └────────┬────────┘  └────────┬────────┘              │    │
│  │           │                    │                        │    │
│  │           └────────┬───────────┘                        │    │
│  │                    │                                    │    │
│  │           ┌────────▼────────┐                          │    │
│  │           │  S - Soft State │                          │    │
│  │           │                 │                          │    │
│  │           │  允许中间状态    │                          │    │
│  │           │  允许临时不一致  │                          │    │
│  │           └────────┬────────┘                          │    │
│  │                    │                                    │    │
│  │           ┌────────▼────────┐                          │    │
│  │           │  E - Eventually │                          │    │
│  │           │    Consistent   │                          │    │
│  │           │                 │                          │    │
│  │           │  最终达到一致   │                          │    │
│  │           │  无新更新时一致 │                          │    │
│  │           └─────────────────┘                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  最终一致性类型:                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  因果一致性  │  读己之写  │  会话一致性  │  单调读      │    │
│  │  单调写      │  读后写    │  时间线一致性              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现 - BASE演示**

```python
"""
BASE理论演示 - 最终一致性实现
"""
import threading
import time
import random
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid


@dataclass
class DataItem:
    """数据项"""
    key: str
    value: any
    version: int = 1
    timestamp: float = field(default_factory=time.time)
    ttl: Optional[int] = None  # 生存时间（秒）

    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.ttl is None:
            return False
        return time.time() - self.timestamp > self.ttl


class BaseAvailableSystem:
    """基本可用系统"""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.data: Dict[str, DataItem] = {}
        self.is_degraded = False
        self.request_count = 0
        self.error_count = 0
        self.lock = threading.RLock()

    def write(self, key: str, value: any, ttl: Optional[int] = None) -> bool:
        """写入数据 - 基本可用"""
        with self.lock:
            self.request_count += 1

            # 模拟降级模式
            if self.is_degraded:
                print(f"[{self.node_id}] ⚠️  System degraded, write may be delayed")
                time.sleep(0.1)  # 延迟响应

            try:
                # 检查是否存在，增加版本号
                version = 1
                if key in self.data:
                    version = self.data[key].version + 1

                self.data[key] = DataItem(
                    key=key,
                    value=value,
                    version=version,
                    ttl=ttl
                )

                print(f"[{self.node_id}] ✓ Written: {key}={value} (v{version})")
                return True

            except Exception as e:
                self.error_count += 1
                print(f"[{self.node_id}] ✗ Write failed: {e}")
                return False

    def read(self, key: str) -> Optional[any]:
        """读取数据 - 基本可用"""
        with self.lock:
            self.request_count += 1

            # 检查降级模式
            if self.is_degraded:
                print(f"[{self.node_id}] ⚠️  System degraded, returning cached/stale data")

            # 检查数据是否存在
            if key not in self.data:
                return None

            item = self.data[key]

            # 检查是否过期（软状态）
            if item.is_expired():
                print(f"[{self.node_id}] ⚠️  Data expired: {key}")
                # 在BASE系统中，可能仍然返回过期数据
                if not self.is_degraded:
                    del self.data[key]
                    return None

            print(f"[{self.node_id}] ✓ Read: {key}={item.value} (v{item.version})")
            return item.value

    def set_degraded_mode(self, degraded: bool):
        """设置降级模式"""
        self.is_degraded = degraded
        print(f"[{self.node_id}] {'Entered' if degraded else 'Exited'} degraded mode")

    def cleanup_expired(self):
        """清理过期数据"""
        with self.lock:
            expired_keys = [
                k for k, v in self.data.items()
                if v.is_expired()
            ]
            for key in expired_keys:
                del self.data[key]
            if expired_keys:
                print(f"[{self.node_id}] Cleaned up {len(expired_keys)} expired items")


class EventuallyConsistentCluster:
    """最终一致性集群"""

    def __init__(self, num_nodes: int = 3, sync_interval: float = 2.0):
        self.nodes: Dict[str, BaseAvailableSystem] = {}
        self.sync_interval = sync_interval
        self.sync_thread = None
        self.running = False

        # 初始化节点
        for i in range(num_nodes):
            node_id = f"node-{i}"
            self.nodes[node_id] = BaseAvailableSystem(node_id)

        # 启动同步线程
        self.start_sync()

    def write(self, key: str, value: any, node_id: Optional[str] = None) -> bool:
        """写入数据（写入指定节点或随机节点）"""
        target_node = node_id or random.choice(list(self.nodes.keys()))
        node = self.nodes[target_node]

        success = node.write(key, value)

        if success:
            print(f"  Note: Data may not be immediately available on all nodes")

        return success

    def read(self, key: str, node_id: Optional[str] = None) -> Optional[any]:
        """读取数据"""
        target_node = node_id or random.choice(list(self.nodes.keys()))
        node = self.nodes[target_node]

        value = node.read(key)

        if value is None:
            print(f"  Note: Data may exist on other nodes, waiting for sync")

        return value

    def start_sync(self):
        """启动后台同步"""
        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop)
        self.sync_thread.daemon = True
        self.sync_thread.start()
        print("[Cluster] Background sync started")

    def _sync_loop(self):
        """同步循环"""
        while self.running:
            time.sleep(self.sync_interval)
            self._sync_nodes()

    def _sync_nodes(self):
        """节点间数据同步"""
        # 收集所有数据
        all_data: Dict[str, List[DataItem]] = {}

        for node in self.nodes.values():
            for key, item in node.data.items():
                if key not in all_data:
                    all_data[key] = []
                all_data[key].append(item)

        # 同步最新版本到所有节点
        sync_count = 0
        for key, items in all_data.items():
            # 找到最新版本
            latest = max(items, key=lambda x: (x.version, x.timestamp))

            # 同步到所有节点
            for node in self.nodes.values():
                current = node.data.get(key)
                if current is None or current.version < latest.version:
                    node.data[key] = DataItem(
                        key=key,
                        value=latest.value,
                        version=latest.version,
                        timestamp=latest.timestamp,
                        ttl=latest.ttl
                    )
                    sync_count += 1

        if sync_count > 0:
            print(f"[Cluster] Synced {sync_count} items across {len(self.nodes)} nodes")

    def check_consistency(self, key: str) -> Dict:
        """检查数据一致性"""
        values = {}
        for node_id, node in self.nodes.items():
            if key in node.data:
                item = node.data[key]
                values[node_id] = {
                    'value': item.value,
                    'version': item.version
                }
            else:
                values[node_id] = None

        # 检查是否一致
        non_none = [v for v in values.values() if v is not None]
        if len(non_none) == 0:
            return {'consistent': True, 'values': values, 'status': 'not_found'}

        versions = set(v['version'] for v in non_none)
        consistent = len(versions) == 1 and len(non_none) == len(self.nodes)

        return {
            'consistent': consistent,
            'values': values,
            'status': 'consistent' if consistent else 'inconsistent'
        }

    def print_state(self):
        """打印集群状态"""
        print(f"\n{'='*60}")
        print("Cluster State")
        print(f"{'='*60}")
        for node_id, node in self.nodes.items():
            print(f"\n{node_id}:")
            for key, item in node.data.items():
                print(f"  {key}={item.value} (v{item.version})")

    def stop(self):
        """停止集群"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)


def demo_base():
    """BASE理论演示"""
    print("\n" + "="*60)
    print("BASE THEORY DEMONSTRATION")
    print("="*60)

    # 创建集群
    cluster = EventuallyConsistentCluster(num_nodes=3, sync_interval=2.0)

    # 1. 基本可用演示
    print("\n" + "-"*60)
    print("1. BASICALLY AVAILABLE")
    print("-"*60)

    # 正常写入
    cluster.write("user:1:name", "Alice", "node-0")
    cluster.write("user:2:name", "Bob", "node-1")

    # 模拟降级
    cluster.nodes["node-0"].set_degraded_mode(True)
    cluster.write("user:3:name", "Charlie", "node-0")  # 仍然可以写入，但延迟
    cluster.nodes["node-0"].set_degraded_mode(False)

    # 2. 软状态演示
    print("\n" + "-"*60)
    print("2. SOFT STATE")
    print("-"*60)

    # 写入带TTL的数据
    cluster.write("session:123", "active", node_id="node-0")
    print("  (Simulating TTL expiration...)")
    # 在真实系统中，数据会在TTL后过期

    # 3. 最终一致性演示
    print("\n" + "-"*60)
    print("3. EVENTUAL CONSISTENCY")
    print("-"*60)

    # 写入到单个节点
    cluster.write("product:1:stock", 100, "node-0")

    # 立即检查一致性
    print("\nImmediately after write:")
    result = cluster.check_consistency("product:1:stock")
    print(f"  Consistent: {result['consistent']}")
    print(f"  Values: {result['values']}")

    # 等待同步
    print("\nWaiting for sync...")
    time.sleep(3)

    # 再次检查一致性
    print("\nAfter sync:")
    result = cluster.check_consistency("product:1:stock")
    print(f"  Consistent: {result['consistent']}")
    print(f"  Values: {result['values']}")

    # 4. 并发写入演示
    print("\n" + "-"*60)
    print("4. CONCURRENT WRITES (Last-Write-Wins)")
    print("-"*60)

    # 两个节点同时写入同一key
    cluster.write("config:theme", "dark", "node-0")
    time.sleep(0.1)
    cluster.write("config:theme", "light", "node-1")

    print("\nBefore sync:")
    cluster.print_state()

    time.sleep(3)

    print("\nAfter sync (Last-Write-Wins):")
    cluster.print_state()

    cluster.stop()


if __name__ == '__main__':
    demo_base()
```

---

### 2.3 一致性协议

#### 2.3.1 Raft（理解层面）

**概念定义**

Raft是一种用于管理复制日志的共识算法。它通过选举领导者（Leader）来简化分布式一致性问题，相比Paxos更容易理解和实现。

**Raft核心机制：**

1. **领导者选举（Leader Election）**
   - 每个节点处于三种状态之一：Follower、Candidate、Leader
   - 通过超时机制触发选举
   - 获得多数票的节点成为Leader

2. **日志复制（Log Replication）**
   - Leader接收客户端请求
   - Leader将日志条目复制到所有Follower
   - 多数节点确认后，日志提交

3. **安全性（Safety）**
   - 只有包含所有已提交日志条目的节点才能被选为Leader
   - 已提交的日志条目不会被覆盖

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Raft 共识算法                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    节点状态转换                          │    │
│  │                                                          │    │
│  │    ┌──────────┐                                          │    │
│  │    │ Follower │◄──────────────────────────────┐         │    │
│  │    │ (跟随者)  │                               │         │    │
│  │    └────┬─────┘                               │         │    │
│  │         │ 选举超时                              │         │    │
│  │         ▼                                       │         │    │
│  │    ┌──────────┐     获得多数票                    │         │    │
│  │    │Candidate │────────────────►┌────────┐      │         │    │
│  │    │(候选人)  │                 │ Leader │      │         │    │
│  │    └────┬─────┘◄────────────────│(领导者)│──────┘         │    │
│  │         │ 选举超时               └────────┘ 心跳超时       │    │
│  │         └─────────────────────────────────────┘            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    日志复制流程                          │    │
│  │                                                          │    │
│  │  Client ──► Leader ──► Follower 1                       │    │
│  │              │    │      (复制日志)                       │    │
│  │              │    └─► Follower 2                         │    │
│  │              │         (复制日志)                         │    │
│  │              │                                           │    │
│  │              ▼ 多数确认                                   │    │
│  │           Commit (提交)                                   │    │
│  │              │                                           │    │
│  │              ▼                                           │    │
│  │           Apply (应用到状态机)                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  关键概念:                                                       │
│  - Term: 任期号，单调递增                                        │
│  - Index: 日志索引                                               │
│  - Commit Index: 已提交的最大索引                                │
│  - Match Index: 每个Follower匹配的最大索引                       │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现 - Raft简化演示**


```python
"""
Raft共识算法简化演示
"""
import threading
import time
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import uuid


class NodeState(Enum):
    """节点状态"""
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


@dataclass
class LogEntry:
    """日志条目"""
    index: int
    term: int
    command: str
    data: any


@dataclass
class RaftNode:
    """Raft节点"""
    node_id: str
    state: NodeState = NodeState.FOLLOWER
    current_term: int = 0
    voted_for: Optional[str] = None
    log: List[LogEntry] = field(default_factory=list)
    commit_index: int = 0
    last_applied: int = 0

    # Leader状态
    next_index: Dict[str, int] = field(default_factory=dict)
    match_index: Dict[str, int] = field(default_factory=dict)

    # 超时控制
    election_timeout: float = field(default_factory=lambda: random.uniform(0.15, 0.3))
    heartbeat_interval: float = 0.05
    last_heartbeat: float = field(default_factory=time.time)


class RaftCluster:
    """Raft集群"""

    def __init__(self, num_nodes: int = 5):
        self.nodes: Dict[str, RaftNode] = {}
        self.lock = threading.RLock()
        self.running = False
        self.leader_id: Optional[str] = None

        # 初始化节点
        for i in range(num_nodes):
            node_id = f"node-{i}"
            self.nodes[node_id] = RaftNode(node_id=node_id)

        # 为每个节点初始化leader状态
        for node in self.nodes.values():
            for other_id in self.nodes.keys():
                if other_id != node.node_id:
                    node.next_index[other_id] = 1
                    node.match_index[other_id] = 0

    def start(self):
        """启动集群"""
        self.running = True

        # 为每个节点启动处理线程
        for node in self.nodes.values():
            thread = threading.Thread(target=self._node_loop, args=(node.node_id,))
            thread.daemon = True
            thread.start()

        print("[Raft] Cluster started with {} nodes".format(len(self.nodes)))

    def _node_loop(self, node_id: str):
        """节点主循环"""
        while self.running:
            with self.lock:
                node = self.nodes[node_id]

                if node.state == NodeState.FOLLOWER:
                    self._follower_behavior(node)
                elif node.state == NodeState.CANDIDATE:
                    self._candidate_behavior(node)
                elif node.state == NodeState.LEADER:
                    self._leader_behavior(node)

            time.sleep(0.01)  # 10ms tick

    def _follower_behavior(self, node: RaftNode):
        """Follower行为"""
        # 检查选举超时
        if time.time() - node.last_heartbeat > node.election_timeout:
            print(f"[{node.node_id}] Election timeout, becoming candidate")
            node.state = NodeState.CANDIDATE
            node.current_term += 1
            node.voted_for = node.node_id
            node.last_heartbeat = time.time()

    def _candidate_behavior(self, node: RaftNode):
        """Candidate行为"""
        # 请求投票
        votes = self._request_votes(node)

        # 检查是否获得多数票
        majority = (len(self.nodes) // 2) + 1

        if votes >= majority:
            print(f"[{node.node_id}] Elected as leader for term {node.current_term}")
            node.state = NodeState.LEADER
            self.leader_id = node.node_id

            # 初始化leader状态
            for other_id in self.nodes.keys():
                if other_id != node.node_id:
                    node.next_index[other_id] = len(node.log) + 1
                    node.match_index[other_id] = 0
        elif time.time() - node.last_heartbeat > node.election_timeout:
            # 选举超时，开始新一轮选举
            print(f"[{node.node_id}] Election failed, retrying")
            node.current_term += 1
            node.voted_for = node.node_id
            node.last_heartbeat = time.time()

    def _leader_behavior(self, node: RaftNode):
        """Leader行为"""
        # 发送心跳
        if time.time() - node.last_heartbeat > node.heartbeat_interval:
            self._send_heartbeats(node)
            node.last_heartbeat = time.time()

        # 尝试提交日志
        self._try_commit(node)

    def _request_votes(self, candidate: RaftNode) -> int:
        """请求投票"""
        votes = 1  # 自己投自己

        for node_id, node in self.nodes.items():
            if node_id == candidate.node_id:
                continue

            # 检查是否可以投票
            if (node.voted_for is None or node.voted_for == candidate.node_id) and \
               node.current_term <= candidate.current_term:
                # 检查日志是否至少一样新
                if self._is_log_up_to_date(candidate, node):
                    node.voted_for = candidate.node_id
                    node.current_term = candidate.current_term
                    votes += 1
                    print(f"[{node_id}] Voted for {candidate.node_id} in term {candidate.current_term}")

        return votes

    def _is_log_up_to_date(self, candidate: RaftNode, voter: RaftNode) -> bool:
        """检查候选人的日志是否至少一样新"""
        if not voter.log:
            return True
        if not candidate.log:
            return False

        last_candidate = candidate.log[-1]
        last_voter = voter.log[-1]

        if last_candidate.term != last_voter.term:
            return last_candidate.term >= last_voter.term
        return last_candidate.index >= last_voter.index

    def _send_heartbeats(self, leader: RaftNode):
        """发送心跳/日志复制"""
        for node_id, node in self.nodes.items():
            if node_id == leader.node_id:
                continue

            # 更新心跳时间
            node.last_heartbeat = time.time()

            # 发送日志条目
            next_idx = leader.next_index.get(node_id, 1)

            if next_idx <= len(leader.log):
                # 有日志需要复制
                entries = leader.log[next_idx - 1:]
                print(f"[{leader.node_id}] Replicating {len(entries)} entries to {node_id}")

                # 模拟复制成功
                for entry in entries:
                    # 检查任期
                    if len(node.log) >= entry.index:
                        if node.log[entry.index - 1].term != entry.term:
                            # 冲突，删除后续日志
                            node.log = node.log[:entry.index - 1]

                    # 添加日志条目
                    if entry.index > len(node.log):
                        node.log.append(entry)

                leader.match_index[node_id] = len(node.log)
                leader.next_index[node_id] = len(node.log) + 1

    def _try_commit(self, leader: RaftNode):
        """尝试提交日志"""
        for index in range(leader.commit_index + 1, len(leader.log) + 1):
            # 统计有多少节点包含这个日志条目
            count = 1  # Leader自己
            for node_id in self.nodes.keys():
                if node_id != leader.node_id:
                    if leader.match_index.get(node_id, 0) >= index:
                        count += 1

            # 如果多数节点包含，且是当前任期的日志，则提交
            if count > len(self.nodes) // 2 and leader.log[index - 1].term == leader.current_term:
                leader.commit_index = index
                print(f"[{leader.node_id}] Committed log entry {index}")

    def client_request(self, command: str, data: any) -> bool:
        """客户端请求"""
        with self.lock:
            if self.leader_id is None:
                print("[Raft] No leader available")
                return False

            leader = self.nodes[self.leader_id]

            # 创建日志条目
            entry = LogEntry(
                index=len(leader.log) + 1,
                term=leader.current_term,
                command=command,
                data=data
            )

            leader.log.append(entry)
            print(f"[{self.leader_id}] Received client request: {command} {data}")

            # 等待提交（简化版，实际应该异步等待）
            return True

    def get_state(self) -> Dict:
        """获取集群状态"""
        with self.lock:
            return {
                'leader': self.leader_id,
                'nodes': {
                    node_id: {
                        'state': node.state.value,
                        'term': node.current_term,
                        'log_length': len(node.log),
                        'commit_index': node.commit_index
                    }
                    for node_id, node in self.nodes.items()
                }
            }

    def print_state(self):
        """打印集群状态"""
        state = self.get_state()
        print(f"\n{'='*60}")
        print(f"Raft Cluster State")
        print(f"{'='*60}")
        print(f"Leader: {state['leader']}")
        print(f"\nNodes:")
        for node_id, info in state['nodes'].items():
            leader_mark = "★" if node_id == state['leader'] else " "
            print(f"  {leader_mark} {node_id}: {info['state']} (term={info['term']}, "
                  f"log={info['log_length']}, commit={info['commit_index']})")


def demo_raft():
    """Raft算法演示"""
    print("\n" + "="*60)
    print("RAFT CONSENSUS ALGORITHM DEMONSTRATION")
    print("="*60)

    # 创建集群
    cluster = RaftCluster(num_nodes=5)
    cluster.start()

    # 等待选举完成
    print("\nWaiting for leader election...")
    time.sleep(1)
    cluster.print_state()

    # 发送客户端请求
    print("\n" + "-"*60)
    print("Sending client requests...")
    print("-"*60)

    cluster.client_request("SET", {"key": "x", "value": 1})
    time.sleep(0.5)
    cluster.client_request("SET", {"key": "y", "value": 2})
    time.sleep(0.5)
    cluster.client_request("ADD", {"key": "x", "value": 1})

    time.sleep(1)
    cluster.print_state()

    # 模拟Leader故障
    print("\n" + "-"*60)
    print("Simulating leader failure...")
    print("-"*60)

    if cluster.leader_id:
        leader = cluster.nodes[cluster.leader_id]
        leader.state = NodeState.FOLLOWER  # 强制变为Follower
        cluster.leader_id = None

    time.sleep(1)
    cluster.print_state()


if __name__ == '__main__':
    demo_raft()
```

#### 2.3.2 Paxos（理解层面）

**概念定义**

Paxos是由Leslie Lamport提出的分布式一致性算法，用于在不可靠的分布式系统中就某个值达成一致。它是许多分布式系统的理论基础。

**Paxos核心角色：**

1. **Proposer（提议者）**：提出提案
2. **Acceptor（接受者）**：对提案进行投票
3. **Learner（学习者）**：学习已通过的提案

**Paxos两阶段协议：**

**Phase 1 - Prepare（准备阶段）**

- Proposer发送Prepare请求给Acceptor
- Acceptor承诺不接受编号更小的提案

**Phase 2 - Accept（接受阶段）**

- Proposer发送Accept请求给Acceptor
- Acceptor接受提案（如果满足条件）

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Paxos 共识算法                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      Paxos 角色                          │    │
│  │                                                          │    │
│  │   ┌──────────┐      ┌──────────┐      ┌──────────┐     │    │
│  │   │ Proposer │      │ Acceptor │      │ Learner  │     │    │
│  │   │ (提议者)  │      │ (接受者)  │      │ (学习者)  │     │    │
│  │   └────┬─────┘      └────┬─────┘      └────┬─────┘     │    │
│  │        │                 │                 │            │    │
│  │        │  Phase 1: Prepare(n)              │            │    │
│  │        │────────────────►│                 │            │    │
│  │        │                 │                 │            │    │
│  │        │  Promise(n, v)  │                 │            │    │
│  │        │◄────────────────│                 │            │    │
│  │        │                 │                 │            │    │
│  │        │  Phase 2: Accept(n, v)            │            │    │
│  │        │────────────────►│                 │            │    │
│  │        │                 │                 │            │    │
│  │        │  Accepted(n, v) │                 │            │    │
│  │        │◄────────────────│                 │            │    │
│  │        │                 │                 │            │    │
│  │        │                 │  Learn(n, v)    │            │    │
│  │        │                 │────────────────►│            │    │
│  └────────┴─────────────────┴─────────────────┴────────────┘    │
│                                                                  │
│  关键概念:                                                       │
│  - Proposal Number: 提案编号，全局唯一且递增                     │
│  - Majority: 多数派，超过一半的Acceptor                          │
│  - Promise: Acceptor承诺不接受编号更小的提案                     │
│  - Accepted: Acceptor接受提案                                    │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现 - Paxos简化演示**

```python
"""
Paxos共识算法简化演示
"""
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import random


@dataclass
class Proposal:
    """提案"""
    number: int
    value: any


@dataclass
class AcceptorState:
    """Acceptor状态"""
    promised_n: int = 0  # 承诺的最大提案号
    accepted_n: int = 0  # 已接受的提案号
    accepted_v: any = None  # 已接受的值


class PaxosNode:
    """Paxos节点（可以同时是Proposer、Acceptor和Learner）"""

    def __init__(self, node_id: str, all_nodes: List[str]):
        self.node_id = node_id
        self.all_nodes = all_nodes
        self.acceptor_state = AcceptorState()
        self.learned_values: Dict[int, any] = {}  # 已学习的值
        self.lock = threading.Lock()

        # Proposer状态
        self.proposal_counter = 0
        self.highest_proposal_number = 0

    def prepare(self, proposal_n: int) -> Optional[int]:
        """
        Phase 1a: Proposer发送Prepare请求
        Phase 1b: Acceptor处理Prepare请求

        返回：如果已经接受了值，返回该值；否则返回None
        """
        with self.lock:
            if proposal_n > self.acceptor_state.promised_n:
                self.acceptor_state.promised_n = proposal_n
                print(f"[{self.node_id}] Promised not to accept proposals < {proposal_n}")

                # 如果已经接受了值，返回该值
                if self.acceptor_state.accepted_v is not None:
                    return self.acceptor_state.accepted_n
                return None
            else:
                print(f"[{self.node_id}] Rejected prepare({proposal_n}), already promised {self.acceptor_state.promised_n}")
                return -1  # 拒绝

    def accept(self, proposal_n: int, value: any) -> bool:
        """
        Phase 2a: Proposer发送Accept请求
        Phase 2b: Acceptor处理Accept请求
        """
        with self.lock:
            if proposal_n >= self.acceptor_state.promised_n:
                self.acceptor_state.accepted_n = proposal_n
                self.acceptor_state.accepted_v = value
                print(f"[{self.node_id}] Accepted proposal {proposal_n} with value {value}")
                return True
            else:
                print(f"[{self.node_id}] Rejected accept({proposal_n}), promised {self.acceptor_state.promised_n}")
                return False

    def learn(self, proposal_n: int, value: any):
        """Learner学习已接受的值"""
        with self.lock:
            self.learned_values[proposal_n] = value
            print(f"[{self.node_id}] Learned: proposal {proposal_n} = {value}")

    def get_next_proposal_number(self) -> int:
        """获取下一个提案编号"""
        self.proposal_counter += 1
        # 提案编号格式: (轮次, 节点ID)
        return self.proposal_counter * 100 + int(self.node_id.split('-')[1])


class PaxosCluster:
    """Paxos集群"""

    def __init__(self, num_nodes: int = 5):
        self.nodes: Dict[str, PaxosNode] = {}
        self.num_nodes = num_nodes

        node_ids = [f"node-{i}" for i in range(num_nodes)]
        for node_id in node_ids:
            self.nodes[node_id] = PaxosNode(node_id, node_ids)

    def propose(self, proposer_id: str, value: any) -> bool:
        """
        完整的Paxos提案流程

        Phase 1: Prepare
        Phase 2: Accept
        """
        proposer = self.nodes[proposer_id]
        proposal_n = proposer.get_next_proposal_number()

        print(f"\n{'='*60}")
        print(f"[Paxos] Proposer {proposer_id} proposing value: {value}")
        print(f"[Paxos] Proposal number: {proposal_n}")
        print(f"{'='*60}")

        # Phase 1: Prepare
        print("\n--- Phase 1: Prepare ---")
        promises = 0
        highest_accepted_n = 0
        value_to_propose = value

        for node_id, node in self.nodes.items():
            result = node.prepare(proposal_n)

            if result == -1:
                continue  # 被拒绝

            promises += 1

            # 如果Acceptor已经接受了值，使用那个值
            if result is not None and result > highest_accepted_n:
                highest_accepted_n = result
                value_to_propose = node.acceptor_state.accepted_v
                print(f"  -> Using previously accepted value: {value_to_propose}")

        # 检查是否获得多数Promise
        if promises <= self.num_nodes // 2:
            print(f"\n✗ Prepare phase failed: only {promises} promises (need {self.num_nodes // 2 + 1})")
            return False

        print(f"\n✓ Prepare phase succeeded: {promises} promises")

        # Phase 2: Accept
        print("\n--- Phase 2: Accept ---")
        accepts = 0

        for node_id, node in self.nodes.items():
            if node.accept(proposal_n, value_to_propose):
                accepts += 1

        # 检查是否获得多数Accept
        if accepts <= self.num_nodes // 2:
            print(f"\n✗ Accept phase failed: only {accepts} accepts (need {self.num_nodes // 2 + 1})")
            return False

        print(f"\n✓ Accept phase succeeded: {accepts} accepts")
        print(f"✓ Consensus reached: {value_to_propose}")

        # 通知所有Learner
        print("\n--- Learning Phase ---")
        for node in self.nodes.values():
            node.learn(proposal_n, value_to_propose)

        return True

    def get_state(self) -> Dict:
        """获取集群状态"""
        return {
            node_id: {
                'promised_n': node.acceptor_state.promised_n,
                'accepted_n': node.acceptor_state.accepted_n,
                'accepted_v': node.acceptor_state.accepted_v,
                'learned': node.learned_values
            }
            for node_id, node in self.nodes.items()
        }

    def print_state(self):
        """打印集群状态"""
        print(f"\n{'='*60}")
        print("Paxos Cluster State")
        print(f"{'='*60}")

        for node_id, state in self.get_state().items():
            print(f"\n{node_id}:")
            print(f"  Promised N: {state['promised_n']}")
            print(f"  Accepted N: {state['accepted_n']}")
            print(f"  Accepted V: {state['accepted_v']}")
            print(f"  Learned: {state['learned']}")


def demo_paxos():
    """Paxos算法演示"""
    print("\n" + "="*60)
    print("PAXOS CONSENSUS ALGORITHM DEMONSTRATION")
    print("="*60)

    # 创建集群
    cluster = PaxosCluster(num_nodes=5)

    # 第一个提案
    print("\n" + "-"*60)
    print("Proposal 1: Set x = 10")
    print("-"*60)
    success = cluster.propose("node-0", "x = 10")

    if success:
        cluster.print_state()

    # 第二个提案（不同值）
    print("\n" + "-"*60)
    print("Proposal 2: Set x = 20 (from different proposer)")
    print("-"*60)
    success = cluster.propose("node-1", "x = 20")

    if success:
        cluster.print_state()

    # 演示冲突解决
    print("\n" + "-"*60)
    print("Conflict Resolution Demo")
    print("-"*60)
    print("Note: If two proposers try simultaneously, one may need to retry")


if __name__ == '__main__':
    demo_paxos()
```

---

## 第三部分：服务发现与注册

### 3.1 服务注册中心

#### 3.1.1 Consul

**概念定义**

Consul是HashiCorp开发的服务发现、配置和服务编排工具。它提供服务发现、健康检查、键值存储、安全服务通信等功能。

**核心特性：**

- 服务发现（DNS和HTTP接口）
- 健康检查（HTTP、TCP、脚本、TTL）
- 键值存储
- 多数据中心支持
- 安全服务通信（mTLS）

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Consul 架构                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Consul Cluster                        │    │
│  │                                                          │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │    │
│  │  │ Server  │  │ Server  │  │ Server  │  (Raft共识)       │    │
│  │  │  (Leader)│  │(Follower)│  │(Follower)│                  │    │
│  │  └────┬────┘  └────┬────┘  └────┬────┘                  │    │
│  │       └────────────┴────────────┘                        │    │
│  │                    │                                     │    │
│  │              Service Catalog                             │    │
│  │       ┌────────────┴────────────┐                        │    │
│  │       │                         │                        │    │
│  │  ┌────▼────┐              ┌─────▼─────┐                  │    │
│  │  │ Client  │              │  Client   │                  │    │
│  │  │ (Agent) │              │  (Agent)  │                  │    │
│  │  └────┬────┘              └─────┬─────┘                  │    │
│  │       │                         │                        │    │
│  │  ┌────▼────┐              ┌─────▼─────┐                  │    │
│  │  │Service A│              │ Service B │                  │    │
│  │  │(Web App)│              │ (API Svc) │                  │    │
│  │  └─────────┘              └───────────┘                  │    │
│  │                                                          │    │
│  │  功能: 服务注册 │ 健康检查 │ 键值存储 │ 安全通信          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  服务发现方式:                                                   │
│  1. DNS: service-name.service.consul.                           │
│  2. HTTP API: /v1/catalog/service/service-name                  │
│  3. Consul Template: 动态配置文件生成                           │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

安装依赖：

```bash
pip install python-consul
```

Consul客户端实现（`consul_client.py`）：

```python
"""
Consul服务发现客户端实现
"""
import consul
import json
import time
import socket
import threading
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
import uuid


@dataclass
class ServiceInfo:
    """服务信息"""
    name: str
    service_id: str
    address: str
    port: int
    tags: List[str]
    meta: Dict[str, str]
    health_check_url: Optional[str] = None


class ConsulServiceRegistry:
    """Consul服务注册中心"""

    def __init__(self, host='localhost', port=8500):
        self.consul = consul.Consul(host=host, port=port)
        self.registered_services: Dict[str, str] = {}
        self.heartbeat_threads: Dict[str, threading.Thread] = {}
        self.running = False

    def register_service(
        self,
        name: str,
        service_id: Optional[str] = None,
        address: Optional[str] = None,
        port: int = 80,
        tags: Optional[List[str]] = None,
        meta: Optional[Dict[str, str]] = None,
        health_check_interval: str = '10s',
        deregister_after: str = '1m'
    ) -> str:
        """注册服务"""
        service_id = service_id or f"{name}-{uuid.uuid4().hex[:8]}"
        address = address or self._get_local_ip()

        # 健康检查
        check = consul.Check.http(
            url=f"http://{address}:{port}/health",
            interval=health_check_interval,
            timeout='5s',
            deregister=deregister_after
        )

        # 注册服务
        self.consul.agent.service.register(
            name=name,
            service_id=service_id,
            address=address,
            port=port,
            tags=tags or [],
            meta=meta or {},
            check=check
        )

        self.registered_services[name] = service_id
        print(f"[Consul] Registered service: {name} ({service_id}) at {address}:{port}")

        return service_id

    def deregister_service(self, service_id: str):
        """注销服务"""
        self.consul.agent.service.deregister(service_id)
        print(f"[Consul] Deregistered service: {service_id}")

        # 从注册列表中移除
        for name, sid in list(self.registered_services.items()):
            if sid == service_id:
                del self.registered_services[name]

    def discover_service(self, name: str) -> List[Dict]:
        """发现服务"""
        index, services = self.consul.health.service(name)

        result = []
        for service in services:
            service_info = service['Service']
            checks = service['Checks']

            # 只返回健康的服务
            is_healthy = all(check['Status'] == 'passing' for check in checks)

            result.append({
                'id': service_info['ID'],
                'name': service_info['Service'],
                'address': service_info['Address'],
                'port': service_info['Port'],
                'tags': service_info.get('Tags', []),
                'meta': service_info.get('Meta', {}),
                'healthy': is_healthy
            })

        return result

    def get_service_url(self, name: str, scheme='http') -> Optional[str]:
        """获取服务URL（负载均衡）"""
        services = self.discover_service(name)
        healthy_services = [s for s in services if s['healthy']]

        if not healthy_services:
            return None

        # 简单轮询
        import random
        service = random.choice(healthy_services)
        return f"{scheme}://{service['address']}:{service['port']}"

    def watch_service(self, name: str, callback: Callable[[List[Dict]], None]):
        """监视服务变化"""
        def watch_loop():
            index = None
            while self.running:
                try:
                    index, services = self.consul.health.service(
                        name,
                        index=index,
                        wait='30s'
                    )

                    result = []
                    for service in services:
                        service_info = service['Service']
                        checks = service['Checks']
                        is_healthy = all(check['Status'] == 'passing' for check in checks)

                        result.append({
                            'id': service_info['ID'],
                            'name': service_info['Service'],
                            'address': service_info['Address'],
                            'port': service_info['Port'],
                            'healthy': is_healthy
                        })

                    callback(result)

                except Exception as e:
                    print(f"[Consul] Watch error: {e}")
                    time.sleep(5)

        thread = threading.Thread(target=watch_loop)
        thread.daemon = True
        thread.start()

    def put_kv(self, key: str, value: any):
        """存储键值对"""
        self.consul.kv.put(key, json.dumps(value))
        print(f"[Consul] Put KV: {key}")

    def get_kv(self, key: str) -> Optional[any]:
        """获取键值对"""
        index, data = self.consul.kv.get(key)
        if data:
            return json.loads(data['Value'])
        return None

    def delete_kv(self, key: str):
        """删除键值对"""
        self.consul.kv.delete(key)
        print(f"[Consul] Deleted KV: {key}")

    def _get_local_ip(self) -> str:
        """获取本地IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def start(self):
        """启动"""
        self.running = True

    def stop(self):
        """停止并注销所有服务"""
        self.running = False
        for service_id in list(self.registered_services.values()):
            self.deregister_service(service_id)


class ServiceClient:
    """服务客户端"""

    def __init__(self, consul_registry: ConsulServiceRegistry):
        self.registry = consul_registry
        self.service_cache: Dict[str, List[Dict]] = {}
        self.cache_lock = threading.Lock()

    def call_service(
        self,
        service_name: str,
        endpoint: str,
        method: str = 'GET',
        **kwargs
    ) -> Dict:
        """调用服务"""
        import requests

        # 获取服务地址
        service_url = self.registry.get_service_url(service_name)

        if not service_url:
            raise Exception(f"Service {service_name} not available")

        url = f"{service_url}{endpoint}"

        # 发送请求
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()

        return response.json()

    def get_cached_services(self, name: str) -> List[Dict]:
        """获取缓存的服务列表"""
        with self.cache_lock:
            return self.service_cache.get(name, [])

    def start_watching(self, name: str):
        """开始监视服务"""
        def update_cache(services):
            with self.cache_lock:
                self.service_cache[name] = services
            print(f"[ServiceClient] Updated cache for {name}: {len(services)} services")

        self.registry.watch_service(name, update_cache)


# ==================== 使用示例 ====================

def demo_service_registration():
    """服务注册演示"""
    print("="*60)
    print("Consul Service Registration Demo")
    print("="*60)

    registry = ConsulServiceRegistry()
    registry.start()

    # 注册用户服务
    user_service_id = registry.register_service(
        name='user-service',
        port=8001,
        tags=['v1', 'python'],
        meta={'version': '1.0.0', 'team': 'platform'}
    )

    # 注册订单服务
    order_service_id = registry.register_service(
        name='order-service',
        port=8002,
        tags=['v1', 'python'],
        meta={'version': '1.0.0', 'team': 'commerce'}
    )

    # 等待注册生效
    time.sleep(2)

    # 发现服务
    print("\n--- Service Discovery ---")
    user_services = registry.discover_service('user-service')
    print(f"User services: {len(user_services)}")
    for s in user_services:
        print(f"  - {s['address']}:{s['port']} (healthy: {s['healthy']})")

    order_services = registry.discover_service('order-service')
    print(f"Order services: {len(order_services)}")

    # 获取服务URL
    user_url = registry.get_service_url('user-service')
    print(f"\nUser service URL: {user_url}")

    # 清理
    registry.stop()


def demo_kv_store():
    """键值存储演示"""
    print("\n" + "="*60)
    print("Consul KV Store Demo")
    print("="*60)

    registry = ConsulServiceRegistry()

    # 存储配置
    config = {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'myapp'
        },
        'cache': {
            'host': 'localhost',
            'port': 6379
        }
    }

    registry.put_kv('myapp/config', config)

    # 读取配置
    retrieved_config = registry.get_kv('myapp/config')
    print(f"Retrieved config: {json.dumps(retrieved_config, indent=2)}")

    # 删除配置
    registry.delete_kv('myapp/config')


def demo_service_watching():
    """服务监视演示"""
    print("\n" + "="*60)
    print("Consul Service Watching Demo")
    print("="*60)

    registry = ConsulServiceRegistry()
    registry.start()

    # 注册服务
    service_id = registry.register_service(
        name='test-service',
        port=8080
    )

    # 创建客户端并监视
    client = ServiceClient(registry)
    client.start_watching('test-service')

    print("Watching service for 10 seconds...")
    time.sleep(10)

    registry.stop()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        demo_service_registration()
        demo_kv_store()
    elif sys.argv[1] == 'watch':
        demo_service_watching()
```

#### 3.1.2 etcd

**概念定义**

etcd是一个分布式键值存储系统，使用Raft算法实现分布式一致性。它是Kubernetes的核心组件，用于存储集群状态和配置。

**核心特性：**

- 基于Raft的一致性保证
- 键值存储，支持版本和TTL
- Watch机制，监视键值变化
- 事务支持
- 租约（Lease）机制

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                      etcd 架构                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     etcd Cluster                         │    │
│  │                    (Raft Consensus)                      │    │
│  │                                                          │    │
│  │  ┌─────────┐      ┌─────────┐      ┌─────────┐         │    │
│  │  │  etcd   │      │  etcd   │      │  etcd   │         │    │
│  │  │ (Leader)│◄────►│(Follower│◄────►│(Follower│         │    │
│  │  └────┬────┘      └────┬────┘      └────┬────┘         │    │
│  │       │                │                │              │    │
│  │       └────────────────┴────────────────┘              │    │
│  │                    │                                    │    │
│  │              Key-Value Store                           │    │
│  │       ┌────────────┴────────────┐                      │    │
│  │       │                         │                      │    │
│  │  ┌────▼────┐              ┌─────▼─────┐                │    │
│  │  │ /config │              │ /services │                │    │
│  │  │ /locks  │              │ /leaders  │                │    │
│  │  └─────────┘              └───────────┘                │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  核心API:                                                        │
│  - PUT key value                 - 设置键值                     │
│  - GET key                       - 获取键值                     │
│  - DELETE key                    - 删除键值                     │
│  - WATCH key                     - 监视键值变化                 │
│  - TXN compare then else         - 事务                         │
│  - LEASE grant/keepalive/revoke  - 租约管理                     │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

安装依赖：

```bash
pip install etcd3
```

etcd客户端实现（`etcd_client.py`）：

```python
"""
etcd客户端实现
"""
import etcd3
import json
import time
import threading
from typing import Dict, List, Optional, Callable, Tuple
from dataclasses import dataclass


class EtcdClient:
    """etcd客户端"""

    def __init__(self, host='localhost', port=2379):
        self.client = etcd3.client(host=host, port=port)
        self.leases: Dict[str, etcd3.Lease] = {}
        self.watch_ids: List = []

    def put(self, key: str, value: any, lease_id: Optional[int] = None):
        """存储键值对"""
        value_str = json.dumps(value) if not isinstance(value, str) else value

        if lease_id:
            self.client.put(key, value_str, lease=lease_id)
        else:
            self.client.put(key, value_str)

        print(f"[etcd] Put: {key}")

    def get(self, key: str) -> Optional[any]:
        """获取键值对"""
        value, metadata = self.client.get(key)
        if value:
            try:
                return json.loads(value.decode('utf-8'))
            except:
                return value.decode('utf-8')
        return None

    def get_prefix(self, prefix: str) -> List[Tuple[str, any]]:
        """获取前缀匹配的所有键值对"""
        results = []
        for value, metadata in self.client.get_prefix(prefix):
            key = metadata.key.decode('utf-8')
            try:
                val = json.loads(value.decode('utf-8'))
            except:
                val = value.decode('utf-8')
            results.append((key, val))
        return results

    def delete(self, key: str):
        """删除键值对"""
        self.client.delete(key)
        print(f"[etcd] Deleted: {key}")

    def delete_prefix(self, prefix: str):
        """删除前缀匹配的所有键值对"""
        deleted = self.client.delete_prefix(prefix)
        print(f"[etcd] Deleted {deleted} keys with prefix: {prefix}")

    def watch(self, key: str, callback: Callable[[etcd3.events.Event], None]):
        """监视键值变化"""
        events_iterator, cancel = self.client.watch(key)

        def watch_loop():
            for event in events_iterator:
                callback(event)

        thread = threading.Thread(target=watch_loop)
        thread.daemon = True
        thread.start()

        return cancel

    def watch_prefix(self, prefix: str, callback: Callable[[etcd3.events.Event], None]):
        """监视前缀匹配的键值变化"""
        events_iterator, cancel = self.client.watch_prefix(prefix)

        def watch_loop():
            for event in events_iterator:
                callback(event)

        thread = threading.Thread(target=watch_loop)
        thread.daemon = True
        thread.start()

        return cancel

    def grant_lease(self, ttl: int, lease_id: Optional[int] = None) -> etcd3.Lease:
        """创建租约"""
        lease = self.client.lease(ttl, lease_id=lease_id)
        print(f"[etcd] Granted lease: {lease.id} (TTL: {ttl}s)")
        return lease

    def keep_alive(self, lease_id: int):
        """保持租约有效"""
        self.client.refresh_lease(lease_id)

    def revoke_lease(self, lease_id: int):
        """撤销租约"""
        self.client.revoke_lease(lease_id)
        print(f"[etcd] Revoked lease: {lease_id}")

    def lock(self, lock_name: str, ttl: int = 60) -> etcd3.Lock:
        """获取分布式锁"""
        lock = self.client.lock(lock_name, ttl=ttl)
        print(f"[etcd] Acquired lock: {lock_name}")
        return lock

    def transaction(self, compare, success, failure):
        """执行事务"""
        return self.client.transaction(compare, success, failure)

    def close(self):
        """关闭连接"""
        for watch_id in self.watch_ids:
            self.client.cancel_watch(watch_id)
        self.client.close()


class EtcdServiceRegistry:
    """基于etcd的服务注册中心"""

    SERVICE_PREFIX = '/services/'

    def __init__(self, host='localhost', port=2379):
        self.etcd = EtcdClient(host, port)
        self.service_leases: Dict[str, int] = {}

    def register_service(
        self,
        name: str,
        instance_id: str,
        address: str,
        port: int,
        ttl: int = 30,
        metadata: Optional[Dict] = None
    ):
        """注册服务"""
        # 创建租约
        lease = self.etcd.grant_lease(ttl)
        self.service_leases[instance_id] = lease.id

        # 服务信息
        service_info = {
            'name': name,
            'instance_id': instance_id,
            'address': address,
            'port': port,
            'metadata': metadata or {},
            'registered_at': time.time()
        }

        # 存储到etcd
        key = f"{self.SERVICE_PREFIX}{name}/{instance_id}"
        self.etcd.put(key, service_info, lease.id)

        print(f"[Registry] Registered service: {name}/{instance_id}")

        # 启动保活线程
        self._start_keepalive(instance_id, lease.id, ttl)

        return lease.id

    def _start_keepalive(self, instance_id: str, lease_id: int, ttl: int):
        """启动保活线程"""
        def keepalive_loop():
            while instance_id in self.service_leases:
                time.sleep(ttl / 3)  # 每1/3 TTL续租一次
                try:
                    self.etcd.keep_alive(lease_id)
                except Exception as e:
                    print(f"[Registry] Keepalive failed: {e}")
                    break

        thread = threading.Thread(target=keepalive_loop)
        thread.daemon = True
        thread.start()

    def deregister_service(self, instance_id: str):
        """注销服务"""
        if instance_id in self.service_leases:
            lease_id = self.service_leases.pop(instance_id)
            self.etcd.revoke_lease(lease_id)
            print(f"[Registry] Deregistered service: {instance_id}")

    def discover_service(self, name: str) -> List[Dict]:
        """发现服务"""
        prefix = f"{self.SERVICE_PREFIX}{name}/"
        results = self.etcd.get_prefix(prefix)

        services = []
        for key, value in results:
            if isinstance(value, dict):
                services.append(value)

        return services

    def get_service_instance(self, name: str) -> Optional[Dict]:
        """获取服务实例（负载均衡）"""
        services = self.discover_service(name)
        if not services:
            return None

        # 简单轮询
        import random
        return random.choice(services)

    def watch_service(self, name: str, callback: Callable[[str, List[Dict]], None]):
        """监视服务变化"""
        prefix = f"{self.SERVICE_PREFIX}{name}/"

        def on_event(event):
            services = self.discover_service(name)
            callback(event.key.decode('utf-8'), services)

        return self.etcd.watch_prefix(prefix, on_event)

    def close(self):
        """关闭注册中心"""
        for instance_id in list(self.service_leases.keys()):
            self.deregister_service(instance_id)
        self.etcd.close()


class DistributedLock:
    """基于etcd的分布式锁"""

    def __init__(self, etcd_client: EtcdClient, lock_name: str, ttl: int = 60):
        self.etcd = etcd_client
        self.lock_name = lock_name
        self.ttl = ttl
        self.lock = None

    def __enter__(self):
        self.lock = self.etcd.lock(self.lock_name, self.ttl)
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock:
            self.lock.release()
            print(f"[etcd] Released lock: {self.lock_name}")


# ==================== 使用示例 ====================

def demo_basic_operations():
    """基本操作演示"""
    print("="*60)
    print("etcd Basic Operations Demo")
    print("="*60)

    etcd = EtcdClient()

    # 存储键值对
    etcd.put('/config/app/name', 'MyApplication')
    etcd.put('/config/app/version', '1.0.0')
    etcd.put('/config/database/host', 'localhost')
    etcd.put('/config/database/port', 5432)

    # 获取键值对
    name = etcd.get('/config/app/name')
    print(f"App name: {name}")

    # 获取前缀匹配的所有键值对
    config = etcd.get_prefix('/config/')
    print(f"\nAll config:")
    for key, value in config:
        print(f"  {key}: {value}")

    # 删除键值对
    etcd.delete('/config/app/version')

    etcd.close()


def demo_service_registry():
    """服务注册演示"""
    print("\n" + "="*60)
    print("etcd Service Registry Demo")
    print("="*60)

    registry = EtcdServiceRegistry()

    # 注册服务
    registry.register_service(
        name='user-service',
        instance_id='user-1',
        address='192.168.1.10',
        port=8001,
        metadata={'version': '1.0.0'}
    )

    registry.register_service(
        name='user-service',
        instance_id='user-2',
        address='192.168.1.11',
        port=8001,
        metadata={'version': '1.0.0'}
    )

    # 发现服务
    services = registry.discover_service('user-service')
    print(f"\nDiscovered {len(services)} user-service instances:")
    for s in services:
        print(f"  - {s['address']}:{s['port']}")

    # 获取一个实例
    instance = registry.get_service_instance('user-service')
    print(f"\nSelected instance: {instance}")

    registry.close()


def demo_distributed_lock():
    """分布式锁演示"""
    print("\n" + "="*60)
    print("etcd Distributed Lock Demo")
    print("="*60)

    etcd = EtcdClient()

    # 获取分布式锁
    with DistributedLock(etcd, 'resource-lock', ttl=30):
        print("Lock acquired, doing critical work...")
        time.sleep(2)

    print("Lock released")

    etcd.close()


def demo_watching():
    """监视演示"""
    print("\n" + "="*60)
    print("etcd Watch Demo")
    print("="*60)

    etcd = EtcdClient()

    # 设置监视
    def on_change(event):
        print(f"\n[Watch] Event: {event}")

    cancel = etcd.watch('/watch-test', on_change)

    # 修改键值
    print("Setting value...")
    etcd.put('/watch-test', 'value1')
    time.sleep(1)

    print("Updating value...")
    etcd.put('/watch-test', 'value2')
    time.sleep(1)

    print("Deleting value...")
    etcd.delete('/watch-test')
    time.sleep(1)

    cancel()
    etcd.close()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        demo_basic_operations()
        demo_service_registry()
        demo_distributed_lock()
    elif sys.argv[1] == 'watch':
        demo_watching()
```

#### 3.1.3 ZooKeeper（kazoo）

**概念定义**

Apache ZooKeeper是一个分布式协调服务，提供配置维护、命名服务、分布式同步、组服务等功能。它使用ZAB（ZooKeeper Atomic Broadcast）协议保证一致性。

**核心概念：**

- **ZNode**：ZooKeeper的数据节点，类似文件系统
- **Watcher**：事件监听器
- **ACL**：访问控制列表
- **Ephemeral Node**：临时节点，会话结束时自动删除
- **Sequential Node**：顺序节点，自动添加序号

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                    ZooKeeper 架构                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   ZooKeeper Ensemble                     │    │
│  │                    (ZAB Protocol)                        │    │
│  │                                                          │    │
│  │  ┌─────────┐      ┌─────────┐      ┌─────────┐         │    │
│  │  │  ZK     │      │  ZK     │      │  ZK     │         │    │
│  │  │ (Leader)│◄────►│(Follower│◄────►│(Observer│         │    │
│  │  └────┬────┘      └────┬────┘      └────┬────┘         │    │
│  │       │                │                │              │    │
│  │       └────────────────┴────────────────┘              │    │
│  │                    │                                    │    │
│  │              ZNode Tree                                │    │
│  │       ┌────────────┴────────────┐                      │    │
│  │       │                         │                      │    │
│  │  ┌────▼────┐              ┌─────▼─────┐                │    │
│  │  │/services│              │ /config   │                │    │
│  │  │  /app1  │              │  /db      │                │    │
│  │  │  /app2  │              │  /cache   │                │    │
│  │  └─────────┘              └───────────┘                │    │
│  │                                                          │    │
│  │  ZNode类型:                                              │    │
│  │  - Persistent: 持久节点                                  │    │
│  │  - Ephemeral: 临时节点（会话结束删除）                    │    │
│  │  - Sequential: 顺序节点                                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  核心API:                                                        │
│  - create(path, data, acl, flags)  - 创建节点                   │
│  - delete(path, version)           - 删除节点                   │
│  - exists(path, watch)             - 检查节点存在               │
│  - getData(path, watch)            - 获取数据                   │
│  - setData(path, data, version)    - 设置数据                   │
│  - getChildren(path, watch)        - 获取子节点                 │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

安装依赖：

```bash
pip install kazoo
```

ZooKeeper客户端实现（`zookeeper_client.py`）：


---

## 第五部分：分布式事务

### 5.1 两阶段提交（2PC）

**概念定义**

两阶段提交（Two-Phase Commit，2PC）是一种分布式事务协议，通过协调者（Coordinator）和参与者（Participants）的协作来保证分布式事务的原子性。

**两阶段：**

1. **准备阶段（Prepare Phase）**：协调者询问所有参与者是否可以提交
2. **提交阶段（Commit Phase）**：根据参与者的响应决定提交或回滚

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                    两阶段提交 (2PC)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐                                                │
│  │ Coordinator │                                                │
│  │  (协调者)    │                                                │
│  └──────┬──────┘                                                │
│         │                                                        │
│  Phase 1: Prepare                                                │
│         │                                                        │
│    ┌────┼────┬────────┐                                         │
│    │    │    │        │                                         │
│    ▼    ▼    ▼        ▼                                         │
│  ┌──┐ ┌──┐ ┌──┐   ┌──┐                                          │
│  │P1│ │P2│ │P3│   │P4│  Participants (参与者)                   │
│  └──┘ └──┘ └──┘   └──┘                                          │
│   │    │    │      │                                             │
│   │    │    │      │  Vote: YES/NO                               │
│   │    │    │      │                                             │
│   └────┴────┴──────┘                                             │
│            │                                                     │
│  Phase 2: Commit/Abort                                           │
│            │                                                     │
│    ┌───────┴───────┐                                             │
│    │               │                                             │
│    ▼               ▼                                             │
│  Commit          Abort                                           │
│  (if all YES)   (if any NO)                                      │
│                                                                  │
│  优点: 强一致性，实现简单                                        │
│  缺点: 同步阻塞，单点故障（协调者），性能较低                    │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

```python
"""
两阶段提交（2PC）实现
"""
import threading
import time
from enum import Enum
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass


class TransactionStatus(Enum):
    """事务状态"""
    PENDING = "pending"
    PREPARING = "preparing"
    PREPARED = "prepared"
    COMMITTING = "committing"
    COMMITTED = "committed"
    ABORTING = "aborting"
    ABORTED = "aborted"


class Vote(Enum):
    """投票结果"""
    YES = "yes"
    NO = "no"


@dataclass
class Transaction:
    """事务"""
    tx_id: str
    status: TransactionStatus
    participants: List[str]
    votes: Dict[str, Vote] = None

    def __post_init__(self):
        if self.votes is None:
            self.votes = {}


class Participant:
    """2PC参与者"""

    def __init__(self, participant_id: str):
        self.participant_id = participant_id
        self.prepared_transactions: Dict[str, any] = {}
        self.committed_transactions: Dict[str, any] = {}
        self.lock = threading.Lock()

    def prepare(self, tx_id: str, operation: Callable) -> Vote:
        """准备阶段"""
        print(f"[{self.participant_id}] Preparing transaction {tx_id}")

        try:
            # 执行本地操作（但不提交）
            result = operation()

            with self.lock:
                # 记录准备状态
                self.prepared_transactions[tx_id] = {
                    'operation': operation,
                    'result': result,
                    'prepared_at': time.time()
                }

            print(f"[{self.participant_id}] Voted YES for {tx_id}")
            return Vote.YES

        except Exception as e:
            print(f"[{self.participant_id}] Voted NO for {tx_id}: {e}")
            return Vote.NO

    def commit(self, tx_id: str) -> bool:
        """提交事务"""
        print(f"[{self.participant_id}] Committing transaction {tx_id}")

        with self.lock:
            if tx_id not in self.prepared_transactions:
                print(f"[{self.participant_id}] Transaction {tx_id} not prepared")
                return False

            # 实际提交
            tx_data = self.prepared_transactions.pop(tx_id)
            self.committed_transactions[tx_id] = tx_data

            print(f"[{self.participant_id}] Committed transaction {tx_id}")
            return True

    def abort(self, tx_id: str) -> bool:
        """中止事务"""
        print(f"[{self.participant_id}] Aborting transaction {tx_id}")

        with self.lock:
            if tx_id in self.prepared_transactions:
                self.prepared_transactions.pop(tx_id)

            print(f"[{self.participant_id}] Aborted transaction {tx_id}")
            return True


class Coordinator:
    """2PC协调者"""

    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}
        self.participants: Dict[str, Participant] = {}
        self.lock = threading.Lock()

    def register_participant(self, participant: Participant):
        """注册参与者"""
        self.participants[participant.participant_id] = participant

    def execute_transaction(
        self,
        tx_id: str,
        operations: Dict[str, Callable]
    ) -> bool:
        """
        执行分布式事务

        Args:
            tx_id: 事务ID
            operations: {participant_id: operation}

        Returns:
            事务是否成功
        """
        # 创建事务
        transaction = Transaction(
            tx_id=tx_id,
            status=TransactionStatus.PENDING,
            participants=list(operations.keys())
        )

        with self.lock:
            self.transactions[tx_id] = transaction

        try:
            # Phase 1: Prepare
            print(f"\n[Coordinator] Phase 1: Prepare for {tx_id}")
            transaction.status = TransactionStatus.PREPARING

            all_yes = True
            for participant_id, operation in operations.items():
                participant = self.participants.get(participant_id)
                if not participant:
                    all_yes = False
                    break

                vote = participant.prepare(tx_id, operation)
                transaction.votes[participant_id] = vote

                if vote == Vote.NO:
                    all_yes = False
                    break

            # Phase 2: Commit or Abort
            if all_yes:
                print(f"\n[Coordinator] Phase 2: Commit for {tx_id}")
                transaction.status = TransactionStatus.COMMITTING

                for participant_id in transaction.participants:
                    participant = self.participants[participant_id]
                    participant.commit(tx_id)

                transaction.status = TransactionStatus.COMMITTED
                print(f"[Coordinator] Transaction {tx_id} COMMITTED")
                return True

            else:
                print(f"\n[Coordinator] Phase 2: Abort for {tx_id}")
                transaction.status = TransactionStatus.ABORTING

                for participant_id in transaction.participants:
                    participant = self.participants[participant_id]
                    participant.abort(tx_id)

                transaction.status = TransactionStatus.ABORTED
                print(f"[Coordinator] Transaction {tx_id} ABORTED")
                return False

        except Exception as e:
            print(f"[Coordinator] Error in transaction {tx_id}: {e}")
            # 中止事务
            for participant_id in transaction.participants:
                participant = self.participants.get(participant_id)
                if participant:
                    participant.abort(tx_id)

            transaction.status = TransactionStatus.ABORTED
            return False


# ==================== 使用示例 ====================

def demo_2pc():
    """2PC演示"""
    print("="*60)
    print("Two-Phase Commit (2PC) Demo")
    print("="*60)

    # 创建协调者
    coordinator = Coordinator()

    # 创建参与者（模拟数据库）
    db1 = Participant("Database-1")
    db2 = Participant("Database-2")
    db3 = Participant("Database-3")

    coordinator.register_participant(db1)
    coordinator.register_participant(db2)
    coordinator.register_participant(db3)

    # 模拟数据存储
    data_store = {
        'db1': {},
        'db2': {},
        'db3': {}
    }

    # 定义操作
    def operation_db1():
        """数据库1的操作"""
        data_store['db1']['user'] = {'id': 1, 'name': 'Alice'}
        return True

    def operation_db2():
        """数据库2的操作"""
        data_store['db2']['account'] = {'user_id': 1, 'balance': 1000}
        return True

    def operation_db3():
        """数据库3的操作"""
        data_store['db3']['profile'] = {'user_id': 1, 'avatar': 'default.png'}
        return True

    # 执行事务
    operations = {
        'Database-1': operation_db1,
        'Database-2': operation_db2,
        'Database-3': operation_db3,
    }

    success = coordinator.execute_transaction('TX-001', operations)
    print(f"\nTransaction result: {'SUCCESS' if success else 'FAILED'}")
    print(f"Data store: {data_store}")

    # 演示失败场景
    print("\n" + "-"*60)
    print("Failure Scenario Demo")
    print("-"*60)

    def failing_operation():
        raise Exception("Simulated failure")

    operations_with_failure = {
        'Database-1': operation_db1,
        'Database-2': failing_operation,  # 这个会失败
        'Database-3': operation_db3,
    }

    success = coordinator.execute_transaction('TX-002', operations_with_failure)
    print(f"\nTransaction result: {'SUCCESS' if success else 'FAILED'}")


if __name__ == '__main__':
    demo_2pc()
```

### 5.2 TCC（Try-Confirm-Cancel）

**概念定义**

TCC是一种业务层面的分布式事务模式，将每个操作拆分为三个阶段：

- **Try**：预留资源，执行业务检查
- **Confirm**：确认执行业务
- **Cancel**：取消执行，释放资源

**Python实现**

```python
"""
TCC分布式事务实现
"""
from typing import Dict, Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time


class TCCStatus(Enum):
    """TCC事务状态"""
    TRYING = "trying"
    TRY_SUCCESS = "try_success"
    TRY_FAILED = "try_failed"
    CONFIRMING = "confirming"
    CONFIRMED = "confirmed"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"


@dataclass
class TCCAction:
    """TCC动作"""
    name: str
    try_func: Callable[[], bool]
    confirm_func: Callable[[], bool]
    cancel_func: Callable[[], bool]
    status: TCCStatus = TCCStatus.TRYING


class TCCTransaction:
    """TCC事务"""

    def __init__(self, tx_id: str):
        self.tx_id = tx_id
        self.actions: Dict[str, TCCAction] = {}
        self.status = TCCStatus.TRYING

    def register_action(self, action: TCCAction):
        """注册TCC动作"""
        self.actions[action.name] = action

    def execute(self) -> bool:
        """执行TCC事务"""
        print(f"\n[TCC] Starting transaction {self.tx_id}")

        # Phase 1: Try
        print(f"[TCC] Phase 1: Try")
        try_results = {}

        for name, action in self.actions.items():
            print(f"  Trying {name}...")
            try:
                result = action.try_func()
                try_results[name] = result
                action.status = TCCStatus.TRY_SUCCESS if result else TCCStatus.TRY_FAILED

                if not result:
                    print(f"  {name} Try FAILED")
                    break
                else:
                    print(f"  {name} Try SUCCESS")

            except Exception as e:
                print(f"  {name} Try EXCEPTION: {e}")
                try_results[name] = False
                action.status = TCCStatus.TRY_FAILED
                break

        # 检查所有Try是否成功
        all_try_success = all(try_results.values()) and len(try_results) == len(self.actions)

        if all_try_success:
            # Phase 2: Confirm
            print(f"\n[TCC] Phase 2: Confirm")
            self.status = TCCStatus.CONFIRMING

            for name, action in self.actions.items():
                print(f"  Confirming {name}...")
                try:
                    action.confirm_func()
                    action.status = TCCStatus.CONFIRMED
                    print(f"  {name} Confirm SUCCESS")
                except Exception as e:
                    print(f"  {name} Confirm FAILED: {e}")

            self.status = TCCStatus.CONFIRMED
            print(f"[TCC] Transaction {self.tx_id} CONFIRMED")
            return True

        else:
            # Phase 2: Cancel
            print(f"\n[TCC] Phase 2: Cancel")
            self.status = TCCStatus.CANCELLING

            for name, action in self.actions.items():
                if action.status == TCCStatus.TRY_SUCCESS:
                    print(f"  Cancelling {name}...")
                    try:
                        action.cancel_func()
                        action.status = TCCStatus.CANCELLED
                        print(f"  {name} Cancel SUCCESS")
                    except Exception as e:
                        print(f"  {name} Cancel FAILED: {e}")

            self.status = TCCStatus.CANCELLED
            print(f"[TCC] Transaction {self.tx_id} CANCELLED")
            return False


# ==================== 使用示例 ====================

def demo_tcc():
    """TCC演示 - 电商订单场景"""
    print("="*60)
    print("TCC Distributed Transaction Demo")
    print("="*60)

    # 模拟库存、账户、订单服务
    inventory = {'product-1': 100}
    account = {'user-1': 1000}
    orders = {}

    # 预留资源记录
    reserved_inventory = {}
    reserved_balance = {}

    # 创建TCC事务
    tx = TCCTransaction('ORDER-001')

    # 库存服务TCC
    def inventory_try():
        """预留库存"""
        product_id = 'product-1'
        quantity = 2

        if inventory.get(product_id, 0) >= quantity:
            inventory[product_id] -= quantity
            reserved_inventory[product_id] = reserved_inventory.get(product_id, 0) + quantity
            print(f"    Reserved {quantity} {product_id}")
            return True
        return False

    def inventory_confirm():
        """确认扣减库存"""
        product_id = 'product-1'
        quantity = 2
        reserved_inventory[product_id] -= quantity
        print(f"    Confirmed inventory deduction")
        return True

    def inventory_cancel():
        """释放库存"""
        product_id = 'product-1'
        quantity = 2
        inventory[product_id] = inventory.get(product_id, 0) + quantity
        reserved_inventory[product_id] -= quantity
        print(f"    Released inventory")
        return True

    # 账户服务TCC
    def account_try():
        """预留余额"""
        user_id = 'user-1'
        amount = 200

        if account.get(user_id, 0) >= amount:
            account[user_id] -= amount
            reserved_balance[user_id] = reserved_balance.get(user_id, 0) + amount
            print(f"    Reserved ${amount} from {user_id}")
            return True
        return False

    def account_confirm():
        """确认扣款"""
        user_id = 'user-1'
        amount = 200
        reserved_balance[user_id] -= amount
        print(f"    Confirmed payment")
        return True

    def account_cancel():
        """释放余额"""
        user_id = 'user-1'
        amount = 200
        account[user_id] = account.get(user_id, 0) + amount
        reserved_balance[user_id] -= amount
        print(f"    Released balance")
        return True

    # 订单服务TCC
    def order_try():
        """创建待确认订单"""
        order_id = 'ORDER-001'
        orders[order_id] = {
            'status': 'pending',
            'product': 'product-1',
            'quantity': 2,
            'amount': 200
        }
        print(f"    Created pending order {order_id}")
        return True

    def order_confirm():
        """确认订单"""
        order_id = 'ORDER-001'
        orders[order_id]['status'] = 'confirmed'
        print(f"    Confirmed order {order_id}")
        return True

    def order_cancel():
        """取消订单"""
        order_id = 'ORDER-001'
        orders[order_id]['status'] = 'cancelled'
        print(f"    Cancelled order {order_id}")
        return True

    # 注册TCC动作
    tx.register_action(TCCAction('inventory', inventory_try, inventory_confirm, inventory_cancel))
    tx.register_action(TCCAction('account', account_try, account_confirm, account_cancel))
    tx.register_action(TCCAction('order', order_try, order_confirm, order_cancel))

    # 执行事务
    success = tx.execute()

    print(f"\nFinal state:")
    print(f"  Inventory: {inventory}")
    print(f"  Account: {account}")
    print(f"  Orders: {orders}")


if __name__ == '__main__':
    demo_tcc()
```

### 5.3 Saga模式

**概念定义**

Saga模式将长事务拆分为多个本地事务，每个本地事务有对应的补偿操作。如果某个本地事务失败，执行前面所有已完成事务的补偿操作。

**两种实现方式：**

- **编排式（Choreography）**：各服务通过事件驱动协作
- **协调式（Orchestration）**：由Saga协调器统一管理

**Python实现**

```python
"""
Saga分布式事务实现
"""
from typing import List, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum
import time


class SagaStatus(Enum):
    """Saga状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    FAILED = "failed"


@dataclass
class SagaStep:
    """Saga步骤"""
    name: str
    action: Callable[[], Any]
    compensation: Callable[[], Any]
    result: Any = None
    executed: bool = False


class SagaOrchestrator:
    """Saga协调器"""

    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps: List[SagaStep] = []
        self.status = SagaStatus.PENDING
        self.current_step = 0

    def add_step(self, step: SagaStep):
        """添加步骤"""
        self.steps.append(step)

    def execute(self) -> bool:
        """执行Saga"""
        print(f"\n[Saga] Starting saga {self.saga_id}")
        self.status = SagaStatus.RUNNING

        for i, step in enumerate(self.steps):
            self.current_step = i
            print(f"\n[Saga] Executing step {i+1}/{len(self.steps)}: {step.name}")

            try:
                step.result = step.action()
                step.executed = True
                print(f"  Step {step.name} completed")

            except Exception as e:
                print(f"  Step {step.name} failed: {e}")
                self._compensate(i)
                self.status = SagaStatus.FAILED
                return False

        self.status = SagaStatus.COMPLETED
        print(f"\n[Saga] Saga {self.saga_id} COMPLETED")
        return True

    def _compensate(self, failed_step_index: int):
        """执行补偿"""
        print(f"\n[Saga] Compensating steps 1 to {failed_step_index}")
        self.status = SagaStatus.COMPENSATING

        # 逆向执行补偿
        for i in range(failed_step_index - 1, -1, -1):
            step = self.steps[i]
            if step.executed:
                print(f"  Compensating step: {step.name}")
                try:
                    step.compensation()
                    print(f"    Compensation successful")
                except Exception as e:
                    print(f"    Compensation failed: {e}")

        self.status = SagaStatus.COMPENSATED
        print(f"\n[Saga] Saga {self.saga_id} COMPENSATED")


# ==================== 使用示例 ====================

def demo_saga():
    """Saga演示 - 旅游预订"""
    print("="*60)
    print("Saga Distributed Transaction Demo")
    print("="*60)

    # 模拟预订状态
    bookings = {
        'flight': None,
        'hotel': None,
        'car': None
    }

    # 创建Saga
    saga = SagaOrchestrator('TRAVEL-001')

    # 预订航班
    def book_flight():
        print("  Booking flight...")
        bookings['flight'] = {'id': 'FL-001', 'status': 'booked'}
        return bookings['flight']

    def cancel_flight():
        print("  Cancelling flight...")
        bookings['flight']['status'] = 'cancelled'

    # 预订酒店
    def book_hotel():
        print("  Booking hotel...")
        bookings['hotel'] = {'id': 'HT-001', 'status': 'booked'}
        return bookings['hotel']

    def cancel_hotel():
        print("  Cancelling hotel...")
        bookings['hotel']['status'] = 'cancelled'

    # 租车（模拟失败）
    def rent_car():
        print("  Renting car...")
        raise Exception("Car rental service unavailable")

    def cancel_car():
        print("  Cancelling car rental...")
        if bookings['car']:
            bookings['car']['status'] = 'cancelled'

    # 添加步骤
    saga.add_step(SagaStep('book_flight', book_flight, cancel_flight))
    saga.add_step(SagaStep('book_hotel', book_hotel, cancel_hotel))
    saga.add_step(SagaStep('rent_car', rent_car, cancel_car))

    # 执行Saga
    success = saga.execute()

    print(f"\nFinal bookings: {bookings}")
    print(f"Saga status: {saga.status.value}")


if __name__ == '__main__':
    demo_saga()
```

### 5.4 本地消息表

**概念定义**

本地消息表是一种最终一致性的分布式事务方案。将消息和业务数据在同一个本地事务中写入数据库，然后通过定时任务或消息队列异步发送消息。

**Python实现**

```python
"""
本地消息表实现
"""
import sqlite3
import json
import time
import threading
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import queue


class MessageStatus(Enum):
    """消息状态"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


@dataclass
class Message:
    """消息"""
    id: int
    topic: str
    payload: Dict
    status: MessageStatus
    retry_count: int
    created_at: float


class LocalMessageTable:
    """本地消息表"""

    def __init__(self, db_path: str = ':memory:'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 业务表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS business_data (
                id INTEGER PRIMARY KEY,
                data TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        ''')

        # 消息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                payload TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                retry_count INTEGER DEFAULT 0,
                created_at REAL NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def execute_with_message(
        self,
        business_sql: str,
        business_params: tuple,
        message_topic: str,
        message_payload: Dict
    ) -> bool:
        """
        执行业务操作并记录消息（在同一事务中）
        """
        conn = sqlite3.connect(self.db_path)

        try:
            cursor = conn.cursor()

            # 执行业务操作
            cursor.execute(business_sql, business_params)

            # 记录消息
            cursor.execute('''
                INSERT INTO message_table (topic, payload, status, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                message_topic,
                json.dumps(message_payload),
                MessageStatus.PENDING.value,
                time.time()
            ))

            conn.commit()
            print(f"[LocalMessage] Business executed and message recorded")
            return True

        except Exception as e:
            conn.rollback()
            print(f"[LocalMessage] Transaction failed: {e}")
            return False
        finally:
            conn.close()

    def get_pending_messages(self, limit: int = 100) -> List[Message]:
        """获取待发送消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, topic, payload, status, retry_count, created_at
            FROM message_table
            WHERE status = ?
            LIMIT ?
        ''', (MessageStatus.PENDING.value, limit))

        rows = cursor.fetchall()
        conn.close()

        return [
            Message(
                id=row[0],
                topic=row[1],
                payload=json.loads(row[2]),
                status=MessageStatus(row[3]),
                retry_count=row[4],
                created_at=row[5]
            )
            for row in rows
        ]

    def mark_message_sent(self, message_id: int):
        """标记消息已发送"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE message_table
            SET status = ?
            WHERE id = ?
        ''', (MessageStatus.SENT.value, message_id))

        conn.commit()
        conn.close()

    def increment_retry(self, message_id: int):
        """增加重试次数"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE message_table
            SET retry_count = retry_count + 1
            WHERE id = ?
        ''', (message_id,))

        conn.commit()
        conn.close()


class MessageRelayService:
    """消息投递服务"""

    def __init__(self, message_table: LocalMessageTable):
        self.message_table = message_table
        self.running = False
        self.message_queue = queue.Queue()

    def start(self):
        """启动消息投递服务"""
        self.running = True

        # 启动扫描线程
        scan_thread = threading.Thread(target=self._scan_loop)
        scan_thread.daemon = True
        scan_thread.start()

        # 启动投递线程
        relay_thread = threading.Thread(target=self._relay_loop)
        relay_thread.daemon = True
        relay_thread.start()

    def _scan_loop(self):
        """扫描消息表"""
        while self.running:
            messages = self.message_table.get_pending_messages()

            for message in messages:
                self.message_queue.put(message)

            time.sleep(5)  # 每5秒扫描一次

    def _relay_loop(self):
        """投递消息"""
        while self.running:
            try:
                message = self.message_queue.get(timeout=1)
                self._send_message(message)
            except queue.Empty:
                continue

    def _send_message(self, message: Message):
        """发送消息到消息队列"""
        print(f"[Relay] Sending message {message.id} to topic {message.topic}")

        try:
            # 模拟发送到消息队列
            print(f"  Payload: {message.payload}")

            # 标记为已发送
            self.message_table.mark_message_sent(message.id)
            print(f"  Message {message.id} sent successfully")

        except Exception as e:
            print(f"  Failed to send message {message.id}: {e}")
            self.message_table.increment_retry(message.id)

    def stop(self):
        """停止服务"""
        self.running = False


# ==================== 使用示例 ====================

def demo_local_message_table():
    """本地消息表演示"""
    print("="*60)
    print("Local Message Table Demo")
    print("="*60)

    # 创建本地消息表
    message_table = LocalMessageTable()

    # 创建消息投递服务
    relay_service = MessageRelayService(message_table)
    relay_service.start()

    # 模拟订单创建
    print("\n--- Creating order ---")
    order_data = {
        'order_id': 'ORDER-001',
        'user_id': 'USER-001',
        'amount': 100.00,
        'items': [{'product_id': 'P001', 'quantity': 2}]
    }

    # 在同一事务中保存订单和消息
    success = message_table.execute_with_message(
        business_sql='INSERT INTO business_data (data, created_at) VALUES (?, ?)',
        business_params=(json.dumps(order_data), time.time()),
        message_topic='order_created',
        message_payload=order_data
    )

    print(f"Order creation: {'SUCCESS' if success else 'FAILED'}")

    # 等待消息投递
    print("\n--- Waiting for message relay ---")
    time.sleep(3)

    # 检查消息状态
    pending = message_table.get_pending_messages()
    print(f"Pending messages: {len(pending)}")

    relay_service.stop()


if __name__ == '__main__':
    demo_local_message_table()
```

---

## 第六部分：分布式缓存

### 6.1 Redis集群

**概念定义**

Redis集群提供数据分片和高可用性。数据自动分布在多个节点上，支持主从复制和故障转移。

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Redis Cluster 架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Redis Cluster                         │    │
│  │                   (16384 hash slots)                     │
│  │                                                          │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │    │
│  │  │  Master A   │  │  Master B   │  │  Master C   │     │    │
│  │  │ (slots 0-5k)│  │(slots 5k-10k│  │(slots 10k-16k)     │    │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │    │
│  │         │                │                │              │    │
│  │    ┌────┴────┐      ┌────┴────┐      ┌────┴────┐       │    │
│  │    │ Replica │      │ Replica │      │ Replica │       │    │
│  │    │   A'    │      │   B'    │      │   C'    │       │    │
│  │    └─────────┘      └─────────┘      └─────────┘       │    │
│  │                                                          │    │
│  │  特点:                                                   │    │
│  │  - 自动分片: 数据分布在16384个slot中                     │    │
│  │  - 主从复制: 每个主节点有从节点                          │    │
│  │  - 故障转移: 主节点故障时从节点自动提升                  │    │
│  │  - 无中心架构: 所有节点平等，Gossip协议通信              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  数据路由:                                                       │
│  CRC16(key) % 16384 = slot number                               │
└─────────────────────────────────────────────────────────────────┘
```

**Python实现**

```python
"""
Redis集群操作示例
"""
import redis
from rediscluster import RedisCluster
from typing import List, Dict, Optional
import hashlib


class RedisClusterClient:
    """Redis集群客户端"""

    def __init__(self, startup_nodes: List[Dict]):
        """
        Args:
            startup_nodes: 启动节点列表，如 [{'host': '127.0.0.1', 'port': 7000}]
        """
        self.rc = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=True,
            skip_full_coverage_check=True
        )

    def set(self, key: str, value: str, expire: int = None) -> bool:
        """设置键值"""
        return self.rc.set(key, value, ex=expire)

    def get(self, key: str) -> Optional[str]:
        """获取键值"""
        return self.rc.get(key)

    def delete(self, key: str) -> int:
        """删除键"""
        return self.rc.delete(key)

    def get_slot(self, key: str) -> int:
        """获取key对应的slot"""
        return redis.cluster.key_slot(key)

    def get_node_for_key(self, key: str) -> str:
        """获取key所在的节点"""
        slot = self.get_slot(key)
        node = self.rc.connection_pool.get_node_by_slot(slot)
        return f"{node['host']}:{node['port']}"

    def mget(self, keys: List[str]) -> List[Optional[str]]:
        """批量获取（注意：可能跨多个节点）"""
        return self.rc.mget(keys)

    def pipeline(self):
        """获取管道对象"""
        return self.rc.pipeline()

    def info(self) -> Dict:
        """获取集群信息"""
        return self.rc.info()


# ==================== 使用示例 ====================

def demo_cluster():
    """Redis集群演示"""
    print("="*60)
    print("Redis Cluster Demo")
    print("="*60)

    # 启动节点配置
    startup_nodes = [
        {"host": "127.0.0.1", "port": "7000"},
        {"host": "127.0.0.1", "port": "7001"},
        {"host": "127.0.0.1", "port": "7002"},
    ]

    try:
        client = RedisClusterClient(startup_nodes)

        # 写入数据
        print("\n--- Writing data ---")
        keys = ['user:1', 'user:2', 'user:3', 'order:1', 'order:2']
        for i, key in enumerate(keys):
            client.set(key, f"value-{i}")
            slot = client.get_slot(key)
            node = client.get_node_for_key(key)
            print(f"  {key} -> slot {slot} -> {node}")

        # 读取数据
        print("\n--- Reading data ---")
        for key in keys:
            value = client.get(key)
            print(f"  {key}: {value}")

        # 批量操作
        print("\n--- Pipeline operations ---")
        pipe = client.pipeline()
        for i in range(10):
            pipe.set(f"batch:{i}", f"value-{i}")
        results = pipe.execute()
        print(f"  Pipeline executed: {len(results)} commands")

    except Exception as e:
        print(f"Redis Cluster not available: {e}")
        print("Note: This demo requires a running Redis Cluster")


if __name__ == '__main__':
    demo_cluster()
```

### 6.2 缓存策略

#### 6.2.1 缓存穿透、击穿、雪崩

**概念定义**

- **缓存穿透**：查询不存在的数据，绕过缓存直接访问数据库
- **缓存击穿**：热点key过期，大量请求同时访问数据库
- **缓存雪崩**：大量key同时过期，数据库压力激增

**解决方案：**

- 穿透：布隆过滤器、缓存空值
- 击穿：互斥锁、逻辑过期
- 雪崩：随机过期时间、多级缓存

**Python实现**

```python
"""
缓存问题解决方案
"""
import redis
import threading
import time
import hashlib
from typing import Optional, Callable, Any
from dataclasses import dataclass
import mmh3  # murmurhash3
from bitarray import bitarray


class BloomFilter:
    """布隆过滤器 - 解决缓存穿透"""

    def __init__(self, size: int = 1000000, hash_count: int = 7):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.lock = threading.Lock()

    def _get_hashes(self, item: str) -> list:
        """获取多个哈希值"""
        hashes = []
        for i in range(self.hash_count):
            hash_val = mmh3.hash(item, i) % self.size
            hashes.append(hash_val)
        return hashes

    def add(self, item: str):
        """添加元素"""
        with self.lock:
            for hash_val in self._get_hashes(item):
                self.bit_array[hash_val] = 1

    def contains(self, item: str) -> bool:
        """检查元素可能存在（有一定误判率）或肯定不存在"""
        for hash_val in self._get_hashes(item):
            if not self.bit_array[hash_val]:
                return False
        return True


class CachePenetrationSolution:
    """缓存穿透解决方案"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.bloom = BloomFilter()
        self.null_value_ttl = 60  # 空值缓存时间

    def get_with_bloom_filter(
        self,
        key: str,
        db_query: Callable[[], Any]
    ) -> Any:
        """使用布隆过滤器防止缓存穿透"""
        # 先检查布隆过滤器
        if not self.bloom.contains(key):
            # 肯定不存在，直接返回None
            return None

        # 查询缓存
        value = self.redis.get(key)
        if value:
            return value

        # 查询数据库
        value = db_query()

        if value:
            self.redis.setex(key, 3600, value)
        else:
            # 缓存空值
            self.redis.setex(f"null:{key}", self.null_value_ttl, "null")

        return value

    def add_to_bloom(self, key: str):
        """将key添加到布隆过滤器"""
        self.bloom.add(key)


class CacheBreakdownSolution:
    """缓存击穿解决方案"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.locks: dict = {}
        self.lock_timeout = 10

    def get_with_mutex(
        self,
        key: str,
        db_query: Callable[[], Any],
        cache_ttl: int = 3600
    ) -> Any:
        """使用互斥锁防止缓存击穿"""
        # 查询缓存
        value = self.redis.get(key)
        if value:
            return value

        # 获取锁
        lock_key = f"lock:{key}"
        lock_acquired = self.redis.set(
            lock_key,
            "1",
            nx=True,
            ex=self.lock_timeout
        )

        if lock_acquired:
            try:
                # 双重检查
                value = self.redis.get(key)
                if value:
                    return value

                # 查询数据库
                value = db_query()
                if value:
                    self.redis.setex(key, cache_ttl, value)

                return value
            finally:
                self.redis.delete(lock_key)
        else:
            # 未获取到锁，短暂等待后重试
            time.sleep(0.1)
            return self.redis.get(key)

    def get_with_logical_expire(
        self,
        key: str,
        db_query: Callable[[], Any],
        cache_ttl: int = 3600,
        logical_ttl: int = 300
    ) -> Any:
        """使用逻辑过期防止缓存击穿"""
        # 查询缓存（不过期）
        value = self.redis.get(key)

        if value:
            # 解析数据和过期时间
            import json
            data = json.loads(value)

            if data['expire_time'] > time.time():
                # 未过期，直接返回
                return data['value']

            # 已过期，尝试重建
            lock_key = f"lock:{key}"
            lock_acquired = self.redis.set(lock_key, "1", nx=True, ex=10)

            if lock_acquired:
                # 异步重建缓存
                threading.Thread(
                    target=self._rebuild_cache,
                    args=(key, db_query, cache_ttl, logical_ttl)
                ).start()

            # 返回过期数据（总比没有好）
            return data['value']

        # 缓存不存在，查询数据库
        value = db_query()
        if value:
            self._set_with_logical_expire(key, value, logical_ttl)

        return value

    def _rebuild_cache(self, key: str, db_query: Callable, cache_ttl: int, logical_ttl: int):
        """重建缓存"""
        try:
            value = db_query()
            if value:
                self._set_with_logical_expire(key, value, logical_ttl)
        finally:
            self.redis.delete(f"lock:{key}")

    def _set_with_logical_expire(self, key: str, value: Any, logical_ttl: int):
        """设置逻辑过期时间"""
        import json
        data = {
            'value': value,
            'expire_time': time.time() + logical_ttl
        }
        # 物理不过期，逻辑过期
        self.redis.set(key, json.dumps(data))


class CacheAvalancheSolution:
    """缓存雪崩解决方案"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.local_cache = {}  # 本地缓存作为二级缓存
        self.local_cache_ttl = 60

    def set_with_random_ttl(
        self,
        key: str,
        value: Any,
        base_ttl: int = 3600,
        variance: int = 300
    ):
        """设置随机过期时间"""
        import random
        ttl = base_ttl + random.randint(0, variance)
        self.redis.setex(key, ttl, value)

    def get_with_multi_level(
        self,
        key: str,
        db_query: Callable[[], Any]
    ) -> Any:
        """多级缓存防止雪崩"""
        # L1: 本地缓存
        if key in self.local_cache:
            value, expire_time = self.local_cache[key]
            if time.time() < expire_time:
                return value

        # L2: Redis缓存
        value = self.redis.get(key)
        if value:
            # 回填本地缓存
            self.local_cache[key] = (value, time.time() + self.local_cache_ttl)
            return value

        # L3: 数据库
        value = db_query()
        if value:
            self.redis.setex(key, 3600, value)
            self.local_cache[key] = (value, time.time() + self.local_cache_ttl)

        return value

    def preheat_cache(self, keys_values: dict, base_ttl: int = 3600):
        """缓存预热"""
        for key, value in keys_values.items():
            self.set_with_random_ttl(key, value, base_ttl)


# ==================== 使用示例 ====================

def demo_cache_solutions():
    """缓存问题解决方案演示"""
    print("="*60)
    print("Cache Problem Solutions Demo")
    print("="*60)

    # 模拟Redis
    class MockRedis:
        def __init__(self):
            self.data = {}

        def get(self, key):
            return self.data.get(key)

        def set(self, key, value, nx=False, ex=None):
            if nx and key in self.data:
                return None
            self.data[key] = value
            return True

        def setex(self, key, ttl, value):
            self.data[key] = value

        def delete(self, key):
            self.data.pop(key, None)

    mock_redis = MockRedis()

    # 布隆过滤器演示
    print("\n--- Bloom Filter Demo ---")
    bloom = BloomFilter(size=1000, hash_count=5)

    # 添加一些key
    for i in range(100):
        bloom.add(f"user:{i}")

    # 测试
    print(f"Contains user:50? {bloom.contains('user:50')}")
    print(f"Contains user:999? {bloom.contains('user:999')}")
    print(f"Contains not_exist? {bloom.contains('not_exist')}")

    # 缓存击穿解决方案演示
    print("\n--- Cache Breakdown Solution ---")
    solution = CacheBreakdownSolution(mock_redis)

    def db_query():
        print("  Querying database...")
        return "database_value"

    # 模拟并发请求
    import threading
    results = []

    def request():
        result = solution.get_with_mutex("hot_key", db_query, 3600)
        results.append(result)

    threads = [threading.Thread(target=request) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Results: {results}")
    print("Note: Only one database query should be executed")


if __name__ == '__main__':
    demo_cache_solutions()
```

---

## 第七部分：数据分片

### 7.1 水平分片

**概念定义**

水平分片（Horizontal Sharding）将同一张表的数据按行分散到多个数据库中，每个数据库包含部分数据。

**Python实现**

```python
"""
水平分片实现
"""
import hashlib
from typing import List, Dict, Any, Callable


class HorizontalShardRouter:
    """水平分片路由器"""

    def __init__(self, shard_count: int):
        self.shard_count = shard_count
        self.shards: Dict[int, Any] = {}

    def register_shard(self, shard_id: int, connection: Any):
        """注册分片"""
        self.shards[shard_id] = connection

    def get_shard_id(self, shard_key: str) -> int:
        """根据分片键计算分片ID"""
        hash_val = int(hashlib.md5(str(shard_key).encode()).hexdigest(), 16)
        return hash_val % self.shard_count

    def get_shard(self, shard_key: str) -> Any:
        """获取分片连接"""
        shard_id = self.get_shard_id(shard_key)
        return self.shards.get(shard_id)

    def route_query(self, shard_key: str, query_func: Callable, *args, **kwargs):
        """路由查询到对应分片"""
        shard = self.get_shard(shard_key)
        if not shard:
            raise Exception(f"Shard not found for key: {shard_key}")
        return query_func(shard, *args, **kwargs)

    def broadcast_query(self, query_func: Callable, *args, **kwargs) -> List:
        """广播查询到所有分片"""
        results = []
        for shard_id, shard in self.shards.items():
            result = query_func(shard, *args, **kwargs)
            results.append(result)
        return results


# ==================== 使用示例 ====================

def demo_horizontal_sharding():
    """水平分片演示"""
    print("="*60)
    print("Horizontal Sharding Demo")
    print("="*60)

    # 创建路由器（4个分片）
    router = HorizontalShardRouter(shard_count=4)

    # 注册分片
    for i in range(4):
        router.register_shard(i, f"db-shard-{i}")

    # 测试分片路由
    user_ids = ['user-1', 'user-2', 'user-3', 'user-100', 'user-999']

    print("\n--- Shard Routing ---")
    for user_id in user_ids:
        shard_id = router.get_shard_id(user_id)
        shard = router.get_shard(user_id)
        print(f"  {user_id} -> shard {shard_id} -> {shard}")


if __name__ == '__main__':
    demo_horizontal_sharding()
```

### 7.2 垂直分片

**概念定义**

垂直分片（Vertical Sharding）将表的不同字段分散到不同数据库中，通常按业务模块划分。

### 7.3 分片策略

**Python实现**

```python
"""
分片策略实现
"""
import hashlib
from typing import List, Dict, Any
from enum import Enum


class ShardStrategy(Enum):
    """分片策略"""
    HASH = "hash"           # 哈希分片
    RANGE = "range"         # 范围分片
    LIST = "list"           # 列表分片
    MODULO = "modulo"       # 取模分片


class HashShardStrategy:
    """哈希分片策略"""

    def __init__(self, shard_count: int):
        self.shard_count = shard_count

    def get_shard(self, shard_key: Any) -> int:
        """获取分片ID"""
        hash_val = int(hashlib.md5(str(shard_key).encode()).hexdigest(), 16)
        return hash_val % self.shard_count


class RangeShardStrategy:
    """范围分片策略"""

    def __init__(self, ranges: List[tuple]):
        """
        Args:
            ranges: 范围列表，如 [(0, 1000), (1000, 2000), (2000, None)]
        """
        self.ranges = sorted(ranges, key=lambda x: x[0])

    def get_shard(self, shard_key: int) -> int:
        """获取分片ID"""
        for i, (start, end) in enumerate(self.ranges):
            if end is None:
                if shard_key >= start:
                    return i
            elif start <= shard_key < end:
                return i
        raise ValueError(f"Key {shard_key} out of range")


class ModuloShardStrategy:
    """取模分片策略"""

    def __init__(self, shard_count: int):
        self.shard_count = shard_count

    def get_shard(self, shard_key: int) -> int:
        """获取分片ID"""
        return shard_key % self.shard_count


# ==================== 使用示例 ====================

def demo_shard_strategies():
    """分片策略演示"""
    print("="*60)
    print("Shard Strategies Demo")
    print("="*60)

    # 哈希分片
    print("\n--- Hash Sharding ---")
    hash_strategy = HashShardStrategy(shard_count=4)
    for i in range(10):
        shard = hash_strategy.get_shard(f"user-{i}")
        print(f"  user-{i} -> shard {shard}")

    # 范围分片
    print("\n--- Range Sharding ---")
    range_strategy = RangeShardStrategy([
        (0, 1000),
        (1000, 2000),
        (2000, None)
    ])
    for user_id in [100, 999, 1000, 1500, 2000, 5000]:
        shard = range_strategy.get_shard(user_id)
        print(f"  user_id={user_id} -> shard {shard}")

    # 取模分片
    print("\n--- Modulo Sharding ---")
    modulo_strategy = ModuloShardStrategy(shard_count=4)
    for i in range(10):
        shard = modulo_strategy.get_shard(i)
        print(f"  id={i} -> shard {shard}")


if __name__ == '__main__':
    demo_shard_strategies()
```

---

## 第八部分：微服务架构

### 8.1 服务拆分原则

**核心原则：**

1. **单一职责原则（SRP）**：每个服务只负责一个业务功能
2. **高内聚低耦合**：服务内部紧密相关，服务间依赖最小
3. **按业务能力拆分**：根据业务边界划分服务
4. **按数据边界拆分**：每个服务管理自己的数据

**拆分策略：**

| 策略 | 说明 | 示例 |
|------|------|------|
| 按业务功能 | 按业务模块拆分 | 用户服务、订单服务、支付服务 |
| 按数据边界 | 每个服务管理独立数据 | 用户数据、订单数据分离 |
| 按读写分离 | 读服务和写服务分离 | 商品查询服务、商品管理服务 |
| 按优先级 | 核心服务和辅助服务分离 | 核心交易服务、日志服务 |

### 8.2 API网关

**概念定义**

API网关是微服务架构的入口，提供统一的服务访问点，处理认证、限流、路由等功能。

**Python实现**

```python
"""
API网关实现
"""
from flask import Flask, request, jsonify, Response
import requests
import time
import functools
from typing import Dict, List, Callable


class APIGateway:
    """API网关"""

    def __init__(self):
        self.app = Flask(__name__)
        self.routes: Dict[str, Dict] = {}
        self.middlewares: List[Callable] = []
        self.rate_limiter = TokenBucketRateLimiter(rate=100, capacity=200)

        self._register_default_routes()

    def _register_default_routes(self):
        """注册默认路由"""

        @self.app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def proxy(service, path):
            return self._handle_request(service, path)

        @self.app.route('/health')
        def health():
            return jsonify({'status': 'healthy'})

        @self.app.route('/routes')
        def list_routes():
            return jsonify(self.routes)

    def register_service(self, name: str, base_url: str, prefix: str = None):
        """注册服务"""
        self.routes[name] = {
            'base_url': base_url,
            'prefix': prefix or f'/{name}'
        }

    def add_middleware(self, middleware: Callable):
        """添加中间件"""
        self.middlewares.append(middleware)

    def _handle_request(self, service: str, path: str) -> Response:
        """处理请求"""
        # 限流检查
        if not self.rate_limiter.allow_request():
            return jsonify({'error': 'Rate limit exceeded'}), 429

        # 查找服务
        route = self.routes.get(service)
        if not route:
            return jsonify({'error': f'Service {service} not found'}), 404

        # 构建目标URL
        target_url = f"{route['base_url']}/{path}"

        # 转发请求
        try:
            resp = requests.request(
                method=request.method,
                url=target_url,
                headers={k: v for k, v in request.headers if k != 'Host'},
                data=request.get_data(),
                params=request.args,
                timeout=30
            )

            return Response(
                resp.content,
                status=resp.status_code,
                headers=dict(resp.headers)
            )
        except requests.RequestException as e:
            return jsonify({'error': str(e)}), 502

    def run(self, host='0.0.0.0', port=8080):
        """运行网关"""
        self.app.run(host=host, port=port)


class TokenBucketRateLimiter:
    """令牌桶限流器"""

    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()

    def allow_request(self, tokens: int = 1) -> bool:
        """是否允许请求"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


# ==================== 使用示例 ====================

def demo_api_gateway():
    """API网关演示"""
    print("="*60)
    print("API Gateway Demo")
    print("="*60)

    gateway = APIGateway()

    # 注册服务
    gateway.register_service('user-service', 'http://localhost:8001')
    gateway.register_service('order-service', 'http://localhost:8002')
    gateway.register_service('payment-service', 'http://localhost:8003')

    print("Registered services:")
    for name, route in gateway.routes.items():
        print(f"  {name}: {route['base_url']}")


if __name__ == '__main__':
    demo_api_gateway()
```

### 8.3 服务网格概念

**概念定义**

服务网格（Service Mesh）是处理服务间通信的基础设施层，将服务发现、负载均衡、熔断、监控等功能从应用代码中剥离出来。

**核心组件：**

- **数据平面**：Sidecar代理（如Envoy），处理服务间通信
- **控制平面**：管理和配置代理（如Istio、Linkerd）

**架构图（文字描述）**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Service Mesh 架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   Control Plane                          │    │
│  │              (Istio / Linkerd / Consul)                  │    │
│  │                                                          │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │    │
│  │  │  Pilot  │  │ Citadel │  │ Galley  │                 │    │
│  │  │(服务发现)│  │ (安全)  │  │(配置)   │                 │    │
│  │  └─────────┘  └─────────┘  └─────────┘                 │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│                           │ 配置下发                             │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Data Plane                            │    │
│  │                   (Envoy Sidecar)                        │    │
│  │                                                          │    │
│  │  ┌─────────┐      ┌─────────┐      ┌─────────┐         │    │
│  │  │Service A│◄────►│Service B│◄────►│Service C│         │    │
│  │  │┌───────┐│      │┌───────┐│      │┌───────┐│         │    │
│  │  ││Envoy  ││      ││Envoy  ││      ││Envoy  ││         │    │
│  │  ││Sidecar││      ││Sidecar││      ││Sidecar││         │    │
│  │  │└───────┘│      │└───────┘│      │└───────┘│         │    │
│  │  └─────────┘      └─────────┘      └─────────┘         │    │
│  │                                                          │    │
│  │  Sidecar功能:                                            │    │
│  │  - 服务发现    - 负载均衡    - 熔断器                    │    │
│  │  - mTLS加密    - 流量管理    - 可观测性                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  优点:                                                           │
│  - 应用无感知，无需修改代码                                      │
│  - 语言无关，支持任何技术栈                                      │
│  - 集中管理，统一策略                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 总结

本文档全面梳理了Python分布式系统设计中的核心概念和实现方案：

### 关键知识点回顾

1. **分布式通信**：gRPC、RESTful API、消息队列（RabbitMQ、Kafka、Redis Pub/Sub）
2. **分布式一致性**：CAP定理、BASE理论、一致性协议（Raft、Paxos）
3. **服务发现与注册**：Consul、etcd、ZooKeeper
4. **负载均衡与熔断**：多种负载均衡算法、熔断器模式、限流算法
5. **分布式事务**：2PC、TCC、Saga、本地消息表
6. **分布式缓存**：Redis集群、缓存策略
7. **数据分片**：水平分片、垂直分片、分片策略
8. **微服务架构**：服务拆分原则、API网关、服务网格

### 最佳实践建议

1. 根据业务场景选择合适的CAP权衡
2. 优先使用成熟的分布式组件（如etcd、Consul）
3. 实现完善的监控和告警机制
4. 设计降级策略，保证系统可用性
5. 进行充分的混沌工程测试

---

*文档生成时间: 2024年*
*Python分布式系统设计模型全面指南*
