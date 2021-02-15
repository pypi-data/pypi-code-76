"""
PyREXX - Library that enables parsing and analysis of REXX source code.

This program and the accompanying materials are made available under the terms of
The Apache-2.0 License which accompanies this distribution, and is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0

Copyright (c) Mainframe Services Engineering (IBM GTS).

"""

from .rexx_statement import RexxStatement


class DocstringStatement(RexxStatement):

    def __init__(self, docstring_code):
        super().__init__(docstring_code)
        # TODO Improve this logic for error handling.
        self.statement = docstring_code.group(2).split('@')[1]
        self.values = docstring_code.group(3).strip()
