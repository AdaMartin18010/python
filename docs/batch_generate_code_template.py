import os
from pathlib import Path

root = Path('python_knowledge_system')
for dirpath, dirnames, filenames in os.walk(root):
    if dirpath == str(root): continue
    examples = Path(dirpath) / 'examples'
    examples.mkdir(exist_ok=True)
    example_file = examples / 'example_1.py'
    if not example_file.exists():
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write('# 示例代码：请补充\n') 