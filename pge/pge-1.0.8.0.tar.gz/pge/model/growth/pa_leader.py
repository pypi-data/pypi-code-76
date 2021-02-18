import networkx as nx
import numpy as np
import pandas as pd

from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.mse import boot_estimate
from pge.model.growth.pa_com_leader import PAСomDiGrowth
from pge.ranks.rank import estimate_rank


class PAFixComDiGrowth(PAСomDiGrowth):
    def __init__(self, graph, schema, deg, model_param):
        super().__init__(graph, schema, deg, model_param)

    def prep(self, graph):
        estimate_rank(graph, "one", pers=None)

        self.cur_alps = []
        for com in set(graph.get_attributes("part")):
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
