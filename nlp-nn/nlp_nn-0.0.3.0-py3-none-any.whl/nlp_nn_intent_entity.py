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
from typing import Dict
from .base.common import DeviceSettings
from .model.intent_entity import IntentEntity as IntentSlot_


class IntentSlot(object):
    def __init__(self, model_path: str):
        self.__parser = IntentSlot_(device_settings=DeviceSettings(gpu_idx=-1))
        if self.__parser.load_released_model(model_path_script=model_path) is False:
            raise ValueError

    def parse(self, query: str) -> Dict:
        """
        短文本意图实体识别
        :param query:
        :return:
        """
        return self.__parser.inference(query=query)
