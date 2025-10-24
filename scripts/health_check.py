#!/usr/bin/env python3
"""
Python 2025 Knowledge Base - Health Check Script
健康检查脚本：检查项目配置、依赖、服务状态等

Usage:
    python scripts/health_check.py
    python scripts/health_check.py --fix
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Tuple
import shutil

# 颜色代码
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


class HealthChecker:
    """健康检查器"""

    def __init__(self, auto_fix: bool = False):
        self.auto_fix = auto_fix
        self.root_dir = Path(__file__).parent.parent
        self.issues: List[Dict] = []
        self.passed: List[str] = []
        self.warnings: List[str] = []

    def print_header(self, text: str) -> None:
        """打印标题"""
        print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
        print(f"{BLUE}{BOLD}{text:^60}{RESET}")
        print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

    def print_success(self, text: str) -> None:
        """打印成功信息"""
        print(f"{GREEN}✓{RESET} {text}")

    def print_warning(self, text: str) -> None:
        """打印警告信息"""
        print(f"{YELLOW}⚠{RESET} {text}")

    def print_error(self, text: str) -> None:
        """打印错误信息"""
        print(f"{RED}✗{RESET} {text}")

    def print_info(self, text: str) -> None:
        """打印信息"""
        print(f"{BLUE}ℹ{RESET} {text}")

    def check_python_version(self) -> bool:
        """检查Python版本"""
        self.print_info("检查 Python 版本...")
        version = sys.version_info
        if version >= (3, 12):
            self.print_success(f"Python {version.major}.{version.minor}.{version.micro}")
            self.passed.append("Python version")
            return True
        else:
            self.print_warning(
                f"Python {version.major}.{version.minor}.{version.micro} "
                f"(推荐 3.12+)"
            )
            self.warnings.append("Python version < 3.12")
            return False

    def check_command_exists(self, command: str) -> bool:
        """检查命令是否存在"""
        return shutil.which(command) is not None

    def check_tools(self) -> None:
        """检查开发工具"""
        self.print_info("检查开发工具...")
        
        tools = {
            "uv": "包管理工具",
            "git": "版本控制",
            "docker": "容器化",
            "make": "构建工具",
        }

        for tool, desc in tools.items():
            if self.check_command_exists(tool):
                self.print_success(f"{tool} ({desc})")
                self.passed.append(f"Tool: {tool}")
            else:
                self.print_warning(f"{tool} 未安装 ({desc})")
                self.warnings.append(f"Missing tool: {tool}")

    def check_files(self) -> None:
        """检查必要文件"""
        self.print_info("检查必要文件...")
        
        required_files = [
            ("pyproject.toml", "项目配置"),
            ("README.md", "项目文档"),
            ("LICENSE", "许可证"),
            ("CONTRIBUTING.md", "贡献指南"),
            ("CODE_OF_CONDUCT.md", "行为准则"),
            ("SECURITY.md", "安全政策"),
            ("Makefile", "构建脚本"),
            (".gitignore", "Git忽略"),
            (".pre-commit-config.yaml", "Pre-commit配置"),
        ]

        for file_path, desc in required_files:
            full_path = self.root_dir / file_path
            if full_path.exists():
                self.print_success(f"{file_path} ({desc})")
                self.passed.append(f"File: {file_path}")
            else:
                self.print_error(f"{file_path} 缺失 ({desc})")
                self.issues.append({
                    "type": "missing_file",
                    "file": file_path,
                    "description": desc
                })

    def check_directories(self) -> None:
        """检查目录结构"""
        self.print_info("检查目录结构...")
        
        required_dirs = [
            ("python", "核心章节"),
            ("scripts", "脚本目录"),
            (".github/workflows", "CI/CD配置"),
        ]

        for dir_path, desc in required_dirs:
            full_path = self.root_dir / dir_path
            if full_path.exists() and full_path.is_dir():
                self.print_success(f"{dir_path}/ ({desc})")
                self.passed.append(f"Directory: {dir_path}")
            else:
                self.print_error(f"{dir_path}/ 缺失 ({desc})")
                self.issues.append({
                    "type": "missing_directory",
                    "directory": dir_path,
                    "description": desc
                })

    def check_pyproject_toml(self) -> None:
        """检查 pyproject.toml 配置"""
        self.print_info("检查 pyproject.toml 配置...")
        
        pyproject_path = self.root_dir / "pyproject.toml"
        if not pyproject_path.exists():
            self.print_error("pyproject.toml 不存在")
            return

        try:
            import tomli
        except ImportError:
            try:
                import tomllib as tomli
            except ImportError:
                self.print_warning("无法导入 tomli/tomllib，跳过配置检查")
                return

        with open(pyproject_path, "rb") as f:
            try:
                config = tomli.load(f)
                
                # 检查必要的配置项
                if "project" in config:
                    self.print_success("找到 [project] 配置")
                    self.passed.append("pyproject.toml: [project]")
                else:
                    self.print_error("缺少 [project] 配置")
                    self.issues.append({
                        "type": "config",
                        "section": "project",
                        "description": "Missing [project] section"
                    })

                if "tool" in config:
                    tools = config["tool"]
                    for tool_name in ["ruff", "mypy", "pytest"]:
                        if tool_name in tools:
                            self.print_success(f"找到 [tool.{tool_name}] 配置")
                            self.passed.append(f"pyproject.toml: [tool.{tool_name}]")
                        else:
                            self.print_warning(f"缺少 [tool.{tool_name}] 配置")
                            self.warnings.append(f"Missing [tool.{tool_name}]")

            except Exception as e:
                self.print_error(f"解析 pyproject.toml 失败: {e}")
                self.issues.append({
                    "type": "config_parse_error",
                    "error": str(e)
                })

    def check_git_status(self) -> None:
        """检查 Git 状态"""
        self.print_info("检查 Git 状态...")
        
        if not self.check_command_exists("git"):
            self.print_warning("Git 未安装，跳过检查")
            return

        try:
            # 检查是否是 Git 仓库
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                self.print_success("Git 仓库已初始化")
                self.passed.append("Git repository")
                
                # 检查是否有未提交的更改
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=self.root_dir,
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.stdout.strip():
                    self.print_warning("有未提交的更改")
                    self.warnings.append("Uncommitted changes")
                else:
                    self.print_success("工作目录干净")
                    self.passed.append("Clean working directory")
            else:
                self.print_warning("不是 Git 仓库")
                self.warnings.append("Not a git repository")
        except Exception as e:
            self.print_error(f"检查 Git 状态失败: {e}")

    def check_docker_services(self) -> None:
        """检查 Docker 服务状态"""
        self.print_info("检查 Docker 服务...")
        
        if not self.check_command_exists("docker"):
            self.print_warning("Docker 未安装，跳过检查")
            return

        try:
            # 检查 Docker 是否运行
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                self.print_success("Docker 服务运行中")
                self.passed.append("Docker running")
                
                # 统计运行中的容器
                lines = result.stdout.strip().split("\n")
                container_count = len(lines) - 1  # 减去标题行
                if container_count > 0:
                    self.print_info(f"运行中的容器: {container_count}")
                    self.passed.append(f"{container_count} containers running")
                else:
                    self.print_info("没有运行中的容器")
            else:
                self.print_warning("Docker 未运行")
                self.warnings.append("Docker not running")
        except Exception as e:
            self.print_error(f"检查 Docker 状态失败: {e}")

    def generate_report(self) -> None:
        """生成报告"""
        self.print_header("健康检查报告")
        
        total = len(self.passed) + len(self.warnings) + len(self.issues)
        
        print(f"{BOLD}总检查项:{RESET} {total}")
        print(f"{GREEN}✓ 通过:{RESET} {len(self.passed)}")
        print(f"{YELLOW}⚠ 警告:{RESET} {len(self.warnings)}")
        print(f"{RED}✗ 错误:{RESET} {len(self.issues)}")
        
        if self.issues:
            print(f"\n{RED}{BOLD}发现的问题:{RESET}")
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue.get('type')}: {issue}")
        
        if self.warnings:
            print(f"\n{YELLOW}{BOLD}警告:{RESET}")
            for warning in self.warnings:
                print(f"  - {warning}")

        print(f"\n{BOLD}健康评分:{RESET} ", end="")
        if len(self.issues) == 0 and len(self.warnings) == 0:
            print(f"{GREEN}100% - 完美!{RESET} 🎉")
        elif len(self.issues) == 0:
            score = int((len(self.passed) / total) * 100)
            print(f"{YELLOW}{score}% - 良好{RESET} ✅")
        else:
            score = int((len(self.passed) / total) * 100)
            print(f"{RED}{score}% - 需要改进{RESET} ⚠️")

    def run_all_checks(self) -> bool:
        """运行所有检查"""
        self.print_header("Python 2025 知识库 - 健康检查")
        
        self.check_python_version()
        self.check_tools()
        self.check_files()
        self.check_directories()
        self.check_pyproject_toml()
        self.check_git_status()
        self.check_docker_services()
        
        self.generate_report()
        
        return len(self.issues) == 0


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Python 2025 知识库 - 健康检查脚本"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="尝试自动修复发现的问题"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出结果"
    )
    
    args = parser.parse_args()
    
    checker = HealthChecker(auto_fix=args.fix)
    success = checker.run_all_checks()
    
    if args.json:
        result = {
            "passed": checker.passed,
            "warnings": checker.warnings,
            "issues": checker.issues,
            "success": success
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

