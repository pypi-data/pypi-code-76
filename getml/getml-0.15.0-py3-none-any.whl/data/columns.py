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

"""Handlers for 1-d arrays storing the data of an individual variable.

Like the :class:`~getml.data.DataFrame`, the
:mod:`~getml.data.columns` do not contain any actual data themselves
but are only handlers to objects within the getML engine. These
containers store data of a single variable in a one-dimensional array
of an uniform type.

Columns are *immutable* and *lazily evaluated*.

- *Immutable* means that there are no in-place
  operation on the columns. Any change to the column
  will return a new, changed column.

- *Lazy evaluation* means that operations won't be
  executed until results are required. This is reflected
  in the *virtual columns*: Virtual columns do not exist
  until they are required.

Example:

.. code-block:: python

    import numpy as np

    import getml.data as data
    import getml.engine as engine
    import getml.data.roles as roles

    # ----------------

    engine.set_project("examples")

    # ----------------
    # Create a data frame from a JSON string

    json_str = \"\"\"{
        "names": ["patrick", "alex", "phil", "ulrike"],
        "column_01": [2.4, 3.0, 1.2, 1.4],
        "join_key": ["0", "1", "2", "3"],
        "time_stamp": ["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04"]
    }\"\"\"

    my_df = data.DataFrame(
        "MY DF",
        roles={
            "unused_string": ["names", "join_key", "time_stamp"],
            "unused_float": ["column_01"]}
    ).read_json(
        json_str
    )

    # ----------------

    col1 = my_df["column_01"]

    # ----------------

    # col2 is a virtual column.
    # The operation is not executed yet.
    col2 = 2.0 - col1

    # This is when '2.0 - col1' is actually
    # executed.
    my_df["column_02"] = col2
    my_df.set_role("column_02", roles.numerical)

    # If you want to update column_01,
    # you can't do that in-place.
    # You need to replace it with a new column
    col1 = col1 + col2
    my_df["column_01"] = col1
    my_df.set_role("column_01", roles.numerical)

"""

import copy
import datetime
import json
import numbers

import numpy as np

import getml.communication as comm
import getml.constants as constants

from .visualization import (
    _add_index,
    _get_column_content,
    _make_ascii_table,
    _make_html_table,
    _make_link,
    _monitor_url,
)

# ------------------------------------------------------------------------------


class _Column:
    """
    Base object not meant to be called directly.
    """

    # -------------------------------------------------------------------------

    def __init__(self):
        self.thisptr = dict()

    # -------------------------------------------------------------------------

    @property
    def name(self):
        """
        The role of this column.
        """
        return self.thisptr["name_"]

    # -------------------------------------------------------------------------

    @property
    def role(self):
        """
        The role of this column.

        Roles are needed by the feature learning algorithm so it knows how
        to treat the columns.
        """
        return self.thisptr["role_"]

    # -------------------------------------------------------------------------

    @property
    def unit(self):
        """
        The unit of this column.

        Units are used to determine which columns can be compared to each other
        by the feature learning algorithms.
        """

        # -------------------------------------------
        # Build command string

        cmd = dict()

        cmd.update(self.thisptr)

        cmd["type_"] += ".get_unit"

        # -------------------------------------------
        # Send JSON command to engine

        sock = comm.send_and_receive_socket(cmd)

        # -------------------------------------------
        # Make sure everything went well

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        # -------------------------------------------

        unit = comm.recv_string(sock)

        return unit


# ------------------------------------------------------------------------------


class Aggregation:
    """
    Lazily evaluated aggregation over a column.

    Example:

    .. code-block:: python

        >>> my_data_frame["my_column"].avg().get()
        3.0
    """

    def __init__(self, alias, col, agg_type):
        self.thisptr = dict()
        self.thisptr["as_"] = alias
        self.thisptr["col_"] = col.thisptr
        self.thisptr["type_"] = agg_type

    # -----------------------------------------------------------------------------

    def __repr__(self):
        return str(self)

    # -----------------------------------------------------------------------------

    def __str__(self):
        val = self.get()
        return self.thisptr["type_"].upper() + " aggregation, value: " + str(val) + "."

    # --------------------------------------------------------------------------

    def get(self):
        """
        Receives the value of the aggregation over the column.
        """

        # -------------------------------------------
        # Build command string

        cmd = dict()

        cmd["name_"] = ""
        cmd["type_"] = "FloatColumn.aggregate"

        cmd["aggregation_"] = self.thisptr
        cmd["df_name_"] = self.thisptr["col_"]["df_name_"]

        # -------------------------------------------
        # Create connection and send the command

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        # -------------------------------------------
        # Make sure everything went well, receive data
        # and close connection

        if msg != "Success!":
            sock.close()
            comm.engine_exception_handler(msg)

        mat = comm.recv_matrix(sock)

        # -------------------------------------------
        # Close connection.

        sock.close()

        # -------------------------------------------

        return mat.ravel()[0]


# -----------------------------------------------------------------------------


