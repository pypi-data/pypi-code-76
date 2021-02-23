# -*- coding: utf-8 -*-
"""Sensor Independent  Atmospheric CORrection (SICOR)"""

import os
from .version import __version__
from .sicor_ac import ac, ac_gms
from .sicor_enmap import sicor_ac_enmap
from .options.options import get_options

if 'MPLBACKEND' not in os.environ:
    os.environ['MPLBACKEND'] = 'Agg'

__authors__ = """Niklas Bohn, André Hollstein, René Preusker"""
__email__ = 'nbohn@gfz-potsdam.de'
__all__ = ["__version__", "ac", "ac_gms", "sicor_ac_enmap", "get_options"]
