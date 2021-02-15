"""
PyREXX - Library that enables parsing and analysis of REXX source code.

This program and the accompanying materials are made available under the terms of
The Apache-2.0 License which accompanies this distribution, and is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0

Copyright (c) Mainframe Services Engineering (IBM GTS).

"""


class PatternNotFound(Exception):
    """Exception class for missing pattern."""

    def __init__(self, message):
        super().__init__(f'Unable to find required Regex pattern: {message}')
