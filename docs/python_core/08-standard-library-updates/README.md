# Python 3.13 标准库更新

> Python 3.13 标准库的重要变更和新特性

---

## 概述

Python 3.13 引入了多个标准库的重要更新，包括新功能、性能改进和 API 移除。

**主要变更类别**:

- ✅ 新增功能和模块
- ✅ 现有模块改进
- ✅ 安全增强
- ✅ 移除的废弃模块 (PEP 594)

---

## 新增功能概览

| 模块 | 新功能 | 说明 |
|------|--------|------|
| `copy` | `copy.replace()` | 不可变对象的替换 |
| `warnings` | `@deprecated` 装饰器 | 标准化弃用标记 |
| `base64` | `z85encode/decode` | Z85 编码支持 |
| `dbm` | `dbm.sqlite3` 后端 | SQLite 作为默认后端 |
| `os` | 定时器文件描述符 | Linux 定时器通知 |
| `random` | CLI 接口 | 命令行随机数生成 |
| `argparse` | 弃用支持 | 参数弃用标记 |

---

## 详细文档

### 1. copy.replace() - 不可变对象替换

```python
import copy
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

# 创建不可变对象
p = Point(1, 2)

# 使用 copy.replace() 创建修改后的副本
p2 = copy.replace(p, x=10)
print(p2)  # Point(x=10, y=2)

# 原始对象不变
print(p)   # Point(x=1, y=2)

# 多个字段替换
p3 = copy.replace(p, x=100, y=200)
print(p3)  # Point(x=100, y=200)
```

**支持的类型**:

- `namedtuple`
- `dataclass` (frozen 和普通)
- 实现 `__replace__` 方法的自定义类
- 内置不可变类型 (tuple, frozenset 等)

### 2. warnings.deprecated() 装饰器

详见 [PEP 702 文档](../03-type-system/09-pep702-deprecated.md)

### 3. base64 Z85 编码

```python
import base64

# Z85 编码 - 适合在文本环境中传输二进制数据
data = b"Hello, World! 123"

# 编码
encoded = base64.z85encode(data)
print(f"Z85: {encoded}")  # b'nm=QNzY8O0WM{4^%8Fqs'

# 解码
decoded = base64.z85decode(encoded)
print(f"Decoded: {decoded}")  # b'Hello, World! 123'
```

### 4. dbm.sqlite3 后端

```python
import dbm

# Python 3.13+ 默认使用 SQLite 作为 dbm 后端
# 更可靠，支持更大的值

with dbm.open('test.db', 'c') as db:
    db['key1'] = 'value1'
    db['key2'] = 'value2'

    print(db['key1'])  # b'value1'

# 明确指定后端
with dbm.open('test.db', 'c', backend='sqlite3') as db:
    db['key3'] = 'value3'
```

### 5. random CLI 接口

```bash
# 生成随机数
python -m random
# 输出: 0.37444887175646646

# 生成整数
python -m random --integer 1 100
# 输出: 42

# 从列表选择
python -m random --choice "apple banana cherry"
# 输出: banana

# 打乱列表
python -m random --shuffle "1 2 3 4 5"
# 输出: 3 1 5 2 4
```

### 6. argparse 弃用支持

```python
import argparse
import warnings

parser = argparse.ArgumentParser()
parser.add_argument('--old-option', help='旧选项',
                   deprecated=True,  # 标记为弃用
                   deprecation_message='Use --new-option instead')
parser.add_argument('--new-option', help='新选项')

args = parser.parse_args(['--old-option', 'value'])
# 发出警告: --old-option is deprecated: Use --new-option instead
```

---

## 移除的模块 (PEP 594)

Python 3.13 移除了 19 个"死电池"模块：

