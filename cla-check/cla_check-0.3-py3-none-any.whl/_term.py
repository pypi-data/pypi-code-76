# Copyright 2021 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import contextlib
import os
import sys


def _is_travis() -> bool:
    return os.getenv("TRAVIS", "") == "true"


def _is_github_actions() -> bool:
    return os.getenv("GITHUB_ACTIONS", "") == "true"


if sys.stdout.isatty() or _is_travis() or _is_github_actions():
    GREEN = "\033[32;1m"
    RED = "\033[31;1m"
    YELLOW = "\033[33;1m"
    RESET = "\033[0m"
    CLEAR = "\033[0K"
else:
    GREEN = ""
    RED = ""
    YELLOW = ""
    RESET = ""
    CLEAR = ""

if _is_travis():
    FOLD_START = "travis_fold:start:{{tag}}\r{}{}{{message}}{}".format(
        CLEAR, YELLOW, RESET
    )
    FOLD_END = "travis_fold:end:{{tag}}\r{}".format(CLEAR)
elif _is_github_actions():
    FOLD_START = "::group::{message}"
    FOLD_END = "::endgroup::"
else:
    FOLD_START = "{}{{message}}{}".format(YELLOW, RESET)
    FOLD_END = ""


@contextlib.contextmanager
def fold(*, tag: str, message: str):
    """Fold block of output for supported services.

    :param tag: Fold tag.
    :param message: Fold description.
    """
    print(FOLD_START.format(tag=tag, message=message))
    yield
    print(FOLD_END.format(tag=tag))
