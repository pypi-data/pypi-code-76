# Copyright (c) 2020-2021, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of the Optimyzer Client, which is released under the BSD 3-Clause License.

"""
Optimyzer -- a hyperparameter optimization framework that fits into every workflow
"""
# Optimyzer uses semantic versioning according to PEP-0440:
# https://www.python.org/dev/peps/pep-0440/
__version__ = "0.2.0"


# automatically import the modules
from . import external, filesystem, optimyzer, parameterspace

# convenience imports
from .optimyzer import (
    Configuration,
    Optimyzer,
    get_instance_config,
    get_optimal_config,
    list_best_configurations,
)
from .parameterspace import CategoricalParameter, FloatParameter, IntParameter
