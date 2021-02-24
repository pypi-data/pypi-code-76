import numpy as np

from dtg.stationary.dierckx import stat_exponential
from dtg.stationary.giratis import stat
from pge.cluster.cycle import all_cycles_undirected
from pge.ranks.extrem_onl import NodeExInfo


class CircleEx(NodeExInfo):
    @staticmethod
    def get_exes_comm(gr, nodes, params):
        res = []
        cycles = all_cycles_undirected(gr.subgraph(nodes))

        for params_ in params:
            exes = []
            alps = []

            for cycle in cycles:
                cls = gr.get_attributes(params_[0], cycle)
                for _ in np.arange(8):
                    cls = np.append(cls, cls)

                cls = [gr.get_attributes(params_[0], cycle) for cycle in cycles]
                exes.append(params_[1].estimate(cls))
                alps.append(params_[2].estimate(cls))

            exes = np.array(exes)
            alps = np.array(alps)

            res.append(np.mean(exes[alps == np.max(alps)]))
        return res

    @staticmethod
    def get_view(gr, nodes, params):
        res = []

        # ds = np.array([gr.count_in_degree(node) for node in gr.get_ids()])
        ds = np.array([gr.count_in_degree(node) for node in nodes])
        for params_ in params:
            cls = gr.get_attributes(params_[0], nodes)

            for u in np.unique(cls)[::-1]:
                ts = np.array(gr.get_all_short_pathes(nodes[cls > u])[1])

                res.append(np.mean(ds[cls > u]) / ts.size)
        return res, np.unique(cls)[::-1]

    @staticmethod
    def get_test_comm(gr, nodes, level, param):
        if nodes.size == 0:
            return (0, 0), (0, 0)

        cls = gr.get_attributes(param, nodes)
        ts = gr.get_all_short_pathes(nodes[cls > level], plain=True)[1]
        if ts.size == 0:
            return (0, 0), (stat(cls), np.mean(cls))

        q = np.sum(gr.get_attributes(param) > level) / gr.size()
        return (
            (
                stat_exponential(ts, q),
                q
                * np.sum([np.sum(ti) for ti in ts])
                / np.sum([np.size(ti) for ti in ts]),
            ),
            (stat(cls), np.mean(cls)),
        )
