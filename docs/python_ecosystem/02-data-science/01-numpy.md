# NumPy 数值计算基础

**Python科学计算的基础库**

---

## 📋 概述

NumPy (Numerical Python) 是Python科学计算的基础包。提供高性能的多维数组对象和用于处理这些数组的工具。

### 核心特性

- 📊 **多维数组** - 强大的N维数组对象
- ⚡ **高性能** - C语言实现，速度快
- 🔢 **数学函数** - 丰富的数学运算
- 🎯 **广播机制** - 灵活的数组运算
- 🔗 **基础库** - 其他科学库的基础

---

## 🚀 快速开始

### 安装

```bash
# 使用 uv (推荐)
uv add numpy

# 或使用 pip
pip install numpy
```

### Hello NumPy

```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
print(arr)  # [1 2 3 4 5]

# 数组运算
print(arr * 2)  # [ 2  4  6  8 10]
print(arr + 10)  # [11 12 13 14 15]
```

---

## 💻 核心功能

### 1. 创建数组

```python
import numpy as np

# 从列表创建
arr1d = np.array([1, 2, 3])
arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# 特殊数组
zeros = np.zeros((3, 3))          # 全零数组
ones = np.ones((2, 4))            # 全一数组
empty = np.empty((2, 3))          # 空数组
full = np.full((2, 2), 7)         # 填充值

# 数值范围
arange = np.arange(0, 10, 2)      # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)   # 5个均匀分布的值

# 随机数组
random = np.random.rand(3, 3)     # [0, 1)均匀分布
randn = np.random.randn(3, 3)     # 标准正态分布
randint = np.random.randint(0, 10, (3, 3))  # 随机整数

# 单位矩阵
identity = np.eye(3)
```

### 2. 数组属性

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)      # (2, 3) - 形状
print(arr.ndim)       # 2 - 维度
print(arr.size)       # 6 - 元素总数
print(arr.dtype)      # int64 - 数据类型
print(arr.itemsize)   # 8 - 每个元素字节数
print(arr.nbytes)     # 48 - 总字节数
```

### 3. 索引和切片

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 基本索引
print(arr[0, 0])      # 1
print(arr[1, 2])      # 6

# 切片
print(arr[0:2, 1:3])  # [[2 3] [5 6]]
print(arr[:, 1])      # [2 5 8] - 第2列
print(arr[1, :])      # [4 5 6] - 第2行

# 布尔索引
mask = arr > 5
print(arr[mask])      # [6 7 8 9]

# 花式索引
indices = [0, 2]
print(arr[indices])   # [[1 2 3] [7 8 9]]
```

### 4. 数组变形

```python
arr = np.arange(12)

# 改变形状
reshaped = arr.reshape(3, 4)
reshaped = arr.reshape(2, 2, 3)

# 展平
flattened = reshaped.flatten()    # 返回副本
raveled = reshaped.ravel()        # 返回视图

# 转置
transposed = reshaped.T
transposed = reshaped.transpose()

# 添加维度
expanded = arr[np.newaxis, :]     # (12,) -> (1, 12)
expanded = np.expand_dims(arr, axis=0)
```

---

## 🔢 数学运算

### 1. 基本运算

```python
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

# 算术运算
print(a + b)    # [ 6  8 10 12]
print(a - b)    # [-4 -4 -4 -4]
print(a * b)    # [ 5 12 21 32]
print(a / b)    # [0.2  0.33 0.43 0.5]
print(a ** 2)   # [ 1  4  9 16]

# 比较运算
print(a > 2)    # [False False  True  True]
print(a == 3)   # [False False  True False]
```

### 2. 统计函数

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# 基本统计
print(np.mean(arr))         # 3.5 - 均值
print(np.median(arr))       # 3.5 - 中位数
print(np.std(arr))          # 1.707 - 标准差
print(np.var(arr))          # 2.917 - 方差

# 最值
print(np.min(arr))          # 1
print(np.max(arr))          # 6
print(np.argmin(arr))       # 0 - 最小值索引
print(np.argmax(arr))       # 5 - 最大值索引

# 求和
print(np.sum(arr))          # 21
print(np.sum(arr, axis=0))  # [5 7 9] - 按列求和
print(np.sum(arr, axis=1))  # [ 6 15] - 按行求和

