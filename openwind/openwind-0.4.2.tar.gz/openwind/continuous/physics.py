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


class Physics:
    """
    The actual Physics class.

    Parameters
    ----------
    T :
        temperature in Kelvin
    rho :
        air density
    c :
        air sound speed
    mu :
        viscosity
    Cp :
        specific heat with constant pressure
    kappa :
        thermal conductivity
    gamma :
        ratio of specific heats
    khi :
        isentropic compressibility
    c_lt :
        velocity times a characteristic distance for loss computation
    c_lv :
        velocity times a characteristic distance for loss computation

    """

    def __init__(self, temp):
        """Define the quantitities described above.

        You can find the formulae in the Chaigne and Kergomard book
        """
        T0 = 273.15
        self.T0 = T0
        self.Cp = 240
        self.gamma = 1.402

        if callable(temp):
            self.temp = temp
            self._uniform = False
        else:
            self.temp = lambda x: np.full_like(x, temp, dtype=float)
            self._uniform = True

        self.T = lambda x: self.temp(x) + T0
        self.rho = lambda x: 1.2929 * T0 / self.T(x)
        self.c = lambda x: 331.45 * np.sqrt(self.T(x) / T0)
        self.mu = lambda x: 1.708e-5 * (1 + 0.0029 * self.temp(x))
        self.kappa = lambda x: 5.77 * 1e-3 * (1 + 0.0033 * self.temp(x))
        self.khi = lambda x: 1 / (self.rho(x) * self.c(x) ** 2)
        self.c_lt = lambda x: self.kappa(x) / (self.rho(x) * self.Cp)
        self.c_lv = lambda x: self.mu(x) / self.rho(x)
        self.lt = lambda x: self.c_lt(x) / self.c(x)
        self.lv = lambda x: self.c_lv(x) / self.c(x)

    def get_coefs(self, x, *names):
        """Get the values of several coefficients at the same time.

        Parameters
        ----------
        x : float or array-like
            where to evaluate the coefficients.
        *names : string...
            the names of the coefficients to take

        Returns
        -------
        values : tuple of (float or array-like)
        """
        coefs = tuple(getattr(self, name) for name in names)
        return tuple(coef(x) if callable(coef)
                     else coef
                     for coef in coefs)

    @property
    def uniform(self):
        """Are the coefficients independent of space?

        False if the physical coefficients depend on x, True otherwise.
        """
        return self._uniform
