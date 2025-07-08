# Python最佳实践2025

## 1. 代码质量与规范

### 1.1 类型安全编程

```python
# 类型注解最佳实践
from typing import Optional, List, Dict, Union, TypeVar, Generic
from dataclasses import dataclass
from pydantic import BaseModel, Field

# 基础类型注解
def calculate_total(items: List[float], discount: Optional[float] = None) -> float:
    """计算商品总价"""
    total = sum(items)
    if discount:
        total *= (1 - discount)
    return total

# 泛型类型
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()

# 数据类
@dataclass
class User:
    name: str
    email: str
    age: int
    is_active: bool = True

# Pydantic模型
class Product(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = Field(..., regex=r'^[A-Za-z\s]+$')
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Python编程指南",
                "price": 99.99,
                "category": "技术书籍",
                "tags": ["Python", "编程", "技术"]
            }
        }

# 类型安全的最佳实践
class TypeSafePractices:
    """类型安全编程最佳实践"""
    
    @staticmethod
    def use_union_types(value: Union[str, int, float]) -> str:
        """使用联合类型处理多种输入"""
        return str(value)
    
    @staticmethod
    def use_optional_for_none_values(value: Optional[str] = None) -> str:
        """使用Optional表示可能为None的值"""
        return value or "default"
    
    @staticmethod
    def use_generics_for_reusable_code(items: List[T]) -> List[T]:
        """使用泛型编写可重用代码"""
        return items.copy()
    
    @staticmethod
    def validate_with_pydantic(data: Dict[str, any]) -> Product:
        """使用Pydantic进行数据验证"""
        return Product(**data)
```

### 1.2 异步编程最佳实践

```python
import asyncio
import aiohttp
from typing import List, Dict, Any
from contextlib import asynccontextmanager

# 异步上下文管理器
@asynccontextmanager
async def get_session():
    """异步会话管理器"""
    async with aiohttp.ClientSession() as session:
        yield session

# 异步函数最佳实践
class AsyncBestPractices:
    """异步编程最佳实践"""
    
    @staticmethod
    async def fetch_data_with_retry(url: str, max_retries: int = 3) -> Dict[str, Any]:
        """带重试机制的数据获取"""
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            raise aiohttp.ClientError(f"HTTP {response.status}")
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                await asyncio.sleep(2 ** attempt)  # 指数退避
        raise Exception("Max retries exceeded")
    
    @staticmethod
    async def process_items_concurrently(items: List[str]) -> List[str]:
        """并发处理多个项目"""
        async def process_item(item: str) -> str:
            await asyncio.sleep(0.1)  # 模拟处理时间
            return f"processed_{item}"
        
        # 使用asyncio.gather并发执行
        tasks = [process_item(item) for item in items]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 过滤异常结果
        return [result for result in results if not isinstance(result, Exception)]
    
    @staticmethod
    async def batch_processing(items: List[str], batch_size: int = 10) -> List[str]:
        """批量处理大量数据"""
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[asyncio.sleep(0.1) for _ in batch]  # 模拟处理
            )
            results.extend(batch_results)
        return results

# 异步资源管理
class AsyncResourceManager:
    """异步资源管理最佳实践"""
    
    def __init__(self):
        self._resources = []
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self._acquire_resources()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self._release_resources()
    
    async def _acquire_resources(self):
        """获取资源"""
        # 模拟资源获取
        await asyncio.sleep(0.1)
    
    async def _release_resources(self):
        """释放资源"""
        # 模拟资源释放
        await asyncio.sleep(0.1)
```

### 1.3 错误处理与日志记录

