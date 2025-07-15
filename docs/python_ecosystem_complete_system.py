#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语言生态文档完整整理系统
整合备份、扫描、整理、验证、报告等所有功能
"""

import os
import sys
import time
import shutil
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import colorama
from colorama import Fore, Back, Style

# 初始化colorama
colorama.init()

class PythonEcosystemCompleteSystem:
    """Python语言生态文档完整整理系统"""
    
    def __init__(self):
        self.docs_dir = Path(".")
        self.backup_dir = self.docs_dir / "backup"
        self.organized_dir = Path("python_ecosystem")
        self.reports_dir = Path("reports")
        
        # 分类规则
        self.categories = {
            "01-基础语法": {
                "keywords": ["语法", "基础", "变量", "数据类型", "控制流", "函数", "基本"],
                "description": "Python基础语法、变量、数据类型、控制结构等"
            },
            "02-高级特性": {
                "keywords": ["高级", "特性", "装饰器", "生成器", "上下文", "元类", "高级特性"],
                "description": "装饰器、生成器、上下文管理器、元类等高级特性"
            },
            "03-生态系统": {
                "keywords": ["生态", "包管理", "pip", "虚拟环境", "依赖", "包", "模块"],
                "description": "包管理、虚拟环境、依赖管理等生态系统"
            },
            "04-版本特性": {
                "keywords": ["版本", "3.8", "3.9", "3.10", "3.11", "3.12", "新特性", "版本特性"],
                "description": "各版本新特性、版本差异等"
            },
            "05-性能优化": {
                "keywords": ["性能", "优化", "内存", "并发", "异步", "性能优化"],
                "description": "性能优化技巧、内存管理、并发编程等"
            },
            "06-安全编程": {
                "keywords": ["安全", "加密", "验证", "防护", "安全编程"],
                "description": "安全编程实践、加密解密、输入验证等"
            },
            "07-设计模式": {
                "keywords": ["设计模式", "模式", "架构", "设计"],
                "description": "Python设计模式实现、架构设计等"
            },
            "08-Web开发": {
                "keywords": ["web", "flask", "django", "fastapi", "框架", "web开发"],
                "description": "Web框架、API开发、前后端等"
            },
            "09-数据科学": {
                "keywords": ["数据", "科学", "numpy", "pandas", "matplotlib", "机器学习", "数据科学"],
                "description": "数据分析、机器学习、科学计算等"
            },
            "10-自动化运维": {
                "keywords": ["运维", "自动化", "脚本", "部署", "监控", "自动化运维"],
                "description": "自动化脚本、部署运维、监控等"
            },
            "11-行业应用": {
                "keywords": ["行业", "应用", "金融", "人工智能", "物联网", "区块链", "行业应用"],
                "description": "各行业Python应用案例"
            },
            "12-最佳实践": {
                "keywords": ["最佳实践", "规范", "代码质量", "测试", "实践"],
                "description": "编程规范、代码质量、测试策略等"
            }
        }
        
        self.scan_results = {}
        self.organization_results = {}
        self.system_status = {}
    
    def create_backup(self) -> str:
        """创建备份"""
        print(f"{Fore.YELLOW}💾 创建文档备份...{Style.RESET_ALL}")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"python_ecosystem_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # 备份重要目录
        important_dirs = ["refactor", "model"]
        backed_up_dirs = []
        
        for dir_name in important_dirs:
            src_dir = self.docs_dir / dir_name
            if src_dir.exists():
                dst_dir = backup_path / dir_name
                try:
                    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
                    print(f"{Fore.GREEN}✅ 已备份: {dir_name}{Style.RESET_ALL}")
                    backed_up_dirs.append(dir_name)
                except Exception as e:
                    print(f"{Fore.RED}❌ 备份失败: {dir_name} - {e}{Style.RESET_ALL}")
        
        # 备份Python相关文件
        python_files = []
        for file_path in self.docs_dir.rglob("*.py"):
            if "python" in file_path.name.lower():
                try:
                    dst_file = backup_path / file_path.name
                    shutil.copy2(file_path, dst_file)
                    python_files.append(file_path.name)
                except Exception as e:
                    print(f"{Fore.RED}❌ 备份失败: {file_path.name} - {e}{Style.RESET_ALL}")
        
        if python_files:
            print(f"{Fore.GREEN}✅ 已备份Python文件: {', '.join(python_files)}{Style.RESET_ALL}")
        
        # 生成备份报告
        backup_report = {
            "backup_time": datetime.datetime.now().isoformat(),
            "backup_name": backup_name,
            "backup_path": str(backup_path),
            "backed_up_dirs": backed_up_dirs,
            "backed_up_files": python_files,
            "total_size": self._get_dir_size(backup_path)
        }
        
        report_file = backup_path / "backup_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(backup_report, f, ensure_ascii=False, indent=2)
        
        print(f"{Fore.GREEN}✅ 备份完成: {backup_path}{Style.RESET_ALL}")
        return str(backup_path)
    
    def _get_dir_size(self, path: Path) -> int:
        """获取目录大小"""
        total_size = 0
        for file_path in path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
    
    def scan_documents(self) -> Dict[str, List[str]]:
        """扫描Python相关文档"""
        print(f"{Fore.YELLOW}🔍 扫描Python语言生态文档...{Style.RESET_ALL}")
        
        python_docs = {}
        
        # 扫描refactor目录
        refactor_dir = self.docs_dir / "refactor"
        if refactor_dir.exists():
            for file_path in refactor_dir.rglob("*.md"):
                if self._is_python_related(file_path):
                    category = self._categorize_document(file_path)
                    if category:
                        if category not in python_docs:
                            python_docs[category] = []
                        python_docs[category].append(str(file_path))
        
        # 扫描model目录
        model_dir = self.docs_dir / "model"
        if model_dir.exists():
            for file_path in model_dir.rglob("*.md"):
                if self._is_python_related(file_path):
                    category = self._categorize_document(file_path)
                    if category:
                        if category not in python_docs:
                            python_docs[category] = []
                        python_docs[category].append(str(file_path))
        
        self.scan_results = python_docs
        total_files = sum(len(files) for files in python_docs.values())
        print(f"{Fore.GREEN}✅ 找到 {total_files} 个Python相关文档{Style.RESET_ALL}")
        return python_docs
    
    def _is_python_related(self, file_path: Path) -> bool:
        """判断文件是否与Python相关"""
        filename = file_path.name.lower()
        if "python" in filename or "py" in filename:
            return True
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            python_keywords = ["python", "def ", "class ", "import ", "from ", "pip", "django", "flask"]
            return any(keyword in content.lower() for keyword in python_keywords)
        except:
            return False
    
    def _categorize_document(self, file_path: Path) -> str:
        """分类文档"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            content_lower = content.lower()
            file_lower = str(file_path).lower()
            
            # 根据关键词匹配分类
            for category, config in self.categories.items():
                for keyword in config["keywords"]:
                    if keyword in content_lower or keyword in file_lower:
                        return category
            
            # 根据文件路径推断
            if "基础" in str(file_path) or "basic" in str(file_path):
                return "01-基础语法"
            elif "高级" in str(file_path) or "advanced" in str(file_path):
                return "02-高级特性"
            elif "生态" in str(file_path) or "ecosystem" in str(file_path):
                return "03-生态系统"
            elif "版本" in str(file_path) or "version" in str(file_path):
                return "04-版本特性"
            elif "性能" in str(file_path) or "performance" in str(file_path):
                return "05-性能优化"
            elif "安全" in str(file_path) or "security" in str(file_path):
                return "06-安全编程"
            elif "模式" in str(file_path) or "pattern" in str(file_path):
                return "07-设计模式"
            elif "web" in str(file_path) or "框架" in str(file_path):
                return "08-Web开发"
            elif "数据" in str(file_path) or "data" in str(file_path):
                return "09-数据科学"
            elif "运维" in str(file_path) or "devops" in str(file_path):
                return "10-自动化运维"
            elif "行业" in str(file_path) or "industry" in str(file_path):
                return "11-行业应用"
            elif "实践" in str(file_path) or "practice" in str(file_path):
                return "12-最佳实践"
            
            return "01-基础语法"  # 默认分类
        except:
            return "01-基础语法"
    
    def create_organized_structure(self):
        """创建整理后的目录结构"""
        print(f"{Fore.YELLOW}📁 创建Python语言生态文档结构...{Style.RESET_ALL}")
        
        # 创建主目录
        self.organized_dir.mkdir(exist_ok=True)
        
        # 创建分类目录
        for category in self.categories.keys():
            target_dir = self.organized_dir / category
            target_dir.mkdir(exist_ok=True)
            
            # 创建README
            readme_content = self._generate_category_readme(category)
            with open(target_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)
        
        print(f"{Fore.GREEN}✅ 目录结构创建完成{Style.RESET_ALL}")
    
    def _generate_category_readme(self, category: str) -> str:
        """生成分类README内容"""
        config = self.categories[category]
        
        return f"""# {category}

## 简介
{config['description']}

## 文档列表
<!-- 文档将自动添加到这里 -->

## 学习资源
- [Python官方文档](https://docs.python.org/)
- [Python教程](https://docs.python.org/3/tutorial/)

## 相关链接
- [返回上级](../README.md)
"""
    
    def organize_documents(self):
        """整理文档到对应目录"""
        print(f"{Fore.YELLOW}📋 开始整理文档...{Style.RESET_ALL}")
        
        organized_files = {}
        
        for category, files in self.scan_results.items():
            if category in self.categories:
                target_dir = self.organized_dir / category
                organized_files[category] = []
                
                print(f"\n{Fore.BLUE}📁 整理 {category}: {len(files)} 个文件{Style.RESET_ALL}")
                
                for file_path in files:
                    source_path = Path(file_path)
                    if source_path.exists():
                        # 生成新的文件名
                        new_name = self._generate_new_filename(source_path, category)
                        target_path = target_dir / new_name
                        
                        # 复制文件
                        try:
                            shutil.copy2(source_path, target_path)
                            organized_files[category].append(new_name)
                            print(f"  {Fore.GREEN}✅ {source_path.name} -> {new_name}{Style.RESET_ALL}")
                        except Exception as e:
                            print(f"  {Fore.RED}❌ 复制失败: {source_path.name} - {e}{Style.RESET_ALL}")
        
        self.organization_results = organized_files
        return organized_files
    
    def _generate_new_filename(self, file_path: Path, category: str) -> str:
        """生成新的文件名"""
        original_name = file_path.stem
        extension = file_path.suffix
        
        # 根据分类添加前缀
        category_prefixes = {
            "01-基础语法": "01-",
            "02-高级特性": "02-",
            "03-生态系统": "03-",
            "04-版本特性": "04-",
            "05-性能优化": "05-",
            "06-安全编程": "06-",
            "07-设计模式": "07-",
            "08-Web开发": "08-",
            "09-数据科学": "09-",
            "10-自动化运维": "10-",
            "11-行业应用": "11-",
            "12-最佳实践": "12-"
        }
        
        prefix = category_prefixes.get(category, "")
        return f"{prefix}{original_name}{extension}"
    
    def verify_organization(self):
        """验证整理结果"""
        print(f"{Fore.YELLOW}🔍 验证整理结果...{Style.RESET_ALL}")
        
        verification_results = {
            "total_categories": 0,
            "total_files": 0,
            "missing_files": [],
            "duplicate_files": [],
            "structure_issues": []
        }
        
        for category in self.categories.keys():
            target_dir = self.organized_dir / category
            if target_dir.exists():
                verification_results["total_categories"] += 1
                
                # 检查文件数量
                files = list(target_dir.glob("*.md"))
                verification_results["total_files"] += len(files)
                
                # 检查README
                readme_file = target_dir / "README.md"
                if not readme_file.exists():
                    verification_results["structure_issues"].append(f"缺少README: {category}")
                
                # 检查重复文件
                file_names = [f.name for f in files]
                duplicates = [name for name in file_names if file_names.count(name) > 1]
                if duplicates:
                    verification_results["duplicate_files"].extend(duplicates)
        
        # 输出验证结果
        print(f"{Fore.GREEN}✅ 验证完成{Style.RESET_ALL}")
        print(f"  分类数: {verification_results['total_categories']}")
        print(f"  文件数: {verification_results['total_files']}")
        
        if verification_results["structure_issues"]:
            print(f"{Fore.RED}⚠️ 结构问题: {verification_results['structure_issues']}{Style.RESET_ALL}")
        
        if verification_results["duplicate_files"]:
            print(f"{Fore.YELLOW}⚠️ 重复文件: {verification_results['duplicate_files']}{Style.RESET_ALL}")
        
        return verification_results
    
    def generate_reports(self):
        """生成整理报告"""
        print(f"{Fore.YELLOW}📊 生成整理报告...{Style.RESET_ALL}")
        
        # 创建报告目录
        self.reports_dir.mkdir(exist_ok=True)
        
        # 生成主报告
        main_report = {
            "organization_time": datetime.datetime.now().isoformat(),
            "total_files": sum(len(files) for files in self.scan_results.values()),
            "categories": {},
            "organized_structure": str(self.organized_dir),
            "backup_created": True
        }
        
        for category, files in self.scan_results.items():
            if category in self.categories:
                main_report["categories"][category] = {
                    "file_count": len(files),
                    "files": [Path(f).name for f in files],
                    "description": self.categories[category]["description"]
                }
        
        # 保存主报告
        with open(self.reports_dir / "python_ecosystem_organization_report.json", 'w', encoding='utf-8') as f:
            json.dump(main_report, f, ensure_ascii=False, indent=2)
        
        # 生成主README
        main_readme = self._generate_main_readme(main_report)
        with open(self.organized_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(main_readme)
        
        # 生成系统状态报告
        system_status = {
            "system_time": datetime.datetime.now().isoformat(),
            "scan_results": self.scan_results,
            "organization_results": self.organization_results,
            "system_status": self.system_status
        }
        
        with open(self.reports_dir / "python_ecosystem_system_status.json", 'w', encoding='utf-8') as f:
            json.dump(system_status, f, ensure_ascii=False, indent=2)
        
        print(f"{Fore.GREEN}✅ 报告生成完成{Style.RESET_ALL}")
        print(f"📁 报告保存在: {self.reports_dir}")
        print(f"📋 主报告: python_ecosystem_organization_report.json")
        print(f"📊 系统状态: python_ecosystem_system_status.json")
    
    def _generate_main_readme(self, report: Dict) -> str:
        """生成主README"""
        readme = """# Python语言生态文档体系

## 📋 概述
本目录包含完整的Python语言生态相关文档，按主题分类整理，便于学习和查阅。

## 📁 目录结构

"""
        
        for category, info in report["categories"].items():
            readme += f"### {category}\n"
            readme += f"- 描述: {info['description']}\n"
            readme += f"- 文档数量: {info['file_count']} 个\n"
            readme += f"- 主要文档: {', '.join(info['files'][:3])}\n"
            readme += f"- [查看详情]({category}/README.md)\n\n"
        
        readme += """## 🚀 快速开始
1. 选择感兴趣的主题目录
2. 查看该目录下的README了解内容
3. 阅读相关文档深入学习

## 📊 统计信息
- 总文档数: {total_files} 个
- 分类数: {category_count} 个
- 覆盖主题: Python基础到高级应用

## 🔗 相关链接
- [Python官方文档](https://docs.python.org/)
- [Python包索引](https://pypi.org/)
- [Python社区](https://www.python.org/community/)

## 📝 整理信息
- 整理时间: {organization_time}
- 备份状态: {backup_status}

---
*本文档体系自动整理生成，持续更新中*
""".format(
            total_files=report["total_files"],
            category_count=len(report["categories"]),
            organization_time=report["organization_time"],
            backup_status="已创建" if report.get("backup_created") else "未创建"
        )
        
        return readme
    
    def run_complete_system(self):
        """运行完整系统"""
        print(f"{Fore.CYAN}🐍 Python语言生态文档完整整理系统{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        start_time = time.time()
        
        try:
            # 1. 创建备份
            backup_path = self.create_backup()
            self.system_status["backup"] = {"status": "success", "path": backup_path}
            
            # 2. 扫描文档
            scan_results = self.scan_documents()
            self.system_status["scan"] = {"status": "success", "total_files": sum(len(files) for files in scan_results.values())}
            
            if not scan_results:
                print(f"{Fore.RED}❌ 未找到Python相关文档{Style.RESET_ALL}")
                return False
            
            # 3. 创建目录结构
            self.create_organized_structure()
            self.system_status["structure"] = {"status": "success"}
            
            # 4. 整理文档
            organize_results = self.organize_documents()
            self.system_status["organization"] = {"status": "success", "results": organize_results}
            
            # 5. 验证结果
            verify_results = self.verify_organization()
            self.system_status["verification"] = {"status": "success", "results": verify_results}
            
            # 6. 生成报告
            self.generate_reports()
            self.system_status["reports"] = {"status": "success"}
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n{Fore.GREEN}🎉 Python语言生态文档整理完成！{Style.RESET_ALL}")
            print(f"⏱️ 总耗时: {duration:.2f} 秒")
            print(f"📁 整理结果: {self.organized_dir}")
            print(f"📋 报告位置: {self.reports_dir}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ 系统运行失败: {e}{Style.RESET_ALL}")
            return False

def main():
    """主函数"""
    system = PythonEcosystemCompleteSystem()
    system.run_complete_system()

if __name__ == "__main__":
    main() 