# 07-实践应用 (Practical Application)

## 概述

实践应用层将前面各层的理论知识转化为具体的工程实践。这一层涵盖了开发实践、测试策略、部署运维、性能优化和安全实践等核心内容，为软件工程提供了完整的实践指导。

## 目录结构

```
07-实践应用/
├── 01-开发实践/
│   ├── 01-代码规范.md
│   ├── 02-版本控制.md
│   ├── 03-代码审查.md
│   └── 04-持续集成.md
├── 02-测试策略/
│   ├── 01-单元测试.md
│   ├── 02-集成测试.md
│   ├── 03-性能测试.md
│   └── 04-自动化测试.md
├── 03-部署运维/
│   ├── 01-容器化部署.md
│   ├── 02-云原生部署.md
│   ├── 03-监控告警.md
│   └── 04-故障处理.md
├── 04-性能优化/
│   ├── 01-代码优化.md
│   ├── 02-数据库优化.md
│   ├── 03-缓存优化.md
│   └── 04-系统优化.md
└── 05-安全实践/
    ├── 01-代码安全.md
    ├── 02-数据安全.md
    ├── 03-网络安全.md
    └── 04-安全运维.md
```

## 核心实践

### 1. 开发实践

```math
\text{开发实践框架:}

\text{实践} P = (C, V, R, I)

\text{其中:}
\begin{align}
C &= \text{代码规范 (Code Standards)} \\
V &= \text{版本控制 (Version Control)} \\
R &= \text{代码审查 (Code Review)} \\
I &= \text{持续集成 (Continuous Integration)}
\end{align}
```

### 2. 测试策略

```math
\text{测试策略模型:}

\text{测试} T = (U, I, P, A)

\text{其中:}
\begin{align}
U &= \text{单元测试 (Unit Testing)} \\
I &= \text{集成测试 (Integration Testing)} \\
P &= \text{性能测试 (Performance Testing)} \\
A &= \text{自动化测试 (Automated Testing)}
\end{align}
```

### 3. 部署运维

```math
\text{部署运维模型:}

\text{运维} O = (D, M, A, F)

\text{其中:}
\begin{align}
D &= \text{部署 (Deployment)} \\
M &= \text{监控 (Monitoring)} \\
A &= \text{告警 (Alerting)} \\
F &= \text{故障处理 (Fault Handling)}
\end{align}
```

## Python实现

### 1. 开发实践实现

