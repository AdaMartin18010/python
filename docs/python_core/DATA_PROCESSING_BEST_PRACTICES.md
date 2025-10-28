# Python 数据处理最佳实践 2025

**现代化数据处理技术栈与实战**

---

## 📊 数据处理技术栈

```mermaid
mindmap
  root((数据处理))
    数据读取
      CSV/Excel
      JSON/XML
      数据库
      API接口
      
    数据清洗
      缺失值处理
      异常值检测
      数据去重
      类型转换
      
    数据转换
      过滤筛选
      聚合统计
      合并拼接
      重塑透视
      
    数据分析
      描述统计
      分组分析
      时间序列
      关联分析
      
    性能优化
      Pandas优化
      Polars加速
      并行处理
      内存管理
```

---

## 1️⃣ 数据读取

### 1.1 CSV/Excel处理

```python
"""
CSV和Excel数据读取
"""
import pandas as pd
import polars as pl
from pathlib import Path

# ============================================
# 1. Pandas读取CSV
# ============================================

# 基础读取
df = pd.read_csv("data.csv")

# 优化读取
df = pd.read_csv(
    "data.csv",
    dtype={  # 指定类型减少内存
        "user_id": "int32",
        "amount": "float32",
        "status": "category"
    },
    parse_dates=["created_at"],  # 解析日期
    usecols=["user_id", "amount", "status", "created_at"],  # 只读取需要的列
    chunksize=10000  # 分块读取大文件
)

# 分块处理大文件
def process_large_csv(filename: str):
    """分块处理大CSV"""
    for chunk in pd.read_csv(filename, chunksize=100000):
        # 处理每个chunk
        result = process_chunk(chunk)
        # 保存或累积结果
        yield result

# ============================================
# 2. Polars读取 (更快!)
# ============================================

# Polars读取CSV (比Pandas快5-10x)
df = pl.read_csv(
    "data.csv",
    schema={  # 指定模式
        "user_id": pl.Int32,
        "amount": pl.Float32,
        "status": pl.Categorical,
        "created_at": pl.Datetime
    }
)

# 懒加载 (只在需要时计算)
lazy_df = pl.scan_csv("data.csv")
result = (
    lazy_df
    .filter(pl.col("amount") > 100)
    .groupby("user_id")
    .agg(pl.col("amount").sum())
    .collect()  # 触发计算
)

# ============================================
# 3. Excel处理
# ============================================

# 读取Excel
df = pd.read_excel(
    "data.xlsx",
    sheet_name="Sales",  # 指定sheet
    header=0,  # 表头行
    skiprows=2,  # 跳过前2行
    usecols="A:D",  # 只读取A-D列
)

# 写入Excel (多sheet)
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="Sales", index=False)
    df2.to_excel(writer, sheet_name="Products", index=False)

# ============================================
# 性能对比
# ============================================

"""
读取1GB CSV文件:
- Pandas:  ~45s
- Polars:  ~8s  (5.6x faster!)

内存占用:
- Pandas:  ~4GB
- Polars:  ~1GB (4x less!)
"""
```

### 1.2 JSON/数据库

```python
"""
JSON和数据库数据处理
"""
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================
# 1. JSON处理
# ============================================

# 读取JSON
df = pd.read_json("data.json")

# 读取JSON Lines (每行一个JSON)
df = pd.read_json("data.jsonl", lines=True)

# 处理嵌套JSON
data = [
    {"id": 1, "user": {"name": "Alice", "age": 30}},
    {"id": 2, "user": {"name": "Bob", "age": 25}}
]

# 展平嵌套结构
df = pd.json_normalize(data)
# 结果:
#    id user.name  user.age
# 0   1     Alice        30
# 1   2       Bob        25

# ============================================
# 2. 数据库读取 (Pandas)
# ============================================

from sqlalchemy import create_engine

# 创建引擎
engine = create_engine("postgresql://user:pass@localhost/db")

# 读取整表
df = pd.read_sql_table("users", engine)

# 执行SQL查询
df = pd.read_sql_query(
    "SELECT * FROM users WHERE created_at > '2024-01-01'",
    engine
)

# 使用参数化查询
df = pd.read_sql_query(
    "SELECT * FROM users WHERE id = %(user_id)s",
    engine,
    params={"user_id": 123}
)

# ============================================
# 3. 异步数据库读取
# ============================================

async def fetch_data_async(session: AsyncSession) -> pd.DataFrame:
    """异步读取数据"""
    stmt = select(User).where(User.active == True)
    result = await session.execute(stmt)
    users = result.scalars().all()
    
    # 转换为DataFrame
    return pd.DataFrame([
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ])

# ============================================
# 4. Polars数据库连接
# ============================================

# Polars读取数据库 (通过connectorx更快)
import connectorx as cx

df = pl.read_database(
    "SELECT * FROM users",
    "postgresql://user:pass@localhost/db"
)
```

