import json

# 输入：路径有效性报告
REPORT_FILE = 'path_validity_report.json'
# 输出：修正后的路径清单
FIXED_PATH_LIST = 'python_ecosystem_path_list_fixed.txt'
# 输出：修正日志
FIX_LOG = 'path_autofix_log.txt'


def main():
    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        report = json.load(f)
    valid_paths = report.get('valid_paths', [])
    invalid_paths = report.get('invalid_paths', [])

    fixed_paths = list(valid_paths)  # 先加上所有有效路径
    log_lines = []
    for item in invalid_paths:
        orig = item['original']
        sugg = item['suggestion']
        if sugg:
            fixed_paths.append(sugg)
            log_lines.append(f"修正: {orig} => {sugg}")
        else:
            log_lines.append(f"未修正: {orig} => 无推荐路径")

    # 去重并保持顺序
    seen = set()
    fixed_paths_unique = []
    for p in fixed_paths:
        if p not in seen:
            fixed_paths_unique.append(p)
            seen.add(p)

    with open(FIXED_PATH_LIST, 'w', encoding='utf-8') as f:
        for p in fixed_paths_unique:
            f.write(p + '\n')
    with open(FIX_LOG, 'w', encoding='utf-8') as f:
        for line in log_lines:
            f.write(line + '\n')
    print(f'已生成修正后的路径清单：{FIXED_PATH_LIST}，共 {len(fixed_paths_unique)} 条。')
    print(f'修正日志已保存至：{FIX_LOG}')

if __name__ == '__main__':
    main()

"""
用法说明：
1. 确保已生成 path_validity_report.json。
2. 运行脚本：python python_ecosystem_path_autofix.py
3. 会自动生成 python_ecosystem_path_list_fixed.txt（修正后的路径清单）和 path_autofix_log.txt（修正日志）。
4. 用新清单推进整理流程，或人工复核后再用。
""" 