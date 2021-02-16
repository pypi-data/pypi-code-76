import numpy as np
import matplotlib.pyplot as plt
from hypothtst.alpha_beta_sim import rejectn_rate


def plot_4_pvals(p_vals1, p_vals2,p_vals3,p_vals4,
                    labels=["null","theta:0.3","theta:0.2","theta:0.1"]):
    """
    This particular type of histogram happens to work very well for plotting p-values.
    """
    plt.hist(p_vals1,alpha=0.5,label=labels[0], histtype='step',\
            fill=False,stacked=True,color='green')
    plt.hist(p_vals2,alpha=0.5,label=labels[1], \
            histtype='step',fill=False,stacked=True,color='red')
    plt.hist(p_vals3,alpha=0.5,label=labels[2], histtype='step',\
            fill=False,stacked=True,color='orange')
    plt.hist(p_vals4,alpha=0.5,label=labels[3], histtype='step',\
            fill=False,stacked=True,color=(251/255, 206/255, 177/255))
    #plt.hist([p_vals_nul,p_vals_alt1,p_vals_alt2],alpha=0.5,label="theta:0.2",density=True, histtype='bar')
    plt.legend()
    plt.show()


def plot_power_3alt(p_vals_nul, p_vals_alt1,p_vals_alt2,p_vals_alt3,
                    labels=["theta:0.3","theta:0.2","theta:0.1"]):
    alphas = rejectn_rate(p_vals_nul)
    power1 = rejectn_rate(p_vals_alt1)
    power2 = rejectn_rate(p_vals_alt2)
    power3 = rejectn_rate(p_vals_alt3)
    plt.plot(alphas,power1,label=labels[0])
    plt.plot(alphas,power2,label=labels[1])
    plt.plot(alphas,power3,label=labels[2])
    plt.plot([0, 1], [0, 1], 'k-', lw=2)
    plt.legend()
    plt.show()


