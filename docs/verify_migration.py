#!/usr/bin/env python3
"""
Python迁移验证脚本

用于验证迁移结果，检查文件完整性，并生成验证报告。
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MigrationVerifier:
    """迁移验证器"""
    
    def __init__(self):
        self.new_path = Path("docs/python_knowledge")
        self.old_path = Path("docs")
        
        # 期望的目录结构
        self.expected_directories = [
            "01-Python基础",
            "02-Python高级特性",
            "03-Python生态系统",
            "04-Python版本特性", 
            "05-Python性能优化",
            "06-Python安全编程",
            "07-Python设计模式",
            "08-Python Web开发",
            "09-Python数据科学",
            "10-Python自动化运维",
            "11-Python行业应用",
            "12-Python最佳实践"
        ]
        
        # 期望的子目录
        self.expected_subdirectories = {
            "03-Python生态系统": [
                "03-01-Python包管理工具",
                "03-02-Python开发工具",
                "03-03-Python测试框架",
                "03-04-Python文档工具"
            ],
            "07-Python设计模式": [
                "07-01-创建型模式",
                "07-02-结构型模式",
                "07-03-行为型模式"
            ],
            "08-Python Web开发": [
                "08-01-Web框架",
                "08-02-API开发",
                "08-03-数据库集成",
                "08-04-部署运维"
            ],
            "09-Python数据科学": [
                "09-01-数据处理",
                "09-02-机器学习",
                "09-03-深度学习",
                "09-04-大数据处理"
            ],
            "10-Python自动化运维": [
                "10-01-系统管理",
                "10-02-DevOps工具",
                "10-03-监控告警",
                "10-04-云原生"
            ],
            "11-Python行业应用": [
                "11-01-金融科技",
                "11-02-人工智能",
                "11-03-物联网",
                "11-04-游戏开发",
                "11-05-其他行业"
            ],
            "12-Python最佳实践": [
                "12-01-代码质量",
                "12-02-项目管理",
                "12-03-团队协作",
                "12-04-持续改进"
            ]
        }
        
        # 关键文件检查
        self.key_files = [
            "README.md",
            "SUMMARY.md"
        ]
        
        # Python相关关键词
        self.python_keywords = [
            'python', 'pip', 'poetry', 'uv', 'django', 'flask', 'fastapi',
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
            'pytest', 'unittest', 'docker', 'kubernetes', 'ansible'
        ]

    def verify_directory_structure(self) -> Dict:
        """验证目录结构"""
        logger.info("验证目录结构...")
        
        verification_result = {
            'directory_structure': {},
            'missing_directories': [],
            'extra_directories': [],
            'subdirectory_verification': {},
            'overall_structure_score': 0
        }
        
        if not self.new_path.exists():
            logger.error(f"新目录不存在: {self.new_path}")
            return verification_result
        
        # 检查主要目录
        existing_dirs = [d.name for d in self.new_path.iterdir() if d.is_dir()]
        
        for expected_dir in self.expected_directories:
            dir_path = self.new_path / expected_dir
            if dir_path.exists():
                verification_result['directory_structure'][expected_dir] = True
            else:
                verification_result['directory_structure'][expected_dir] = False
                verification_result['missing_directories'].append(expected_dir)
        
        # 检查额外目录
        for existing_dir in existing_dirs:
            if existing_dir not in self.expected_directories:
                verification_result['extra_directories'].append(existing_dir)
        
        # 检查子目录
        for parent_dir, expected_subdirs in self.expected_subdirectories.items():
            parent_path = self.new_path / parent_dir
            if parent_path.exists():
                existing_subdirs = [d.name for d in parent_path.iterdir() if d.is_dir()]
                missing_subdirs = [d for d in expected_subdirs if d not in existing_subdirs]
                extra_subdirs = [d for d in existing_subdirs if d not in expected_subdirs]
                
                verification_result['subdirectory_verification'][parent_dir] = {
                    'exists': True,
                    'missing_subdirs': missing_subdirs,
                    'extra_subdirs': extra_subdirs,
                    'score': len(expected_subdirs) - len(missing_subdirs)
                }
            else:
                verification_result['subdirectory_verification'][parent_dir] = {
                    'exists': False,
                    'missing_subdirs': expected_subdirs,
                    'extra_subdirs': [],
                    'score': 0
                }
        
        # 计算总体结构分数
        total_dirs = len(self.expected_directories)
        existing_dirs = sum(1 for exists in verification_result['directory_structure'].values() if exists)
        verification_result['overall_structure_score'] = existing_dirs / total_dirs
        
        return verification_result

    def verify_files(self) -> Dict:
        """验证文件"""
        logger.info("验证文件...")
        
        verification_result = {
            'total_files': 0,
            'markdown_files': 0,
            'python_files': 0,
            'key_files': {},
            'file_distribution': {},
            'python_related_files': 0,
            'content_quality_score': 0
        }
        
        if not self.new_path.exists():
            return verification_result
        
        # 统计文件
        all_files = list(self.new_path.rglob('*'))
        verification_result['total_files'] = len([f for f in all_files if f.is_file()])
        
        # 按类型统计
        for file_path in all_files:
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext == '.md':
                    verification_result['markdown_files'] += 1
                elif ext == '.py':
                    verification_result['python_files'] += 1
                
                # 检查Python相关性
                if self._is_python_related(file_path):
                    verification_result['python_related_files'] += 1
        
        # 检查关键文件
        for key_file in self.key_files:
            key_path = self.new_path / key_file
            verification_result['key_files'][key_file] = key_path.exists()
        
        # 按目录统计文件分布
        for dir_path in self.new_path.iterdir():
            if dir_path.is_dir():
                dir_name = dir_path.name
                md_count = len(list(dir_path.rglob('*.md')))
                py_count = len(list(dir_path.rglob('*.py')))
                verification_result['file_distribution'][dir_name] = {
                    'markdown': md_count,
                    'python': py_count,
                    'total': md_count + py_count
                }
        
        # 计算内容质量分数
        if verification_result['total_files'] > 0:
            verification_result['content_quality_score'] = verification_result['python_related_files'] / verification_result['total_files']
        
        return verification_result

    def _is_python_related(self, file_path: Path) -> bool:
        """检查文件是否与Python相关"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            # 检查文件名
            file_name = file_path.name.lower()
            if any(keyword in file_name for keyword in self.python_keywords):
                return True
            
            # 检查文件内容
            if any(keyword in content for keyword in self.python_keywords):
                return True
            
            return False
        except Exception:
            return False

    def verify_links(self) -> Dict:
        """验证链接"""
        logger.info("验证链接...")
        
        verification_result = {
            'total_links': 0,
            'valid_links': 0,
            'broken_links': [],
            'link_quality_score': 0
        }
        
        if not self.new_path.exists():
            return verification_result
        
        # 检查README和SUMMARY中的链接
        for file_name in ['README.md', 'SUMMARY.md']:
            file_path = self.new_path / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 简单的链接检查
                    import re
                    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                    verification_result['total_links'] += len(links)
                    
                    for link_text, link_url in links:
                        if link_url.startswith('http'):
                            # 外部链接，暂时标记为有效
                            verification_result['valid_links'] += 1
                        else:
                            # 内部链接，检查文件是否存在
                            target_path = self.new_path / link_url.lstrip('./')
                            if target_path.exists():
                                verification_result['valid_links'] += 1
                            else:
                                verification_result['broken_links'].append({
                                    'file': file_name,
                                    'link_text': link_text,
                                    'link_url': link_url
                                })
                
                except Exception as e:
                    logger.warning(f"检查链接失败 {file_name}: {e}")
        
        # 计算链接质量分数
        if verification_result['total_links'] > 0:
            verification_result['link_quality_score'] = verification_result['valid_links'] / verification_result['total_links']
        
        return verification_result

    def generate_verification_report(self, structure_result: Dict, files_result: Dict, links_result: Dict) -> str:
        """生成验证报告"""
        report = []
        report.append("# Python迁移验证报告")
        report.append("")
        
        # 总体评分
        overall_score = (
            structure_result['overall_structure_score'] * 0.4 +
            files_result['content_quality_score'] * 0.4 +
            links_result['link_quality_score'] * 0.2
        )
        
        report.append("## 📊 总体评分")
        report.append("")
        report.append(f"**总体评分**: {overall_score:.1%}")
        report.append(f"**目录结构**: {structure_result['overall_structure_score']:.1%}")
        report.append(f"**内容质量**: {files_result['content_quality_score']:.1%}")
        report.append(f"**链接质量**: {links_result['link_quality_score']:.1%}")
        report.append("")
        
        # 目录结构验证
        report.append("## 📁 目录结构验证")
        report.append("")
        
        for dir_name, exists in structure_result['directory_structure'].items():
            status = "✅" if exists else "❌"
            report.append(f"{status} {dir_name}")
        
        if structure_result['missing_directories']:
            report.append("")
            report.append("### 缺失的目录")
            for dir_name in structure_result['missing_directories']:
                report.append(f"- {dir_name}")
        
        if structure_result['extra_directories']:
            report.append("")
            report.append("### 额外的目录")
            for dir_name in structure_result['extra_directories']:
                report.append(f"- {dir_name}")
        
        report.append("")
        
        # 子目录验证
        report.append("## 📂 子目录验证")
        report.append("")
        
        for parent_dir, subdir_info in structure_result['subdirectory_verification'].items():
            if subdir_info['exists']:
                score = subdir_info['score']
                total = len(self.expected_subdirectories.get(parent_dir, []))
                percentage = (score / total * 100) if total > 0 else 0
                report.append(f"**{parent_dir}**: {score}/{total} ({percentage:.0f}%)")
                
                if subdir_info['missing_subdirs']:
                    report.append(f"  - 缺失: {', '.join(subdir_info['missing_subdirs'])}")
                if subdir_info['extra_subdirs']:
                    report.append(f"  - 额外: {', '.join(subdir_info['extra_subdirs'])}")
            else:
                report.append(f"❌ {parent_dir}: 目录不存在")
        
        report.append("")
        
        # 文件验证
        report.append("## 📄 文件验证")
        report.append("")
        report.append(f"**总文件数**: {files_result['total_files']}")
        report.append(f"**Markdown文件**: {files_result['markdown_files']}")
        report.append(f"**Python文件**: {files_result['python_files']}")
        report.append(f"**Python相关文件**: {files_result['python_related_files']}")
        report.append(f"**内容质量分数**: {files_result['content_quality_score']:.1%}")
        report.append("")
        
        # 关键文件检查
        report.append("### 关键文件检查")
        report.append("")
        for file_name, exists in files_result['key_files'].items():
            status = "✅" if exists else "❌"
            report.append(f"{status} {file_name}")
        report.append("")
        
        # 文件分布
        report.append("### 文件分布")
        report.append("")
        for dir_name, file_info in files_result['file_distribution'].items():
            if file_info['total'] > 0:
                report.append(f"**{dir_name}**: {file_info['markdown']} MD, {file_info['python']} PY")
        report.append("")
        
        # 链接验证
        report.append("## 🔗 链接验证")
        report.append("")
        report.append(f"**总链接数**: {links_result['total_links']}")
        report.append(f"**有效链接**: {links_result['valid_links']}")
        report.append(f"**链接质量分数**: {links_result['link_quality_score']:.1%}")
        report.append("")
        
        if links_result['broken_links']:
            report.append("### 损坏的链接")
            report.append("")
            for link_info in links_result['broken_links']:
                report.append(f"- `{link_info['file']}`: `{link_info['link_text']}` -> `{link_info['link_url']}`")
            report.append("")
        
        # 建议
        report.append("## 💡 改进建议")
        report.append("")
        
        if overall_score < 0.8:
            report.append("⚠️ 迁移质量需要改进")
            if structure_result['overall_structure_score'] < 0.8:
                report.append("- 检查目录结构是否完整")
            if files_result['content_quality_score'] < 0.8:
                report.append("- 确保所有文件都与Python相关")
            if links_result['link_quality_score'] < 0.8:
                report.append("- 修复损坏的链接")
        else:
            report.append("✅ 迁移质量良好")
        
        report.append("")
        report.append("## 🎯 下一步行动")
        report.append("")
        report.append("1. 检查并修复损坏的链接")
        report.append("2. 补充缺失的目录和文件")
        report.append("3. 更新导航文件")
        report.append("4. 测试所有功能")
        report.append("5. 收集用户反馈")
        
        return "\n".join(report)

    def run_verification(self) -> Dict:
        """执行完整验证"""
        logger.info("开始验证迁移结果...")
        
        # 执行各项验证
        structure_result = self.verify_directory_structure()
        files_result = self.verify_files()
        links_result = self.verify_links()
        
        # 生成报告
        report = self.generate_verification_report(structure_result, files_result, links_result)
        
        # 保存报告
        with open("python_migration_verification_report.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        # 保存详细结果
        detailed_result = {
            'structure': structure_result,
            'files': files_result,
            'links': links_result,
            'timestamp': str(Path().cwd())
        }
        
        with open("python_migration_verification_result.json", "w", encoding="utf-8") as f:
            json.dump(detailed_result, f, indent=2, ensure_ascii=False)
        
        logger.info("验证完成！")
        logger.info("- 验证报告: python_migration_verification_report.md")
        logger.info("- 详细结果: python_migration_verification_result.json")
        
        return {
            'structure': structure_result,
            'files': files_result,
            'links': links_result,
            'report': report
        }

def main():
    """主函数"""
    verifier = MigrationVerifier()
    
    print("🔍 Python迁移验证工具")
    print("="*50)
    print("此工具将验证Python内容迁移的结果")
    print()
    
    result = verifier.run_verification()
    
    # 显示关键指标
    overall_score = (
        result['structure']['overall_structure_score'] * 0.4 +
        result['files']['content_quality_score'] * 0.4 +
        result['links']['link_quality_score'] * 0.2
    )
    
    print("\n" + "="*50)
    print("验证结果摘要")
    print("="*50)
    print(f"📊 总体评分: {overall_score:.1%}")
    print(f"📁 目录结构: {result['structure']['overall_structure_score']:.1%}")
    print(f"📄 内容质量: {result['files']['content_quality_score']:.1%}")
    print(f"🔗 链接质量: {result['links']['link_quality_score']:.1%}")
    print(f"📄 总文件数: {result['files']['total_files']}")
    print(f"🐍 Python相关: {result['files']['python_related_files']}")
    print("="*50)

if __name__ == "__main__":
    main() 