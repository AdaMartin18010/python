#!/usr/bin/env python3
"""
高级构建示例
展示现代Python项目的构建、打包和发布流程
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import zipfile
import tarfile

@dataclass
class BuildConfig:
    """构建配置"""
    project_name: str
    version: str
    description: str
    author: str
    author_email: str
    license: str
    python_requires: str
    classifiers: List[str]
    dependencies: List[str]
    dev_dependencies: List[str]
    entry_points: Dict[str, str]
    package_data: Dict[str, List[str]]
    data_files: List[tuple]

class ProjectBuilder:
    """项目构建器"""
    
    def __init__(self, config: BuildConfig):
        self.config = config
        self.project_dir = Path.cwd()
        self.build_dir = self.project_dir / "build"
        self.dist_dir = self.project_dir / "dist"
        self.src_dir = self.project_dir / "src"
        self.tests_dir = self.project_dir / "tests"
        self.docs_dir = self.project_dir / "docs"
    
    def create_project_structure(self):
        """创建项目结构"""
        print("创建项目结构...")
        
        # 创建目录
        directories = [
            self.src_dir / self.config.project_name,
            self.tests_dir,
            self.docs_dir,
            self.build_dir,
            self.dist_dir,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {directory}")
        
        # 创建__init__.py文件
        init_file = self.src_dir / self.config.project_name / "__init__.py"
        init_file.write_text(f'"""\n{self.config.description}\n"""\n\n__version__ = "{self.config.version}"\n')
        print(f"创建文件: {init_file}")
    
    def create_pyproject_toml(self):
        """创建pyproject.toml文件"""
        print("创建pyproject.toml...")
        
        pyproject_content = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{self.config.project_name}"
version = "{self.config.version}"
description = "{self.config.description}"
readme = "README.md"
requires-python = "{self.config.python_requires}"
license = {{text = "{self.config.license}"}}
authors = [
    {{name = "{self.config.author}", email = "{self.config.author_email}"}},
]
keywords = ["python", "package"]
classifiers = {json.dumps(self.config.classifiers, indent=2)}
dependencies = {json.dumps(self.config.dependencies, indent=2)}

[project.optional-dependencies]
dev = {json.dumps(self.config.dev_dependencies, indent=2)}
test = [
    "pytest>=6.0",
    "pytest-cov",
    "pytest-mock",
    "pytest-xdist",
]

[project.scripts]
{self._format_entry_points()}

[project.urls]
Homepage = "https://github.com/user/{self.config.project_name}"
Documentation = "https://{self.config.project_name}.readthedocs.io"
Repository = "https://github.com/user/{self.config.project_name}.git"
"Bug Tracker" = "https://github.com/user/{self.config.project_name}/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/{self.config.project_name}"]

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/tests",
    "/docs",
    "/README.md",
    "/LICENSE",
    "/CHANGELOG.md",
]

[tool.hatch.version]
path = "src/{self.config.project_name}/__init__.py"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
]

[tool.black]
line-length = 88
target-version = ['py38']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["{self.config.project_name}"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
'''
        
        pyproject_file = self.project_dir / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)
        print(f"创建文件: {pyproject_file}")
    
    def _format_entry_points(self) -> str:
        """格式化入口点"""
        if not self.config.entry_points:
            return ""
        
        lines = []
        for name, path in self.config.entry_points.items():
            lines.append(f'{name} = "{path}"')
        return "\n".join(lines)
    
    def create_readme(self):
        """创建README.md文件"""
        print("创建README.md...")
        
        readme_content = f'''# {self.config.project_name}

{self.config.description}

## 安装

```bash
pip install {self.config.project_name}
```

## 使用方法

```python
import {self.config.project_name}

# 示例代码
```

## 开发

```bash
# 克隆仓库
git clone https://github.com/user/{self.config.project_name}.git
cd {self.config.project_name}

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black .
isort .

# 类型检查
mypy src/
```

## 许可证

{self.config.license}
'''
        
        readme_file = self.project_dir / "README.md"
        readme_file.write_text(readme_content)
        print(f"创建文件: {readme_file}")
    
    def create_license(self):
        """创建LICENSE文件"""
        print("创建LICENSE...")
        
        if self.config.license == "MIT":
            license_content = f'''MIT License

Copyright (c) {datetime.now().year} {self.config.author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
        else:
            license_content = f"License: {self.config.license}"
        
        license_file = self.project_dir / "LICENSE"
        license_file.write_text(license_content)
        print(f"创建文件: {license_file}")
    
    def create_changelog(self):
        """创建CHANGELOG.md文件"""
        print("创建CHANGELOG.md...")
        
        changelog_content = f'''# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 初始版本

## [{self.config.version}] - {datetime.now().strftime('%Y-%m-%d')}

### Added
- 初始版本发布
'''
        
        changelog_file = self.project_dir / "CHANGELOG.md"
        changelog_file.write_text(changelog_content)
        print(f"创建文件: {changelog_file}")
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        print("创建.gitignore...")
        
        gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
'''
        
        gitignore_file = self.project_dir / ".gitignore"
        gitignore_file.write_text(gitignore_content)
        print(f"创建文件: {gitignore_file}")
    
    def create_pre_commit_config(self):
        """创建.pre-commit-config.yaml文件"""
        print("创建.pre-commit-config.yaml...")
        
        pre_commit_content = '''repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]
'''
        
        pre_commit_file = self.project_dir / ".pre-commit-config.yaml"
        pre_commit_file.write_text(pre_commit_content)
        print(f"创建文件: {pre_commit_file}")
    
    def create_github_workflows(self):
        """创建GitHub Actions工作流"""
        print("创建GitHub Actions工作流...")
        
        workflows_dir = self.project_dir / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # CI工作流
        ci_content = f'''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{{{ matrix.python-version }}}}
      uses: actions/setup-python@v5
      with:
        python-version: ${{{{ matrix.python-version }}}}
    
    - name: Install uv
      run: pipx install uv
    
    - name: Install dependencies
      run: |
        uv pip install -e ".[dev,test]"
    
    - name: Lint with flake8
      run: |
        flake8 src/ tests/
    
    - name: Type check with mypy
      run: |
        mypy src/
    
    - name: Test with pytest
      run: |
        pytest --cov=src --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
'''
        
        ci_file = workflows_dir / "ci.yml"
        ci_file.write_text(ci_content)
        print(f"创建文件: {ci_file}")
        
        # 发布工作流
        release_content = f'''name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install uv
      run: pipx install uv
    
    - name: Install dependencies
      run: |
        uv pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{{{ secrets.PYPI_API_TOKEN }}}}
      run: twine upload dist/*
'''
        
        release_file = workflows_dir / "release.yml"
        release_file.write_text(release_content)
        print(f"创建文件: {release_file}")
    
    def create_dockerfile(self):
        """创建Dockerfile"""
        print("创建Dockerfile...")
        
        dockerfile_content = f'''FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app
USER app

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "{self.config.project_name}"]
'''
        
        dockerfile = self.project_dir / "Dockerfile"
        dockerfile.write_text(dockerfile_content)
        print(f"创建文件: {dockerfile}")
    
    def create_docker_compose(self):
        """创建docker-compose.yml"""
        print("创建docker-compose.yml...")
        
        docker_compose_content = f'''version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
    volumes:
      - .:/app
    command: python -m {self.config.project_name}

  test:
    build: .
    environment:
      - PYTHONPATH=/app
    volumes:
      - .:/app
    command: pytest tests/ -v

  lint:
    build: .
    environment:
      - PYTHONPATH=/app
    volumes:
      - .:/app
    command: flake8 src/ tests/
'''
        
        docker_compose_file = self.project_dir / "docker-compose.yml"
        docker_compose_file.write_text(docker_compose_content)
        print(f"创建文件: {docker_compose_file}")
    
    def create_requirements_files(self):
        """创建requirements文件"""
        print("创建requirements文件...")
        
        # requirements.txt
        requirements_content = "\n".join(self.config.dependencies)
        requirements_file = self.project_dir / "requirements.txt"
        requirements_file.write_text(requirements_content)
        print(f"创建文件: {requirements_file}")
        
        # requirements-dev.txt
        dev_requirements = self.config.dependencies + self.config.dev_dependencies
        dev_requirements_content = "\n".join(dev_requirements)
        dev_requirements_file = self.project_dir / "requirements-dev.txt"
        dev_requirements_file.write_text(dev_requirements_content)
        print(f"创建文件: {dev_requirements_file}")
    
    def build_package(self):
        """构建包"""
        print("构建包...")
        
        try:
            # 清理构建目录
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
            if self.dist_dir.exists():
                shutil.rmtree(self.dist_dir)
            
            # 运行构建命令
            result = subprocess.run(
                [sys.executable, "-m", "build"],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("构建成功!")
                print("构建输出:")
                print(result.stdout)
            else:
                print("构建失败!")
                print("错误输出:")
                print(result.stderr)
                return False
            
            return True
            
        except Exception as e:
            print(f"构建过程中出现错误: {e}")
            return False
    
    def generate_checksums(self):
        """生成校验和"""
        print("生成校验和...")
        
        checksums = {}
        
        for file_path in self.dist_dir.glob("*"):
            if file_path.is_file():
                with open(file_path, 'rb') as f:
                    content = f.read()
                    sha256_hash = hashlib.sha256(content).hexdigest()
                    checksums[file_path.name] = sha256_hash
        
        checksums_file = self.dist_dir / "checksums.txt"
        with open(checksums_file, 'w') as f:
            for filename, checksum in checksums.items():
                f.write(f"{checksum}  {filename}\n")
        
        print(f"校验和文件: {checksums_file}")
        return checksums
    
    def create_sbom(self):
        """创建软件物料清单"""
        print("创建SBOM...")
        
        sbom = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "version": 1,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "tools": [
                    {
                        "vendor": "Python",
                        "name": "Build System",
                        "version": "1.0.0"
                    }
                ],
                "component": {
                    "type": "application",
                    "name": self.config.project_name,
                    "version": self.config.version,
                    "description": self.config.description,
                    "licenses": [{"id": self.config.license}],
                    "purl": f"pkg:pypi/{self.config.project_name}@{self.config.version}"
                }
            },
            "components": []
        }
        
        # 添加依赖组件
        for dep in self.config.dependencies:
            component = {
                "type": "library",
                "name": dep.split(">=")[0].split("==")[0],
                "purl": f"pkg:pypi/{dep.split('>=')[0].split('==')[0]}"
            }
            sbom["components"].append(component)
        
        sbom_file = self.dist_dir / "sbom.json"
        with open(sbom_file, 'w') as f:
            json.dump(sbom, f, indent=2)
        
        print(f"SBOM文件: {sbom_file}")
        return sbom
    
    def build_all(self):
        """执行完整构建流程"""
        print("开始完整构建流程...")
        
        # 创建项目结构
        self.create_project_structure()
        
        # 创建配置文件
        self.create_pyproject_toml()
        self.create_readme()
        self.create_license()
        self.create_changelog()
        self.create_gitignore()
        self.create_pre_commit_config()
        self.create_github_workflows()
        self.create_dockerfile()
        self.create_docker_compose()
        self.create_requirements_files()
        
        # 构建包
        if self.build_package():
            # 生成校验和
            self.generate_checksums()
            
            # 创建SBOM
            self.create_sbom()
            
            print("构建流程完成!")
            return True
        else:
            print("构建流程失败!")
            return False

def main():
    """主函数"""
    # 构建配置
    config = BuildConfig(
        project_name="advanced_build_example",
        version="0.1.0",
        description="高级构建示例项目",
        author="示例作者",
        author_email="author@example.com",
        license="MIT",
        python_requires=">=3.8",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
        ],
        dependencies=[
            "requests>=2.25.0",
            "click>=8.0.0",
        ],
        dev_dependencies=[
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "isort",
            "mypy",
            "flake8",
            "pre-commit",
        ],
        entry_points={
            "console_scripts": [
                "advanced-build=advanced_build_example.cli:main",
            ],
        },
        package_data={
            "advanced_build_example": ["data/*.json", "templates/*.html"],
        },
        data_files=[
            ("share/advanced_build_example", ["config/default.conf"]),
        ],
    )
    
    # 创建构建器并执行构建
    builder = ProjectBuilder(config)
    success = builder.build_all()
    
    if success:
        print("\n构建成功! 生成的文件:")
        for file_path in builder.dist_dir.glob("*"):
            print(f"  {file_path}")
    else:
        print("\n构建失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()
