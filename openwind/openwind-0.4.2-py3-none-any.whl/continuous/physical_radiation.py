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

from openwind.continuous import NetlistComponent
from openwind.continuous import (RadiationModel,
                                 RadiationPulsatingSphere,
                                 RadiationPerfectlyOpen,
                                 radiation_pade)

def radiation_model(model_name):
    """Get a RadiationModel corresponding to the given model name.

    List of available model names :
        ['planar_piston', 'unflanged', 'infinite_flanged',
        'pulsating_sphere', 'perfectly_open', 'total_transmission',
        'closed']

    Parameters
    ----------
    model_name : str or openwind.continuous.RadiationModel
        The name of a radiation model, or an actual RadiationModel.
        If model_name is a RadiationModel, it is returned unchanged.

    Returns
    -------
    A RadiationModel corresponding to `model_name`.
    """
    if isinstance(model_name, RadiationModel):
        return model_name
    # Specialized models
    if model_name == 'pulsating_sphere':
        print("WARNING: pulsating_sphere assumes a 72.4° cone for now")
        return RadiationPulsatingSphere(theta=72.4/180*np.pi)
    if model_name == "perfectly_open":
        return RadiationPerfectlyOpen()
    # All other models are of type RadiationPade
    return radiation_pade(model_name)

class PhysicalRadiation(NetlistComponent):
    """Netlist component corresponding to a radiating end.

    Contains a RadiationModel used to compute the radiation impedance.
    """

    def __init__(self, rad_model, label, scaling, convention):
        super().__init__(label, scaling, convention)
        self.model = rad_model

    def get_impedance(self, omegas_scaled, radius, rho, c, opening_factor):
        """Compute radiation impedance at pulsation 'omegas'."""
        omegas = omegas_scaled / self.scaling.get_time()
        Zr =  self.model.get_impedance(omegas, radius, rho, c, opening_factor)
        return Zr / self.scaling.get_impedance()

    def get_radiation_at(self, omegas_scaled, radius, rho, c, opening_factor):
        """Radiation coefficient, to be put in the matrix."""
        omegas = omegas_scaled / self.scaling.get_time()
        if self.convention == 'PH1':
            Yr = self.model.get_admitance(omegas, radius, rho, c,
                                          opening_factor)
            return Yr * self.scaling.get_impedance()
        elif self.convention == 'VH1':
            Zr = self.model.get_impedance(omegas, radius, rho, c,
                                                 opening_factor)
            return Zr / self.scaling.get_impedance()
        assert False  # Should not be reached

    def get_diff_radiation_at(self, dr, omegas_scaled, radius,
                              rho, c, opening_factor):
        """Give the differentiate of the radiation with respect to the
        opening radius at the angular frequencies 'omegas' """
        omegas = omegas_scaled / self.scaling.get_time()
        if self.convention == 'PH1':
            d_Yr = self.model.get_diff_admitance(dr, omegas, radius, rho, c,
                                             opening_factor)
            return d_Yr * self.scaling.get_impedance()
        elif self.convention == 'VH1':
            d_Zr = self.model.get_diff_impedance(dr, omegas, radius, rho, c,
                                             opening_factor)
            return d_Zr / self.scaling.get_impedance()
        assert False  # Should not be reached