```python
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import subprocess
import json
import os
import re

@dataclass
class CodeReview:
    """代码审查"""
    id: str
    author: str
    reviewers: List[str]
    files: List[str]
    status: str
    comments: List[Dict[str, Any]]
    created_at: datetime

class CodeQualityChecker:
    """代码质量检查器"""
    
    def __init__(self):
        self.rules: Dict[str, Callable] = {
            "function_length": self._check_function_length,
            "naming_convention": self._check_naming_convention,
            "complexity": self._check_complexity,
            "documentation": self._check_documentation
        }
    
    def check_file(self, file_path: str) -> Dict[str, Any]:
        """检查文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {}
        for rule_name, rule_func in self.rules.items():
            results[rule_name] = rule_func(content)
        
        return results
    
    def _check_function_length(self, content: str) -> Dict[str, Any]:
        """检查函数长度"""
        lines = content.split('\n')
        functions = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                # 找到函数结束
                start_line = i
                end_line = start_line
                indent_level = len(line) - len(line.lstrip())
                
                for j in range(start_line + 1, len(lines)):
                    if lines[j].strip() and len(lines[j]) - len(lines[j].lstrip()) <= indent_level:
                        end_line = j - 1
                        break
                    end_line = j
                
                function_length = end_line - start_line + 1
                functions.append({
                    "name": line.split('(')[0].split('def ')[1].strip(),
                    "length": function_length,
                    "line": start_line + 1
                })
        
        long_functions = [f for f in functions if f["length"] > 20]
        
        return {
            "total_functions": len(functions),
            "long_functions": long_functions,
            "passed": len(long_functions) == 0
        }
    
    def _check_naming_convention(self, content: str) -> Dict[str, Any]:
        """检查命名规范"""
        issues = []
        
        # 检查函数名
        function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        functions = re.findall(function_pattern, content)
        
        for func_name in functions:
            if not func_name.islower() and '_' not in func_name:
                issues.append(f"Function '{func_name}' should use snake_case")
        
        # 检查类名
        class_pattern = r'class\s+([A-Z][a-zA-Z0-9_]*)'
        classes = re.findall(class_pattern, content)
        
        for class_name in classes:
            if not class_name[0].isupper():
                issues.append(f"Class '{class_name}' should use PascalCase")
        
        return {
            "issues": issues,
            "passed": len(issues) == 0
        }
    
    def _check_complexity(self, content: str) -> Dict[str, Any]:
        """检查复杂度"""
        # 简化的圈复杂度计算
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'and', 'or']
        complexity_score = 0
        
        for keyword in complexity_keywords:
            complexity_score += content.count(keyword)
        
        return {
            "complexity_score": complexity_score,
            "passed": complexity_score < 50
        }
    
    def _check_documentation(self, content: str) -> Dict[str, Any]:
        """检查文档"""
        issues = []
        
        # 检查函数是否有文档字符串
        function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        functions = re.findall(function_pattern, content)
        
        for func_name in functions:
            # 简化的文档检查
            if f'def {func_name}' in content:
                func_start = content.find(f'def {func_name}')
                func_end = content.find('\n', func_start)
                next_lines = content[func_end:func_end+200]
                
                if '"""' not in next_lines and "'''" not in next_lines:
                    issues.append(f"Function '{func_name}' missing docstring")
        
        return {
            "issues": issues,
            "passed": len(issues) == 0
        }

class GitManager:
    """Git版本控制管理器"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
    
    def get_status(self) -> Dict[str, Any]:
        """获取仓库状态"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            return {
                "modified": [f for f in files if f.startswith('M')],
                "added": [f for f in files if f.startswith('A')],
                "deleted": [f for f in files if f.startswith('D')],
                "untracked": [f for f in files if f.startswith('??')]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def commit(self, message: str) -> bool:
        """提交更改"""
        try:
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', message], cwd=self.repo_path, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_branch(self) -> str:
        """获取当前分支"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except:
            return "unknown"
    
    def create_branch(self, branch_name: str) -> bool:
        """创建分支"""
        try:
            subprocess.run(['git', 'checkout', '-b', branch_name], cwd=self.repo_path, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

class ContinuousIntegration:
    """持续集成"""
    
    def __init__(self):
        self.pipelines: Dict[str, List[Callable]] = {}
        self.build_history: List[Dict[str, Any]] = []
    
    def add_pipeline(self, name: str, steps: List[Callable]) -> None:
        """添加流水线"""
        self.pipelines[name] = steps
    
    def run_pipeline(self, name: str) -> Dict[str, Any]:
        """运行流水线"""
        if name not in self.pipelines:
            return {"error": f"Pipeline {name} not found"}
        
        start_time = datetime.now()
        results = []
        
        try:
            for step in self.pipelines[name]:
                step_result = step()
                results.append(step_result)
                
                if not step_result.get("success", True):
                    break
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            build_result = {
                "pipeline": name,
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
                "success": all(r.get("success", True) for r in results),
                "steps": results
            }
            
            self.build_history.append(build_result)
            return build_result
            
        except Exception as e:
            return {
                "pipeline": name,
                "success": False,
                "error": str(e)
            }
    
    def get_build_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取构建历史"""
        return self.build_history[-limit:]
```

### 2. 测试策略实现

