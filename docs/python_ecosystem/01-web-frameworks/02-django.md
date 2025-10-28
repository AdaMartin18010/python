# Django 全功能Web框架

**功能完整的Python Web框架**

---

## 📋 概述

Django是一个高级Python Web框架，鼓励快速开发和简洁、实用的设计。
内置管理后台、ORM、认证系统等功能，适合构建完整的Web应用。

### 核心特性

- 🏗️ **全功能框架** - 包含开发所需的一切
- 🔐 **内置Admin** - 强大的管理后台
- 🗄️ **Django ORM** - 优秀的数据库抽象层
- 🔒 **安全性** - 内置安全防护
- 📱 **可扩展** - 丰富的第三方包

---

## 🚀 快速开始

### 安装

```bash
# 使用 uv (推荐)
uv add django

# 或使用 pip
pip install django
```

### 创建项目

```bash
# 创建项目
django-admin startproject myproject
cd myproject

# 创建应用
python manage.py startapp myapp

# 运行开发服务器
python manage.py runserver
```

---

## 💻 核心功能

### 1. 模型 (Models)

```python
# myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### 2. 视图 (Views)

```python
# myapp/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

# 函数视图
def post_list(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'myapp/post_list.html', {'posts': posts})

# 类视图
class PostListView(ListView):
    model = Post
    template_name = 'myapp/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(published=True)

class PostDetailView(DetailView):
    model = Post
    template_name = 'myapp/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### 3. URL配置

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

# myapp/urls.py
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
]
```

### 4. 模板 (Templates)

```html
<!-- myapp/templates/myapp/post_list.html -->
{% extends "base.html" %}

{% block content %}
<h1>博客文章</h1>

{% for post in posts %}
<article>
    <h2><a href="{% url 'myapp:post-detail' post.pk %}">{{ post.title }}</a></h2>
    <p>作者: {{ post.author.username }} | 发布于: {{ post.created_at|date:"Y-m-d" }}</p>
    <p>{{ post.content|truncatewords:50 }}</p>
</article>
{% endfor %}

<!-- 分页 -->
{% if is_paginated %}
<nav>
    {% if page_obj.has_previous %}
    <a href="?page={{ page_obj.previous_page_number }}">上一页</a>
    {% endif %}
    
    <span>第 {{ page_obj.number }} 页 / 共 {{ page_obj.paginator.num_pages }} 页</span>
    
    {% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">下一页</a>
    {% endif %}
</nav>
{% endif %}
{% endblock %}
```

---

## 🗄️ Django ORM

### 基本查询

```python
from myapp.models import Post

# 获取所有
posts = Post.objects.all()

# 过滤
published_posts = Post.objects.filter(published=True)
recent_posts = Post.objects.filter(created_at__gte='2025-01-01')

# 排除
unpublished = Post.objects.exclude(published=True)

# 获取单个
post = Post.objects.get(pk=1)
post = get_object_or_404(Post, pk=1)

# 排序
posts = Post.objects.order_by('-created_at')

# 限制
latest_10 = Post.objects.all()[:10]
```

### 高级查询

```python
from django.db.models import Q, Count, Avg

# 复杂条件
posts = Post.objects.filter(
    Q(title__icontains='django') | Q(content__icontains='django')
)

# 聚合
post_count = Post.objects.count()
avg_comments = Post.objects.aggregate(Avg('comments__count'))

# 注解
posts_with_comment_count = Post.objects.annotate(
    comment_count=Count('comments')
).filter(comment_count__gt=5)

# 关联查询
posts = Post.objects.select_related('author').prefetch_related('comments')

# 原始SQL
posts = Post.objects.raw('SELECT * FROM myapp_post WHERE published = %s', [True])
```

---

## 🔐 认证与权限

### 用户认证

```python
# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def protected_view(request):
    return render(request, 'protected.html')

def user_logout(request):
    logout(request)
    return redirect('home')
```

### 权限控制

```python
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

@permission_required('myapp.add_post')
def create_post(request):
    pass

class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'myapp.add_post'
    model = Post
```

---

## 🏗️ 项目结构

### 标准结构

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py         # 配置
│   ├── urls.py             # 根URL配置
│   ├── asgi.py
│   └── wsgi.py
├── myapp/
│   ├── __init__.py
│   ├── models.py           # 模型
│   ├── views.py            # 视图
│   ├── urls.py             # URL配置
│   ├── admin.py            # Admin配置
│   ├── forms.py            # 表单
│   ├── serializers.py      # REST序列化器
│   ├── tests.py            # 测试
│   ├── templates/          # 模板
│   │   └── myapp/
│   ├── static/             # 静态文件
│   │   └── myapp/
│   └── migrations/         # 数据库迁移
├── static/                 # 全局静态文件
├── media/                  # 用户上传文件
├── templates/              # 全局模板
└── requirements.txt
```

---

## 📊 Django Admin

### 注册模型

```python
# myapp/admin.py
from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'created_at']
    list_filter = ['published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    list_filter = ['created_at']
```

---

## 🔌 Django REST Framework

### API视图

```python
# myapp/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'published']

# myapp/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# myapp/urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
```

---

## ⚡ 性能优化

### 1. 数据库优化

```python
# ✅ 好 - 使用select_related
posts = Post.objects.select_related('author').all()

# ❌ 差 - N+1查询
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # 每次查询

# ✅ 好 - 使用prefetch_related
posts = Post.objects.prefetch_related('comments').all()

# 索引
class Post(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
```

### 2. 缓存

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# views.py
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 缓存15分钟
def my_view(request):
    pass
```

---

## 🧪 测试

```python
# myapp/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )
    
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertFalse(self.post.published)
    
    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_post_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
```

---

## 📚 最佳实践

### 1. 使用环境变量

```python
# settings.py
import os
from pathlib import Path

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### 2. 自定义管理命令

```python
# myapp/management/commands/import_data.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '导入数据'
    
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
    
    def handle(self, *args, **options):
        file_path = options['file']
        self.stdout.write(f'导入文件: {file_path}')
        # 导入逻辑
        self.stdout.write(self.style.SUCCESS('导入成功!'))

# 运行: python manage.py import_data data.csv
```

---

## 🔗 相关资源

- [官方文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Packages](https://djangopackages.org/)

---

**最后更新**: 2025年10月28日

