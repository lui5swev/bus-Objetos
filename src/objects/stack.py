EMPTY_STRUCTURE = "EMPTY_STRUCTURE"

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class DynamicStack:
    def __init__(self):
        self.top = None

    def push(self, value):
        """RF10: Push value."""
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        """RF11: Pop value."""
        if self.is_empty():
            return EMPTY_STRUCTURE
        value = self.top.value
        self.top = self.top.next
        return value

    def peek(self):
        """RF12: Peek value."""
        if self.is_empty():
            return EMPTY_STRUCTURE
        return self.top.value

    def is_empty(self):
        """RF13: Check if empty."""
        return self.top is None
