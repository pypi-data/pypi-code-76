import numpy as np

class BaseCorr:
    """
    Base class for covariancem matrix
    """
    def __init__(self):
        pass
    
    def cor2cov(self, cor, mu):
        """
        function transforming the correlation matrix to covariance matrix
        """
        std = np.diag(np.sqrt(mu * (1 - mu)))
        return np.matmul(np.matmul(std, cor), std)
    
    def checkbinomial(self, cor, mu):
        """
        function check the boundries of correlation matrix of binomial outcomes
        """
        n = len(mu)
        std = np.sqrt(mu * (1 - mu))
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                uij = mu[i] * mu[j] + cor[i,j] * std[i] * std[j]
                
                if uij > min(mu[i], mu[j]) or uij < max(0, mu[i] + mu[j] - 1):
                    return True
        
        return False
         
        