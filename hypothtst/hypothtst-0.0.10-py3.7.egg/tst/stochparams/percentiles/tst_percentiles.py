import numpy as np
from scipy.stats import norm
from hypothtst.tst.stochparams.mean.t_test import t_test
import matplotlib.pyplot as plt

def alpha_beta_tradeoff():
    ## The various significance levels at which we reject the null.
    ## this effectively corresponds to different tests with lower
    ## and lower willingness to reject the null.
    alpha_hats = np.arange(1e-4,1,0.00001)
    ## The number of simluations for drawing our alpha-beta curve.
    n_sim=10000
    ## The two distributions. In the null hypothesis, there is no differene
    ## between the populations and both follow dist1. In the alternate hypothsis,
    ## the first population follows dist1 and the second one follows dist2, with
    ## a higher mean.
    dist1 = norm(10,2)
    dist2 = norm(12,1.8)
    alphas = np.zeros(len(alpha_hats))
    for _ in range(n_sim):
        ## Draw 15 samples each from both populations
        ## per the assumption of the null. So, both follow
        ## the same distribution.
        m1 = dist1.rvs(size=25)
        m2 = dist1.rvs(size=25)
        per_1, std1 = bootstrap_var(m1)
        per_2, std2 = bootstrap_var(m2)
        p_val = t_test(per_1,per_2,std1,std2,25,25)
        ## The false positive rate is probability of
        ## incorrectly rejecting the null.
        alphas += (p_val < alpha_hats)/n_sim
    betas = np.zeros(len(alpha_hats))
    for _ in range(n_sim):
        ##This time, generate the first sample from dist1
        ## and the second sample from dist2 in keeping with the assumptions
        ## of the alternate hypothesis.
        m1 = dist1.rvs(size=25)
        m2 = dist2.rvs(size=25)
        per_1, std1 = bootstrap_var(m1)
        per_2, std2 = bootstrap_var(m2)
        p_val = t_test(per_1,per_2,std1,std2,25,25)
        ## The false negative rate is probability of
        ## incorrectly *not* rejecting the null.
        betas += (1.0-(p_val < alpha_hats))/n_sim
    return alphas, betas


def bootstrap_var(m,q=.75,b_n=300):
    n = len(m)
    per = m[int(n*q)+1]
    var = 0
    for _ in range(b_n):
        b_m = np.random.choice(m,size=len(m))
        var += 1/(b_n-1)*(b_m[int(n*q)+1]-per)**2
    return per, np.sqrt(var)


alphas, betas = alpha_beta_tradeoff()
plt.plot(alphas, betas)


