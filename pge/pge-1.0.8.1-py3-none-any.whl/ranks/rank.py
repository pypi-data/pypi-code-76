import networkx as nx


def estimate_rank(graph, tp, pers=None, c=0.85, max_iter=100, eps=0.000001, w=None):
    if pers is None:
        tel = {node: 1/graph.size() for node in graph.get_ids()}
    else:
        tel = graph.get_attrs_dict(pers)
    res = nx.pagerank(graph.get_nx_graph(), alpha=c, personalization=tel,
                      max_iter=max_iter, tol=eps, weight=w)
    res = {i: res.get(i)*graph.size() for i in res}
    graph.set_attrs(tp, res)


def esp(graph, tp, frm, per="tel", c=0.85, w=None):
    nodes = graph.get_ids()
    graph.set_attrs(tp, 0)

    for node in nodes:
        rank = (1 - c) * graph.get_attr(node, per)
        k = graph.get_in_degrees(node, w=w)

        for n in k:
            t = graph.count_out_degree(n)
            if t != 0:
                t = c * graph.get_attr(n, frm) / t

            if tp == "max":
                rank = max(rank, t)
            else:
                rank = min(rank, t)
        graph.set_attr(node, tp, rank)
