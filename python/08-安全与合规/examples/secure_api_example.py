"""
安全API示例应用
包含：认证、授权、速率限制、数据验证、审计日志、CORS配置

运行方式:
    uv add fastapi[standard] pydantic python-jose[cryptography] passlib[bcrypt] python-multipart
    uvicorn secure_api_example:app --reload
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, EmailStr, Field, validator
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
import secrets
import hashlib
from collections import defaultdict
import asyncio

# ============ 配置 ============

SECRET_KEY = secrets.token_urlsafe(32)  # 生产环境应从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ============ 数据模型 ============

class Role(str, Enum):
    """用户角色"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Permission(str, Enum):
    """权限"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


# 角色权限映射
ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
    Role.USER: [Permission.READ, Permission.WRITE],
    Role.GUEST: [Permission.READ]
}


class User(BaseModel):
    """用户模型"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = Role.USER
    disabled: bool = False


class UserInDB(User):
    """数据库用户模型"""
    hashed_password: str


class Token(BaseModel):
    """令牌"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """令牌数据"""
    username: Optional[str] = None


class UserCreate(BaseModel):
    """创建用户"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=12)
    full_name: Optional[str] = None
    
    @validator('password')
    def password_strength(cls, v):
        """密码强度验证"""
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含大写字母')
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含小写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('密码必须包含特殊字符')
        return v


class DocumentCreate(BaseModel):
    """创建文档"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str
    is_public: bool = False


class Document(DocumentCreate):
    """文档模型"""
    id: str
    owner_id: str
    created_at: datetime


# ============ 模拟数据库 ============

fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "role": Role.ADMIN,
        "hashed_password": pwd_context.hash("Admin123!@#"),
        "disabled": False,
    },
    "testuser": {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": Role.USER,
        "hashed_password": pwd_context.hash("Test123!@#"),
        "disabled": False,
    }
}

fake_documents_db = {}

# ============ 速率限制 ============

class RateLimiter:
    """简单的速率限制器"""
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def is_allowed(self, identifier: str) -> bool:
        """检查是否允许请求"""
        async with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=self.time_window)
            
            # 清理过期请求
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > cutoff
            ]
            
            # 检查是否超限
            if len(self.requests[identifier]) >= self.max_requests:
                return False
            
            # 记录本次请求
            self.requests[identifier].append(now)
            return True


# 登录速率限制：5次/5分钟
login_limiter = RateLimiter(max_requests=5, time_window=300)

# API速率限制：100次/分钟
api_limiter = RateLimiter(max_requests=100, time_window=60)

# ============ 审计日志 ============

class AuditLog:
    """审计日志"""
    
    logs: List[dict] = []
    
    @classmethod
    def log(cls, event_type: str, user_id: str, details: dict):
        """记录审计事件"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details
        }
        cls.logs.append(log_entry)
        # 生产环境应写入数据库或日志系统
        print(f"[AUDIT] {log_entry}")


# ============ 辅助函数 ============

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """密码哈希"""
    return pwd_context.hash(password)


def get_user(username: str) -> Optional[UserInDB]:
    """获取用户"""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """认证用户"""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return User(**user.dict())


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_permission(permission: Permission):
    """权限检查装饰器"""
    async def permission_checker(current_user: User = Depends(get_current_active_user)):
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
        if permission not in user_permissions:
            AuditLog.log(
                "permission_denied",
                current_user.username,
                {"required_permission": permission.value}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission.value}' required"
            )
        return current_user
    return permission_checker


# ============ 创建应用 ============

app = FastAPI(
    title="Secure API Demo",
    description="Security best practices demonstration",
    version="1.0.0",
    docs_url="/docs",  # 生产环境应禁用
    redoc_url=None
)

# ============ 安全中间件 ============

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],  # 生产环境使用白名单
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# 受信任主机
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
)

# 安全响应头
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """添加安全响应头"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# ============ 认证端点 ============

@app.post("/token", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """登录获取令牌"""
    
    # 速率限制
    client_ip = request.client.host
    if not await login_limiter.is_allowed(client_ip):
        AuditLog.log("rate_limit_exceeded", "anonymous", {"ip": client_ip})
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
            headers={"Retry-After": "300"}
        )
    
    # 认证用户
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        AuditLog.log(
            "login_failed",
            form_data.username,
            {"ip": client_ip, "reason": "invalid_credentials"}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    AuditLog.log("login_success", user.username, {"ip": client_ip})
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """创建用户"""
    # 检查用户是否存在
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 创建用户
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["role"] = Role.USER
    user_dict["disabled"] = False
    
    fake_users_db[user.username] = user_dict
    
    AuditLog.log("user_created", user.username, {"email": user.email})
    
    return User(**user_dict)


# ============ 受保护端点 ============

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user


@app.get("/documents", response_model=List[Document])
async def list_documents(
    current_user: User = Depends(require_permission(Permission.READ))
):
    """列出文档"""
    # 只返回用户自己的文档或公开文档
    user_docs = [
        doc for doc in fake_documents_db.values()
        if doc["owner_id"] == current_user.username or doc["is_public"]
    ]
    return user_docs


@app.post("/documents", response_model=Document)
async def create_document(
    document: DocumentCreate,
    current_user: User = Depends(require_permission(Permission.WRITE))
):
    """创建文档"""
    doc_id = hashlib.sha256(
        f"{current_user.username}{datetime.now()}".encode()
    ).hexdigest()[:16]
    
    doc_dict = document.dict()
    doc_dict.update({
        "id": doc_id,
        "owner_id": current_user.username,
        "created_at": datetime.now()
    })
    
    fake_documents_db[doc_id] = doc_dict
    
    AuditLog.log(
        "document_created",
        current_user.username,
        {"document_id": doc_id, "title": document.title}
    )
    
    return Document(**doc_dict)


@app.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    current_user: User = Depends(require_permission(Permission.DELETE))
):
    """删除文档"""
    if doc_id not in fake_documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc = fake_documents_db[doc_id]
    
    # 验证所有权（管理员可以删除任何文档）
    if doc["owner_id"] != current_user.username and current_user.role != Role.ADMIN:
        AuditLog.log(
            "unauthorized_delete_attempt",
            current_user.username,
            {"document_id": doc_id}
        )
        raise HTTPException(status_code=403, detail="Access denied")
    
    del fake_documents_db[doc_id]
    
    AuditLog.log(
        "document_deleted",
        current_user.username,
        {"document_id": doc_id}
    )
    
    return {"message": "Document deleted"}


@app.get("/admin/audit-logs")
async def get_audit_logs(
    current_user: User = Depends(require_permission(Permission.ADMIN))
):
    """获取审计日志（仅管理员）"""
    return {"logs": AuditLog.logs}


# ============ 公开端点 ============

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Secure API Demo",
        "endpoints": {
            "token": "/token",
            "users": "/users",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

