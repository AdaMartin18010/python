# Python安全开发指南

## 1. 安全基础

### 1.1 安全编程原则

```python
import hashlib
import secrets
import hmac
import base64
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityPrinciples:
    """安全编程基本原则"""
    
    @staticmethod
    def defense_in_depth():
        """纵深防御原则"""
        # 多层安全防护
        security_layers = {
            'network': '网络层安全',
            'application': '应用层安全',
            'data': '数据层安全',
            'user': '用户层安全'
        }
        return security_layers
    
    @staticmethod
    def principle_of_least_privilege():
        """最小权限原则"""
        # 只授予必要的权限
        permissions = {
            'read': True,
            'write': False,
            'execute': False,
            'admin': False
        }
        return permissions
    
    @staticmethod
    def fail_secure():
        """故障安全原则"""
        # 系统故障时保持安全状态
        def secure_function():
            try:
                # 执行操作
                result = perform_operation()
                return result
            except Exception:
                # 故障时返回安全默认值
                return secure_default_value()
        
        return secure_function
    
    @staticmethod
    def input_validation():
        """输入验证原则"""
        def validate_input(data: str) -> bool:
            # 白名单验证
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            return all(char in allowed_chars for char in data)
        
        return validate_input
```

### 1.2 威胁建模

```python
class ThreatModeling:
    """威胁建模"""
    
    @staticmethod
    def identify_threats():
        """识别威胁"""
        threats = {
            'authentication': {
                'threat': '身份验证绕过',
                'impact': '高',
                'probability': '中',
                'mitigation': '强身份验证机制'
            },
            'authorization': {
                'threat': '权限提升',
                'impact': '高',
                'probability': '中',
                'mitigation': '基于角色的访问控制'
            },
            'data_exposure': {
                'threat': '数据泄露',
                'impact': '高',
                'probability': '高',
                'mitigation': '数据加密和访问控制'
            },
            'injection': {
                'threat': '代码注入',
                'impact': '高',
                'probability': '高',
                'mitigation': '输入验证和参数化查询'
            }
        }
        return threats
    
    @staticmethod
    def risk_assessment():
        """风险评估"""
        def calculate_risk(impact: str, probability: str) -> str:
            risk_matrix = {
                ('高', '高'): '极高',
                ('高', '中'): '高',
                ('高', '低'): '中',
                ('中', '高'): '高',
                ('中', '中'): '中',
                ('中', '低'): '低',
                ('低', '高'): '中',
                ('低', '中'): '低',
                ('低', '低'): '极低'
            }
            return risk_matrix.get((impact, probability), '未知')
        
        return calculate_risk
```

## 2. 身份验证与授权

### 2.1 安全身份验证

```python
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class SecureAuthentication:
    """安全身份验证"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def hash_password(self, password: str) -> str:
        """安全哈希密码"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_jwt_token(self, user_id: str, expires_in: int = 3600) -> str:
        """生成JWT令牌"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def generate_secure_token(self) -> str:
        """生成安全令牌"""
        return secrets.token_urlsafe(32)
    
    def implement_mfa(self, user_id: str) -> Dict[str, Any]:
        """实现多因素认证"""
        # 生成TOTP密钥
        totp_secret = secrets.token_hex(16)
        
        # 生成二维码数据
        totp_uri = f"otpauth://totp/App:{user_id}?secret={totp_secret}&issuer=App"
        
        return {
            'secret': totp_secret,
            'uri': totp_uri
        }

# 使用示例
auth = SecureAuthentication('your-secret-key')

# 密码哈希
hashed_password = auth.hash_password('my_secure_password')
is_valid = auth.verify_password('my_secure_password', hashed_password)

# JWT令牌
token = auth.generate_jwt_token('user123')
payload = auth.verify_jwt_token(token)
```

### 2.2 基于角色的访问控制

```python
from enum import Enum
from typing import List, Set, Dict, Any

class Permission(Enum):
    """权限枚举"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class Role(Enum):
    """角色枚举"""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class RBAC:
    """基于角色的访问控制"""
    
    def __init__(self):
        self.role_permissions = {
            Role.USER: {Permission.READ},
            Role.MODERATOR: {Permission.READ, Permission.WRITE},
            Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN}
        }
        self.user_roles = {}
    
    def assign_role(self, user_id: str, role: Role):
        """分配角色"""
        self.user_roles[user_id] = role
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """检查权限"""
        if user_id not in self.user_roles:
            return False
        
        user_role = self.user_roles[user_id]
        return permission in self.role_permissions.get(user_role, set())
    
    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """获取用户权限"""
        if user_id not in self.user_roles:
            return set()
        
        user_role = self.user_roles[user_id]
        return self.role_permissions.get(user_role, set())

# 使用示例
rbac = RBAC()

# 分配角色
rbac.assign_role('user1', Role.USER)
rbac.assign_role('user2', Role.MODERATOR)
rbac.assign_role('user3', Role.ADMIN)

# 检查权限
can_read = rbac.check_permission('user1', Permission.READ)
can_write = rbac.check_permission('user1', Permission.WRITE)
can_admin = rbac.check_permission('user3', Permission.ADMIN)
```