class VirtualBooleanColumn:
    """
    Handle to a (lazily evaluated) virtual boolean column.

    Virtual columns do not actually exist - they will be lazily
    evaluated when necessary.

    They can be used to take subselection of the data frame
    or to update other columns.

    Example:

    .. code-block:: python

        import numpy as np

        import getml.data as data
        import getml.engine as engine
        import getml.data.roles as roles

        # ----------------

        engine.set_project("examples")

        # ----------------
        # Create a data frame from a JSON string

        json_str = \"\"\"{
            "names": ["patrick", "alex", "phil", "ulrike"],
            "column_01": [2.4, 3.0, 1.2, 1.4],
            "join_key": ["0", "1", "2", "3"],
            "time_stamp": ["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04"]
        }\"\"\"

        my_df = data.DataFrame(
            "MY DF",
            roles={
                "unused_string": ["names", "join_key", "time_stamp"],
                "unused_float": ["column_01"]}
        ).read_json(
            json_str
        )

        # ----------------

        names = my_df["names"]

        # This is a virtual boolean column.
        a_or_p_in_names = names.contains("p") | names.contains("a")

        # Creates another data frame containing
        # only those entries, where "names" contains a or p.
        my_other_df = my_df.where("MY OTHER DF", a_or_p_in_names)

        # ----------------

        # Returns a new column, where all names
        # containing "rick" are replaced by "Patrick".
        # Again, columns are immutable - this returns an updated
        # version, but leaves the original column unchanged.
        new_names = names.update(names.contains("rick"), "Patrick")

        my_df["new_names"] = new_names

        # ----------------

        # Boolean columns can also be used to
        # create binary target variables.
        target = (names == "phil")

        my_df["target"] = target
        my_df.set_role(target, roles.target)

        # By the way, instead of using the
        # __setitem__ operator and .set_role(...)
        # you can just use .add(...).
        my_df.add(target, "target", roles.target)

    """

    def __init__(self, df_name, operator, operand1, operand2):
        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["type_"] = "VirtualBooleanColumn"

        self.thisptr["operator_"] = operator

        self.thisptr["operand1_"] = self._parse_operand(operand1)

        if operand2 is not None:
            self.thisptr["operand2_"] = self._parse_operand(operand2)

    # -----------------------------------------------------------------------------

    def __and__(self, other):
        return VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="and",
            operand1=self,
            operand2=other,
        )

    # -----------------------------------------------------------------------------

    def __eq__(self, other):
        return VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="equal_to",
            operand1=self,
            operand2=other,
        )

    # -----------------------------------------------------------------------------

    def __invert__(self):
        return self.is_false()

    # -----------------------------------------------------------------------------

    def __or__(self, other):
        return VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="or",
            operand1=self,
            operand2=other,
        )

    # -----------------------------------------------------------------------------

    def __ne__(self, other):
        return VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="not_equal_to",
            operand1=self,
            operand2=other,
        )

    # -----------------------------------------------------------------------------

    def __xor__(self, other):
        return VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="xor",
            operand1=self,
            operand2=other,
        )

    # -----------------------------------------------------------------------------

    def _parse_operand(self, operand):

        if isinstance(operand, bool):
            return {"type_": "BooleanValue", "value_": operand}

        if isinstance(operand, str):
            return {"type_": "CategoricalValue", "value_": operand}

        if isinstance(operand, numbers.Number):
            return {"type_": "Value", "value_": operand}

        if isinstance(operand, np.datetime64):
            val = np.datetime64(operand).astype("datetime64[s]").astype(np.float)
            return {"type_": "Value", "value_": val}

        if not hasattr(operand, "thisptr"):
            raise TypeError(
                """Operand for a VirtualBooleanColumn must be a 
                boolean, string, a number, a numpy.datetime64
                or a getml.data.Column!"""
            )

        if self.thisptr["operator_"] in ["and", "or", "not", "xor"]:
            if operand.thisptr["type_"] != "VirtualBooleanColumn":
                raise TypeError("This operator can only be applied to a BooleanColumn!")

        return operand.thisptr

    # -----------------------------------------------------------------------------

    def to_numpy(self):
        """
        Transform column to numpy array
        """

        # -------------------------------------------
        # Build command string

        cmd = dict()

        cmd["name_"] = self.thisptr["df_name_"]
        cmd["type_"] = "BooleanColumn.get"

        cmd["col_"] = self.thisptr

        # -------------------------------------------
        # Send command to engine

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        # -------------------------------------------
        # Make sure everything went well, receive data
        # and close connection

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        mat = comm.recv_boolean_matrix(sock)

        # -------------------------------------------
        # Close connection, if necessary.

        sock.close()

        # -------------------------------------------

        return mat.ravel()

    # -----------------------------------------------------------------------------

    def is_false(self):
        """Whether an entry is False - effectively inverts the Boolean column."""
        return VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="not",
            operand1=self,
            operand2=None,
        )

    # -----------------------------------------------------------------------------

    def as_num(self):
        """Transforms the boolean column into a numerical column"""
        return VirtualFloatColumn(
            df_name=self.thisptr["df_name_"],
            operator="boolean_as_num",
            operand1=self,
            operand2=None,
        )


# -----------------------------------------------------------------------------


class StringColumn(_Column):
    """Handle for categorical data that is kept in the getML engine

    Args:
        name (str, optional): Name of the categorical column.
        role (str, optional): Role that the column plays.
        num (int, optional): Number of the column.
        df_name (str, optional):

            ``name`` instance variable of the
            :class:`~getml.data.DataFrame` containing this column.

    Examples:

        .. code-block:: python

            import numpy as np

            import getml.data as data
            import getml.engine as engine
            import getml.data.roles as roles

            # ----------------

            engine.set_project("examples")

            # ----------------
            # Create a data frame from a JSON string

            json_str = \"\"\"{
                "names": ["patrick", "alex", "phil", "ulrike"],
                "column_01": [2.4, 3.0, 1.2, 1.4],
                "join_key": ["0", "1", "2", "3"],
                "time_stamp": ["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04"]
            }\"\"\"

            my_df = data.DataFrame(
                "MY DF",
                roles={
                    "unused_string": ["names", "join_key", "time_stamp"],
                    "unused_float": ["column_01"]}
            ).read_json(
                json_str
            )

            # ----------------

            col1 = my_df["names"]

            # ----------------

            col2 = col1.substr(4, 3)

            my_df.add(col2, "short_names", roles.categorical)

            # ----------------
            # If you do not explicitly set a role,
            # the assigned role will either be
            # roles.unused_string.

            col3 = "user-" + col1 + "-" + col2

            my_df["new_names"] = col3
            my_df.set_role("new_names", roles.categorical)
    """

    _num_columns = 0

    def __init__(self, name="", role="categorical", num=0, df_name=""):

        super(StringColumn, self).__init__()

        StringColumn._num_columns += 1
        if name == "":
            name = "StringColumn " + str(StringColumn._num_columns)

        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["name_"] = name

        self.thisptr["role_"] = role

        self.thisptr["type_"] = "StringColumn"


