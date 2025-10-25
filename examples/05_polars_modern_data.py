"""
Polars 2025现代数据处理实战
10-100x 性能提升 vs Pandas
"""

import polars as pl
from datetime import datetime, timedelta
import time

# ============================================================================
# 1. Polars 基础 - 与 Pandas 对比
# ============================================================================


def demonstrate_basics() -> None:
    """Polars 基础演示"""

    print("\n1️⃣ Polars 基础操作")
    print("=" * 70)

    # 创建 DataFrame
    df = pl.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
            "age": [25, 30, 35, 28, 32],
            "city": ["NYC", "LA", "Chicago", "Houston", "Phoenix"],
            "salary": [70000, 80000, 90000, 75000, 85000],
        }
    )

    print("原始数据:")
    print(df)

    # 选择列
    print("\n选择列:")
    print(df.select(["name", "age"]))

    # 过滤
    print("\n过滤 (age > 28):")
    print(df.filter(pl.col("age") > 28))

    # 排序
    print("\n按 salary 降序:")
    print(df.sort("salary", descending=True))

    # 聚合
    print("\n统计信息:")
    print(df.select([pl.col("age").mean(), pl.col("salary").sum()]))


# ============================================================================
# 2. 表达式 API (Expression API) - Polars 核心优势
# ============================================================================


def demonstrate_expressions() -> None:
    """表达式 API 演示"""

    print("\n2️⃣ Polars 表达式 API")
    print("=" * 70)

    df = pl.DataFrame(
        {
            "product": ["A", "B", "A", "C", "B", "A"],
            "sales": [100, 150, 120, 200, 180, 90],
            "quantity": [10, 15, 12, 20, 18, 9],
            "date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05", "2025-01-06"],
        }
    ).with_columns(pl.col("date").str.to_date())

    # 链式操作 - Polars 的强项
    result = (
        df.group_by("product")
        .agg(
            [
                pl.col("sales").sum().alias("total_sales"),
                pl.col("quantity").sum().alias("total_quantity"),
                pl.col("sales").mean().alias("avg_sales"),
                pl.len().alias("count"),
            ]
        )
        .with_columns((pl.col("total_sales") / pl.col("total_quantity")).alias("price_per_unit"))
        .sort("total_sales", descending=True)
    )

    print("分组聚合结果:")
    print(result)


# ============================================================================
# 3. 懒加载 (Lazy Evaluation) - 性能关键
# ============================================================================


def demonstrate_lazy_evaluation() -> None:
    """懒加载演示"""

    print("\n3️⃣ 懒加载 (Lazy Evaluation)")
    print("=" * 70)

    # 创建懒加载 DataFrame
    lazy_df = pl.LazyFrame(
        {
            "id": range(1, 1001),
            "value": range(1000, 2000),
            "category": ["A", "B", "C", "D"] * 250,
        }
    )

    # 构建查询 (不会立即执行)
    query = (
        lazy_df.filter(pl.col("value") > 1500)
        .group_by("category")
        .agg([pl.col("value").sum().alias("total"), pl.count().alias("count")])
        .sort("total", descending=True)
    )

    print("查询计划:")
    print(query.explain())

    print("\n执行查询:")
    start = time.perf_counter()
    result = query.collect()  # 执行查询
    end = time.perf_counter()

    print(result)
    print(f"执行时间: {(end - start) * 1000:.2f} ms")


# ============================================================================
# 4. 窗口函数 (Window Functions)
# ============================================================================


def demonstrate_window_functions() -> None:
    """窗口函数演示"""

    print("\n4️⃣ 窗口函数 (Window Functions)")
    print("=" * 70)

    df = pl.DataFrame(
        {
            "department": ["IT", "IT", "HR", "HR", "Sales", "Sales"],
            "employee": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
            "salary": [70000, 80000, 60000, 65000, 75000, 72000],
        }
    )

    # 窗口函数: 计算部门内排名
    result = df.with_columns(
        [
            # 部门平均工资
            pl.col("salary").mean().over("department").alias("dept_avg_salary"),
            # 部门内排名
            pl.col("salary").rank("dense").over("department").alias("dept_rank"),
            # 与部门平均的差值
            (pl.col("salary") - pl.col("salary").mean().over("department")).alias("diff_from_avg"),
        ]
    )

    print("窗口函数结果:")
    print(result)


