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
This module convert the instrument in a netlist (graph) of pipes, whose
ends are connected to different conditions (radiations, junctions, etc).
Each netlist element can compute the coefficients of the corresponding physical
equation (wave propagation, losses, etc).
"""

# === Things Used Everywhere ===

from .physics import Physics
from .scaling import Scaling

# - Boundary condition (for temporal) -
# TODO maybe move this ?
# from .flow_model import (dirac_flow, chirp_flow)


# === All the Models ===

from .netlist_component import (NetlistComponent)

# - Reed -
from .reed_model import ReedModel

# - Losses -
from .thermoviscous_models import (ThermoviscousModel,
                                   ThermoviscousLossless,
                                   ThermoviscousBessel,
                                   ThermoviscousDiffusiveRepresentation,
                                   WebsterLokshin,
                                   Keefe,
                                   MiniKeefe,
                                   losses_model)

# - Propagation in Pipes -
from .pipe import Pipe

# - Radiation Impedances -
from .radiation_model import (RadiationModel, radiation_pade, RadiationPade,
                              RadiationPerfectlyOpen, RadiationPade2ndOrder)
from .radiation_from_data import RadiationFromData, radiation_from_data
from .radiation_pulsating_sphere import RadiationPulsatingSphere
from .physical_radiation import PhysicalRadiation, radiation_model

# - Junctions of Pipes -
from .junction import (PhysicalJunction,
                       JunctionTjoint,
                       JunctionSimple,
                       JunctionDiscontinuity)

# - Excitators -
from .excitator import (Excitator, Flow, Flue, Valve)

# === Graph Representation of the Instrument ===

from .netlist import Netlist, EndPos
from .instrument_physics import InstrumentPhysics
