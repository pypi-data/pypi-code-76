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
Handles access to project-related information.
"""

from sys import modules

import getml.communication as comm
from getml import data, hyperopt, pipeline
from getml.engine import is_engine_alive, is_monitor_alive, list_projects

_functions = []

_props = []


def __getattr__(key):

    if key in _functions:
        return getattr(modules.get(__name__), key)

    if key in _props:
        if is_engine_alive():
            return getattr(modules.get(__name__), "_" + key)()
        elif is_monitor_alive():
            projects = "\n".join(list_projects())
            msg = comm._make_error_msg()
            msg += "\n\nAvailable projects:\n\n"
            msg += projects
            print(msg)
            return None
        else:
            msg = comm._make_error_msg()
            print(msg)
            return None

    raise AttributeError(f"module 'getml.project' has no attribute {key}")


def module_function(func):
    _functions.append(func.__name__)
    return func


def module_prop(prop):
    _props.append(prop.__name__[1:])
    return prop


@module_prop
def _data_frames():
    return data.DataFrames()


@module_prop
def _hyperopts():
    return hyperopt.Hyperopts()


@module_prop
def _pipelines():
    return pipeline.Pipelines()


@module_prop
def _name():
    return comm._get_project_name()


@module_function
def delete():
    """
    Deletes the currently connected project. All related pipelines,
    data frames and hyperopts will be irretrivably deleted.
    """
    comm._delete_project(_name())


@module_function
def restart():
    """
    Suspends and then relaunches the currently connected project.
    This will kill all jobs currently running on that process.
    """
    comm._set_project(_name(), restart=True)


@module_function
def suspend():
    """
    Suspends the currently connected project.
    """
    return comm._suspend_project(_name())


@module_function
def switch(name):
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


_all = _functions + _props
