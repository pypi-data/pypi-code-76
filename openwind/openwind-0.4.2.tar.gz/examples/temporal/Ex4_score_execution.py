#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a score, modify it and run temporal simulations on a cylindrical 
instrument. Low level classes are used. 
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

import numpy as np
import matplotlib.pyplot as plt

from openwind.technical import InstrumentGeometry, Score, Player
from openwind.continuous import InstrumentPhysics
from openwind.temporal import TemporalSolver
from openwind.temporal import ExecuteScore, RecordingDevice



# a simple instrument with one hole ...
geom = [[0, 0.5, 2e-3, 10e-3, 'linear']]
hole = [['label', 'position', 'radius', 'chimney'],
        ['hole1', .25, 3e-3, 5e-3]]

# ... and 2 fingerings
fingerings = [['label', 'note1', 'note2'],
              ['hole1', 'o', 'x']]

instrument = InstrumentGeometry(geom, hole, fingerings)
# the default player is a impulse flow
player = Player('CLARINET')
instrument_physics = InstrumentPhysics(instrument, 20, player, False)
temporalsolver = TemporalSolver(instrument_physics, l_ele=0.01,
                                   order=4)
# %% low level instanciation
# ExecuteScore makes the link between a score (list of notes) and 
# and instrument and its fingering
score_execution = ExecuteScore(instrument.fingering_chart,
                               temporalsolver.t_components)
no_note_events = []
# Set a score based on this empty list of notes
no_note_score = Score(no_note_events)
# set_score allows to modify the score with a series of notes
score_execution.set_score(no_note_score)
# set_fingering takes a time t (here 10) and sets the correct fingering 
# according to the given notes series
score_execution.set_fingering(10)

# a list of notes and their time of beginning
note_events = [('note1', .02), ('note2', .03), ('note1', .04)]
# the second parameter is the transition duration between notes (here 1e-3)
with_note_score = Score(note_events, 1e-3)
# display the score along time 
time = np.linspace(0,0.1,1000)
with_note_score.plot_score(time)
# change the score of the score_execution instance 
score_execution.set_score(with_note_score)
score_execution.set_fingering(1.5)

# %% Run simulation!
# the player is updated with the empty score no_note_events
player.update_score(no_note_events)
# run a temporal simulation with a duration (here .1)
temporalsolver.run_simulation(.1)

#%% Run simulation and record output signals 
# the player is updated with the new score note_events
player.update_score(note_events, 1e-3)
player.plot_controls(time)
# the output will be stored in a Recording device
rec = RecordingDevice(record_energy=False)
# run the simulation with a duration (here .1) and a callback class
temporalsolver.run_simulation(.1, callback=rec.callback)
rec.stop_recording()
# plot the output value of pressure at the bell
output_bell = rec.values['bell_radiation_pressure']
plt.figure()
plt.plot(output_bell)
# %% an error message when the asked notes are not in the fingering chart
strange_note = [('Do', .02), ('Re', .03), ('E', .04)]
player.update_score(strange_note, 1e-3)
temporalsolver.run_simulation(.1)
