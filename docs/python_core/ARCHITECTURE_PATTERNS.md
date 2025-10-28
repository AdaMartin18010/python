# Python 架构模式与设计 2025

**现代架构模式的Python实践**

---

## 📊 架构模式总览

```mermaid
mindmap
  root((架构模式))
    分层架构
      表现层
      业务层
      数据层
      基础设施层
    
    清洁架构
      实体层
      用例层
      接口适配层
      框架驱动层
    
    领域驱动设计
      战略设计
        限界上下文
        上下文映射
      战术设计
        聚合根
        实体值对象
        领域服务
        仓储
    
    事件驱动架构
      事件溯源
      CQRS
      消息总线
      Saga模式
    
    微服务架构
      服务拆分
      API网关
      服务发现
      配置中心
      分布式追踪
    
    六边形架构
      核心领域
      端口
      适配器
```

---

## 1️⃣ 分层架构 (Layered Architecture)

### 1.1 四层架构模式

```python
"""
分层架构示例 - FastAPI + SQLAlchemy
"""
from typing import Protocol, List
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

# ============================================
# 第1层: 表现层 (Presentation Layer)
# ============================================

class UserCreateRequest(BaseModel):
    """API请求模型"""
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    """API响应模型"""
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

app = FastAPI()

@app.post("/users", response_model=UserResponse)
async def create_user(
    request: UserCreateRequest,
    service: "UserService" = Depends()
) -> UserResponse:
    """创建用户API端点"""
    try:
        user = await service.create_user(
            username=request.username,
            email=request.email,
            password=request.password
        )
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: "UserService" = Depends()
) -> UserResponse:
    """获取用户API端点"""
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)

# ============================================
# 第2层: 业务逻辑层 (Business Logic Layer)
# ============================================

@dataclass
class User:
    """领域模型"""
    id: int | None
    username: str
    email: str
    password_hash: str
    created_at: datetime
    
    def change_email(self, new_email: str) -> None:
        """业务规则: 修改邮箱"""
        if not self._is_valid_email(new_email):
            raise ValueError("Invalid email format")
        self.email = new_email
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """验证邮箱格式"""
        return "@" in email and "." in email.split("@")[1]

class UserService:
    """业务服务层"""
    
    def __init__(self, repository: "UserRepository"):
        self.repository = repository
    
    async def create_user(
        self,
        username: str,
        email: str,
        password: str
    ) -> User:
        """创建用户业务逻辑"""
        # 业务规则验证
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # 检查用户名是否存在
        existing = await self.repository.find_by_username(username)
        if existing:
            raise ValueError("Username already exists")
        
        # 创建用户
        password_hash = self._hash_password(password)
        user = User(
            id=None,
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now()
        )
        
        return await self.repository.save(user)
    
    async def get_user(self, user_id: int) -> User | None:
        """获取用户"""
        return await self.repository.find_by_id(user_id)
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """密码哈希"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

# ============================================
# 第3层: 数据访问层 (Data Access Layer)
# ============================================

class UserRepository(Protocol):
    """仓储接口"""
    
    async def save(self, user: User) -> User: ...
    async def find_by_id(self, user_id: int) -> User | None: ...
    async def find_by_username(self, username: str) -> User | None: ...
    async def delete(self, user_id: int) -> bool: ...

Base = declarative_base()

class UserModel(Base):
    """ORM模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, nullable=False)

class SQLAlchemyUserRepository:
    """SQLAlchemy仓储实现"""
    
    def __init__(self, session):
        self.session = session
    
    async def save(self, user: User) -> User:
        """保存用户"""
        model = UserModel(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        
        return self._to_domain(model)
    
    async def find_by_id(self, user_id: int) -> User | None:
        """根据ID查找"""
        model = await self.session.get(UserModel, user_id)
        return self._to_domain(model) if model else None
    
    async def find_by_username(self, username: str) -> User | None:
        """根据用户名查找"""
        from sqlalchemy import select
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def delete(self, user_id: int) -> bool:
        """删除用户"""
        model = await self.session.get(UserModel, user_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()
            return True
        return False
    
    @staticmethod
    def _to_domain(model: UserModel) -> User:
        """ORM模型转领域模型"""
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            created_at=model.created_at
        )

# ============================================
# 第4层: 基础设施层 (Infrastructure Layer)
# ============================================

class DatabaseConfig:
    """数据库配置"""
    DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DatabaseConfig.DATABASE_URL)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """数据库会话依赖"""
    async with async_session() as session:
        yield session

def get_user_service(
    session: AsyncSession = Depends(get_db)
) -> UserService:
    """用户服务依赖注入"""
    repository = SQLAlchemyUserRepository(session)
    return UserService(repository)
```

### 1.2 分层架构优缺点

**优点**:
- ✅ 关注点分离清晰
- ✅ 易于理解和维护
- ✅ 可测试性好
- ✅ 技术栈替换容易

**缺点**:
- ⚠️ 层级间耦合
- ⚠️ 可能过度工程化
- ⚠️ 性能开销

---

## 2️⃣ 清洁架构 (Clean Architecture)

### 2.1 依赖规则