# 累积
print(np.cumsum(arr))       # [ 1  3  6 10 15 21]
print(np.cumprod(arr))      # [1 2 6 24 120 720]
```

### 3. 线性代数

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# 矩阵乘法
print(np.dot(a, b))         # [[19 22] [43 50]]
print(a @ b)                # 同上 (Python 3.5+)

# 转置
print(a.T)

# 行列式
print(np.linalg.det(a))     # -2.0

# 逆矩阵
print(np.linalg.inv(a))

# 特征值和特征向量
eigenvalues, eigenvectors = np.linalg.eig(a)

# 解线性方程组 Ax = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
x = np.linalg.solve(A, b)
print(x)  # [2. 3.]
```

---

## 🎯 广播机制

```python
# 标量与数组
arr = np.array([1, 2, 3])
print(arr + 10)  # [11 12 13]

# 不同形状数组
a = np.array([[1], [2], [3]])  # (3, 1)
b = np.array([10, 20, 30])     # (3,)
print(a + b)
# [[11 21 31]
#  [12 22 32]
#  [13 23 33]]

# 广播规则示例
a = np.ones((3, 4))    # (3, 4)
b = np.ones((4,))      # (4,)
c = a + b              # (3, 4) - 广播成功

# a = np.ones((3, 4))  # (3, 4)
# b = np.ones((3,))    # (3,)
# c = a + b            # 错误 - 无法广播
```

---

## 🔄 数组操作

### 1. 连接和分割

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])

# 垂直连接
vertical = np.vstack((a, b))    # (3, 2)
vertical = np.concatenate((a, b), axis=0)

# 水平连接
horizontal = np.hstack((a, a))  # (2, 4)
horizontal = np.concatenate((a, a), axis=1)

# 分割
arr = np.arange(12).reshape(3, 4)
rows = np.vsplit(arr, 3)        # 分成3行
cols = np.hsplit(arr, 2)        # 分成2列
```

### 2. 排序和搜索

```python
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# 排序
sorted_arr = np.sort(arr)       # [1 1 2 3 4 5 6 9]
arr.sort()                      # 原地排序

# 排序索引
indices = np.argsort(arr)

# 搜索
index = np.searchsorted(sorted_arr, 4)

# 唯一值
unique = np.unique(arr)

# 条件筛选
filtered = arr[arr > 3]         # [4 5 9 6]
indices = np.where(arr > 3)     # 返回索引
```

---

## ⚡ 性能优化

### 1. 向量化操作

```python
import time

# ❌ 差 - 使用循环
n = 1000000
start = time.time()
result = []
for i in range(n):
    result.append(i ** 2)
loop_time = time.time() - start

# ✅ 好 - 使用NumPy
start = time.time()
arr = np.arange(n)
result = arr ** 2
numpy_time = time.time() - start

print(f"Loop: {loop_time:.4f}s")
print(f"NumPy: {numpy_time:.4f}s")
print(f"Speedup: {loop_time/numpy_time:.1f}x")
# 输出: Speedup: 50-100x
```

### 2. 内存优化

```python
# 使用视图而非副本
arr = np.arange(1000000)
view = arr[::2]         # 视图，不复制数据
copy = arr[::2].copy()  # 副本，复制数据

# 指定数据类型
small = np.array([1, 2, 3], dtype=np.int8)   # 1字节
large = np.array([1, 2, 3], dtype=np.int64)  # 8字节
```

---

## 📚 实用技巧

### 1. 条件操作

```python
arr = np.array([1, 2, 3, 4, 5])

# np.where (三元运算)
result = np.where(arr > 3, arr, 0)  # [0 0 0 4 5]

# np.select (多条件)
conditions = [arr < 2, arr < 4]
choices = ['small', 'medium']
result = np.select(conditions, choices, default='large')
```

### 2. 数组保存和加载

```python
# 保存单个数组
arr = np.array([1, 2, 3])
np.save('array.npy', arr)

# 加载
loaded = np.load('array.npy')

# 保存多个数组
np.savez('arrays.npz', a=arr1, b=arr2)

# 加载
data = np.load('arrays.npz')
arr1 = data['a']
arr2 = data['b']

# 文本格式
np.savetxt('array.txt', arr)
loaded = np.loadtxt('array.txt')
```

---

## 🔗 相关资源

- [官方文档](https://numpy.org/doc/)
- [NumPy教程](https://numpy.org/numpy-tutorials/)
- [从Python到NumPy](https://www.labri.fr/perso/nrougier/from-python-to-numpy/)

---

**最后更新**: 2025年10月28日

