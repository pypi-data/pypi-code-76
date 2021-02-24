import networkx as nx
import numpy as np
import pandas as pd

from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.mse import boot_estimate
from pge.model.growth.pa import PADiGrowth
from pge.model.growth.pa_com_leader import PAСomDiGrowth
from pge.ranks.rank import estimate_rank


class PAFixComDiGrowth(PAСomDiGrowth):
    def __init__(self, graph, schema, deg, model_param):
        super().__init__(graph, schema, deg, model_param)
        self.chosen = None

    def prep(self, graph):
        estimate_rank(graph, "one", pers=None)

        self.cur_alps = []
        sets = list(set(graph.get_attributes("prt")))
        for com in sets:
            ones = graph.get_attributes("one", graph.get_nodes_with("part", com))
            self.cur_alps.append(
                            boot_estimate(
                                         HillEstimator,
                                         ones,
                                         1 / 2,
                                         2 / 3,
                                         30,
                                         speed=False,
                                     )[0]
                                 )
            if self.cur_alps[-1] is None:
                self.cur_alps[-1] = np.infty
            else:
                self.cur_alps[-1] = 1 / self.cur_alps[-1]
        self.alps.append(self.cur_alps[np.argmin(self.cur_alps)])
        self.chosen = sets[np.argmin(self.cur_alps)]

        graph.set_attrs(
            "dg_in", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        graph.set_attrs(
            "dg_out", {node: graph.count_out_degree(node) for node in graph.get_ids()}
        )
        return graph

    def save(self, gr, to):
        nx.write_graphml(gr, to + ".graphml")
        prd = pd.DataFrame({"alp":self.alps})
        prd.to_csv(to+".csv")

    def new_load(self, gr):
        for node in gr.get_ids():
            gr.set_attr(node, "prt", self.gr.get_attr(node, "prt"))
        return gr

    def new_node_add(self, graph, to, tp, attrs):
        super().new_node_add(graph, to, tp, attrs)
        graph.set_attr(to, "prt", -1)

    def stop(self):
        return self.chosen == -1


class PACancerDiGrowth(PAСomDiGrowth):
    def __init__(self, graph, schema, deg, model_param):
        super().__init__(graph, schema, deg, model_param)
        self.chosen = None
        self.alps_nw = []

    def prep(self, graph):
        estimate_rank(graph, "one", pers=None)

        self.cur_alps = []
        sets = list(set(graph.get_attributes("prt")))
        for com in sets:
            ones = graph.get_attributes("one", graph.get_nodes_with("part", com))
            self.cur_alps.append(
                    boot_estimate(
                        HillEstimator,
                        ones,
                        1 / 2,
                        2 / 3,
                        30,
                        speed=False,
                    )[0]
                )
            if self.cur_alps[-1] is None:
                self.cur_alps[-1] = np.infty
            else:
                self.cur_alps[-1] = 1 / self.cur_alps[-1]
        self.alps.append(self.cur_alps[np.argmin(self.cur_alps)])
        self.chosen = sets[np.argmin(self.cur_alps)]
        self.alps_nw.append(boot_estimate(
                        HillEstimator,
                        graph.get_attributes("one", graph.get_nodes_with("nw", 1)),
                        1 / 2,
                        2 / 3,
                        30,
                        speed=False,
                    )[0])
        if self.alps_nw[-1] is None:
            self.alps_nw[-1] = np.infty
        else:
            self.alps_nw[-1] = 1 / self.alps_nw[-1]

        graph.set_attrs(
                "dg_in", {node: graph.count_in_degree(node) for node in graph.get_ids()}
            )
        graph.set_attrs(
                "dg_out", {node: graph.count_out_degree(node) for node in graph.get_ids()}
            )
        return graph

    def save(self, gr, to):
        nx.write_graphml(gr, to + ".graphml")
        prd = pd.DataFrame({"alp": self.alps, "alp_nw": self.alps_nw})
        prd.to_csv(to + ".csv")

    def new_load(self, gr):
        for node in gr.get_ids():
            gr.set_attr(node, "prt", self.gr.get_attr(node, "prt"))
            gr.set_attr(node, "nw", 0)
        return gr

    def new_node_add(self, graph, to, tp, attrs):
        super().new_node_add(graph, to, tp, attrs)
        graph.set_attr(to, "prt", self.chosen)
        graph.set_attr(to, "nw", 1)

    def stop(self):
        return False

    def new_edge_add(self, gr, attrs):
        trg = gr.get_nodes_with("nw", 1)
        if trg.size == 0:
            return

        while True:
            node1, node2 = self.choice(gr, 1, tp="out")[0], self.choice(gr, 1, tp="in")[0]
            if node1 in trg or node2 in trg:
                break
        gr.add_edge(node1, node2)
        gr.set_edge_data(node1, node2, attrs[0], attrs[1] + 1)
