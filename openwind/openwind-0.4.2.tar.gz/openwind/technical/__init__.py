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
Read and transcript the data from user format to openwind data.
"""


from .fingering_chart import FingeringChart, Fingering
from .instrument_geometry import InstrumentGeometry
from .score import Score
from .adjust_instrument_geometry import AdjustInstrumentGeometry
from .player import Player
