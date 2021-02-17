def max_heapify(A, O = None):
    """
    This method is used to maintain max-heap property in the binary tree data structure. Also used for max priority
    queues
    :param A: Elements of the binary tree as a list
    :param O: List of objects/events/tasks required for priority queues
    :return: Array satisfying the max-heap property
    """
    left = lambda x: (x << 1) + 1
    right = lambda x: (x << 1) + 2
    # parent = lambda x: math.floor(math.log2(x))

    def recurse(A, i, O = None):
        l, r = left(i), right(i)
        if l < len(A) and A[l] > A[i]:
            largest = l
        else:
            largest = i
        if r < len(A) and A[r] > A[largest]:
            largest = r
        if largest != i:
            A[i], A[largest] = A[largest], A[i]
            if O is not None:
                O[i], O[largest] = O[largest], O[i]
            recurse(A, largest, O)

    for index in reversed(range(len(A))):
        recurse(A, index, O)
    if O is not None:
        return A, O
    else:
        return A

def min_heapify(A, O = None):
    """
    This method is used to maintain min-heap property in the binary tree data structure. Also used for min priority
    queues
    :param A: Elements of the binary tree as a list
    :param O: List of objects/events/tasks required for priority queues
    :return: Array satisfying the min-heap property
    """
    left = lambda x: (x << 1) + 1
    right = lambda x: (x << 1) + 2
    # parent = lambda x: math.floor(math.log2(x))

    def recurse(A, i, O = None):
        l, r = left(i), right(i)
        if l < len(A) and A[l] < A[i]:
            smallest = l
        else:
            smallest = i
        if r < len(A) and A[r] < A[smallest]:
            smallest = r
        if smallest != i:
            A[i], A[smallest] = A[smallest], A[i]
            if O is not None:
                O[i], O[smallest] = O[smallest], O[i]
            recurse(A, smallest, O)

    for index in reversed(range(len(A))):
        recurse(A, index, O)
    if O is not None:
        return A, O
    else:
        return A
