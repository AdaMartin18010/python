# CLI工具开发

**Python命令行工具开发指南**

---

## 📋 概述

Python提供多种库来创建命令行工具，从简单的参数解析到复杂的交互式应用。

### 核心工具

- 🎯 **Click** - 最流行的CLI框架
- ⚡ **Typer** - 基于类型提示
- 🎨 **Rich** - 终端美化
- 📝 **argparse** - 标准库

---

## 🚀 Click

### 快速开始

```bash
uv add click
```

### 基本命令

```python
import click

@click.command()
@click.option('--count', default=1, help='重复次数')
@click.option('--name', prompt='你的名字', help='要问候的人')
def hello(count, name):
    """简单的问候程序"""
    for _ in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
```

### 命令组

```python
@click.group()
def cli():
    """CLI工具"""
    pass

@cli.command()
@click.argument('name')
def greet(name):
    """问候命令"""
    click.echo(f'Hello {name}!')

@cli.command()
def status():
    """状态命令"""
    click.echo('System OK')

if __name__ == '__main__':
    cli()
```

---

## ⚡ Typer

### 基于类型提示

```python
import typer
from typing import Optional

app = typer.Typer()

@app.command()
def hello(
    name: str,
    count: int = 1,
    formal: bool = False
):
    """问候程序"""
    greeting = "Good day" if formal else "Hello"
    for _ in range(count):
        typer.echo(f"{greeting} {name}")

if __name__ == "__main__":
    app()
```

---

## 🎨 Rich

### 美化输出

```python
from rich.console import Console
from rich.table import Table

console = Console()

# 彩色输出
console.print("Hello", style="bold red")

# 表格
table = Table(title="Users")
table.add_column("ID", style="cyan")
table.add_column("Name", style="magenta")
table.add_row("1", "Alice")
table.add_row("2", "Bob")
console.print(table)

# 进度条
from rich.progress import track
import time

for i in track(range(100), description="Processing..."):
    time.sleep(0.01)
```

---

## 📚 最佳实践

### 完整CLI应用

```python
import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """我的CLI工具"""
    pass

@cli.command()
@click.option('--format', type=click.Choice(['table', 'json']))
def list_users(format):
    """列出用户"""
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
    
    if format == 'json':
        import json
        click.echo(json.dumps(users, indent=2))
    else:
        table = Table()
        table.add_column("ID")
        table.add_column("Name")
        for user in users:
            table.add_row(str(user['id']), user['name'])
        console.print(table)

if __name__ == '__main__':
    cli()
```

---

## 🔗 相关资源

- [Click文档](https://click.palletsprojects.com/)
- [Typer文档](https://typer.tiangolo.com/)
- [Rich文档](https://rich.readthedocs.io/)

---

**最后更新**: 2025年10月28日