```
外层依赖内层，内层不知道外层

框架&驱动层 → 接口适配层 → 用例层 → 实体层
   (UI, DB)     (控制器)    (业务)   (核心)
```

### 2.2 Python实现

```python
"""
清洁架构示例
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, List

# ============================================
# 核心层: 实体 (Entities)
# ============================================

@dataclass
class Order:
    """订单实体 - 业务核心"""
    id: int | None
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List["OrderItem"]
    
    def calculate_total(self) -> float:
        """计算总金额 - 业务规则"""
        total = sum(item.price * item.quantity for item in self.items)
        return round(total, 2)
    
    def can_cancel(self) -> bool:
        """是否可以取消 - 业务规则"""
        return self.status in ["pending", "paid"]
    
    def cancel(self) -> None:
        """取消订单 - 业务规则"""
        if not self.can_cancel():
            raise ValueError(f"Cannot cancel order with status: {self.status}")
        self.status = "cancelled"
    
    def confirm(self) -> None:
        """确认订单 - 业务规则"""
        if self.status != "pending":
            raise ValueError(f"Cannot confirm order with status: {self.status}")
        self.status = "confirmed"

@dataclass
class OrderItem:
    """订单项"""
    product_id: int
    product_name: str
    price: float
    quantity: int

# ============================================
# 用例层: 业务用例 (Use Cases)
# ============================================

class CreateOrderUseCase:
    """创建订单用例"""
    
    def __init__(
        self,
        order_repository: "OrderRepository",
        product_repository: "ProductRepository",
        event_publisher: "EventPublisher"
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.event_publisher = event_publisher
    
    async def execute(
        self,
        user_id: int,
        items: List[dict]
    ) -> Order:
        """执行创建订单用例"""
        # 1. 验证产品
        order_items = []
        for item in items:
            product = await self.product_repository.find_by_id(
                item["product_id"]
            )
            if not product:
                raise ValueError(f"Product {item['product_id']} not found")
            
            if product.stock < item["quantity"]:
                raise ValueError(f"Insufficient stock for {product.name}")
            
            order_items.append(OrderItem(
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=item["quantity"]
            ))
        
        # 2. 创建订单实体
        order = Order(
            id=None,
            user_id=user_id,
            total_amount=0,
            status="pending",
            created_at=datetime.now(),
            items=order_items
        )
        order.total_amount = order.calculate_total()
        
        # 3. 保存订单
        saved_order = await self.order_repository.save(order)
        
        # 4. 发布事件
        await self.event_publisher.publish("order.created", {
            "order_id": saved_order.id,
            "user_id": saved_order.user_id,
            "total_amount": saved_order.total_amount
        })
        
        return saved_order

class CancelOrderUseCase:
    """取消订单用例"""
    
    def __init__(
        self,
        order_repository: "OrderRepository",
        event_publisher: "EventPublisher"
    ):
        self.order_repository = order_repository
        self.event_publisher = event_publisher
    
    async def execute(self, order_id: int, user_id: int) -> Order:
        """执行取消订单用例"""
        # 1. 获取订单
        order = await self.order_repository.find_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        
        # 2. 验证权限
        if order.user_id != user_id:
            raise ValueError("Not authorized to cancel this order")
        
        # 3. 取消订单(业务规则在实体中)
        order.cancel()
        
        # 4. 保存
        updated_order = await self.order_repository.update(order)
        
        # 5. 发布事件
        await self.event_publisher.publish("order.cancelled", {
            "order_id": updated_order.id,
            "user_id": updated_order.user_id
        })
        
        return updated_order

# ============================================
# 接口层: 仓储接口 (Repositories)
# ============================================

class OrderRepository(Protocol):
    """订单仓储接口 - 端口"""
    async def save(self, order: Order) -> Order: ...
    async def update(self, order: Order) -> Order: ...
    async def find_by_id(self, order_id: int) -> Order | None: ...
    async def find_by_user(self, user_id: int) -> List[Order]: ...

class ProductRepository(Protocol):
    """产品仓储接口 - 端口"""
    async def find_by_id(self, product_id: int) -> "Product | None": ...

class EventPublisher(Protocol):
    """事件发布器接口 - 端口"""
    async def publish(self, event_type: str, data: dict) -> None: ...

# ============================================
# 外层: 适配器实现 (Adapters)
# ============================================

class PostgresOrderRepository:
    """PostgreSQL适配器"""
    
    def __init__(self, session):
        self.session = session
    
    async def save(self, order: Order) -> Order:
        """保存实现"""
        # ORM映射逻辑
        ...
        return order
    
    async def update(self, order: Order) -> Order:
        """更新实现"""
        # ORM映射逻辑
        ...
        return order
    
    async def find_by_id(self, order_id: int) -> Order | None:
        """查询实现"""
        # ORM映射逻辑
        ...

class RedisEventPublisher:
    """Redis事件发布器适配器"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def publish(self, event_type: str, data: dict) -> None:
        """发布事件到Redis"""
        import json
        await self.redis.publish(
            event_type,
            json.dumps(data)
        )

class RabbitMQEventPublisher:
    """RabbitMQ事件发布器适配器"""
    
    def __init__(self, channel):
        self.channel = channel
    
    async def publish(self, event_type: str, data: dict) -> None:
        """发布事件到RabbitMQ"""
        import json
        await self.channel.basic_publish(
            exchange="events",
            routing_key=event_type,
            body=json.dumps(data)
        )

# ============================================
# 外层: 控制器 (Controllers)
# ============================================

from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/orders")
async def create_order(
    request: dict,
    use_case: CreateOrderUseCase = Depends()
):
    """创建订单控制器"""
    order = await use_case.execute(
        user_id=request["user_id"],
        items=request["items"]
    )
    return {"order_id": order.id, "total": order.total_amount}

@router.post("/orders/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    user_id: int,
    use_case: CancelOrderUseCase = Depends()
):
    """取消订单控制器"""
    order = await use_case.execute(order_id, user_id)
    return {"order_id": order.id, "status": order.status}
```