```python
import logging
import traceback
from typing import Optional, Callable, Any
from functools import wraps
from contextlib import contextmanager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 错误处理装饰器
def error_handler(func: Callable) -> Callable:
    """通用错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    return wrapper

# 自定义异常类
class ValidationError(Exception):
    """数据验证错误"""
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class BusinessLogicError(Exception):
    """业务逻辑错误"""
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

# 错误处理最佳实践
class ErrorHandlingBestPractices:
    """错误处理最佳实践"""
    
    @staticmethod
    @error_handler
    def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """处理数据并处理可能的错误"""
        if not data:
            raise ValidationError("数据不能为空")
        
        try:
            # 模拟数据处理
            result = {k: v * 2 for k, v in data.items() if isinstance(v, (int, float))}
            logger.info(f"成功处理数据: {len(result)} 项")
            return result
        except Exception as e:
            logger.error(f"数据处理失败: {str(e)}")
            raise BusinessLogicError("数据处理失败", "DATA_PROCESSING_ERROR")
    
    @staticmethod
    @contextmanager
    def safe_operation():
        """安全操作上下文管理器"""
        try:
            yield
        except Exception as e:
            logger.error(f"操作失败: {str(e)}")
            raise
    
    @staticmethod
    def retry_operation(operation: Callable, max_retries: int = 3) -> Any:
        """重试操作"""
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"操作最终失败: {str(e)}")
                    raise
                logger.warning(f"操作失败，重试 {attempt + 1}/{max_retries}: {str(e)}")
                import time
                time.sleep(2 ** attempt)  # 指数退避
```

## 2. 性能优化

### 2.1 内存管理

```python
import sys
import gc
import weakref
from typing import Dict, List, Any
from memory_profiler import profile

# 内存优化最佳实践
class MemoryOptimization:
    """内存优化最佳实践"""
    
    @staticmethod
    def use_generators_for_large_data():
        """使用生成器处理大数据"""
        def large_data_generator():
            for i in range(1000000):
                yield i * 2
        
        # 而不是
        # large_list = [i * 2 for i in range(1000000)]
        
        total = sum(large_data_generator())
        return total
    
    @staticmethod
    def use_slots_for_memory_efficient_classes():
        """使用__slots__减少内存使用"""
        class EfficientUser:
            __slots__ = ['name', 'email', 'age']
            
            def __init__(self, name: str, email: str, age: int):
                self.name = name
                self.email = email
                self.age = age
        
        return EfficientUser("John", "john@example.com", 30)
    
    @staticmethod
    def use_weak_references():
        """使用弱引用避免循环引用"""
        class Cache:
            def __init__(self):
                self._cache = weakref.WeakValueDictionary()
            
            def get(self, key: str) -> Any:
                return self._cache.get(key)
            
            def set(self, key: str, value: Any) -> None:
                self._cache[key] = value
        
        return Cache()
    
    @staticmethod
    @profile
    def memory_profiling_example():
        """内存分析示例"""
        data = []
        for i in range(10000):
            data.append(f"item_{i}")
        return len(data)

# 内存泄漏检测
class MemoryLeakDetector:
    """内存泄漏检测工具"""
    
    @staticmethod
    def detect_circular_references():
        """检测循环引用"""
        gc.collect()  # 强制垃圾回收
        before_count = len(gc.get_objects())
        
        # 执行可能产生循环引用的操作
        # ...
        
        gc.collect()
        after_count = len(gc.get_objects())
        
        if after_count > before_count * 1.1:  # 对象数量增长超过10%
            logger.warning("可能存在内存泄漏")
    
    @staticmethod
    def monitor_memory_usage():
        """监控内存使用"""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        logger.info(f"内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")
```

### 2.2 算法优化

