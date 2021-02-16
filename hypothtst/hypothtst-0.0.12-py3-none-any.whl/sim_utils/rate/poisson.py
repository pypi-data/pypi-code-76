import numpy as np
from scipy.stats import poisson, binom_test

rate_tst = lambda n1,n2,t1,t2,alternative,scale=1.0: binom_test(n2/scale,(n1+n2)/scale,\
        t2/(t1+t2),alternative=alternative)

class PoissonDist():
    def __init__(self,lmb):
        self.lmb=lmb

    def rvs(self):
        return poisson.rvs(self.lmb)


class Poisson():
    def __init__(self, lmb1, lmb2, t1, t2):
        self.lmb1=lmb1
        self.lmb2=lmb2
        self.t1=t1
        self.t2=t2

    @staticmethod
    def one_pval_s(lmb1,t1,lmb2,t2,alternative='greater',tst=rate_tst):
        """
        Simulates data from two Poisson distributions
        and finds the p-value for a one-sided test.
        args:
            lmb1: The failure rate for first population.
            t1: The time observed for first population.
            lmb2: The failure rate for second population.
            t2: The time observed for second population
        """
        n1 = poisson.rvs(lmb1*t1)
        n2 = poisson.rvs(lmb2*t2)
        #p_val = binom_test(n2,n1+n2,t2/(t1+t2),alternative=alternative)
        ## We know that for Poisson, only time periods and total events
        ## are important due to independent increments.
        p_val = tst(n1,n2,t1,t2,alternative)
        return p_val

    def one_pval(self,alternative='greater',tst=rate_tst):
        return Poisson.one_pval_s(self.lmb1,self.t1,self.lmb2,\
                    self.t2,alternative,tst)

    @staticmethod
    def rejection_rate_s(lmb1=12.0, lmb2=12.0,
                            t1=2.5, t2=2.5, n_sim=10000,
                            thresh=np.arange(0.001,1.0,0.01),tst=rate_tst):
        """
        Given various values of alpha, gets the percentage of time
        the second sample is deemed to have a greater rate than the
        first sample. In other words, rate at which the null is rejected.
        args:
            lmb1: The failure rate of the first population.
            lmb2: The failure rate of the second population.
            t1: The time data is collected for first population.
            t2: The time data is collected for the second population.
            n: The number of simulations.
            thresh: The alpha levels.            
        """
        reject_rate=np.zeros(len(thresh))
        for _ in range(n_sim):
            #n1 is control, n2 is treatment.
            p_val = Poisson.one_pval_s(lmb1,t1,lmb2,t2,tst=tst)
            reject_rate+=(p_val<thresh)
        return reject_rate/n_sim

    def rejection_rate(self,n_sim=10000):
        return Poisson.rejection_rate_s(self.lmb1,self.lmb2,\
                                self.t1,self.t2,n_sim)

