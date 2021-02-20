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

import argparse
import subprocess
import sys

from cla_check import _cla, _git, _term


def _print_debug_checkout_info(commit_range: str):
    with _term.fold(tag="checkout_info", message="Debug information"):
        print("Commit range:", commit_range)
        print("Remotes:")
        subprocess.check_call(["git", "remote", "-v"])
        print("Branches:")
        subprocess.check_call(["git", "branch", "-v"])


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "commit_range", help="Commit range in format <upstream-head>..<fork-head>"
    )
    opts = parser.parse_args()

    _print_debug_checkout_info(opts.commit_range)

    range_emails = _git.get_emails_for_range(opts.commit_range)
    if len(range_emails) == 0:
        sys.exit("No emails found in in the given commit range.")

    align_width = max(map(len, range_emails))

    print("Checking {} emails:".format(len(range_emails)))
    if all(
        [
            _cla.check_email(email=email, align_width=align_width)
            for email in range_emails
        ]
    ):
        return 0
    else:
        return 1
