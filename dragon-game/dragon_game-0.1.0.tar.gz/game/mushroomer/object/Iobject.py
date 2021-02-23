#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : IObject.py
# @Author: Perhaps
# @Date  : 2021/2/4
# @Desc  : 物体类接口
import pygame
from pygame.locals import *


class IObject(pygame.sprite.Sprite):
    """class MySprite extends pygame.sprite.Sprite.
       Function:
       1. loading images
       2. updating frame
       3. getting sprite's position

    Attributes:
        master_image: sprite's master_image
        frame: image's frame
        frame_width: width of per frame
        frame_height: height of per frame
        first_frame: The first frame within a specific frame range
        last_frame: The last frame within a specific frame range
        columns: frame_width * columns = master_image's width
        direction: sprite's direction u,d,l,r...
        z_distance: the distance moved in the Z axis direction
        reward: sprite's reward

    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.z_distance = 0
        # self.velocity = Point(0.0, 0.0)
        self.reward = 0

    # X property
    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    # Y property
    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    # position property
    def _getpos(self):
        return self.rect.x, self.rect.y, self.z_distance

    def _setpos(self, pos):
        self.rect.x, self.rect.y, self.z_distance = pos

    position = property(_getpos, _setpos)

    # load image by image file
    def load(self, image, width, height, columns):
        # self.master_image = image
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        # try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1  # player is 63,mushroom is 0

    # update frame
    def update(self, current_time, rate=30):
        # update animation frame number per 30
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        # build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)


# Point class
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self):
        return self.__x

    def setx(self, x):
        self.__x = x

    x = property(getx, setx)

    # Y property
    def gety(self):
        return self.__y

    def sety(self, y):
        self.__y = y

    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
               ",Y:" + "{:.0f}".format(self.__y) + "}"