# -----------------------------------------------------------------------------


class VirtualStringColumn:
    """
    Handle to a (lazily evaluated) virtual string column.

    Virtual columns do not actually exist - they will be lazily
    evaluated when necessary.

    Examples:

        .. code-block:: python

            import numpy as np

            import getml.data as data
            import getml.engine as engine
            import getml.data.roles as roles

            # ----------------

            engine.set_project("examples")

            # ----------------
            # Create a data frame from a JSON string

            json_str = \"\"\"{
                "names": ["patrick", "alex", "phil", "ulrike"],
                "column_01": [2.4, 3.0, 1.2, 1.4],
                "join_key": ["0", "1", "2", "3"],
                "time_stamp": ["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04"]
            }\"\"\"

            my_df = data.DataFrame(
                "MY DF",
                roles={
                    "unused_string": ["names", "join_key", "time_stamp"],
                    "unused_float": ["column_01"]}
            ).read_json(
                json_str
            )

            # ----------------

            col1 = my_df["names"]

            # ----------------

            # col2 is a virtual column.
            # The substring operation is not
            # executed yet.
            col2 = col1.substr(4, 3)

            # This is where the engine executes
            # the substring operation.
            my_df.add(col2, "short_names", roles.categorical)

            # ----------------
            # If you do not explicitly set a role,
            # the assigned role will either be
            # roles.unused_string.

            # col3 is a virtual column.
            # The operation is not
            # executed yet.
            col3 = "user-" + col1 + "-" + col2

            # This is where the operation is
            # is executed.
            my_df["new_names"] = col3
            my_df.set_role("new_names", roles.categorical)
    """

    def __init__(self, df_name, operator, operand1, operand2):
        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["type_"] = "VirtualStringColumn"

        self.thisptr["operator_"] = operator

        if operand1 is not None:
            self.thisptr["operand1_"] = self._parse_operand(operand1)

        if operand2 is not None:
            self.thisptr["operand2_"] = self._parse_operand(operand2)

    # -----------------------------------------------------------------------------

    def _parse_operand(self, operand):

        if isinstance(operand, str):
            return {"type_": "CategoricalValue", "value_": operand}

        if not hasattr(operand, "thisptr"):
            raise TypeError(
                """Operand for a VirtualStringColumn must 
                   be a string or a column!"""
            )

        oper = self.thisptr["operator_"]
        optype = operand.thisptr["type_"]

        if oper == "as_str":
            wrong_coltype = optype not in [
                "FloatColumn",
                "VirtualFloatColumn",
                "VirtualBooleanColumn",
            ]
            if wrong_coltype:
                raise TypeError(
                    "This operator can only be applied to a FloatColumn or a BooleanColumn!"
                )

        else:
            wrong_coltype = optype not in ["StringColumn", "VirtualStringColumn"]
            if wrong_coltype:
                raise TypeError("This operator can only be applied to a StringColumn!")

        return operand.thisptr


# -----------------------------------------------------------------------------


class FloatColumn(_Column):
    """Handler for numerical data in the engine.

    This is a handler for all numerical data in the getML engine,
    including time stamps.

    Args:
        name (str, optional): Name of the categorical column.
        role (str, optional): Role that the column plays.
        num (int, optional): Number of the column.
        df_name (str, optional):

            ``name`` instance variable of the
            :class:`~getml.data.DataFrame` containing this column.

    Examples:

        .. code-block:: python

            import numpy as np

            import getml.data as data
            import getml.engine as engine
            import getml.data.roles as roles

            # ----------------

            engine.set_project("examples")

            # ----------------
            # Create a data frame from a JSON string

            json_str = \"\"\"{
                "names": ["patrick", "alex", "phil", "ulrike"],
                "column_01": [2.4, 3.0, 1.2, 1.4],
                "join_key": ["0", "1", "2", "3"],
                "time_stamp": ["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04"]
            }\"\"\"

            my_df = data.DataFrame(
                "MY DF",
                roles={
                    "unused_string": ["names", "join_key", "time_stamp"],
                    "unused_float": ["column_01"]}
            ).read_json(
                json_str
            )

            # ----------------

            col1 = my_df["column_01"]

            # ----------------

            col2 = 2.0 - col1

            my_df.add(col2, "name", roles.numerical)

            # ----------------
            # If you do not explicitly set a role,
            # the assigned role will either be
            # roles.unused_float.

            col3 = (col1 + 2.0*col2) / 3.0

            my_df["column_03"] = col3
            my_df.set_role("column_03", roles.numerical)
    """

    _num_columns = 0

    def __init__(self, name="", role="numerical", num=0, df_name=""):

        super(FloatColumn, self).__init__()

        FloatColumn._num_columns += 1
        if name == "":
            name = "FloatColumn " + str(FloatColumn._num_columns)

        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["name_"] = name

        self.thisptr["role_"] = role

        self.thisptr["type_"] = "FloatColumn"


# -----------------------------------------------------------------------------


