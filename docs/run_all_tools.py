#!/usr/bin/env python3
"""
一键运行所有Python知识体系工具
按顺序执行迁移、验证、模板生成等所有操作
"""

import subprocess
import sys
from pathlib import Path
import time

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"执行命令: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"执行失败: {e}")
        return False

def check_prerequisites():
    """检查前置条件"""
    print("🔍 检查前置条件...")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ Python版本过低，需要Python 3.7+")
        return False
    
    # 检查docs目录是否存在
    if not Path("docs").exists():
        print("❌ docs目录不存在")
        return False
    
    print("✅ 前置条件检查通过")
    return True

def main():
    print("🚀 Python知识体系一键构建工具")
    print("=" * 60)
    print("本工具将按顺序执行以下操作：")
    print("1. 内容分析")
    print("2. 快速迁移")
    print("3. 迁移验证")
    print("4. 生成模板")
    print("5. 生成代码示例")
    print("6. 添加知识点清单")
    print("7. 检查链接")
    print("8. 生成目录树")
    print("=" * 60)
    
    # 检查前置条件
    if not check_prerequisites():
        print("❌ 前置条件检查失败，请先解决上述问题")
        return
    
    # 确认执行
    response = input("\n是否继续执行？(y/N): ")
    if response.lower() != 'y':
        print("操作已取消")
        return
    
    start_time = time.time()
    
    # 执行步骤
    steps = [
        ("python docs/python_content_analyzer.py", "内容分析"),
        ("python docs/quick_migrate.py", "快速迁移"),
        ("python docs/verify_migration.py", "迁移验证"),
        ("python docs/create_python_templates.py", "生成模板"),
        ("python docs/generate_code_examples.py", "生成代码示例"),
        ("python docs/generate_knowledge_checklist.py", "添加知识点清单"),
        ("python docs/check_and_fix_links.py", "检查链接"),
        ("python docs/generate_directory_tree.py", "生成目录树")
    ]
    
    success_count = 0
    total_count = len(steps)
    
    for command, description in steps:
        if run_command(command, description):
            success_count += 1
            print(f"✅ {description} 完成")
        else:
            print(f"❌ {description} 失败")
            # 询问是否继续
            response = input("是否继续执行后续步骤？(y/N): ")
            if response.lower() != 'y':
                break
    
    # 显示结果
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("🎉 执行完成！")
    print(f"{'='*60}")
    print(f"成功步骤: {success_count}/{total_count}")
    print(f"执行时间: {duration:.1f} 秒")
    
    if success_count == total_count:
        print("✅ 所有步骤执行成功！")
        print("\n📁 生成的文件:")
        print("- python_analysis_report.md (内容分析报告)")
        print("- python_migration_verification_report.md (迁移验证报告)")
        print("- link_check_report.md (链接检查报告)")
        print("- directory_tree_report.md (目录树报告)")
        print("\n📂 新目录结构:")
        print("- docs/python_knowledge/ (Python知识体系)")
        print("\n💡 下一步建议:")
        print("1. 检查生成的报告文件")
        print("2. 根据各模块README.md补充具体内容")
        print("3. 运行代码示例，验证功能")
        print("4. 定期运行验证工具，确保质量")
    else:
        print("⚠️ 部分步骤执行失败，请检查错误信息")
        print("建议手动执行失败的步骤")

if __name__ == "__main__":
    main() 