# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;cli

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.2
dpt_cli/cli.py
"""

# pylint: disable=import-error,invalid-name,unused-import

from errno import EINVAL, ESRCH
from time import sleep
from weakref import ref
import os

try: import signal
except ImportError: signal = object()

from dpt_logging import ExceptionLogTrap
from dpt_runtime.exceptions import TracedException, ValueException
from dpt_threading import Event
from dpt_threading.encapsulated import Thread

_IMPLEMENTATION_JAVA = 1
"""
Java based Python implementation
"""
_IMPLEMENTATION_PYTHON = 2
"""
Native Python implementation
"""
_IMPLEMENTATION_MONO = 3
"""
Mono/.NET based Python implementation
"""

try:
    import java.lang.System
    _mode = _IMPLEMENTATION_JAVA
except ImportError: _mode = _IMPLEMENTATION_PYTHON

if (_mode == _IMPLEMENTATION_PYTHON):
    try:
        import clr
        clr.AddReferenceByPartialName("IronPython")
        _mode = _IMPLEMENTATION_MONO
    except ImportError: pass
#

class Cli(object):
    """
"Cli" makes it easy to build command line applications.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: cli
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    IMPLEMENTATION_JAVA = _IMPLEMENTATION_JAVA
    """
Java based Python implementation
    """
    IMPLEMENTATION_PYTHON = _IMPLEMENTATION_PYTHON
    """
Native Python implementation
    """
    IMPLEMENTATION_MONO = _IMPLEMENTATION_MONO
    """
Mono/.NET based Python implementation
    """

    __slots__ = [ "__weakref__", "arg_parser", "_log_handler", "_mainloop", "mainloop_event" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _callbacks_run = [ ]
    """
Callbacks for "run()"
    """
    _callbacks_shutdown = [ ]
    """
Callbacks for "shutdown()"
    """
    _weakref_instance = None
    """
"Cli" weakref instance
    """

    def __init__(self):
        """
Constructor __init__(Cli)

:since: v1.0.0
        """

        self.arg_parser = None
        """
ArgumentParser instance
        """
        self._log_handler = None
        """
The log handler is called whenever debug messages should be logged or errors
happened.
        """
        self._mainloop = None
        """
Callable main loop without arguments
        """
        self.mainloop_event = Event()
        """
Mainloop event
        """

        Cli._weakref_instance = ref(self)
    #

    @property
    def log_handler(self):
        """
Returns the log handler.

:return: (object) Log handler in use
:since:  v1.0.0
        """

        return self._log_handler
    #

    @log_handler.setter
    def log_handler(self, log_handler):
        """
Sets the log handler.

:param log_handler: Log handler to use

:since: v1.0.0
        """

        self._log_handler = log_handler
    #

    @property
    def mainloop(self):
        """
Returns the registered callback for the application main loop.

:return: (object) Python callback; None if not set
:since:  v1.0.0
        """

        return self._mainloop
    #

    @mainloop.setter
    def mainloop(self, callback):
        """
Register a callback for the application main loop.

:param callback: Python callback

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("dpt_cli/cli.py -{0!r}.mainloop()- (182)", self, context = "dpt_cli")

        if (self._mainloop is not None): raise ValueException("Main loop already registered")
        if (not callable(callback)): raise ValueException("Main loop callback given is invalid")

        self._mainloop = callback
    #

    def error(self, _exception):
        """
Prints the stack trace on this error event.

:param _exception: Inner exception

:since: v1.0.0
        """

        if (isinstance(_exception, TracedException)): _exception.print_stack_trace()
        else: TracedException.print_current_stack_trace()
    #

    def run(self):
        """
Executes registered callbacks for the active application.

:since: v1.0.0
        """

        # pylint: disable=broad-except,not-callable

        if (self._log_handler is not None): self._log_handler.debug("dpt_cli/cli.py -{0!r}.run()- (212)", self, context = "dpt_cli")

        if (self.arg_parser is not None and hasattr(self.arg_parser, "parse_args")): args = self.arg_parser.parse_args()
        else: args = { }

        self.arg_parser = None

        try:
            for callback in Cli._callbacks_run: callback(args)
            Cli._callbacks_run = [ ]

            self.mainloop_event.set()
            if (self.mainloop is not None): self.mainloop()
        except Exception as handled_exception: self.error(handled_exception)
        finally: self.shutdown()
    #

    def _signal(self, signal_name, stack_frame):
        """
Handles an OS signal.

:param signal_name: Signal name
:param stack_frame: Stack frame

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("dpt_cli/cli.py -{0!r}._signal()- (239)", self, context = "dpt_cli")
        self.shutdown()
    #

    def shutdown(self, _exception = None):
        """
Executes registered callbacks before shutting down this application.

:param _exception: Inner exception

:since: v1.0.0
        """

        # pylint: disable=raising-bad-type

        if (Cli._weakref_instance is not None):
            if (self._log_handler is not None): self._log_handler.debug("dpt_cli/cli.py -{0!r}.shutdown()- (255)", self, context = "dpt_cli")

            Thread.set_inactive()

            """
Cleanup unused objects
            """

            for callback in Cli._callbacks_shutdown:
                with ExceptionLogTrap("dpt_cli"): callback()
            #

            Cli._callbacks_shutdown = [ ]
            Cli._weakref_instance = None
        #

        if (_exception is not None): raise _exception
    #

    def _wait_for_os_pid(self, pid):
        """
Waits for the given OS process ID to exit.

:param pid: OS process ID

:since: v1.0.0
        """

        if (pid is not None and pid > 0 and hasattr(os, "kill")):
            for _ in range(0, 60):
                try:
                    os.kill(pid, 0)
                    sleep(0.5)
                except OSError as handled_exception:
                    if (handled_exception.errno not in ( EINVAL, ESRCH )): raise
                    break
                #
            #
        #
    #

    @staticmethod
    def get_instance():
        """
Get the Cli singleton.

:return: (Cli) Object on success
:since:  v1.0.0
        """

        weakref_callable = Cli._weakref_instance
        return (None if (weakref_callable is None) else weakref_callable())
    #

    @staticmethod
    def get_py_implementation():
        """
Returns the current Python implementation (one constant for "java", "mono"
or "py").

:return: (int) Active mode
:since:  v1.0.0
        """

        # global: _mode

        return _mode
    #

    @staticmethod
    def register_mainloop(callback):
        """
Register a callback for the application main loop.

:param callback: Python callback

:since: v1.0.0
        """

        instance = Cli.get_instance()
        if (instance is not None): instance.mainloop = callback
    #

    @staticmethod
    def register_run_callback(callback):
        """
Register a callback for the application activation event.

:param callback: Python callback

:since: v1.0.0
        """

        if (callback not in Cli._callbacks_run): Cli._callbacks_run.append(callback)
    #

    @staticmethod
    def register_shutdown_callback(callback):
        """
Register a callback for the application shutdown event.

:param callback: Python callback

:since: v1.0.0
        """

        if (callback not in Cli._callbacks_shutdown): Cli._callbacks_shutdown.append(callback)
    #
#

def _on_signal(os_signal, stack_frame):
    """
Callback function for OS signals.

:param os_signal: OS signal
:param stack_frame: Stack frame

:since: v1.0.0
    """

    # pylint: disable=protected-access

    signal_name = "unknown"

    if (hasattr(signal, "SIGABRT") and os_signal == signal.SIGABRT): signal_name = "SIGABRT"
    elif (hasattr(signal, "SIGINT") and os_signal == signal.SIGINT): signal_name = "SIGINT"
    elif (hasattr(signal, "SIGHUP") and os_signal == signal.SIGHUP): signal_name = "SIGHUP"
    elif (hasattr(signal, "SIGTERM") and os_signal == signal.SIGTERM): signal_name = "SIGTERM"
    elif (hasattr(signal, "SIGQUIT") and os_signal == signal.SIGQUIT): signal_name = "SIGQUIT"

    instance = Cli.get_instance()
    if (instance is not None): instance._signal(signal_name, stack_frame)
#

if (hasattr(signal, "SIGABRT")): signal.signal(signal.SIGABRT, _on_signal)
if (hasattr(signal, "SIGINT")): signal.signal(signal.SIGINT, _on_signal)
if (hasattr(signal, "SIGHUP")): signal.signal(signal.SIGHUP, _on_signal)
if (hasattr(signal, "SIGTERM")): signal.signal(signal.SIGTERM, _on_signal)
if (hasattr(signal, "SIGQUIT")): signal.signal(signal.SIGQUIT, _on_signal)
