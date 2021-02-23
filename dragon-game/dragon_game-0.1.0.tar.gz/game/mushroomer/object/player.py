#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : player.py
# @Author: perhaps
# @Date  : 2021/2/4
# @Desc  : 角色
import random

import pygame

from .Iobject import IObject


class Player(IObject):
    """class Player extends MySprite.

    Attributes:
        reward: The reward of eating mushroom
        sight: The sight of player(MySprite)
        position: player(MySprite)'s position  eg: player.position = (0,1,1)
        direction: player(MySprite)'direction u,d,l,r...

    """

    def __init__(self):
        super(Player, self).__init__()
        # self.reward = 0
        self.sight = [0, 0]  # 玩家的视距[x,y],x为距离，y为半径
        self.master_image = pygame.image.load("../resources/images/walker.png").convert_alpha()
        self.load(self.master_image, 100, 100, 8)
        print(self.rect.topleft)
        self.position = random.randrange(0, 1000, 100), 100, random.randrange(0, 1000, 100)
        # self.direction = 0

    def get_score(self):
        pass

    def move_player(self, state):
        pass

    def get_sight(self):
        pass
