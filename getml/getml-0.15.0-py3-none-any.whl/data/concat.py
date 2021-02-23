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
Creates a new data frame by concatenating a list of existing ones.
"""

import getml.communication as comm

from .data_frame import DataFrame
from .helpers import _is_non_empty_typed_list

# --------------------------------------------------------------------


def concat(name, data_frames):
    """
    Creates a new data frame by concatenating a list of existing ones.

    Args:
        name (str): Name of the new column.

        data_frames(List[:class:`~getml.data.DataFrame`]): The data frames to concatenate.
            Must be non-empty. However, it can contain only one data frame.
            Column names and roles must match. Columns will be appended by name, not order.

    Example:

        >>> new_df = data.concat("NEW_DF_NAME", [df1, df2])
    """

    if not isinstance(name, str):
        raise TypeError("'name' must be a string.")

    if not _is_non_empty_typed_list(data_frames, DataFrame):
        raise TypeError("'data_frames' must be a non-empty list of data frames.")

    cmd = dict()
    cmd["type_"] = "DataFrame.concat"
    cmd["name_"] = name

    cmd["df_names_"] = [df.name for df in data_frames]

    comm.send(cmd)

    return DataFrame(name=name).refresh()


# --------------------------------------------------------------------
