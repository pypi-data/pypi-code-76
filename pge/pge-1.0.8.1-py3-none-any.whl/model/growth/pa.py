import numpy as np


from pge.model.growth.basic import BUnGrowth, BDiGrowth
from pge.model.growth.basic_fix import FixUnGrowth, FixDiGrowth


class PAGrowth(BUnGrowth):
    def choice(self, graph, sz):
        probs = np.array([graph.count_in_degree(node) for node in graph.get_ids()]) + self.param
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(), sz, replace=False, p=probs)


class PADiGrowth(BDiGrowth):
    def choice(self, graph, sz, tp="in"):
        if tp == "in":
            probs = np.array([graph.count_in_degree(node) for node in graph.get_ids()]) + self.param[0]
        else:
            probs = np.array([graph.count_in_degree(node) for node in graph.get_ids()]) + self.param[1]
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(), sz, replace=False, p=probs)


class PAFixUnGrowth(FixUnGrowth):
    def choice(self, graph, sz):
        probs = graph.get_attributes("dg") + self.param
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(stable=True), sz, replace=False, p=probs)

    def clean(self, graph):
        graph = self.prep(graph)
        if self.param != 0:
            return []

        dels = graph.get_ids(stable=True)[(graph.get_attributes("dg") == 0)]
        return dels

    def prep(self, graph):
        graph.set_attrs(
            "dg", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        return graph


class PAFixDiGrowth(FixDiGrowth):
    def choice(self, graph, sz, tp="in"):
        probs = graph.get_attributes("dg_" + tp) + self.param[tp != "in"]
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(stable=True), sz, replace=False, p=probs)

    def clean(self, graph):
        if np.sum(self.param) != 0:
            return []

        graph = self.prep(graph)
        dels = graph.get_ids(stable=True)[(graph.get_attributes("dg_in") == 0)
                                         & (graph.get_attributes("dg_out") == 0)]
        return dels

    def prep(self, graph):
        graph.set_attrs(
            "dg_in", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        graph.set_attrs(
            "dg_out", {node: graph.count_out_degree(node) for node in graph.get_ids()}
        )
        return graph
