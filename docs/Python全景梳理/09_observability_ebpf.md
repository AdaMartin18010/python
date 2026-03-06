              f"Duration: {duration_ms:.3f}ms Len: {event.len}")

    b["ssl_events"].open_perf_buffer(print_event)

    try:
        while True:
            b.perf_buffer_poll()
    except KeyboardInterrupt:
        print("\nExiting...")


# ==================== 运行示例 ====================

if __name__ == "__main__":
    import os

    if os.geteuid() != 0:
        print("This script must be run as root!")
        exit(1)

    print("=" * 50)
    print("eBPF uprobe/uretprobe 示例")
    print("=" * 50)

    # 取消注释以运行示例
    # basic_uprobe_example()
    # trace_library_function()
    # trace_ssl_operations()

```

---

## 第四部分：分布式追踪实现

### 4.1 上下文传播

#### 4.1.1 W3C Trace Context

**概念定义**

W3C Trace Context是W3C标准化的分布式追踪上下文传播规范，定义了traceparent和tracestate两个HTTP头字段。

**traceparent格式**

```

traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             │  │                                  │                │
             │  │                                  │                └── flags
             │  │                                  │                    (8-bit)
             │  │                                  └── parent-id (16 hex)
             │  │                                      (span-id)
             │  └── trace-id (32 hex)
             │      (全局唯一)
             └── version (2 hex)

