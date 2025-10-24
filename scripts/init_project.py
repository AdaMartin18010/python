#!/usr/bin/env python3
"""
Python 2025 Knowledge Base - Project Initialization Script
项目初始化脚本：快速创建新的Python项目

Usage:
    python scripts/init_project.py my-project
    python scripts/init_project.py my-project --template fastapi
    python scripts/init_project.py my-project --template data-science
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Dict, List
import subprocess

# 颜色代码
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


class ProjectInitializer:
    """项目初始化器"""

    def __init__(self, project_name: str, template: str = "basic"):
        self.project_name = project_name
        self.template = template
        self.project_dir = Path.cwd() / project_name
        self.template_dir = Path(__file__).parent.parent / "python" / "01-语言与生态" / "templates"

    def print_header(self, text: str) -> None:
        """打印标题"""
        print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
        print(f"{BLUE}{BOLD}{text:^60}{RESET}")
        print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

    def print_success(self, text: str) -> None:
        """打印成功信息"""
        print(f"{GREEN}✓{RESET} {text}")

    def print_info(self, text: str) -> None:
        """打印信息"""
        print(f"{BLUE}ℹ{RESET} {text}")

    def print_error(self, text: str) -> None:
        """打印错误信息"""
        print(f"{RED}✗{RESET} {text}")

    def check_prerequisites(self) -> bool:
        """检查先决条件"""
        self.print_info("检查先决条件...")
        
        # 检查项目名称
        if not self.project_name:
            self.print_error("项目名称不能为空")
            return False
        
        # 检查目录是否已存在
        if self.project_dir.exists():
            self.print_error(f"目录 {self.project_name} 已存在")
            return False
        
        # 检查 uv 是否安装
        if shutil.which("uv"):
            self.print_success("uv 已安装")
        else:
            self.print_info("uv 未安装，将使用标准 pip")
        
        return True

    def create_directory_structure(self) -> None:
        """创建目录结构"""
        self.print_info("创建目录结构...")
        
        directories = [
            self.project_dir,
            self.project_dir / "src" / self.project_name.replace("-", "_"),
            self.project_dir / "tests",
            self.project_dir / "docs",
            self.project_dir / ".github" / "workflows",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.print_success(f"创建目录: {directory.relative_to(Path.cwd())}")

    def create_pyproject_toml(self) -> None:
        """创建 pyproject.toml"""
        self.print_info("创建 pyproject.toml...")
        
        package_name = self.project_name.replace("-", "_")
        
        content = f'''[project]
name = "{self.project_name}"
version = "0.1.0"
description = "A Python 2025 project"
readme = "README.md"
requires-python = ">=3.12"
license = {{ text = "MIT" }}
authors = [
    {{ name = "Your Name", email = "your.email@example.com" }}
]
keywords = ["python", "2025"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.6.0",
    "mypy>=1.11.0",
    "pre-commit>=3.8.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/{self.project_name}"
Documentation = "https://github.com/yourusername/{self.project_name}#readme"
Repository = "https://github.com/yourusername/{self.project_name}"
Issues = "https://github.com/yourusername/{self.project_name}/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
ignore = []

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src/{package_name} --cov-report=term-missing"

[tool.coverage.run]
source = ["src/{package_name}"]
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
'''
        
        file_path = self.project_dir / "pyproject.toml"
        file_path.write_text(content)
        self.print_success(f"创建: pyproject.toml")

    def create_readme(self) -> None:
        """创建 README.md"""
        self.print_info("创建 README.md...")
        
        content = f'''# {self.project_name}

A Python 2025 project.

## 快速开始

### 安装依赖

使用 uv（推荐）：

```bash
uv sync
```

或使用 pip：

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码检查

```bash
ruff check .
mypy src/
```

### 格式化代码

```bash
ruff format .
```

## 开发

### 安装 Pre-commit Hooks

```bash
pre-commit install
```

### 项目结构

```
{self.project_name}/
├── src/
│   └── {self.project_name.replace("-", "_")}/
│       └── __init__.py
├── tests/
│   └── test_example.py
├── docs/
├── .github/
│   └── workflows/
├── pyproject.toml
├── README.md
└── LICENSE
```

## 许可证

MIT License
'''
        
        file_path = self.project_dir / "README.md"
        file_path.write_text(content)
        self.print_success("创建: README.md")

    def create_gitignore(self) -> None:
        """创建 .gitignore"""
        self.print_info("创建 .gitignore...")
        
        content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
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
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Type checking
.mypy_cache/
.pytype/
'''
        
        file_path = self.project_dir / ".gitignore"
        file_path.write_text(content)
        self.print_success("创建: .gitignore")

    def create_license(self) -> None:
        """创建 LICENSE"""
        self.print_info("创建 LICENSE...")
        
        import datetime
        year = datetime.datetime.now().year
        
        content = f'''MIT License

Copyright (c) {year} Your Name

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
        
        file_path = self.project_dir / "LICENSE"
        file_path.write_text(content)
        self.print_success("创建: LICENSE")

    def create_source_files(self) -> None:
        """创建源文件"""
        self.print_info("创建源文件...")
        
        package_name = self.project_name.replace("-", "_")
        src_dir = self.project_dir / "src" / package_name
        
        # __init__.py
        init_content = '''"""
{} - A Python 2025 project
"""

__version__ = "0.1.0"
'''.format(self.project_name)
        
        (src_dir / "__init__.py").write_text(init_content)
        self.print_success(f"创建: src/{package_name}/__init__.py")
        
        # main.py
        main_content = '''"""Main module"""


def main() -> None:
    """Main function"""
    print("Hello, Python 2025!")


if __name__ == "__main__":
    main()
'''
        
        (src_dir / "main.py").write_text(main_content)
        self.print_success(f"创建: src/{package_name}/main.py")

    def create_test_files(self) -> None:
        """创建测试文件"""
        self.print_info("创建测试文件...")
        
        package_name = self.project_name.replace("-", "_")
        
        test_content = f'''"""Test module"""

from {package_name} import __version__


def test_version() -> None:
    """Test version"""
    assert __version__ == "0.1.0"


def test_example() -> None:
    """Example test"""
    assert 1 + 1 == 2
'''
        
        test_file = self.project_dir / "tests" / "test_example.py"
        test_file.write_text(test_content)
        self.print_success("创建: tests/test_example.py")
        
        # __init__.py
        (self.project_dir / "tests" / "__init__.py").touch()

    def initialize_git(self) -> None:
        """初始化 Git 仓库"""
        if not shutil.which("git"):
            self.print_info("Git 未安装，跳过初始化")
            return
        
        self.print_info("初始化 Git 仓库...")
        
        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.project_dir,
                check=True,
                capture_output=True
            )
            self.print_success("Git 仓库已初始化")
            
            subprocess.run(
                ["git", "add", "."],
                cwd=self.project_dir,
                check=True,
                capture_output=True
            )
            
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=self.project_dir,
                check=True,
                capture_output=True
            )
            self.print_success("创建初始提交")
        except subprocess.CalledProcessError:
            self.print_info("Git 初始化失败，请手动执行")

    def print_next_steps(self) -> None:
        """打印后续步骤"""
        self.print_header("项目创建完成！")
        
        print(f"{BOLD}后续步骤:{RESET}\n")
        print(f"1. 进入项目目录:")
        print(f"   {GREEN}cd {self.project_name}{RESET}\n")
        print(f"2. 安装依赖:")
        print(f"   {GREEN}uv sync{RESET}  # 使用 uv")
        print(f"   或")
        print(f"   {GREEN}pip install -e \".[dev]\"{RESET}  # 使用 pip\n")
        print(f"3. 运行测试:")
        print(f"   {GREEN}pytest{RESET}\n")
        print(f"4. 开始开发:")
        print(f"   {GREEN}code .{RESET}  # 使用 VS Code")
        print(f"   或")
        print(f"   {GREEN}vim src/{self.project_name.replace('-', '_')}/main.py{RESET}\n")
        print(f"{BOLD}祝您开发愉快！{RESET} 🎉\n")

    def run(self) -> bool:
        """运行项目初始化"""
        self.print_header(f"初始化项目: {self.project_name}")
        
        if not self.check_prerequisites():
            return False
        
        try:
            self.create_directory_structure()
            self.create_pyproject_toml()
            self.create_readme()
            self.create_gitignore()
            self.create_license()
            self.create_source_files()
            self.create_test_files()
            self.initialize_git()
            self.print_next_steps()
            return True
        except Exception as e:
            self.print_error(f"初始化失败: {e}")
            return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Python 2025 知识库 - 项目初始化脚本"
    )
    parser.add_argument(
        "project_name",
        help="项目名称"
    )
    parser.add_argument(
        "--template",
        choices=["basic", "fastapi", "data-science"],
        default="basic",
        help="项目模板"
    )
    
    args = parser.parse_args()
    
    initializer = ProjectInitializer(
        project_name=args.project_name,
        template=args.template
    )
    
    success = initializer.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

