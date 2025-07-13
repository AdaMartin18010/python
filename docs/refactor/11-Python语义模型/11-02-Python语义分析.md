# Python语义分析

## 1. Python语义分析概述

### 1.1 语义分析定义

Python语义分析是对Python程序进行语义理解和验证的过程，包括：

1. **语义检查**：验证程序的语义正确性
2. **类型推断**：推断变量和表达式的类型
3. **作用域分析**：分析变量和函数的作用域
4. **控制流分析**：分析程序的控制流
5. **数据流分析**：分析数据的流动和变化

### 1.2 语义分析层次

**层次 11.2.1** 静态语义分析

```python
# 静态语义分析示例
def analyze_static_semantics(code):
    # 1. 语法分析
    ast = parse(code)
    
    # 2. 符号表构建
    symbol_table = build_symbol_table(ast)
    
    # 3. 类型检查
    type_info = type_check(ast, symbol_table)
    
    # 4. 作用域分析
    scope_info = analyze_scopes(ast)
    
    return {
        'ast': ast,
        'symbol_table': symbol_table,
        'type_info': type_info,
        'scope_info': scope_info
    }
```

**层次 11.2.2** 动态语义分析

```python
# 动态语义分析示例
def analyze_dynamic_semantics(code):
    # 1. 运行时类型检查
    runtime_types = check_runtime_types(code)
    
    # 2. 异常分析
    exception_analysis = analyze_exceptions(code)
    
    # 3. 性能分析
    performance_analysis = analyze_performance(code)
    
    return {
        'runtime_types': runtime_types,
        'exception_analysis': exception_analysis,
        'performance_analysis': performance_analysis
    }
```

## 2. Python类型语义分析

### 2.1 类型推断算法

**算法 11.2.1** 基础类型推断

```python
class TypeInferrer:
    """Python类型推断器"""
    
    def __init__(self):
        self.type_environment = {}
        self.type_constraints = []
    
    def infer_type(self, expression):
        """推断表达式的类型"""
        if isinstance(expression, ast.Num):
            return self._infer_literal_type(expression)
        elif isinstance(expression, ast.Name):
            return self._infer_variable_type(expression)
        elif isinstance(expression, ast.BinOp):
            return self._infer_binary_op_type(expression)
        elif isinstance(expression, ast.Call):
            return self._infer_function_call_type(expression)
        else:
            return self._infer_generic_type(expression)
    
    def _infer_literal_type(self, literal):
        """推断字面量类型"""
        if isinstance(literal.n, int):
            return 'int'
        elif isinstance(literal.n, float):
            return 'float'
        elif isinstance(literal.n, complex):
            return 'complex'
        else:
            return 'unknown'
    
    def _infer_variable_type(self, variable):
        """推断变量类型"""
        var_name = variable.id
        if var_name in self.type_environment:
            return self.type_environment[var_name]
        else:
            return 'unknown'
    
    def _infer_binary_op_type(self, bin_op):
        """推断二元操作类型"""
        left_type = self.infer_type(bin_op.left)
        right_type = self.infer_type(bin_op.right)
        
        # 根据操作符和操作数类型推断结果类型
        if isinstance(bin_op.op, ast.Add):
            if left_type == 'str' and right_type == 'str':
                return 'str'
            elif left_type in ['int', 'float'] and right_type in ['int', 'float']:
                return 'float' if 'float' in [left_type, right_type] else 'int'
        
        return 'unknown'
```

### 2.2 鸭子类型分析

**分析 11.2.1** 鸭子类型语义分析

