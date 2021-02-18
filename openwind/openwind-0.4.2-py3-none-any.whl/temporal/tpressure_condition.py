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


"""Temporal version of a pressure constraint."""
import numpy as np

from openwind.temporal import TemporalComponentExit


class TemporalPressureCondition(TemporalComponentExit):
    """Constrain the value of the pressure P to zero at the end of the pipe."""

    def __init__(self, source, pipe_ends, t_solver):
        super().__init__(source, t_solver)
        self._pipe_end, = pipe_ends

    def one_step(self):
        p_no_flow = self._pipe_end.get_p_no_flow()
        alpha =  self._pipe_end.get_alpha()
        # p^{n+1/2} = p_no_flow - alpha * w must be zero
        w = p_no_flow/alpha
        self._pipe_end.update_flow(w)
        super().remember_flow_and_pressure(self._pipe_end)

    def set_dt(self, dt):
        pass # nothing to do
    def get_maximal_dt(self):
        return np.infty # no CFL
    def reset_variables(self):
        pass # nothing to do
    def energy(self):
        return 0
    def dissipated_last_step(self):
        return 0
    def __repr__(self):
        return "TPressure(0, {})".format(str(self._pipe_end))
