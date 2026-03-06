# Python 内存模型

**理解Python的内存管理机制**

---

## 📋 目录

- [Python 内存模型](#python-内存模型)
  - [📋 目录](#-目录)
  - [内存管理概述](#内存管理概述)
    - [Python内存管理架构](#python内存管理架构)
    - [对象的内存布局](#对象的内存布局)
  - [对象内存结构](#对象内存结构)
    - [不可变对象的内存](#不可变对象的内存)
    - [可变对象的内存](#可变对象的内存)
  - [引用计数](#引用计数)
    - [引用计数机制](#引用计数机制)
    - [循环引用问题](#循环引用问题)
  - [垃圾回收](#垃圾回收)
    - [分代垃圾回收](#分代垃圾回收)
    - [\_\_del\_\_方法的陷阱](#__del__方法的陷阱)
  - [内存优化](#内存优化)
    - [\_\_slots\_\_优化](#__slots__优化)
    - [内存池和对象缓存](#内存池和对象缓存)
    - [内存监控](#内存监控)
  - [📚 核心要点](#-核心要点)
    - [内存管理](#内存管理)
    - [优化技巧](#优化技巧)
    - [最佳实践](#最佳实践)

---

## 内存管理概述

### Python内存管理架构

```python
"""
Python内存管理层次
"""

# 层次结构:
"""
Layer 3: Python对象分配器
         ├── PyObject_Malloc
         ├── PyObject_Realloc
         └── PyObject_Free

Layer 2: Python内存池 (pymalloc)
         ├── 小对象分配 (<512字节)
         └── Arena/Pool/Block管理

Layer 1: C运行时malloc/free
         └── 大对象分配 (>=512字节)

Layer 0: 操作系统内存管理
         └── 虚拟内存、物理内存
"""

# 查看内存使用
import sys

x = [1, 2, 3]
print(sys.getsizeof(x))  # 对象大小(字节)

# 不同对象的内存占用
print(sys.getsizeof(42))         # 28 bytes
print(sys.getsizeof("hello"))    # 54 bytes
print(sys.getsizeof([1, 2, 3]))  # 80 bytes
print(sys.getsizeof({1: 2}))     # 232 bytes
```

### 对象的内存布局

```python
"""
CPython对象内存布局
"""

# PyObject结构 (简化)
"""
typedef struct _object {
    Py_ssize_t ob_refcnt;      # 引用计数 (8字节)
    PyTypeObject *ob_type;      # 类型指针 (8字节)
} PyObject;                     # 总计: 16字节
"""

# PyVarObject (可变大小对象)
"""
typedef struct {
    PyObject ob_base;           # 16字节
    Py_ssize_t ob_size;         # 元素数量 (8字节)
} PyVarObject;                  # 总计: 24字节
"""

# 实际例子
import sys

# int对象
i = 42
print(sys.getsizeof(i))  # 28 = 16(PyObject) + 12(int数据)

# list对象
lst = []
print(sys.getsizeof(lst))  # 56 = 24(PyVarObject) + 32(数组指针等)

# 增加元素
lst.append(1)
print(sys.getsizeof(lst))  # 88 (分配了更多空间)
```

---

## 对象内存结构

### 不可变对象的内存

```python
"""
不可变对象内存共享
"""

# 小整数缓存 (-5 到 256)
a = 100
b = 100
print(a is b)    # True (同一对象)
print(id(a) == id(b))  # True

a = 1000
b = 1000
print(a is b)    # False (不同对象)

# 字符串驻留 (intern)
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True (驻留)

# 但动态创建的字符串不驻留
s3 = "".join(["h", "e", "l", "l", "o"])
print(s1 is s3)  # False

# 手动驻留
import sys
s4 = sys.intern("hello")
print(s1 is s4)  # True

# ============================================
# None, True, False是单例
# ============================================

a = None
b = None
print(a is b)    # True (单例)

a = True
b = True
print(a is b)    # True (单例)
```

### 可变对象的内存

```python
"""
可变对象的内存行为
"""

# 列表的内存增长策略
import sys

lst = []
print(f"Empty: {sys.getsizeof(lst)} bytes")

for i in range(10):
    lst.append(i)
    print(f"Size {len(lst)}: {sys.getsizeof(lst)} bytes")

"""
输出:
Empty: 56 bytes
Size 1: 88 bytes   # 分配4个槽位
Size 2: 88 bytes
Size 3: 88 bytes
Size 4: 88 bytes
Size 5: 120 bytes  # 扩容到8个槽位
Size 6: 120 bytes
...
"""

# ============================================
# 字典的内存
# ============================================

d = {}
print(f"Empty dict: {sys.getsizeof(d)} bytes")

for i in range(10):
    d[i] = i
    print(f"Size {len(d)}: {sys.getsizeof(d)} bytes")
```

---

## 引用计数

### 引用计数机制

```python
"""
引用计数是Python主要的内存管理方式
"""
import sys

# 创建对象
x = []
print(sys.getrefcount(x))  # 2 (x + getrefcount参数)

# 增加引用
y = x
print(sys.getrefcount(x))  # 3

z = x
print(sys.getrefcount(x))  # 4

# 减少引用
del y
print(sys.getrefcount(x))  # 3

del z
print(sys.getrefcount(x))  # 2

# 当引用计数为0时,对象被立即释放

# ============================================
# 引用计数的增减
# ============================================

# 增加引用的情况:
# 1. 赋值: y = x
# 2. 作为参数传递: func(x)
# 3. 加入容器: lst.append(x)
# 4. 作为返回值: return x

# 减少引用的情况:
# 1. del语句: del x
# 2. 超出作用域
# 3. 重新赋值: x = y
# 4. 容器被删除
```

### 循环引用问题

```python
"""
引用计数无法处理循环引用
"""

# 创建循环引用
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# 循环引用
a = Node(1)
b = Node(2)
a.next = b
b.next = a  # 循环!

# 删除引用
del a
del b

# 但对象仍在内存中,因为它们互相引用
# 需要垃圾回收器处理

# ============================================
# 避免循环引用: weakref
# ============================================

import weakref

class Node:
    def __init__(self, value):
        self.value = value
        self._next = None

    @property
    def next(self):
        return self._next() if self._next else None

    @next.setter
    def next(self, node):
        self._next = weakref.ref(node) if node else None

# 使用弱引用避免循环
a = Node(1)
b = Node(2)
a.next = b
b.next = a  # 弱引用,不增加引用计数

del a  # 对象可以被回收
```

---

## 垃圾回收

### 分代垃圾回收

```python
"""
Python使用分代垃圾回收处理循环引用
"""
import gc

# 查看垃圾回收配置
print(gc.get_threshold())  # (700, 10, 10)
# 第0代: 700次分配后触发
# 第1代: 10次第0代GC后触发
# 第2代: 10次第1代GC后触发

# 查看GC统计
print(gc.get_count())  # (当前对象数, GC次数, ...)

# 手动触发GC
collected = gc.collect()
print(f"Collected {collected} objects")

# 禁用/启用GC
gc.disable()  # 禁用
gc.enable()   # 启用

# ============================================
# 查找垃圾
# ============================================

# 找到所有垃圾对象
gc.collect()
garbage = gc.garbage
print(f"Garbage objects: {len(garbage)}")

# 找到引用某对象的对象
obj = []
referrers = gc.get_referrers(obj)
print(f"Objects referring to obj: {len(referrers)}")
```

### __del__方法的陷阱

```python
"""
__del__方法的问题
"""

class Resource:
    def __init__(self, name):
        self.name = name
        print(f"Creating {name}")

    def __del__(self):
        """析构函数"""
        print(f"Destroying {name}")

# 正常情况
r = Resource("R1")
del r  # Destroying R1

# 循环引用问题
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __del__(self):
        print(f"Deleting node {self.value}")

a = Node(1)
b = Node(2)
a.next = b
b.next = a

del a
del b
# __del__不会被调用!因为循环引用

# 需要GC处理
import gc
gc.collect()  # 现在才会调用__del__

# ⚠️ 不要依赖__del__释放资源
# ✅ 使用上下文管理器
```

---

## 内存优化

### __slots__优化

```python
"""
使用__slots__减少内存占用
"""

# 普通类
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Point(1, 2)
print(p1.__dict__)  # {'x': 1, 'y': 2}

import sys
print(sys.getsizeof(p1.__dict__))  # ~232 bytes

# 使用__slots__
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

p2 = Point(1, 2)
# print(p2.__dict__)  # AttributeError! 没有__dict__

# 内存节省
"""
普通类: 56(对象) + 232(字典) = 288 bytes
slots类: 56(对象) + 16(x) + 16(y) = 88 bytes
节省: 70%内存!
"""

# 适用场景
"""
✅ 大量相同结构的实例
✅ 属性固定不变
❌ 需要动态添加属性
❌ 需要继承
"""
```

### 内存池和对象缓存

```python
"""
内存池优化
"""

# 列表预分配
lst = [None] * 1000000  # 预分配100万元素

# 比逐个append快很多
# lst = []
# for i in range(1000000):
#     lst.append(None)

# ============================================
# 对象池模式
# ============================================

class ObjectPool:
    """对象池"""

    def __init__(self, object_class, size=10):
        self._pool = [object_class() for _ in range(size)]

    def acquire(self):
        """获取对象"""
        if self._pool:
            return self._pool.pop()
        return None

    def release(self, obj):
        """归还对象"""
        self._pool.append(obj)

# 使用
class ExpensiveObject:
    def __init__(self):
        # 昂贵的初始化
        pass

pool = ObjectPool(ExpensiveObject, size=5)
obj = pool.acquire()
# 使用obj...
pool.release(obj)  # 归还
```

### 内存监控

```python
"""
内存使用监控
"""

# 1. tracemalloc (Python 3.4+)
import tracemalloc

tracemalloc.start()

# 运行代码
data = [i for i in range(1000000)]

# 获取内存快照
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 memory usage:")
for stat in top_stats[:10]:
    print(stat)

tracemalloc.stop()

# 2. memory_profiler
"""
使用memory_profiler详细分析:

@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

运行: python -m memory_profiler script.py
"""

# 3. sys.getsizeof 深度计算
import sys

def total_size(obj, seen=None):
    """递归计算对象总大小"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)

    if isinstance(obj, dict):
        size += sum(total_size(k, seen) + total_size(v, seen)
                   for k, v in obj.items())
    elif hasattr(obj, '__dict__'):
        size += total_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        size += sum(total_size(i, seen) for i in obj)

    return size
```

---

## 📚 核心要点

### 内存管理

- ✅ **引用计数**: 主要的内存管理方式
- ✅ **垃圾回收**: 处理循环引用
- ✅ **分代GC**: 优化GC性能
- ✅ **内存池**: 小对象快速分配

### 优化技巧

- ✅ ****slots****: 大量实例时节省内存
- ✅ **对象池**: 重用昂贵对象
- ✅ **生成器**: 惰性计算节省内存
- ✅ **弱引用**: 避免循环引用

### 最佳实践

- ✅ 避免循环引用
- ✅ 及时删除大对象
- ✅ 使用上下文管理器管理资源
- ✅ 监控内存使用
- ❌ 不要依赖`__del__`

---

**理解内存模型，写出高效代码！** 💾✨

**相关文档**:

- [01-data-model.md](01-data-model.md) - 数据模型
- [04-execution-model.md](04-execution-model.md) - 执行模型

**最后更新**: 2025年10月28日
