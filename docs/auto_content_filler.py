import os
from pathlib import Path
import random

# 预定义的内容模板
CONTENT_TEMPLATES = {
    'python_basic': {
        'intro': 'Python基础模块涵盖了Python编程的核心概念和基础知识。',
        'topics': ['变量和数据类型', '控制流语句', '函数定义和调用', '模块和包'],
        'examples': ['hello_world.py', 'calculator.py', 'list_operations.py']
    },
    'advanced_features': {
        'intro': 'Python高级特性模块深入探讨Python的进阶功能和特性。',
        'topics': ['面向对象编程', '装饰器', '生成器和迭代器', '上下文管理器'],
        'examples': ['class_example.py', 'decorator_demo.py', 'generator_example.py']
    },
    'web_development': {
        'intro': 'Web开发模块介绍Python在Web开发中的应用和框架。',
        'topics': ['Flask框架', 'Django框架', 'FastAPI框架', 'RESTful API'],
        'examples': ['flask_app.py', 'django_project.py', 'fastapi_demo.py']
    }
}

def get_module_type(dirname):
    """根据目录名判断模块类型"""
    dirname_lower = dirname.lower()
    if '基础' in dirname or 'basic' in dirname:
        return 'python_basic'
    elif '高级' in dirname or 'advanced' in dirname:
        return 'advanced_features'
    elif 'web' in dirname or '开发' in dirname:
        return 'web_development'
    else:
        return 'python_basic'  # 默认类型

def fill_readme_content(dirpath, module_type):
    """填充README内容"""
    template = CONTENT_TEMPLATES[module_type]
    
    content = f"""# {Path(dirpath).name}

## 简介
{template['intro']}

## 主要知识点
"""
    for topic in template['topics']:
        content += f"- {topic}\n"
    
    content += """
## 代码示例
"""
    for example in template['examples']:
        content += f"- [{example}](examples/{example})\n"
    
    content += """
## 学习资源
- [官方文档](https://docs.python.org/)
- [Python教程](https://docs.python.org/3/tutorial/)

## 常见问题
- Q: 如何开始学习Python？
- A: 建议从基础语法开始，逐步深入高级特性。

## 实践建议
- 多动手编写代码
- 参与开源项目
- 阅读优秀代码
"""
    return content

def fill_code_example(example_name, module_type):
    """填充代码示例内容"""
    template = CONTENT_TEMPLATES[module_type]
    
    if 'hello_world' in example_name:
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hello World示例
演示Python基础语法
"""

def main():
    """主函数"""
    print("Hello, World!")
    
    # 变量定义
    name = "Python"
    version = 3.9
    
    # 字符串格式化
    print(f"Welcome to {name} {version}!")
    
    # 列表操作
    numbers = [1, 2, 3, 4, 5]
    print(f"Numbers: {numbers}")
    print(f"Sum: {sum(numbers)}")

if __name__ == "__main__":
    main()
'''
    elif 'calculator' in example_name:
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单计算器示例
演示函数定义和基本运算
"""

def add(a, b):
    """加法函数"""
    return a + b

def subtract(a, b):
    """减法函数"""
    return a - b

def multiply(a, b):
    """乘法函数"""
    return a * b

def divide(a, b):
    """除法函数"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def main():
    """主函数"""
    print("简单计算器")
    print("1. 加法")
    print("2. 减法")
    print("3. 乘法")
    print("4. 除法")
    
    choice = input("请选择操作 (1-4): ")
    a = float(input("请输入第一个数字: "))
    b = float(input("请输入第二个数字: "))
    
    if choice == '1':
        result = add(a, b)
    elif choice == '2':
        result = subtract(a, b)
    elif choice == '3':
        result = multiply(a, b)
    elif choice == '4':
        result = divide(a, b)
    else:
        print("无效选择")
        return
    
    print(f"结果: {result}")

if __name__ == "__main__":
    main()
'''
    else:
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{example_name} 示例代码
请根据实际需求补充具体实现
"""

def main():
    """主函数"""
    print("示例代码 - 请补充具体实现")
    
    # TODO: 在这里添加具体功能
    pass

if __name__ == "__main__":
    main()
'''

def fill_knowledge_checklist(module_type):
    """填充知识点清单"""
    template = CONTENT_TEMPLATES[module_type]
    
    content = """# 知识点清单

## 必须掌握
"""
    for topic in template['topics']:
        content += f"- [ ] {topic}\n"
    
    content += """
## 进阶知识点
- [ ] 性能优化技巧
- [ ] 最佳实践
- [ ] 常见陷阱和解决方案

## 实践项目
- [ ] 完成基础练习
- [ ] 参与小型项目
- [ ] 阅读优秀开源代码

## 学习建议
1. 理论结合实践
2. 多写代码，多调试
3. 参与社区讨论
4. 持续学习新特性
"""
    return content

def auto_fill_content():
    """自动填充内容"""
    root = Path('python_knowledge_system')
    
    if not root.exists():
        print("❌ python_knowledge_system 目录不存在，请先运行迁移脚本")
        return
    
    print("🔄 开始自动填充内容...")
    
    for dirpath, dirnames, filenames in os.walk(root):
        if dirpath == str(root):  # 跳过根目录
            continue
            
        dirname = Path(dirpath).name
        module_type = get_module_type(dirname)
        
        # 填充README
        readme_file = Path(dirpath) / 'README.md'
        if readme_file.exists():
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '（请补充本模块简介）' in content:
                    new_content = fill_readme_content(dirpath, module_type)
                    with open(readme_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ 已填充: {readme_file}")
        
        # 填充代码示例
        examples_dir = Path(dirpath) / 'examples'
        if examples_dir.exists():
            for example_file in examples_dir.glob('*.py'):
                with open(example_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '请补充' in content:
                        new_content = fill_code_example(example_file.name, module_type)
                        with open(example_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✅ 已填充: {example_file}")
        
        # 填充知识点清单
        checklist_file = Path(dirpath) / 'knowledge_checklist.md'
        if checklist_file.exists():
            with open(checklist_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '请补充本模块应掌握的知识点' in content:
                    new_content = fill_knowledge_checklist(module_type)
                    with open(checklist_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ 已填充: {checklist_file}")
    
    print("🎉 内容填充完成！")

if __name__ == "__main__":
    auto_fill_content() 