import numpy as np
from scipy.stats import binom_test
from algorith.arrays.pt_process.overlap import critical_events
from algorith.arrays.pt_process.window import critical_interval

def correlation_score(ts1,ts2,w,delt,verbose=False):
    """
    ts1 rains on ts2 in a w-window.
    """
    interv = critical_interval(ts2,w,delt)
    evnts = critical_events(ts1,ts2,w)
    if verbose:
        print(str(evnts)+","+str(len(ts1))+","+str(interv/delt))
    return binom_test(evnts,len(ts1),interv/delt,alternative='greater')

