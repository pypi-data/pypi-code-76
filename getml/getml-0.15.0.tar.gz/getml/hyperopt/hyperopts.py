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
Container which holds a project's hyperopts.
"""

from getml.utilities.formatter import Formatter

from .helpers import list_hyperopts
from .load_hyperopt import load_hyperopt

# --------------------------------------------------------------------


class Hyperopts:
    """
    Container which holds all hyperopts associated with the currently running
    project. The container supports slicing and is sort- and filterable.
    """

    # ----------------------------------------------------------------

    def __init__(self, data=None):
        self.ids = list_hyperopts()

        if data is None:
            self.data = [load_hyperopt(id) for id in self.ids]
        else:
            self.data = data

    # ----------------------------------------------------------------

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        if isinstance(key, slice):
            hyperopts_subset = self.data[key]
            return Hyperopts(data=hyperopts_subset)
        if isinstance(key, str):
            if key in self.ids:
                return [hyperopt for hyperopt in self.data if hyperopt.name == key][0]
            raise AttributeError(f"No Hyperopt with id: {key}")
        raise TypeError(
            f"Hyperopts can only be indexed by: int, slices, or str, not {type(key).__name__}"
        )

    # ----------------------------------------------------------------

    def __len__(self):
        return len(self.data)

    # ----------------------------------------------------------------

    def __repr__(self):
        if len(list_hyperopts()) == 0:
            return "No hyperopt in memory."

        return self._format().render_string()

    # ----------------------------------------------------------------

    def _repr_html_(self):
        if len(list_hyperopts()) == 0:
            return "<p>No hyperopt in memory.</p>"

        return self._format().render_html()

    # ----------------------------------------------------------------

    def _format(self):
        headers = [["", "id", "type", "best pipeline"]]

        rows = [
            [index, self.ids[index], hyperopt.type, hyperopt.best_pipeline.name]
            for index, hyperopt in enumerate(self.data)
        ]

        return Formatter(headers, rows)

    # ----------------------------------------------------------------

    def filter(self, conditional):
        """
        Filters the hyperopts container.

        Args:
            conditional (callable):
                A callable that evaluates to a boolean for a given item.

        Returns:
            :class:`getml.pipeline.Hyperopts`:
                A container of filtered hyperopts.

        Example:
            .. code-block:: python

                gaussian_hyperopts = getml.project.hyperopts.filter(lamda hyp: "Gaussian" in hyp.type)

        """
        hyperopts_filtered = [
            hyperopt for hyperopt in self.data if conditional(hyperopt)
        ]
        return Hyperopts(data=hyperopts_filtered)

    # ----------------------------------------------------------------

    def sort(self, key, descending=False):
        """
        Sorts the hyperopts container.

        Args:
            key (callable, optional):
                A callable that evaluates to a sort key for a given item.
            descending (bool, optional):
                Whether to sort in descending order.

        Return:
            :class:`getml.pipeline.Hyperopts`:
                A container of sorted hyperopts.

        Example:
            .. code-block:: python

                by_type = getml.project.hyperopt.sort(lambda hyp: hyp.type)

        """
        hyperopts_sorted = sorted(self.data, key=key, reverse=descending)
        return Hyperopts(data=hyperopts_sorted)
