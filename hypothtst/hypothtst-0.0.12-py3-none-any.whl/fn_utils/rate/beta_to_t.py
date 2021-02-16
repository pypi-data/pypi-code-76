import numpy as np
from scipy import optimize
from hypothtst.tst.greater.rate.ump import UMPPoisson

def bake_time(t1=25,
                lmb_base=12,alpha=0.05,
                beta=0.05,effect=3,n=1000):
    t2=1.0; beta_tmp=1.0
    betas = []
    while beta_tmp>beta:
        beta_tmp = UMPPoisson.beta_on_poisson_sim(t1=t1,t2=t2,\
                    lmb_base=lmb_base,
                    alpha=alpha,effect=effect,n_sim=n)
        betas.append(beta_tmp)
        t2+=1
    return t2, np.array(betas)


def bake_time_v2(t1=25,
                    lmb_base=12,alpha=0.05,
                    beta=0.05,effect=3):
    t2=1.0; beta_tmp=1.0
    betas = []
    while beta_tmp>beta:
        beta_tmp = UMPPoisson.beta_on_poisson_closed_form(t1=t1,t2=t2,\
                    lmb_base=lmb_base,
                    alpha=alpha,effect=effect)[0]
        betas.append(beta_tmp)
        t2+=1
    return t2, np.array(betas)


def bake_time_v3(t1=25,
                    lmb_base=12,alpha=0.05,
                    beta=0.05,effect=3):
    fn = lambda t2: UMPPoisson.beta_on_poisson_closed_form(t1=t1,t2=t2,\
                        lmb_base=lmb_base,
                        alpha=alpha,effect=effect)[0]-beta
    if fn(100)*fn(.01)>0:
        return 100
    root = optimize.bisect(fn,.01,200)
    #root = optimize.root(fn,x0=5).x[0]
    return root
