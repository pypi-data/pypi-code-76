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


"""Temporal version of a flow constraint."""
import numpy as np

from openwind.temporal import TemporalComponentExit
from openwind.continuous import Flow


class TemporalFlowCondition(TemporalComponentExit):
    """Constrain the value of the flow V at the end of the pipe.

    This boundary condition may be used for closed pipes, but
    its main purpose is for simulating the response of an instrument to an
    impulse, a chirp tone, or any such input signal.

    Only PH1 convention is supported for now.
    """

    def __init__(self, flow, pipe_ends, t_solver):
        """
        Parameters
        ----------
        flow : float or openwind.continuous.Flow
            If float, the constant value of the flow.
            If Flow, flow.get_value(t) should be the value of the flow at time t
        pipe_end : TemporalPipe.End
            The PipeEnd on which this condition applies
        dt : float
            Time step increment
        t_0 : float
            initial time
        """
        super().__init__(flow, t_solver)
        self._pipe_end, = pipe_ends
        self._flow = flow  # Continuous model
        self._input_flow = flow.input_flow

    def one_step(self):
        flow_value = self._input_flow.get_value(self.get_current_time())
        self._pipe_end.update_flow(flow_value)
        super().remember_flow_and_pressure(self._pipe_end)

    def set_dt(self, dt):
        pass # nothing to do

    def get_maximal_dt(self):
        return np.infty # no CFL

    def reset_variables(self):
        pass # nothing to do

    def energy(self):
        """As a TemporalFlowCondition does not store energy, return zero.

        It may be a source of energy into the system, but the
        amount cannot be known in advance."""
        return 0

    def dissipated_last_step(self):
        """A nonzero flow condition is an external source of energy.
        It does not count as dissipation.

        However let us use this method abusively to also represent
        a source term."""
        return self.get_exit_flow() * self.get_exit_pressure() * self._t_solver.get_dt()

    def __str__(self):
        return "TFlow({}, {})".format(str(self._flow), str(self._pipe_end))
    def __repr__(self):
        return self.__str__()

