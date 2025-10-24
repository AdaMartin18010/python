# Python 2025 快速参考手册

**版本：** v2025.10.24  
**最后更新：** 2025年10月24日

---

## 🚀 快速开始

### 安装环境

```bash
# 1. 运行安装脚本
chmod +x scripts/setup_dev_env.sh
./scripts/setup_dev_env.sh

# 2. 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 3. 安装依赖
uv sync
```

### 运行示例

```bash
# 使用示例运行器
chmod +x scripts/run_examples.sh
./scripts/run_examples.sh

# 或手动运行
cd python/07-监控与可观测性/examples
uvicorn complete_monitoring_app:app --reload
```

---

## 📚 常用命令

### uv包管理

```bash
# 初始化项目
uv init

# 安装包
uv add fastapi
uv add --dev pytest

# 同步依赖
uv sync

# 更新包
uv lock --upgrade

# 运行脚本
uv run python script.py
```

### ruff代码质量

```bash
# 检查代码
ruff check .

# 自动修复
ruff check --fix .

# 格式化代码
ruff format .

# 检查特定文件
ruff check app/main.py
```

### mypy类型检查

```bash
# 检查整个项目
mypy .

# 检查特定模块
mypy app/

# 严格模式
mypy --strict .
```

### pytest测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_api.py

# 带覆盖率
pytest --cov

# 详细输出
pytest -v

# 只运行失败的
pytest --lf
```

---

## 🎯 核心概念速查

### Python 3.13新特性

```python
# Free-Threaded模式（无GIL）
# 启动方式: python3.13t app.py
# 或设置: export PYTHON_GIL=0

# JIT编译器
# 启动方式: export PYTHON_JIT=1

# 性能提升
# Free-Threaded: 2-8x (多核CPU)
# JIT: 20-60% (纯Python代码)
```

### 类型注解

```python
from typing import Optional, List, Dict, Union, Any
from collections.abc import Callable

# 基础类型
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 可选类型
def find_user(user_id: int) -> Optional[dict]:
    return None

# 泛型
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# 联合类型
def handle_data(data: Union[str, int, None]) -> str:
    return str(data)

# Callable
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

# Python 3.12+ 泛型语法
def first[T](items: list[T]) -> T:
    return items[0]
```

### 异步编程

```python
import asyncio

# 基础async/await
async def fetch_data():
    await asyncio.sleep(1)
    return "data"

# 并发执行
async def main():
    results = await asyncio.gather(
        fetch_data(),
        fetch_data(),
        fetch_data()
    )

# 异步上下文管理器
async with aiofiles.open("file.txt") as f:
    content = await f.read()

# 异步迭代器
async for item in async_iterator:
    process(item)
```

---

## 🛠️ 常用代码片段

### FastAPI基础

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items")
async def create_item(item: Item):
    return item

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

### Pytest基础

```python
import pytest

# 基础测试
def test_addition():
    assert 1 + 1 == 2

# Fixture
@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

# 参数化
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 3),
    (3, 4),
])
def test_increment(input, expected):
    assert input + 1 == expected

# 异步测试
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

### Pydantic模型

```python
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., gt=0, lt=150)
    created_at: datetime = Field(default_factory=datetime.now)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "age": 30
            }
        }
```

---

## 📊 性能优化清单

### 代码级优化

- [ ] 使用生成器代替列表（内存优化）
- [ ] 使用`@lru_cache`缓存函数结果
- [ ] 避免重复计算，提取常量
- [ ] 使用列表推导式代替循环
- [ ] 使用`set`进行快速查找（O(1) vs O(n)）
- [ ] 使用`collections.defaultdict`简化代码
- [ ] 使用`bisect`维护有序列表

### 数据库优化

- [ ] 使用连接池（pool_size=20-50）
- [ ] 批量操作代替逐条操作
- [ ] 使用`joinedload`/`selectinload`避免N+1
- [ ] 添加适当的索引
- [ ] 使用`select_in_loading`预加载关系

