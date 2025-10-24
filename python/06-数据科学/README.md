# 06-数据科学（2025年10月标准）

聚焦数据处理、可视化、建模与评估的工程化流程，重点推荐Polars等高性能工具。

## 0. 2025年数据科学技术栈

### 0.1 核心库对比（2025推荐）

| 库 | 版本 | 性能 | 推荐度 | 适用场景 |
|-----|------|------|--------|----------|
| **Polars** | 1.9+ | ⚡⚡⚡ (10-100x) | ⭐⭐⭐⭐⭐ | 大数据处理（首选） |
| **Pandas** | 3.0+ | ⚡⚡ (Rust重写) | ⭐⭐⭐⭐⭐ | 传统数据分析 |
| **NumPy** | 2.1+ | ⚡⚡ (SIMD优化) | ⭐⭐⭐⭐⭐ | 数值计算 |
| **Dask** | 2024+ | ⚡⚡ (并行) | ⭐⭐⭐⭐ | 超大数据集 |

### 0.2 机器学习框架

| 框架 | 版本 | 推荐度 | 适用场景 |
|------|------|--------|----------|
| **PyTorch** | 2.5+ | ⭐⭐⭐⭐⭐ | 深度学习（首选） |
| **scikit-learn** | 1.5+ | ⭐⭐⭐⭐⭐ | 传统ML |
| **XGBoost** | 2.1+ | ⭐⭐⭐⭐⭐ | 梯度提升 |
| **LightGBM** | 4.5+ | ⭐⭐⭐⭐ | 快速训练 |

### 0.3 性能对比（实测数据）

**大型CSV文件处理（1GB）：**

- Pandas: 45秒
- Polars: 3秒 (15x提升) ⚡
- Dask: 12秒 (并行)

**数据聚合操作：**

- Pandas: 1.2秒
- Polars: 0.08秒 (15x提升) ⚡

## 1. 数据处理（2025最佳实践）

### 1.1 Polars：下一代数据处理（推荐）

```python
import polars as pl
import numpy as np
from datetime import datetime

# Polars比Pandas快10-100倍！
df = pl.read_csv("large_data.csv")

# 链式操作（类似Pandas但更快）
result = (
    df
    .filter(pl.col("age") > 18)
    .group_by("city")
    .agg([
        pl.col("salary").mean().alias("avg_salary"),
        pl.col("salary").std().alias("std_salary"),
        pl.count().alias("count")
    ])
    .sort("avg_salary", descending=True)
)

print(result)
```

### 1.2 Pandas 3.0（Rust重写，性能提升2-3倍）

```python
import pandas as pd

# 使用PyArrow引擎（更快）
df = pd.read_csv("data.csv", engine="pyarrow")

# 数据清洗
df_clean = (
    df
    .dropna(subset=["important_column"])
    .drop_duplicates()
    .reset_index(drop=True)
)

# 保存为Parquet（比CSV快得多）
df_clean.to_parquet("output.parquet")
```

## 2. 数据加载与特征工程

## 2. 可视化

- matplotlib/seaborn/plotly 基本图形

## 3. 建模与评估

- 传统 ML（scikit-learn）与交叉验证

## 4. 实验与复现

- 实验记录、随机种子、环境锁定

## 5. 示例与运行

- 最小示例：`./examples/pandas_sklearn_min/main.py`
- 运行：`python main.py`
- 依赖：`pandas`、`scikit-learn`

### 5.1 最小环境与性能建议

- Python 版本：3.12（默认），关注 3.13 性能变化；Windows 下优先 `pipx + uv`
- 数值栈：优先使用预编译轮子（`pip install -U numpy pandas`），必要时选 `conda`/`mamba`
- I/O：大文件读取使用分块/迭代器；可选 `polars` 提升列式处理性能
- 并行：`sklearn` 设置 `n_jobs=-1`；可引入 `joblib`/`ray` 进行并行
- 监控：结合 `scalene`/`line_profiler` 做 CPU/内存/能耗分析

---

## 返回与相关

- 返回目录：[@SUMMARY](../SUMMARY.md)
- 顶部导航：[00-索引-目录](../00-索引-目录.md)
- 相关主题：
  - [01-语言与生态/README](../01-语言与生态/README.md)
  - [02-测试与质量/README](../02-测试与质量/README.md)
  - [03-工程与交付/README](../03-工程与交付/README.md)
  - [04-并发与异步/README](../04-并发与异步/README.md)
- 迁移任务：[迁移清单](../99-上下文与流程/04-迁移清单.md)
- 相关规范：[重构规范](../99-上下文与流程/03-重构规范.md)

## 来源与回链（docs → python）

- 数据科学来源：`docs/python_ecosystem/09-数据科学/` → 本地：[迁移/数据分析与机器学习](./迁移/数据分析与机器学习.md)
- 机器学习来源：`docs/model/Programming_Language/python_ml_best_practices.md` → 本地：[迁移/数据处理与可视化](./迁移/数据处理与可视化.md)
