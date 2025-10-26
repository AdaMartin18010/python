"""
FastAPI - 完整的实战应用示例

展示6个实际应用场景：
1. 博客系统（Blog System）
2. 电商平台（E-commerce Platform）
3. 任务管理系统（Task Management）
4. 实时聊天（Real-time Chat）
5. 文件分享系统（File Sharing）
6. API限流和监控（Rate Limiting & Monitoring）
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
    HTTPException,
    Request,
    UploadFile,
    WebSocket,
    status,
)
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import String, Text, Integer, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app import Base, get_db, get_current_active_user, User

# ============================================================================
# 场景1: 博客系统
# ============================================================================


class BlogStatus(str, Enum):
    """博客状态"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class BlogPost(Base):
    """博客文章模型"""
    __tablename__ = "blog_posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[str] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20), default=BlogStatus.DRAFT)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    published_at: Mapped[datetime | None] = mapped_column()
    
    # 关系
    author: Mapped["User"] = relationship()
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    """评论模型"""
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # 关系
    post: Mapped["BlogPost"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship()


class BlogPostCreate(BaseModel):
    """创建博客文章"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=10)
    summary: str | None = Field(None, max_length=500)
    status: BlogStatus = BlogStatus.DRAFT


class BlogPostResponse(BaseModel):
    """博客文章响应"""
    id: int
    title: str
    content: str
    summary: str | None
    status: str
    author_id: int
    view_count: int
    created_at: datetime
    published_at: datetime | None
    
    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    """创建评论"""
    content: str = Field(..., min_length=1, max_length=1000)


class CommentResponse(BaseModel):
    """评论响应"""
    id: int
    content: str
    author_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}


app_blog = FastAPI(title="Blog System API")


@app_blog.post("/posts/", response_model=BlogPostResponse)
async def create_post(
    post_in: BlogPostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建博客文章"""
    db_post = BlogPost(
        **post_in.model_dump(),
        author_id=current_user.id
    )
    
    if post_in.status == BlogStatus.PUBLISHED:
        db_post.published_at = datetime.utcnow()
    
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    
    return db_post


@app_blog.get("/posts/{post_id}", response_model=BlogPostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """获取博客文章（增加浏览量）"""
    result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 增加浏览量
    post.view_count += 1
    await db.commit()
    
    return post


@app_blog.post("/posts/{post_id}/publish", response_model=BlogPostResponse)
async def publish_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """发布博客文章"""
    result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    post.status = BlogStatus.PUBLISHED
    post.published_at = datetime.utcnow()
    await db.commit()
    await db.refresh(post)
    
    return post


@app_blog.post("/posts/{post_id}/comments/", response_model=CommentResponse)
async def create_comment(
    post_id: int,
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """添加评论"""
    # 检查文章是否存在
    result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(
        content=comment_in.content,
        post_id=post_id,
        author_id=current_user.id
    )
    
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    
    return db_comment


@app_blog.get("/posts/{post_id}/comments/", response_model=list[CommentResponse])
async def get_post_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    """获取文章评论"""
    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())
    )
    comments = list(result.scalars().all())
    
    return comments


# ============================================================================
# 场景2: 电商平台
# ============================================================================


class OrderStatus(str, Enum):
    """订单状态"""
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Product(Base):
    """商品模型"""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Order(Base):
    """订单模型"""
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(20), default=OrderStatus.PENDING)
    total_amount: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # 关系
    user: Mapped["User"] = relationship()
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    """订单项模型"""
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column()
    
    # 关系
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()


class ProductCreate(BaseModel):
    """创建商品"""
    name: str
    description: str
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: str


class ProductResponse(BaseModel):
    """商品响应"""
    id: int
    name: str
    description: str
    price: float
    stock: int
    category: str
    
    model_config = {"from_attributes": True}


class OrderItemCreate(BaseModel):
    """创建订单项"""
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    """创建订单"""
    items: list[OrderItemCreate]


class OrderResponse(BaseModel):
    """订单响应"""
    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    
    model_config = {"from_attributes": True}


app_ecommerce = FastAPI(title="E-commerce API")


@app_ecommerce.post("/products/", response_model=ProductResponse)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建商品"""
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    
    return db_product


@app_ecommerce.get("/products/", response_model=list[ProductResponse])
async def list_products(
    category: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """列出商品"""
    query = select(Product)
    
    if category:
        query = query.where(Product.category == category)
    
    result = await db.execute(query.offset(skip).limit(limit))
    products = list(result.scalars().all())
    
    return products


@app_ecommerce.post("/orders/", response_model=OrderResponse)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建订单"""
    total_amount = 0.0
    order_items_data = []
    
    # 验证商品和计算总价
    for item_in in order_in.items:
        result = await db.execute(
            select(Product).where(Product.id == item_in.product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item_in.product_id} not found"
            )
        
        if product.stock < item_in.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )
        
        item_total = product.price * item_in.quantity
        total_amount += item_total
        
        order_items_data.append({
            "product_id": product.id,
            "quantity": item_in.quantity,
            "price": product.price
        })
        
        # 减少库存
        product.stock -= item_in.quantity
    
    # 创建订单
    db_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status=OrderStatus.PENDING
    )
    db.add(db_order)
    await db.flush()
    
    # 创建订单项
    for item_data in order_items_data:
        db_item = OrderItem(order_id=db_order.id, **item_data)
        db.add(db_item)
    
    await db.commit()
    await db.refresh(db_order)
    
    return db_order


