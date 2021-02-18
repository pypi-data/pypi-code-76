import numpy as np
import networkx as nx
from itertools import combinations, product


def graph_coherence(graph, nodes):
    L = nx.laplacian_matrix(graph.get_nx_graph()).toarray()
    Q = np.delete(np.delete(L, nodes, axis=0), nodes, axis=1)
    return np.trace(Q)/2


def min_error(graph, k):
    combs = list(combinations(np.arange(graph.size()), k))
    HS = [graph_coherence(graph, comb) for comb in combs]

    res = np.argmin(HS)
    return [list(graph.get_ids())[node] for node in combs[res]]


def kswap(graph, nodes):
    T = np.array(graph.get_ids())
    T = list(T[~np.isin(T, nodes)])

    decreased = True
    while decreased:
        prev = graph_coherence(graph, nodes)
        brk = True
        for i, j in product(nodes, T):
            cp = nodes.copy()
            cp.remove(i)
            if prev > graph_coherence(graph, cp+[j]):
                nodes = cp+[j]
                T.remove(j)
                T.append(i)
                brk = False
                break
        if brk:
            decreased = False

    return nodes


def kgreedy(graph, k):
    res = []
    prev = None

    nodes = list(graph.get_ids())
    while len(res) < k:
        er = [graph_coherence(graph, res+[node]) for node in nodes]
        if prev is None or prev > np.min(er):
            ind = np.argmin(er)
            if hasattr(ind, "__iter__"):
                nd = nodes[ind[0]]
            else:
                nd = nodes[ind]
            res.append(nd)
            prev = np.min(er)
            nodes.remove(nd)
        else:
            break
    return res