class VirtualFloatColumn:
    """
    Handle to a (lazily evaluated) virtual float column.

    Virtual columns do not actually exist - they will be lazily
    evaluated when necessary.
    """

    def __init__(self, df_name, operator, operand1, operand2):
        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["type_"] = "VirtualFloatColumn"

        self.thisptr["operator_"] = operator

        if operand1 is not None:
            self.thisptr["operand1_"] = self._parse_operand(operand1)

        if operand2 is not None:
            self.thisptr["operand2_"] = self._parse_operand(operand2)

    # -----------------------------------------------------------------------------

    def _parse_operand(self, operand):

        if isinstance(operand, numbers.Number):
            return {"type_": "Value", "value_": operand}

        if isinstance(operand, np.datetime64):
            val = np.datetime64(operand).astype("datetime64[s]").astype(np.float)
            return {"type_": "Value", "value_": val}

        if not hasattr(operand, "thisptr"):
            raise TypeError(
                """Operand for a VirtualFloatColumn must 
                   be a number or a column!"""
            )

        special_ops = ["as_num", "as_ts", "boolean_as_num"]
        oper = self.thisptr["operator_"]
        optype = operand.thisptr["type_"]

        if oper not in special_ops:
            wrong_coltype = optype not in ["FloatColumn", "VirtualFloatColumn"]
            if wrong_coltype:
                raise TypeError("This operator can only be applied to a FloatColumn!")

        if oper in special_ops and oper != "boolean_as_num":
            wrong_coltype = optype not in ["StringColumn", "VirtualStringColumn"]
            if wrong_coltype:
                raise TypeError("This operator can only be applied to a StringColumn!")

        if oper == "boolean_as_num" and optype != "VirtualBooleanColumn":
            raise TypeError("This operator can only be applied to a BooleanColumn!")

        return operand.thisptr


# -----------------------------------------------------------------------------


def _abs(self):
    """Compute absolute value."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="abs", operand1=self, operand2=None
    )


FloatColumn.abs = _abs
VirtualFloatColumn.abs = _abs

# -----------------------------------------------------------------------------


def _acos(self):
    """Compute arc cosine."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="acos", operand1=self, operand2=None
    )


FloatColumn.acos = _acos
VirtualFloatColumn.acos = _acos


# -----------------------------------------------------------------------------


def _add(self, other):

    if (
        isinstance(other, StringColumn)
        or isinstance(other, VirtualStringColumn)
        or isinstance(other, str)
    ):
        return self.as_str() + other

    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="plus", operand1=self, operand2=other
    )


def _radd(self, other):

    if (
        isinstance(other, StringColumn)
        or isinstance(other, VirtualStringColumn)
        or isinstance(other, str)
    ):
        return other + self.as_str()

    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="plus", operand1=other, operand2=self
    )


FloatColumn.__add__ = _add
FloatColumn.__radd__ = _radd

VirtualFloatColumn.__add__ = _add
VirtualFloatColumn.__radd__ = _radd

# -----------------------------------------------------------------------------


def _alias(self, alias):
    """
    Adds an alias to the column. This is useful for joins.

    Args:
        alias (str): The name of the column as it should appear in the new DataFrame.
    """
    col = copy.deepcopy(self)
    col.thisptr["as_"] = alias
    return col


StringColumn.alias = _alias
FloatColumn.alias = _alias

# -----------------------------------------------------------------------------


def _assert_equal(self, alias="new_column"):
    """
    ASSERT EQUAL aggregation.

    Throws an exception unless all values inserted
    into the aggregation are equal.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "assert_equal")


FloatColumn.assert_equal = _assert_equal
VirtualFloatColumn.assert_equal = _assert_equal


# -----------------------------------------------------------------------------


def _asin(self):
    """Compute arc sine."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="asin", operand1=self, operand2=None
    )


FloatColumn.asin = _asin
VirtualFloatColumn.asin = _asin

# -----------------------------------------------------------------------------


def _atan(self):
    """Compute arc tangent."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="atan", operand1=self, operand2=None
    )


FloatColumn.atan = _atan
VirtualFloatColumn.atan = _atan

# -----------------------------------------------------------------------------


def _avg(self, alias="new_column"):
    """
    AVG aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "avg")


FloatColumn.avg = _avg
VirtualFloatColumn.avg = _avg

# -----------------------------------------------------------------------------


def _cbrt(self):
    """Compute cube root."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="cbrt", operand1=self, operand2=None
    )


FloatColumn.cbrt = _cbrt
VirtualFloatColumn.cbrt = _cbrt


# -----------------------------------------------------------------------------


def _ceil(self):
    """Round up value."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="ceil", operand1=self, operand2=None
    )


FloatColumn.ceil = _ceil
VirtualFloatColumn.ceil = _ceil

# -----------------------------------------------------------------------------


def _to_str(col):
    if isinstance(col, StringColumn) or isinstance(col, VirtualStringColumn):
        return col

    if (
        isinstance(col, FloatColumn)
        or isinstance(col, VirtualFloatColumn)
        or isinstance(col, VirtualBooleanColumn)
    ):
        return col.as_str()

    return str(col)


# -----------------------------------------------------------------------------


def _concat(self, other):
    return VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="concat",
        operand1=self,
        operand2=_to_str(other),
    )


def _rconcat(self, other):
    return VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="concat",
        operand1=_to_str(other),
        operand2=self,
    )


StringColumn.__add__ = _concat
StringColumn.__radd__ = _rconcat

VirtualStringColumn.__add__ = _concat
VirtualStringColumn.__radd__ = _rconcat

# -----------------------------------------------------------------------------