```

**Python实现**

```python
"""
W3C Trace Context 实现
"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.propagate import extract, inject
import requests


# ==================== 1. 基础传播 ====================

def basic_propagation():
    """基础上下文传播"""

    # 设置TracerProvider
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    # 创建根Span
    with tracer.start_as_current_span("parent-operation") as span:
        print(f"Trace ID: {span.get_span_context().trace_id:032x}")
        print(f"Span ID: {span.get_span_context().span_id:016x}")

        # 创建carrier（HTTP头）
        carrier = {}

        # 注入上下文到carrier
        TraceContextTextMapPropagator().inject(carrier)

        print(f"\nInjected headers:")
        for key, value in carrier.items():
            print(f"  {key}: {value}")

        # 模拟下游服务接收
        print(f"\nSimulating downstream service...")

        # 提取上下文
        ctx = TraceContextTextMapPropagator().extract(carrier)

        # 创建子Span（延续trace）
        with tracer.start_as_current_span("child-operation", context=ctx) as child_span:
            print(f"Child Trace ID: {child_span.get_span_context().trace_id:032x}")
            print(f"Child Span ID: {child_span.get_span_context().span_id:016x}")
            print(f"Child Parent ID: {span.get_span_context().span_id:016x}")


# ==================== 2. HTTP请求传播 ====================

def http_propagation_example():
    """HTTP请求上下文传播"""

    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    class TracedHTTPClient:
        """带追踪的HTTP客户端"""

        def __init__(self):
            self.session = requests.Session()

        def request(self, method: str, url: str, **kwargs):
            tracer = trace.get_tracer(__name__)

            with tracer.start_as_current_span(
                f"HTTP {method}",
                kind=trace.SpanKind.CLIENT
            ) as span:
                # 设置Span属性
                span.set_attributes({
                    "http.method": method,
                    "http.url": url,
                })

                # 注入追踪上下文到请求头
                headers = kwargs.pop('headers', {})
                TraceContextTextMapPropagator().inject(headers)

                span.set_attribute("http.request.headers", str(headers))

                # 发送请求
                try:
                    response = self.session.request(
                        method, url, headers=headers, **kwargs
                    )

                    span.set_attributes({
                        "http.status_code": response.status_code,
                        "http.response_content_length": len(response.content)
                    })

                    if response.status_code >= 400:
                        span.set_status(trace.Status(trace.StatusCode.ERROR))

                    return response

                except Exception as e:
                    span.record_exception(e)
                    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                    raise

    # 使用示例
    client = TracedHTTPClient()

    # 模拟请求（不会真正发送）
    print("HTTP Client with Trace Context propagation")
    print("Headers will include traceparent for distributed tracing")


# ==================== 3. 消息队列传播 ====================

def messaging_propagation_example():
    """消息队列上下文传播"""

    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    class TracedMessageProducer:
        """带追踪的消息生产者"""

        def send(self, topic: str, message: dict):
            with tracer.start_as_current_span(
                "send-message",
                kind=trace.SpanKind.PRODUCER
            ) as span:
                span.set_attributes({
                    "messaging.system": "kafka",
                    "messaging.destination": topic,
                    "messaging.destination_kind": "topic"
                })

                # 注入上下文到消息属性
                properties = {}
                TraceContextTextMapPropagator().inject(properties)

                # 添加追踪信息到消息
                message['_trace_context'] = properties

                print(f"Sending message to {topic}")
                print(f"Trace context injected: {properties}")

                return message

    class TracedMessageConsumer:
        """带追踪的消息消费者"""

        def receive(self, message: dict):
            # 提取追踪上下文
            properties = message.pop('_trace_context', {})
            ctx = TraceContextTextMapPropagator().extract(properties)

            with tracer.start_as_current_span(
                "receive-message",
                context=ctx,
                kind=trace.SpanKind.CONSUMER
            ) as span:
                span.set_attributes({
                    "messaging.system": "kafka",
                    "messaging.operation": "receive"
                })

                print(f"Received message")
                print(f"Continuing trace: {span.get_span_context().trace_id:032x}")

                return message

    # 使用示例
    producer = TracedMessageProducer()
    consumer = TracedMessageConsumer()

    # 发送消息
    message = {"order_id": "123", "amount": 99.99}
    sent_message = producer.send("orders-topic", message)

    # 接收消息
    received_message = consumer.receive(sent_message)


# ==================== 4. 异步任务传播 ====================

def async_propagation_example():
    """异步任务上下文传播"""

    import asyncio
    from opentelemetry.context import attach, detach, get_current

    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    async def async_task(task_id: int, parent_context):
        """异步任务 - 使用父上下文"""
        # 附加父上下文
        token = attach(parent_context)

        try:
            with tracer.start_as_current_span(f"async-task-{task_id}") as span:
                span.set_attribute("task.id", task_id)
                await asyncio.sleep(0.1)
                print(f"Task {task_id} completed in trace {span.get_span_context().trace_id:032x}")
        finally:
            detach(token)

    async def main():
        with tracer.start_as_current_span("parent-operation") as span:
            print(f"Parent trace: {span.get_span_context().trace_id:032x}")

            # 获取当前上下文
            parent_context = get_current()

            # 创建多个异步任务，传递上下文
            tasks = [
                async_task(i, parent_context)
                for i in range(3)
            ]

            await asyncio.gather(*tasks)

    # 运行
    asyncio.run(main())


# ==================== 运行示例 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("W3C Trace Context 传播示例")
    print("=" * 50)

    print("\n示例1: 基础传播")
    basic_propagation()

    print("\n示例2: HTTP传播")
    http_propagation_example()

    print("\n示例3: 消息队列传播")
    messaging_propagation_example()

    print("\n示例4: 异步任务传播")
    async_propagation_example()
```

#### 4.1.2 Baggage

__概念定义__

Baggage是一种用于在分布式追踪中传递键值对数据的机制，数据会随追踪上下文一起传播到所有下游服务。

__Baggage使用场景__

| 场景 | 示例 |
|------|------|
| 用户标识 | user_id, tenant_id |
| 请求属性 | request_type, priority |
| 调试信息 | debug_flag, trace_level |
| 业务上下文 | order_id, session_id |

__Python实现__

```python
"""
Baggage 实现和使用
"""
from opentelemetry import trace, baggage
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.context import get_current


# ==================== 1. 基础Baggage ====================

def basic_baggage_example():
    """基础Baggage使用"""

    trace.set_tracer_provider(trace.TracerProvider())
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("parent-operation"):
        # 设置Baggage
        ctx = baggage.set_baggage("user.id", "user-123")
        ctx = baggage.set_baggage("tenant.id", "tenant-456", context=ctx)
        ctx = baggage.set_baggage("request.priority", "high", context=ctx)

        # 获取Baggage
        user_id = baggage.get_baggage("user.id", context=ctx)
        tenant_id = baggage.get_baggage("tenant.id", context=ctx)

        print(f"User ID: {user_id}")
        print(f"Tenant ID: {tenant_id}")

        # 获取所有Baggage
        all_baggage = baggage.get_all(context=ctx)
        print(f"\nAll Baggage: {all_baggage}")

        # 在子Span中使用
        with tracer.start_as_current_span("child-operation", context=ctx):
            # Baggage在子Span中仍然可用
            user_id_child = baggage.get_baggage("user.id")
            print(f"\nChild span - User ID: {user_id_child}")


# ==================== 2. Baggage传播 ====================

def baggage_propagation_example():
    """Baggage传播示例"""

    trace.set_tracer_provider(trace.TracerProvider())
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("service-a"):
        # 设置Baggage
        ctx = baggage.set_baggage("user.id", "user-123")
        ctx = baggage.set_baggage("session.id", "sess-abc", context=ctx)

        # 创建carrier
        carrier = {}

        # 注入Trace Context
        TraceContextTextMapPropagator().inject(carrier, context=ctx)

        # 注入Baggage
        W3CBaggagePropagator().inject(carrier, context=ctx)

        print("Carrier headers:")
        for key, value in carrier.items():
            print(f"  {key}: {value}")

        # 模拟服务B接收
        print("\n--- Service B ---")

        # 提取Trace Context
        trace_ctx = TraceContextTextMapPropagator().extract(carrier)

        # 提取Baggage
        baggage_ctx = W3CBaggagePropagator().extract(carrier)

        # 合并上下文
        from opentelemetry.context import set_value
        merged_ctx = trace_ctx
        for key, value in baggage.get_all(context=baggage_ctx).items():
            merged_ctx = baggage.set_baggage(key, value, context=merged_ctx)

        with tracer.start_as_current_span("service-b", context=merged_ctx):
            user_id = baggage.get_baggage("user.id")
            session_id = baggage.get_baggage("session.id")

            print(f"Received User ID: {user_id}")
            print(f"Received Session ID: {session_id}")


# ==================== 3. Baggage最佳实践 ====================

def baggage_best_practices():
    """Baggage最佳实践"""

    print("""