### 2.3 清洁架构优势

**核心优势**:
- ✅ **独立于框架**: 业务逻辑不依赖框架
- ✅ **可测试**: 核心逻辑易于单元测试
- ✅ **独立于UI**: 可以轻松更换前端
- ✅ **独立于数据库**: 可以更换数据库
- ✅ **独立于外部代理**: 业务规则不知道外部世界

---

## 3️⃣ 领域驱动设计 (DDD)

### 3.1 战略设计

```python
"""
DDD战略设计 - 限界上下文
"""

# ============================================
# 订单上下文 (Order Context)
# ============================================

class OrderContext:
    """订单限界上下文"""
    
    # 订单聚合根
    class Order:
        """订单聚合根"""
        
        def __init__(self, order_id: "OrderId"):
            self.id = order_id
            self.items: List["OrderItem"] = []
            self.status = OrderStatus.PENDING
            self._domain_events: List["DomainEvent"] = []
        
        def add_item(self, product_id: "ProductId", quantity: int) -> None:
            """添加订单项 - 业务操作"""
            # 业务规则验证
            if self.status != OrderStatus.PENDING:
                raise ValueError("Cannot add items to non-pending order")
            
            # 创建订单项(实体)
            item = OrderItem(product_id, quantity)
            self.items.append(item)
            
            # 记录领域事件
            self._domain_events.append(
                OrderItemAdded(self.id, product_id, quantity)
            )
        
        def confirm(self) -> None:
            """确认订单"""
            if self.status != OrderStatus.PENDING:
                raise ValueError("Can only confirm pending orders")
            
            if not self.items:
                raise ValueError("Cannot confirm empty order")
            
            self.status = OrderStatus.CONFIRMED
            self._domain_events.append(OrderConfirmed(self.id))
        
        def get_events(self) -> List["DomainEvent"]:
            """获取领域事件"""
            events = self._domain_events.copy()
            self._domain_events.clear()
            return events
    
    # 值对象
    @dataclass(frozen=True)
    class OrderId:
        """订单ID - 值对象"""
        value: int
    
    @dataclass(frozen=True)
    class ProductId:
        """产品ID - 值对象"""
        value: int
    
    # 实体
    class OrderItem:
        """订单项 - 实体"""
        
        def __init__(self, product_id: "ProductId", quantity: int):
            self.product_id = product_id
            self.quantity = quantity
            self._validate()
        
        def _validate(self) -> None:
            if self.quantity <= 0:
                raise ValueError("Quantity must be positive")
    
    # 枚举
    from enum import Enum
    
    class OrderStatus(Enum):
        """订单状态"""
        PENDING = "pending"
        CONFIRMED = "confirmed"
        SHIPPED = "shipped"
        DELIVERED = "delivered"
        CANCELLED = "cancelled"
    
    # 领域事件
    @dataclass
    class DomainEvent:
        """领域事件基类"""
        occurred_at: datetime
    
    @dataclass
    class OrderItemAdded(DomainEvent):
        """订单项已添加事件"""
        order_id: "OrderId"
        product_id: "ProductId"
        quantity: int
    
    @dataclass
    class OrderConfirmed(DomainEvent):
        """订单已确认事件"""
        order_id: "OrderId"
    
    # 领域服务
    class OrderPricingService:
        """订单定价服务 - 领域服务"""
        
        def __init__(self, product_catalog: "ProductCatalog"):
            self.product_catalog = product_catalog
        
        async def calculate_total(self, order: "Order") -> float:
            """计算订单总金额"""
            total = 0.0
            for item in order.items:
                product = await self.product_catalog.find(item.product_id)
                total += product.price * item.quantity
            return total
    
    # 仓储接口
    class OrderRepository(Protocol):
        """订单仓储"""
        async def save(self, order: "Order") -> None: ...
        async def find(self, order_id: "OrderId") -> "Order | None": ...
        async def next_id(self) -> "OrderId": ...

# ============================================
# 库存上下文 (Inventory Context)
# ============================================

class InventoryContext:
    """库存限界上下文"""
    
    class Product:
        """产品聚合根"""
        
        def __init__(self, product_id: "ProductId", stock: int):
            self.id = product_id
            self.stock = stock
        
        def reserve(self, quantity: int) -> None:
            """预留库存"""
            if self.stock < quantity:
                raise ValueError("Insufficient stock")
            self.stock -= quantity
        
        def release(self, quantity: int) -> None:
            """释放库存"""
            self.stock += quantity
    
    @dataclass(frozen=True)
    class ProductId:
        """产品ID"""
        value: int
    
    class ProductRepository(Protocol):
        """产品仓储"""
        async def find(self, product_id: "ProductId") -> "Product | None": ...
        async def save(self, product: "Product") -> None: ...

# ============================================
# 上下文映射 (Context Mapping)
# ============================================

class OrderToInventoryMapper:
    """订单上下文到库存上下文的映射"""
    
    @staticmethod
    def map_product_id(
        order_product_id: OrderContext.ProductId
    ) -> InventoryContext.ProductId:
        """映射产品ID"""
        return InventoryContext.ProductId(order_product_id.value)

class ReserveInventoryOnOrderConfirmed:
    """订单确认时预留库存 - 集成事件处理"""
    
    def __init__(
        self,
        inventory_repo: InventoryContext.ProductRepository,
        mapper: OrderToInventoryMapper
    ):
        self.inventory_repo = inventory_repo
        self.mapper = mapper
    
    async def handle(self, event: OrderContext.OrderConfirmed) -> None:
        """处理订单确认事件"""
        # 这里需要从订单上下文获取订单详情
        # 然后在库存上下文中预留库存
        ...
```