@app_ecommerce.get("/orders/my", response_model=list[OrderResponse])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取我的订单"""
    result = await db.execute(
        select(Order)
        .where(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
    )
    orders = list(result.scalars().all())
    
    return orders


# ============================================================================
# 场景3: 任务管理系统
# ============================================================================


class TaskPriority(str, Enum):
    """任务优先级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    """任务状态"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default=TaskStatus.TODO)
    priority: Mapped[str] = mapped_column(String(20), default=TaskPriority.MEDIUM)
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    due_date: Mapped[datetime | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column()
    
    # 关系
    assignee: Mapped["User"] = relationship()


class TaskCreate(BaseModel):
    """创建任务"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: int
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    """更新任务"""
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    """任务响应"""
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    assignee_id: int
    due_date: datetime | None
    created_at: datetime
    completed_at: datetime | None
    
    model_config = {"from_attributes": True}


app_tasks = FastAPI(title="Task Management API")


@app_tasks.post("/tasks/", response_model=TaskResponse)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建任务"""
    db_task = Task(**task_in.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    
    return db_task


@app_tasks.get("/tasks/my", response_model=list[TaskResponse])
async def get_my_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取我的任务"""
    query = select(Task).where(Task.assignee_id == current_user.id)
    
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    
    result = await db.execute(query.order_by(Task.due_date))
    tasks = list(result.scalars().all())
    
    return tasks


@app_tasks.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """更新任务"""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = task_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(task, field, value)
    
    # 如果标记为完成，设置完成时间
    if task_in.status == TaskStatus.DONE and not task.completed_at:
        task.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(task)
    
    return task


@app_tasks.get("/tasks/overdue", response_model=list[TaskResponse])
async def get_overdue_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取逾期任务"""
    now = datetime.utcnow()
    result = await db.execute(
        select(Task)
        .where(
            Task.assignee_id == current_user.id,
            Task.status != TaskStatus.DONE,
            Task.due_date < now
        )
        .order_by(Task.due_date)
    )
    tasks = list(result.scalars().all())
    
    return tasks


# ============================================================================
# 场景4: 实时聊天
# ============================================================================


class ChatMessage(Base):
    """聊天消息模型"""
    __tablename__ = "chat_messages"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[str] = mapped_column(String(100), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # 关系
    user: Mapped["User"] = relationship()


class ChatRoom:
    """聊天室管理器"""
    
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
    
    async def connect(self, room_id: str, websocket: WebSocket):
        """连接到聊天室"""
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        
        self.active_connections[room_id].append(websocket)
    
    def disconnect(self, room_id: str, websocket: WebSocket):
        """断开连接"""
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
    
    async def broadcast(self, room_id: str, message: str):
        """广播消息到聊天室"""
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)


chat_manager = ChatRoom()

app_chat = FastAPI(title="Real-time Chat API")


@app_chat.websocket("/ws/chat/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: str,
    db: AsyncSession = Depends(get_db)
):
    """WebSocket聊天端点"""
    await chat_manager.connect(room_id, websocket)
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_json()
            
            # 保存到数据库
            message = ChatMessage(
                room_id=room_id,
                user_id=data["user_id"],
                content=data["content"]
            )
            db.add(message)
            await db.commit()
            
            # 广播给房间内所有用户
            await chat_manager.broadcast(
                room_id,
                f"{data['username']}: {data['content']}"
            )
    
    except WebSocketDisconnect:
        chat_manager.disconnect(room_id, websocket)


@app_chat.get("/chat/{room_id}/history")
async def get_chat_history(
    room_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """获取聊天历史"""
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.room_id == room_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )
    messages = list(result.scalars().all())
    
    return messages[::-1]  # 反转顺序


# ============================================================================
# 场景5: 文件分享系统
# ============================================================================


import aiofiles
import os
from pathlib import Path


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class SharedFile(Base):
    """共享文件模型"""
    __tablename__ = "shared_files"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    filepath: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(100))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_public: Mapped[bool] = mapped_column(default=False)
    download_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # 关系
    owner: Mapped["User"] = relationship()


class FileResponse(BaseModel):
    """文件响应"""
    id: int
    filename: str
    file_size: int
    content_type: str
    owner_id: int
    is_public: bool
    download_count: int
    created_at: datetime
    
    model_config = {"from_attributes": True}


app_files = FastAPI(title="File Sharing API")


@app_files.post("/files/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    is_public: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """上传文件"""
    # 生成唯一文件名
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{timestamp}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename
    
    # 保存文件
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # 创建数据库记录
    db_file = SharedFile(
        filename=file.filename,
        filepath=str(file_path),
        file_size=len(content),
        content_type=file.content_type or "application/octet-stream",
        owner_id=current_user.id,
        is_public=is_public
    )
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    
    return db_file


@app_files.get("/files/{file_id}/download")
async def download_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_active_user),
):
    """下载文件"""
    result = await db.execute(select(SharedFile).where(SharedFile.id == file_id))
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # 检查权限
    if not file.is_public and (not current_user or file.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # 增加下载次数
    file.download_count += 1
    await db.commit()
    
    return FileResponse(filename=file.filename, path=file.filepath)


@app_files.get("/files/my", response_model=list[FileResponse])
async def get_my_files(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取我的文件"""
    result = await db.execute(
        select(SharedFile)
        .where(SharedFile.owner_id == current_user.id)
        .order_by(SharedFile.created_at.desc())
    )
    files = list(result.scalars().all())
    
    return files


