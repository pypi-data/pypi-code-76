#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mushroomer_Qlearning.py
# @Author: Perhaps
# @Date  : 2021/2/4
# @Desc  : 游戏"采蘑菇的小姑娘"
from collections import defaultdict
from pygame.locals import *
from game import *

sys.path.append("../")
sys.path.append("./")
q_table_train = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
arr_stone = []
arr_tree = []


class MushroomerQlearning:

    def __init__(self):
        pygame.init()
        self.env = Env()
        self.agent = None
        self.action = None
        self.timer = pygame.time.Clock()

    def run(self, agent, q_table, model=None):
        self.agent = agent

        for episode in range(1000):
            state = self.env.reset()
            while True:
                pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN])
                self.timer.tick(200)
                ticks = pygame.time.get_ticks()
                # 设置停止键
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.env.close()

                # agent产生动作
                if model == 'AI':
                    self.agent.q_table = q_table
                    self.action = self.agent.select_action(str(state))
                    next_state, reward, GameOver, direction = self.env.step(self.action, model='AI')
                    state = next_state
                    pygame.time.delay(5)
                elif model == 'human':
                    self.get_events(events)
                    self.get_events(events)
                    if self.env.player_moving:
                        next_state, reward, self.env.GameOver, self.env.player.direction = self.env.step(self.action,
                                                                                                         model='human')
                        self.env.player_moving = False
                    # else:
                    #     self.env.player.frame = self.env.player.first_frame = self.env.player.last_frame
                    show_text(self.env.font, 500, 0, 'YOUR SCORE IS : ' + f'{self.env.total_reward}', (255, 255, 0))

                # 通过鼠标添加树和石头
                self.env.add_stone_tree_by_mouse(arr_stone, arr_tree)

                # 更新3D 精灵的group
                self.env.tree_group.update(ticks, 50)
                self.env.mushroom_group.update(ticks, 50)
                self.env.stone_group.update(ticks, 50)
                self.env.player_group.update(ticks, 50)
                self.env.shadow_group.update(ticks, 50)

                # 更新3D地图
                self.env.update_map()

                # 3D 2D所有物体映射转换
                for sprite in self.env.mushroom_group:
                    self.env.show_mushrooms_in_2d(sprite)
                for sprite in self.env.tree_group:
                    self.env.show_trees_in_2d(sprite)
                for sprite in self.env.stone_group:
                    self.env.show_stones_in_2d(sprite)
                for sprite in self.env.shadow_group:
                    self.env.show_shadows_in_2d(sprite)
                self.env.show_players_in_2d(self.env.player)

                # 大地图小地图物体位置映射转换
                self.env.player_sample.position = int(self.env.player.X / 100) * 20 + 800, int(
                    self.env.player.z_distance / 5), 0

                for sprite in self.env.mushroom_group:
                    self.env.mushroom_sample = mushroom.Mushroom()
                    self.env.mushroom_sample.master_image = pygame.transform.smoothscale(self.env.mushroom.master_image,
                                                                                         (20, 20))
                    self.env.mushroom_sample.load(self.env.mushroom.master_image, 20, 20, 1)
                    self.env.mushroom_sample.position = int(sprite.X / 100) * 20 + 800, int(
                        sprite.z_distance / 5), 0
                    for sprite0 in self.env.mushroom_sample_group:
                        self.env.mushroom_sample_group.remove(sprite0)
                    self.env.mushroom_sample_group.add(self.env.mushroom_sample)
                for sprite in self.env.tree_group:
                    self.env.tree_sample = tree.Tree()
                    self.env.tree_sample.master_image = pygame.transform.smoothscale(self.env.tree.master_image,
                                                                                     (20, 20))
                    self.env.tree_sample.load(self.env.tree.master_image, 20, 20, 1)
                    self.env.tree_sample.position = int(sprite.X / 100) * 20 + 800, int(sprite.z_distance / 5), 0
                    self.env.tree_sample_group.add(self.env.tree_sample)
                for sprite in self.env.stone_group:
                    self.env.stone_sample = stone.Stone()
                    self.env.stone_sample.master_image = pygame.transform.smoothscale(self.env.stone.master_image,
                                                                                      (20, 20))
                    self.env.stone_sample.load(self.env.stone.master_image, 20, 20, 1)
                    self.env.stone_sample.position = int(sprite.X / 100) * 20 + 800, int(sprite.z_distance / 5), 0
                    self.env.stone_sample_group.add(self.env.stone_sample)

                # 填充屏幕
                self.env.screen.fill((50, 50, 100))

                # 创建背景
                self.env.build_background()

                # 暂时单独显示太阳
                self.env.sun_group.update(ticks, 50)
                self.env.sun_group.draw(self.env.screen)

                # 显示阴影
                self.env.show_shadow()

                # 创建小地图
                self.env.show_small_map()

                # 绘画网格线
                self.env.show_grid()

                # 显示时间
                self.env.show_time()

                # 显示所有小地图物体
                self.env.player_sample_group.update(ticks, 50)
                self.env.player_sample_group.draw(self.env.screen)

                self.env.mushroom_sample_group.update(ticks, 50)
                self.env.mushroom_sample_group.draw(self.env.screen)

                self.env.tree_sample_group.update(ticks, 50)
                self.env.tree_sample_group.draw(self.env.screen)

                self.env.stone_sample_group.update(ticks, 50)
                self.env.stone_sample_group.draw(self.env.screen)

                # 显示所有2D物体
                self.env.mushroom_2d_group.update(ticks, 50)
                self.env.mushroom_2d_group.draw(self.env.screen)

                self.env.shadow_2d_group.update(ticks, 50)
                self.env.shadow_2d_group.draw(self.env.screen)

                self.env.tree_2d_group.update(ticks, 50)
                self.env.tree_2d_group.draw(self.env.screen)

                self.env.stone_2d_group.update(ticks, 50)
                self.env.stone_2d_group.draw(self.env.screen)

                self.env.player2d.direction = self.env.player.direction
                self.env.player_2d_group.update(ticks, 50)
                self.env.player_2d_group.draw(self.env.screen)
                # 渲染
                self.env.render()
                if self.env.GameOver:
                    break

    def train(self, agent):
        self.agent = agent
        global q_table_train
        for episode in range(300):
            state = self.env.reset()
            print(episode)
            while True:
                # 设置停止键
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.env.close()
                # 更新地图
                self.env.update_map()
                # agent产生动作
                action = self.agent.select_action(str(state))
                next_state, reward, GameOver, direction = self.env.step(action, model='AI')
                # 更新Q表
                self.agent.learn(str(state), action, reward, str(next_state))
                state = next_state
                q_table_train = self.agent.q_table

                if GameOver:
                    break
        return q_table_train

    def get_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 800 <= event.pos[0] <= 1000 and 0 <= event.pos[1] <= 200:
                    arr_tree.append(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if 800 <= event.pos[0] <= 1000 and 0 <= event.pos[1] <= 200:
                    arr_stone.append(event.pos)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.action = 2
                    self.env.player_moving = True
                elif event.key == pygame.K_RIGHT:
                    self.action = 3
                    self.env.player_moving = True
                elif event.key == pygame.K_UP:
                    self.action = 0
                    self.env.player_moving = True
                elif event.key == pygame.K_DOWN:
                    self.action = 1
                    self.env.player_moving = True
                else:
                    self.env.player_moving = False
