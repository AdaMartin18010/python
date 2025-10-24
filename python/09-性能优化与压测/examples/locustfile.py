"""
Locust压测脚本示例
用于压测Web API的负载测试

运行方式:
    # 安装
    uv add locust
    
    # Web界面模式
    locust -f locustfile.py --host=http://localhost:8000
    # 访问 http://localhost:8089
    
    # 命令行模式（无界面）
    locust -f locustfile.py --host=http://localhost:8000 \
           --users=100 --spawn-rate=10 --run-time=5m --headless
    
    # 分布式压测（主节点）
    locust -f locustfile.py --master
    
    # 分布式压测（工作节点）
    locust -f locustfile.py --worker --master-host=localhost
"""

from locust import HttpUser, task, between, events
from locust.exception import RescheduleTask
import random
import json
import time
from typing import Optional

# ============ 配置 ============

# 用户凭证（用于认证）
USERS = [
    {"username": "admin", "password": "Admin123!@#"},
    {"username": "testuser", "password": "Test123!@#"},
]

# 测试数据
SAMPLE_DOCUMENTS = [
    {"title": "Document 1", "content": "Content for document 1", "is_public": False},
    {"title": "Document 2", "content": "Content for document 2", "is_public": True},
    {"title": "Document 3", "content": "Content for document 3", "is_public": False},
]

# ============ 基础用户类 ============

class AuthenticatedUser(HttpUser):
    """已认证用户基类"""
    
    abstract = True
    wait_time = between(1, 3)  # 请求间隔1-3秒
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token: Optional[str] = None
        self.user_credentials: Optional[dict] = None
    
    def on_start(self):
        """用户启动时执行：登录"""
        # 随机选择一个用户
        self.user_credentials = random.choice(USERS)
        self.login()
    
    def login(self):
        """登录获取令牌"""
        response = self.client.post(
            "/token",
            data={
                "username": self.user_credentials["username"],
                "password": self.user_credentials["password"]
            },
            name="POST /token (login)"
        )
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            print(f"✓ Logged in as {self.user_credentials['username']}")
        else:
            print(f"✗ Login failed: {response.status_code}")
            raise RescheduleTask()
    
    @property
    def auth_headers(self) -> dict:
        """认证头"""
        return {"Authorization": f"Bearer {self.token}"}


# ============ 测试场景 ============

class APIUser(AuthenticatedUser):
    """API用户：执行各种API操作"""
    
    @task(10)  # 权重10：最常见的操作
    def view_documents(self):
        """查看文档列表"""
        self.client.get(
            "/documents",
            headers=self.auth_headers,
            name="GET /documents"
        )
    
    @task(5)  # 权重5
    def view_own_profile(self):
        """查看自己的资料"""
        self.client.get(
            "/users/me",
            headers=self.auth_headers,
            name="GET /users/me"
        )
    
    @task(3)  # 权重3
    def create_document(self):
        """创建文档"""
        document = random.choice(SAMPLE_DOCUMENTS)
        response = self.client.post(
            "/documents",
            headers=self.auth_headers,
            json=document,
            name="POST /documents"
        )
        
        if response.status_code == 200:
            doc_id = response.json().get("id")
            # 存储文档ID供后续删除使用
            if not hasattr(self, "document_ids"):
                self.document_ids = []
            self.document_ids.append(doc_id)
    
    @task(1)  # 权重1：较少的操作
    def delete_document(self):
        """删除文档"""
        if hasattr(self, "document_ids") and self.document_ids:
            doc_id = self.document_ids.pop()
            self.client.delete(
                f"/documents/{doc_id}",
                headers=self.auth_headers,
                name="DELETE /documents/{id}"
            )


class ReadOnlyUser(AuthenticatedUser):
    """只读用户：只查看不修改"""
    
    @task(20)
    def view_documents(self):
        """查看文档列表"""
        self.client.get(
            "/documents",
            headers=self.auth_headers,
            name="GET /documents (readonly)"
        )
    
    @task(10)
    def view_profile(self):
        """查看资料"""
        self.client.get(
            "/users/me",
            headers=self.auth_headers,
            name="GET /users/me (readonly)"
        )
    
    @task(5)
    def check_health(self):
        """健康检查"""
        self.client.get("/health", name="GET /health")


