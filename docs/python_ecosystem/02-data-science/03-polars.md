# Polars 高性能数据框架

**比Pandas快10-100倍的现代数据框架**

---

## 📋 概述

Polars是一个极速的数据框架库，使用Rust编写，提供Python绑定。在大多数操作上比Pandas快10-100倍，同时提供更好的API设计。

### 核心特性

- ⚡ **极速性能** - 比Pandas快10-100倍
- 💾 **内存高效** - 优化的内存使用
- 🔄 **并行处理** - 自动并行化
- 🎯 **表达式API** - 清晰的查询语法
- 🦀 **Rust核心** - 底层使用Rust实现

---

## 🚀 快速开始

### 安装

```bash
# 使用 uv (推荐)
uv add polars

# 或使用 pip
pip install polars
```

### Hello Polars

```python
import polars as pl

# 创建DataFrame
df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NYC", "LA", "Chicago"]
})

print(df)
```

---

## 💻 核心功能

### 1. 数据读取

```python
import polars as pl

# 读取CSV
df = pl.read_csv("data.csv")

# 读取Parquet (推荐，更快)
df = pl.read_parquet("data.parquet")

# 读取JSON
df = pl.read_json("data.json")

# 扫描大文件 (惰性加载)
lazy_df = pl.scan_csv("huge_file.csv")
```

### 2. 数据筛选

```python
# 单条件筛选
df_filtered = df.filter(pl.col("age") > 25)

# 多条件筛选
df_filtered = df.filter(
    (pl.col("age") > 25) & (pl.col("city") == "NYC")
)

# 字符串筛选
df_filtered = df.filter(pl.col("name").str.contains("Alice"))
```

### 3. 数据选择

```python
# 选择列
df_selected = df.select(["name", "age"])

# 使用表达式
df_selected = df.select([
    pl.col("name"),
    pl.col("age"),
    (pl.col("age") + 10).alias("age_plus_10")
])

# 排除列
df_selected = df.select(pl.exclude("city"))
```

### 4. 数据转换

```python
# 添加新列
df = df.with_columns([
    (pl.col("age") * 2).alias("double_age"),
    pl.when(pl.col("age") > 30)
        .then(pl.lit("Senior"))
        .otherwise(pl.lit("Junior"))
        .alias("level")
])

# 重命名列
df = df.rename({"name": "full_name"})

# 类型转换
df = df.with_columns([
    pl.col("age").cast(pl.Float64)
])
```

### 5. 分组聚合

```python
# 简单分组
result = df.group_by("city").agg([
    pl.col("age").mean().alias("avg_age"),
    pl.col("age").count().alias("count")
])

# 多列分组
result = df.group_by(["city", "level"]).agg([
    pl.col("age").min(),
    pl.col("age").max(),
    pl.col("age").std()
])
```

---

## 🎯 表达式API

### 强大的表达式系统

```python
# 复杂表达式
df = df.with_columns([
    # 条件表达式
    pl.when(pl.col("age") < 18)
        .then(pl.lit("Child"))
        .when(pl.col("age") < 65)
        .then(pl.lit("Adult"))
        .otherwise(pl.lit("Senior"))
        .alias("age_group"),
    
    # 数学表达式
    ((pl.col("age") - pl.col("age").mean()) / pl.col("age").std())
        .alias("age_zscore"),
    
    # 字符串操作
    pl.col("name").str.to_uppercase().alias("name_upper")
])
```

---

## ⚡ 惰性计算 (Lazy API)

### 查询优化

```python
# 惰性模式 - 不立即执行
lazy_df = (
    pl.scan_csv("data.csv")
    .filter(pl.col("age") > 25)
    .select(["name", "age", "city"])
    .group_by("city")
    .agg([
        pl.col("age").mean().alias("avg_age")
    ])
)

# 查看执行计划
print(lazy_df.explain())

# 执行查询
result = lazy_df.collect()
```

---

## 📊 性能对比

