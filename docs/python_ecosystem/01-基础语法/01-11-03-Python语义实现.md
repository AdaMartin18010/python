# Python语义实现

## 1. Python语义实现概述

### 1.1 实现架构

Python语义实现包括以下几个核心组件：

1. **语义解析器**：解析Python代码并构建语义表示
2. **语义检查器**：验证语义正确性
3. **语义优化器**：优化语义表示
4. **语义执行器**：执行语义操作
5. **语义调试器**：调试语义问题

### 1.2 实现层次

**层次 11.3.1** 语义解析实现

```python
class SemanticParser:
    """Python语义解析器"""
    
    def __init__(self):
        self.ast_parser = ast.parse
        self.semantic_tree = {}
        self.symbol_table = {}
    
    def parse_semantics(self, source_code):
        """解析Python代码的语义"""
        # 1. 语法分析
        ast_tree = self.ast_parser(source_code)
        
        # 2. 语义分析
        semantic_info = self._analyze_semantics(ast_tree)
        
        # 3. 符号表构建
        symbol_table = self._build_symbol_table(ast_tree)
        
        # 4. 类型信息收集
        type_info = self._collect_type_info(ast_tree)
        
        return {
            'ast': ast_tree,
            'semantic_info': semantic_info,
            'symbol_table': symbol_table,
            'type_info': type_info
        }
    
    def _analyze_semantics(self, ast_tree):
        """分析语义信息"""
        semantic_info = {
            'expressions': [],
            'statements': [],
            'functions': [],
            'classes': []
        }
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Expr):
                semantic_info['expressions'].append(self._analyze_expression(node))
            elif isinstance(node, ast.Assign):
                semantic_info['statements'].append(self._analyze_statement(node))
            elif isinstance(node, ast.FunctionDef):
                semantic_info['functions'].append(self._analyze_function(node))
            elif isinstance(node, ast.ClassDef):
                semantic_info['classes'].append(self._analyze_class(node))
        
        return semantic_info
```

## 2. Python语义检查实现

### 2.1 语义验证器

**实现 11.3.1** 语义验证器

```python
class SemanticValidator:
    """Python语义验证器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.symbol_table = {}
    
    def validate_semantics(self, ast_tree):
        """验证语义正确性"""
        # 1. 作用域验证
        scope_errors = self._validate_scopes(ast_tree)
        
        # 2. 类型验证
        type_errors = self._validate_types(ast_tree)
        
        # 3. 控制流验证
        flow_errors = self._validate_control_flow(ast_tree)
        
        # 4. 异常处理验证
        exception_errors = self._validate_exceptions(ast_tree)
        
        return {
            'scope_errors': scope_errors,
            'type_errors': type_errors,
            'flow_errors': flow_errors,
            'exception_errors': exception_errors,
            'is_valid': len(scope_errors + type_errors + flow_errors + exception_errors) == 0
        }
    
    def _validate_scopes(self, ast_tree):
        """验证作用域"""
        errors = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Name):
                # 检查变量是否在使用前定义
                if isinstance(node.ctx, ast.Load):
                    if not self._is_variable_defined(node.id, node):
                        errors.append({
                            'type': 'undefined_variable',
                            'variable': node.id,
                            'line': node.lineno
                        })
        
        return errors
    
    def _validate_types(self, ast_tree):
        """验证类型"""
        errors = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.BinOp):
                # 检查二元操作的类型兼容性
                type_error = self._check_binary_op_types(node)
                if type_error:
                    errors.append(type_error)
        
        return errors
    
    def _validate_control_flow(self, ast_tree):
        """验证控制流"""
        errors = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.For):
                # 检查迭代器是否可迭代
                if not self._is_iterable(node.iter):
                    errors.append({
                        'type': 'non_iterable_in_for',
                        'line': node.lineno
                    })
        
        return errors
    
    def _validate_exceptions(self, ast_tree):
        """验证异常处理"""
        errors = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Try):
                # 检查try块是否有对应的except
                if not node.handlers:
                    errors.append({
                        'type': 'bare_try_without_except',
                        'line': node.lineno
                    })
        
        return errors
```

### 2.2 类型检查器

**实现 11.3.2** 类型检查器

