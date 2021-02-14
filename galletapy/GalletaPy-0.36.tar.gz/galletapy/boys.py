from scipy.special import hyp1f1

def F_n(n,x):
    return hyp1f1(n+1/2,n+3/2,-x)/(2*n+1)
