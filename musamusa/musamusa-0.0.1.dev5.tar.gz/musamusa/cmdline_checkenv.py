#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    musamusa Copyright (C) 2021 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of musamusa.
#    musamusa is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    musamusa is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with musamusa.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa project : musamusa/cmdline_checkenv.py

   code for the --checkenv command line option.

   ____________________________________________________________________________

   * cmdline_checkenv : display informations about Python version
                        and required third party packages
"""
import importlib
import sys

from musamusa.aboutproject import THIRDPARTIES_DEPENDENCIES


def cmdline_checkenv():
    """
        cmdline_checkenv()

        Check the version of Python and the presence of required third party packages.

        This function is what executes the --checkenv command line option.

        This function doesn't use a logger or rich text output.

        ________________________________________________________________________

        no PARAMETER

        RETURNED VALUE :
            (bool) success
    """
    print("* Python version is {major}.{minor}.{release}".format(
        major=sys.version_info[0],
        minor=sys.version_info[1],
        release=sys.version_info[2]))

    for module in THIRDPARTIES_DEPENDENCIES:
        res = "[OK]"
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            res = "[NOT OK]"
        print("* {res} third party module '{module}'".format(
            res=res,
            module=module))

    return True
