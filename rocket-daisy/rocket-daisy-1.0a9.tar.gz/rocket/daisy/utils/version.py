def logo():
    print()
    print("      ____        _            ")
    print("     / __ \____ _(_)______  __ ")
    print("    / / / / __ `/ / ___/ / / / ")
    print("   / /_/ / /_/ / (__  ) /_/ /  ")
    print("  /_____/\__,_/_/____/\__, /   ")
    print("  martin shishkov    /____/    ")
    print("                               ")
#
#   Copyright 2020 Martin Shishkov, gulliversoft.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re
import sys

VERSION         = '0.1.rc'
VERSION_STRING  = "Daisy/%s/Python%d.%d" % (VERSION, sys.version_info.major, sys.version_info.minor)
PYTHON_MAJOR    = sys.version_info.major
BOARD_REVISION  = 0

_MAPPING = [[], [], []]
_MAPPING[1] = ["V33", "V50", 0, "V50", 1, "GND", 4, 14, "GND", 15, 17, 18, 21, "GND", 22, 23, "V33", 24, 10, "GND", 9, 25, 11, 8, "GND", 7]
_MAPPING[2] = ["V33", "V50", 2, "V50", 3, "GND", 4, 14, "GND", 15, 17, 18, 27, "GND", 22, 23, "V33", 24, 10, "GND", 9, 25, 11, 8, "GND", 7]


try:
    with open("/proc/cpuinfo") as f:
        rc = re.compile("Revision\s*:\s(.*)\n")
        info = f.read()
        result = rc.search(info)
        if result != None:
            hex_cpurev = result.group(1)
            if hex_cpurev.startswith("1000"):
                hex_cpurev = hex_cpurev[-4:]
            cpurev = int(hex_cpurev, 16)
            BOARD_REVISION = 1 if (cpurev < 4) else 2
        
except:
    pass

MAPPING = _MAPPING[BOARD_REVISION]
