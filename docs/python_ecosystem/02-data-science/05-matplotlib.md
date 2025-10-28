# Matplotlib 数据可视化

**Python最经典的绘图库**

---

## 📋 概述

Matplotlib是Python中最流行的绘图库，提供类似MATLAB的绘图接口。

### 核心特性

- 📊 **丰富图表** - 折线、散点、柱状等
- 🎨 **高度定制** - 完全控制样式
- 📈 **出版质量** - 适合学术论文
- 🔧 **灵活** - 面向对象和pyplot接口

---

## 🚀 快速开始

### 安装

```bash
uv add matplotlib
```

### 基本绘图

```python
import matplotlib.pyplot as plt
import numpy as np

# 数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘图
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
```

---

## 💻 常用图表

### 折线图

```python
plt.plot(x, y, label='sin(x)', color='blue', linewidth=2)
plt.plot(x, np.cos(x), label='cos(x)', color='red', linestyle='--')
plt.legend()
plt.show()
```

### 散点图

```python
x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = 1000 * np.random.rand(50)

plt.scatter(x, y, c=colors, s=sizes, alpha=0.5)
plt.colorbar()
plt.show()
```

### 柱状图

```python
categories = ['A', 'B', 'C', 'D']
values = [23, 45, 56, 78]

plt.bar(categories, values, color='skyblue')
plt.title('Bar Chart')
plt.show()
```

### 直方图

```python
data = np.random.randn(1000)
plt.hist(data, bins=30, edgecolor='black')
plt.title('Histogram')
plt.show()
```

---

## 🎨 子图

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title('Sine')

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title('Cosine')

axes[1, 0].scatter(x[:20], np.random.rand(20))
axes[1, 0].set_title('Scatter')

axes[1, 1].bar(range(5), [1, 2, 3, 2, 1])
axes[1, 1].set_title('Bar')

plt.tight_layout()
plt.show()
```

---

## 📚 最佳实践

### 面向对象API

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(x, y, label='Data')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Title')
ax.legend()
ax.grid(True, alpha=0.3)

plt.show()
```

### 保存图片

```python
plt.plot(x, y)
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
plt.savefig('figure.pdf')  # 矢量格式
```

---

## 🔗 相关资源

- [官方文档](https://matplotlib.org/)
- [图表画廊](https://matplotlib.org/stable/gallery/)

---

**最后更新**: 2025年10月28日

