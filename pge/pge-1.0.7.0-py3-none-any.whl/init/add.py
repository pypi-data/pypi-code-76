import networkx as nx


def actual(graph, sg):
    ids = graph.get_ids(stable=True)

    if sg is not None:
        # if sg > 0:
        # nx.set_node_attributes(graph.get_nx_graph(), name="tel", values={n: float(pwrlaw(sg, 1, 0, 1)) for n in ids})
        if sg == 0:
            nx.set_node_attributes(graph.get_nx_graph(), name="tel", values=1)
    nx.set_node_attributes(
        graph.get_nx_graph(),
        name="ind",
        values={n: graph.count_in_degree(n) for n in ids},
    )
    nx.set_node_attributes(
        graph.get_nx_graph(),
        name="out",
        values={n: graph.count_out_degree(n) for n in ids},
    )
