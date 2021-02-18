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


"""
Numerical schemes used for time-domain simulation.
"""

# ====== Temporal Components ======
from .tcomponent import TemporalComponent, TemporalComponentExit

# - Pipes -
from .tpipe import TemporalPipe
from .tpipe_lossy import TemporalLossyPipe

# - One-end components -
from .tflow_condition import TemporalFlowCondition
from .tpressure_condition import TemporalPressureCondition
from .tradiation import TemporalRadiation
from .tvalve import TemporalValve

# - Junctions -
from .tjunction import TemporalJunction
from .tsimplejunction import TemporalSimpleJunction


# ====== Managing the Simulation ======
# - the fingerings
from .execute_score import ExecuteScore

# - Running the simulation -
from .temporal_solver import TemporalSolver

# - Recording data -
from .recording_device import RecordingDevice
