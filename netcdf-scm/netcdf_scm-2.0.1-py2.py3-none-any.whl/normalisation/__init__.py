"""
Normalisation handling

Within netCDF-SCM, 'normalisation' refers to taking anomalies from some set
of reference values. For example, subtracting a 21-year running mean from
a pre-industrial control experiment from the results of a projection
experiment.
"""
from .after_branch_time_mean import AfterBranchTimeMean
from .running_mean import NormaliserRunningMean
from .running_mean_dedrift import NormaliserRunningMeanDedrift


def get_normaliser(key):
    """
    Get the appropriate normaliser for a given key

    Parameters
    ----------
    key : str
        Key which specifies the type of normaliser to get

    Returns
    -------
    :obj:`netcdf_scm.normalisation.base.Normaliser`
        Normaliser appropriate for ``key``

    Raises
    ------
    ValueError
        ``key`` cannot be mapped to a known normaliser
    """
    if key == "21-yr-running-mean":
        return NormaliserRunningMean(nyears=21)

    if key == "30-yr-running-mean":
        return NormaliserRunningMean(nyears=30)

    if key == "21-yr-running-mean-dedrift":
        return NormaliserRunningMeanDedrift(nyears=21)

    if key == "30-yr-running-mean-dedrift":
        return NormaliserRunningMeanDedrift(nyears=30)

    if key == "31-yr-mean-after-branch-time":
        return AfterBranchTimeMean()

    raise ValueError("Unrecognised key: '{}'".format(key))
