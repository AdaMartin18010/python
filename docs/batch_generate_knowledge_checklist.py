import os
from pathlib import Path

root = Path('python_knowledge_system')
for dirpath, dirnames, filenames in os.walk(root):
    if dirpath == str(root): continue
    checklist = Path(dirpath) / 'knowledge_checklist.md'
    if not checklist.exists():
        with open(checklist, 'w', encoding='utf-8') as f:
            f.write('# 知识点清单\n- 请补充本模块应掌握的知识点\n') 