Baggage最佳实践:

1. 数据大小限制:
   - 每个键值对不超过256字符
   - 总大小不超过8192字符
   - 避免传递大量数据

2. 敏感信息:
   - 不要传递密码、密钥等敏感信息
   - 可以传递用户ID，不要传递PII

3. 命名规范:
   - 使用小写字母和下划线
   - 使用命名空间前缀: service.attribute
   - 示例: user.id, tenant.id, request.priority

4. 使用场景:
   ✓ 用户/租户标识
   ✓ 请求属性（优先级、类型）
   ✓ 调试标志
   ✓ 会话ID

   ✗ 大对象
   ✗ 敏感信息
   ✗ 频繁变化的数据

5. 与Span属性的区别:
   - Baggage: 跨服务传播
   - Span属性: 仅当前Span
""")


# ==================== 4. 完整示例 ====================

def complete_baggage_example():
    """完整Baggage使用示例"""

    trace.set_tracer_provider(trace.TracerProvider())
    tracer = trace.get_tracer(__name__)

    class TracedService:
        """带Baggage支持的服务"""

        def __init__(self, name: str):
            self.name = name
            self.tracer = trace.get_tracer(name)

        def process_request(self, headers: dict):
            """处理请求 - 提取和使用Baggage"""

            # 提取上下文
            ctx = TraceContextTextMapPropagator().extract(headers)
            ctx = W3CBaggagePropagator().extract(headers, context=ctx)

            with self.tracer.start_as_current_span(
                f"{self.name}.process",
                context=ctx
            ) as span:
                # 读取Baggage
                user_id = baggage.get_baggage("user.id", context=ctx)
                tenant_id = baggage.get_baggage("tenant.id", context=ctx)
                priority = baggage.get_baggage("request.priority", context=ctx)

                # 添加到Span属性
                if user_id:
                    span.set_attribute("user.id", user_id)
                if tenant_id:
                    span.set_attribute("tenant.id", tenant_id)
                if priority:
                    span.set_attribute("request.priority", priority)

                print(f"[{self.name}] Processing request:")
                print(f"  User: {user_id}")
                print(f"  Tenant: {tenant_id}")
                print(f"  Priority: {priority}")

                # 可以添加更多Baggage
                ctx = baggage.set_baggage(
                    f"{self.name}.processed_at",
                    "2024-01-15T10:30:00Z",
                    context=ctx
                )

                return ctx

        def call_downstream(self, ctx, downstream_service):
            """调用下游服务 - 传播Baggage"""

            with self.tracer.start_as_current_span(
                f"{self.name}.call_downstream",
                context=ctx
            ):
                # 准备headers
                headers = {}
                TraceContextTextMapPropagator().inject(headers, context=ctx)
                W3CBaggagePropagator().inject(headers, context=ctx)

                print(f"\n[{self.name}] Calling downstream service")
                print(f"  Headers: {headers}")

                # 调用下游
                return downstream_service.process_request(headers)

    # 创建服务链
    service_a = TracedService("service-a")
    service_b = TracedService("service-b")
    service_c = TracedService("service-c")

    # 模拟请求
    with tracer.start_as_current_span("client-request"):
        # 设置初始Baggage
        ctx = baggage.set_baggage("user.id", "user-12345")
        ctx = baggage.set_baggage("tenant.id", "tenant-abc", context=ctx)
        ctx = baggage.set_baggage("request.priority", "high", context=ctx)

        # 准备初始headers
        headers = {}
        TraceContextTextMapPropagator().inject(headers, context=ctx)
        W3CBaggagePropagator().inject(headers, context=ctx)

        print("=" * 50)
        print("分布式Baggage传播示例")
        print("=" * 50)

        # 服务链调用
        ctx = service_a.process_request(headers)
        ctx = service_a.call_downstream(ctx, service_b)
        service_b.call_downstream(ctx, service_c)


# ==================== 运行示例 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("Baggage 示例")
    print("=" * 50)

    print("\n示例1: 基础Baggage")
    basic_baggage_example()

    print("\n示例2: Baggage传播")
    baggage_propagation_example()

    print("\n示例3: 最佳实践")
    baggage_best_practices()

    print("\n示例4: 完整示例")
    complete_baggage_example()
```

---

### 4.2 采样策略

#### 4.2.1 头部采样

__概念定义__

头部采样（Head-based Sampling）在请求开始时决定是否采样，决策在整个请求链路中保持一致。

__采样策略对比__

| 策略 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| __AlwaysOn__ | 全部采样 | 完整数据 | 高开销 |
| __AlwaysOff__ | 不采样 | 零开销 | 无数据 |
| __TraceIdRatio__ | 按比例采样 | 简单可控 | 不均匀 |
| __ParentBased__ | 基于父Span决策 | 保持一致性 | 依赖父决策 |

__Python实现__

```python
"""
头部采样策略实现
"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import (
    ALWAYS_ON,
    ALWAYS_OFF,
    TraceIdRatioBased,
    ParentBased
)
import random


