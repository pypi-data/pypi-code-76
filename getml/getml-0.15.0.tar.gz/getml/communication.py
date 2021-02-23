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
Handles the communication for the getML library
"""

import json
import numbers
import socket
import sys

import numpy as np

from getml.engine import is_monitor_alive
from getml.log import logger

# --------------------------------------------------------------------
port = 1708
"""
The port of the getML engine. The port is automaticallly set according to the process spawned
when setting a project. The monitor automatically looks up a free port (starting from 1708).
Setting the port here has no effect.
"""

tcp_port = 1711
"""
The TCP port of the getML monitor.
"""

# --------------------------------------------------------------------

ENGINE_CANNOT_CONNECT_ERROR_MSG = (
    """Cannot reach the getML engine. Please make sure you have set a project."""
)
MONITOR_CANNOT_CONNECT_ERROR_MSG = (
    """Cannot reach the getML monitor. Please make sure the getML app is running."""
)


# --------------------------------------------------------------------


class _Encoding:
    """
    Maps strings to integers, so we can speed up the sending
    of string columns.
    """

    def __init__(self):
        self.map = dict()
        self.vec = []

    def __getitem__(self, key):
        if key in self.map:
            return self.map[key]

        val = len(self.vec)
        self.map[key] = val
        self.vec.append(key)
        return val


# --------------------------------------------------------------------


class _GetmlEncoder(json.JSONEncoder):
    """Enables a custom serialization of the getML classes."""

    def default(self, obj):
        """Checks for the particular type of the provided object and
        deserializes it into an escaped string.

        To ensure the getML can handle all keys, we have to add a
        trailing underscore.

        Args:
            obj: Any of the classes defined in the getml package.

        Returns:
            string:
                Encoded JSON.

        Examples:
            Create a :class:`~getml.predictors.LinearRegression`,
            serialize it, and deserialize it again.

            .. code-block:: python

                p = getml.predictors.LinearRegression()
                p_serialized = json.dumps(
                    p, cls = getml.communication._GetmlEncoder)
                p2 = json.loads(
                    p_serialized,
                    object_hook=getml.helpers.predictors._decode_predictor
                )
                p == p2

        """

        if hasattr(obj, "_getml_deserialize"):
            return obj._getml_deserialize()

        return json.JSONEncoder.default(self, obj)


# --------------------------------------------------------------------


class _ProgressBar:
    """Displays progress in bar form."""

    def __init__(self):
        self.length = 40

    def show(self, progress):
        """Displays an updated version of the progress bar.

        Args:
            progress (float): The progress to be shown. Must
                be between 0 and 100.
        """
        done = int(progress * self.length / 100.0)

        remaining = self.length - done

        pbar = "[" + "=" * done
        pbar += " " * remaining + "] "
        pbar += str(progress) + "%"

        print(pbar, end="\r", flush=True)

        if progress == 100:
            print()


# --------------------------------------------------------------------


def _make_error_msg():
    if not is_monitor_alive():
        return MONITOR_CANNOT_CONNECT_ERROR_MSG
    else:
        msg = ENGINE_CANNOT_CONNECT_ERROR_MSG
        msg += "\n\nTo set: `getml.engine.set_project`"
        return msg


# --------------------------------------------------------------------


def engine_exception_handler(msg, fallback=""):
    """Looks at the error message thrown by the engine and decides whether
    to throw a corresponding Exception using the same string or
    altering the message first.

    In either way, this function will always throw some sort of Exception.

    Args:

        msg (str): Error message returned by the getML engine.
        fallback (str):

            If not empty, the default Exception will carry this
            string.

    Raises:

        IOError: In any case.

    """

    if not fallback:
        fallback = msg

    raise IOError(fallback)


# --------------------------------------------------------------------


def recv_data(sock, size):
    """Receives data (of any type) sent by the getml engine.

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`
            or `size` is not a number.
        RuntimeError: If no data could be received from the engine.
    """

    # ----------------------------------------------------------------

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    if not isinstance(size, numbers.Real):
        raise TypeError("'size' must be a number.")

    # ----------------------------------------------------------------

    data = []

    bytes_received = np.uint64(0)

    max_chunk_size = np.uint64(2048)

    while bytes_received < size:

        current_chunk_size = int(min(size - bytes_received, max_chunk_size))

        chunk = sock.recv(current_chunk_size)

        if not chunk:
            raise IOError(
                """The getML engine died unexpectedly.
                    If this wasn't done on purpose, please get in contact
                    with our support or file a bug report."""
            )

        data.append(chunk)

        bytes_received += np.uint64(len(chunk))

    return "".encode().join(data)


# --------------------------------------------------------------------


def recv_boolean_matrix(sock):
    """Receives a matrix (type boolean) from the getml engine.

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    # ----------------------------------------------------------------

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).byteswap().astype(np.uint64)

        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.int32])

        matrix = recv_data(sock, size)

        matrix = np.frombuffer(matrix, dtype=np.int32).byteswap()

        matrix = matrix.reshape(shape[0], shape[1])

    else:
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).astype(np.uint64)

        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.int32])

        matrix = recv_data(sock, size)

        matrix = np.frombuffer(matrix, dtype=np.int32)

        matrix = matrix.reshape(shape[0], shape[1])

    return matrix == 1


# --------------------------------------------------------------------


def recv_matrix(sock):
    """
    Receives a matrix (type np.float64) from the getml engine.

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    # ----------------------------------------------------------------

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).byteswap().astype(np.uint64)

        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.float64])

        matrix = recv_data(sock, size)

        matrix = np.frombuffer(matrix, dtype=np.float64).byteswap()

        matrix = matrix.reshape(shape[0], shape[1])

    else:
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).astype(np.uint64)

        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.float64])

        matrix = recv_data(sock, size)

        matrix = np.frombuffer(matrix, dtype=np.float64)

        matrix = matrix.reshape(shape[0], shape[1])

    return matrix


# --------------------------------------------------------------------


def recv_string(sock):
    """
    Receives a string from the getml engine
    (an actual string, not a bytestring).

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    # ----------------------------------------------------------------

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":

        size_str = recv_data(sock, np.nbytes[np.int32])

        size = np.frombuffer(size_str, dtype=np.int32).byteswap()[0]

    else:
        size_str = recv_data(sock, np.nbytes[np.int32])

        size = np.frombuffer(size_str, dtype=np.int32)[0]

    data = recv_data(sock, size)

    return data.decode(errors="ignore")


# --------------------------------------------------------------------


def recv_warnings(sock):
    """
    Receives a set of warnings to raise from the getml engine.

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    json_str = recv_string(sock)

    if json_str[0] != "{":
        raise ValueError(json_str)

    json_obj = json.loads(json_str)

    all_warnings = json_obj["warnings_"]

    for warning in all_warnings:
        if "WARNING" in warning:
            logger.warning(warning)
        elif "INFO" in warning:
            logger.info(warning)

    return len(all_warnings) == 0


# --------------------------------------------------------------------

# Depends on recv_string, so it is not in alphabetical order.


def recv_categorical_matrix(sock):
    """
    Receives a matrix of type string from the getml engine

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    # ----------------------------------------------------------------
    # Receive shape

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).byteswap().astype(np.uint64)

        size = shape[0] * shape[1]

    else:
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).astype(np.uint64)

        size = shape[0] * shape[1]

    # ----------------------------------------------------------------
    # Receive actual strings

    mat = []

    for _ in range(size):
        mat.append(recv_string(sock))

    # ----------------------------------------------------------------
    # Cast as numpy.array and reshape

    mat = np.asarray(mat)

    return mat.reshape(shape[0], shape[1])


# --------------------------------------------------------------------


def send(cmd):
    """Sends a command to the getml engine and closes the established
    connection.

    Creates a socket and sends a command to the getML engine using the
    module-wide variable :py:const:`~getml.port`.

    A message (string) from the :py:class:`socket.socket` will be
    received using :py:func:`~getml.recv_string` and the socket will
    be closed. If the message is "Success!", everything work
    properly. Else, an Exception will be thrown containing the
    message.

    In case another message is supposed to be send by the engine,
    :py:func:`~getml.communication.send_and_receive_socket` has to be used
    and the calling function must handle the message itself!

    Please be very careful when altering the routing/calling behavior
    of the socket communication! The engine might react in a quite
    sensible and freezing way.

    Arg:
        cmd (dict): A dictionary specifying the command the engine is
            supposed to execute. It _must_ contain at least two string
            values with the corresponding keys being named "name_" and
            "type_".

    Raises:
        Exception: If the message received from the engine is not
            "Success!
        TypeError: If `cmd` is not a dict.
        ConnectionRefusedError: If the getML is unreachable.

    """

    if not isinstance(cmd, dict):
        raise TypeError("'cmd' must be a dict.")

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("localhost", port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    # Use a custom encoder which knows how to handle the classes
    # defined in the getml package.
    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ---------------------------------------------------------------
    # The calling function does not want to further use the
    # socket. Therefore, it will be checked here whether the
    # request was successful and closed.
    msg = recv_string(sock)

    sock.close()

    if msg != "Success!":
        engine_exception_handler(msg)


# --------------------------------------------------------------------


def send_and_receive_socket(cmd):
    """Sends a command to the getml engine and returns the established
    connection.

    Creates a socket and sends a command to the getML engine using the
    module-wide variable :py:const:`~getml.port`.

    The function will return the socket it opened and the calling
    function is free to receive whatever data is desires over it. But
    the latter has also to take care of closing the socket afterwards
    itself!

    Please be very careful when altering the routing/calling behavior
    of the socket communication! The engine might react in a quite
    sensible and freezing way. Especially implemented handling of
    socket sessions (their passing from function to function) must not
    be altered or separated in distinct calls to the
    :py:func:`~getml.communication.send` function! Some commands have
    to be send via the same socket or the engine will not be able to
    handle them and might block.

    Arg:
        cmd (dict): A dictionary specifying the command the engine is
            supposed to execute. It _must_ contain at least two string
            values with the corresponding keys being named "name_" and
            "type_"."

    Returns:
        :py:class:`socket.socket`: A socket using which the Python API
            can communicate with the getML engine.

    Raises:
        TypeError: If `cmd` is not a dict.
        ConnectionRefusedError: If the getML is unreachable.

    """

    if not isinstance(cmd, dict):
        raise TypeError("'cmd' must be a dict.")

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("localhost", port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    # Use a custom encoder which knows how to handle the classes
    # defined in the getml package.
    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    return sock


# --------------------------------------------------------------------


def send_categorical_matrix(sock, categorical_matrix):
    """Sends a list of strings to the getml engine
    (an actual string, not a bytestring).

    Raises:
        TypeError: If the input is not of proper type.
        Exception: If the dimension of `categorical_matrix` is larger
            than two.
    """

    # ----------------------------------------------------------------

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    if not isinstance(categorical_matrix, np.ndarray):
        raise TypeError("'categorical_matrix' must be a numpy.ndarray.")

    if len(categorical_matrix.shape) > 2 or len(categorical_matrix.shape) == 0:
        raise Exception("Numpy array must be one-dimensional or two-dimensional!")

    if len(categorical_matrix.shape) == 2 and categorical_matrix.shape[1] != 1:
        raise Exception("Numpy array must be single column!")

    # ----------------------------------------------------------------

    encoding = _Encoding()

    integers = [
        encoding[string.encode("utf-8")]
        for string in categorical_matrix.astype(str).flatten()
    ]

    integers = np.asarray(integers).astype(np.int32)

    # ----------------------------------------------------------------

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":
        # Create the shape
        shape = [integers.shape[0], 1]

        # Send the shape.
        sock.sendall(np.asarray(shape).astype(np.int32).byteswap().tostring())

        # Send the integers
        sock.sendall(integers.byteswap().tostring())

        # Create the raw data
        raw_data = "".encode().join(
            [
                np.asarray(len(elem)).astype(np.int32).byteswap().tostring() + elem
                for elem in encoding.vec
            ]
        )

        # Create the shape
        shape = [len(encoding.vec), len(raw_data)]

        # Send the shape.
        sock.sendall(np.asarray(shape).astype(np.int32).byteswap().tostring())

        # Send the raw data
        sock.sendall(raw_data)

    else:
        # Create the shape
        shape = [integers.shape[0], 1]

        # Send the shape.
        sock.sendall(np.asarray(shape).astype(np.int32).tostring())

        # Send the integers
        sock.sendall(integers.tostring())

        # Create the raw data
        raw_data = "".encode().join(
            [
                np.asarray(len(elem)).astype(np.int32).tostring() + elem
                for elem in encoding.vec
            ]
        )

        # Create the shape
        shape = [len(encoding.vec), len(raw_data)]

        # Send the shape.
        sock.sendall(np.asarray(shape).astype(np.int32).tostring())

        # Send the raw data
        sock.sendall(raw_data)


# --------------------------------------------------------------------


def send_matrix(sock, matrix):
    """Sends a matrix (type np.float64) to the getml engine.

    Raises:
        TypeError: If the input is not of proper type.
        Exception: If the dimension of `matrix` is larger than two.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    if not isinstance(matrix, np.ndarray):
        raise TypeError("'matrix' must be a numpy.ndarray.")

    # ----------------------------------------------------------------

    if len(matrix.shape) == 1:
        shape = [matrix.shape[0], 1]

    elif len(matrix.shape) > 2:
        raise Exception("Numpy array must be one-dimensional or two-dimensional!")

    else:
        shape = matrix.shape

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":

        sock.sendall(np.asarray(shape).astype(np.int32).byteswap().tostring())

        sock.sendall(matrix.astype(np.float64).byteswap().tostring())

    else:

        sock.sendall(np.asarray(shape).astype(np.int32).tostring())

        sock.sendall(matrix.astype(np.float64).tostring())


# --------------------------------------------------------------------


def send_string(sock, string):
    """
    Sends a string to the getml engine
    (an actual string, not a bytestring).

    Raises:
        TypeError: If the input is not of proper type.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    if not isinstance(string, str):
        raise TypeError("'string' must be a str.")

    # ----------------------------------------------------------------

    encoded = string.encode("utf-8")

    size = len(encoded)

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":

        sock.sendall(np.asarray([size]).astype(np.int32).byteswap().tostring())

    else:

        sock.sendall(np.asarray([size]).astype(np.int32).tostring())

    sock.sendall(encoded)


# --------------------------------------------------------------------


def log(sock):
    """
    Prints all the logs received by the socket.
    """
    pbar = _ProgressBar()

    while True:
        msg = recv_string(sock)

        if msg[:5] != "log: ":
            return msg

        msg = msg[5:]

        if "Progress: " in msg:
            msg = msg.split("Progress: ")[1].split("%")[0]
            progress = int(msg)
            pbar.show(progress)
            continue

        print()
        print(msg)
        pbar.show(0)


# --------------------------------------------------------------------


def _delete_project(name):

    # ----------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "deleteproject"
    cmd["body_"] = name

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = recv_string(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    # ----------------------------------------------------------------

    sock.close()


# --------------------------------------------------------------------


def _get_project_name():
    cmd = dict()
    cmd["type_"] = "project_name"
    cmd["name_"] = ""

    sock = send_and_receive_socket(cmd)

    pname = recv_string(sock)

    sock.close()

    return pname


# --------------------------------------------------------------------


def _list_projects_impl(running_only):

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "listallprojects"
    cmd["body_"] = ""

    # ----------------------------------------------------------------

    if running_only:
        cmd["type_"] = "listrunningprojects"

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = recv_string(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    # ----------------------------------------------------------------

    json_str = recv_string(sock)

    sock.close()

    # ----------------------------------------------------------------

    return json.loads(json_str)["projects"]


# --------------------------------------------------------------------


def _set_project(name, restart=False):

    # ----------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "setproject"
    cmd["body_"] = name

    # ----------------------------------------------------------------

    if restart:
        cmd["type_"] = "restartproject"

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = log(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    global port

    port = int(recv_string(sock))

    # ----------------------------------------------------------------

    print()
    print("Connected to project '" + name + "'")


# --------------------------------------------------------------------


def _shutdown():

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "shutdownlocal"
    cmd["body_"] = ""

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    sock.close()


# --------------------------------------------------------------------


def _suspend_project(name):

    # ----------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "suspendproject"
    cmd["body_"] = name

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = recv_string(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    # ----------------------------------------------------------------

    sock.close()
