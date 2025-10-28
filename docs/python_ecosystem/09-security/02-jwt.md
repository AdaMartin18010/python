# JWT 认证

**JSON Web Token认证实现**

---

## 📋 概述

JWT是一种开放标准，用于在各方之间安全地传输信息作为JSON对象。

### 核心特性

- 🔐 **无状态** - 服务器不存储会话
- 📝 **自包含** - 包含所需信息
- 🌐 **跨域友好** - 易于跨服务使用
- ✅ **可验证** - 数字签名验证

---

## 🚀 快速开始

### 安装

```bash
uv add pyjwt[crypto]
```

### 基本使用

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"

# 创建JWT
payload = {
    'user_id': 123,
    'username': 'alice',
    'exp': datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# 验证JWT
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    print(decoded)  # {'user_id': 123, 'username': 'alice', 'exp': ...}
except jwt.ExpiredSignatureError:
    print("Token expired")
except jwt.InvalidTokenError:
    print("Invalid token")
```

---

## 💻 FastAPI集成

### 完整认证系统

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@app.post("/login")
def login(user: User):
    # 验证用户（省略实际验证逻辑）
    if user.username == "alice" and user.password == "secret":
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(hours=1)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/protected")
def protected_route(payload: dict = Depends(verify_token)):
    return {"message": "Protected content", "user": payload["sub"]}
```

---

## 🔐 刷新Token

```python
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/refresh")
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        new_access_token = create_access_token(data={"sub": payload["sub"]})
        return {"access_token": new_access_token}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## 📚 最佳实践

### 1. 使用环境变量

```python
import os

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not set")
```

### 2. Token黑名单

```python
# 使用Redis存储已撤销的token
blacklist = set()

def revoke_token(token: str):
    blacklist.add(token)

def is_token_revoked(token: str) -> bool:
    return token in blacklist
```

---

## 🔗 相关资源

- [PyJWT文档](https://pyjwt.readthedocs.io/)
- [JWT.io](https://jwt.io/)

---

**最后更新**: 2025年10月28日

