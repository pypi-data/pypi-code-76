# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本转向量模型

Authors: fubo
Date: 2019/11/28 00:00:00
"""
from typing import List

import torch
from .base.common import DeviceSettings
from .model.sent_similarity_cross import SentSimilarity


class SentSimilarityCross(object):
    def __init__(self, model_path: str):
        self.__model = SentSimilarity(device_settings=DeviceSettings(gpu_idx=-1))
        if self.__model.load_released_model(model_path_script=model_path) is False:
            raise ValueError

    def similarity(self, query1: str, query2: str) -> float:
        """
        计算query相似度
        :param query1:
        :param query2:
        :return:
        """
        return self.__model.inference(query1=query1, query2=query2)

    def base_encode(self, queries: List[str]) -> torch.FloatTensor:
        """
        短文本转向量
        :param queries:
        :return:
        """
        return self.__model.base_encode(queries=queries)

    def base_encode_similarity(self, tokens1: torch.FloatTensor, tokens2: torch.FloatTensor) -> float:
        """
        短文本转向量
        :param tokens1:
        :param tokens2:
        :return:
        """
        return self.__model.base_encode_similarity(tokens1=tokens1, tokens2=tokens2)
