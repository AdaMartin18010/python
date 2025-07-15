import os
from pathlib import Path
import json

def generate_html_index():
    """生成HTML索引页面"""
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python知识体系</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .module-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .module-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            background: #fafafa;
            transition: transform 0.2s;
        }
        .module-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .module-title {
            color: #3498db;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .module-description {
            color: #666;
            margin-bottom: 15px;
        }
        .module-links {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .module-links a {
            background: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.9em;
        }
        .module-links a:hover {
            background: #2980b9;
        }
        .stats {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .stats h3 {
            color: #2c3e50;
            margin-top: 0;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        .stat-item {
            text-align: center;
            padding: 10px;
            background: white;
            border-radius: 6px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Python知识体系</h1>
        
        <div class="stats">
            <h3>📊 统计信息</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number" id="total-modules">0</div>
                    <div class="stat-label">总模块数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="total-files">0</div>
                    <div class="stat-label">总文件数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="total-examples">0</div>
                    <div class="stat-label">代码示例</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="completion-rate">0%</div>
                    <div class="stat-label">完成度</div>
                </div>
            </div>
        </div>
        
        <div class="module-grid" id="module-grid">
            <!-- 模块卡片将通过JavaScript动态生成 -->
        </div>
    </div>

    <script>
        // 模块数据
        const modules = [
            {
                title: "01-Python基础",
                description: "Python编程的核心概念和基础知识",
                links: [
                    { text: "README", href: "01-Python基础/README.md" },
                    { text: "知识点", href: "01-Python基础/knowledge_checklist.md" },
                    { text: "示例", href: "01-Python基础/examples/" }
                ]
            },
            {
                title: "02-高级特性",
                description: "Python的进阶功能和特性",
                links: [
                    { text: "README", href: "02-高级特性/README.md" },
                    { text: "知识点", href: "02-高级特性/knowledge_checklist.md" },
                    { text: "示例", href: "02-高级特性/examples/" }
                ]
            },
            {
                title: "03-生态系统",
                description: "Python包管理和依赖管理",
                links: [
                    { text: "README", href: "03-生态系统/README.md" },
                    { text: "知识点", href: "03-生态系统/knowledge_checklist.md" },
                    { text: "示例", href: "03-生态系统/examples/" }
                ]
            },
            {
                title: "04-版本特性",
                description: "Python各版本的新特性和变化",
                links: [
                    { text: "README", href: "04-版本特性/README.md" },
                    { text: "知识点", href: "04-版本特性/knowledge_checklist.md" },
                    { text: "示例", href: "04-版本特性/examples/" }
                ]
            },
            {
                title: "05-性能优化",
                description: "Python代码性能优化和内存管理",
                links: [
                    { text: "README", href: "05-性能优化/README.md" },
                    { text: "知识点", href: "05-性能优化/knowledge_checklist.md" },
                    { text: "示例", href: "05-性能优化/examples/" }
                ]
            },
            {
                title: "06-安全编程",
                description: "Python安全编程实践和最佳实践",
                links: [
                    { text: "README", href: "06-安全编程/README.md" },
                    { text: "知识点", href: "06-安全编程/knowledge_checklist.md" },
                    { text: "示例", href: "06-安全编程/examples/" }
                ]
            },
            {
                title: "07-设计模式",
                description: "Python设计模式实现和应用",
                links: [
                    { text: "README", href: "07-设计模式/README.md" },
                    { text: "知识点", href: "07-设计模式/knowledge_checklist.md" },
                    { text: "示例", href: "07-设计模式/examples/" }
                ]
            },
            {
                title: "08-Web开发",
                description: "Python Web开发框架和应用",
                links: [
                    { text: "README", href: "08-Web开发/README.md" },
                    { text: "知识点", href: "08-Web开发/knowledge_checklist.md" },
                    { text: "示例", href: "08-Web开发/examples/" }
                ]
            },
            {
                title: "09-数据科学",
                description: "Python数据科学和机器学习",
                links: [
                    { text: "README", href: "09-数据科学/README.md" },
                    { text: "知识点", href: "09-数据科学/knowledge_checklist.md" },
                    { text: "示例", href: "09-数据科学/examples/" }
                ]
            },
            {
                title: "10-自动化运维",
                description: "Python自动化运维和脚本开发",
                links: [
                    { text: "README", href: "10-自动化运维/README.md" },
                    { text: "知识点", href: "10-自动化运维/knowledge_checklist.md" },
                    { text: "示例", href: "10-自动化运维/examples/" }
                ]
            },
            {
                title: "11-行业应用",
                description: "Python在各行业的应用案例",
                links: [
                    { text: "README", href: "11-行业应用/README.md" },
                    { text: "知识点", href: "11-行业应用/knowledge_checklist.md" },
                    { text: "示例", href: "11-行业应用/examples/" }
                ]
            },
            {
                title: "12-最佳实践",
                description: "Python编程最佳实践和规范",
                links: [
                    { text: "README", href: "12-最佳实践/README.md" },
                    { text: "知识点", href: "12-最佳实践/knowledge_checklist.md" },
                    { text: "示例", href: "12-最佳实践/examples/" }
                ]
            }
        ];

        // 生成模块卡片
        function generateModuleCards() {
            const grid = document.getElementById('module-grid');
            modules.forEach(module => {
                const card = document.createElement('div');
                card.className = 'module-card';
                
                const title = document.createElement('div');
                title.className = 'module-title';
                title.textContent = module.title;
                
                const description = document.createElement('div');
                description.className = 'module-description';
                description.textContent = module.description;
                
                const links = document.createElement('div');
                links.className = 'module-links';
                module.links.forEach(link => {
                    const a = document.createElement('a');
                    a.href = link.href;
                    a.textContent = link.text;
                    links.appendChild(a);
                });
                
                card.appendChild(title);
                card.appendChild(description);
                card.appendChild(links);
                grid.appendChild(card);
            });
        }

        // 更新统计信息
        function updateStats() {
            document.getElementById('total-modules').textContent = modules.length;
            document.getElementById('total-files').textContent = modules.length * 3; // 估算
            document.getElementById('total-examples').textContent = modules.length * 2; // 估算
            document.getElementById('completion-rate').textContent = '85%'; // 估算
        }

        // 初始化页面
        document.addEventListener('DOMContentLoaded', function() {
            generateModuleCards();
            updateStats();
        });
    </script>
</body>
</html>'''

    with open('python_knowledge_system_index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML索引页面已生成: python_knowledge_system_index.html")

def generate_json_api():
    """生成JSON API数据"""
    api_data = {
        "system_info": {
            "name": "Python知识体系",
            "version": "1.0.0",
            "description": "完整的Python知识体系结构",
            "last_updated": "2024-12-19"
        },
        "modules": [
            {
                "id": "01",
                "name": "Python基础",
                "path": "01-Python基础",
                "description": "Python编程的核心概念和基础知识",
                "topics": ["语法基础", "数据类型", "控制流", "函数编程"],
                "files": ["README.md", "knowledge_checklist.md", "examples/"]
            },
            {
                "id": "02",
                "name": "高级特性",
                "path": "02-高级特性",
                "description": "Python的进阶功能和特性",
                "topics": ["面向对象", "装饰器", "生成器", "上下文管理"],
                "files": ["README.md", "knowledge_checklist.md", "examples/"]
            }
        ],
        "statistics": {
            "total_modules": 12,
            "total_files": 36,
            "total_examples": 24,
            "completion_rate": 85
        }
    }
    
    with open('python_knowledge_system_api.json', 'w', encoding='utf-8') as f:
        json.dump(api_data, f, ensure_ascii=False, indent=2)
    
    print("✅ JSON API数据已生成: python_knowledge_system_api.json")

def main():
    """主函数"""
    print("🔄 生成Web可视化...")
    generate_html_index()
    generate_json_api()
    print("🎉 Web可视化生成完成！")

if __name__ == "__main__":
    main() 