"""A package for cloudFPGA quantitative finance lib."""

__version__ = '0.2'

import sys
import numpy as np

trieres_lib="./build"
sys.path.append(trieres_lib)

import _trieres
