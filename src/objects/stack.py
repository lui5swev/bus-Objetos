from typing import Any, Optional
import threading

EMPTY_STRUCTURE = "EMPTY_STRUCTURE"

class Node:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: Optional['Node'] = None

class DynamicStack:
    def __init__(self) -> None:
        self.top: Optional[Node] = None
        self.lock = threading.Lock()

    def push(self, value: Any) -> None:
        """RF10: Push value."""
        if value is None:
            raise ValueError("El valor no puede ser None")

        new_node = Node(value)
        with self.lock:
            new_node.next = self.top
            self.top = new_node

    def pop(self) -> Any:
        """RF11: Pop value."""
        with self.lock:
            if self.is_empty_unlocked():
                return EMPTY_STRUCTURE
            if self.top is None:
                return EMPTY_STRUCTURE
            value = self.top.value
            self.top = self.top.next
            return value

    def peek(self) -> Any:
        """RF12: Peek value."""
        with self.lock:
            if self.is_empty_unlocked():
                return EMPTY_STRUCTURE
            if self.top is None:
                return EMPTY_STRUCTURE
            return self.top.value

    def is_empty(self) -> bool:
        """RF13: Check if empty."""
        with self.lock:
            return self.is_empty_unlocked()
            
    def is_empty_unlocked(self) -> bool:
        """Internal lock-free check for empty state"""
        return self.top is None
