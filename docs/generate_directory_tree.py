#!/usr/bin/env python3
"""
生成python_knowledge目录的树形结构文档
"""

from pathlib import Path
import os

def generate_tree_structure(base_path: Path, prefix="", max_depth=3, current_depth=0):
    """生成目录树结构"""
    if current_depth >= max_depth:
        return []
    
    lines = []
    items = sorted(base_path.iterdir())
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        next_prefix = "    " if is_last else "│   "
        
        if item.is_dir():
            lines.append(f"{prefix}{current_prefix}{item.name}/")
            lines.extend(generate_tree_structure(
                item, 
                prefix + next_prefix, 
                max_depth, 
                current_depth + 1
            ))
        else:
            # 根据文件类型添加不同的图标
            icon = get_file_icon(item.name)
            lines.append(f"{prefix}{current_prefix}{icon} {item.name}")
    
    return lines

def get_file_icon(filename: str) -> str:
    """根据文件名返回图标"""
    if filename.endswith('.md'):
        return "📄"
    elif filename.endswith('.py'):
        return "🐍"
    elif filename.endswith('.json'):
        return "📋"
    elif filename.endswith('.yml') or filename.endswith('.yaml'):
        return "⚙️"
    elif filename.endswith('.txt'):
        return "📝"
    else:
        return "📄"

def generate_statistics(base_path: Path):
    """生成统计信息"""
    stats = {
        'directories': 0,
        'markdown_files': 0,
        'python_files': 0,
        'other_files': 0
    }
    
    for item in base_path.rglob('*'):
        if item.is_file():
            if item.suffix == '.md':
                stats['markdown_files'] += 1
            elif item.suffix == '.py':
                stats['python_files'] += 1
            else:
                stats['other_files'] += 1
        elif item.is_dir():
            stats['directories'] += 1
    
    return stats

def main():
    base_path = Path("docs/python_knowledge")
    
    if not base_path.exists():
        print("目标目录不存在！请先执行迁移。")
        return
    
    print("🌳 生成目录树结构...")
    
    # 生成树形结构
    tree_lines = [f"{base_path.name}/"]
    tree_lines.extend(generate_tree_structure(base_path))
    
    # 生成统计信息
    stats = generate_statistics(base_path)
    
    # 生成完整报告
    report = []
    report.append("# Python知识体系目录结构")
    report.append("")
    report.append("## 📊 统计信息")
    report.append("")
    report.append(f"- **目录数量**: {stats['directories']}")
    report.append(f"- **Markdown文件**: {stats['markdown_files']}")
    report.append(f"- **Python文件**: {stats['python_files']}")
    report.append(f"- **其他文件**: {stats['other_files']}")
    report.append(f"- **总文件数**: {stats['markdown_files'] + stats['python_files'] + stats['other_files']}")
    report.append("")
    
    report.append("## 📁 目录结构")
    report.append("")
    report.append("```")
    report.extend(tree_lines)
    report.append("```")
    report.append("")
    
    report.append("## 🎯 模块说明")
    report.append("")
    report.append("### 主要模块")
    report.append("")
    report.append("- **01-Python基础**: 语法、数据类型、控制流等基础概念")
    report.append("- **02-Python高级特性**: 装饰器、生成器、元类等高级概念")
    report.append("- **03-Python生态系统**: 包管理、开发工具、测试框架等")
    report.append("- **04-Python版本特性**: 各版本新特性和PEP解读")
    report.append("- **05-Python性能优化**: 性能分析、内存优化、并发编程")
    report.append("- **06-Python安全编程**: 输入验证、SQL注入防护等")
    report.append("- **07-Python设计模式**: 创建型、结构型、行为型模式")
    report.append("- **08-Python Web开发**: Django、Flask、FastAPI等框架")
    report.append("- **09-Python数据科学**: pandas、numpy、机器学习等")
    report.append("- **10-Python自动化运维**: 系统管理、DevOps、监控告警")
    report.append("- **11-Python行业应用**: 金融科技、AI、物联网等应用")
    report.append("- **12-Python最佳实践**: 代码质量、项目管理、团队协作")
    report.append("")
    
    report.append("### 图标说明")
    report.append("")
    report.append("- 📄 Markdown文档")
    report.append("- 🐍 Python代码文件")
    report.append("- 📋 JSON配置文件")
    report.append("- ⚙️ YAML配置文件")
    report.append("- 📝 文本文件")
    report.append("")
    
    report.append("## 📈 内容分布")
    report.append("")
    
    # 按模块统计文件数量
    module_stats = {}
    for level1_dir in base_path.iterdir():
        if level1_dir.is_dir():
            module_name = level1_dir.name
            md_count = len(list(level1_dir.rglob("*.md")))
            py_count = len(list(level1_dir.rglob("*.py")))
            module_stats[module_name] = {
                'markdown': md_count,
                'python': py_count,
                'total': md_count + py_count
            }
    
    # 按文件数量排序
    sorted_modules = sorted(module_stats.items(), key=lambda x: x[1]['total'], reverse=True)
    
    report.append("| 模块 | Markdown | Python | 总计 |")
    report.append("|------|----------|--------|------|")
    for module_name, counts in sorted_modules:
        report.append(f"| {module_name} | {counts['markdown']} | {counts['python']} | {counts['total']} |")
    report.append("")
    
    # 保存报告
    with open("directory_tree_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    
    print("✅ 目录树结构生成完成！")
    print("- 详细报告: directory_tree_report.md")
    print(f"- 总目录数: {stats['directories']}")
    print(f"- 总文件数: {stats['markdown_files'] + stats['python_files'] + stats['other_files']}")

if __name__ == "__main__":
    main() 