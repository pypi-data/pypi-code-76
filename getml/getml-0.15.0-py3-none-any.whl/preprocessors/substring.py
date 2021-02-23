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


class Substring(_Preprocessor):
    """
    Substring extracts substrings from categorical columns
    and unused string columns.

    The preprocessor automatically iterates through
    all categorical columns and unused string columns
    in any data frame. The substring operator is then
    applied to any such column for which the
    unit matches `unit`.

    .. code-block:: python

        substr13 = getml.preprocessors.Substring(0, 3, "UCC")

        pipe = getml.pipeline.Pipeline(
            population=population_placeholder,
            peripheral=[order_placeholder, trans_placeholder],
            preprocessors=[substr13],
            feature_learners=[feature_learner_1, feature_learner_2],
            feature_selectors=feature_selector,
            predictors=predictor,
            share_selected_features=0.5
        )

    Args:
        begin (int): Index of the beginning of the substring (starting from 0).

        length (int): The length of the substring.

        unit (str): The unit of all columns to which the proprocessor
            should be applied.
    """

    def __init__(self, begin, length, unit):
        if not isinstance(begin, int):
            raise TypeError("'begin' must be an integer!")

        if not isinstance(length, int):
            raise TypeError("'length' must be an integer!")

        if not isinstance(unit, str):
            raise TypeError("'unit' must be a string!")

        if begin < 0:
            raise ValueError("'begin' must be >= 0!")

        if length <= 0:
            raise ValueError("'length' must be > 0!")

        if not unit:
            raise ValueError("'unit' cannot be empty!")

        super().__init__()
        self.type = "Substring"
        self.begin = begin
        self.length = length
        self.unit = unit
