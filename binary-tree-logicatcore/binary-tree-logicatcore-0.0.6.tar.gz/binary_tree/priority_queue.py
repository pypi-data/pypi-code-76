from binary_tree.binary_tree import BT, Node
from binary_tree import heapify
import math

class MaxPQueue(BT):
    def __init__(self, keys, values) -> None:
        super().__init__(keys)
        self.objects = values
        self.max_heapify()

    def swap(self, i1: int, i2: int) -> None:
        """
        Swaps the keys and values at two positions specified
        :param i1: Index 1
        :param i2: Index 2
        :return: None
        """
        self.objects[i1], self.objects[i2] = self.objects[i2], self.objects[i1]
        self.elements[i1], self.elements[i2] = self.elements[i2], self.elements[i1]

    def max(self) -> object:
        """
        Returns the object with the highest priority
        :return: object
        """
        return self.objects[0]

    def get_max(self) -> object:
        """
        Removes and returns the max object from the priority queue
        :return:
        """
        if len(self.elements) < 1:
            raise UnboundLocalError("Heap underflow")
        else:
            m = self.objects.pop(0)
            self.elements.pop(0)
            if len(self.elements) > 0:
                self.max_heapify()
            return m

    def max_heapify(self) -> None:
        """
        This is wrap to the general max_heapify algorithm
        :return: None
        """
        self.root, self.objects = heapify.max_heapify(self.elements, self.objects)

    def increase_key(self, obj, new_key: [int, float]) -> None:
        """
        Update the key of an object/event/task in the queue
        :return: None
        """
        parent = lambda x: math.floor(math.log2(x))

        i = self.objects.index(obj)
        if new_key < self.elements[i]:
            raise ValueError('New key is smaller than the current key')
        else:
            self.elements[i] = new_key
            while i > 0 and self.elements[parent(i)] < self.elements[i]:
                self.swap(i, parent(i))
                i = parent(i)

    def heap_insert(self, obj, key: [int, float]):
        """
        Insert a new object with a corresponding key into the queue
        :param obj: The object/event/task
        :param key: The relevant priority value i.e. key corresponding to the object
        :return: None
        """
        self.elements.append(-1000)
        self.objects.append(obj)
        self.increase_key(obj, key)

class MinPQueue(BT):
    def __init__(self, keys, values) -> None:
        super().__init__(keys)
        self.objects = values
        self.min_heapify()

    def swap(self, i1: int, i2: int) -> None:
        """
        Swaps the keys and values at two positions specified
        :param i1: Index 1
        :param i2: Index 2
        :return: None
        """
        self.objects[i1], self.objects[i2] = self.objects[i2], self.objects[i1]
        self.elements[i1], self.elements[i2] = self.elements[i2], self.elements[i1]

    def min(self) -> object:
        """
        Returns the object with the highest priority
        :return: object
        """
        return self.objects[0]

    def get_min(self) -> object:
        """
        Removes and returns the max object from the priority queue
        :return:
        """
        if len(self.elements) < 1:
            raise UnboundLocalError("Heap underflow")
        else:
            m = self.objects.pop(0)
            self.elements.pop(0)
            if len(self.elements) > 0:
                self.min_heapify()
            return m

    def min_heapify(self) -> None:
        """
        This is wrap to the general max_heapify algorithm
        :return: None
        """
        self.root, self.objects = heapify.min_heapify(self.elements, self.objects)

    def decrease_key(self, obj, new_key: [int, float]) -> None:
        """
        Update the key of an object/event/task in the queue
        :return: None
        """
        parent = lambda x: math.floor(math.log2(x))

        i = self.objects.index(obj)
        if new_key > self.elements[i]:
            raise ValueError('New key is bigger than the current key')
        else:
            self.elements[i] = new_key
            while i > 0 and self.elements[parent(i)] > self.elements[i]:
                self.swap(i, parent(i))
                i = parent(i)

    def heap_insert(self, obj, key: [int, float]):
        """
        Insert a new object with a corresponding key into the queue
        :param obj: The object/event/task
        :param key: The relevant priority value i.e. key corresponding to the object
        :return: None
        """
        self.elements.append(1000)
        self.objects.append(obj)
        self.decrease_key(obj, key)

