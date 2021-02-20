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

import functools
import sys

try:
    from launchpadlib.launchpad import Launchpad  # type: ignore
except ImportError:
    sys.exit("missing launchpadlib (sudo apt install python3-launchpadlib)")


@functools.lru_cache(128)
def _login():
    print("Logging into launchpad...")
    return Launchpad.login_anonymously("check CLA", "production")


@functools.lru_cache(128)
def query_cla_participants():
    print("Querying participants...")
    return _login().people["contributor-agreement-canonical"].participants


@functools.lru_cache(128)
def query_person(email: str):
    return _login().people.getByEmail(email=email)
