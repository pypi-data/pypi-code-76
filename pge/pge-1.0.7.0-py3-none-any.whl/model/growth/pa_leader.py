import networkx as nx
import numpy as np

from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.mse import boot_estimate
from pge.ranks.rank import estimate_rank


class PAFixComDiGrowth:
    def __init__(self, graph, schema, deg):
        self.gr = graph
        self.deg = deg
        self.schema = schema

    def proceed(self, n, save, comm, attr="cnt"):
        nw_graph = self.gr.clean_copy()
        graph = self.prep(self.gr.clean_copy())
        for node in nw_graph.get_ids():
            nw_graph.set_attr(node, attr, 0)
            nw_graph.set_attr(node, comm, self.gr.get_attr(node, comm))
            graph.set_attr(node, comm, self.gr.get_attr(node, comm))

        for edge in nw_graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr, 0)

        coms = np.unique(graph.get_attributes(comm))
        count = self.gr.size()
        for _ in np.arange(n):
            alp = []
            for comm_ in coms:
                ids = graph.get_nodes_with(comm, comm_)
                alp.append(
                    1
                    / (
                        boot_estimate(
                            HillEstimator,
                            graph.get_attributes("one", ids),
                            1 / 2,
                            2 / 3,
                            30,
                            speed=False,
                        )[0]
                    ))
            try:
                bst = coms[np.nanargmin(alp)]
            except:
                break

            best_comm = graph.get_nodes_with(comm, bst)

            new_node = np.random.choice(len(self.schema), p=self.schema)
            if new_node != 1:
                del_node = np.random.choice(best_comm)
                if self.deg[0][0] == "const":
                    nodes = self.choice(graph, [del_node], self.deg[0][1], tp="all")
                else:
                    nodes = self.choice(graph, [del_node], self.deg[0][0](self.deg[0][1]), tp="all")

                for node in nodes:
                    if self.deg[1] <= np.random.uniform(size=1):
                        graph.add_edge(str(count), node)
                        nw_graph.add_edge(str(count), node)
                        nw_graph.set_edge_data(str(count), node, attr, _ + 1)
                    else:
                        graph.add_edge(node, str(count))
                        nw_graph.add_edge(node, str(count))
                        nw_graph.set_edge_data(node, str(count), attr, _ + 1)
                nw_graph.set_attr(str(count), comm, bst)
                graph.set_attr(str(count), comm, bst)
                nw_graph.set_attr(str(count), attr, _ + 1)

                nw_graph.set_attr(del_node, attr + "_end", _ + 1)
                for deg_node in nw_graph.get_in_degrees(del_node):
                    nw_graph.set_edge_data(deg_node, del_node, attr + "_end", _ + 1)
                graph.del_node(del_node)
                for node in self.clean(graph):
                    nw_graph.set_attr(node, attr + "_end", _ + 1)
                    for deg_node in nw_graph.get_in_degrees(node):
                        nw_graph.set_edge_data(deg_node, node, attr + "_end", _ + 1)
                    graph.del_node(node)
                count += 1
            else:
                node1, node2 = self.choice(graph, best_comm, 2, tp="all")
                graph.add_edge(node1, node2)
                graph.set_edge_data(node1, node2, attr, _ + 1)
                nw_graph.add_edge(node1, node2)

        for node in graph.get_ids():
            nw_graph.set_attr(node, attr + "_end", _ + 1)
        for edge in graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr + "_end", _ + 1)
        nx.write_graphml(nw_graph.get_nx_graph(), save + ".graphml")

    def choice(self, graph, frm, sz, tp):
        if tp == "all":
            ids = frm
        elif tp == "in":
            ids = graph.get_in_degrees(frm)
        else:
            ids = graph.get_out_degrees(frm)

        probs = []
        for id in ids:
            dg = graph.get_attr(id, "dg")
            dgs = np.sum([graph.get_attr(node, "dg") for node in
                                                          np.unique(np.append(graph.get_in_degrees(id),
                                                                              graph.get_out_degrees(id)))])
            probs.append(dg/dgs)

        probs = np.array(probs)
        probs = probs / np.sum(probs)
        return [ids[np.argmax(probs)]]
        #return np.random.choice(ids, min(sz, probs.size), replace=False, p=probs)

    def prep(self, graph):
        estimate_rank(graph, "one", pers=None)
        graph.set_attrs(
            "dg", {node: graph.count_in_degree(node)+graph.count_out_degree(node) for node in graph.get_ids()}
        )
        return graph

    def clean(self, graph):
        graph = self.prep(graph)
        dels = graph.get_ids(stable=True)[graph.get_attributes("dg") == 0]
        return dels