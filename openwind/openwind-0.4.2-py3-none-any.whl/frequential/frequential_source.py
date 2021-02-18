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
from scipy.sparse import csr_matrix
from openwind.frequential import FrequentialComponent



class FrequentialSource(FrequentialComponent):
    """Compute the source terme Lh for the linear system to solve (Ah.Uh=Lh)

    Parameters
    ----------
    source : Excitator. Must be Flow. 
    (end,) : frequential pipe end associated to this source condition
    """

    def __init__(self, source, ends):
        self.end, = ends  # Unpack one
        self.source = source

    def get_scaling(self):
        return self.source.scaling

    def get_convention(self):
        return self.end.convention

    def get_number_dof(self):
        return 0

    def get_contrib_source(self):
        index_source = self.get_source_index()
        return csr_matrix(([1], ([index_source], [0])),
                          shape=(self.ntot_dof, 1))

    def get_source_index(self):
        """Get index where this source brings a nonzero term.
        """
        return self.end.get_index()

    def get_Zc0(self):
        radius, rho, c = self.end.get_physical_params()
        return rho*c/(np.pi*radius**2)
