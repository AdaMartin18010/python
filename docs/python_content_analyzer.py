#!/usr/bin/env python3
"""
Python内容分析工具

用于分析现有文档中与Python相关的内容，并生成迁移建议。
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PythonContentAnalyzer:
    """Python内容分析器"""
    
    def __init__(self, base_path: str = "docs"):
        self.base_path = Path(base_path)
        
        # Python相关关键词
        self.python_keywords = {
            'python', 'py', 'pip', 'poetry', 'uv', 'conda', 'virtualenv',
            'django', 'flask', 'fastapi', 'tornado', 'sqlalchemy',
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn',
            'tensorflow', 'pytorch', 'keras', 'jupyter', 'ipython',
            'pytest', 'unittest', 'nose', 'coverage', 'black', 'flake8',
            'mypy', 'pylint', 'sphinx', 'docstring', 'pep8', 'pep',
            'async', 'await', 'asyncio', 'threading', 'multiprocessing',
            'decorator', 'generator', 'iterator', 'contextmanager',
            'metaclass', 'descriptor', 'property', 'slots', 'dataclass',
            'type_hint', 'typing', 'mypy', 'pydantic', 'marshmallow',
            'celery', 'redis', 'postgresql', 'mysql', 'sqlite',
            'docker', 'kubernetes', 'ansible', 'salt', 'jenkins',
            'git', 'github', 'gitlab', 'bitbucket', 'travis', 'circleci'
        }
        
        # 文件类型映射
        self.file_type_mapping = {
            'python': ['.py', '.pyx', '.pyi'],
            'markdown': ['.md', '.markdown'],
            'documentation': ['.rst', '.txt', '.adoc'],
            'config': ['.toml', '.yaml', '.yml', '.json', '.ini', '.cfg'],
            'other': ['.sh', '.bat', '.ps1', '.js', '.html', '.css']
        }
        
        # 内容分类规则
        self.content_categories = {
            'core_python': {
                'keywords': ['python', 'py', 'syntax', 'grammar', 'language'],
                'patterns': [r'python\s+[0-9]+\.[0-9]+', r'pep\s+[0-9]+']
            },
            'ecosystem': {
                'keywords': ['pip', 'poetry', 'uv', 'conda', 'virtualenv', 'requirements'],
                'patterns': [r'pip\s+install', r'poetry\s+add', r'uv\s+pip']
            },
            'web_frameworks': {
                'keywords': ['django', 'flask', 'fastapi', 'tornado', 'bottle'],
                'patterns': [r'from\s+django', r'from\s+flask', r'from\s+fastapi']
            },
            'data_science': {
                'keywords': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn'],
                'patterns': [r'import\s+pandas', r'import\s+numpy', r'import\s+sklearn']
            },
            'machine_learning': {
                'keywords': ['tensorflow', 'pytorch', 'keras', 'scikit-learn', 'xgboost'],
                'patterns': [r'import\s+tensorflow', r'import\s+torch', r'import\s+keras']
            },
            'testing': {
                'keywords': ['pytest', 'unittest', 'nose', 'coverage', 'mock'],
                'patterns': [r'import\s+pytest', r'import\s+unittest', r'def\s+test_']
            },
            'devops': {
                'keywords': ['docker', 'kubernetes', 'ansible', 'jenkins', 'git'],
                'patterns': [r'docker\s+run', r'kubectl', r'ansible-playbook']
            },
            'security': {
                'keywords': ['security', 'cryptography', 'hashlib', 'ssl', 'tls'],
                'patterns': [r'import\s+cryptography', r'import\s+hashlib', r'import\s+ssl']
            },
            'performance': {
                'keywords': ['performance', 'profiling', 'cprofile', 'memory', 'optimization'],
                'patterns': [r'import\s+cProfile', r'import\s+memory_profiler']
            }
        }

    def analyze_directory(self) -> Dict:
        """分析整个目录结构"""
        logger.info("开始分析目录结构...")
        
        analysis_result = {
            'total_files': 0,
            'python_files': 0,
            'markdown_files': 0,
            'python_related_files': 0,
            'file_types': defaultdict(int),
            'python_keywords_found': set(),
            'content_categories': defaultdict(list),
            'migration_candidates': [],
            'removal_candidates': [],
            'directory_structure': {},
            'file_details': []
        }
        
        # 遍历所有文件
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file():
                analysis_result['total_files'] += 1
                file_info = self._analyze_file(file_path)
                analysis_result['file_details'].append(file_info)
                
                # 统计文件类型
                file_ext = file_path.suffix.lower()
                analysis_result['file_types'][file_ext] += 1
                
                # 统计Python相关文件
                if file_ext in self.file_type_mapping['python']:
                    analysis_result['python_files'] += 1
                elif file_ext in self.file_type_mapping['markdown']:
                    analysis_result['markdown_files'] += 1
                
                # 分析内容相关性
                if file_info['python_related']:
                    analysis_result['python_related_files'] += 1
                    analysis_result['migration_candidates'].append(file_info)
                    analysis_result['python_keywords_found'].update(file_info['python_keywords'])
                    
                    # 分类内容
                    for category, keywords in file_info['categories'].items():
                        if keywords:
                            analysis_result['content_categories'][category].append(file_info)
                else:
                    analysis_result['removal_candidates'].append(file_info)
        
        # 分析目录结构
        analysis_result['directory_structure'] = self._analyze_directory_structure()
        
        return analysis_result

    def _analyze_file(self, file_path: Path) -> Dict:
        """分析单个文件"""
        file_info = {
            'path': str(file_path.relative_to(self.base_path)),
            'name': file_path.name,
            'size': file_path.stat().st_size,
            'extension': file_path.suffix.lower(),
            'python_related': False,
            'python_keywords': set(),
            'categories': defaultdict(set),
            'content_score': 0,
            'migration_target': None
        }
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            # 检查Python关键词
            found_keywords = set()
            for keyword in self.python_keywords:
                if keyword in content:
                    found_keywords.add(keyword)
            
            file_info['python_keywords'] = found_keywords
            
            # 计算相关性分数
            if found_keywords:
                file_info['python_related'] = True
                file_info['content_score'] = len(found_keywords) / len(self.python_keywords)
            
            # 分类内容
            for category, rules in self.content_categories.items():
                category_keywords = set()
                for keyword in rules['keywords']:
                    if keyword in content:
                        category_keywords.add(keyword)
                
                for pattern in rules['patterns']:
                    if re.search(pattern, content, re.IGNORECASE):
                        category_keywords.add(pattern)
                
                if category_keywords:
                    file_info['categories'][category] = category_keywords
            
            # 确定迁移目标
            file_info['migration_target'] = self._determine_migration_target(file_info)
            
        except Exception as e:
            logger.warning(f"分析文件失败 {file_path}: {e}")
        
        return file_info

    def _determine_migration_target(self, file_info: Dict) -> str:
        """确定文件迁移目标"""
        categories = file_info['categories']
        
        # 根据内容分类确定迁移目标
        if 'core_python' in categories:
            return '01-Python基础'
        elif 'ecosystem' in categories:
            return '03-Python生态系统'
        elif 'web_frameworks' in categories:
            return '08-Python Web开发'
        elif 'data_science' in categories or 'machine_learning' in categories:
            return '09-Python数据科学'
        elif 'testing' in categories:
            return '03-Python生态系统/03-03-Python测试框架'
        elif 'devops' in categories:
            return '10-Python自动化运维'
        elif 'security' in categories:
            return '06-Python安全编程'
        elif 'performance' in categories:
            return '05-Python性能优化'
        else:
            return '12-Python最佳实践'

    def _analyze_directory_structure(self) -> Dict:
        """分析目录结构"""
        structure = {}
        
        for item in self.base_path.rglob('*'):
            if item.is_dir():
                relative_path = str(item.relative_to(self.base_path))
                structure[relative_path] = {
                    'files': len(list(item.glob('*.md'))) + len(list(item.glob('*.py'))),
                    'subdirs': len([x for x in item.iterdir() if x.is_dir()]),
                    'python_related': self._is_directory_python_related(item)
                }
        
        return structure

    def _is_directory_python_related(self, dir_path: Path) -> bool:
        """判断目录是否与Python相关"""
        python_files = list(dir_path.rglob('*.py'))
        markdown_files = list(dir_path.rglob('*.md'))
        
        # 检查文件名是否包含Python关键词
        for file_path in python_files + markdown_files:
            if any(keyword in file_path.name.lower() for keyword in self.python_keywords):
                return True
        
        return False

    def generate_migration_report(self, analysis_result: Dict) -> str:
        """生成迁移报告"""
        report = []
        report.append("# Python内容分析报告")
        report.append("")
        
        # 总体统计
        report.append("## 📊 总体统计")
        report.append("")
        report.append(f"- **总文件数**: {analysis_result['total_files']}")
        report.append(f"- **Python文件数**: {analysis_result['python_files']}")
        report.append(f"- **Markdown文件数**: {analysis_result['markdown_files']}")
        report.append(f"- **Python相关文件数**: {analysis_result['python_related_files']}")
        report.append(f"- **Python相关性比例**: {analysis_result['python_related_files']/analysis_result['total_files']*100:.1f}%")
        report.append("")
        
        # 文件类型统计
        report.append("## 📁 文件类型统计")
        report.append("")
        for ext, count in sorted(analysis_result['file_types'].items(), key=lambda x: x[1], reverse=True):
            report.append(f"- **{ext}**: {count} 个文件")
        report.append("")
        
        # 内容分类统计
        report.append("## 🏷️ 内容分类统计")
        report.append("")
        for category, files in analysis_result['content_categories'].items():
            report.append(f"- **{category}**: {len(files)} 个文件")
        report.append("")
        
        # 迁移候选文件
        report.append("## ✅ 迁移候选文件")
        report.append("")
        for file_info in analysis_result['migration_candidates'][:20]:  # 显示前20个
            report.append(f"- `{file_info['path']}` -> `{file_info['migration_target']}` (分数: {file_info['content_score']:.2f})")
        report.append("")
        
        # 移除候选文件
        report.append("## ❌ 移除候选文件")
        report.append("")
        for file_info in analysis_result['removal_candidates'][:20]:  # 显示前20个
            report.append(f"- `{file_info['path']}` (无Python相关内容)")
        report.append("")
        
        # Python关键词统计
        report.append("## 🔍 发现的Python关键词")
        report.append("")
        for keyword in sorted(analysis_result['python_keywords_found']):
            report.append(f"- `{keyword}`")
        report.append("")
        
        # 迁移建议
        report.append("## 🚀 迁移建议")
        report.append("")
        report.append("### 1. 高优先级迁移")
        high_priority = [f for f in analysis_result['migration_candidates'] if f['content_score'] > 0.5]
        for file_info in high_priority[:10]:
            report.append(f"- `{file_info['path']}` -> `{file_info['migration_target']}`")
        report.append("")
        
        report.append("### 2. 中优先级迁移")
        medium_priority = [f for f in analysis_result['migration_candidates'] if 0.2 < f['content_score'] <= 0.5]
        for file_info in medium_priority[:10]:
            report.append(f"- `{file_info['path']}` -> `{file_info['migration_target']}`")
        report.append("")
        
        report.append("### 3. 可移除内容")
        for file_info in analysis_result['removal_candidates'][:10]:
            report.append(f"- `{file_info['path']}`")
        report.append("")
        
        return "\n".join(report)

    def save_analysis_result(self, analysis_result: Dict, output_file: str = "python_analysis_result.json"):
        """保存分析结果到JSON文件"""
        # 转换set为list以便JSON序列化
        serializable_result = {}
        for key, value in analysis_result.items():
            if isinstance(value, set):
                serializable_result[key] = list(value)
            elif isinstance(value, defaultdict):
                serializable_result[key] = dict(value)
            else:
                serializable_result[key] = value
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"分析结果已保存到: {output_file}")

    def generate_migration_script(self, analysis_result: Dict) -> str:
        """生成迁移脚本"""
        script_lines = [
            "#!/bin/bash",
            "# Python内容迁移脚本",
            "# 基于分析结果自动生成",
            "",
            "echo '开始Python内容迁移...'",
            "",
            "# 创建备份",
            f"cp -r {self.base_path} docs_backup_$(date +%Y%m%d)",
            "",
            "# 创建新目录结构",
            "mkdir -p docs/python_knowledge",
            ""
        ]
        
        # 添加迁移命令
        for file_info in analysis_result['migration_candidates']:
            if file_info['migration_target']:
                source_path = file_info['path']
                target_path = f"docs/python_knowledge/{file_info['migration_target']}"
                
                script_lines.extend([
                    f"# 迁移: {source_path}",
                    f"mkdir -p {target_path}",
                    f"cp '{source_path}' '{target_path}/'",
                    ""
                ])
        
        script_lines.extend([
            "echo '迁移完成!'",
            "echo '请检查迁移结果并更新导航文件'"
        ])
        
        return "\n".join(script_lines)

def main():
    """主函数"""
    analyzer = PythonContentAnalyzer()
    
    print("Python内容分析工具")
    print("=" * 50)
    
    # 执行分析
    print("正在分析目录内容...")
    analysis_result = analyzer.analyze_directory()
    
    # 生成报告
    print("正在生成分析报告...")
    report = analyzer.generate_migration_report(analysis_result)
    
    # 保存报告
    with open("python_analysis_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    # 保存分析结果
    analyzer.save_analysis_result(analysis_result)
    
    # 生成迁移脚本
    migration_script = analyzer.generate_migration_script(analysis_result)
    with open("migrate_python_content.sh", "w", encoding="utf-8") as f:
        f.write(migration_script)
    
    print("分析完成!")
    print(f"- 分析报告: python_analysis_report.md")
    print(f"- 分析结果: python_analysis_result.json")
    print(f"- 迁移脚本: migrate_python_content.sh")
    
    # 显示关键统计
    print("\n关键统计:")
    print(f"- 总文件数: {analysis_result['total_files']}")
    print(f"- Python相关文件: {analysis_result['python_related_files']}")
    print(f"- 相关性比例: {analysis_result['python_related_files']/analysis_result['total_files']*100:.1f}%")

if __name__ == "__main__":
    main() 