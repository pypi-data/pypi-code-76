# -*- coding: utf-8 -*-
from .nnmeta import NNClass

from setuptools import setup, find_packages

__all__ = (
    '__version__',
    'NNClass'
)

import pkg_resources
__version__           = pkg_resources.get_distribution("nnmeta").version

__short_description__ = "NN class for any purpose based on schnetpack."
__license__           = "MIT"
__author__            = "Alexander D. Kazakov"
__author_email__      = "alexander.d.kazakov@gmail.com"
__github_username__   = "AlexanderDKazakov"
