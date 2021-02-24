import numpy as np
import networkx as nx


from pge.model.growth.basic import BasicGrowth


class FixGrowth(BasicGrowth):
    def __init__(self, graph, schema, deg, model_param, del_typ):
        super().__init__(graph, schema, deg, model_param)
        self.typ = del_typ

    def proceed(self, n, save, attr="cnt"):
        nw_graph = self.gr.clean_copy()
        for node in nw_graph.get_ids():
            nw_graph.set_attr(node, attr, 0)
            nw_graph.set_attr(node, attr + "_end", -1)

        for edge in nw_graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr, 0)
            nw_graph.set_edge_data(edge[0], edge[1], attr + "_end", -1)
        graph = self.prep(self.gr.clean_copy())

        count = self.gr.size()
        for _ in np.arange(n):
            new_node = np.random.choice(len(self.schema), p=self.schema)
            if new_node != 1:
                if self.typ == "un":
                    del_node = np.random.choice(graph.get_ids(stable=True))
                else:
                    ids = graph.get_ids(stable=True)
                    vals = graph.get_attributes(attr)
                    del_node = np.random.choice(ids[vals == np.min(vals)])
                nw_graph.set_attr(del_node, attr + "_end", _ + 1)
                for deg_node in nw_graph.get_in_degrees(del_node):
                    nw_graph.set_edge_data(deg_node, del_node, attr + "_end", _ + 1)
                graph.del_node(del_node)

                for node in self.clean(graph):
                    nw_graph.set_attr(node, attr + "_end", _ + 1)
                    for deg_node in nw_graph.get_in_degrees(node):
                        nw_graph.set_edge_data(deg_node, node, attr + "_end", _ + 1)
                    graph.del_node(node)

                self.new_node_add((graph, nw_graph), str(count), new_node, (attr, _))
                count += 1
            else:
                self.new_edge_add((graph, nw_graph), (attr, _))

        for node in graph.get_ids():
            nw_graph.set_attr(node, attr + "_end", _ + 1)
        for edge in graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr + "_end", _ + 1)
        nx.write_graphml(nw_graph.get_nx_graph(), save + ".graphml")

    def clean(self, graph):
        return graph


class FixDiGrowth(FixGrowth):
    def new_node_add(self, graph, to, tp, attrs):
        if tp == 0:
            if self.deg[0][0] == "const":
                nodes = self.choice(graph[0], self.deg[0][1], tp="in")
            else:
                nodes = self.choice(graph[0], self.deg[0][0](self.deg[0][1]), tp="in")

            for node in nodes:
                graph[0].add_edge(to, node)
                graph[1].add_edge(to, node)
                graph[1].set_edge_data(node, to, attrs[0], attrs[1] + 1)
        else:
            if self.deg[1][0] == "const":
                nodes = self.choice(graph, self.deg[1][1], tp="out")
            else:
                nodes = self.choice(graph, self.deg[1][0](self.deg[1][1]), tp="out")

            for node in nodes:
                graph[0].add_edge(to, node)
                graph[1].add_edge(to, node)
                graph[1].set_edge_data(node, to, attrs[0], attrs[1] + 1)
        graph[1].set_attr(to, attrs[0], attrs[1] + 1)

    def new_edge_add(self, gr, attrs):
        node1, node2 = self.choice(gr[0], 1, tp="out"), self.choice(gr[0], 1, tp="in")
        gr[0].add_edge(node1, node2)
        gr[1].add_edge(node1, node2)
        gr[1].set_edge_data(node1, node2, attrs[0], attrs[1] + 1)

    def choice(self, gr, sz, tp="in"):
        return []


class FixUnGrowth(FixGrowth):
    def new_node_add(self, graph, to, tp, attrs):
        if self.deg[0] == "const":
            nodes = self.choice(graph[0], self.deg[1])
        else:
            nodes = self.choice(graph[0], self.deg[0](self.deg[1]))

        for node in nodes:
            graph[0].add_edge(to, node)
            graph[1].add_edge(to, node)
            graph[1].set_edge_data(to, node, attrs[0], attrs[1] + 1)
        graph[1].set_attr(to, attrs[0], attrs[1] + 1)

    def new_edge_add(self, gr, attrs):
        nodes = self.choice(gr[0], 2)
        gr[0].add_edge(nodes[0], nodes[1])
        gr[1].add_edge(nodes[0], nodes[1])
        gr[1].set_edge_data(nodes[0], nodes[1], attrs[0], attrs[1] + 1)
