# Python 语法结构

**从Token到抽象语法树(AST)**

---

## 📋 目录

- [语法分析概述](#语法分析概述)
- [Python语法规则](#Python语法规则)
- [抽象语法树AST](#抽象语法树AST)
- [语句结构](#语句结构)
- [表达式结构](#表达式结构)

---

## 语法分析概述

### 从Token到AST

```python
"""
语法分析: Token序列 → 抽象语法树(AST)
"""

import ast

# 源代码
code = """
def add(a, b):
    return a + b

result = add(1, 2)
"""

# 解析为AST
tree = ast.parse(code)

# 查看AST结构
print(ast.dump(tree, indent=2))

"""
输出 (简化):
Module(
  body=[
    FunctionDef(
      name='add',
      args=arguments(args=[arg('a'), arg('b')]),
      body=[Return(value=BinOp(left=Name('a'), op=Add(), right=Name('b')))]
    ),
    Assign(
      targets=[Name('result')],
      value=Call(func=Name('add'), args=[Constant(1), Constant(2)])
    )
  ]
)
"""
```

### 语法分析流程

```python
"""
完整的编译流程
"""

# 流程图:
"""
源代码 (Source Code)
    ↓
词法分析 (Lexer)
    ↓
Token序列
    ↓
语法分析 (Parser)
    ↓
抽象语法树 (AST)
    ↓
编译器 (Compiler)
    ↓
字节码 (Bytecode)
    ↓
虚拟机 (VM)
"""

# 使用compile查看中间步骤
code = "x = 1 + 2"

# 编译为AST
tree = ast.parse(code)

# 编译为代码对象
code_obj = compile(tree, '<string>', 'exec')

# 查看字节码
import dis
dis.dis(code_obj)

"""
  1           0 LOAD_CONST               0 (3)
              2 STORE_NAME               0 (x)
              4 LOAD_CONST               1 (None)
              6 RETURN_VALUE
"""
```

---

## Python语法规则

### BNF语法表示

```python
"""
Python使用修改版的BNF (Backus-Naur Form)
"""

# 简单语句示例
"""
simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE

small_stmt: (
    | expr_stmt
    | del_stmt
    | pass_stmt
    | flow_stmt
    | import_stmt
    | global_stmt
    | nonlocal_stmt
    | assert_stmt
)

expr_stmt: (
    | testlist_star_expr (annassign | augassign | ('=' testlist_star_expr)*)
)
"""

# 复合语句示例
"""
compound_stmt: (
    | if_stmt
    | while_stmt
    | for_stmt
    | try_stmt
    | with_stmt
    | funcdef
    | classdef
    | async_with_stmt
    | async_for_stmt
    | async_funcdef
)

if_stmt: (
    'if' named_expression ':' block
    ('elif' named_expression ':' block)*
    ['else' ':' block]
)
"""

# 查看完整语法
# Python的语法定义在: Grammar/python.gram
```

### 优先级与结合性

```python
"""
运算符优先级 (从低到高)
"""

precedence_table = """
1. lambda                  # Lambda表达式
2. if-else                 # 条件表达式
3. or                      # 逻辑或
4. and                     # 逻辑与
5. not                     # 逻辑非
6. in, not in, is, is not, <, <=, >, >=, !=, ==  # 比较
7. |                       # 按位或
8. ^                       # 按位异或
9. &                       # 按位与
10. <<, >>                 # 移位
11. +, -                   # 加减
12. *, @, /, //, %         # 乘除
13. +, -, ~                # 一元运算
14. **                     # 幂(右结合)
15. await                  # await表达式
16. x[i], x[i:j], x(args), x.attr  # 下标、切片、调用、属性
17. (expr), [expr], {expr}, {k:v}  # 括号、列表、集合、字典
"""

# 示例
result = 2 + 3 * 4      # 14 (乘法优先)
result = (2 + 3) * 4    # 20 (括号改变优先级)

result = 2 ** 3 ** 2    # 512 (右结合: 2 ** (3 ** 2))
result = (2 ** 3) ** 2  # 64

# 短路求值
x = False and expensive_function()  # 不会调用expensive_function
y = True or expensive_function()    # 不会调用expensive_function
```

---

## 抽象语法树AST

### AST节点类型

```python
"""
AST主要节点类型
"""
import ast

# Module: 模块
# - body: 语句列表

# FunctionDef: 函数定义
# - name: 函数名
# - args: 参数
# - body: 函数体
# - decorator_list: 装饰器
# - returns: 返回类型注解

# ClassDef: 类定义
# - name: 类名
# - bases: 基类
# - body: 类体
# - decorator_list: 装饰器

# Assign: 赋值
# - targets: 赋值目标
# - value: 值

# AugAssign: 增强赋值 (+=, -=等)
# - target: 目标
# - op: 运算符
# - value: 值

# Return: 返回语句
# - value: 返回值

# If: if语句
# - test: 条件
# - body: if块
# - orelse: else块

# For: for循环
# - target: 循环变量
# - iter: 迭代对象
# - body: 循环体
# - orelse: else块

# While: while循环
# - test: 条件
# - body: 循环体
# - orelse: else块
```

### AST遍历

```python
"""
遍历和分析AST
"""
import ast

code = """
def greet(name):
    message = f"Hello, {name}"
    return message

result = greet("Alice")
"""

tree = ast.parse(code)

# 方法1: ast.walk (广度优先)
print("All nodes:")
for node in ast.walk(tree):
    print(type(node).__name__)

# 方法2: ast.NodeVisitor (自定义遍历)
class FunctionAnalyzer(ast.NodeVisitor):
    """分析函数定义"""

    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        """访问函数定义节点"""
        self.functions.append({
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'line': node.lineno
        })
        # 继续遍历子节点
        self.generic_visit(node)

analyzer = FunctionAnalyzer()
analyzer.visit(tree)

print(f"Functions: {analyzer.functions}")
# [{'name': 'greet', 'args': ['name'], 'line': 2}]
```

### AST转换

```python
"""
修改AST - 代码转换
"""
import ast

class ConstantFolder(ast.NodeTransformer):
    """常量折叠优化"""

    def visit_BinOp(self, node):
        """访问二元运算"""
        # 先递归处理子节点
        node = self.generic_visit(node)

        # 如果两个操作数都是常量
        if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            # 计算结果
            if isinstance(node.op, ast.Add):
                return ast.Constant(node.left.value + node.right.value)
            elif isinstance(node.op, ast.Mult):
                return ast.Constant(node.left.value * node.right.value)

        return node

# 原始代码
code = "x = 1 + 2 * 3"
tree = ast.parse(code)

print("Before:")
print(ast.unparse(tree))  # x = 1 + 2 * 3

# 应用优化
optimizer = ConstantFolder()
optimized_tree = optimizer.visit(tree)
ast.fix_missing_locations(optimized_tree)

print("After:")
print(ast.unparse(optimized_tree))  # x = 1 + 6 或 x = 7
```

---

## 语句结构

### 简单语句

```python
"""
简单语句 (simple statement)
"""

# 1. 表达式语句
x + y
print("hello")

# 2. 赋值语句
x = 10
x, y = 1, 2
[a, b] = [1, 2]

# 3. 增强赋值
x += 1
x *= 2

# 4. 断言语句
assert x > 0
assert x > 0, "x must be positive"

# 5. pass语句
if True:
    pass  # 空操作

# 6. del语句
del x
del lst[0]
del d['key']

# 7. return语句
def func():
    return 42

# 8. yield语句
def generator():
    yield 1

# 9. raise语句
raise ValueError("error")
raise ValueError("error") from cause

# 10. break/continue
for i in range(10):
    if i == 5:
        break
    if i == 3:
        continue

# 11. import语句
import os
from os import path
from os.path import *
import os as operating_system

# 12. global/nonlocal
global x
nonlocal y
```

### 复合语句

```python
"""
复合语句 (compound statement)
"""

# 1. if语句
if condition:
    pass
elif other_condition:
    pass
else:
    pass

# 2. while循环
while condition:
    pass
else:  # 循环正常结束时执行
    pass

# 3. for循环
for item in iterable:
    pass
else:  # 循环正常结束时执行
    pass

# 4. try语句
try:
    pass
except ExceptionType:
    pass
except (Type1, Type2) as e:
    pass
else:  # 没有异常时执行
    pass
finally:  # 总是执行
    pass

# 5. with语句
with context_manager as cm:
    pass

with cm1 as a, cm2 as b:
    pass

# 6. 函数定义
def func(arg, *args, kwarg=None, **kwargs):
    """Docstring"""
    pass

# 7. 类定义
class MyClass(Base):
    """Docstring"""
    class_var = 10

    def __init__(self):
        pass

# 8. 异步语句 (Python 3.5+)
async def async_func():
    await some_coroutine()

async with async_context_manager:
    pass

async for item in async_iterable:
    pass

# 9. match语句 (Python 3.10+)
match value:
    case 1:
        pass
    case [x, y]:
        pass
    case _:
        pass
```

---

## 表达式结构

### 基础表达式

```python
"""
表达式类型
"""

# 1. 字面量
42, 3.14, "hello", True, None

# 2. 标识符
variable_name

# 3. 属性引用
obj.attribute

# 4. 下标
lst[0]
d['key']

# 5. 切片
lst[1:5]
lst[::2]
lst[::-1]

# 6. 调用
func()
func(arg1, arg2)
func(arg, kwarg=value)

# 7. 一元运算
-x, +x, ~x, not x

# 8. 二元运算
x + y, x - y, x * y, x / y
x // y, x % y, x ** y
x & y, x | y, x ^ y
x << y, x >> y

# 9. 比较
x < y, x > y, x <= y, x >= y
x == y, x != y
x is y, x is not y
x in y, x not in y

# 10. 逻辑运算
x and y, x or y, not x

# 11. 条件表达式
x if condition else y

# 12. lambda表达式
lambda x: x + 1
lambda x, y: x * y

# 13. 推导式
[x for x in range(10)]
{x for x in range(10)}
{x: x**2 for x in range(10)}
(x for x in range(10))
```

### 表达式AST

```python
"""
表达式的AST表示
"""
import ast

# 简单表达式
expr = "x + y"
tree = ast.parse(expr, mode='eval')
print(ast.dump(tree))

"""
Expression(
  body=BinOp(
    left=Name(id='x', ctx=Load()),
    op=Add(),
    right=Name(id='y', ctx=Load())
  )
)
"""

# 复杂表达式
expr = "f(a, b=2) if x > 0 else g(c)"
tree = ast.parse(expr, mode='eval')
print(ast.dump(tree, indent=2))

"""
Expression(
  body=IfExp(
    test=Compare(
      left=Name(id='x', ctx=Load()),
      ops=[Gt()],
      comparators=[Constant(value=0)]
    ),
    body=Call(
      func=Name(id='f', ctx=Load()),
      args=[Name(id='a', ctx=Load())],
      keywords=[keyword(arg='b', value=Constant(value=2))]
    ),
    orelse=Call(
      func=Name(id='g', ctx=Load()),
      args=[Name(id='c', ctx=Load())]
    )
  )
)
"""
```

### 表达式求值

```python
"""
表达式求值顺序
"""

# 1. 从左到右求值
def f(x):
    print(f"f({x})")
    return x

result = f(1) + f(2) + f(3)
"""
输出:
f(1)
f(2)
f(3)
"""

# 2. 短路求值
x = False and f(1)  # f(1)不会被调用
y = True or f(2)    # f(2)不会被调用

# 3. 条件表达式求值
result = f(1) if True else f(2)  # f(2)不会被调用

# 4. 函数参数求值顺序
def func(a, b, c):
    pass

func(f(1), f(2), f(3))  # 按顺序: f(1), f(2), f(3)

# 5. 关键字参数求值顺序
func(c=f(3), a=f(1), b=f(2))  # 按出现顺序: f(3), f(1), f(2)
```

---

## 📚 核心要点

### 语法分析

- ✅ **作用**: Token序列 → AST
- ✅ **BNF**: 语法规则的形式化描述
- ✅ **优先级**: 决定表达式的结合方式
- ✅ **结合性**: 左结合 vs 右结合

### AST

- ✅ **节点类型**: Module, FunctionDef, Assign等
- ✅ **遍历**: ast.walk, ast.NodeVisitor
- ✅ **转换**: ast.NodeTransformer
- ✅ **应用**: 代码分析、优化、转换

### 语句

- ✅ **简单语句**: 赋值、断言、pass、del等
- ✅ **复合语句**: if, for, while, try, with等
- ✅ **语句块**: 通过缩进表示

### 表达式

- ✅ **类型**: 字面量、运算、调用、推导式等
- ✅ **求值**: 从左到右、短路求值
- ✅ **优先级**: 影响解析结果

### 最佳实践

- ✅ 理解运算符优先级
- ✅ 合理使用括号提高可读性
- ✅ 注意短路求值的副作用
- ✅ 使用AST进行代码分析
- ✅ 遵循PEP 8的语句格式

---

**掌握Python语法，写出清晰的代码！** 📐✨

**相关文档**:

- [01-lexical.md](01-lexical.md) - 词法分析
- [03-expressions.md](03-expressions.md) - 表达式语义
- [04-statements.md](04-statements.md) - 语句语义

**最后更新**: 2025年10月28日