---

## 2️⃣ 数据清洗

### 2.1 缺失值处理

```python
"""
缺失值处理策略
"""

# ============================================
# 1. 检测缺失值
# ============================================

# 查看缺失值数量
print(df.isnull().sum())

# 缺失值占比
print(df.isnull().sum() / len(df))

# 可视化缺失值
import missingno as msno
msno.matrix(df)  # 缺失值矩阵图
msno.bar(df)     # 缺失值条形图

# ============================================
# 2. 删除缺失值
# ============================================

# 删除包含任何缺失值的行
df_clean = df.dropna()

# 删除特定列缺失的行
df_clean = df.dropna(subset=["email", "phone"])

# 删除缺失值过多的列 (>50%)
threshold = len(df) * 0.5
df_clean = df.dropna(axis=1, thresh=threshold)

# ============================================
# 3. 填充缺失值
# ============================================

# 用固定值填充
df["age"] = df["age"].fillna(0)

# 用均值填充
df["age"] = df["age"].fillna(df["age"].mean())

# 用中位数填充 (对异常值鲁棒)
df["age"] = df["age"].fillna(df["age"].median())

# 用众数填充 (分类变量)
df["category"] = df["category"].fillna(df["category"].mode()[0])

# 前向填充 (时间序列)
df["price"] = df["price"].fillna(method="ffill")

# 后向填充
df["price"] = df["price"].fillna(method="bfill")

# 插值填充 (数值序列)
df["temperature"] = df["temperature"].interpolate(method="linear")

# ============================================
# 4. 分组填充
# ============================================

# 按分组用均值填充
df["price"] = df.groupby("category")["price"].transform(
    lambda x: x.fillna(x.mean())
)

# ============================================
# 5. Polars缺失值处理
# ============================================

# Polars中的缺失值处理
df = (
    pl.read_csv("data.csv")
    .fill_null(strategy="forward")  # 前向填充
    .fill_null(0)  # 剩余用0填充
)

# 条件填充
df = df.with_columns([
    pl.when(pl.col("age").is_null())
    .then(pl.col("age").mean())
    .otherwise(pl.col("age"))
    .alias("age")
])
```

### 2.2 数据验证与清洗

```python
"""
数据验证和清洗
"""
from typing import Dict, List
import re

# ============================================
# 1. 数据类型验证
# ============================================

def validate_dtypes(df: pd.DataFrame, schema: Dict[str, str]) -> pd.DataFrame:
    """验证并转换数据类型"""
    for col, dtype in schema.items():
        if col not in df.columns:
            raise ValueError(f"Column {col} not found")
        
        try:
            df[col] = df[col].astype(dtype)
        except Exception as e:
            print(f"Failed to convert {col} to {dtype}: {e}")
    
    return df

# 使用
schema = {
    "user_id": "int32",
    "amount": "float32",
    "created_at": "datetime64[ns]"
}
df = validate_dtypes(df, schema)

# ============================================
# 2. 数值范围验证
# ============================================

# 检测异常值 (IQR方法)
def detect_outliers_iqr(df: pd.DataFrame, column: str) -> pd.Series:
    """使用IQR检测异常值"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    return (df[column] < lower_bound) | (df[column] > upper_bound)

# 移除异常值
outliers = detect_outliers_iqr(df, "price")
df_clean = df[~outliers]

# 截断异常值
def clip_outliers(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """截断异常值到合理范围"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df[column] = df[column].clip(lower_bound, upper_bound)
    return df

# ============================================
# 3. 字符串清洗
# ============================================

# 去除空白
df["name"] = df["name"].str.strip()

# 转换大小写
df["email"] = df["email"].str.lower()

# 替换字符
df["phone"] = df["phone"].str.replace(r"[^\d]", "", regex=True)

# 验证邮箱格式
def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

df["valid_email"] = df["email"].apply(validate_email)

# ============================================
# 4. 去重
# ============================================

# 删除完全重复的行
df_unique = df.drop_duplicates()

# 基于特定列去重
df_unique = df.drop_duplicates(subset=["user_id"])

# 保留最后一次出现
df_unique = df.drop_duplicates(subset=["user_id"], keep="last")

# 标记重复
df["is_duplicate"] = df.duplicated(subset=["user_id"])
```