### 3.2 战术设计模式

```python
"""
DDD战术模式
"""
from typing import Generic, TypeVar

# ============================================
# 1. 聚合 (Aggregate)
# ============================================

class Aggregate:
    """聚合基类"""
    
    def __init__(self):
        self._domain_events: List[DomainEvent] = []
    
    def add_event(self, event: DomainEvent) -> None:
        """添加领域事件"""
        self._domain_events.append(event)
    
    def clear_events(self) -> List[DomainEvent]:
        """清除并返回事件"""
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events

# ============================================
# 2. 实体 (Entity)
# ============================================

T = TypeVar("T")

class Entity(Generic[T]):
    """实体基类"""
    
    def __init__(self, id: T):
        self._id = id
    
    @property
    def id(self) -> T:
        return self._id
    
    def __eq__(self, other: object) -> bool:
        """实体相等性基于ID"""
        if not isinstance(other, Entity):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)

# ============================================
# 3. 值对象 (Value Object)
# ============================================

@dataclass(frozen=True)
class Money:
    """金额值对象"""
    amount: float
    currency: str
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if self.currency not in ["USD", "EUR", "CNY"]:
            raise ValueError(f"Unsupported currency: {self.currency}")
    
    def add(self, other: "Money") -> "Money":
        """加法"""
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def multiply(self, factor: float) -> "Money":
        """乘法"""
        return Money(self.amount * factor, self.currency)

@dataclass(frozen=True)
class Address:
    """地址值对象"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    
    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}, {self.country}"

# ============================================
# 4. 领域服务 (Domain Service)
# ============================================

class TransferService:
    """转账服务 - 领域服务"""
    
    async def transfer(
        self,
        from_account: "Account",
        to_account: "Account",
        amount: Money
    ) -> None:
        """转账操作"""
        # 业务规则: 同一货币才能转账
        if from_account.balance.currency != amount.currency:
            raise ValueError("Currency mismatch")
        
        # 执行转账
        from_account.withdraw(amount)
        to_account.deposit(amount)
        
        # 记录领域事件
        from_account.add_event(MoneyTransferred(
            from_account.id,
            to_account.id,
            amount
        ))

# ============================================
# 5. 仓储 (Repository)
# ============================================

class Repository(Protocol, Generic[T]):
    """仓储基类"""
    
    async def save(self, entity: T) -> None:
        """保存实体"""
        ...
    
    async def find_by_id(self, id: any) -> T | None:
        """根据ID查找"""
        ...
    
    async def delete(self, entity: T) -> None:
        """删除实体"""
        ...

# ============================================
# 6. 工厂 (Factory)
# ============================================

class OrderFactory:
    """订单工厂"""
    
    @staticmethod
    def create_order(
        user_id: int,
        shipping_address: Address
    ) -> "Order":
        """创建订单"""
        order_id = OrderId(generate_unique_id())
        order = Order(order_id, user_id)
        order.set_shipping_address(shipping_address)
        order.add_event(OrderCreated(order_id, user_id))
        return order
    
    @staticmethod
    def create_from_cart(cart: "ShoppingCart") -> "Order":
        """从购物车创建订单"""
        order = OrderFactory.create_order(
            cart.user_id,
            cart.shipping_address
        )
        for item in cart.items:
            order.add_item(item.product_id, item.quantity)
        return order

# ============================================
# 7. 规约 (Specification)
# ============================================

class Specification(ABC, Generic[T]):
    """规约模式基类"""
    
    @abstractmethod
    def is_satisfied_by(self, entity: T) -> bool:
        """是否满足规约"""
        ...
    
    def and_(self, other: "Specification[T]") -> "Specification[T]":
        """与操作"""
        return AndSpecification(self, other)
    
    def or_(self, other: "Specification[T]") -> "Specification[T]":
        """或操作"""
        return OrSpecification(self, other)
    
    def not_(self) -> "Specification[T]":
        """非操作"""
        return NotSpecification(self)

class OrderIsOverdueSpecification(Specification["Order"]):
    """订单逾期规约"""
    
    def is_satisfied_by(self, order: "Order") -> bool:
        """检查订单是否逾期"""
        days_since_created = (datetime.now() - order.created_at).days
        return (
            order.status == OrderStatus.PENDING
            and days_since_created > 7
        )

class AndSpecification(Specification[T]):
    """与规约"""
    
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right
    
    def is_satisfied_by(self, entity: T) -> bool:
        return (
            self.left.is_satisfied_by(entity)
            and self.right.is_satisfied_by(entity)
        )
```

