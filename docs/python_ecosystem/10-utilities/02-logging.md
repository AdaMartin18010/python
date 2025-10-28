# 日志处理

**Python日志系统最佳实践**

---

## 📋 概述

良好的日志系统对于应用监控和问题排查至关重要。

---

## 🚀 标准库logging

### 基本使用

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### 完整配置

```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

---

## ✨ loguru - 现代日志库

### 安装

```bash
uv add loguru
```

### 简单优雅

```python
from loguru import logger

# 自动配置，开箱即用
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# 异常记录
try:
    1 / 0
except Exception:
    logger.exception("Error occurred")

# 添加文件输出
logger.add("app.log", rotation="500 MB", retention="10 days")
```

### 结构化日志

```python
logger.add("logs/app_{time}.log", serialize=True)  # JSON格式

logger.bind(user_id=123, request_id="abc").info("User action")
# 输出: {"text": "User action", "record": {"extra": {"user_id": 123, "request_id": "abc"}}}
```

---

## 📚 最佳实践

### FastAPI集成

```python
from fastapi import FastAPI, Request
from loguru import logger
import time

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"Response: {response.status_code} - {process_time:.3f}s",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "duration": process_time
        }
    )
    
    return response
```

---

## 🔗 相关资源

- [logging文档](https://docs.python.org/3/library/logging.html)
- [loguru文档](https://loguru.readthedocs.io/)

---

**最后更新**: 2025年10月28日

