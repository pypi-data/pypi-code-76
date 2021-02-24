# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for interacting with game configuration files as defined by
Config objects in the profile
"""

import csv
import os
from typing import Dict, Set

from portmod.atom import Atom
from portmod.loader import load_installed_pkg


def usedep_matches_installed(atom: Atom) -> bool:
    mod = load_installed_pkg(atom.strip_use())
    if not mod:
        return False  # If override isn't installed, it won't be in the graph

    for flag in atom.USE:
        if flag.startswith("-") and flag.lstrip("-") in mod.INSTALLED_USE:
            return False  # Required flag is not set
        elif not flag.startswith("-") and flag not in mod.INSTALLED_USE:
            return False  # Required flag is not set

    return True


def read_userconfig(path: str) -> Dict[str, Set[str]]:
    userconfig = {}

    if os.path.exists(path):
        # Read user config
        with open(path, newline="") as csvfile:
            csvreader = csv.reader(csvfile, skipinitialspace=True)
            for row in csvreader:
                assert len(row) > 1
                atom = row[0].strip()
                if atom not in userconfig:
                    userconfig[atom] = set(map(lambda x: x.strip(), row[1:]))
                else:
                    userconfig[atom] |= set(map(lambda x: x.strip(), row[1:]))

    return userconfig
