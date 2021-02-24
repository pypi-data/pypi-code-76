import numpy as np


class GroupEstimator:
    def __init__(self):
        self.z = 0
        self.l = 0

    def add(self, x):
        k = []
        blk_ = np.sort(x)
        k.append(blk_[-2]/blk_[-1])

        sz = len(k)
        self.z = (self.l*self.z + np.mean(k))/(self.l + sz)
        self.l += sz

    def get_l(self):
        return self.l

    def get_z(self):
        return self.z

    def plus(self, est):
        self.z = self.l*self.z + est.get_l()*est.get_z()
        self.l += est.get_l()
        self.z = self.z/self.l

    def estimate(self):
        return self.z**(-1) - 1
