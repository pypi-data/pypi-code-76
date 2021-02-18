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


"""Numerical scheme for a junction of two pipes."""

import numpy as np

from openwind.temporal import TemporalComponent

class TemporalSimpleJunction(TemporalComponent):
    """A model of junction, for use in temporal simulation.

    Interacts with two ``TemporalPipe.End``.
    Ensures pressure continuity, and flow conservation (Kirchhoff conditions).
    Does not store energy.

    TODO: the same, with any number of pipes?
    TODO: the same with an acoustic mass?

    Only PH1 convention supported yet.
    """

    def __init__(self, simplejunction, pipe_ends, **kwargs):
        """
        Parameters
        ----------
        dt : float
            time step increment
        pipe_end_1 , pipe_end_2: TemporalPipe.End
            the pipe ends to connect
        """
        super().__init__(simplejunction, **kwargs)
        self.pipe_end_1, self.pipe_end_2 = pipe_ends

    def set_dt(self, dt):
        self.dt = dt
        self._should_recompute_coefficients = True

    def reset_variables(self):
        # Nothing to do!
        pass

    def _precompute_coefficients(self):
        alpha_1 = self.pipe_end_1.get_alpha()
        alpha_2 = self.pipe_end_2.get_alpha()
        self._dp_to_flow = 1/(alpha_1 + alpha_2)

        self._should_recompute_coefficients = False


    def one_step(self):
        if self._should_recompute_coefficients:
            self._precompute_coefficients()

        # p_corr_1 + dt/(2 m_end_1) * lambda = p_corr_2 - dt/(2 m_end_2) * lambda
        p_corr_1 = self.pipe_end_1.get_p_no_flow()
        p_corr_2 = self.pipe_end_2.get_p_no_flow()
        flow = self._dp_to_flow * (p_corr_2 - p_corr_1)

        self.pipe_end_1.update_flow(-flow)
        self.pipe_end_2.update_flow(flow)

    def __str__(self):
        return 'TSimpleJunction({},{})'.format(self.pipe_end_1, self.pipe_end_2)

    def __repr__(self):
        return self.__str__()

    def energy(self):
        return 0

    def dissipated_last_step(self):
        return 0

    def get_maximal_dt(self):
        return np.infty
