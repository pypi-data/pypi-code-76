#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :pipeline.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

class Pipeline(object):
    def __init__(self, components, kwargs, temp_item):
        self.temp_item = temp_item
        self.components = components
        self.kwargs = kwargs

    def excute(self):
        temp_item = self.temp_item
        for component in self.components:
            temp_item = component(self.kwargs, temp_item).excute()
        return temp_item
