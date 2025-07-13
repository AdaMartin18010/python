#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语义模型演示脚本

本脚本演示了Python语义模型的核心功能，包括：
1. 语义分析
2. 类型推断
3. 作用域分析
4. 控制流分析
5. 语义优化
"""

import ast
import sys
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class SemanticInfo:
    """语义信息数据类"""
    type_info: Dict[str, str]
    scope_info: Dict[str, str]
    flow_info: Dict[str, Any]
    errors: List[str]
    warnings: List[str]


class PythonSemanticAnalyzer:
    """Python语义分析器"""
    
    def __init__(self):
        self.type_environment = {}
        self.scope_stack = [{'type': 'global', 'symbols': {}}]
        self.semantic_info = SemanticInfo(
            type_info={},
            scope_info={},
            flow_info={},
            errors=[],
            warnings=[]
        )
    
    def analyze_code(self, source_code: str) -> SemanticInfo:
        """分析Python代码的语义"""
        try:
            # 解析AST
            ast_tree = ast.parse(source_code)
            
            # 语义分析
            self._analyze_semantics(ast_tree)
            
            return self.semantic_info
            
        except SyntaxError as e:
            self.semantic_info.errors.append(f"语法错误: {e}")
            return self.semantic_info
    
    def _analyze_semantics(self, ast_tree: ast.AST):
        """分析语义"""
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Assign):
                self._analyze_assignment(node)
            elif isinstance(node, ast.FunctionDef):
                self._analyze_function_def(node)
            elif isinstance(node, ast.ClassDef):
                self._analyze_class_def(node)
            elif isinstance(node, ast.Name):
                self._analyze_name_usage(node)
            elif isinstance(node, ast.Call):
                self._analyze_function_call(node)
    
    def _analyze_assignment(self, node: ast.Assign):
        """分析赋值语句"""
        value_type = self._infer_expression_type(node.value)
        
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                self.type_environment[var_name] = value_type
                self.semantic_info.type_info[var_name] = value_type
                
                # 添加到当前作用域
                current_scope = self.scope_stack[-1]
                current_scope['symbols'][var_name] = {
                    'type': value_type,
                    'scope': current_scope['type']
                }
    
    def _analyze_function_def(self, node: ast.FunctionDef):
        """分析函数定义"""
        # 进入函数作用域
        function_scope = {
            'type': 'function',
            'name': node.name,
            'symbols': {},
            'parameters': [arg.arg for arg in node.args.args]
        }
        self.scope_stack.append(function_scope)
        
        # 添加参数到符号表
        for param in function_scope['parameters']:
            function_scope['symbols'][param] = {
                'type': 'parameter',
                'scope': 'local'
            }
        
        # 分析函数体
        for stmt in node.body:
            self._analyze_semantics(stmt)
        
        # 退出函数作用域
        self.scope_stack.pop()
    
    def _analyze_class_def(self, node: ast.ClassDef):
        """分析类定义"""
        # 进入类作用域
        class_scope = {
            'type': 'class',
            'name': node.name,
            'symbols': {},
            'methods': []
        }
        self.scope_stack.append(class_scope)
        
        # 分析类体
        for stmt in node.body:
            self._analyze_semantics(stmt)
        
        # 退出类作用域
        self.scope_stack.pop()
    
    def _analyze_name_usage(self, node: ast.Name):
        """分析名称使用"""
        name = node.id
        
        # 检查变量是否定义
        if isinstance(node.ctx, ast.Load):
            if not self._is_variable_defined(name):
                self.semantic_info.errors.append(
                    f"未定义变量: {name} (行 {node.lineno})"
                )
        
        # 记录作用域信息
        scope_level = self._find_name_in_scopes(name)
        if scope_level is not None:
            self.semantic_info.scope_info[name] = f"scope_level_{scope_level}"
    
    def _analyze_function_call(self, node: ast.Call):
        """分析函数调用"""
        if hasattr(node.func, 'id'):
            func_name = node.func.id
            
            # 检查函数是否定义
            if not self._is_variable_defined(func_name):
                self.semantic_info.warnings.append(
                    f"可能未定义的函数: {func_name} (行 {node.lineno})"
                )
    
    def _infer_expression_type(self, expr: ast.expr) -> str:
        """推断表达式类型"""
        if isinstance(expr, ast.Num):
            return type(expr.n).__name__
        elif isinstance(expr, ast.Str):
            return 'str'
        elif isinstance(expr, ast.List):
            return 'list'
        elif isinstance(expr, ast.Dict):
            return 'dict'
        elif isinstance(expr, ast.Name):
            return self.type_environment.get(expr.id, 'unknown')
        elif isinstance(expr, ast.BinOp):
            return self._infer_binary_op_type(expr)
        else:
            return 'unknown'
    
    def _infer_binary_op_type(self, bin_op: ast.BinOp) -> str:
        """推断二元操作类型"""
        left_type = self._infer_expression_type(bin_op.left)
        right_type = self._infer_expression_type(bin_op.right)
        
        if isinstance(bin_op.op, ast.Add):
            if left_type == 'str' and right_type == 'str':
                return 'str'
            elif left_type in ['int', 'float'] and right_type in ['int', 'float']:
                return 'float' if 'float' in [left_type, right_type] else 'int'
        
        return 'unknown'
    
    def _is_variable_defined(self, name: str) -> bool:
        """检查变量是否定义"""
        for scope in reversed(self.scope_stack):
            if name in scope['symbols']:
                return True
        return False
    
    def _find_name_in_scopes(self, name: str) -> Optional[int]:
        """在作用域栈中查找名称"""
        for i, scope in enumerate(reversed(self.scope_stack)):
            if name in scope['symbols']:
                return len(self.scope_stack) - 1 - i
        return None


class TypeInferrer:
    """类型推断器"""
    
    def __init__(self):
        self.type_constraints = []
        self.inferred_types = {}
    
    def infer_types(self, ast_tree: ast.AST) -> Dict[str, str]:
        """推断类型"""
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Assign):
                self._infer_assignment_types(node)
            elif isinstance(node, ast.FunctionDef):
                self._infer_function_types(node)
            elif isinstance(node, ast.Call):
                self._infer_call_types(node)
        
        return self.inferred_types
    
    def _infer_assignment_types(self, node: ast.Assign):
        """推断赋值类型"""
        value_type = self._infer_expression_type(node.value)
        
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.inferred_types[target.id] = value_type
    
    def _infer_function_types(self, node: ast.FunctionDef):
        """推断函数类型"""
        # 分析函数体推断返回类型
        return_type = self._infer_function_return_type(node)
        self.inferred_types[node.name] = f"function -> {return_type}"
    
    def _infer_call_types(self, node: ast.Call):
        """推断函数调用类型"""
        if hasattr(node.func, 'id'):
            func_name = node.func.id
            # 根据函数名推断返回类型
            if func_name in ['len', 'str', 'int', 'float']:
                self.inferred_types[f"call_{func_name}"] = func_name
    
    def _infer_expression_type(self, expr: ast.expr) -> str:
        """推断表达式类型"""
        if isinstance(expr, ast.Num):
            return type(expr.n).__name__
        elif isinstance(expr, ast.Str):
            return 'str'
        elif isinstance(expr, ast.List):
            return 'list'
        elif isinstance(expr, ast.Dict):
            return 'dict'
        else:
            return 'unknown'
    
    def _infer_function_return_type(self, func_def: ast.FunctionDef) -> str:
        """推断函数返回类型"""
        # 简化实现：分析函数体中的return语句
        for node in ast.walk(func_def):
            if isinstance(node, ast.Return):
                if node.value:
                    return self._infer_expression_type(node.value)
        return 'None'


class ScopeAnalyzer:
    """作用域分析器"""
    
    def __init__(self):
        self.scope_stack = []
        self.symbol_table = {}
    
    def analyze_scopes(self, ast_tree: ast.AST) -> Dict[str, Any]:
        """分析作用域"""
        self.scope_stack = [{'type': 'global', 'symbols': {}}]
        
        def visit_node(node):
            if isinstance(node, ast.FunctionDef):
                self._enter_function_scope(node)
                for child in ast.iter_child_nodes(node):
                    visit_node(child)
                self._exit_scope()
            elif isinstance(node, ast.ClassDef):
                self._enter_class_scope(node)
                for child in ast.iter_child_nodes(node):
                    visit_node(child)
                self._exit_scope()
            elif isinstance(node, ast.Name):
                self._analyze_name_usage(node)
            else:
                for child in ast.iter_child_nodes(node):
                    visit_node(child)
        
        visit_node(ast_tree)
        return self.symbol_table
    
    def _enter_function_scope(self, func_def: ast.FunctionDef):
        """进入函数作用域"""
        scope = {
            'type': 'function',
            'name': func_def.name,
            'symbols': {},
            'parameters': [arg.arg for arg in func_def.args.args]
        }
        self.scope_stack.append(scope)
        
        # 添加参数到符号表
        for param in scope['parameters']:
            scope['symbols'][param] = {'type': 'parameter', 'scope': 'local'}
    
    def _enter_class_scope(self, class_def: ast.ClassDef):
        """进入类作用域"""
        scope = {
            'type': 'class',
            'name': class_def.name,
            'symbols': {},
            'methods': []
        }
        self.scope_stack.append(scope)
    
    def _exit_scope(self):
        """退出作用域"""
        if self.scope_stack:
            self.scope_stack.pop()
    
    def _analyze_name_usage(self, name_node: ast.Name):
        """分析名称使用"""
        name = name_node.id
        scope_level = self._find_name_in_scopes(name)
        
        if scope_level is not None:
            self.symbol_table[name] = {
                'scope_level': scope_level,
                'usage_type': 'read' if isinstance(name_node.ctx, ast.Load) else 'write'
            }
    
    def _find_name_in_scopes(self, name: str) -> Optional[int]:
        """在作用域栈中查找名称"""
        for i, scope in enumerate(reversed(self.scope_stack)):
            if name in scope['symbols']:
                return len(self.scope_stack) - 1 - i
        return None


class SemanticOptimizer:
    """语义优化器"""
    
    def __init__(self):
        self.optimizations = []
    
    def optimize_ast(self, ast_tree: ast.AST) -> ast.AST:
        """优化AST"""
        # 常量折叠
        ast_tree = self._constant_folding(ast_tree)
        
        # 死代码消除
        ast_tree = self._dead_code_elimination(ast_tree)
        
        # 表达式简化
        ast_tree = self._expression_simplification(ast_tree)
        
        return ast_tree
    
    def _constant_folding(self, ast_tree: ast.AST) -> ast.AST:
        """常量折叠"""
        class ConstantFolder(ast.NodeTransformer):
            def visit_BinOp(self, node):
                if (isinstance(node.left, ast.Num) and 
                    isinstance(node.right, ast.Num)):
                    left_val = node.left.n
                    right_val = node.right.n
                    
                    if isinstance(node.op, ast.Add):
                        return ast.Num(n=left_val + right_val)
                    elif isinstance(node.op, ast.Sub):
                        return ast.Num(n=left_val - right_val)
                    elif isinstance(node.op, ast.Mult):
                        return ast.Num(n=left_val * right_val)
                    elif isinstance(node.op, ast.Div):
                        return ast.Num(n=left_val / right_val)
                
                return node
        
        return ConstantFolder().visit(ast_tree)
    
    def _dead_code_elimination(self, ast_tree: ast.AST) -> ast.AST:
        """死代码消除"""
        class DeadCodeEliminator(ast.NodeTransformer):
            def visit_If(self, node):
                if isinstance(node.test, ast.NameConstant):
                    if node.test.value is True:
                        return node.body
                    elif node.test.value is False:
                        return node.orelse
                return node
        
        return DeadCodeEliminator().visit(ast_tree)
    
    def _expression_simplification(self, ast_tree: ast.AST) -> ast.AST:
        """表达式简化"""
        class ExpressionSimplifier(ast.NodeTransformer):
            def visit_BinOp(self, node):
                if isinstance(node.op, ast.Add):
                    if isinstance(node.right, ast.Num) and node.right.n == 0:
                        return node.left
                    elif isinstance(node.left, ast.Num) and node.left.n == 0:
                        return node.right
                
                elif isinstance(node.op, ast.Mult):
                    if isinstance(node.right, ast.Num) and node.right.n == 1:
                        return node.left
                    elif isinstance(node.left, ast.Num) and node.left.n == 1:
                        return node.right
                
                return node
        
        return ExpressionSimplifier().visit(ast_tree)


def demo_semantic_analysis():
    """演示语义分析"""
    print("=== Python语义模型演示 ===\n")
    
    # 测试代码
    test_code = """
