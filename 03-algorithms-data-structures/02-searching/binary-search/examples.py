"""
Binary Search - 实战应用示例

包含6个实际应用场景：
1. 数据库索引查询
2. 版本控制系统
3. 资源分配问题
4. 时间调度系统
5. 价格区间查询
6. 日志分析系统
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from binary_search import (
    binary_search_first,
    binary_search_iterative,
    binary_search_last,
    first_bad_version,
    lower_bound,
    split_array,
    upper_bound,
)

# ============================================================================
# 示例1: 数据库索引查询系统
# ============================================================================


@dataclass
class DatabaseRecord:
    """数据库记录"""

    id: int
    name: str
    email: str
    created_at: datetime

    def __repr__(self) -> str:
        return f"Record(id={self.id}, name={self.name})"


class DatabaseIndex:
    """数据库索引 - 使用二分搜索优化查询"""

    def __init__(self, records: list[DatabaseRecord]):
        """
        Args:
            records: 数据库记录列表
        """
        # 按 ID 排序（模拟 B-Tree 索引）
        self.records = sorted(records, key=lambda x: x.id)
        self.query_count = 0

    def find_by_id(self, record_id: int) -> DatabaseRecord | None:
        """
        通过 ID 查找记录

        时间复杂度: O(log n)

        Args:
            record_id: 记录 ID

        Returns:
            找到的记录，不存在返回 None
        """
        self.query_count += 1
        left, right = 0, len(self.records) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if self.records[mid].id == record_id:
                return self.records[mid]
            elif self.records[mid].id < record_id:
                left = mid + 1
            else:
                right = mid - 1

        return None

    def find_range(self, start_id: int, end_id: int) -> list[DatabaseRecord]:
        """
        范围查询：查找 ID 在 [start_id, end_id] 范围内的所有记录

        Args:
            start_id: 起始 ID
            end_id: 结束 ID

        Returns:
            范围内的所有记录
        """
        # 使用 lower_bound 和 upper_bound
        ids = [r.id for r in self.records]
        left_idx = lower_bound(ids, start_id)
        right_idx = upper_bound(ids, end_id)

        return self.records[left_idx:right_idx]

    def count_records_before(self, record_id: int) -> int:
        """统计 ID < record_id 的记录数"""
        ids = [r.id for r in self.records]
        return lower_bound(ids, record_id)

    def get_statistics(self) -> dict[str, Any]:
        """获取统计信息"""
        return {
            "total_records": len(self.records),
            "total_queries": self.query_count,
            "avg_search_steps": "O(log n)",
            "index_type": "B-Tree (simulated)",
        }


def demo_database_index() -> None:
    """演示数据库索引查询"""
    print("\n" + "=" * 80)
    print("示例1: 数据库索引查询系统")
    print("=" * 80)

    # 创建测试数据
    records = [
        DatabaseRecord(1001, "Alice", "alice@example.com", datetime.now()),
        DatabaseRecord(1003, "Bob", "bob@example.com", datetime.now()),
        DatabaseRecord(1007, "Charlie", "charlie@example.com", datetime.now()),
        DatabaseRecord(1010, "David", "david@example.com", datetime.now()),
        DatabaseRecord(1015, "Eve", "eve@example.com", datetime.now()),
        DatabaseRecord(1020, "Frank", "frank@example.com", datetime.now()),
    ]

    db = DatabaseIndex(records)

    # 1. 精确查询
    print("\n1. 精确查询")
    record = db.find_by_id(1007)
    print(f"查找 ID=1007: {record}")

    # 2. 范围查询
    print("\n2. 范围查询")
    range_records = db.find_range(1005, 1015)
    print(f"ID 在 [1005, 1015] 范围内的记录:")
    for r in range_records:
        print(f"  {r}")

    # 3. 统计查询
    print("\n3. 统计查询")
    count = db.count_records_before(1010)
    print(f"ID < 1010 的记录数: {count}")

    # 4. 统计信息
    print("\n4. 统计信息")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")


# ============================================================================
# 示例2: 版本控制系统
# ============================================================================


class VersionStatus(Enum):
    """版本状态"""

    GOOD = "good"
    BAD = "bad"
    UNKNOWN = "unknown"


@dataclass
class Version:
    """软件版本"""

    version_number: int
    commit_hash: str
    status: VersionStatus
    timestamp: datetime


class VersionControl:
    """版本控制系统 - 二分法查找第一个坏版本"""

    def __init__(self, versions: list[Version]):
        """
        Args:
            versions: 版本列表（按版本号排序）
        """
        self.versions = sorted(versions, key=lambda x: x.version_number)

    def is_bad_version(self, version_number: int) -> bool:
        """判断版本是否是坏的"""
        for v in self.versions:
            if v.version_number == version_number:
                return v.status == VersionStatus.BAD
        return False

    def find_first_bad_version(self) -> Version | None:
        """
        查找第一个坏版本

        使用二分搜索，最小化测试次数

        Returns:
            第一个坏版本，不存在返回 None
        """
        if not self.versions:
            return None

        n = len(self.versions)
        left, right = 0, n - 1
        result = -1

        tests = 0
        while left <= right:
            mid = left + (right - left) // 2
            tests += 1

            if self.is_bad_version(self.versions[mid].version_number):
                result = mid
                right = mid - 1  # 继续向左找
            else:
                left = mid + 1

        print(f"总测试次数: {tests} (线性搜索需要 {result + 1} 次)")

        return self.versions[result] if result != -1 else None

    def find_bad_range(self) -> tuple[int, int]:
        """查找所有坏版本的范围"""
        version_numbers = [v.version_number for v in self.versions]
        bad_versions = [v.version_number for v in self.versions if v.status == VersionStatus.BAD]

        if not bad_versions:
            return (-1, -1)

        first_bad = bad_versions[0]
        last_bad = bad_versions[-1]

        first_idx = binary_search_first(version_numbers, first_bad)
        last_idx = binary_search_last(version_numbers, last_bad)

        return (first_idx, last_idx)


def demo_version_control() -> None:
    """演示版本控制系统"""
    print("\n" + "=" * 80)
    print("示例2: 版本控制系统 - 查找第一个坏版本")
    print("=" * 80)

    # 创建测试数据：版本 1-20，从版本 15 开始是坏的
    versions = []
    for i in range(1, 21):
        status = VersionStatus.BAD if i >= 15 else VersionStatus.GOOD
        versions.append(
            Version(
                version_number=i,
                commit_hash=f"abc{i:03d}",
                status=status,
                timestamp=datetime.now() - timedelta(days=20 - i),
            )
        )

    vc = VersionControl(versions)

    print(f"\n总版本数: {len(versions)}")
    print(f"状态: v1-v14 正常, v15-v20 有问题")

    # 查找第一个坏版本
    print("\n使用二分搜索查找第一个坏版本...")
    first_bad = vc.find_first_bad_version()
    if first_bad:
        print(f"第一个坏版本: v{first_bad.version_number} ({first_bad.commit_hash})")

    # 查找坏版本范围
    print("\n查找所有坏版本的范围...")
    first_idx, last_idx = vc.find_bad_range()
    print(f"坏版本索引范围: [{first_idx}, {last_idx}]")
    print(
        f"坏版本号范围: [v{versions[first_idx].version_number}, "
        f"v{versions[last_idx].version_number}]"
    )


# ============================================================================
# 示例3: 资源分配问题
# ============================================================================


@dataclass
class Task:
    """任务"""

    id: int
    workload: int  # 工作量
    priority: int


class ResourceAllocator:
    """资源分配器 - 使用二分答案"""

    def __init__(self, tasks: list[Task]):
        """
        Args:
            tasks: 任务列表
        """
        self.tasks = tasks

    def minimize_max_workload(self, num_workers: int) -> int:
        """
        最小化最大工作量

        将任务分配给 num_workers 个工人，
        使得工作量最大的工人的工作量最小

        Args:
            num_workers: 工人数量

        Returns:
            最小化后的最大工作量
        """
        workloads = [task.workload for task in self.tasks]

        return split_array(workloads, num_workers)

    def allocate_tasks(self, num_workers: int) -> list[list[Task]]:
        """
        分配任务

        Args:
            num_workers: 工人数量

        Returns:
            每个工人的任务列表
        """
        max_workload = self.minimize_max_workload(num_workers)

        allocations: list[list[Task]] = [[] for _ in range(num_workers)]
        worker_idx = 0
        current_workload = 0

        for task in self.tasks:
            if current_workload + task.workload > max_workload and worker_idx < num_workers - 1:
                worker_idx += 1
                current_workload = 0

            allocations[worker_idx].append(task)
            current_workload += task.workload

        return allocations

    def print_allocation(self, allocations: list[list[Task]]) -> None:
        """打印分配结果"""
        for i, tasks in enumerate(allocations):
            total_workload = sum(task.workload for task in tasks)
            task_ids = [task.id for task in tasks]
            print(f"工人 {i+1}: 任务 {task_ids}, 总工作量 = {total_workload}")


def demo_resource_allocation() -> None:
    """演示资源分配"""
    print("\n" + "=" * 80)
    print("示例3: 资源分配问题 - 最小化最大工作量")
    print("=" * 80)

    # 创建测试数据
    tasks = [
        Task(1, 7, 1),
        Task(2, 2, 2),
        Task(3, 5, 1),
        Task(4, 10, 3),
        Task(5, 8, 2),
    ]

    allocator = ResourceAllocator(tasks)

    print(f"\n任务列表:")
    for task in tasks:
        print(f"  Task {task.id}: workload={task.workload}")

    # 分配给2个工人
    num_workers = 2
    print(f"\n分配给 {num_workers} 个工人:")

    max_workload = allocator.minimize_max_workload(num_workers)
    print(f"最小化后的最大工作量: {max_workload}")

    allocations = allocator.allocate_tasks(num_workers)
    allocator.print_allocation(allocations)


# ============================================================================
# 示例4: 时间调度系统
# ============================================================================


@dataclass
class FlowerBed:
    """花圃"""

    id: int
    bloom_day: int  # 开花日期
    location: int


class FlowerScheduler:
    """花卉调度系统 - 二分答案"""

    def __init__(self, flower_beds: list[FlowerBed]):
        """
        Args:
            flower_beds: 花圃列表
        """
        self.flower_beds = flower_beds

    def min_days_to_make_bouquets(self, num_bouquets: int, flowers_per_bouquet: int) -> int:
        """
        制作花束的最少天数

        需要制作 num_bouquets 束花，每束需要 flowers_per_bouquet 朵相邻的花

        Args:
            num_bouquets: 需要的花束数量
            flowers_per_bouquet: 每束花的花朵数量

        Returns:
            最少等待天数，不可能返回 -1
        """
        bloom_days = [bed.bloom_day for bed in self.flower_beds]

        if num_bouquets * flowers_per_bouquet > len(bloom_days):
            return -1

        def can_make(days: int) -> bool:
            """判断在 days 天内能否制作 num_bouquets 束花"""
            bouquets = 0
            flowers = 0

            for day in bloom_days:
                if day <= days:
                    flowers += 1
                    if flowers == flowers_per_bouquet:
                        bouquets += 1
                        flowers = 0
                else:
                    flowers = 0

            return bouquets >= num_bouquets

        left = min(bloom_days)
        right = max(bloom_days)

        while left < right:
            mid = left + (right - left) // 2

            if can_make(mid):
                right = mid
            else:
                left = mid + 1

        return left


def demo_flower_scheduler() -> None:
    """演示花卉调度"""
    print("\n" + "=" * 80)
    print("示例4: 时间调度系统 - 花束制作")
    print("=" * 80)

    # 创建测试数据
    flower_beds = [
        FlowerBed(1, 1, 0),
        FlowerBed(2, 10, 1),
        FlowerBed(3, 3, 2),
        FlowerBed(4, 10, 3),
        FlowerBed(5, 2, 4),
    ]

    scheduler = FlowerScheduler(flower_beds)

    print("\n花圃开花时间:")
    for bed in flower_beds:
        print(f"  花圃 {bed.id}: 第 {bed.bloom_day} 天开花 (位置 {bed.location})")

    # 需要制作3束花，每束1朵（相邻）
    num_bouquets = 3
    flowers_per_bouquet = 1

    print(f"\n需求: {num_bouquets} 束花，每束 {flowers_per_bouquet} 朵")

    min_days = scheduler.min_days_to_make_bouquets(num_bouquets, flowers_per_bouquet)

    if min_days == -1:
        print("无法满足需求！")
    else:
        print(f"最少等待天数: {min_days}")


# ============================================================================
# 示例5: 价格区间查询系统
# ============================================================================


@dataclass
class Product:
    """商品"""

    id: int
    name: str
    price: float
    category: str


class PriceQuerySystem:
    """价格查询系统 - 范围查询"""

    def __init__(self, products: list[Product]):
        """
        Args:
            products: 商品列表
        """
        # 按价格排序
        self.products = sorted(products, key=lambda x: x.price)

    def find_in_price_range(self, min_price: float, max_price: float) -> list[Product]:
        """
        查找价格在指定范围内的商品

        Args:
            min_price: 最低价格
            max_price: 最高价格

        Returns:
            价格在范围内的商品列表
        """
        prices = [p.price for p in self.products]

        # 使用 lower_bound 和 upper_bound
        left_idx = lower_bound(prices, min_price)
        right_idx = upper_bound(prices, max_price)

        return self.products[left_idx:right_idx]

    def count_in_range(self, min_price: float, max_price: float) -> int:
        """统计价格范围内的商品数量"""
        return len(self.find_in_price_range(min_price, max_price))

    def find_closest_price(self, target_price: float) -> Product | None:
        """查找价格最接近目标价格的商品"""
        if not self.products:
            return None

        prices = [p.price for p in self.products]
        left, right = 0, len(prices) - 1

        while left < right:
            mid = left + (right - left) // 2

            if prices[mid] < target_price:
                left = mid + 1
            else:
                right = mid

        # left 指向 >= target_price 的位置
        if left == 0:
            return self.products[0]
        if left == len(prices):
            return self.products[-1]

        # 比较 left 和 left-1
        if abs(prices[left] - target_price) < abs(prices[left - 1] - target_price):
            return self.products[left]
        return self.products[left - 1]


def demo_price_query() -> None:
    """演示价格查询系统"""
    print("\n" + "=" * 80)
    print("示例5: 价格区间查询系统")
    print("=" * 80)

    # 创建测试数据
    products = [
        Product(1, "Laptop", 999.99, "Electronics"),
        Product(2, "Mouse", 29.99, "Electronics"),
        Product(3, "Keyboard", 79.99, "Electronics"),
        Product(4, "Monitor", 299.99, "Electronics"),
        Product(5, "Headphones", 199.99, "Electronics"),
        Product(6, "Webcam", 89.99, "Electronics"),
    ]

    pqs = PriceQuerySystem(products)

    print("\n商品列表（按价格排序）:")
    for product in pqs.products:
        print(f"  {product.name}: ${product.price}")

    # 1. 范围查询
    print("\n1. 价格范围查询")
    min_price, max_price = 50.0, 200.0
    products_in_range = pqs.find_in_price_range(min_price, max_price)
    print(f"价格在 [${min_price}, ${max_price}] 范围内的商品:")
    for product in products_in_range:
        print(f"  {product.name}: ${product.price}")

    # 2. 统计查询
    print("\n2. 统计查询")
    count = pqs.count_in_range(min_price, max_price)
    print(f"价格在 [${min_price}, ${max_price}] 范围内的商品数量: {count}")

    # 3. 查找最接近的价格
    print("\n3. 查找最接近的价格")
    target_price = 150.0
    closest = pqs.find_closest_price(target_price)
    if closest:
        print(f"最接近 ${target_price} 的商品: {closest.name} (${closest.price})")


# ============================================================================
# 示例6: 日志分析系统
# ============================================================================


@dataclass
class LogEntry:
    """日志条目"""

    timestamp: datetime
    level: str
    message: str


class LogAnalyzer:
    """日志分析系统 - 时间范围查询"""

    def __init__(self, logs: list[LogEntry]):
        """
        Args:
            logs: 日志列表（按时间排序）
        """
        self.logs = sorted(logs, key=lambda x: x.timestamp)

    def find_logs_in_time_range(
        self, start_time: datetime, end_time: datetime
    ) -> list[LogEntry]:
        """
        查找时间范围内的日志

        Args:
            start_time: 开始时间
            end_time: 结束时间

        Returns:
            时间范围内的日志列表
        """
        left = self._find_first_after(start_time)
        right = self._find_last_before(end_time)

        if left == -1 or right == -1 or left > right:
            return []

        return self.logs[left : right + 1]

    def _find_first_after(self, target_time: datetime) -> int:
        """查找第一个 >= target_time 的日志索引"""
        left, right = 0, len(self.logs) - 1
        result = -1

        while left <= right:
            mid = left + (right - left) // 2

            if self.logs[mid].timestamp >= target_time:
                result = mid
                right = mid - 1
            else:
                left = mid + 1

        return result

    def _find_last_before(self, target_time: datetime) -> int:
        """查找最后一个 <= target_time 的日志索引"""
        left, right = 0, len(self.logs) - 1
        result = -1

        while left <= right:
            mid = left + (right - left) // 2

            if self.logs[mid].timestamp <= target_time:
                result = mid
                left = mid + 1
            else:
                right = mid - 1

        return result

    def count_errors_in_range(self, start_time: datetime, end_time: datetime) -> int:
        """统计时间范围内的错误日志数量"""
        logs = self.find_logs_in_time_range(start_time, end_time)
        return sum(1 for log in logs if log.level == "ERROR")


def demo_log_analyzer() -> None:
    """演示日志分析系统"""
    print("\n" + "=" * 80)
    print("示例6: 日志分析系统 - 时间范围查询")
    print("=" * 80)

    # 创建测试数据
    base_time = datetime(2025, 10, 26, 10, 0, 0)
    logs = [
        LogEntry(base_time, "INFO", "Application started"),
        LogEntry(base_time + timedelta(minutes=1), "INFO", "User logged in"),
        LogEntry(base_time + timedelta(minutes=2), "WARNING", "High memory usage"),
        LogEntry(base_time + timedelta(minutes=3), "ERROR", "Database connection failed"),
        LogEntry(base_time + timedelta(minutes=4), "INFO", "Retrying connection"),
        LogEntry(base_time + timedelta(minutes=5), "INFO", "Connection restored"),
        LogEntry(base_time + timedelta(minutes=6), "ERROR", "File not found"),
    ]

    analyzer = LogAnalyzer(logs)

    print(f"\n总日志数: {len(logs)}")

    # 1. 时间范围查询
    print("\n1. 时间范围查询")
    start_time = base_time + timedelta(minutes=2)
    end_time = base_time + timedelta(minutes=5)
    logs_in_range = analyzer.find_logs_in_time_range(start_time, end_time)

    print(f"时间范围: {start_time.strftime('%H:%M:%S')} - {end_time.strftime('%H:%M:%S')}")
    print(f"找到 {len(logs_in_range)} 条日志:")
    for log in logs_in_range:
        print(f"  [{log.timestamp.strftime('%H:%M:%S')}] {log.level}: {log.message}")

    # 2. 错误统计
    print("\n2. 错误统计")
    error_count = analyzer.count_errors_in_range(start_time, end_time)
    print(f"时间范围内的错误日志数: {error_count}")


# ============================================================================
# 主函数
# ============================================================================


def main() -> None:
    """运行所有示例"""

    print("\n" + "=" * 80)
    print("Binary Search - 实战应用示例")
    print("=" * 80)

    # 运行所有示例
    demo_database_index()
    demo_version_control()
    demo_resource_allocation()
    demo_flower_scheduler()
    demo_price_query()
    demo_log_analyzer()

    print("\n" + "=" * 80)
    print("所有示例运行完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()

