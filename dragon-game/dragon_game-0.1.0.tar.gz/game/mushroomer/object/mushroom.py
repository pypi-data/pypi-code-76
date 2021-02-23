#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mushroom.py
# @Author: Perhaps
# @Date  : 2021/2/4
# @Desc  : 蘑菇
import random

import pygame
from .Iobject import IObject


class Mushroom(IObject):
    """class Mushroom extends MySprite.

    Attributes:
        reward: mushroom(MySprite)'s reward
        position: mushroom(MySprite)'s position eg: mushroom.position = (0,0,1)

    """

    def __init__(self):
        super(Mushroom, self).__init__()
        self.reward = 0
        self.master_image = pygame.image.load("../resources/images/mushroom1.0.png").convert_alpha()
        self.load(self.master_image, 50, 50, 1)
        # self.position = random.randrange(0, 1000, 100), 50, random.randrange(0, 1000, 100)
        self.position = 500, 50, 400

    def grow_with_time(self):
        pass
