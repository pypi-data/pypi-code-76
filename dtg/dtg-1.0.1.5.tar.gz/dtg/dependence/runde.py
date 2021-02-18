import numpy as np

from dtg.add.transform import symmetrization
from dtg.dependence.acf import acf


def stat(x, h, alp, sym=True, fun=acf):
    n = x.size
    if sym:
        x = symmetrization(x)

    res = (n / np.log(n)) ** (2 / alp) * np.sum(
        [fun(x, i + 1) ** 2 for i in np.arange(h)]
    )
    return res, p_value(res, alp)


def p_value(x, alp):
    return
