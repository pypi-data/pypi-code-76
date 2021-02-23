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
Container for the features associated with a pipeline.
"""

import json
import re

import numpy as np
import pandas as pd

import getml.communication as comm
from getml.data.helpers import _is_typed_list
from getml.utilities.formatter import Formatter

from .feature import Feature
from .helpers import _attach_empty
from .sql_code import SQLCode
from .sql_string import SQLString

# --------------------------------------------------------------------


class Features:
    """
    Container which holds a pipeline's features. Features can be accessed
    by name, index or with a numpy array. The container supports slicing and
    is sort- and filterable.

    Further, the container holds global methods to request features' importances,
    correlations and their respective transpiled sql representation.

    Note:
        The container is an iterable. So, in addition to
            :method:`getml.pipeline.features.filter` you can
            also use python list comprehensions for filtering.

    Example:

        .. code-block:: python

            all_my_features = my_pipeline.features

            first_feature = my_pipeline.features[0]

            second_feature = my_pipeline.features["feature_1_2"]

            all_but_last_10_features = my_pipeline.features[:-10]

            important_features = [feature for feature in my_pipeline.features if feature.importance > 0.1]

            names, importances = my_pipeline.features.importances()

            names, correlations = my_pipeline.features.correlations()

            sql_code = my_pipeline.features.to_sql()
    """

    # ----------------------------------------------------------------

    def __init__(self, pipeline, targets, data=None):

        if not isinstance(pipeline, str):
            raise ValueError("'pipeline' must be a str.")

        if not _is_typed_list(targets, str):
            raise TypeError("'targets' must be a list of str.")

        self.pipeline = pipeline

        self.targets = targets

        if data is None:
            self.data = self._load_features()

        else:
            self.data = data

    # ----------------------------------------------------------------

    def __repr__(self):
        return self._format().render_string()

    # ------------------------------------------------------------

    def _repr_html_(self):
        return self._format().render_html()

    # ----------------------------------------------------------------

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        if isinstance(key, slice):
            features_subset = self.data[key]
            return self._make_features(features_subset)
        if isinstance(key, str):
            if key in self.names:
                return [feature for feature in self.data if feature.name == key][0]
            raise AttributeError(f"No Feature with name: {key}")
        if isinstance(key, np.ndarray):
            features_subset = np.array(self.data)[key].tolist()
            return features_subset
        raise TypeError(
            f"Features can only be indexed by: int, slices, or str, not {type(key).__name__}"
        )

    # ----------------------------------------------------------------

    def __iter__(self):
        yield from self.data

    # ----------------------------------------------------------------

    def __len__(self):
        return len(self.data)

    # ----------------------------------------------------------------

    def _pivot(self, field):
        """
        Pivots the data for a given field. Returns a list of values of the field's type.
        """
        return [getattr(feature, field) for feature in self.data]

    # ----------------------------------------------------------------

    def _load_features(self):
        """
        Loads the actual feature data from the engine.
        """
        features = []

        for target_num, target in enumerate(self.targets):
            names = self.correlations(target_num, sort=False)[0].tolist()
            indices = range(len(names))
            correlations = _attach_empty(
                self.correlations(target_num, sort=False)[1].tolist(),
                len(names),
                np.NaN,
            )
            importances = _attach_empty(
                self.importances(target_num, sort=False)[1].tolist(), len(names), np.NaN
            )
            sql_transpilations = _attach_empty(
                list(self.to_sql(subfeatures=False))[:-1], len(names), ""
            )

            features.extend(
                [
                    Feature(
                        index=index,
                        name=names[index],
                        pipeline=self.pipeline,
                        target=target,
                        targets=self.targets,
                        importance=importances[index],
                        correlation=correlations[index],
                        sql=SQLString(sql_transpilations[index]),
                    )
                    for index in indices
                ]
            )
        return features

    # ----------------------------------------------------------------

    def _format(self):
        rows = [
            [
                index,
                feature.target,
                feature.name,
                feature.correlation,
                feature.importance,
            ]
            for index, feature in enumerate(self.data)
        ]

        headers = [["", "target", "name", "correlation", "importance"]]

        return Formatter(headers, rows)

    # ----------------------------------------------------------------

    def _make_features(self, data):
        """
        A factory to construct a `Features` container from a list of
        sole `Feature`s.
        """
        return Features(self.pipeline, self.targets, data)

    # ----------------------------------------------------------------

    def _to_pandas(self):

        names, correlations, importances, sql, target = (
            self._pivot(field)
            for field in ["name", "correlation", "importance", "sql", "target"]
        )

        data_frame = pd.DataFrame(index=range(len(names)))

        data_frame["names"] = names

        data_frame["correlations"] = correlations

        data_frame["importances"] = importances

        data_frame["target"] = target

        data_frame["sql"] = sql

        return data_frame

    # ----------------------------------------------------------------

    @property
    def correlation(self):
        return self._pivot("correlation")

    # ------------------------------------------------------------

    def correlations(self, target_num=0, sort=True):
        """
        Returns the data for the feature correlations,
        as displayed in the getML monitor.

        Args:
            target_num (int):
                Indicates for which target you want to view the
                importances.
                (Pipelines can have more than one target.)

            sort (bool):
                Whether you want the results to be sorted.

        Return:
            (:class:`numpy.ndarray`, :class:`numpy.ndarray`):
                - The first array contains the names of
                  the features.
                - The second array contains the correlations with
                  the target.
        """

        # ------------------------------------------------------------

        cmd = dict()

        cmd["type_"] = "Pipeline.feature_correlations"
        cmd["name_"] = self.pipeline

        cmd["target_num_"] = target_num

        # ------------------------------------------------------------

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        json_obj = json.loads(msg)

        # ------------------------------------------------------------

        names = np.asarray(json_obj["feature_names_"])
        correlations = np.asarray(json_obj["feature_correlations_"])

        # ------------------------------------------------------------

        assert len(correlations) <= len(names), "Correlations must be <= names"

        if hasattr(self, "data"):
            indices = np.asarray(
                [
                    feature.index
                    for feature in self.data
                    if feature.target == self.targets[target_num]
                    and feature.index < len(correlations)
                ]
            )

            names = names[indices]
            correlations = correlations[indices]

        # ------------------------------------------------------------

        if not sort:
            return names, correlations

        # ------------------------------------------------------------

        indices = np.argsort(np.abs(correlations))[::-1]

        # ------------------------------------------------------------

        return (names[indices], correlations[indices])

    # ----------------------------------------------------------------

    def filter(self, conditional):
        """
        Filters the Features container.

        Args:
            conditional (callable, optional):
                A callable that evaluates to a boolean for a given item.

        Return:
            :class:`getml.pipeline.Features`:
                A container of filtered Features.

        Example:
            .. code-block:: python

                important_features = my_pipeline.features.filter(lambda feature: feature.importance > 0.1)

                correlated_features = my_pipeline.features.filter(lambda feature: feature.correlation > 0.3)

        """
        features_filtered = [feature for feature in self.data if conditional(feature)]
        return Features(self.pipeline, self.targets, data=features_filtered)

    # ----------------------------------------------------------------

    @property
    def importance(self):
        return self._pivot("importance")

    # ----------------------------------------------------------------

    def importances(self, target_num=0, sort=True):
        """
        Returns the data for the feature importances,
        as displayed in the getML monitor.

        Args:
            target_num (int):
                Indicates for which target you want to view the
                importances.
                (Pipelines can have more than one target.)

            sort (bool):
                Whether you want the results to be sorted.

        Return:
            (:class:`numpy.ndarray`, :class:`numpy.ndarray`):
                - The first array contains the names of
                  the features.
                - The second array contains their importances.
                  By definition, all importances add up to 1.
        """

        # ------------------------------------------------------------

        cmd = dict()

        cmd["type_"] = "Pipeline.feature_importances"
        cmd["name_"] = self.pipeline

        cmd["target_num_"] = target_num

        # ------------------------------------------------------------

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        json_obj = json.loads(msg)

        # ------------------------------------------------------------

        names = np.asarray(json_obj["feature_names_"])
        importances = np.asarray(json_obj["feature_importances_"])

        # ------------------------------------------------------------

        if hasattr(self, "data"):
            assert len(importances) <= len(names), "Importances must be <= names"

            indices = np.asarray(
                [
                    feature.index
                    for feature in self.data
                    if feature.target == self.targets[target_num]
                    and feature.index < len(importances)
                ]
            )

            names = names[indices]
            importances = importances[indices]

        # ------------------------------------------------------------

        if not sort:
            return names, importances

        # ------------------------------------------------------------

        assert len(importances) <= len(names), "Must have the same length"

        indices = np.argsort(importances)[::-1]

        # ------------------------------------------------------------

        return (names[indices], importances[indices])

    # ----------------------------------------------------------------

    @property
    def name(self):
        return self._pivot("name")

    # ----------------------------------------------------------------

    @property
    def names(self):
        return self._pivot("name")

    # ----------------------------------------------------------------

    def sort(self, by=None, key=None, descending=None):
        """
        Sorts the Features container. If no arguments are provided the
        container is sorted by target and name.

        Args:
            by (str, optional):
                The name of field to sort by. Possible fields:
                    - name(s)
                    - correlation(s)
                    - importances(s)
            key (callable, optional):
                A callable that evaluates to a sort key for a given item.
            descending (bool, optional):
                Whether to sort in descending order.

        Return:
            :class:`getml.pipeline.Features`:
                A container of sorted Features.

        Example:
            .. code-block:: python

                by_correlation = my_pipeline.features.sort(by="correlation")

                by_importance = my_pipeline.features.sort(key=lambda feature: feature.importance)

        """

        reverse = descending or False

        if (by is not None) and (key is not None):
            raise ValueError("Only one of `by` and `key` can be provided.")

        if key is not None:
            features_sorted = sorted(self.data, key=key, reverse=reverse)
            return self._make_features(features_sorted)

        else:
            if by is None:
                features_sorted = sorted(
                    self.data, key=lambda feature: feature.index, reverse=reverse
                )
                features_sorted.sort(key=lambda feature: feature.target)
                return self._make_features(features_sorted)

            if re.match(by, "names?"):
                features_sorted = sorted(
                    self.data, key=lambda feature: feature.name, reverse=reverse
                )
                return self._make_features(features_sorted)

            if re.match(by, "correlations?"):
                reverse = descending or True
                features_sorted = sorted(
                    self.data,
                    key=lambda feature: abs(feature.correlation),
                    reverse=reverse,
                )
                return self._make_features(features_sorted)

            if re.match(by, "importances?"):
                reverse = descending or True
                features_sorted = sorted(
                    self.data, key=lambda feature: feature.importance, reverse=reverse
                )
                return self._make_features(features_sorted)

            raise ValueError(f"Cannot sort by: {by}.")

    # ----------------------------------------------------------------

    def to_pandas(self):
        """
        Returns all information related to the features in a pandas data frame.
        """

        return self._to_pandas()

    # ----------------------------------------------------------------

    def to_sql(self, targets=True, subfeatures=True):
        """
        Returns SQL statements visualizing the features.

            Args:
                targets (boolean):
                    Whether you want to include the target columns
                    in the main table.

                subfeatures (boolean):
                    Whether you want to include the code for the
                    subfeatures of a snowflake schema.

            Examples:

                .. code-block:: python

                    my_pipeline.features.to_sql()

            Raises:
                IOError: If the pipeline could not be found
                    on the engine or
                    the pipeline could not be fitted.
                KeyError: If an unsupported instance variable is
                    encountered.
                TypeError: If any instance variable is of wrong type.

            Returns:
                :class:`~getml.pipeline.SQLCode`
                    Object representing the features.

            Note:
                Only fitted pipelines
                (:meth:`~getml.pipeline.Pipeline.fit`) can hold trained
                features which can be returned as SQL statements.
                The dialect is based on the SQLite3 standard.
        """

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = "Pipeline.to_sql"
        cmd["name_"] = self.pipeline

        cmd["targets_"] = targets
        cmd["subfeatures_"] = subfeatures

        sock = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        if msg != "Found!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        sql = comm.recv_string(sock)

        # ------------------------------------------------------------

        sock.close()

        # ------------------------------------------------------------

        return SQLCode(sql.split("\n\n\n"))
