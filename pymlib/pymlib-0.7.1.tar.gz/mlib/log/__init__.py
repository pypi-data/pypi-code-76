# coding: utf-8

import logging

# 初始化日志
def initLog(**conf):
    mlog = logging.getLogger("mlog")
    mlog.setLevel( getattr(logging, conf["log"]["level"]) )
    formatter = logging.Formatter(conf["log"]["formatter"])

    console = logging.StreamHandler()  
    console.setLevel( getattr(logging, conf["log"]["level"]) )
    console.setFormatter(formatter)
    mlog.addHandler(console)

def getLog():
    mlog = logging.getLogger("mlog")
    return mlog