# Pandas 数据分析

**强大的数据分析和处理库**

---

## 📋 概述

Pandas是Python中最流行的数据分析库，提供高性能、易用的数据结构和数据分析工具。

### 核心特性

- 📊 **DataFrame** - 强大的表格数据结构
- 🔄 **数据清洗** - 处理缺失值、重复数据
- 📈 **数据分析** - 分组、聚合、透视
- 📁 **文件I/O** - 支持多种文件格式
- ⏱️ **时间序列** - 强大的时间序列功能

---

## 🚀 快速开始

### 安装

```bash
uv add pandas
```

### Hello Pandas

```python
import pandas as pd

# 创建DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

print(df)
```

---

## 💻 核心数据结构

### 1. Series (一维)

```python
# 从列表创建
s = pd.Series([1, 2, 3, 4, 5])

# 自定义索引
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])

# 从字典创建
s = pd.Series({'a': 1, 'b': 2, 'c': 3})

# 访问元素
print(s['a'])      # 1
print(s[0])        # 1
```

### 2. DataFrame (二维)

```python
# 从字典创建
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

# 从列表创建
df = pd.DataFrame(
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
    columns=['A', 'B', 'C']
)

# 查看数据
print(df.head())       # 前5行
print(df.tail(3))      # 后3行
print(df.info())       # 信息
print(df.describe())   # 统计摘要
```

---

## 📁 数据读取

### 读取文件

```python
# CSV
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv', sep=';', encoding='utf-8')

# Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# JSON
df = pd.read_json('data.json')

# SQL
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql_query('SELECT * FROM users', conn)

# Parquet (推荐，最快)
df = pd.read_parquet('data.parquet')
```

### 保存文件

```python
# CSV
df.to_csv('output.csv', index=False)

# Excel
df.to_excel('output.xlsx', sheet_name='Data', index=False)

# JSON
df.to_json('output.json', orient='records')

# Parquet
df.to_parquet('output.parquet')
```

---

## 🔍 数据选择

### 列选择

```python
# 单列
df['A']          # Series
df.A             # Series (仅当列名是有效标识符时)

# 多列
df[['A', 'B']]   # DataFrame
```

### 行选择

```python
# iloc - 位置索引
df.iloc[0]          # 第1行
df.iloc[0:3]        # 前3行
df.iloc[[0, 2, 4]]  # 指定行

# loc - 标签索引
df.loc[0]           # 索引为0的行
df.loc[0:2]         # 索引0到2的行

# 布尔索引
df[df['age'] > 25]
df[(df['age'] > 25) & (df['city'] == 'NYC')]
```

### 条件选择

```python
# query方法
df.query('age > 25 and city == "NYC"')

# isin
df[df['city'].isin(['NYC', 'LA'])]

# between
df[df['age'].between(25, 35)]
```

---

## 🔄 数据清洗

### 处理缺失值

```python
# 检查缺失值
df.isnull()          # 返回布尔DataFrame
df.isnull().sum()    # 每列缺失值数量

# 删除缺失值
df.dropna()          # 删除任何包含NaN的行
df.dropna(axis=1)    # 删除任何包含NaN的列
df.dropna(subset=['age'])  # 删除age列为NaN的行

# 填充缺失值
df.fillna(0)         # 用0填充
df.fillna(method='ffill')  # 前向填充
df.fillna(method='bfill')  # 后向填充
df['age'].fillna(df['age'].mean())  # 用均值填充
```

### 处理重复值

```python
# 检查重复
df.duplicated()      # 返回布尔Series

# 删除重复
df.drop_duplicates()
df.drop_duplicates(subset=['name'], keep='first')
```

### 数据类型转换

```python
# 查看类型
df.dtypes

# 转换类型
df['age'] = df['age'].astype(int)
df['date'] = pd.to_datetime(df['date'])
df['category'] = df['category'].astype('category')
```

---

## 📊 数据转换

### 添加/删除列

```python
# 添加列
df['new_col'] = df['A'] + df['B']
df['age_group'] = df['age'].apply(lambda x: 'young' if x < 30 else 'old')

# 删除列
df.drop('new_col', axis=1, inplace=True)
df.drop(['col1', 'col2'], axis=1, inplace=True)
```

### 重命名

```python
# 重命名列
df.rename(columns={'old_name': 'new_name'}, inplace=True)

# 重命名索引
df.rename(index={0: 'first', 1: 'second'}, inplace=True)
```

### 应用函数

