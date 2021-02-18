# OPBOT - pure python3 IRC bot (op/run.py)
#
# This file is placed in the Public Domain.

"runtime"

# imports

import os, sys, time

from .obj import Cfg, cfg, save, update
from .hdl import Core, Console
from .prs import parse
from .trm import exec

# functions

def run(main):
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError as ex:
        print(str(ex))

def parse_cli():
    c = Cfg()
    parse(cfg, " ".join(sys.argv[1:]))
    if cfg.sets:
        cfg.changed = True
    cfg.wd = cfg.sets.wd or cfg.wd
    cfg.mods = cfg.sets.mods or cfg.mods
    return cfg

# runtime

starttime = time.time()