### Polars vs Pandas

```python
import polars as pl
import pandas as pd
import time

# 生成测试数据
n = 10_000_000
data = {
    "a": list(range(n)),
    "b": list(range(n, 2*n)),
    "c": ["x" if i % 2 == 0 else "y" for i in range(n)]
}

# Pandas
start = time.time()
df_pandas = pd.DataFrame(data)
result_pandas = df_pandas.groupby("c")["a"].mean()
pandas_time = time.time() - start

# Polars
start = time.time()
df_polars = pl.DataFrame(data)
result_polars = df_polars.group_by("c").agg(pl.col("a").mean())
polars_time = time.time() - start

print(f"Pandas: {pandas_time:.2f}s")
print(f"Polars: {polars_time:.2f}s")
print(f"Speedup: {pandas_time/polars_time:.1f}x")
# 输出: Speedup: 15-50x (取决于操作)
```

---

## 🔄 与Pandas互操作

### 转换

```python
import polars as pl
import pandas as pd

# Pandas → Polars
pandas_df = pd.DataFrame({"a": [1, 2, 3]})
polars_df = pl.from_pandas(pandas_df)

# Polars → Pandas
pandas_df = polars_df.to_pandas()

# Arrow格式 (零拷贝)
arrow_table = polars_df.to_arrow()
```

---

## 💡 最佳实践

### 1. 优先使用Parquet

```python
# ✅ 好 - Parquet格式
df = pl.read_parquet("data.parquet")  # 快10-100倍

# ❌ 差 - CSV格式
df = pl.read_csv("data.csv")  # 慢且占用内存
```

### 2. 使用惰性API处理大文件

```python
# ✅ 好 - 惰性加载
result = (
    pl.scan_csv("huge.csv")
    .filter(pl.col("age") > 25)
    .collect()
)

# ❌ 差 - 立即加载
df = pl.read_csv("huge.csv")  # 可能内存不足
result = df.filter(pl.col("age") > 25)
```

### 3. 链式操作

```python
# ✅ 好 - 链式操作
result = (
    df
    .filter(pl.col("age") > 25)
    .with_columns([
        (pl.col("age") * 2).alias("double_age")
    ])
    .group_by("city")
    .agg(pl.col("age").mean())
)
```

---

## 🎓 常见操作对照

### Pandas → Polars

| 操作 | Pandas | Polars |
|------|--------|--------|
| 筛选 | `df[df['age'] > 25]` | `df.filter(pl.col("age") > 25)` |
| 选择 | `df[['name', 'age']]` | `df.select(["name", "age"])` |
| 分组 | `df.groupby('city').mean()` | `df.group_by("city").agg(pl.all().mean())` |
| 排序 | `df.sort_values('age')` | `df.sort("age")` |
| 新列 | `df['new'] = df['a'] + df['b']` | `df.with_columns([(pl.col("a") + pl.col("b")).alias("new")])` |

---

## 📚 高级功能

### 窗口函数

```python
df = df.with_columns([
    # 排名
    pl.col("age").rank().over("city").alias("age_rank"),
    
    # 移动平均
    pl.col("age").rolling_mean(window_size=3).alias("age_ma"),
    
    # 累计和
    pl.col("age").cum_sum().over("city").alias("age_cumsum")
])
```

### Join操作

```python
df1 = pl.DataFrame({"id": [1, 2, 3], "name": ["A", "B", "C"]})
df2 = pl.DataFrame({"id": [1, 2, 4], "score": [90, 85, 95]})

# Inner join
result = df1.join(df2, on="id", how="inner")

# Left join
result = df1.join(df2, on="id", how="left")

# Cross join
result = df1.join(df2, how="cross")
```

---

## 🔗 相关资源

- [官方文档](https://pola-rs.github.io/polars/)
- [GitHub仓库](https://github.com/pola-rs/polars)
- [性能测试](https://www.pola.rs/benchmarks.html)

---

**最后更新**: 2025年10月28日