## 3. 数据安全

### 3.1 数据加密

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class DataEncryption:
    """数据加密"""
    
    @staticmethod
    def generate_key() -> bytes:
        """生成加密密钥"""
        return Fernet.generate_key()
    
    @staticmethod
    def encrypt_data(data: str, key: bytes) -> Dict[str, bytes]:
        """加密数据"""
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return {
            'encrypted_data': encrypted_data,
            'key': key
        }
    
    @staticmethod
    def decrypt_data(encrypted_data: bytes, key: bytes) -> str:
        """解密数据"""
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data.decode()
    
    @staticmethod
    def encrypt_file(file_path: str, key: bytes) -> str:
        """加密文件"""
        f = Fernet(key)
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = f.encrypt(file_data)
        encrypted_file_path = file_path + '.encrypted'
        
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)
        
        return encrypted_file_path
    
    @staticmethod
    def decrypt_file(encrypted_file_path: str, key: bytes) -> str:
        """解密文件"""
        f = Fernet(key)
        
        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = f.decrypt(encrypted_data)
        decrypted_file_path = encrypted_file_path.replace('.encrypted', '.decrypted')
        
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)
        
        return decrypted_file_path

# 使用示例
encryption = DataEncryption()
key = encryption.generate_key()

# 加密数据
encrypted = encryption.encrypt_data("sensitive_data", key)
decrypted = encryption.decrypt_data(encrypted['encrypted_data'], key)
```

### 3.2 敏感数据处理

```python
import re
from typing import List, Dict, Any

class SensitiveDataHandler:
    """敏感数据处理"""
    
    def __init__(self):
        self.sensitive_patterns = {
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}-\d{3}-\d{4}\b'
        }
    
    def detect_sensitive_data(self, text: str) -> Dict[str, List[str]]:
        """检测敏感数据"""
        detected = {}
        
        for data_type, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                detected[data_type] = matches
        
        return detected
    
    def mask_sensitive_data(self, text: str) -> str:
        """遮蔽敏感数据"""
        masked_text = text
        
        # 遮蔽信用卡号
        masked_text = re.sub(
            r'\b(\d{4})[- ]?(\d{4})[- ]?(\d{4})[- ]?(\d{4})\b',
            r'\1-****-****-\4',
            masked_text
        )
        
        # 遮蔽SSN
        masked_text = re.sub(
            r'\b(\d{3})-(\d{2})-(\d{4})\b',
            r'\1-**-\3',
            masked_text
        )
        
        # 遮蔽邮箱
        masked_text = re.sub(
            r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b',
            r'***@\2',
            masked_text
        )
        
        return masked_text
    
    def validate_data_format(self, data_type: str, value: str) -> bool:
        """验证数据格式"""
        if data_type not in self.sensitive_patterns:
            return False
        
        pattern = self.sensitive_patterns[data_type]
        return bool(re.match(pattern, value))

# 使用示例
handler = SensitiveDataHandler()

# 检测敏感数据
text = "My credit card is 1234-5678-9012-3456 and SSN is 123-45-6789"
detected = handler.detect_sensitive_data(text)

# 遮蔽敏感数据
masked = handler.mask_sensitive_data(text)
```

## 4. 输入验证与清理

### 4.1 输入验证

```python
import re
import html
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, validator, Field

