#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语言生态文档整理一键启动器
整合所有工具，提供统一的入口
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
import json

class PythonEcosystemLauncher:
    """Python语言生态文档整理启动器"""
    
    def __init__(self):
        self.docs_dir = Path(".")
        self.available_tools = {
            "backup": "python_ecosystem_backup.py",
            "organizer": "python_ecosystem_organizer.py", 
            "enhanced": "python_ecosystem_enhanced_organizer.py",
            "workflow": "python_ecosystem_workflow.py",
            "guide": "python_ecosystem_guide.md"
        }
        self.tool_status = {}
    
    def check_tools(self) -> Dict[str, bool]:
        """检查工具可用性"""
        print("🔍 检查工具可用性...")
        
        for tool_name, tool_file in self.available_tools.items():
            tool_path = self.docs_dir / tool_file
            if tool_path.exists():
                self.tool_status[tool_name] = True
                print(f"✅ {tool_name}: {tool_file}")
            else:
                self.tool_status[tool_name] = False
                print(f"❌ {tool_name}: {tool_file} (未找到)")
        
        return self.tool_status
    
    def show_menu(self):
        """显示主菜单"""
        print("\n🐍 Python语言生态文档整理工具")
        print("=" * 50)
        print("请选择操作:")
        print("1. 快速整理 (推荐)")
        print("2. 完整工作流")
        print("3. 仅备份文档")
        print("4. 仅扫描文档")
        print("5. 预览整理计划")
        print("6. 查看使用指南")
        print("7. 检查工具状态")
        print("0. 退出")
        print("-" * 50)
    
    def quick_organize(self):
        """快速整理"""
        print("🚀 开始快速整理...")
        
        # 检查工具
        if not self.tool_status.get("organizer", False):
            print("❌ 整理工具不可用")
            return False
        
        try:
            # 导入并运行整理工具
            from python_ecosystem_organizer import PythonEcosystemOrganizer
            organizer = PythonEcosystemOrganizer()
            
            # 扫描文档
            print("📋 扫描Python相关文档...")
            scan_results = organizer.scan_existing_docs()
            
            if not scan_results:
                print("❌ 未找到Python相关文档")
                return False
            
            # 整理文档
            print("📁 整理文档...")
            organize_results = organizer.organize_documents(scan_results)
            
            # 生成总结
            print("📊 生成总结...")
            organizer.generate_summary(scan_results)
            
            print("✅ 快速整理完成！")
            return True
            
        except Exception as e:
            print(f"❌ 快速整理失败: {e}")
            return False
    
    def full_workflow(self):
        """完整工作流"""
        print("🔄 开始完整工作流...")
        
        if not self.tool_status.get("workflow", False):
            print("❌ 工作流工具不可用")
            return False
        
        try:
            # 运行工作流
            from python_ecosystem_workflow import PythonEcosystemWorkflow
            workflow = PythonEcosystemWorkflow()
            return workflow.run_workflow()
        except Exception as e:
            print(f"❌ 完整工作流失败: {e}")
            return False
    
    def backup_only(self):
        """仅备份文档"""
        print("💾 仅备份文档...")
        
        if not self.tool_status.get("backup", False):
            print("❌ 备份工具不可用")
            return False
        
        try:
            from python_ecosystem_backup import PythonEcosystemBackup
            backup_tool = PythonEcosystemBackup()
            backup_path = backup_tool.create_backup()
            print(f"✅ 备份完成: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False
    
    def scan_only(self):
        """仅扫描文档"""
        print("🔍 仅扫描文档...")
        
        if not self.tool_status.get("organizer", False):
            print("❌ 整理工具不可用")
            return False
        
        try:
            from python_ecosystem_organizer import PythonEcosystemOrganizer
            organizer = PythonEcosystemOrganizer()
            scan_results = organizer.scan_existing_docs()
            
            print(f"📊 扫描结果:")
            total_files = sum(len(files) for files in scan_results.values())
            print(f"  总文档数: {total_files}")
            
            for category, files in scan_results.items():
                print(f"  {category}: {len(files)} 个文件")
                for file_path in files[:3]:  # 显示前3个
                    print(f"    - {Path(file_path).name}")
                if len(files) > 3:
                    print(f"    ... 还有 {len(files) - 3} 个")
            
            return True
        except Exception as e:
            print(f"❌ 扫描失败: {e}")
            return False
    
    def preview_plan(self):
        """预览整理计划"""
        print("📋 预览整理计划...")
        
        if not self.tool_status.get("organizer", False):
            print("❌ 整理工具不可用")
            return False
        
        try:
            from python_ecosystem_organizer import PythonEcosystemOrganizer
            organizer = PythonEcosystemOrganizer()
            scan_results = organizer.scan_existing_docs()
            
            print("📋 整理计划预览:")
            print("=" * 50)
            
            for category, files in scan_results.items():
                if category in organizer.mapping_rules:
                    config = organizer.mapping_rules[category]
                    print(f"\n📁 {config['target_dir']}")
                    print(f"   描述: {config['description']}")
                    print(f"   文档数: {len(files)} 个")
                    print(f"   示例文档:")
                    for file_path in files[:3]:
                        print(f"     - {Path(file_path).name}")
            
            total_files = sum(len(files) for files in scan_results.values())
            print(f"\n📊 总计: {total_files} 个文档将被整理")
            
            return True
        except Exception as e:
            print(f"❌ 预览失败: {e}")
            return False
    
    def show_guide(self):
        """显示使用指南"""
        print("📖 使用指南...")
        
        guide_file = self.docs_dir / "python_ecosystem_guide.md"
        if guide_file.exists():
            try:
                with open(guide_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(content)
            except Exception as e:
                print(f"❌ 读取指南失败: {e}")
        else:
            print("❌ 使用指南文件不存在")
    
    def interactive_mode(self):
        """交互模式"""
        while True:
            self.show_menu()
            
            try:
                choice = input("请输入选择 (0-7): ").strip()
                
                if choice == "0":
                    print("👋 再见！")
                    break
                elif choice == "1":
                    self.quick_organize()
                elif choice == "2":
                    self.full_workflow()
                elif choice == "3":
                    self.backup_only()
                elif choice == "4":
                    self.scan_only()
                elif choice == "5":
                    self.preview_plan()
                elif choice == "6":
                    self.show_guide()
                elif choice == "7":
                    self.check_tools()
                else:
                    print("❌ 无效选择，请重新输入")
                
                input("\n按回车键继续...")
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 操作失败: {e}")
    
    def run(self, mode: str = "interactive"):
        """运行启动器"""
        print("🐍 Python语言生态文档整理启动器")
        print("=" * 50)
        
        # 检查工具
        self.check_tools()
        
        if mode == "interactive":
            self.interactive_mode()
        elif mode == "quick":
            self.quick_organize()
        elif mode == "full":
            self.full_workflow()
        elif mode == "backup":
            self.backup_only()
        elif mode == "scan":
            self.scan_only()
        elif mode == "preview":
            self.preview_plan()
        else:
            print(f"❌ 未知模式: {mode}")
            self.show_help()
    
    def show_help(self):
        """显示帮助信息"""
        print("""
🐍 Python语言生态文档整理启动器

用法:
  python python_ecosystem_launcher.py [模式]

可用模式:
  interactive  - 交互模式 (默认)
  quick        - 快速整理
  full         - 完整工作流
  backup       - 仅备份
  scan         - 仅扫描
  preview      - 预览计划

示例:
  python python_ecosystem_launcher.py              # 交互模式
  python python_ecosystem_launcher.py quick        # 快速整理
  python python_ecosystem_launcher.py full         # 完整工作流

功能说明:
  - 快速整理: 扫描并整理文档，适合日常使用
  - 完整工作流: 包含备份、扫描、整理、验证等完整流程
  - 仅备份: 创建文档备份
  - 仅扫描: 扫描并显示Python相关文档
  - 预览计划: 预览整理计划而不执行
        """)

def main():
    """主函数"""
    launcher = PythonEcosystemLauncher()
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help", "help"]:
            launcher.show_help()
            return
        
        # 运行指定模式
        mode = sys.argv[1]
        launcher.run(mode)
    else:
        # 运行交互模式
        launcher.run()

if __name__ == "__main__":
    main() 