#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""How to simulate a simplified clarinet in time domain.

The simplified clarinet is a cylinder with a hole.
This example demonstrates the use of a Valve-based Player.

See also
--------
openwind.continuous.excitator
openwind.technical.player
openwind.temporal.simulate
"""
__author__ = ("Juliette Chabassier, Augustin Ernoult, Olivier Geber,"
              " Alexis Thibault, Tobias Van Baarsel")
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"


from openwind import simulate
from openwind.technical.player import Player
from openwind.temporal.utils import export_mono

# 50cm cylinder
instrument = [[0.0, 5e-3],
              [0.5, 5e-3]]
# One small hole positioned at 45cm
# 1cm long, 2mm of radius, open by default.
holes = [['x', 'l', 'r', 'label'],
         [0.45, 0.01, 2e-3, 'hole1']]

player = Player('CLARINET')
# Parameters of the reed can be changed manually
# Available parameters are:
# "opening", "mass","section","pulsation","dissip","width",
# "mouth_pressure","model","contact_pulsation","contact_exponent"
player.update_curve("width", 2e-2)


duration = 0.2  # simulation time in seconds
rec = simulate(duration,
               instrument,
               holes,
               player = player,
               losses='diffrepr',
               temperature=20,
               l_ele=0.01, order=4 # Discretization parameters
               )
# show the discretization infos
rec.t_solver.discretization_infos()

signal = rec.values['bell_radiation_pressure']
export_mono('Ex2_cylinder_reed.wav', signal, rec.ts)