class InputValidator:
    """输入验证器"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, bool]:
        """验证密码强度"""
        checks = {
            'length': len(password) >= 8,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'digit': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
        return checks
    
    @staticmethod
    def validate_sql_injection_safe(query: str) -> bool:
        """验证SQL注入安全"""
        dangerous_patterns = [
            r'(\b(union|select|insert|update|delete|drop|create|alter)\b)',
            r'(\b(or|and)\b\s+\d+\s*=\s*\d+)',
            r'(\b(union|select|insert|update|delete|drop|create|alter)\b.*\b(union|select|insert|update|delete|drop|create|alter)\b)'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return False
        return True
    
    @staticmethod
    def validate_xss_safe(text: str) -> bool:
        """验证XSS安全"""
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe.*?>',
            r'<object.*?>'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        return True

# Pydantic模型验证
class SecureUser(BaseModel):
    """安全用户模型"""
    username: str = Field(..., min_length=3, max_length=20, regex=r'^[a-zA-Z0-9_]+$')
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含小写字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含数字')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('密码必须包含特殊字符')
        return v

# 使用示例
validator = InputValidator()

# 验证邮箱
is_valid_email = validator.validate_email('user@example.com')

# 验证密码强度
password_checks = validator.validate_password_strength('MySecurePass123!')

# 验证SQL注入安全
is_sql_safe = validator.validate_sql_injection_safe('SELECT * FROM users WHERE id = 1')
```

### 4.2 数据清理

```python
import bleach
import html
from typing import Any, Dict, List

class DataSanitizer:
    """数据清理器"""
    
    def __init__(self):
        self.allowed_tags = ['p', 'br', 'strong', 'em', 'u']
        self.allowed_attributes = {'*': ['class']}
    
    def sanitize_html(self, html_content: str) -> str:
        """清理HTML内容"""
        return bleach.clean(
            html_content,
            tags=self.allowed_tags,
            attributes=self.allowed_attributes,
            strip=True
        )
    
    def escape_html(self, text: str) -> str:
        """转义HTML"""
        return html.escape(text)
    
    def sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        # 移除危险字符
        dangerous_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # 限制长度
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:255-len(ext)-1] + '.' + ext
        
        return filename
    
    def sanitize_url(self, url: str) -> str:
        """清理URL"""
        # 验证URL格式
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 移除危险字符
        dangerous_chars = ['<', '>', '"', "'"]
        for char in dangerous_chars:
            url = url.replace(char, '')
        
        return url
    
    def sanitize_json(self, data: Any) -> Any:
        """清理JSON数据"""
        if isinstance(data, dict):
            return {k: self.sanitize_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_json(item) for item in data]
        elif isinstance(data, str):
            return self.escape_html(data)
        else:
            return data

# 使用示例
sanitizer = DataSanitizer()

# 清理HTML
dirty_html = '<script>alert("xss")</script><p>Hello <strong>World</strong></p>'
clean_html = sanitizer.sanitize_html(dirty_html)

# 清理文件名
dirty_filename = 'file<>:"/\\|?*.txt'
clean_filename = sanitizer.sanitize_filename(dirty_filename)

# 清理URL
dirty_url = 'javascript:alert("xss")'
clean_url = sanitizer.sanitize_url(dirty_url)
```

## 5. 安全配置

### 5.1 环境变量安全

```python
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

class SecureConfig:
    """安全配置管理"""
    
    def __init__(self, env_file: str = '.env'):
        load_dotenv(env_file)
        self.sensitive_keys = {
            'DATABASE_PASSWORD',
            'SECRET_KEY',
            'API_KEY',
            'JWT_SECRET',
            'REDIS_PASSWORD'
        }
    
    def get_sensitive_config(self, key: str) -> Optional[str]:
        """获取敏感配置"""
        if key in self.sensitive_keys:
            value = os.getenv(key)
            if not value:
                raise ValueError(f"敏感配置 {key} 未设置")
            return value
        return None
    
    def validate_config(self) -> Dict[str, bool]:
        """验证配置完整性"""
        validation_results = {}
        
        for key in self.sensitive_keys:
            validation_results[key] = bool(os.getenv(key))
        
        return validation_results
    
    def mask_sensitive_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """遮蔽敏感配置"""
        masked_config = {}
        
        for key, value in config.items():
            if key in self.sensitive_keys:
                masked_config[key] = '***' if value else None
            else:
                masked_config[key] = value
        
        return masked_config

# 使用示例
config = SecureConfig()

# 获取敏感配置
try:
    db_password = config.get_sensitive_config('DATABASE_PASSWORD')
    secret_key = config.get_sensitive_config('SECRET_KEY')
except ValueError as e:
    print(f"配置错误: {e}")

# 验证配置
validation = config.validate_config()
```

### 5.2 安全HTTP头

```python
from typing import Dict, List

class SecurityHeaders:
    """安全HTTP头"""
    
    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """获取安全HTTP头"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }
    
    @staticmethod
    def get_cors_headers(allowed_origins: List[str]) -> Dict[str, str]:
        """获取CORS头"""
        return {
            'Access-Control-Allow-Origin': ', '.join(allowed_origins),
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        }
    
    @staticmethod
    def validate_origin(origin: str, allowed_origins: List[str]) -> bool:
        """验证来源"""
        return origin in allowed_origins

# 使用示例
headers = SecurityHeaders()

# 获取安全头
security_headers = headers.get_security_headers()