```python
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import time
import unittest
import asyncio
import statistics

@dataclass
class TestResult:
    """测试结果"""
    name: str
    status: str  # "passed", "failed", "error"
    duration: float
    message: str = ""
    details: Dict[str, Any] = None

class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.tests: Dict[str, Callable] = {}
        self.results: List[TestResult] = []
    
    def add_test(self, name: str, test_func: Callable) -> None:
        """添加测试"""
        self.tests[name] = test_func
    
    def run_tests(self) -> List[TestResult]:
        """运行所有测试"""
        self.results = []
        
        for name, test_func in self.tests.items():
            start_time = time.time()
            
            try:
                test_func()
                duration = time.time() - start_time
                result = TestResult(name, "passed", duration)
            except AssertionError as e:
                duration = time.time() - start_time
                result = TestResult(name, "failed", duration, str(e))
            except Exception as e:
                duration = time.time() - start_time
                result = TestResult(name, "error", duration, str(e))
            
            self.results.append(result)
        
        return self.results
    
    def get_summary(self) -> Dict[str, Any]:
        """获取测试摘要"""
        total = len(self.results)
        passed = len([r for r in self.results if r.status == "passed"])
        failed = len([r for r in self.results if r.status == "failed"])
        errors = len([r for r in self.results if r.status == "error"])
        
        durations = [r.duration for r in self.results]
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "success_rate": passed / total if total > 0 else 0,
            "average_duration": statistics.mean(durations) if durations else 0,
            "total_duration": sum(durations)
        }

class PerformanceTester:
    """性能测试器"""
    
    def __init__(self):
        self.test_scenarios: Dict[str, Callable] = {}
    
    def add_scenario(self, name: str, scenario: Callable) -> None:
        """添加测试场景"""
        self.test_scenarios[name] = scenario
    
    def run_performance_test(self, scenario_name: str, iterations: int = 100) -> Dict[str, Any]:
        """运行性能测试"""
        if scenario_name not in self.test_scenarios:
            return {"error": f"Scenario {scenario_name} not found"}
        
        scenario = self.test_scenarios[scenario_name]
        durations = []
        
        for i in range(iterations):
            start_time = time.time()
            scenario()
            duration = time.time() - start_time
            durations.append(duration)
        
        return {
            "scenario": scenario_name,
            "iterations": iterations,
            "min_duration": min(durations),
            "max_duration": max(durations),
            "average_duration": statistics.mean(durations),
            "median_duration": statistics.median(durations),
            "std_deviation": statistics.stdev(durations) if len(durations) > 1 else 0
        }
    
    def run_load_test(self, scenario_name: str, concurrent_users: int, duration: int) -> Dict[str, Any]:
        """运行负载测试"""
        if scenario_name not in self.test_scenarios:
            return {"error": f"Scenario {scenario_name} not found"}
        
        scenario = self.test_scenarios[scenario_name]
        results = []
        
        async def user_simulation():
            start_time = time.time()
            while time.time() - start_time < duration:
                try:
                    scenario_start = time.time()
                    scenario()
                    scenario_duration = time.time() - scenario_start
                    results.append(scenario_duration)
                except Exception as e:
                    results.append({"error": str(e)})
                await asyncio.sleep(0.1)
        
        # 创建并发用户
        tasks = [user_simulation() for _ in range(concurrent_users)]
        asyncio.run(asyncio.gather(*tasks))
        
        successful_requests = [r for r in results if isinstance(r, (int, float))]
        failed_requests = len(results) - len(successful_requests)
        
        return {
            "scenario": scenario_name,
            "concurrent_users": concurrent_users,
            "duration": duration,
            "total_requests": len(results),
            "successful_requests": len(successful_requests),
            "failed_requests": failed_requests,
            "requests_per_second": len(successful_requests) / duration,
            "average_response_time": statistics.mean(successful_requests) if successful_requests else 0
        }

class MockDatabase:
    """模拟数据库"""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
    
    def insert(self, table: str, data: Dict[str, Any]) -> str:
        """插入数据"""
        if table not in self.data:
            self.data[table] = []
        
        record_id = str(len(self.data[table]) + 1)
        record = {"id": record_id, **data}
        self.data[table].append(record)
        return record_id
    
    def select(self, table: str, conditions: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """查询数据"""
        if table not in self.data:
            return []
        
        results = self.data[table]
        
        if conditions:
            filtered_results = []
            for record in results:
                if all(record.get(k) == v for k, v in conditions.items()):
                    filtered_results.append(record)
            return filtered_results
        
        return results
    
    def update(self, table: str, record_id: str, data: Dict[str, Any]) -> bool:
        """更新数据"""
        if table not in self.data:
            return False
        
        for record in self.data[table]:
            if record["id"] == record_id:
                record.update(data)
                return True
        
        return False
    
    def delete(self, table: str, record_id: str) -> bool:
        """删除数据"""
        if table not in self.data:
            return False
        
        self.data[table] = [r for r in self.data[table] if r["id"] != record_id]
        return True
```

