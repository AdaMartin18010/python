# 安全最佳实践

**Python应用安全开发指南**

---

## 📋 安全开发生命周期

### SSDLC阶段

```
设计 → 开发 → 测试 → 部署 → 运维
  ↓      ↓      ↓      ↓      ↓
威胁  安全编码 安全测试 安全配置 监控
建模   审查              告警
```

---

## 🔒 核心安全原则

### 1. 最小权限原则

```python
# ❌ 差 - 过度权限
database_url = "postgresql://superuser:password@localhost/db"

# ✅ 好 - 最小权限
database_url = "postgresql://app_user:password@localhost/db"
# app_user只有SELECT, INSERT, UPDATE权限

# 文件权限
import os
os.chmod('/app/config.json', 0o600)  # 只有所有者可读写
```

### 2. 深度防御

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from slowapi import Limiter

app = FastAPI()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

# 多层防御
@app.post("/api/sensitive")
@limiter.limit("10/minute")  # 1. 限流
async def sensitive_operation(
    credentials: HTTPAuthorizationCredentials = Depends(security),  # 2. 认证
    user: User = Depends(get_current_user)  # 3. 用户验证
):
    if not user.has_permission('sensitive'):  # 4. 授权检查
        raise HTTPException(status_code=403)
    
    # 5. 输入验证
    validate_input(data)
    
    # 6. 审计日志
    audit_log.info(f"User {user.id} performed sensitive operation")
    
    return perform_operation()
```

### 3. 默认安全

```python
# ✅ 默认关闭调试模式
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ✅ 默认使用HTTPS
SECURE_SSL_REDIRECT = True

# ✅ 默认启用安全头部
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
```

---

## 🛡️ 输入验证

### 使用Pydantic

```python
from pydantic import BaseModel, validator, EmailStr, constr
from typing import Optional

class UserInput(BaseModel):
    username: constr(min_length=3, max_length=20, regex=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    age: int
    website: Optional[str] = None
    
    @validator('age')
    def validate_age(cls, v):
        if not 0 <= v <= 150:
            raise ValueError('年龄必须在0-150之间')
        return v
    
    @validator('website')
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('网址必须以http://或https://开头')
        return v

# 使用
@app.post("/users")
async def create_user(user: UserInput):  # 自动验证
    return user
```

### SQL注入防护

```python
# ❌ 危险 - SQL注入
def get_user(username: str):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# ✅ 安全 - 参数化查询
def get_user(username: str):
    query = "SELECT * FROM users WHERE username = %s"
    return db.execute(query, (username,))

# ✅ 安全 - ORM
def get_user(username: str):
    return session.query(User).filter(User.username == username).first()
```

### XSS防护

```python
from markupsafe import escape
from bleach import clean

# ❌ 危险 - 直接输出
def render_comment(comment: str):
    return f"<div>{comment}</div>"

# ✅ 安全 - HTML转义
def render_comment(comment: str):
    return f"<div>{escape(comment)}</div>"

# ✅ 安全 - 清理HTML
ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'a']
ALLOWED_ATTRIBUTES = {'a': ['href']}

def sanitize_html(content: str):
    return clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
```

---

## 🔐 认证和授权

### JWT最佳实践

```python
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密码哈希
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT令牌
SECRET_KEY = os.getenv('SECRET_KEY')  # 从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        'sub': str(user_id),
        'exp': expire,
        'type': 'access'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        'sub': str(user_id),
        'exp': expire,
        'type': 'refresh'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

### RBAC权限控制

```python
from enum import Enum
from functools import wraps

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"

ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE],
    Role.USER: [Permission.READ, Permission.WRITE],
    Role.GUEST: [Permission.READ]
}

def require_permission(permission: Permission):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user: User = Depends(get_current_user), **kwargs):
            if permission not in ROLE_PERMISSIONS.get(user.role, []):
                raise HTTPException(status_code=403, detail="权限不足")
            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator

# 使用
@app.delete("/users/{user_id}")
@require_permission(Permission.DELETE)
async def delete_user(user_id: int, user: User):
    return {"status": "deleted"}
```

---

## 🔒 敏感数据保护

### 密钥管理

```python
# ❌ 危险 - 硬编码
API_KEY = "sk-1234567890abcdef"

# ✅ 安全 - 环境变量
import os
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")

# ✅ 更安全 - 密钥管理服务
import boto3

def get_secret(secret_name: str) -> str:
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

API_KEY = get_secret('my-app/api-key')
```

### 数据加密

