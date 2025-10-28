# Scikit-learn 机器学习

**经典机器学习库**

---

## 📋 概述

Scikit-learn是Python中最流行的机器学习库，提供简单高效的数据分析工具。

### 核心特性

- 🎯 **分类** - 识别类别
- 📊 **回归** - 预测连续值
- 🔍 **聚类** - 分组相似对象
- 📈 **降维** - 特征压缩
- 🔧 **模型选择** - 参数调优

---

## 🚀 快速开始

### 安装

```bash
uv add scikit-learn
```

### 简单示例

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 加载数据
iris = load_iris()
X, y = iris.data, iris.target

# 分割数据
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 训练模型
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# 预测
y_pred = clf.predict(X_test)

# 评估
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
```

---

## 💻 常用算法

### 分类

```python
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# 逻辑回归
clf = LogisticRegression()
clf.fit(X_train, y_train)

# 支持向量机
clf = SVC(kernel='rbf')
clf.fit(X_train, y_train)

# 决策树
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
```

### 回归

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor

# 线性回归
reg = LinearRegression()
reg.fit(X_train, y_train)

# 梯度提升
reg = GradientBoostingRegressor()
reg.fit(X_train, y_train)
```

### 聚类

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(X)
```

---

## 🔧 数据预处理

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# 归一化
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)
```

---

## 📊 模型评估

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')
```

---

## 🎯 交叉验证

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf, X, y, cv=5)
print(f"Accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")
```

---

## 📚 最佳实践

### Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', SVC())
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

---

## 🔗 相关资源

- [官方文档](https://scikit-learn.org/)
- [用户指南](https://scikit-learn.org/stable/user_guide.html)

---

**最后更新**: 2025年10月28日