# ============================================================================
# 场景6: API限流和监控
# ============================================================================


from collections import defaultdict
from time import time


class RateLimiter:
    """简单的速率限制器"""
    
    def __init__(self, rate: int = 10, per: int = 60):
        """
        Args:
            rate: 允许的请求数
            per: 时间窗口（秒）
        """
        self.rate = rate
        self.per = per
        self.requests: dict[str, list[float]] = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        """检查是否允许请求"""
        now = time()
        cutoff = now - self.per
        
        # 清理过期的请求记录
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > cutoff
        ]
        
        # 检查是否超过限制
        if len(self.requests[key]) >= self.rate:
            return False
        
        # 记录新请求
        self.requests[key].append(now)
        return True


rate_limiter = RateLimiter(rate=10, per=60)


class APIMetrics:
    """API指标收集"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.endpoint_stats: dict[str, dict] = defaultdict(
            lambda: {"count": 0, "errors": 0, "total_time": 0.0}
        )
    
    def record_request(
        self,
        endpoint: str,
        response_time: float,
        is_error: bool = False
    ):
        """记录请求"""
        self.request_count += 1
        self.total_response_time += response_time
        
        if is_error:
            self.error_count += 1
        
        stats = self.endpoint_stats[endpoint]
        stats["count"] += 1
        stats["total_time"] += response_time
        
        if is_error:
            stats["errors"] += 1
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        avg_response_time = (
            self.total_response_time / self.request_count
            if self.request_count > 0
            else 0
        )
        
        error_rate = (
            self.error_count / self.request_count
            if self.request_count > 0
            else 0
        )
        
        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate": f"{error_rate:.2%}",
            "avg_response_time": f"{avg_response_time:.3f}s",
            "endpoints": {
                endpoint: {
                    **stats,
                    "avg_time": f"{stats['total_time'] / stats['count']:.3f}s"
                    if stats['count'] > 0
                    else "0s"
                }
                for endpoint, stats in self.endpoint_stats.items()
            }
        }


api_metrics = APIMetrics()

app_monitoring = FastAPI(title="API Monitoring")


@app_monitoring.middleware("http")
async def add_monitoring(request: Request, call_next):
    """监控中间件"""
    start_time = time()
    
    # 检查速率限制
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=429,
            content={"error": "Too many requests"}
        )
    
    # 执行请求
    try:
        response = await call_next(request)
        is_error = response.status_code >= 400
    except Exception:
        is_error = True
        raise
    finally:
        # 记录指标
        response_time = time() - start_time
        api_metrics.record_request(
            endpoint=request.url.path,
            response_time=response_time,
            is_error=is_error
        )
    
    return response


@app_monitoring.get("/metrics")
async def get_metrics():
    """获取API指标"""
    return api_metrics.get_stats()


@app_monitoring.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# 主应用 - 组合所有子应用
# ============================================================================


main_app = FastAPI(
    title="Complete FastAPI Application",
    description="展示6个实战场景的完整应用",
    version="1.0.0"
)

# 挂载子应用
main_app.mount("/blog", app_blog)
main_app.mount("/ecommerce", app_ecommerce)
main_app.mount("/tasks", app_tasks)
main_app.mount("/chat", app_chat)
main_app.mount("/files", app_files)
main_app.mount("/monitoring", app_monitoring)


@main_app.get("/")
async def root():
    """根路由"""
    return {
        "message": "Welcome to Complete FastAPI Application!",
        "services": {
            "blog": "/blog",
            "ecommerce": "/ecommerce",
            "tasks": "/tasks",
            "chat": "/chat",
            "files": "/files",
            "monitoring": "/monitoring"
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "complete_app:main_app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