```python
class TypeChecker:
    """Python类型检查器"""
    
    def __init__(self):
        self.type_environment = {}
        self.type_constraints = []
    
    def check_types(self, ast_tree):
        """检查类型"""
        # 1. 收集类型信息
        type_info = self._collect_type_info(ast_tree)
        
        # 2. 推断类型
        inferred_types = self._infer_types(ast_tree)
        
        # 3. 检查类型一致性
        type_errors = self._check_type_consistency(ast_tree, inferred_types)
        
        # 4. 检查类型安全
        safety_errors = self._check_type_safety(ast_tree)
        
        return {
            'type_info': type_info,
            'inferred_types': inferred_types,
            'type_errors': type_errors,
            'safety_errors': safety_errors
        }
    
    def _collect_type_info(self, ast_tree):
        """收集类型信息"""
        type_info = {}
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Assign):
                # 收集赋值语句的类型信息
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        type_info[target.id] = self._infer_expression_type(node.value)
        
        return type_info
    
    def _infer_types(self, ast_tree):
        """推断类型"""
        inferred_types = {}
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Load):
                    inferred_types[node] = self._infer_variable_type(node.id)
            elif isinstance(node, ast.Call):
                inferred_types[node] = self._infer_call_type(node)
            elif isinstance(node, ast.BinOp):
                inferred_types[node] = self._infer_binary_op_type(node)
        
        return inferred_types
    
    def _infer_expression_type(self, expr):
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
    
    def _infer_variable_type(self, var_name):
        """推断变量类型"""
        if var_name in self.type_environment:
            return self.type_environment[var_name]
        else:
            return 'unknown'
    
    def _infer_call_type(self, call_node):
        """推断函数调用类型"""
        # 简化实现：根据函数名推断返回类型
        if hasattr(call_node.func, 'id'):
            func_name = call_node.func.id
            if func_name in ['len', 'str', 'int', 'float']:
                return func_name
            elif func_name in ['list', 'dict', 'set']:
                return func_name
        return 'unknown'
    
    def _infer_binary_op_type(self, bin_op):
        """推断二元操作类型"""
        left_type = self._infer_expression_type(bin_op.left)
        right_type = self._infer_expression_type(bin_op.right)
        
        if isinstance(bin_op.op, ast.Add):
            if left_type == 'str' and right_type == 'str':
                return 'str'
            elif left_type in ['int', 'float'] and right_type in ['int', 'float']:
                return 'float' if 'float' in [left_type, right_type] else 'int'
        
        return 'unknown'
```

## 3. Python语义优化实现

### 3.1 语义优化器

**实现 11.3.3** 语义优化器

```python
class SemanticOptimizer:
    """Python语义优化器"""
    
    def __init__(self):
        self.optimizations = []
        self.optimized_ast = None
    
    def optimize_semantics(self, ast_tree):
        """优化语义"""
        # 1. 常量折叠
        ast_tree = self._constant_folding(ast_tree)
        
        # 2. 死代码消除
        ast_tree = self._dead_code_elimination(ast_tree)
        
        # 3. 表达式简化
        ast_tree = self._expression_simplification(ast_tree)
        
        # 4. 循环优化
        ast_tree = self._loop_optimization(ast_tree)
        
        self.optimized_ast = ast_tree
        return ast_tree
    
    def _constant_folding(self, ast_tree):
        """常量折叠"""
        class ConstantFolder(ast.NodeTransformer):
            def visit_BinOp(self, node):
                # 如果两个操作数都是常量，计算结果
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
    
    def _dead_code_elimination(self, ast_tree):
        """死代码消除"""
        class DeadCodeEliminator(ast.NodeTransformer):
            def visit_If(self, node):
                # 如果条件总是True或False，消除分支
                if isinstance(node.test, ast.NameConstant):
                    if node.test.value is True:
                        return node.body
                    elif node.test.value is False:
                        return node.orelse
                return node
        
        return DeadCodeEliminator().visit(ast_tree)
    
    def _expression_simplification(self, ast_tree):
        """表达式简化"""
        class ExpressionSimplifier(ast.NodeTransformer):
            def visit_BinOp(self, node):
                # 简化 x + 0 -> x
                if isinstance(node.op, ast.Add):
                    if isinstance(node.right, ast.Num) and node.right.n == 0:
                        return node.left
                    elif isinstance(node.left, ast.Num) and node.left.n == 0:
                        return node.right
                
                # 简化 x * 1 -> x
                elif isinstance(node.op, ast.Mult):
                    if isinstance(node.right, ast.Num) and node.right.n == 1:
                        return node.left
                    elif isinstance(node.left, ast.Num) and node.left.n == 1:
                        return node.right
                
                return node
        
        return ExpressionSimplifier().visit(ast_tree)
    
    def _loop_optimization(self, ast_tree):
        """循环优化"""
        class LoopOptimizer(ast.NodeTransformer):
            def visit_For(self, node):
                # 优化 for i in range(n) 为 while 循环
                if (isinstance(node.iter, ast.Call) and
                    isinstance(node.iter.func, ast.Name) and
                    node.iter.func.id == 'range'):
                    # 转换为while循环
                    return self._convert_range_to_while(node)
                return node
            
            def _convert_range_to_while(self, for_node):
                """将range循环转换为while循环"""
                # 简化实现：这里只是示例
                return for_node
        
        return LoopOptimizer().visit(ast_tree)
```

