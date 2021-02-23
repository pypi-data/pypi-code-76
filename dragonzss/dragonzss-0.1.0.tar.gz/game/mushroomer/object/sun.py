#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sun.py
# @Author: perhaps
# @Date  : 2021/2/4
# @Desc  : 太阳
import pygame

from .Iobject import IObject


class Sun(IObject):
    """class Sun extends MySprite.

    Attributes:
        position: sun(MySprite)'s position

    """
    def __init__(self):
        super(Sun, self).__init__()
        self.master_image = pygame.image.load("../resources/images/sun.png").convert_alpha()
        self.load(self.master_image, 100, 100, 1)
        self.position = (450, 0, 0)

    def sun_round(self, hour):
        if 0 < hour < 6:
            self.X, self.Y = -200, -200
        elif 18 < hour < 24:
            self.X, self.Y = -200, -200
        else:
            self.X, self.Y = (hour - 8) * 100, 0
