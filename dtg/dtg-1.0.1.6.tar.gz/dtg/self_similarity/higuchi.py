import numpy as np


def method_higushi(x):
    l = []
    k = np.arange(4, x.size/2)

    for i in k:
        js = []
        for j in np.arange(i):
            sub = x[j:x.size:i]
            c = (x.size-1)/(((j+1)**2) * int((x.size-j-1)/(j+1)))
            js.append(c*np.sum([abs(sub[f+1] - sub[f]) for f in np.arange(sub.size-1)]))
        l.append(np.mean(js))

    return np.array(l), k


def h_higushi(x):
    l, k = method_higushi(x)
    return np.mean(np.divide(np.log(k),np.log(l)))