```python
# apply - 对列/行应用函数
df['age'].apply(lambda x: x * 2)
df.apply(lambda row: row['A'] + row['B'], axis=1)

# applymap - 对每个元素应用函数
df.applymap(lambda x: x * 2)

# map - 映射值
df['grade'] = df['score'].map({100: 'A', 90: 'B', 80: 'C'})
```

---

## 📈 分组和聚合

### 分组操作

```python
# 简单分组
grouped = df.groupby('city')

# 聚合函数
grouped.mean()
grouped.sum()
grouped.count()
grouped.size()

# 多列分组
df.groupby(['city', 'gender']).mean()

# 多个聚合函数
df.groupby('city').agg({
    'age': ['mean', 'min', 'max'],
    'salary': 'sum'
})

# 自定义聚合
df.groupby('city').agg(
    avg_age=('age', 'mean'),
    total_salary=('salary', 'sum'),
    count=('name', 'count')
)
```

### 透视表

```python
# 透视表
pivot = pd.pivot_table(
    df,
    values='salary',
    index='city',
    columns='gender',
    aggfunc='mean'
)

# 交叉表
crosstab = pd.crosstab(
    df['city'],
    df['gender'],
    values=df['salary'],
    aggfunc='mean'
)
```

---

## 🔗 合并数据

### concat - 连接

```python
# 垂直连接
result = pd.concat([df1, df2])

# 水平连接
result = pd.concat([df1, df2], axis=1)
```

### merge - 合并

```python
# Inner join
merged = pd.merge(df1, df2, on='key')

# Left join
merged = pd.merge(df1, df2, on='key', how='left')

# Right join
merged = pd.merge(df1, df2, on='key', how='right')

# Outer join
merged = pd.merge(df1, df2, on='key', how='outer')

# 多键合并
merged = pd.merge(df1, df2, on=['key1', 'key2'])
```

### join

```python
# 基于索引join
result = df1.join(df2)
result = df1.join(df2, how='left')
```

---

## ⏱️ 时间序列

### 日期处理

```python
# 创建日期范围
dates = pd.date_range('2025-01-01', periods=10, freq='D')

# 解析日期
df['date'] = pd.to_datetime(df['date_string'])

# 提取日期组件
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['weekday'] = df['date'].dt.day_name()

# 时间差
df['days_diff'] = (df['end_date'] - df['start_date']).dt.days
```

### 时间序列操作

```python
# 设置日期索引
df.set_index('date', inplace=True)

# 重采样
daily_data = hourly_data.resample('D').mean()
monthly_data = daily_data.resample('M').sum()

# 滚动窗口
rolling_mean = df['value'].rolling(window=7).mean()

# 移位
df['prev_value'] = df['value'].shift(1)
df['pct_change'] = df['value'].pct_change()
```

---

## ⚡ 性能优化

### 1. 使用向量化操作

```python
# ❌ 差 - 循环
for i in range(len(df)):
    df.loc[i, 'result'] = df.loc[i, 'A'] + df.loc[i, 'B']

# ✅ 好 - 向量化
df['result'] = df['A'] + df['B']
```

### 2. 选择合适的数据类型

```python
# 减少内存使用
df['category'] = df['category'].astype('category')
df['int_col'] = df['int_col'].astype('int32')  # 而不是int64
```

### 3. 使用Parquet格式

```python
# ✅ Parquet - 快且压缩
df.to_parquet('data.parquet')
df = pd.read_parquet('data.parquet')

# ❌ CSV - 慢且占空间
df.to_csv('data.csv')
df = pd.read_csv('data.csv')
```

---

## 📚 实用技巧

### 链式操作

```python
result = (df
    .query('age > 25')
    .groupby('city')
    .agg({'salary': 'mean'})
    .sort_values('salary', ascending=False)
    .head(10)
)
```

### 样式和格式化

```python
# 数值格式化
df.style.format({'price': '${:.2f}', 'percentage': '{:.1%}'})

# 高亮显示
df.style.highlight_max(axis=0)
df.style.highlight_min(axis=1)

# 条件格式化
def color_negative_red(val):
    color = 'red' if val < 0 else 'black'
    return f'color: {color}'

df.style.applymap(color_negative_red)
```

---

## 🆚 Pandas vs Polars

| 特性 | Pandas | Polars |
|------|--------|--------|
| 性能 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 内存效率 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 易用性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 生态系统 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 文档 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**建议**: 新项目优先使用Polars，现有项目可继续使用Pandas

---

## 🔗 相关资源

- [官方文档](https://pandas.pydata.org/docs/)
- [10分钟入门Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Pandas Cookbook](https://pandas.pydata.org/docs/user_guide/cookbook.html)

---

**最后更新**: 2025年10月28日