```python
class DuckTypeAnalyzer:
    """鸭子类型分析器"""
    
    def __init__(self):
        self.interface_requirements = {}
    
    def analyze_duck_typing(self, function_def):
        """分析函数的鸭子类型要求"""
        requirements = {
            'attributes': set(),
            'methods': set(),
            'protocols': set()
        }
        
        # 分析函数体中的属性访问和方法调用
        for node in ast.walk(function_def):
            if isinstance(node, ast.Attribute):
                requirements['attributes'].add(node.attr)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    requirements['methods'].add(node.func.attr)
        
        return requirements
    
    def check_interface_compatibility(self, obj_type, requirements):
        """检查对象类型是否满足接口要求"""
        compatibility = {
            'attributes': [],
            'methods': [],
            'protocols': []
        }
        
        # 检查属性
        for attr in requirements['attributes']:
            if hasattr(obj_type, attr):
                compatibility['attributes'].append(attr)
        
        # 检查方法
        for method in requirements['methods']:
            if hasattr(obj_type, method):
                compatibility['methods'].append(method)
        
        return compatibility
```

## 3. Python作用域语义分析

### 3.1 作用域分析算法

**算法 11.2.2** LEGB作用域分析

```python
class ScopeAnalyzer:
    """作用域分析器"""
    
    def __init__(self):
        self.scope_stack = []
        self.symbol_table = {}
    
    def analyze_scopes(self, ast_tree):
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
    
    def _enter_function_scope(self, func_def):
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
    
    def _enter_class_scope(self, class_def):
        """进入类作用域"""
        scope = {
            'type': 'class',
            'name': class_def.name,
            'symbols': {},
            'methods': []
        }
        self.scope_stack.append(scope)
    
    def _analyze_name_usage(self, name_node):
        """分析名称使用"""
        name = name_node.id
        scope_level = self._find_name_in_scopes(name)
        
        if scope_level is not None:
            self.symbol_table[name] = {
                'scope_level': scope_level,
                'usage_type': 'read' if isinstance(name_node.ctx, ast.Load) else 'write'
            }
    
    def _find_name_in_scopes(self, name):
        """在作用域栈中查找名称"""
        for i, scope in enumerate(reversed(self.scope_stack)):
            if name in scope['symbols']:
                return len(self.scope_stack) - 1 - i
        return None
```

### 3.2 闭包分析

**分析 11.2.2** 闭包语义分析

```python
class ClosureAnalyzer:
    """闭包分析器"""
    
    def __init__(self):
        self.closure_vars = {}
        self.free_vars = {}
    
    def analyze_closure(self, function_def):
        """分析函数的闭包变量"""
        # 收集函数中使用的变量
        used_vars = self._collect_used_variables(function_def)
        
        # 识别自由变量（在函数外部定义但在函数内部使用）
        free_vars = self._identify_free_variables(function_def, used_vars)
        
        # 分析闭包变量的生命周期
        closure_info = self._analyze_closure_lifetime(function_def, free_vars)
        
        return {
            'function_name': function_def.name,
            'free_variables': free_vars,
            'closure_info': closure_info
        }
    
    def _collect_used_variables(self, function_def):
        """收集函数中使用的变量"""
        used_vars = set()
        
        for node in ast.walk(function_def):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Load):
                    used_vars.add(node.id)
        
        return used_vars
    
    def _identify_free_variables(self, function_def, used_vars):
        """识别自由变量"""
        # 获取函数参数和局部变量
        local_vars = set()
        
        # 添加参数
        for arg in function_def.args.args:
            local_vars.add(arg.arg)
        
        # 添加局部变量（简化处理）
        for node in ast.walk(function_def):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        local_vars.add(target.id)
        
        # 自由变量 = 使用的变量 - 局部变量
        free_vars = used_vars - local_vars
        return free_vars
```

## 4. Python控制流语义分析

### 4.1 控制流图构建

**算法 11.2.3** 控制流图构建

