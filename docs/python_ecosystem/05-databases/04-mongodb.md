# MongoDB Python驱动

**NoSQL文档数据库**

---

## 📋 概述

MongoDB是流行的NoSQL文档数据库，Python提供官方和异步驱动。

### 核心特性

- 📄 **文档存储** - JSON-like文档
- 🔍 **灵活Schema** - 无需预定义结构
- 📊 **聚合框架** - 强大的数据聚合
- 🔄 **异步支持** - Motor异步驱动

---

## 🚀 PyMongo (同步)

### 安装

```bash
uv add pymongo
```

### 基本使用

```python
from pymongo import MongoClient

# 连接
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# 插入
user = {'name': 'Alice', 'email': 'alice@example.com', 'age': 25}
result = collection.insert_one(user)
print(result.inserted_id)

# 查询
user = collection.find_one({'name': 'Alice'})
print(user)

# 查询多个
users = collection.find({'age': {'$gte': 18}})
for user in users:
    print(user)

# 更新
collection.update_one(
    {'name': 'Alice'},
    {'$set': {'age': 26}}
)

# 删除
collection.delete_one({'name': 'Alice'})
```

---

## ⚡ Motor (异步)

### 安装

```bash
uv add motor
```

### 异步操作

```python
import motor.motor_asyncio
import asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
    db = client['mydb']
    collection = db['users']
    
    # 插入
    await collection.insert_one({'name': 'Bob', 'age': 30})
    
    # 查询
    user = await collection.find_one({'name': 'Bob'})
    print(user)
    
    # 查询多个
    cursor = collection.find({'age': {'$gte': 18}})
    async for user in cursor:
        print(user)

asyncio.run(main())
```

---

## 💻 高级查询

### 聚合

```python
pipeline = [
    {'$match': {'age': {'$gte': 18}}},
    {'$group': {
        '_id': '$city',
        'avg_age': {'$avg': '$age'},
        'count': {'$sum': 1}
    }},
    {'$sort': {'count': -1}}
]

results = collection.aggregate(pipeline)
for result in results:
    print(result)
```

### 索引

```python
# 创建索引
collection.create_index('email', unique=True)
collection.create_index([('name', 1), ('age', -1)])

# 查看索引
for index in collection.list_indexes():
    print(index)
```

---

## 📚 最佳实践

### FastAPI集成

```python
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

@app.on_event("startup")
async def startup_db():
    app.mongodb_client = AsyncIOMotorClient('mongodb://localhost:27017/')
    app.mongodb = app.mongodb_client['mydb']

@app.on_event("shutdown")
async def shutdown_db():
    app.mongodb_client.close()

@app.get("/users")
async def get_users():
    users = []
    async for user in app.mongodb.users.find():
        user['_id'] = str(user['_id'])
        users.append(user)
    return users
```

---

## 🔗 相关资源

- [PyMongo文档](https://pymongo.readthedocs.io/)
- [Motor文档](https://motor.readthedocs.io/)

---

**最后更新**: 2025年10月28日

