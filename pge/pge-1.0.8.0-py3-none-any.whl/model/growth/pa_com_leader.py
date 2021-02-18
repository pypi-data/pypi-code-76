import networkx as nx
import numpy as np
import pandas as pd

from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.mse import boot_estimate
from pge.cluster.directed.dir_louvain import best_partition_to
from pge.model.growth.basic import BDiGrowth
from pge.ranks.rank import estimate_rank


class PAСomDiGrowth(BDiGrowth):
    def __init__(self, graph, schema, deg, model_param):
        super().__init__(graph, schema, deg, model_param)
        self.alps = []
        self.mods = []
        self.cur_alps = []

    def choice(self, graph, sz, tp="in"):
        coms = np.unique(graph.get_attributes("com"))

        nodes = []
        for i, com in enumerate(coms):
            if self.cur_alps[i] == self.alps[-1]:
                nodes = np.append(nodes, graph.get_nodes_with("com", com))
        if tp == "in":
            probs = np.array([graph.count_in_degree(node) for node in nodes]) + self.param[0]
        else:
            probs = np.array([graph.count_in_degree(node) for node in nodes]) + self.param[1]
        probs = probs / np.sum(probs)
        return np.random.choice(nodes, sz, replace=False, p=probs)

    def prep(self, graph):
        estimate_rank(graph, "one", pers=None)
        coms = best_partition_to(graph.clean_copy())
        graph.set_attrs("com", coms[0])
        self.mods.append(coms[1])

        self.cur_alps = []
        for com in set(coms[0].values()):
            ones = graph.get_attributes("one", graph.get_nodes_with("com", com))
            self.cur_alps.append((
                                     boot_estimate(
                                         HillEstimator,
                                         ones,
                                         1 / 2,
                                         2 / 3,
                                         30,
                                         speed=False,
                                     )[0]
                                 ))
            if self.cur_alps[-1] is None:
                self.cur_alps[-1] = np.infty
            else:
                self.cur_alps[-1] = 1/self.cur_alps[-1]
        self.alps.append(self.cur_alps[np.argmin(self.cur_alps)])

        graph.set_attrs(
            "dg_in", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        graph.set_attrs(
            "dg_out", {node: graph.count_out_degree(node) for node in graph.get_ids()}
        )
        return graph

    def save(self, gr, to):
        nx.write_graphml(gr, to + ".graphml")
        prd = pd.DataFrame({"alp":self.alps, "mods":self.mods})
        prd.to_csv(to+".csv")
