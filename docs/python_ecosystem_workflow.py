#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语言生态文档整理工作流
整合备份、扫描、整理、验证等完整流程
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

class PythonEcosystemWorkflow:
    """Python语言生态文档整理工作流"""
    
    def __init__(self):
        self.docs_dir = Path(".")
        self.workflow_steps = [
            "backup",
            "scan", 
            "preview",
            "organize",
            "verify",
            "summary"
        ]
        self.step_results = {}
    
    def run_workflow(self, steps: Optional[List[str]] = None):
        """运行工作流"""
        if steps is None:
            steps = self.workflow_steps
        
        print("🐍 Python语言生态文档整理工作流")
        print("=" * 60)
        
        start_time = time.time()
        
        for i, step in enumerate(steps, 1):
            print(f"\n📋 步骤 {i}/{len(steps)}: {step}")
            print("-" * 40)
            
            try:
                if step == "backup":
                    self.step_results[step] = self._run_backup()
                elif step == "scan":
                    self.step_results[step] = self._run_scan()
                elif step == "preview":
                    self.step_results[step] = self._run_preview()
                elif step == "organize":
                    self.step_results[step] = self._run_organize()
                elif step == "verify":
                    self.step_results[step] = self._run_verify()
                elif step == "summary":
                    self.step_results[step] = self._run_summary()
                else:
                    print(f"❌ 未知步骤: {step}")
                    continue
                
                print(f"✅ 步骤 {step} 完成")
                
            except Exception as e:
                print(f"❌ 步骤 {step} 失败: {e}")
                return False
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🎉 工作流完成！总耗时: {duration:.2f} 秒")
        self._save_workflow_report(duration)
        return True
    
    def _run_backup(self) -> Dict:
        """运行备份步骤"""
        print("💾 创建文档备份...")
        
        # 导入备份工具
        try:
            from python_ecosystem_backup import PythonEcosystemBackup
            backup_tool = PythonEcosystemBackup()
            backup_path = backup_tool.create_backup()
            return {"status": "success", "backup_path": backup_path}
        except ImportError:
            print("⚠️ 备份工具不可用，跳过备份")
            return {"status": "skipped", "reason": "backup tool not available"}
    
    def _run_scan(self) -> Dict:
        """运行扫描步骤"""
        print("🔍 扫描Python相关文档...")
        
        try:
            from python_ecosystem_organizer import PythonEcosystemOrganizer
            organizer = PythonEcosystemOrganizer()
            scan_results = organizer.scan_existing_docs()
            return {"status": "success", "scan_results": scan_results}
        except ImportError:
            print("⚠️ 整理工具不可用，跳过扫描")
            return {"status": "skipped", "reason": "organizer tool not available"}
    
    def _run_preview(self) -> Dict:
        """运行预览步骤"""
        print("📋 预览整理计划...")
        
        try:
            from python_ecosystem_organizer import PythonEcosystemOrganizer
            organizer = PythonEcosystemOrganizer()
            scan_results = organizer.scan_existing_docs()
            # 简单预览扫描结果
            total_files = sum(len(files) for files in scan_results.values())
            print(f"📊 扫描到 {total_files} 个Python相关文档")
            for category, files in scan_results.items():
                print(f"  - {category}: {len(files)} 个文件")
            return {"status": "success", "total_files": total_files}
        except ImportError:
            print("⚠️ 整理工具不可用，跳过预览")
            return {"status": "skipped", "reason": "organizer tool not available"}
    
    def _run_organize(self) -> Dict:
        """运行整理步骤"""
        print("📁 整理文档...")
        
        try:
            from python_ecosystem_organizer import PythonEcosystemOrganizer
            organizer = PythonEcosystemOrganizer()
            scan_results = organizer.scan_existing_docs()
            organize_results = organizer.organize_documents(scan_results)
            return {"status": "success", "organize_results": organize_results}
        except ImportError:
            print("⚠️ 整理工具不可用，跳过整理")
            return {"status": "skipped", "reason": "organizer tool not available"}
    
    def _run_verify(self) -> Dict:
        """运行验证步骤"""
        print("🔍 验证整理结果...")
        
        try:
            from python_ecosystem_organizer import PythonEcosystemOrganizer
            organizer = PythonEcosystemOrganizer()
            # 简单验证：检查整理后的目录是否存在
            organized_dir = Path("python_ecosystem")
            if organized_dir.exists():
                categories = [d for d in organized_dir.iterdir() if d.is_dir()]
                verify_results = {
                    "status": "success",
                    "organized_dir_exists": True,
                    "category_count": len(categories),
                    "categories": [d.name for d in categories]
                }
            else:
                verify_results = {"status": "failed", "reason": "organized directory not found"}
            return {"status": "success", "verify_results": verify_results}
        except ImportError:
            print("⚠️ 整理工具不可用，跳过验证")
            return {"status": "skipped", "reason": "organizer tool not available"}
    
    def _run_summary(self) -> Dict:
        """运行总结步骤"""
        print("📊 生成整理总结...")
        
        try:
            from python_ecosystem_organizer import PythonEcosystemOrganizer
            organizer = PythonEcosystemOrganizer()
            scan_results = organizer.scan_existing_docs()
            organizer.generate_summary(scan_results)
            return {"status": "success"}
        except ImportError:
            print("⚠️ 整理工具不可用，跳过总结")
            return {"status": "skipped", "reason": "organizer tool not available"}
    
    def _save_workflow_report(self, duration: float):
        """保存工作流报告"""
        report = {
            "workflow_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": duration,
            "steps": self.step_results,
            "total_steps": len(self.workflow_steps),
            "successful_steps": len([s for s in self.step_results.values() if s.get("status") == "success"])
        }
        
        with open("python_ecosystem_workflow_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📋 工作流报告已保存: python_ecosystem_workflow_report.json")
    
    def show_help(self):
        """显示帮助信息"""
        print("""
🐍 Python语言生态文档整理工作流

用法:
  python python_ecosystem_workflow.py [步骤...]

可用步骤:
  backup    - 创建文档备份
  scan      - 扫描Python相关文档
  preview   - 预览整理计划
  organize  - 整理文档到分类目录
  verify    - 验证整理结果
  summary   - 生成整理总结

示例:
  python python_ecosystem_workflow.py                    # 运行完整工作流
  python python_ecosystem_workflow.py backup scan        # 只运行备份和扫描
  python python_ecosystem_workflow.py organize verify    # 只运行整理和验证

注意事项:
  - 建议先运行完整工作流
  - 备份步骤会创建时间戳备份
  - 整理步骤会创建新的目录结构
  - 所有步骤都会生成详细报告
        """)

def main():
    """主函数"""
    workflow = PythonEcosystemWorkflow()
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help", "help"]:
            workflow.show_help()
            return
        
        # 运行指定步骤
        steps = sys.argv[1:]
        workflow.run_workflow(steps)
    else:
        # 运行完整工作流
        workflow.run_workflow()

if __name__ == "__main__":
    main() 