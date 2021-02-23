#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : algorithmABC.py
# @Author: Perhaps
# @Date  : 2021/2/4
# @Desc  : RL算法类的接口定义
import abc


class AlgorithmABC(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def optimize(self):
        pass

    @abc.abstractmethod
    def select_action(self, s):
        pass
