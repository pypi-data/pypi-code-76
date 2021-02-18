import numpy as np

from dtg.stationary.dierckx import stat_exponential
from dtg.stationary.giratis import stat
from pge.ranks.extrem_onl import NodeExInfo


class WayEx(NodeExInfo):
    @staticmethod
    def get_exes_comm(gr, nodes, params, mn=True):
        res = []
        for params_ in params:
            cls = gr.get_attributes(params_[0], nodes)
            ex_tmp = 1
            ex = 1
            u = np.max(cls)
            for u in np.unique(cls)[::-1]:
                ts = np.array(gr.get_all_short_pathes(nodes[cls > u])[1])
                if ts.size == 0:
                    continue

                if np.max(ts) > 2:
                    ex = min(
                        [
                            1,
                            2
                            * np.mean(ts - 1) ** 2
                            / (np.mean(np.multiply(ts - 1, ts - 2))),
                        ]
                    )
                else:
                    ex = min([1, 2 * np.mean(ts) ** 2 / (np.mean(ts ** 2))])
                if mn:
                    if ex < 1:
                        break
                else:
                    if 1 > ex >= ex_tmp > 0:
                        ex = ex_tmp
                        break
                ex_tmp = ex
            res.append((ex, u))
        return res

    @staticmethod
    def get_gen_exes_comm(gr, nodes, params):
        res = []

        ds = np.array([gr.count_in_degree(node) for node in gr.get_ids()])
        for params_ in params:
            fl_cls = gr.get_attributes(params_[0])
            cls = gr.get_attributes(params_[0], nodes)
            ex_tmp = 1
            ex = 1
            u = np.min(cls)
            for u in np.unique(cls)[::-1]:
                ts = np.array(gr.get_all_short_pathes(nodes[cls > u])[1])
                if ts.size == 0:
                    continue

                t1 = np.mean(ts)
                t2 = np.mean(ts ** 2)
                t3 = np.mean(ts ** 3)
                ex = max(
                    [
                        0,
                        min(
                            [
                                1,
                                np.log(1 - 3 * (t2 - t1) / (t3 - t1))
                                / (np.log(np.sum(ds[fl_cls <= u]) / np.sum(ds))),
                            ]
                        ),
                    ]
                )

                if 1 > ex >= ex_tmp > 0:
                    break
                ex_tmp = ex
            res.append((ex_tmp, u))
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