### 3. 部署运维实现

```python
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import docker
import psutil
import time
import json

@dataclass
class DeploymentConfig:
    """部署配置"""
    name: str
    image: str
    ports: Dict[str, str]
    environment: Dict[str, str]
    volumes: List[str]
    replicas: int = 1

class ContainerManager:
    """容器管理器"""
    
    def __init__(self):
        self.client = docker.from_env()
        self.containers: Dict[str, Any] = {}
    
    def deploy_service(self, config: DeploymentConfig) -> Dict[str, Any]:
        """部署服务"""
        try:
            containers = []
            
            for i in range(config.replicas):
                container = self.client.containers.run(
                    config.image,
                    name=f"{config.name}-{i}",
                    ports=config.ports,
                    environment=config.environment,
                    volumes=config.volumes,
                    detach=True
                )
                containers.append(container)
                self.containers[container.id] = container
            
            return {
                "success": True,
                "service_name": config.name,
                "containers": [c.id for c in containers]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def stop_service(self, service_name: str) -> bool:
        """停止服务"""
        try:
            for container in self.client.containers.list():
                if container.name.startswith(service_name):
                    container.stop()
                    container.remove()
            return True
        except Exception:
            return False
    
    def get_service_status(self, service_name: str) -> Dict[str, Any]:
        """获取服务状态"""
        containers = []
        
        for container in self.client.containers.list():
            if container.name.startswith(service_name):
                containers.append({
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "ports": container.ports
                })
        
        return {
            "service_name": service_name,
            "containers": containers,
            "total_containers": len(containers)
        }

class SystemMonitor:
    """系统监控器"""
    
    def __init__(self):
        self.metrics_history: List[Dict[str, Any]] = []
    
    def collect_metrics(self) -> Dict[str, Any]:
        """收集系统指标"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            "timestamp": time.time(),
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_used": memory.used,
            "memory_total": memory.total,
            "disk_percent": disk.percent,
            "disk_used": disk.used,
            "disk_total": disk.total
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_metrics_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取指标历史"""
        return self.metrics_history[-limit:]
    
    def check_alerts(self, thresholds: Dict[str, float]) -> List[str]:
        """检查告警"""
        if not self.metrics_history:
            return []
        
        current_metrics = self.metrics_history[-1]
        alerts = []
        
        if current_metrics["cpu_percent"] > thresholds.get("cpu", 80):
            alerts.append(f"CPU usage high: {current_metrics['cpu_percent']}%")
        
        if current_metrics["memory_percent"] > thresholds.get("memory", 80):
            alerts.append(f"Memory usage high: {current_metrics['memory_percent']}%")
        
        if current_metrics["disk_percent"] > thresholds.get("disk", 80):
            alerts.append(f"Disk usage high: {current_metrics['disk_percent']}%")
        
        return alerts

class LogAnalyzer:
    """日志分析器"""
    
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
    
    def add_log(self, level: str, message: str, source: str = "application") -> None:
        """添加日志"""
        log_entry = {
            "timestamp": time.time(),
            "level": level,
            "message": message,
            "source": source
        }
        self.logs.append(log_entry)
    
    def get_logs_by_level(self, level: str) -> List[Dict[str, Any]]:
        """按级别获取日志"""
        return [log for log in self.logs if log["level"] == level]
    
    def get_logs_by_source(self, source: str) -> List[Dict[str, Any]]:
        """按来源获取日志"""
        return [log for log in self.logs if log["source"] == source]
    
    def analyze_errors(self) -> Dict[str, Any]:
        """分析错误"""
        error_logs = self.get_logs_by_level("ERROR")
        
        error_counts = {}
        for log in error_logs:
            error_type = log["message"].split(":")[0] if ":" in log["message"] else "Unknown"
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return {
            "total_errors": len(error_logs),
            "error_types": error_counts,
            "recent_errors": error_logs[-10:] if error_logs else []
        }
```

