from typing import Any, Optional
import threading

OUT_OF_BOUNDS = "OUT_OF_BOUNDS"


class Node:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size: int = 0
        self.lock = threading.Lock()

    def append(self, value: Any) -> None:
        """RF05: Insert value at the end."""
        if value is None:
            raise ValueError("El valor no puede ser None")

        new_node = Node(value)
        with self.lock:
            if self.head is None:
                self.head = new_node
                self.tail = new_node
            else:
                if self.tail is not None:
                    self.tail.next = new_node
                    new_node.prev = self.tail
                    self.tail = new_node
            self.size += 1

    def get(self, position: int) -> Any:
        """RF06: Get value by position."""
        with self.lock:
            if position < 0 or position >= self.size:
                return OUT_OF_BOUNDS

            current = self.head
            for _ in range(position):
                if current:
                    current = current.next
            return current.value if current else OUT_OF_BOUNDS

    def remove(self, position: int) -> Any:
        """RF07: Remove value by position."""
        with self.lock:
            if position < 0 or position >= self.size:
                return OUT_OF_BOUNDS

            current = self.head
            for _ in range(position):
                if current:
                    current = current.next

            if current is None:
                return OUT_OF_BOUNDS

            if current.prev:
                current.prev.next = current.next
            else:
                self.head = current.next

            if current.next:
                current.next.prev = current.prev
            else:
                self.tail = current.prev

            self.size -= 1
            return current.value

    def get_size(self) -> int:
        """RF08: Get size."""
        with self.lock:
            return self.size

    def contains(self, value: Any) -> bool:
        """RF09: Search value."""
        with self.lock:
            current = self.head
            while current:
                if current.value == value:
                    return True
                current = current.next
            return False