# 获取CORS头
cors_headers = headers.get_cors_headers(['https://example.com', 'https://app.example.com'])

# 验证来源
is_valid_origin = headers.validate_origin('https://example.com', ['https://example.com'])
```

## 6. 日志与监控

### 6.1 安全日志

```python
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional

class SecurityLogger:
    """安全日志记录器"""
    
    def __init__(self, log_file: str = 'security.log'):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def log_security_event(self, event_type: str, details: Dict[str, Any], 
                          user_id: Optional[str] = None, ip_address: Optional[str] = None):
        """记录安全事件"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details,
            'user_id': user_id,
            'ip_address': ip_address
        }
        
        self.logger.info(json.dumps(log_entry))
    
    def log_authentication_event(self, user_id: str, success: bool, 
                               ip_address: str, user_agent: str):
        """记录认证事件"""
        event_type = 'login_success' if success else 'login_failure'
        details = {
            'success': success,
            'user_agent': user_agent
        }
        
        self.log_security_event(event_type, details, user_id, ip_address)
    
    def log_authorization_event(self, user_id: str, resource: str, 
                              action: str, success: bool):
        """记录授权事件"""
        event_type = 'authorization_success' if success else 'authorization_failure'
        details = {
            'resource': resource,
            'action': action,
            'success': success
        }
        
        self.log_security_event(event_type, details, user_id)
    
    def log_data_access_event(self, user_id: str, data_type: str, 
                            action: str, record_count: int):
        """记录数据访问事件"""
        details = {
            'data_type': data_type,
            'action': action,
            'record_count': record_count
        }
        
        self.log_security_event('data_access', details, user_id)

# 使用示例
security_logger = SecurityLogger()

# 记录认证事件
security_logger.log_authentication_event(
    user_id='user123',
    success=True,
    ip_address='192.168.1.100',
    user_agent='Mozilla/5.0...'
)

# 记录授权事件
security_logger.log_authorization_event(
    user_id='user123',
    resource='/api/users',
    action='read',
    success=True
)
```

### 6.2 安全监控

```python
import time
from typing import Dict, List, Any
from collections import defaultdict

class SecurityMonitor:
    """安全监控器"""
    
    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.suspicious_activities = []
        self.rate_limits = {
            'login_attempts': {'max': 5, 'window': 300},  # 5分钟内最多5次
            'api_requests': {'max': 100, 'window': 60}     # 1分钟内最多100次
        }
    
    def check_rate_limit(self, key: str, limit_type: str) -> bool:
        """检查速率限制"""
        if limit_type not in self.rate_limits:
            return True
        
        limit_config = self.rate_limits[limit_type]
        current_time = time.time()
        
        # 清理过期记录
        self.failed_attempts[key] = [
            timestamp for timestamp in self.failed_attempts[key]
            if current_time - timestamp < limit_config['window']
        ]
        
        # 检查是否超过限制
        if len(self.failed_attempts[key]) >= limit_config['max']:
            return False
        
        # 记录当前尝试
        self.failed_attempts[key].append(current_time)
        return True
    
    def detect_suspicious_activity(self, user_id: str, activity: Dict[str, Any]):
        """检测可疑活动"""
        suspicious_patterns = [
            'multiple_failed_logins',
            'unusual_access_pattern',
            'data_exfiltration_attempt',
            'privilege_escalation_attempt'
        ]
        
        # 检查可疑模式
        for pattern in suspicious_patterns:
            if self._matches_pattern(activity, pattern):
                self.suspicious_activities.append({
                    'timestamp': time.time(),
                    'user_id': user_id,
                    'pattern': pattern,
                    'activity': activity
                })
                return True
        
        return False
    
    def _matches_pattern(self, activity: Dict[str, Any], pattern: str) -> bool:
        """匹配可疑模式"""
        if pattern == 'multiple_failed_logins':
            # 检查多次失败登录
            recent_failures = [
                a for a in self.suspicious_activities
                if a['pattern'] == 'login_failure' and 
                time.time() - a['timestamp'] < 300  # 5分钟内
            ]
            return len(recent_failures) >= 3
        
        return False
    
    def get_security_report(self) -> Dict[str, Any]:
        """获取安全报告"""
        current_time = time.time()
        
        # 清理过期记录
        self.suspicious_activities = [
            activity for activity in self.suspicious_activities
            if current_time - activity['timestamp'] < 86400  # 24小时内
        ]
        
        return {
            'total_suspicious_activities': len(self.suspicious_activities),
            'rate_limited_keys': len(self.failed_attempts),
            'recent_suspicious_activities': self.suspicious_activities[-10:]  # 最近10个
        }

# 使用示例
monitor = SecurityMonitor()

# 检查速率限制
can_login = monitor.check_rate_limit('user123', 'login_attempts')
can_api_request = monitor.check_rate_limit('192.168.1.100', 'api_requests')

# 检测可疑活动
suspicious = monitor.detect_suspicious_activity('user123', {
    'action': 'login_failure',
    'ip_address': '192.168.1.100'
})

# 获取安全报告
report = monitor.get_security_report()
```

## 7. 安全测试

### 7.1 安全测试框架

```python
import unittest
from typing import Dict, List, Any
import requests

class SecurityTestSuite:
    """安全测试套件"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.test_results = []
    
    def test_sql_injection(self, endpoint: str, params: Dict[str, str]):
        """测试SQL注入"""
        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "1' OR '1'='1'--"
        ]
        
        for payload in payloads:
            test_params = params.copy()
            test_params['username'] = payload
            
            try:
                response = requests.post(f"{self.base_url}{endpoint}", data=test_params)
                
                # 检查是否成功注入
                if self._detect_sql_injection_success(response):
                    self.test_results.append({
                        'test_type': 'sql_injection',
                        'payload': payload,
                        'success': True,
                        'response': response.text
                    })
            except Exception as e:
                self.test_results.append({
                    'test_type': 'sql_injection',
                    'payload': payload,
                    'success': False,
                    'error': str(e)
                })
    
    def test_xss_injection(self, endpoint: str, params: Dict[str, str]):
        """测试XSS注入"""
        payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "<svg onload=alert('xss')>",
            "'><script>alert('xss')</script>"
        ]
        
        for payload in payloads:
            test_params = params.copy()
            test_params['input'] = payload
            
            try:
                response = requests.post(f"{self.base_url}{endpoint}", data=test_params)
                
                # 检查是否成功注入
                if payload in response.text:
                    self.test_results.append({
                        'test_type': 'xss_injection',
                        'payload': payload,
                        'success': True,
                        'response': response.text
                    })
            except Exception as e:
                self.test_results.append({
                    'test_type': 'xss_injection',
                    'payload': payload,
                    'success': False,
                    'error': str(e)
                })
    
    def test_authentication_bypass(self, endpoint: str):
        """测试认证绕过"""
        # 测试未认证访问
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            
            if response.status_code == 200:
                self.test_results.append({
                    'test_type': 'authentication_bypass',
                    'endpoint': endpoint,
                    'success': True,
                    'response_code': response.status_code
                })
        except Exception as e:
            self.test_results.append({
                'test_type': 'authentication_bypass',
                'endpoint': endpoint,
                'success': False,
                'error': str(e)
            })
    
    def _detect_sql_injection_success(self, response) -> bool:
        """检测SQL注入是否成功"""
        # 检查常见的SQL错误信息
        sql_errors = [
            'sql syntax',
            'mysql error',
            'oracle error',
            'sql server error',
            'postgresql error'
        ]
        
        response_text = response.text.lower()
        return any(error in response_text for error in sql_errors)
    
    def generate_report(self) -> Dict[str, Any]:
        """生成测试报告"""
        total_tests = len(self.test_results)
        successful_attacks = len([r for r in self.test_results if r['success']])
        
        return {
            'total_tests': total_tests,
            'successful_attacks': successful_attacks,
            'security_score': max(0, 100 - (successful_attacks / total_tests * 100)) if total_tests > 0 else 100,
            'test_results': self.test_results
        }

# 使用示例
security_tester = SecurityTestSuite('http://localhost:8000')

# 测试SQL注入
security_tester.test_sql_injection('/login', {
    'username': 'admin',
    'password': 'password'
})

# 测试XSS注入
security_tester.test_xss_injection('/comment', {
    'content': 'test comment'
})

# 测试认证绕过
security_tester.test_authentication_bypass('/admin/users')

# 生成报告
report = security_tester.generate_report()
```

---

## 总结

Python安全开发指南涵盖了以下关键领域：

1. **安全基础**：安全编程原则和威胁建模
2. **身份验证与授权**：安全身份验证和基于角色的访问控制
3. **数据安全**：数据加密和敏感数据处理
4. **输入验证与清理**：输入验证和数据清理
5. **安全配置**：环境变量安全和安全HTTP头
6. **日志与监控**：安全日志和安全监控
7. **安全测试**：安全测试框架

通过这些安全实践，开发者可以：

- 保护应用程序免受常见攻击
- 确保数据安全和隐私
- 建立有效的安全监控体系
- 进行全面的安全测试

建议根据具体应用场景选择合适的 security 策略，并定期进行安全审计和更新。
