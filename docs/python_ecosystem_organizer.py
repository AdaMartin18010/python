#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语言生态文档整理工具
专门用于整理和重组现有的Python语言相关文档
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any
import json

class PythonEcosystemOrganizer:
    """Python语言生态文档整理器"""
    
    def __init__(self):
        self.docs_dir = Path(".")
        self.organized_dir = Path("python_ecosystem")
        self.mapping_rules = {
            # Python基础语法
            "python_basic": {
                "keywords": ["语法", "基础", "变量", "数据类型", "控制流", "函数"],
                "target_dir": "01-基础语法",
                "files": []
            },
            # Python高级特性
            "python_advanced": {
                "keywords": ["高级", "特性", "装饰器", "生成器", "上下文", "元类"],
                "target_dir": "02-高级特性", 
                "files": []
            },
            # Python生态系统
            "python_ecosystem": {
                "keywords": ["生态", "包管理", "pip", "虚拟环境", "依赖"],
                "target_dir": "03-生态系统",
                "files": []
            },
            # Python版本特性
            "python_versions": {
                "keywords": ["版本", "3.8", "3.9", "3.10", "3.11", "3.12", "新特性"],
                "target_dir": "04-版本特性",
                "files": []
            },
            # Python性能优化
            "python_performance": {
                "keywords": ["性能", "优化", "内存", "并发", "异步"],
                "target_dir": "05-性能优化",
                "files": []
            },
            # Python安全编程
            "python_security": {
                "keywords": ["安全", "加密", "验证", "防护"],
                "target_dir": "06-安全编程",
                "files": []
            },
            # Python设计模式
            "python_patterns": {
                "keywords": ["设计模式", "模式", "架构"],
                "target_dir": "07-设计模式",
                "files": []
            },
            # Python Web开发
            "python_web": {
                "keywords": ["web", "flask", "django", "fastapi", "框架"],
                "target_dir": "08-Web开发",
                "files": []
            },
            # Python数据科学
            "python_data": {
                "keywords": ["数据", "科学", "numpy", "pandas", "matplotlib", "机器学习"],
                "target_dir": "09-数据科学",
                "files": []
            },
            # Python自动化运维
            "python_devops": {
                "keywords": ["运维", "自动化", "脚本", "部署", "监控"],
                "target_dir": "10-自动化运维",
                "files": []
            },
            # Python行业应用
            "python_industry": {
                "keywords": ["行业", "应用", "金融", "人工智能", "物联网", "区块链"],
                "target_dir": "11-行业应用",
                "files": []
            },
            # Python最佳实践
            "python_best_practices": {
                "keywords": ["最佳实践", "规范", "代码质量", "测试"],
                "target_dir": "12-最佳实践",
                "files": []
            }
        }
    
    def scan_existing_docs(self) -> Dict[str, List[str]]:
        """扫描现有的Python相关文档"""
        print("🔍 扫描现有Python语言生态文档...")
        
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
        
        print(f"✅ 找到 {sum(len(files) for files in python_docs.values())} 个Python相关文档")
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
    
    def create_organized_structure(self):
        """创建整理后的目录结构"""
        print("📁 创建Python语言生态文档结构...")
        
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
本目录包含Python语言生态中关于{category_names.get(category, category)}的相关文档。

## 文档列表
<!-- 文档将自动添加到这里 -->

## 学习资源
- [Python官方文档](https://docs.python.org/)
- [Python教程](https://docs.python.org/3/tutorial/)

## 相关链接
- [上一级](../README.md)
- [下一级](../README.md)
"""
    
    def organize_documents(self, python_docs: Dict[str, List[str]]):
        """整理文档到对应目录"""
        print("📋 开始整理文档...")
        
        for category, files in python_docs.items():
            if category in self.mapping_rules:
                target_dir = self.organized_dir / self.mapping_rules[category]["target_dir"]
                
                print(f"📁 整理 {category}: {len(files)} 个文件")
                
                for file_path in files:
                    source_path = Path(file_path)
                    if source_path.exists():
                        # 生成新的文件名
                        new_name = self._generate_new_filename(source_path, category)
                        target_path = target_dir / new_name
                        
                        # 复制文件
                        try:
                            import shutil
                            shutil.copy2(source_path, target_path)
                            print(f"  ✅ {source_path.name} -> {new_name}")
                        except Exception as e:
                            print(f"  ❌ 复制失败: {source_path.name} - {e}")
    
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
    
    def generate_summary(self, python_docs: Dict[str, List[str]]):
        """生成整理总结"""
        print("📊 生成整理总结...")
        
        summary = {
            "total_files": sum(len(files) for files in python_docs.values()),
            "categories": {},
            "organized_structure": str(self.organized_dir)
        }
        
        for category, files in python_docs.items():
            if category in self.mapping_rules:
                summary["categories"][self.mapping_rules[category]["target_dir"]] = {
                    "file_count": len(files),
                    "files": [Path(f).name for f in files]
                }
        
        # 保存总结报告
        with open("python_ecosystem_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # 生成主README
        main_readme = self._generate_main_readme(summary)
        with open(self.organized_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(main_readme)
        
        print(f"✅ 整理完成！共整理 {summary['total_files']} 个文档")
        print(f"📁 整理结果保存在: {self.organized_dir}")
    
    def _generate_main_readme(self, summary: Dict) -> str:
        """生成主README"""
        readme = """# Python语言生态文档体系

## 📋 概述
本目录包含完整的Python语言生态相关文档，按主题分类整理，便于学习和查阅。

## 📁 目录结构

"""
        
        for category_dir, info in summary["categories"].items():
            readme += f"### {category_dir}\n"
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

---
*本文档体系自动整理生成，持续更新中*
""".format(
            total_files=summary["total_files"],
            category_count=len(summary["categories"])
        )
        
        return readme
    
    def run(self):
        """运行完整的整理流程"""
        print("🐍 Python语言生态文档整理工具")
        print("=" * 50)
        
        # 1. 扫描现有文档
        python_docs = self.scan_existing_docs()
        
        if not python_docs:
            print("❌ 未找到Python相关文档")
            return
        
        # 2. 创建目录结构
        self.create_organized_structure()
        
        # 3. 整理文档
        self.organize_documents(python_docs)
        
        # 4. 生成总结
        self.generate_summary(python_docs)
        
        print("\n🎉 Python语言生态文档整理完成！")

def main():
    """主函数"""
    organizer = PythonEcosystemOrganizer()
    organizer.run()

if __name__ == "__main__":
    main() 