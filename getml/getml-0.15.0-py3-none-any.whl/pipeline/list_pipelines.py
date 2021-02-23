# Copyright 2020 The SQLNet Company GmbH

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

import json
import getml.communication as comm

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
