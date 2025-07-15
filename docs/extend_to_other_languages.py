import os
from pathlib import Path
import shutil

# 其他语言的知识体系配置
LANGUAGE_CONFIGS = {
    'java': {
        'name': 'Java知识体系',
        'modules': [
            '01-Java基础',
            '02-面向对象',
            '03-集合框架',
            '04-多线程',
            '05-JVM原理',
            '06-Spring框架',
            '07-微服务',
            '08-性能优化',
            '09-安全编程',
            '10-最佳实践'
        ],
        'file_extensions': ['.java', '.xml', '.properties'],
        'template_content': 'Java编程语言知识体系'
    },
    'go': {
        'name': 'Go知识体系',
        'modules': [
            '01-Go基础',
            '02-并发编程',
            '03-网络编程',
            '04-Web开发',
            '05-微服务',
            '06-性能优化',
            '07-测试实践',
            '08-最佳实践'
        ],
        'file_extensions': ['.go', '.mod', '.sum'],
        'template_content': 'Go编程语言知识体系'
    },
    'rust': {
        'name': 'Rust知识体系',
        'modules': [
            '01-Rust基础',
            '02-所有权系统',
            '03-并发安全',
            '04-系统编程',
            '05-Web开发',
            '06-性能优化',
            '07-最佳实践'
        ],
        'file_extensions': ['.rs', '.toml'],
        'template_content': 'Rust编程语言知识体系'
    },
    'javascript': {
        'name': 'JavaScript知识体系',
        'modules': [
            '01-JavaScript基础',
            '02-ES6特性',
            '03-异步编程',
            '04-Node.js',
            '05-前端框架',
            '06-性能优化',
            '07-最佳实践'
        ],
        'file_extensions': ['.js', '.ts', '.json'],
        'template_content': 'JavaScript编程语言知识体系'
    }
}

def create_language_system(language):
    """为指定语言创建知识体系"""
    if language not in LANGUAGE_CONFIGS:
        print(f"❌ 不支持的语言: {language}")
        return False
    
    config = LANGUAGE_CONFIGS[language]
    system_name = config['name']
    system_dir = Path(f'{language}_knowledge_system')
    
    print(f"🔄 创建{system_name}...")
    
    # 创建主目录
    system_dir.mkdir(exist_ok=True)
    
    # 创建模块目录
    for module in config['modules']:
        module_dir = system_dir / module
        module_dir.mkdir(exist_ok=True)
        
        # 创建README
        readme_content = f"""# {module}

## 简介
（请补充{config['template_content']}中{module}的简介）

## 主要知识点
- 请补充本模块的主要知识点

## 代码示例
- 请补充代码示例

## 学习资源
- 请补充学习资源

## 常见问题
- 请补充常见问题

## 实践建议
- 请补充实践建议
"""
        with open(module_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 创建知识点清单
        checklist_content = f"""# {module} 知识点清单

## 必须掌握
- 请补充本模块必须掌握的知识点

## 进阶知识点
- 请补充进阶知识点

## 实践项目
- 请补充实践项目建议

## 学习建议
- 请补充学习建议
"""
        with open(module_dir / 'knowledge_checklist.md', 'w', encoding='utf-8') as f:
            f.write(checklist_content)
        
        # 创建示例目录
        examples_dir = module_dir / 'examples'
        examples_dir.mkdir(exist_ok=True)
        
        # 创建示例文件
        ext = config['file_extensions'][0]
        example_file = examples_dir / f'example_1{ext}'
        example_content = f"""// {module} 示例代码
// 请根据实际需求补充具体实现

// TODO: 在这里添加具体功能
"""
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write(example_content)
    
    # 创建主README
    main_readme = f"""# {system_name}

## 概述
{config['template_content']}，涵盖从基础到高级的完整知识体系。

## 目录结构
"""
    for module in config['modules']:
        main_readme += f"- [{module}]({module}/README.md)\n"
    
    main_readme += f"""
## 快速开始
1. 选择感兴趣的模块开始学习
2. 查看知识点清单了解学习目标
3. 运行代码示例加深理解
4. 参与实践项目巩固知识

## 贡献指南
欢迎贡献内容，请参考CONTRIBUTING.md

## 许可证
MIT License
"""
    
    with open(system_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(main_readme)
    
    print(f"✅ {system_name}创建完成: {system_dir}")
    return True

def create_migration_tools_for_language(language):
    """为指定语言创建迁移工具"""
    if language not in LANGUAGE_CONFIGS:
        return False
    
    config = LANGUAGE_CONFIGS[language]
    
    # 创建迁移脚本
    migration_script = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{config['name']}迁移工具
\"\"\"

import os
from pathlib import Path

def migrate_{language}_content():
    \"\"\"迁移{language}相关内容\"\"\"
    print(f"🔄 开始迁移{config['name']}...")
    
    # 这里可以添加具体的迁移逻辑
    # 类似于python_content_analyzer.py的实现
    
    print(f"✅ {config['name']}迁移完成")

if __name__ == "__main__":
    migrate_{language}_content()
"""
    
    with open(f'{language}_content_analyzer.py', 'w', encoding='utf-8') as f:
        f.write(migration_script)
    
    print(f"✅ 已创建{language}迁移工具: {language}_content_analyzer.py")

def create_all_language_systems():
    """创建所有支持的语言知识体系"""
    print("🔄 创建所有语言知识体系...")
    
    for language in LANGUAGE_CONFIGS.keys():
        create_language_system(language)
        create_migration_tools_for_language(language)
    
    print("🎉 所有语言知识体系创建完成！")

def main():
    """主函数"""
    print("=== 多语言知识体系扩展工具 ===")
    print("支持的语言:")
    for lang, config in LANGUAGE_CONFIGS.items():
        print(f"  - {lang}: {config['name']}")
    
    print("\n选择操作:")
    print("1. 创建所有语言知识体系")
    print("2. 创建指定语言知识体系")
    
    choice = input("请选择 (1/2): ")
    
    if choice == '1':
        create_all_language_systems()
    elif choice == '2':
        language = input("请输入语言名称 (java/go/rust/javascript): ")
        if create_language_system(language):
            create_migration_tools_for_language(language)
    else:
        print("无效选择")

if __name__ == "__main__":
    main() 