```python
import time
from typing import List, Tuple, Optional
from functools import lru_cache
import numpy as np

# 算法优化最佳实践
class AlgorithmOptimization:
    """算法优化最佳实践"""
    
    @staticmethod
    @lru_cache(maxsize=128)
    def fibonacci_cached(n: int) -> int:
        """使用缓存优化斐波那契计算"""
        if n < 2:
            return n
        return AlgorithmOptimization.fibonacci_cached(n-1) + AlgorithmOptimization.fibonacci_cached(n-2)
    
    @staticmethod
    def use_numpy_for_numerical_operations():
        """使用NumPy进行数值计算"""
        # 传统Python列表
        python_list = [i for i in range(1000000)]
        python_sum = sum(python_list)
        
        # NumPy数组
        numpy_array = np.arange(1000000)
        numpy_sum = np.sum(numpy_array)
        
        return python_sum, numpy_sum
    
    @staticmethod
    def optimize_list_operations():
        """优化列表操作"""
        # 使用列表推导式而不是循环
        squares = [x**2 for x in range(1000)]
        
        # 使用生成器表达式处理大数据
        large_sum = sum(x**2 for x in range(1000000))
        
        # 使用内置函数
        numbers = [1, 2, 3, 4, 5]
        total = sum(numbers)
        maximum = max(numbers)
        minimum = min(numbers)
        
        return squares, large_sum, total, maximum, minimum
    
    @staticmethod
    def use_bisect_for_binary_search():
        """使用bisect进行二分查找"""
        import bisect
        
        sorted_list = [1, 3, 5, 7, 9, 11, 13, 15]
        
        # 查找插入位置
        position = bisect.bisect_left(sorted_list, 6)
        
        # 检查元素是否存在
        exists = bisect.bisect_left(sorted_list, 7) != len(sorted_list) and sorted_list[bisect.bisect_left(sorted_list, 7)] == 7
        
        return position, exists

# 性能基准测试
class PerformanceBenchmark:
    """性能基准测试工具"""
    
    @staticmethod
    def benchmark_function(func: callable, *args, iterations: int = 1000) -> float:
        """基准测试函数性能"""
        start_time = time.time()
        for _ in range(iterations):
            func(*args)
        end_time = time.time()
        return (end_time - start_time) / iterations
    
    @staticmethod
    def compare_algorithms():
        """比较不同算法性能"""
        def slow_algorithm(n: int) -> int:
            return sum(i for i in range(n))
        
        def fast_algorithm(n: int) -> int:
            return n * (n - 1) // 2
        
        n = 10000
        slow_time = PerformanceBenchmark.benchmark_function(slow_algorithm, n)
        fast_time = PerformanceBenchmark.benchmark_function(fast_algorithm, n)
        
        logger.info(f"慢算法时间: {slow_time:.6f}秒")
        logger.info(f"快算法时间: {fast_time:.6f}秒")
        logger.info(f"性能提升: {slow_time/fast_time:.2f}倍")
```

## 3. 安全最佳实践

### 3.1 输入验证与清理

```python
import re
import hashlib
import secrets
from typing import Optional, Union
from pydantic import BaseModel, validator

# 输入验证最佳实践
class InputValidation:
    """输入验证最佳实践"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """验证密码强度"""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True
    
    @staticmethod
    def sanitize_html(html_content: str) -> str:
        """清理HTML内容"""
        import html
        return html.escape(html_content)
    
    @staticmethod
    def validate_sql_injection_safe(query: str) -> bool:
        """验证SQL注入安全"""
        dangerous_patterns = [
            r'(\b(union|select|insert|update|delete|drop|create|alter)\b)',
            r'(\b(or|and)\b\s+\d+\s*=\s*\d+)',
            r'(\b(union|select|insert|update|delete|drop|create|alter)\b.*\b(union|select|insert|update|delete|drop|create|alter)\b)'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return False
        return True

# 安全数据模型
class SecureUser(BaseModel):
    """安全用户模型"""
    username: str
    email: str
    password_hash: str
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', v):
            raise ValueError('用户名格式无效')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if not InputValidation.validate_email(v):
            raise ValueError('邮箱格式无效')
        return v

# 密码安全
class PasswordSecurity:
    """密码安全最佳实践"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """安全哈希密码"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${hash_obj.hex()}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """验证密码"""
        try:
            salt, hash_hex = hashed.split('$')
            hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return hash_obj.hex() == hash_hex
        except:
            return False
    
    @staticmethod
    def generate_secure_token() -> str:
        """生成安全令牌"""
        return secrets.token_urlsafe(32)
```

### 3.2 加密与安全通信

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# 加密最佳实践
class EncryptionBestPractices:
    """加密最佳实践"""
    
    @staticmethod
    def generate_key() -> bytes:
        """生成加密密钥"""
        return Fernet.generate_key()
    
    @staticmethod
    def encrypt_data(data: str, key: bytes) -> str:
        """加密数据"""
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    @staticmethod
    def decrypt_data(encrypted_data: str, key: bytes) -> str:
        """解密数据"""
        f = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = f.decrypt(encrypted_bytes)
        return decrypted_data.decode()
    
    @staticmethod
    def secure_key_derivation(password: str, salt: bytes) -> bytes:
        """安全密钥派生"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# 安全配置
class SecurityConfig:
    """安全配置最佳实践"""
    
    @staticmethod
    def get_secure_headers() -> dict:
        """获取安全HTTP头"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'",
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
    
    @staticmethod
    def validate_cors_origin(origin: str, allowed_origins: list) -> bool:
        """验证CORS来源"""
        return origin in allowed_origins
    
    @staticmethod
    def rate_limit_key(client_ip: str, endpoint: str) -> str:
        """生成速率限制键"""
        return f"rate_limit:{client_ip}:{endpoint}"
