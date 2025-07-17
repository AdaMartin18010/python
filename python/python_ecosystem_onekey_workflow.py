import os
import subprocess
import sys

# 步骤1：生成路径清单
STEP1_SCRIPT = 'generate_python_ecosystem_path_list.py'
# 步骤2：路径有效性检测
STEP2_SCRIPT = 'python_ecosystem_path_prechecker.py'
# 步骤3：路径自动修正
STEP3_SCRIPT = 'python_ecosystem_path_autofix.py'
# 步骤4：整理工具（请根据实际情况修改）
# 例如 ORGANIZER_SCRIPT = 'python_ecosystem_organizer.py'
ORGANIZER_SCRIPT = 'python_ecosystem_organizer.py'  # 如有 launcher 可切换
# 步骤4输入参数（如支持自定义路径清单）
ORGANIZER_PATH_LIST = 'python_ecosystem_path_list_fixed.txt'

LOG_FILE = 'python_ecosystem_onekey_workflow.log'

def run_step(cmd, desc):
    print(f'【{desc}】...')
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f'\n==== {desc} ====' + '\n')
        try:
            result = subprocess.run([sys.executable, cmd], capture_output=True, text=True)
            log.write(result.stdout)
            log.write(result.stderr)
            if result.returncode == 0:
                print(f'  {desc} 完成')
            else:
                print(f'  {desc} 失败，详见日志')
        except Exception as e:
            log.write(str(e) + '\n')
            print(f'  {desc} 执行异常，详见日志')

def main():
    # 清空日志
    with open(LOG_FILE, 'w', encoding='utf-8') as log:
        log.write('Python生态文档一键整理流程日志\n')
    # 步骤1
    run_step(STEP1_SCRIPT, '生成路径清单')
    # 步骤2
    run_step(STEP2_SCRIPT, '路径有效性检测')
    # 步骤3
    run_step(STEP3_SCRIPT, '路径自动修正')
    # 步骤4（如整理工具支持自定义路径清单，可加参数，否则请在整理工具内适配）
    if os.path.exists(ORGANIZER_SCRIPT):
        print('【整理工具】...')
        with open(LOG_FILE, 'a', encoding='utf-8') as log:
            log.write('\n==== 整理工具 ====' + '\n')
            try:
                # 假设整理工具支持 -i 参数指定路径清单
                result = subprocess.run([sys.executable, ORGANIZER_SCRIPT, '-i', ORGANIZER_PATH_LIST], capture_output=True, text=True)
                log.write(result.stdout)
                log.write(result.stderr)
                if result.returncode == 0:
                    print('  整理工具执行完成')
                else:
                    print('  整理工具执行失败，详见日志')
            except Exception as e:
                log.write(str(e) + '\n')
                print('  整理工具执行异常，详见日志')
    else:
        print(f'未检测到整理工具脚本：{ORGANIZER_SCRIPT}，请根据实际情况修改本脚本')
    print(f'全部流程已结束，详见日志：{LOG_FILE}')

if __name__ == '__main__':
    main()

"""
用法说明：
1. 可根据实际情况修改 ORGANIZER_SCRIPT 和参数。
2. 运行脚本：python python_ecosystem_onekey_workflow.py
3. 自动串联所有整理流程，输出详细日志。
4. 所有步骤均安全，不删除原始文件。
""" 