# OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://pypi.org/project/genocide !
#
# This file is placed in the Public Domain.

"find"

# imports

from op.obj import format, keys
from op.dbs import find, list_files
from op.hdl import Bus
from op.prs import elapsed
from op.run import cfg
from op.utl import fntime, time

# defines

def __dir__():
    return ("fnd",)

# commands

def fnd(event):
    if not event.args:
        fls = list_files(cfg.wd)
        if fls:
            event.reply("|".join([x.split(".")[-1].lower() for x in fls]))
        return
    name = event.args[0]
    bot = Bus.by_orig(event.orig)
    t = bot.get_names(name)
    nr = -1
    for otype in t:
        for fn, o in find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            txt = "%s %s" % (str(nr), format(o, event.xargs or keys(o), skip=event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
