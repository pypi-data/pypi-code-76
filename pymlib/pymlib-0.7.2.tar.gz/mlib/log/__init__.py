# coding: utf-8

import logging

# 初始化日志
def initLog(**kwargs):
    mlog = logging.getLogger("mlog")
    level = kwargs.get("level")
    if level:
        level = getattr(logging, level)
    else:
        level = logging.DEBUG
    mlog.setLevel( level )

    ft = kwargs.get("formatter", "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(thread)d|%(message)s")
    formatter = logging.Formatter(ft)

    console = logging.StreamHandler()  
    console.setLevel(level)
    console.setFormatter(formatter)
    mlog.addHandler(console)

def getLog():
    mlog = logging.getLogger("mlog")
    return mlog