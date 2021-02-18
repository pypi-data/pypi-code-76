import numpy as np


def method_rs(x):
    r = np.arange(2, int(x.size/3))

    res = []
    for r_n in r:
        l = []
        for i in np.arange(int(x.size/r_n)):
            sub = x[i*r_n:((i+1)*r_n):1]
            bias = sub - np.mean(sub)
            l.append((np.max(bias)-np.min(bias))/np.mean(np.power(bias,2)))
        res.append(np.mean(l))
    return np.array(res), r


def h_rs(x):
    q, r = method_rs(x)
    return - np.mean(np.divide(np.log(q), np.log(r)))
