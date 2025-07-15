#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python知识体系完整系统
一键执行所有功能：迁移、内容填充、健康检查、可视化等
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import colorama
from colorama import Fore, Back, Style

# 初始化colorama
colorama.init()

class CompleteSystem:
    """完整系统管理器"""
    
    def __init__(self):
        self.docs_dir = Path(".")
        self.start_time = None
        self.results = {}
    
    def print_banner(self):
        """打印系统横幅"""
        print(f"{Fore.CYAN}{'='*80}")
        print(f"🐍 Python知识体系完整系统 v2.0")
        print(f"{'='*80}{Style.RESET_ALL}")
        print(f"📅 开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 工作目录: {self.docs_dir.absolute()}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def run_command(self, name, command, description=""):
        """运行命令并记录结果"""
        print(f"{Fore.YELLOW}🔄 {name}{Style.RESET_ALL}")
        if description:
            print(f"   {description}")
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.docs_dir)
            if result.returncode == 0:
                print(f"{Fore.GREEN}✅ {name} 成功{Style.RESET_ALL}")
                self.results[name] = True
                if result.stdout:
                    print(f"   输出: {result.stdout[:200]}...")
            else:
                print(f"{Fore.RED}❌ {name} 失败{Style.RESET_ALL}")
                print(f"   错误: {result.stderr}")
                self.results[name] = False
        except Exception as e:
            print(f"{Fore.RED}❌ {name} 异常: {e}{Style.RESET_ALL}")
            self.results[name] = False
    
    def phase_1_migration(self):
        """第一阶段：迁移"""
        print(f"{Fore.BLUE}📋 第一阶段：数据迁移{Style.RESET_ALL}")
        
        # 1. 内容分析
        self.run_command(
            "内容分析",
            "python python_content_analyzer.py",
            "分析现有Python内容结构"
        )
        
        # 2. 数据迁移
        self.run_command(
            "数据迁移",
            "python quick_migrate.py",
            "执行数据迁移到新结构"
        )
        
        # 3. 结果验证
        self.run_command(
            "结果验证",
            "python verify_migration.py",
            "验证迁移结果"
        )
    
    def phase_2_content_generation(self):
        """第二阶段：内容生成"""
        print(f"{Fore.BLUE}📋 第二阶段：内容生成{Style.RESET_ALL}")
        
        # 1. 生成README骨架
        self.run_command(
            "生成README骨架",
            "python batch_generate_module_readme.py",
            "为所有模块生成README模板"
        )
        
        # 2. 生成代码示例模板
        self.run_command(
            "生成代码示例模板",
            "python batch_generate_code_template.py",
            "为所有模块生成代码示例模板"
        )
        
        # 3. 生成知识点清单
        self.run_command(
            "生成知识点清单",
            "python batch_generate_knowledge_checklist.py",
            "为所有模块生成知识点清单"
        )
        
        # 4. 智能内容填充
        self.run_command(
            "智能内容填充",
            "python auto_content_filler.py",
            "自动填充初始内容"
        )
    
    def phase_3_quality_assurance(self):
        """第三阶段：质量保证"""
        print(f"{Fore.BLUE}📋 第三阶段：质量保证{Style.RESET_ALL}")
        
        # 1. 内容健康检查
        self.run_command(
            "内容健康检查",
            "python periodic_content_health_check.py",
            "检查内容质量和完整性"
        )
        
        # 2. 链接检查和修复
        self.run_command(
            "链接检查和修复",
            "python check_and_fix_links.py",
            "检查并修复内部链接"
        )
        
        # 3. 代码规范检查
        self.run_command(
            "代码规范检查",
            "python pre_commit_check.py",
            "检查代码和文档规范"
        )
    
    def phase_4_visualization(self):
        """第四阶段：可视化"""
        print(f"{Fore.BLUE}📋 第四阶段：可视化{Style.RESET_ALL}")
        
        # 1. 生成目录树
        self.run_command(
            "生成目录树",
            "python generate_directory_tree.py",
            "生成完整的目录结构图"
        )
        
        # 2. 生成思维导图
        self.run_command(
            "生成思维导图",
            "python generate_mindmap.py",
            "生成Mermaid思维导图"
        )
        
        # 3. 生成Web可视化
        self.run_command(
            "生成Web可视化",
            "python web_visualization.py",
            "生成HTML索引页面和JSON API"
        )
    
    def phase_5_collaboration(self):
        """第五阶段：团队协作"""
        print(f"{Fore.BLUE}📋 第五阶段：团队协作{Style.RESET_ALL}")
        
        # 1. 生成贡献指南
        self.run_command(
            "生成贡献指南",
            "python generate_contributing_md.py",
            "生成团队协作规范"
        )
        
        # 2. 生成GitHub Actions配置
        if Path(".github").exists():
            self.run_command(
                "配置CI/CD",
                "cp github_actions_workflow.yml .github/workflows/python-knowledge-ci.yml",
                "配置自动化CI/CD流程"
            )
    
    def phase_6_extension(self):
        """第六阶段：扩展支持"""
        print(f"{Fore.BLUE}📋 第六阶段：扩展支持{Style.RESET_ALL}")
        
        # 1. 扩展到其他语言
        self.run_command(
            "扩展多语言支持",
            "python extend_to_other_languages.py",
            "创建Java、Go、Rust等语言知识体系"
        )
    
    def print_summary(self):
        """打印执行总结"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"📊 执行总结报告")
        print(f"{'='*80}{Style.RESET_ALL}")
        
        total_steps = len(self.results)
        successful_steps = sum(1 for success in self.results.values() if success)
        
        print(f"📈 总体进度: {successful_steps}/{total_steps} 步骤完成")
        if self.start_time:
            print(f"⏱️  总耗时: {time.time() - self.start_time:.2f} 秒")
        
        print(f"\n✅ 成功步骤:")
        for step, success in self.results.items():
            if success:
                print(f"   ✓ {step}")
        
        print(f"\n❌ 失败步骤:")
        for step, success in self.results.items():
            if not success:
                print(f"   ✗ {step}")
        
        if successful_steps == total_steps:
            print(f"\n{Fore.GREEN}🎉 恭喜！所有步骤都成功完成！{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️ 部分步骤失败，请检查日志{Style.RESET_ALL}")
        
        print(f"\n📁 生成的文件:")
        generated_files = [
            "python_knowledge_system/",
            "python_knowledge_system_index.html",
            "python_knowledge_system_api.json",
            "python_knowledge_system_mindmap.mmd",
            "CONTRIBUTING.md"
        ]
        
        for file in generated_files:
            file_path = self.docs_dir / file
            if file_path.exists():
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file} (未找到)")
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    def run_complete_system(self):
        """运行完整系统"""
        self.start_time = time.time()
        self.print_banner()
        
        # 执行所有阶段
        self.phase_1_migration()
        self.phase_2_content_generation()
        self.phase_3_quality_assurance()
        self.phase_4_visualization()
        self.phase_5_collaboration()
        self.phase_6_extension()
        
        # 打印总结
        self.print_summary()
        
        return all(self.results.values())

def main():
    """主函数"""
    system = CompleteSystem()
    
    try:
        success = system.run_complete_system()
        if success:
            print(f"\n{Fore.GREEN}✅ 完整系统执行成功！{Style.RESET_ALL}")
            print(f"📁 请查看生成的 python_knowledge_system/ 目录")
            print(f"🌐 打开 python_knowledge_system_index.html 查看Web界面")
        else:
            print(f"\n{Fore.RED}❌ 完整系统执行失败！{Style.RESET_ALL}")
            print(f"📋 请检查失败的步骤并重试")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ 用户中断了系统执行{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ 系统执行出现异常: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 