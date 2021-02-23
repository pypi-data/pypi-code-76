#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :globals.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

class GlobalVariables(object):
    def __init__(self, kwargs):
        self._global_variables = kwargs

    def get(self, key):
        if key in self._global_variables.keys():
            return self._global_variables[key]
        else:
            return None

    def set(self, key):
        pass