class HeavyUser(AuthenticatedUser):
    """重度用户：大量创建操作"""
    
    @task(15)
    def create_multiple_documents(self):
        """批量创建文档"""
        for i in range(3):
            document = random.choice(SAMPLE_DOCUMENTS)
            document["title"] = f"{document['title']} - {i}"
            self.client.post(
                "/documents",
                headers=self.auth_headers,
                json=document,
                name="POST /documents (heavy)"
            )
            time.sleep(0.1)  # 稍微延迟
    
    @task(5)
    def view_documents(self):
        """查看文档"""
        self.client.get(
            "/documents",
            headers=self.auth_headers,
            name="GET /documents (heavy)"
        )


class StressTestUser(HttpUser):
    """压力测试用户：专门用于压力测试"""
    
    wait_time = between(0.1, 0.5)  # 更短的等待时间
    
    @task
    def stress_endpoint(self):
        """压力测试端点"""
        endpoints = [
            "/health",
            "/",
            "/docs",
        ]
        endpoint = random.choice(endpoints)
        self.client.get(endpoint, name=f"STRESS {endpoint}")


# ============ 事件钩子 ============

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """测试开始时执行"""
    print("\n" + "="*50)
    print("🚀 Load Test Started")
    print("="*50 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """测试结束时执行"""
    print("\n" + "="*50)
    print("✓ Load Test Completed")
    print("="*50)
    
    # 打印统计信息
    stats = environment.stats
    print(f"\n📊 Summary Statistics:")
    print(f"  Total Requests: {stats.total.num_requests}")
    print(f"  Total Failures: {stats.total.num_failures}")
    print(f"  Average Response Time: {stats.total.avg_response_time:.2f}ms")
    print(f"  Min Response Time: {stats.total.min_response_time:.2f}ms")
    print(f"  Max Response Time: {stats.total.max_response_time:.2f}ms")
    print(f"  Requests per Second: {stats.total.total_rps:.2f}")
    print(f"  Failure Rate: {stats.total.fail_ratio*100:.2f}%\n")


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """每个请求后执行（可选）"""
    # 记录慢请求
    if response_time > 1000:  # 超过1秒
        print(f"⚠️  Slow request: {name} took {response_time:.0f}ms")
    
    # 记录错误
    if exception:
        print(f"❌ Error in {name}: {exception}")


# ============ 自定义形状 ============

from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    """
    阶梯式负载：逐步增加用户数
    
    阶段1: 0-60s, 10 users
    阶段2: 60-120s, 50 users
    阶段3: 120-180s, 100 users
    阶段4: 180-240s, 200 users
    """
    
    step_time = 60
    step_load = 10
    spawn_rate = 10
    time_limit = 240
    
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time > self.time_limit:
            return None
        
        current_step = run_time // self.step_time
        user_count = (current_step + 1) * self.step_load
        
        return (user_count, self.spawn_rate)


# ============ 使用说明 ============

"""
压测场景说明:

1. APIUser (默认): 常规API操作，包括读写
2. ReadOnlyUser: 只读操作，适合测试读取性能
3. HeavyUser: 重度操作，测试系统承载能力
4. StressTestUser: 压力测试，短等待时间

运行示例:

# 混合场景（默认会运行所有User类）
locust -f locustfile.py --host=http://localhost:8000

# 只运行特定场景
locust -f locustfile.py --host=http://localhost:8000 --tags readonly

# 使用自定义负载形状
# 取消注释 StepLoadShape 类，Locust会自动检测并使用

# 生成HTML报告
locust -f locustfile.py --host=http://localhost:8000 \
       --users=100 --spawn-rate=10 --run-time=5m \
       --headless --html=report.html

# 性能基准测试（无界面，输出CSV）
locust -f locustfile.py --host=http://localhost:8000 \
       --users=100 --spawn-rate=10 --run-time=10m \
       --headless --csv=benchmark

压测最佳实践:

1. 从小负载开始（10-50用户）
2. 逐步增加负载观察系统表现
3. 记录关键指标：P50、P95、P99延迟
4. 监控系统资源：CPU、内存、网络
5. 测试不同场景：读多写少、写多读少、混合
6. 使用分布式压测模拟更大负载
"""

