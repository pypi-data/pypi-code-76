#!/usr/bin/env python

#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the packagit project.
#  Please respect the license - more about this in the section (*) below.
#  #
#  packagit is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  #
#  packagit is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  #
#  You should have received a copy of the GNU General Public License
#  along with packagit.  If not, see <http://www.gnu.org/licenses/>.
#  #
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
import sys

from packagit_.packagit import extract_version, update_version, create_tag

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Provide the major version number.\n\nUsage:\n\tpackagit 1")
        exit()
    major = args[1]
    error = True

    with open("setup.py", "r") as f:
        txt = f.readlines()
    with open("setup.py", "w") as f:
        for l in txt:
            if "VERSION = " in l:
                error = False
                previous_version = extract_version(l[:-1])
                version = update_version(major, previous_version)
                l = f'VERSION = "{version}"\n'
            f.write(l)

    if error:
        raise Exception("Could not increment VERSION.")
    tag = create_tag(version)
    print(tag, "created and pushed. New setup.py committed and pushed.")
