#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python知识体系迁移进度监控工具
实时监控迁移进度，提供详细的状态报告
"""

import os
import json
import time
import datetime
from pathlib import Path
from typing import Dict, List, Any
import colorama
from colorama import Fore, Back, Style

# 初始化colorama
colorama.init()

class MigrationMonitor:
    """迁移进度监控器"""
    
    def __init__(self, docs_dir: str = "."):
        self.docs_dir = Path(docs_dir)
        self.monitor_file = self.docs_dir / "migration_status.json"
        self.log_file = self.docs_dir / "migration_monitor.log"
        self.start_time = None
        self.status = {
            "start_time": None,
            "current_step": None,
            "progress": 0,
            "steps_completed": [],
            "steps_pending": [],
            "errors": [],
            "warnings": [],
            "statistics": {}
        }
    
    def start_monitoring(self):
        """开始监控"""
        self.start_time = datetime.datetime.now()
        self.status["start_time"] = self.start_time.isoformat()
        self.status["steps_pending"] = [
            "内容分析",
            "数据迁移", 
            "结果验证",
            "模板生成"
        ]
        self._save_status()
        self._log("开始监控迁移进度")
        print(f"{Fore.GREEN}🚀 开始监控迁移进度{Style.RESET_ALL}")
    
    def update_step(self, step_name: str, progress: int | None = None):
        """更新当前步骤"""
        self.status["current_step"] = step_name
        if progress is not None:
            self.status["progress"] = progress
        
        if step_name in self.status["steps_pending"]:
            self.status["steps_pending"].remove(step_name)
            self.status["steps_completed"].append(step_name)
        
        self._save_status()
        progress_str = f"{progress}%" if progress is not None else "未知"
        self._log(f"更新步骤: {step_name}, 进度: {progress_str}")
        self._print_status()
    
    def add_error(self, error_msg: str):
        """添加错误信息"""
        self.status["errors"].append({
            "time": datetime.datetime.now().isoformat(),
            "message": error_msg
        })
        self._save_status()
        self._log(f"错误: {error_msg}")
        print(f"{Fore.RED}❌ 错误: {error_msg}{Style.RESET_ALL}")
    
    def add_warning(self, warning_msg: str):
        """添加警告信息"""
        self.status["warnings"].append({
            "time": datetime.datetime.now().isoformat(),
            "message": warning_msg
        })
        self._save_status()
        self._log(f"警告: {warning_msg}")
        print(f"{Fore.YELLOW}⚠️ 警告: {warning_msg}{Style.RESET_ALL}")
    
    def update_statistics(self, stats: Dict[str, Any]):
        """更新统计信息"""
        self.status["statistics"].update(stats)
        self._save_status()
    
    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return self.status.copy()
    
    def print_summary(self):
        """打印总结报告"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"📊 迁移进度总结报告")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        # 基本信息
        if self.status["start_time"]:
            start_time = datetime.datetime.fromisoformat(self.status["start_time"])
            duration = datetime.datetime.now() - start_time
            print(f"⏱️  开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⏱️  运行时长: {duration}")
        
        # 进度信息
        print(f"📈 总体进度: {self.status['progress']}%")
        print(f"🔄 当前步骤: {self.status['current_step'] or '未开始'}")
        
        # 步骤状态
        print(f"\n✅ 已完成步骤:")
        for step in self.status["steps_completed"]:
            print(f"   ✓ {step}")
        
        print(f"\n⏳ 待完成步骤:")
        for step in self.status["steps_pending"]:
            print(f"   ○ {step}")
        
        # 错误和警告
        if self.status["errors"]:
            print(f"\n❌ 错误 ({len(self.status['errors'])}个):")
            for error in self.status["errors"][-3:]:  # 只显示最近3个
                print(f"   • {error['message']}")
        
        if self.status["warnings"]:
            print(f"\n⚠️ 警告 ({len(self.status['warnings'])}个):")
            for warning in self.status["warnings"][-3:]:  # 只显示最近3个
                print(f"   • {warning['message']}")
        
        # 统计信息
        if self.status["statistics"]:
            print(f"\n📊 统计信息:")
            for key, value in self.status["statistics"].items():
                print(f"   • {key}: {value}")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    def _save_status(self):
        """保存状态到文件"""
        try:
            with open(self.monitor_file, 'w', encoding='utf-8') as f:
                json.dump(self.status, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"{Fore.RED}保存状态文件失败: {e}{Style.RESET_ALL}")
    
    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"{Fore.RED}写入日志失败: {e}{Style.RESET_ALL}")
    
    def _print_status(self):
        """打印当前状态"""
        progress_bar = self._create_progress_bar(self.status["progress"])
        print(f"\n{Fore.BLUE}📊 迁移进度: {progress_bar} {self.status['progress']}%")
        if self.status["current_step"]:
            print(f"🔄 当前步骤: {self.status['current_step']}")
        print(f"{Style.RESET_ALL}")
    
    def _create_progress_bar(self, progress: int, width: int = 30) -> str:
        """创建进度条"""
        filled = int(width * progress / 100)
        bar = "█" * filled + "░" * (width - filled)
        return bar

