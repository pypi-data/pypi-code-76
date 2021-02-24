import numpy as np
import math as mth

from dtg.tail.estimate.hill import HillEstimator


def seq(x, sz=50):
    x_ = HillEstimator.prepare(x)
    ks = HillEstimator.get_k(x)
    g_0 = HillEstimator.estimate(x_, int(2 * mth.sqrt(x.size)))
    r_0 = 0.25 * g_0 * (x.size ** 0.25)
    ga = HillEstimator.estimate(x_, ks)

    mx = np.array(
        [
            np.max([mth.sqrt(i + 1) * (ga[i] - ga[k]) for i in np.arange(1, k)])
            for k in np.arange(2, ga.size)
        ])

    res = []
    for i in np.arange(sz):
        r_1 = r_0 * (sz - i)/sz
        r_2 = r_1 ** 0.7

        k_1 = np.where(mx > r_1)[0]
        if k_1.size == 0:
            continue
        k_1 = k_1[0] + 2
        k_2 = np.where(mx > r_2)[0]
        if k_2.size == 0:
            continue
        k_2 = k_2[0] + 2

        k_op = int(mth.pow(k_2 / mth.pow(k_1, 0.7), 10 / 3) * mth.pow(2 * g_0, 1 / 3) / 3)
        if k_op > x_.size - 2:
            continue
        return HillEstimator.estimate(x_, k_op), k_op
    return None, None
