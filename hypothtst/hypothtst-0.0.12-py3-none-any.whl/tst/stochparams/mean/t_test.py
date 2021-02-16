import numpy as np
from scipy.stats import t, ttest_ind, norm, cauchy


def t_test(mu1,mu2,std1,std2,n1,n2,dist=t,alternative='two-sided'):
    std_dev = (std1**2/(n1-1)+std2**2/(n2-1))**0.5
    test_stat = (mu2-mu1)/std_dev
    df = n1+n2-2
    if test_stat>0:
        p_val = 2*dist.sf(test_stat,df)
    else:
        p_val = 2*dist.cdf(test_stat,df)
    
    if (alternative == 'greater' and mu2>mu1) or\
        (alternative == 'less' and mu2<mu1):
        return p_val/2
    elif (alternative == 'greater' and mu2<mu1) or\
        (alternative == 'less' and mu2>mu1):
        return 1-p_val/2
    else:
        return p_val


def t_test_arr(a1, a2, dist=t, alternative='two-sided'):
    mu1, mu2 = np.mean(a1), np.mean(a2)
    std1, std2 = np.std(a1), np.std(a2)
    n1, n2 = len(a1), len(a2)
    return t_test(mu1, mu2, std1, std2, n1, n2, dist, alternative)


class TTest():
    def __init__(self, alternative='two-sided', dist=t):
        self.alternative = alternative
        self.dist = dist

    def tst(self, a1, a2):
        return t_test_arr(a1, a2, self.dist, self.alternative)


class TTest_equalvar():
    def __init__(self, alternative='two-sided'):
        self.alternative = alternative

    def tst(self, a1, a2):
        return ttest_ind(a1, a2)[1]


class TTest_diffvar():
    def __init__(self, alternative='two-sided'):
        self.alternative = alternative

    def tst(self, a1, a2):
        return ttest_ind(a1, a2, equal_var=False)[1]


class Norm_null():
    def __init__(self,mu=0,sig=1):
        self.mu=mu
        self.sig=sig
    
    def cdf(self,x,df):
        return norm.cdf(x,self.mu,self.sig)

    def sf(self,x,df):
        return norm.sf(x,self.mu,self.sig)


class Cauchy_null():
    def __init__(self,loc=0,scl=1):
        self.loc=loc
        self.scl=scl

    def cdf(self,x,df):
        return cauchy.cdf(x,self.loc,self.scl)

    def sf(self,x,df):
        return cauchy.sf(x,self.loc,self.scl)


def sanity_check():
    a1 = norm.rvs(10,2,size=100)
    a2 = norm.rvs(11,2.4,size=100)
    mu1, mu2 = np.mean(a1), np.mean(a2)
    std1, std2 = np.std(a1), np.std(a2)
    n1,n2 = len(a1), len(a2)
    p_val1 = ttest_ind(a1,a2)[1]
    p_val2 = t_test(mu1,mu2,std1,std2,n1,n2)
    return p_val1 == p_val2
