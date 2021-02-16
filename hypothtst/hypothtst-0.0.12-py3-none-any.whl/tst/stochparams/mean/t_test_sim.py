## From scratch simulation that shows the power of the test remaining the same
## when the distribution corresponding to the null hypothesis is swapped out.
import numpy as np
from scipy.stats import norm, t, cauchy, ttest_ind
import matplotlib.pyplot as plt

## First, implement the t-test from scratch.
def t_test(mu1,mu2,std1,std2,n1,n2,null_dist_cdf):
    std_dev = (std1**2/(n1-1)+std2**2/(n2-1))**0.5
    test_stat = (mu2-mu1)/std_dev
    if test_stat>0:
        return 2*(1-null_dist_cdf(test_stat))
    else:
        return 2*(null_dist_cdf(test_stat))

def t_test_arr(a1,a2,dist=t):
    mu1, mu2 = np.mean(a1), np.mean(a2)
    std1, std2 = np.std(a1), np.std(a2)
    n1,n2 = len(a1), len(a2)
    return t_test(mu1,mu2,std1,std2,n1,n2,dist)

def alpha_beta_tradeoff(null_dist_cdf,bin_size=1):
    ## The various significance levels at which we reject the null.
    ## this effectively corresponds to different tests with lower
    ## and lower willingness to reject the null.
    alpha_hats = np.arange(0,1,0.00001)
    ## The number of simluations for drawing our alpha-beta curve.
    n_sim=10000
    ## The two distributions. In the null hypothesis, there is no differene
    ## between the populations and both follow dist1. In the alternate hypothsis,
    ## the first population follows dist1 and the second one follows dist2, with
    ## a higher mean.
    dist1 = norm(10,1.0)
    dist2 = norm(11.0,1.0)
    alphas = np.zeros(len(alpha_hats))
    for _ in range(n_sim):
        ## Draw 15 samples each from both populations
        ## per the assumption of the null. So, both follow
        ## the same distribution.
        m1 = dist1.rvs(size=15)
        m1=avg_arr_by_bins(m1,bin_size)
        m2 = dist1.rvs(size=15)
        m2=avg_arr_by_bins(m2,bin_size)
        p_val = t_test_arr(m1,m2,dist=null_dist_cdf)
        ## The false positive rate is probability of
        ## incorrectly rejecting the null.
        alphas += (p_val < alpha_hats)/n_sim
    betas = np.zeros(len(alpha_hats))
    for _ in range(n_sim):
        ##This time, generate the first sample from dist1
        ## and the second sample from dist2 in keeping with the assumptions
        ## of the alternate hypothesis.
        m1 = dist1.rvs(size=15)
        m1=avg_arr_by_bins(m1,bin_size)
        m2 = dist2.rvs(size=15)
        m2=avg_arr_by_bins(m2,bin_size)
        p_val = t_test_arr(m1,m2,dist=null_dist_cdf)
        ## The false negative rate is probability of
        ## incorrectly *not* rejecting the null.
        betas += (1.0-(p_val < alpha_hats))/n_sim
    return alphas, betas

def avg_arr_by_bins(a,bin_size):
    summ=0; cnt=0
    binned_vals=[]
    for i in range(len(a)):
        summ+=a[i]
        cnt+=1
        if ((i+1)%bin_size==0) or i==len(a)-1:
            binned_vals.append(float(summ)/cnt)
            summ=0; cnt=0
    return np.array(binned_vals)

## Finally, draw the trade-off for various values of alpha and beta.
n1=15; n2=15

null_t_cdf = lambda t_stat : t.cdf(t_stat,n1+n2-2)
alphas_t, betas_t = alpha_beta_tradeoff(null_t_cdf)

#null_std_norm_cdf = lambda t_stat : norm.cdf(t_stat)
#alphas_std_norm, betas_std_norm = alpha_beta_tradeoff(null_std_norm_cdf)
alphas_binned, betas_binned = alpha_beta_tradeoff(null_t_cdf,3)


plt.plot(alphas_t, betas_t)
#plt.plot(alphas_std_norm, betas_std_norm)
plt.plot(alphas_binned,betas_binned)
plt.show()

