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
This module treats all the aspects of the computation in frequential domain.
It converts the netlist component in frequential components, build and solves
the global linear equation.
"""
# === Frequential Components ===
from .frequential_component import FrequentialComponent

# - Pipes -
from .frequential_pipe_fem import FrequentialPipeFEM
from .frequential_pipe_diffusive_representation import FrequentialPipeDiffusiveRepresentation
from .frequential_pipe_tmm import FrequentialPipeTMM

# - One-end components -
from .frequential_radiation import FrequentialRadiation
from .frequential_source import FrequentialSource

# - Junctions -
from .frequential_junction_tjoint import FrequentialJunctionTjoint
from .frequential_junction_simple import FrequentialJunctionSimple
from .frequential_junction_discontinuity import FrequentialJunctionDiscontinuity


# === Solving and after ===
from .frequential_interpolation import FrequentialInterpolation
from .frequential_solver import FrequentialSolver