# ==================== 1. 基础采样器 ====================

def always_on_sampler():
    """全部采样"""

    # 配置全部采样
    provider = TracerProvider(sampler=ALWAYS_ON)
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)

    print("AlwaysOn Sampler - All spans are recorded")

    for i in range(5):
        with tracer.start_as_current_span(f"operation-{i}") as span:
            print(f"Span {i}: sampled={span.get_span_context().trace_flags.sampled}")


def always_off_sampler():
    """全部不采样"""

    provider = TracerProvider(sampler=ALWAYS_OFF)
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)

    print("\nAlwaysOff Sampler - No spans are recorded")

    for i in range(5):
        with tracer.start_as_current_span(f"operation-{i}") as span:
            print(f"Span {i}: sampled={span.get_span_context().trace_flags.sampled}")


def ratio_sampler():
    """按比例采样"""

    # 30%采样率
    provider = TracerProvider(sampler=TraceIdRatioBased(0.3))
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)

    print("\nTraceIdRatioBased Sampler (30%)")

    sampled_count = 0
    for i in range(100):
        with tracer.start_as_current_span(f"operation-{i}") as span:
            if span.get_span_context().trace_flags.sampled:
                sampled_count += 1

    print(f"Sampled: {sampled_count}/100 ({sampled_count}%)")


