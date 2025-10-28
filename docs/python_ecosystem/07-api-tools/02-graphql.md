# GraphQL Python实现

**现代API查询语言**

---

## 📋 概述

GraphQL是Facebook开发的API查询语言，允许客户端精确指定需要的数据。

### 核心特性

- 🎯 **精确查询** - 只获取需要的字段
- 🔄 **单次请求** - 避免多次往返
- 📝 **强类型** - Schema定义
- 🔌 **订阅** - 实时数据推送

---

## 🚀 Strawberry + FastAPI

### 安装

```bash
uv add strawberry-graphql[fastapi]
```

### 基本Schema

```python
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return User(id=id, name="Alice", email="alice@example.com")
    
    @strawberry.field
    def users(self) -> list[User]:
        return [
            User(id=1, name="Alice", email="alice@example.com"),
            User(id=2, name="Bob", email="bob@example.com"),
        ]

schema = strawberry.Schema(query=Query)

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
```

---

## 💻 核心功能

### Mutations

```python
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str) -> User:
        user = User(id=generate_id(), name=name, email=email)
        save_user(user)
        return user

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

### 查询示例

```graphql
# 查询
query {
  user(id: 1) {
    name
    email
  }
}

# Mutation
mutation {
  createUser(name: "Charlie", email: "charlie@example.com") {
    id
    name
  }
}
```

---

## 🔄 订阅

```python
import asyncio

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 10) -> int:
        for i in range(target):
            yield i
            await asyncio.sleep(1)

schema = strawberry.Schema(query=Query, subscription=Subscription)
```

---

## 📚 最佳实践

### DataLoader

```python
from strawberry.dataloader import DataLoader

async def load_users(keys):
    return await fetch_users_by_ids(keys)

user_loader = DataLoader(load_fn=load_users)

@strawberry.field
async def user(self, id: int) -> User:
    return await user_loader.load(id)
```

---

**最后更新**: 2025年10月28日

