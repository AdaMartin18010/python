# Python 错误处理最佳实践

**Exception Handling完全指南**

---

## 📋 目录

- [异常基础](#异常基础)
- [异常处理模式](#异常处理模式)
- [自定义异常](#自定义异常)
- [最佳实践](#最佳实践)
- [常见陷阱](#常见陷阱)

---

## 异常基础

### Python异常层次

```python
"""
Python异常层次结构
"""

# BaseException (所有异常的基类)
#   ├── SystemExit
#   ├── KeyboardInterrupt
#   ├── GeneratorExit
#   └── Exception (用户异常的基类)
#       ├── StopIteration
#       ├── ArithmeticError
#       │   ├── ZeroDivisionError
#       │   └── OverflowError
#       ├── LookupError
#       │   ├── KeyError
#       │   └── IndexError
#       ├── ValueError
#       ├── TypeError
#       ├── AttributeError
#       ├── ImportError
#       ├── RuntimeError
#       └── OSError
#           ├── FileNotFoundError
#           ├── PermissionError
#           └── TimeoutError

# 自定义异常应继承Exception,不是BaseException
```

### 基本语法

```python
"""
try-except基本语法
"""

# ✅ 捕获特定异常
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

# ✅ 捕获多个异常
try:
    value = int(input())
    result = 10 / value
except ValueError:
    print("Invalid input")
except ZeroDivisionError:
    print("Cannot divide by zero")

# ✅ 捕获多个异常 (同一处理)
try:
    # 代码
    pass
except (ValueError, TypeError) as e:
    print(f"Error: {e}")

# ✅ else子句 (无异常时执行)
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error")
else:
    print(f"Result: {result}")

# ✅ finally子句 (总是执行)
try:
    file = open("data.txt")
    # 处理文件
except FileNotFoundError:
    print("File not found")
finally:
    # 总是执行
    if 'file' in locals():
        file.close()

# ✅ 完整结构
try:
    # 尝试执行的代码
    pass
except SpecificError as e:
    # 处理特定错误
    pass
except AnotherError:
    # 处理另一个错误
    pass
else:
    # 无异常时执行
    pass
finally:
    # 总是执行(清理资源)
    pass
```

---

## 异常处理模式

### EAFP vs LBYL

```python
"""
EAFP vs LBYL
"""

# LBYL (Look Before You Leap) - 跳之前先看
# ❌ 不推荐 (Pythonic)
if key in dictionary:
    value = dictionary[key]
else:
    value = default

if os.path.exists(filename):
    with open(filename) as f:
        data = f.read()

# EAFP (Easier to Ask for Forgiveness than Permission) - 请求宽恕比获得许可容易
# ✅ 推荐 (Pythonic)
try:
    value = dictionary[key]
except KeyError:
    value = default

try:
    with open(filename) as f:
        data = f.read()
except FileNotFoundError:
    data = default_data

# EAFP优势:
# 1. 避免竞态条件
# 2. 代码更简洁
# 3. 更Pythonic
# 4. 性能更好(正常情况)

# LBYL适用场景:
# 1. 预防代价高昂的操作
# 2. 外部资源验证
```

### 上下文管理器

```python
"""
使用上下文管理器自动清理资源
"""

# ✅ 文件操作
with open("data.txt") as f:
    data = f.read()
# 文件自动关闭

# ✅ 数据库连接
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
# 连接自动关闭

# ✅ 锁
from threading import Lock

lock = Lock()
with lock:
    # 临界区代码
    pass
# 锁自动释放

# ✅ 自定义上下文管理器
from contextlib import contextmanager

@contextmanager
def managed_resource():
    # 设置资源
    resource = acquire_resource()
    try:
        yield resource
    finally:
        # 清理资源
        release_resource(resource)

with managed_resource() as res:
    # 使用资源
    pass
```

### 异常链

```python
"""
异常链 (Exception Chaining)
"""

# ✅ 保留原始异常
try:
    result = int("abc")
except ValueError as e:
    raise RuntimeError("Failed to parse value") from e
# RuntimeError: Failed to parse value
# The above exception was the direct cause of...

# ✅ 隐藏原始异常
try:
    result = int("abc")
except ValueError:
    raise RuntimeError("Failed to parse value") from None
# RuntimeError: Failed to parse value (无原始异常信息)

# ✅ 自动异常链
try:
    result = int("abc")
except ValueError:
    raise RuntimeError("Failed to parse value")
# 自动链接到ValueError

# ✅ 访问异常链
try:
    # 代码
    pass
except Exception as e:
    print(f"Current: {e}")
    print(f"Cause: {e.__cause__}")
    print(f"Context: {e.__context__}")
```

### 异常分组 (Python 3.11+)

```python
"""
异常组 (Exception Groups) - Python 3.11+
"""

# ✅ 创建异常组
eg = ExceptionGroup(
    "multiple errors",
    [ValueError("bad value"), TypeError("bad type")]
)

# ✅ 抛出异常组
def process_items(items):
    errors = []
    for item in items:
        try:
            process_item(item)
        except Exception as e:
            errors.append(e)
    if errors:
        raise ExceptionGroup("Processing errors", errors)

# ✅ 捕获异常组
try:
    process_items(data)
except* ValueError as eg:
    # 处理所有ValueError
    for e in eg.exceptions:
        print(f"ValueError: {e}")
except* TypeError as eg:
    # 处理所有TypeError
    for e in eg.exceptions:
        print(f"TypeError: {e}")
```

---

## 自定义异常

### 定义自定义异常

```python
"""
自定义异常类
"""

# ✅ 基础自定义异常
class MyError(Exception):
    """Base exception for my module"""
    pass

class ValidationError(MyError):
    """Raised when validation fails"""
    pass

class AuthenticationError(MyError):
    """Raised when authentication fails"""
    pass

# ✅ 带额外信息的异常
class ValidationError(Exception):
    """Validation error with details"""
    
    def __init__(self, message: str, field: str, value: any):
        super().__init__(message)
        self.field = field
        self.value = value

try:
    raise ValidationError("Invalid email", "email", "invalid@")
except ValidationError as e:
    print(f"Field: {e.field}, Value: {e.value}")

# ✅ 异常层次结构
class AppError(Exception):
    """Base application error"""
    pass

class DatabaseError(AppError):
    """Database related errors"""
    pass

class NetworkError(AppError):
    """Network related errors"""
    pass

class TimeoutError(NetworkError):
    """Network timeout error"""
    pass

# 使用
try:
    # 代码
    pass
except DatabaseError:
    # 处理数据库错误
    pass
except NetworkError:
    # 处理网络错误(包括TimeoutError)
    pass
except AppError:
    # 处理其他应用错误
    pass
```

### 异常最佳设计

```python
"""
异常设计最佳实践
"""

# ✅ 提供有用的错误信息
class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found")

# ✅ 支持错误代码
class APIError(Exception):
    def __init__(self, message: str, code: int, details: dict = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}

try:
    raise APIError("Rate limit exceeded", 429, {"retry_after": 60})
except APIError as e:
    if e.code == 429:
        time.sleep(e.details["retry_after"])

# ✅ 可序列化异常 (用于日志/API)
from dataclasses import dataclass
from typing import Optional

@dataclass
class ValidationError(Exception):
    message: str
    field: str
    value: any
    suggestion: Optional[str] = None
    
    def to_dict(self):
        return {
            "error": "ValidationError",
            "message": self.message,
            "field": self.field,
            "value": str(self.value),
            "suggestion": self.suggestion,
        }
```

---

## 最佳实践

### 异常处理原则

```python
"""
异常处理最佳实践
"""

# ✅ 捕获具体异常,不要裸except
try:
    value = int(input())
except ValueError:
    print("Invalid number")

# ❌ 不要裸except
try:
    value = int(input())
except:  # 捕获所有,包括KeyboardInterrupt
    print("Error")

# ✅ 如果必须捕获所有,使用Exception
try:
    # 代码
    pass
except Exception as e:
    log_error(e)
    raise  # 重新抛出

# ✅ 不要吞没异常
try:
    risky_operation()
except Exception:
    pass  # ❌ 静默失败

# ✅ 记录或处理
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    # 或采取补救措施

# ✅ 早返回,避免深嵌套
def process(data):
    if not data:
        raise ValueError("Data is empty")
    
    if not validate(data):
        raise ValidationError("Invalid data")
    
    return transform(data)

# ❌ 避免深嵌套
def process(data):
    if data:
        if validate(data):
            return transform(data)
        else:
            raise ValidationError()
    else:
        raise ValueError()
```

### 日志记录

```python
"""
异常日志记录
"""

import logging

logger = logging.getLogger(__name__)

# ✅ 记录异常
try:
    result = risky_operation()
except Exception as e:
    logger.exception("Operation failed")  # 自动记录堆栈
    raise

# ✅ 记录异常详情
try:
    result = api_call(user_id=123)
except APIError as e:
    logger.error(
        "API call failed",
        extra={
            "user_id": 123,
            "error_code": e.code,
            "details": e.details,
        },
        exc_info=True  # 包含堆栈信息
    )

# ✅ 结构化日志
import structlog

log = structlog.get_logger()

try:
    result = process_payment(amount=100)
except PaymentError as e:
    log.error(
        "payment_failed",
        amount=100,
        error_code=e.code,
        user_id=current_user.id,
    )
```

### API错误处理

```python
"""
API错误处理模式
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

app = FastAPI()

# ✅ 标准化错误响应
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: dict | None = None

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="ValidationError",
            message="Invalid input",
            details=exc.errors(),
        ).dict()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
        ).dict()
    )

# ✅ 业务逻辑异常
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={"error": "UserNotFound", "user_id": user_id}
        )
    return user
```

---

## 常见陷阱

### 避免的模式

```python
"""
常见错误模式
"""

# ❌ 过于宽泛的except
try:
    code()
except Exception:  # 捕获太多
    pass

# ❌ 吞没异常
try:
    code()
except Exception:
    pass  # 静默失败

# ❌ 使用异常做控制流
# 不要用异常做正常的控制流
try:
    while True:
        item = iterator.next()
except StopIteration:
    pass

# ✅ 使用正常控制流
for item in iterator:
    pass

# ❌ 修改并重新抛出
try:
    code()
except ValueError as e:
    e.args = ("Custom message",)  # 不要修改
    raise

# ✅ 使用异常链
try:
    code()
except ValueError as e:
    raise CustomError("Custom message") from e

# ❌ 返回None表示错误
def get_user(user_id):
    try:
        return db.get(user_id)
    except NotFoundError:
        return None  # 不清楚是错误还是真的None

# ✅ 抛出异常或返回Optional
def get_user(user_id: int) -> User | None:
    try:
        return db.get(user_id)
    except NotFoundError:
        return None  # 文档说明返回None表示不存在

# 或
def get_user(user_id: int) -> User:
    user = db.get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user
```

---

## 📚 核心要点

### 异常基础

- ✅ **继承Exception**: 自定义异常
- ✅ **特定异常**: 捕获具体类型
- ✅ **finally**: 清理资源
- ✅ **else**: 无异常时执行

### 处理模式

- ✅ **EAFP**: Python风格
- ✅ **上下文管理器**: with语句
- ✅ **异常链**: from e
- ✅ **异常组**: Python 3.11+

### 自定义异常

- ✅ **继承Exception**: 不是BaseException
- ✅ **异常层次**: 组织相关异常
- ✅ **有用信息**: 错误详情
- ✅ **可序列化**: to_dict()

### 最佳实践

- ✅ **具体异常**: 不要裸except
- ✅ **不吞没**: 记录或处理
- ✅ **早返回**: 避免深嵌套
- ✅ **日志**: 记录异常详情

### 避免

- ❌ 裸except
- ❌ 过于宽泛
- ❌ 静默失败
- ❌ 异常做控制流
- ❌ 修改异常

---

**正确的错误处理让程序更健壮！** 🛡️✨

**相关文档**:
- [01-pep8.md](01-pep8.md) - PEP 8代码风格
- [06-code-review.md](06-code-review.md) - 代码审查

**最后更新**: 2025年10月28日

