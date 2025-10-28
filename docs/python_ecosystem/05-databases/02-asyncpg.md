# asyncpg PostgreSQL驱动

**最快的PostgreSQL异步驱动**

---

## 📋 概述

asyncpg是PostgreSQL的异步驱动，比其他驱动快3-5倍。

### 核心特性

- ⚡ **极速** - 比psycopg2快3-5倍
- 🔄 **异步** - 完全异步支持
- 🎯 **类型安全** - 自动类型转换
- 📦 **连接池** - 内置连接池

---

## 🚀 快速开始

### 安装

```bash
uv add asyncpg
```

### 基本使用

```python
import asyncpg

async def main():
    # 连接数据库
    conn = await asyncpg.connect(
        host='localhost',
        port=5432,
        user='user',
        password='password',
        database='mydb'
    )
    
    # 查询
    rows = await conn.fetch('SELECT * FROM users')
    for row in rows:
        print(row['name'], row['email'])
    
    # 关闭连接
    await conn.close()
```

---

## 💻 核心功能

### CRUD操作

```python
# 插入
await conn.execute(
    'INSERT INTO users(name, email) VALUES($1, $2)',
    'Alice', 'alice@example.com'
)

# 查询单行
row = await conn.fetchrow('SELECT * FROM users WHERE id = $1', 1)

# 查询多行
rows = await conn.fetch('SELECT * FROM users WHERE active = $1', True)

# 更新
await conn.execute('UPDATE users SET email = $1 WHERE id = $2', 'new@email.com', 1)

# 删除
await conn.execute('DELETE FROM users WHERE id = $1', 1)
```

### 连接池

```python
async def main():
    pool = await asyncpg.create_pool(
        host='localhost',
        database='mydb',
        user='user',
        password='password',
        min_size=10,
        max_size=20
    )
    
    # 使用连接
    async with pool.acquire() as conn:
        result = await conn.fetch('SELECT * FROM users')
    
    await pool.close()
```

---

## 🔄 事务

```python
async with conn.transaction():
    await conn.execute('INSERT INTO users(name) VALUES($1)', 'Alice')
    await conn.execute('INSERT INTO orders(user_id) VALUES($1)', user_id)
    # 自动提交或回滚
```

---

## 📚 最佳实践

### FastAPI集成

```python
from fastapi import FastAPI, Depends
import asyncpg

app = FastAPI()

async def get_pool():
    return await asyncpg.create_pool(
        host='localhost',
        database='mydb'
    )

@app.on_event("startup")
async def startup():
    app.state.pool = await get_pool()

@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()

@app.get("/users")
async def get_users():
    async with app.state.pool.acquire() as conn:
        return await conn.fetch('SELECT * FROM users')
```

---

**最后更新**: 2025年10月28日

