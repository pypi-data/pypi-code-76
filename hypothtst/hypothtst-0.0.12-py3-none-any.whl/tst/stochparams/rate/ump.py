import numpy as np
from scipy.stats import binom_test, poisson, binom, nbinom
from scipy.special import comb
from scipy import optimize
from hypothtst.tst.stochparams.p_heads.binom_test import binom_tst_beta
import hypothtst.sim_utils.rate.poisson as pois
from hypothtst.alpha_beta_sim import AlphaBetaSim

def rate_tst(n1,n2,t1,t2,alternative,scale=1.0):
    return binom_test(n2/scale,(n1+n2)/scale,\
        t2/(t1+t2),alternative=alternative)

class UMPPoisson(object):
    def __init__(self,t0=25,t1=25,lmb_base=12,alpha=0.05,effect=3):
        self.t0,self.t1,self.lmb_base,self.alpha,self.effect=\
            t0,t1,lmb_base,alpha,effect
    
    @staticmethod
    def beta_on_poisson_sim(t0=25,t1=25,lmb_base=12,alpha=0.05,effect=3,
                        thresh=None,n_sim=10000):
        """
        Obtains the beta (false negative rate) given the observation
        durations for treatment and control and hypothesis test to simulate.
        args:
            t1: VM-duration observed in treatment.
            t2: VM-duration observed in control.
            fn: The test to generate simulated p_value.
                for example: simulate_binned_t_test, simulate_rateratio_test.
        """
        if thresh is None:
            thresh = np.array([alpha])
        po0=pois.PoissonDist(lmb_base*t0)
        po1=pois.PoissonDist((lmb_base+effect)*t1)
        tst = lambda n0,n1:binom_test(n1,n0+n1,t1/(t0+t1),\
                    alternative='greater')
        ab = AlphaBetaSim()
        _, _ = ab.alpha_beta_tracer(po0,po1,tst,\
                tst,n_sim=10000)
        beta = ab.beta(alpha)
        return beta

    @staticmethod
    def beta(null, alter, cut_dat=1e4,alpha=0.05):
        beta=0; n=0
        beta_n=0; beta_del=0
        q=null.t/(null.t+alter.t)
        poisson_mu = null.e_lmb*null.t+(alter.e_lmb)*alter.t
        int_poisson_mu = int(poisson_mu)
        n = int_poisson_mu-1
        dels1 = []; ns1=[]
        nbinom_s1={}; nbinom_s2={}
        while (beta_del > 1e-9 or n==int_poisson_mu-1):
            n+=1
            if n-int_poisson_mu>cut_dat:
                break
            surv_inv = int(binom.isf(alpha,n,q))
            beta_del=0
            for j in range(surv_inv+1):
                if j in nbinom_s1:
                    nb1 = nbinom_s1[j]
                else:
                    nb1 = null.pmf(j)
                    nbinom_s1[j] = nb1
                if n-j in nbinom_s2:
                    nb2 = nbinom_s2[n-j]
                else:
                    nb2 = alter.pmf(n-j)
                    nbinom_s2[n-j] = nb2
                beta_n = nb1*nb2
                beta_del+=beta_n
                beta += beta_n
            dels1.append(beta_del); ns1.append(n)
        n = int_poisson_mu
        dels2 = []; ns2=[]
        while beta_del > 1e-9 or n==int_poisson_mu:
            n-=1
            if int_poisson_mu-n>cut_dat:
                break
            surv_inv = int(binom.isf(alpha,n,q))
            beta_del=0
            for j in range(surv_inv+1):
                if j in nbinom_s1:
                    nb1 = nbinom_s1[j]
                else:
                    nb1 = null.pmf(j)
                    nbinom_s1[j] = nb1
                if n-j in nbinom_s2:
                    nb2 = nbinom_s2[n-j]
                else:
                    nb2 = alter.pmf(n-j)
                    nbinom_s2[n-j] = nb2
                beta_n = nb1*nb2
                beta_del+=beta_n
                beta += beta_n
            dels2.append(beta_del); ns2.append(n)
        dels1 = np.array(dels1); dels2 = np.array(dels2)
        dels2 = dels2[::-1]
        ns1 = np.array(ns1); ns2 = np.array(ns2); ns2 = ns2[::-1]
        ns = np.concatenate((ns2,ns1),axis=0)
        dels = np.concatenate((dels2,dels1),axis=0)
        return beta, dels, ns, int_poisson_mu
    
    @staticmethod
    def beta_on_poisson_closed_form(t1=25,t2=25,\
                lmb_base=12,effect=3,alpha=0.05,tol=1e-7):
        poisson_mu = lmb_base*t1+(lmb_base+effect)*t2
        beta = 0.0; prob_mass = 0.0
        p_null=t2/(t1+t2)
        mu_2 = t2*(lmb_base+effect); mu_1 = t1*lmb_base
        p_alt = mu_2/(mu_1+mu_2)
        int_poisson_mu = int(poisson_mu); pmf = 1.0
        while pmf > tol and int_poisson_mu>=0:
            pmf = poisson.pmf(int_poisson_mu,poisson_mu)
            prob_mass += pmf
            beta += pmf*binom_tst_beta(p_null,p_alt,int_poisson_mu,alpha)
            if np.isnan(beta):
                break
            int_poisson_mu -= 1
        int_poisson_mu = int(poisson_mu)+1; pmf=1.0
        while pmf > tol:
            pmf = poisson.pmf(int_poisson_mu,poisson_mu)
            prob_mass += pmf
            beta += pmf*binom_tst_beta(p_null,p_alt,int_poisson_mu,alpha)
            int_poisson_mu += 1
        return beta, prob_mass

    @staticmethod
    def beta_on_poisson_closed_form2(t1=25,t2=25,\
                lmb_base=12,effect=3,alpha=0.05):
        """
        Much, much slower than beta_on_poisson_closed_form. 
        Included only for demonstration of alternate summation.
        """
        beta=0; n=0
        beta_n=0; beta_del=0
        #p=lmb_base*t1/(lmb_base*t1+(lmb_base+effect)*t2)
        q=t1/(t1+t2)
        #mu_1 = t1*(lmb_base+effect); mu_2 = t2*lmb_base
        poisson_mu = lmb_base*t1+(lmb_base+effect)*t2
        int_poisson_mu = int(poisson_mu)
        n = int_poisson_mu-1
        while beta_del > 1e-9 or n==int_poisson_mu-1:
            n+=1
            surv_inv = int(binom.isf(alpha,n,q))
            beta_del=0
            for j in range(surv_inv+1):
                beta_n = poisson.pmf(j,(lmb_base+effect)*t2)*\
                        poisson.pmf(n-j,lmb_base*t1)
                beta_del+=beta_n
                beta += beta_n
        n = int_poisson_mu
        while beta_del > 1e-9 or n==int_poisson_mu:
            n-=1
            surv_inv = int(binom.isf(alpha,n,q))
            beta_del=0
            for j in range(surv_inv+1):
                beta_n = poisson.pmf(j,(lmb_base+effect)*t2)*\
                        poisson.pmf(n-j,lmb_base*t1)
                beta_del+=beta_n
                beta += beta_n
        return beta

    @staticmethod
    def beta_on_poisson_closed_form3(t1=25,t2=25,\
                lmb_base=12,effect=3):
        ## This method is only for alpha=0.5
        poisson_mu = (lmb_base+effect)*t2
        poisson_mu_base = lmb_base*t1
        prob_mass = 0.0
        int_poisson_mu = int(poisson_mu); pmf = 1.0
        beta = 0
        while pmf > 1e-7 and int_poisson_mu>=0:
            pmf = poisson.pmf(int_poisson_mu,poisson_mu)
            prob_mass += pmf
            beta += pmf*poisson.sf(int_poisson_mu-1,poisson_mu_base)
            int_poisson_mu -= 1
        int_poisson_mu = int(poisson_mu)+1; pmf=1.0
        while pmf > 1e-7:
            pmf = poisson.pmf(int_poisson_mu,poisson_mu)
            prob_mass += pmf
            beta += pmf*poisson.sf(int_poisson_mu-1,poisson_mu_base)
            int_poisson_mu += 1
        return beta, prob_mass

    @staticmethod
    def beta_on_negbinom_closed_form(t1=25,t2=25,\
                theta_base=10,m=100.0,deltheta=3,alpha=0.05,cut_dat=1e4):
        del_lmb = m*deltheta/theta_base/(theta_base-deltheta)
        return UMPPoisson.beta_on_negbinom_closed_form2(t1,t2,\
                    theta_base,m,del_lmb,alpha,cut_dat)

    @staticmethod
    def beta_on_negbinom_closed_form2(t1=25,t2=25,\
                theta_base=10,m=100.0,effect=3,alpha=0.05,\
                cut_dat=1e4):
        beta=0; n=0
        beta_n=0; beta_del=0
        q=t1/(t1+t2)
        lmb_base = m/theta_base
        #mu_1 = t1*(lmb_base+effect); mu_2 = t2*lmb_base
        p1 = theta_base/(theta_base+t1)
        del_theta = theta_base**2*effect/(m+theta_base*effect)
        theta2=theta_base-del_theta
        p2 = theta2/(t2+theta2)
        poisson_mu = lmb_base*t1+(lmb_base+effect)*t2
        int_poisson_mu = int(poisson_mu)
        n = int_poisson_mu-1
        dels1 = []; ns1=[]
        if effect == 0:
            nbinom_s1={}; nbinom_s2 = nbinom_s1
        else:
            nbinom_s1={}; nbinom_s2={}
        while (beta_del > 1e-9 or n==int_poisson_mu-1):
            n+=1
            if n-int_poisson_mu>cut_dat:
                break
            surv_inv = int(binom.isf(alpha,n,q))
            beta_del=0
            for j in range(surv_inv+1):
            #for j in range(n+1):
                if j in nbinom_s1:
                    nb1 = nbinom_s1[j]
                else:
                    nb1 = nbinom.pmf(j,m,p2)
                    nbinom_s1[j] = nb1
                if n-j in nbinom_s2:
                    nb2 = nbinom_s2[n-j]
                else:
                    nb2 = nbinom.pmf(n-j,m,p1)
                    nbinom_s2[n-j] = nb2
                beta_n = nb1*nb2
                beta_del+=beta_n
                beta += beta_n
            dels1.append(beta_del); ns1.append(n)
        n = int_poisson_mu
        dels2 = []; ns2=[]
        while beta_del > 1e-9 or n==int_poisson_mu:
            n-=1
            if int_poisson_mu-n>cut_dat:
                break
            surv_inv = int(binom.isf(alpha,n,q))
            beta_del=0
            for j in range(surv_inv+1):
            #for j in range(n+1):
                if j in nbinom_s1:
                    nb1 = nbinom_s1[j]
                else:
                    nb1 = nbinom.pmf(j,m,p2)
                    nbinom_s1[j] = nb1
                if n-j in nbinom_s2:
                    nb2 = nbinom_s2[n-j]
                else:
                    nb2 = nbinom.pmf(n-j,m,p1)
                    nbinom_s2[n-j] = nb2
                beta_n = nb1*nb2
                beta_del+=beta_n
                beta += beta_n
            dels2.append(beta_del); ns2.append(n)
        dels1 = np.array(dels1); dels2 = np.array(dels2); dels2 = dels2[::-1]
        ns1 = np.array(ns1); ns2 = np.array(ns2); ns2 = ns2[::-1]
        ns = np.concatenate((ns2,ns1),axis=0)
        dels = np.concatenate((dels2,dels1),axis=0)
        return beta, dels, ns, int_poisson_mu

    @staticmethod
    def beta_on_negbinom_closed_form3(t1=25,t2=25,\
                theta_base=10,m=100.0,deltheta=3):
        """
        This method only works for alpha=0.5.
        """
        if deltheta > theta_base:
            #TODO: Replace this with exception.
            print("deltheta must be smaller than theta.")
            return
        theta_alt = theta_base-deltheta
        neg_binom_ix = 0
        p2 = theta_alt/(t2+theta_alt)
        p1 = theta_base/(t1+theta_base)
        mode1 = int(p1*(m-1)/(1-p1))
        beta = 0; del_beta = 1
        while del_beta>1e-7 or neg_binom_ix<mode1 or neg_binom_ix<1000:
            del_beta = nbinom.pmf(neg_binom_ix,m,p2)*\
                        nbinom.sf(neg_binom_ix-1,m,p1)
            beta += del_beta
            neg_binom_ix+=1
        return beta

    @staticmethod
    def alpha_on_determinist_compound_closed_form(lmb=10.0,t1=10,\
                                                t2=10,l=3,verbose=False):
        alpha_hats = np.arange(0.00001,1.0,0.01)
        #alpha_hats = np.array([0.05])
        p = t2/(t1+t2)
        alphas = np.zeros(len(alpha_hats))
        k = int(lmb*(t1+t2))
        alpha_dels = np.ones(len(alpha_hats))
        total_pois_mass = 0.0
        #TODO: Replace this with other condition.
        while sum(alpha_dels)>1e-7*len(alpha_dels):
            isfs = binom.isf(alpha_hats,k*l,p)
            cdfs = binom.sf((isfs/l).astype(int),k,p)
            pmf = poisson.pmf(k,lmb*(t1+t2))
            total_pois_mass+=pmf
            alpha_dels = pmf*cdfs
            alphas += alpha_dels
            if verbose and (k-int(lmb*(t1+t2)))%100==0:
                print("k="+str(k-int(lmb*(t1+t2))) + " alpha_dels sum: "\
                    + str(sum(alpha_dels)))
            k+=1
        if verbose:
            print("Completed first loop")
        k = int(lmb*(t1+t2))-1
        while k>=0:
            isfs = binom.isf(alpha_hats,k*l,p)
            cdfs = binom.sf((isfs/l).astype(int),k,p)
            pmf = poisson.pmf(k,lmb*(t1+t2))
            total_pois_mass+=pmf
            alpha_dels = pmf*cdfs
            if np.isnan(sum(alpha_dels)):
                print(k)
            alphas += alpha_dels
            k-=1
        return alphas, alpha_hats, total_pois_mass

    @staticmethod
    def alpha_on_poisson_with_linesrch(t1=25,t2=25,\
                lmb_base=12,effect=3,beta=0.15,tol=1e-7):
        fn = lambda alpha: UMPPoisson.beta_on_poisson_closed_form(t1=t1,t2=t2,\
                        lmb_base=lmb_base,
                        alpha=alpha,effect=effect)[0]-beta
        ## TODO: Since we know the curve is convex, the root will probably be
        ## smaller than bisection point. Take this into account for efficiency.
        root = optimize.bisect(fn,0.0,1.0)
        #root = optimize.root(fn,x0=5).x[0]
        return root

    @staticmethod
    def effect_vmhours_equal_t(t=25,\
                lmb_base=12,beta=0.3,alpha=0.01,tol=1e-7, max_effect=100.0):
        t1=t2=t
        fn = lambda effect: UMPPoisson.beta_on_poisson_closed_form(t1=t1,t2=t2,\
                        lmb_base=lmb_base,
                        alpha=alpha,effect=effect)[0]-beta
        ## TODO: Since we know the curve is convex, the root will probably be
        ## smaller than bisection point. Take this into account for efficiency.
        root = optimize.bisect(fn,0.0,max_effect)
        #root = optimize.root(fn,x0=5).x[0]
        return root

    @staticmethod
    def beta_alpha_curve_on_poisson(t1=25,t2=25,lmb_base=12,effect=3,n_pts=100):
        alphas = np.arange(0,1+1/n_pts,1/n_pts)
        betas = []
        for alp in alphas:
            betas.append(UMPPoisson.beta_on_poisson_closed_form(t1,t2,lmb_base,effect,alp)[0])
        return alphas, np.array(betas)



def p_n1(t0, t1, n0, n1):
    n=n0+n1; t=t0+t1
    return t0**n0*t1**n1/(t**n*comb(n,n0))

