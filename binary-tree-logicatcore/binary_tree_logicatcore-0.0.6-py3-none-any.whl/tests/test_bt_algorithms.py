import pytest
from binary_tree import heapify
from binary_tree import heap_sort
from binary_tree.binary_tree import Node, BT

class TestHeapify:
    def test_max_heapify(self):
        assert [3, 2, 1] == heapify.max_heapify([1, 2, 3]), "The max-heap property is not maintained"
        assert [10, 9, 7, 8, 5, 6, 3, 1, 4, 2] == heapify.max_heapify(list(range(1, 11))), "The max-heap property is not maintained"

    def test_min_heapify(self):
        assert [1, 2, 3] == heapify.min_heapify([3, 2, 1]), "The min-heap property is not maintained"
        assert [1, 2, 4, 3, 6, 5, 8, 10, 7, 9] == heapify.min_heapify(list(reversed(range(1, 11)))), "The min-heap property is not maintained"

class TestWraps:
    def test_max_heapify_wrap(self):
        random_heap = BT([1, 2, 3])
        random_heap.max_heapify()
        assert [3, 2, 1] == random_heap.elements, "The order of elements after max-heapify operation is not as expected"

        random_heap = BT(list(range(1, 11)))
        random_heap.max_heapify()
        assert [10, 9, 7, 8, 5, 6, 3, 1, 4, 2] == random_heap.elements, "The order of elements after max-heapify operation is not as expected"


    def test_min_heapify_wrap(self):
        random_heap = BT([3, 2, 1])
        random_heap.min_heapify()
        assert [1, 2, 3] == random_heap.elements, "The order of elements after min-heapify operation is not as expected"

        random_heap = BT(list(reversed(range(1, 11))))
        random_heap.min_heapify()
        assert [1, 2, 4, 3, 6, 5, 8, 10, 7, 9] == random_heap.elements, "The order of elements after min-heapify operation is not as expected"

class TestHeapSorts:

    def test_max_heap_sort(self):
        assert [1, 2, 3, 4, 7, 8, 9, 10, 14, 16] == heap_sort.heap_sort_asc([1,14,4,3,16,8,7,2,10,9]), "The order of elements after performing ascending heap sort do not match"

    def test_min_heap_sort(self):
        assert [16, 14, 10, 9, 8, 7, 4, 3, 2, 1] == heap_sort.heap_sort_desc([1,14,4,3,16,8,7,2,10,9]), "The order of elements after performing descending heap sort do not match"

    def test_max_heap_sort_wrap(self):
        x = BT([1,14,4,3,16,8,7,2,10,9])
        assert [1, 2, 3, 4, 7, 8, 9, 10, 14, 16] == x.heap_sort(), "The order of elements comprising the tree after ascending heap sort do not match"

    def test_min_heap_sort_wrap(self):
        x = BT([1,14,4,3,16,8,7,2,10,9])
        assert [16, 14, 10, 9, 8, 7, 4, 3, 2, 1] == x.heap_sort(order='descending'), "The order of elements comprising the tree after descending heap sort do not match"