```

## 4. 测试最佳实践

### 4.1 单元测试

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

# 单元测试最佳实践
class UnitTestBestPractices:
    """单元测试最佳实践"""
    
    @staticmethod
    def test_function_with_mock():
        """使用Mock进行测试"""
        # 创建Mock对象
        mock_database = Mock()
        mock_database.query.return_value = [{"id": 1, "name": "test"}]
        
        # 测试函数
        def get_user_by_id(user_id: int, db) -> Dict[str, Any]:
            result = db.query(f"SELECT * FROM users WHERE id = {user_id}")
            return result[0] if result else None
        
        # 执行测试
        result = get_user_by_id(1, mock_database)
        
        # 断言
        assert result["id"] == 1
        assert result["name"] == "test"
        mock_database.query.assert_called_once_with("SELECT * FROM users WHERE id = 1")
    
    @staticmethod
    def test_async_function():
        """测试异步函数"""
        import asyncio
        
        async def async_function(x: int) -> int:
            await asyncio.sleep(0.1)
            return x * 2
        
        # 使用pytest-asyncio测试异步函数
        async def test_async():
            result = await async_function(5)
            assert result == 10
        
        return asyncio.run(test_async())
    
    @staticmethod
    def test_with_fixtures():
        """使用pytest fixtures"""
        @pytest.fixture
        def sample_data():
            return {"name": "test", "value": 42}
        
        def test_function(data):
            assert data["name"] == "test"
            assert data["value"] == 42
        
        # 在实际测试中，pytest会自动注入fixture
        return sample_data, test_function

# 测试数据生成
class TestDataGeneration:
    """测试数据生成最佳实践"""
    
    @staticmethod
    def generate_test_users(count: int) -> List[Dict[str, Any]]:
        """生成测试用户数据"""
        users = []
        for i in range(count):
            users.append({
                "id": i + 1,
                "name": f"user_{i}",
                "email": f"user_{i}@example.com",
                "age": 20 + (i % 50)
            })
        return users
    
    @staticmethod
    def generate_test_products(count: int) -> List[Dict[str, Any]]:
        """生成测试产品数据"""
        products = []
        for i in range(count):
            products.append({
                "id": i + 1,
                "name": f"product_{i}",
                "price": 10.0 + (i * 5.5),
                "category": f"category_{i % 5}"
            })
        return products

# 参数化测试
class ParameterizedTests:
    """参数化测试最佳实践"""
    
    @staticmethod
    def test_calculator():
        """参数化测试示例"""
        test_cases = [
            (2, 3, 5),  # (a, b, expected)
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300)
        ]
        
        def add(a: int, b: int) -> int:
            return a + b
        
        for a, b, expected in test_cases:
            result = add(a, b)
            assert result == expected, f"Expected {expected}, got {result}"
```

### 4.2 集成测试

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 集成测试最佳实践
class IntegrationTestBestPractices:
    """集成测试最佳实践"""
    
    @staticmethod
    def test_api_endpoint():
        """测试API端点"""
        from fastapi import FastAPI
        
        app = FastAPI()
        
        @app.get("/users/{user_id}")
        def get_user(user_id: int):
            return {"user_id": user_id, "name": f"user_{user_id}"}
        
        client = TestClient(app)
        response = client.get("/users/1")
        
        assert response.status_code == 200
        assert response.json() == {"user_id": 1, "name": "user_1"}
    
    @staticmethod
    def test_database_integration():
        """测试数据库集成"""
        # 使用测试数据库
        test_engine = create_engine("sqlite:///test.db")
        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        
        # 创建测试表
        from sqlalchemy import Column, Integer, String
        from sqlalchemy.ext.declarative import declarative_base
        
        Base = declarative_base()
        
        class User(Base):
            __tablename__ = "users"
            id = Column(Integer, primary_key=True, index=True)
            name = Column(String, index=True)
            email = Column(String, unique=True, index=True)
        
        Base.metadata.create_all(bind=test_engine)
        
        # 测试数据库操作
        db = TestSessionLocal()
        try:
            user = User(name="test_user", email="test@example.com")
            db.add(user)
            db.commit()
            db.refresh(user)
            
            assert user.id is not None
            assert user.name == "test_user"
        finally:
            db.close()
    
    @staticmethod
    def test_external_api_integration():
        """测试外部API集成"""
        import requests
        from unittest.mock import patch
        
        def fetch_user_data(user_id: int) -> dict:
            response = requests.get(f"https://api.example.com/users/{user_id}")
            return response.json()
        
        # 使用Mock测试外部API
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {"id": 1, "name": "test"}
            mock_get.return_value.status_code = 200
            
            result = fetch_user_data(1)
            
            assert result["id"] == 1
            assert result["name"] == "test"
            mock_get.assert_called_once_with("https://api.example.com/users/1")
