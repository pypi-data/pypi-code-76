# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
"""
getML (https://getml.com) is a software for automated machine learning
(AutoML) with a special focus on feature learning for relational data
and time series. The getML algorithms can produce features that are far
more advanced than what any data scientist could write by hand or what you
could accomplish using simple brute force approaches.

This is the official python client for the getML engine.

Documentation and more details at https://docs.getml.com
"""

from . import (
    communication,
    constants,
    data,
    database,
    datasets,
    engine,
    feature_learning,
    helpers,
    hyperopt,
    pipeline,
    predictors,
    preprocessors,
    project,
)
from .version import __version__

# Import subpackages into top-level namespace


__all__ = (
    "communication",
    "constants",
    "data",
    "database",
    "datasets",
    "engine",
    "feature_learning",
    "hyperopt",
    "pipeline",
    "predictors",
    "preprocessors",
    "project",
)
