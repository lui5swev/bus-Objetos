OUT_OF_BOUNDS = "OUT_OF_BOUNDS"

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        """RF05: Insert value at the end."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def get(self, position):
        """RF06: Get value by position."""
        if position < 0 or position >= self.size:
            return OUT_OF_BOUNDS
        
        current = self.head
        for _ in range(position):
            current = current.next
        return current.value

    def remove(self, position):
        """RF07: Remove value by position."""
        if position < 0 or position >= self.size:
            return OUT_OF_BOUNDS
        
        current = self.head
        for _ in range(position):
            current = current.next
            
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

    def get_size(self):
        """RF08: Get size."""
        return self.size

    def contains(self, value):
        """RF09: Search value."""
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False