def _contains(self, other):
    """
    Returns a boolean column indicating whether a
    string or column entry is contained in the corresponding
    entry of the other column.
    """
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="contains",
        operand1=self,
        operand2=other,
    )


StringColumn.contains = _contains

VirtualStringColumn.contains = _contains

# -----------------------------------------------------------------------------


def _cos(self):
    """Compute cosine."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="cos", operand1=self, operand2=None
    )


FloatColumn.cos = _cos
VirtualFloatColumn.cos = _cos

# -----------------------------------------------------------------------------


def _count(self, alias="new_column"):
    """
    COUNT aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "count")


FloatColumn.count = _count
VirtualFloatColumn.count = _count

# -----------------------------------------------------------------------------


def _count_categorical(self, alias="new_column"):
    """
    COUNT aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "count_categorical")


StringColumn.count = _count_categorical
VirtualStringColumn.count = _count_categorical

# -----------------------------------------------------------------------------


def _count_distinct(self, alias="new_column"):
    """
    COUNT DISTINCT aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "count_distinct")


StringColumn.count_distinct = _count_distinct
VirtualStringColumn.count_distinct = _count_distinct

# -----------------------------------------------------------------------------


def _day(self):
    """Extract day (of the month) from a time stamp.

    If the column is numerical, that number will be interpreted as the
    number of seconds since epoch time (January 1, 1970).

    """
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="day", operand1=self, operand2=None
    )


FloatColumn.day = _day
VirtualFloatColumn.day = _day

# -----------------------------------------------------------------------------


def _eq(self, other):
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="equal_to",
        operand1=self,
        operand2=other,
    )


FloatColumn.__eq__ = _eq
VirtualFloatColumn.__eq__ = _eq

StringColumn.__eq__ = _eq
VirtualStringColumn.__eq__ = _eq

# -----------------------------------------------------------------------------


def _erf(self):
    """Compute error function."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="erf", operand1=self, operand2=None
    )


FloatColumn.erf = _erf
VirtualFloatColumn.erf = _erf

# -----------------------------------------------------------------------------


def _exp(self):
    """Compute exponential function."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="exp", operand1=self, operand2=None
    )


FloatColumn.exp = _exp
VirtualFloatColumn.exp = _exp

# -----------------------------------------------------------------------------


def _floor(self):
    """Round down value."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="floor", operand1=self, operand2=None
    )


FloatColumn.floor = _floor
VirtualFloatColumn.floor = _floor

# -----------------------------------------------------------------------------


def _gamma(self):
    """Compute gamma function."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="tgamma",
        operand1=self,
        operand2=None,
    )


FloatColumn.gamma = _gamma
VirtualFloatColumn.gamma = _gamma

# -----------------------------------------------------------------------------


def _ge(self, other):
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="greater_equal",
        operand1=self,
        operand2=other,
    )


FloatColumn.__ge__ = _ge
VirtualFloatColumn.__ge__ = _ge

# -----------------------------------------------------------------------------


def _gt(self, other):
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="greater",
        operand1=self,
        operand2=other,
    )


FloatColumn.__gt__ = _gt
VirtualFloatColumn.__gt__ = _gt

# -----------------------------------------------------------------------------


def _hour(self):
    """Extract hour (of the day) from a time stamp.

    If the column is numerical, that number will be interpreted as the
    number of seconds since epoch time (January 1, 1970).

    """
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="hour", operand1=self, operand2=None
    )


FloatColumn.hour = _hour
VirtualFloatColumn.hour = _hour

# -----------------------------------------------------------------------------


def _is_inf(self):
    """Determine whether the value is infinite."""
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="is_inf",
        operand1=self,
        operand2=None,
    )


FloatColumn.is_inf = _is_inf
VirtualFloatColumn.is_inf = _is_inf

# -----------------------------------------------------------------------------


def _is_nan(self):
    """Determine whether the value is nan."""
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="is_nan",
        operand1=self,
        operand2=None,
    )


FloatColumn.is_nan = _is_nan
VirtualFloatColumn.is_nan = _is_nan

FloatColumn.is_null = _is_nan
VirtualFloatColumn.is_null = _is_nan

# -----------------------------------------------------------------------------


def _is_null(self):
    """Determine whether the value is NULL."""
    return self == "NULL"


StringColumn.is_null = _is_null
VirtualStringColumn.is_null = _is_null

# -----------------------------------------------------------------------------


def _le(self, other):
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="less_equal",
        operand1=self,
        operand2=other,
    )


FloatColumn.__le__ = _le
VirtualFloatColumn.__le__ = _le

# -----------------------------------------------------------------------------


def _length(self):
    """The length of the column.
    This is identical to the result of the nrows() method of the DataFrame
    containing this column.
    Alternatively, you can call len(...).
    """

    # ------------------------------------------------------------
    # Build and send JSON command

    cmd = dict()
    cmd["type_"] = "DataFrame.nrows"
    cmd["name_"] = self.thisptr["df_name_"]

    sock = comm.send_and_receive_socket(cmd)

    # ------------------------------------------------------------
    # Make sure model exists on getml engine

    msg = comm.recv_string(sock)

    if msg != "Found!":
        sock.close()
        comm.engine_exception_handler(msg)

    # ------------------------------------------------------------
    # Receive number of rows from getml engine

    nrows = comm.recv_string(sock)

    # ------------------------------------------------------------

    sock.close()

    return np.int32(nrows)

    # ------------------------------------------------------------


VirtualBooleanColumn.__len__ = _length
VirtualFloatColumn.__len__ = _length
VirtualStringColumn.__len__ = _length
FloatColumn.__len__ = _length
StringColumn.__len__ = _length

#  -----------------------------------------------------------------------------


