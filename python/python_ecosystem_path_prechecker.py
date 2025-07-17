import os
import json
import difflib
from typing import List, Dict

# 配置：待检测路径清单文件（每行一个路径，或json/csv格式）
INPUT_PATH_LIST = 'python_ecosystem_path_list.txt'  # 可根据实际情况修改
# 配置：扫描的根目录
SCAN_ROOT = '.'  # 当前目录，可根据实际情况修改
# 输出报告文件
OUTPUT_REPORT = 'path_validity_report.json'


def load_path_list(input_file: str) -> List[str]:
    """
    加载待检测路径清单，支持txt（每行一个路径）或json（list）
    """
    if input_file.endswith('.json'):
        with open(input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(input_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]


def find_similar_path(target: str, search_root: str) -> str:
    """
    在search_root下递归查找与target最相似的文件路径
    """
    all_files = []
    for root, dirs, files in os.walk(search_root):
        for name in files:
            rel_path = os.path.relpath(os.path.join(root, name), search_root)
            all_files.append(rel_path)
    matches = difflib.get_close_matches(target, all_files, n=1, cutoff=0.5)
    return matches[0] if matches else ''


def check_paths(path_list: List[str], search_root: str) -> Dict:
    """
    检查路径有效性，并为无效路径推荐修正
    """
    result = {
        'valid_paths': [],
        'invalid_paths': []
    }
    for path in path_list:
        abs_path = os.path.join(search_root, path)
        if os.path.exists(abs_path):
            result['valid_paths'].append(path)
        else:
            suggestion = find_similar_path(path, search_root)
            result['invalid_paths'].append({
                'original': path,
                'suggestion': suggestion
            })
    return result


def main():
    print(f'加载路径清单: {INPUT_PATH_LIST}')
    path_list = load_path_list(INPUT_PATH_LIST)
    print(f'共加载 {len(path_list)} 个路径，开始检测...')
    report = check_paths(path_list, SCAN_ROOT)
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f'检测完成，报告已保存至: {OUTPUT_REPORT}')
    print(f"有效路径数: {len(report['valid_paths'])}")
    print(f"无效路径数: {len(report['invalid_paths'])}")
    if report['invalid_paths']:
        print('部分无效路径及推荐修正:')
        for item in report['invalid_paths'][:5]:
            print(f"  {item['original']} -> {item['suggestion']}")

if __name__ == '__main__':
    main()

"""
用法说明：
1. 将所有待检测的文档路径写入 python_ecosystem_path_list.txt（每行一个相对路径，或用json list）。
2. 根据实际情况修改 INPUT_PATH_LIST 和 SCAN_ROOT。
3. 运行脚本：python python_ecosystem_path_prechecker.py
4. 检查输出的 path_validity_report.json，确认无效路径及推荐修正。
5. 可将有效路径用于后续整理工具。
""" 