```

## 5. 部署与运维

### 5.1 容器化最佳实践

```python
# Dockerfile最佳实践示例
dockerfile_best_practices = """
# 使用官方Python镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# Docker Compose最佳实践
docker_compose_best_practices = """
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
"""
```

### 5.2 监控与日志

```python
import logging
import json
from datetime import datetime
from typing import Dict, Any
from contextlib import contextmanager

# 结构化日志
class StructuredLogger:
    """结构化日志最佳实践"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 添加JSON格式化处理器
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_event(self, event_type: str, data: Dict[str, Any], level: str = "INFO"):
        """记录结构化事件"""
        log_data = {
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if level.upper() == "INFO":
            self.logger.info(json.dumps(log_data))
        elif level.upper() == "ERROR":
            self.logger.error(json.dumps(log_data))
        elif level.upper() == "WARNING":
            self.logger.warning(json.dumps(log_data))
    
    @contextmanager
    def log_operation(self, operation_name: str):
        """操作日志上下文管理器"""
        start_time = datetime.utcnow()
        self.log_event("operation_start", {"operation": operation_name})
        
        try:
            yield
            self.log_event("operation_success", {
                "operation": operation_name,
                "duration_ms": (datetime.utcnow() - start_time).total_seconds() * 1000
            })
        except Exception as e:
            self.log_event("operation_error", {
                "operation": operation_name,
                "error": str(e),
                "duration_ms": (datetime.utcnow() - start_time).total_seconds() * 1000
            })
            raise

# 性能监控
class PerformanceMonitor:
    """性能监控最佳实践"""
    
    @staticmethod
    def monitor_function_performance(func_name: str):
        """函数性能监控装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = datetime.utcnow()
                try:
                    result = func(*args, **kwargs)
                    duration = (datetime.utcnow() - start_time).total_seconds() * 1000
                    logger.info(f"Function {func_name} completed in {duration:.2f}ms")
                    return result
                except Exception as e:
                    duration = (datetime.utcnow() - start_time).total_seconds() * 1000
                    logger.error(f"Function {func_name} failed after {duration:.2f}ms: {str(e)}")
                    raise
            return wrapper
        return decorator
    
    @staticmethod
    def monitor_memory_usage():
        """监控内存使用"""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    
    @staticmethod
    def monitor_database_queries():
        """监控数据库查询"""
        # 这里可以集成数据库查询监控工具
        # 例如：SQLAlchemy的事件监听器
        pass
```

## 6. 团队协作

### 6.1 代码规范

```python
# 代码规范配置
class CodeStyleGuide:
    """代码规范指南"""
    
    # Black配置
    black_config = """
    [tool.black]
    line-length = 88
    target-version = ['py312']
    include = '\.pyi?$'
    extend-exclude = '''
    /(
      # directories
      \.eggs
      | \.git
      | \.hg
      | \.mypy_cache
      | \.tox
      | \.venv
      | build
      | dist
    )/
    '''
    """
    
    # isort配置
    isort_config = """
    [tool.isort]
    profile = "black"
    line_length = 88
    multi_line_output = 3
    include_trailing_comma = true
    force_grid_wrap = 0
    use_parentheses = true
    ensure_newline_before_comments = true
    """
    
    # mypy配置
    mypy_config = """
    [tool.mypy]
    python_version = "3.12"
    warn_return_any = true
    warn_unused_configs = true
    disallow_untyped_defs = true
    disallow_incomplete_defs = true
    check_untyped_defs = true
    disallow_untyped_decorators = true
    no_implicit_optional = true
    warn_redundant_casts = true
    warn_unused_ignores = true
    warn_no_return = true
    warn_unreachable = true
    strict_equality = true
    """
    
    # flake8配置
    flake8_config = """
    [flake8]
    max-line-length = 88
    extend-ignore = E203, W503
    exclude = .git,__pycache__,build,dist
    """
    
    # pytest配置
    pytest_config = """
    [tool.pytest.ini_options]
    testpaths = ["tests"]
    python_files = ["test_*.py", "*_test.py"]
    python_classes = ["Test*"]
    python_functions = ["test_*"]
    addopts = "-v --tb=short --strict-markers"
    markers = [
        "slow: marks tests as slow (deselect with '-m \"not slow\"')",
        "integration: marks tests as integration tests",
        "unit: marks tests as unit tests"
    ]
    """

# 预提交钩子配置
pre_commit_config = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.12
  
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
"""

# Git提交规范
git_commit_convention = """
# Git提交信息规范

## 格式
<type>(<scope>): <subject>

## 类型
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 示例
feat(auth): 添加用户认证功能
fix(api): 修复用户列表API分页问题
docs(readme): 更新安装说明
style(black): 格式化代码
refactor(database): 重构数据库连接池
test(unit): 添加用户模型单元测试
chore(deps): 更新依赖包版本
"""
```

### 6.2 文档规范

```python
# 文档规范
class DocumentationStandards:
    """文档规范"""
    
    # 函数文档字符串模板
    function_docstring_template = '''
    """简短描述函数功能。

    Args:
        param1 (type): 参数1的描述
        param2 (type, optional): 参数2的描述，默认为None

    Returns:
        type: 返回值的描述

    Raises:
        ValueError: 当参数无效时抛出
        TypeError: 当参数类型错误时抛出

    Example:
        >>> function_name("example", 42)
        "result"
    """
    '''
    
    # 类文档字符串模板
    class_docstring_template = '''
    """类的简短描述。

    详细描述类的功能、用途和主要特性。

    Attributes:
        attr1 (type): 属性1的描述
        attr2 (type): 属性2的描述

    Example:
        >>> obj = ClassName()
        >>> obj.method()
        "result"
    """
    '''
    
    # API文档规范
    api_documentation_template = '''
    # API文档规范

    ## 端点描述
    - **URL**: `/api/v1/resource`
    - **Method**: `GET`
    - **Description**: 获取资源列表

    ## 请求参数
    | 参数名 | 类型 | 必需 | 描述 |
    |--------|------|------|------|
    | page | int | 否 | 页码，默认为1 |
    | size | int | 否 | 每页大小，默认为20 |

    ## 响应格式
    ```json
    {
        "code": 200,
        "message": "success",
        "data": {
            "items": [...],
            "total": 100,
            "page": 1,
            "size": 20
        }
    }
    ```

    ## 错误码
    | 错误码 | 描述 |
    |--------|------|
    | 400 | 请求参数错误 |
    | 401 | 未授权 |
    | 404 | 资源不存在 |
    | 500 | 服务器内部错误 |
    '''
    
    # README模板
    readme_template = '''
    # 项目名称

    简短的项目描述。

    ## 功能特性

    - 特性1
    - 特性2
    - 特性3

    ## 安装

    ```bash
    pip install package-name
    ```

    ## 快速开始

    ```python
    from package_name import main_function
    
    result = main_function()
    print(result)
    ```

    ## 文档

    详细文档请查看 [docs/](docs/) 目录。

    ## 贡献

    欢迎提交Issue和Pull Request！

    ## 许可证

    MIT License
    '''
```

---

## 总结

Python最佳实践2025涵盖了现代Python开发的各个方面：

1. **代码质量与规范**：类型安全、异步编程、错误处理
2. **性能优化**：内存管理、算法优化、基准测试
3. **安全最佳实践**：输入验证、加密、安全通信
4. **测试最佳实践**：单元测试、集成测试、测试数据生成
5. **部署与运维**：容器化、监控、日志记录
6. **团队协作**：代码规范、文档规范、Git规范

这些最佳实践将帮助开发者：

- 编写高质量、可维护的代码
- 提高应用性能和安全性
- 建立有效的测试和部署流程
- 促进团队协作和知识共享

通过遵循这些最佳实践，Python开发者可以在2025年及以后构建出更加优秀、安全、高效的应用程序。
