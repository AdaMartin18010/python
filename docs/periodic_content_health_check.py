import os
from pathlib import Path
import re
from collections import Counter

def check_empty_dirs(root):
    for dirpath, dirnames, filenames in os.walk(root):
        if dirpath == root: continue
        if not dirnames and not filenames:
            print(f'⚠️ 空目录: {dirpath}')

def check_dead_links(root):
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
    for mdfile in Path(root).rglob('*.md'):
        with open(mdfile, 'r', encoding='utf-8') as f:
            for m in link_pattern.finditer(f.read()):
                link = m.group(1)
                if link.endswith('.md') and not Path(mdfile.parent / link).exists():
                    print(f'❌ 死链: {mdfile} -> {link}')

def check_duplicate_titles(root):
    title_counter = Counter()
    for mdfile in Path(root).rglob('*.md'):
        with open(mdfile, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#'):
                    title_counter[line.strip()] += 1
    for title, count in title_counter.items():
        if count > 1:
            print(f'⚠️ 重复标题: {title} ({count}次)')

def check_format(root):
    for mdfile in Path(root).rglob('*.md'):
        with open(mdfile, 'r', encoding='utf-8') as f:
            content = f.read()
            if '\t' in content:
                print(f'⚠️ {mdfile} 包含制表符')
            if content.count('#') == 0:
                print(f'⚠️ {mdfile} 可能缺少标题')

def main():
    root = 'python_knowledge_system'
    print('== 内容健康巡检报告 ==')
    check_empty_dirs(root)
    check_dead_links(root)
    check_duplicate_titles(root)
    check_format(root)
    print('== 巡检完成 ==')

if __name__ == '__main__':
    main() 