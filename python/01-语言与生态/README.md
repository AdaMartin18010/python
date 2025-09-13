# 01-语言与生态（2025）

聚焦语言新特性、生态与工具链的系统化实践。

## 1. 语言与版本

- 收敛到 2025 主流稳定版本
- 新特性综述与可迁移性评估
  - 本地副本：[迁移/01-语言新特性](./迁移/01-语言新特性.md)

> 版本基线：Python 3.12 为默认，关注 3.13 新特性（如更快的解释器、JIT 研究进展、性能与诊断改进）。确保示例与 CI 默认以 3.12 通过，兼容 3.11/3.13。

### 1.1 Python 3.12+ 核心特性

#### 1.1.1 结构化模式匹配（PEP 634）

```python
# 模式匹配示例
def process_data(data):
    match data:
        case {"type": "user", "name": name, "age": age} if age >= 18:
            return f"Adult user: {name}"
        case {"type": "user", "name": name, "age": age}:
            return f"Minor user: {name}"
        case {"type": "admin", "name": name}:
            return f"Admin: {name}"
        case _:
            return "Unknown data type"
```

#### 1.1.2 类型系统增强（PEP 695）

```python
# 类型参数语法
class Container[T]:
    def __init__(self, item: T):
        self.item = item
    
    def get(self) -> T:
        return self.item

# 泛型类型别名
type UserDict = dict[str, User]
type ProcessResult[T] = tuple[bool, T | None]
```

#### 1.1.3 f-string 任意表达式（PEP 701）

```python
# f-string 增强
x = 10
y = 20
print(f'{x=}, {y=}, {x+y=}')  # 输出: x=10, y=20, x+y=30

# 复杂表达式
data = {"name": "Python", "version": "3.12"}
print(f'Language: {data["name"]}, Version: {data["version"]}')
```

## 2. 工具链（uv/pip/venv）

- 安装、迁移策略与镜像源
- 项目级/工作区级依赖管理
  - 本地副本：
    - [迁移/06-uv工具综述](./迁移/06-uv工具综述.md)
    - [迁移/07-uv技术深度分析](./迁移/07-uv技术深度分析.md)
    - [迁移/08-uv生态系统解析](./迁移/08-uv生态系统解析.md)
    - [迁移/09-uv完成度总结](./迁移/09-uv完成度总结.md)
    - [迁移/10-uv技术深潜](./迁移/10-uv技术深潜.md)

### 2.1 uv 工具革命

uv 是 Astral 公司开发的超高速 Python 包管理器，用 Rust 编写，比 pip 快 10-100 倍：

#### 2.1.1 性能对比

```bash
# 数据科学栈安装对比
time pip install numpy pandas scikit-learn matplotlib seaborn
# 结果: 平均120秒

time uv pip install numpy pandas scikit-learn matplotlib seaborn
# 结果: 平均12秒 (10x提升)

# Web开发栈安装对比
time pip install django djangorestframework django-cors-headers
# 结果: 平均45秒

time uv pip install django djangorestframework django-cors-headers
# 结果: 平均4.5秒 (10x提升)
```

#### 2.1.2 核心优势

- **极速安装**: 使用 Rust 实现，并行下载和依赖解析
- **完全兼容**: 100% 兼容 pip 生态系统，支持所有 PyPI 包
- **智能缓存**: 全局缓存机制减少重复下载
- **现代化设计**: 简化的命令行接口，智能依赖解析
- **企业级支持**: 适合大型项目、CI/CD 流水线、数据科学项目

### 2.2 快速开始（Windows / PowerShell）

