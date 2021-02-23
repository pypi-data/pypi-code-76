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

"""Abstract representation of tables and their relations."""

# ------------------------------------------------------------------------------

import copy
import numbers

from getml import constants

from .diagram import _DataModel
from .helpers import _is_typed_list, _merge_join_keys
from .relationship import _all_relationships, many_to_many
from .visualization import _make_ascii_table, _make_html_table

# ------------------------------------------------------------------------------


class Placeholder:
    """Abstract representation of tables and their relations.

    This class provides an abstract representation of the
    :class:`~getml.data.DataFrame`. However, it does not
    contain any actual data.

    Examples:

        This example will construct a data model in which the
        'population_table' depends on the 'peripheral_table' via
        the 'join_key' column. In addition, only those rows in
        'peripheral_table' for which 'time_stamp' is smaller than the
        'time_stamp' in 'population_table' are considered. This is
        to prevent data leaks:

        .. code-block:: python

            population_placeholder = getml.data.Placeholder("POPULATION")
            peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

            population_placeholder.join(peripheral_placeholder,
                                        join_key="join_key",
                                        time_stamp="time_stamp"
            )

        If the relationship between two tables is many-to-one or one-to-one
        you should clearly say so:

        .. code-block:: python

            population_placeholder = getml.data.Placeholder("POPULATION")
            peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

            population_placeholder.join(peripheral_placeholder,
                                        join_key="join_key",
                                        time_stamp="time_stamp",
                                        relationship=getml.data.relationship.many_to_one
            )

        Please also refer to :mod:`~getml.data.relationship`.

        If you want to do a self-join, you can do something like this:

        .. code-block:: python

            population_placeholder = getml.data.Placeholder("POPULATION")
            population_placeholder2 = getml.data.Placeholder("POPULATION")

            population_placeholder.join(population_placeholder2,
                                        join_key="join_key",
                                        time_stamp="time_stamp"
            )

        If the join keys or time stamps are named differently in the two
        different tables, use *other_join_key* and *other_time_stamp*:

        .. code-block:: python

            population_placeholder = getml.data.Placeholder("POPULATION")
            peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

            population_placeholder.join(peripheral_placeholder,
                                        join_key="join_key_in_population",
                                        other_join_key="join_key_in_peripheral",
                                        time_stamp="time_stamp_in_population",
                                        other_time_stamp="time_stamp_in_peripheral"
            )

        You can join over more than one join key:

        .. code-block:: python

            population_placeholder = getml.data.Placeholder("POPULATION")
            peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

            population_placeholder.join(peripheral_placeholder,
                                        join_key=["join_key_1", "join_key_2"],
                                        time_stamp="time_stamp"
            )

        You can also limit the scope of your joins using *memory*. This
        can significantly speed up training time. For instance, if you
        only want to consider data from the last seven days, you could
        do something like this:

        .. code-block:: python

            population_placeholder = getml.data.Placeholder("POPULATION")
            peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

            population_placeholder.join(peripheral_placeholder,
                                        join_key="join_key",
                                        time_stamp="time_stamp",
                                        memory=getml.data.time.days(7)
            )

        In some use cases, particularly those involving time series, it
        might be a good idea to use targets from the past. You can activate
        this using *allow_lagged_targets*. But if you do that, you must
        also define a prediction *horizon*. For instance, if you want to
        predict data for the next hour, using data from the last seven days,
        you could do this:

        .. code-block:: python

            population_placeholder = getml.data.Placeholder("POPULATION")
            peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

            population_placeholder.join(peripheral_placeholder,
                                        join_key="join_key",
                                        time_stamp="time_stamp",
                                        allow_lagged_targets=True,
                                        horizon=getml.data.time.hours(1),
                                        memory=getml.data.time.days(7)
            )

        Please also refer to :mod:`~getml.data.time`.

    Args:
        name (str):
            The name used for this placeholder. This name will appear
            in the generated SQL code.

    Raises:
        TypeError:
            If any of the input arguments is of wrong type.
    """

    # ----------------------------------------------------------------

    _num_placeholders = 0
    """Index keeping track of the number of Placeholders
    constructed. Every call to the `__init__` method will assign a
    unique index to the constructed instance and increment the
    number.
    """

    # ----------------------------------------------------------------

    def __init__(self, name):

        # ------------------------------------------------------------

        if not isinstance(name, str):
            raise TypeError("'name' must be of type str")

        # ------------------------------------------------------------

        self.allow_lagged_targets = []
        self.horizon = []
        self.join_keys_used = []
        self.joined_tables = []
        self.memory = []
        self.name = name
        self.other_join_keys_used = []
        self.other_time_stamps_used = []
        self.relationship = []
        self.time_stamps_used = []
        self.upper_time_stamps_used = []

        # Unique ID of the placeholder. Will not be included in the
        # print or comparison.
        self.num = Placeholder._num_placeholders

        # Keep track of the global number of placeholders by
        # incrementing a module-level variable.
        Placeholder._num_placeholders += 1

    # ----------------------------------------------------------------

    def __eq__(self, other):
        """Compares the current instance with another one."""

        if not isinstance(other, Placeholder):
            raise TypeError("A placeholder can only compared to another placeholder!")

        # ------------------------------------------------------------

        # Check whether both objects have the same number of instance
        # variables.
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False

        # ------------------------------------------------------------

        # Except of `name` all instance variables are lists of
        # strings. As far as I can tell these objects can be compared
        # directly.
        for kkey in self.__dict__:

            if kkey not in other.__dict__:
                return False

            # Each Placeholder does have a different num value, which
            # is _not_ relevant for comparison (and also not included
            # when converting the Placeholder to string).
            if kkey == "num":
                continue

            if self.__dict__[kkey] != other.__dict__[kkey]:
                return False

        # ------------------------------------------------------------

        return True

    # ----------------------------------------------------------------

    def __repr__(self):
        head, body = self._make_head_body()
        return _make_ascii_table(head, body, max_cols=15, has_index=False)

    # ----------------------------------------------------------------

    def _repr_html_(self):
        return _DataModel(self).to_html()

    # ----------------------------------------------------------------

    def _getml_deserialize(self):

        encoding_dict = dict()

        for kkey in self.__dict__:

            if kkey == "num":
                continue

            encoding_dict[kkey + "_"] = self.__dict__[kkey]

        return encoding_dict

    # ----------------------------------------------------------------

    def _make_body(self, body):

        self_dict = copy.deepcopy(self.__dict__)

        del self_dict["name"]
        del self_dict["joined_tables"]
        del self_dict["num"]

        for i, table in enumerate(self.joined_tables):

            line = [self.name, table.name]

            for key in self_dict.keys():
                val = self_dict[key][i]
                if isinstance(val, str):
                    line.append(val)
                else:
                    line.append(str(val))

            line = ["" if elem == constants.NO_JOIN_KEY else elem for elem in line]

            line = [", ".join(elem.split(constants.JOIN_KEY_SEP)) for elem in line]

            line = [
                elem.replace(constants.MULTIPLE_JOIN_KEYS_BEGIN, "") for elem in line
            ]

            line = [elem.replace(constants.MULTIPLE_JOIN_KEYS_END, "") for elem in line]

            body.append(line)

        for table in self.joined_tables:
            body = table._make_body(body)

        return body

    # ----------------------------------------------------------------

    def _make_head_body(self):

        self_dict = copy.deepcopy(self.__dict__)

        del self_dict["name"]
        del self_dict["joined_tables"]
        del self_dict["num"]

        head = ["placeholder", "other placeholder"] + list(self_dict.keys())

        head = [elem.replace("_", " ") for elem in head]

        head = [head]

        body = self._make_body([])

        return head, body

    # ----------------------------------------------------------------

    def join(
        self,
        other,
        join_key="",
        time_stamp="",
        other_join_key="",
        other_time_stamp="",
        upper_time_stamp="",
        horizon=0.0,
        memory=0.0,
        allow_lagged_targets=False,
        relationship=many_to_many,
    ):
        """Establish a relation between two
        :class:`~getml.data.Placeholder` s.

        Examples:

            This example will construct a data model in which the
            'population_table' depends on the 'peripheral_table' via
            the 'join_key' column. In addition, only those rows in
            'peripheral_table' for which 'time_stamp' is smaller than the
            'time_stamp' in 'population_table' are considered. This is
            to prevent data leaks:

            .. code-block:: python

                population_placeholder = getml.data.Placeholder("POPULATION")
                peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

                population_placeholder.join(peripheral_placeholder,
                                            join_key="join_key",
                                            time_stamp="time_stamp"
                )

            If the relationship between two tables is many-to-one or one-to-one
            you should clearly say so:

            .. code-block:: python

                population_placeholder = getml.data.Placeholder("POPULATION")
                peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

                population_placeholder.join(peripheral_placeholder,
                                            join_key="join_key",
                                            time_stamp="time_stamp",
                                            relationship=getml.data.relationship.many_to_one
                )

            Please also refer to :mod:`~getml.data.relationship`.

            If you want to do a self-join, you can do something like this:

             .. code-block:: python

                population_placeholder = getml.data.Placeholder("POPULATION")
                population_placeholder2 = getml.data.Placeholder("POPULATION")

                population_placeholder.join(population_placeholder2,
                                            join_key="join_key",
                                            time_stamp="time_stamp"
                )

            If the join keys or time stamps are named differently in the two
            different tables, use *other_join_key* and *other_time_stamp*:

            .. code-block:: python

                population_placeholder = getml.data.Placeholder("POPULATION")
                peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

                population_placeholder.join(peripheral_placeholder,
                                            join_key="join_key_in_population",
                                            other_join_key="join_key_in_peripheral",
                                            time_stamp="time_stamp_in_population",
                                            other_time_stamp="time_stamp_in_peripheral"
                )

            You can join over more than one join key:

            .. code-block:: python

                population_placeholder = getml.data.Placeholder("POPULATION")
                peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

                population_placeholder.join(peripheral_placeholder,
                                            join_key=["join_key_1", "join_key_2"],
                                            time_stamp="time_stamp"
                )

            You can also limit the scope of your joins using *memory*. This
            can significantly speed up training time. For instance, if you
            only want to consider data from the last seven days, you could
            do something like this:

            .. code-block:: python

                population_placeholder = getml.data.Placeholder("POPULATION")
                peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

                population_placeholder.join(peripheral_placeholder,
                                            join_key="join_key",
                                            time_stamp="time_stamp",
                                            memory=getml.data.time.days(7)
                )

            In some use cases, particularly those involving time series, it
            might be a good idea to use targets from the past. You can activate
            this using *allow_lagged_targets*. But if you do that, you must
            also define a prediction *horizon*. For instance, if you want to
            predict data for the next hour, using data from the last seven days,
            you could do this:

            .. code-block:: python

                population_placeholder = getml.data.Placeholder("POPULATION")
                peripheral_placeholder = getml.data.Placeholder("PERIPHERAL")

                population_placeholder.join(peripheral_placeholder,
                                            join_key="join_key",
                                            time_stamp="time_stamp",
                                            allow_lagged_targets=True,
                                            horizon=getml.data.time.hours(1),
                                            memory=getml.data.time.days(7)
                )

            Please also refer to :mod:`~getml.data.time`.

        Args:
            other (:class:`~getml.data.Placeholder`):

                :class:`~getml.data.Placeholder` the current
                instance will depend on.

            join_key (str or List[str]):

                Name of the :class:`~getml.data.columns.StringColumn` in
                the corresponding :class:`~getml.data.DataFrame` used
                to establish a relation between the current instance
                and `other`.

                If no `join_key` is passed, then all rows of the two
                data frames will be joined.

                If a list of strings is passed, then all join keys
                must match

                If `other_join_key` is an empty string, `join_key`
                will be used to determine the column of `other` too.

            time_stamp (str, optional):

                Name of the :class:`~getml.data.columns.FloatColumn` in
                the corresponding :class:`~getml.data.DataFrame` used
                to ensure causality.

                The provided string must be contained in the
                ``time_stamps`` instance variable.

                If `other_time_stamp` is an empty string, `time_stamp`
                will be used to determine the column of `other` too.

            other_join_key (str or List[str], optional):

                Name of the :class:`~getml.data.columns.StringColumn` in
                the :class:`~getml.data.DataFrame` represented by
                `other` used to establish a relation between the
                current instance and `other`.

                If an empty string is passed, `join_key` will be
                used instead.

            other_time_stamp (str, optional):

                Name of the :class:`~getml.data.columns.FloatColumn` in
                the :class:`~getml.data.DataFrame` represented by
                `other` used to ensure causality.

                If an empty string is provided, `time_stamp` will be
                used instead.

            upper_time_stamp (str, optional):

                Optional additional time stamp in the `other` that
                will limit the number of joined rows to a certain
                point in the past. This is useful for data with
                limited correlation length.

                Expressed as SQL code, this will add the condition

                .. code-block:: sql

                    t1.time_stamp < t2.upper_time_stamp OR
                    t2.upper_time_stamp IS NULL

                to the feature.

                If an empty string is provided, all values in the past
                will be considered.

            horizon (float, optional):

                Period of time between the *time_stamp* and the
                *other_time_stamp*.

                Usually, you need to ensure that no data from the
                future is used for your prediction, like this:

                .. code-block:: sql

                    t1.time_stamp - t2.other_time_stamp >= 0

                But in some cases, you would like the gap to be something
                other than zero. For such cases, you can set a horizon:

                .. code-block:: sql

                    t1.time_stamp - t2.other_time_stamp >= horizon

            memory (float, optional):

                Period of time to which the join is limited.

                Expressed as SQL code, this will add the condition

                .. code-block:: sql

                    t1.time_stamp - t2.other_time_stamp < horizon + memory

                to the feature.

                When the memory is set to 0.0 or a negative number, there
                is no limit.

                Limiting the joins using the *memory* or
                *upper_time_stamp* parameter can significantly reduce
                the training time. However, you can only set an
                *upper_time_stamp* or *memory*, but not both.

            allow_lagged_targets (bool, optional):

                For some applications, it is allowed to aggregate over
                target variables from the past. In others, this is not allowed.
                If *allow_lagged_targets* is set to True, you must pass a horizon
                that is greater than zero, otherwise you would have a data leak
                (an exception will be thrown to prevent this).

            relationship (string, optional);

                If the relationship between two tables in many-to-one or
                one-to-one, then feature learning is not necessary or meaningful.
                If you mark such relationships using one of the constants
                defined in :mod:`~getml.data.relationship`, the tables will
                be joined directly by the pipeline.

        Note:

            `other` must be created (temporally) after the current
            instance. This was implemented as a measure to prevent
            circular dependencies in the data model.

        """

        # ------------------------------------------------------------

        join_key, other_join_key = _merge_join_keys(join_key, other_join_key)

        # ------------------------------------------------------------

        if not isinstance(other, Placeholder):
            raise TypeError("'other' must be a getml.data.Placeholder!")

        if not isinstance(join_key, str):
            raise TypeError("'join_key' must be of type str or a list of strings")

        if not isinstance(time_stamp, str):
            raise TypeError("'time_stamp' must be of type str")

        if not isinstance(other_join_key, str):
            raise TypeError("'other_join_key' must be of type str")

        if not isinstance(other_time_stamp, str):
            raise TypeError("'other_time_stamp' must be of type str")

        if not isinstance(upper_time_stamp, str):
            raise TypeError("'upper_time_stamp' must be of type str")

        if not isinstance(horizon, numbers.Real):
            raise TypeError("'horizon' must be a real number")

        if not isinstance(memory, numbers.Real):
            raise TypeError("'memory' must be a real number")

        if not isinstance(relationship, str):
            raise TypeError("'relationship' must be a str")

        if not isinstance(allow_lagged_targets, bool):
            raise TypeError("'allow_lagged_targets' must be a bool")

        # ------------------------------------------------------------

        if not join_key:
            if other_join_key:
                raise ValueError(
                    """You cannot pass 'other_join_key' if
                                    you haven't passed 'join_key'."""
                )
            join_key = constants.NO_JOIN_KEY

        # ------------------------------------------------------------

        if memory > 0.0 and upper_time_stamp != "":
            raise ValueError(
                """You can either set memory, or an """
                """upper_time_stamp, but not both."""
            )

        # ------------------------------------------------------------

        if allow_lagged_targets and horizon <= 0.0:
            raise ValueError(
                """If allow_lagged_targets is True, then
                                horizon must be greater than 0. Otherwise,
                                you will have a data leak."""
            )

        # ------------------------------------------------------------

        if relationship not in _all_relationships:
            raise ValueError(
                "relationship must be one of the following: "
                + str(_all_relationships)
                + "."
            )

        # ------------------------------------------------------------

        if other.num <= self.num:
            raise Exception(
                """You cannot join a placeholder that was created
                before the placeholder it is joined to.
                This is to avoid circular dependencies.
                Please reverse the order in which the placeholders '"""
                + other.name
                + "' and '"
                + self.name
                + "' are created!"
            )

        if time_stamp == "" and other_time_stamp != "":
            raise ValueError(
                """If time_stamp is an empty string, then"""
                """ other_time_stamp must be empty as well."""
            )

        other_join_key = other_join_key or join_key

        other_time_stamp = other_time_stamp or time_stamp

        # ------------------------------------------------------------

        self.allow_lagged_targets.append(allow_lagged_targets)

        self.horizon.append(horizon)

        self.join_keys_used.append(join_key)

        self.relationship.append(relationship)

        self.other_join_keys_used.append(other_join_key)

        self.time_stamps_used.append(time_stamp)

        self.other_time_stamps_used.append(other_time_stamp)

        self.upper_time_stamps_used.append(upper_time_stamp)

        self.memory.append(memory)

        # ------------------------------------------------------------

        self.joined_tables.append(other)

    # --------------------------------------------------------------------

    def set_relations(
        self,
        allow_lagged_targets=None,
        join_keys_used=None,
        horizon=None,
        relationship=None,
        memory=None,
        other_join_keys_used=None,
        time_stamps_used=None,
        other_time_stamps_used=None,
        upper_time_stamps_used=None,
        joined_tables=None,
    ):
        """Set all relational instance variables not exposed in the
        constructor.

        Args:
            allow_lagged_targets (List[bool]): Whether we want to allow
                lagged targets to be aggregated in the join.

            join_keys_used (List[str]): Elements in
                `join_keys` used to define the relations to the other
                tables provided in `joined_tables`.

            horizon (List[float]): `horizon` of the join. Determines
                the gap between time_stamp and other_time_stamp.

            memory (List[float]): `memory` of the join. Determines
                how much of the past data may be joined.

            other_join_keys_used (List[str]): `join_keys` of the
                :class:`~getml.data.Placeholder` in
                `joined_tables` used to define a relation with the
                current instance. Note that the `join_keys` instance
                variable is *not* contained in the `joined_tabled`.

            time_stamps_used (List[str]): Elements in `time_stamps` used
                to define the relations to the other tables provided
                in `joined_tables`.

            other_time_stamps_used (List[str]): `time_stamps` of the
                :class:`~getml.data.Placeholder` in
                `joined_tables` used to define a relation with the
                current instance. Note that the `time_stamps` instance
                variable is *not* contained in the `joined_tabled`.

            upper_time_stamps_used (List[str]): `time_stamps` of the
                :class:`~getml.data.Placeholder` in
                `joined_tables` used as 'upper_time_stamp' to define a
                relation with the current instance. For details please
                see the :meth:`~getml.data.Placeholder.join`
                method. Note that the `time_stamps` instance variable
                is *not* contained in the `joined_tabled`.

            joined_tables (List[:class:`~getml.data.Placeholder`]):
                List of all other
                :class:`~getml.data.Placeholder` the current
                instance is joined on.

        Raises:
            TypeError: If any of the input arguments is of wrong type.
            ValueError: If the input arguments are not of same length.

        """

        # ------------------------------------------------------------

        allow_lagged_targets = allow_lagged_targets or []

        horizon = horizon or []

        join_keys_used = join_keys_used or []

        relationship = relationship or []

        memory = memory or []

        other_join_keys_used = other_join_keys_used or []

        time_stamps_used = time_stamps_used or []

        other_time_stamps_used = other_time_stamps_used or []

        upper_time_stamps_used = upper_time_stamps_used or []

        joined_tables = joined_tables or []

        # ------------------------------------------------------------

        if not _is_typed_list(allow_lagged_targets, bool):
            raise TypeError(
                "'allow_lagged_targets' must be an empty list or a list of bools."
            )

        if not _is_typed_list(horizon, numbers.Real):
            raise TypeError("'horizon' must be an empty list or a list of real numbers")

        if not _is_typed_list(join_keys_used, str):
            raise TypeError("'join_keys_used' must be an empty list or a list of str")

        if not _is_typed_list(relationship, str):
            raise TypeError(
                "'relationship' must be an empty list or a list of strings."
            )

        if not _is_typed_list(memory, numbers.Real):
            raise TypeError("'memory' must be an empty list or a list of real numbers")

        if not _is_typed_list(other_join_keys_used, str):
            raise TypeError(
                "'other_join_keys_used' must be an empty list or a list of str"
            )

        if not _is_typed_list(time_stamps_used, str):
            raise TypeError("'time_stamps_used' must be an empty list or a list of str")

        if not _is_typed_list(other_time_stamps_used, str):
            raise TypeError(
                "'other_time_stamps_used' must be an empty list or a list of str"
            )

        if not _is_typed_list(upper_time_stamps_used, str):
            raise TypeError(
                "'upper_time_stamps_used' must be an empty list or a list of str"
            )

        if not _is_typed_list(joined_tables, Placeholder):
            raise TypeError(
                "'joined_tables' must be an empty list or a list of getml.data.Placeholder"
            )

        # ------------------------------------------------------------
        # Check whether all provided lists have the same length.

        if (
            len(
                set(
                    [
                        len(allow_lagged_targets),
                        len(horizon),
                        len(join_keys_used),
                        len(relationship),
                        len(memory),
                        len(other_join_keys_used),
                        len(time_stamps_used),
                        len(other_time_stamps_used),
                        len(upper_time_stamps_used),
                        len(joined_tables),
                    ]
                )
            )
            != 1
        ):
            raise ValueError("Mismatching length of the provided lists")

        # ------------------------------------------------------------

        self.allow_lagged_targets = allow_lagged_targets
        self.horizon = horizon
        self.join_keys_used = join_keys_used
        self.relationship = relationship
        self.memory = memory
        self.other_join_keys_used = other_join_keys_used
        self.time_stamps_used = time_stamps_used
        self.other_time_stamps_used = other_time_stamps_used
        self.upper_time_stamps_used = upper_time_stamps_used
        self.joined_tables = joined_tables


