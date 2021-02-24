import networkx as nx
import numpy as np


def information_centrality(graph):
    return nx.information_centrality(graph.get_nx_graph())


def closeness_centrality(graph):
    return nx.closeness_centrality(graph.get_nx_graph())


def closeness2_centrality(graph):
    graph = graph.get_nx_graph()
    path_length = nx.single_source_shortest_path_length
    nodes = graph.nodes

    closeness_centrality2 = {}
    for n in nodes:
        sp = path_length(graph, n)
        totsp = np.sum(np.power(list(sp.values()), 2))/(len(sp) - 1.0)
        closeness_centrality2[n] = totsp
    return closeness_centrality2
