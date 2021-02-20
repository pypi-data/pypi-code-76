# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本分类模型预测

Authors: fubo
Date: 2019/11/28 00:00:00
"""
from typing import List, Dict
from ...base.common import DeviceSettings
from ...model.token_classifier import TokenClassify as TokenClassify_


class TokenClassify(object):
    def __init__(self, model_path: str):
        self.__classifier = TokenClassify_(device_settings=DeviceSettings(gpu_idx=-1))
        if self.__classifier.load_released_model(model_path_script=model_path) is False:
            raise ValueError

    def inference(self, query: str) -> Dict:
        """
        短文本分类
        :param query
        :return:
        """
        return self.__classifier.inference(query=query)