---

## 3️⃣ 数据转换

### 3.1 筛选与聚合

```python
"""
数据筛选和聚合
"""

# ============================================
# 1. 条件筛选
# ============================================

# 单条件
df_filtered = df[df["age"] > 18]

# 多条件 (AND)
df_filtered = df[(df["age"] > 18) & (df["amount"] > 100)]

# 多条件 (OR)
df_filtered = df[(df["status"] == "active") | (df["status"] == "pending")]

# 使用query (更清晰)
df_filtered = df.query("age > 18 and amount > 100")

# 使用isin
df_filtered = df[df["category"].isin(["A", "B", "C"])]

# ============================================
# 2. 分组聚合
# ============================================

# 单列聚合
result = df.groupby("category")["amount"].sum()

# 多列聚合
result = df.groupby("category").agg({
    "amount": ["sum", "mean", "count"],
    "quantity": "sum"
})

# 自定义聚合
result = df.groupby("category").agg({
    "amount": lambda x: x.quantile(0.95),  # 95分位数
    "user_id": "nunique"  # 唯一值数量
})

# 命名聚合 (Pandas 1.0+)
result = df.groupby("category").agg(
    total_amount=("amount", "sum"),
    avg_amount=("amount", "mean"),
    user_count=("user_id", "nunique")
)

# ============================================
# 3. Polars分组聚合 (更快!)
# ============================================

result = (
    df
    .groupby("category")
    .agg([
        pl.col("amount").sum().alias("total_amount"),
        pl.col("amount").mean().alias("avg_amount"),
        pl.col("user_id").n_unique().alias("user_count")
    ])
)

# 多列分组
result = (
    df
    .groupby(["category", "region"])
    .agg([
        pl.col("amount").sum(),
        pl.col("quantity").sum()
    ])
)

# ============================================
# 4. 窗口函数
# ============================================

# 计算排名
df["rank"] = df.groupby("category")["amount"].rank(
    method="dense",
    ascending=False
)

# 累积和
df["cumsum"] = df.groupby("category")["amount"].cumsum()

# 滚动窗口
df["rolling_avg"] = df.groupby("user_id")["amount"].transform(
    lambda x: x.rolling(window=7, min_periods=1).mean()
)
```

### 3.2 数据合并与重塑

```python
"""
数据合并和重塑
"""

# ============================================
# 1. 合并 (Join)
# ============================================

# 内连接
result = pd.merge(df1, df2, on="user_id", how="inner")

# 左连接
result = pd.merge(df1, df2, on="user_id", how="left")

# 多键连接
result = pd.merge(
    df1, df2,
    on=["user_id", "date"],
    how="inner"
)

# 不同列名连接
result = pd.merge(
    df1, df2,
    left_on="user_id",
    right_on="id",
    how="inner"
)

# ============================================
# 2. 拼接 (Concat)
# ============================================

# 垂直拼接 (行)
result = pd.concat([df1, df2], axis=0, ignore_index=True)

# 水平拼接 (列)
result = pd.concat([df1, df2], axis=1)

# ============================================
# 3. 透视表
# ============================================

# 创建透视表
pivot = df.pivot_table(
    values="amount",
    index="date",
    columns="category",
    aggfunc="sum",
    fill_value=0
)

# 多值透视
pivot = df.pivot_table(
    values=["amount", "quantity"],
    index="date",
    columns="category",
    aggfunc={"amount": "sum", "quantity": "sum"}
)

# ============================================
# 4. 重塑
# ============================================

# 宽变长 (melt)
long_df = pd.melt(
    df,
    id_vars=["id", "date"],
    value_vars=["sales", "profit"],
    var_name="metric",
    value_name="value"
)

# 长变宽 (pivot)
wide_df = long_df.pivot(
    index="id",
    columns="metric",
    values="value"
)
```

---

## 4️⃣ 性能优化

### 4.1 Pandas优化技巧