@property
def _length_property(self):
    """
    The length of the column (number of rows in the data frame).
    """
    return len(self)


VirtualBooleanColumn.length = _length_property
VirtualFloatColumn.length = _length_property
VirtualStringColumn.length = _length_property
FloatColumn.length = _length_property
StringColumn.length = _length_property

#  -----------------------------------------------------------------------------


def _lgamma(self):
    """Compute log-gamma function."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="lgamma",
        operand1=self,
        operand2=None,
    )


FloatColumn.lgamma = _lgamma
VirtualFloatColumn.lgamma = _lgamma

# -----------------------------------------------------------------------------


def _log(self):
    """Compute natural logarithm."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="log", operand1=self, operand2=None
    )


FloatColumn.log = _log
VirtualFloatColumn.log = _log

# -----------------------------------------------------------------------------


def _lt(self, other):
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"], operator="less", operand1=self, operand2=other
    )


FloatColumn.__lt__ = _lt
VirtualFloatColumn.__lt__ = _lt

# -----------------------------------------------------------------------------


def _make_body_part(self, start, max_rows):
    coltype = self.thisptr["type_"]

    coltype = coltype.replace("Virtual", "")

    body_part = _get_column_content(
        col=self.thisptr, coltype=coltype, start=start, length=max_rows
    )["data"]

    body_part = _add_index(body_part, begin=start, length=max_rows)

    return body_part


FloatColumn._make_body_part = _make_body_part
VirtualFloatColumn._make_body_part = _make_body_part
StringColumn._make_body_part = _make_body_part
VirtualStringColumn._make_body_part = _make_body_part
VirtualBooleanColumn._make_body_part = _make_body_part

# -----------------------------------------------------------------------------


def _make_footer(self):
    nrows = str(len(self)) + " rows"

    mytype = "type: " + str(type(self)).split("'")[1]

    if not hasattr(self, "name"):
        return [nrows, mytype]

    df_name = self.thisptr["df_name_"]

    url = "url: " + _monitor_url()
    url += (
        "getcolumn/" + comm._get_project_name() + "/" + df_name + "/" + self.name + "/"
    )

    return [nrows, mytype, url]


FloatColumn._make_footer = _make_footer
VirtualFloatColumn._make_footer = _make_footer
StringColumn._make_footer = _make_footer
VirtualStringColumn._make_footer = _make_footer
VirtualBooleanColumn._make_footer = _make_footer

# -----------------------------------------------------------------------------


def _make_head_body(self):

    max_rows = 5

    head = [["Name", ""], ["Role", ""]]

    if hasattr(self, "name"):
        head[0][1] = self.name

    if hasattr(self, "role"):
        head[1][1] = self.role

    if hasattr(self, "unit") and self.unit != "":
        head.append(["Unit", self.unit])

    nrows = len(self)

    if nrows <= max_rows * 2:
        body = self._make_body_part(start=0, max_rows=nrows)
        return head, body

    body_part1 = self._make_body_part(start=0, max_rows=max_rows)

    body_part2 = [[" ", "..."]]

    body_part3 = self._make_body_part(start=nrows - max_rows, max_rows=max_rows)

    body = body_part1 + body_part2 + body_part3

    return head, body


FloatColumn._make_head_body = _make_head_body
VirtualFloatColumn._make_head_body = _make_head_body
StringColumn._make_head_body = _make_head_body
VirtualStringColumn._make_head_body = _make_head_body
VirtualBooleanColumn._make_head_body = _make_head_body

# -----------------------------------------------------------------------------


def _max(self, alias="new_column"):
    """
    MAX aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "max")


FloatColumn.max = _max
VirtualFloatColumn.max = _max

# -----------------------------------------------------------------------------


def _median(self, alias="new_column"):
    """
    MEDIAN aggregation.

    **alias**: Name for the new column.
    """
    return Aggregation(alias, self, "median")


FloatColumn.median = _median
VirtualFloatColumn.median = _median

# -----------------------------------------------------------------------------


def _min(self, alias="new_column"):
    """
    MIN aggregation.

    **alias**: Name for the new column.
    """
    return Aggregation(alias, self, "min")


FloatColumn.min = _min
VirtualFloatColumn.min = _min

# -----------------------------------------------------------------------------


def _minute(self):
    """Extract minute (of the hour) from a time stamp.

    If the column is numerical, that number will be interpreted as the
    number of seconds since epoch time (January 1, 1970).

    """
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="minute",
        operand1=self,
        operand2=None,
    )


FloatColumn.minute = _minute
VirtualFloatColumn.minute = _minute

# -----------------------------------------------------------------------------


def _mod(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="fmod", operand1=self, operand2=other
    )


def _rmod(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="fmod", operand1=other, operand2=self
    )


FloatColumn.__mod__ = _mod
FloatColumn.__rmod__ = _rmod

VirtualFloatColumn.__mod__ = _mod
VirtualFloatColumn.__rmod__ = _rmod

# -----------------------------------------------------------------------------


def _month(self):
    """
    Extract month from a time stamp.

    If the column is numerical, that number will be interpreted
    as the number of seconds since epoch time (January 1, 1970).
    """
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="month", operand1=self, operand2=None
    )


FloatColumn.month = _month
VirtualFloatColumn.month = _month

# -----------------------------------------------------------------------------


def _mul(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="multiplies",
        operand1=self,
        operand2=other,
    )


FloatColumn.__mul__ = _mul
FloatColumn.__rmul__ = _mul

VirtualFloatColumn.__mul__ = _mul
VirtualFloatColumn.__rmul__ = _mul

# -----------------------------------------------------------------------------


def _ne(self, other):
    return VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="not_equal_to",
        operand1=self,
        operand2=other,
    )


FloatColumn.__ne__ = _ne
VirtualFloatColumn.__ne__ = _ne

StringColumn.__ne__ = _ne
VirtualStringColumn.__ne__ = _ne

# -----------------------------------------------------------------------------


def _neg(self):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="multiplies",
        operand1=self,
        operand2=-1.0,
    )


FloatColumn.__neg__ = _neg
VirtualFloatColumn.__neg__ = _neg

# -----------------------------------------------------------------------------


def _pow(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="pow", operand1=self, operand2=other
    )


def _rpow(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="pow", operand1=other, operand2=self
    )


FloatColumn.__pow__ = _pow
FloatColumn.__rpow__ = _rpow

VirtualFloatColumn.__pow__ = _pow
VirtualFloatColumn.__rpow__ = _rpow

# -----------------------------------------------------------------------------


def _repr(self):
    head, body = self._make_head_body()
    footer = self._make_footer()
    return _make_ascii_table(head, body) + "\n" + "\n".join(footer)


FloatColumn.__repr__ = _repr
VirtualFloatColumn.__repr__ = _repr

StringColumn.__repr__ = _repr
VirtualStringColumn.__repr__ = _repr

VirtualBooleanColumn.__repr__ = _repr

# -----------------------------------------------------------------------------


def _repr_html(self):
    head, body = self._make_head_body()
    footer = self._make_footer()
    footer = [_make_link(elem) for elem in footer]
    return _make_html_table(head, body) + "<br>" + "<br>".join(footer)


FloatColumn._repr_html_ = _repr_html
VirtualFloatColumn._repr_html_ = _repr_html

StringColumn._repr_html_ = _repr_html
VirtualStringColumn._repr_html_ = _repr_html

VirtualBooleanColumn._repr_html_ = _repr_html

# -----------------------------------------------------------------------------


def _round(self):
    """Round to nearest."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="round", operand1=self, operand2=None
    )