### 缓存策略

- [ ] 使用Redis缓存热点数据
- [ ] 实现多级缓存（内存+Redis）
- [ ] 设置合理的TTL（1-60分钟）
- [ ] 使用缓存预热避免雪崩
- [ ] 实现缓存击穿保护

---

## 🔒 安全检查清单

### 认证与授权

- [ ] 使用OAuth 2.1 / OIDC
- [ ] 实现JWT令牌认证
- [ ] 设置令牌过期时间（15-30分钟）
- [ ] 实现刷新令牌机制
- [ ] 使用RBAC权限控制

### 输入验证

- [ ] 使用Pydantic验证所有输入
- [ ] 参数化SQL查询（防注入）
- [ ] 验证文件上传类型和大小
- [ ] 限制请求大小
- [ ] 使用白名单验证

### 安全配置

- [ ] 配置CORS白名单
- [ ] 添加安全响应头（HSTS, CSP等）
- [ ] 实现速率限制
- [ ] 禁用生产环境调试模式
- [ ] 使用HTTPS

### 数据保护

- [ ] 加密敏感数据（密码、信用卡等）
- [ ] 实现数据脱敏
- [ ] 记录审计日志
- [ ] 定期备份数据
- [ ] 实现GDPR合规

---

## 📈 监控检查清单

### Prometheus指标

- [ ] HTTP请求总数（Counter）
- [ ] HTTP请求延迟（Histogram）
- [ ] 正在处理的请求数（Gauge）
- [ ] 错误率
- [ ] 业务指标（订单数、用户数等）

### OpenTelemetry追踪

- [ ] 配置追踪提供者
- [ ] 自动追踪HTTP请求
- [ ] 手动追踪关键函数
- [ ] 添加自定义属性
- [ ] 配置采样率（生产5-10%）

### Structlog日志

- [ ] 配置JSON格式输出
- [ ] 添加trace_id和span_id
- [ ] 记录关键业务事件
- [ ] 设置合理的日志级别
- [ ] 实现日志轮转

### Grafana告警

- [ ] 高错误率告警（>5%）
- [ ] 高延迟告警（P95 >1s）
- [ ] 服务下线告警
- [ ] 磁盘空间告警（>80%）
- [ ] CPU/内存使用告警（>80%）

---

## 🎯 部署检查清单

### Docker

- [ ] 使用多阶段构建
- [ ] 指定固定版本标签
- [ ] 非root用户运行
- [ ] 最小化镜像大小
- [ ] 健康检查配置

### Kubernetes

- [ ] 配置资源限制（CPU、内存）
- [ ] 设置副本数（≥2）
- [ ] 配置健康检查（liveness、readiness）
- [ ] 使用ConfigMap和Secrets
- [ ] 配置HPA自动扩缩容

### CI/CD

- [ ] 运行单元测试
- [ ] 运行代码检查（ruff、mypy）
- [ ] 运行安全扫描（Bandit、Trivy）
- [ ] 生成测试覆盖率报告
- [ ] 自动部署到环境

---

## 📞 获取帮助

### 文档

- **完整索引**: [INDEX_COMPREHENSIVE_2025.md](INDEX_COMPREHENSIVE_2025.md)
- **快速开始**: [QUICK_START.md](python/01-语言与生态/templates/QUICK_START.md)
- **更新日志**: [LATEST_UPDATE_2025_10_24.md](LATEST_UPDATE_2025_10_24.md)

### 在线资源

- Python官方: <https://docs.python.org/>
- FastAPI: <https://fastapi.tiangolo.com/>
- LangChain: <https://python.langchain.com/>
- Prometheus: <https://prometheus.io/>

### 运行示例

```bash
# 查看所有可运行的示例
./scripts/run_examples.sh
```

---

**版本：** v2025.10.24  
**维护：** Python Knowledge Base Team  
**许可：** MIT


