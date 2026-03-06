# 软件架构设计模式全面指南

> 本文档系统梳理现代软件架构设计模式，包含概念定义、架构图、Python实现、正例反例及演进路径。

---

## 目录

- [软件架构设计模式全面指南](#软件架构设计模式全面指南)
  - [目录](#目录)
  - [第一部分：分层架构](#第一部分分层架构)
    - [1.1 三层架构（Three-Tier Architecture）](#11-三层架构three-tier-architecture)
      - [概念定义](#概念定义)
      - [架构图](#架构图)
      - [适用场景](#适用场景)
      - [Python实现](#python实现)
      - [正例](#正例)
      - [反例](#反例)
      - [架构演进路径](#架构演进路径)
    - [1.2 N层架构（N-Tier Architecture）](#12-n层架构n-tier-architecture)
      - [概念定义](#概念定义-1)
      - [架构图](#架构图-1)
      - [Python实现](#python实现-1)
    - [1.3 洋葱架构（Onion Architecture）](#13-洋葱架构onion-architecture)
      - [概念定义](#概念定义-2)
      - [架构图](#架构图-2)
      - [Python实现](#python实现-2)
    - [1.4 整洁架构（Clean Architecture）](#14-整洁架构clean-architecture)
      - [概念定义](#概念定义-3)
      - [架构图](#架构图-3)
      - [Python实现](#python实现-3)
      - [分层架构对比](#分层架构对比)
  - [第二部分：微服务架构](#第二部分微服务架构)
    - [2.1 服务拆分原则](#21-服务拆分原则)
      - [概念定义](#概念定义-4)
      - [拆分策略](#拆分策略)
        - [按业务能力拆分（Business Capability）](#按业务能力拆分business-capability)
        - [按领域边界拆分（Domain Boundary）](#按领域边界拆分domain-boundary)
      - [拆分原则（AKF扩展立方）](#拆分原则akf扩展立方)
      - [Python实现 - 服务拆分示例](#python实现---服务拆分示例)
    - [2.2 API网关](#22-api网关)
      - [概念定义](#概念定义-5)
      - [主流API网关对比](#主流api网关对比)
      - [Python实现 - FastAPI API网关](#python实现---fastapi-api网关)
    - [2.3 服务间通信](#23-服务间通信)
      - [同步通信](#同步通信)
        - [REST API](#rest-api)
        - [gRPC](#grpc)
      - [异步通信 - 消息队列](#异步通信---消息队列)
    - [2.4 服务发现](#24-服务发现)
    - [2.5 配置中心](#25-配置中心)
  - [第三部分：事件驱动架构](#第三部分事件驱动架构)
    - [3.1 事件溯源（Event Sourcing）](#31-事件溯源event-sourcing)
      - [概念定义](#概念定义-6)
      - [核心概念](#核心概念)
      - [Python实现](#python实现-4)
    - [3.2 CQRS（命令查询职责分离）](#32-cqrs命令查询职责分离)
      - [概念定义](#概念定义-7)
      - [Python实现](#python实现-5)
    - [3.3 事件总线](#33-事件总线)
    - [3.4 Saga编排](#34-saga编排)
  - [第四部分：领域驱动设计（DDD）](#第四部分领域驱动设计ddd)
    - [4.1 战略设计](#41-战略设计)
      - [概念定义](#概念定义-8)
      - [限界上下文](#限界上下文)
      - [上下文映射模式](#上下文映射模式)
    - [4.2 战术设计](#42-战术设计)
      - [概念定义](#概念定义-9)
      - [实体 vs 值对象](#实体-vs-值对象)
    - [4.3 Python DDD实现](#43-python-ddd实现)
  - [第五部分：六边形架构](#第五部分六边形架构)
    - [5.1 概念定义](#51-概念定义)
    - [5.2 核心原则](#52-核心原则)
    - [5.3 Python实现](#53-python实现)
  - [第六部分：Serverless架构](#第六部分serverless架构)
    - [6.1 概念定义](#61-概念定义)
    - [6.2 FaaS（函数即服务）](#62-faas函数即服务)
      - [核心特征](#核心特征)
      - [主流FaaS平台](#主流faas平台)
    - [6.3 BaaS（后端即服务）](#63-baas后端即服务)
      - [核心服务](#核心服务)
    - [6.4 Python Lambda实现](#64-python-lambda实现)
  - [第七部分：云原生架构](#第七部分云原生架构)
    - [7.1 概念定义](#71-概念定义)
    - [7.2 容器化（Docker）](#72-容器化docker)
      - [核心概念](#核心概念-1)
      - [Dockerfile最佳实践](#dockerfile最佳实践)
      - [Python容器化示例](#python容器化示例)
    - [7.3 编排（Kubernetes概念）](#73-编排kubernetes概念)
      - [Kubernetes YAML示例](#kubernetes-yaml示例)
    - [7.4 服务网格（Istio概念）](#74-服务网格istio概念)
      - [Istio核心功能](#istio核心功能)
    - [7.5 可观测性](#75-可观测性)
      - [Python可观测性实现](#python可观测性实现)
    - [7.6 云原生最佳实践总结](#76-云原生最佳实践总结)
  - [附录：架构演进路径](#附录架构演进路径)
  - [架构选择指南](#架构选择指南)

---

## 第一部分：分层架构

### 1.1 三层架构（Three-Tier Architecture）

#### 概念定义

三层架构是最经典的分层模式，将应用程序划分为三个逻辑层：

- **表示层（Presentation Layer）**：负责用户界面展示和用户交互
- **业务逻辑层（Business Logic Layer）**：处理核心业务规则和逻辑
- **数据访问层（Data Access Layer）**：负责数据持久化和数据库操作

#### 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    表示层 (Presentation)                  │
│              Web界面 / API / 移动端界面                    │
├─────────────────────────────────────────────────────────┤
│                    业务逻辑层 (Business)                  │
│              领域逻辑 / 业务规则 / 流程控制                │
├─────────────────────────────────────────────────────────┤
│                    数据访问层 (Data Access)               │
│              数据库操作 / ORM / 文件存储                   │
└─────────────────────────────────────────────────────────┘
```

#### 适用场景

| 场景 | 说明 |
|------|------|
| 中小型Web应用 | 业务逻辑相对简单，团队规模较小 |
| 快速原型开发 | 需要快速交付的MVP项目 |
| 传统企业应用 | 业务流程清晰，变化频率低 |
| 学习项目 | 理解分层架构的基础概念 |

#### Python实现

```python
"""
三层架构完整实现示例 - 电商订单系统
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict
import json


# ==================== 数据访问层 ====================

class DatabaseConnection:
    """模拟数据库连接"""
    def __init__(self):
        self._orders: Dict[int, dict] = {}
        self._products: Dict[int, dict] = {
            1: {"id": 1, "name": "笔记本电脑", "price": 5999.00, "stock": 100},
            2: {"id": 2, "name": "无线鼠标", "price": 99.00, "stock": 500},
            3: {"id": 3, "name": "机械键盘", "price": 399.00, "stock": 200},
        }
        self._next_order_id = 1

    def execute_query(self, query: str, params: tuple = ()) -> List[dict]:
        """模拟执行查询"""
        # 简化实现
        return list(self._orders.values())

    def execute_insert(self, table: str, data: dict) -> int:
        """模拟插入操作"""
        if table == "orders":
            order_id = self._next_order_id
            self._next_order_id += 1
            data["id"] = order_id
            self._orders[order_id] = data
            return order_id
        return 0

    def execute_update(self, query: str, params: tuple = ()) -> bool:
        """模拟更新操作"""
        return True


class OrderRepository:
    """订单仓储 - 数据访问层"""

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def get_by_id(self, order_id: int) -> Optional[dict]:
        """根据ID获取订单"""
        return self._db._orders.get(order_id)

    def get_all(self) -> List[dict]:
        """获取所有订单"""
        return list(self._db._orders.values())

    def create(self, order_data: dict) -> int:
        """创建订单"""
        order_data["created_at"] = datetime.now().isoformat()
        order_data["status"] = "pending"
        return self._db.execute_insert("orders", order_data)

    def update_status(self, order_id: int, status: str) -> bool:
        """更新订单状态"""
        if order_id in self._db._orders:
            self._db._orders[order_id]["status"] = status
            return True
        return False


class ProductRepository:
    """产品仓储 - 数据访问层"""

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def get_by_id(self, product_id: int) -> Optional[dict]:
        """根据ID获取产品"""
        return self._db._products.get(product_id)

    def update_stock(self, product_id: int, quantity: int) -> bool:
        """更新库存"""
        if product_id in self._db._products:
            self._db._products[product_id]["stock"] -= quantity
            return True
        return False


# ==================== 业务逻辑层 ====================

@dataclass
class OrderItem:
    """订单项"""
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    """订单领域对象"""
    id: Optional[int]
    customer_name: str
    items: List[OrderItem]
    status: str = "pending"
    created_at: Optional[str] = None

    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.items)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal
                }
                for item in self.items
            ],
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at
        }


class OrderService:
    """订单服务 - 业务逻辑层"""

    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self._order_repo = order_repo
        self._product_repo = product_repo

    def create_order(self, customer_name: str, items_data: List[dict]) -> dict:
        """创建订单 - 核心业务逻辑"""
        # 1. 验证产品并构建订单项
        order_items = []
        for item_data in items_data:
            product = self._product_repo.get_by_id(item_data["product_id"])
            if not product:
                raise ValueError(f"产品不存在: {item_data['product_id']}")

            if product["stock"] < item_data["quantity"]:
                raise ValueError(f"库存不足: {product['name']}")

            order_items.append(OrderItem(
                product_id=product["id"],
                product_name=product["name"],
                quantity=item_data["quantity"],
                unit_price=product["price"]
            ))

        # 2. 创建订单对象
        order = Order(
            id=None,
            customer_name=customer_name,
            items=order_items
        )

        # 3. 应用业务规则
        if order.total_amount > 10000:
            # 大额订单需要额外验证
            pass  # 实际项目中可能有更多逻辑

        # 4. 保存订单
        order_dict = order.to_dict()
        order_id = self._order_repo.create(order_dict)
        order.id = order_id
        order.created_at = datetime.now().isoformat()

        # 5. 扣减库存
        for item in order_items:
            self._product_repo.update_stock(item.product_id, item.quantity)

        return order.to_dict()

    def get_order(self, order_id: int) -> Optional[dict]:
        """获取订单详情"""
        return self._order_repo.get_by_id(order_id)

    def confirm_order(self, order_id: int) -> bool:
        """确认订单"""
        order = self._order_repo.get_by_id(order_id)
        if not order:
            return False

        if order["status"] != "pending":
            raise ValueError("只能确认待处理订单")

        return self._order_repo.update_status(order_id, "confirmed")

    def list_orders(self) -> List[dict]:
        """列出所有订单"""
        return self._order_repo.get_all()


# ==================== 表示层 ====================

class OrderController:
    """订单控制器 - 表示层"""

    def __init__(self, order_service: OrderService):
        self._order_service = order_service

    def create_order(self, request_data: dict) -> dict:
        """处理创建订单请求"""
        try:
            # 1. 验证请求数据
            if "customer_name" not in request_data:
                return {"success": False, "error": "缺少客户名称"}

            if "items" not in request_data or not request_data["items"]:
                return {"success": False, "error": "订单项不能为空"}

            # 2. 调用业务层
            result = self._order_service.create_order(
                customer_name=request_data["customer_name"],
                items_data=request_data["items"]
            )

            # 3. 构建响应
            return {
                "success": True,
                "data": result,
                "message": "订单创建成功"
            }

        except ValueError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"系统错误: {str(e)}"}

    def get_order(self, order_id: int) -> dict:
        """处理获取订单请求"""
        order = self._order_service.get_order(order_id)
        if order:
            return {"success": True, "data": order}
        return {"success": False, "error": "订单不存在"}

    def list_orders(self) -> dict:
        """处理列出订单请求"""
        orders = self._order_service.list_orders()
        return {"success": True, "data": orders, "total": len(orders)}


# ==================== 应用入口 ====================

def create_app():
    """工厂函数 - 创建应用实例"""
    # 1. 创建数据库连接
    db = DatabaseConnection()

    # 2. 创建仓储
    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)

    # 3. 创建服务
    order_service = OrderService(order_repo, product_repo)

    # 4. 创建控制器
    order_controller = OrderController(order_service)

    return order_controller


# ==================== 运行示例 ====================

if __name__ == "__main__":
    # 创建应用
    app = create_app()

    print("=" * 60)
    print("三层架构演示 - 电商订单系统")
    print("=" * 60)

    # 创建订单
    print("\n1. 创建订单:")
    create_request = {
        "customer_name": "张三",
        "items": [
            {"product_id": 1, "quantity": 1},  # 笔记本电脑
            {"product_id": 2, "quantity": 2}   # 无线鼠标x2
        ]
    }
    result = app.create_order(create_request)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 创建另一个订单
    create_request2 = {
        "customer_name": "李四",
        "items": [
            {"product_id": 3, "quantity": 1}   # 机械键盘
        ]
    }
    result2 = app.create_order(create_request2)
    print(json.dumps(result2, indent=2, ensure_ascii=False))

    # 列出所有订单
    print("\n2. 列出所有订单:")
    list_result = app.list_orders()
    print(json.dumps(list_result, indent=2, ensure_ascii=False))

    # 获取单个订单
    print("\n3. 获取订单详情:")
    order_result = app.get_order(1)
    print(json.dumps(order_result, indent=2, ensure_ascii=False))
```

#### 正例

```python
# ✅ 正确的三层架构实践

# 1. 数据层只负责数据操作
class UserRepository:
    def get_user(self, user_id: int) -> dict:
        return self.db.query("SELECT * FROM users WHERE id = ?", (user_id,))

# 2. 业务层只负责业务逻辑
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def validate_and_create_user(self, user_data: dict) -> dict:
        # 业务验证
        if not self._is_valid_email(user_data["email"]):
            raise ValueError("Invalid email")
        # 调用数据层
        return self.user_repo.create(user_data)

# 3. 表示层只负责请求处理
class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle_create_request(self, request: dict) -> dict:
        try:
            result = self.user_service.validate_and_create_user(request)
            return {"success": True, "data": result}
        except ValueError as e:
            return {"success": False, "error": str(e)}
```

#### 反例

```python
# ❌ 错误的三层架构实践

# 1. 数据层混入业务逻辑
class UserRepository:
    def create_user(self, user_data: dict):
        # ❌ 业务逻辑不应该在这里
        if not self._validate_email(user_data["email"]):
            raise ValueError("Invalid email")
        if user_data["age"] < 18:
            raise ValueError("Must be 18+")
        # ... 数据库操作

# 2. 表示层直接操作数据库
class UserController:
    def handle_request(self, request: dict):
        # ❌ 控制器不应该直接访问数据库
        db = DatabaseConnection()
        db.execute("INSERT INTO users ...")
        # 缺少业务层验证

# 3. 层间依赖混乱
class BusinessService:
    def __init__(self):
        # ❌ 服务层不应该知道HTTP请求细节
        self.http_client = HttpClient()
        self.request_parser = RequestParser()
```

#### 架构演进路径

```
单层架构 → 三层架构 → N层架构 → 洋葱架构/整洁架构
     ↓           ↓           ↓
   快速原型    企业应用    复杂业务系统
```

---

### 1.2 N层架构（N-Tier Architecture）

#### 概念定义

N层架构是三层架构的扩展，将系统划分为更多的细粒度层次，常见扩展包括：

- **API网关层**：请求路由、认证、限流
- **应用服务层**：用例编排、事务管理
- **领域服务层**：核心业务规则
- **基础设施层**：日志、缓存、消息队列

#### 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    API网关层                              │
│              认证 / 限流 / 路由 / 负载均衡                  │
├─────────────────────────────────────────────────────────┤
│                    表示层 (Controller)                    │
│              REST API / GraphQL / gRPC                   │
├─────────────────────────────────────────────────────────┤
│                    应用服务层 (Application)               │
│              用例编排 / 事务管理 / 工作流                  │
├─────────────────────────────────────────────────────────┤
│                    领域服务层 (Domain)                    │
│              业务规则 / 领域逻辑 / 策略模式                │
├─────────────────────────────────────────────────────────┤
│                    数据访问层 (Repository)                │
│              ORM / 数据库 / 缓存 / 搜索引擎                │
├─────────────────────────────────────────────────────────┤
│                    基础设施层 (Infrastructure)            │
│              日志 / 监控 / 消息队列 / 文件存储             │
└─────────────────────────────────────────────────────────┘
```

#### Python实现

```python
"""
N层架构实现 - 用户管理系统
包含：API网关层、应用服务层、领域服务层、数据访问层、基础设施层
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Callable
from functools import wraps
import hashlib
import json
import time


# ==================== 基础设施层 ====================

class Logger:
    """日志服务"""
    def log(self, level: str, message: str, context: dict = None):
        timestamp = datetime.now().isoformat()
        ctx = json.dumps(context, ensure_ascii=False) if context else "{}"
        print(f"[{timestamp}] [{level}] {message} | Context: {ctx}")

    def info(self, message: str, context: dict = None):
        self.log("INFO", message, context)

    def error(self, message: str, context: dict = None):
        self.log("ERROR", message, context)


class CacheService:
    """缓存服务"""
    def __init__(self):
        self._cache: Dict[str, tuple] = {}  # value, expire_time

    def get(self, key: str) -> Optional[any]:
        if key in self._cache:
            value, expire_time = self._cache[key]
            if expire_time > time.time():
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: any, ttl: int = 300):
        self._cache[key] = (value, time.time() + ttl)

    def delete(self, key: str):
        self._cache.pop(key, None)


class EventBus:
    """事件总线"""
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event_type: str, event_data: dict):
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event_data)


# ==================== 数据访问层 ====================

@dataclass
class UserEntity:
    """用户实体"""
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UserRepository:
    """用户仓储"""

    def __init__(self, logger: Logger):
        self._users: Dict[int, UserEntity] = {}
        self._next_id = 1
        self._logger = logger

    def find_by_id(self, user_id: int) -> Optional[UserEntity]:
        self._logger.info(f"Finding user by id: {user_id}")
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[UserEntity]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def find_all(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        users = list(self._users.values())
        return users[skip:skip + limit]

    def save(self, user: UserEntity) -> UserEntity:
        now = datetime.now().isoformat()
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
            user.created_at = now
        user.updated_at = now
        self._users[user.id] = user
        self._logger.info(f"User saved: {user.id}")
        return user

    def delete(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            self._logger.info(f"User deleted: {user_id}")
            return True
        return False


# ==================== 领域服务层 ====================

class PasswordHasher:
    """密码哈希服务"""
    @staticmethod
    def hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return PasswordHasher.hash(password) == hashed


class UserDomainService:
    """用户领域服务 - 核心业务规则"""

    def __init__(self, logger: Logger):
        self._logger = logger

    def validate_username(self, username: str) -> bool:
        """验证用户名规则"""
        if not username or len(username) < 3:
            return False
        if not username.isalnum():
            return False
        return True

    def validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_password(self, password: str) -> tuple[bool, str]:
        """验证密码强度"""
        if len(password) < 8:
            return False, "密码长度至少8位"
        if not any(c.isupper() for c in password):
            return False, "密码必须包含大写字母"
        if not any(c.islower() for c in password):
            return False, "密码必须包含小写字母"
        if not any(c.isdigit() for c in password):
            return False, "密码必须包含数字"
        return True, "密码强度合格"

    def create_user_entity(self, username: str, email: str, password: str) -> UserEntity:
        """创建用户实体"""
        # 验证所有规则
        if not self.validate_username(username):
            raise ValueError("用户名无效")
        if not self.validate_email(email):
            raise ValueError("邮箱格式无效")

        valid, msg = self.validate_password(password)
        if not valid:
            raise ValueError(msg)

        return UserEntity(
            id=None,
            username=username,
            email=email,
            password_hash=PasswordHasher.hash(password)
        )


# ==================== 应用服务层 ====================

class TransactionManager:
    """事务管理器"""
    def __init__(self, logger: Logger):
        self._logger = logger
        self._operations: List[Callable] = []

    def add_operation(self, operation: Callable, rollback: Callable):
        self._operations.append((operation, rollback))

    def execute(self):
        executed = []
        try:
            for operation, _ in self._operations:
                operation()
                executed.append(operation)
        except Exception as e:
            # 回滚已执行的操作
            for i in range(len(executed) - 1, -1, -1):
                _, rollback = self._operations[i]
                rollback()
            raise e


class UserApplicationService:
    """用户应用服务 - 用例编排"""

    def __init__(
        self,
        user_repo: UserRepository,
        domain_service: UserDomainService,
        cache: CacheService,
        event_bus: EventBus,
        logger: Logger
    ):
        self._user_repo = user_repo
        self._domain_service = domain_service
        self._cache = cache
        self._event_bus = event_bus
        self._logger = logger

    def register_user(self, username: str, email: str, password: str) -> dict:
        """用户注册用例"""
        self._logger.info("Starting user registration", {"username": username, "email": email})

        # 1. 检查邮箱是否已存在
        existing = self._user_repo.find_by_email(email)
        if existing:
            raise ValueError("邮箱已被注册")

        # 2. 创建用户实体（领域服务处理业务规则）
        user = self._domain_service.create_user_entity(username, email, password)

        # 3. 保存用户
        saved_user = self._user_repo.save(user)

        # 4. 发布事件
        self._event_bus.publish("user.created", {
            "user_id": saved_user.id,
            "username": saved_user.username,
            "email": saved_user.email
        })

        # 5. 更新缓存
        self._cache.set(f"user:{saved_user.id}", saved_user)

        self._logger.info("User registration completed", {"user_id": saved_user.id})

        return {
            "id": saved_user.id,
            "username": saved_user.username,
            "email": saved_user.email,
            "created_at": saved_user.created_at
        }

    def get_user(self, user_id: int) -> Optional[dict]:
        """获取用户信息用例"""
        # 1. 先查缓存
        cache_key = f"user:{user_id}"
        cached = self._cache.get(cache_key)
        if cached:
            self._logger.info(f"User {user_id} found in cache")
            return {
                "id": cached.id,
                "username": cached.username,
                "email": cached.email
            }

        # 2. 查数据库
        user = self._user_repo.find_by_id(user_id)
        if user:
            # 3. 更新缓存
            self._cache.set(cache_key, user)
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }

        return None

    def list_users(self, page: int = 1, page_size: int = 10) -> dict:
        """列出用户用例"""
        skip = (page - 1) * page_size
        users = self._user_repo.find_all(skip=skip, limit=page_size)

        return {
            "users": [
                {"id": u.id, "username": u.username, "email": u.email}
                for u in users
            ],
            "page": page,
            "page_size": page_size,
            "total": len(self._user_repo._users)
        }


# ==================== API网关层 ====================

class RateLimiter:
    """限流器"""
    def __init__(self, max_requests: int = 100, window: int = 60):
        self._max_requests = max_requests
        self._window = window
        self._requests: Dict[str, List[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self._requests:
            self._requests[client_id] = []

        # 清理过期请求
        self._requests[client_id] = [
            req_time for req_time in self._requests[client_id]
            if now - req_time < self._window
        ]

        if len(self._requests[client_id]) >= self._max_requests:
            return False

        self._requests[client_id].append(now)
        return True


class AuthMiddleware:
    """认证中间件"""
    def __init__(self, logger: Logger):
        self._logger = logger
        self._tokens: Dict[str, int] = {}  # token -> user_id

    def generate_token(self, user_id: int) -> str:
        token = hashlib.sha256(f"{user_id}:{time.time()}".encode()).hexdigest()
        self._tokens[token] = user_id
        return token

    def validate_token(self, token: str) -> Optional[int]:
        return self._tokens.get(token)


class ApiGateway:
    """API网关"""

    def __init__(
        self,
        user_app_service: UserApplicationService,
        rate_limiter: RateLimiter,
        auth: AuthMiddleware,
        logger: Logger
    ):
        self._user_service = user_app_service
        self._rate_limiter = rate_limiter
        self._auth = auth
        self._logger = logger

    def _check_rate_limit(self, client_id: str):
        if not self._rate_limiter.is_allowed(client_id):
            raise PermissionError("请求过于频繁，请稍后再试")

    def register(self, request: dict, client_id: str) -> dict:
        """注册端点"""
        self._check_rate_limit(client_id)

        try:
            result = self._user_service.register_user(
                username=request["username"],
                email=request["email"],
                password=request["password"]
            )
            return {"success": True, "data": result}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def get_user(self, user_id: int, client_id: str, token: str = None) -> dict:
        """获取用户端点"""
        self._check_rate_limit(client_id)

        # 可选：验证token
        if token:
            auth_user = self._auth.validate_token(token)
            if not auth_user:
                return {"success": False, "error": "无效的认证令牌"}

        result = self._user_service.get_user(user_id)
        if result:
            return {"success": True, "data": result}
        return {"success": False, "error": "用户不存在"}

    def list_users(self, client_id: str, page: int = 1, page_size: int = 10) -> dict:
        """列出用户端点"""
        self._check_rate_limit(client_id)

        result = self._user_service.list_users(page, page_size)
        return {"success": True, "data": result}


# ==================== 应用组装 ====================

def create_application():
    """应用组装 - 依赖注入"""
    # 基础设施
    logger = Logger()
    cache = CacheService()
    event_bus = EventBus()

    # 数据访问
    user_repo = UserRepository(logger)

    # 领域服务
    domain_service = UserDomainService(logger)

    # 应用服务
    app_service = UserApplicationService(
        user_repo=user_repo,
        domain_service=domain_service,
        cache=cache,
        event_bus=event_bus,
        logger=logger
    )

    # API网关
    rate_limiter = RateLimiter(max_requests=10, window=60)
    auth = AuthMiddleware(logger)
    gateway = ApiGateway(app_service, rate_limiter, auth, logger)

    return gateway


# ==================== 运行示例 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("N层架构演示 - 用户管理系统")
    print("=" * 60)

    app = create_application()
    client_id = "client_001"

    # 注册用户
    print("\n1. 注册用户:")
    register_result = app.register({
        "username": "john_doe",
        "email": "john@example.com",
        "password": "Password123"
    }, client_id)
    print(json.dumps(register_result, indent=2, ensure_ascii=False))

    # 再注册一个
    register_result2 = app.register({
        "username": "jane_doe",
        "email": "jane@example.com",
        "password": "SecurePass456"
    }, client_id)
    print(json.dumps(register_result2, indent=2, ensure_ascii=False))

    # 获取用户
    print("\n2. 获取用户:")
    user_result = app.get_user(1, client_id)
    print(json.dumps(user_result, indent=2, ensure_ascii=False))

    # 再次获取（从缓存）
    print("\n3. 再次获取用户（从缓存）:")
    user_result2 = app.get_user(1, client_id)
    print(json.dumps(user_result2, indent=2, ensure_ascii=False))

    # 列出用户
    print("\n4. 列出所有用户:")
    list_result = app.list_users(client_id)
    print(json.dumps(list_result, indent=2, ensure_ascii=False))

    # 测试限流
    print("\n5. 测试限流:")
    for i in range(15):
        try:
            result = app.get_user(1, client_id)
            print(f"请求 {i+1}: 成功")
        except PermissionError as e:
            print(f"请求 {i+1}: {e}")
            break
```

---

### 1.3 洋葱架构（Onion Architecture）

#### 概念定义

洋葱架构由Jeffrey Palermo提出，核心思想是**依赖向内指向领域核心**：

- **领域核心（Domain Core）**：实体、值对象、领域服务
- **应用核心（Application Core）**：用例、接口定义
- **基础设施层（Infrastructure）**：数据库、外部服务
- **UI层（Presentation）**：用户界面

依赖规则：**外层依赖内层，内层不依赖外层**

#### 架构图

```
                    ┌─────────────┐
                    │   UI/API    │  ← 外层（依赖内层）
                    │   表示层     │
                    ├─────────────┤
                    │  Application│
                    │  应用服务层   │
                    ├─────────────┤
                    │   Domain    │
                    │   领域层     │  ← 核心（无外部依赖）
                    │ ┌─────────┐ │
                    │ │ Entities│ │
                    │ │Services │ │
                    │ └─────────┘ │
                    └─────────────┘

        依赖方向: 外层 → 内层（向内指向核心）
```

#### Python实现

```python
"""
洋葱架构实现 - 博客系统
核心原则：依赖向内指向领域核心
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Protocol
from uuid import uuid4, UUID


# ==================== 领域核心层（最内层）====================
# 这一层没有任何外部依赖，只包含纯业务逻辑

@dataclass(frozen=True)
class PostId:
    """文章ID - 值对象"""
    value: UUID

    @classmethod
    def generate(cls) -> "PostId":
        return cls(value=uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class Post:
    """文章实体 - 领域核心"""
    id: PostId
    title: str
    content: str
    author_id: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_published: bool = False

    def publish(self) -> None:
        """发布文章 - 领域行为"""
        if not self.title or len(self.title) < 3:
            raise ValueError("标题至少需要3个字符")
        if not self.content or len(self.content) < 10:
            raise ValueError("内容至少需要10个字符")
        self.is_published = True
        self.updated_at = datetime.now()

    def update_content(self, new_title: str, new_content: str) -> None:
        """更新内容 - 领域行为"""
        self.title = new_title
        self.content = new_content
        self.updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        """添加标签 - 领域行为"""
        if tag not in self.tags:
            self.tags.append(tag)


class PostDomainService:
    """文章领域服务 - 处理跨实体的业务逻辑"""

    def create_post(self, title: str, content: str, author_id: str) -> Post:
        """创建文章 - 工厂方法"""
        return Post(
            id=PostId.generate(),
            title=title,
            content=content,
            author_id=author_id
        )

    def validate_post(self, post: Post) -> List[str]:
        """验证文章 - 返回错误列表"""
        errors = []
        if len(post.title) > 100:
            errors.append("标题不能超过100字符")
        if len(post.content) > 50000:
            errors.append("内容不能超过50000字符")
        return errors


# ==================== 应用核心层（接口定义）====================
# 这一层定义端口（接口），但不实现

class IPostRepository(ABC):
    """文章仓储接口 - 端口"""

    @abstractmethod
    def get_by_id(self, post_id: PostId) -> Optional[Post]:
        pass

    @abstractmethod
    def get_all(self, published_only: bool = False) -> List[Post]:
        pass

    @abstractmethod
    def save(self, post: Post) -> None:
        pass

    @abstractmethod
    def delete(self, post_id: PostId) -> bool:
        pass


class IEventPublisher(ABC):
    """事件发布器接口 - 端口"""

    @abstractmethod
    def publish(self, event_type: str, event_data: dict) -> None:
        pass


class ICacheService(ABC):
    """缓存服务接口 - 端口"""

    @abstractmethod
    def get(self, key: str) -> Optional[any]:
        pass

    @abstractmethod
    def set(self, key: str, value: any, ttl: int = 300) -> None:
        pass


# ==================== 应用服务层（用例编排）====================

@dataclass
class CreatePostCommand:
    """创建文章命令"""
    title: str
    content: str
    author_id: str
    tags: List[str] = field(default_factory=list)


@dataclass
class PostDto:
    """文章数据传输对象"""
    id: str
    title: str
    content: str
    author_id: str
    tags: List[str]
    is_published: bool
    created_at: str

    @classmethod
    def from_entity(cls, post: Post) -> "PostDto":
        return cls(
            id=str(post.id),
            title=post.title,
            content=post.content[:100] + "..." if len(post.content) > 100 else post.content,
            author_id=post.author_id,
            tags=post.tags,
            is_published=post.is_published,
            created_at=post.created_at.isoformat()
        )


class PostApplicationService:
    """文章应用服务 - 用例编排"""

    def __init__(
        self,
        post_repo: IPostRepository,
        event_publisher: IEventPublisher,
        cache: ICacheService,
        domain_service: PostDomainService
    ):
        self._post_repo = post_repo
        self._event_publisher = event_publisher
        self._cache = cache
        self._domain_service = domain_service

    def create_post(self, command: CreatePostCommand) -> PostDto:
        """创建文章用例"""
        # 1. 创建领域实体
        post = self._domain_service.create_post(
            title=command.title,
            content=command.content,
            author_id=command.author_id
        )

        # 2. 添加标签
        for tag in command.tags:
            post.add_tag(tag)

        # 3. 验证
        errors = self._domain_service.validate_post(post)
        if errors:
            raise ValueError(f"验证失败: {', '.join(errors)}")

        # 4. 保存
        self._post_repo.save(post)

        # 5. 发布事件
        self._event_publisher.publish("post.created", {
            "post_id": str(post.id),
            "title": post.title,
            "author_id": post.author_id
        })

        # 6. 更新缓存
        self._cache.set(f"post:{post.id}", post)

        return PostDto.from_entity(post)

    def publish_post(self, post_id: str) -> PostDto:
        """发布文章用例"""
        # 1. 获取文章
        post = self._post_repo.get_by_id(PostId(UUID(post_id)))
        if not post:
            raise ValueError("文章不存在")

        # 2. 执行业务操作
        post.publish()

        # 3. 保存
        self._post_repo.save(post)

        # 4. 发布事件
        self._event_publisher.publish("post.published", {
            "post_id": str(post.id),
            "title": post.title
        })

        # 5. 更新缓存
        self._cache.set(f"post:{post.id}", post)

        return PostDto.from_entity(post)

    def get_post(self, post_id: str) -> Optional[PostDto]:
        """获取文章用例"""
        # 1. 尝试从缓存获取
        cache_key = f"post:{post_id}"
        cached = self._cache.get(cache_key)
        if cached:
            return PostDto.from_entity(cached)

        # 2. 从仓储获取
        post = self._post_repo.get_by_id(PostId(UUID(post_id)))
        if post:
            # 3. 更新缓存
            self._cache.set(cache_key, post)
            return PostDto.from_entity(post)

        return None

    def list_posts(self, published_only: bool = True) -> List[PostDto]:
        """列出文章用例"""
        posts = self._post_repo.get_all(published_only=published_only)
        return [PostDto.from_entity(p) for p in posts]


# ==================== 基础设施层（适配器实现）====================
# 这一层实现领域层定义的接口

class InMemoryPostRepository(IPostRepository):
    """内存文章仓储 - 适配器"""

    def __init__(self):
        self._posts: dict[str, Post] = {}

    def get_by_id(self, post_id: PostId) -> Optional[Post]:
        return self._posts.get(str(post_id))

    def get_all(self, published_only: bool = False) -> List[Post]:
        posts = list(self._posts.values())
        if published_only:
            posts = [p for p in posts if p.is_published]
        return posts

    def save(self, post: Post) -> None:
        self._posts[str(post.id)] = post

    def delete(self, post_id: PostId) -> bool:
        if str(post_id) in self._posts:
            del self._posts[str(post_id)]
            return True
        return False


class ConsoleEventPublisher(IEventPublisher):
    """控制台事件发布器 - 适配器"""

    def publish(self, event_type: str, event_data: dict) -> None:
        print(f"[EVENT] {event_type}: {event_data}")


class InMemoryCacheService(ICacheService):
    """内存缓存服务 - 适配器"""

    def __init__(self):
        self._cache: dict = {}

    def get(self, key: str) -> Optional[any]:
        return self._cache.get(key)

    def set(self, key: str, value: any, ttl: int = 300) -> None:
        self._cache[key] = value


# ==================== UI层（最外层）====================

class PostController:
    """文章控制器 - UI层"""

    def __init__(self, app_service: PostApplicationService):
        self._app_service = app_service

    def create(self, request: dict) -> dict:
        """处理创建请求"""
        try:
            command = CreatePostCommand(
                title=request["title"],
                content=request["content"],
                author_id=request["author_id"],
                tags=request.get("tags", [])
            )
            result = self._app_service.create_post(command)
            return {"success": True, "data": result}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def publish(self, post_id: str) -> dict:
        """处理发布请求"""
        try:
            result = self._app_service.publish_post(post_id)
            return {"success": True, "data": result}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def get(self, post_id: str) -> dict:
        """处理获取请求"""
        result = self._app_service.get_post(post_id)
        if result:
            return {"success": True, "data": result}
        return {"success": False, "error": "文章不存在"}

    def list(self, published_only: bool = True) -> dict:
        """处理列表请求"""
        result = self._app_service.list_posts(published_only)
        return {"success": True, "data": result}


# ==================== 依赖注入容器 ====================

class ApplicationContainer:
    """应用容器 - 组装所有依赖"""

    @staticmethod
    def create_application():
        # 基础设施（适配器）
        post_repo = InMemoryPostRepository()
        event_publisher = ConsoleEventPublisher()
        cache = InMemoryCacheService()

        # 领域服务
        domain_service = PostDomainService()

        # 应用服务
        app_service = PostApplicationService(
            post_repo=post_repo,
            event_publisher=event_publisher,
            cache=cache,
            domain_service=domain_service
        )

        # UI
        controller = PostController(app_service)

        return controller


# ==================== 运行示例 ====================

if __name__ == "__main__":
    import json

    print("=" * 60)
    print("洋葱架构演示 - 博客系统")
    print("=" * 60)

    app = ApplicationContainer.create_application()

    # 创建文章
    print("\n1. 创建文章:")
    create_result = app.create({
        "title": "洋葱架构详解",
        "content": "洋葱架构是一种软件架构模式，它将应用程序组织成同心圆层..." * 5,
        "author_id": "author_001",
        "tags": ["architecture", "ddd"]
    })
    print(json.dumps(create_result, indent=2, default=str, ensure_ascii=False))

    post_id = create_result["data"]["id"] if create_result["success"] else None

    # 创建另一篇文章
    print("\n2. 创建另一篇文章:")
    create_result2 = app.create({
        "title": "领域驱动设计入门",
        "content": "领域驱动设计是一种软件开发方法..." * 5,
        "author_id": "author_002",
        "tags": ["ddd", "design"]
    })
    print(json.dumps(create_result2, indent=2, default=str, ensure_ascii=False))

    # 发布文章
    if post_id:
        print("\n3. 发布文章:")
        publish_result = app.publish(post_id)
        print(json.dumps(publish_result, indent=2, default=str, ensure_ascii=False))

    # 获取文章
    if post_id:
        print("\n4. 获取文章:")
        get_result = app.get(post_id)
        print(json.dumps(get_result, indent=2, default=str, ensure_ascii=False))

    # 列出已发布文章
    print("\n5. 列出已发布文章:")
    list_result = app.list(published_only=True)
    print(json.dumps(list_result, indent=2, default=str, ensure_ascii=False))
```

---

### 1.4 整洁架构（Clean Architecture）

#### 概念定义

整洁架构由Robert C. Martin（Uncle Bob）提出，与洋葱架构类似但更加强调：

- **实体（Entities）**：企业级业务规则
- **用例（Use Cases）**：应用特定的业务规则
- **接口适配器（Interface Adapters）**：数据转换
- **框架与驱动（Frameworks & Drivers）**：外部工具

依赖规则：**源代码依赖只能向内指向高层策略**

#### 架构图

```
                    ┌─────────────────────────┐
                    │   Frameworks & Drivers  │
                    │   框架与驱动层           │
                    │  (Web, DB, UI, External)│
                    ├─────────────────────────┤
                    │   Interface Adapters    │
                    │   接口适配器层           │
                    │ (Controllers, Presenters│
                    │   Gateways)             │
                    ├─────────────────────────┤
                    │     Use Cases           │
                    │     用例层              │
                    │  (Application Business  │
                    │   Rules)                │
                    ├─────────────────────────┤
                    │       Entities          │
                    │       实体层            │
                    │   (Enterprise Business  │
                    │    Rules)               │
                    └─────────────────────────┘

        依赖规则: 外层只能依赖内层，内层不知道外层存在
```

#### Python实现

```python
"""
整洁架构实现 - 电商支付系统
核心原则：依赖向内指向高层策略
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import List, Optional, Dict, Callable
from uuid import uuid4, UUID
import json


# ==================== 实体层（最内层 - 企业级业务规则）====================

class PaymentStatus(Enum):
    """支付状态"""
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()
    REFUNDED = auto()


@dataclass(frozen=True)
class Money:
    """金额值对象 - 不可变"""
    amount: Decimal
    currency: str = "CNY"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("金额不能为负数")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("货币类型不匹配")
        return Money(self.amount + other.amount, self.currency)

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"


@dataclass
class Payment:
    """支付实体 - 企业级业务规则"""
    id: UUID
    order_id: str
    amount: Money
    payer_id: str
    payee_id: str
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None

    def process(self) -> None:
        """处理支付 - 业务规则"""
        if self.status != PaymentStatus.PENDING:
            raise ValueError("只能处理待支付状态的订单")
        self.status = PaymentStatus.PROCESSING

    def complete(self) -> None:
        """完成支付 - 业务规则"""
        if self.status != PaymentStatus.PROCESSING:
            raise ValueError("只能完成处理中的支付")
        self.status = PaymentStatus.COMPLETED
        self.completed_at = datetime.now()

    def fail(self, reason: str) -> None:
        """支付失败 - 业务规则"""
        if self.status not in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]:
            raise ValueError("当前状态不能标记为失败")
        self.status = PaymentStatus.FAILED
        self.failure_reason = reason

    def refund(self) -> None:
        """退款 - 业务规则"""
        if self.status != PaymentStatus.COMPLETED:
            raise ValueError("只能对已完成的支付进行退款")
        self.status = PaymentStatus.REFUNDED


class PaymentEntityRules:
    """支付实体规则 - 纯业务逻辑，无外部依赖"""

    MAX_PAYMENT_AMOUNT = Decimal("1000000")  # 最大支付金额
    MIN_PAYMENT_AMOUNT = Decimal("0.01")     # 最小支付金额

    @classmethod
    def validate_payment_amount(cls, amount: Money) -> List[str]:
        """验证支付金额"""
        errors = []
        if amount.amount > cls.MAX_PAYMENT_AMOUNT:
            errors.append(f"支付金额不能超过 {cls.MAX_PAYMENT_AMOUNT}")
        if amount.amount < cls.MIN_PAYMENT_AMOUNT:
            errors.append(f"支付金额不能少于 {cls.MIN_PAYMENT_AMOUNT}")
        return errors

    @classmethod
    def can_process(cls, payment: Payment) -> bool:
        """判断是否可以处理支付"""
        return payment.status == PaymentStatus.PENDING


# ==================== 用例层（应用特定的业务规则）====================

@dataclass
class ProcessPaymentInput:
    """处理支付输入"""
    order_id: str
    amount: Decimal
    currency: str
    payer_id: str
    payee_id: str
    payment_method: str


@dataclass
class ProcessPaymentOutput:
    """处理支付输出"""
    payment_id: str
    status: str
    amount: str
    message: str


class IPaymentRepository(ABC):
    """支付仓储接口"""

    @abstractmethod
    def find_by_id(self, payment_id: UUID) -> Optional[Payment]:
        pass

    @abstractmethod
    def save(self, payment: Payment) -> None:
        pass


class IPaymentGateway(ABC):
    """支付网关接口"""

    @abstractmethod
    def process_payment(self, payment: Payment) -> Dict:
        """处理支付，返回结果"""
        pass


class IEventDispatcher(ABC):
    """事件分发器接口"""

    @abstractmethod
    def dispatch(self, event_name: str, payload: dict) -> None:
        pass


class ProcessPaymentUseCase:
    """处理支付用例 - 应用特定的业务规则"""

    def __init__(
        self,
        payment_repo: IPaymentRepository,
        payment_gateway: IPaymentGateway,
        event_dispatcher: IEventDispatcher
    ):
        self._payment_repo = payment_repo
        self._payment_gateway = payment_gateway
        self._event_dispatcher = event_dispatcher

    def execute(self, input_data: ProcessPaymentInput) -> ProcessPaymentOutput:
        """执行用例"""
        # 1. 创建金额对象
        amount = Money(input_data.amount, input_data.currency)

        # 2. 验证金额（调用实体层规则）
        errors = PaymentEntityRules.validate_payment_amount(amount)
        if errors:
            return ProcessPaymentOutput(
                payment_id="",
                status="failed",
                amount=str(amount),
                message="; ".join(errors)
            )

        # 3. 创建支付实体
        payment = Payment(
            id=uuid4(),
            order_id=input_data.order_id,
            amount=amount,
            payer_id=input_data.payer_id,
            payee_id=input_data.payee_id
        )

        # 4. 保存初始状态
        self._payment_repo.save(payment)

        # 5. 处理支付
        payment.process()
        self._payment_repo.save(payment)

        # 6. 调用支付网关
        try:
            gateway_result = self._payment_gateway.process_payment(payment)

            if gateway_result.get("success"):
                payment.complete()
                self._payment_repo.save(payment)

                # 发布成功事件
                self._event_dispatcher.dispatch("payment.completed", {
                    "payment_id": str(payment.id),
                    "order_id": payment.order_id,
                    "amount": str(payment.amount)
                })

                return ProcessPaymentOutput(
                    payment_id=str(payment.id),
                    status="completed",
                    amount=str(payment.amount),
                    message="支付成功"
                )
            else:
                payment.fail(gateway_result.get("error", "支付失败"))
                self._payment_repo.save(payment)

                return ProcessPaymentOutput(
                    payment_id=str(payment.id),
                    status="failed",
                    amount=str(payment.amount),
                    message=gateway_result.get("error", "支付失败")
                )

        except Exception as e:
            payment.fail(str(e))
            self._payment_repo.save(payment)

            return ProcessPaymentOutput(
                payment_id=str(payment.id),
                status="failed",
                amount=str(payment.amount),
                message=f"系统错误: {str(e)}"
            )


# ==================== 接口适配器层 ====================

class PaymentRequestModel:
    """支付请求模型"""
    def __init__(self, data: dict):
        self.order_id = data.get("order_id")
        self.amount = Decimal(data.get("amount", "0"))
        self.currency = data.get("currency", "CNY")
        self.payer_id = data.get("payer_id")
        self.payee_id = data.get("payee_id")
        self.payment_method = data.get("payment_method", "alipay")

    def to_use_case_input(self) -> ProcessPaymentInput:
        return ProcessPaymentInput(
            order_id=self.order_id,
            amount=self.amount,
            currency=self.currency,
            payer_id=self.payer_id,
            payee_id=self.payee_id,
            payment_method=self.payment_method
        )


class PaymentPresenter:
    """支付展示器 - 格式化输出"""

    @staticmethod
    def present(output: ProcessPaymentOutput) -> dict:
        return {
            "success": output.status == "completed",
            "payment_id": output.payment_id,
            "status": output.status,
            "amount": output.amount,
            "message": output.message
        }


class PaymentController:
    """支付控制器"""

    def __init__(self, process_use_case: ProcessPaymentUseCase):
        self._process_use_case = process_use_case

    def process_payment(self, request_data: dict) -> dict:
        """处理支付请求"""
        try:
            # 1. 转换请求数据
            request_model = PaymentRequestModel(request_data)
            use_case_input = request_model.to_use_case_input()

            # 2. 执行用例
            output = self._process_use_case.execute(use_case_input)

            # 3. 格式化响应
            return PaymentPresenter.present(output)

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# ==================== 框架与驱动层（最外层）====================

class InMemoryPaymentRepository(IPaymentRepository):
    """内存支付仓储 - 数据库适配器"""

    def __init__(self):
        self._payments: Dict[UUID, Payment] = {}

    def find_by_id(self, payment_id: UUID) -> Optional[Payment]:
        return self._payments.get(payment_id)

    def save(self, payment: Payment) -> None:
        self._payments[payment.id] = payment
        print(f"[DB] Payment saved: {payment.id} - {payment.status.name}")


class MockPaymentGateway(IPaymentGateway):
    """模拟支付网关 - 外部服务适配器"""

    def __init__(self, success_rate: float = 0.8):
        self._success_rate = success_rate
        import random
        self._random = random

    def process_payment(self, payment: Payment) -> Dict:
        """模拟支付处理"""
        print(f"[GATEWAY] Processing payment: {payment.id} - {payment.amount}")

        # 模拟处理延迟
        import time
        time.sleep(0.1)

        # 模拟成功率
        if self._random.random() < self._success_rate:
            return {"success": True, "transaction_id": str(uuid4())}
        else:
            return {"success": False, "error": "余额不足"}


class ConsoleEventDispatcher(IEventDispatcher):
    """控制台事件分发器 - 消息队列适配器"""

    def dispatch(self, event_name: str, payload: dict) -> None:
        print(f"[EVENT] {event_name}: {json.dumps(payload, ensure_ascii=False)}")


# ==================== 依赖注入与组装 ====================

class CleanArchitectureContainer:
    """整洁架构容器"""

    @staticmethod
    def create_application():
        # 框架与驱动层（最外层）
        payment_repo = InMemoryPaymentRepository()
        payment_gateway = MockPaymentGateway(success_rate=0.9)
        event_dispatcher = ConsoleEventDispatcher()

        # 用例层
        process_use_case = ProcessPaymentUseCase(
            payment_repo=payment_repo,
            payment_gateway=payment_gateway,
            event_dispatcher=event_dispatcher
        )

        # 接口适配器层
        controller = PaymentController(process_use_case)

        return controller


# ==================== 运行示例 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("整洁架构演示 - 电商支付系统")
    print("=" * 60)

    app = CleanArchitectureContainer.create_application()

    # 测试支付
    print("\n1. 正常支付:")
    result1 = app.process_payment({
        "order_id": "ORDER_001",
        "amount": "299.99",
        "currency": "CNY",
        "payer_id": "USER_001",
        "payee_id": "MERCHANT_001",
        "payment_method": "alipay"
    })
    print(json.dumps(result1, indent=2, ensure_ascii=False))

    print("\n2. 大额支付:")
    result2 = app.process_payment({
        "order_id": "ORDER_002",
        "amount": "2000000",
        "currency": "CNY",
        "payer_id": "USER_002",
        "payee_id": "MERCHANT_002",
        "payment_method": "wechat"
    })
    print(json.dumps(result2, indent=2, ensure_ascii=False))

    print("\n3. 小额支付:")
    result3 = app.process_payment({
        "order_id": "ORDER_003",
        "amount": "0.001",
        "currency": "CNY",
        "payer_id": "USER_003",
        "payee_id": "MERCHANT_003",
        "payment_method": "alipay"
    })
    print(json.dumps(result3, indent=2, ensure_ascii=False))

    # 多次支付测试成功率
    print("\n4. 多次支付测试:")
    success_count = 0
    for i in range(5):
        result = app.process_payment({
            "order_id": f"ORDER_{100+i}",
            "amount": "100.00",
            "currency": "CNY",
            "payer_id": f"USER_{100+i}",
            "payee_id": "MERCHANT_TEST",
            "payment_method": "alipay"
        })
        if result["success"]:
            success_count += 1
        print(f"支付 {i+1}: {'成功' if result['success'] else '失败'}")

    print(f"\n成功率: {success_count}/5")
```

#### 分层架构对比

| 特性 | 三层架构 | N层架构 | 洋葱架构 | 整洁架构 |
|------|----------|---------|----------|----------|
| 层数 | 3层 | N层（可扩展） | 4层 | 4层 |
| 依赖方向 | 单向 | 单向 | 向内指向核心 | 向内指向核心 |
| 领域核心 | 业务层 | 领域服务层 | 最内层 | 实体层 |
| 外部依赖 | 数据层 | 基础设施层 | 适配器 | 框架驱动 |
| 适用场景 | 简单应用 | 企业应用 | 复杂领域 | 复杂领域 |
| 测试难度 | 中等 | 中等 | 容易 | 容易 |
| 演进灵活性 | 低 | 中 | 高 | 高 |

---


## 第二部分：微服务架构

### 2.1 服务拆分原则

#### 概念定义

微服务架构将单体应用拆分为一组小型、独立部署的服务，每个服务：

- **独立开发**：不同团队可并行开发
- **独立部署**：服务可独立发布
- **独立扩展**：根据负载单独扩缩容
- **独立技术栈**：可选择最适合的技术

#### 拆分策略

##### 按业务能力拆分（Business Capability）

```
┌─────────────────────────────────────────────────────────┐
│                    电商平台                              │
├─────────────┬─────────────┬─────────────┬───────────────┤
│   用户服务   │   商品服务   │   订单服务   │   支付服务     │
│  (User)     │  (Product)  │  (Order)    │  (Payment)    │
├─────────────┼─────────────┼─────────────┼───────────────┤
│ • 用户注册   │ • 商品管理   │ • 订单创建   │ • 支付处理     │
│ • 用户登录   │ • 库存管理   │ • 订单查询   │ • 退款处理     │
│ • 用户信息   │ • 商品搜索   │ • 订单状态   │ • 对账查询     │
│ • 权限管理   │ • 分类管理   │ • 订单取消   │ • 支付回调     │
└─────────────┴─────────────┴─────────────┴───────────────┘
```

##### 按领域边界拆分（Domain Boundary）

```
┌─────────────────────────────────────────────────────────┐
│                    领域边界划分                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐      ┌─────────────┐                 │
│   │  用户领域   │◄────►│  订单领域   │                 │
│   │  (User BC)  │      │ (Order BC)  │                 │
│   └──────┬──────┘      └──────┬──────┘                 │
│          │                    │                        │
│          ▼                    ▼                        │
│   ┌─────────────┐      ┌─────────────┐                 │
│   │  商品领域   │◄────►│  支付领域   │                 │
│   │(Product BC) │      │(Payment BC) │                 │
│   └─────────────┘      └─────────────┘                 │
│                                                         │
│   每个领域内部高内聚，领域之间低耦合                      │
└─────────────────────────────────────────────────────────┘
```

#### 拆分原则（AKF扩展立方）

```
                    X轴：水平复制
                         │
                         ▼
              ┌─────────────────────┐
              │  负载均衡器          │
              └──────────┬──────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ 服务A-1 │    │ 服务A-2 │    │ 服务A-3 │
    └─────────┘    └─────────┘    └─────────┘

    Y轴：功能分解（按业务拆分）

    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ 用户服务 │    │ 订单服务 │    │ 商品服务 │
    └─────────┘    └─────────┘    └─────────┘

    Z轴：数据分区（按用户ID分片）

    用户ID % 3 = 0 ──► 数据库分片0
    用户ID % 3 = 1 ──► 数据库分片1
    用户ID % 3 = 2 ──► 数据库分片2
```

#### Python实现 - 服务拆分示例

```python
"""
微服务拆分示例 - 电商平台
演示用户服务、商品服务、订单服务的独立实现
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Set
from enum import Enum, auto
import json
import uuid


# ==================== 共享领域模型（Shared Kernel）====================

class ServiceType(Enum):
    """服务类型"""
    USER = "user-service"
    PRODUCT = "product-service"
    ORDER = "order-service"
    PAYMENT = "payment-service"


@dataclass(frozen=True)
class ServiceEndpoint:
    """服务端点"""
    service_type: ServiceType
    host: str
    port: int

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


# ==================== 用户服务（User Service）====================

@dataclass
class User:
    """用户实体"""
    id: str
    username: str
    email: str
    phone: str
    created_at: str
    is_active: bool = True


class UserRepository:
    """用户仓储"""

    def __init__(self):
        self._users: Dict[str, User] = {}
        # 初始化测试数据
        self._init_test_data()

    def _init_test_data(self):
        test_users = [
            User("U001", "张三", "zhangsan@example.com", "13800138001", datetime.now().isoformat()),
            User("U002", "李四", "lisi@example.com", "13800138002", datetime.now().isoformat()),
            User("U003", "王五", "wangwu@example.com", "13800138003", datetime.now().isoformat()),
        ]
        for user in test_users:
            self._users[user.id] = user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def find_all(self) -> List[User]:
        return list(self._users.values())

    def save(self, user: User) -> None:
        self._users[user.id] = user


class UserService:
    """用户服务 - 业务逻辑"""

    def __init__(self, repository: UserRepository):
        self._repo = repository

    def get_user(self, user_id: str) -> Optional[dict]:
        """获取用户信息"""
        user = self._repo.find_by_id(user_id)
        return asdict(user) if user else None

    def validate_user(self, user_id: str) -> bool:
        """验证用户是否存在且有效"""
        user = self._repo.find_by_id(user_id)
        return user is not None and user.is_active

    def get_user_profile(self, user_id: str) -> Optional[dict]:
        """获取用户完整资料"""
        user = self._repo.find_by_id(user_id)
        if not user:
            return None

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "member_level": self._calculate_member_level(user_id),
            "created_at": user.created_at
        }

    def _calculate_member_level(self, user_id: str) -> str:
        """计算会员等级"""
        # 模拟会员等级计算
        levels = ["普通会员", "银卡会员", "金卡会员", "钻石会员"]
        return levels[hash(user_id) % len(levels)]


# ==================== 商品服务（Product Service）====================

@dataclass
class Product:
    """商品实体"""
    id: str
    name: str
    description: str
    price: Decimal
    stock: int
    category: str
    is_available: bool = True


class ProductRepository:
    """商品仓储"""

    def __init__(self):
        self._products: Dict[str, Product] = {}
        self._init_test_data()

    def _init_test_data(self):
        test_products = [
            Product("P001", "iPhone 15", "最新款苹果手机", Decimal("6999.00"), 100, "电子产品"),
            Product("P002", "MacBook Pro", "专业级笔记本电脑", Decimal("14999.00"), 50, "电子产品"),
            Product("P003", "AirPods Pro", "降噪耳机", Decimal("1999.00"), 200, "电子产品"),
            Product("P004", "Nike运动鞋", "专业跑步鞋", Decimal("899.00"), 150, "运动用品"),
        ]
        for p in test_products:
            self._products[p.id] = p

    def find_by_id(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def find_by_category(self, category: str) -> List[Product]:
        return [p for p in self._products.values() if p.category == category]

    def update_stock(self, product_id: str, quantity: int) -> bool:
        product = self._products.get(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
            return True
        return False


class ProductService:
    """商品服务 - 业务逻辑"""

    def __init__(self, repository: ProductRepository):
        self._repo = repository

    def get_product(self, product_id: str) -> Optional[dict]:
        """获取商品信息"""
        product = self._repo.find_by_id(product_id)
        if not product:
            return None
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "stock": product.stock,
            "category": product.category,
            "is_available": product.is_available and product.stock > 0
        }

    def check_stock(self, product_id: str, quantity: int) -> dict:
        """检查库存"""
        product = self._repo.find_by_id(product_id)
        if not product:
            return {"available": False, "reason": "商品不存在"}

        if product.stock < quantity:
            return {
                "available": False,
                "reason": f"库存不足，当前库存: {product.stock}",
                "current_stock": product.stock
            }

        return {"available": True, "current_stock": product.stock}

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """预留库存"""
        return self._repo.update_stock(product_id, quantity)

    def search_products(self, keyword: str, category: str = None) -> List[dict]:
        """搜索商品"""
        results = []
        for product in self._repo._products.values():
            if keyword.lower() in product.name.lower():
                if category is None or product.category == category:
                    results.append(self.get_product(product.id))
        return results


# ==================== 订单服务（Order Service）====================

@dataclass
class OrderItem:
    """订单项"""
    product_id: str
    product_name: str
    quantity: int
    unit_price: Decimal


@dataclass
class Order:
    """订单实体"""
    id: str
    user_id: str
    items: List[OrderItem]
    total_amount: Decimal
    status: str  # pending, confirmed, paid, shipped, completed, cancelled
    created_at: str
    shipping_address: str = ""


class OrderRepository:
    """订单仓储"""

    def __init__(self):
        self._orders: Dict[str, Order] = {}

    def find_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def find_by_user(self, user_id: str) -> List[Order]:
        return [o for o in self._orders.values() if o.user_id == user_id]

    def save(self, order: Order) -> None:
        self._orders[order.id] = order


class OrderService:
    """订单服务 - 业务逻辑"""

    def __init__(
        self,
        order_repo: OrderRepository,
        user_service: UserService,
        product_service: ProductService
    ):
        self._order_repo = order_repo
        self._user_service = user_service
        self._product_service = product_service

    def create_order(self, user_id: str, items_data: List[dict], address: str = "") -> dict:
        """创建订单"""
        # 1. 验证用户
        if not self._user_service.validate_user(user_id):
            return {"success": False, "error": "用户不存在或已禁用"}

        # 2. 验证商品和库存
        order_items = []
        total_amount = Decimal("0")

        for item_data in items_data:
            product_id = item_data["product_id"]
            quantity = item_data["quantity"]

            # 检查商品
            product = self._product_service.get_product(product_id)
            if not product:
                return {"success": False, "error": f"商品不存在: {product_id}"}

            # 检查库存
            stock_check = self._product_service.check_stock(product_id, quantity)
            if not stock_check["available"]:
                return {"success": False, "error": f"{product['name']}: {stock_check['reason']}"}

            # 预留库存
            if not self._product_service.reserve_stock(product_id, quantity):
                return {"success": False, "error": f"预留库存失败: {product['name']}"}

            # 创建订单项
            order_items.append(OrderItem(
                product_id=product_id,
                product_name=product["name"],
                quantity=quantity,
                unit_price=Decimal(str(product["price"]))
            ))

            total_amount += Decimal(str(product["price"])) * quantity

        # 3. 创建订单
        order = Order(
            id=f"ORD{uuid.uuid4().hex[:12].upper()}",
            user_id=user_id,
            items=order_items,
            total_amount=total_amount,
            status="pending",
            created_at=datetime.now().isoformat(),
            shipping_address=address
        )

        self._order_repo.save(order)

        return {
            "success": True,
            "order_id": order.id,
            "total_amount": float(total_amount),
            "status": order.status,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price)
                }
                for item in order_items
            ]
        }

    def get_order(self, order_id: str) -> Optional[dict]:
        """获取订单详情"""
        order = self._order_repo.find_by_id(order_id)
        if not order:
            return None

        return {
            "order_id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_amount": float(order.total_amount),
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price)
                }
                for item in order.items
            ]
        }

    def confirm_order(self, order_id: str) -> dict:
        """确认订单"""
        order = self._order_repo.find_by_id(order_id)
        if not order:
            return {"success": False, "error": "订单不存在"}

        if order.status != "pending":
            return {"success": False, "error": f"订单状态为 {order.status}，无法确认"}

        order.status = "confirmed"
        self._order_repo.save(order)

        return {"success": True, "order_id": order_id, "status": order.status}


# ==================== 服务编排器（Service Orchestrator）====================

class ECommerceOrchestrator:
    """电商服务编排器 - 协调多个服务"""

    def __init__(
        self,
        user_service: UserService,
        product_service: ProductService,
        order_service: OrderService
    ):
        self._user_service = user_service
        self._product_service = product_service
        self._order_service = order_service

    def place_order(self, user_id: str, items: List[dict], address: str = "") -> dict:
        """下单流程"""
        print(f"\n[流程] 开始处理用户 {user_id} 的订单...")

        # 1. 获取用户信息
        user = self._user_service.get_user_profile(user_id)
        if not user:
            return {"success": False, "error": "用户不存在"}

        print(f"[流程] 用户信息: {user['username']} ({user['member_level']})")

        # 2. 创建订单
        order_result = self._order_service.create_order(user_id, items, address)

        if not order_result["success"]:
            print(f"[流程] 订单创建失败: {order_result['error']}")
            return order_result

        print(f"[流程] 订单创建成功: {order_result['order_id']}")
        print(f"[流程] 订单金额: ¥{order_result['total_amount']}")

        # 3. 确认订单
        confirm_result = self._order_service.confirm_order(order_result["order_id"])

        print(f"[流程] 订单确认: {'成功' if confirm_result['success'] else '失败'}")

        return {
            "success": True,
            "order_id": order_result["order_id"],
            "total_amount": order_result["total_amount"],
            "user": {
                "id": user["id"],
                "name": user["username"],
                "level": user["member_level"]
            },
            "items": order_result["items"]
        }

    def get_order_details(self, order_id: str) -> dict:
        """获取订单完整详情"""
        order = self._order_service.get_order(order_id)
        if not order:
            return {"success": False, "error": "订单不存在"}

        # 获取用户信息
        user = self._user_service.get_user(order["user_id"])

        # 获取商品详情
        products = []
        for item in order["items"]:
            product = self._product_service.get_product(item["product_id"])
            if product:
                products.append(product)

        return {
            "success": True,
            "order": order,
            "user": user,
            "products": products
        }


# ==================== 运行示例 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("微服务拆分演示 - 电商平台")
    print("=" * 60)

    # 初始化各服务
    user_repo = UserRepository()
    product_repo = ProductRepository()
    order_repo = OrderRepository()

    user_service = UserService(user_repo)
    product_service = ProductService(product_repo)
    order_service = OrderService(order_repo, user_service, product_service)

    # 创建编排器
    orchestrator = ECommerceOrchestrator(user_service, product_service, order_service)

    # 场景1: 正常下单
    print("\n场景1: 正常下单")
    result1 = orchestrator.place_order(
        user_id="U001",
        items=[
            {"product_id": "P001", "quantity": 1},  # iPhone 15
            {"product_id": "P003", "quantity": 2}   # AirPods Pro x2
        ],
        address="北京市朝阳区xxx街道"
    )
    print(json.dumps(result1, indent=2, ensure_ascii=False))

    # 场景2: 库存不足
    print("\n场景2: 库存不足")
    result2 = orchestrator.place_order(
        user_id="U002",
        items=[
            {"product_id": "P001", "quantity": 1000}  # 超库存
        ]
    )
    print(json.dumps(result2, indent=2, ensure_ascii=False))

    # 场景3: 获取订单详情
    if result1["success"]:
        print("\n场景3: 获取订单详情")
        order_details = orchestrator.get_order_details(result1["order_id"])
        print(json.dumps(order_details, indent=2, ensure_ascii=False))
```

---

### 2.2 API网关

#### 概念定义

API网关是微服务架构的入口，提供统一的服务访问点：

- **请求路由**：将请求转发到对应的服务
- **负载均衡**：分发请求到多个服务实例
- **认证授权**：统一的身份验证
- **限流熔断**：保护后端服务
- **协议转换**：HTTP ↔ gRPC 等
- **日志监控**：统一的可观测性

#### 主流API网关对比

| 特性 | Kong | Zuul | Spring Cloud Gateway | Nginx |
|------|------|------|---------------------|-------|
| 语言 | Lua/OpenResty | Java | Java | C |
| 性能 | 高 | 中 | 高 | 极高 |
| 插件生态 | 丰富 | 一般 | 良好 | 丰富 |
| 动态配置 | 支持 | 支持 | 支持 | 需重载 |
| 服务发现 | 支持 | 支持 | 支持 | 需配置 |
| 适用场景 | 大规模 | Spring生态 | Spring生态 | 静态资源 |

#### Python实现 - FastAPI API网关

```python
"""
API网关实现 - 基于FastAPI
功能：路由、认证、限流、日志、熔断
"""

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import hashlib
import json
import time
import random


# ==================== 核心组件 ====================

@dataclass
class ServiceInstance:
    """服务实例"""
    service_name: str
    host: str
    port: int
    weight: int = 1
    healthy: bool = True
    last_heartbeat: float = field(default_factory=time.time)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


class LoadBalancer:
    """负载均衡器"""

    def __init__(self):
        self._instances: Dict[str, List[ServiceInstance]] = {}
        self._round_robin_index: Dict[str, int] = {}

    def register(self, instance: ServiceInstance) -> None:
        """注册服务实例"""
        if instance.service_name not in self._instances:
            self._instances[instance.service_name] = []
            self._round_robin_index[instance.service_name] = 0

        self._instances[instance.service_name].append(instance)
        print(f"[LoadBalancer] 注册服务: {instance.service_name} @ {instance.url}")

    def get_instance(self, service_name: str, strategy: str = "round_robin") -> Optional[ServiceInstance]:
        """获取服务实例"""
        instances = self._instances.get(service_name, [])
        healthy_instances = [i for i in instances if i.healthy]

        if not healthy_instances:
            return None

        if strategy == "round_robin":
            idx = self._round_robin_index.get(service_name, 0)
            instance = healthy_instances[idx % len(healthy_instances)]
            self._round_robin_index[service_name] = (idx + 1) % len(healthy_instances)
            return instance

        elif strategy == "random":
            return random.choice(healthy_instances)

        elif strategy == "weighted":
            # 加权随机
            total_weight = sum(i.weight for i in healthy_instances)
            r = random.randint(1, total_weight)
            current = 0
            for instance in healthy_instances:
                current += instance.weight
                if r <= current:
                    return instance

        return healthy_instances[0]


class RateLimiter:
    """限流器 - 令牌桶算法"""

    def __init__(self, rate: int = 100, capacity: int = 100):
        self._rate = rate  # 每秒产生令牌数
        self._capacity = capacity  # 桶容量
        self._tokens: Dict[str, float] = {}  # 当前令牌数
        self._last_update: Dict[str, float] = {}  # 上次更新时间

    def allow_request(self, key: str) -> bool:
        """是否允许请求"""
        now = time.time()

        if key not in self._tokens:
            self._tokens[key] = self._capacity
            self._last_update[key] = now

        # 计算新增令牌
        elapsed = now - self._last_update[key]
        self._tokens[key] = min(
            self._capacity,
            self._tokens[key] + elapsed * self._rate
        )
        self._last_update[key] = now

        # 消费令牌
        if self._tokens[key] >= 1:
            self._tokens[key] -= 1
            return True

        return False


class CircuitBreaker:
    """熔断器"""

    class State(Enum):
        CLOSED = "closed"      # 正常
        OPEN = "open"          # 熔断
        HALF_OPEN = "half_open"  # 半开

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        half_open_max_calls: int = 3
    ):
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._half_open_max_calls = half_open_max_calls

        self._state: Dict[str, CircuitBreaker.State] = {}
        self._failure_count: Dict[str, int] = {}
        self._last_failure_time: Dict[str, float] = {}
        self._half_open_calls: Dict[str, int] = {}

    def can_execute(self, service_name: str) -> bool:
        """检查是否可以执行"""
        state = self._state.get(service_name, CircuitBreaker.State.CLOSED)

        if state == CircuitBreaker.State.CLOSED:
            return True

        if state == CircuitBreaker.State.OPEN:
            last_failure = self._last_failure_time.get(service_name, 0)
            if time.time() - last_failure >= self._recovery_timeout:
                self._state[service_name] = CircuitBreaker.State.HALF_OPEN
                self._half_open_calls[service_name] = 0
                print(f"[CircuitBreaker] {service_name} 进入半开状态")
                return True
            return False

        if state == CircuitBreaker.State.HALF_OPEN:
            calls = self._half_open_calls.get(service_name, 0)
            if calls < self._half_open_max_calls:
                self._half_open_calls[service_name] = calls + 1
                return True
            return False

        return True

    def record_success(self, service_name: str) -> None:
        """记录成功"""
        state = self._state.get(service_name, CircuitBreaker.State.CLOSED)

        if state == CircuitBreaker.State.HALF_OPEN:
            # 半开状态下成功次数足够，关闭熔断
            self._state[service_name] = CircuitBreaker.State.CLOSED
            self._failure_count[service_name] = 0
            print(f"[CircuitBreaker] {service_name} 熔断器关闭")

        elif state == CircuitBreaker.State.CLOSED:
            self._failure_count[service_name] = 0

    def record_failure(self, service_name: str) -> None:
        """记录失败"""
        state = self._state.get(service_name, CircuitBreaker.State.CLOSED)

        self._failure_count[service_name] = self._failure_count.get(service_name, 0) + 1
        self._last_failure_time[service_name] = time.time()

        if state == CircuitBreaker.State.CLOSED:
            if self._failure_count[service_name] >= self._failure_threshold:
                self._state[service_name] = CircuitBreaker.State.OPEN
                print(f"[CircuitBreaker] {service_name} 熔断器打开")

        elif state == CircuitBreaker.State.HALF_OPEN:
            self._state[service_name] = CircuitBreaker.State.OPEN
            print(f"[CircuitBreaker] {service_name} 半开状态失败，重新打开熔断器")


class AuthManager:
    """认证管理器"""

    def __init__(self):
        self._tokens: Dict[str, Dict] = {}  # token -> user_info
        self._user_tokens: Dict[str, str] = {}  # user_id -> token

    def generate_token(self, user_id: str, roles: List[str] = None) -> str:
        """生成令牌"""
        # 如果用户已有token，先删除
        if user_id in self._user_tokens:
            old_token = self._user_tokens[user_id]
            del self._tokens[old_token]

        token = hashlib.sha256(f"{user_id}:{time.time()}".encode()).hexdigest()
        self._tokens[token] = {
            "user_id": user_id,
            "roles": roles or ["user"],
            "created_at": time.time()
        }
        self._user_tokens[user_id] = token
        return token

    def validate_token(self, token: str) -> Optional[Dict]:
        """验证令牌"""
        return self._tokens.get(token)

    def check_permission(self, token: str, required_role: str) -> bool:
        """检查权限"""
        user_info = self.validate_token(token)
        if not user_info:
            return False
        return required_role in user_info.get("roles", [])


# ==================== API网关核心 ====================

class ApiGateway:
    """API网关核心"""

    def __init__(self):
        self.load_balancer = LoadBalancer()
        self.rate_limiter = RateLimiter(rate=10, capacity=20)
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=10
        )
        self.auth_manager = AuthManager()
        self.routes: Dict[str, Dict] = {}
        self.request_log: List[Dict] = []

    def add_route(self, path: str, service_name: str, auth_required: bool = True) -> None:
        """添加路由规则"""
        self.routes[path] = {
            "service_name": service_name,
            "auth_required": auth_required
        }
        print(f"[Gateway] 添加路由: {path} -> {service_name}")

    async def route_request(
        self,
        path: str,
        method: str = "GET",
        headers: Dict = None,
        body: Dict = None,
        client_ip: str = "127.0.0.1"
    ) -> Dict:
        """路由请求"""
        start_time = time.time()

        # 1. 查找路由
        route = self.routes.get(path)
        if not route:
            return {"success": False, "error": "路由不存在", "status_code": 404}

        service_name = route["service_name"]

        # 2. 限流检查
        if not self.rate_limiter.allow_request(f"{client_ip}:{path}"):
            return {"success": False, "error": "请求过于频繁", "status_code": 429}

        # 3. 认证检查
        if route["auth_required"]:
            auth_header = headers.get("Authorization", "") if headers else ""
            token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else auth_header

            if not token or not self.auth_manager.validate_token(token):
                return {"success": False, "error": "未授权", "status_code": 401}

        # 4. 熔断检查
        if not self.circuit_breaker.can_execute(service_name):
            return {"success": False, "error": f"服务 {service_name} 暂时不可用", "status_code": 503}

        # 5. 负载均衡获取实例
        instance = self.load_balancer.get_instance(service_name)
        if not instance:
            return {"success": False, "error": f"服务 {service_name} 无可用实例", "status_code": 503}

        # 6. 转发请求（模拟）
        try:
            result = await self._forward_request(instance, method, path, headers, body)

            # 记录成功
            self.circuit_breaker.record_success(service_name)

            # 记录日志
            self._log_request(
                client_ip=client_ip,
                path=path,
                service=service_name,
                status="success",
                duration=time.time() - start_time
            )

            return result

        except Exception as e:
            # 记录失败
            self.circuit_breaker.record_failure(service_name)

            self._log_request(
                client_ip=client_ip,
                path=path,
                service=service_name,
                status="failed",
                duration=time.time() - start_time,
                error=str(e)
            )

            return {"success": False, "error": str(e), "status_code": 500}

    async def _forward_request(
        self,
        instance: ServiceInstance,
        method: str,
        path: str,
        headers: Dict,
        body: Dict
    ) -> Dict:
        """转发请求到后端服务（模拟）"""
        # 模拟网络延迟
        await asyncio.sleep(random.uniform(0.01, 0.1))

        # 模拟随机失败（用于测试熔断）
        if random.random() < 0.1:  # 10%失败率
            raise Exception("服务暂时不可用")

        # 模拟响应
        return {
            "success": True,
            "data": {
                "service": instance.service_name,
                "instance": instance.url,
                "path": path,
                "method": method,
                "processed_at": datetime.now().isoformat()
            },
            "status_code": 200
        }

    def _log_request(self, **kwargs) -> None:
        """记录请求日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        self.request_log.append(log_entry)
        print(f"[Gateway Log] {log_entry}")


# ==================== FastAPI应用 ====================

app = FastAPI(title="API Gateway", version="1.0.0")
gateway = ApiGateway()
security = HTTPBearer()

# 初始化服务实例
gateway.load_balancer.register(ServiceInstance("user-service", "localhost", 8001, weight=2))
gateway.load_balancer.register(ServiceInstance("user-service", "localhost", 8002, weight=1))
gateway.load_balancer.register(ServiceInstance("order-service", "localhost", 8003))
gateway.load_balancer.register(ServiceInstance("product-service", "localhost", 8004))

# 添加路由规则
gateway.add_route("/api/users", "user-service", auth_required=True)
gateway.add_route("/api/orders", "order-service", auth_required=True)
gateway.add_route("/api/products", "product-service", auth_required=False)
gateway.add_route("/api/public/health", "user-service", auth_required=False)

# 生成测试token
test_token = gateway.auth_manager.generate_token("user_001", ["user", "admin"])
print(f"\n[测试Token] {test_token}")


@app.get("/")
async def root():
    return {"message": "API Gateway", "version": "1.0.0"}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_request(request: Request, path: str):
    """代理所有请求"""
    # 获取请求信息
    method = request.method
    headers = dict(request.headers)
    body = await request.json() if request.method in ["POST", "PUT"] else {}
    client_ip = request.client.host

    # 构建完整路径
    full_path = f"/api/{path}" if not path.startswith("api/") else f"/{path}"

    # 路由请求
    result = await gateway.route_request(
        path=full_path,
        method=method,
        headers=headers,
        body=body,
        client_ip=client_ip
    )

    status_code = result.pop("status_code", 200)
    return JSONResponse(content=result, status_code=status_code)


@app.get("/gateway/stats")
async def gateway_stats():
    """网关统计信息"""
    return {
        "routes": gateway.routes,
        "request_count": len(gateway.request_log),
        "recent_requests": gateway.request_log[-10:],
        "circuit_breaker_states": {
            name: state.value
            for name, state in gateway.circuit_breaker._state.items()
        }
    }


# ==================== 独立运行示例 ====================

async def demo_gateway():
    """演示API网关功能"""
    print("=" * 60)
    print("API网关演示")
    print("=" * 60)

    gw = ApiGateway()

    # 注册服务
    gw.load_balancer.register(ServiceInstance("user-service", "localhost", 8001))
    gw.load_balancer.register(ServiceInstance("order-service", "localhost", 8002))

    # 添加路由
    gw.add_route("/api/users", "user-service")
    gw.add_route("/api/orders", "order-service")

    # 生成token
    token = gw.auth_manager.generate_token("user_001")

    # 测试请求
    print("\n1. 正常请求（带认证）:")
    result1 = await gw.route_request(
        path="/api/users",
        method="GET",
        headers={"Authorization": token},
        client_ip="192.168.1.1"
    )
    print(json.dumps(result1, indent=2, ensure_ascii=False))

    print("\n2. 未授权请求:")
    result2 = await gw.route_request(
        path="/api/users",
        method="GET",
        headers={},
        client_ip="192.168.1.2"
    )
    print(json.dumps(result2, indent=2, ensure_ascii=False))

    print("\n3. 路由不存在:")
    result3 = await gw.route_request(
        path="/api/unknown",
        method="GET",
        headers={"Authorization": token},
        client_ip="192.168.1.3"
    )
    print(json.dumps(result3, indent=2, ensure_ascii=False))

    print("\n4. 测试限流（快速请求）:")
    for i in range(25):
        result = await gw.route_request(
            path="/api/users",
            method="GET",
            headers={"Authorization": token},
            client_ip="192.168.1.4"
        )
        if not result["success"]:
            print(f"请求 {i+1}: {result['error']}")
            break

    print("\n5. 测试熔断器:")
    # 模拟多次失败
    for i in range(10):
        try:
            # 强制失败
            gw.circuit_breaker.record_failure("order-service")
            state = gw.circuit_breaker._state.get("order-service")
            if state:
                print(f"失败 {i+1}: 熔断器状态 = {state.value}")
                if state.value == "open":
                    break
        except:
            pass

    print("\n网关统计:")
    print(f"请求总数: {len(gw.request_log)}")


if __name__ == "__main__":
    asyncio.run(demo_gateway())
```

---

### 2.3 服务间通信

#### 同步通信

##### REST API

```python
"""
REST API 客户端实现
"""

import asyncio
from dataclasses import dataclass
from typing import Optional, Dict, Any
import json


class RestClient:
    """REST客户端"""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    async def get(self, path: str, headers: Dict = None) -> Dict:
        """GET请求"""
        # 模拟HTTP请求
        await asyncio.sleep(0.05)  # 模拟网络延迟

        url = f"{self.base_url}{path}"
        print(f"[REST] GET {url}")

        # 模拟响应
        return {
            "status": 200,
            "data": {"message": "GET success", "path": path}
        }

    async def post(self, path: str, data: Dict, headers: Dict = None) -> Dict:
        """POST请求"""
        await asyncio.sleep(0.05)

        url = f"{self.base_url}{path}"
        print(f"[REST] POST {url} - {json.dumps(data, ensure_ascii=False)}")

        return {
            "status": 201,
            "data": {"message": "POST success", "received": data}
        }

    async def put(self, path: str, data: Dict, headers: Dict = None) -> Dict:
        """PUT请求"""
        await asyncio.sleep(0.05)

        url = f"{self.base_url}{path}"
        print(f"[REST] PUT {url}")

        return {
            "status": 200,
            "data": {"message": "PUT success"}
        }

    async def delete(self, path: str, headers: Dict = None) -> Dict:
        """DELETE请求"""
        await asyncio.sleep(0.05)

        url = f"{self.base_url}{path}"
        print(f"[REST] DELETE {url}")

        return {
            "status": 204,
            "data": {"message": "DELETE success"}
        }


# REST优缺点
REST_PROS_CONS = """
REST API 优缺点:

优点:
1. 简单易用，广泛支持
2. 基于HTTP，易于调试
3. 无状态，易于水平扩展
4. 可读性好，自描述

缺点:
1. 多次往返（N+1问题）
2. 数据冗余（过度获取）
3. 版本管理困难
4. 实时性差

适用场景:
- 浏览器客户端
- 第三方API
- 简单CRUD操作
- 需要人类可读的场景
"""
```

##### gRPC

```python
"""
gRPC 概念与Python实现示例
注意：需要安装 grpcio 和 grpcio-tools
"""

# 定义.proto文件（通常单独存放）
PROTO_DEFINITION = '''
syntax = "proto3";

package ecommerce;

// 商品服务
service ProductService {
    rpc GetProduct(GetProductRequest) returns (Product);
    rpc ListProducts(ListProductsRequest) returns (ProductList);
    rpc CreateProduct(CreateProductRequest) returns (Product);
}

message GetProductRequest {
    string product_id = 1;
}

message ListProductsRequest {
    string category = 1;
    int32 page = 2;
    int32 page_size = 3;
}

message CreateProductRequest {
    string name = 1;
    string description = 2;
    double price = 3;
    int32 stock = 4;
}

message Product {
    string id = 1;
    string name = 2;
    string description = 3;
    double price = 4;
    int32 stock = 5;
    string created_at = 6;
}

message ProductList {
    repeated Product products = 1;
    int32 total = 2;
}
'''

# 模拟gRPC客户端（实际使用时需要生成代码）
class GrpcClient:
    """gRPC客户端模拟"""

    def __init__(self, target: str):
        self.target = target
        print(f"[gRPC] 连接到 {target}")

    async def get_product(self, product_id: str) -> dict:
        """获取商品"""
        # 模拟gRPC调用
        await asyncio.sleep(0.02)  # gRPC通常比REST快

        print(f"[gRPC] GetProduct({product_id})")

        return {
            "id": product_id,
            "name": "示例商品",
            "price": 99.99,
            "stock": 100
        }

    async def list_products(self, category: str = None, page: int = 1) -> list:
        """列出商品"""
        await asyncio.sleep(0.02)

        print(f"[gRPC] ListProducts(category={category}, page={page})")

        return [
            {"id": "P001", "name": "商品1", "price": 100},
            {"id": "P002", "name": "商品2", "price": 200}
        ]


# gRPC优缺点
GRPC_PROS_CONS = """
gRPC 优缺点:

优点:
1. 高性能（HTTP/2 + Protobuf）
2. 强类型，编译时检查
3. 支持流式通信
4. 自动生成客户端代码
5. 双向认证

缺点:
1. 需要.proto定义
2. 浏览器支持有限
3. 调试相对复杂
4. 学习曲线较陡

适用场景:
- 微服务间通信
- 高性能要求
- 多语言环境
- 内部服务通信
"""


# REST vs gRPC 对比
COMMUNICATION_COMPARISON = """
同步通信方式对比:

特性          | REST      | gRPC      | GraphQL
--------------|-----------|-----------|----------
协议          | HTTP/1.1  | HTTP/2    | HTTP/1.1
数据格式      | JSON/XML  | Protobuf  | JSON
性能          | 中        | 高        | 中
类型安全      | 无        | 有        | 有Schema
浏览器支持    | 优秀      | 有限      | 优秀
流式支持      | SSE/WebSocket | 原生  | Subscriptions
调试难度      | 低        | 中        | 中
学习曲线      | 低        | 中        | 中

选择建议:
- 对外API: REST 或 GraphQL
- 内部服务: gRPC
- 实时通信: WebSocket / gRPC Streaming
"""
```

#### 异步通信 - 消息队列

```python
"""
消息队列实现 - 基于内存的简化版
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Callable, Optional, Any
from enum import Enum, auto
from collections import defaultdict
import asyncio
import json
import uuid


class MessagePriority(Enum):
    """消息优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Message:
    """消息"""
    id: str
    topic: str
    payload: Dict[str, Any]
    priority: MessagePriority = MessagePriority.NORMAL
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    retry_count: int = 0
    max_retries: int = 3

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "topic": self.topic,
            "payload": self.payload,
            "priority": self.priority.name,
            "created_at": self.created_at
        }


class MessageQueue(ABC):
    """消息队列抽象"""

    @abstractmethod
    async def publish(self, topic: str, message: Message) -> bool:
        pass

    @abstractmethod
    async def subscribe(self, topic: str, handler: Callable[[Message], None]) -> None:
        pass

    @abstractmethod
    async def consume(self, topic: str, consumer_group: str = None) -> Optional[Message]:
        pass


class InMemoryMessageQueue(MessageQueue):
    """内存消息队列实现"""

    def __init__(self):
        self._queues: Dict[str, List[Message]] = defaultdict(list)
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._consumer_offsets: Dict[str, int] = defaultdict(int)
        self._running = True

    async def publish(self, topic: str, message: Message) -> bool:
        """发布消息"""
        self._queues[topic].append(message)
        print(f"[MQ] 消息发布到 {topic}: {message.id}")

        # 通知订阅者
        for handler in self._subscribers[topic]:
            asyncio.create_task(self._notify_handler(handler, message))

        return True

    async def _notify_handler(self, handler: Callable, message: Message) -> None:
        """通知处理器"""
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(message)
            else:
                handler(message)
        except Exception as e:
            print(f"[MQ] 处理器错误: {e}")

    async def subscribe(self, topic: str, handler: Callable[[Message], None]) -> None:
        """订阅主题"""
        self._subscribers[topic].append(handler)
        print(f"[MQ] 订阅主题: {topic}")

    async def consume(self, topic: str, consumer_group: str = None) -> Optional[Message]:
        """消费消息"""
        consumer_key = f"{topic}:{consumer_group}" if consumer_group else topic
        offset = self._consumer_offsets[consumer_key]

        if offset < len(self._queues[topic]):
            message = self._queues[topic][offset]
            self._consumer_offsets[consumer_key] = offset + 1
            return message

        return None

    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "topics": list(self._queues.keys()),
            "message_counts": {topic: len(msgs) for topic, msgs in self._queues.items()},
            "subscriber_counts": {topic: len(subs) for topic, subs in self._subscribers.items()}
        }


# ==================== 消息模式 ====================

class MessagePatterns:
    """消息模式实现"""

    @staticmethod
    async def pub_sub_demo(mq: MessageQueue):
        """发布-订阅模式演示"""
        print("\n=== 发布-订阅模式 ===")

        # 订阅者1
        async def subscriber1(message: Message):
            print(f"[Subscriber1] 收到: {message.payload}")

        # 订阅者2
        async def subscriber2(message: Message):
            print(f"[Subscriber2] 收到: {message.payload}")

        await mq.subscribe("order.created", subscriber1)
        await mq.subscribe("order.created", subscriber2)

        # 发布消息
        message = Message(
            id=str(uuid.uuid4()),
            topic="order.created",
            payload={"order_id": "ORD001", "amount": 100}
        )
        await mq.publish("order.created", message)

        await asyncio.sleep(0.1)  # 等待消息处理

    @staticmethod
    async def work_queue_demo(mq: MessageQueue):
        """工作队列模式演示"""
        print("\n=== 工作队列模式 ===")

        # 多个消费者
        processed = []

        async def worker1(message: Message):
            processed.append(f"worker1-{message.id}")
            print(f"[Worker1] 处理: {message.id}")

        async def worker2(message: Message):
            processed.append(f"worker2-{message.id}")
            print(f"[Worker2] 处理: {message.id}")

        await mq.subscribe("tasks", worker1)
        await mq.subscribe("tasks", worker2)

        # 发布多个任务
        for i in range(5):
            message = Message(
                id=f"TASK{i+1}",
                topic="tasks",
                payload={"task_id": i+1, "data": f"任务数据{i+1}"}
            )
            await mq.publish("tasks", message)

        await asyncio.sleep(0.2)
        print(f"处理完成: {processed}")

    @staticmethod
    async def request_reply_demo(mq: MessageQueue):
        """请求-回复模式演示"""
        print("\n=== 请求-回复模式 ===")

        # RPC服务端
        async def rpc_server(message: Message):
            request = message.payload
            print(f"[RPC Server] 收到请求: {request}")

            # 处理请求
            result = {"result": request.get("x", 0) + request.get("y", 0)}

            # 发送响应
            response = Message(
                id=str(uuid.uuid4()),
                topic="rpc.response",
                payload={"request_id": message.id, "result": result}
            )
            await mq.publish("rpc.response", response)

        await mq.subscribe("rpc.request", rpc_server)

        # RPC客户端
        request = Message(
            id=str(uuid.uuid4()),
            topic="rpc.request",
            payload={"x": 10, "y": 20}
        )
        await mq.publish("rpc.request", request)

        # 等待响应
        await asyncio.sleep(0.1)
        response = await mq.consume("rpc.response")
        if response:
            print(f"[RPC Client] 收到响应: {response.payload}")


# ==================== 事件总线 ====================

class EventBus:
    """事件总线 - 简化版"""

    def __init__(self, message_queue: MessageQueue):
        self._mq = message_queue
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)

    async def emit(self, event_type: str, payload: dict) -> None:
        """发送事件"""
        message = Message(
            id=str(uuid.uuid4()),
            topic=f"event.{event_type}",
            payload=payload
        )
        await self._mq.publish(message.topic, message)

    async def on(self, event_type: str, handler: Callable) -> None:
        """监听事件"""
        topic = f"event.{event_type}"

        async def wrapper(message: Message):
            await handler(message.payload)

        self._handlers[event_type].append(handler)
        await self._mq.subscribe(topic, wrapper)


# ==================== 运行示例 ====================

async def main():
    print("=" * 60)
    print("消息队列演示")
    print("=" * 60)

    mq = InMemoryMessageQueue()

    # 发布-订阅模式
    await MessagePatterns.pub_sub_demo(mq)

    # 工作队列模式
    await MessagePatterns.work_queue_demo(mq)

    # 请求-回复模式
    await MessagePatterns.request_reply_demo(mq)

    # 统计信息
    print("\n=== 队列统计 ===")
    print(json.dumps(mq.get_stats(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
```

---

### 2.4 服务发现

```python
"""
服务发现实现 - 基于内存的简化版服务注册中心
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
import asyncio
import json
import time


@dataclass
class ServiceInstance:
    """服务实例"""
    service_name: str
    instance_id: str
    host: str
    port: int
    metadata: Dict = field(default_factory=dict)
    health_check_url: str = ""
    registered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_heartbeat: float = field(default_factory=time.time)
    healthy: bool = True

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def is_expired(self, timeout_seconds: int = 30) -> bool:
        """检查是否过期"""
        return time.time() - self.last_heartbeat > timeout_seconds


class ServiceRegistry:
    """服务注册中心"""

    def __init__(self, heartbeat_timeout: int = 30):
        self._services: Dict[str, List[ServiceInstance]] = {}
        self._heartbeat_timeout = heartbeat_timeout
        self._running = False

    def register(self, instance: ServiceInstance) -> bool:
        """注册服务实例"""
        if instance.service_name not in self._services:
            self._services[instance.service_name] = []

        # 检查是否已存在
        existing = self._find_instance(instance.service_name, instance.instance_id)
        if existing:
            # 更新心跳
            existing.last_heartbeat = time.time()
            print(f"[Registry] 服务心跳更新: {instance.service_name}/{instance.instance_id}")
            return True

        self._services[instance.service_name].append(instance)
        print(f"[Registry] 服务注册成功: {instance.service_name}/{instance.instance_id} @ {instance.url}")
        return True

    def deregister(self, service_name: str, instance_id: str) -> bool:
        """注销服务实例"""
        if service_name not in self._services:
            return False

        instances = self._services[service_name]
        for i, instance in enumerate(instances):
            if instance.instance_id == instance_id:
                instances.pop(i)
                print(f"[Registry] 服务注销: {service_name}/{instance_id}")
                return True

        return False

    def heartbeat(self, service_name: str, instance_id: str) -> bool:
        """服务心跳"""
        instance = self._find_instance(service_name, instance_id)
        if instance:
            instance.last_heartbeat = time.time()
            instance.healthy = True
            return True
        return False

    def discover(self, service_name: str) -> List[ServiceInstance]:
        """发现服务"""
        instances = self._services.get(service_name, [])
        # 过滤掉过期的实例
        healthy_instances = [
            i for i in instances
            if not i.is_expired(self._heartbeat_timeout) and i.healthy
        ]
        return healthy_instances

    def get_all_services(self) -> Dict[str, List[dict]]:
        """获取所有服务"""
        result = {}
        for service_name, instances in self._services.items():
            result[service_name] = [
                {
                    "instance_id": i.instance_id,
                    "url": i.url,
                    "healthy": i.healthy and not i.is_expired(self._heartbeat_timeout),
                    "metadata": i.metadata
                }
                for i in instances
            ]
        return result

    def _find_instance(self, service_name: str, instance_id: str) -> Optional[ServiceInstance]:
        """查找实例"""
        instances = self._services.get(service_name, [])
        for instance in instances:
            if instance.instance_id == instance_id:
                return instance
        return None

    async def start_health_check(self, interval: int = 10):
        """启动健康检查"""
        self._running = True
        while self._running:
            await asyncio.sleep(interval)
            await self._check_health()

    async def _check_health(self):
        """检查服务健康状态"""
        for service_name, instances in self._services.items():
            for instance in instances:
                if instance.is_expired(self._heartbeat_timeout):
                    instance.healthy = False
                    print(f"[HealthCheck] 服务不健康: {service_name}/{instance.instance_id}")


class ServiceClient:
    """服务客户端 - 自动服务发现"""

    def __init__(self, registry: ServiceRegistry):
        self._registry = registry
        self._cache: Dict[str, List[ServiceInstance]] = {}
        self._cache_ttl = 5  # 缓存5秒
        self._cache_time: Dict[str, float] = {}

    def get_service(self, service_name: str, use_cache: bool = True) -> Optional[ServiceInstance]:
        """获取服务实例（带缓存）"""
        now = time.time()

        # 检查缓存
        if use_cache and service_name in self._cache:
            cache_time = self._cache_time.get(service_name, 0)
            if now - cache_time < self._cache_ttl:
                instances = self._cache[service_name]
                if instances:
                    # 简单轮询
                    instance = instances[0]
                    return instance

        # 从注册中心获取
        instances = self._registry.discover(service_name)
        if instances:
            self._cache[service_name] = instances
            self._cache_time[service_name] = now
            return instances[0]

        return None

    def call_service(self, service_name: str, path: str = "/") -> dict:
        """调用服务"""
        instance = self.get_service(service_name)
        if not instance:
            return {"success": False, "error": f"服务 {service_name} 不可用"}

        # 模拟调用
        url = f"{instance.url}{path}"
        print(f"[ServiceClient] 调用 {url}")

        return {
            "success": True,
            "service": service_name,
            "instance": instance.instance_id,
            "url": url
        }


# ==================== 运行示例 ====================

async def demo_service_discovery():
    print("=" * 60)
    print("服务发现演示")
    print("=" * 60)

    # 创建注册中心
    registry = ServiceRegistry(heartbeat_timeout=10)

    # 注册服务实例
    instances = [
        ServiceInstance("user-service", "user-1", "localhost", 8001, {"version": "1.0"}),
        ServiceInstance("user-service", "user-2", "localhost", 8002, {"version": "1.0"}),
        ServiceInstance("order-service", "order-1", "localhost", 8003, {"version": "2.0"}),
    ]

    for instance in instances:
        registry.register(instance)

    # 查看所有服务
    print("\n1. 注册的所有服务:")
    print(json.dumps(registry.get_all_services(), indent=2, ensure_ascii=False))

    # 服务发现
    print("\n2. 发现 user-service:")
    user_services = registry.discover("user-service")
    for s in user_services:
        print(f"  - {s.instance_id} @ {s.url}")

    # 服务客户端调用
    print("\n3. 服务客户端调用:")
    client = ServiceClient(registry)
    result = client.call_service("user-service", "/api/users/1")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 模拟心跳
    print("\n4. 模拟心跳:")
    registry.heartbeat("user-service", "user-1")

    # 模拟服务下线
    print("\n5. 服务注销:")
    registry.deregister("user-service", "user-2")
    print(json.dumps(registry.get_all_services(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(demo_service_discovery())
```

---

### 2.5 配置中心

```python
"""
配置中心实现 - 集中式配置管理
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any, Set
from enum import Enum
import json
import time
import asyncio


class ConfigFormat(Enum):
    """配置格式"""
    JSON = "json"
    YAML = "yaml"
    PROPERTIES = "properties"
    ENV = "env"


@dataclass
class ConfigItem:
    """配置项"""
    key: str
    value: Any
    format: ConfigFormat = ConfigFormat.JSON
    version: int = 1
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    description: str = ""


@dataclass
class ConfigNamespace:
    """配置命名空间"""
    name: str
    configs: Dict[str, ConfigItem] = field(default_factory=dict)
    subscribers: Set[str] = field(default_factory=set)


class ConfigCenter:
    """配置中心"""

    def __init__(self):
        self._namespaces: Dict[str, ConfigNamespace] = {}
        self._subscribers: Dict[str, List[Callable]] = {}
        self._history: Dict[str, List[Dict]] = {}  # 配置历史

    def create_namespace(self, name: str) -> ConfigNamespace:
        """创建命名空间"""
        if name not in self._namespaces:
            self._namespaces[name] = ConfigNamespace(name)
            print(f"[ConfigCenter] 创建命名空间: {name}")
        return self._namespaces[name]

    def set_config(
        self,
        namespace: str,
        key: str,
        value: Any,
        description: str = ""
    ) -> ConfigItem:
        """设置配置"""
        ns = self._namespaces.get(namespace)
        if not ns:
            ns = self.create_namespace(namespace)

        # 检查是否已存在
        existing = ns.configs.get(key)
        version = existing.version + 1 if existing else 1

        config = ConfigItem(
            key=key,
            value=value,
            version=version,
            description=description
        )

        ns.configs[key] = config

        # 记录历史
        history_key = f"{namespace}:{key}"
        if history_key not in self._history:
            self._history[history_key] = []
        self._history[history_key].append({
            "version": version,
            "value": value,
            "timestamp": time.time()
        })

        # 通知订阅者
        self._notify_subscribers(namespace, key, config)

        print(f"[ConfigCenter] 配置更新: {namespace}/{key} = {value} (v{version})")
        return config

    def get_config(self, namespace: str, key: str, default: Any = None) -> Any:
        """获取配置"""
        ns = self._namespaces.get(namespace)
        if not ns:
            return default

        config = ns.configs.get(key)
        return config.value if config else default

    def get_all_configs(self, namespace: str) -> Dict[str, Any]:
        """获取命名空间下所有配置"""
        ns = self._namespaces.get(namespace)
        if not ns:
            return {}

        return {key: config.value for key, config in ns.configs.items()}

    def subscribe(self, namespace: str, key: str, callback: Callable[[str, Any], None]) -> None:
        """订阅配置变更"""
        subscribe_key = f"{namespace}:{key}"
        if subscribe_key not in self._subscribers:
            self._subscribers[subscribe_key] = []
        self._subscribers[subscribe_key].append(callback)
        print(f"[ConfigCenter] 订阅配置: {subscribe_key}")

    def _notify_subscribers(self, namespace: str, key: str, config: ConfigItem) -> None:
        """通知订阅者"""
        subscribe_key = f"{namespace}:{key}"
        callbacks = self._subscribers.get(subscribe_key, [])
        for callback in callbacks:
            try:
                callback(key, config.value)
            except Exception as e:
                print(f"[ConfigCenter] 通知订阅者失败: {e}")

    def get_history(self, namespace: str, key: str) -> List[Dict]:
        """获取配置历史"""
        history_key = f"{namespace}:{key}"
        return self._history.get(history_key, [])

    def export_namespace(self, namespace: str) -> Dict:
        """导出命名空间配置"""
        ns = self._namespaces.get(namespace)
        if not ns:
            return {}

        return {
            "namespace": namespace,
            "configs": {
                key: {
                    "value": config.value,
                    "version": config.version,
                    "updated_at": config.updated_at,
                    "description": config.description
                }
                for key, config in ns.configs.items()
            }
        }


class ConfigClient:
    """配置客户端 - 服务使用"""

    def __init__(self, config_center: ConfigCenter, service_name: str):
        self._center = config_center
        self._service_name = service_name
        self._local_cache: Dict[str, Any] = {}
        self._namespace = f"service.{service_name}"

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置"""
        # 先查本地缓存
        if key in self._local_cache:
            return self._local_cache[key]

        # 从配置中心获取
        value = self._center.get_config(self._namespace, key, default)
        self._local_cache[key] = value
        return value

    def refresh(self) -> None:
        """刷新配置"""
        configs = self._center.get_all_configs(self._namespace)
        self._local_cache.update(configs)
        print(f"[ConfigClient] {self._service_name} 配置已刷新")

    def watch(self, key: str) -> None:
        """监听配置变更"""
        def on_change(key: str, value: Any):
            self._local_cache[key] = value
            print(f"[ConfigClient] {self._service_name} 配置变更: {key} = {value}")

        self._center.subscribe(self._namespace, key, on_change)


# ==================== 运行示例 ====================

async def demo_config_center():
    print("=" * 60)
    print("配置中心演示")
    print("=" * 60)

    # 创建配置中心
    center = ConfigCenter()

    # 设置配置
    print("\n1. 设置配置:")
    center.set_config("service.user-service", "db.host", "localhost", "数据库主机")
    center.set_config("service.user-service", "db.port", 5432, "数据库端口")
    center.set_config("service.user-service", "cache.ttl", 300, "缓存时间")
    center.set_config("service.order-service", "payment.timeout", 30, "支付超时")

    # 获取配置
    print("\n2. 获取配置:")
    db_host = center.get_config("service.user-service", "db.host")
    print(f"  db.host = {db_host}")

    # 获取所有配置
    print("\n3. 获取所有配置:")
    all_configs = center.get_all_configs("service.user-service")
    print(json.dumps(all_configs, indent=2, ensure_ascii=False))

    # 配置客户端
    print("\n4. 配置客户端使用:")
    client = ConfigClient(center, "user-service")
    print(f"  db.host = {client.get('db.host')}")
    print(f"  db.port = {client.get('db.port')}")

    # 订阅配置变更
    print("\n5. 配置变更通知:")
    client.watch("db.host")
    center.set_config("service.user-service", "db.host", "192.168.1.100")

    # 配置历史
    print("\n6. 配置历史:")
    history = center.get_history("service.user-service", "db.host")
    for h in history:
        print(f"  v{h['version']}: {h['value']} @ {h['timestamp']}")

    # 导出配置
    print("\n7. 导出配置:")
    exported = center.export_namespace("service.user-service")
    print(json.dumps(exported, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(demo_config_center())
```

---


## 第三部分：事件驱动架构

### 3.1 事件溯源（Event Sourcing）

#### 概念定义

事件溯源是一种数据持久化模式，不存储对象的当前状态，而是存储导致状态变更的所有事件序列。通过重放事件可以重建任何时刻的状态。

```
传统方式:                    事件溯源:
┌──────────┐                ┌─────────────┐
│  当前状态  │                │  事件1: 创建  │
│  User    │                │  事件2: 修改  │
│  name=XX │                │  事件3: 修改  │
│  age=XX  │                │  事件4: 删除  │
└──────────┘                └─────────────┘
     │                              │
     ▼                              ▼
  直接更新                      追加事件
  丢失历史                      完整历史
```

#### 核心概念

| 概念 | 说明 |
|------|------|
| **事件（Event）** | 表示状态变更的不可变记录 |
| **事件存储（Event Store）** | 持久化事件的存储系统 |
| **聚合（Aggregate）** | 通过事件重建的领域对象 |
| **快照（Snapshot）** | 聚合状态的时间点备份，用于优化 |
| **投影（Projection）** | 从事件派生的只读视图 |

#### Python实现

```python
"""
事件溯源实现 - 银行账户系统
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Optional, Type, Callable
from enum import Enum, auto
from uuid import uuid4, UUID
import json
import copy


# ==================== 领域事件 ====================

@dataclass(frozen=True)
class DomainEvent:
    """领域事件基类"""
    aggregate_id: str
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_on: str = field(default_factory=lambda: datetime.now().isoformat())
    version: int = 1

    def event_type(self) -> str:
        return self.__class__.__name__


@dataclass(frozen=True)
class AccountCreated(DomainEvent):
    """账户创建事件"""
    owner_name: str
    initial_balance: Decimal


@dataclass(frozen=True)
class MoneyDeposited(DomainEvent):
    """存款事件"""
    amount: Decimal
    description: str


@dataclass(frozen=True)
class MoneyWithdrawn(DomainEvent):
    """取款事件"""
    amount: Decimal
    description: str


@dataclass(frozen=True)
class MoneyTransferred(DomainEvent):
    """转账事件"""
    to_account_id: str
    amount: Decimal
    description: str


# ==================== 事件存储 ====================

class EventStore:
    """事件存储"""

    def __init__(self):
        # 按聚合ID存储事件
        self._streams: Dict[str, List[DomainEvent]] = {}
        # 所有事件（用于投影）
        self._all_events: List[DomainEvent] = []

    def append(self, aggregate_id: str, event: DomainEvent, expected_version: int = None) -> None:
        """追加事件"""
        if aggregate_id not in self._streams:
            self._streams[aggregate_id] = []

        stream = self._streams[aggregate_id]

        # 乐观并发控制
        if expected_version is not None:
            current_version = len(stream)
            if current_version != expected_version:
                raise ConcurrencyException(
                    f"并发冲突: 期望版本 {expected_version}, 当前版本 {current_version}"
                )

        stream.append(event)
        self._all_events.append(event)

        print(f"[EventStore] 事件追加: {aggregate_id} - {event.event_type()}")

    def get_events(self, aggregate_id: str, after_version: int = 0) -> List[DomainEvent]:
        """获取聚合的事件流"""
        events = self._streams.get(aggregate_id, [])
        return events[after_version:]

    def get_all_events(self, event_types: List[str] = None) -> List[DomainEvent]:
        """获取所有事件"""
        if event_types:
            return [e for e in self._all_events if e.event_type() in event_types]
        return self._all_events.copy()

    def get_event_stream(self, aggregate_id: str) -> List[DomainEvent]:
        """获取完整事件流"""
        return self._streams.get(aggregate_id, []).copy()


class ConcurrencyException(Exception):
    """并发异常"""
    pass


# ==================== 聚合根 ====================

class AggregateRoot:
    """聚合根基类"""

    def __init__(self, aggregate_id: str):
        self._id = aggregate_id
        self._version = 0
        self._uncommitted_events: List[DomainEvent] = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def version(self) -> int:
        return self._version

    def apply_event(self, event: DomainEvent) -> None:
        """应用事件到聚合"""
        handler = getattr(self, f'_on_{event.event_type().lower()}', None)
        if handler:
            handler(event)
        self._version += 1

    def apply(self, event: DomainEvent) -> None:
        """应用新事件"""
        self.apply_event(event)
        self._uncommitted_events.append(event)

    def get_uncommitted_events(self) -> List[DomainEvent]:
        """获取未提交事件"""
        return self._uncommitted_events.copy()

    def commit(self) -> None:
        """提交事件"""
        self._uncommitted_events.clear()

    @classmethod
    def load_from_history(cls, aggregate_id: str, events: List[DomainEvent]) -> "AggregateRoot":
        """从历史事件重建聚合"""
        aggregate = cls(aggregate_id)
        for event in events:
            aggregate.apply_event(event)
        aggregate._uncommitted_events.clear()
        return aggregate


class BankAccount(AggregateRoot):
    """银行账户聚合"""

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self._owner_name: str = ""
        self._balance: Decimal = Decimal("0")
        self._is_active: bool = False
        self._transaction_history: List[Dict] = []

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def owner_name(self) -> str:
        return self._owner_name

    @property
    def is_active(self) -> bool:
        return self._is_active

    @classmethod
    def create(cls, account_id: str, owner_name: str, initial_balance: Decimal = Decimal("0")) -> "BankAccount":
        """创建账户"""
        account = cls(account_id)
        event = AccountCreated(
            aggregate_id=account_id,
            owner_name=owner_name,
            initial_balance=initial_balance
        )
        account.apply(event)
        return account

    def deposit(self, amount: Decimal, description: str = "") -> None:
        """存款"""
        if amount <= 0:
            raise ValueError("存款金额必须大于0")

        event = MoneyDeposited(
            aggregate_id=self._id,
            amount=amount,
            description=description
        )
        self.apply(event)

    def withdraw(self, amount: Decimal, description: str = "") -> None:
        """取款"""
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        if amount > self._balance:
            raise ValueError("余额不足")

        event = MoneyWithdrawn(
            aggregate_id=self._id,
            amount=amount,
            description=description
        )
        self.apply(event)

    def transfer(self, to_account_id: str, amount: Decimal, description: str = "") -> None:
        """转账"""
        if amount <= 0:
            raise ValueError("转账金额必须大于0")
        if amount > self._balance:
            raise ValueError("余额不足")

        event = MoneyTransferred(
            aggregate_id=self._id,
            to_account_id=to_account_id,
            amount=amount,
            description=description
        )
        self.apply(event)

    # 事件处理器
    def _on_accountcreated(self, event: AccountCreated) -> None:
        self._owner_name = event.owner_name
        self._balance = event.initial_balance
        self._is_active = True

    def _on_moneydeposited(self, event: MoneyDeposited) -> None:
        self._balance += event.amount
        self._transaction_history.append({
            "type": "deposit",
            "amount": float(event.amount),
            "description": event.description,
            "time": event.occurred_on
        })

    def _on_moneywithdrawn(self, event: MoneyWithdrawn) -> None:
        self._balance -= event.amount
        self._transaction_history.append({
            "type": "withdrawal",
            "amount": float(event.amount),
            "description": event.description,
            "time": event.occurred_on
        })

    def _on_moneytransferred(self, event: MoneyTransferred) -> None:
        self._balance -= event.amount
        self._transaction_history.append({
            "type": "transfer_out",
            "to": event.to_account_id,
            "amount": float(event.amount),
            "description": event.description,
            "time": event.occurred_on
        })

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "owner_name": self._owner_name,
            "balance": float(self._balance),
            "is_active": self._is_active,
            "version": self._version,
            "transaction_count": len(self._transaction_history)
        }


# ==================== 仓储 ====================

class BankAccountRepository:
    """银行账户仓储"""

    def __init__(self, event_store: EventStore):
        self._event_store = event_store

    def save(self, account: BankAccount) -> None:
        """保存账户"""
        events = account.get_uncommitted_events()
        for event in events:
            self._event_store.append(account.id, event, account.version - len(events))
        account.commit()

    def find_by_id(self, account_id: str) -> Optional[BankAccount]:
        """查找账户"""
        events = self._event_store.get_event_stream(account_id)
        if not events:
            return None
        return BankAccount.load_from_history(account_id, events)


# ==================== 投影（只读视图）====================

class AccountProjection:
    """账户投影 - 从事件构建的只读视图"""

    def __init__(self, event_store: EventStore):
        self._event_store = event_store
        self._account_summaries: Dict[str, dict] = {}
        self._daily_transactions: Dict[str, List[dict]] = {}

    def rebuild(self) -> None:
        """重建投影"""
        print("\n[Projection] 重建投影...")
        self._account_summaries.clear()
        self._daily_transactions.clear()

        events = self._event_store.get_all_events()
        for event in events:
            self._apply_to_projection(event)

        print(f"[Projection] 重建完成: {len(self._account_summaries)} 个账户")

    def _apply_to_projection(self, event: DomainEvent) -> None:
        """应用事件到投影"""
        if isinstance(event, AccountCreated):
            self._account_summaries[event.aggregate_id] = {
                "id": event.aggregate_id,
                "owner": event.owner_name,
                "balance": float(event.initial_balance),
                "status": "active"
            }

        elif isinstance(event, MoneyDeposited):
            summary = self._account_summaries.get(event.aggregate_id)
            if summary:
                summary["balance"] += float(event.amount)

        elif isinstance(event, MoneyWithdrawn):
            summary = self._account_summaries.get(event.aggregate_id)
            if summary:
                summary["balance"] -= float(event.amount)

        elif isinstance(event, MoneyTransferred):
            summary = self._account_summaries.get(event.aggregate_id)
            if summary:
                summary["balance"] -= float(event.amount)

    def get_account_summary(self, account_id: str) -> Optional[dict]:
        """获取账户摘要"""
        return self._account_summaries.get(account_id)

    def get_all_accounts(self) -> List[dict]:
        """获取所有账户"""
        return list(self._account_summaries.values())

    def get_total_balance(self) -> float:
        """获取总余额"""
        return sum(a["balance"] for a in self._account_summaries.values())


# ==================== 运行示例 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("事件溯源演示 - 银行账户系统")
    print("=" * 60)

    # 创建事件存储
    event_store = EventStore()

    # 创建仓储
    account_repo = BankAccountRepository(event_store)

    # 场景1: 创建账户
    print("\n1. 创建账户:")
    account1 = BankAccount.create(
        account_id="ACC001",
        owner_name="张三",
        initial_balance=Decimal("1000.00")
    )
    account_repo.save(account1)
    print(f"  账户: {account1.to_dict()}")

    # 场景2: 存款
    print("\n2. 存款:")
    account1.deposit(Decimal("500.00"), "工资")
    account1.deposit(Decimal("200.00"), "奖金")
    account_repo.save(account1)
    print(f"  余额: {account1.balance}")

    # 场景3: 取款
    print("\n3. 取款:")
    account1.withdraw(Decimal("300.00"), "购物")
    account_repo.save(account1)
    print(f"  余额: {account1.balance}")

    # 场景4: 从事件重建账户
    print("\n4. 从事件重建账户:")
    account1_rebuilt = account_repo.find_by_id("ACC001")
    print(f"  重建后余额: {account1_rebuilt.balance}")
    print(f"  重建后版本: {account1_rebuilt.version}")

    # 场景5: 创建第二个账户并转账
    print("\n5. 转账:")
    account2 = BankAccount.create("ACC002", "李四", Decimal("500.00"))
    account_repo.save(account2)

    account1.transfer("ACC002", Decimal("200.00"), "还款")
    account_repo.save(account1)
    print(f"  账户1余额: {account1.balance}")

    # 场景6: 查看所有事件
    print("\n6. 所有事件:")
    all_events = event_store.get_all_events()
    for event in all_events:
        print(f"  {event.occurred_on} - {event.event_type()} - {event.aggregate_id}")

    # 场景7: 投影
    print("\n7. 账户投影:")
    projection = AccountProjection(event_store)
    projection.rebuild()

    print("\n  所有账户摘要:")
    for summary in projection.get_all_accounts():
        print(f"    {summary}")

    print(f"\n  系统总余额: {projection.get_total_balance()}")
```

---

### 3.2 CQRS（命令查询职责分离）

#### 概念定义

CQRS将读操作和写操作分离到不同的模型：

- **命令端（Command Side）**：处理写操作，修改状态
- **查询端（Query Side）**：处理读操作，返回数据

```
传统CRUD:                    CQRS:
┌──────────┐                ┌──────────────┐
│  Controller│               │   Command   │
└────┬─────┘                │   Handler   │
     │                       └──────┬──────┘
     ▼                              │
┌──────────┐                        ▼
│  Service │                ┌──────────────┐
│ (CRUD)   │                │  Command DB  │
└────┬─────┘                │ (Write Model)│
     │                       └──────────────┘
     ▼                              │
┌──────────┐                       Event
│  Database│                        │
└──────────┘                        ▼
                              ┌──────────────┐
                              │   Event Bus  │
                              └──────┬───────┘
                                     │
                              ┌──────┴──────┐
                              ▼             ▼
                       ┌──────────┐  ┌──────────┐
                       │  Query   │  │  Query   │
                       │ Handler  │  │ Handler  │
                       └────┬─────┘  └────┬─────┘
                            │             │
                            ▼             ▼
                       ┌──────────┐  ┌──────────┐
                       │ Query DB │  │ Query DB │
                       │(Read Model)│(Read Model)│
                       └──────────┘  └──────────┘
```

#### Python实现

```python
"""
CQRS实现 - 订单管理系统
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Optional, Callable, Any
from enum import Enum, auto
from uuid import uuid4
import asyncio
import json


# ==================== 命令端 ====================

@dataclass
class Command:
    """命令基类"""
    command_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CreateOrderCommand(Command):
    """创建订单命令"""
    customer_id: str = ""
    items: List[Dict] = field(default_factory=list)
    shipping_address: str = ""


@dataclass
class UpdateOrderStatusCommand(Command):
    """更新订单状态命令"""
    order_id: str = ""
    new_status: str = ""
    reason: str = ""


@dataclass
class CancelOrderCommand(Command):
    """取消订单命令"""
    order_id: str = ""
    reason: str = ""


class CommandHandler(ABC):
    """命令处理器接口"""

    @abstractmethod
    async def handle(self, command: Command) -> Dict:
        pass


class OrderCommandHandler(CommandHandler):
    """订单命令处理器"""

    def __init__(self, write_db: "WriteDatabase", event_publisher: "EventPublisher"):
        self._write_db = write_db
        self._event_publisher = event_publisher

    async def handle(self, command: Command) -> Dict:
        """处理命令"""
        if isinstance(command, CreateOrderCommand):
            return await self._handle_create_order(command)
        elif isinstance(command, UpdateOrderStatusCommand):
            return await self._handle_update_status(command)
        elif isinstance(command, CancelOrderCommand):
            return await self._handle_cancel_order(command)
        else:
            return {"success": False, "error": "未知命令类型"}

    async def _handle_create_order(self, command: CreateOrderCommand) -> Dict:
        """处理创建订单"""
        # 1. 验证
        if not command.items:
            return {"success": False, "error": "订单项不能为空"}

        # 2. 计算总价
        total_amount = sum(
            Decimal(str(item["price"])) * item["quantity"]
            for item in command.items
        )

        # 3. 创建订单（写模型）
        order_id = f"ORD{uuid4().hex[:12].upper()}"
        order = {
            "id": order_id,
            "customer_id": command.customer_id,
            "items": command.items,
            "total_amount": float(total_amount),
            "status": "created",
            "shipping_address": command.shipping_address,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        # 4. 保存到写数据库
        await self._write_db.save_order(order)

        # 5. 发布事件
        await self._event_publisher.publish("order.created", {
            "order_id": order_id,
            "customer_id": command.customer_id,
            "total_amount": float(total_amount),
            "items_count": len(command.items)
        })

        return {"success": True, "order_id": order_id}

    async def _handle_update_status(self, command: UpdateOrderStatusCommand) -> Dict:
        """处理更新状态"""
        order = await self._write_db.get_order(command.order_id)
        if not order:
            return {"success": False, "error": "订单不存在"}

        # 状态机验证
        valid_transitions = {
            "created": ["confirmed", "cancelled"],
            "confirmed": ["paid", "cancelled"],
            "paid": ["shipped"],
            "shipped": ["delivered"],
            "delivered": [],
            "cancelled": []
        }

        current_status = order["status"]
        if command.new_status not in valid_transitions.get(current_status, []):
            return {
                "success": False,
                "error": f"不能从 {current_status} 转换到 {command.new_status}"
            }

        # 更新状态
        order["status"] = command.new_status
        order["updated_at"] = datetime.now().isoformat()
        await self._write_db.save_order(order)

        # 发布事件
        await self._event_publisher.publish(f"order.{command.new_status}", {
            "order_id": command.order_id,
            "previous_status": current_status,
            "new_status": command.new_status,
            "reason": command.reason
        })

        return {"success": True}

    async def _handle_cancel_order(self, command: CancelOrderCommand) -> Dict:
        """处理取消订单"""
        update_cmd = UpdateOrderStatusCommand(
            order_id=command.order_id,
            new_status="cancelled",
            reason=command.reason
        )
        return await self._handle_update_status(update_cmd)


# ==================== 查询端 ====================

@dataclass
class Query:
    """查询基类"""
    query_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class GetOrderQuery(Query):
    """获取订单查询"""
    order_id: str = ""


@dataclass
class ListOrdersQuery(Query):
    """列出订单查询"""
    customer_id: str = ""
    status: str = ""
    page: int = 1
    page_size: int = 10


@dataclass
class GetOrderStatisticsQuery(Query):
    """获取订单统计查询"""
    start_date: str = ""
    end_date: str = ""


class QueryHandler(ABC):
    """查询处理器接口"""

    @abstractmethod
    async def handle(self, query: Query) -> Any:
        pass


class OrderQueryHandler(QueryHandler):
    """订单查询处理器"""

    def __init__(self, read_db: "ReadDatabase"):
        self._read_db = read_db

    async def handle(self, query: Query) -> Any:
        """处理查询"""
        if isinstance(query, GetOrderQuery):
            return await self._handle_get_order(query)
        elif isinstance(query, ListOrdersQuery):
            return await self._handle_list_orders(query)
        elif isinstance(query, GetOrderStatisticsQuery):
            return await self._handle_get_statistics(query)
        else:
            return {"success": False, "error": "未知查询类型"}

    async def _handle_get_order(self, query: GetOrderQuery) -> Dict:
        """处理获取订单"""
        order = await self._read_db.get_order(query.order_id)
        if order:
            return {"success": True, "data": order}
        return {"success": False, "error": "订单不存在"}

    async def _handle_list_orders(self, query: ListOrdersQuery) -> Dict:
        """处理列出订单"""
        orders = await self._read_db.list_orders(
            customer_id=query.customer_id,
            status=query.status,
            page=query.page,
            page_size=query.page_size
        )
        return {"success": True, "data": orders, "total": len(orders)}

    async def _handle_get_statistics(self, query: GetOrderStatisticsQuery) -> Dict:
        """处理获取统计"""
        stats = await self._read_db.get_statistics(
            start_date=query.start_date,
            end_date=query.end_date
        )
        return {"success": True, "data": stats}


# ==================== 数据库（模拟）====================

class WriteDatabase:
    """写数据库 - 规范化存储"""

    def __init__(self):
        self._orders: Dict[str, dict] = {}

    async def save_order(self, order: dict) -> None:
        """保存订单"""
        self._orders[order["id"]] = order
        print(f"[WriteDB] 订单保存: {order['id']}")

    async def get_order(self, order_id: str) -> Optional[dict]:
        """获取订单"""
        return self._orders.get(order_id)


class ReadDatabase:
    """读数据库 - 为查询优化的视图"""

    def __init__(self):
        # 为不同查询优化的视图
        self._order_views: Dict[str, dict] = {}  # 订单详情视图
        self._customer_orders: Dict[str, List[str]] = {}  # 客户订单索引
        self._status_orders: Dict[str, List[str]] = {}  # 状态订单索引
        self._statistics: Dict[str, dict] = {}  # 统计视图

    async def update_from_event(self, event_type: str, event_data: dict) -> None:
        """从事件更新读模型"""
        if event_type == "order.created":
            order_id = event_data["order_id"]
            # 创建视图
            self._order_views[order_id] = {
                "id": order_id,
                "customer_id": event_data["customer_id"],
                "total_amount": event_data["total_amount"],
                "status": "created",
                "items_count": event_data["items_count"]
            }

            # 更新索引
            customer_id = event_data["customer_id"]
            if customer_id not in self._customer_orders:
                self._customer_orders[customer_id] = []
            self._customer_orders[customer_id].append(order_id)

            if "created" not in self._status_orders:
                self._status_orders["created"] = []
            self._status_orders["created"].append(order_id)

            print(f"[ReadDB] 视图更新: order.created - {order_id}")

        elif event_type.startswith("order.") and event_type != "order.created":
            order_id = event_data["order_id"]
            new_status = event_data["new_status"]
            previous_status = event_data["previous_status"]

            # 更新视图
            if order_id in self._order_views:
                self._order_views[order_id]["status"] = new_status

            # 更新状态索引
            if previous_status in self._status_orders:
                if order_id in self._status_orders[previous_status]:
                    self._status_orders[previous_status].remove(order_id)

            if new_status not in self._status_orders:
                self._status_orders[new_status] = []
            self._status_orders[new_status].append(order_id)

            print(f"[ReadDB] 视图更新: {event_type} - {order_id}")

    async def get_order(self, order_id: str) -> Optional[dict]:
        """获取订单视图"""
        return self._order_views.get(order_id)

    async def list_orders(
        self,
        customer_id: str = "",
        status: str = "",
        page: int = 1,
        page_size: int = 10
    ) -> List[dict]:
        """列出订单"""
        result = list(self._order_views.values())

        if customer_id:
            result = [o for o in result if o["customer_id"] == customer_id]

        if status:
            result = [o for o in result if o["status"] == status]

        # 分页
        start = (page - 1) * page_size
        return result[start:start + page_size]

    async def get_statistics(self, start_date: str = "", end_date: str = "") -> dict:
        """获取统计"""
        total_orders = len(self._order_views)

        status_counts = {}
        for order in self._order_views.values():
            status = order["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

        total_amount = sum(o["total_amount"] for o in self._order_views.values())

        return {
            "total_orders": total_orders,
            "status_distribution": status_counts,
            "total_amount": total_amount
        }


# ==================== 事件发布器 ====================

class EventPublisher:
    """事件发布器"""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._all_events: List[tuple] = []

    async def publish(self, event_type: str, event_data: dict) -> None:
        """发布事件"""
        self._all_events.append((event_type, event_data))
        print(f"[Event] {event_type}: {json.dumps(event_data, ensure_ascii=False)}")

        # 通知订阅者
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                await handler(event_type, event_data)
            except Exception as e:
                print(f"[Event] 处理器错误: {e}")

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """订阅事件"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)


# ==================== CQRS 门面 ====================

class CqrsFacade:
    """CQRS门面 - 统一入口"""

    def __init__(self):
        # 数据库
        self.write_db = WriteDatabase()
        self.read_db = ReadDatabase()

        # 事件发布器
        self.event_publisher = EventPublisher()

        # 处理器
        self.command_handler = OrderCommandHandler(self.write_db, self.event_publisher)
        self.query_handler = OrderQueryHandler(self.read_db)

        # 设置事件同步
        self._setup_event_sync()

    def _setup_event_sync(self) -> None:
        """设置事件同步到读模型"""
        async def sync_handler(event_type: str, event_data: dict):
            await self.read_db.update_from_event(event_type, event_data)

        self.event_publisher.subscribe("order.created", sync_handler)
        self.event_publisher.subscribe("order.confirmed", sync_handler)
        self.event_publisher.subscribe("order.paid", sync_handler)
        self.event_publisher.subscribe("order.shipped", sync_handler)
        self.event_publisher.subscribe("order.delivered", sync_handler)
        self.event_publisher.subscribe("order.cancelled", sync_handler)

    async def execute_command(self, command: Command) -> Dict:
        """执行命令"""
        return await self.command_handler.handle(command)

    async def execute_query(self, query: Query) -> Any:
        """执行查询"""
        return await self.query_handler.handle(query)


# ==================== 运行示例 ====================

async def main():
    print("=" * 60)
    print("CQRS演示 - 订单管理系统")
    print("=" * 60)

    cqrs = CqrsFacade()

    # 1. 创建订单（命令）
    print("\n1. 创建订单:")
    create_cmd = CreateOrderCommand(
        customer_id="C001",
        items=[
            {"product_id": "P001", "name": "商品A", "price": 100, "quantity": 2},
            {"product_id": "P002", "name": "商品B", "price": 200, "quantity": 1}
        ],
        shipping_address="北京市"
    )
    result1 = await cqrs.execute_command(create_cmd)
    print(f"  结果: {result1}")
    order_id = result1.get("order_id")

    # 2. 创建更多订单
    print("\n2. 创建更多订单:")
    for i in range(3):
        cmd = CreateOrderCommand(
            customer_id=f"C00{i+1}",
            items=[{"product_id": f"P00{i+1}", "name": f"商品{i+1}", "price": (i+1)*100, "quantity": 1}],
            shipping_address=f"地址{i+1}"
        )
        await cqrs.execute_command(cmd)

    # 3. 查询订单（查询）
    print("\n3. 查询订单:")
    get_query = GetOrderQuery(order_id=order_id)
    result3 = await cqrs.execute_query(get_query)
    print(f"  结果: {result3}")

    # 4. 列出订单（查询）
    print("\n4. 列出所有订单:")
    list_query = ListOrdersQuery(page=1, page_size=10)
    result4 = await cqrs.execute_query(list_query)
    print(f"  结果: {json.dumps(result4, indent=2, ensure_ascii=False)}")

    # 5. 更新订单状态（命令）
    print("\n5. 确认订单:")
    update_cmd = UpdateOrderStatusCommand(
        order_id=order_id,
        new_status="confirmed",
        reason="客户确认"
    )
    result5 = await cqrs.execute_command(update_cmd)
    print(f"  结果: {result5}")

    # 6. 获取统计（查询）
    print("\n6. 订单统计:")
    stats_query = GetOrderStatisticsQuery()
    result6 = await cqrs.execute_query(stats_query)
    print(f"  结果: {json.dumps(result6, indent=2, ensure_ascii=False)}")

    # 7. 再次查询，验证读模型已更新
    print("\n7. 再次查询订单（验证读模型更新）:")
    result7 = await cqrs.execute_query(get_query)
    print(f"  结果: {result7}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

### 3.3 事件总线

```python
"""
事件总线实现 - 支持多种模式
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Callable, Optional, Any, Set
from enum import Enum, auto
from collections import defaultdict
import asyncio
import json
import uuid


class DeliveryMode(Enum):
    """投递模式"""
    AT_MOST_ONCE = auto()   # 最多一次（可能丢失）
    AT_LEAST_ONCE = auto()  # 至少一次（可能重复）
    EXACTLY_ONCE = auto()   # 恰好一次（最难实现）


@dataclass
class Event:
    """事件"""
    type: str
    payload: Dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    correlation_id: str = ""
    source: str = ""
    priority: int = 5  # 1-10, 10为最高


class EventHandler(ABC):
    """事件处理器接口"""

    @abstractmethod
    async def handle(self, event: Event) -> None:
        pass

    @property
    @abstractmethod
    def event_types(self) -> List[str]:
        """订阅的事件类型"""
        pass


class EventBus(ABC):
    """事件总线接口"""

    @abstractmethod
    async def publish(self, event: Event) -> None:
        """发布事件"""
        pass

    @abstractmethod
    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """订阅事件"""
        pass

    @abstractmethod
    def unsubscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """取消订阅"""
        pass


class InMemoryEventBus(EventBus):
    """内存事件总线"""

    def __init__(self, delivery_mode: DeliveryMode = DeliveryMode.AT_LEAST_ONCE):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._delivery_mode = delivery_mode
        self._event_history: List[Event] = []
        self._processed_events: Set[str] = set()  # 用于去重

    async def publish(self, event: Event) -> None:
        """发布事件"""
        self._event_history.append(event)

        print(f"[EventBus] 发布事件: {event.type} (id={event.event_id})")

        # 获取订阅者
        handlers = self._subscribers.get(event.type, [])

        # 按优先级排序
        if event.priority >= 8:
            # 高优先级事件同步处理
            for handler in handlers:
                await self._invoke_handler(handler, event)
        else:
            # 普通事件异步处理
            tasks = [self._invoke_handler(handler, event) for handler in handlers]
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _invoke_handler(self, handler: Callable, event: Event) -> None:
        """调用处理器"""
        # 恰好一次语义：检查是否已处理
        if self._delivery_mode == DeliveryMode.EXACTLY_ONCE:
            if event.event_id in self._processed_events:
                print(f"[EventBus] 事件已处理，跳过: {event.event_id}")
                return

        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)

            # 标记为已处理
            if self._delivery_mode == DeliveryMode.EXACTLY_ONCE:
                self._processed_events.add(event.event_id)

        except Exception as e:
            print(f"[EventBus] 处理器错误: {e}")
            # 至少一次语义：重试
            if self._delivery_mode == DeliveryMode.AT_LEAST_ONCE:
                await asyncio.sleep(0.1)
                await self._invoke_handler(handler, event)

    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """订阅事件"""
        self._subscribers[event_type].append(handler)
        print(f"[EventBus] 订阅: {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """取消订阅"""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                h for h in self._subscribers[event_type] if h != handler
            ]

    def get_stats(self) -> dict:
        """获取统计"""
        return {
            "total_events": len(self._event_history),
            "subscribed_types": list(self._subscribers.keys()),
            "subscriber_counts": {
                t: len(h) for t, h in self._subscribers.items()
            }
        }


# ==================== 事件处理器示例 ====================

class OrderEventHandler:
    """订单事件处理器"""

    def __init__(self):
        self.processed_orders: List[str] = []

    async def on_order_created(self, event: Event) -> None:
        """处理订单创建事件"""
        order_id = event.payload.get("order_id")
        self.processed_orders.append(order_id)
        print(f"[Handler] 订单创建处理: {order_id}")

    async def on_order_paid(self, event: Event) -> None:
        """处理订单支付事件"""
        order_id = event.payload.get("order_id")
        print(f"[Handler] 订单支付处理: {order_id}")
        # 发送通知
        await self._send_notification(order_id, "支付成功")

    async def _send_notification(self, order_id: str, message: str) -> None:
        """发送通知"""
        print(f"[Notification] 订单 {order_id}: {message}")


class InventoryEventHandler:
    """库存事件处理器"""

    async def on_order_created(self, event: Event) -> None:
        """处理订单创建事件 - 扣减库存"""
        items = event.payload.get("items", [])
        for item in items:
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            print(f"[Inventory] 扣减库存: {product_id} x {quantity}")

    async def on_order_cancelled(self, event: Event) -> None:
        """处理订单取消事件 - 恢复库存"""
        order_id = event.payload.get("order_id")
        print(f"[Inventory] 恢复库存: 订单 {order_id}")


class AnalyticsEventHandler:
    """分析事件处理器"""

    def __init__(self):
        self.event_counts: Dict[str, int] = defaultdict(int)

    async def handle_all(self, event: Event) -> None:
        """处理所有事件"""
        self.event_counts[event.type] += 1
        print(f"[Analytics] 事件统计: {event.type} = {self.event_counts[event.type]}")


# ==================== 领域事件集成 ====================

class DomainEventPublisher:
    """领域事件发布器 - 集成事件总线"""

    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    async def publish_domain_event(
        self,
        event_type: str,
        payload: dict,
        correlation_id: str = "",
        source: str = ""
    ) -> None:
        """发布领域事件"""
        event = Event(
            type=event_type,
            payload=payload,
            correlation_id=correlation_id,
            source=source
        )
        await self._event_bus.publish(event)


# ==================== 运行示例 ====================

async def main():
    print("=" * 60)
    print("事件总线演示")
    print("=" * 60)

    # 创建事件总线
    event_bus = InMemoryEventBus(delivery_mode=DeliveryMode.AT_LEAST_ONCE)

    # 创建处理器
    order_handler = OrderEventHandler()
    inventory_handler = InventoryEventHandler()
    analytics_handler = AnalyticsEventHandler()

    # 订阅事件
    event_bus.subscribe("order.created", order_handler.on_order_created)
    event_bus.subscribe("order.paid", order_handler.on_order_paid)
    event_bus.subscribe("order.created", inventory_handler.on_order_created)
    event_bus.subscribe("order.cancelled", inventory_handler.on_order_cancelled)
    event_bus.subscribe("order.created", analytics_handler.handle_all)
    event_bus.subscribe("order.paid", analytics_handler.handle_all)

    # 发布事件
    print("\n1. 发布订单创建事件:")
    await event_bus.publish(Event(
        type="order.created",
        payload={
            "order_id": "ORD001",
            "customer_id": "C001",
            "items": [
                {"product_id": "P001", "quantity": 2},
                {"product_id": "P002", "quantity": 1}
            ],
            "total_amount": 500
        }
    ))

    print("\n2. 发布订单支付事件:")
    await event_bus.publish(Event(
        type="order.paid",
        payload={
            "order_id": "ORD001",
            "payment_method": "alipay",
            "amount": 500
        }
    ))

    print("\n3. 发布订单取消事件:")
    await event_bus.publish(Event(
        type="order.cancelled",
        payload={
            "order_id": "ORD001",
            "reason": "客户取消"
        }
    ))

    # 统计
    print("\n4. 事件总线统计:")
    print(json.dumps(event_bus.get_stats(), indent=2, ensure_ascii=False))

    print("\n5. 分析统计:")
    print(json.dumps(dict(analytics_handler.event_counts), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
```

---

### 3.4 Saga编排

```python
"""
Saga模式实现 - 分布式事务协调
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from enum import Enum, auto
from uuid import uuid4
import asyncio
import json


class SagaStatus(Enum):
    """Saga状态"""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    COMPENSATING = auto()
    COMPENSATED = auto()
    FAILED = auto()


class StepStatus(Enum):
    """步骤状态"""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    COMPENSATING = auto()
    COMPENSATED = auto()


@dataclass
class SagaLog:
    """Saga日志"""
    step_name: str
    action: str  # execute/compensate
    status: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    error: str = ""


@dataclass
class SagaContext:
    """Saga上下文"""
    saga_id: str
    payload: Dict[str, Any] = field(default_factory=dict)
    results: Dict[str, Any] = field(default_factory=dict)
    logs: List[SagaLog] = field(default_factory=list)

    def log(self, step_name: str, action: str, status: str, error: str = ""):
        """记录日志"""
        self.logs.append(SagaLog(step_name, action, status, error=error))


class SagaStep(ABC):
    """Saga步骤基类"""

    def __init__(self, name: str):
        self.name = name
        self.status = StepStatus.PENDING
        self.compensation_data: Any = None

    @abstractmethod
    async def execute(self, context: SagaContext) -> bool:
        """执行步骤"""
        pass

    @abstractmethod
    async def compensate(self, context: SagaContext) -> bool:
        """补偿步骤"""
        pass


class Saga:
    """Saga编排器"""

    def __init__(self, name: str):
        self.name = name
        self.saga_id = str(uuid4())
        self.steps: List[SagaStep] = []
        self.status = SagaStatus.PENDING
        self.current_step_index = 0
        self.on_complete: Optional[Callable] = None
        self.on_failure: Optional[Callable] = None

    def add_step(self, step: SagaStep) -> "Saga":
        """添加步骤"""
        self.steps.append(step)
        return self

    async def execute(self, payload: Dict[str, Any]) -> SagaContext:
        """执行Saga"""
        context = SagaContext(saga_id=self.saga_id, payload=payload)
        self.status = SagaStatus.RUNNING

        print(f"\n[Saga] 开始执行: {self.name} (id={self.saga_id})")

        for i, step in enumerate(self.steps):
            self.current_step_index = i
            step.status = StepStatus.RUNNING

            print(f"[Saga] 执行步骤 {i+1}/{len(self.steps)}: {step.name}")

            try:
                success = await step.execute(context)

                if success:
                    step.status = StepStatus.COMPLETED
                    context.log(step.name, "execute", "success")
                    print(f"[Saga] 步骤成功: {step.name}")
                else:
                    step.status = StepStatus.FAILED
                    context.log(step.name, "execute", "failed")
                    print(f"[Saga] 步骤失败: {step.name}")

                    # 触发补偿
                    await self._compensate(context, i)
                    return context

            except Exception as e:
                step.status = StepStatus.FAILED
                context.log(step.name, "execute", "error", str(e))
                print(f"[Saga] 步骤异常: {step.name} - {e}")

                # 触发补偿
                await self._compensate(context, i)
                return context

        # 所有步骤成功
        self.status = SagaStatus.COMPLETED
        print(f"[Saga] 执行完成: {self.name}")

        if self.on_complete:
            await self.on_complete(context)

        return context

    async def _compensate(self, context: SagaContext, failed_step_index: int) -> None:
        """执行补偿"""
        self.status = SagaStatus.COMPENSATING
        print(f"\n[Saga] 开始补偿...")

        # 逆序补偿已完成的步骤
        for i in range(failed_step_index - 1, -1, -1):
            step = self.steps[i]
            if step.status == StepStatus.COMPLETED:
                print(f"[Saga] 补偿步骤: {step.name}")

                try:
                    success = await step.compensate(context)
                    if success:
                        step.status = StepStatus.COMPENSATED
                        context.log(step.name, "compensate", "success")
                    else:
                        context.log(step.name, "compensate", "failed")
                        print(f"[Saga] 补偿失败: {step.name}")
                except Exception as e:
                    context.log(step.name, "compensate", "error", str(e))
                    print(f"[Saga] 补偿异常: {step.name} - {e}")

        self.status = SagaStatus.COMPENSATED
        print(f"[Saga] 补偿完成")

        if self.on_failure:
            await self.on_failure(context)


# ==================== 具体步骤实现 ====================

class CreateOrderStep(SagaStep):
    """创建订单步骤"""

    def __init__(self):
        super().__init__("CreateOrder")

    async def execute(self, context: SagaContext) -> bool:
        """创建订单"""
        customer_id = context.payload.get("customer_id")
        items = context.payload.get("items", [])

        # 模拟创建订单
        await asyncio.sleep(0.1)
        order_id = f"ORD{uuid4().hex[:8].upper()}"

        context.results["order_id"] = order_id
        self.compensation_data = order_id

        print(f"  [Step] 订单创建: {order_id}")
        return True

    async def compensate(self, context: SagaContext) -> bool:
        """取消订单"""
        order_id = self.compensation_data

        # 模拟取消订单
        await asyncio.sleep(0.1)

        print(f"  [Compensate] 订单取消: {order_id}")
        return True


class ReserveInventoryStep(SagaStep):
    """预留库存步骤"""

    def __init__(self, fail_probability: float = 0):
        super().__init__("ReserveInventory")
        self._fail_probability = fail_probability

    async def execute(self, context: SagaContext) -> bool:
        """预留库存"""
        items = context.payload.get("items", [])

        # 模拟预留库存
        await asyncio.sleep(0.1)

        # 模拟失败
        import random
        if random.random() < self._fail_probability:
            print(f"  [Step] 库存预留失败")
            return False

        reservation_id = f"RES{uuid4().hex[:8].upper()}"
        context.results["reservation_id"] = reservation_id
        self.compensation_data = {"reservation_id": reservation_id, "items": items}

        print(f"  [Step] 库存预留: {reservation_id}")
        return True

    async def compensate(self, context: SagaContext) -> bool:
        """释放库存"""
        reservation_id = self.compensation_data["reservation_id"]

        # 模拟释放库存
        await asyncio.sleep(0.1)

        print(f"  [Compensate] 库存释放: {reservation_id}")
        return True


class ProcessPaymentStep(SagaStep):
    """处理支付步骤"""

    def __init__(self, fail_probability: float = 0):
        super().__init__("ProcessPayment")
        self._fail_probability = fail_probability

    async def execute(self, context: SagaContext) -> bool:
        """处理支付"""
        order_id = context.results.get("order_id")
        amount = sum(
            item.get("price", 0) * item.get("quantity", 1)
            for item in context.payload.get("items", [])
        )

        # 模拟支付处理
        await asyncio.sleep(0.1)

        # 模拟失败
        import random
        if random.random() < self._fail_probability:
            print(f"  [Step] 支付失败")
            return False

        payment_id = f"PAY{uuid4().hex[:8].upper()}"
        context.results["payment_id"] = payment_id
        context.results["amount"] = amount
        self.compensation_data = payment_id

        print(f"  [Step] 支付成功: {payment_id}, 金额: {amount}")
        return True

    async def compensate(self, context: SagaContext) -> bool:
        """退款"""
        payment_id = self.compensation_data

        # 模拟退款
        await asyncio.sleep(0.1)

        print(f"  [Compensate] 退款: {payment_id}")
        return True


class SendNotificationStep(SagaStep):
    """发送通知步骤"""

    def __init__(self):
        super().__init__("SendNotification")

    async def execute(self, context: SagaContext) -> bool:
        """发送通知"""
        order_id = context.results.get("order_id")

        # 模拟发送通知
        await asyncio.sleep(0.05)

        print(f"  [Step] 通知发送: 订单 {order_id} 已确认")
        return True

    async def compensate(self, context: SagaContext) -> bool:
        """无需补偿"""
        return True


# ==================== Saga工厂 ====================

class OrderSagaFactory:
    """订单Saga工厂"""

    @staticmethod
    def create_order_saga(inventory_fail: float = 0, payment_fail: float = 0) -> Saga:
        """创建订单Saga"""
        saga = Saga("CreateOrderSaga")

        saga.add_step(CreateOrderStep())
        saga.add_step(ReserveInventoryStep(fail_probability=inventory_fail))
        saga.add_step(ProcessPaymentStep(fail_probability=payment_fail))
        saga.add_step(SendNotificationStep())

        return saga


# ==================== 运行示例 ====================

async def main():
    print("=" * 60)
    print("Saga模式演示 - 分布式事务")
    print("=" * 60)

    # 场景1: 成功场景
    print("\n场景1: 订单流程成功")
    saga1 = OrderSagaFactory.create_order_saga()
    context1 = await saga1.execute({
        "customer_id": "C001",
        "items": [
            {"product_id": "P001", "price": 100, "quantity": 2},
            {"product_id": "P002", "price": 200, "quantity": 1}
        ]
    })
    print(f"结果: {saga1.status.name}")
    print(f"上下文: {json.dumps(context1.results, indent=2, ensure_ascii=False)}")

    # 场景2: 库存不足
    print("\n场景2: 库存不足（触发补偿）")
    saga2 = OrderSagaFactory.create_order_saga(inventory_fail=1.0)
    context2 = await saga2.execute({
        "customer_id": "C002",
        "items": [{"product_id": "P003", "price": 500, "quantity": 1}]
    })
    print(f"结果: {saga2.status.name}")

    # 场景3: 支付失败
    print("\n场景3: 支付失败（触发补偿）")
    saga3 = OrderSagaFactory.create_order_saga(payment_fail=1.0)
    context3 = await saga3.execute({
        "customer_id": "C003",
        "items": [{"product_id": "P004", "price": 1000, "quantity": 1}]
    })
    print(f"结果: {saga3.status.name}")


if __name__ == "__main__":
    asyncio.run(main())
```

---


## 第四部分：领域驱动设计（DDD）

### 4.1 战略设计

#### 概念定义

战略设计关注宏观层面的领域划分和团队协作：

- **限界上下文（Bounded Context）**：领域的边界，内部使用统一语言
- **上下文映射（Context Mapping）**：不同上下文之间的关系
- **通用语言（Ubiquitous Language）**：团队共享的领域术语

#### 限界上下文

```
┌─────────────────────────────────────────────────────────────┐
│                      电商平台                                 │
├─────────────────┬─────────────────┬─────────────────────────┤
│  商品上下文      │   订单上下文     │   库存上下文            │
│  (Product BC)   │   (Order BC)    │   (Inventory BC)       │
├─────────────────┼─────────────────┼─────────────────────────┤
│ • Product       │ • Order         │ • Stock                │
│ • Category      │ • OrderItem     │ • Reservation          │
│ • Price         │ • OrderStatus   │ • Warehouse            │
│ • Review        │ • Payment       │ • Replenishment        │
├─────────────────┴─────────────────┴─────────────────────────┤
│  每个上下文有自己的模型，术语可能不同                          │
│  例如：Product在商品上下文是商品，在订单上下文是OrderItem       │
└─────────────────────────────────────────────────────────────┘
```

#### 上下文映射模式

```
┌─────────────────────────────────────────────────────────────┐
│                      上下文映射模式                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 合作关系 (Partnership)                                   │
│     ┌─────┐◄─────────────►┌─────┐                          │
│     │ BC1 │  紧密协作      │ BC2 │                          │
│     └─────┘               └─────┘                          │
│                                                             │
│  2. 共享内核 (Shared Kernel)                                 │
│     ┌─────┐   ┌─────────┐   ┌─────┐                        │
│     │ BC1 │◄─►│ Shared  │◄─►│ BC2 │                        │
│     └─────┘   │  Kernel │   └─────┘                        │
│               └─────────┘                                   │
│                                                             │
│  3. 客户-供应商 (Customer-Supplier)                          │
│     ┌─────────┐  上游(供应)   ┌─────────┐                   │
│     │Supplier │─────────────►│Customer │                   │
│     └─────────┘              └─────────┘                   │
│                                                             │
│  4. 遵奉者 (Conformist)                                      │
│     ┌─────────┐  上游主导    ┌─────────┐                    │
│     │Upstream │─────────────►│Downstream│                   │
│     └─────────┘  下游遵奉    └─────────┘                    │
│                                                             │
│  5. 防腐层 (Anti-Corruption Layer)                           │
│     ┌─────────┐  ┌─────┐    ┌─────────┐                    │
│     │   BC1   │◄─►│ ACL │◄──►│   BC2   │                    │
│     └─────────┘  └─────┘    └─────────┘                    │
│                  防腐层转换                                  │
│                                                             │
│  6. 开放主机服务 (Open Host Service)                         │
│     ┌─────────┐  公开API    ┌─────────┐                    │
│     │   BC1   │◄──────────►│  BC2,3..│                    │
│     └─────────┘            └─────────┘                     │
│                                                             │
│  7. 发布语言 (Published Language)                            │
│     使用统一的交换格式（如JSON Schema）                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 4.2 战术设计

#### 概念定义

战术设计关注微观层面的领域模型构建：

| 概念 | 定义 | 特征 |
|------|------|------|
| **实体（Entity）** | 有唯一标识的对象 | ID相等即相等 |
| **值对象（Value Object）** | 无标识，由属性定义 | 不可变，可替换 |
| **聚合（Aggregate）** | 一致性边界内的实体和值对象 | 根实体控制访问 |
| **领域服务（Domain Service）** | 跨实体的业务逻辑 | 无状态 |
| **仓储（Repository）** | 聚合的持久化抽象 | 类似集合接口 |
| **工厂（Factory）** | 复杂对象的创建逻辑 | 封装创建细节 |

#### 实体 vs 值对象

```
实体 (Entity):                    值对象 (Value Object):
┌─────────────┐                   ┌─────────────┐
│   User      │                   │   Address   │
├─────────────┤                   ├─────────────┤
│ id: UUID    │◄── 唯一标识        │ street: str │
│ name: str   │                   │ city: str   │
│ email: str  │                   │ zip: str    │
│ address:    │                   │ country: str│
│   Address   │                   └─────────────┘
└─────────────┘                        │
     │                                 │
     ▼                                 ▼
  修改name，                           修改city，
  还是同一个User                       就是新的Address
```

---

### 4.3 Python DDD实现

```python
"""
领域驱动设计完整实现 - 电商订单系统
包含：实体、值对象、聚合、领域服务、仓储、工厂
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Optional, Set, Callable
from enum import Enum, auto
from uuid import uuid4, UUID
import json
import copy


# ==================== 值对象 ====================

@dataclass(frozen=True)
class Money:
    """金额值对象 - 不可变"""
    amount: Decimal
    currency: str = "CNY"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("金额不能为负数")

    def add(self, other: "Money") -> "Money":
        """加法"""
        if self.currency != other.currency:
            raise ValueError("货币类型不匹配")
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        """减法"""
        if self.currency != other.currency:
            raise ValueError("货币类型不匹配")
        if self.amount < other.amount:
            raise ValueError("余额不足")
        return Money(self.amount - other.amount, self.currency)

    def multiply(self, factor: int) -> "Money":
        """乘法"""
        return Money(self.amount * factor, self.currency)

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"


@dataclass(frozen=True)
class Address:
    """地址值对象"""
    province: str
    city: str
    district: str
    street: str
    zip_code: str
    recipient_name: str
    recipient_phone: str

    def __str__(self) -> str:
        return f"{self.province}{self.city}{self.district}{self.street}"


@dataclass(frozen=True)
class ProductSnapshot:
    """产品快照值对象 - 记录下单时的产品信息"""
    product_id: str
    name: str
    price: Money

    def __str__(self) -> str:
        return f"{self.name} ({self.price})"


# ==================== 实体 ====================

class Entity:
    """实体基类"""

    def __init__(self, entity_id: str):
        self._id = entity_id

    @property
    def id(self) -> str:
        return self._id

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)


class Customer(Entity):
    """客户实体"""

    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        super().__init__(customer_id)
        self._name = name
        self._email = email
        self._phone = phone
        self._addresses: List[Address] = []
        self._member_level: str = "normal"
        self._created_at = datetime.now().isoformat()

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def member_level(self) -> str:
        return self._member_level

    def add_address(self, address: Address) -> None:
        """添加地址"""
        self._addresses.append(address)

    def upgrade_member_level(self, new_level: str) -> None:
        """升级会员等级"""
        self._member_level = new_level

    def get_discount_rate(self) -> Decimal:
        """获取折扣率"""
        rates = {
            "normal": Decimal("1.0"),
            "silver": Decimal("0.95"),
            "gold": Decimal("0.90"),
            "platinum": Decimal("0.85")
        }
        return rates.get(self._member_level, Decimal("1.0"))

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "member_level": self._member_level,
            "address_count": len(self._addresses)
        }


class Product(Entity):
    """产品实体"""

    def __init__(self, product_id: str, name: str, price: Money, stock: int):
        super().__init__(product_id)
        self._name = name
        self._price = price
        self._stock = stock
        self._is_active = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> Money:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def reduce_stock(self, quantity: int) -> None:
        """减少库存"""
        if quantity > self._stock:
            raise ValueError("库存不足")
        self._stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """增加库存"""
        self._stock += quantity

    def create_snapshot(self) -> ProductSnapshot:
        """创建快照"""
        return ProductSnapshot(
            product_id=self._id,
            name=self._name,
            price=self._price
        )

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "price": str(self._price),
            "stock": self._stock,
            "is_active": self._is_active
        }


# ==================== 领域事件 ====================

@dataclass
class DomainEvent:
    """领域事件"""
    event_type: str
    aggregate_id: str
    payload: dict
    occurred_on: str = field(default_factory=lambda: datetime.now().isoformat())


# ==================== 聚合根 ====================

class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"           # 待处理
    CONFIRMED = "confirmed"       # 已确认
    PAID = "paid"                 # 已支付
    SHIPPED = "shipped"           # 已发货
    DELIVERED = "delivered"       # 已送达
    CANCELLED = "cancelled"       # 已取消


class OrderLine:
    """订单行 - 聚合内的实体"""

    def __init__(self, line_id: str, product_snapshot: ProductSnapshot, quantity: int):
        self._id = line_id
        self._product_snapshot = product_snapshot
        self._quantity = quantity

    @property
    def subtotal(self) -> Money:
        return self._product_snapshot.price.multiply(self._quantity)

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "product": {
                "id": self._product_snapshot.product_id,
                "name": self._product_snapshot.name,
                "price": str(self._product_snapshot.price)
            },
            "quantity": self._quantity,
            "subtotal": str(self.subtotal)
        }


class Order(Entity):
    """订单聚合根"""

    def __init__(self, order_id: str, customer: Customer):
        super().__init__(order_id)
        self._customer = customer
        self._lines: List[OrderLine] = []
        self._status = OrderStatus.PENDING
        self._shipping_address: Optional[Address] = None
        self._total_amount: Money = Money(Decimal("0"))
        self._discount_amount: Money = Money(Decimal("0"))
        self._created_at = datetime.now().isoformat()
        self._domain_events: List[DomainEvent] = []

    # ========== 聚合根行为 ==========

    def add_line(self, product: Product, quantity: int) -> None:
        """添加订单行"""
        # 业务规则验证
        if self._status != OrderStatus.PENDING:
            raise ValueError("只能向待处理订单添加商品")

        if quantity <= 0:
            raise ValueError("数量必须大于0")

        if product.stock < quantity:
            raise ValueError(f"商品 {product.name} 库存不足")

        # 创建订单行
        line = OrderLine(
            line_id=str(uuid4()),
            product_snapshot=product.create_snapshot(),
            quantity=quantity
        )

        self._lines.append(line)
        self._recalculate_total()

        # 扣减库存
        product.reduce_stock(quantity)

    def remove_line(self, line_id: str) -> None:
        """移除订单行"""
        if self._status != OrderStatus.PENDING:
            raise ValueError("只能修改待处理订单")

        self._lines = [l for l in self._lines if l._id != line_id]
        self._recalculate_total()

    def set_shipping_address(self, address: Address) -> None:
        """设置配送地址"""
        self._shipping_address = address

    def confirm(self) -> None:
        """确认订单"""
        if self._status != OrderStatus.PENDING:
            raise ValueError("只能确认待处理订单")

        if not self._lines:
            raise ValueError("订单不能为空")

        self._status = OrderStatus.CONFIRMED
        self._add_domain_event("order.confirmed", {"order_id": self._id})

    def pay(self) -> None:
        """支付订单"""
        if self._status != OrderStatus.CONFIRMED:
            raise ValueError("只能支付已确认订单")

        self._status = OrderStatus.PAID
        self._add_domain_event("order.paid", {
            "order_id": self._id,
            "amount": str(self._total_amount)
        })

    def ship(self) -> None:
        """发货"""
        if self._status != OrderStatus.PAID:
            raise ValueError("只能发货已支付订单")

        self._status = OrderStatus.SHIPPED
        self._add_domain_event("order.shipped", {"order_id": self._id})

    def deliver(self) -> None:
        """送达"""
        if self._status != OrderStatus.SHIPPED:
            raise ValueError("只能送达已发货订单")

        self._status = OrderStatus.DELIVERED
        self._add_domain_event("order.delivered", {"order_id": self._id})

    def cancel(self, reason: str) -> None:
        """取消订单"""
        if self._status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            raise ValueError("已送达或已取消的订单不能取消")

        self._status = OrderStatus.CANCELLED
        self._add_domain_event("order.cancelled", {
            "order_id": self._id,
            "reason": reason
        })

    def _recalculate_total(self) -> None:
        """重新计算总价"""
        total = Money(Decimal("0"))
        for line in self._lines:
            total = total.add(line.subtotal)

        # 应用会员折扣
        discount_rate = self._customer.get_discount_rate()
        self._discount_amount = Money(total.amount * (Decimal("1") - discount_rate))
        self._total_amount = Money(total.amount * discount_rate)

    def _add_domain_event(self, event_type: str, payload: dict) -> None:
        """添加领域事件"""
        event = DomainEvent(
            event_type=event_type,
            aggregate_id=self._id,
            payload=payload
        )
        self._domain_events.append(event)

    def get_domain_events(self) -> List[DomainEvent]:
        """获取领域事件"""
        return self._domain_events.copy()

    def clear_domain_events(self) -> None:
        """清空领域事件"""
        self._domain_events.clear()

    # ========== 属性访问 ==========

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def total_amount(self) -> Money:
        return self._total_amount

    @property
    def line_count(self) -> int:
        return len(self._lines)

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "customer": self._customer.to_dict(),
            "status": self._status.value,
            "lines": [l.to_dict() for l in self._lines],
            "total_amount": str(self._total_amount),
            "discount_amount": str(self._discount_amount),
            "shipping_address": str(self._shipping_address) if self._shipping_address else None,
            "created_at": self._created_at
        }


# ==================== 领域服务 ====================

class PricingService:
    """定价服务 - 跨实体的业务逻辑"""

    def calculate_order_total(
        self,
        lines: List[OrderLine],
        customer: Customer,
        coupon_code: str = None
    ) -> Money:
        """计算订单总价"""
        subtotal = Money(Decimal("0"))
        for line in lines:
            subtotal = subtotal.add(line.subtotal)

        # 会员折扣
        discount_rate = customer.get_discount_rate()
        after_member_discount = Money(subtotal.amount * discount_rate)

        # 优惠券折扣
        if coupon_code:
            coupon_discount = self._calculate_coupon_discount(coupon_code, after_member_discount)
            after_member_discount = after_member_discount.subtract(coupon_discount)

        return after_member_discount

    def _calculate_coupon_discount(self, coupon_code: str, amount: Money) -> Money:
        """计算优惠券折扣"""
        # 简化实现
        coupons = {
            "SAVE10": Decimal("10"),
            "SAVE50": Decimal("50"),
            "HALF": amount.amount / 2
        }
        discount = coupons.get(coupon_code, Decimal("0"))
        return Money(min(discount, amount.amount))


class InventoryService:
    """库存服务 - 跨聚合的业务逻辑"""

    def __init__(self, product_repo: "ProductRepository"):
        self._product_repo = product_repo

    def check_availability(self, product_id: str, quantity: int) -> bool:
        """检查库存"""
        product = self._product_repo.find_by_id(product_id)
        if not product:
            return False
        return product.stock >= quantity

    def reserve_inventory(self, order: Order) -> bool:
        """预留库存"""
        # 实际实现中可能需要分布式锁
        return True


class OrderDomainService:
    """订单领域服务"""

    def __init__(
        self,
        pricing_service: PricingService,
        inventory_service: InventoryService
    ):
        self._pricing_service = pricing_service
        self._inventory_service = inventory_service

    def validate_order(self, order: Order) -> List[str]:
        """验证订单"""
        errors = []

        if not order.line_count:
            errors.append("订单不能为空")

        if order.total_amount.amount <= 0:
            errors.append("订单金额必须大于0")

        return errors

    def can_cancel(self, order: Order) -> bool:
        """判断订单是否可以取消"""
        return order.status not in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]


# ==================== 仓储 ====================

class CustomerRepository(ABC):
    """客户仓储接口"""

    @abstractmethod
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass


class ProductRepository(ABC):
    """产品仓储接口"""

    @abstractmethod
    def find_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> None:
        pass

    @abstractmethod
    def find_all(self) -> List[Product]:
        pass


class OrderRepository(ABC):
    """订单仓储接口"""

    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def find_by_customer(self, customer_id: str) -> List[Order]:
        pass


# 内存实现
class InMemoryCustomerRepository(CustomerRepository):
    """内存客户仓储"""

    def __init__(self):
        self._customers: Dict[str, Customer] = {}
        # 初始化测试数据
        self._init_test_data()

    def _init_test_data(self):
        customers = [
            Customer("C001", "张三", "zhangsan@example.com", "13800138001"),
            Customer("C002", "李四", "lisi@example.com", "13800138002"),
        ]
        customers[0].upgrade_member_level("gold")
        for c in customers:
            self._customers[c.id] = c

    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        return self._customers.get(customer_id)

    def save(self, customer: Customer) -> None:
        self._customers[customer.id] = customer


class InMemoryProductRepository(ProductRepository):
    """内存产品仓储"""

    def __init__(self):
        self._products: Dict[str, Product] = {}
        self._init_test_data()

    def _init_test_data(self):
        products = [
            Product("P001", "iPhone 15", Money(Decimal("6999")), 100),
            Product("P002", "MacBook Pro", Money(Decimal("14999")), 50),
            Product("P003", "AirPods Pro", Money(Decimal("1999")), 200),
        ]
        for p in products:
            self._products[p.id] = p

    def find_by_id(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def save(self, product: Product) -> None:
        self._products[product.id] = product

    def find_all(self) -> List[Product]:
        return list(self._products.values())


class InMemoryOrderRepository(OrderRepository):
    """内存订单仓储"""

    def __init__(self):
        self._orders: Dict[str, Order] = {}

    def find_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        self._orders[order.id] = order
        print(f"[Repository] 订单保存: {order.id}")

        # 处理领域事件
        events = order.get_domain_events()
        for event in events:
            print(f"[Domain Event] {event.event_type}: {event.payload}")
        order.clear_domain_events()

    def find_by_customer(self, customer_id: str) -> List[Order]:
        return [o for o in self._orders.values() if o._customer.id == customer_id]


# ==================== 工厂 ====================

class OrderFactory:
    """订单工厂"""

    @staticmethod
    def create_order(customer: Customer) -> Order:
        """创建订单"""
        order_id = f"ORD{uuid4().hex[:12].upper()}"
        return Order(order_id, customer)

    @staticmethod
    def create_order_with_items(
        customer: Customer,
        items: List[tuple]  # (product, quantity) 列表
    ) -> Order:
        """创建带商品的订单"""
        order = OrderFactory.create_order(customer)

        for product, quantity in items:
            order.add_line(product, quantity)

        return order


# ==================== 应用服务 ====================

class OrderApplicationService:
    """订单应用服务"""

    def __init__(
        self,
        customer_repo: CustomerRepository,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
        order_domain_service: OrderDomainService
    ):
        self._customer_repo = customer_repo
        self._product_repo = product_repo
        self._order_repo = order_repo
        self._order_domain_service = order_domain_service

    def create_order(self, customer_id: str, items_data: List[dict]) -> dict:
        """创建订单"""
        # 1. 获取客户
        customer = self._customer_repo.find_by_id(customer_id)
        if not customer:
            return {"success": False, "error": "客户不存在"}

        # 2. 创建订单
        order = OrderFactory.create_order(customer)

        # 3. 添加商品
        for item_data in items_data:
            product = self._product_repo.find_by_id(item_data["product_id"])
            if not product:
                return {"success": False, "error": f"商品不存在: {item_data['product_id']}"}

            try:
                order.add_line(product, item_data["quantity"])
            except ValueError as e:
                return {"success": False, "error": str(e)}

        # 4. 验证订单
        errors = self._order_domain_service.validate_order(order)
        if errors:
            return {"success": False, "error": "; ".join(errors)}

        # 5. 保存订单
        self._order_repo.save(order)

        return {
            "success": True,
            "order_id": order.id,
            "total_amount": str(order.total_amount),
            "status": order.status.value
        }

    def confirm_order(self, order_id: str) -> dict:
        """确认订单"""
        order = self._order_repo.find_by_id(order_id)
        if not order:
            return {"success": False, "error": "订单不存在"}

        try:
            order.confirm()
            self._order_repo.save(order)
            return {"success": True, "status": order.status.value}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def pay_order(self, order_id: str) -> dict:
        """支付订单"""
        order = self._order_repo.find_by_id(order_id)
        if not order:
            return {"success": False, "error": "订单不存在"}

        try:
            order.pay()
            self._order_repo.save(order)
            return {"success": True, "status": order.status.value}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def get_order(self, order_id: str) -> dict:
        """获取订单"""
        order = self._order_repo.find_by_id(order_id)
        if not order:
            return {"success": False, "error": "订单不存在"}

        return {"success": True, "data": order.to_dict()}


# ==================== 运行示例 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("领域驱动设计演示 - 电商订单系统")
    print("=" * 60)

    # 初始化仓储
    customer_repo = InMemoryCustomerRepository()
    product_repo = InMemoryProductRepository()
    order_repo = InMemoryOrderRepository()

    # 初始化领域服务
    pricing_service = PricingService()
    inventory_service = InventoryService(product_repo)
    order_domain_service = OrderDomainService(pricing_service, inventory_service)

    # 初始化应用服务
    app_service = OrderApplicationService(
        customer_repo, product_repo, order_repo, order_domain_service
    )

    # 场景1: 创建订单
    print("\n1. 创建订单（金卡会员）:")
    result1 = app_service.create_order(
        customer_id="C001",
        items_data=[
            {"product_id": "P001", "quantity": 1},  # iPhone 15
            {"product_id": "P003", "quantity": 2}   # AirPods Pro x2
        ]
    )
    print(json.dumps(result1, indent=2, ensure_ascii=False))
    order_id = result1.get("order_id")

    # 场景2: 确认订单
    if order_id:
        print("\n2. 确认订单:")
        result2 = app_service.confirm_order(order_id)
        print(json.dumps(result2, indent=2, ensure_ascii=False))

    # 场景3: 支付订单
    if order_id:
        print("\n3. 支付订单:")
        result3 = app_service.pay_order(order_id)
        print(json.dumps(result3, indent=2, ensure_ascii=False))

    # 场景4: 获取订单详情
    if order_id:
        print("\n4. 获取订单详情:")
        result4 = app_service.get_order(order_id)
        print(json.dumps(result4, indent=2, ensure_ascii=False))

    # 场景5: 普通会员订单（无折扣）
    print("\n5. 创建订单（普通会员）:")
    result5 = app_service.create_order(
        customer_id="C002",
        items_data=[
            {"product_id": "P002", "quantity": 1}   # MacBook Pro
        ]
    )
    print(json.dumps(result5, indent=2, ensure_ascii=False))


# ==================== DDD战术设计总结 ====================
"""
DDD战术设计核心概念总结:

1. 实体 (Entity)
   - 有唯一标识
   - 通过ID判断相等
   - 可以修改状态
   - 例如: Customer, Order, Product

2. 值对象 (Value Object)
   - 无唯一标识
   - 通过属性判断相等
   - 不可变
   - 例如: Money, Address, ProductSnapshot

3. 聚合 (Aggregate)
   - 一致性边界
   - 聚合根控制访问
   - 外部只能通过聚合根引用
   - 例如: Order (包含OrderLine)

4. 领域服务 (Domain Service)
   - 跨实体的业务逻辑
   - 无状态
   - 例如: PricingService, OrderDomainService

5. 仓储 (Repository)
   - 聚合的持久化
   - 类似集合接口
   - 屏蔽数据访问细节

6. 工厂 (Factory)
   - 复杂对象创建
   - 封装创建逻辑
   - 例如: OrderFactory

7. 领域事件 (Domain Event)
   - 记录领域变化
   - 用于解耦
   - 例如: order.confirmed, order.paid
"""
```

---


## 第五部分：六边形架构

### 5.1 概念定义

六边形架构（Hexagonal Architecture），又称端口与适配器架构（Ports and Adapters），由Alistair Cockburn提出。核心思想是：

- **应用核心（Application Core）**：包含业务逻辑，不依赖外部
- **端口（Ports）**：定义应用与外部交互的接口
- **适配器（Adapters）**：实现端口，连接外部系统

```
                    ┌─────────────────────────┐
                    │    外部系统 (External)   │
                    │  Web UI / CLI / API     │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   输入适配器 (Inbound)   │
                    │  Controller / Handler   │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │      输入端口            │
                    │   (Inbound Port)        │
                    ├─────────────────────────┤
                    │                         │
                    │    应用核心 (Core)      │
                    │   - 领域逻辑            │
                    │   - 业务规则            │
                    │   - 用例编排            │
                    │                         │
                    ├─────────────────────────┤
                    │      输出端口            │
                    │   (Outbound Port)       │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   输出适配器 (Outbound)  │
                    │ Repository / Client     │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │    外部基础设施          │
                    │  Database / MQ / API    │
                    └─────────────────────────┘
```

### 5.2 核心原则

| 原则 | 说明 |
|------|------|
| **依赖倒置** | 应用核心不依赖外部，外部依赖核心 |
| **端口定义** | 通过接口定义交互契约 |
| **适配器实现** | 具体实现由适配器完成 |
| **可测试性** | 核心逻辑可独立测试 |
| **可替换性** | 适配器可随时替换 |

### 5.3 Python实现

```python
"""
六边形架构完整实现 - 任务管理系统
展示端口、适配器、依赖倒置的核心概念
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable, Any, Protocol
from enum import Enum, auto
from uuid import uuid4
import json
import asyncio


# ═══════════════════════════════════════════════════════════════
# 第一部分：领域核心（Domain Core）- 不依赖任何外部
# ═══════════════════════════════════════════════════════════════

class TaskStatus(Enum):
    """任务状态"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """任务优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass(frozen=True)
class TaskId:
    """任务ID值对象"""
    value: str

    @classmethod
    def generate(cls) -> "TaskId":
        return cls(value=str(uuid4()))


@dataclass(frozen=True)
class TimeRange:
    """时间范围值对象"""
    start: datetime
    end: datetime

    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() / 60)

    def overlaps(self, other: "TimeRange") -> bool:
        return self.start < other.end and other.start < self.end


# ═══════════════════════════════════════════════════════════════
# 领域实体 - 核心业务对象
# ═══════════════════════════════════════════════════════════════

class Task:
    """任务实体"""

    def __init__(
        self,
        task_id: TaskId,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM
    ):
        self._id = task_id
        self._title = title
        self._description = description
        self._priority = priority
        self._status = TaskStatus.TODO
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._completed_at: Optional[datetime] = None
        self._tags: List[str] = []
        self._assignee_id: Optional[str] = None

    # ========== 领域行为 ==========

    def start(self) -> None:
        """开始任务"""
        if self._status != TaskStatus.TODO:
            raise ValueError("只能开始待办任务")
        self._status = TaskStatus.IN_PROGRESS
        self._updated_at = datetime.now()

    def complete(self) -> None:
        """完成任务"""
        if self._status not in [TaskStatus.TODO, TaskStatus.IN_PROGRESS]:
            raise ValueError("只能完成进行中的任务")
        self._status = TaskStatus.DONE
        self._completed_at = datetime.now()
        self._updated_at = datetime.now()

    def cancel(self, reason: str = "") -> None:
        """取消任务"""
        if self._status == TaskStatus.DONE:
            raise ValueError("已完成的任务不能取消")
        self._status = TaskStatus.CANCELLED
        self._updated_at = datetime.now()

    def assign_to(self, user_id: str) -> None:
        """分配给某人"""
        self._assignee_id = user_id
        self._updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        """添加标签"""
        if tag not in self._tags:
            self._tags.append(tag)

    def update_priority(self, priority: TaskPriority) -> None:
        """更新优先级"""
        self._priority = priority
        self._updated_at = datetime.now()

    # ========== 属性访问 ==========

    @property
    def id(self) -> TaskId:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def status(self) -> TaskStatus:
        return self._status

    @property
    def priority(self) -> TaskPriority:
        return self._priority

    @property
    def is_overdue(self) -> bool:
        """是否逾期"""
        # 简化实现
        return False

    def to_dict(self) -> dict:
        return {
            "id": self._id.value,
            "title": self._title,
            "description": self._description,
            "priority": self._priority.name,
            "status": self._status.value,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "completed_at": self._completed_at.isoformat() if self._completed_at else None,
            "tags": self._tags,
            "assignee_id": self._assignee_id
        }


# ═══════════════════════════════════════════════════════════════
# 领域服务 - 跨实体的业务逻辑
# ═══════════════════════════════════════════════════════════════

class TaskDomainService:
    """任务领域服务"""

    def can_assign(self, task: Task, user_id: str) -> bool:
        """判断是否可以分配任务"""
        return task.status != TaskStatus.CANCELLED

    def calculate_workload(self, tasks: List[Task]) -> Dict[str, int]:
        """计算工作量分布"""
        workload = {"todo": 0, "in_progress": 0, "done": 0}
        for task in tasks:
            workload[task.status.value] += 1
        return workload

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """按优先级排序"""
        return sorted(tasks, key=lambda t: t.priority.value, reverse=True)


# ═══════════════════════════════════════════════════════════════
# 第二部分：端口（Ports）- 定义与外部的交互契约
# ═══════════════════════════════════════════════════════════════

# ========== 输入端口（驱动端口）==========

class TaskServicePort(ABC):
    """任务服务端口 - 入站端口"""

    @abstractmethod
    def create_task(self, title: str, description: str, priority: str) -> dict:
        """创建任务"""
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Optional[dict]:
        """获取任务"""
        pass

    @abstractmethod
    def list_tasks(self, status: str = None, assignee: str = None) -> List[dict]:
        """列出任务"""
        pass

    @abstractmethod
    def start_task(self, task_id: str) -> dict:
        """开始任务"""
        pass

    @abstractmethod
    def complete_task(self, task_id: str) -> dict:
        """完成任务"""
        pass

    @abstractmethod
    def assign_task(self, task_id: str, user_id: str) -> dict:
        """分配任务"""
        pass


# ========== 输出端口（被驱动端口）==========

class TaskRepositoryPort(ABC):
    """任务仓储端口 - 出站端口"""

    @abstractmethod
    def find_by_id(self, task_id: TaskId) -> Optional[Task]:
        """根据ID查找任务"""
        pass

    @abstractmethod
    def find_all(self, filters: dict = None) -> List[Task]:
        """查找所有任务"""
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        """保存任务"""
        pass

    @abstractmethod
    def delete(self, task_id: TaskId) -> bool:
        """删除任务"""
        pass


class NotificationPort(ABC):
    """通知端口 - 出站端口"""

    @abstractmethod
    def notify_task_assigned(self, task_id: str, user_id: str, task_title: str) -> None:
        """通知任务分配"""
        pass

    @abstractmethod
    def notify_task_completed(self, task_id: str, task_title: str) -> None:
        """通知任务完成"""
        pass


class LoggingPort(ABC):
    """日志端口 - 出站端口"""

    @abstractmethod
    def log_info(self, message: str, context: dict = None) -> None:
        """记录信息日志"""
        pass

    @abstractmethod
    def log_error(self, message: str, error: Exception = None) -> None:
        """记录错误日志"""
        pass


# ═══════════════════════════════════════════════════════════════
# 第三部分：应用核心实现
# ═══════════════════════════════════════════════════════════════

class TaskApplicationService:
    """任务应用服务 - 实现输入端口"""

    def __init__(
        self,
        task_repo: TaskRepositoryPort,
        notification: NotificationPort,
        logging: LoggingPort,
        domain_service: TaskDomainService
    ):
        # 通过端口依赖外部，不直接依赖具体实现
        self._task_repo = task_repo
        self._notification = notification
        self._logging = logging
        self._domain_service = domain_service

    def create_task(self, title: str, description: str, priority: str) -> dict:
        """创建任务"""
        try:
            self._logging.log_info(f"创建任务: {title}")

            # 解析优先级
            try:
                priority_enum = TaskPriority[priority.upper()]
            except KeyError:
                priority_enum = TaskPriority.MEDIUM

            # 创建任务
            task = Task(
                task_id=TaskId.generate(),
                title=title,
                description=description,
                priority=priority_enum
            )

            # 保存
            self._task_repo.save(task)

            return {
                "success": True,
                "task": task.to_dict()
            }

        except Exception as e:
            self._logging.log_error("创建任务失败", e)
            return {"success": False, "error": str(e)}

    def get_task(self, task_id: str) -> Optional[dict]:
        """获取任务"""
        task = self._task_repo.find_by_id(TaskId(task_id))
        return task.to_dict() if task else None

    def list_tasks(self, status: str = None, assignee: str = None) -> List[dict]:
        """列出任务"""
        filters = {}
        if status:
            filters["status"] = status
        if assignee:
            filters["assignee"] = assignee

        tasks = self._task_repo.find_all(filters)

        # 使用领域服务排序
        sorted_tasks = self._domain_service.sort_by_priority(tasks)

        return [t.to_dict() for t in sorted_tasks]

    def start_task(self, task_id: str) -> dict:
        """开始任务"""
        try:
            task = self._task_repo.find_by_id(TaskId(task_id))
            if not task:
                return {"success": False, "error": "任务不存在"}

            task.start()
            self._task_repo.save(task)

            self._logging.log_info(f"任务开始: {task_id}")

            return {"success": True, "task": task.to_dict()}

        except ValueError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            self._logging.log_error("开始任务失败", e)
            return {"success": False, "error": str(e)}

    def complete_task(self, task_id: str) -> dict:
        """完成任务"""
        try:
            task = self._task_repo.find_by_id(TaskId(task_id))
            if not task:
                return {"success": False, "error": "任务不存在"}

            task.complete()
            self._task_repo.save(task)

            # 发送通知
            self._notification.notify_task_completed(task_id, task.title)

            self._logging.log_info(f"任务完成: {task_id}")

            return {"success": True, "task": task.to_dict()}

        except ValueError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            self._logging.log_error("完成任务失败", e)
            return {"success": False, "error": str(e)}

    def assign_task(self, task_id: str, user_id: str) -> dict:
        """分配任务"""
        try:
            task = self._task_repo.find_by_id(TaskId(task_id))
            if not task:
                return {"success": False, "error": "任务不存在"}

            # 使用领域服务验证
            if not self._domain_service.can_assign(task, user_id):
                return {"success": False, "error": "任务无法分配"}

            task.assign_to(user_id)
            self._task_repo.save(task)

            # 发送通知
            self._notification.notify_task_assigned(task_id, user_id, task.title)

            self._logging.log_info(f"任务分配: {task_id} -> {user_id}")

            return {"success": True, "task": task.to_dict()}

        except Exception as e:
            self._logging.log_error("分配任务失败", e)
            return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════════
# 第四部分：适配器（Adapters）- 实现端口
# ═══════════════════════════════════════════════════════════════

# ========== 输出适配器（基础设施适配器）==========

class InMemoryTaskRepository(TaskRepositoryPort):
    """内存任务仓储适配器"""

    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def find_by_id(self, task_id: TaskId) -> Optional[Task]:
        return self._tasks.get(task_id.value)

    def find_all(self, filters: dict = None) -> List[Task]:
        tasks = list(self._tasks.values())

        if filters:
            if "status" in filters:
                status = TaskStatus(filters["status"])
                tasks = [t for t in tasks if t.status == status]

        return tasks

    def save(self, task: Task) -> None:
        self._tasks[task.id.value] = task
        print(f"[Repository] 任务保存: {task.id.value}")

    def delete(self, task_id: TaskId) -> bool:
        if task_id.value in self._tasks:
            del self._tasks[task_id.value]
            return True
        return False


class ConsoleNotificationAdapter(NotificationPort):
    """控制台通知适配器"""

    def notify_task_assigned(self, task_id: str, user_id: str, task_title: str) -> None:
        print(f"[Notification] 任务 '{task_title}' 已分配给用户 {user_id}")

    def notify_task_completed(self, task_id: str, task_title: str) -> None:
        print(f"[Notification] 任务 '{task_title}' 已完成!")


class EmailNotificationAdapter(NotificationPort):
    """邮件通知适配器（模拟）"""

    def notify_task_assigned(self, task_id: str, user_id: str, task_title: str) -> None:
        print(f"[Email] To: {user_id}@company.com")
        print(f"[Email] Subject: 新任务分配 - {task_title}")
        print(f"[Email] Body: 您被分配了新任务: {task_title}")

    def notify_task_completed(self, task_id: str, task_title: str) -> None:
        print(f"[Email] Subject: 任务完成 - {task_title}")
        print(f"[Email] Body: 任务 '{task_title}' 已标记为完成")


class ConsoleLoggingAdapter(LoggingPort):
    """控制台日志适配器"""

    def log_info(self, message: str, context: dict = None) -> None:
        ctx = json.dumps(context, ensure_ascii=False) if context else ""
        print(f"[INFO] {message} {ctx}")

    def log_error(self, message: str, error: Exception = None) -> None:
        err = f" - {error}" if error else ""
        print(f"[ERROR] {message}{err}")


class FileLoggingAdapter(LoggingPort):
    """文件日志适配器（模拟）"""

    def __init__(self, filename: str = "app.log"):
        self._filename = filename
        self._logs: List[str] = []

    def log_info(self, message: str, context: dict = None) -> None:
        log_entry = f"[{datetime.now().isoformat()}] INFO: {message}"
        self._logs.append(log_entry)
        print(f"[FileLog] {log_entry}")

    def log_error(self, message: str, error: Exception = None) -> None:
        err = f" - {error}" if error else ""
        log_entry = f"[{datetime.now().isoformat()}] ERROR: {message}{err}"
        self._logs.append(log_entry)
        print(f"[FileLog] {log_entry}")

    def get_logs(self) -> List[str]:
        return self._logs


# ========== 输入适配器（接口适配器）==========

class TaskController:
    """任务控制器 - REST API适配器"""

    def __init__(self, task_service: TaskServicePort):
        self._task_service = task_service

    def handle_create(self, request: dict) -> dict:
        """处理创建请求"""
        return self._task_service.create_task(
            title=request.get("title", ""),
            description=request.get("description", ""),
            priority=request.get("priority", "medium")
        )

    def handle_get(self, task_id: str) -> dict:
        """处理获取请求"""
        task = self._task_service.get_task(task_id)
        if task:
            return {"success": True, "task": task}
        return {"success": False, "error": "任务不存在"}

    def handle_list(self, query: dict = None) -> dict:
        """处理列表请求"""
        query = query or {}
        tasks = self._task_service.list_tasks(
            status=query.get("status"),
            assignee=query.get("assignee")
        )
        return {"success": True, "tasks": tasks, "total": len(tasks)}

    def handle_start(self, task_id: str) -> dict:
        """处理开始请求"""
        return self._task_service.start_task(task_id)

    def handle_complete(self, task_id: str) -> dict:
        """处理完成请求"""
        return self._task_service.complete_task(task_id)

    def handle_assign(self, task_id: str, request: dict) -> dict:
        """处理分配请求"""
        return self._task_service.assign_task(
            task_id=task_id,
            user_id=request.get("user_id", "")
        )


class TaskCLIAdapter:
    """任务CLI适配器"""

    def __init__(self, task_service: TaskServicePort):
        self._task_service = task_service

    def run(self):
        """运行CLI"""
        print("\n=== 任务管理CLI ===")
        print("命令: create, list, get, start, complete, assign, quit")

        while True:
            cmd = input("\n> ").strip().split()
            if not cmd:
                continue

            action = cmd[0].lower()

            if action == "quit":
                break

            elif action == "create":
                result = self._task_service.create_task(
                    title=input("标题: "),
                    description=input("描述: "),
                    priority=input("优先级 (low/medium/high): ") or "medium"
                )
                print(json.dumps(result, indent=2, ensure_ascii=False))

            elif action == "list":
                result = self._task_service.list_tasks()
                print(json.dumps(result, indent=2, ensure_ascii=False))

            elif action == "get" and len(cmd) > 1:
                task = self._task_service.get_task(cmd[1])
                print(json.dumps(task, indent=2, ensure_ascii=False))

            elif action == "start" and len(cmd) > 1:
                result = self._task_service.start_task(cmd[1])
                print(json.dumps(result, indent=2, ensure_ascii=False))

            elif action == "complete" and len(cmd) > 1:
                result = self._task_service.complete_task(cmd[1])
                print(json.dumps(result, indent=2, ensure_ascii=False))

            else:
                print("未知命令")


# ═══════════════════════════════════════════════════════════════
# 第五部分：依赖注入容器
# ═══════════════════════════════════════════════════════════════

class ApplicationContainer:
    """应用容器 - 组装所有组件"""

    @staticmethod
    def create_application(
        use_email_notification: bool = False,
        use_file_logging: bool = False
    ):
        """创建应用"""
        # 输出适配器（基础设施）
        task_repo = InMemoryTaskRepository()

        if use_email_notification:
            notification = EmailNotificationAdapter()
        else:
            notification = ConsoleNotificationAdapter()

        if use_file_logging:
            logging = FileLoggingAdapter()
        else:
            logging = ConsoleLoggingAdapter()

        # 领域服务
        domain_service = TaskDomainService()

        # 应用服务（实现输入端口）
        app_service = TaskApplicationService(
            task_repo=task_repo,
            notification=notification,
            logging=logging,
            domain_service=domain_service
        )

        # 输入适配器
        controller = TaskController(app_service)
        cli = TaskCLIAdapter(app_service)

        return {
            "app_service": app_service,
            "controller": controller,
            "cli": cli,
            "repository": task_repo
        }


# ═══════════════════════════════════════════════════════════════
# 运行示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("六边形架构演示 - 任务管理系统")
    print("=" * 60)

    # 创建应用（使用控制台适配器）
    app = ApplicationContainer.create_application(
        use_email_notification=False,
        use_file_logging=False
    )

    controller = app["controller"]

    # 场景1: 创建任务
    print("\n1. 创建任务:")
    result1 = controller.handle_create({
        "title": "完成架构设计文档",
        "description": "编写六边形架构的详细文档",
        "priority": "high"
    })
    print(json.dumps(result1, indent=2, ensure_ascii=False))
    task_id = result1.get("task", {}).get("id")

    # 创建更多任务
    controller.handle_create({
        "title": "代码审查",
        "description": "审查团队成员的代码",
        "priority": "medium"
    })

    controller.handle_create({
        "title": "修复Bug",
        "description": "修复生产环境的紧急Bug",
        "priority": "critical"
    })

    # 场景2: 列出任务
    print("\n2. 列出所有任务:")
    result2 = controller.handle_list()
    print(json.dumps(result2, indent=2, ensure_ascii=False))

    # 场景3: 开始任务
    if task_id:
        print("\n3. 开始任务:")
        result3 = controller.handle_start(task_id)
        print(json.dumps(result3, indent=2, ensure_ascii=False))

    # 场景4: 分配任务
    if task_id:
        print("\n4. 分配任务:")
        result4 = controller.handle_assign(task_id, {"user_id": "U001"})
        print(json.dumps(result4, indent=2, ensure_ascii=False))

    # 场景5: 完成任务
    if task_id:
        print("\n5. 完成任务:")
        result5 = controller.handle_complete(task_id)
        print(json.dumps(result5, indent=2, ensure_ascii=False))

    # 场景6: 使用不同适配器
    print("\n6. 使用邮件通知适配器:")
    app2 = ApplicationContainer.create_application(
        use_email_notification=True,
        use_file_logging=True
    )
    controller2 = app2["controller"]

    result6 = controller2.handle_create({
        "title": "测试邮件通知",
        "description": "测试邮件通知功能",
        "priority": "low"
    })
    task_id2 = result6.get("task", {}).get("id")

    if task_id2:
        controller2.handle_assign(task_id2, {"user_id": "U002"})
        controller2.handle_complete(task_id2)

    # 查看文件日志
    print("\n7. 文件日志:")
    logs = app2["repository"]
    print(f"任务数量: {len(logs._tasks)}")


# ═══════════════════════════════════════════════════════════════
# 六边形架构总结
# ═══════════════════════════════════════════════════════════════
"""
六边形架构核心要点:

1. 端口（Ports）
   - 输入端口：定义外部如何调用应用（如TaskServicePort）
   - 输出端口：定义应用如何调用外部（如TaskRepositoryPort）
   - 端口是接口，属于应用核心

2. 适配器（Adapters）
   - 输入适配器：实现输入端口，如Controller、CLI
   - 输出适配器：实现输出端口，如Repository、Notification
   - 适配器可以替换，不影响核心

3. 依赖倒置
   - 应用核心只依赖端口（接口）
   - 适配器依赖应用核心
   - 依赖方向：适配器 → 核心

4. 优势
   - 可测试性：核心可独立单元测试
   - 可替换性：适配器可随时替换
   - 延迟决策：技术选型可延后
   - 清晰边界：核心业务与技术细节分离

5. 与洋葱架构、整洁架构的关系
   - 三者思想一致：依赖向内
   - 六边形架构强调"端口和适配器"
   - 洋葱架构强调"同心圆层"
   - 整洁架构强调"用例驱动"
"""
```

---


## 第六部分：Serverless架构

### 6.1 概念定义

Serverless（无服务器）是一种云计算执行模型，开发者无需管理服务器，只需关注业务代码。

```
┌─────────────────────────────────────────────────────────────┐
│                      Serverless 架构                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    函数层 (FaaS)                      │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐  │   │
│  │  │ Function│  │ Function│  │ Function│  │Function│  │   │
│  │  │   A     │  │   B     │  │   C     │  │   D    │  │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └───┬────┘  │   │
│  │       └─────────────┴─────────────┴──────────┘       │   │
│  │                    事件触发器                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │                  后端服务层 (BaaS)                      │ │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐          │ │
│  │  │  Auth  │ │  DB    │ │Storage │ │ Queue  │          │ │
│  │  │Cognito │ │DynamoDB│ │  S3    │ │ SQS    │          │ │
│  │  └────────┘ └────────┘ └────────┘ └────────┘          │ │
│  └───────────────────────────────────────────────────────┘ │
│                            │                                │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │                   基础设施层                            │ │
│  │         (由云服务商管理，开发者不可见)                    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 FaaS（函数即服务）

#### 核心特征

| 特征 | 说明 |
|------|------|
| **事件驱动** | 函数由事件触发执行 |
| **无状态** | 每次执行都是独立的 |
| **自动扩缩容** | 根据请求量自动调整 |
| **按需付费** | 按执行时间和内存计费 |
| **冷启动** | 首次执行可能有延迟 |

#### 主流FaaS平台

| 平台 | 服务商 | 特点 |
|------|--------|------|
| AWS Lambda | Amazon | 生态最完善 |
| Azure Functions | Microsoft | 与Azure集成好 |
| Google Cloud Functions | Google | 简单易用 |
| 阿里云函数计算 | 阿里云 | 国内首选 |
| 腾讯云SCF | 腾讯云 | 微信生态集成 |

### 6.3 BaaS（后端即服务）

#### 核心服务

```
┌─────────────────────────────────────────────────────────────┐
│                      BaaS 服务                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  认证服务    │  │  数据库服务  │  │  存储服务   │         │
│  │  (Auth)     │  │  (Database) │  │  (Storage)  │         │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤         │
│  │ • 用户注册   │  │ • NoSQL     │  │ • 文件上传  │         │
│  │ • 用户登录   │  │ • 实时同步  │  │ • CDN分发   │         │
│  │ • 社交登录   │  │ • 权限控制  │  │ • 图片处理  │         │
│  │ • JWT令牌   │  │ • 离线支持  │  │ • 备份恢复  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  消息服务    │  │  分析服务   │  │  AI/ML服务  │         │
│  │  (Messaging)│  │  (Analytics)│  │  (AI/ML)    │         │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤         │
│  │ • 推送通知   │  │ • 用户行为  │  │ • 图像识别  │         │
│  │ • 邮件发送   │  │ • 性能监控  │  │ • 语音识别  │         │
│  │ • SMS短信   │  │ • A/B测试   │  │ • 自然语言  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.4 Python Lambda实现

```python
"""
Serverless架构实现 - 模拟AWS Lambda风格
包含：Handler模式、事件处理、BaaS集成
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any, Union
from enum import Enum, auto
import json
import time
import asyncio


# ═══════════════════════════════════════════════════════════════
# Lambda运行时模拟
# ═══════════════════════════════════════════════════════════════

@dataclass
class LambdaContext:
    """Lambda上下文"""
    function_name: str
    function_version: str = "$LATEST"
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = ""
    aws_request_id: str = ""
    log_group_name: str = ""
    log_stream_name: str = ""
    identity: Dict = field(default_factory=dict)
    client_context: Dict = field(default_factory=dict)

    def get_remaining_time_in_millis(self) -> int:
        """获取剩余执行时间"""
        # 模拟实现
        return 300000  # 5分钟


@dataclass
class LambdaEvent:
    """Lambda事件"""
    event_type: str
    payload: Dict[str, Any]
    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)
    path_params: Dict[str, str] = field(default_factory=dict)


class LambdaHandler(ABC):
    """Lambda处理器基类"""

    @abstractmethod
    def handle(self, event: Dict, context: LambdaContext) -> Dict:
        """处理事件"""
        pass


class LambdaRuntime:
    """Lambda运行时模拟"""

    def __init__(self):
        self._handlers: Dict[str, LambdaHandler] = {}
        self._cold_start = True
        self._invocation_count = 0
        self._start_time = time.time()

    def register_handler(self, name: str, handler: LambdaHandler) -> None:
        """注册处理器"""
        self._handlers[name] = handler
        print(f"[LambdaRuntime] 注册处理器: {name}")

    def invoke(
        self,
        handler_name: str,
        event: Dict,
        context: Optional[LambdaContext] = None
    ) -> Dict:
        """调用处理器"""
        handler = self._handlers.get(handler_name)
        if not handler:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"Handler not found: {handler_name}"})
            }

        # 模拟冷启动
        if self._cold_start:
            print(f"[LambdaRuntime] 冷启动...")
            time.sleep(0.1)  # 模拟初始化延迟
            self._cold_start = False

        # 创建上下文
        if context is None:
            context = LambdaContext(
                function_name=handler_name,
                aws_request_id=str(int(time.time() * 1000))
            )

        # 执行
        self._invocation_count += 1
        start = time.time()

        try:
            result = handler.handle(event, context)
            duration = (time.time() - start) * 1000
            print(f"[LambdaRuntime] 执行完成: {duration:.2f}ms")
            return result
        except Exception as e:
            duration = (time.time() - start) * 1000
            print(f"[LambdaRuntime] 执行失败: {duration:.2f}ms - {e}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "uptime": time.time() - self._start_time,
            "invocation_count": self._invocation_count,
            "handlers": list(self._handlers.keys()),
            "is_cold_start": self._cold_start
        }


# ═══════════════════════════════════════════════════════════════
# BaaS服务模拟
# ═══════════════════════════════════════════════════════════════

class AuthenticationService:
    """认证服务（BaaS）"""

    def __init__(self):
        self._users: Dict[str, dict] = {}
        self._tokens: Dict[str, str] = {}

    def register(self, username: str, password: str) -> dict:
        """注册用户"""
        if username in self._users:
            return {"success": False, "error": "用户已存在"}

        user_id = f"user_{int(time.time())}"
        self._users[username] = {
            "id": user_id,
            "username": username,
            "password": password,  # 实际应该哈希
            "created_at": datetime.now().isoformat()
        }

        return {"success": True, "user_id": user_id}

    def login(self, username: str, password: str) -> dict:
        """用户登录"""
        user = self._users.get(username)
        if not user or user["password"] != password:
            return {"success": False, "error": "用户名或密码错误"}

        token = f"token_{int(time.time())}"
        self._tokens[token] = user["id"]

        return {"success": True, "token": token, "user_id": user["id"]}

    def verify_token(self, token: str) -> Optional[str]:
        """验证令牌"""
        return self._tokens.get(token)


class DatabaseService:
    """数据库服务（BaaS）- 模拟NoSQL数据库"""

    def __init__(self):
        self._tables: Dict[str, Dict[str, dict]] = {}

    def create_table(self, table_name: str) -> None:
        """创建表"""
        if table_name not in self._tables:
            self._tables[table_name] = {}

    def put_item(self, table_name: str, item: dict) -> dict:
        """插入/更新项目"""
        if table_name not in self._tables:
            self.create_table(table_name)

        item_id = item.get("id") or str(int(time.time() * 1000))
        item["id"] = item_id
        item["updated_at"] = datetime.now().isoformat()

        self._tables[table_name][item_id] = item
        return {"success": True, "id": item_id}

    def get_item(self, table_name: str, item_id: str) -> Optional[dict]:
        """获取项目"""
        table = self._tables.get(table_name, {})
        return table.get(item_id)

    def query(
        self,
        table_name: str,
        filters: dict = None,
        limit: int = 100
    ) -> List[dict]:
        """查询"""
        table = self._tables.get(table_name, {})
        items = list(table.values())

        if filters:
            for key, value in filters.items():
                items = [i for i in items if i.get(key) == value]

        return items[:limit]

    def delete_item(self, table_name: str, item_id: str) -> bool:
        """删除项目"""
        table = self._tables.get(table_name, {})
        if item_id in table:
            del table[item_id]
            return True
        return False


class StorageService:
    """存储服务（BaaS）"""

    def __init__(self):
        self._buckets: Dict[str, Dict[str, bytes]] = {}

    def create_bucket(self, bucket_name: str) -> None:
        """创建存储桶"""
        if bucket_name not in self._buckets:
            self._buckets[bucket_name] = {}

    def upload(
        self,
        bucket_name: str,
        key: str,
        data: bytes,
        metadata: dict = None
    ) -> dict:
        """上传文件"""
        if bucket_name not in self._buckets:
            self.create_bucket(bucket_name)

        self._buckets[bucket_name][key] = data

        return {
            "success": True,
            "bucket": bucket_name,
            "key": key,
            "size": len(data),
            "url": f"https://storage.example.com/{bucket_name}/{key}"
        }

    def download(self, bucket_name: str, key: str) -> Optional[bytes]:
        """下载文件"""
        bucket = self._buckets.get(bucket_name, {})
        return bucket.get(key)

    def delete(self, bucket_name: str, key: str) -> bool:
        """删除文件"""
        bucket = self._buckets.get(bucket_name, {})
        if key in bucket:
            del bucket[key]
            return True
        return False


class QueueService:
    """消息队列服务（BaaS）"""

    def __init__(self):
        self._queues: Dict[str, List[dict]] = {}

    def create_queue(self, queue_name: str) -> None:
        """创建队列"""
        if queue_name not in self._queues:
            self._queues[queue_name] = []

    def send_message(self, queue_name: str, message: dict) -> dict:
        """发送消息"""
        if queue_name not in self._queues:
            self.create_queue(queue_name)

        message_id = f"msg_{int(time.time() * 1000)}"
        message["message_id"] = message_id
        message["sent_at"] = datetime.now().isoformat()

        self._queues[queue_name].append(message)

        return {"success": True, "message_id": message_id}

    def receive_messages(self, queue_name: str, max_messages: int = 10) -> List[dict]:
        """接收消息"""
        queue = self._queues.get(queue_name, [])
        return queue[:max_messages]


# ═══════════════════════════════════════════════════════════════
# 具体Lambda函数实现
# ═══════════════════════════════════════════════════════════════

class UserRegistrationHandler(LambdaHandler):
    """用户注册处理器"""

    def __init__(self, auth_service: AuthenticationService):
        self._auth = auth_service

    def handle(self, event: Dict, context: LambdaContext) -> Dict:
        """处理注册请求"""
        print(f"[Handler] 用户注册 - RequestId: {context.aws_request_id}")

        body = json.loads(event.get("body", "{}"))
        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "用户名和密码不能为空"})
            }

        result = self._auth.register(username, password)

        return {
            "statusCode": 200 if result["success"] else 400,
            "body": json.dumps(result)
        }


class TodoApiHandler(LambdaHandler):
    """Todo API处理器 - CRUD操作"""

    def __init__(
        self,
        db_service: DatabaseService,
        auth_service: AuthenticationService
    ):
        self._db = db_service
        self._auth = auth_service
        self._db.create_table("todos")

    def handle(self, event: Dict, context: LambdaContext) -> Dict:
        """处理API请求"""
        http_method = event.get("httpMethod", "GET")
        path = event.get("path", "")

        # 认证检查
        headers = event.get("headers", {})
        auth_header = headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else ""
        user_id = self._auth.verify_token(token)

        if not user_id:
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "未授权"})
            }

        # 路由请求
        if http_method == "GET" and path == "/todos":
            return self._list_todos(user_id)
        elif http_method == "POST" and path == "/todos":
            return self._create_todo(event, user_id)
        elif http_method == "GET" and path.startswith("/todos/"):
            todo_id = path.split("/")[-1]
            return self._get_todo(todo_id, user_id)
        elif http_method == "PUT" and path.startswith("/todos/"):
            todo_id = path.split("/")[-1]
            return self._update_todo(todo_id, event, user_id)
        elif http_method == "DELETE" and path.startswith("/todos/"):
            todo_id = path.split("/")[-1]
            return self._delete_todo(todo_id, user_id)

        return {
            "statusCode": 404,
            "body": json.dumps({"error": "未找到"})
        }

    def _list_todos(self, user_id: str) -> Dict:
        """列出待办"""
        todos = self._db.query("todos", filters={"user_id": user_id})
        return {
            "statusCode": 200,
            "body": json.dumps({"todos": todos})
        }

    def _create_todo(self, event: Dict, user_id: str) -> Dict:
        """创建待办"""
        body = json.loads(event.get("body", "{}"))

        todo = {
            "title": body.get("title"),
            "completed": False,
            "user_id": user_id,
            "created_at": datetime.now().isoformat()
        }

        result = self._db.put_item("todos", todo)

        return {
            "statusCode": 201,
            "body": json.dumps(result)
        }

    def _get_todo(self, todo_id: str, user_id: str) -> Dict:
        """获取待办"""
        todo = self._db.get_item("todos", todo_id)

        if not todo or todo.get("user_id") != user_id:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "待办不存在"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps(todo)
        }

    def _update_todo(self, todo_id: str, event: Dict, user_id: str) -> Dict:
        """更新待办"""
        todo = self._db.get_item("todos", todo_id)

        if not todo or todo.get("user_id") != user_id:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "待办不存在"})
            }

        body = json.loads(event.get("body", "{}"))
        todo.update(body)

        self._db.put_item("todos", todo)

        return {
            "statusCode": 200,
            "body": json.dumps(todo)
        }

    def _delete_todo(self, todo_id: str, user_id: str) -> Dict:
        """删除待办"""
        todo = self._db.get_item("todos", todo_id)

        if not todo or todo.get("user_id") != user_id:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "待办不存在"})
            }

        self._db.delete_item("todos", todo_id)

        return {
            "statusCode": 204,
            "body": ""
        }


class FileUploadHandler(LambdaHandler):
    """文件上传处理器"""

    def __init__(
        self,
        storage_service: StorageService,
        auth_service: AuthenticationService
    ):
        self._storage = storage_service
        self._auth = auth_service

    def handle(self, event: Dict, context: LambdaContext) -> Dict:
        """处理文件上传"""
        # 解析 multipart/form-data（简化）
        body = event.get("body", "")

        # 模拟文件上传
        filename = event.get("queryStringParameters", {}).get("filename", "upload.bin")
        file_data = body.encode() if isinstance(body, str) else b"file_content"

        # 上传到存储服务
        result = self._storage.upload(
            bucket_name="user-uploads",
            key=f"uploads/{int(time.time())}_{filename}",
            data=file_data
        )

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }


class EventProcessorHandler(LambdaHandler):
    """事件处理器 - 处理队列消息"""

    def __init__(
        self,
        queue_service: QueueService,
        db_service: DatabaseService
    ):
        self._queue = queue_service
        self._db = db_service

    def handle(self, event: Dict, context: LambdaContext) -> Dict:
        """处理队列事件"""
        # 从队列获取消息
        messages = self._queue.receive_messages("task-queue", max_messages=10)

        processed = []
        for message in messages:
            print(f"[EventProcessor] 处理消息: {message.get('message_id')}")

            # 处理消息
            task_type = message.get("task_type")
            if task_type == "send_email":
                self._process_email_task(message)
            elif task_type == "generate_report":
                self._process_report_task(message)

            processed.append(message.get("message_id"))

        return {
            "statusCode": 200,
            "body": json.dumps({"processed": len(processed), "message_ids": processed})
        }

    def _process_email_task(self, message: dict) -> None:
        """处理邮件任务"""
        to = message.get("to")
        subject = message.get("subject")
        print(f"[Email] 发送邮件到 {to}: {subject}")

    def _process_report_task(self, message: dict) -> None:
        """处理报表任务"""
        report_type = message.get("report_type")
        print(f"[Report] 生成报表: {report_type}")


# ═══════════════════════════════════════════════════════════════
# 应用组装
# ═══════════════════════════════════════════════════════════════

class ServerlessApplication:
    """Serverless应用"""

    def __init__(self):
        # BaaS服务
        self.auth = AuthenticationService()
        self.db = DatabaseService()
        self.storage = StorageService()
        self.queue = QueueService()

        # Lambda运行时
        self.runtime = LambdaRuntime()

        # 注册处理器
        self._register_handlers()

    def _register_handlers(self) -> None:
        """注册Lambda处理器"""
        # 用户注册
        self.runtime.register_handler(
            "user-registration",
            UserRegistrationHandler(self.auth)
        )

        # Todo API
        self.runtime.register_handler(
            "todo-api",
            TodoApiHandler(self.db, self.auth)
        )

        # 文件上传
        self.runtime.register_handler(
            "file-upload",
            FileUploadHandler(self.storage, self.auth)
        )

        # 事件处理
        self.runtime.register_handler(
            "event-processor",
            EventProcessorHandler(self.queue, self.db)
        )

    def invoke(self, handler_name: str, event: Dict) -> Dict:
        """调用Lambda函数"""
        return self.runtime.invoke(handler_name, event)


# ═══════════════════════════════════════════════════════════════
# 运行示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Serverless架构演示")
    print("=" * 60)

    app = ServerlessApplication()

    # 场景1: 用户注册
    print("\n1. 用户注册:")
    result1 = app.invoke("user-registration", {
        "body": json.dumps({"username": "zhangsan", "password": "123456"})
    })
    print(json.dumps(result1, indent=2, ensure_ascii=False))

    # 场景2: 用户登录（获取token）
    print("\n2. 用户登录:")
    login_result = app.auth.login("zhangsan", "123456")
    token = login_result.get("token")
    print(f"Token: {token}")

    # 场景3: 创建待办
    print("\n3. 创建待办:")
    result3 = app.invoke("todo-api", {
        "httpMethod": "POST",
        "path": "/todos",
        "headers": {"Authorization": f"Bearer {token}"},
        "body": json.dumps({"title": "学习Serverless架构"})
    })
    print(json.dumps(result3, indent=2, ensure_ascii=False))

    # 场景4: 列出待办
    print("\n4. 列出待办:")
    result4 = app.invoke("todo-api", {
        "httpMethod": "GET",
        "path": "/todos",
        "headers": {"Authorization": f"Bearer {token}"}
    })
    print(json.dumps(result4, indent=2, ensure_ascii=False))

    # 场景5: 发送队列消息
    print("\n5. 发送队列消息:")
    app.queue.send_message("task-queue", {
        "task_type": "send_email",
        "to": "user@example.com",
        "subject": "欢迎注册"
    })

    # 场景6: 处理队列消息
    print("\n6. 处理队列消息:")
    result6 = app.invoke("event-processor", {})
    print(json.dumps(result6, indent=2, ensure_ascii=False))

    # 场景7: 运行时统计
    print("\n7. Lambda运行时统计:")
    print(json.dumps(app.runtime.get_stats(), indent=2, ensure_ascii=False))


# ═══════════════════════════════════════════════════════════════
# Serverless最佳实践
# ═══════════════════════════════════════════════════════════════
"""
Serverless最佳实践:

1. 函数设计
   - 单一职责：每个函数只做一件事
   - 无状态设计：不依赖本地状态
   - 快速启动：减少冷启动时间
   - 合理超时：设置适当的超时时间

2. 事件驱动
   - 使用事件触发函数执行
   - 异步处理耗时操作
   - 利用消息队列解耦

3. BaaS集成
   - 使用托管服务减少运维
   - 认证：Cognito/Auth0
   - 数据库：DynamoDB/Firestore
   - 存储：S3/Cloud Storage
   - 队列：SQS/Pub/Sub

4. 监控与日志
   - 结构化日志输出
   - 分布式追踪
   - 设置告警阈值

5. 安全
   - 最小权限原则
   - 环境变量管理密钥
   - 输入验证与过滤

6. 成本优化
   - 合理设置内存
   - 利用预留并发
   - 监控执行时间和次数
"""
```

---


## 第七部分：云原生架构

### 7.1 概念定义

云原生（Cloud Native）是一种构建和运行应用程序的方法，充分利用云计算的弹性、分布式和自动化优势。

```
┌─────────────────────────────────────────────────────────────┐
│                     云原生技术栈                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  应用层 (Applications)               │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐  │   │
│  │  │Microsvc │  │  FaaS   │  │   Job   │  │ Batch  │  │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │              服务网格层 (Service Mesh)                 │ │
│  │         Istio / Linkerd / AWS App Mesh                │ │
│  │    流量管理 / 安全通信 / 可观测性 / 策略控制            │ │
│  └───────────────────────────────────────────────────────┘ │
│                            │                                │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │              编排层 (Orchestration)                    │ │
│  │              Kubernetes / Docker Swarm                 │ │
│  │    调度 / 扩缩容 / 服务发现 / 配置管理 / 存储编排        │ │
│  └───────────────────────────────────────────────────────┘ │
│                            │                                │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │              容器层 (Container Runtime)                │ │
│  │         Docker / containerd / CRI-O                    │ │
│  │    镜像 / 容器 / 网络 / 存储                           │ │
│  └───────────────────────────────────────────────────────┘ │
│                            │                                │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │              基础设施层 (Infrastructure)               │ │
│  │    公有云 / 私有云 / 混合云 / 边缘计算                   │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 容器化（Docker）

#### 核心概念

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker 核心概念                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  镜像 (Image):                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer N: 应用代码                                    │   │
│  │  Layer 3: 依赖库 (pip install)                       │   │
│  │  Layer 2: Python Runtime                             │   │
│  │  Layer 1: 基础镜像 (Ubuntu/Alpine)                   │   │
│  │  Layer 0: 基础系统层                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  容器 (Container):                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  可写层 (Container Layer)                            │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │           只读镜像层 (Image Layers)          │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Dockerfile 示例:                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  FROM python:3.11-slim                              │   │
│  │  WORKDIR /app                                       │   │
│  │  COPY requirements.txt .                            │   │
│  │  RUN pip install -r requirements.txt                │   │
│  │  COPY . .                                           │   │
│  │  CMD ["python", "app.py"]                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Dockerfile最佳实践

```dockerfile
# ═══════════════════════════════════════════════════════════════
# Python应用 Dockerfile 最佳实践
# ═══════════════════════════════════════════════════════════════

# 使用多阶段构建减小镜像大小
# 阶段1: 构建阶段
FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 阶段2: 运行阶段
FROM python:3.11-slim

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 设置工作目录
WORKDIR /app

# 从构建阶段复制依赖
COPY --from=builder /root/.local /home/appuser/.local

# 复制应用代码
COPY --chown=appuser:appuser . .

# 设置环境变量
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production

# 切换到非root用户
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Python容器化示例

```python
"""
容器化Python应用示例
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import os
import socket
import time

app = FastAPI(title="Cloud Native App", version="1.0.0")

# 启动时间（用于健康检查）
START_TIME = time.time()


# ═══════════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════════

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: str = ""
    price: float
    in_stock: bool = True


class HealthStatus(BaseModel):
    status: str
    hostname: str
    uptime_seconds: float
    version: str
    environment: str


# ═══════════════════════════════════════════════════════════════
# 内存存储（实际应用应使用数据库）
# ═══════════════════════════════════════════════════════════════

items_db: List[dict] = [
    {"id": 1, "name": "商品A", "description": "描述A", "price": 100.0, "in_stock": True},
    {"id": 2, "name": "商品B", "description": "描述B", "price": 200.0, "in_stock": False},
]
next_id = 3


# ═══════════════════════════════════════════════════════════════
# API端点
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Cloud Native Application",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthStatus)
async def health_check():
    """健康检查端点 - Kubernetes使用"""
    return HealthStatus(
        status="healthy",
        hostname=socket.gethostname(),
        uptime_seconds=round(time.time() - START_TIME, 2),
        version="1.0.0",
        environment=os.getenv("APP_ENV", "development")
    )


@app.get("/ready")
async def readiness_check():
    """就绪检查端点"""
    # 检查依赖服务是否就绪
    # 如数据库连接、缓存服务等
    return {"status": "ready"}


@app.get("/metrics")
async def metrics():
    """Prometheus指标端点"""
    return {
        "uptime_seconds": time.time() - START_TIME,
        "request_count": 0,  # 实际应统计
        "items_count": len(items_db)
    }


# CRUD端点
@app.get("/items", response_model=List[dict])
async def list_items():
    """列出所有商品"""
    return items_db


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """获取商品详情"""
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="商品不存在")


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """创建商品"""
    global next_id
    new_item = item.dict()
    new_item["id"] = next_id
    next_id += 1
    items_db.append(new_item)
    return new_item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """更新商品"""
    for i, existing in enumerate(items_db):
        if existing["id"] == item_id:
            updated = item.dict()
            updated["id"] = item_id
            items_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="商品不存在")


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """删除商品"""
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(i)
            return {"message": "删除成功"}
    raise HTTPException(status_code=404, detail="商品不存在")


# ═══════════════════════════════════════════════════════════════
# 配置管理
# ═══════════════════════════════════════════════════════════════

class Config:
    """应用配置"""

    # 从环境变量读取配置
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    PORT = int(os.getenv("PORT", "8000"))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Kubernetes相关
    KUBERNETES_NAMESPACE = os.getenv("KUBERNETES_NAMESPACE", "default")
    POD_NAME = os.getenv("HOSTNAME", "unknown")


# ═══════════════════════════════════════════════════════════════
# 启动事件
# ═══════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print(f"🚀 应用启动")
    print(f"   环境: {Config.LOG_LEVEL}")
    print(f"   端口: {Config.PORT}")
    print(f"   Pod: {Config.POD_NAME}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("🛑 应用关闭")


# ═══════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level=Config.LOG_LEVEL.lower()
    )
```

### 7.3 编排（Kubernetes概念）

```
┌─────────────────────────────────────────────────────────────┐
│                  Kubernetes 核心概念                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Pod (最小部署单元):                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Pod                                                │   │
│  │  ┌─────────────┐  ┌─────────────┐                  │   │
│  │  │  Container  │  │  Container  │                  │   │
│  │  │    App      │  │   Sidecar   │                  │   │
│  │  │  (Main)     │  │ (Log/Proxy) │                  │   │
│  │  └─────────────┘  └─────────────┘                  │   │
│  │  共享: Network Namespace, Storage                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Deployment (无状态应用):                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Deployment: my-app                                 │   │
│  │  Replicas: 3                                        │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐               │   │
│  │  │  Pod 1  │ │  Pod 2  │ │  Pod 3  │               │   │
│  │  └─────────┘ └─────────┘ └─────────┘               │   │
│  │  滚动更新 / 回滚 / 扩缩容                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Service (服务发现):                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Service: my-app-service                            │   │
│  │  Type: ClusterIP / NodePort / LoadBalancer          │   │
│  │  Selector: app=my-app                               │   │
│  │         ┌─────────┐                                 │   │
│  │  ──────►│  Pod 1  │                                 │   │
│  │  ──────►│  Pod 2  │  负载均衡                        │   │
│  │  ──────►│  Pod 3  │                                 │   │
│  │         └─────────┘                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ConfigMap / Secret (配置管理):                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ConfigMap: app-config                              │   │
│  │  data:                                              │   │
│  │    DATABASE_URL: postgres://...                     │   │
│  │    LOG_LEVEL: info                                  │   │
│  │                                                     │   │
│  │  Secret: app-secret                                 │   │
│  │  data:                                              │   │
│  │    API_KEY: <base64>                                │   │
│  │    PASSWORD: <base64>                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Kubernetes YAML示例

```yaml
# ═══════════════════════════════════════════════════════════════
# Kubernetes Deployment 配置
# ═══════════════════════════════════════════════════════════════

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloud-native-app
  labels:
    app: cloud-native-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cloud-native-app
  template:
    metadata:
      labels:
        app: cloud-native-app
    spec:
      containers:
        - name: app
          image: cloud-native-app:latest
          ports:
            - containerPort: 8000
          env:
            - name: APP_ENV
              value: "production"
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: LOG_LEVEL
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secret
                  key: DATABASE_URL
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: cloud-native-app-service
spec:
  selector:
    app: cloud-native-app
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "INFO"
  CACHE_TTL: "300"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DATABASE_URL: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0Bsb2NhbGhvc3Q6NTQzMi9kYg==  # base64
  API_KEY: bXktc2VjcmV0LWtleQ==  # base64
---
# 水平自动扩缩容 (HPA)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cloud-native-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cloud-native-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### 7.4 服务网格（Istio概念）

```
┌─────────────────────────────────────────────────────────────┐
│                    服务网格架构                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  传统微服务通信:                                             │
│  ┌─────────┐      HTTP/gRPC       ┌─────────┐              │
│  │ Service │◄────────────────────►│ Service │              │
│  │    A    │                      │    B    │              │
│  └─────────┘                      └─────────┘              │
│                                                             │
│  服务网格通信:                                               │
│  ┌─────────┐  ┌─────────┐    ┌─────────┐  ┌─────────┐     │
│  │ Service │  │  Envoy  │◄──►│  Envoy  │  │ Service │     │
│  │    A    │◄─┤  Proxy  │    │  Proxy  ├─►│    B    │     │
│  └─────────┘  └────┬────┘    └────┬────┘  └─────────┘     │
│                    │              │                         │
│                    └──────────────┘                         │
│                         mTLS                                │
│                                                             │
│  Istio 控制平面:                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Istiod                                             │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │   │
│  │  │ Pilot    │ │ Citadel  │ │ Galley   │            │   │
│  │  │(流量管理) │ │(证书管理) │ │(配置验证) │            │   │
│  │  └──────────┘ └──────────┘ └──────────┘            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  数据平面:                                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │ Envoy   │ │ Envoy   │ │ Envoy   │ │ Envoy   │          │
│  │ Proxy   │ │ Proxy   │ │ Proxy   │ │ Proxy   │          │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘          │
│       │           │           │           │                │
│  ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐          │
│  │ Service │ │ Service │ │ Service │ │ Service │          │
│  │    A    │ │    B    │ │    C    │ │    D    │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Istio核心功能

| 功能 | 说明 | 应用场景 |
|------|------|----------|
| **流量管理** | 路由、分流、重试、超时 | 金丝雀发布、A/B测试 |
| **安全通信** | mTLS自动加密 | 服务间安全通信 |
| **可观测性** | 指标、日志、追踪 | 监控和故障排查 |
| **策略控制** | 限流、访问控制 | 服务保护 |

### 7.5 可观测性

```
┌─────────────────────────────────────────────────────────────┐
│                    可观测性三大支柱                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 指标 (Metrics)                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • CPU使用率                                         │   │
│  │  • 内存使用率                                        │   │
│  │  • 请求QPS                                           │   │
│  │  • 响应时间P99                                       │   │
│  │  • 错误率                                            │   │
│  │                                                     │   │
│  │  工具: Prometheus, Grafana, Datadog                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  2. 日志 (Logging)                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • 应用日志                                          │   │
│  │  • 访问日志                                          │   │
│  │  • 错误日志                                          │   │
│  │  • 审计日志                                          │   │
│  │                                                     │   │
│  │  工具: ELK Stack, Fluentd, Loki                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  3. 追踪 (Tracing)                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • 请求链路                                          │   │
│  │  • 服务依赖                                          │   │
│  │  • 性能瓶颈                                          │   │
│  │  • 故障定位                                          │   │
│  │                                                     │   │
│  │  工具: Jaeger, Zipkin, SkyWalking                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Python可观测性实现

```python
"""
可观测性实现 - 指标、日志、追踪
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging
import time
import json
import sys

app = FastAPI(title="Observable App", version="1.0.0")

# ═══════════════════════════════════════════════════════════════
# 1. 指标 (Metrics) - Prometheus
# ═══════════════════════════════════════════════════════════════

# 请求计数器
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# 请求耗时直方图
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# 应用指标
ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

ITEMS_IN_DB = Gauge(
    'items_in_database',
    'Number of items in database'
)


# ═══════════════════════════════════════════════════════════════
# 2. 日志 (Logging) - 结构化日志
# ═══════════════════════════════════════════════════════════════

class JSONFormatter(logging.Formatter):
    """JSON格式日志"""

    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


# 配置日志
logger = logging.getLogger("observable_app")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)


# ═══════════════════════════════════════════════════════════════
# 3. 追踪 (Tracing) - OpenTelemetry
# ═══════════════════════════════════════════════════════════════

# 配置Tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# 配置Jaeger导出器
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# 自动插桩FastAPI
FastAPIInstrumentor.instrument_app(app)


# ═══════════════════════════════════════════════════════════════
# 中间件
# ═══════════════════════════════════════════════════════════════

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """指标收集中间件"""
    start_time = time.time()

    # 记录活跃连接
    ACTIVE_CONNECTIONS.inc()

    try:
        response = await call_next(request)

        # 记录请求耗时
        duration = time.time() - start_time
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        # 记录请求数
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()

        # 记录日志
        logger.info(
            f"{request.method} {request.url.path} {response.status_code}",
            extra={"extra_data": {
                "duration_ms": round(duration * 1000, 2),
                "status_code": response.status_code,
                "client_ip": request.client.host if request.client else None
            }}
        )

        return response

    finally:
        ACTIVE_CONNECTIONS.dec()


# ═══════════════════════════════════════════════════════════════
# API端点
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """根路径"""
    with tracer.start_as_current_span("root_operation"):
        logger.info("访问根路径")
        return {"message": "Observable Application"}


@app.get("/metrics")
async def metrics():
    """Prometheus指标端点"""
    from starlette.responses import Response
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "active_connections": ACTIVE_CONNECTIONS._value.get()
    }


@app.get("/items")
async def list_items():
    """列出项目"""
    with tracer.start_as_current_span("list_items") as span:
        # 模拟数据库查询
        items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

        span.set_attribute("items.count", len(items))
        logger.info(f"列出 {len(items)} 个项目")

        ITEMS_IN_DB.set(len(items))

        return {"items": items}


@app.post("/items")
async def create_item(request: Request):
    """创建项目"""
    with tracer.start_as_current_span("create_item") as span:
        data = await request.json()

        span.set_attribute("item.name", data.get("name"))
        logger.info(f"创建项目: {data}")

        # 模拟创建
        return {"id": 3, "name": data.get("name")}


@app.get("/error")
async def trigger_error():
    """触发错误（测试用）"""
    try:
        raise ValueError("测试错误")
    except Exception as e:
        logger.error("发生错误", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ═══════════════════════════════════════════════════════════════
# 启动事件
# ═══════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup():
    """启动事件"""
    logger.info("应用启动", extra={"extra_data": {"event": "startup"}})


@app.on_event("shutdown")
async def shutdown():
    """关闭事件"""
    logger.info("应用关闭", extra={"extra_data": {"event": "shutdown"}})


# ═══════════════════════════════════════════════════════════════
# 运行
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 7.6 云原生最佳实践总结

```
┌─────────────────────────────────────────────────────────────┐
│                  云原生最佳实践                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 容器化                                                  │
│     ✓ 使用多阶段构建减小镜像                                │
│     ✓ 非root用户运行                                        │
│     ✓ 健康检查端点                                          │
│     ✓ 资源限制                                              │
│                                                             │
│  2. Kubernetes                                              │
│     ✓ 使用Deployment管理无状态应用                          │
│     ✓ 使用StatefulSet管理有状态应用                         │
│     ✓ 配置与代码分离（ConfigMap/Secret）                     │
│     ✓ 健康检查和就绪检查                                     │
│     ✓ 水平自动扩缩容（HPA）                                  │
│                                                             │
│  3. 可观测性                                                │
│     ✓ 结构化日志                                            │
│     ✓ 关键指标监控                                          │
│     ✓ 分布式追踪                                            │
│     ✓ 告警配置                                              │
│                                                             │
│  4. 安全                                                    │
│     ✓ 镜像安全扫描                                          │
│     ✓ 最小权限原则                                          │
│     ✓ 密钥管理                                              │
│     ✓ 网络隔离                                              │
│                                                             │
│  5. 持续交付                                                │
│     ✓ GitOps工作流                                          │
│     ✓ 蓝绿部署/金丝雀发布                                    │
│     ✓ 自动化测试                                            │
│     ✓ 回滚策略                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 附录：架构演进路径

```
┌─────────────────────────────────────────────────────────────┐
│                    架构演进路径                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  单体应用                                                   │
│     │                                                       │
│     ▼                                                       │
│  分层架构 ──────────────────────────────────────────────┐  │
│  (三层/N层)                                              │  │
│     │                                                    │  │
│     ▼                                                    │  │
│  领域驱动设计 + 洋葱/整洁架构 ───────────────────────────┤  │
│     │                                                    │  │
│     ▼                                                    │  │
│  微服务架构 ─────────────────────────────────────────────┤  │
│     │                                                    │  │
│     ├──► 服务拆分                                        │  │
│     ├──► API网关                                         │  │
│     ├──► 事件驱动                                        │  │
│     └──► 服务网格                                        │  │
│                                                          │  │
│  云原生架构 ◄────────────────────────────────────────────┘  │
│     │                                                       │
│     ├──► 容器化 (Docker)                                    │
│     ├──► 编排 (Kubernetes)                                  │
│     ├──► Serverless                                         │
│     └──► 可观测性                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 架构选择指南

| 场景 | 推荐架构 | 理由 |
|------|----------|------|
| 初创MVP | 三层架构 | 快速开发，简单维护 |
| 企业应用 | N层/洋葱架构 | 清晰的职责分离 |
| 复杂领域 | DDD + 整洁架构 | 应对业务复杂性 |
| 大规模系统 | 微服务 | 独立扩展，团队自治 |
| 高并发 | 事件驱动 | 异步处理，削峰填谷 |
| 快速迭代 | Serverless | 免运维，按需付费 |
| 云部署 | 云原生 | 充分利用云优势 |

---

*文档生成时间: 2024*

*本文档涵盖现代软件架构的核心模式，所有代码示例均可直接运行。*
