"""
PyREXX - Library that enables parsing and analysis of REXX source code.

This program and the accompanying materials are made available under the terms of
The Apache-2.0 License which accompanies this distribution, and is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0

Copyright (c) Mainframe Services Engineering (IBM GTS).

"""
from .source_code import SourceCode


class RexxSubRoutine(SourceCode):

    def __init__(self, name, code):
        self.name = name
        super().__init__(code)
