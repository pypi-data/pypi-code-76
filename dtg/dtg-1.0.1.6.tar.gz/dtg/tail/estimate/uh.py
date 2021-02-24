import numpy as np

from dtg.tail.estimate.hill import HillEstimator


class UHEstimator(HillEstimator):
    @staticmethod
    def estimate(x, k):
        if hasattr(k, '__iter__'):
            return np.array([UHEstimator.estimate(x, i) for i in k])
        x_ = np.array([x[-i - 1] * (super(UHEstimator, UHEstimator).estimate(x, i)) for i in super(UHEstimator, UHEstimator).get_k(x)])
        if k >= x_.size or k < 0:
            k = x_.size - 1
        return super(UHEstimator, UHEstimator).estimate(x_, k)

    @staticmethod
    def get_k(x):
        res = super(UHEstimator, UHEstimator).get_k(x)
        return np.arange(res.size)