```python
"""
Pandas性能优化
"""

# ============================================
# 1. 使用合适的数据类型
# ============================================

# ❌ 默认类型 (占用多)
df = pd.read_csv("data.csv")
print(df.memory_usage(deep=True))

# ✅ 优化类型 (节省内存)
dtype_map = {
    "user_id": "int32",      # int64 → int32
    "amount": "float32",      # float64 → float32
    "status": "category",     # object → category
}
df = pd.read_csv("data.csv", dtype=dtype_map)

# 内存节省示例:
# Before: 400MB
# After:  120MB (70% reduction!)

# ============================================
# 2. 向量化操作
# ============================================

# ❌ 循环 (慢)
for i in range(len(df)):
    df.loc[i, "total"] = df.loc[i, "price"] * df.loc[i, "quantity"]

# ✅ 向量化 (快 100x+)
df["total"] = df["price"] * df["quantity"]

# ❌ apply (慢)
df["category"] = df["value"].apply(lambda x: "high" if x > 100 else "low")

# ✅ 向量化条件 (快 10x+)
df["category"] = np.where(df["value"] > 100, "high", "low")

# ============================================
# 3. 使用eval和query
# ============================================

# 复杂表达式优化
# ❌ 普通方式
df["result"] = df["a"] + df["b"] * df["c"] - df["d"]

# ✅ eval (快 2-3x)
df.eval("result = a + b * c - d", inplace=True)

# 复杂筛选
# ❌ 普通方式
filtered = df[(df["a"] > 0) & (df["b"] < 100)]

# ✅ query (更快更清晰)
filtered = df.query("a > 0 and b < 100")

# ============================================
# 4. 避免链式索引
# ============================================

# ❌ 链式索引 (慢且警告)
df[df["age"] > 18]["name"] = "Adult"

# ✅ loc (快且正确)
df.loc[df["age"] > 18, "name"] = "Adult"

# ============================================
# 5. 使用inplace
# ============================================

# ❌ 创建副本 (慢,占内存)
df = df.drop("column", axis=1)

# ✅ inplace修改 (快)
df.drop("column", axis=1, inplace=True)
```

### 4.2 Polars现代化方案

```python
"""
Polars - 现代化高性能数据处理
"""
import polars as pl

# ============================================
# 1. Polars vs Pandas性能对比
# ============================================

# Polars优势:
# - 多线程并行
# - 懒加载优化
# - Arrow内存格式
# - Rust实现

# 读取速度: 5-10x faster
df = pl.read_csv("large.csv")

# 聚合速度: 10-100x faster
result = (
    df
    .groupby("category")
    .agg([
        pl.col("amount").sum(),
        pl.col("amount").mean()
    ])
)

# ============================================
# 2. 懒加载查询优化
# ============================================

# 懒加载 (只记录操作,不执行)
lazy = (
    pl.scan_csv("data.csv")
    .filter(pl.col("amount") > 100)
    .groupby("user_id")
    .agg(pl.col("amount").sum())
)

# 查看优化后的执行计划
print(lazy.explain())

# 触发计算
result = lazy.collect()

# ============================================
# 3. 表达式API (链式操作)
# ============================================

result = (
    pl.read_csv("data.csv")
    # 筛选
    .filter(pl.col("age") > 18)
    # 添加列
    .with_columns([
        (pl.col("amount") * 1.1).alias("amount_with_tax"),
        pl.col("name").str.to_uppercase().alias("name_upper")
    ])
    # 分组聚合
    .groupby("category")
    .agg([
        pl.col("amount").sum().alias("total"),
        pl.col("user_id").n_unique().alias("users")
    ])
    # 排序
    .sort("total", descending=True)
    # 取前10
    .head(10)
)

# ============================================
# 4. 并行处理
# ============================================

# Polars自动并行,无需手动设置
# 自动使用所有CPU核心

# 性能示例:
# 数据集: 10GB, 100M行
# 操作: 分组聚合

# Pandas (单线程): ~120s
# Polars (多线程):  ~8s  (15x faster!)
```

---

## 📊 工具选择指南

### Pandas vs Polars对比

| 维度 | Pandas | Polars | 推荐 |
|------|--------|--------|------|
| **性能** | 基准 | 5-100x faster | Polars |
| **内存** | 高 | 低 (50-70% less) | Polars |
| **并行** | 有限 | 原生多线程 | Polars |
| **生态** | 成熟完整 | 快速成长 | Pandas |
| **学习曲线** | 平缓 | 中等 | Pandas |
| **API稳定性** | 稳定 | 快速迭代 | Pandas |

### 使用场景

**使用Pandas**:
- 数据量 < 1GB
- 需要丰富的生态库
- 团队已熟悉Pandas
- 需要最大兼容性

**使用Polars**:
- 数据量 > 1GB
- 性能要求高
- 新项目或可迁移
- 需要并行处理

---

**掌握现代数据处理,构建高效数据管道！** 📊✨

**最后更新**: 2025年10月28日

