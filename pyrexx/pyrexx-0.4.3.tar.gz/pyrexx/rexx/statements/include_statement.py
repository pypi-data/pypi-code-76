"""
PyREXX - Library that enables parsing and analysis of REXX source code.

This program and the accompanying materials are made available under the terms of
The Apache-2.0 License which accompanies this distribution, and is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0

Copyright (c) Mainframe Services Engineering (IBM GTS).

"""
import sys 
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from exceptions import PatternNotFound
from .rexx_statement import RexxStatement

NEGATIVE_INCLUDE = '!'

class IncludeStatement(RexxStatement):

    def __init__(self, include_statement):
        super().__init__(include_statement)
        self.routines = ""
        self.negative_routines = ""
        try:
            self.file_name = include_statement.group(3)
            if include_statement.group(5):
                self.raw_routines = include_statement.group(5).split(",")
                self.routines = [routine for routine in self.raw_routines if not routine.startswith(NEGATIVE_INCLUDE)]
                self.negative_routines = [routine.strip(NEGATIVE_INCLUDE) for routine in self.raw_routines if routine.startswith(NEGATIVE_INCLUDE)]
        except IndexError:
            raise PatternNotFound("The created IncludeStatement don't resolve to required groups")
