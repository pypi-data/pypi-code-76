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
Container which holds all of a project's pipelines.
"""

from getml.utilities.formatter import Formatter

from .helpers2 import _refresh_all, list_pipelines
from .scores import accuracy, auc, cross_entropy, mae, rmse, rsquared

# --------------------------------------------------------------------


class Pipelines:
    """
    Container which holds all pipelines associated with the currently running
    project. The container supports slicing and is sort- and filterable.

        Example:

            Show the first 10 pipelines belonging to the current project:

            .. code-block:: python

                getml.project.pipelines[:10]

            You can use nested list comprehensions to retrieve a scoring history
            for your project:

            .. code-block:: python

                import matplotlib.pyplot as plt

                hyperopt_scores = [(score.date_time, score.mae) for pipe in getml.project.pipelines
                                      for score in pipe.scores["data_test"]
                                      if "hyperopt" in pipe.tags]

                fig, ax = plt.subplots()
                ax.bar(*zip(*hyperopt_scores))
    """

    # ----------------------------------------------------------------

    def __init__(self, data=None):
        self.ids = list_pipelines()

        if data is None:
            self.data = _refresh_all()
        else:
            self.data = data

    # ----------------------------------------------------------------

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        if isinstance(key, slice):
            pipelines_subset = self.data[key]
            return Pipelines(data=pipelines_subset)
        if isinstance(key, str):
            if key in self.ids:
                return [pipeline for pipeline in self.data if pipeline.id == key][0]
            raise AttributeError(f"No Pipeline with id: {key}")
        raise TypeError(
            f"Pipelines can only be indexed by: int, slices, or str, not {type(key).__name__}"
        )

    # ----------------------------------------------------------------

    def __len__(self):
        return len(self.data)

    # ----------------------------------------------------------------

    def __repr__(self):
        if len(self.ids) == 0:
            return "No pipelines in memory."

        return self._format().render_string()

    # ----------------------------------------------------------------

    def _repr_html_(self):
        if len(self.ids) == 0:
            return "<p>No pipelines in memory.</p>"
        return self._format().render_html()

    # ----------------------------------------------------------------

    @property
    def _contains_regresion_pipelines(self):
        return any(pipe.is_regression for pipe in self.data)

    # ----------------------------------------------------------------

    @property
    def _contains_classification_pipelines(self):
        return any(pipe.is_classification for pipe in self.data)

    # ----------------------------------------------------------------

    def _format(self):

        scores = []
        scores_headers = []

        # ------------------------------------------------------------

        if self._contains_classification_pipelines:
            scores.extend(
                [
                    [
                        pipeline._scores.get(accuracy, []),
                        pipeline._scores.get(auc, []),
                        pipeline._scores.get(cross_entropy, []),
                    ]
                    for pipeline in self.data
                ]
            )

            scores_headers.extend([accuracy, auc, cross_entropy])

        # ------------------------------------------------------------

        if self._contains_regresion_pipelines:
            scores.extend(
                [
                    [
                        pipeline._scores.get(mae, []),
                        pipeline._scores.get(rmse, []),
                        pipeline._scores.get(rsquared, []),
                    ]
                    for pipeline in self.data
                ]
            )

            scores_headers.extend([mae, rmse, rsquared])

        # ------------------------------------------------------------

        sets_used = [pipeline._scores.get("set_used", "") for pipeline in self.data]

        targets = [pipeline.targets for pipeline in self.data]

        feature_learners = [
            [feature_learner.type for feature_learner in pipeline.feature_learners]
            for pipeline in self.data
        ]

        tags = [pipeline.tags for pipeline in self.data]

        headers = [
            [
                "",
                "id",
                "tags",
                "feature learners",
                "targets",
                *scores_headers,
                "set used",
            ]
        ]

        rows = [
            [
                str(index),
                pipeline.id,
                tags[index],
                feature_learners[index],
                targets[index],
                *scores[index],
                sets_used[index],
            ]
            for index, pipeline in enumerate(self.data)
        ]

        # ------------------------------------------------------------

        return Formatter(headers, rows)

    # ----------------------------------------------------------------

    def sort(self, key, descending=False):
        """
        Sorts the pipelines container.

        Args:
            key (callable, optional):
                A callable that evaluates to a sort key for a given item.
            descending (bool, optional):
                Whether to sort in descending order.

        Returns:
            :class:`getml.pipeline.Pipelines`:
                A container of sorted pipelines.

        Example:
            .. code-block:: python

                by_auc = getml.project.pipelines.sort(key=lambda pipe: pipe.auc)

                by_fl = getml.project.pipelines.sort(key=lambda pipe: pipe.feature_learners[0].type)

        """
        pipelines_sorted = sorted(self.data, key=key, reverse=descending)
        return Pipelines(data=pipelines_sorted)

    # ----------------------------------------------------------------

    def filter(self, conditional):
        """
        Filters the pipelines container.

        Args:
            conditional (callable):
                A callable that evaluates to a boolean for a given item.

        Returns:
            :class:`getml.pipeline.Pipeline`:
                A container of filtered pipelines.

        Example:
            .. code-block:: python

                pipes_with_tags = getml.project.pipelines.filter(lambda pipe: len(pipe.tags) > 0)

                accurate_pipes = getml.project.pipelines.filter(lambda pipe: all(acc > 0.9 for acc in pipe.accuracy))

        """
        pipelines_filtered = [
            pipeline for pipeline in self.data if conditional(pipeline)
        ]

        return Pipelines(data=pipelines_filtered)
