# Python 生态文档自动化整理工具集

## 一键化整理集成脚本说明

本仓库已集成一键化整理脚本 `python_ecosystem_onekey_workflow.py`，可自动完成以下流程：

1. **自动扫描并生成所有 Markdown 文档路径清单**
2. **路径有效性检测**，提前发现无效或错误路径
3. **路径自动修正**，用推荐路径替换无效路径，生成新清单
4. **自动调用整理工具**（如 python_ecosystem_organizer.py），实现文档体系化整理
5. **全流程日志输出**，便于追溯和复核

### 使用方法

1. 如需自定义整理工具脚本及参数，请修改 `python_ecosystem_onekey_workflow.py` 顶部的 `ORGANIZER_SCRIPT` 和 `ORGANIZER_PATH_LIST` 变量。
2. 运行脚本：

   ```bash
   python python_ecosystem_onekey_workflow.py
   ```

3. 全流程自动执行，日志输出至 `python_ecosystem_onekey_workflow.log`。
4. 所有步骤均安全，不删除原始文件。

### 自动化整理流程图

- 路径扫描 → 路径检测 → 路径修正 → 整理归档 → 日志报告

---

## 自动化整理相关脚本功能简介与推荐顺序

| 脚本文件名                              | 主要功能简介                                                         |
|------------------------------------------|---------------------------------------------------------------------|
| generate_python_ecosystem_path_list.py   | 扫描指定目录下所有 Markdown 文档，生成路径清单 txt 文件               |
| python_ecosystem_path_prechecker.py      | 检测路径清单中每个文件是否真实存在，对无效路径给出推荐修正           |
| python_ecosystem_path_autofix.py         | 自动用推荐路径替换无效路径，生成修正后的新路径清单                   |
| python_ecosystem_onekey_workflow.py      | 串联上述所有流程并自动调用整理工具，一键完成整理与日志输出           |
| python_ecosystem_organizer.py（示例）    | 具体的文档整理归档实现脚本（可根据实际需求替换为 launcher 等工具）   |

**推荐使用顺序：**

1. generate_python_ecosystem_path_list.py
2. python_ecosystem_path_prechecker.py
3. python_ecosystem_path_autofix.py
4. python_ecosystem_onekey_workflow.py（可一键完成全部流程）
5. 结合 python_ecosystem_organizer.py 或其他整理工具实现最终归档

---

## 常见问题与使用建议

### 1. 路径不存在或“系统找不到指定的路径”报错

- 先运行 `python_ecosystem_path_prechecker.py` 检查无效路径，并用 `python_ecosystem_path_autofix.py` 自动修正。
- 检查路径清单是否为相对路径，且与实际文件结构一致。
- 如推荐路径不准确，可人工修正 `python_ecosystem_path_list_fixed.txt` 后再整理。

### 2. 整理工具未生成扫描结果文件（如 organization_summary.json）

- 多因输入路径有误或部分文件缺失导致，建议先用自动化路径检测与修正流程。
- 检查整理工具参数，确保已指定修正后的路径清单。

### 3. 如何安全备份和恢复

- 所有自动化脚本均不删除原始文件，整理前可手动备份文档目录。
- 如需自动备份，可扩展集成 `python_ecosystem_backup.py` 等脚本。

### 4. 日志与排查建议

- 全流程日志输出至 `python_ecosystem_onekey_workflow.log`，遇到异常可先查阅日志定位问题。
- 如遇脚本异常或流程中断，可单步运行各脚本排查。

### 5. 其他建议

- 推荐先用一键化脚本自动整理，遇到特殊情况再单独运行各子工具。
- 如需集成更多自动检测、报告、备份等功能，可随时扩展本工具集。

---

如有特殊需求、脚本适配或自动化扩展需求，请联系维护者或使用助手自动生成。
