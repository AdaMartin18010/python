#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语言生态文档增强整理工具
包含备份、预览、验证、智能分类等功能
"""

import os
import re
import shutil
import datetime
from pathlib import Path
from typing import Dict, List, Any
import json
import colorama
from colorama import Fore, Back, Style

# 初始化colorama
colorama.init()

class EnhancedPythonEcosystemOrganizer:
    """增强版Python语言生态文档整理器"""
    
    def __init__(self):
        self.docs_dir = Path(".")
        self.organized_dir = Path("python_ecosystem")
        self.backup_dir = self.docs_dir / "backup"
        self.mapping_rules = {
            # Python基础语法
            "python_basic": {
                "keywords": ["语法", "基础", "变量", "数据类型", "控制流", "函数", "基本"],
                "target_dir": "01-基础语法",
                "description": "Python基础语法、变量、数据类型、控制结构等"
            },
            # Python高级特性
            "python_advanced": {
                "keywords": ["高级", "特性", "装饰器", "生成器", "上下文", "元类", "高级特性"],
                "target_dir": "02-高级特性",
                "description": "装饰器、生成器、上下文管理器、元类等高级特性"
            },
            # Python生态系统
            "python_ecosystem": {
                "keywords": ["生态", "包管理", "pip", "虚拟环境", "依赖", "包", "模块"],
                "target_dir": "03-生态系统",
                "description": "包管理、虚拟环境、依赖管理等生态系统"
            },
            # Python版本特性
            "python_versions": {
                "keywords": ["版本", "3.8", "3.9", "3.10", "3.11", "3.12", "新特性", "版本特性"],
                "target_dir": "04-版本特性",
                "description": "各版本新特性、版本差异等"
            },
            # Python性能优化
            "python_performance": {
                "keywords": ["性能", "优化", "内存", "并发", "异步", "性能优化"],
                "target_dir": "05-性能优化",
                "description": "性能优化技巧、内存管理、并发编程等"
            },
            # Python安全编程
            "python_security": {
                "keywords": ["安全", "加密", "验证", "防护", "安全编程"],
                "target_dir": "06-安全编程",
                "description": "安全编程实践、加密解密、输入验证等"
            },
            # Python设计模式
            "python_patterns": {
                "keywords": ["设计模式", "模式", "架构", "设计"],
                "target_dir": "07-设计模式",
                "description": "Python设计模式实现、架构设计等"
            },
            # Python Web开发
            "python_web": {
                "keywords": ["web", "flask", "django", "fastapi", "框架", "web开发"],
                "target_dir": "08-Web开发",
                "description": "Web框架、API开发、前后端等"
            },
            # Python数据科学
            "python_data": {
                "keywords": ["数据", "科学", "numpy", "pandas", "matplotlib", "机器学习", "数据科学"],
                "target_dir": "09-数据科学",
                "description": "数据分析、机器学习、科学计算等"
            },
            # Python自动化运维
            "python_devops": {
                "keywords": ["运维", "自动化", "脚本", "部署", "监控", "自动化运维"],
                "target_dir": "10-自动化运维",
                "description": "自动化脚本、部署运维、监控等"
            },
            # Python行业应用
            "python_industry": {
                "keywords": ["行业", "应用", "金融", "人工智能", "物联网", "区块链", "行业应用"],
                "target_dir": "11-行业应用",
                "description": "各行业Python应用案例"
            },
            # Python最佳实践
            "python_best_practices": {
                "keywords": ["最佳实践", "规范", "代码质量", "测试", "实践"],
                "target_dir": "12-最佳实践",
                "description": "编程规范、代码质量、测试策略等"
            }
        }
        self.scan_results = {}
        self.organization_plan = {}
    
    def create_backup(self):
        """创建备份"""
        print(f"{Fore.YELLOW}💾 创建备份...{Style.RESET_ALL}")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"python_ecosystem_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # 备份重要目录
        important_dirs = ["refactor", "model"]
        for dir_name in important_dirs:
            src_dir = self.docs_dir / dir_name
            if src_dir.exists():
                dst_dir = backup_path / dir_name
                try:
                    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
                    print(f"{Fore.GREEN}✅ 已备份: {dir_name}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ 备份失败: {dir_name} - {e}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ 备份完成: {backup_path}{Style.RESET_ALL}")
        return str(backup_path)
    
    def scan_existing_docs(self) -> Dict[str, List[str]]:
        """扫描现有的Python相关文档"""
        print(f"{Fore.YELLOW}🔍 扫描现有Python语言生态文档...{Style.RESET_ALL}")
        
        python_docs = {}
        
        # 扫描refactor目录
        refactor_dir = self.docs_dir / "refactor"
        if refactor_dir.exists():
            for file_path in refactor_dir.rglob("*.md"):
                if self._is_python_related(file_path):
                    content = self._read_file_content(file_path)
                    category = self._categorize_content(content, str(file_path))
                    if category:
                        if category not in python_docs:
                            python_docs[category] = []
                        python_docs[category].append(str(file_path))
        
        # 扫描model目录
        model_dir = self.docs_dir / "model"
        if model_dir.exists():
            for file_path in model_dir.rglob("*.md"):
                if self._is_python_related(file_path):
                    content = self._read_file_content(file_path)
                    category = self._categorize_content(content, str(file_path))
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
        # 检查文件名
        filename = file_path.name.lower()
        if "python" in filename or "py" in filename:
            return True
        
        # 检查文件内容
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            python_keywords = ["python", "def ", "class ", "import ", "from ", "pip", "django", "flask"]
            return any(keyword in content.lower() for keyword in python_keywords)
        except:
            return False
    
    def _read_file_content(self, file_path: Path) -> str:
        """读取文件内容"""
        try:
            return file_path.read_text(encoding='utf-8', errors='ignore')
        except:
            return ""
    
    def _categorize_content(self, content: str, file_path: str) -> str:
        """根据内容分类文档"""
        content_lower = content.lower()
        file_lower = file_path.lower()
        
        # 根据关键词匹配分类
        for category, config in self.mapping_rules.items():
            for keyword in config["keywords"]:
                if keyword in content_lower or keyword in file_lower:
                    return category
        
        # 如果没有明确匹配，根据文件路径推断
        if "基础" in file_path or "basic" in file_path:
            return "python_basic"
        elif "高级" in file_path or "advanced" in file_path:
            return "python_advanced"
        elif "生态" in file_path or "ecosystem" in file_path:
            return "python_ecosystem"
        elif "版本" in file_path or "version" in file_path:
            return "python_versions"
        elif "性能" in file_path or "performance" in file_path:
            return "python_performance"
        elif "安全" in file_path or "security" in file_path:
            return "python_security"
        elif "模式" in file_path or "pattern" in file_path:
            return "python_patterns"
        elif "web" in file_path or "框架" in file_path:
            return "python_web"
        elif "数据" in file_path or "data" in file_path:
            return "python_data"
        elif "运维" in file_path or "devops" in file_path:
            return "python_devops"
        elif "行业" in file_path or "industry" in file_path:
            return "python_industry"
        elif "实践" in file_path or "practice" in file_path:
            return "python_best_practices"
        
        return "python_basic"  # 默认分类
    
    def preview_organization(self):
        """预览整理计划"""
        print(f"{Fore.CYAN}📋 整理计划预览{Style.RESET_ALL}")
        print("=" * 60)
        
        for category, files in self.scan_results.items():
            if category in self.mapping_rules:
                config = self.mapping_rules[category]
                print(f"\n{Fore.BLUE}📁 {config['target_dir']}{Style.RESET_ALL}")
                print(f"   描述: {config['description']}")
                print(f"   文档数: {len(files)} 个")
                print(f"   文档列表:")
                for file_path in files[:5]:  # 只显示前5个
                    print(f"     - {Path(file_path).name}")
                if len(files) > 5:
                    print(f"     ... 还有 {len(files) - 5} 个文档")
        
        total_files = sum(len(files) for files in self.scan_results.values())
        print(f"\n{Fore.GREEN}📊 总计: {total_files} 个文档将被整理{Style.RESET_ALL}")
    
    def create_organized_structure(self):
        """创建整理后的目录结构"""
        print(f"{Fore.YELLOW}📁 创建Python语言生态文档结构...{Style.RESET_ALL}")
        
        # 创建主目录
        self.organized_dir.mkdir(exist_ok=True)
        
        # 创建分类目录
        for category, config in self.mapping_rules.items():
            target_dir = self.organized_dir / config["target_dir"]
            target_dir.mkdir(exist_ok=True)
            
            # 创建README
            readme_content = self._generate_category_readme(category, config)
            with open(target_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)
    
    def _generate_category_readme(self, category: str, config: Dict) -> str:
        """生成分类README内容"""
        category_names = {
            "python_basic": "Python基础语法",
            "python_advanced": "Python高级特性", 
            "python_ecosystem": "Python生态系统",
            "python_versions": "Python版本特性",
            "python_performance": "Python性能优化",
            "python_security": "Python安全编程",
            "python_patterns": "Python设计模式",
            "python_web": "Python Web开发",
            "python_data": "Python数据科学",
            "python_devops": "Python自动化运维",
            "python_industry": "Python行业应用",
            "python_best_practices": "Python最佳实践"
        }
        
        return f"""# {category_names.get(category, category)}

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
            if category in self.mapping_rules:
                target_dir = self.organized_dir / self.mapping_rules[category]["target_dir"]
                organized_files[category] = []
                
                print(f"\n{Fore.BLUE}📁 整理 {self.mapping_rules[category]['target_dir']}: {len(files)} 个文件{Style.RESET_ALL}")
                
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
        
        self.organization_plan = organized_files
        return organized_files
    
    def _generate_new_filename(self, file_path: Path, category: str) -> str:
        """生成新的文件名"""
        original_name = file_path.stem
        extension = file_path.suffix
        
        # 根据分类添加前缀
        category_prefixes = {
            "python_basic": "01-",
            "python_advanced": "02-",
            "python_ecosystem": "03-",
            "python_versions": "04-",
            "python_performance": "05-",
            "python_security": "06-",
            "python_patterns": "07-",
            "python_web": "08-",
            "python_data": "09-",
            "python_devops": "10-",
            "python_industry": "11-",
            "python_best_practices": "12-"
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
        
        for category, config in self.mapping_rules.items():
            target_dir = self.organized_dir / config["target_dir"]
            if target_dir.exists():
                verification_results["total_categories"] += 1
                
                # 检查文件数量
                files = list(target_dir.glob("*.md"))
                verification_results["total_files"] += len(files)
                
                # 检查README
                readme_file = target_dir / "README.md"
                if not readme_file.exists():
                    verification_results["structure_issues"].append(f"缺少README: {config['target_dir']}")
                
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
    
    def generate_summary(self):
        """生成整理总结"""
        print(f"{Fore.YELLOW}📊 生成整理总结...{Style.RESET_ALL}")
        
        summary = {
            "organization_time": datetime.datetime.now().isoformat(),
            "total_files": sum(len(files) for files in self.scan_results.values()),
            "categories": {},
            "organized_structure": str(self.organized_dir),
            "backup_created": True
        }
        
        for category, files in self.scan_results.items():
            if category in self.mapping_rules:
                summary["categories"][self.mapping_rules[category]["target_dir"]] = {
                    "file_count": len(files),
                    "files": [Path(f).name for f in files],
                    "description": self.mapping_rules[category]["description"]
                }
        
        # 保存总结报告
        with open("python_ecosystem_organization_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # 生成主README
        main_readme = self._generate_main_readme(summary)
        with open(self.organized_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(main_readme)
        
        print(f"{Fore.GREEN}✅ 整理完成！共整理 {summary['total_files']} 个文档{Style.RESET_ALL}")
        print(f"📁 整理结果保存在: {self.organized_dir}")
        print(f"📋 总结报告: python_ecosystem_organization_summary.json")
    
    def _generate_main_readme(self, summary: Dict) -> str:
        """生成主README"""
        readme = """# Python语言生态文档体系

## 📋 概述
本目录包含完整的Python语言生态相关文档，按主题分类整理，便于学习和查阅。

## 📁 目录结构

"""
        
        for category_dir, info in summary["categories"].items():
            readme += f"### {category_dir}\n"
            readme += f"- 描述: {info['description']}\n"
            readme += f"- 文档数量: {info['file_count']} 个\n"
            readme += f"- 主要文档: {', '.join(info['files'][:3])}\n"
            readme += f"- [查看详情]({category_dir}/README.md)\n\n"
        
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
            total_files=summary["total_files"],
            category_count=len(summary["categories"]),
            organization_time=summary["organization_time"],
            backup_status="已创建" if summary.get("backup_created") else "未创建"
        )
        
        return readme
    
    def run(self):
        """运行完整的整理流程"""
        print(f"{Fore.CYAN}🐍 Python语言生态文档增强整理工具{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # 1. 创建备份
        self.create_backup()
        
        # 2. 扫描现有文档
        self.scan_existing_docs()
        
        if not self.scan_results:
            print(f"{Fore.RED}❌ 未找到Python相关文档{Style.RESET_ALL}")
            return
        
        # 3. 预览整理计划
        self.preview_organization()
        
        # 4. 创建目录结构
        self.create_organized_structure()
        
        # 5. 整理文档
        self.organize_documents()
        
        # 6. 验证整理结果
        self.verify_organization()
        
        # 7. 生成总结
        self.generate_summary()
        
        print(f"\n{Fore.GREEN}🎉 Python语言生态文档整理完成！{Style.RESET_ALL}")

def main():
    """主函数"""
    organizer = EnhancedPythonEcosystemOrganizer()
    organizer.run()

if __name__ == "__main__":
    main() 