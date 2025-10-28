# gRPC Python实现

**高性能RPC框架**

---

## 📋 概述

gRPC是Google开发的高性能、开源RPC框架，基于HTTP/2和Protocol Buffers。

### 核心特性

- ⚡ **高性能** - HTTP/2 + Protobuf
- 🔄 **双向流** - 支持流式传输
- 🌐 **跨语言** - 多语言支持
- 🎯 **强类型** - Protocol Buffers

---

## 🚀 快速开始

### 安装

```bash
uv add grpcio grpcio-tools
```

### 定义服务 (.proto)

```protobuf
// hello.proto
syntax = "proto3";

package hello;

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

### 生成代码

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hello.proto
```

---

## 💻 服务器实现

```python
import grpc
from concurrent import futures
import hello_pb2
import hello_pb2_grpc

class GreeterServicer(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(
            message=f'Hello, {request.name}!'
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(
        GreeterServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

---

## 📡 客户端实现

```python
import grpc
import hello_pb2
import hello_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name='World'))
        print(f"Greeter client received: {response.message}")

if __name__ == '__main__':
    run()
```

---

## 🔄 流式RPC

### 服务器流式

```protobuf
service DataService {
  rpc GetStream (Request) returns (stream Data) {}
}
```

```python
def GetStream(self, request, context):
    for i in range(10):
        yield Data(value=i)
```

### 客户端流式

```protobuf
service DataService {
  rpc UploadStream (stream Data) returns (Response) {}
}
```

```python
def UploadStream(self, request_iterator, context):
    for data in request_iterator:
        process(data)
    return Response(status='ok')
```

---

## 📚 最佳实践

### 异步gRPC

```python
import grpc.aio

class AsyncGreeterServicer(hello_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        return hello_pb2.HelloReply(
            message=f'Hello, {request.name}!'
        )

async def serve():
    server = grpc.aio.server()
    hello_pb2_grpc.add_GreeterServicer_to_server(
        AsyncGreeterServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()
```

---

## 🔗 相关资源

- [官方文档](https://grpc.io/docs/languages/python/)
- [Protocol Buffers](https://protobuf.dev/)

---

**最后更新**: 2025年10月28日

