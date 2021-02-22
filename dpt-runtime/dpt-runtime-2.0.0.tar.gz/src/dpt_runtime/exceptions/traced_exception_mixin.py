# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;runtime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v2.0.0
dpt_runtime/exceptions/traced_exception_mixin.py
"""

import sys

try: import traceback
except ImportError: traceback = None

class TracedExceptionMixin(object):
    """
The extended "RuntimeError" is used to redirect exceptions to output
streams.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v2.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=assigning-non-slot

    _mixin_slots_ = [ "_trace_list" ]
    """
Additional __slots__ used for inherited classes.
    """
    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, _exception = None):
        """
Constructor __init__(TracedExceptionMixin)

:param _exception: Inner exception

:since: v2.0.0
        """

        self._trace_list = None
        """
Exception traceback list
        """

        if (_exception is not None): self.__cause__ = _exception
        elif (not hasattr(self, "__cause__")): self.__cause__ = None

        exc_traceback = getattr(self, "__traceback__", None)

        if (exc_traceback is not None): self._trace_list = traceback.format_tb(exc_traceback)
        elif (hasattr(traceback, "format_stack")): self._trace_list = traceback.format_stack()[:-1]
    #

    @property
    def cause(self):
        """
Return the cause.

:return: (mixed) Inner exception
:since:  v2.0.0
        """

        return self.__cause__
    #

    @property
    def printable_trace(self):
        """
Returns the stack trace.

:return: (str) Exception stack trace
:since:  v2.0.0
        """

        _return = "{0!r}: {1!s}\n".format(self.__class__, self)

        if (self._trace_list is not None): _return += "".join(self._trace_list)

        if (self.__cause__ is not None
            and hasattr(self.__cause__, "__traceback__")
           ): _return += "".join(traceback.format_tb(self.__cause__.__traceback__))

        return _return
    #

    def __str__(self):
        """
python.org: Called by the str(object) and the built-in functions format()
and print() to compute the "informal" or nicely printable string
representation of an object.

:return: (str) The "informal" or nicely printable string representation
:since:  v2.0.0
        """

        _super = super(self.__class__, self)
        _return = (repr(self) if (getattr(_super, "__str__") == self.__str__) else _super.__str__())

        if (self.__cause__ is not None):
            _return += " ({0!r}: {1!s})".format(self.__cause__.__class__, self.__cause__)
        #

        return _return
    #

    def print_stack_trace(self, out_stream = None):
        """
Prints the stack trace to the given output stream or stderr.

:param out_stream: Output stream

:since: v2.0.0
        """

        if (out_stream is None): out_stream = sys.stderr
        out_stream.write(self.printable_trace)
    #

    def with_traceback(self, tb):
        """
python.org: This method sets tb as the new traceback for the exception and
returns the exception object.

:param tb: New traceback for the exception

:return: (object) Manipulated exception instance
:since:  v2.0.0
        """

        # pylint: disable=bad-option-value,comparison-with-callable,no-member

        self._trace_list = ([ repr(tb) ] if (traceback is None) else traceback.format_tb(tb))

        _super = super(self.__class__, self)
        if (hasattr(_super, "with_traceback") and _super.with_traceback != self.with_traceback): _super.with_traceback(tb)

        return self
    #

    @staticmethod
    def print_current_stack_trace(out_stream = None):
        """
Prints the stack trace to the given output stream or stderr.

:param out_stream: Output stream

:since: v2.0.0
        """

        # pylint: disable=too-few-format-args

        printable_trace = ("{0!r}: {1!s}\n{2!r}".format(sys.exc_info()[:3])
                           if (traceback is None) else
                           traceback.format_exc()
                          )

        if (out_stream is None): out_stream = sys.stderr
        out_stream.write(printable_trace)
    #
#
