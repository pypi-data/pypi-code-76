import numpy as np

from pge.ranks.rank import estimate_rank


def pgr(graph, c, nodes, params):
    other = graph.get_attr(nodes[0], params[0])
    if graph.directed():
        t = graph.count_out_degree(nodes[0])
    else:
        t = graph.count_degree(nodes[0])
    t = np.where(t == 0, 0.00000001, t)
    ns = c * params[1] / t
    return np.multiply(other, ns*np.ones(other.size))/graph.get_attr(nodes[1], params[0])


def bpgr(graph, c, nodes, params):
    t = graph.count_out_degree(nodes[1])
    if t == 0:
        return np.array([])
    other = 1/graph.get_attr(nodes[0], params[0])
    return other*c*params[1]*graph.get_attr(nodes[1], params[0])/t


def wpgr(graph, c, nodes, params):
    other = graph.get_attr(nodes[0], params[0])
    t = np.multiply(graph.count_out_degree(nodes[0], w=params[0]+"w"), [graph.get_edge_data(i, nodes[1], params[0]+"w") for i in nodes[0]])

    t = np.where(t == 0, 0.00000001, t)
    ns = np.multiply(c * params[1] / t, [graph.get_edge_data(i, nodes[1], params[0]+"w") for i in nodes[0]])
    ns = np.where(ns == 0, 100000000, ns)
    return other, ns


def sumr(graph, c, nodes, params):
    other = np.array([graph.get_edge_data(i, nodes[1], params[0]) for i in nodes[0]])
    return other, np.ones(other.size)*params[1]/graph.get_attr(nodes[1], params[0])


def full(graph, c, nodes, params):
    res = []
    for node in nodes[0]:
        dels = graph.copy()
        dels.del_node(node)

        estimate_rank(dels, tp=params[0], c=c)

        ori = graph.get_attr(nodes[2], params[0])
        nw = graph.get_attr(nodes[2], params[0])
        res.append((ori-nw)/ori)

    return np.array(res), np.ones(len(res))
