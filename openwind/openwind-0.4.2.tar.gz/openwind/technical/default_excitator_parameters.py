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
from openwind.technical.temporal_curves import constant_with_initial_ramp, dirac_flow, triangle



REED = {
    "excitator_type" : "Valve",
    "opening" : 1e-4,
    "mass" : 3.376e-6,
    "section" : 14.6e-5,
    "pulsation" : 2*np.pi*3700,
    "dissip" : 3000,
    "width" : 3e-2,
    "mouth_pressure" : constant_with_initial_ramp(2000, 2e-2),
    "model" : "reed",
        #  valeurs de Bilbao 2008
    "contact_pulsation": 316,
    "contact_exponent": 4
}

# from Fréour et al, JASA 2020
LIPS = {
    "excitator_type" : "Valve",
    "opening" : 1e-4,
    "mass" : 8e-5,
    "section" : 4e-5,
    "pulsation" : 2*np.pi*382,
    "dissip" : 0.3*2*np.pi*382,
    "width" : 8e-3,
    "mouth_pressure" : constant_with_initial_ramp(5500, 1e-2),#triangle(3200, .5),
    "model" : "lips",
    "contact_pulsation": 0*316,
    "contact_exponent": 4
}

# These parameters are only used by the basic tutorial
# but they do not correspond to anything physical
TUTORIAL_LIPS = {
    "excitator_type" : "Valve",
    "opening" : 9.4e-4,
    "mass" : 6.4e-5,
    "section" : 1.9e-4,
    "pulsation" : 2*np.pi*750,
    "dissip" : 0.7*2*np.pi*750,
    "width" : 11.9e-3,
    "mouth_pressure" : constant_with_initial_ramp(5000, 1e-2),
    "model" : "lips",
    "contact_pulsation": 0,
    "contact_exponent": 4
}

TUTORIAL_REED = {
    "excitator_type" : "Valve",
    "opening" : 9.4e-4,
    "mass" : 6.4e-5,
    "section" : 1.9e-4,
    "pulsation" : 2*np.pi*750,
    "dissip" : 0.7*2*np.pi*750,
    "width" : 11.9e-3,
    "mouth_pressure" : constant_with_initial_ramp(5000, 1e-2),
    "model" : "reed",
    "contact_pulsation": 0,
    "contact_exponent": 4
}

OBOE = {
    "excitator_type" : "Valve",
    "opening" : 8.9e-5,
    "mass" : 7.1e-4,
    "section" : 4.5e-5,
    "pulsation" : 2*np.pi*600,
    "dissip" : 0.4*2*np.pi*600,
    "width" : 9e-3,
    "mouth_pressure" : constant_with_initial_ramp(12000, 2e-2),
    "model" : "reed",
    "contact_pulsation": 316,
    "contact_exponent": 4
}

# values of Bilbao 2008
CLARINET = {
    "excitator_type" : "Valve",
    "opening" : 4e-4,
    "mass" : 3.376e-6,
    "section" : 14.6e-5,
    "pulsation" : 2*np.pi*3700,
    "dissip" : 3000,
    "width" : 3e-2,
    "mouth_pressure" : constant_with_initial_ramp(2000, 2e-2),
    "model" : "reed",
    "contact_pulsation": 316,
    "contact_exponent": 4
}


UNITARY_FLOW = {
    "excitator_type":"Flow",
    "input_flow":1
}

ZERO_FLOW = {
    "excitator_type":"Flow",
    "input_flow":0
}

IMPULSE_400us = {
    "excitator_type":"Flow",
    "input_flow": dirac_flow(4e-4)
}

IMPULSE_100us = {
    "excitator_type":"Flow",
    "input_flow": dirac_flow(1e-4)
}
