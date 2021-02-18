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
import scipy.sparse as ssp

from openwind.frequential import FrequentialComponent


class FrequentialJunctionDiscontinuity(FrequentialComponent):
    """Frequential representation of a junction between two pipes with
    discontinuity of section.

    Assumes convention PH1.

    Parameters
    ----------
    ends : list(FrequentialPipe.End)
        the pipe ends this junction connects
    junc : JunctionModel
    """

    def __init__(self, junc, ends):
        self.junc = junc
        assert len(ends) == 2
        self.ends = ends
        if any(end.convention != 'PH1' for end in ends):
            msg = ("FrequentialJunction does not yet support VH1 convention")
            raise ValueError(msg)

    def __get_physical_params(self):
        radii = []
        rhos = []
        for end in self.ends:
            radius, rho, _ = end.get_physical_params()
            radii.append(radius)
            rhos.append(rho)
        assert all(np.isclose(rhos, rho))
        rho = sum(rhos)/2.0
        r1, r2 = radii
        return r1, r2, rho

    def __get_masses(self):
        r1, r2, rho = self.__get_physical_params()
        mass = self.junc.compute_masse(r1, r2, rho)
        return mass

    def get_number_dof(self):
        return 1

    def get_contrib_freq(self, omegas_scaled):
        """ Contribution of this component to the frequency-dependent diagonal
        of Ah.

        Return a sparse matrix with a shape ((number of dof) x (size of freq.))
        """
        mass_junction = self.__get_masses()
        my_contrib = 1j * omegas_scaled * mass_junction
        # Place on our indices
        Ah_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                            dtype='complex128')
        Ah_diags[self.get_indices(), :] = my_contrib
        return Ah_diags

    def get_contrib_indep_freq(self):
        assembled_interaction_matrix = ssp.lil_matrix((self.ntot_dof,
                                                       self.ntot_dof))
        interaction = [-1, 1]
        for i in range(len(self.ends)):
            f_pipe_end = self.ends[i]
            assembled_interaction_matrix[self.get_indices(),
                                         f_pipe_end.get_index()] = interaction[i]
        return assembled_interaction_matrix - assembled_interaction_matrix.T

# ----- differential -----
    def get_diff_masses(self, diff_index):
        r1, r2, rho = self.__get_physical_params()

        d_radii = []
        for end in self.ends:
            d_radius = end.get_diff_radius(diff_index)
            d_radii.append(d_radius)
        dmass = self.junc.get_diff_mass(r1, r2, rho, d_radii[0], d_radii[1])
        return dmass

    def get_contrib_dAh_freq(self, omegas_scaled, diff_index):
        dmass = self.get_diff_masses(diff_index)
        local_dAh_diags = 1j * omegas_scaled * dmass
        # Place on our indices
        dAh_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                             dtype='complex128')
        dAh_diags[self.get_indices(), :] = local_dAh_diags
        return dAh_diags