---

## 4️⃣ 事件驱动架构 (Event-Driven Architecture)

### 4.1 事件溯源 (Event Sourcing)

```python
"""
事件溯源模式
"""
from typing import List, Type
from dataclasses import dataclass, field
from datetime import datetime
import json

# ============================================
# 领域事件
# ============================================

@dataclass
class DomainEvent:
    """领域事件基类"""
    event_id: str
    aggregate_id: str
    occurred_at: datetime
    version: int
    
    def to_dict(self) -> dict:
        """序列化"""
        return {
            "event_type": self.__class__.__name__,
            "event_id": self.event_id,
            "aggregate_id": self.aggregate_id,
            "occurred_at": self.occurred_at.isoformat(),
            "version": self.version,
            **self._data()
        }
    
    @abstractmethod
    def _data(self) -> dict:
        """事件数据"""
        ...

@dataclass
class AccountCreated(DomainEvent):
    """账户已创建"""
    owner_name: str
    initial_balance: float
    
    def _data(self) -> dict:
        return {
            "owner_name": self.owner_name,
            "initial_balance": self.initial_balance
        }

@dataclass
class MoneyDeposited(DomainEvent):
    """已存款"""
    amount: float
    
    def _data(self) -> dict:
        return {"amount": self.amount}

@dataclass
class MoneyWithdrawn(DomainEvent):
    """已取款"""
    amount: float
    
    def _data(self) -> dict:
        return {"amount": self.amount}

# ============================================
# 聚合根(使用事件溯源)
# ============================================

class Account:
    """银行账户聚合根"""
    
    def __init__(self, account_id: str):
        self.id = account_id
        self.owner_name: str = ""
        self.balance: float = 0.0
        self.version: int = 0
        self._uncommitted_events: List[DomainEvent] = []
    
    # ========== 命令方法 ==========
    
    @staticmethod
    def create(
        account_id: str,
        owner_name: str,
        initial_balance: float
    ) -> "Account":
        """创建账户"""
        account = Account(account_id)
        event = AccountCreated(
            event_id=generate_uuid(),
            aggregate_id=account_id,
            occurred_at=datetime.now(),
            version=1,
            owner_name=owner_name,
            initial_balance=initial_balance
        )
        account._apply_event(event)
        account._uncommitted_events.append(event)
        return account
    
    def deposit(self, amount: float) -> None:
        """存款"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        event = MoneyDeposited(
            event_id=generate_uuid(),
            aggregate_id=self.id,
            occurred_at=datetime.now(),
            version=self.version + 1,
            amount=amount
        )
        self._apply_event(event)
        self._uncommitted_events.append(event)
    
    def withdraw(self, amount: float) -> None:
        """取款"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        
        event = MoneyWithdrawn(
            event_id=generate_uuid(),
            aggregate_id=self.id,
            occurred_at=datetime.now(),
            version=self.version + 1,
            amount=amount
        )
        self._apply_event(event)
        self._uncommitted_events.append(event)
    
    # ========== 事件应用 ==========
    
    def _apply_event(self, event: DomainEvent) -> None:
        """应用事件到状态"""
        if isinstance(event, AccountCreated):
            self._apply_account_created(event)
        elif isinstance(event, MoneyDeposited):
            self._apply_money_deposited(event)
        elif isinstance(event, MoneyWithdrawn):
            self._apply_money_withdrawn(event)
        
        self.version = event.version
    
    def _apply_account_created(self, event: AccountCreated) -> None:
        """应用账户创建事件"""
        self.owner_name = event.owner_name
        self.balance = event.initial_balance
    
    def _apply_money_deposited(self, event: MoneyDeposited) -> None:
        """应用存款事件"""
        self.balance += event.amount
    
    def _apply_money_withdrawn(self, event: MoneyWithdrawn) -> None:
        """应用取款事件"""
        self.balance -= event.amount
    
    # ========== 事件管理 ==========
    
    def get_uncommitted_events(self) -> List[DomainEvent]:
        """获取未提交事件"""
        return self._uncommitted_events.copy()
    
    def mark_events_as_committed(self) -> None:
        """标记事件已提交"""
        self._uncommitted_events.clear()
    
    # ========== 事件溯源重放 ==========
    
    @staticmethod
    def from_events(events: List[DomainEvent]) -> "Account":
        """从事件流重建聚合"""
        if not events:
            raise ValueError("No events to rebuild from")
        
        first_event = events[0]
        if not isinstance(first_event, AccountCreated):
            raise ValueError("First event must be AccountCreated")
        
        account = Account(first_event.aggregate_id)
        for event in events:
            account._apply_event(event)
        
        return account

# ============================================
# 事件存储
# ============================================

class EventStore:
    """事件存储"""
    
    def __init__(self, connection):
        self.connection = connection
    
    async def save_events(
        self,
        aggregate_id: str,
        events: List[DomainEvent],
        expected_version: int
    ) -> None:
        """保存事件流"""
        # 乐观锁: 检查版本号
        current_version = await self._get_current_version(aggregate_id)
        if current_version != expected_version:
            raise ValueError(
                f"Concurrency conflict: expected {expected_version}, "
                f"got {current_version}"
            )
        
        # 保存事件
        for event in events:
            await self._append_event(event)
    
    async def _append_event(self, event: DomainEvent) -> None:
        """追加事件"""
        query = """
            INSERT INTO events (
                event_id, aggregate_id, event_type, event_data,
                occurred_at, version
            ) VALUES ($1, $2, $3, $4, $5, $6)
        """
        await self.connection.execute(
            query,
            event.event_id,
            event.aggregate_id,
            event.__class__.__name__,
            json.dumps(event.to_dict()),
            event.occurred_at,
            event.version
        )
    
    async def get_events(
        self,
        aggregate_id: str,
        from_version: int = 0
    ) -> List[DomainEvent]:
        """获取事件流"""
        query = """
            SELECT event_type, event_data
            FROM events
            WHERE aggregate_id = $1 AND version > $2
            ORDER BY version ASC
        """
        rows = await self.connection.fetch(query, aggregate_id, from_version)
        
        events = []
        for row in rows:
            event = self._deserialize_event(row["event_type"], row["event_data"])
            events.append(event)
        
        return events
    
    async def _get_current_version(self, aggregate_id: str) -> int:
        """获取当前版本号"""
        query = """
            SELECT COALESCE(MAX(version), 0) as version
            FROM events
            WHERE aggregate_id = $1
        """
        row = await self.connection.fetchrow(query, aggregate_id)
        return row["version"]
    
    def _deserialize_event(
        self,
        event_type: str,
        event_data: str
    ) -> DomainEvent:
        """反序列化事件"""
        data = json.loads(event_data)
        event_class = globals()[event_type]
        return event_class(**data)

# ============================================
# 应用服务(使用事件溯源)
# ============================================

class AccountApplicationService:
    """账户应用服务"""
    
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
    
    async def create_account(
        self,
        account_id: str,
        owner_name: str,
        initial_balance: float
    ) -> None:
        """创建账户"""
        # 创建聚合
        account = Account.create(account_id, owner_name, initial_balance)
        
        # 保存事件
        events = account.get_uncommitted_events()
        await self.event_store.save_events(account_id, events, 0)
        account.mark_events_as_committed()
    
    async def deposit(self, account_id: str, amount: float) -> None:
        """存款"""
        # 从事件重建聚合
        events = await self.event_store.get_events(account_id)
        account = Account.from_events(events)
        expected_version = account.version
        
        # 执行命令
        account.deposit(amount)
        
        # 保存新事件
        new_events = account.get_uncommitted_events()
        await self.event_store.save_events(
            account_id,
            new_events,
            expected_version
        )
        account.mark_events_as_committed()
    
    async def withdraw(self, account_id: str, amount: float) -> None:
        """取款"""
        # 类似deposit实现
        events = await self.event_store.get_events(account_id)
        account = Account.from_events(events)
        expected_version = account.version
        
        account.withdraw(amount)
        
        new_events = account.get_uncommitted_events()
        await self.event_store.save_events(
            account_id,
            new_events,
            expected_version
        )
        account.mark_events_as_committed()
```

