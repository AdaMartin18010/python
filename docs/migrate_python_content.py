#!/usr/bin/env python3
"""
Python知识体系迁移脚本

此脚本用于将现有的Python相关内容重新组织为清晰的Python学习路径。
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PythonContentMigrator:
    """Python内容迁移器"""
    
    def __init__(self, base_path: str = "docs"):
        self.base_path = Path(base_path)
        self.new_structure = "python_knowledge"
        self.backup_path = f"docs_backup_{self._get_timestamp()}"
        
        # 定义新的目录结构
        self.directory_structure = {
            "01-Python基础": [],
            "02-Python高级特性": [],
            "03-Python生态系统": [
                "03-01-Python包管理工具",
                "03-02-Python开发工具", 
                "03-03-Python测试框架",
                "03-04-Python文档工具"
            ],
            "04-Python版本特性": [],
            "05-Python性能优化": [],
            "06-Python安全编程": [],
            "07-Python设计模式": [
                "07-01-创建型模式",
                "07-02-结构型模式", 
                "07-03-行为型模式"
            ],
            "08-Python Web开发": [
                "08-01-Web框架",
                "08-02-API开发",
                "08-03-数据库集成",
                "08-04-部署运维"
            ],
            "09-Python数据科学": [
                "09-01-数据处理",
                "09-02-机器学习",
                "09-03-深度学习", 
                "09-04-大数据处理"
            ],
            "10-Python自动化运维": [
                "10-01-系统管理",
                "10-02-DevOps工具",
                "10-03-监控告警",
                "10-04-云原生"
            ],
            "11-Python行业应用": [
                "11-01-金融科技",
                "11-02-人工智能",
                "11-03-物联网",
                "11-04-游戏开发",
                "11-05-其他行业"
            ],
            "12-Python最佳实践": [
                "12-01-代码质量",
                "12-02-项目管理", 
                "12-03-团队协作",
                "12-04-持续改进"
            ]
        }
        
        # 定义文件迁移映射
        self.file_mapping = {
            # 核心Python文档
            "python_best_practices_2025.md": "12-Python最佳实践/12-01-代码质量/",
            "python_documentation_summary.md": "03-Python生态系统/03-04-Python文档工具/",
            "python_ecosystem_maturity.md": "03-Python生态系统/",
            "python_ml_best_practices.md": "09-Python数据科学/09-02-机器学习/",
            "python_new_features.md": "04-Python版本特性/",
            "python_performance_optimization.md": "05-Python性能优化/",
            "python_project_management.md": "03-Python生态系统/03-01-Python包管理工具/",
            "python_security_guide.md": "06-Python安全编程/",
            "python_tech_stack_2025.md": "03-Python生态系统/",
            
            # Python语义模型
            "11-01-Python语义基础.md": "02-Python高级特性/",
            "11-02-Python语义分析.md": "02-Python高级特性/",
            "11-03-Python语义实现.md": "02-Python高级特性/",
            "11-04-Python语义模型总结.md": "02-Python高级特性/",
            "11-05-Python语义形式化证明.md": "02-Python高级特性/",
            "11-06-Python语义高级证明.md": "02-Python高级特性/",
            "11-07-Python语义完整证明.md": "02-Python高级特性/",
        }
        
        # 定义目录迁移映射
        self.dir_mapping = {
            "dp1_creational_patterns": "07-Python设计模式/07-01-创建型模式/",
            "dp2_structural_patterns": "07-Python设计模式/07-02-结构型模式/",
            "dp3_behavioral_patterns": "07-Python设计模式/07-03-行为型模式/",
            "ai_ml": "11-Python行业应用/11-02-人工智能/",
            "fintech": "11-Python行业应用/11-01-金融科技/",
            "big_data_analytics": "09-Python数据科学/09-04-大数据处理/",
        }
        
        # 需要移除的内容
        self.to_remove = [
            "rust/",
            "lang_compare/",
            "software/",
            "00-理念基础/",
            "01-形式科学/",
            "02-理论基础/",
            "09-递归极限理论/",
            "10-超递归理论/",
        ]

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def create_backup(self) -> None:
        """创建备份"""
        logger.info("创建备份...")
        if self.base_path.exists():
            shutil.copytree(self.base_path, self.backup_path)
            logger.info(f"备份已创建: {self.backup_path}")

    def create_directory_structure(self) -> None:
        """创建新的目录结构"""
        logger.info("创建新的目录结构...")
        
        new_base = self.base_path / self.new_structure
        new_base.mkdir(exist_ok=True)
        
        for main_dir, sub_dirs in self.directory_structure.items():
            main_path = new_base / main_dir
            main_path.mkdir(exist_ok=True)
            
            for sub_dir in sub_dirs:
                sub_path = main_path / sub_dir
                sub_path.mkdir(exist_ok=True)
                
        logger.info("目录结构创建完成")

    def migrate_files(self) -> None:
        """迁移文件"""
        logger.info("开始迁移文件...")
        
        new_base = self.base_path / self.new_structure
        
        # 迁移核心Python文档
        source_dir = self.base_path / "model" / "Programming_Language"
        if source_dir.exists():
            for file_pattern, target_dir in self.file_mapping.items():
                if file_pattern.startswith("python_"):
                    source_files = list(source_dir.glob(f"{file_pattern}"))
                    for source_file in source_files:
                        target_path = new_base / target_dir / source_file.name
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_file, target_path)
                        logger.info(f"迁移文件: {source_file} -> {target_path}")

        # 迁移Python语义模型
        semantic_dir = self.base_path / "refactor" / "11-Python语义模型"
        if semantic_dir.exists():
            for file_pattern, target_dir in self.file_mapping.items():
                if file_pattern.startswith("11-"):
                    source_files = list(semantic_dir.glob(f"{file_pattern}"))
                    for source_file in source_files:
                        target_path = new_base / target_dir / source_file.name
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_file, target_path)
                        logger.info(f"迁移文件: {source_file} -> {target_path}")
            
            # 迁移Python代码文件
            for py_file in semantic_dir.glob("*.py"):
                target_path = new_base / "02-Python高级特性" / py_file.name
                shutil.copy2(py_file, target_path)
                logger.info(f"迁移代码文件: {py_file} -> {target_path}")

    def migrate_directories(self) -> None:
        """迁移目录"""
        logger.info("开始迁移目录...")
        
        new_base = self.base_path / self.new_structure
        
        # 迁移设计模式
        design_pattern_dir = self.base_path / "model" / "Design_Pattern"
        if design_pattern_dir.exists():
            for source_dir, target_dir in self.dir_mapping.items():
                if source_dir.startswith("dp"):
                    source_path = design_pattern_dir / source_dir
                    if source_path.exists():
                        target_path = new_base / target_dir
                        target_path.mkdir(parents=True, exist_ok=True)
                        
                        # 复制目录内容
                        for item in source_path.iterdir():
                            if item.is_file():
                                shutil.copy2(item, target_path / item.name)
                            elif item.is_dir():
                                shutil.copytree(item, target_path / item.name)
                        
                        logger.info(f"迁移目录: {source_path} -> {target_path}")

        # 迁移行业应用
        industry_dir = self.base_path / "model" / "industry_domains"
        if industry_dir.exists():
            for source_dir, target_dir in self.dir_mapping.items():
                if not source_dir.startswith("dp"):
                    source_path = industry_dir / source_dir
                    if source_path.exists():
                        target_path = new_base / target_dir
                        target_path.mkdir(parents=True, exist_ok=True)
                        
                        # 复制目录内容
                        for item in source_path.iterdir():
                            if item.is_file():
                                shutil.copy2(item, target_path / item.name)
                            elif item.is_dir():
                                shutil.copytree(item, target_path / item.name)
                        
                        logger.info(f"迁移目录: {source_path} -> {target_path}")

    def update_links(self) -> None:
        """更新文档中的链接"""
        logger.info("更新文档链接...")
        
        new_base = self.base_path / self.new_structure
        
        # 遍历所有markdown文件
        for md_file in new_base.rglob("*.md"):
            if md_file.is_file():
                self._update_file_links(md_file)

    def _update_file_links(self, file_path: Path) -> None:
        """更新单个文件中的链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新相对路径链接
            updated_content = self._update_relative_links(content, file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
                
        except Exception as e:
            logger.warning(f"更新链接失败 {file_path}: {e}")

    def _update_relative_links(self, content: str, file_path: Path) -> str:
        """更新相对链接"""
        # 这里可以添加更复杂的链接更新逻辑
        # 目前只是简单的占位符
        return content

    def create_navigation_files(self) -> None:
        """创建导航文件"""
        logger.info("创建导航文件...")
        
        new_base = self.base_path / self.new_structure
        
        # 创建README.md
        readme_content = self._generate_readme()
        readme_path = new_base / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 创建SUMMARY.md
        summary_content = self._generate_summary()
        summary_path = new_base / "SUMMARY.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        logger.info("导航文件创建完成")

    def _generate_readme(self) -> str:
        """生成README内容"""
        return """# Python知识体系

## 📚 概述

这是一个完整的Python编程语言知识体系，涵盖了从基础语法到高级应用的所有方面。

## 🎯 学习路径

### 初学者路径
1. **Python基础** - 掌握Python基本语法和概念
2. **Python生态系统** - 了解Python工具链和开发环境
3. **Python版本特性** - 学习最新Python特性
4. **Python最佳实践** - 掌握编程规范和最佳实践

### 进阶开发者路径
1. **Python高级特性** - 深入学习Python高级概念
2. **Python性能优化** - 掌握性能优化技巧
3. **Python设计模式** - 学习设计模式在Python中的应用
4. **Python安全编程** - 掌握安全编程实践

### 专业领域路径
- **Web开发**: Python Web开发 + Python最佳实践
- **数据科学**: Python数据科学 + Python性能优化
- **自动化运维**: Python自动化运维 + Python性能优化
- **行业应用**: Python行业应用 + Python设计模式

## 📁 目录结构

详细目录结构请参考各章节文档。

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个知识体系。

## 📄 许可证

本项目采用MIT许可证。
"""

    def _generate_summary(self) -> str:
        """生成SUMMARY内容"""
        summary = """# Summary

* [Python知识体系](README.md)

## 01. Python基础

* [Python语法基础](01-Python基础/01-01-Python语法基础.md)
* [Python数据类型](01-Python基础/01-02-Python数据类型.md)
* [Python控制流](01-Python基础/01-03-Python控制流.md)
* [Python函数编程](01-Python基础/01-04-Python函数编程.md)
* [Python面向对象](01-Python基础/01-05-Python面向对象.md)
* [Python模块包管理](01-Python基础/01-06-Python模块包管理.md)
* [Python异常处理](01-Python基础/01-07-Python异常处理.md)

## 02. Python高级特性

* [Python装饰器](02-Python高级特性/02-01-Python装饰器.md)
* [Python生成器迭代器](02-Python高级特性/02-02-Python生成器迭代器.md)
* [Python上下文管理器](02-Python高级特性/02-03-Python上下文管理器.md)
* [Python元类编程](02-Python高级特性/02-04-Python元类编程.md)
* [Python描述符协议](02-Python高级特性/02-05-Python描述符协议.md)
* [Python类型注解](02-Python高级特性/02-06-Python类型注解.md)
* [Python异步编程](02-Python高级特性/02-07-Python异步编程.md)

## 03. Python生态系统

### 03-01. Python包管理工具

* [pip使用指南](03-Python生态系统/03-01-Python包管理工具/pip使用指南.md)
* [poetry项目管理](03-Python生态系统/03-01-Python包管理工具/poetry项目管理.md)
* [uv构建工具](03-Python生态系统/03-01-Python包管理工具/uv构建工具.md)
* [conda环境管理](03-Python生态系统/03-01-Python包管理工具/conda环境管理.md)

### 03-02. Python开发工具

* [IDE配置指南](03-Python生态系统/03-02-Python开发工具/IDE配置指南.md)
* [调试技巧](03-Python生态系统/03-02-Python开发工具/调试技巧.md)
* [代码格式化](03-Python生态系统/03-02-Python开发工具/代码格式化.md)
* [静态类型检查](03-Python生态系统/03-02-Python开发工具/静态类型检查.md)

### 03-03. Python测试框架

* [pytest使用指南](03-Python生态系统/03-03-Python测试框架/pytest使用指南.md)
* [unittest框架](03-Python生态系统/03-03-Python测试框架/unittest框架.md)
* [测试策略](03-Python生态系统/03-03-Python测试框架/测试策略.md)
* [测试覆盖率](03-Python生态系统/03-03-Python测试框架/测试覆盖率.md)

### 03-04. Python文档工具

* [Sphinx文档生成](03-Python生态系统/03-04-Python文档工具/Sphinx文档生成.md)
* [docstring规范](03-Python生态系统/03-04-Python文档工具/docstring规范.md)
* [API文档编写](03-Python生态系统/03-04-Python文档工具/API文档编写.md)

## 04. Python版本特性

* [Python3.10新特性](04-Python版本特性/04-01-Python3.10新特性.md)
* [Python3.11新特性](04-Python版本特性/04-02-Python3.11新特性.md)
* [Python3.12新特性](04-Python版本特性/04-03-Python3.12新特性.md)
* [Python3.13新特性](04-Python版本特性/04-04-Python3.13新特性.md)
* [PEP提案解读](04-Python版本特性/04-05-PEP提案解读.md)
* [版本迁移指南](04-Python版本特性/04-06-版本迁移指南.md)

## 05. Python性能优化

* [性能分析工具](05-Python性能优化/05-01-性能分析工具.md)
* [内存优化](05-Python性能优化/05-02-内存优化.md)
* [算法优化](05-Python性能优化/05-03-算法优化.md)
* [并发编程](05-Python性能优化/05-04-并发编程.md)
* [异步IO优化](05-Python性能优化/05-05-异步IO优化.md)
* [扩展模块开发](05-Python性能优化/05-06-扩展模块开发.md)

## 06. Python安全编程

* [输入验证](06-Python安全编程/06-01-输入验证.md)
* [SQL注入防护](06-Python安全编程/06-02-SQL注入防护.md)
* [XSS防护](06-Python安全编程/06-03-XSS防护.md)
* [密码安全](06-Python安全编程/06-04-密码安全.md)
* [加密解密](06-Python安全编程/06-05-加密解密.md)
* [安全最佳实践](06-Python安全编程/06-06-安全最佳实践.md)

## 07. Python设计模式

### 07-01. 创建型模式

* [单例模式](07-Python设计模式/07-01-创建型模式/单例模式.md)
* [工厂模式](07-Python设计模式/07-01-创建型模式/工厂模式.md)
* [建造者模式](07-Python设计模式/07-01-创建型模式/建造者模式.md)
* [原型模式](07-Python设计模式/07-01-创建型模式/原型模式.md)

### 07-02. 结构型模式

* [适配器模式](07-Python设计模式/07-02-结构型模式/适配器模式.md)
* [装饰器模式](07-Python设计模式/07-02-结构型模式/装饰器模式.md)
* [代理模式](07-Python设计模式/07-02-结构型模式/代理模式.md)
* [组合模式](07-Python设计模式/07-02-结构型模式/组合模式.md)

### 07-03. 行为型模式

* [观察者模式](07-Python设计模式/07-03-行为型模式/观察者模式.md)
* [策略模式](07-Python设计模式/07-03-行为型模式/策略模式.md)
* [命令模式](07-Python设计模式/07-03-行为型模式/命令模式.md)
* [状态模式](07-Python设计模式/07-03-行为型模式/状态模式.md)

## 08. Python Web开发

### 08-01. Web框架

* [Django框架](08-Python Web开发/08-01-Web框架/Django框架.md)
* [Flask框架](08-Python Web开发/08-01-Web框架/Flask框架.md)
* [FastAPI框架](08-Python Web开发/08-01-Web框架/FastAPI框架.md)
* [Tornado框架](08-Python Web开发/08-01-Web框架/Tornado框架.md)

### 08-02. API开发

* [RESTful API设计](08-Python Web开发/08-02-API开发/RESTful API设计.md)
* [GraphQL API](08-Python Web开发/08-02-API开发/GraphQL API.md)
* [API文档生成](08-Python Web开发/08-02-API开发/API文档生成.md)
* [API测试策略](08-Python Web开发/08-02-API开发/API测试策略.md)

### 08-03. 数据库集成

* [SQLAlchemy ORM](08-Python Web开发/08-03-数据库集成/SQLAlchemy ORM.md)
* [Django ORM](08-Python Web开发/08-03-数据库集成/Django ORM.md)
* [数据库迁移](08-Python Web开发/08-03-数据库集成/数据库迁移.md)
* [数据库优化](08-Python Web开发/08-03-数据库集成/数据库优化.md)

### 08-04. 部署运维

* [Docker容器化](08-Python Web开发/08-04-部署运维/Docker容器化.md)
* [云平台部署](08-Python Web开发/08-04-部署运维/云平台部署.md)
* [性能监控](08-Python Web开发/08-04-部署运维/性能监控.md)
* [日志管理](08-Python Web开发/08-04-部署运维/日志管理.md)

## 09. Python数据科学

### 09-01. 数据处理

* [pandas数据分析](09-Python数据科学/09-01-数据处理/pandas数据分析.md)
* [numpy数值计算](09-Python数据科学/09-01-数据处理/numpy数值计算.md)
* [数据清洗](09-Python数据科学/09-01-数据处理/数据清洗.md)
* [数据可视化](09-Python数据科学/09-01-数据处理/数据可视化.md)

### 09-02. 机器学习

* [scikit-learn使用](09-Python数据科学/09-02-机器学习/scikit-learn使用.md)
* [特征工程](09-Python数据科学/09-02-机器学习/特征工程.md)
* [模型评估](09-Python数据科学/09-02-机器学习/模型评估.md)
* [模型部署](09-Python数据科学/09-02-机器学习/模型部署.md)

### 09-03. 深度学习

* [TensorFlow使用](09-Python数据科学/09-03-深度学习/TensorFlow使用.md)
* [PyTorch使用](09-Python数据科学/09-03-深度学习/PyTorch使用.md)
* [神经网络构建](09-Python数据科学/09-03-深度学习/神经网络构建.md)
* [模型训练优化](09-Python数据科学/09-03-深度学习/模型训练优化.md)

### 09-04. 大数据处理

* [Spark集成](09-Python数据科学/09-04-大数据处理/Spark集成.md)
* [Dask并行计算](09-Python数据科学/09-04-大数据处理/Dask并行计算.md)
* [流数据处理](09-Python数据科学/09-04-大数据处理/流数据处理.md)
* [分布式计算](09-Python数据科学/09-04-大数据处理/分布式计算.md)

## 10. Python自动化运维

### 10-01. 系统管理

* [文件系统操作](10-Python自动化运维/10-01-系统管理/文件系统操作.md)
* [进程管理](10-Python自动化运维/10-01-系统管理/进程管理.md)
* [网络编程](10-Python自动化运维/10-01-系统管理/网络编程.md)
* [系统监控](10-Python自动化运维/10-01-系统管理/系统监控.md)

### 10-02. DevOps工具

* [Ansible自动化](10-Python自动化运维/10-02-DevOps工具/Ansible自动化.md)
* [SaltStack配置](10-Python自动化运维/10-02-DevOps工具/SaltStack配置.md)
* [CI/CD流水线](10-Python自动化运维/10-02-DevOps工具/CI_CD流水线.md)
* [容器编排](10-Python自动化运维/10-02-DevOps工具/容器编排.md)

### 10-03. 监控告警

* [日志收集](10-Python自动化运维/10-03-监控告警/日志收集.md)
* [指标监控](10-Python自动化运维/10-03-监控告警/指标监控.md)
* [告警系统](10-Python自动化运维/10-03-监控告警/告警系统.md)
* [故障排查](10-Python自动化运维/10-03-监控告警/故障排查.md)

### 10-04. 云原生

* [Kubernetes集成](10-Python自动化运维/10-04-云原生/Kubernetes集成.md)
* [微服务架构](10-Python自动化运维/10-04-云原生/微服务架构.md)
* [服务网格](10-Python自动化运维/10-04-云原生/服务网格.md)
* [云函数开发](10-Python自动化运维/10-04-云原生/云函数开发.md)

## 11. Python行业应用

### 11-01. 金融科技

* [量化交易](11-Python行业应用/11-01-金融科技/量化交易.md)
* [风险管理](11-Python行业应用/11-01-金融科技/风险管理.md)
* [区块链开发](11-Python行业应用/11-01-金融科技/区块链开发.md)
* [支付系统](11-Python行业应用/11-01-金融科技/支付系统.md)

### 11-02. 人工智能

* [自然语言处理](11-Python行业应用/11-02-人工智能/自然语言处理.md)
* [计算机视觉](11-Python行业应用/11-02-人工智能/计算机视觉.md)
* [推荐系统](11-Python行业应用/11-02-人工智能/推荐系统.md)
* [智能对话](11-Python行业应用/11-02-人工智能/智能对话.md)

### 11-03. 物联网

* [设备通信](11-Python行业应用/11-03-物联网/设备通信.md)
* [数据采集](11-Python行业应用/11-03-物联网/数据采集.md)
* [边缘计算](11-Python行业应用/11-03-物联网/边缘计算.md)
* [智能家居](11-Python行业应用/11-03-物联网/智能家居.md)

### 11-04. 游戏开发

* [Pygame使用](11-Python行业应用/11-04-游戏开发/Pygame使用.md)
* [游戏引擎](11-Python行业应用/11-04-游戏开发/游戏引擎.md)
* [物理引擎](11-Python行业应用/11-04-游戏开发/物理引擎.md)
* [网络游戏](11-Python行业应用/11-04-游戏开发/网络游戏.md)

### 11-05. 其他行业

* [医疗健康](11-Python行业应用/11-05-其他行业/医疗健康.md)
* [教育科技](11-Python行业应用/11-05-其他行业/教育科技.md)
* [电子商务](11-Python行业应用/11-05-其他行业/电子商务.md)
* [汽车工业](11-Python行业应用/11-05-其他行业/汽车工业.md)

## 12. Python最佳实践

### 12-01. 代码质量

* [代码规范](12-Python最佳实践/12-01-代码质量/代码规范.md)
* [代码审查](12-Python最佳实践/12-01-代码质量/代码审查.md)
* [重构技巧](12-Python最佳实践/12-01-代码质量/重构技巧.md)
* [技术债务管理](12-Python最佳实践/12-01-代码质量/技术债务管理.md)

### 12-02. 项目管理

* [项目结构](12-Python最佳实践/12-02-项目管理/项目结构.md)
* [依赖管理](12-Python最佳实践/12-02-项目管理/依赖管理.md)
* [版本控制](12-Python最佳实践/12-02-项目管理/版本控制.md)
* [发布流程](12-Python最佳实践/12-02-项目管理/发布流程.md)

### 12-03. 团队协作

* [代码规范](12-Python最佳实践/12-03-团队协作/代码规范.md)
* [文档编写](12-Python最佳实践/12-03-团队协作/文档编写.md)
* [知识分享](12-Python最佳实践/12-03-团队协作/知识分享.md)
* [代码审查](12-Python最佳实践/12-03-团队协作/代码审查.md)

### 12-04. 持续改进

* [性能监控](12-Python最佳实践/12-04-持续改进/性能监控.md)
* [错误追踪](12-Python最佳实践/12-04-持续改进/错误追踪.md)
* [用户反馈](12-Python最佳实践/12-04-持续改进/用户反馈.md)
* [技术选型](12-Python最佳实践/12-04-持续改进/技术选型.md)
"""
        return summary

    def cleanup_old_content(self) -> None:
        """清理旧内容"""
        logger.info("清理旧内容...")
        
        # 这里可以添加清理逻辑
        # 注意：在实际执行前应该谨慎处理
        logger.warning("清理功能需要手动确认，请谨慎操作")

    def run_migration(self) -> None:
        """执行完整的迁移流程"""
        logger.info("开始Python内容迁移...")
        
        try:
            # 1. 创建备份
            self.create_backup()
            
            # 2. 创建新目录结构
            self.create_directory_structure()
            
            # 3. 迁移文件
            self.migrate_files()
            
            # 4. 迁移目录
            self.migrate_directories()
            
            # 5. 更新链接
            self.update_links()
            
            # 6. 创建导航文件
            self.create_navigation_files()
            
            logger.info("迁移完成！")
            logger.info(f"新结构位置: {self.base_path / self.new_structure}")
            logger.info(f"备份位置: {self.backup_path}")
            
        except Exception as e:
            logger.error(f"迁移过程中出现错误: {e}")
            raise

def main():
    """主函数"""
    migrator = PythonContentMigrator()
    
    print("Python知识体系迁移工具")
    print("=" * 50)
    print("此工具将帮助您重新组织Python相关内容")
    print("请确保您已经备份了重要数据")
    print()
    
    response = input("是否继续执行迁移？(y/N): ")
    if response.lower() == 'y':
        migrator.run_migration()
    else:
        print("迁移已取消")

if __name__ == "__main__":
    main() 