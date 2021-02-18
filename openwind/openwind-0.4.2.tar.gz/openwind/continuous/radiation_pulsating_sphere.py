#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
              "Alexis Thibault", "Tobias Van Baarsel"]
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"

import numpy as np

from openwind.continuous import RadiationModel


class RadiationPulsatingSphere(RadiationModel):
    """Radiation impedance model based on a pulsating portion of a sphere.

    Formulas from [1], equation (15).

    References
    ----------
    [1] Hélie, T., Hézard, T., Mignot, R., & Matignon, D. (2013).
    One-dimensional acoustic models of horns and comparison with measurements.
    Acta acustica united with Acustica, 99(6), 960-974.
    """

    def __init__(self, theta):
        """
        Parameters
        ----------
        theta : float
            Bell opening angle in radians.
        """
        self.theta = theta
        assert theta >= 0
        assert theta <= np.pi/2
        # Compute parameters of the model
        self.xi = 0.0207*theta**4 - 0.144*theta**3 + 0.221*theta**2 \
            + 0.0799*theta + 0.72
        self.alpha = 1/(0.1113*theta**5 - 0.6360*theta**4 + 1.162*theta**3
                        - 1.242*theta**2 + 1.083*theta + 0.8788)
        self.nu_c = 1/(-0.198*theta**5 + 0.2607*theta**4 - 0.424*theta**3
                       -0.07946*theta**2 + 4.704*theta + 0.022)

    @property
    def name(self):
        return "pulsating_sphere"

    def __repr__(self):
        return "RadiationPulsatingSphere(theta={:.5f})".format(self.theta)

    def get_impedance(self, omegas_scaled, radius, rho, c, opening_factor):
        r_sphere = radius / np.sin(self.theta)
        nu_ratio = omegas_scaled/c * r_sphere/(2*np.pi * self.nu_c)
        impedance = ((1j*self.alpha*nu_ratio - nu_ratio**2)
            / (1 + 2j*self.xi*nu_ratio - nu_ratio**2))
        return impedance * rho*c/(radius**2*np.pi)

    def get_admitance(self, *args, **kwargs):
        return 1/self.get_impedance(*args, **kwargs)

    def get_diff_impedance(self, *args, **kwargs):
        raise NotImplementedError
    def get_diff_admitance(self, *args, **kwargs):
        raise NotImplementedError
