#!/usr/bin/env python3
"""
批量生成代码示例模板
在每个二级子目录下生成example.py文件
"""

from pathlib import Path
import os

EXAMPLE_TEMPLATE = '''"""
{module_name} - 代码示例

本文件包含{module_name}模块的典型代码示例。
请根据实际需求修改和完善这些示例。
"""

def main():
    """主函数 - 演示模块的核心功能"""
    print("=" * 50)
    print(f"{module_name} 模块示例")
    print("=" * 50)
    
    # 在这里添加具体的代码示例
    basic_example()
    
    print("\\n示例执行完成！")

def basic_example():
    """基础示例"""
    print("\\n1. 基础示例:")
    print("   - 这里可以添加基础用法示例")
    print("   - 包含核心概念演示")
    print("   - 提供实际应用场景")

def advanced_example():
    """进阶示例"""
    print("\\n2. 进阶示例:")
    print("   - 这里可以添加进阶用法示例")
    print("   - 包含最佳实践演示")
    print("   - 提供性能优化建议")

def practical_example():
    """实践示例"""
    print("\\n3. 实践示例:")
    print("   - 这里可以添加实际项目示例")
    print("   - 包含真实场景应用")
    print("   - 提供问题解决方案")

if __name__ == "__main__":
    main()
'''

def get_module_name(dir_path: Path) -> str:
    """根据目录路径生成模块名称"""
    # 移除数字前缀和Python前缀
    name = dir_path.name
    if name.startswith(('01-', '02-', '03-', '04-', '05-', '06-', '07-', '08-', '09-', '10-', '11-', '12-')):
        name = name[3:]
    if name.startswith('Python'):
        name = name[6:].strip()
    return name or "示例模块"

def create_example_file(dir_path: Path):
    """在指定目录下创建example.py文件"""
    example_path = dir_path / "example.py"
    
    # 如果文件已存在，跳过
    if example_path.exists():
        print(f"跳过已存在的文件: {example_path}")
        return
    
    module_name = get_module_name(dir_path)
    content = EXAMPLE_TEMPLATE.format(module_name=module_name)
    
    with open(example_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已生成: {example_path}")

def main():
    base_path = Path("docs/python_knowledge")
    
    if not base_path.exists():
        print("目标目录不存在！请先执行迁移。")
        return
    
    print("开始生成代码示例模板...")
    
    # 遍历所有二级子目录
    for level1_dir in base_path.iterdir():
        if level1_dir.is_dir():
            for level2_dir in level1_dir.iterdir():
                if level2_dir.is_dir():
                    create_example_file(level2_dir)
    
    print("\\n代码示例模板生成完成！")
    print("请根据各模块的具体内容修改example.py文件。")

if __name__ == "__main__":
    main() 