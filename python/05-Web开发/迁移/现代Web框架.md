# Python现代Web开发框架

## 目录

- [Python现代Web开发框架](#python现代web开发框架)
  - [目录](#目录)
  - [概述](#概述)
    - [Web框架生态系统](#web框架生态系统)
  - [FastAPI - 现代异步Web框架](#fastapi---现代异步web框架)
    - [FastAPI核心特性](#fastapi核心特性)
    - [FastAPI高级特性](#fastapi高级特性)
  - [Django - 全功能Web框架](#django---全功能web框架)
    - [Django核心特性](#django核心特性)
    - [Django视图和序列化器](#django视图和序列化器)
  - [相关主题](#相关主题)

---

## 概述

Python现代Web开发框架提供了构建高性能、可扩展Web应用程序的完整解决方案。
从轻量级的Flask到全功能的Django，再到现代的FastAPI，每个框架都有其独特的优势和适用场景。

### Web框架生态系统

```python
# Web框架生态系统
web_framework_ecosystem = {
    "async_frameworks": {
        "fastapi": {
            "description": "现代异步Web框架",
            "features": ["自动API文档", "类型提示", "高性能", "异步支持"],
            "use_cases": ["API服务", "微服务", "实时应用"]
        },
        "quart": {
            "description": "异步Flask",
            "features": ["Flask兼容", "异步支持", "WebSocket"],
            "use_cases": ["异步Web应用", "实时通信"]
        }
    },
    "sync_frameworks": {
        "django": {
            "description": "全功能Web框架",
            "features": ["ORM", "管理后台", "认证系统", "模板引擎"],
            "use_cases": ["企业应用", "内容管理", "全栈开发"]
        },
        "flask": {
            "description": "轻量级Web框架",
            "features": ["灵活性", "可扩展性", "简单易用"],
            "use_cases": ["原型开发", "小型应用", "API服务"]
        }
    },
    "specialized_frameworks": {
        "streamlit": {
            "description": "数据科学Web应用",
            "features": ["快速原型", "数据可视化", "交互式界面"],
            "use_cases": ["数据科学应用", "机器学习界面"]
        },
        "dash": {
            "description": "分析Web应用",
            "features": ["交互式图表", "实时更新", "Python后端"],
            "use_cases": ["数据分析", "监控面板", "商业智能"]
        }
    }
}
```

---

## FastAPI - 现代异步Web框架

### FastAPI核心特性

```python
# FastAPI 核心特性示例
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime

# 创建FastAPI应用
app = FastAPI(
    title="现代Web API",
    description="基于FastAPI的现代Web API示例",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 数据模型
class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)
    created_at: datetime = Field(default_factory=datetime.now)
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('姓名不能为空')
        return v.strip()

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)

# 安全认证
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """获取当前用户"""
    # 这里应该验证token并返回用户信息
    # 简化示例
    if credentials.credentials != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据"
        )
    return {"user_id": 1, "username": "admin"}

# 依赖注入
class Database:
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    async def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        user = User(
            id=self.next_id,
            **user_data.dict()
        )
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """获取用户"""
        return self.users.get(user_id)
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """更新用户"""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """列出用户"""
        users = list(self.users.values())
        return users[skip:skip + limit]

# 全局数据库实例
db = Database()

# API路由
@app.get("/", response_model=Dict[str, str])
async def root():
    """根路径"""
    return {"message": "欢迎使用现代Web API"}

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_user)):
    """创建用户"""
    return await db.create_user(user)

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """获取用户"""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int, 
    user: UserUpdate, 
    current_user: dict = Depends(get_current_user)
):
    """更新用户"""
    updated_user = await db.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """删除用户"""
    success = await db.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

@app.get("/users/", response_model=List[User])
async def list_users(
    skip: int = 0, 
    limit: int = 100, 
    current_user: dict = Depends(get_current_user)
):
    """列出用户"""
    return await db.list_users(skip, limit)

# 异步任务示例
@app.post("/users/{user_id}/send-email")
async def send_email_to_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """发送邮件给用户（异步任务）"""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 模拟异步邮件发送
    await asyncio.sleep(1)  # 模拟网络延迟
    
    return {"message": f"邮件已发送给 {user.name}"}

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理"""
    return {
        "error": {
            "code": exc.status_code,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    }

# 中间件
@app.middleware("http")
async def add_process_time_header(request, call_next):
    """添加处理时间头"""
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### FastAPI高级特性

```python
# FastAPI 高级特性
from fastapi import BackgroundTasks, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
import aiofiles
import os

class AdvancedFastAPI:
    """FastAPI高级特性示例"""
    
    @staticmethod
    @app.post("/upload/")
    async def upload_file(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        description: str = Form(...)
    ):
        """文件上传处理"""
        # 保存文件
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # 后台任务处理
        background_tasks.add_task(process_uploaded_file, file_path, description)
        
        return {
            "filename": file.filename,
            "size": len(content),
            "description": description,
            "message": "文件上传成功，正在后台处理"
        }
    
    @staticmethod
    async def process_uploaded_file(file_path: str, description: str):
        """后台处理上传的文件"""
        # 模拟文件处理
        await asyncio.sleep(2)
        print(f"处理文件: {file_path}, 描述: {description}")
    
    @staticmethod
    @app.get("/download/{filename}")
    async def download_file(filename: str):
        """文件下载"""
        file_path = f"uploads/{filename}"
        if os.path.exists(file_path):
            return FileResponse(
                file_path,
                media_type='application/octet-stream',
                filename=filename
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
    
    @staticmethod
    @app.get("/health")
    async def health_check():
        """健康检查"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
```

---

## Django - 全功能Web框架

### Django核心特性

```python
# Django 核心特性示例
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings
import uuid

# 用户模型
class User(AbstractUser):
    """自定义用户模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return self.email

# 产品模型
class Product(models.Model):
    """产品模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='产品名称')
    description = models.TextField(verbose_name='产品描述')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name='价格'
    )
    category = models.ForeignKey(
        'Category', 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='分类'
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='库存')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_stock(self):
        """检查是否有库存"""
        return self.stock > 0

# 分类模型
class Category(models.Model):
    """产品分类模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='children',
        verbose_name='父分类'
    )
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def full_path(self):
        """获取完整路径"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name

# 订单模型
class Order(models.Model):
    """订单模型"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('confirmed', '已确认'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name='用户'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='订单状态'
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='总金额'
    )
    shipping_address = models.TextField(verbose_name='收货地址')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"订单 {self.id} - {self.user.email}"

# 订单项模型
class OrderItem(models.Model):
    """订单项模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name='订单'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name='产品'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='数量'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='单价'
    )
    
    class Meta:
        db_table = 'order_items'
        verbose_name = '订单项'
        verbose_name_plural = '订单项'
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        """计算总价"""
        return self.quantity * self.price
```

### Django视图和序列化器

```python
# Django REST Framework 视图和序列化器
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# 序列化器
class UserSerializer(ModelSerializer):
    """用户序列化器"""
    full_name = SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'phone', 'bio', 'birth_date', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        """获取全名"""
        return f"{obj.first_name} {obj.last_name}".strip()

class ProductSerializer(ModelSerializer):
    """产品序列化器"""
    category_name = SerializerMethodField()
    is_in_stock = SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category',
            'category_name', 'stock', 'is_in_stock', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_category_name(self, obj):
        """获取分类名称"""
        return obj.category.name if obj.category else None
    
    def get_is_in_stock(self, obj):
        """检查是否有库存"""
        return obj.is_in_stock

class OrderSerializer(ModelSerializer):
    """订单序列化器"""
    user_email = SerializerMethodField()
    items_count = SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_email', 'status', 'total_amount',
            'shipping_address', 'notes', 'items_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_email(self, obj):
        """获取用户邮箱"""
        return obj.user.email
    
    def get_items_count(self, obj):
        """获取订单项数量"""
        return obj.items.count()

# 视图集
class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_verified', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'updated_at', 'username']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """验证用户"""
        user = self.get_object()
        user.is_verified = True
        user.save()
        return Response({'status': '用户已验证'})

class ProductViewSet(viewsets.ModelViewSet):
    """产品视图集"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        """添加到购物车"""
        product = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if not product.is_in_stock:
            return Response(
                {'error': '产品缺货'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 这里应该实现购物车逻辑
        return Response({'message': f'已添加 {quantity} 个 {product.name} 到购物车'})

class OrderViewSet(viewsets.ModelViewSet):
    """订单视图集"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """获取用户订单"""
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """创建订单"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消订单"""
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return Response({'status': '订单已取消'})
        else:
            return Response(
                {'error': '只能取消待处理的订单'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
```

---

## 相关主题

- [Python语言新特性](./../../01-语言与生态/迁移/01-语言新特性.md)
- [Python技术栈2025](./../../01-语言与生态/迁移/02-技术栈2025.md)
- [质量检查](./../../02-测试与质量/迁移/质量检查.md)
- [项目管理](./../../03-工程与交付/迁移/项目管理.md)
- [数据科学](./../../06-数据科学/README.md)

---

**下一主题**: [数据科学](./../../06-数据科学/README.md)