# --------------------------------------------------------------------


def _decode_placeholder(raw_dict):
    """A custom decoder function for
    :class:`~getml.data.Placeholder`.

    Args:
        raw_dict (dict or `~getml.data.Placeholder`):

            dict naively deserialized from the JSON message provided
            by the getML engine. If a placeholder is passed, that
            placeholder is returned without any modifications.

    Raises:
        KeyError: If the ``type`` key in `raw_dict` is either not present
            or of unknown type.
        ValueError: If not all keys in `raw_dict` have a trailing
            underscore.
        TypeError: If `raw_dict` is not of type :py:class:`dict`.

    Returns:
        :class:`~getml.data.Placeholder`

    Examples:

        Create a :class:`~getml.data.Placeholder`, serialize
        it, and deserialize it again.

        .. code-block:: python

            p = getml.data.Placeholder(name = "placebert")
            p_serialized = json.dumps(p, cls = getml.communication._GetmlEncoder)
            p2 = json.loads(p_serialized, object_hook = getml.placeholders._decode_placeholder)
            p == p2

    """

    # ----------------------------------------------------------------

    if isinstance(raw_dict, Placeholder):
        return raw_dict

    # ----------------------------------------------------------------

    if not isinstance(raw_dict, dict):
        raise TypeError("_decode_placeholder is expecting a dict as input")

    # ----------------------------------------------------------------

    decoding_dict = dict()

    relation_dict = dict()

    for kkey in raw_dict:

        if kkey[len(kkey) - 1] != "_":
            raise ValueError("All keys in the JSON must have a trailing underscore.")

        if kkey == "joined_tables_":
            relation_dict[kkey[:-1]] = [
                _decode_placeholder(elem) for elem in raw_dict[kkey]
            ]

        elif kkey in [
            "allow_lagged_targets_",
            "horizon_",
            "join_keys_used_",
            "memory_",
            "other_join_keys_used_",
            "relationship_",
            "time_stamps_used_",
            "other_time_stamps_used_",
            "upper_time_stamps_used_",
        ]:
            relation_dict[kkey[:-1]] = raw_dict[kkey]

        else:
            decoding_dict[kkey[:-1]] = raw_dict[kkey]

    # ----------------------------------------------------------------

    placeholder = Placeholder(**decoding_dict)

    placeholder.set_relations(**relation_dict)

    # ----------------------------------------------------------------

    return placeholder


# --------------------------------------------------------------------


def _decode_joined_tables(raw_list):
    return [_decode_placeholder(elem) for elem in raw_list]


# --------------------------------------------------------------------
