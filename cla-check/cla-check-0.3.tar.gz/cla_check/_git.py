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

import re
import subprocess

shortlog_email_rx = re.compile(r"^\s*\d+\s+.*<(\S+)>$", re.M)


def get_emails_for_range(commit_range: str):
    output = subprocess.check_output(["git", "shortlog", "-se", commit_range]).decode(
        "utf-8"
    )

    return set(m.group(1) for m in shortlog_email_rx.finditer(output))