# ============================================================================
# 5. 连接 (Joins)
# ============================================================================


def demonstrate_joins() -> None:
    """连接操作演示"""

    print("\n5️⃣ 数据连接 (Joins)")
    print("=" * 70)

    # 用户表
    users = pl.DataFrame(
        {
            "user_id": [1, 2, 3, 4],
            "username": ["alice", "bob", "charlie", "diana"],
            "email": [
                "alice@example.com",
                "bob@example.com",
                "charlie@example.com",
                "diana@example.com",
            ],
        }
    )

    # 订单表
    orders = pl.DataFrame(
        {
            "order_id": [101, 102, 103, 104, 105],
            "user_id": [1, 2, 1, 3, 2],
            "amount": [100, 200, 150, 300, 250],
        }
    )

    # Inner Join
    inner_join = users.join(orders, on="user_id", how="inner")
    print("Inner Join:")
    print(inner_join)

    # Left Join
    left_join = users.join(orders, on="user_id", how="left")
    print("\nLeft Join:")
    print(left_join)

    # 聚合 Join
    user_stats = (
        users.join(
            orders.group_by("user_id").agg(
                [pl.col("amount").sum().alias("total_amount"), pl.count().alias("order_count")]
            ),
            on="user_id",
            how="left",
        )
        .with_columns(
            [
                pl.col("total_amount").fill_null(0),
                pl.col("order_count").fill_null(0),
            ]
        )
    )

    print("\n用户订单统计:")
    print(user_stats)


# ============================================================================
# 6. 时间序列处理
# ============================================================================


def demonstrate_time_series() -> None:
    """时间序列处理"""

    print("\n6️⃣ 时间序列处理")
    print("=" * 70)

    # 生成时间序列数据
    dates = pl.date_range(
        datetime(2025, 1, 1), datetime(2025, 1, 31), interval="1d", eager=True
    )

    df = pl.DataFrame(
        {
            "date": dates,
            "value": range(1, 32),
            "category": ["A", "B"] * 15 + ["A"],
        }
    )

    print("原始时间序列:")
    print(df.head())

    # 时间操作
    result = df.with_columns(
        [
            pl.col("date").dt.day().alias("day"),
            pl.col("date").dt.month().alias("month"),
            pl.col("date").dt.weekday().alias("weekday"),
            pl.col("date").dt.week().alias("week"),
        ]
    )

    print("\n时间特征提取:")
    print(result.head())

    # 按周聚合
    weekly = df.group_by_dynamic("date", every="1w").agg(
        [pl.col("value").sum().alias("weekly_sum"), pl.col("value").mean().alias("weekly_avg")]
    )

    print("\n按周聚合:")
    print(weekly)


# ============================================================================
# 7. 性能对比 (Polars vs Pandas)
# ============================================================================


