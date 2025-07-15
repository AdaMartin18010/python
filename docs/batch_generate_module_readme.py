import os
from pathlib import Path

root = Path('python_knowledge_system')
template = '''# {modulename}
## 简介
（请补充本模块简介）

## 目录
- [知识点清单](knowledge_checklist.md)
- [代码示例](examples/)
- [常见问题](#常见问题)

## 推荐阅读
- 

## 常见问题
- 
'''

for dirpath, dirnames, filenames in os.walk(root):
    if dirpath == str(root): continue
    readme = Path(dirpath) / 'README.md'
    if not readme.exists():
        with open(readme, 'w', encoding='utf-8') as f:
            f.write(template.format(modulename=Path(dirpath).name)) 