x = 42
y = "hello"
z = [1, 2, 3]

def add_numbers(a, b):
    result = a + b
    return result

def process_data(data):
    if len(data) > 0:
        return data[0]
    else:
        return None

class Calculator:
    def __init__(self):
        self.value = 0
    
    def add(self, x):
        self.value += x
        return self.value

# 测试代码
result = add_numbers(10, 20)
calc = Calculator()
final_result = calc.add(result)
"""
    
    print("测试代码:")
    print(test_code)
    print("-" * 50)
    
    # 语义分析
    analyzer = PythonSemanticAnalyzer()
    semantic_info = analyzer.analyze_code(test_code)
    
    print("语义分析结果:")
    print(f"类型信息: {semantic_info.type_info}")
    print(f"作用域信息: {semantic_info.scope_info}")
    print(f"错误: {semantic_info.errors}")
    print(f"警告: {semantic_info.warnings}")
    print("-" * 50)
    
    # 类型推断
    ast_tree = ast.parse(test_code)
    type_inferrer = TypeInferrer()
    inferred_types = type_inferrer.infer_types(ast_tree)
    
    print("类型推断结果:")
    for var, type_info in inferred_types.items():
        print(f"  {var}: {type_info}")
    print("-" * 50)
    
    # 作用域分析
    scope_analyzer = ScopeAnalyzer()
    scope_info = scope_analyzer.analyze_scopes(ast_tree)
    
    print("作用域分析结果:")
    for symbol, info in scope_info.items():
        print(f"  {symbol}: {info}")
    print("-" * 50)
    
    # 语义优化
    optimizer = SemanticOptimizer()
    optimized_ast = optimizer.optimize_ast(ast_tree)
    
    print("语义优化完成")
    print("-" * 50)
    
    # 演示鸭子类型
    print("鸭子类型演示:")
    duck_type_code = """
