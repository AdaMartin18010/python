import os

# 配置：文档根目录
ROOT_DIR = '.'  # 可根据实际情况修改
# 输出路径清单文件
OUTPUT_FILE = 'python_ecosystem_path_list.txt'


def main():
    count = 0
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for dirpath, _, filenames in os.walk(ROOT_DIR):
            for name in filenames:
                if name.endswith('.md'):
                    rel_path = os.path.relpath(os.path.join(dirpath, name), ROOT_DIR)
                    f.write(rel_path + '\n')
                    count += 1
    print(f'已生成路径清单：{OUTPUT_FILE}，共 {count} 个 Markdown 文档。')

if __name__ == '__main__':
    main()

"""
用法说明：
1. 根据实际情况修改 ROOT_DIR。
2. 运行脚本：python generate_python_ecosystem_path_list.py
3. 会自动生成 python_ecosystem_path_list.txt，供路径预检测与整理工具使用。
""" 