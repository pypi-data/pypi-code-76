import numpy as np 
import sys
from .base import BaseCorr

class simbinCLF(BaseCorr):
    """
    A python class to simulate correlated binary outcomes using the conditional linear family method
    """
    def __init__(self, mu, cor, ncluster = 1):
        BaseCorr.__init__(self)
        self.mu = mu
        self.cor = cor
        self.ncluster = ncluster
     
 
    def allreg(self, Amatrix):
        n = Amatrix.shape[0]
        Bmatrix = Amatrix.copy()
        for t in range(1, n):
            t1 = t
            Gmatrix, Smatrix = Amatrix[:t1, :t1], Amatrix[:t1, [t]]
            Bvector = np.matmul(np.linalg.inv(Gmatrix), Smatrix)
            Bmatrix[:t1, [t]] = Bvector
        return Bmatrix
            
    def mbslr(self, Bmatrix, mu):
        """
        conditional means for conditional linear family
        """
        n = Bmatrix.shape[0]
        y = np.zeros(n)
        y[0] = np.random.binomial(size=1, n=1, p = mu[0])
        for t in range(1, n):
            r = y[:t] - mu[:t]
            c = mu[t] + sum(r * Bmatrix[:t, t] )
            if c < 0 or c > 1:
                raise ValueError('Conditional mean out of boundry')
                sys.exit(1)
            y[t] =  np.random.binomial(size=1, n=1, p = c)
         
        return y
    
    def simulate(self):
        """
        simulate n clusters of correlated binary outcomes 
        """
        y = None
        for i in range(self.ncluster):
            
            if self.ncluster > 1:
                cor = self.cor[i]
                mu = self.mu[i]
            else:
                cor, mu = self.cor, self.mu
                
            wrong_result = self.checkbinomial(cor, mu)
            if wrong_result:
                raise ValueError('Correlation values violate the range')
                #sys.exit(1)
                
            cov = self.cor2cov(cor, mu)
            Bmatrix = self.allreg(cov)
         
            
            if y is None:
                y = self.mbslr(Bmatrix, mu)
            else:
                yi = self.mbslr(Bmatrix, mu)
                y = np.concatenate((y, yi))
        return y
    
    def __repr__(self):
        return "Conditional Linear Family for Generating {} cluster(s)".format(self.ncluster)