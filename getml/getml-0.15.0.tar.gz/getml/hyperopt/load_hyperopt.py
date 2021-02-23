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

"""Loads a hyperparameter optimization object from the getML engine into Python."""

from getml.data import Placeholder
from getml.pipeline import Pipeline
from getml.predictors import LinearRegression

from .hyperopt import (
    GaussianHyperparameterSearch,
    LatinHypercubeSearch,
    RandomSearch,
    _get_json_obj,
)


def load_hyperopt(name):
    """Loads a hyperparameter optimization object from the getML engine into Python.

    Args:
        name: The name of the hyperopt to be loaded.

    Returns:
        A `~getml.hyperopt.GaussianHyperparameterSearch` that is a handler
        for the pipeline signified by name.
    """
    # This will be overwritten by .refresh(...) anyway
    dummy = Placeholder(name="dummy")
    dummy2 = Placeholder(name="dummy2")
    dummy.join(dummy2, join_key="join_key")

    dummy_pipeline = Pipeline(
        population=dummy, peripheral=dummy2, predictors=[LinearRegression()]
    )

    dummy_param_space = {"predictors": [{"reg_lambda": [0.0, 1.0]}]}

    json_obj = _get_json_obj(name)

    if json_obj["type_"] == "GaussianHyperparameterSearch":
        return GaussianHyperparameterSearch(
            param_space=dummy_param_space, pipeline=dummy_pipeline
        )._parse_json_obj(json_obj)

    if json_obj["type_"] == "LatinHypercubeSearch":
        return LatinHypercubeSearch(
            param_space=dummy_param_space, pipeline=dummy_pipeline
        )._parse_json_obj(json_obj)

    if json_obj["type_"] == "RandomSearch":
        return RandomSearch(
            param_space=dummy_param_space, pipeline=dummy_pipeline
        )._parse_json_obj(json_obj)

    raise ValueError("Unknown type: '" + json_obj["type_"] + "'!")
