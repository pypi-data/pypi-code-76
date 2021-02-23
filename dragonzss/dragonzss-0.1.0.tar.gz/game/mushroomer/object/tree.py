#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tree.py
# @Author: perhaps
# @Date  : 2021/2/4
# @Desc  : 树木
import random

import pygame

from . import shadow
from .Iobject import IObject


class Tree(IObject):
    """class Tree extends MySprite.

    Attributes:
        reward: collision reward of tree(MySprite)
        position: tree(MySprite)'s position

    """

    def __init__(self):
        super(Tree, self).__init__()
        self.reward = 0
        self.master_image = pygame.image.load("../resources/images/tree3D1.0.png").convert_alpha()
        self.load(self.master_image, 100, 100, 1)
        # self.position = random.randrange(0, 1000, 100), 100, random.randrange(0, 1000, 100)
        self.position = 700, 100, 400

    def appear_shadow(self):
        tree_shadow = shadow.Shadow()
        tree_shadow.position = self.X, 0, self.z_distance + 100
