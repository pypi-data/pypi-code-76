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

"""Helper functions that depend on the DataFrame class."""

from .data_frame import DataFrame
from .helpers import list_data_frames

# --------------------------------------------------------------------


def load_data_frame(name):
    """Retrieves a :class:`~getml.data.DataFrame` handler of data in the
    getML engine.

    A data frame object can be loaded regardless if it is held in
    memory (accessible through the 'Data Frames' tab in the getML
    monitor) or not. It only has to be present in the current project
    and thus listed in the output of
    :func:`~getml.data.list_data_frames`.

    Args:
        name (str):
            Name of the data frame.

    Examples:

        .. code-block:: python

            d, _ = getml.datasets.make_numerical(population_name = 'test')
            d2 = getml.data.load_data_frame('test')


    Raises:
        TypeError: If any of the input arguments is of wrong type.

        ValueError:

            If `name` does not corresponding to a data frame on the
            engine.

    Returns:
        :class:`~getml.data.DataFrame`:
            Handle the underlying data frame in the getML engine.

    Note:

        The getML engine knows to different states of a data frame
        object. First, the current instance in memory (RAM) that
        holds the most recent changes applied via the Python API
        (listed under the 'in_memory' key of
        :func:`~getml.data.list_data_frames`). Second, the
        version stored to disk by calling the
        :meth:`~getml.data.DataFrame.save` method (listed under the
        'in_project_folder' key). If a data frame object corresponding
        to `name` is present in both of them, the most recent version
        held in memory is loaded. To load the one from memory instead,
        you use the :meth:`~getml.data.DataFrame.load` method.

        In order to load a data frame object from a different project,
        you have to switch projects first. Caution: any changes
        applied after the last call to
        :meth:`~getml.data.DataFrame.save` will be lost. See
        :func:`~getml.engine.set_project` and
        :class:`~getml.data.DataFrame` for more details about the
        lifecycles of the models.

    """

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    data_frames_available = list_data_frames()

    # First, attempt to load a data frame held in memory.
    if name in data_frames_available["in_memory"]:
        return DataFrame(name).refresh()

    if name in data_frames_available["in_project_folder"]:
        return DataFrame(name).load()

    raise ValueError(
        "No data frame holding the name '" + name + "' present on the getML engine"
    )


# --------------------------------------------------------------------


def exists(name):
    """
    Returns true if a data frame named 'name' exists.

    Args:
        name (str):
            Name of the data frame.
    """
    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    all_df = list_data_frames()

    return name in (all_df["in_memory"] + all_df["in_project_folder"])


# --------------------------------------------------------------------


def delete(name):
    """
    If a data frame named 'name' exists, it is deleted.

    Args:
        name (str):
            Name of the data frame.
    """

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    if exists(name):
        DataFrame(name).delete()


# --------------------------------------------------------------------
