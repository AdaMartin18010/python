#!/usr/bin/env python3
"""
检测和修复Markdown文件中的内部链接
"""

from pathlib import Path
import re
import os

class LinkChecker:
    def __init__(self, base_path: str = "docs/python_knowledge"):
        self.base_path = Path(base_path)
        self.broken_links = []
        self.fixed_links = []
        
    def check_links_in_file(self, file_path: Path):
        """检查单个文件中的链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找所有链接
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            
            for link_text, link_url in links:
                if self._is_internal_link(link_url):
                    if not self._link_exists(file_path, link_url):
                        self.broken_links.append({
                            'file': str(file_path.relative_to(self.base_path)),
                            'link_text': link_text,
                            'link_url': link_url
                        })
                        
        except Exception as e:
            print(f"检查文件失败 {file_path}: {e}")
    
    def _is_internal_link(self, url: str) -> bool:
        """判断是否为内部链接"""
        return not url.startswith(('http://', 'https://', 'mailto:', '#'))
    
    def _link_exists(self, source_file: Path, link_url: str) -> bool:
        """检查链接是否存在"""
        # 处理相对路径
        if link_url.startswith('./'):
            link_url = link_url[2:]
        elif link_url.startswith('../'):
            # 处理上级目录
            parts = link_url.split('/')
            up_count = 0
            for part in parts:
                if part == '..':
                    up_count += 1
                else:
                    break
            link_url = '/'.join(parts[up_count:])
        
        # 构建目标路径
        target_path = source_file.parent / link_url
        
        # 检查文件是否存在
        if target_path.exists():
            return True
        
        # 检查是否为锚点链接
        if '#' in link_url:
            file_part, anchor = link_url.split('#', 1)
            if file_part:
                target_path = source_file.parent / file_part
            else:
                target_path = source_file
            
            if target_path.exists():
                # 简单检查锚点是否存在（这里只是检查文件存在）
                return True
        
        return False
    
    def fix_common_links(self, file_path: Path):
        """修复常见的链接问题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 修复常见的链接问题
            # 1. 修复README.md链接
            content = re.sub(r'\[([^\]]+)\]\(([^)]*README\.md)\)', r'[\1](\2)', content)
            
            # 2. 修复相对路径
            content = re.sub(r'\[([^\]]+)\]\(\./([^)]+)\)', r'[\1](\2)', content)
            
            # 3. 修复文件扩展名
            content = re.sub(r'\[([^\]]+)\]\(([^)]+)\.md\)', r'[\1](\2.md)', content)
            
            # 如果内容有变化，保存文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_links.append(str(file_path.relative_to(self.base_path)))
                print(f"已修复链接: {file_path}")
                
        except Exception as e:
            print(f"修复文件失败 {file_path}: {e}")
    
    def check_all_files(self):
        """检查所有Markdown文件"""
        print("开始检查内部链接...")
        
        md_files = list(self.base_path.rglob("*.md"))
        
        for md_file in md_files:
            self.check_links_in_file(md_file)
        
        print(f"检查完成！发现 {len(self.broken_links)} 个损坏的链接。")
    
    def fix_all_files(self):
        """修复所有文件的链接"""
        print("开始修复常见链接问题...")
        
        md_files = list(self.base_path.rglob("*.md"))
        
        for md_file in md_files:
            self.fix_common_links(md_file)
        
        print(f"修复完成！修复了 {len(self.fixed_links)} 个文件。")
    
    def generate_report(self):
        """生成链接检查报告"""
        report = []
        report.append("# 内部链接检查报告")
        report.append("")
        
        if self.broken_links:
            report.append("## ❌ 损坏的链接")
            report.append("")
            for link_info in self.broken_links:
                report.append(f"- **文件**: `{link_info['file']}`")
                report.append(f"  - 链接文本: `{link_info['link_text']}`")
                report.append(f"  - 链接地址: `{link_info['link_url']}`")
                report.append("")
        else:
            report.append("## ✅ 所有链接正常")
            report.append("")
        
        if self.fixed_links:
            report.append("## 🔧 已修复的文件")
            report.append("")
            for file_path in self.fixed_links:
                report.append(f"- `{file_path}`")
            report.append("")
        
        report.append("## 💡 修复建议")
        report.append("")
        report.append("1. 检查损坏的链接，确保目标文件存在")
        report.append("2. 更新链接地址为正确的相对路径")
        report.append("3. 确保文件名和路径大小写正确")
        report.append("4. 检查锚点链接是否正确")
        
        return "\n".join(report)

def main():
    checker = LinkChecker()
    
    print("🔍 Markdown内部链接检查工具")
    print("=" * 50)
    
    # 检查链接
    checker.check_all_files()
    
    # 修复常见问题
    checker.fix_all_files()
    
    # 生成报告
    report = checker.generate_report()
    
    # 保存报告
    with open("link_check_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\\n检查完成！")
    print("- 详细报告: link_check_report.md")
    
    if checker.broken_links:
        print(f"- 发现 {len(checker.broken_links)} 个损坏的链接，请手动修复")
    else:
        print("- 所有链接正常")

if __name__ == "__main__":
    main() 