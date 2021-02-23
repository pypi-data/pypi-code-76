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

"""Lists all hyperparameter optimization objects present in the engine."""

import json

import getml.communication as comm

# --------------------------------------------------------------------


def list_hyperopts():
    """Lists all hyperparameter optimization objects present in the engine.

    Note that this function only lists hyperopts which are part of the
    current project. See :func:`~getml.engine.set_project` for
    changing projects.

    To subsequently load one of them, use
    :func:`~getml.hyperopt.load_hyperopt`.

    Raises:
        IOError: If command could not be processed by the engine.

    Returns:
        list containing the names of all hyperopts.
    """

    cmd = dict()
    cmd["type_"] = "list_hyperopts"
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


def exists(name):
    """Determines whether an hyperopt exists.

    Args:
        name (str): The name of the hyperopt.

    Returns:
        A boolean indicating whether a hyperopt named *name* exists.
    """
    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    return name in list_hyperopts()


# --------------------------------------------------------------------


def delete(name):
    """
    If a hyperopt named 'name' exists, it is deleted.

    Args:
        name (str): The name of the hyperopt.
    """
    # ----------------------------------------------------------------

    if not exists(name):
        return

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "Hyperopt.delete"
    cmd["name_"] = name

    # ----------------------------------------------------------------

    sock = comm.send_and_receive_socket(cmd)

    # ----------------------------------------------------------------

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # ----------------------------------------------------------------

    sock.close()
