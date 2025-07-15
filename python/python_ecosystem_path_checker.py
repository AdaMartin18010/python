#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python文档整理无效路径检测与修复工具
自动检测整理扫描结果中的无效文件路径，并生成修正建议
"""

import os
from pathlib import Path
import json

SCAN_RESULT_FILE = "python_ecosystem_organization_summary.json"
REPORT_FILE = "invalid_path_report.json"


def load_scan_results():
    """加载整理扫描结果"""
    if not Path(SCAN_RESULT_FILE).exists():
        print(f"❌ 未找到扫描结果文件: {SCAN_RESULT_FILE}")
        return None
    with open(SCAN_RESULT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def check_paths(scan_results):
    """检测所有文件路径有效性"""
    invalid_files = []
    valid_files = []
    for category, info in scan_results.get("categories", {}).items():
        for file_name in info.get("files", []):
            # 在refactor和model目录下查找
            found = False
            for base in ["refactor", "model"]:
                for root, dirs, files in os.walk(base):
                    if file_name in files:
                        valid_files.append(os.path.join(root, file_name))
                        found = True
                        break
                if found:
                    break
            if not found:
                invalid_files.append({
                    "category": category,
                    "file_name": file_name
                })
    return valid_files, invalid_files


def suggest_fixes(invalid_files):
    """为无效文件生成修正建议"""
    suggestions = []
    for item in invalid_files:
        file_name = item["file_name"]
        # 建议：模糊查找相似文件名
        candidates = []
        for base in ["refactor", "model"]:
            for root, dirs, files in os.walk(base):
                for f in files:
                    if file_name.lower() in f.lower() or f.lower() in file_name.lower():
                        candidates.append(os.path.join(root, f))
        suggestions.append({
            "category": item["category"],
            "file_name": file_name,
            "candidates": candidates
        })
    return suggestions


def main():
    print("🐍 Python文档无效路径检测与修复工具")
    print("=" * 50)
    scan_results = load_scan_results()
    if not scan_results:
        return
    valid_files, invalid_files = check_paths(scan_results)
    print(f"✅ 有效文件数: {len(valid_files)}")
    print(f"❌ 无效文件数: {len(invalid_files)}")
    if invalid_files:
        print("部分无效文件示例:")
        for item in invalid_files[:10]:
            print(f"  - [{item['category']}] {item['file_name']}")
    suggestions = suggest_fixes(invalid_files)
    # 保存报告
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "valid_files": valid_files,
            "invalid_files": invalid_files,
            "suggestions": suggestions
        }, f, ensure_ascii=False, indent=2)
    print(f"📋 检查报告已生成: {REPORT_FILE}")
    print("如需自动修复，可根据suggestions字段手动或批量调整文件名/路径。")

if __name__ == "__main__":
    main() 