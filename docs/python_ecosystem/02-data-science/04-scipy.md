# SciPy 科学计算

**Python科学计算工具集**

---

## 📋 概述

SciPy是基于NumPy的科学计算库，提供优化、积分、插值、统计等功能。

### 核心特性

- 🔬 **优化** - 函数优化算法
- 📊 **统计** - 统计分析
- 📈 **插值** - 数据插值
- ∫ **积分** - 数值积分
- 🔢 **线性代数** - 高级线性代数

---

## 🚀 快速开始

### 安装

```bash
uv add scipy
```

---

## 💻 核心功能

### 优化

```python
from scipy.optimize import minimize

def objective(x):
    return x[0]**2 + x[1]**2

result = minimize(objective, x0=[1, 1])
print(result.x)  # 最优解
```

### 插值

```python
from scipy.interpolate import interp1d
import numpy as np

x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])

f = interp1d(x, y, kind='cubic')
xnew = np.linspace(0, 4, 100)
ynew = f(xnew)
```

### 统计

```python
from scipy import stats

# 正态分布
data = stats.norm.rvs(size=1000)

# t检验
t_stat, p_value = stats.ttest_ind(group1, group2)
```

---

**最后更新**: 2025年10月28日

