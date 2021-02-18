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
Defines openwind object used to design the bore profile. The radius evolution
of each tube is described by a design shape parametrize by several design
parameters.
"""


from .design_parameter import (DesignParameter,
                               FixedParameter,
                               VariableParameter,
                               VariableParameterSquare,
                               VariableParameterLimitedRange,
                               VariableHolePosition,
                               VariableHoleRadius,
                               OptimizationParameters,
                               eval_, diff_)

# === Design Shapes ===
from .design_shape import DesignShape

# - Basic shape formulas
from .bessel import Bessel
from .circle import Circle
from .cone import Cone
from .exponential import Exponential
from .spline import Spline

# - Shape defined using another shape
from .shape_slice import ShapeSlice
