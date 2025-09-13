# 06-数据科学

聚焦数据处理、可视化、建模与评估的工程化流程。

## 1. 数据与特征

- 数据加载/清洗/特征工程

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