#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : q_learning.py
# @Author: perhaps
# @Date  : 2021/2/4
# @Desc  : 基础的Q_Learning算法

import random
import numpy as np
from collections import defaultdict

from ml_algorithm.algorithmABC import AlgorithmABC


class QLearningBase(AlgorithmABC):
    def __init__(self, actions):
        # actions = [0, 1, 2, 3]
        self.actions = actions
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    # 采样 <s, a, r, s'>
    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        # 贝尔曼方程更新
        new_q = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)

    def optimize(self):
        pass

    # 从Q-table中选取动作
    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            # 贪婪策略随机探索动作
            action = np.random.choice(self.actions)
        else:
            # 从q表中选择
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
        return action

    @staticmethod
    def arg_max(state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)
