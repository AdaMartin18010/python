#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语言生态文档备份工具
在整理前自动备份现有文档，确保数据安全
"""

import os
import shutil
import datetime
from pathlib import Path
import json

class PythonEcosystemBackup:
    """Python语言生态文档备份器"""
    
    def __init__(self):
        self.docs_dir = Path(".")
        self.backup_dir = self.docs_dir / "backup"
        self.backup_name = None
        
    def create_backup(self) -> str:
        """创建备份"""
        print("💾 创建Python语言生态文档备份...")
        
        # 生成备份名称
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_name = f"python_ecosystem_backup_{timestamp}"
        backup_path = self.backup_dir / self.backup_name
        
        # 创建备份目录
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # 备份重要目录
        important_dirs = ["refactor", "model"]
        backed_up_files = []
        
        for dir_name in important_dirs:
            src_dir = self.docs_dir / dir_name
            if src_dir.exists():
                dst_dir = backup_path / dir_name
                try:
                    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
                    print(f"✅ 已备份: {dir_name}")
                    backed_up_files.append(dir_name)
                except Exception as e:
                    print(f"❌ 备份失败: {dir_name} - {e}")
        
        # 备份Python相关文件
        python_files = []
        for file_path in self.docs_dir.rglob("*.py"):
            if "python" in file_path.name.lower():
                try:
                    dst_file = backup_path / file_path.name
                    shutil.copy2(file_path, dst_file)
                    python_files.append(file_path.name)
                except Exception as e:
                    print(f"❌ 备份失败: {file_path.name} - {e}")
        
        if python_files:
            print(f"✅ 已备份Python文件: {', '.join(python_files)}")
        
        # 生成备份报告
        backup_report = {
            "backup_time": datetime.datetime.now().isoformat(),
            "backup_name": self.backup_name,
            "backup_path": str(backup_path),
            "backed_up_dirs": backed_up_files,
            "backed_up_files": python_files,
            "total_size": self._get_dir_size(backup_path)
        }
        
        # 保存备份报告
        report_file = backup_path / "backup_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(backup_report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 备份完成: {backup_path}")
        print(f"📊 备份大小: {backup_report['total_size']} bytes")
        
        return str(backup_path)
    
    def _get_dir_size(self, path: Path) -> int:
        """获取目录大小"""
        total_size = 0
        for file_path in path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
    
    def list_backups(self):
        """列出所有备份"""
        if not self.backup_dir.exists():
            print("❌ 备份目录不存在")
            return
        
        backups = []
        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir() and backup_dir.name.startswith("python_ecosystem_backup_"):
                report_file = backup_dir / "backup_report.json"
                if report_file.exists():
                    try:
                        with open(report_file, 'r', encoding='utf-8') as f:
                            report = json.load(f)
                        backups.append(report)
                    except:
                        pass
        
        if not backups:
            print("❌ 未找到备份")
            return
        
        print("📋 现有备份列表:")
        for backup in sorted(backups, key=lambda x: x['backup_time'], reverse=True):
            print(f"  📁 {backup['backup_name']}")
            print(f"    时间: {backup['backup_time']}")
            print(f"    大小: {backup['total_size']} bytes")
            print(f"    目录: {', '.join(backup['backed_up_dirs'])}")
            print()
    
    def restore_backup(self, backup_name: str):
        """恢复备份"""
        backup_path = self.backup_dir / backup_name
        if not backup_path.exists():
            print(f"❌ 备份不存在: {backup_name}")
            return False
        
        print(f"🔄 恢复备份: {backup_name}")
        
        # 恢复目录
        for dir_name in ["refactor", "model"]:
            src_dir = backup_path / dir_name
            dst_dir = self.docs_dir / dir_name
            
            if src_dir.exists():
                try:
                    if dst_dir.exists():
                        shutil.rmtree(dst_dir)
                    shutil.copytree(src_dir, dst_dir)
                    print(f"✅ 已恢复: {dir_name}")
                except Exception as e:
                    print(f"❌ 恢复失败: {dir_name} - {e}")
        
        # 恢复Python文件
        for file_path in backup_path.glob("*.py"):
            try:
                dst_file = self.docs_dir / file_path.name
                shutil.copy2(file_path, dst_file)
                print(f"✅ 已恢复: {file_path.name}")
            except Exception as e:
                print(f"❌ 恢复失败: {file_path.name} - {e}")
        
        print("✅ 备份恢复完成")
        return True

def main():
    """主函数"""
    backup_tool = PythonEcosystemBackup()
    
    print("🐍 Python语言生态文档备份工具")
    print("=" * 50)
    
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "backup":
            backup_tool.create_backup()
        elif command == "list":
            backup_tool.list_backups()
        elif command == "restore" and len(sys.argv) > 2:
            backup_tool.restore_backup(sys.argv[2])
        else:
            print("用法:")
            print("  python python_ecosystem_backup.py backup  # 创建备份")
            print("  python python_ecosystem_backup.py list     # 列出备份")
            print("  python python_ecosystem_backup.py restore <backup_name>  # 恢复备份")
    else:
        # 默认创建备份
        backup_tool.create_backup()

if __name__ == "__main__":
    main() 