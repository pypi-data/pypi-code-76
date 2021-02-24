import numpy as np


class PoisTimer:
    def __init__(self, lamb):
        self.lamb = lamb

    def get_times(self, n):
        return np.random.poisson(self.lamb, n)


class ExpTimer:
    def __init__(self, lamb):
        self.lamb = lamb

    def get_times(self, n):
        return np.random.exponential(self.lamb, n)
