#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : shadow.py
# @Author: perhaps
# @Date  : 2021/2/4
# @Desc  : 物体的影子
import pygame

from .Iobject import IObject


class Shadow(IObject):
    def __init__(self):
        super(Shadow, self).__init__()
        self.master_image = pygame.image.load("../resources/images/shadow.png").convert_alpha()
        self.load(self.master_image, 10, 10, 1)

    def appear_shadow(self, sprite):
        self.position = sprite.X, 0, sprite.z_distance + 100

    def disappear_shadow(self):
        pass
