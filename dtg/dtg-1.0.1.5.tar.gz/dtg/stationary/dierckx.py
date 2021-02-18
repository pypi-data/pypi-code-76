import numpy as np
import itertools


def stat_exponential(data_split, q):
    sz = np.sum([np.size(data) for data in data_split])
    st = sz * np.log(np.sum([q*np.sum(data) for data in data_split])/sz)
    for data in data_split:
        st -= np.size(data)*np.log(q*np.mean(data))
    return np.sqrt(2*np.abs(st))


def full_stat_exponential(data):
    st0 = np.size(data) * np.log(np.mean(data))
    st = []
    for r in np.arange(1, np.floor((np.size(data)/2))):
        for data_ in itertools.combinations(data, int(r)):
            st.append(st0-r*np.log(np.mean(data_))-(np.size(data_)-r)*np.log((np.sum(data)-np.sum(data_))/(np.size(data_)-r)))
    return np.sqrt(2*np.max(st))