### 4. 性能优化实现

```python
from typing import Dict, List, Any, Optional, Callable
import time
import cProfile
import pstats
import io
import functools

class PerformanceProfiler:
    """性能分析器"""
    
    def __init__(self):
        self.profiles: Dict[str, pstats.Stats] = {}
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """分析函数性能"""
        profiler = cProfile.Profile()
        profiler.enable()
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        profiler.disable()
        
        # 获取统计信息
        stats_stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        
        return {
            "function": func.__name__,
            "result": result,
            "execution_time": end_time - start_time,
            "profile_stats": stats_stream.getvalue()
        }
    
    def profile_decorator(self, func: Callable) -> Callable:
        """性能分析装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.profile_function(func, *args, **kwargs)
        return wrapper

class CacheOptimizer:
    """缓存优化器"""
    
    def __init__(self):
        self.caches: Dict[str, Dict[str, Any]] = {}
    
    def create_cache(self, name: str, max_size: int = 1000) -> None:
        """创建缓存"""
        self.caches[name] = {
            "data": {},
            "max_size": max_size,
            "hits": 0,
            "misses": 0
        }
    
    def get(self, cache_name: str, key: str) -> Optional[Any]:
        """获取缓存"""
        if cache_name not in self.caches:
            return None
        
        cache = self.caches[cache_name]
        
        if key in cache["data"]:
            cache["hits"] += 1
            return cache["data"][key]
        else:
            cache["misses"] += 1
            return None
    
    def set(self, cache_name: str, key: str, value: Any) -> None:
        """设置缓存"""
        if cache_name not in self.caches:
            return
        
        cache = self.caches[cache_name]
        
        # 如果缓存满了，删除最旧的项
        if len(cache["data"]) >= cache["max_size"]:
            oldest_key = next(iter(cache["data"]))
            del cache["data"][oldest_key]
        
        cache["data"][key] = value
    
    def get_cache_stats(self, cache_name: str) -> Dict[str, Any]:
        """获取缓存统计"""
        if cache_name not in self.caches:
            return {}
        
        cache = self.caches[cache_name]
        total_requests = cache["hits"] + cache["misses"]
        
        return {
            "name": cache_name,
            "size": len(cache["data"]),
            "max_size": cache["max_size"],
            "hits": cache["hits"],
            "misses": cache["misses"],
            "hit_rate": cache["hits"] / total_requests if total_requests > 0 else 0
        }

class DatabaseOptimizer:
    """数据库优化器"""
    
    def __init__(self, db_connection: Any):
        self.db = db_connection
        self.query_stats: List[Dict[str, Any]] = []
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """分析查询"""
        start_time = time.time()
        
        # 模拟查询执行
        result = self._execute_query(query)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 分析查询复杂度
        complexity = self._analyze_query_complexity(query)
        
        stats = {
            "query": query,
            "execution_time": execution_time,
            "complexity": complexity,
            "timestamp": time.time()
        }
        
        self.query_stats.append(stats)
        return stats
    
    def _execute_query(self, query: str) -> Any:
        """执行查询"""
        # 模拟查询执行
        time.sleep(0.01)  # 模拟查询时间
        return {"result": "data"}
    
    def _analyze_query_complexity(self, query: str) -> str:
        """分析查询复杂度"""
        query_lower = query.lower()
        
        if "select *" in query_lower:
            return "HIGH"  # 全表扫描
        elif "join" in query_lower:
            return "MEDIUM"  # 连接查询
        elif "where" in query_lower:
            return "LOW"  # 条件查询
        else:
            return "UNKNOWN"
    
    def get_slow_queries(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """获取慢查询"""
        return [stats for stats in self.query_stats if stats["execution_time"] > threshold]
    
    def get_query_recommendations(self) -> List[str]:
        """获取查询优化建议"""
        recommendations = []
        
        for stats in self.query_stats:
            if stats["complexity"] == "HIGH":
                recommendations.append(f"Query '{stats['query']}' uses SELECT *, consider specifying columns")
            elif stats["execution_time"] > 0.5:
                recommendations.append(f"Query '{stats['query']}' is slow, consider adding indexes")
        
        return recommendations

class MemoryOptimizer:
    """内存优化器"""
    
    def __init__(self):
        self.memory_usage: List[Dict[str, Any]] = []
    
    def track_memory_usage(self, label: str) -> Dict[str, Any]:
        """跟踪内存使用"""
        import gc
        gc.collect()  # 强制垃圾回收
        
        memory = psutil.virtual_memory()
        process = psutil.Process()
        
        usage = {
            "label": label,
            "timestamp": time.time(),
            "process_memory": process.memory_info().rss,
            "system_memory": memory.percent,
            "available_memory": memory.available
        }
        
        self.memory_usage.append(usage)
        return usage
    
    def get_memory_trend(self) -> Dict[str, Any]:
        """获取内存使用趋势"""
        if len(self.memory_usage) < 2:
            return {}
        
        recent_usage = self.memory_usage[-10:]
        process_memory_trend = [u["process_memory"] for u in recent_usage]
        
        return {
            "current_process_memory": process_memory_trend[-1],
            "average_process_memory": sum(process_memory_trend) / len(process_memory_trend),
            "memory_growth": process_memory_trend[-1] - process_memory_trend[0],
            "trend": "increasing" if process_memory_trend[-1] > process_memory_trend[0] else "decreasing"
        }
    
    def detect_memory_leaks(self) -> List[str]:
        """检测内存泄漏"""
        if len(self.memory_usage) < 10:
            return []
        
        warnings = []
        recent_usage = self.memory_usage[-10:]
        
        # 检查内存持续增长
        process_memory_values = [u["process_memory"] for u in recent_usage]
        if all(process_memory_values[i] <= process_memory_values[i+1] for i in range(len(process_memory_values)-1)):
            warnings.append("Potential memory leak detected: continuous memory growth")
        
        # 检查内存使用过高
        if process_memory_values[-1] > 100 * 1024 * 1024:  # 100MB
            warnings.append("High memory usage detected")
        
        return warnings
```

