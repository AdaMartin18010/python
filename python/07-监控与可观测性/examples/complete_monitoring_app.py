"""
完整的监控示例应用
包含 Prometheus指标、OpenTelemetry追踪、Structlog日志

运行方式:
    uv add fastapi[standard] prometheus-client opentelemetry-api opentelemetry-sdk structlog
    uvicorn complete_monitoring_app:app --reload
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import structlog
import logging
import sys
import time
from functools import wraps
from typing import Callable, Any
import random

# ============ 配置日志 ============

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO
)

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# ============ 配置追踪 ============

resource = Resource(attributes={
    SERVICE_NAME: "monitoring-demo",
    SERVICE_VERSION: "1.0.0",
})

provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# ============ 配置指标 ============

# HTTP请求计数
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# HTTP请求延迟
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

# 活跃请求数
http_requests_in_progress = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests in progress",
    ["method", "endpoint"]
)

# 业务指标：处理的订单数
orders_processed_total = Counter(
    "orders_processed_total",
    "Total orders processed",
    ["status"]
)

# 业务指标：订单金额
order_amount_total = Counter(
    "order_amount_total",
    "Total order amount in USD"
)

# ============ 装饰器 ============

def monitor_endpoint(func: Callable) -> Callable:
    """综合监控装饰器：指标+追踪+日志"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # 提取请求信息
        request = kwargs.get("request")
        method = request.method if request else "UNKNOWN"
        endpoint = request.url.path if request else "UNKNOWN"
        
        # 开始追踪
        with tracer.start_as_current_span(f"{method} {endpoint}") as span:
            span.set_attribute("http.method", method)
            span.set_attribute("http.url", endpoint)
            
            # 增加进行中请求计数
            http_requests_in_progress.labels(method=method, endpoint=endpoint).inc()
            
            start_time = time.time()
            status = 500
            
            # 记录开始日志
            logger.info(
                "request_started",
                method=method,
                endpoint=endpoint,
                trace_id=span.get_span_context().trace_id,
                span_id=span.get_span_context().span_id
            )
            
            try:
                response = await func(*args, **kwargs)
                status = response.status_code if hasattr(response, "status_code") else 200
                span.set_attribute("http.status_code", status)
                return response
            except HTTPException as e:
                status = e.status_code
                span.set_attribute("http.status_code", status)
                span.record_exception(e)
                logger.error(
                    "request_error",
                    method=method,
                    endpoint=endpoint,
                    status=status,
                    error=str(e)
                )
                raise
            except Exception as e:
                status = 500
                span.set_attribute("http.status_code", status)
                span.record_exception(e)
                logger.error(
                    "request_failed",
                    method=method,
                    endpoint=endpoint,
                    error=str(e),
                    exc_info=True
                )
                raise
            finally:
                # 记录指标
                duration = time.time() - start_time
                http_requests_total.labels(
                    method=method,
                    endpoint=endpoint,
                    status=str(status)
                ).inc()
                http_request_duration_seconds.labels(
                    method=method,
                    endpoint=endpoint
                ).observe(duration)
                http_requests_in_progress.labels(method=method, endpoint=endpoint).dec()
                
                # 记录完成日志
                logger.info(
                    "request_completed",
                    method=method,
                    endpoint=endpoint,
                    status=status,
                    duration_ms=round(duration * 1000, 2)
                )
    
    return wrapper


# ============ 创建应用 ============

app = FastAPI(
    title="Monitoring Demo",
    description="Complete monitoring example with metrics, tracing, and logging",
    version="1.0.0"
)

# 自动追踪FastAPI
FastAPIInstrumentor.instrument_app(app)

# ============ 端点 ============

@app.get("/")
@monitor_endpoint
async def root(request: Request):
    """根路径"""
    return {"message": "Hello, Monitoring World!"}


@app.get("/health")
async def health_check():
    """健康检查（不监控）"""
    return {"status": "healthy"}


@app.get("/metrics", include_in_schema=False)
async def metrics():
    """Prometheus指标端点"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.post("/orders")
@monitor_endpoint
async def create_order(request: Request, amount: float, user_id: str):
    """创建订单（模拟业务逻辑）"""
    
    # 模拟处理时间
    processing_time = random.uniform(0.1, 0.5)
    
    with tracer.start_as_current_span("validate_order") as span:
        span.set_attribute("order.amount", amount)
        span.set_attribute("user.id", user_id)
        time.sleep(processing_time * 0.3)
        
        if amount < 0:
            logger.warning("invalid_order_amount", amount=amount, user_id=user_id)
            raise HTTPException(status_code=400, detail="Invalid amount")
    
    with tracer.start_as_current_span("process_payment") as span:
        span.set_attribute("payment.amount", amount)
        time.sleep(processing_time * 0.5)
        
        # 模拟5%失败率
        if random.random() < 0.05:
            orders_processed_total.labels(status="failed").inc()
            logger.error("payment_failed", amount=amount, user_id=user_id)
            raise HTTPException(status_code=500, detail="Payment failed")
    
    with tracer.start_as_current_span("save_order") as span:
        time.sleep(processing_time * 0.2)
        
        # 记录成功
        orders_processed_total.labels(status="success").inc()
        order_amount_total.inc(amount)
        
        logger.info(
            "order_created",
            order_id=f"order_{random.randint(1000, 9999)}",
            amount=amount,
            user_id=user_id
        )
    
    return {
        "status": "success",
        "amount": amount,
        "processing_time_ms": round(processing_time * 1000, 2)
    }


@app.get("/users/{user_id}")
@monitor_endpoint
async def get_user(request: Request, user_id: str):
    """获取用户信息"""
    
    with tracer.start_as_current_span("fetch_user") as span:
        span.set_attribute("user.id", user_id)
        time.sleep(random.uniform(0.05, 0.15))
        
        # 模拟10%用户不存在
        if random.random() < 0.1:
            logger.warning("user_not_found", user_id=user_id)
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = {
            "user_id": user_id,
            "name": f"User {user_id}",
            "email": f"{user_id}@example.com"
        }
        
        logger.info("user_fetched", user_id=user_id)
        return user_data


@app.get("/slow")
@monitor_endpoint
async def slow_endpoint(request: Request):
    """慢端点（用于测试告警）"""
    time.sleep(2)  # 模拟慢查询
    return {"message": "This was slow"}


@app.get("/error")
@monitor_endpoint
async def error_endpoint(request: Request):
    """错误端点（用于测试告警）"""
    logger.error("intentional_error", reason="testing")
    raise HTTPException(status_code=500, detail="Intentional error for testing")


# ============ 启动事件 ============

@app.on_event("startup")
async def startup_event():
    """应用启动"""
    logger.info(
        "application_started",
        service="monitoring-demo",
        version="1.0.0"
    )


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭"""
    logger.info("application_shutdown")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

