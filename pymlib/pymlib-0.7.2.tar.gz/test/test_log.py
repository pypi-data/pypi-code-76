# coding: utf-8

import mlib

conf = {
    "formatter": "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(thread)d|%(message)s",
    "level": "DEBUG"
}

mlib.initLog(**conf)
mlog = mlib.getLog()
mlog.debug("debug")
mlog.error("error")