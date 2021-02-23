#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : timer.py
# @Author: Perhaps
# @Date  : 2021/2/4
# @Desc  : 时间
import time


class Timer(object):
    @staticmethod
    def get_current_time():
        return time.localtime(time.time())