FloatColumn.round = _round
VirtualFloatColumn.round = _round

# -----------------------------------------------------------------------------


def _second(self):
    """Extract second (of the minute) from a time stamp.

    If the column is numerical, that number will be interpreted as the
    number of seconds since epoch time (January 1, 1970).

    """
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="second",
        operand1=self,
        operand2=None,
    )


FloatColumn.second = _second
VirtualFloatColumn.second = _second

# -----------------------------------------------------------------------------


def _sin(self):
    """Compute sine."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="sin", operand1=self, operand2=None
    )


FloatColumn.sin = _sin
VirtualFloatColumn.sin = _sin

# -----------------------------------------------------------------------------


def _sqrt(self):
    """Compute square root."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="sqrt", operand1=self, operand2=None
    )


FloatColumn.sqrt = _sqrt
VirtualFloatColumn.sqrt = _sqrt

# -----------------------------------------------------------------------------


def _stddev(self, alias="new_column"):
    """
    STDDEV aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "stddev")


FloatColumn.stddev = _stddev
VirtualFloatColumn.stddev = _stddev

# -----------------------------------------------------------------------------


def _sub(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="minus",
        operand1=self,
        operand2=other,
    )


def _rsub(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="minus",
        operand1=other,
        operand2=self,
    )


FloatColumn.__sub__ = _sub
FloatColumn.__rsub__ = _rsub

VirtualFloatColumn.__sub__ = _sub
VirtualFloatColumn.__rsub__ = _rsub


# -----------------------------------------------------------------------------


def _substr(self, begin, length):
    """
    Return a substring for every element in the column.

    Args:
        begin (int): First position of the original string.
        length (int): Length of the extracted string.
    """
    col = VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="substr",
        operand1=self,
        operand2=None,
    )
    col.thisptr["begin_"] = begin
    col.thisptr["len_"] = length
    return col


StringColumn.substr = _substr
VirtualStringColumn.substr = _substr

# -----------------------------------------------------------------------------


def _sum(self, alias="new_column"):
    """
    SUM aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "sum")


FloatColumn.sum = _sum
VirtualFloatColumn.sum = _sum

# -----------------------------------------------------------------------------