def benchmark_polars_vs_pandas() -> None:
    """性能对比"""

    print("\n7️⃣ 性能对比 (Polars vs Pandas)")
    print("=" * 70)

    # 生成测试数据
    n = 1_000_000
    data = {
        "id": range(n),
        "value": range(n),
        "category": ["A", "B", "C", "D"] * (n // 4),
    }

    # Polars 测试
    print("\nPolars 测试 (1,000,000 行):")
    start = time.perf_counter()

    df_polars = pl.DataFrame(data)
    result_polars = (
        df_polars.filter(pl.col("value") > 500000)
        .group_by("category")
        .agg([pl.col("value").sum().alias("sum"), pl.col("value").mean().alias("mean")])
    )

    end = time.perf_counter()
    polars_time = (end - start) * 1000

    print(f"✅ Polars 耗时: {polars_time:.2f} ms")
    print(result_polars)

    # Pandas 对比 (如果安装了pandas)
    try:
        import pandas as pd

        print("\nPandas 测试 (1,000,000 行):")
        start = time.perf_counter()

        df_pandas = pd.DataFrame(data)
        result_pandas = (
            df_pandas[df_pandas["value"] > 500000].groupby("category")["value"].agg(["sum", "mean"])
        )

        end = time.perf_counter()
        pandas_time = (end - start) * 1000

        print(f"✅ Pandas 耗时: {pandas_time:.2f} ms")
        print(result_pandas)

        speedup = pandas_time / polars_time
        print(f"\n🚀 Polars 速度提升: {speedup:.1f}x")

    except ImportError:
        print("\n⚠️  Pandas 未安装,跳过对比")


# ============================================================================
# 8. 数据导入导出
# ============================================================================


def demonstrate_io() -> None:
    """数据 I/O 演示"""

    print("\n8️⃣ 数据 I/O")
    print("=" * 70)

    # 创建示例数据
    df = pl.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
            "score": [85, 92, 78, 88, 95],
        }
    )

    # 写入 CSV
    df.write_csv("examples/data/sample.csv")
    print("✅ 写入 CSV: examples/data/sample.csv")

    # 读取 CSV (懒加载)
    df_lazy = pl.scan_csv("examples/data/sample.csv")
    print("✅ 懒加载 CSV:")
    print(df_lazy.collect())

    # 写入 Parquet (推荐格式)
    df.write_parquet("examples/data/sample.parquet")
    print("\n✅ 写入 Parquet: examples/data/sample.parquet")

    # 读取 Parquet
    df_parquet = pl.read_parquet("examples/data/sample.parquet")
    print("✅ 读取 Parquet:")
    print(df_parquet)


# ============================================================================
# 9. 高级特性 - UDF 和自定义函数
# ============================================================================


def demonstrate_advanced() -> None:
    """高级特性演示"""

    print("\n9️⃣ 高级特性")
    print("=" * 70)

    df = pl.DataFrame({"a": [1, 2, 3, 4, 5], "b": [10, 20, 30, 40, 50]})

    # 使用 map_elements 应用自定义函数
    def custom_function(x: int) -> int:
        return x * 2 + 1

    result = df.with_columns(pl.col("a").map_elements(custom_function, return_dtype=pl.Int64).alias("custom"))

    print("自定义函数应用:")
    print(result)

    # when-then-otherwise (类似 SQL CASE WHEN)
    result2 = df.with_columns(
        pl.when(pl.col("a") > 3)
        .then(pl.lit("high"))
        .when(pl.col("a") > 1)
        .then(pl.lit("medium"))
        .otherwise(pl.lit("low"))
        .alias("category")
    )

    print("\nwhen-then-otherwise:")
    print(result2)


# ============================================================================
# 主程序
# ============================================================================


def main() -> None:
    """主函数"""
    print("=" * 70)
    print("Polars 2025 现代数据处理实战")
    print("=" * 70)

    # 创建数据目录
    import os

    os.makedirs("examples/data", exist_ok=True)

    try:
        # 1. 基础操作
        demonstrate_basics()

        # 2. 表达式 API
        demonstrate_expressions()

        # 3. 懒加载
        demonstrate_lazy_evaluation()

        # 4. 窗口函数
        demonstrate_window_functions()

        # 5. 连接
        demonstrate_joins()

        # 6. 时间序列
        demonstrate_time_series()

        # 7. 性能对比
        benchmark_polars_vs_pandas()

        # 8. I/O 操作
        demonstrate_io()

        # 9. 高级特性
        demonstrate_advanced()

        print("\n" + "=" * 70)
        print("✅ Polars 演示完成!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # 检查 Polars 是否安装
    try:
        import polars as pl

        print(f"✅ Polars 版本: {pl.__version__}")
        main()
    except ImportError:
        print("❌ Polars 未安装")
        print("安装命令: uv pip install polars")

