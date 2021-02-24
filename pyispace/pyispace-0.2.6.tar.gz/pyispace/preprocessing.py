import numpy as np
from scipy.stats import boxcox, zscore, iqr


def auto_normalize(X, Y):
    Xpos = np.subtract(X, np.min(X, axis=0)) + 1

    def normalize(v):
        if ~np.all(v[1:] == v[:-1]):
            return zscore(boxcox(v)[0], ddof=1)
        else:
            return np.zeros(np.shape(v))

    Xnorm = np.apply_along_axis(normalize, 0, Xpos)
    Ynorm = np.apply_along_axis(normalize, 0, Y)

    return Xnorm, Ynorm


def bound_outliers(X):
    IQR = iqr(X, axis=0)
    a_min = np.median(X, axis=0) - 5 * IQR
    a_max = np.median(X, axis=0) + 5 * IQR

    return np.clip(X, a_min, a_max)
