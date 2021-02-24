import numpy as np

from scipy.stats import kstest

from dtg.tail.estimate.hill import HillEstimator


def optimal_value(x):
    ks = HillEstimator.get_k(x)
    i = np.sort(x)[::-1]
    x_ = HillEstimator.prepare(x)

    res = []
    exes = []
    for k in ks:
        exes.append(1/HillEstimator.estimate(x_, k))
        fs = lambda x: 1 - x**-exes[-1]
        res.append(kstest(i/i[k], fs, N=1000)[0])

    return exes[np.argmin(res)], ks[np.argmin(res)]
