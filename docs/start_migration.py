#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python知识体系迁移一键启动脚本
整合所有迁移工具，提供完整的迁移流程
"""

import os
import sys
import subprocess
import time
import datetime
from pathlib import Path
import colorama
from colorama import Fore, Back, Style

# 初始化colorama
colorama.init()

class MigrationOrchestrator:
    """迁移流程编排器"""
    
    def __init__(self):
        self.docs_dir = Path(".")
        self.backup_dir = self.docs_dir / "backup"
        self.log_file = self.docs_dir / "migration_orchestrator.log"
        self.start_time = None
        
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"{Fore.RED}写入日志失败: {e}{Style.RESET_ALL}")
    
    def print_header(self):
        """打印标题"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"🚀 Python知识体系迁移工具")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"📅 开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 工作目录: {self.docs_dir.absolute()}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def check_environment(self) -> bool:
        """检查环境"""
        print(f"{Fore.YELLOW}🔍 检查环境...{Style.RESET_ALL}")
        
        # 检查Python版本
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            python_version = result.stdout.strip()
            print(f"✅ Python版本: {python_version}")
        except Exception as e:
            print(f"❌ 无法获取Python版本: {e}")
            return False
        
        # 检查必要文件
        required_files = [
            "python_content_analyzer.py",
            "quick_migrate.py", 
            "verify_migration.py",
            "run_all_tools.py"
        ]
        
        missing_files = []
        for file in required_files:
            if not (self.docs_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
            return False
        
        print(f"✅ 环境检查通过")
        return True
    
    def create_backup(self) -> bool:
        """创建备份"""
        print(f"\n{Fore.YELLOW}💾 创建备份...{Style.RESET_ALL}")
        
        try:
            # 创建备份目录
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / timestamp
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # 备份重要目录
            important_dirs = ["refactor", "model"]
            for dir_name in important_dirs:
                src_dir = self.docs_dir / dir_name
                if src_dir.exists():
                    dst_dir = backup_path / dir_name
                    self._copy_directory(src_dir, dst_dir)
                    print(f"✅ 已备份: {dir_name}")
            
            print(f"✅ 备份完成: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False
    
    def _copy_directory(self, src: Path, dst: Path):
        """复制目录"""
        import shutil
        shutil.copytree(src, dst, dirs_exist_ok=True)
    
    def run_analysis(self) -> bool:
        """运行内容分析"""
        print(f"\n{Fore.YELLOW}📊 运行内容分析...{Style.RESET_ALL}")
        
        try:
            result = subprocess.run([sys.executable, "python_content_analyzer.py"],
                                  capture_output=True, text=True, cwd=self.docs_dir)
            
            if result.returncode == 0:
                print(f"✅ 内容分析完成")
                if result.stdout:
                    print(f"📋 分析输出:\n{result.stdout}")
                return True
            else:
                print(f"❌ 内容分析失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 运行分析工具失败: {e}")
            return False
    
    def run_migration(self) -> bool:
        """运行迁移"""
        print(f"\n{Fore.YELLOW}🔄 运行数据迁移...{Style.RESET_ALL}")
        
        try:
            result = subprocess.run([sys.executable, "quick_migrate.py"],
                                  capture_output=True, text=True, cwd=self.docs_dir)
            
            if result.returncode == 0:
                print(f"✅ 数据迁移完成")
                if result.stdout:
                    print(f"📋 迁移输出:\n{result.stdout}")
                return True
            else:
                print(f"❌ 数据迁移失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 运行迁移工具失败: {e}")
            return False
    
    def run_verification(self) -> bool:
        """运行验证"""
        print(f"\n{Fore.YELLOW}🔍 运行结果验证...{Style.RESET_ALL}")
        
        try:
            result = subprocess.run([sys.executable, "verify_migration.py"],
                                  capture_output=True, text=True, cwd=self.docs_dir)
            
            if result.returncode == 0:
                print(f"✅ 结果验证完成")
                if result.stdout:
                    print(f"📋 验证输出:\n{result.stdout}")
                return True
            else:
                print(f"❌ 结果验证失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 运行验证工具失败: {e}")
            return False
    
    def run_tools(self) -> bool:
        """运行工具生成"""
        print(f"\n{Fore.YELLOW}🛠️ 生成模板和工具...{Style.RESET_ALL}")
        
        try:
            result = subprocess.run([sys.executable, "run_all_tools.py"],
                                  capture_output=True, text=True, cwd=self.docs_dir)
            
            if result.returncode == 0:
                print(f"✅ 工具生成完成")
                if result.stdout:
                    print(f"📋 生成输出:\n{result.stdout}")
                return True
            else:
                print(f"❌ 工具生成失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 运行工具生成失败: {e}")
            return False
    
    def print_summary(self, results: dict):
        """打印总结"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"📊 迁移流程总结")
        print(f"{'='*70}{Style.RESET_ALL}")
        
        total_steps = len(results)
        successful_steps = sum(1 for success in results.values() if success)
        
        print(f"📈 总体进度: {successful_steps}/{total_steps} 步骤完成")
        if self.start_time:
            print(f"⏱️  总耗时: {datetime.datetime.now() - self.start_time}")
        
        print(f"\n✅ 成功步骤:")
        for step, success in results.items():
            status = "✓" if success else "✗"
            color = Fore.GREEN if success else Fore.RED
            print(f"   {color}{status} {step}{Style.RESET_ALL}")
        
        if successful_steps == total_steps:
            print(f"\n{Fore.GREEN}🎉 恭喜！所有步骤都成功完成！{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️ 部分步骤失败，请检查日志文件{Style.RESET_ALL}")
        
        print(f"\n📁 生成的文件:")
        generated_files = [
            "python_knowledge_system/",
            "templates/",
            "migration_status.json",
            "migration_log.txt"
        ]
        
        for file in generated_files:
            file_path = self.docs_dir / file
            if file_path.exists():
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file} (未找到)")
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    def run(self):
        """运行完整迁移流程"""
        self.start_time = datetime.datetime.now()
        self.print_header()
        
        # 记录开始
        self.log("开始迁移流程")
        
        # 检查环境
        if not self.check_environment():
            self.log("环境检查失败")
            return False
        
        # 创建备份
        if not self.create_backup():
            self.log("备份创建失败")
            return False
        
        # 执行迁移步骤
        steps = [
            ("内容分析", self.run_analysis),
            ("数据迁移", self.run_migration),
            ("结果验证", self.run_verification),
            ("工具生成", self.run_tools)
        ]
        
        results = {}
        
        for step_name, step_func in steps:
            print(f"\n{Fore.BLUE}🔄 执行步骤: {step_name}{Style.RESET_ALL}")
            self.log(f"开始执行: {step_name}")
            
            success = step_func()
            results[step_name] = success
            
            if success:
                self.log(f"步骤成功: {step_name}")
            else:
                self.log(f"步骤失败: {step_name}")
                print(f"{Fore.RED}❌ 步骤失败: {step_name}{Style.RESET_ALL}")
                # 可以选择是否继续
                continue
        
        # 打印总结
        self.print_summary(results)
        
        # 记录结束
        self.log("迁移流程结束")
        
        return all(results.values())

def main():
    """主函数"""
    orchestrator = MigrationOrchestrator()
    
    try:
        success = orchestrator.run()
        if success:
            print(f"\n{Fore.GREEN}✅ 迁移流程完成！{Style.RESET_ALL}")
            print(f"📁 请查看生成的 python_knowledge_system/ 目录")
        else:
            print(f"\n{Fore.RED}❌ 迁移流程失败！{Style.RESET_ALL}")
            print(f"📋 请查看日志文件: {orchestrator.log_file}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ 用户中断了迁移流程{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ 迁移流程出现异常: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 