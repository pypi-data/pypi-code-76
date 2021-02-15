import networkx as nx
import numpy as np

from pge.model.growth.basic import BUnGrowth
from pge.model.growth.basic_fix import FixUnGrowth


class CAGrowth(BUnGrowth):
    def choice(self, graph, sz):
        cs = {
            k: v ** self.param[0] + self.param[1]
            for k, v in nx.clustering(graph.get_nx_graph()).items()
            if v is not np.NaN
        }
        probs = list(cs.values())
        probs = probs / np.sum(probs)
        return np.random.choice(list(cs.keys()), sz, replace=False, p=probs)


class CAFixGrowth(FixUnGrowth):
    def prep(self, graph):
        rs = nx.clustering(graph.get_nx_graph())
        graph.set_attrs("clust", {k: 0 if v is np.NaN else v for k, v in rs.items()})
        return graph

    def choice(self, graph, sz):
        nodes = graph.get_ids(stable=True)
        probs = graph.get_attributes("clust") ** self.param[0] + self.param[1]

        nodes, probs = nodes[probs > 0], probs[probs > 0]
        if probs.size == 0:
            return None
        probs = probs / np.sum(probs)
        return np.random.choice(nodes, sz, replace=False, p=probs)

    def clean(self, graph):
        graph = self.prep(graph)
        if self.param[1] == 0:
            return []

        dels = graph.get_ids(stable=True)[(graph.get_attributes("clust") == 0)]
        return dels