### 4.2 CQRS (命令查询职责分离)

```python
"""
CQRS模式
"""

# ============================================
# 命令端 (Write Side)
# ============================================

@dataclass
class Command:
    """命令基类"""
    pass

@dataclass
class CreateOrderCommand(Command):
    """创建订单命令"""
    order_id: str
    user_id: int
    items: List[dict]

@dataclass
class CancelOrderCommand(Command):
    """取消订单命令"""
    order_id: str
    user_id: int

class CommandHandler(ABC, Generic[T]):
    """命令处理器基类"""
    
    @abstractmethod
    async def handle(self, command: T) -> None:
        """处理命令"""
        ...

class CreateOrderCommandHandler(CommandHandler[CreateOrderCommand]):
    """创建订单命令处理器"""
    
    def __init__(
        self,
        event_store: EventStore,
        event_bus: "EventBus"
    ):
        self.event_store = event_store
        self.event_bus = event_bus
    
    async def handle(self, command: CreateOrderCommand) -> None:
        """处理创建订单"""
        # 1. 创建聚合并执行业务逻辑
        order = Order.create(
            order_id=command.order_id,
            user_id=command.user_id
        )
        
        for item in command.items:
            order.add_item(item["product_id"], item["quantity"])
        
        # 2. 保存事件
        events = order.get_uncommitted_events()
        await self.event_store.save_events(
            command.order_id,
            events,
            0
        )
        
        # 3. 发布事件到事件总线
        for event in events:
            await self.event_bus.publish(event)

# ============================================
# 查询端 (Read Side)
# ============================================

@dataclass
class Query:
    """查询基类"""
    pass

@dataclass
class GetOrderQuery(Query):
    """获取订单查询"""
    order_id: str

@dataclass
class ListUserOrdersQuery(Query):
    """列出用户订单查询"""
    user_id: int
    page: int = 1
    page_size: int = 20

@dataclass
class OrderReadModel:
    """订单读模型"""
    order_id: str
    user_id: int
    total_amount: float
    status: str
    items: List[dict]
    created_at: datetime
    updated_at: datetime

class QueryHandler(ABC, Generic[T, R]):
    """查询处理器基类"""
    
    @abstractmethod
    async def handle(self, query: T) -> R:
        """处理查询"""
        ...

class GetOrderQueryHandler(QueryHandler[GetOrderQuery, OrderReadModel | None]):
    """获取订单查询处理器"""
    
    def __init__(self, read_db):
        self.read_db = read_db
    
    async def handle(self, query: GetOrderQuery) -> OrderReadModel | None:
        """处理查询"""
        # 从读模型数据库查询
        result = await self.read_db.fetchrow(
            "SELECT * FROM order_read_model WHERE order_id = $1",
            query.order_id
        )
        
        if not result:
            return None
        
        return OrderReadModel(**dict(result))

class ListUserOrdersQueryHandler(
    QueryHandler[ListUserOrdersQuery, List[OrderReadModel]]
):
    """列出用户订单查询处理器"""
    
    def __init__(self, read_db):
        self.read_db = read_db
    
    async def handle(self, query: ListUserOrdersQuery) -> List[OrderReadModel]:
        """处理查询"""
        offset = (query.page - 1) * query.page_size
        
        results = await self.read_db.fetch(
            """
            SELECT * FROM order_read_model
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT $2 OFFSET $3
            """,
            query.user_id,
            query.page_size,
            offset
        )
        
        return [OrderReadModel(**dict(r)) for r in results]

# ============================================
# 事件处理器 (更新读模型)
# ============================================

class OrderCreatedEventHandler:
    """订单创建事件处理器"""
    
    def __init__(self, read_db):
        self.read_db = read_db
    
    async def handle(self, event: "OrderCreated") -> None:
        """更新读模型"""
        await self.read_db.execute(
            """
            INSERT INTO order_read_model (
                order_id, user_id, total_amount, status,
                items, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            event.aggregate_id,
            event.user_id,
            0.0,  # 初始金额
            "pending",
            json.dumps([]),
            event.occurred_at,
            event.occurred_at
        )

class OrderConfirmedEventHandler:
    """订单确认事件处理器"""
    
    def __init__(self, read_db):
        self.read_db = read_db
    
    async def handle(self, event: "OrderConfirmed") -> None:
        """更新读模型"""
        await self.read_db.execute(
            """
            UPDATE order_read_model
            SET status = $1, updated_at = $2
            WHERE order_id = $3
            """,
            "confirmed",
            event.occurred_at,
            event.aggregate_id
        )

# ============================================
# 命令/查询总线
# ============================================

class CommandBus:
    """命令总线"""
    
    def __init__(self):
        self._handlers: dict[Type[Command], CommandHandler] = {}
    
    def register(
        self,
        command_type: Type[Command],
        handler: CommandHandler
    ) -> None:
        """注册处理器"""
        self._handlers[command_type] = handler
    
    async def dispatch(self, command: Command) -> None:
        """分发命令"""
        handler = self._handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler for {type(command).__name__}")
        
        await handler.handle(command)

class QueryBus:
    """查询总线"""
    
    def __init__(self):
        self._handlers: dict[Type[Query], QueryHandler] = {}
    
    def register(
        self,
        query_type: Type[Query],
        handler: QueryHandler
    ) -> None:
        """注册处理器"""
        self._handlers[query_type] = handler
    
    async def dispatch(self, query: Query) -> any:
        """分发查询"""
        handler = self._handlers.get(type(query))
        if not handler:
            raise ValueError(f"No handler for {type(query).__name__}")
        
        return await handler.handle(query)
```

