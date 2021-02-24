import numpy as np
import networkx as nx

from pge.init.classes.graph import SGraph


class CustomCreator:
    @staticmethod
    def partitioned_grow(types, prt):
        graph = nx.Graph()
        count = 0
        for tp in types:
            nw_graph = tp[0](*tp[1])
            nw_graph.set_attrs("prt", count)
            graph = nx.union(graph, nw_graph.get_nx_graph(), rename=(None, tp[2]))
            count += 1

        graph = SGraph(graph)
        nodes = graph.get_ids(stable=True)
        dg = np.array(
            [
                np.random.choice(
                    max(int(prt * graph.count_out_degree(node)), 1) + 1, 1
                )[0]
                for node in nodes
            ]
        )
        if np.sum(dg) % 2 != 0:
            dg[0] += 1
        prts = graph.get_attributes("prt")

        for i in np.arange(nodes.size):
            if dg[i] == 0:
                continue

            indx = np.arange(nodes.size)[(prts != prts[i]) & (dg > 0)]
            if indx.size == 0:
                continue
            adds = np.random.choice(indx, dg[i])

            for add in adds:
                if dg[add] > 0:
                    graph.add_edge(nodes[i], nodes[add])
                    dg[add] -= 1
            dg[i] = 0
        return graph

    @staticmethod
    def partitioned_di_grow(types, prt):
        graph = nx.DiGraph()
        count = 0
        for tp in types:
            nw_graph = tp[0](*tp[1])
            nw_graph.set_attrs("prt", count)
            graph = nx.union(graph, nw_graph.get_nx_graph(), rename=(None, tp[2]))
            count += 1

        graph = SGraph(graph)
        nodes = graph.get_ids(stable=True)
        dg_out = [int(prt * graph.count_out_degree(node)) + 1 for node in nodes]
        dg_out = np.array([np.random.choice(i, 1, p=(np.arange(i)+1)[::-1]/(np.sum(np.arange(i)+1)))[0] for i in dg_out])
        dg_in = [int(prt * graph.count_in_degree(node)) + 1 for node in nodes]
        dg_in = np.array([np.random.choice(i, 1, p=(np.arange(i) + 1)[::-1] / (np.sum(np.arange(i) + 1)))[0] for i in dg_in])
        print(np.sum(dg_in), np.sum(dg_out))

        prts = graph.get_attributes("prt")
        id_ns = np.arange(nodes.size)
        np.random.shuffle(id_ns)
        for i in id_ns:
            if dg_in[i] != 0:
                indx = np.arange(nodes.size)[(prts != prts[i]) & (dg_out > 0)]
                if indx.size == 0:
                    continue

                adds = np.random.choice(indx, dg_in[i])

                for add in adds:
                    if dg_out[add] > 0:
                        graph.add_edge(nodes[i], nodes[add])
                        dg_out[add] -= 1
                dg_in[i] = 0

        return graph