def process_data(obj):
    if hasattr(obj, '__len__'):
        return len(obj)
    return 0

# 测试不同类型的对象
data1 = [1, 2, 3]
data2 = "hello"
data3 = {"a": 1, "b": 2}

result1 = process_data(data1)  # 3
result2 = process_data(data2)  # 5
result3 = process_data(data3)  # 2
"""
    
    print(duck_type_code)
    
    # 分析鸭子类型代码
    duck_analyzer = PythonSemanticAnalyzer()
    duck_semantic_info = duck_analyzer.analyze_code(duck_type_code)
    
    print("鸭子类型语义分析:")
    print(f"类型信息: {duck_semantic_info.type_info}")
    print(f"作用域信息: {duck_semantic_info.scope_info}")
    print("-" * 50)
    
    # 演示动态语义
    print("动态语义演示:")
    dynamic_code = """
x = 42          # int类型
print(f"x的类型: {type(x)}")

x = "hello"     # 动态改变为str类型
print(f"x的类型: {type(x)}")

x = [1, 2, 3]   # 动态改变为list类型
print(f"x的类型: {type(x)}")
"""
    
    print(dynamic_code)
    
    # 分析动态语义代码
    dynamic_analyzer = PythonSemanticAnalyzer()
    dynamic_semantic_info = dynamic_analyzer.analyze_code(dynamic_code)
    
    print("动态语义分析:")
    print(f"类型信息: {dynamic_semantic_info.type_info}")
    print("-" * 50)
    
    print("=== 演示完成 ===")


def demo_advanced_features():
    """演示高级特性"""
    print("\n=== 高级特性演示 ===\n")
    
    # 闭包演示
    closure_code = """
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

