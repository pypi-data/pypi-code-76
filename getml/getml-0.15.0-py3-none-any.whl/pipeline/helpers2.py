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
Helper functions that depend on Pipeline.
"""

import json

import getml.communication as comm
from getml.data import Placeholder
from getml.data.helpers import _remove_trailing_underscores

from .pipeline import Pipeline

# --------------------------------------------------------------------


def _make_dummy(name):
    dummy = Placeholder(name="dummy")
    dummy2 = Placeholder(name="dummy2")
    dummy.join(dummy2, join_key="join_key")

    pipeline = Pipeline(population=dummy, peripheral=dummy2)
    pipeline._id = name

    return pipeline


# --------------------------------------------------------------------


def _from_json(json_obj):
    pipe = _make_dummy("dummy")
    pipe._parse_json_obj(json_obj)
    return pipe


# --------------------------------------------------------------------


def _refresh_all():

    cmd = dict()
    cmd["type_"] = "Pipeline.refresh_all"
    cmd["name_"] = ""

    # ----------------------------------------------------------------

    sock = comm.send_and_receive_socket(cmd)

    # ----------------------------------------------------------------

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # ----------------------------------------------------------------

    json_str = comm.recv_string(sock)

    # ----------------------------------------------------------------

    sock.close()

    # ----------------------------------------------------------------

    json_obj = json.loads(json_str)

    return [_from_json(obj) for obj in json_obj["pipelines"]]


# --------------------------------------------------------------------


def list_pipelines():
    """Lists all pipelines present in the engine.

    Note that this function only lists pipelines which are part of the
    current project. See :func:`~getml.engine.set_project` for
    changing projects and :mod:`~getml.pipelines` for more details about
    the lifecycles of the pipelines.

    To subsequently load one of them, use
    :func:`~getml.pipeline.load`.

    Raises:
        IOError: If command could not be processed by the engine.

    Returns:
        list containing the names of all pipelines.
    """

    cmd = dict()
    cmd["type_"] = "list_pipelines"
    cmd["name_"] = ""

    # ----------------------------------------------------------------

    sock = comm.send_and_receive_socket(cmd)

    # ----------------------------------------------------------------

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # ----------------------------------------------------------------

    json_str = comm.recv_string(sock)

    # ----------------------------------------------------------------

    sock.close()

    # ----------------------------------------------------------------

    return json.loads(json_str)["names"]


# --------------------------------------------------------------------


def load(name):
    """Loads a pipeline from the getML engine into Python.

    Args:
        name: The name of the pipeline to be loaded.

    Returns:
        A :meth:`~getml.pipeline.Pipeline` that is a handler
        for the pipeline signified by name.
    """

    return _make_dummy(name).refresh()


# --------------------------------------------------------------------


def exists(name):
    """
    Returns true if a pipeline named 'name' exists.

    Args:
        name (str):
            Name of the pipeline.
    """
    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    all_pipelines = list_pipelines()

    return name in all_pipelines


# --------------------------------------------------------------------


def delete(name):
    """
    If a pipeline named 'name' exists, it is deleted.

    Args:
        name (str):
            Name of the pipeline.
    """

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    if exists(name):
        _make_dummy(name).delete()


# --------------------------------------------------------------------
