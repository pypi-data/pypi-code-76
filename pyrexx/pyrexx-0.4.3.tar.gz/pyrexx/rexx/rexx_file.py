"""
PyREXX - Library that enables parsing and analysis of REXX source code.

This program and the accompanying materials are made available under the terms of
The Apache-2.0 License which accompanies this distribution, and is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0

Copyright (c) Mainframe Services Engineering (IBM GTS).

"""

import re
import os
from .rexx_sub_routine import RexxSubRoutine
from .rexx_code import RexxCode
from .statements import IncludeStatement
from utilities import LOG

class RexxFile:
    """Class used to represent a REXX file abstraction."""

    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = os.path.abspath(file_path)
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as f:
                self.file_contents = f.read()
            self.code = RexxCode(self.file_contents)
