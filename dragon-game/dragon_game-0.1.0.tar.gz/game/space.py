#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : space.py
# @Author: perhaps
# @Date  : 2021/2/4
# @Desc  : 空间

import numpy as np


class Space(object):
    """class TimeSpace(whole map of game environment).
       3D map contain time and space for per unit
    Attributes:
        space: sprite's position in 3D map
        dict: container of 3D map
    """

    def __init__(self):
        self.space = np.array([0, 0, 0])
        self.dict = {}
        self.EXIST = None

    def check_map(self, sprite):
        self.space = sprite.position
        if self.space in self.dict:
            self.EXIST = False
        else:
            self.dict[self.space] = sprite.master_image
            self.EXIST = True

    def del_map(self):
        pass