---

## 5️⃣ 微服务架构模式

### 5.1 API网关模式

```python
"""
API网关实现
"""
from fastapi import FastAPI, Request, HTTPException
from httpx import AsyncClient
import asyncio

class APIGateway:
    """API网关"""
    
    def __init__(self):
        self.app = FastAPI(title="API Gateway")
        self.http_client = AsyncClient()
        
        # 服务注册表
        self.services = {
            "user": "http://user-service:8001",
            "order": "http://order-service:8002",
            "product": "http://product-service:8003",
        }
        
        self._setup_routes()
    
    def _setup_routes(self) -> None:
        """设置路由"""
        
        # 用户服务路由
        @self.app.api_route(
            "/api/users/{path:path}",
            methods=["GET", "POST", "PUT", "DELETE"]
        )
        async def user_proxy(request: Request, path: str):
            return await self._proxy_request("user", path, request)
        
        # 订单服务路由
        @self.app.api_route(
            "/api/orders/{path:path}",
            methods=["GET", "POST", "PUT", "DELETE"]
        )
        async def order_proxy(request: Request, path: str):
            return await self._proxy_request("order", path, request)
        
        # 聚合API: 获取订单详情(包含用户和产品信息)
        @self.app.get("/api/orders/{order_id}/details")
        async def get_order_details(order_id: str):
            return await self._get_order_details(order_id)
    
    async def _proxy_request(
        self,
        service: str,
        path: str,
        request: Request
    ) -> dict:
        """代理请求到后端服务"""
        service_url = self.services.get(service)
        if not service_url:
            raise HTTPException(status_code=404, detail="Service not found")
        
        # 构造完整URL
        url = f"{service_url}/{path}"
        
        # 转发请求
        try:
            response = await self.http_client.request(
                method=request.method,
                url=url,
                headers=dict(request.headers),
                content=await request.body()
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _get_order_details(self, order_id: str) -> dict:
        """聚合多个服务的数据"""
        # 并行调用多个服务
        order_task = self.http_client.get(
            f"{self.services['order']}/orders/{order_id}"
        )
        
        order_response = await order_task
        order_data = order_response.json()
        
        # 获取用户信息
        user_task = self.http_client.get(
            f"{self.services['user']}/users/{order_data['user_id']}"
        )
        
        # 获取产品信息
        product_tasks = [
            self.http_client.get(
                f"{self.services['product']}/products/{item['product_id']}"
            )
            for item in order_data["items"]
        ]
        
        # 等待所有请求完成
        user_response, *product_responses = await asyncio.gather(
            user_task,
            *product_tasks
        )
        
        # 组装响应
        return {
            "order": order_data,
            "user": user_response.json(),
            "products": [r.json() for r in product_responses]
        }
```

