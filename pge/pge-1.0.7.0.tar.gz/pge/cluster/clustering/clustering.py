import networkx as nx


def clustering(gr):
    return nx.clustering(gr.get_nx_graph())
