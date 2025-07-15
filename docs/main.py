import os
import sys
import subprocess
from pathlib import Path

def run(cmd):
    print(f'\n>>> {cmd}')
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f'❌ 命令失败: {cmd}')
        sys.exit(1)

def menu():
    print('''\n==== Python知识体系自动化工具集 ====
1. 一键迁移（start_migration.py）
2. 进度监控（migration_monitor.py）
3. 内容健康巡检（periodic_content_health_check.py）
4. 批量生成README骨架
5. 批量生成代码示例模板
6. 批量生成知识点清单
7. 生成Mermaid思维导图
8. 生成贡献指南（CONTRIBUTING.md）
9. 运行pre-commit检查
0. 退出
''')
    return input('请选择操作: ')

while True:
    choice = menu()
    if choice == '1':
        run('python start_migration.py')
    elif choice == '2':
        run('python migration_monitor.py')
    elif choice == '3':
        run('python periodic_content_health_check.py')
    elif choice == '4':
        run('python batch_generate_module_readme.py')
    elif choice == '5':
        run('python batch_generate_code_template.py')
    elif choice == '6':
        run('python batch_generate_knowledge_checklist.py')
    elif choice == '7':
        run('python generate_mindmap.py')
    elif choice == '8':
        run('python generate_contributing_md.py')
    elif choice == '9':
        run('python pre_commit_check.py')
    elif choice == '0':
        print('Bye!')
        break
    else:
        print('无效选择，请重试。') 