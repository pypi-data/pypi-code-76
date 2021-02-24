"""netCDF-SCM's custom error handling"""
import warnings


def raise_no_iris_warning():
    """
    Raise a warning that iris is not installed

    Warns
    -----
    UserWarning
        `Iris <https://github.com/SciTools/iris>`_ is not installed
    """
    warn_msg = (
        "A compatible version of Iris is not installed, not all functionality will "
        "work. We recommend installing the lastest version of Iris using conda to "
        "address this."
    )
    warnings.warn(warn_msg)


class NoLicenseInformationError(AttributeError):
    """
    Exception raised when a dataset contains no license information
    """


class NonStandardLicenseError(ValueError):
    """
    Exception raised when a dataset contains a non-standard license

    For example, if a CMIP6 dataset does not contain a Creative Commons
    Attribution ShareAlike 4.0 International License
    """