def _tan(self):
    """Compute tangent."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="tan", operand1=self, operand2=None
    )


FloatColumn.tan = _tan
VirtualFloatColumn.tan = _tan

# -----------------------------------------------------------------------------


def _as_num(self):
    """Transforms a categorical column to a numerical column."""
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="as_num",
        operand1=self,
        operand2=None,
    )


StringColumn.as_num = _as_num
VirtualStringColumn.as_num = _as_num

# -----------------------------------------------------------------------------


def _to_numpy(self, sock=None):
    """
    Transform column to numpy array

    Args:
        sock (optional): Socket connecting the Python API with the getML
            engine.
    """

    # -------------------------------------------
    # Build command string

    cmd = dict()

    cmd["name_"] = self.thisptr["df_name_"]
    cmd["type_"] = "FloatColumn.get"

    cmd["col_"] = self.thisptr

    # -------------------------------------------
    # Establish communication with getml engine

    if sock is None:
        sock2 = comm.send_and_receive_socket(cmd)
    else:
        sock2 = sock
        comm.send_string(sock2, json.dumps(cmd))

    msg = comm.recv_string(sock2)

    # -------------------------------------------
    # Make sure everything went well, receive data
    # and close connection

    if msg != "Found!":
        sock2.close()
        comm.engine_exception_handler(msg)

    mat = comm.recv_matrix(sock2)

    # -------------------------------------------
    # Close connection.

    if sock is None:
        sock2.close()

    # -------------------------------------------
    # If this is a time stamp, then transform to
    # pd.Timestamp.

    if self.thisptr["type_"] == "FloatColumn":
        if self.thisptr["role_"] == "time_stamp":
            shape = mat.shape
            mat = [
                np.datetime64(datetime.datetime.utcfromtimestamp(ts))
                for ts in mat.ravel()
            ]
            mat = np.asarray(mat)
            mat.reshape(shape[0], shape[1])

    # -------------------------------------------

    return mat.ravel()

    # -------------------------------------------


FloatColumn.to_numpy = _to_numpy
VirtualFloatColumn.to_numpy = _to_numpy

# -----------------------------------------------------------------------------


def _to_numpy_categorical(self, sock=None):
    """
    Transform column to numpy array

    Args:
        sock (optional): Socket connecting the Python API with the getML
            engine.
    """

    # -------------------------------------------
    # Build command string

    cmd = dict()

    cmd["name_"] = self.thisptr["df_name_"]
    cmd["type_"] = "StringColumn.get"

    cmd["col_"] = self.thisptr

    # -------------------------------------------
    # Send command to engine

    if sock is None:
        sock2 = comm.send_and_receive_socket(cmd)
    else:
        sock2 = sock
        comm.send_string(sock2, json.dumps(cmd))

    msg = comm.recv_string(sock2)

    # -------------------------------------------
    # Make sure everything went well, receive data
    # and close connection

    if msg != "Found!":
        sock2.close()
        comm.engine_exception_handler(msg)

    mat = comm.recv_categorical_matrix(sock2)

    # -------------------------------------------
    # Close connection.
    if sock is None:
        sock2.close()

    # -------------------------------------------

    return mat.ravel()


StringColumn.to_numpy = _to_numpy_categorical
VirtualStringColumn.to_numpy = _to_numpy_categorical

# -----------------------------------------------------------------------------


def _as_str(self):
    """Transforms column to a string."""
    return VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="as_str",
        operand1=self,
        operand2=None,
    )


FloatColumn.as_str = _as_str
VirtualFloatColumn.as_str = _as_str

VirtualBooleanColumn.as_str = _as_str

# -----------------------------------------------------------------------------


def _as_ts(self, time_formats=None):
    """
    Transforms a categorical column to a time stamp.

    Args:
        time_formats (str): Formats to be used to parse the time stamps.
    """
    time_formats = time_formats or constants.TIME_FORMATS
    col = VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="as_ts", operand1=self, operand2=None
    )
    col.thisptr["time_formats_"] = time_formats
    return col


StringColumn.as_ts = _as_ts
VirtualStringColumn.as_ts = _as_ts

# -----------------------------------------------------------------------------


def _truediv(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="divides",
        operand1=self,
        operand2=other,
    )


def _rtruediv(self, other):
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="divides",
        operand1=other,
        operand2=self,
    )


FloatColumn.__truediv__ = _truediv
FloatColumn.__rtruediv__ = _rtruediv

VirtualFloatColumn.__truediv__ = _truediv
VirtualFloatColumn.__rtruediv__ = _rtruediv

# -----------------------------------------------------------------------------


def _update(self, condition, values):
    """
    Returns an updated version of this column.

    All entries for which the corresponding **condition** is True,
    are updated using the corresponding entry in **values**.

    Args:
        condition (Boolean column): Condition according to which the update is done
        values: Values to update with
    """
    col = VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="update",
        operand1=self,
        operand2=values,
    )
    if condition.thisptr["type_"] != "VirtualBooleanColumn":
        raise TypeError("Condition for an update must be a Boolen column.")
    col.thisptr["condition_"] = condition.thisptr
    return col


FloatColumn.update = _update

VirtualFloatColumn.update = _update

# -----------------------------------------------------------------------------


def _update_categorical(self, condition, values):
    """
    Returns an updated version of this column.

    All entries for which the corresponding **condition** is True,
    are updated using the corresponding entry in **values**.

    Args:
        condition (Boolean column): Condition according to which the update is done
        values: Values to update with
    """
    col = VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="update",
        operand1=self,
        operand2=values,
    )
    if condition.thisptr["type_"] != "VirtualBooleanColumn":
        raise TypeError("Condition for an update must be a Boolean column.")
    col.thisptr["condition_"] = condition.thisptr
    return col


StringColumn.update = _update_categorical

VirtualStringColumn.update = _update_categorical

# -----------------------------------------------------------------------------


def _var(self, alias="new_column"):
    """
    VAR aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return Aggregation(alias, self, "var")


FloatColumn.var = _var
VirtualFloatColumn.var = _var

# -----------------------------------------------------------------------------


def _weekday(self):
    """Extract day of the week from a time stamp, Sunday being 0.

    If the column is numerical, that number will be interpreted as the
    number of seconds since epoch time (January 1, 1970).

    """
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="weekday",
        operand1=self,
        operand2=None,
    )


FloatColumn.weekday = _weekday
VirtualFloatColumn.weekday = _weekday

# -----------------------------------------------------------------------------


def _year(self):
    """
    Extract year from a time stamp.

    If the column is numerical, that number will be interpreted
    as the number of seconds since epoch time (January 1, 1970).
    """
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"], operator="year", operand1=self, operand2=None
    )


FloatColumn.year = _year
VirtualFloatColumn.year = _year

# -----------------------------------------------------------------------------


def _yearday(self):
    """
    Extract day of the year from a time stamp.

    If the column is numerical, that number will be interpreted
    as the number of seconds since epoch time (January 1, 1970).
    """
    return VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="yearday",
        operand1=self,
        operand2=None,
    )


FloatColumn.yearday = _yearday
VirtualFloatColumn.yearday = _yearday


# -----------------------------------------------------------------------------
