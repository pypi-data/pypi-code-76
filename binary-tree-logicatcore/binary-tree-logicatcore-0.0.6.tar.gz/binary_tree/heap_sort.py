from binary_tree import heapify

def heap_sort_asc(A):
    """
    Performs an ascending heap sort using min-heapify to order elements in ascending
    :param A: List of elements of the tree
    :return: Sorted list of elements
    """
    sorted = []
    tmp = heapify.min_heapify(A)
    sorted.append(A[0])
    while len(tmp) > 2:
        tmp = heapify.min_heapify(tmp[1:])
        sorted.append(tmp[0])
    sorted.append(tmp[1])

    return sorted

def heap_sort_desc(A):
    """
    Performs an descending heap sort using max-heapify to order elements in descending
    :param A: List of elements of the tree
    :return: Sorted list of elements
    """
    sorted = []
    tmp = heapify.max_heapify(A)
    sorted.append(A[0])
    while len(tmp) > 2:
        tmp = heapify.max_heapify(tmp[1:])
        sorted.append(tmp[0])
    sorted.append(tmp[1])

    return sorted