### 5.2 服务发现模式

```python
"""
服务发现实现
"""
from typing import Dict, List
import consul
import random

class ServiceDiscovery:
    """服务发现"""
    
    def __init__(self, consul_host: str = "localhost", consul_port: int = 8500):
        self.consul = consul.Consul(host=consul_host, port=consul_port)
    
    def register_service(
        self,
        service_name: str,
        service_id: str,
        host: str,
        port: int,
        tags: List[str] = None
    ) -> None:
        """注册服务"""
        self.consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=host,
            port=port,
            tags=tags or [],
            check=consul.Check.http(
                f"http://{host}:{port}/health",
                interval="10s",
                timeout="5s"
            )
        )
    
    def deregister_service(self, service_id: str) -> None:
        """注销服务"""
        self.consul.agent.service.deregister(service_id)
    
    def discover_service(
        self,
        service_name: str,
        tag: str | None = None
    ) -> str | None:
        """发现服务(负载均衡)"""
        # 获取健康的服务实例
        _, services = self.consul.health.service(
            service_name,
            passing=True,
            tag=tag
        )
        
        if not services:
            return None
        
        # 随机选择一个实例(简单负载均衡)
        service = random.choice(services)
        address = service["Service"]["Address"]
        port = service["Service"]["Port"]
        
        return f"http://{address}:{port}"

# 使用示例
class MicroserviceApp:
    """微服务应用"""
    
    def __init__(self):
        self.app = FastAPI()
        self.service_discovery = ServiceDiscovery()
        self.service_id = f"order-service-{uuid.uuid4()}"
        
        # 启动时注册服务
        self.service_discovery.register_service(
            service_name="order-service",
            service_id=self.service_id,
            host="localhost",
            port=8002,
            tags=["v1", "production"]
        )
        
        # 设置路由
        @self.app.get("/orders/{order_id}")
        async def get_order(order_id: str):
            # 调用用户服务
            user_service_url = self.service_discovery.discover_service(
                "user-service"
            )
            if not user_service_url:
                raise HTTPException(
                    status_code=503,
                    detail="User service unavailable"
                )
            
            # 调用用户服务API
            async with AsyncClient() as client:
                response = await client.get(
                    f"{user_service_url}/users/{order_id}"
                )
                return response.json()
        
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy"}
    
    def shutdown(self):
        """关闭时注销服务"""
        self.service_discovery.deregister_service(self.service_id)
```

---

## 📚 总结与选择指南

### 架构模式选择矩阵

| 场景 | 推荐架构 | 理由 |
|------|---------|------|
| **小型单体应用** | 分层架构 | 简单直接,易于实现 |
| **中型业务应用** | 清洁架构 | 可测试,易维护 |
| **复杂业务系统** | DDD | 业务复杂度高,需要深度建模 |
| **高并发系统** | 事件驱动 | 异步解耦,可扩展 |
| **大规模分布式** | 微服务 | 独立部署,技术异构 |
| **金融/审计系统** | 事件溯源+CQRS | 完整历史,审计追溯 |

### 架构演进路径

```
简单系统 → 分层架构
    ↓
业务复杂 → 清洁架构/DDD
    ↓
性能要求 → 事件驱动
    ↓
规模扩展 → 微服务架构
```

---

**选择合适的架构,构建可持续的系统!** 🏗️✨

**最后更新**: 2025年10月28日