```python
class ControlFlowAnalyzer:
    """控制流分析器"""
    
    def __init__(self):
        self.cfg = {}
        self.basic_blocks = []
        self.edges = []
    
    def build_control_flow_graph(self, ast_tree):
        """构建控制流图"""
        # 将AST转换为基本块
        self.basic_blocks = self._extract_basic_blocks(ast_tree)
        
        # 构建基本块之间的边
        self.edges = self._build_edges()
        
        # 分析控制流
        flow_analysis = self._analyze_control_flow()
        
        return {
            'basic_blocks': self.basic_blocks,
            'edges': self.edges,
            'flow_analysis': flow_analysis
        }
    
    def _extract_basic_blocks(self, ast_tree):
        """提取基本块"""
        blocks = []
        current_block = []
        
        def visit_node(node):
            nonlocal current_block
            
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                # 结束当前块
                if current_block:
                    blocks.append(current_block)
                    current_block = []
                
                # 处理控制流节点
                self._handle_control_flow_node(node)
            else:
                current_block.append(node)
        
        # 遍历AST
        for node in ast.walk(ast_tree):
            visit_node(node)
        
        # 添加最后一个块
        if current_block:
            blocks.append(current_block)
        
        return blocks
    
    def _handle_control_flow_node(self, node):
        """处理控制流节点"""
        if isinstance(node, ast.If):
            self._handle_if_statement(node)
        elif isinstance(node, ast.For):
            self._handle_for_loop(node)
        elif isinstance(node, ast.While):
            self._handle_while_loop(node)
        elif isinstance(node, ast.Try):
            self._handle_try_statement(node)
    
    def _analyze_control_flow(self):
        """分析控制流"""
        analysis = {
            'reachability': self._analyze_reachability(),
            'dominators': self._analyze_dominators(),
            'loops': self._analyze_loops()
        }
        return analysis
```

### 4.2 数据流分析

**分析 11.2.3** 数据流语义分析

```python
class DataFlowAnalyzer:
    """数据流分析器"""
    
    def __init__(self):
        self.def_use_chains = {}
        self.live_variables = {}
        self.reaching_definitions = {}
    
    def analyze_data_flow(self, ast_tree):
        """分析数据流"""
        # 构建定义-使用链
        self.def_use_chains = self._build_def_use_chains(ast_tree)
        
        # 活跃变量分析
        self.live_variables = self._analyze_live_variables(ast_tree)
        
        # 到达定义分析
        self.reaching_definitions = self._analyze_reaching_definitions(ast_tree)
        
        return {
            'def_use_chains': self.def_use_chains,
            'live_variables': self.live_variables,
            'reaching_definitions': self.reaching_definitions
        }
    
    def _build_def_use_chains(self, ast_tree):
        """构建定义-使用链"""
        def_use_chains = {}
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Assign):
                # 处理赋值语句
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        def_use_chains[var_name] = {
                            'definitions': [],
                            'uses': []
                        }
                        
                        # 添加定义
                        def_use_chains[var_name]['definitions'].append({
                            'node': node,
                            'line': node.lineno
                        })
            
            elif isinstance(node, ast.Name):
                # 处理变量使用
                var_name = node.id
                if var_name in def_use_chains:
                    def_use_chains[var_name]['uses'].append({
                        'node': node,
                        'line': node.lineno,
                        'context': 'load' if isinstance(node.ctx, ast.Load) else 'store'
                    })
        
        return def_use_chains
    
    def _analyze_live_variables(self, ast_tree):
        """分析活跃变量"""
        # 简化实现：识别在函数中使用的变量
        live_vars = set()
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Load):
                    live_vars.add(node.id)
        
        return live_vars
```

## 5. Python异常语义分析

### 5.1 异常流分析

**分析 11.2.4** 异常语义分析

