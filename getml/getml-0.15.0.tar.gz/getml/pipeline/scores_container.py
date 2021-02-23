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
A container for storing a pipeline's scoring history.
"""

from getml.utilities.formatter import Formatter

from .helpers import _unlist_maybe
from .score import ClassificationScore
from .scores import _all_scores, accuracy, auc, cross_entropy, mae, rmse, rsquared


class Scores:
    """
    Container which holds the history of all scores associated with a given pipeline.
    The container supports slicing and is sort- and filterable.
    """

    # ----------------------------------------------------------------

    def __init__(self, data, latest):
        self._latest = latest

        self.is_classification = all(
            isinstance(score, ClassificationScore) for score in data
        )

        self.is_regression = not self.is_classification

        self.data = data

        self.sets_used = [score.set_used for score in data]

    # ----------------------------------------------------------------

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]

        if isinstance(key, slice):
            scores_subset = self.data[key]
            return Scores(scores_subset, self._latest)

        if isinstance(key, str):
            # allow to access latest scores via their name for backward compatiblilty
            if key in _all_scores:
                return self._latest[key]

            scores_subset = [score for score in self.data if score.set_used == key]

            return Scores(scores_subset, self._latest)

        raise TypeError(
            f"Scores can only be indexed by: int, slices, or str, not {type(key).__name__}"
        )

    # ----------------------------------------------------------------

    def __len__(self):
        return len(self.data)

    # ------------------------------------------------------------

    def __repr__(self):
        return self._format().render_string()

    # ------------------------------------------------------------

    def _repr_html_(self):
        return self._format().render_html()

    # ------------------------------------------------------------

    def _format(self):
        headers = ["", "date time", "set used", "target"]
        if self.is_classification:
            headers += ["accuracy", "auc", "cross entropy"]
        if self.is_regression:
            headers += ["mae", "rmse", "rsquared"]

        rows = [
            [index] + list(vars(score).values())
            for index, score in enumerate(self.data)
        ]

        return Formatter([headers], rows)

    # ----------------------------------------------------------------

    @property
    def accuracy(self):
        """
        A convenience wrapper to retrieve the `accuracy` from the latest scoring run.
        """
        return _unlist_maybe(self._latest[accuracy])

    # ----------------------------------------------------------------

    @property
    def auc(self):
        """
        A convenience wrapper to retrieve the `auc` from the latest scoring run.
        """
        return _unlist_maybe(self._latest[auc])

    # ----------------------------------------------------------------

    @property
    def cross_entropy(self):
        """
        A convenience wrapper to retrieve the `cross entropy` from the latest scoring run.
        """
        return _unlist_maybe(self._latest[cross_entropy])

    # ----------------------------------------------------------------

    def filter(self, conditional):
        """
        Filters the scores container.

        Args:
            conditional (callable):
                A callable that evaluates to a boolean for a given item.

        Returns:
            :class:`getml.pipeline.Scores`:
                A container of filtered scores.

        Example:
            .. code-block:: python

                from datetime import datetime, timedelta

                one_week_ago = datetime.today() - timedelta(days=7)

                scores_last_week = pipe.scores.filter(lambda score: score.date_time >= one_week_ago)

        """
        scores_filtered = [score for score in self.data if conditional(score)]

        return Scores(scores_filtered, self._latest)

    # ----------------------------------------------------------------

    @property
    def mae(self):
        """
        A convenience wrapper to retrieve the `mae` from the latest scoring run.
        """
        return _unlist_maybe(self._latest[mae])

    # ----------------------------------------------------------------

    @property
    def rmse(self):
        """
        A convenience wrapper to retrieve the `rmse` from the latest scoring run.
        """
        return _unlist_maybe(self._latest[rmse])

    # ----------------------------------------------------------------

    @property
    def rsquared(self):
        """
        A convenience wrapper to retrieve the `rsquared` from the latest scoring run.
        """
        return _unlist_maybe(self._latest[rsquared])

    # ----------------------------------------------------------------

    def sort(self, key, descending=False):
        """
        Sorts the scores container.

        Args:
            key (callable, optional):
                A callable that evaluates to a sort key for a given item.
            descending (bool, optional):
                Whether to sort in descending order.

        Return:
            :class:`getml.pipeline.Scores`:
                A container of sorted scores.

        Example:
            .. code-block:: python

                by_auc = pipe.scores.sort(key=lambda score: score.auc)

                most_recent_first = pipe.scores.sort(key=lambda score: score.date_time, descending=True)
        """

        scores_sorted = sorted(self.data, key=key, reverse=descending)
        return Scores(scores_sorted, self._latest)
