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
Contains various helper functions related to the getML engine.
"""

import json
import socket

import getml.communication as comm

# --------------------------------------------------------------------


def delete_project(name):
    """Deletes a project.

    Args:
        name (str): Name of your project.

    Raises:
        TypeError: If any of the input arguments is of wrong type.

    Note:

        All data and models contained in the project directory will be
        permanently lost.

    """
    comm._delete_project(name)


# -----------------------------------------------------------------------------


def is_engine_alive():
    """Checks if the getML engine is running.

    Returns:
        bool:

            True if the getML engine is running and ready to accept
            commands and False otherwise.

    """

    # ---------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "is_alive"
    cmd["name_"] = ""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("localhost", comm.port))
    except ConnectionRefusedError:
        return False

    comm.send_string(sock, json.dumps(cmd))

    sock.close()

    return True


# define compatability alias
is_alive = is_engine_alive

# -----------------------------------------------------------------------------


def is_monitor_alive():
    """Checks if the getML monitor is running.

    Returns:
        bool:

            True if the getML monitor is running and ready to accept
            commands and False otherwise.
    """

    # ---------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", comm.tcp_port))
    except ConnectionRefusedError:
        return False

    sock.close()

    return True


# -----------------p------------------------------------------------------------


def list_projects():
    """
    List all projects on the getML engine.

    Raises:
        IOError:
            If an error in the communication with the getML engine
            occurred.

    Returns:
        List[str]: Lists the name all of the projects.
    """
    return comm._list_projects_impl(running_only=False)


# -----------------------------------------------------------------------------


def list_running_projects():
    """
    List all projects on the getML engine that are currently running.

    Raises:
        IOError:
            If an error in the communication with the getML engine
            occurred.

    Returns:
        List[str]: Lists the name all of the projects currently running.
    """
    return comm._list_projects_impl(running_only=True)


# -----------------------------------------------------------------------------


def restart_project(name):
    """
    Suspends and then relaunches the currently connected project.
    This will kill all jobs currently running on that process.

    Args:
        name (str): Name of the new project.

    Raises:
        ConnectionRefusedError: If unable to connect to engine
        TypeError: If any of the input arguments is of wrong type.
    """
    comm._set_project(name, restart=True)


# -----------------------------------------------------------------------------


def set_project(name):
    """Creates a new project or loads an existing one.

    If there is no project called `name` present on the engine, a new one will
    be created. See the :ref:`User guide <the_getml_engine_projects>` for more
    information.

    Args:
        name (str): Name of the new project.

    Raises:
        ConnectionRefusedError: If unable to connect to engine
        TypeError: If any of the input arguments is of wrong type.
    """
    comm._set_project(name)


# -----------------------------------------------------------------------------


def set_s3_access_key_id(value):
    """Sets the Access Key ID to S3.

    NOTE THAT S3 IS NOT SUPPORTED ON WINDOWS.

    In order to retrieve data from S3, you need to set the Access Key ID
    and the Secret Access Key. You can either set them as environment
    variables before you start the getML engine or you can set them from
    this module.

    Args:
        value (str): The value to which you want to set the Access Key ID.

    Raises:
        ConnectionRefusedError: If unable to connect to engine
        TypeError: If any of the input arguments is of wrong type.
    """

    if not isinstance(value, str):
        raise TypeError("'value' must be of type str")

    if not is_alive():
        raise ConnectionRefusedError(
            """
        Cannot connect to getML engine.
        Make sure the engine is running on port '"""
            + str(comm.port)
            + """' and you are logged in.
        See `help(getml.engine)`."""
        )

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "set_s3_access_key_id"
    cmd["name_"] = ""

    sock = comm.send_and_receive_socket(cmd)

    comm.send_string(sock, value)

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)


# -----------------------------------------------------------------------------


def set_s3_secret_access_key(value):
    """Sets the Secret Access Key to S3.

    NOTE THAT S3 IS NOT SUPPORTED ON WINDOWS.

    In order to retrieve data from S3, you need to set the Access Key ID
    and the Secret Access Key. You can either set them as environment
    variables before you start the getML engine or you can set them from
    this module.

    Args:
        value (str): The value to which you want to set the Secret Access Key.

    Raises:
        ConnectionRefusedError: If unable to connect to engine
        TypeError: If any of the input arguments is of wrong type.
    """

    if not isinstance(value, str):
        raise TypeError("'value' must be of type str")

    if not is_alive():
        raise ConnectionRefusedError(
            """
        Cannot connect to getML engine.
        Make sure the engine is running on port '"""
            + str(comm.port)
            + """' and you are logged in.
        See `help(getml.engine)`."""
        )

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "set_s3_secret_access_key"
    cmd["name_"] = ""

    sock = comm.send_and_receive_socket(cmd)

    comm.send_string(sock, value)

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)


# -----------------------------------------------------------------------------


def shutdown():
    """Shuts down the getML engine.

    Raises:
        ConnectionRefusedError: If unable to connect to engine

    Note:

        All changes applied to the :class:`~getml.data.DataFrame`
        after calling their :meth:`~getml.data.DataFrame.save`
        method will be lost.

    """
    comm._shutdown()


# --------------------------------------------------------------------


def suspend_project(name):
    """Suspends a project that is currently running.

    Args:
        name (str): Name of your project.

    Raises:
        TypeError: If any of the input arguments is of wrong type.

    Note:

        All data and models contained in the project directory will be
        permanently lost.

    """
    comm._suspend_project(name)


# -----------------------------------------------------------------------------
