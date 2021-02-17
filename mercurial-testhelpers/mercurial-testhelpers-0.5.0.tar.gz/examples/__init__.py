# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Examples of integration tests for Mercurial core and extensions."""

import pytest
from mercurial_testhelpers import (
    extension,
)


def skipif_extension_not_available(name):
    return pytest.mark.skipif(
        not extension.is_available(name),
        reason="The %r extension is not available" % name)
