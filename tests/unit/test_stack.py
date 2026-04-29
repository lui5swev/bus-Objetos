import pytest
from src.objects.stack import DynamicStack, EMPTY_STRUCTURE

class TestDynamicStack:
    def setup_method(self):
        self.stack = DynamicStack()

    def test_tc_stack_01_push_and_peek(self):
        """RF10, RF12: Push value and Peek value."""
        self.stack.push("A")
        assert self.stack.peek() == "A"
        self.stack.push("B")
        assert self.stack.peek() == "B"

    def test_tc_stack_02_pop(self):
        """RF11: Pop value."""
        self.stack.push("A")
        self.stack.push("B")
        assert self.stack.pop() == "B"
        assert self.stack.pop() == "A"

    def test_tc_stack_03_pop_empty(self):
        """RF11: Pop empty stack."""
        assert self.stack.pop() == EMPTY_STRUCTURE

    def test_tc_stack_04_peek_empty(self):
        """RF12: Peek empty stack."""
        assert self.stack.peek() == EMPTY_STRUCTURE

    def test_tc_stack_05_is_empty(self):
        """RF13: Check if empty."""
        assert self.stack.is_empty() is True
        self.stack.push("A")
        assert self.stack.is_empty() is False
        self.stack.pop()
        assert self.stack.is_empty() is True
