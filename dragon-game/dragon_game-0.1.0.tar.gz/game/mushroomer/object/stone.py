#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : stone.py
@Author: Perhaps
@Date  : 2021/2/18 3:14 下午
@Desc  : 阻碍物石头
"""
import random

import pygame

from .Iobject import IObject


class Stone(IObject):
    """class Tree extends MySprite.

    Attributes:
        reward: collision reward of tree(MySprite)
        position: tree(MySprite)'s position

    """

    def __init__(self):
        super(Stone, self).__init__()
        self.reward = 0
        self.master_image = pygame.image.load("../resources/images/stone3D.png").convert_alpha()
        self.load(self.master_image, 100, 100, 1)
        # self.position = random.randrange(0, 1000, 100), 100, random.randrange(0, 1000, 100)
        self.position = 500, 100, 500

    def test(self):
        pass
