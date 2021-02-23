#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : main.py
@Author: Perhaps
@Date  : 2021/2/23 11:23 上午
@Desc  : 
"""
import pickle
from app.mushroomer_Qlearning import MushroomerQlearning
from game import *
from ml_algorithm import *

# RUN = sys.argv[1]
# MODEL = sys.argv[2]
Train = False

if __name__ == "__main__":

    mushroom_app = MushroomerQlearning()
    env = Env()
    agent = QLearningBase(actions=list(range(env.n_actions)))

    if Train:
        q_table = mushroom_app.train(agent)
        print(q_table)
        with open('q_table.pkl', "wb") as f:
            f.write(pickle.dumps(dict(q_table)))
    else:
        with open('q_table.pkl', "rb") as f:
            q_table = pickle.load(f)
        mushroom_app.run(agent, q_table, model='human')
