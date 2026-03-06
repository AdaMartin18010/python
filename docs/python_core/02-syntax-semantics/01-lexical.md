# Python 词法分析

**Token化：从源代码到词法单元**

---

## 📋 目录

- [词法分析概述](#词法分析概述)
- [Token类型](#Token类型)
- [标识符与关键字](#标识符与关键字)
- [字面量](#字面量)
- [运算符与分隔符](#运算符与分隔符)
- [编码与注释](#编码与注释)

---

## 词法分析概述

### 什么是词法分析

```python
"""
词法分析: 源代码 → Token序列
"""

# 源代码
source = "x = 42 + y"

# 词法分析后的Token序列:
"""
NAME        'x'
OP          '='
NUMBER      '42'
OP          '+'
NAME        'y'
NEWLINE
"""

# Python的tokenize模块
import tokenize
import io

code = "x = 42 + y"
tokens = tokenize.generate_tokens(io.StringIO(code).readline)

for token in tokens:
    print(f"{tokenize.tok_name[token.type]:10} {token.string!r:10} "
          f"{token.start} {token.end}")

"""
输出:
NAME       'x'        (1, 0) (1, 1)
OP         '='        (1, 2) (1, 3)
NUMBER     '42'       (1, 4) (1, 6)
OP         '+'        (1, 7) (1, 8)
NAME       'y'        (1, 9) (1, 10)
NEWLINE    ''         (1, 10) (1, 10)
ENDMARKER  ''         (2, 0) (2, 0)
"""
```

### 词法分析流程

```python
"""
词法分析的三个阶段
"""

# 阶段1: 物理行 → 逻辑行
physical_lines = """
x = 1 + \\
    2 + \\
    3
"""

# 转换为逻辑行: "x = 1 + 2 + 3"

# 阶段2: 逻辑行 → Token序列
# 识别标识符、关键字、字面量、运算符

# 阶段3: 缩进处理
indented_code = """
if True:
    x = 1
    y = 2
"""

# 生成INDENT和DEDENT token
"""
NAME    'if'
NAME    'True'
OP      ':'
NEWLINE
INDENT          # 缩进开始
NAME    'x'
...
DEDENT          # 缩进结束
"""
```

---

## Token类型

### 主要Token类型

```python
"""
Python的Token类型
"""
import token

# 查看所有Token类型
print("Token types:")
for name in dir(token):
    if name.isupper():
        value = getattr(token, name)
        if isinstance(value, int):
            print(f"{value:3} {name}")

"""
主要类型:
0   ENDMARKER    # 文件结束
1   NAME         # 标识符
2   NUMBER       # 数字字面量
3   STRING       # 字符串字面量
4   NEWLINE      # 换行
5   INDENT       # 缩进
6   DEDENT       # 反缩进
7   LPAR         # (
8   RPAR         # )
9   LSQB         # [
10  RSQB         # ]
...
54  OP           # 运算符
62  ENCODING     # 编码声明
63  NL           # 非终止换行
"""
```

### Token结构

```python
"""
Token对象的属性
"""
import tokenize
import io

code = "x = 42"
tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))

for tok in tokens:
    print(f"""
Token:
  type:   {tokenize.tok_name[tok.type]}
  string: {tok.string!r}
  start:  {tok.start}  # (行号, 列号)
  end:    {tok.end}
  line:   {tok.line!r}
""")

# TokenInfo命名元组
"""
TokenInfo(
    type=1,              # Token类型
    string='x',          # Token字符串
    start=(1, 0),        # 起始位置
    end=(1, 1),          # 结束位置
    line='x = 42'        # 所在行
)
"""
```

---

## 标识符与关键字

### 标识符规则

```python
"""
标识符命名规则
"""

# ✅ 合法标识符
valid_names = [
    "x",
    "my_var",
    "_private",
    "__dunder__",
    "Class",
    "function123",
    "α",          # Unicode字符
    "变量",       # 中文
]

# ❌ 非法标识符
"""
123abc       # 不能以数字开头
my-var       # 不能包含连字符
for          # 不能是关键字
my var       # 不能包含空格
"""

# 标识符的正则模式
import re

identifier_pattern = r'[a-zA-Z_]\w*'
print(re.match(identifier_pattern, "my_var"))  # Match

# Unicode标识符 (Python 3)
identifier_unicode = r'[\w\u0080-\uFFFF]+'
```

### 关键字

```python
"""
Python关键字
"""
import keyword

# 所有关键字
print(keyword.kwlist)
"""
['False', 'None', 'True', 'and', 'as', 'assert',
 'async', 'await', 'break', 'class', 'continue',
 'def', 'del', 'elif', 'else', 'except', 'finally',
 'for', 'from', 'global', 'if', 'import', 'in',
 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass',
 'raise', 'return', 'try', 'while', 'with', 'yield']
"""

# 检查是否为关键字
print(keyword.iskeyword("for"))    # True
print(keyword.iskeyword("print"))  # False

# 软关键字 (Python 3.10+)
print(keyword.softkwlist)
"""
['_', 'case', 'match', 'type']
"""

# 软关键字只在特定上下文中是关键字
match = 10  # ✅ 作为变量名OK
```

### 保留标识符

```python
"""
特殊标识符
"""

# 1. 单下划线: _ (常用于临时变量)
for _ in range(5):
    print("Hello")

# 2. 单前导下划线: _name (内部使用)
class MyClass:
    def _internal_method(self):  # 约定为内部方法
        pass

# 3. 单后置下划线: name_ (避免关键字冲突)
class_ = type("MyClass", (), {})

# 4. 双前导下划线: __name (名称改写)
class MyClass:
    def __private(self):  # 改写为 _MyClass__private
        pass

# 5. 双下划线包围: __name__ (魔法方法/属性)
class MyClass:
    def __init__(self):  # 特殊方法
        pass
```

---

## 字面量

### 数字字面量

```python
"""
数字字面量的各种形式
"""

# 整数
decimal = 42          # 十进制
binary = 0b101010     # 二进制
octal = 0o52          # 八进制
hexadecimal = 0x2A    # 十六进制

# 大整数使用下划线分隔
million = 1_000_000
hex_value = 0xFF_FF_FF

# 浮点数
float1 = 3.14
float2 = .5           # 0.5
float3 = 10.          # 10.0
scientific = 1.5e10   # 科学计数法
small = 3e-5

# 复数
complex1 = 3 + 4j
complex2 = complex(3, 4)
imaginary = 2j

# 查看Token
import tokenize, io

code = "0b101010, 1_000_000, 3.14, 2j"
tokens = tokenize.generate_tokens(io.StringIO(code).readline)

for tok in tokens:
    if tok.type == tokenize.NUMBER:
        print(f"NUMBER: {tok.string!r}")

"""
NUMBER: '0b101010'
NUMBER: '1_000_000'
NUMBER: '3.14'
NUMBER: '2j'
"""
```

### 字符串字面量

```python
"""
字符串字面量的多种形式
"""

# 1. 单引号和双引号
s1 = 'Hello'
s2 = "World"
s3 = 'He said "Hi"'    # 包含双引号
s4 = "It's fine"       # 包含单引号

# 2. 三引号字符串 (多行)
multiline = """
This is a
multiline string
"""

# 3. 原始字符串 (不转义)
raw = r"C:\Users\name"  # 不转义\n, \t等
regex = r"\d+\.\d+"

# 4. 格式化字符串 (f-string)
name = "Alice"
age = 30
f_string = f"Name: {name}, Age: {age}"

# 5. 字节字符串
bytes_str = b"Hello"
raw_bytes = rb"C:\path"

# 6. 字符串前缀组合
# r, u, b, f 可以组合
fr_string = fr"Raw f-string: {value}"
rb_string = rb"Raw bytes"

# Token示例
code = '''r"\\n", f"{x}", b"bytes"'''
tokens = tokenize.generate_tokens(io.StringIO(code).readline)

for tok in tokens:
    if tok.type == tokenize.STRING:
        print(f"STRING: {tok.string!r}")

"""
STRING: 'r"\\\\n"'
STRING: 'f"{x}"'
STRING: 'b"bytes"'
"""
```

### 转义序列

```python
"""
字符串转义序列
"""

# 常用转义序列
escapes = {
    r'\n': '换行 (LF)',
    r'\r': '回车 (CR)',
    r'\t': '制表符',
    r'\\': '反斜杠',
    r'\'': '单引号',
    r'\"': '双引号',
    r'\a': '响铃',
    r'\b': '退格',
    r'\f': '换页',
    r'\v': '垂直制表符',
}

# Unicode转义
unicode_str = "\u4e2d\u6587"  # '中文'
unicode32 = "\U0001F600"      # '😀'
named = "\N{GREEK CAPITAL LETTER DELTA}"  # 'Δ'

# 八进制和十六进制
octal = "\101"     # 'A' (8进制101)
hex_char = "\x41"  # 'A' (16进制41)

# 原始字符串不转义
raw = r"\n\t"  # 字面上的 '\n\t'
```

---

## 运算符与分隔符

### 运算符

```python
"""
Python运算符
"""

# 算术运算符
operators_arithmetic = [
    '+',   # 加
    '-',   # 减
    '*',   # 乘
    '/',   # 除
    '//',  # 整除
    '%',   # 取模
    '**',  # 幂
]

# 位运算符
operators_bitwise = [
    '&',   # 按位与
    '|',   # 按位或
    '^',   # 按位异或
    '~',   # 按位取反
    '<<',  # 左移
    '>>',  # 右移
]

# 比较运算符
operators_comparison = [
    '==',  # 等于
    '!=',  # 不等于
    '<',   # 小于
    '>',   # 大于
    '<=',  # 小于等于
    '>=',  # 大于等于
]

# 赋值运算符
operators_assignment = [
    '=',   # 赋值
    '+=',  # 加赋值
    '-=',  # 减赋值
    '*=',  # 乘赋值
    '/=',  # 除赋值
    '//=', # 整除赋值
    '%=',  # 取模赋值
    '**=', # 幂赋值
    '&=',  # 按位与赋值
    '|=',  # 按位或赋值
    '^=',  # 按位异或赋值
    '>>=', # 右移赋值
    '<<=', # 左移赋值
    ':=',  # 海象运算符 (Python 3.8+)
]

# 逻辑运算符 (关键字)
# and, or, not

# 成员运算符 (关键字)
# in, not in

# 身份运算符 (关键字)
# is, is not
```

### 分隔符

```python
"""
Python分隔符
"""

# 括号类
delimiters_brackets = [
    '(',   # 左圆括号
    ')',   # 右圆括号
    '[',   # 左方括号
    ']',   # 右方括号
    '{',   # 左花括号
    '}',   # 右花括号
]

# 标点类
delimiters_punctuation = [
    ',',   # 逗号
    ':',   # 冒号
    ';',   # 分号
    '.',   # 点
    '...',  # 省略号 (Ellipsis)
    '@',   # 装饰器
    '->',  # 函数注解
]

# 特殊
delimiters_special = [
    '=',   # 赋值
    '\n',  # 换行
]

# Token类型
code = "(a, b): c[0] @ decorator"
tokens = tokenize.generate_tokens(io.StringIO(code).readline)

for tok in tokens:
    if tok.type == tokenize.OP:
        print(f"OP: {tok.string!r}")

"""
OP: '('
OP: ','
OP: ')'
OP: ':'
OP: '['
OP: ']'
OP: '@'
"""
```

---

## 编码与注释

### 源文件编码

```python
"""
源文件编码声明
"""

# 默认编码: UTF-8 (Python 3)

# 显式声明编码 (必须在第一或第二行)
# -*- coding: utf-8 -*-

# 或
# coding: utf-8

# 或
# coding=utf-8

# 检测编码
import tokenize

with open(__file__, 'rb') as f:
    encoding = tokenize.detect_encoding(f.readline)[0]
    print(f"File encoding: {encoding}")
```

### 注释

```python
"""
注释的Token处理
"""

# 1. 单行注释
x = 42  # 这是注释

# 2. 多行注释 (文档字符串)
"""
这是多行注释
实际上是字符串字面量
"""

# 3. 注释不会生成Token
import tokenize, io

code = """
x = 42  # 注释
y = 10
"""

tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))

# 默认情况下注释被跳过
print("Tokens without comments:")
for tok in tokens:
    if tok.type != tokenize.ENCODING:
        print(f"{tokenize.tok_name[tok.type]:10} {tok.string!r}")

# 使用generate_tokens可以获取注释
print("\nAll tokens including comments:")
tokens = tokenize.tokenize(io.BytesIO(code.encode()).readline)
for tok in tokens:
    print(f"{tokenize.tok_name[tok.type]:10} {tok.string!r}")
```

### 行连接

```python
"""
物理行连接为逻辑行
"""

# 1. 显式行连接 (反斜杠)
total = 1 + 2 + \
        3 + 4 + \
        5

# 2. 隐式行连接 (括号内)
total = (1 + 2 +
         3 + 4 +
         5)

items = [
    'a',
    'b',
    'c',
]

# 3. 字符串字面量拼接
message = "Hello " \
          "World"  # 自动拼接

# Token示例
code = """
x = (1 +
     2 +
     3)
"""

tokens = tokenize.generate_tokens(io.StringIO(code).readline)

for tok in tokens:
    if tok.type in (tokenize.NAME, tokenize.NUMBER, tokenize.OP):
        print(f"{tokenize.tok_name[tok.type]:10} {tok.string!r:5} "
              f"at line {tok.start[0]}")

"""
输出:
NAME       'x'   at line 2
OP         '='   at line 2
OP         '('   at line 2
NUMBER     '1'   at line 2
OP         '+'   at line 2
NUMBER     '2'   at line 3  # 注意行号
OP         '+'   at line 3
NUMBER     '3'   at line 4
OP         ')'   at line 4
"""
```

---

## 📚 核心要点

### 词法分析

- ✅ **作用**: 将源代码转换为Token序列
- ✅ **流程**: 物理行 → 逻辑行 → Token序列
- ✅ **缩进**: 通过INDENT/DEDENT Token表示

### Token类型

- ✅ **NAME**: 标识符和关键字
- ✅ **NUMBER**: 数字字面量
- ✅ **STRING**: 字符串字面量
- ✅ **OP**: 运算符和分隔符
- ✅ **INDENT/DEDENT**: 缩进控制

### 标识符

- ✅ **规则**: 字母/下划线开头，可含数字
- ✅ **Unicode**: 支持Unicode字符
- ✅ **关键字**: 不能作为标识符
- ✅ **约定**: _private, **dunder**

### 字面量

- ✅ **数字**: 整数、浮点、复数、多进制
- ✅ **字符串**: 单/双/三引号、原始、f-string
- ✅ **转义**: \n, \t, \u, \x等

### 最佳实践

- ✅ 使用有意义的标识符
- ✅ 遵循PEP 8命名约定
- ✅ 合理使用f-string
- ✅ 大数字使用下划线分隔
- ✅ 注意编码声明（非UTF-8时）

---

**理解词法分析，掌握Python语法基础！** 🔤✨

**相关文档**:

- [02-grammar.md](02-grammar.md) - 语法结构
- [03-expressions.md](03-expressions.md) - 表达式语义

**最后更新**: 2025年10月28日
