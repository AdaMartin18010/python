# OAuth 授权

**OAuth 2.0授权实现**

---

## 📋 概述

OAuth 2.0是行业标准的授权协议，允许应用安全地访问用户资源。

### 核心特性

- 🔐 **授权** - 不是认证
- 🎯 **委托访问** - 第三方应用访问
- 🔑 **Access Token** - 访问令牌
- 🔄 **Refresh Token** - 刷新令牌

---

## 🚀 Authlib

### 安装

```bash
uv add authlib
```

### OAuth客户端

```python
from authlib.integrations.requests_client import OAuth2Session

client = OAuth2Session(
    client_id='your-client-id',
    client_secret='your-client-secret',
    scope='read write'
)

# 获取授权URL
authorization_url, state = client.create_authorization_url(
    'https://provider.com/oauth/authorize'
)

# 用户授权后，交换code获取token
token = client.fetch_token(
    'https://provider.com/oauth/token',
    authorization_response='https://yourapp.com/callback?code=...'
)

# 使用token访问API
response = client.get('https://api.provider.com/user')
```

---

## 💻 FastAPI OAuth

### GitHub OAuth示例

```python
from fastapi import FastAPI, Request
from authlib.integrations.starlette_client import OAuth

app = FastAPI()

oauth = OAuth()
oauth.register(
    name='github',
    client_id='your-github-client-id',
    client_secret='your-github-secret',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.github.authorize_redirect(request, redirect_uri)

@app.get('/auth')
async def auth(request: Request):
    token = await oauth.github.authorize_access_token(request)
    user = await oauth.github.get('user', token=token)
    return {'user': user.json()}
```

---

## 🔐 OAuth服务器

```python
from authlib.oauth2.rfc6749 import grants
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2TokenMixin,
)

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def save_authorization_code(self, code, request):
        # 保存授权码
        pass
    
    def query_authorization_code(self, code, client):
        # 查询授权码
        pass
    
    def delete_authorization_code(self, authorization_code):
        # 删除授权码
        pass
    
    def authenticate_user(self, authorization_code):
        # 认证用户
        pass
```

---

## 📚 授权流程

### 授权码模式

```python
# 1. 重定向到授权页面
GET /oauth/authorize?
    response_type=code&
    client_id=CLIENT_ID&
    redirect_uri=REDIRECT_URI&
    scope=read write

# 2. 用户授权后，重定向回应用
GET /callback?code=AUTHORIZATION_CODE

# 3. 交换授权码获取token
POST /oauth/token
    grant_type=authorization_code&
    code=AUTHORIZATION_CODE&
    redirect_uri=REDIRECT_URI&
    client_id=CLIENT_ID&
    client_secret=CLIENT_SECRET

# 4. 返回access_token
{
    "access_token": "...",
    "refresh_token": "...",
    "expires_in": 3600
}
```

---

## 🔗 相关资源

- [Authlib文档](https://docs.authlib.org/)
- [OAuth 2.0规范](https://oauth.net/2/)

---

**最后更新**: 2025年10月28日

