"""
Stack - 测试套件

测试覆盖率目标: 95%+
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from stack import (
    Stack,
    LinkedStack,
    DequeStack,
    GenericStack,
    ThreadSafeStack,
    BoundedStack,
    MinStack,
    is_valid_parentheses,
    eval_rpn,
    infix_to_postfix,
    BrowserHistory,
    TextEditor
)


# ============================================================================
# 基础栈测试
# ============================================================================


class TestStack:
    """基础栈测试"""
    
    def test_push_and_pop(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
        assert stack.pop() == 1
    
    def test_peek(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.peek() == 2
        assert stack.size() == 2  # peek不移除元素
    
    def test_is_empty(self):
        stack = Stack()
        assert stack.is_empty()
        stack.push(1)
        assert not stack.is_empty()
    
    def test_size(self):
        stack = Stack()
        assert stack.size() == 0
        stack.push(1)
        stack.push(2)
        assert stack.size() == 2
    
    def test_pop_empty(self):
        stack = Stack()
        with pytest.raises(IndexError):
            stack.pop()
    
    def test_peek_empty(self):
        stack = Stack()
        with pytest.raises(IndexError):
            stack.peek()


# ============================================================================
# 链表栈测试
# ============================================================================


class TestLinkedStack:
    """链表栈测试"""
    
    def test_basic_operations(self):
        stack = LinkedStack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
        assert stack.size() == 1
    
    def test_empty_operations(self):
        stack = LinkedStack()
        with pytest.raises(IndexError):
            stack.pop()


# ============================================================================
# 最小栈测试
# ============================================================================


class TestMinStack:
    """最小栈测试"""
    
    def test_get_min(self):
        stack = MinStack()
        stack.push(3)
        stack.push(1)
        stack.push(2)
        assert stack.get_min() == 1
    
    def test_get_min_after_pop(self):
        stack = MinStack()
        stack.push(3)
        stack.push(1)
        stack.push(2)
        stack.pop()
        assert stack.get_min() == 1
        stack.pop()
        assert stack.get_min() == 3


# ============================================================================
# 有界栈测试
# ============================================================================


class TestBoundedStack:
    """有界栈测试"""
    
    def test_capacity(self):
        stack = BoundedStack(3)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.is_full()
    
    def test_overflow(self):
        stack = BoundedStack(2)
        stack.push(1)
        stack.push(2)
        with pytest.raises(OverflowError):
            stack.push(3)


# ============================================================================
# 应用测试
# ============================================================================


class TestApplications:
    """实战应用测试"""
    
    def test_valid_parentheses(self):
        assert is_valid_parentheses("()")
        assert is_valid_parentheses("()[]{}")
        assert is_valid_parentheses("{[]}")
        assert not is_valid_parentheses("([)]")
        assert not is_valid_parentheses("(")
    
    def test_eval_rpn(self):
        assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
        assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    
    def test_infix_to_postfix(self):
        assert infix_to_postfix("a+b") == "ab+"
        assert infix_to_postfix("a+b*c") == "abc*+"
    
    def test_browser_history(self):
        browser = BrowserHistory("google.com")
        browser.visit("facebook.com")
        browser.visit("youtube.com")
        assert browser.back(1) == "facebook.com"
        assert browser.forward(1) == "youtube.com"
    
    def test_text_editor(self):
        editor = TextEditor()
        editor.type("Hello")
        editor.type(" World")
        assert editor.get_text() == "Hello World"
        editor.undo()
        assert editor.get_text() == "Hello"
        editor.redo()
        assert editor.get_text() == "Hello World"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