### 3.2 性能优化器

**实现 11.3.4** 性能优化器

```python
class PerformanceOptimizer:
    """Python性能优化器"""
    
    def __init__(self):
        self.performance_metrics = {}
        self.optimization_suggestions = []
    
    def optimize_performance(self, ast_tree):
        """优化性能"""
        # 1. 分析性能瓶颈
        bottlenecks = self._analyze_bottlenecks(ast_tree)
        
        # 2. 生成优化建议
        suggestions = self._generate_optimization_suggestions(bottlenecks)
        
        # 3. 应用优化
        optimized_ast = self._apply_optimizations(ast_tree, suggestions)
        
        return {
            'bottlenecks': bottlenecks,
            'suggestions': suggestions,
            'optimized_ast': optimized_ast
        }
    
    def _analyze_bottlenecks(self, ast_tree):
        """分析性能瓶颈"""
        bottlenecks = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.For):
                # 检查循环中的操作
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        bottlenecks.append({
                            'type': 'function_call_in_loop',
                            'line': child.lineno,
                            'severity': 'high'
                        })
            
            elif isinstance(node, ast.ListComp):
                # 列表推导式可能比循环更高效
                bottlenecks.append({
                    'type': 'list_comprehension_opportunity',
                    'line': node.lineno,
                    'severity': 'medium'
                })
        
        return bottlenecks
    
    def _generate_optimization_suggestions(self, bottlenecks):
        """生成优化建议"""
        suggestions = []
        
        for bottleneck in bottlenecks:
            if bottleneck['type'] == 'function_call_in_loop':
                suggestions.append({
                    'type': 'move_function_call_outside_loop',
                    'line': bottleneck['line'],
                    'description': '将函数调用移到循环外部'
                })
            elif bottleneck['type'] == 'list_comprehension_opportunity':
                suggestions.append({
                    'type': 'use_list_comprehension',
                    'line': bottleneck['line'],
                    'description': '使用列表推导式替代循环'
                })
        
        return suggestions
    
    def _apply_optimizations(self, ast_tree, suggestions):
        """应用优化"""
        # 这里实现具体的优化应用
        # 简化实现：返回原始AST
        return ast_tree
```

## 4. Python语义执行实现

### 4.1 语义执行器

**实现 11.3.5** 语义执行器