# 创建闭包
add_five = outer_function(5)
result = add_five(3)  # 8
"""
    
    print("闭包语义演示:")
    print(closure_code)
    
    closure_analyzer = PythonSemanticAnalyzer()
    closure_info = closure_analyzer.analyze_code(closure_code)
    
    print("闭包分析结果:")
    print(f"作用域信息: {closure_info.scope_info}")
    print("-" * 50)
    
    # 异常处理语义
    exception_code = """
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return None
    finally:
        print("计算完成")

# 测试异常处理
result1 = safe_divide(10, 2)   # 5.0
result2 = safe_divide(10, 0)   # None
"""
    
    print("异常处理语义演示:")
    print(exception_code)
    
    exception_analyzer = PythonSemanticAnalyzer()
    exception_info = exception_analyzer.analyze_code(exception_code)
    
    print("异常处理分析:")
    print(f"类型信息: {exception_info.type_info}")
    print(f"错误: {exception_info.errors}")
    print("-" * 50)
    
    print("=== 高级特性演示完成 ===")


if __name__ == "__main__":
    # 运行演示
    demo_semantic_analysis()
    demo_advanced_features()
    
    print("\nPython语义模型演示完成！")
    print("本演示展示了Python语义模型的核心功能，包括：")
    print("1. 语义分析和验证")
    print("2. 类型推断和检查")
    print("3. 作用域分析")
    print("4. 语义优化")
    print("5. 鸭子类型支持")
    print("6. 动态语义特性")
    print("7. 闭包和异常处理语义") 