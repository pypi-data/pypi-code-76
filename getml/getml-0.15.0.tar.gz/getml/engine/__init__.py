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
# AUTHORS OR COPYRIGHT :wHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""This module is a collection of utility functions for the overall
communication and the session management of the getML engine.

In order to log into the engine, you have to open your favorite
internet browser and enter `http://localhost:1709
<http://localhost:1709>`_ in the navigation bar. This tells it to
connect to a local TCP socket at port 1709 opened by the getML
monitor. This will only be possible from within the same device!

The appearing page will prompt you for your email address and
password or, if you haven't registered yet, enable you
to create a user account. The account management and all
associated data is hosted by AWS in Frankfurt, Germany.

Note that while all your data and results stay locally at your
device, the login does require a working internet connection in
order to authenticate your account. For more information please
see the official documentation at docs.getml.com.

Examples:

    First of all, you need to start the getML engine.
    Next, you need to create a new project or
    load an existing one.

    .. code-block:: python

        getml.engine.list_projects()
        getml.engine.set_project('test')

    After doing all calculations for today you can shut down the getML
    engine.

    .. code-block:: python

        print(getml.engine.is_alive())
        getml.engine.shutdown()

Note:

    The Python process and the getML engine must be located on
    the same machine. If you
    intend to run the engine on a remote host, make sure to start your
    Python session on that device as well. Also, when using SSH sessions,
    make sure to start Python using `python &` followed by `disown` or
    using `nohup python`. This ensures the Python process and all the
    script it has to run won't get killed the moment your remote
    connection becomes unstable and
    you are able to recover them later on (see
    :ref:`remote_access`).

    All data frame objects and models in the getML engine are
    bundled in projects. When loading an existing project, the
    current memory of the engine will be flushed and all changes
    applied to :class:`~getml.data.DataFrame` instances after
    calling their :meth:`~getml.data.DataFrame.save` method will
    be lost. Afterwards, all
    :class:`~getml.pipeline.Pipeline` will be loaded into
    memory automatically. The data frame objects
    will not be loaded automatically since they consume significantly
    more
    memory than the pipelines. They can be loaded manually using
    :func:`~getml.data.load_data_frame` or
    :meth:`~getml.data.DataFrame.load`.

    The getML engine reflects the separation of data into individual
    projects on the level of the filesystem too. All data
    belonging to a single project is stored in a dedicated folder in
    the 'projects' directory located in '.getML' in your home
    folder. These projects can be copied and shared between different
    platforms and architectures without any loss of information. However,
    you must copy the entire project and not just individual data frames
    or pipelines.
"""

from .helpers import (
    delete_project,
    is_alive,
    is_engine_alive,
    is_monitor_alive,
    list_projects,
    list_running_projects,
    restart_project,
    set_project,
    set_s3_access_key_id,
    set_s3_secret_access_key,
    shutdown,
    suspend_project,
)

__all__ = (
    "delete_project",
    "is_engine_alive",
    "is_monitor_alive",
    "is_alive",
    "list_projects",
    "list_running_projects",
    "restart_project",
    "set_project",
    "set_s3_access_key_id",
    "set_s3_secret_access_key",
    "shutdown",
    "suspend_project",
)
