import numpy as np
import math as m

from dtg.tail.estimate.hill import HillEstimator


class MomentEstimator(HillEstimator):
    @staticmethod
    def estimate(x, k):
        if hasattr(k, '__iter__'):
            return np.array([MomentEstimator.estimate(x, i) for i in k])

        h = super(MomentEstimator, MomentEstimator).estimate(x, k)
        s = np.mean([(m.log(x[-i-1]/x[-k-1]))**2 for i in np.arange(k) if x[-i-1]/x[-k-1] > 0])
        if s == 0:
            return np.NAN
        return h + 1 - 0.5*((1 - ((h**2)/s))**2)