```python
class SemanticExecutor:
    """Python语义执行器"""
    
    def __init__(self):
        self.execution_environment = {}
        self.execution_trace = []
    
    def execute_semantics(self, ast_tree):
        """执行语义"""
        # 1. 初始化执行环境
        self._initialize_environment()
        
        # 2. 执行AST
        result = self._execute_ast(ast_tree)
        
        # 3. 收集执行信息
        execution_info = self._collect_execution_info()
        
        return {
            'result': result,
            'execution_info': execution_info,
            'trace': self.execution_trace
        }
    
    def _initialize_environment(self):
        """初始化执行环境"""
        self.execution_environment = {
            'variables': {},
            'functions': {},
            'classes': {},
            'modules': {}
        }
    
    def _execute_ast(self, ast_tree):
        """执行AST"""
        if isinstance(ast_tree, ast.Module):
            return self._execute_module(ast_tree)
        elif isinstance(ast_tree, ast.FunctionDef):
            return self._execute_function_def(ast_tree)
        elif isinstance(ast_tree, ast.ClassDef):
            return self._execute_class_def(ast_tree)
        else:
            return self._execute_statement(ast_tree)
    
    def _execute_module(self, module):
        """执行模块"""
        results = []
        for stmt in module.body:
            result = self._execute_statement(stmt)
            results.append(result)
        return results
    
    def _execute_statement(self, stmt):
        """执行语句"""
        if isinstance(stmt, ast.Assign):
            return self._execute_assign(stmt)
        elif isinstance(stmt, ast.Expr):
            return self._execute_expression(stmt.value)
        elif isinstance(stmt, ast.If):
            return self._execute_if(stmt)
        elif isinstance(stmt, ast.For):
            return self._execute_for(stmt)
        else:
            return None
    
    def _execute_assign(self, assign):
        """执行赋值语句"""
        value = self._execute_expression(assign.value)
        
        for target in assign.targets:
            if isinstance(target, ast.Name):
                self.execution_environment['variables'][target.id] = value
                self.execution_trace.append({
                    'type': 'assignment',
                    'variable': target.id,
                    'value': value
                })
        
        return value
    
    def _execute_expression(self, expr):
        """执行表达式"""
        if isinstance(expr, ast.Num):
            return expr.n
        elif isinstance(expr, ast.Str):
            return expr.s
        elif isinstance(expr, ast.Name):
            return self.execution_environment['variables'].get(expr.id)
        elif isinstance(expr, ast.BinOp):
            left = self._execute_expression(expr.left)
            right = self._execute_expression(expr.right)
            
            if isinstance(expr.op, ast.Add):
                return left + right
            elif isinstance(expr.op, ast.Sub):
                return left - right
            elif isinstance(expr.op, ast.Mult):
                return left * right
            elif isinstance(expr.op, ast.Div):
                return left / right
        
        return None
    
    def _execute_if(self, if_stmt):
        """执行if语句"""
        condition = self._execute_expression(if_stmt.test)
        
        if condition:
            for stmt in if_stmt.body:
                self._execute_statement(stmt)
        else:
            for stmt in if_stmt.orelse:
                self._execute_statement(stmt)
    
    def _execute_for(self, for_stmt):
        """执行for循环"""
        iterable = self._execute_expression(for_stmt.iter)
        
        if hasattr(iterable, '__iter__'):
            for item in iterable:
                if isinstance(for_stmt.target, ast.Name):
                    self.execution_environment['variables'][for_stmt.target.id] = item
                
                for stmt in for_stmt.body:
                    self._execute_statement(stmt)
    
    def _collect_execution_info(self):
        """收集执行信息"""
        return {
            'variables': self.execution_environment['variables'],
            'trace_length': len(self.execution_trace),
            'execution_time': 0  # 简化实现
        }
```

## 5. Python语义调试实现

### 5.1 语义调试器

**实现 11.3.6** 语义调试器

```python
class SemanticDebugger:
    """Python语义调试器"""
    
    def __init__(self):
        self.breakpoints = []
        self.debug_info = {}
        self.execution_state = {}
    
    def debug_semantics(self, ast_tree):
        """调试语义"""
        # 1. 设置断点
        self._setup_breakpoints(ast_tree)
        
        # 2. 执行调试
        debug_result = self._execute_debug(ast_tree)
        
        # 3. 收集调试信息
        debug_info = self._collect_debug_info()
        
        return {
            'debug_result': debug_result,
            'debug_info': debug_info,
            'breakpoints': self.breakpoints
        }
    
    def _setup_breakpoints(self, ast_tree):
        """设置断点"""
        for node in ast.walk(ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                self.breakpoints.append({
                    'type': 'function_or_class',
                    'name': node.name,
                    'line': node.lineno
                })
            elif isinstance(node, ast.Assign):
                self.breakpoints.append({
                    'type': 'assignment',
                    'line': node.lineno
                })
    
    def _execute_debug(self, ast_tree):
        """执行调试"""
        debug_result = {
            'executed_nodes': [],
            'variable_states': [],
            'error_points': []
        }
        
        # 简化实现：遍历AST并记录执行信息
        for node in ast.walk(ast_tree):
            if hasattr(node, 'lineno'):
                debug_result['executed_nodes'].append({
                    'type': type(node).__name__,
                    'line': node.lineno
                })
        
        return debug_result
    
    def _collect_debug_info(self):
        """收集调试信息"""
        return {
            'total_nodes': len(self.breakpoints),
            'execution_path': [],
            'memory_usage': 0  # 简化实现
        }
```

## 6. 总结

Python语义实现提供了完整的语义处理框架：

1. **语义解析**：将Python代码转换为语义表示
2. **语义检查**：验证语义正确性和类型安全
3. **语义优化**：优化语义表示以提高性能
4. **语义执行**：执行语义操作并收集执行信息
5. **语义调试**：调试语义问题和性能瓶颈

这些实现为Python程序的开发、优化和调试提供了强大的工具支持。
