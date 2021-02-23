#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : gameABC.py
# @Author: Perhaps
# @Date  : 2021/2/4
# @Desc  : 游戏类的接口定义
import abc


class GameABC(metaclass=abc.ABCMeta):

    def seed(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def step(self, action):
        pass

    @abc.abstractmethod
    def render(self, mode="human", close=False):
        pass

    def close(self):
        pass
