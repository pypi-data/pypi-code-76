import numpy as np

from dtg.tail.estimate.estimator import TailEstimator


class HillEstimator(TailEstimator):
    @staticmethod
    def estimate(x, k):
        if hasattr(k, '__iter__'):
            return np.array([HillEstimator.estimate(x, i) for i in k])

        res = np.mean(np.log(x[-k:])) - np.log(x[-k-1])
        if np.isnan(res) or np.isinf(res):
            return -1
        return res
