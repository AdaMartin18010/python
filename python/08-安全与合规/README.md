# Python 安全与合规完整指南 (2025)

**最后更新：** 2025年10月24日  
**状态：** ✅ 生产就绪

---

## 📋 目录

- [技术栈概览](#技术栈概览)
- [OWASP Top 10 2025](#owasp-top-10-2025)
- [供应链安全](#供应链安全)
- [身份认证与授权](#身份认证与授权)
- [数据加密与脱敏](#数据加密与脱敏)
- [安全编码实践](#安全编码实践)
- [审计日志](#审计日志)
- [合规框架](#合规框架)
- [安全工具链](#安全工具链)

---

## 🚀 技术栈概览

### 2025年推荐安全工具栈

| 类别 | 工具 | 版本 | 用途 |
|------|------|------|------|
| **静态分析** | Bandit | 1.7.10+ | Python代码安全扫描 |
| **依赖审计** | pip-audit | 2.7+ | 依赖漏洞检测 |
| **SBOM生成** | CycloneDX | 6.7+ | 软件物料清单 |
| **密钥管理** | HashiCorp Vault | 1.18+ | 密钥存储和管理 |
| **认证** | OAuth 2.1 / OIDC | - | 身份认证标准 |
| **加密** | cryptography | 43.0+ | 现代加密库 |
| **WAF** | ModSecurity | 3.0+ | Web应用防火墙 |
| **容器安全** | Trivy | 0.57+ | 容器镜像扫描 |
| **SAST** | Semgrep | 1.95+ | 语义代码分析 |
| **DAST** | OWASP ZAP | 2.15+ | 动态安全测试 |

### 安全框架对比

| 框架 | 优势 | 适用场景 |
|------|------|---------|
| **OWASP ASVS** | 全面、分级 | Web应用安全验证 |
| **NIST CSF** | 权威、系统 | 企业级安全管理 |
| **ISO 27001** | 国际认证 | 合规和认证需求 |
| **CIS Controls** | 实用、可操作 | 安全基线建设 |

---

## 🔐 OWASP Top 10 2025

### 1. API不安全设计 (API01:2025 Broken Object Level Authorization)

**威胁：** 未正确验证用户对资源的访问权限

**防护措施：**

```python
# app/security/authorization.py
from fastapi import HTTPException, Depends
from typing import Annotated

class ResourceAccessControl:
    """资源访问控制"""
    
    @staticmethod
    async def verify_resource_ownership(
        resource_id: str,
        user_id: str,
        resource_type: str
    ) -> bool:
        """验证用户是否拥有资源"""
        # 从数据库查询资源所有权
        resource = await db.get_resource(resource_type, resource_id)
        
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        # 严格验证所有权
        if resource.owner_id != user_id:
            # ⚠️ 审计日志记录未授权访问尝试
            await audit_log.record_unauthorized_access(
                user_id=user_id,
                resource_type=resource_type,
                resource_id=resource_id,
                action="read"
            )
            raise HTTPException(status_code=403, detail="Access denied")
        
        return True


# ✅ 正确实现
@app.get("/api/documents/{document_id}")
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    # 验证所有权
    await ResourceAccessControl.verify_resource_ownership(
        resource_id=document_id,
        user_id=current_user.id,
        resource_type="document"
    )
    
    # 查询并返回文档
    document = await db.get_document(document_id)
    return document


# ❌ 不安全的实现
@app.get("/api/documents/{document_id}")
async def get_document_insecure(document_id: str):
    # 直接返回文档，没有验证所有权！
    return await db.get_document(document_id)
```

### 2. 加密失败 (Cryptographic Failures)

**威胁：** 敏感数据未加密或使用弱加密

**防护措施：**

```python
# app/security/encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import os

class DataEncryption:
    """数据加密工具类"""
    
    @staticmethod
    def generate_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
        """从密码生成加密密钥"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,  # OWASP 2025推荐
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    @staticmethod
    def encrypt_data(data: str, key: bytes) -> str:
        """加密数据"""
        f = Fernet(key)
        encrypted = f.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    @staticmethod
    def decrypt_data(encrypted_data: str, key: bytes) -> str:
        """解密数据"""
        f = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = f.decrypt(encrypted_bytes)
        return decrypted.decode()


# ✅ 使用示例：加密PII数据
class UserService:
    """用户服务（含加密）"""
    
    async def store_sensitive_data(
        self,
        user_id: str,
        ssn: str,  # 社会安全号（敏感）
        credit_card: str  # 信用卡号（敏感）
    ) -> None:
        """存储敏感数据"""
        # 获取加密密钥（从Vault或环境变量）
        encryption_key = await self.get_encryption_key()
        
        # 加密敏感字段
        encrypted_ssn = DataEncryption.encrypt_data(ssn, encryption_key)
        encrypted_cc = DataEncryption.encrypt_data(credit_card, encryption_key)
        
        # 存储到数据库
        await db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "ssn_encrypted": encrypted_ssn,
                    "credit_card_encrypted": encrypted_cc,
                    "encryption_version": "v2025.10"
                }
            }
        )
```

### 3. 注入攻击 (Injection)

**威胁：** SQL注入、NoSQL注入、命令注入

**防护措施：**

```python
# ✅ SQL注入防护
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_safe(db: AsyncSession, user_id: str) -> User:
    """安全的SQL查询（参数化）"""
    # ✅ 使用参数化查询
    query = text("SELECT * FROM users WHERE id = :user_id")
    result = await db.execute(query, {"user_id": user_id})
    return result.fetchone()


# ❌ 不安全的SQL拼接
async def get_user_unsafe(db: AsyncSession, user_id: str) -> User:
    """不安全的SQL查询"""
    # ❌ 直接拼接字符串，容易SQL注入！
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    result = await db.execute(text(query))
    return result.fetchone()


# ✅ NoSQL注入防护（MongoDB）
from pymongo import MongoClient
from bson.objectid import ObjectId

async def get_user_mongo_safe(user_id: str) -> dict:
    """安全的MongoDB查询"""
    # ✅ 验证输入格式
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid user ID format")
    
    # ✅ 使用类型安全的查询
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    return user


# ❌ NoSQL注入风险
async def get_user_mongo_unsafe(user_input: dict) -> dict:
    """不安全的MongoDB查询"""
    # ❌ 直接使用用户输入作为查询条件
    # 攻击者可以传入: {"$ne": null} 绕过验证
    user = await db.users.find_one(user_input)
    return user


# ✅ 命令注入防护
import subprocess
import shlex

def execute_command_safe(filename: str) -> str:
    """安全的命令执行"""
    # ✅ 输入验证：只允许特定字符
    if not filename.isalnum():
        raise ValueError("Invalid filename")
    
    # ✅ 使用列表传参（不通过shell）
    result = subprocess.run(
        ["cat", f"/data/{filename}"],
        capture_output=True,
        text=True,
        timeout=5,
        check=True
    )
    return result.stdout


# ❌ 命令注入风险
def execute_command_unsafe(filename: str) -> str:
    """不安全的命令执行"""
    # ❌ 直接拼接命令，容易注入！
    # 攻击者可以传入: "file.txt; rm -rf /"
    result = subprocess.run(
        f"cat /data/{filename}",
        shell=True,  # ❌ 危险！
        capture_output=True,
        text=True
    )
    return result.stdout
```

### 4. 不安全的设计 (Insecure Design)

**威胁：** 业务逻辑漏洞、缺少安全控制

**防护措施：**

```python
# app/security/rate_limiting.py
from fastapi import HTTPException, Request
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    """请求速率限制器"""
    
    def __init__(self, max_requests: int, time_window: int):
        """
        初始化速率限制器
        
        Args:
            max_requests: 时间窗口内最大请求数
            time_window: 时间窗口（秒）
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: defaultdict = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def is_allowed(self, identifier: str) -> bool:
        """检查请求是否允许"""
        async with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=self.time_window)
            
            # 清理过期记录
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


# 应用示例：登录接口防暴力破解
login_limiter = RateLimiter(max_requests=5, time_window=300)  # 5次/5分钟

@app.post("/api/auth/login")
async def login(request: Request, credentials: LoginCredentials):
    """登录接口（带速率限制）"""
    identifier = request.client.host  # 或使用用户名
    
    # ✅ 检查速率限制
    if not await login_limiter.is_allowed(identifier):
        # 审计日志
        await audit_log.record_rate_limit_exceeded(
            ip=request.client.host,
            endpoint="/api/auth/login"
        )
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please try again later.",
            headers={"Retry-After": "300"}
        )
    
    # 验证凭证
    user = await authenticate_user(credentials)
    if not user:
        # ✅ 失败也计入速率限制
        return {"error": "Invalid credentials"}
    
    # 生成令牌
    token = create_access_token(user.id)
    return {"access_token": token}
```

### 5. 安全配置错误 (Security Misconfiguration)

**威胁：** 默认配置、调试模式、不必要的功能

**防护措施：**

```python
# app/config/security.py
from pydantic_settings import BaseSettings
from typing import Literal

class SecuritySettings(BaseSettings):
    """安全配置"""
    
    # ✅ 环境配置
    environment: Literal["development", "staging", "production"] = "production"
    
    # ✅ 调试模式（生产环境必须关闭）
    debug: bool = False
    
    # ✅ CORS配置
    cors_origins: list[str] = ["https://app.example.com"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    cors_allow_headers: list[str] = ["Authorization", "Content-Type"]
    
    # ✅ 安全头配置
    hsts_max_age: int = 31536000  # 1年
    csp_policy: str = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.example.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' https://api.example.com; "
        "frame-ancestors 'none';"
    )
    
    # ✅ 会话配置
    session_timeout: int = 3600  # 1小时
    jwt_secret_key: str  # 必须从环境变量读取
    jwt_algorithm: str = "HS256"
    
    # ✅ 密码策略
    password_min_length: int = 12
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_digit: bool = True
    password_require_special: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 应用安全头
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

def configure_security(app: FastAPI, settings: SecuritySettings) -> None:
    """配置应用安全"""
    
    # ✅ CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # ✅ 受信任主机
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["app.example.com", "*.example.com"]
    )
    
    # ✅ 安全响应头
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            f"max-age={settings.hsts_max_age}; includeSubDomains; preload"
        )
        response.headers["Content-Security-Policy"] = settings.csp_policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )
        return response
    
    # ✅ 禁用不必要的端点（生产环境）
    if settings.environment == "production":
        # 移除Swagger文档
        app.openapi_url = None
        app.docs_url = None
        app.redoc_url = None
```

---

## 📦 供应链安全

### SBOM（软件物料清单）

```bash
# 1. 生成SBOM（CycloneDX格式）
uv pip install cyclonedx-bom==6.7.0

# 生成SBOM
cyclonedx-py requirements requirements.txt -o sbom.json

# 或使用poetry
cyclonedx-poetry -o sbom.xml
```

### 依赖审计

```python
# app/security/dependency_check.py
import subprocess
import json
from typing import List, Dict

class DependencyAuditor:
    """依赖安全审计"""
    
    @staticmethod
    def audit_dependencies() -> List[Dict]:
        """审计项目依赖"""
        # 使用pip-audit
        result = subprocess.run(
            ["pip-audit", "--format", "json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        
        raise Exception("Dependency audit failed")
    
    @staticmethod
    def get_vulnerability_summary() -> Dict:
        """获取漏洞摘要"""
        vulnerabilities = DependencyAuditor.audit_dependencies()
        
        summary = {
            "total": len(vulnerabilities),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "").lower()
            if severity in summary:
                summary[severity] += 1
        
        return summary
```

### GitHub Actions集成

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    # 每天UTC 00:00运行
    - cron: '0 0 * * *'

jobs:
  dependency-audit:
    name: Dependency Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Install dependencies
        run: uv sync
      
      - name: Run pip-audit
        run: |
          uv pip install pip-audit
          pip-audit --format json --output audit-report.json
        continue-on-error: true
      
      - name: Upload audit report
        uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: audit-report.json
  
  code-scan:
    name: Code Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Bandit
        run: |
          pip install bandit[toml]
          bandit -r app/ -f json -o bandit-report.json
        continue-on-error: true
      
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/python
      
      - name: Upload scan results
        uses: actions/upload-artifact@v4
        with:
          name: security-scan
          path: |
            bandit-report.json
            semgrep-results.json
  
  container-scan:
    name: Container Image Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .
      
      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
  
  sbom-generation:
    name: Generate SBOM
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate SBOM
        run: |
          pip install cyclonedx-bom
          cyclonedx-py requirements requirements.txt -o sbom.json
      
      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json
      
      - name: Attest SBOM
        uses: actions/attest-sbom@v1
        with:
          subject-path: sbom.json
          sbom-path: sbom.json
```

---

## 🔑 身份认证与授权

### OAuth 2.1 + OIDC实现

```python
# app/auth/oauth.py
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# OAuth配置
config = Config('.env')
oauth = OAuth(config)

# 注册Google OAuth
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# JWT工具
class JWTManager:
    """JWT令牌管理"""
    
    SECRET_KEY = config('JWT_SECRET_KEY')
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 30
    
    @classmethod
    def create_access_token(cls, data: dict) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt
    
    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        """创建刷新令牌"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt
    
    @classmethod
    def verify_token(cls, token: str, token_type: str = "access") -> Optional[dict]:
        """验证令牌"""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            
            # 验证令牌类型
            if payload.get("type") != token_type:
                return None
            
            return payload
        except JWTError:
            return None


# RBAC（基于角色的访问控制）
from enum import Enum
from fastapi import HTTPException, Depends, status

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

def require_permission(permission: Permission):
    """权限检查装饰器"""
    async def permission_checker(current_user: User = Depends(get_current_user)):
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
        
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        
        return current_user
    
    return permission_checker


# 使用示例
@app.delete("/api/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_permission(Permission.DELETE))
):
    """删除用户（需要DELETE权限）"""
    await db.users.delete_one({"_id": user_id})
    return {"message": "User deleted"}
```

---

## 🔒 数据加密与脱敏

### 数据脱敏

```python
# app/security/data_masking.py
import re
from typing import Any, Dict

class DataMasker:
    """数据脱敏工具"""
    
    @staticmethod
    def mask_email(email: str) -> str:
        """脱敏邮箱"""
        if '@' not in email:
            return "***"
        
        username, domain = email.split('@')
        if len(username) <= 2:
            masked_username = '*' * len(username)
        else:
            masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
        
        return f"{masked_username}@{domain}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """脱敏电话"""
        # 保留前3位和后4位
        if len(phone) <= 7:
            return '*' * len(phone)
        return phone[:3] + '*' * (len(phone) - 7) + phone[-4:]
    
    @staticmethod
    def mask_credit_card(card: str) -> str:
        """脱敏信用卡"""
        # 只显示后4位
        return '*' * (len(card) - 4) + card[-4:]
    
    @staticmethod
    def mask_ssn(ssn: str) -> str:
        """脱敏社会安全号"""
        # 格式：XXX-XX-1234
        return 'XXX-XX-' + ssn[-4:]
    
    @staticmethod
    def mask_dict(data: Dict[str, Any], fields: list[str]) -> Dict[str, Any]:
        """批量脱敏字典数据"""
        masked_data = data.copy()
        
        for field in fields:
            if field in masked_data:
                value = str(masked_data[field])
                
                # 根据字段名自动选择脱敏方法
                if 'email' in field.lower():
                    masked_data[field] = DataMasker.mask_email(value)
                elif 'phone' in field.lower():
                    masked_data[field] = DataMasker.mask_phone(value)
                elif 'card' in field.lower() or 'credit' in field.lower():
                    masked_data[field] = DataMasker.mask_credit_card(value)
                elif 'ssn' in field.lower():
                    masked_data[field] = DataMasker.mask_ssn(value)
                else:
                    masked_data[field] = '***'
        
        return masked_data


# 使用示例
user_data = {
    "id": "user_123",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "credit_card": "4532123456789012",
    "ssn": "123-45-6789"
}

# 脱敏敏感字段
masked = DataMasker.mask_dict(
    user_data,
    fields=["email", "phone", "credit_card", "ssn"]
)

print(masked)
# {
#     "id": "user_123",
#     "name": "John Doe",
#     "email": "j***e@example.com",
#     "phone": "123***7890",
#     "credit_card": "************9012",
#     "ssn": "XXX-XX-6789"
# }
```

---

## 📝 审计日志

### 完整审计日志系统

```python
# app/security/audit_log.py
from datetime import datetime
from typing import Any, Optional
import structlog
from enum import Enum

logger = structlog.get_logger()

class AuditEventType(str, Enum):
    """审计事件类型"""
    # 认证相关
    LOGIN_SUCCESS = "auth.login.success"
    LOGIN_FAILURE = "auth.login.failure"
    LOGOUT = "auth.logout"
    PASSWORD_CHANGE = "auth.password_change"
    
    # 授权相关
    ACCESS_GRANTED = "authz.access.granted"
    ACCESS_DENIED = "authz.access.denied"
    
    # 数据操作
    DATA_CREATE = "data.create"
    DATA_READ = "data.read"
    DATA_UPDATE = "data.update"
    DATA_DELETE = "data.delete"
    
    # 系统事件
    CONFIG_CHANGE = "system.config_change"
    SECURITY_ALERT = "system.security_alert"


class AuditLogger:
    """审计日志记录器"""
    
    @staticmethod
    async def log_event(
        event_type: AuditEventType,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        action: Optional[str] = None,
        result: str = "success",
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[dict] = None
    ) -> None:
        """记录审计事件"""
        
        # 构建审计记录
        audit_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type.value,
            "user_id": user_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "action": action,
            "result": result,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "details": details or {}
        }
        
        # 记录到日志系统
        logger.info("audit_event", **audit_record)
        
        # 同时存储到数据库（用于查询和合规）
        await db.audit_logs.insert_one(audit_record)
        
        # 关键事件实时告警
        if event_type in [
            AuditEventType.LOGIN_FAILURE,
            AuditEventType.ACCESS_DENIED,
            AuditEventType.SECURITY_ALERT
        ]:
            await send_security_alert(audit_record)
    
    @staticmethod
    async def log_login_attempt(
        user_id: str,
        ip_address: str,
        success: bool,
        reason: Optional[str] = None
    ) -> None:
        """记录登录尝试"""
        await AuditLogger.log_event(
            event_type=AuditEventType.LOGIN_SUCCESS if success else AuditEventType.LOGIN_FAILURE,
            user_id=user_id,
            result="success" if success else "failure",
            ip_address=ip_address,
            details={"reason": reason} if reason else None
        )
    
    @staticmethod
    async def log_data_access(
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        success: bool
    ) -> None:
        """记录数据访问"""
        event_map = {
            "create": AuditEventType.DATA_CREATE,
            "read": AuditEventType.DATA_READ,
            "update": AuditEventType.DATA_UPDATE,
            "delete": AuditEventType.DATA_DELETE
        }
        
        await AuditLogger.log_event(
            event_type=event_map.get(action, AuditEventType.DATA_READ),
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            result="success" if success else "failure"
        )


# FastAPI中间件集成
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class AuditMiddleware(BaseHTTPMiddleware):
    """审计日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 提取用户信息
        user_id = None
        if hasattr(request.state, "user"):
            user_id = request.state.user.id
        
        # 记录请求
        await AuditLogger.log_event(
            event_type=AuditEventType.ACCESS_GRANTED,
            user_id=user_id,
            action=f"{request.method} {request.url.path}",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        
        # 处理请求
        response = await call_next(request)
        
        return response
```

---

## 📊 合规框架

### GDPR合规

```python
# app/compliance/gdpr.py
from datetime import datetime, timedelta
from typing import List, Dict

class GDPRCompliance:
    """GDPR合规工具"""
    
    @staticmethod
    async def export_user_data(user_id: str) -> Dict:
        """导出用户数据（数据可携带权）"""
        # 收集所有用户数据
        user_profile = await db.users.find_one({"_id": user_id})
        user_orders = await db.orders.find({"user_id": user_id}).to_list(length=None)
        user_activities = await db.activities.find({"user_id": user_id}).to_list(length=None)
        
        return {
            "profile": user_profile,
            "orders": user_orders,
            "activities": user_activities,
            "export_date": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    async def delete_user_data(user_id: str) -> None:
        """删除用户数据（被遗忘权）"""
        # 删除所有相关数据
        await db.users.delete_one({"_id": user_id})
        await db.orders.update_many(
            {"user_id": user_id},
            {"$set": {"user_id": "deleted", "user_data": None}}
        )
        await db.activities.delete_many({"user_id": user_id})
        
        # 审计日志
        await AuditLogger.log_event(
            event_type=AuditEventType.DATA_DELETE,
            user_id=user_id,
            action="gdpr_delete_all"
        )
    
    @staticmethod
    async def get_consent_status(user_id: str) -> Dict:
        """获取用户同意状态"""
        consent = await db.consents.find_one({"user_id": user_id})
        return consent or {}
    
    @staticmethod
    async def update_consent(user_id: str, consent_type: str, granted: bool) -> None:
        """更新用户同意"""
        await db.consents.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    f"consents.{consent_type}": {
                        "granted": granted,
                        "timestamp": datetime.utcnow()
                    }
                }
            },
            upsert=True
        )
```

---

## 🛡️ 安全工具链

### pyproject.toml配置

```toml
[tool.bandit]
exclude_dirs = ["tests", "venv"]
skips = ["B101"]  # 跳过assert检查（测试中常用）

[tool.bandit.assert_used]
skips = ["*/test_*.py"]

[tool.safety]
ignore-ids = []  # 忽略特定漏洞ID

[tool.semgrep]
config = ["p/security-audit", "p/owasp-top-ten"]
```

### pre-commit配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: '1.7.10'
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
        additional_dependencies: ['bandit[toml]']
  
  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.3
    hooks:
      - id: python-safety-dependencies-check
  
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

---

## 📚 参考资源

### 标准与框架

- **OWASP**: https://owasp.org/
- **NIST CSF**: https://www.nist.gov/cyberframework
- **CIS Controls**: https://www.cisecurity.org/controls
- **GDPR**: https://gdpr.eu/

### 工具文档

- **Bandit**: https://bandit.readthedocs.io/
- **pip-audit**: https://github.com/pypa/pip-audit
- **Trivy**: https://aquasecurity.github.io/trivy/
- **Vault**: https://www.vaultproject.io/docs

---

**更新日期：** 2025年10月24日  
**维护者：** Python Knowledge Base Team  
**下一步：** [性能优化与压测](../09-性能优化与压测/README.md) | [返回目录](../README.md)

