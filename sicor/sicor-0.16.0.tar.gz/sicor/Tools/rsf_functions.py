import numpy as np

__author__ = "Niklas Bohn, Andre Hollstein"


def gauss_rspf(wvl_center, wvl_sol_irr, sigma=None, fwhm=None):
    """ Returns normalized Gaussian response function with respect to given wavelenght grid.
        You should either give FWHM or sigma, an ValueError is raised if not
    """
    if sigma is None and fwhm is not None:
        # convert FWHM to sigma
        sigma = fwhm / (2.0 * np.sqrt(2.0 * np.log(2.0)))
    elif sigma is not None and fwhm is None:
        pass  # sigma given
    else:
        raise ValueError("Give either sigma or FWHM, not both or none!")
    rspf = np.exp(-0.5 * ((wvl_center - wvl_sol_irr) / sigma) ** 2) / (sigma * np.sqrt(2.0 * np.pi))
    rspf /= np.trapz(x=wvl_sol_irr, y=rspf)  # assure normalization (numeric errors)
    return rspf


def box_rspf(wvl_center, wvl_sol_irr, width):
    """ Returns normalized box response function with respect to given wavelenght grid. """

    rspf = np.zeros(len(wvl_sol_irr))
    rspf[np.logical_and(wvl_sol_irr < (wvl_center + width), wvl_sol_irr > (wvl_center - width))] = 1.0
    rspf /= np.trapz(x=wvl_sol_irr, y=rspf)
    return rspf