```python
from cryptography.fernet import Fernet
import base64

class EncryptionService:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """加密数据"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(data)
        return decrypted.decode()

# 使用
key = Fernet.generate_key()  # 保存到安全位置
encryptor = EncryptionService(key)

# 加密敏感数据
encrypted_ssn = encryptor.encrypt("123-45-6789")
db.save_user(encrypted_ssn=encrypted_ssn)

# 解密
ssn = encryptor.decrypt(user.encrypted_ssn)
```

---

## 🌐 Web安全

### 安全头部

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # 防止MIME类型嗅探
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # 防止点击劫持
        response.headers["X-Frame-Options"] = "DENY"
        
        # XSS保护
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # HSTS
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # CSP
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'"
        )
        
        # 防止信息泄露
        response.headers["X-Powered-By"] = ""
        
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

### CSRF保护

```python
from fastapi import Cookie, Form, HTTPException
import secrets

# 生成CSRF令牌
def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)

# 验证CSRF令牌
@app.post("/api/action")
async def protected_action(
    csrf_token: str = Form(...),
    csrf_cookie: str = Cookie(None, alias="csrf_token")
):
    if not csrf_cookie or csrf_token != csrf_cookie:
        raise HTTPException(status_code=403, detail="CSRF验证失败")
    
    return {"status": "ok"}
```

---

## 📝 审计日志

```python
import logging
from datetime import datetime
from typing import Optional

# 配置审计日志
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/app/audit.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
audit_logger.addHandler(handler)

class AuditLog:
    @staticmethod
    def log_access(user_id: int, resource: str, action: str, 
                   ip_address: str, success: bool):
        """记录访问日志"""
        audit_logger.info(
            f"USER_ACCESS: user_id={user_id}, resource={resource}, "
            f"action={action}, ip={ip_address}, success={success}"
        )
    
    @staticmethod
    def log_authentication(username: str, success: bool, 
                          ip_address: str, reason: Optional[str] = None):
        """记录认证日志"""
        audit_logger.info(
            f"AUTH: username={username}, success={success}, "
            f"ip={ip_address}, reason={reason}"
        )
    
    @staticmethod
    def log_data_change(user_id: int, table: str, record_id: int, 
                       action: str, old_value: dict, new_value: dict):
        """记录数据变更"""
        audit_logger.info(
            f"DATA_CHANGE: user_id={user_id}, table={table}, "
            f"record_id={record_id}, action={action}, "
            f"old={old_value}, new={new_value}"
        )

# 使用
@app.post("/users")
async def create_user(user: UserInput, request: Request, 
                     current_user: User = Depends(get_current_user)):
    new_user = db.create_user(user)
    
    AuditLog.log_access(
        user_id=current_user.id,
        resource="users",
        action="create",
        ip_address=request.client.host,
        success=True
    )
    
    return new_user
```

---

## 🔍 安全测试

### 单元测试

```python
import pytest
from fastapi.testclient import TestClient

def test_sql_injection_prevention():
    """测试SQL注入防护"""
    client = TestClient(app)
    
    # 尝试SQL注入
    malicious_input = "'; DROP TABLE users; --"
    response = client.get(f"/users?name={malicious_input}")
    
    # 应该返回空结果或404，而不是500错误
    assert response.status_code in [200, 404]
    
    # 验证表仍然存在
    assert db.table_exists('users')

def test_xss_prevention():
    """测试XSS防护"""
    client = TestClient(app)
    
    malicious_script = "<script>alert('XSS')</script>"
    response = client.post("/comments", json={"text": malicious_script})
    
    # 脚本应该被转义
    assert '<script>' not in response.text
    assert '&lt;script&gt;' in response.text
```

---

## 📚 安全检查清单

### 开发阶段

- [ ] 所有输入都经过验证
- [ ] 使用参数化查询
- [ ] 密码正确哈希（bcrypt/argon2）
- [ ] 敏感数据加密存储
- [ ] 没有硬编码密钥
- [ ] 实现了适当的错误处理
- [ ] 添加了安全日志

### 部署阶段

- [ ] HTTPS强制启用
- [ ] 安全头部配置
- [ ] 最小权限原则
- [ ] 禁用调试模式
- [ ] 更新所有依赖
- [ ] 配置防火墙
- [ ] 设置限流

### 运维阶段

- [ ] 定期安全扫描
- [ ] 监控异常访问
- [ ] 及时更新补丁
- [ ] 备份和恢复测试
- [ ] 审计日志审查
- [ ] 应急响应计划

---

## 🔗 相关资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python安全最佳实践](https://python.readthedocs.io/en/latest/library/security.html)

---

**最后更新**: 2025年10月28日