# ==================== 2. 父级基于采样 ====================

def parent_based_sampler():
    """父级基于采样"""

    # 配置：
    # - 根Span：30%采样
    # - 有采样父Span的子Span：采样
    # - 有未采样父Span的子Span：不采样
    provider = TracerProvider(
        sampler=ParentBased(
            root=TraceIdRatioBased(0.3),
            remote_parent_sampled=ALWAYS_ON,
            remote_parent_not_sampled=ALWAYS_OFF,
            local_parent_sampled=ALWAYS_ON,
            local_parent_not_sampled=ALWAYS_OFF
        )
    )
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)

    print("\nParentBased Sampler")

    # 测试1: 采样的父Span
    with tracer.start_as_current_span("sampled-parent") as parent:
        print(f"Parent sampled: {parent.get_span_context().trace_flags.sampled}")

        with tracer.start_as_current_span("child") as child:
            print(f"Child of sampled parent: {child.get_span_context().trace_flags.sampled}")

    # 测试2: 未采样的父Span
    # 强制创建未采样Span（模拟）
    from opentelemetry.trace import SpanContext, TraceFlags
    unsampled_context = trace.set_span_in_context(
        trace.NonRecordingSpan(
            SpanContext(
                trace_id=random.getrandbits(128),
                span_id=random.getrandbits(64),
                is_remote=False,
                trace_flags=TraceFlags(0x00)
            )
        )
    )

    with tracer.start_as_current_span("unsampled-parent", context=unsampled_context) as parent:
        print(f"\nParent sampled: {parent.get_span_context().trace_flags.sampled}")

        with tracer.start_as_current_span("child") as child:
            print(f"Child of unsampled parent: {child.get_span_context().trace_flags.sampled}")


# ==================== 3. 自定义采样器 ====================

def custom_sampler_example():
    """自定义采样器"""

    from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision
    from opentelemetry.trace import TraceFlags

    class CustomSampler(Sampler):
        """自定义采样器 - 基于操作名称和优先级"""

        def __init__(self, base_rate: float = 0.1):
            self.base_rate = base_rate
            self.high_priority_ops = {"payment", "login", "order"}

        def should_sample(
            self,
            parent_context,
            trace_id,
            name,
            kind,
            attributes,
            links,
            trace_state
        ) -> SamplingResult:

            # 高优先级操作100%采样
            if any(op in name.lower() for op in self.high_priority_ops):
                return SamplingResult(
                    decision=Decision.RECORD_AND_SAMPLE,
                    attributes={"sampler.priority": "high"}
                )

            # 错误操作100%采样
            if attributes and attributes.get("error"):
                return SamplingResult(
                    decision=Decision.RECORD_AND_SAMPLE,
                    attributes={"sampler.reason": "error"}
                )

            # 其他按比例采样
            if random.random() < self.base_rate:
                return SamplingResult(
                    decision=Decision.RECORD_AND_SAMPLE,
                    attributes={"sampler.rate": self.base_rate}
                )

            return SamplingResult(decision=Decision.DROP)

        def get_description(self) -> str:
            return f"CustomSampler(base_rate={self.base_rate})"

    # 使用自定义采样器
    provider = TracerProvider(sampler=CustomSampler(base_rate=0.2))
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)

    print("\nCustom Sampler")

    # 高优先级操作
    with tracer.start_as_current_span("process-payment") as span:
        print(f"Payment operation: sampled={span.get_span_context().trace_flags.sampled}")

    # 普通操作
    for i in range(10):
        with tracer.start_as_current_span(f"regular-operation-{i}") as span:
            print(f"Regular operation {i}: sampled={span.get_span_context().trace_flags.sampled}")


