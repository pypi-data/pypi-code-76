import itertools

import networkx as nx
import numpy as np


def all_cycles_undirected(graph):
    basic_cycles = nx.minimum_cycle_basis(graph.get_nx_graph())

    cycles = []
    for bas in basic_cycles:
        cycles.append(bas)

    for i in np.arange(2, len(basic_cycles) + 1):
        for sums_cycles in itertools.combinations(basic_cycles, i):
            G_sub = nx.Graph()

            for cycle in sums_cycles:
                ln = len(cycle)
                for j in np.arange(ln)[::-1]:
                    if G_sub.has_edge(cycle[j], cycle[j - 1]):
                        G_sub[cycle[j]][cycle[j - 1]].update(
                            {"count": G_sub[cycle[j]][cycle[j - 1]]["count"] + 1}
                        )
                    else:
                        G_sub.add_edge(cycle[i], cycle[i - 1], count=1)

            if nx.is_connected(G_sub):
                dls = [dt for dt in G_sub.edges.data() if dt[2]["count"] > 1]
                if len(dls) > 0:
                    for dl in dls:
                        G_sub.remove_edge(dl[0], dl[1])

                    add_cycles = nx.minimum_cycle_basis(G_sub)
                    if len(add_cycles) > 1:
                        continue

                    cycles.append(add_cycles[0])

    return cycles
