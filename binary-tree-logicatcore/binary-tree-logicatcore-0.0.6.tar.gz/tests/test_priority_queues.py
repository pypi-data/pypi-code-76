import pytest
from binary_tree.priority_queue import MaxPQueue, MinPQueue

class TestMaxPQueue:
    def test_basic_functionality(self):
        max_queue = MaxPQueue([3, 1, 2], ["Hello", "!", "World"])
        for x in ["Hello", "World", "!"]:
            assert x == max_queue.get_max(), "Max Priority queue did not return the object/events/tasks in the correct order"

    def test_max(self):
        max_queue = MaxPQueue([3, 1, 2], ["Hello", "!", "World"])
        assert "Hello" == max_queue.max(), "Max Priority queue did not return the correct object/events/tasks with highest priority"

    def test_increase_key(self):
        max_queue = MaxPQueue([3, 1, 2], ["Hello", "!", "World"])
        for o, k in zip(["Hello", "World", "!"], [30, 200, 1000]):
            max_queue.increase_key(o, k)
        for x in reversed(["Hello", "World", "!"]):
            assert x == max_queue.get_max(), "Max Priority queue did not return the object/events/tasks in the correct order"

    def test_insert_key(self):
        max_queue = MaxPQueue([3, 1, 2], ["Hello", "!", "World"])
        max_queue.heap_insert(',', 2.5)
        for x in ["Hello", ",", "World", "!"]:
            assert x == max_queue.get_max(), "Max Priority queue did not return the object/events/tasks in the correct order"


class TestMinPQueue:
    def test_basic_functionality(self):
        min_queue = MinPQueue([-3, -1, -2], ["Hello", "!", "World"])
        for x in ["Hello", "World", "!"]:
            assert x == min_queue.get_min(), "Min Priority queue did not return the object/events/tasks in the correct order"

    def test_min(self):
        min_queue = MinPQueue([-3, -1, -2], ["Hello", "!", "World"])
        assert "Hello" == min_queue.min(), "Min Priority queue did not return the correct object/events/tasks with least priority"

    def test_decrease_key(self):
        min_queue = MinPQueue([-3, -1, -2], ["Hello", "!", "World"])
        for o, k in zip(["Hello", "World", "!"], [-30, -200, -1000]):
            min_queue.decrease_key(o, k)
        for x in reversed(["Hello", "World", "!"]):
            assert x == min_queue.get_min(), "Min Priority queue did not return the object/events/tasks in the correct order"

    def test_insert_key(self):
        min_queue = MinPQueue([-3, -1, -2], ["Hello", "!", "World"])
        min_queue.heap_insert(',', -2.5)
        for x in ["Hello", ",", "World", "!"]:
            assert x == min_queue.get_min(), "Min Priority queue did not return the object/events/tasks in the correct order"