| 移除模块 | 替代方案 |
|----------|----------|
| `aifc` | `wave` |
| `audioop` | 第三方库 `pyaudio` |
| `cgi` | `urllib.parse` + 框架 |
| `cgitb` | 框架内置调试 |
| `chunk` | 手动解析 |
| `crypt` | `hashlib` 或 `bcrypt` |
| `imghdr` | `filetype` 或 `python-magic` |
| `mailcap` | 无直接替代 |
| `msilib` | 无直接替代 |
| `nis` | 无直接替代 |
| `nntplib` | 无直接替代 |
| `ossaudiodev` | `pyaudio` |
| `pipes` | `subprocess` |
| `sndhdr` | `filetype` |
| `spwd` | `pwd` |
| `sunau` | `wave` |
| `telnetlib` | `telnetlib3` |
| `uu` | `base64` |
| `xdrlib` | `struct` |

### 迁移示例

```python
# 旧代码 (Python 3.12)
import cgi
form = cgi.FieldStorage()
value = form.getvalue('key')

# 新代码 (Python 3.13)
from urllib.parse import parse_qs
query_string = 'key=value'
params = parse_qs(query_string)
value = params.get('key', [None])[0]
```

---

## 其他改进

### typing 模块增强

```python
from typing import TypeVar, get_protocol_members, is_protocol
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

# 检查是否为 Protocol
print(is_protocol(Drawable))  # True

# 获取 Protocol 成员
members = get_protocol_members(Drawable)
print(members)  # {'draw'}

# TypeVar 默认值 (Python 3.13+)
T = TypeVar("T", default=str)
```

### os 模块 - Linux 定时器

```python
import os

# Linux 定时器通知文件描述符（仅限 Linux）
if hasattr(os, 'timerfd_create'):
    fd = os.timerfd_create(os.CLOCK_REALTIME)
    # 使用定时器文件描述符
```

### venv 模块改进

```python
# Python 3.13+ venv 支持创建 SCM 忽略文件
import venv

builder = venv.EnvBuilder(
    system_site_packages=False,
    with_pip=True,
    # 新增：创建 .gitignore
    scm_ignore_files={'git'}
)
builder.create('myenv')
```

---

## 安全改进

### SSL 模块

```python
import ssl

# Python 3.13+ 默认设置更严格
context = ssl.create_default_context()
# 默认启用:
# - ssl.VERIFY_X509_PARTIAL_CHAIN
# - ssl.VERIFY_X509_STRICT
```

### XML 模块

```python
import xml.etree.ElementTree as ET

# Python 3.13+ 允许控制 Expat 重解析延迟（安全修复）
parser = ET.XMLParser()
parser.flush()  # 新增方法
```

---

## 兼容性检查清单

迁移到 Python 3.13 前检查：

```python
"""
Python 3.13 兼容性检查脚本
"""
import sys
import importlib.util

def check_compatibility():
    """检查 Python 3.13 兼容性"""
    issues = []

    # 检查移除的模块
    removed_modules = [
        'aifc', 'audioop', 'cgi', 'cgitb', 'chunk',
        'crypt', 'imghdr', 'mailcap', 'msilib', 'nis',
        'nntplib', 'ossaudiodev', 'pipes', 'sndhdr',
        'spwd', 'sunau', 'telnetlib', 'uu', 'xdrlib',
        'lib2to3', 'tkinter.tix'
    ]

    for module in removed_modules:
        if importlib.util.find_spec(module) is not None:
            issues.append(f"✓ {module} - 仍可用")
        else:
            issues.append(f"✗ {module} - 已移除，需要迁移")

    return issues

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print("\nCompatibility Check:")
    for issue in check_compatibility():
        print(f"  {issue}")
```

---

## 延伸阅读

- [PEP 594 - Removing dead batteries](https://peps.python.org/pep-0594/)
- [Python 3.13 What's New](https://docs.python.org/3.13/whatsnew/3.13.html)
- [标准库文档](https://docs.python.org/3.13/library/index.html)

---

**掌握 Python 3.13 标准库更新，保持代码现代化！** 📚✨