```powershell
# 安装 uv（优先使用 pipx）
pipx install uv || pip install uv

# 创建与同步依赖（基于 pyproject.toml）
uv pip compile pyproject.toml -o uv.lock
uv pip sync uv.lock

# 创建并激活虚拟环境（如需）
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

### 2.3 常见任务对照

- 创建项目骨架：使用 `pyproject.toml` + `uv` 生成与同步；发布前锁定 `uv.lock`。
- 多工作区：在仓库根维护统一锁文件；子项目继承基础工具链（ruff/mypy/pytest）。
- 国内镜像：`uv pip --index-url <mirror> sync uv.lock`，或在 `pip.conf`/`uv config` 中设置。

## 3. 测试与质量

- pytest、类型、lint 体系
- 最小可运行样例与项目模板
  - 本地副本：
    - [../02-测试与质量/迁移/质量检查.md](../02-测试与质量/迁移/质量检查.md)
  - 推荐工具集：pytest + ruff + mypy（或 pyright）+ pre-commit

## 4. 性能与安全

- 性能剖析与优化策略
- 供应链与运行安全
  - 本地副本：
    - [迁移/05-性能优化指南](./迁移/05-性能优化指南.md)
    - [迁移/04-安全开发指南](./迁移/04-安全开发指南.md)

## 5. 工程与交付

- 打包/发布/部署流水线
- 多环境配置与运维接口

## 6. 生态综述

- 库与框架成熟度
  - 本地副本：[迁移/02-技术栈2025](./迁移/02-技术栈2025.md)

### 6.1 2025年主流技术栈

#### 6.1.1 Web与API开发技术栈

```python
# FastAPI + Pydantic 2.x 现代API开发
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Annotated
import uvicorn

app = FastAPI(title="Modern Python API", version="2.0.0")

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(regex=r"^[^@]+@[^@]+\.[^@]+$")
    age: int = Field(ge=0, le=150)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    is_active: bool = True

# 依赖注入与类型安全
async def get_user_service() -> UserService:
    return UserService()

@app.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    return await service.create_user(user)
```

#### 6.1.2 数据科学与AI技术栈

```python
# 现代数据科学工作流
import polars as pl
import numpy as np
from typing import TypeVar, Generic

# 类型安全的数据处理
class DataProcessor[T]:
    def __init__(self, data: pl.DataFrame):
        self.data = data
    
    def filter_by_condition(self, condition: pl.Expr) -> "DataProcessor[T]":
        self.data = self.data.filter(condition)
        return self
    
    def select_columns(self, columns: list[str]) -> "DataProcessor[T]":
        self.data = self.data.select(columns)
        return self
    
    def group_by_agg(self, group_cols: list[str], agg_exprs: list[pl.Expr]) -> "DataProcessor[T]":
        self.data = self.data.group_by(group_cols).agg(agg_exprs)
        return self
```

#### 6.1.3 工具生态对比

| 工具 | 成熟度 | 性能 | 生态系统兼容性 | 企业支持 | 适用场景 |
|------|--------|------|----------------|----------|----------|
| pip | 极高 | 中等 | 100% | 官方支持 | 通用场景 |
| uv | 高 | 极高 | 100% | Astral支持 | 大型项目、CI/CD |
| poetry | 高 | 高 | 95% | 社区驱动 | 中大型项目 |
| conda | 高 | 中等 | 80% | Anaconda支持 | 数据科学 |
| rye | 中 | 高 | 90% | 社区驱动 | 极简开发 |

## 7. 最佳实践

- 团队与工程实践
  - 本地副本：[迁移/03-最佳实践2025](./迁移/03-最佳实践2025.md)

### 7.1 类型安全编程最佳实践

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
```

### 7.2 异步编程最佳实践

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
```

### 7.3 性能优化最佳实践

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
```

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 相关规范：[重构规范](../99-上下文与流程/03-重构规范.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)
- 相关主题：
  - [02-测试与质量](../02-测试与质量/README.md)
  - [03-工程与交付](../03-工程与交付/README.md)
  - [04-并发与异步](../04-并发与异步/README.md)

## 来源与回链（docs → python）

- 新特性来源：`docs/model/Programming_Language/python_new_features.md` → 本地：[迁移/01-语言新特性](./迁移/01-语言新特性.md)
- 性能来源：`docs/model/Programming_Language/python_performance_optimization.md` → 本地：[迁移/05-性能优化指南](./迁移/05-性能优化指南.md)
- 最佳实践来源：`docs/model/Programming_Language/python_best_practices_2025.md` → 本地：[迁移/03-最佳实践2025](./迁移/03-最佳实践2025.md)
- uv工具来源：`docs/model/Programming_Language/python_uv_*.md` → 本地：[迁移/06-uv工具综述](./迁移/06-uv工具综述.md)
- 技术栈来源：`docs/model/Programming_Language/python_tech_stack_2025.md` → 本地：[迁移/02-技术栈2025](./迁移/02-技术栈2025.md)
