import numpy as np

from joblib import Parallel, delayed

from dtg.stationary.giratis import stat
from pge.ranks.extrem_onl import NodeExInfo


class LineEx(NodeExInfo):
    @staticmethod
    def get_exes(gr, root, params):
        paths, di = gr.get_short_line_paths(root)
        res = []

        for params_ in params:
            xs, lv = gr.get_ln_attrs(params_[0], paths)
            xs2 = []
            for xs_ in xs:
                xs2 = np.append(xs2, xs_)
            ex1, ex2 = LineEx.estimate(xs, lv)
            res.append((ex1, ex2, params_[1], stat(xs2)))
        return res

    @staticmethod
    def estimate(xs, lv):
        exes = []
        ms = []

        for t1 in [True, False]:
            res = np.array(
                Parallel(n_jobs=2, backend="multiprocessing")(
                    delayed(LineEx.ex_estimate)(xs, u, t1) for u in lv
                )
            )
            res_, us_ = res[res < 1], lv[res < 1]
            if res_.size > 0:
                ex = res_[-1]
                u = us_[-1]
            else:
                ex = res[-1]
                u = lv[-1]

            exes.append(ex)
            ms.append(
                np.sum([np.sum(xs_ <= u) for xs_ in xs])
                / np.sum([xs_.size for xs_ in xs])
            )

        return (exes[0], ms[0]), (exes[1], ms[1])

    @staticmethod
    def ex_estimate(xs, lv, t1):
        ts = np.array([])

        for xs_ in xs:
            if t1:
                ts_ = np.where(xs_ > lv)[0]
            else:
                ts_ = np.where(xs_ <= lv)[0]

            if ts_.size > 1:
                ts = np.append(ts, np.diff(ts_))

        if ts.size == 0:
            return 1

        if np.max(ts) > 2:
            ex = min(
                [
                    1,
                    2
                    * np.sum(ts - 1) ** 2
                    / (ts.size * np.sum(np.multiply(ts - 1, ts - 2))),
                ]
            )
        else:
            ex = min([1, 2 * np.sum(ts) ** 2 / (ts.size * np.sum(ts ** 2))])
        return ex
