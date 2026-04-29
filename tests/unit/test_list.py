import pytest
from src.objects.list import DoublyLinkedList, OUT_OF_BOUNDS

class TestDoublyLinkedList:
    def setup_method(self):
        self.dll = DoublyLinkedList()

    def test_tc_list_01_append(self):
        """RF05: Insert value at the end."""
        self.dll.append("Data1")
        assert self.dll.get_size() == 1
        self.dll.append("Data2")
        assert self.dll.get_size() == 2

    def test_tc_list_02_get_valid(self):
        """RF06: Get value by position."""
        self.dll.append("A")
        self.dll.append("B")
        self.dll.append("C")
        assert self.dll.get(0) == "A"
        assert self.dll.get(1) == "B"
        assert self.dll.get(2) == "C"

    def test_tc_list_03_get_out_of_bounds(self):
        """RF06: Get value by position - Out of bounds."""
        assert self.dll.get(0) == OUT_OF_BOUNDS
        self.dll.append("A")
        assert self.dll.get(1) == OUT_OF_BOUNDS
        assert self.dll.get(-1) == OUT_OF_BOUNDS

    def test_tc_list_04_remove_valid(self):
        """RF07: Remove value by position."""
        self.dll.append("A")
        self.dll.append("B")
        self.dll.append("C")
        
        # Remove middle
        removed = self.dll.remove(1)
        assert removed == "B"
        assert self.dll.get_size() == 2
        assert self.dll.get(1) == "C"
        
        # Remove head
        removed = self.dll.remove(0)
        assert removed == "A"
        assert self.dll.get_size() == 1
        assert self.dll.get(0) == "C"

        # Remove tail
        removed = self.dll.remove(0)
        assert removed == "C"
        assert self.dll.get_size() == 0

    def test_tc_list_05_remove_out_of_bounds(self):
        """RF07: Remove value by position - Out of bounds."""
        assert self.dll.remove(0) == OUT_OF_BOUNDS
        self.dll.append("A")
        assert self.dll.remove(1) == OUT_OF_BOUNDS
        assert self.dll.remove(-1) == OUT_OF_BOUNDS

    def test_tc_list_06_get_size(self):
        """RF08: Get size."""
        assert self.dll.get_size() == 0
        self.dll.append("A")
        assert self.dll.get_size() == 1

    def test_tc_list_07_contains(self):
        """RF09: Search value."""
        self.dll.append("A")
        self.dll.append("B")
        assert self.dll.contains("A") is True
        assert self.dll.contains("B") is True
        assert self.dll.contains("C") is False
