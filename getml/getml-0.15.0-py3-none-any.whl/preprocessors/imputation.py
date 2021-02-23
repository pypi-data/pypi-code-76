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
Contains routines for preprocessing data frames.
"""

from .preprocessor import _Preprocessor


class Imputation(_Preprocessor):
    """
    Imputation replaces all NULL values in
    numerical columns with the mean of the remaining
    columns.

    Optionally, it can additionally add a dummy column
    that signifies whether the original value was imputed.

    .. code-block:: python

        imputation = getml.preprocessors.Imputation()

        pipe = getml.pipeline.Pipeline(
            population=population_placeholder,
            peripheral=[order_placeholder, trans_placeholder],
            preprocessors=[imputation],
            feature_learners=[feature_learner_1, feature_learner_2],
            feature_selectors=feature_selector,
            predictors=predictor,
            share_selected_features=0.5
        )

    Args:
        add_dummies (bool): Whether you want to add dummy variables
            that signify whether the original value was imputed..

    """

    def __init__(self, add_dummies=False):
        if not isinstance(add_dummies, bool):
            raise TypeError("'add_dummies' must be a boolean!")

        super().__init__()
        self.type = "Imputation"
        self.add_dummies = add_dummies
