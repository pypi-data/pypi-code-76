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

"""Contains handlers for all steps involved in a data science project after
data preparation:

* automated feature learning
* automated feature selection
* training and evaluation of machine learning (ML) algorithms
* deployment of the fitted models

Example:

    We assume that you have already set up your
    data model using :class:`~getml.data.Placeholder`,
    your feature learners (refer to :mod:`~getml.feature_learning`)
    as well as your feature selectors and predictors
    (refer to :mod:`~getml.predictors`, which can be used
    for prediction and feature selection).

    .. code-block:: python

        pipe = getml.pipeline.Pipeline(
            tags=["multirel", "relboost", "31 features"],
            population=population_placeholder,
            peripheral=[order_placeholder, trans_placeholder],
            feature_learners=[feature_learner_1, feature_learner_2],
            feature_selectors=feature_selector,
            predictors=predictor,
            share_selected_features=0.5
        )

        # "order" and "trans" refer to the names of the
        # placeholders.
        pipe.check(
            population_table=population_training,
            peripheral_tables={"order": order, "trans": trans}
        )

        pipe.fit(
            population_table=population_training,
            peripheral_tables={"order": order, "trans": trans}
        )

        pipe.score(
            population_table=population_testing,
            peripheral_tables={"order": order, "trans": trans}
        )

"""

from . import scores
from .columns import Columns
from .features import Features
from .helpers2 import delete, exists, list_pipelines, load
from .metrics import Metrics
from .pipeline import Pipeline
from .pipelines import Pipelines
from .scores_container import Scores
from .sql_code import SQLCode

__all__ = (
    "delete",
    "exists",
    "list_pipelines",
    "load",
    "Columns",
    "Features",
    "Metrics",
    "Pipeline",
    "Pipelines",
    "Scores",
    "SQLCode",
)
