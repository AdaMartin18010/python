import os
import sys
import subprocess
from pathlib import Path

# 检查所有md文件格式
for mdfile in Path('.').rglob('*.md'):
    with open(mdfile, 'r', encoding='utf-8') as f:
        content = f.read()
        if '\t' in content:
            print(f'❌ {mdfile} 包含制表符，请改为空格')
            sys.exit(1)
        if content.count('#') == 0:
            print(f'❌ {mdfile} 可能缺少标题')
            sys.exit(1)

# 检查所有py文件PEP8规范
for pyfile in Path('.').rglob('*.py'):
    if 'venv' in str(pyfile): continue
    result = subprocess.run(['flake8', str(pyfile)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f'❌ {pyfile} 不符合PEP8规范:\n{result.stdout}')
        sys.exit(1)

# 检查所有md文件内部链接
import re
link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
for mdfile in Path('.').rglob('*.md'):
    with open(mdfile, 'r', encoding='utf-8') as f:
        for m in link_pattern.finditer(f.read()):
            link = m.group(1)
            if link.endswith('.md') and not Path(mdfile.parent / link).exists():
                print(f'❌ {mdfile} 存在无效链接: {link}')
                sys.exit(1)
print('✅ pre-commit检查通过') 