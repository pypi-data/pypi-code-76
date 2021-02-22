# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;interactive_cli

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.4
dpt_interactive_cli/interactive_cli_mixin.py
"""

from time import ctime
import os

try: from html import escape as html_escape
except ImportError: from cgi import escape as html_escape

from dpt_runtime import Binary
from dpt_runtime.exceptions import TracedException
from prompt_toolkit import HTML, print_formatted_text, PromptSession
from prompt_toolkit.output import create_output

class InteractiveCliMixin(object):
    """
This mixin provides methods to handle console input and output.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    dpt
:subpackage: interactive_cli
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=assigning-non-slot

    _mixin_slots_ = [ "prompt_session", "output_pid" ]
    """
Additional __slots__ used for inherited classes.
    """
    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self):
        """
Constructor __init__(InteractiveCliMixin)

:since: v1.0.00
        """

        self.prompt_session = None
        """
prompt_toolkit based input prompt session
        """
        self.output_pid = os.getpid()
        """
PID used for output separation
        """

        self.output_stream = None
    #

    @property
    def output_stream(self):
        """
Returns the current output stream pointer in use.

:return: (int) Stream pointer number
:since:  v1.0.0
        """

        return self.prompt_session.output.fileno()
    #

    @output_stream.setter
    def output_stream(self, pointer):
        """
Sets the output stream pointer to use.

:param pointer: Stream pointer number

:since: v1.0.0
        """

        self.prompt_session = PromptSession(output = (None if (pointer is None) else create_output(pointer)),
                                            mouse_support = True
                                           )
    #

    def error(self, _exception):
        """
Prints the stack trace on this error event.

:param _exception: Inner exception

:since: v1.0.0
        """

        if (isinstance(_exception, TracedException)): _exception.print_stack_trace(self.output_stream)
        else: TracedException.print_current_stack_trace(self.output_stream)
    #

    def input(self, prompt):
        """
Reads one line of input.

:param prompt: Inline prompt

:return: (str) Cli input
:since:  v1.0.0
        """

        return self.prompt_session.prompt(prompt)
    #

    def output(self, line, *args):
        """
Outputs the given line. Additional positional arguments are used for string
formatting.

:param line: Output line

:since: v1.0.0
        """

        print_formatted_text(line.format(*args) if (len(args) > 0) else line)
    #

    def output_error(self, line, *args):
        """
Outputs the given error line. Additional positional arguments are used for
string formatting.

:param line: Output line

:since: v1.0.0
        """

        line = Binary.str(line)
        if (type(line) is not str): line = str(line)
        line = html_escape(line.format(*args) if (len(args) > 0) else line)

        self.output_formatted("<small>[{0}({1:d}) {2}]</small> <strong>{3}</strong>",
                              self.__class__.__name__,
                              self.output_pid,
                              ctime(),
                              line
                             )
    #

    def output_formatted(self, line, *args):
        """
Outputs the given HTML-formatted line. Additional positional arguments are
used for string formatting.

:param line: Output line

:since: v1.0.0
        """

        print_formatted_text(HTML(Binary.utf8(line.format(*args) if (len(args) > 0) else line)))
    #

    def output_info(self, line, *args):
        """
Outputs the given informational line. Additional positional arguments are
used for string formatting.

:param line: Output line

:since: v1.0.0
        """

        line = Binary.str(line)
        if (type(line) is not str): line = str(line)
        line = html_escape(line.format(*args) if (len(args) > 0) else line)

        self.output_formatted("<small>[{0}({1:d}) {2}]</small> {3}",
                              self.__class__.__name__,
                              self.output_pid,
                              ctime(),
                              line
                             )
    #

    def secure_input(self, prompt):
        """
Reads one line of input without showing the user what he typed.

:param prompt: Inline prompt

:return: (str) Cli input
:since:  v1.0.0
        """

        return self.prompt_session.prompt(prompt, is_password = True)
    #
#
