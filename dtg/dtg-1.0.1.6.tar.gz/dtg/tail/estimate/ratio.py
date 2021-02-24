import numpy as np

from dtg.tail.estimate.estimator import TailEstimator


class RatioEstimator(TailEstimator):
    @staticmethod
    def estimate(x, k):
        if hasattr(k, '__iter__'):
            return np.array([RatioEstimator.estimate(x, i) for i in k])

        x_n = x[-k-1]
        x_ = x[x > x_n]

        if x_.size == 0:
            return np.NAN

        return np.sum(np.log(x_/x_n))/x_.size
