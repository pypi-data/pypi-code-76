#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :main.py
# @Time     :2021/2/24
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None


import pandas as pd
import json
import sys
from ETAES.operations import excute_pipeline, build_pipeline, build_configurations

def init(kwargs, inputs):
    return build_pipeline(kwargs, inputs)

def infer(pipeline):
    return excute_pipeline(pipeline)

# if __name__ == '__main__':
#     _, config_path = sys.argv
#     kwargs = build_configurations(config_path)
#
#     if kwargs['basic']['status'] == 'online':
#         kwargs['basic']['task_id'] = '1612682787'
#         waybills_df = pd.read_csv('data/waybills.csv')
#         waybills_df.drop(['Unnamed: 0'], axis=1, inplace=True)
#         waybills_str = waybills_df[:2].to_json(orient="records")
#         waybills_js = json.loads(waybills_str)
#         pipeline = init(kwargs, waybills_js)
#         excute_pipeline(pipeline)
#     else:
#         pipeline = init(kwargs, inputs=None)
#         excute_pipeline(pipeline)

    # result = infer()
    # print(result)
