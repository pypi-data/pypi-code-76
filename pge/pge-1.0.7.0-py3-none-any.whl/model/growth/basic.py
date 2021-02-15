import numpy as np
import networkx as nx


class BasicGrowth:
    def __init__(self, graph, schema, deg, model_param):
        self.gr = graph
        self.deg = deg
        self.schema = schema
        self.param = model_param

    def choice(self, gr, sz):
        return []

    def new_edge_add(self, gr, attrs):
        return

    def new_node_add(self, graph, to, tp, attrs):
        return

    def proceed(self, n, save, attr="cnt"):
        nw_graph = self.gr.clean_copy()
        for node in nw_graph.get_ids():
            nw_graph.set_attr(node, attr, 0)

        for edge in nw_graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr, 0)

        count = self.gr.size()
        for _ in np.arange(n):
            new_node = np.random.choice(len(self.schema), p=self.schema)
            if new_node == 1:
                self.new_edge_add(new_node, (attr, _))
            else:
                self.new_node_add(nw_graph, str(count), new_node, (attr, _))
                count += 1
        nx.write_graphml(nw_graph.get_nx_graph(), save + ".graphml")


class BDiGrowth(BasicGrowth):
    def new_node_add(self, graph, to, tp, attrs):
        if tp == 0:
            if self.deg[0][0] == "const":
                nodes = self.choice(graph, self.deg[0][1], tp="in")
            else:
                nodes = self.choice(graph, self.deg[0][0](self.deg[0][1]), tp="in")

            for node in nodes:
                graph.add_edge(to, node)
                graph.set_edge_data(to, node, attrs[0], attrs[1] + 1)
        else:
            if self.deg[1][0] == "const":
                nodes = self.choice(graph, self.deg[1][1], tp="out")
            else:
                nodes = self.choice(graph, self.deg[1][0](self.deg[1][1]), tp="out")

            for node in nodes:
                graph.add_edge(node, to)
                graph.set_edge_data(node, to, attrs[0], attrs[1] + 1)
        graph.set_attr(to, attrs[0], attrs[1] + 1)

    def new_edge_add(self, gr, attrs):
        node1, node2 = self.choice(gr, 1, tp="out"), self.choice(gr, 1, tp="in")
        gr.add_edge(node1, node2)
        gr.set_edge_data(node1, node2, attrs[0], attrs[1] + 1)

    def choice(self, gr, sz, tp="in"):
        return []


class BUnGrowth(BasicGrowth):
    def new_node_add(self, graph, to, tp, attrs):
        if self.deg[0] == "const":
            nodes = self.choice(graph, self.deg[1])
        else:
            nodes = self.choice(graph, self.deg[0](self.deg[1]))

        for node in nodes:
            graph.add_edge(to, node)
            graph.set_edge_data(to, node, attrs[0], attrs[1] + 1)
        graph.set_attr(to, attrs[0], attrs[1] + 1)

    def new_edge_add(self, gr, attrs):
        nodes = self.choice(gr, 2)
        gr.add_edge(nodes[0], nodes[1])
        gr.set_edge_data(nodes[0], nodes[1], attrs[0], attrs[1] + 1)