# ==================== 4. 动态采样配置 ====================

def dynamic_sampling():
    """动态采样配置"""

    from opentelemetry.sdk.trace.sampling import Sampler

    class DynamicSampler(Sampler):
        """动态采样器 - 可在运行时调整采样率"""

        def __init__(self, initial_rate: float = 0.1):
            self._rate = initial_rate
            self._lock = __import__('threading').Lock()

        @property
        def rate(self) -> float:
            return self._rate

        @rate.setter
        def rate(self, value: float):
            with self._lock:
                self._rate = max(0.0, min(1.0, value))

        def should_sample(self, parent_context, trace_id, name,
                         kind, attributes, links, trace_state):
            from opentelemetry.sdk.trace.sampling import SamplingResult, Decision

            with self._lock:
                rate = self._rate

            if random.random() < rate:
                return SamplingResult(
                    decision=Decision.RECORD_AND_SAMPLE,
                    attributes={"sampler.rate": rate}
                )
            return SamplingResult(decision=Decision.DROP)

        def get_description(self) -> str:
            return f"DynamicSampler(rate={self.rate})"

    # 使用动态采样器
    sampler = DynamicSampler(initial_rate=0.5)
    provider = TracerProvider(sampler=sampler)
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer(__name__)

    print("\nDynamic Sampler")

    # 初始采样率50%
    print(f"Initial rate: {sampler.rate}")
    sampled = sum(
        1 for _ in range(100)
        if tracer.start_span("test").get_span_context().trace_flags.sampled
    )
    print(f"Sampled at 50%: {sampled}/100")

    # 调整采样率到10%
    sampler.rate = 0.1
    print(f"\nAdjusted rate: {sampler.rate}")
    sampled = sum(
        1 for _ in range(100)
        if tracer.start_span("test").get_span_context().trace_flags.sampled
    )
    print(f"Sampled at 10%: {sampled}/100")


# ==================== 运行示例 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("头部采样策略示例")
    print("=" * 50)

    always_on_sampler()
    always_off_sampler()
    ratio_sampler()
    parent_based_sampler()
    custom_sampler_example()
    dynamic_sampling()
```

---

## 附录：参考资源

### 文档链接

| 资源 | 链接 |
|------|------|
| OpenTelemetry官方文档 | <https://opentelemetry.io/docs/> |
| OpenTelemetry Python | <https://opentelemetry-python.readthedocs.io/> |
| Prometheus文档 | <https://prometheus.io/docs/> |
| Jaeger文档 | <https://www.jaegertracing.io/docs/> |
| Grafana文档 | <https://grafana.com/docs/> |
| eBPF文档 | <https://ebpf.io/what-is-ebpf> |
| BCC工具 | <https://github.com/iovisor/bcc> |
| bpftrace | <https://github.com/iovisor/bpftrace> |

### 推荐书籍

1. 《Systems Performance》 - Brendan Gregg
2. 《BPF Performance Tools》 - Brendan Gregg
3. 《Distributed Systems Observability》 - Cindy Sridharan

### 相关标准

- W3C Trace Context: <https://www.w3.org/TR/trace-context/>
- OpenTelemetry Protocol: <https://opentelemetry.io/docs/specs/otlp/>

---

*文档版本: 1.0*
*最后更新: 2024年*
