# Redis Python客户端

**高性能内存数据库**

---

## 📋 概述

Redis是高性能的键值存储数据库，常用于缓存、会话存储、消息队列等场景。

### 核心特性

- ⚡ **极速** - 内存存储，微秒级响应
- 🔄 **多种数据结构** - 字符串、列表、集合、哈希等
- 📊 **持久化** - RDB和AOF持久化
- 🔐 **事务** - 原子操作
- 📡 **发布订阅** - 消息系统

---

## 🚀 快速开始

### 安装

```bash
uv add redis
# 异步支持
uv add redis[hiredis]
```

### 基本使用

```python
import redis

# 连接Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 字符串操作
r.set('key', 'value')
value = r.get('key')

# 过期时间
r.setex('temp_key', 60, 'value')  # 60秒后过期

# 删除
r.delete('key')
```

---

## 💻 数据类型

### 哈希

```python
# 设置哈希字段
r.hset('user:1', 'name', 'Alice')
r.hset('user:1', 'email', 'alice@example.com')

# 批量设置
r.hset('user:1', mapping={
    'name': 'Alice',
    'email': 'alice@example.com',
    'age': 25
})

# 获取
name = r.hget('user:1', 'name')
user = r.hgetall('user:1')
```

### 列表

```python
# 推入
r.lpush('queue', 'task1')
r.rpush('queue', 'task2')

# 弹出
task = r.lpop('queue')
task = r.rpop('queue')

# 阻塞弹出（队列）
task = r.blpop('queue', timeout=5)
```

### 集合

```python
# 添加
r.sadd('tags', 'python', 'redis', 'async')

# 成员检查
is_member = r.sismember('tags', 'python')

# 获取所有成员
members = r.smembers('tags')

# 集合运算
r.sinter('set1', 'set2')  # 交集
r.sunion('set1', 'set2')  # 并集
```

---

## 🔄 异步Redis

```python
import redis.asyncio as redis

async def main():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    await r.set('key', 'value')
    value = await r.get('key')
    
    await r.close()

# 连接池
pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)
```

---

## 📚 实用场景

### 缓存

```python
import json

def get_user(user_id):
    # 先查缓存
    cached = r.get(f'user:{user_id}')
    if cached:
        return json.loads(cached)
    
    # 查数据库
    user = db.get_user(user_id)
    
    # 写入缓存
    r.setex(f'user:{user_id}', 3600, json.dumps(user))
    return user
```

### 分布式锁

```python
def acquire_lock(lock_name, timeout=10):
    identifier = str(uuid.uuid4())
    end = time.time() + timeout
    
    while time.time() < end:
        if r.set(lock_name, identifier, nx=True, ex=timeout):
            return identifier
        time.sleep(0.001)
    return False

def release_lock(lock_name, identifier):
    pipe = r.pipeline(True)
    while True:
        try:
            pipe.watch(lock_name)
            if pipe.get(lock_name) == identifier:
                pipe.multi()
                pipe.delete(lock_name)
                pipe.execute()
                return True
            pipe.unwatch()
            break
        except redis.WatchError:
            pass
    return False
```

### 限流器

```python
def is_rate_limited(user_id, limit=100, window=60):
    key = f'rate_limit:{user_id}'
    pipe = r.pipeline()
    now = time.time()
    
    pipe.zadd(key, {now: now})
    pipe.zremrangebyscore(key, 0, now - window)
    pipe.zcard(key)
    pipe.expire(key, window)
    
    _, _, count, _ = pipe.execute()
    return count > limit
```

---

## 🔗 相关资源

- [redis-py文档](https://redis-py.readthedocs.io/)
- [Redis命令参考](https://redis.io/commands/)

---

**最后更新**: 2025年10月28日

