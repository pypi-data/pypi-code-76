#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :builder.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import yaml
import os

def build_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        return config


def build_paths(task_id, configs):
    path_cfgs = configs['basic']['paths']
    # mlflow_tracking_path = path_cfgs.pop('mlflow_tracking_path')
    # if not os.path.exists(mlflow_tracking_path):
    #     os.mkdir(mlflow_tracking_path)
    for k, v in path_cfgs.items():
        v = v.format(task_id=task_id)
        if not os.path.exists(v):
            if not '/' in v:
                os.mkdir(v)
            else:
                path_items = v.split('/')[:-1]
                for idx, item in enumerate(path_items):
                    path = '/'.join(path_items[: min(idx + 1, len(path_items))])
                    if not os.path.exists(path):
                        os.mkdir(path)