class FileAnalyzer:
    """文件分析器"""
    
    def __init__(self, docs_dir: str = "."):
        self.docs_dir = Path(docs_dir)
    
    def analyze_directory(self) -> Dict[str, Any]:
        """分析目录结构"""
        stats = {
            "total_files": 0,
            "total_dirs": 0,
            "python_files": 0,
            "markdown_files": 0,
            "other_files": 0,
            "file_types": {},
            "largest_files": [],
            "recent_files": []
        }
        
        for root, dirs, files in os.walk(self.docs_dir):
            # 跳过隐藏目录和临时文件
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            stats["total_dirs"] += len(dirs)
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                stats["total_files"] += 1
                
                # 统计文件类型
                ext = file_path.suffix.lower()
                stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                
                # 统计特定类型文件
                if ext == '.py':
                    stats["python_files"] += 1
                elif ext == '.md':
                    stats["markdown_files"] += 1
                else:
                    stats["other_files"] += 1
                
                # 记录文件大小
                try:
                    size = file_path.stat().st_size
                    stats["largest_files"].append((str(file_path), size))
                except:
                    pass
        
        # 排序并保留前10个最大的文件
        stats["largest_files"].sort(key=lambda x: x[1], reverse=True)
        stats["largest_files"] = stats["largest_files"][:10]
        
        return stats

def main():
    """主函数"""
    print(f"{Fore.CYAN}🔍 Python知识体系迁移监控工具{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # 创建监控器
    monitor = MigrationMonitor()
    analyzer = FileAnalyzer()
    
    # 开始监控
    monitor.start_monitoring()
    
    # 分析当前目录
    print(f"\n{Fore.YELLOW}📁 分析当前目录结构...{Style.RESET_ALL}")
    stats = analyzer.analyze_directory()
    monitor.update_statistics(stats)
    monitor.update_step("目录分析", 25)
    
    # 模拟迁移过程
    steps = [
        ("内容分析", 25),
        ("数据迁移", 50), 
        ("结果验证", 75),
        ("模板生成", 100)
    ]
    
    for step_name, progress in steps:
        print(f"\n{Fore.GREEN}🔄 执行步骤: {step_name}{Style.RESET_ALL}")
        monitor.update_step(step_name, progress)
        
        # 模拟处理时间
        time.sleep(2)
        
        # 模拟一些事件
        if step_name == "数据迁移":
            monitor.add_warning("发现重复内容，已自动去重")
        elif step_name == "结果验证":
            monitor.add_error("发现3个损坏的链接，已记录到日志")
    
    # 打印最终报告
    monitor.print_summary()
    
    print(f"\n{Fore.GREEN}✅ 监控完成！详细报告已保存到 migration_status.json{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 