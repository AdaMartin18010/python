# Flask 轻量级微框架

**简单、灵活、可扩展的Python Web框架**

---

## 📋 概述

Flask是一个轻量级的Python Web框架，设计简洁，易于上手。提供核心功能，可根据需要添加扩展，适合中小型项目和API开发。

### 核心特性

- 🪶 **轻量级** - 核心简洁，易于学习
- 🔧 **灵活** - 高度可定制
- 🧩 **扩展丰富** - 大量第三方扩展
- 📝 **简单** - 代码简洁直观
- 🎯 **适用广泛** - API、网站、原型

---

## 🚀 快速开始

### 安装

```bash
# 使用 uv (推荐)
uv add flask

# 或使用 pip
pip install flask
```

### Hello Flask

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask!'

if __name__ == '__main__':
    app.run(debug=True)
```

运行: `python app.py`

---

## 💻 核心功能

### 1. 路由

```python
from flask import Flask, request

app = Flask(__name__)

# 基本路由
@app.route('/')
def index():
    return 'Home Page'

# URL参数
@app.route('/user/<username>')
def show_user(username):
    return f'User: {username}'

# 类型转换
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post ID: {post_id}'

# HTTP方法
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Logging in...'
    return 'Login Page'

# 多URL
@app.route('/about')
@app.route('/about-us')
def about():
    return 'About Page'
```

### 2. 请求处理

```python
from flask import request, jsonify

@app.route('/api/users', methods=['POST'])
def create_user():
    # JSON数据
    data = request.json
    username = data.get('username')
    email = data.get('email')
    
    # 表单数据
    # username = request.form.get('username')
    
    # 查询参数
    page = request.args.get('page', 1, type=int)
    
    # 文件上传
    # file = request.files['file']
    
    return jsonify({
        'message': 'User created',
        'username': username,
        'email': email
    }), 201
```

### 3. 模板渲染

```python
from flask import render_template

@app.route('/profile/<username>')
def profile(username):
    user_data = {
        'username': username,
        'email': f'{username}@example.com',
        'posts': ['Post 1', 'Post 2']
    }
    return render_template('profile.html', user=user_data)
```

```html
<!-- templates/profile.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ user.username }}'s Profile</title>
</head>
<body>
    <h1>{{ user.username }}</h1>
    <p>Email: {{ user.email }}</p>
    
    <h2>Posts</h2>
    <ul>
    {% for post in user.posts %}
        <li>{{ post }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

### 4. 蓝图 (Blueprints)

```python
# auth/routes.py
from flask import Blueprint, render_template, request

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 登录逻辑
        pass
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    # 登出逻辑
    return 'Logged out'

# app.py
from auth.routes import auth_bp

app.register_blueprint(auth_bp)
```

---

## 🏗️ 项目结构

### 标准结构

```
myapp/
├── app/
│   ├── __init__.py         # 应用工厂
│   ├── models.py           # 数据模型
│   ├── routes/             # 路由
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── auth.py
│   ├── templates/          # 模板
│   │   ├── base.html
│   │   ├── index.html
│   │   └── auth/
│   ├── static/             # 静态文件
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/              # 工具函数
├── tests/
│   ├── __init__.py
│   └── test_routes.py
├── config.py               # 配置
├── requirements.txt
└── run.py                  # 启动文件
```

### 应用工厂模式

```python
# app/__init__.py
from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 注册蓝图
    from app.routes import main_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    return app

# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🔌 常用扩展

### Flask-SQLAlchemy (数据库)

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

# 创建表
with app.app_context():
    db.create_all()

# 使用
@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{'username': u.username, 'email': u.email} for u in users])
```

### Flask-Login (用户认证)

```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return 'Logged in'
    return 'Invalid credentials'

@app.route('/protected')
@login_required
def protected():
    return 'Protected content'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'
```

### Flask-CORS (跨域)

```python
from flask_cors import CORS

# 允许所有域
CORS(app)

# 限制特定域
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
```

### Flask-RESTful (RESTful API)

```python
from flask_restful import Api, Resource

api = Api(app)

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {'username': user.username, 'email': user.email}
    
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.json
        user.email = data.get('email', user.email)
        db.session.commit()
        return {'message': 'User updated'}
    
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}

api.add_resource(UserResource, '/api/users/<int:user_id>')
```

---

## ⚙️ 配置管理

### config.py

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

---

## 🧪 测试

```python
# tests/test_routes.py
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app('testing')
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home Page' in response.data

def test_create_user(client):
    response = client.post('/api/users', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    data = response.json
    assert data['username'] == 'testuser'
```

---

## 📚 最佳实践

### 1. 错误处理

```python
from flask import jsonify

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
```

### 2. 请求钩子

```python
@app.before_request
def before_request():
    # 在每个请求前执行
    print('Before request')

@app.after_request
def after_request(response):
    # 在每个请求后执行
    response.headers['X-Custom-Header'] = 'Value'
    return response

@app.teardown_request
def teardown_request(exception=None):
    # 请求结束时清理
    if exception:
        db.session.rollback()
    db.session.remove()
```

### 3. 上下文处理器

```python
@app.context_processor
def utility_processor():
    def format_date(date):
        return date.strftime('%Y-%m-%d')
    return dict(format_date=format_date)

# 在模板中使用
# {{ format_date(user.created_at) }}
```

---

## ⚡ 性能优化

### 1. 缓存

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/expensive')
@cache.cached(timeout=300)  # 5分钟
def expensive_operation():
    # 耗时操作
    return 'Result'
```

### 2. 异步任务 (Celery)

```python
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379/0')

@celery.task
def send_email(email, subject, body):
    # 发送邮件
    pass

@app.route('/send')
def send():
    send_email.delay('user@example.com', 'Hello', 'Test')
    return 'Email queued'
```

---

## 🔗 相关资源

- [官方文档](https://flask.palletsprojects.com/)
- [Flask扩展](https://flask.palletsprojects.com/extensions/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

---

**最后更新**: 2025年10月28日

