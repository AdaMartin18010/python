# 配置管理

**Python应用配置管理最佳实践**

---

## 📋 概述

良好的配置管理对于应用的灵活性和安全性至关重要。

---

## 🚀 环境变量

### python-decouple

```bash
uv add python-decouple
```

```python
from decouple import config

# .env文件
# DEBUG=True
# DATABASE_URL=postgresql://localhost/db
# SECRET_KEY=your-secret-key

DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_URL = config('DATABASE_URL')
SECRET_KEY = config('SECRET_KEY')
```

---

## ⚙️ Pydantic Settings

### 类型安全配置

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My App"
    debug: bool = False
    database_url: str
    secret_key: str
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

---

## 📁 配置文件

### YAML配置

```bash
uv add pyyaml
```

```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

database_url = config['database']['url']
```

### TOML配置

```python
import tomli

with open('config.toml', 'rb') as f:
    config = tomli.load(f)
```

---

## 🏗️ 多环境配置

```python
import os

class Config:
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "sqlite:///dev.db"

class ProductionConfig(Config):
    DATABASE_URL = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
```

---

## 📚 最佳实践

### 1. 不要提交敏感信息

```gitignore
# .gitignore
.env
*.secret
config/production.yaml
```

### 2. 提供示例配置

```env
# .env.example
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key-here
```

### 3. 验证配置

```python
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    database_url: str
    
    @validator('database_url')
    def validate_db_url(cls, v):
        if not v.startswith(('postgresql://', 'mysql://')):
            raise ValueError('Invalid database URL')
        return v
```

---

## 🔗 相关资源

- [python-decouple](https://github.com/HBNetwork/python-decouple)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

**最后更新**: 2025年10月28日

