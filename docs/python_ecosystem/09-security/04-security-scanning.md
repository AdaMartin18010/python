# 安全扫描与漏洞检测

**Python应用安全检测工具**

---

## 📋 概述

安全扫描是识别代码中潜在安全漏洞和依赖项风险的重要环节。

### 核心工具

- 🔍 **Bandit** - 代码安全扫描
- 🛡️ **Safety** - 依赖漏洞检查
- 🔒 **pip-audit** - 依赖审计
- 📊 **Snyk** - 全面安全分析

---

## 🔍 Bandit 代码扫描

### 安装和使用

```bash
uv add --dev bandit

# 扫描单个文件
bandit myfile.py

# 扫描整个项目
bandit -r myproject/

# 生成报告
bandit -r myproject/ -f json -o report.json
bandit -r myproject/ -f html -o report.html
```

### 常见漏洞检测

```python
# ❌ 危险：使用exec
user_input = request.get('code')
exec(user_input)  # B102: exec被检测

# ❌ 危险：SQL注入
query = f"SELECT * FROM users WHERE id = {user_id}"  # B608
cursor.execute(query)

# ✅ 安全：参数化查询
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ❌ 危险：硬编码密码
password = "MySecretPassword123"  # B105

# ✅ 安全：使用环境变量
import os
password = os.getenv('DATABASE_PASSWORD')

# ❌ 危险：弱加密
import md5  # B303: MD5不安全
hash = md5.new(data)

# ✅ 安全：强加密
import hashlib
hash = hashlib.sha256(data).hexdigest()
```

### 配置文件

```yaml
# .bandit
exclude_dirs:
  - /tests
  - /venv

skips:
  - B404  # 跳过subprocess检查
  - B603

tests:
  - B201  # Flask debug
  - B501  # SSL/TLS
```

---

## 🛡️ Safety 依赖检查

### 安装和使用

```bash
uv add --dev safety

# 检查已安装的包
safety check

# 检查requirements.txt
safety check -r requirements.txt

# 生成JSON报告
safety check --json
```

### 输出示例

```
+==============================================================================+
|                                                                              |
|                               /$$$$$$            /$$                         |
|                              /$$__  $$          | $$                         |
|           /$$$$$$$  /$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$           |
|          /$$_____/ |____  $$| $$$$   /$$__  $$|_  $$_/  | $$  | $$           |
|         |  $$$$$$   /$$$$$$$| $$_/  | $$$$$$$$  | $$    | $$  | $$           |
|          \____  $$ /$$__  $$| $$    | $$_____/  | $$ /$$| $$  | $$           |
|          /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$$  |  $$$$/|  $$$$$$$           |
|         |_______/  \_______/|__/     \_______/   \___/   \____  $$           |
|                                                            /$$  | $$           |
|                                                           |  $$$$$$/           |
|  by pyup.io                                                \______/            |
|                                                                              |
+==============================================================================+

 REPORT 

  Safety is using PyUp's free open-source vulnerability database.

+==============================================================================+
| PACKAGE  | AFFECTED         | INSTALLED | VULNERABILITY                    |
+==============================================================================+
| django   | <2.2.24          | 2.2.0     | CVE-2021-33203                  |
+==============================================================================+
```

---

## 🔒 pip-audit

### 使用

```bash
uv add --dev pip-audit

# 审计当前环境
pip-audit

# 审计requirements文件
pip-audit -r requirements.txt

# 修复漏洞（生成新的requirements）
pip-audit --fix --dry-run
```

---

## 📊 综合扫描脚本

```python
#!/usr/bin/env python3
"""安全扫描脚本"""

import subprocess
import sys
from pathlib import Path

def run_bandit():
    """运行Bandit代码扫描"""
    print("🔍 运行Bandit代码扫描...")
    result = subprocess.run(
        ['bandit', '-r', 'myproject/', '-f', 'json', '-o', 'bandit-report.json'],
        capture_output=True
    )
    if result.returncode != 0:
        print("❌ Bandit发现安全问题")
        return False
    print("✅ Bandit扫描通过")
    return True

def run_safety():
    """运行Safety依赖检查"""
    print("🛡️ 运行Safety依赖检查...")
    result = subprocess.run(
        ['safety', 'check', '--json'],
        capture_output=True
    )
    if result.returncode != 0:
        print("❌ Safety发现漏洞")
        return False
    print("✅ Safety检查通过")
    return True

def run_pip_audit():
    """运行pip-audit"""
    print("🔒 运行pip-audit...")
    result = subprocess.run(
        ['pip-audit'],
        capture_output=True
    )
    if result.returncode != 0:
        print("❌ pip-audit发现漏洞")
        return False
    print("✅ pip-audit检查通过")
    return True

def main():
    """主函数"""
    checks = [
        run_bandit(),
        run_safety(),
        run_pip_audit()
    ]
    
    if all(checks):
        print("\n✅ 所有安全检查通过！")
        sys.exit(0)
    else:
        print("\n❌ 存在安全问题，请修复")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## 🔐 代码审计清单

### 1. 输入验证

```python
# ❌ 危险：未验证输入
def create_user(username: str):
    User.objects.create(username=username)

# ✅ 安全：验证输入
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    username: str
    
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        if len(v) < 3:
            raise ValueError('用户名至少3个字符')
        return v
```

### 2. SQL注入防护

```python
# ❌ 危险：字符串拼接
query = f"SELECT * FROM users WHERE name = '{name}'"
cursor.execute(query)

# ✅ 安全：参数化查询
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))

# ✅ 安全：ORM
from sqlalchemy.orm import Session
user = session.query(User).filter_by(name=name).first()
```

### 3. XSS防护

```python
from markupsafe import escape

# ❌ 危险：直接输出
return f"<div>{user_input}</div>"

# ✅ 安全：转义输出
return f"<div>{escape(user_input)}</div>"
```

### 4. CSRF防护

```python
from fastapi import FastAPI, Form, HTTPException
from fastapi.security import HTTPBearer

app = FastAPI()
security = HTTPBearer()

@app.post("/action")
async def protected_action(
    data: str = Form(...),
    token: str = Depends(security)
):
    # 验证CSRF token
    if not verify_csrf_token(token):
        raise HTTPException(status_code=403)
    return {"status": "ok"}
```

---

## 🚀 CI/CD集成

### GitHub Actions

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install bandit safety pip-audit
      
      - name: Run Bandit
        run: bandit -r myproject/ -ll
      
      - name: Run Safety
        run: safety check
      
      - name: Run pip-audit
        run: pip-audit
```

### pre-commit配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: '1.7.5'
    hooks:
      - id: bandit
        args: ['-ll']
  
  - repo: local
    hooks:
      - id: safety
        name: safety
        entry: safety check
        language: system
        pass_filenames: false
```

---

## 📊 Snyk集成

```bash
# 安装Snyk CLI
npm install -g snyk

# 认证
snyk auth

# 测试项目
snyk test

# 监控项目
snyk monitor

# 修复漏洞
snyk fix
```

---

## 📚 最佳实践

### 1. 定期扫描

```bash
# 每日自动扫描
0 2 * * * /usr/bin/safety check --json > /var/log/safety.json
```

### 2. 依赖更新策略

```python
# requirements.txt 使用版本范围
django>=4.2,<5.0  # 允许小版本更新
requests~=2.31.0  # 允许补丁版本更新
```

### 3. 安全头部

```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 限制可信主机
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

---

## 🔗 相关资源

- [Bandit文档](https://bandit.readthedocs.io/)
- [Safety文档](https://pyup.io/safety/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**最后更新**: 2025年10月28日

