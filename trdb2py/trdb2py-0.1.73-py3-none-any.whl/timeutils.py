# -*- coding:utf-8 -*-
from datetime import datetime


def str2timestamp(strtime: str, strformat: str):
    dt = datetime.strptime(strtime, strformat)
    return dt.timestamp()
