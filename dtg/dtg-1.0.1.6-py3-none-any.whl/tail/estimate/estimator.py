import numpy as np


class TailEstimator:
    @staticmethod
    def prepare(x):
        return np.sort(x)

    @staticmethod
    def get_k(x):
        return np.arange(2, x.size-2)

    @staticmethod
    def estimate(x, k):
        return None

    @staticmethod
    def get_opt_k(x):
        return None
