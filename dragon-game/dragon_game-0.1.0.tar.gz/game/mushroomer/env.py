#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : env.py
# @Author: Perhaps
# @Date  : 2021/2/4
# @Desc  : 游戏环境
import random
import sys

import pygame
import math
import time
import numpy as np

from game.space import Space
from game.timer import Timer
from game.gameABC import GameABC
from game.mushroomer.object import *

WIDTH = 10
HEIGHT = 10
UNIT = 100
# GameOver = False
PI = math.pi
theta = 250 / 180 * PI
# rvec: Rotation matrix tvec: Translation vector camera_matrix: camera matrix
rvec = np.mat([[1, 0, 0], [0, math.cos(theta), -math.sin(theta)], [0, math.sin(theta), math.cos(theta)]])
tvec = np.mat([[500], [300], [920]])
camera_matrix = ([[250, 0, 500, 0], [0, 250, 500, 0], [0, 0, 1, 0]])


def show_text(font_t, x, y, text, color=(255, 255, 255)):
    img_text = font_t.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(img_text, (x, y))


class Env(Timer, Space, GameABC):
    """class Env extends TimeSpace.
    Function:
    1. building background
    2. coords_to_state && state_to_coords
    3. 3d_to_2d && 2d_to_3d
    4. updating map
    5. reset
    6. step

    Attributes:
        action_space: action direction list u,d,l,r...
        xx_group: sprite's group  eg:player_group

    """

    def __init__(self):
        super(Env, self).__init__()

        # self.mushroom2d = Iobject.IObject()

        self.action_space = ['u', 'd', 'l', 'r']
        self.reward = 0
        self.total_reward = 0
        self.n_actions = len(self.action_space)
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((WIDTH * UNIT, HEIGHT * UNIT))

        self.player2d = Iobject.IObject()
        self.player_2d_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.player = player.Player()
        self.player_group.add(self.player)
        self.player_sample_group = pygame.sprite.Group()
        self.player_sample = player.Player()
        self.player_sample.master_image = pygame.transform.smoothscale(self.player.master_image, (160, 160))
        self.player_sample.load(self.player.master_image, 20, 20, 8)
        self.player_sample.position = 0, 180, 0
        self.player_sample_group.add(self.player_sample)

        self.mushroom_2d_group = pygame.sprite.Group()
        self.mushroom_group = pygame.sprite.Group()
        self.mushroom_sample_group = pygame.sprite.Group()
        self.mushroom = mushroom.Mushroom()
        self.mushroom_group.add(self.mushroom)

        self.tree_group = pygame.sprite.Group()
        self.tree_2d_group = pygame.sprite.Group()
        self.tree_sample_group = pygame.sprite.Group()
        self.tree = tree.Tree()
        self.tree_group.add(self.tree)

        self.stone_group = pygame.sprite.Group()
        self.stone_2d_group = pygame.sprite.Group()
        self.stone_sample_group = pygame.sprite.Group()
        self.stone = stone.Stone()
        self.stone_group.add(self.stone)
        self.stone = stone.Stone()
        self.stone.position = 500, 100, 300
        self.stone_group.add(self.stone)
        self.stone = stone.Stone()
        self.stone.position = 400, 100, 400
        self.stone_group.add(self.stone)

        self.sun_group = pygame.sprite.Group()
        self.sun = sun.Sun()
        self.sun_group.add(self.sun)

        self.shadow_group = pygame.sprite.Group()
        self.shadow_2d_group = pygame.sprite.Group()

        self.player_moving = False
        self.col = False
        self.GameOver = False

    def build_background(self):
        pygame.display.set_caption("MushRoomer")
        self.screen.blit(
            pygame.transform.scale(pygame.image.load('../resources/images/background.png'),
                                   (WIDTH * UNIT, HEIGHT * UNIT)),
            self.screen.get_rect())

    def seed(self):
        pygame.init()
        self.build_background()
        # pygame.draw.rect()

    # show mushroom in 2d
    def show_mushrooms_in_2d(self, sprite):
        mushroom2d = Iobject.IObject()
        # mushroom2d左上点（右上点）坐标
        mushroom_2d_l = self.point_3to2([sprite.X, 0, sprite.z_distance])
        mushroom_2d_r = self.point_3to2(
            [sprite.X + sprite.rect.width, 0, sprite.z_distance])
        mushroom_2d_x, mushroom_2d_y = mushroom_2d_l[0], mushroom_2d_l[1]

        # mushroom2d's width height
        mushroom_2d_w = abs(mushroom_2d_l[0] - mushroom_2d_r[0])
        mushroom_2d_h = abs(mushroom_2d_l[0] - mushroom_2d_r[0])

        # mushroom2d's master_image
        mushroom2d.master_image = pygame.transform.smoothscale(sprite.master_image,
                                                               (int(mushroom_2d_w), int(mushroom_2d_h)))
        mushroom2d.load(mushroom2d.master_image, int(mushroom_2d_w), int(mushroom_2d_h), 1)

        mushroom2d.position = mushroom_2d_x, mushroom_2d_y + 10, 0
        for sprite in self.mushroom_2d_group:
            self.mushroom_2d_group.remove(sprite)
        self.mushroom_2d_group.add(mushroom2d)

    def show_shadows_in_2d(self, sprite):
        shadow2d = Iobject.IObject()
        # show tree in 2d
        shadow_2d_l = self.point_3to2([sprite.X, 0, sprite.z_distance])
        shadow_2d_r = self.point_3to2([sprite.X + sprite.rect.width, 0, sprite.z_distance])
        shadow_2d_x, tree_2d_y = shadow_2d_l[0], shadow_2d_l[1]
        shadow_2d_w = int(abs(shadow_2d_l[0] - shadow_2d_r[0]) * 0.8)
        shadow_2d_h = int(abs(shadow_2d_l[0] - shadow_2d_r[0]) * 0.8)
        # print("tree:", tree_2d_l, tree_2d_r, tree_2d_w)
        shadow2d.master_image = pygame.transform.smoothscale(sprite.master_image,
                                                             (int(shadow_2d_w), int(shadow_2d_h)))

        shadow2d.load(shadow2d.master_image, int(shadow_2d_w), int(shadow_2d_h), 1)
        shadow2d.position = shadow_2d_x, tree_2d_y, 0

        # if sprite.z_distance >= 500:
        #     tree2d.position = tree_2d_x + int(tree_2d_w*3/8), tree_2d_y + int(tree_2d_w/2) - int(((sprite.z_distance-500)/100)/4 * tree_2d_w), 0
        #
        # else:
        #     tree2d.position = tree_2d_x + int(tree_2d_w * 3 / 8), tree_2d_y + int(tree_2d_w / 2) + int(((400 - sprite.z_distance)/400)*tree_2d_w), 0
        # # print(tree2d.position)
        self.shadow_2d_group.add(shadow2d)

    def show_trees_in_2d(self, sprite):
        tree2d = Iobject.IObject()
        # show tree in 2d
        tree_2d_l = self.point_3to2([sprite.X, 0, sprite.z_distance])
        tree_2d_r = self.point_3to2([sprite.X + sprite.rect.width, 0, sprite.z_distance])
        tree_2d_x, tree_2d_y = tree_2d_l[0], tree_2d_l[1]
        tree_2d_w = int(abs(tree_2d_l[0] - tree_2d_r[0]) * 0.8)
        tree_2d_h = int(abs(tree_2d_l[0] - tree_2d_r[0]) * 0.8)
        # print("tree:", tree_2d_l, tree_2d_r, tree_2d_w)
        tree2d.master_image = pygame.transform.smoothscale(sprite.master_image,
                                                           (int(tree_2d_w), int(tree_2d_h)))

        tree2d.load(tree2d.master_image, int(tree_2d_w), int(tree_2d_h), 1)
        tree2d.position = tree_2d_x, tree_2d_y, 0

        # if sprite.z_distance >= 500:
        #     tree2d.position = tree_2d_x + int(tree_2d_w*3/8), tree_2d_y + int(tree_2d_w/2) - int(((sprite.z_distance-500)/100)/4 * tree_2d_w), 0
        #
        # else:
        #     tree2d.position = tree_2d_x + int(tree_2d_w * 3 / 8), tree_2d_y + int(tree_2d_w / 2) + int(((400 - sprite.z_distance)/400)*tree_2d_w), 0
        # # print(tree2d.position)
        self.tree_2d_group.add(tree2d)

    def show_stones_in_2d(self, sprite):
        stone2d = Iobject.IObject()
        # show stone in 2d
        stone_2d_l = self.point_3to2([sprite.X, 0, sprite.z_distance])
        stone_2d_r = self.point_3to2([sprite.X + sprite.rect.width, 0, sprite.z_distance])
        stone_2d_x, stone_2d_y = stone_2d_l[0], stone_2d_l[1]
        stone_2d_w = int(abs(stone_2d_l[0] - stone_2d_r[0]) * 0.7)
        stone_2d_h = int(abs(stone_2d_l[0] - stone_2d_r[0]) * 0.7)
        stone2d.master_image = pygame.transform.smoothscale(sprite.master_image,
                                                            (int(stone_2d_w), int(stone_2d_h)))

        stone2d.load(stone2d.master_image, int(stone_2d_w), int(stone_2d_h), 1)
        stone2d.position = stone_2d_x, stone_2d_y, 0
        # if sprite.z_distance >= 500:
        #     stone2d.position = stone_2d_x + int(stone_2d_w * 3 / 8) - int(stone_2d_w/2), stone_2d_y + int(stone_2d_w / 2) - int(
        #         ((sprite.z_distance - 500) / 100) / 4 * stone_2d_w) + int(stone_2d_w/2), 0
        #
        # else:
        #     stone2d.position = stone_2d_x + int(stone_2d_w * 3 / 8) - int(stone_2d_w/2), stone_2d_y + int(stone_2d_w / 2) + int(
        #         ((400 - sprite.z_distance) / 400) * stone_2d_w) + int(stone_2d_w/2), 0
        self.stone_2d_group.add(stone2d)

    def show_players_in_2d(self, sprite):
        self.player = sprite
        # show player in 2d
        player_2D_l = self.point_3to2([self.player.X, 0, self.player.z_distance])
        player_2D_r = self.point_3to2(
            [self.player.X + self.player.rect.width, 0, self.player.z_distance])
        player_2d_x, player_2d_y = player_2D_l[0], player_2D_l[1]
        player_2d_w, player_2d_h = abs(player_2D_l[0] - player_2D_r[0]), abs(
            player_2D_l[0] - player_2D_r[0])
        self.player2d.master_image = pygame.transform.smoothscale(self.player.master_image,
                                                                  (int(player_2d_w) * 8, int(player_2d_w) * 8))
        self.player2d.load(self.player2d.master_image, player_2d_w, player_2d_h, 8)
        self.player2d.position = player_2d_x, player_2d_y, 0
        self.player2d.frame = self.player.frame
        self.player_2d_group.add(self.player2d)

    @staticmethod
    def coords_to_state(coords):
        x = int(coords[0] / UNIT)
        y = int(coords[1] / UNIT)
        return [x, y]

    @staticmethod
    def state_to_coords(state):
        x = int(state[0] * UNIT)
        y = int(state[1] * UNIT)
        return [x, y]

    # 点3D到2D的坐标映射
    @staticmethod
    def point_3to2(cube):
        cube = np.mat([[cube[0]], [cube[1]], [cube[2]]])
        Pc = rvec * (cube - tvec)
        # 增广一列
        a_ = np.mat([[1]])
        Pc_ = np.r_[Pc, a_]
        Pp = camera_matrix * Pc_ / int(Pc[2])
        return [int(Pp[0]), int(Pp[1])]

    @staticmethod
    def render():
        time.sleep(0.3)
        pygame.display.flip()

    # def start(self):
    #     return self.GameOver

    def close(self):
        pygame.quit()
        sys.exit()

    # 初始化玩家的位置
    def reset(self):
        time.sleep(0.3)
        x, z = self.player.X, self.player.z_distance
        self.player.X, self.player.Y, self.player.z_distance = 0, 50, 900
        return self.coords_to_state([x, z])

    # player moving
    def step(self, action, model=None):
        state = [self.player.X, self.player.z_distance]
        print(state)
        base_action = np.array([0, 0])
        if action == 0:  # up
            self.player.direction = 0
            if state[1] >= UNIT:
                base_action[1] -= UNIT
        elif action == 1:  # down
            self.player.direction = 4
            if state[1] < (HEIGHT - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:  # left
            self.player.direction = 6
            if state[0] >= UNIT:
                base_action[0] -= UNIT
        elif action == 3:  # right
            self.player.direction = 2
            if state[0] < (WIDTH - 1) * UNIT:
                base_action[0] += UNIT

        self.change_frame(self.player.direction)
        self.player.X, self.player.z_distance = self.player.X + base_action[0], self.player.z_distance + base_action[1]
        next_state = [self.player.X, self.player.z_distance]

        # 通过reward判断玩家的next_state
        for sprite1 in self.mushroom_group:
            if self.dict.get((self.player.X, 50, self.player.z_distance)) == sprite1.master_image:
                self.reward = 100
                if model == 'human':
                    self.GameOver = False
                    for sprite in self.mushroom_group:
                        self.mushroom_group.remove(sprite)
                    self.mushroom = mushroom.Mushroom()
                    self.mushroom.position = random.randrange(0, 901, 100), 50, random.randrange(0, 901, 100)
                    self.mushroom_group.add(self.mushroom)
                    self.total_reward += 100
                    self.reward = 0
                #     self.reward += 100
                #     print(self.reward)
                #     self.GameOver = False
                #     self.mushroom_group.remove(sprite1)
                #     self.mushroom = mushroom.Mushroom()
                #     self.mushroom.position = random.randrange(0, 901, 100), 50, random.randrange(0, 901, 100)
                #     self.mushroom_group.add(self.mushroom)
                # else:
                #     self.reward = 100
                #     self.GameOver = True
                else:
                    self.GameOver = True
                break
            else:
                for sprite2 in self.tree_group:
                    if self.dict.get((self.player.X, 100, self.player.z_distance)) == sprite2.master_image:
                        self.reward = -100
                        self.GameOver = True
                        break
                    else:
                        for sprite3 in self.stone_group:
                            if self.dict.get((self.player.X, 100, self.player.z_distance)) == sprite3.master_image:
                                self.reward = -100
                                self.GameOver = True
                                break
                            else:
                                self.reward = 0
                                self.GameOver = False

        next_state = self.coords_to_state(next_state)
        return next_state, self.reward, self.GameOver, self.player.direction

    # 通过direction改变方向
    def change_frame(self, direction):
        self.player.first_frame = direction * self.player.columns
        self.player.last_frame = self.player.first_frame + self.player.columns - 1

        if self.player.frame < self.player.first_frame:
            self.player.frame = self.player.first_frame
        # print(self.frame, self.first_frame, self.last_frame)
        # #self.player_group.update(self.ticks,50)
        # print(self.frame,self.first_frame,self.last_frame)

    # 更新3D map
    def update_map(self):
        self.dict = {}
        for group in self.player_group, self.mushroom_group, self.tree_group, self.sun_group, self.stone_group:
            for sprite in group:
                self.check_map(sprite)

    def show_shadow(self):
        for sprite in self.tree_group:
            tree_shadow = shadow.Shadow()
            tree_shadow.appear_shadow(sprite)
            self.shadow_group.add(tree_shadow)
            for x in range(0, 101, 10):
                pygame.draw.line(self.screen, (0, 0, 0),
                                 self.point_3to2([tree_shadow.X + x, 0, tree_shadow.z_distance]),
                                 self.point_3to2([tree_shadow.X + x, 0, tree_shadow.z_distance + 100]), 2)

    def show_small_map(self):
        self.screen.blit(pygame.image.load("../resources/images/background2d.png"), (800, 0))
        for i in range(800, 1001, 20):
            pygame.draw.line(self.screen, (255, 255, 255), (i, 0), (i, 200))
            for j in range(0, 201, 20):
                pygame.draw.line(self.screen, (255, 255, 255), (800, j), (1000, j))

    def show_grid(self):
        for k in range(0, 1, 1):
            t = (k % 255, k % 255, k % 255)
            for j in range(0, 1001, 100):
                pygame.draw.line(self.screen, t, self.point_3to2([j, k, 0]),
                                 self.point_3to2([j, k, 1000]), 1)
                pygame.draw.line(self.screen, t, self.point_3to2([0, k, j]),
                                 self.point_3to2([1000, k, j]), 1)

    def add_stone_tree_by_mouse(self, arr_stone, arr_tree):
        for array in arr_stone:
            self.stone = stone.Stone()
            self.stone.position = int((array[0] - 800) / 20) * 100, 100, int(array[1] / 20) * 100
            self.stone_group.add(self.stone)
        for array in arr_tree:
            self.tree = tree.Tree()
            self.tree.position = int((array[0] - 800) / 20) * 100, 100, int(array[1] / 20) * 100
            self.tree_group.add(self.tree)

    def show_time(self):
        current_time = self.get_current_time()
        time_text = f'{current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday} {current_time.tm_hour}:{current_time.tm_min} '
        show_text(self.font, 0, 0, time_text, (0, 0, 0))

    def objects_2d_in_2dmap(self):
        for sprite in self.mushroom_group:
            self.show_mushrooms_in_2d(sprite)
        for sprite in self.tree_group:
            self.show_trees_in_2d(sprite)
        for sprite in self.stone_group:
            self.show_stones_in_2d(sprite)
        for sprite in self.shadow_group:
            self.show_shadows_in_2d(sprite)
        self.show_players_in_2d(self.player)

    def objects_sample_in_smap(self):
        self.player_sample.position = int(self.player.X / 100) * 20 + 800, int(
            self.player.z_distance / 5), 0

        for sprite in self.mushroom_group:
            self.mushroom_sample = mushroom.Mushroom()
            self.mushroom_sample.master_image = pygame.transform.smoothscale(self.mushroom.master_image,
                                                                                 (20, 20))
            self.mushroom_sample.load(self.mushroom.master_image, 20, 20, 1)
            self.mushroom_sample.position = int(sprite.X / 100) * 20 + 800, int(
                sprite.z_distance / 5), 0
            for sprite0 in self.mushroom_sample_group:
                self.mushroom_sample_group.remove(sprite0)
            self.mushroom_sample_group.add(self.mushroom_sample)
        for sprite in self.tree_group:
            self.tree_sample = tree.Tree()
            self.tree_sample.master_image = pygame.transform.smoothscale(self.tree.master_image,
                                                                             (20, 20))
            self.tree_sample.load(self.tree.master_image, 20, 20, 1)
            self.tree_sample.position = int(sprite.X / 100) * 20 + 800, int(sprite.z_distance / 5), 0
            self.tree_sample_group.add(self.tree_sample)
        for sprite in self.stone_group:
            self.stone_sample = stone.Stone()
            self.stone_sample.master_image = pygame.transform.smoothscale(self.stone.master_image,
                                                                              (20, 20))
            self.stone_sample.load(self.stone.master_image, 20, 20, 1)
            self.stone_sample.position = int(sprite.X / 100) * 20 + 800, int(sprite.z_distance / 5), 0
            self.stone_sample_group.add(self.stone_sample)