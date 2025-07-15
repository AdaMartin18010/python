import os
from pathlib import Path

def walk_dir(root, prefix=''):
    lines = []
    for name in sorted(os.listdir(root)):
        path = Path(root) / name
        if path.is_dir():
            node = f'{prefix}{name.replace("-", "_")}'
            lines.append(f'{prefix}root --> {node}')
            lines += walk_dir(path, node + '_')
    return lines

root = 'python_knowledge_system'
mermaid = ['graph TD', 'root["Python知识体系"]']
mermaid += walk_dir(root)

with open('python_knowledge_system_mindmap.mmd', 'w', encoding='utf-8') as f:
    f.write('\n'.join(mermaid))
print('✅ Mermaid思维导图已生成: python_knowledge_system_mindmap.mmd') 