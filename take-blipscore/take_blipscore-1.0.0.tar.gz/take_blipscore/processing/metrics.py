import numpy as np

ARRAY = np.ndarray
FLOAT = np.float64
ln = np.log


def blip_metric(weight: ARRAY, x: ARRAY) -> FLOAT:
    """Calculate BLiP Score metric.

    :param weight: Weight for each score.
    :type weight: ``numpy.ndarray``
    :param x: Variable array.
    :type x: ``numpy.ndarray``
    :return: Geometric meam of weighted metrics.
    :rtype: ``numpy.float64``
    """
    return __weighted_gmean(weight=weight, x=x)


def __weighted_gmean(weight: ARRAY, x: ARRAY) -> FLOAT:
    """Weighted geometric mean.
    
    :math:
    \\exp(\\sum^(n)_(i=0)wi*\\ln(xi) \\(1/\\sum^(n)_(i=0)wi)), \n
    for w as weight
    
    :param weight: Weight for each `xi`.
    :type weight: ``numpy.ndarray``
    :param x: Variable array.
    :type x: ``numpy.ndarray``
    :return: Weighted geometric mean.
    :rtype: ``numpy.float64``
    """
    return np.exp(np.vdot(weight, ln(x)) / sum(weight))

