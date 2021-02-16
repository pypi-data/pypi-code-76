import numpy as np
from scipy.stats import norm

class NormDist():
    def __init__(self, mu, sigma, n):
        self.mu = mu
        self.sigma = sigma
        self.n = n

    def rvs(self):
        if self.n>1:
            return norm.rvs(self.mu,self.sigma,size=self.n)
        else:
            return norm.rvs(self.mu,self.sigma)

