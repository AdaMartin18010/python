#!/usr/bin/env python3
"""
批量为python_knowledge目录下所有一级和二级子目录生成README.md模板（如已存在则跳过）。
"""
import os
from pathlib import Path

TEMPLATE = """# {title}

## 简介

本模块属于Python知识体系的组成部分，主要内容包括：
- 主要知识点
- 典型应用场景
- 推荐学习顺序

## 推荐用法

- 按目录顺序学习本模块内容
- 阅读代码示例，结合实际项目实践
- 参考相关资源链接，扩展知识面

## 目录导航

{nav}

---

> 如有建议或补充，请在本README下方留言或提交PR。
"""

def get_title_from_dir(dir_path: Path) -> str:
    """根据目录名生成标题"""
    return dir_path.name.replace('_', ' ').replace('-', ' ').replace('Python', 'Python ').strip()

def get_nav(dir_path: Path) -> str:
    """生成目录下的导航列表"""
    items = []
    for f in sorted(dir_path.iterdir()):
        if f.is_file() and f.suffix == '.md' and f.name != 'README.md':
            items.append(f"- [{f.stem}]({f.name})")
        elif f.is_dir():
            items.append(f"- [{f.name}](./{f.name}/README.md)")
    return '\n'.join(items) if items else '（待补充）'

def create_readme_for_dir(dir_path: Path):
    readme_path = dir_path / 'README.md'
    if readme_path.exists():
        return
    title = get_title_from_dir(dir_path)
    nav = get_nav(dir_path)
    content = TEMPLATE.format(title=title, nav=nav)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"已生成: {readme_path}")

def main():
    base = Path('docs/python_knowledge')
    if not base.exists():
        print('目标目录不存在！请先执行迁移。')
        return
    # 一级目录
    for d1 in base.iterdir():
        if d1.is_dir():
            create_readme_for_dir(d1)
            # 二级目录
            for d2 in d1.iterdir():
                if d2.is_dir():
                    create_readme_for_dir(d2)

if __name__ == '__main__':
    main() 