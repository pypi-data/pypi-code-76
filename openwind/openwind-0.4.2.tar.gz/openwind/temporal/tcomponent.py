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


from abc import ABC, abstractmethod
import numpy as np

class TemporalComponent(ABC):
    """Abstract class representing a component of an instrument in a temporal simulation."""

    def __init__(self, component, t_solver):
        self.label = component.label
        self._t_solver = t_solver

    def get_current_time(self):
        return self._t_solver.get_current_time()

    @abstractmethod
    def one_step(self):
        """Advance one time step."""

    @abstractmethod
    def reset_variables(self):
        """Reinitialize all variables to start the simulation over.

        Implementing classes should ensure that after a call to this method,
        the object behaves like a fresh instance
        with with same __init__ parameters.
        """

    @abstractmethod
    def energy(self):
        """Compute amount of energy currently stored in element."""

    @abstractmethod
    def dissipated_last_step(self):
        """Amount of energy dissipated by this component during the last time step."""

    @abstractmethod
    def get_maximal_dt(self):
        """Get the largest time step allowed by CFL condition."""
        return np.infty

    @abstractmethod
    def set_dt(self):
        """Set the time step of the component."""

    def get_values_to_record(self):
        """Extract the current value of data that we want to record.

        Returns
        -------
        values : Dict[str, float]
            The names and values of the data.
        """
        return {}



class TemporalComponentExit(TemporalComponent):
    """An exit is a point where we can record one pressure and one flow.

    A TemporalComponent which connects to a single pipe will
    usually be an exit, but it may connect to several
    (e.g. a possible future component "tonehole", including junction,
    chimney and radiation, would connect to two pipes, but we can
    measure the pressure/flow at the end of the chimney).


    16/01/2020: I think this method of recording is hacky and bad,
    because it entails bad object-oriented programming and shotgun surgery.
    If all we want is the flow and pressure at some PipeEnds,
    we should probably rather mark the PipeEnds that we want to record.
    -- Alexis
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_flow = None
        self._last_pressure = None
        self._last_y = None

    def remember_flow_and_pressure(self, pipe_end):
        self._last_flow = pipe_end.get_w_nph()
        self._last_pressure = pipe_end.get_q_nph()

    def remember_y(self, y):
        self._last_y = y

    def get_exit_flow(self):
        """Measure flow w^{n+1/2} at this exit."""
        assert self._last_flow is not None
        return self._last_flow

    def get_exit_pressure(self):
        """Measure pressure q^{n+1/2} at this exit."""
        assert self._last_pressure is not None
        return self._last_pressure

    def get_values_to_record(self):
        assert self._last_pressure is not None
        return {'pressure': self._last_pressure,
                'flow': self._last_flow,
                'y': self._last_y}