```python
class ExceptionAnalyzer:
    """异常分析器"""
    
    def __init__(self):
        self.exception_flows = {}
        self.handler_coverage = {}
    
    def analyze_exception_flow(self, ast_tree):
        """分析异常流"""
        # 识别可能抛出异常的语句
        exception_points = self._identify_exception_points(ast_tree)
        
        # 分析异常处理器
        exception_handlers = self._analyze_exception_handlers(ast_tree)
        
        # 分析异常传播路径
        propagation_paths = self._analyze_propagation_paths(ast_tree)
        
        return {
            'exception_points': exception_points,
            'exception_handlers': exception_handlers,
            'propagation_paths': propagation_paths
        }
    
    def _identify_exception_points(self, ast_tree):
        """识别可能抛出异常的语句"""
        exception_points = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Call):
                # 函数调用可能抛出异常
                exception_points.append({
                    'type': 'function_call',
                    'node': node,
                    'line': node.lineno
                })
            elif isinstance(node, ast.BinOp):
                # 二元操作可能抛出异常
                exception_points.append({
                    'type': 'binary_operation',
                    'node': node,
                    'line': node.lineno
                })
            elif isinstance(node, ast.Attribute):
                # 属性访问可能抛出异常
                exception_points.append({
                    'type': 'attribute_access',
                    'node': node,
                    'line': node.lineno
                })
        
        return exception_points
    
    def _analyze_exception_handlers(self, ast_tree):
        """分析异常处理器"""
        handlers = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    handlers.append({
                        'type': handler.type.id if handler.type else None,
                        'name': handler.name,
                        'body': handler.body,
                        'line': handler.lineno
                    })
        
        return handlers
```

## 6. Python性能语义分析

### 6.1 性能特征分析

**分析 11.2.5** 性能语义分析

```python
class PerformanceAnalyzer:
    """性能分析器"""
    
    def __init__(self):
        self.complexity_analysis = {}
        self.memory_analysis = {}
        self.bottleneck_analysis = {}
    
    def analyze_performance(self, ast_tree):
        """分析性能特征"""
        # 时间复杂度分析
        time_complexity = self._analyze_time_complexity(ast_tree)
        
        # 空间复杂度分析
        space_complexity = self._analyze_space_complexity(ast_tree)
        
        # 瓶颈识别
        bottlenecks = self._identify_bottlenecks(ast_tree)
        
        return {
            'time_complexity': time_complexity,
            'space_complexity': space_complexity,
            'bottlenecks': bottlenecks
        }
    
    def _analyze_time_complexity(self, ast_tree):
        """分析时间复杂度"""
        complexity = 'O(1)'  # 默认复杂度
        
        # 分析循环结构
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.For):
                # 嵌套循环会增加复杂度
                if complexity == 'O(1)':
                    complexity = 'O(n)'
                elif complexity == 'O(n)':
                    complexity = 'O(n²)'
            elif isinstance(node, ast.While):
                # while循环需要更仔细的分析
                complexity = 'O(n)'  # 简化处理
        
        return complexity
    
    def _analyze_space_complexity(self, ast_tree):
        """分析空间复杂度"""
        space_usage = {
            'variables': 0,
            'data_structures': [],
            'recursion_depth': 0
        }
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Assign):
                space_usage['variables'] += 1
            
            elif isinstance(node, (ast.List, ast.Dict, ast.Set)):
                space_usage['data_structures'].append({
                    'type': type(node).__name__,
                    'line': node.lineno
                })
        
        return space_usage
    
    def _identify_bottlenecks(self, ast_tree):
        """识别性能瓶颈"""
        bottlenecks = []
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Call):
                # 检查是否是已知的慢函数
                if hasattr(node.func, 'id'):
                    func_name = node.func.id
                    if func_name in ['sort', 'sorted', 'filter', 'map']:
                        bottlenecks.append({
                            'type': 'slow_function',
                            'function': func_name,
                            'line': node.lineno
                        })
            
            elif isinstance(node, ast.For):
                # 检查循环中的操作
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        bottlenecks.append({
                            'type': 'loop_operation',
                            'operation': 'function_call_in_loop',
                            'line': child.lineno
                        })
        
        return bottlenecks
```

## 7. 总结

Python语义分析涵盖了多个重要方面：

1. **类型语义分析**：包括类型推断和鸭子类型分析
2. **作用域语义分析**：LEGB规则和闭包分析
3. **控制流语义分析**：控制流图构建和数据流分析
4. **异常语义分析**：异常流和处理器分析
5. **性能语义分析**：复杂度和瓶颈分析

这些分析为Python程序的优化、调试和维护提供了重要的理论基础。