## 应用示例

```python
def demonstrate_practical_applications():
    """演示实践应用"""
    
    # 1. 开发实践
    print("=== 开发实践 ===")
    
    # 代码质量检查
    checker = CodeQualityChecker()
    
    # 创建测试文件
    test_code = '''
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

class OrderProcessor:
    def process_order(self, order):
        # 处理订单
        pass
'''
    
    with open('test_file.py', 'w') as f:
        f.write(test_code)
    
    results = checker.check_file('test_file.py')
    print("代码质量检查结果:")
    for rule, result in results.items():
        print(f"{rule}: {'通过' if result.get('passed', False) else '失败'}")
    
    # Git管理
    git_manager = GitManager('.')
    status = git_manager.get_status()
    print(f"Git状态: {status}")
    
    # 2. 测试策略
    print("\n=== 测试策略 ===")
    
    # 测试运行器
    test_runner = TestRunner()
    
    def test_addition():
        assert 2 + 2 == 4
    
    def test_multiplication():
        assert 3 * 4 == 12
    
    def test_failing_test():
        assert 1 == 2  # 这个测试会失败
    
    test_runner.add_test("test_addition", test_addition)
    test_runner.add_test("test_multiplication", test_multiplication)
    test_runner.add_test("test_failing_test", test_failing_test)
    
    results = test_runner.run_tests()
    summary = test_runner.get_summary()
    
    print(f"测试摘要: {summary}")
    
    # 性能测试
    performance_tester = PerformanceTester()
    
    def slow_function():
        time.sleep(0.01)
    
    performance_tester.add_scenario("slow_function", slow_function)
    
    perf_result = performance_tester.run_performance_test("slow_function", 10)
    print(f"性能测试结果: {perf_result}")
    
    # 3. 部署运维
    print("\n=== 部署运维 ===")
    
    # 系统监控
    monitor = SystemMonitor()
    
    for i in range(3):
        metrics = monitor.collect_metrics()
        print(f"系统指标 {i+1}: CPU={metrics['cpu_percent']}%, Memory={metrics['memory_percent']}%")
        time.sleep(1)
    
    # 检查告警
    alerts = monitor.check_alerts({"cpu": 50, "memory": 50, "disk": 50})
    if alerts:
        print(f"告警: {alerts}")
    
    # 日志分析
    log_analyzer = LogAnalyzer()
    
    log_analyzer.add_log("INFO", "Application started")
    log_analyzer.add_log("ERROR", "Database connection failed: timeout")
    log_analyzer.add_log("WARNING", "High memory usage detected")
    log_analyzer.add_log("ERROR", "Database connection failed: timeout")
    
    error_analysis = log_analyzer.analyze_errors()
    print(f"错误分析: {error_analysis}")
    
    # 4. 性能优化
    print("\n=== 性能优化 ===")
    
    # 性能分析
    profiler = PerformanceProfiler()
    
    @profiler.profile_decorator
    def expensive_function():
        result = 0
        for i in range(10000):
            result += i
        return result
    
    prof_result = expensive_function()
    print(f"函数执行时间: {prof_result['execution_time']:.4f}秒")
    
    # 缓存优化
    cache_optimizer = CacheOptimizer()
    cache_optimizer.create_cache("user_cache", max_size=100)
    
    # 模拟缓存使用
    for i in range(10):
        cache_optimizer.set("user_cache", f"user_{i}", {"name": f"User {i}"})
    
    user_data = cache_optimizer.get("user_cache", "user_1")
    print(f"缓存数据: {user_data}")
    
    cache_stats = cache_optimizer.get_cache_stats("user_cache")
    print(f"缓存统计: {cache_stats}")
    
    # 内存优化
    memory_optimizer = MemoryOptimizer()
    
    memory_optimizer.track_memory_usage("start")
    
    # 模拟内存使用
    large_list = [i for i in range(100000)]
    memory_optimizer.track_memory_usage("after_creating_list")
    
    del large_list
    memory_optimizer.track_memory_usage("after_deleting_list")
    
    memory_trend = memory_optimizer.get_memory_trend()
    print(f"内存趋势: {memory_trend}")
    
    memory_leaks = memory_optimizer.detect_memory_leaks()
    if memory_leaks:
        print(f"内存泄漏警告: {memory_leaks}")

if __name__ == "__main__":
    demonstrate_practical_applications()
```

## 总结

实践应用层将理论知识转化为具体的工程实践：

1. **开发实践**: 代码规范、版本控制、代码审查、持续集成
2. **测试策略**: 单元测试、集成测试、性能测试、自动化测试
3. **部署运维**: 容器化部署、监控告警、故障处理
4. **性能优化**: 代码优化、缓存优化、系统优化
5. **安全实践**: 代码安全、数据安全、网络安全

这些实践为构建高质量、高性能、高可靠的软件系统提供了完整的工程指导。

---

**相关链接**:

- [06-组件算法](../06-组件算法/README.md) - 组件算法
- [08-项目进度](../08-项目进度/README.md) - 项目进度
- [00-理念基础](../00-理念基础/README.md) - 理念基础

**更新时间**: 2024年12月
**版本**: 1.0.0
