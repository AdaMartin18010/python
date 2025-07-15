#!/usr/bin/env python3
"""
批量生成知识点清单占位符
在每个README.md文件中添加知识点清单部分
"""

from pathlib import Path
import re

KNOWLEDGE_CHECKLIST = """

## 知识点清单

### 基础概念
- [ ] 核心概念1
- [ ] 核心概念2
- [ ] 核心概念3

### 实践技能
- [ ] 基础技能1
- [ ] 基础技能2
- [ ] 基础技能3

### 进阶应用
- [ ] 进阶应用1
- [ ] 进阶应用2
- [ ] 进阶应用3

### 最佳实践
- [ ] 最佳实践1
- [ ] 最佳实践2
- [ ] 最佳实践3

---

"""

def add_knowledge_checklist(file_path: Path):
    """在README.md文件中添加知识点清单"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经包含知识点清单
        if "## 知识点清单" in content:
            print(f"跳过已包含知识点清单的文件: {file_path}")
            return
        
        # 在文件末尾添加知识点清单
        new_content = content + KNOWLEDGE_CHECKLIST
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已添加知识点清单: {file_path}")
        
    except Exception as e:
        print(f"处理文件失败 {file_path}: {e}")

def main():
    base_path = Path("docs/python_knowledge")
    
    if not base_path.exists():
        print("目标目录不存在！请先执行迁移。")
        return
    
    print("开始添加知识点清单...")
    
    # 遍历所有README.md文件
    readme_files = list(base_path.rglob("README.md"))
    
    for readme_file in readme_files:
        add_knowledge_checklist(readme_file)
    
    print(f"\n知识点清单添加完成！共处理 {len(readme_files)} 个文件。")
    print("请根据各模块的具体内容修改知识点清单。")

if __name__ == "__main__":
    main() 