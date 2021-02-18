#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-
#
# Copyright 2020-2021 Pradyumna Paranjape
# This file is part of ppsi.
#
# ppsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ppsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ppsi.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Psi Pythonic Sway Interface

Still under testing

Person ⟷ Python ⟷ Sway - Interface
to deal with various faculties
that are not offerred by sway such as:

 * work-space cycling
 * work-space-specific program binding
 * visual feedback for volume and light

Employing:
 * a ppsid server that is contacted by
 * a ppsi client

AND

A swaybar-protocol-compatible 'pspbar'
that can call ppsi functions
'''

import subprocess


from . import server
from . import client
from . import pspbar


def _check_installation() -> None:
    '''
    check if dependencies are available
    '''
    server._check_installation()
    pspbar._check_installation()
    client._check_installation()


__all__ = [
    'server',
    'client',
    'pspbar'
]

__version__ = '21.2.18'
