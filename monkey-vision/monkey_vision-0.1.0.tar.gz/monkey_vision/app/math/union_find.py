"""
Disjoint Set Union (Union Find)
"""


# union find equipped with "path compression"
def find(data, i):
    root = i
    # Find the root of the dataset
    while root != data[root]:
        root = data[root]

    # Compress the path leading back to the root.
    # this operation is called "path compression"
    while i != root:
        next = data[i]
        data[i] = root
        i = next

    return root


def union(data, i, j):
    if connected(data, i, j):
        return
    pi, pj = find(data, i), find(data, j)
    if pi != pj:
        data[pi] = pj


def connected(data, i, j):
    return find(data, i) == find(data, j)
