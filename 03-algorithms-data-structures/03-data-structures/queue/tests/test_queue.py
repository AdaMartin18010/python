"""Queue - 测试套件"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from queue import Queue, CircularQueue, PriorityQueue, Deque, bfs, max_sliding_window


class TestQueue:
    """基础队列测试"""
    
    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        assert q.dequeue() == 2
    
    def test_front(self):
        q = Queue()
        q.enqueue(1)
        assert q.front() == 1
        assert q.size() == 1
    
    def test_is_empty(self):
        q = Queue()
        assert q.is_empty()
        q.enqueue(1)
        assert not q.is_empty()
    
    def test_dequeue_empty(self):
        q = Queue()
        with pytest.raises(IndexError):
            q.dequeue()


class TestCircularQueue:
    """循环队列测试"""
    
    def test_circular_behavior(self):
        cq = CircularQueue(3)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.enqueue(3)
        assert cq.is_full()
        
        assert cq.dequeue() == 1
        cq.enqueue(4)
        assert cq.front() == 2
    
    def test_overflow(self):
        cq = CircularQueue(2)
        cq.enqueue(1)
        cq.enqueue(2)
        with pytest.raises(OverflowError):
            cq.enqueue(3)


class TestPriorityQueue:
    """优先级队列测试"""
    
    def test_priority_order(self):
        pq = PriorityQueue()
        pq.enqueue("Low", 3)
        pq.enqueue("High", 1)
        pq.enqueue("Medium", 2)
        
        assert pq.dequeue() == "High"
        assert pq.dequeue() == "Medium"
        assert pq.dequeue() == "Low"


class TestApplications:
    """应用测试"""
    
    def test_bfs(self):
        graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
        result = bfs(graph, 'A')
        assert result == ['A', 'B', 'C', 'D']
    
    def test_max_sliding_window(self):
        nums = [1, 3, -1, -3, 5, 3, 6, 7]
        result = max_sliding_window(nums, 3)
        assert result == [3, 3, 5, 5, 6, 7]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

