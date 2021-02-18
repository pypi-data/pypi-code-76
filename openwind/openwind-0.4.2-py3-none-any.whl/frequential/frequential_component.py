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

"""Base class for the matrices of linear components and their interactions."""
from abc import ABC, abstractmethod

from scipy.sparse import csr_matrix, bmat


class FrequentialComponent(ABC): # Abstract Base Class
    """A component of an instrument with linear behavior.

    Computing the impedance of a complex instrument with
    the Finite Elements Method or with the Transfer Matrix Method
    amounts to solving a rather large system of equations,
    given by the fundamental equations of each component
    of the instrument, and the way they are connected: \
        Ah Uh = Lh,
    where Ah is the sum of the matrix contributions of all components,
    and Lh is the sum of the source contributions of all components.

    Each FComponent may have internal variables, also
    called "degrees of freedom" or `dof`,
    corresponding to coefficients in the unknown vector `Uh`.

    For performance reasons, its contribution to Ah is split into
    a frequency-independent part and a frequency-dependent part.
    The latter is assumed to lie on the diagonal of Ah.
    """

    # --------------------------------------------------------
    # These methods must be overridden by implementing classes
    # --------------------------------------------------------

    @abstractmethod
    def get_number_dof(self):
        """Number of degrees of freedom added by this component.

        The number of equations is the total number of degrees of freedom.
        """

    def get_contrib_indep_freq(self):
        """Contribution of this component to the frequency-independent
        terms of Ah.

        Returns a sparse matrix of size (ntot_dof x ntot_dof).
        """
        return 0


    def get_contrib_freq(self, omegas_scaled):
        """ Contribution of this component to the frequency-dependent
        diagonal of Ah.
        Return a dense matrix with a shape ((number of dof) x len(fs)).
        """
        return 0

    def get_contrib_source(self):
        """ Contribution of this component to the right-hand side Lh.
        Return a sparse matrix with a shape ((number of dof) x 1).
        """
        return 0

    def get_contrib_dAh_freq(self, omegas_scaled, diff_index):
        return 0

    def get_contrib_dAh_indep_freq(self, diff_index):
        return 0

    # ---------------------------------------------------
    # The following functions do not need to be overriden
    # ---------------------------------------------------

    def set_total_degrees_of_freedom(self, ntot_dof):
        self.ntot_dof = ntot_dof

    def set_first_index(self, ind_1st):
        self.ind_1st = ind_1st

    def get_first_index(self):
        return self.ind_1st

    def get_indices(self):
        i0 = self.get_first_index()
        return range(i0, i0 + self.get_number_dof())

    def place_in_big_matrix(self, local_Ah):
        """Build the contribution to the overall matrix Ah, assuming it is
        locally given by local_Ah.
        """
        assert local_Ah.shape == (self.get_number_dof(),)*2
        n_left = self.get_first_index()
        Ah_left = csr_matrix((n_left, n_left))
        n_right = self.ntot_dof - self.get_indices().stop
        Ah_right = csr_matrix((n_right, n_right))
        Ah = bmat([[Ah_left, None, None], [None, local_Ah, None],
                   [None, None, Ah_right]], dtype='complex128')
        return Ah

    def __repr__(self):
        classname = type(self).__name__
        classname = classname.replace('Frequential','F')
        msg = "<{}>".format(classname, id(self))
        return msg
