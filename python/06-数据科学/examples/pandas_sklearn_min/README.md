# pandas + scikit-learn 最小示例

## 依赖

- 快速安装（推荐 uv）：
  - `uv pip install -e .[dev]`
- 或使用 pip：`pip install pandas scikit-learn joblib`

## 运行

- Windows PowerShell：`python .\main.py`
- *nix：`python ./main.py`

## 数据

- 示例中生成内存数据；如需外部 CSV，请在 `main.py` 中替换为 `pd.read_csv()` 并确保路径可用。

## 评估与持久化

- 程序将输出 `accuracy/precision/recall/f1` 指标，并将训练好的模型保存为 `model.joblib`。
- 你可以在后续脚本中通过 `joblib.load("model.joblib")` 加载并进行预测。

### 预期输出（示例）

```json
{"accuracy": 0.667, "precision": 1.0, "recall": 0.5, "f1": 0.667}
```

## 预测脚本（predict.py）

- 训练后运行：

```bash
python predict.py --x1 2.0 --x2 1.0 --model model.joblib
```

## 超参搜索（grid_search.py）

- 运行：

```bash
python grid_search.py
```

## 返回与相关

- 返回目录：[@SUMMARY](../../../SUMMARY.md)
- 上级主题：[06-数据科学/README](../../README.md)
