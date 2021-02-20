# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本相关性模型预测

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import torch
from typing import List
from ...base.common import DeviceSettings
from ...model.sent_similarity import SentSimilarity as SentSimilarity_


class SentSimilarity(object):
    def __init__(self, model_path: str):
        self.__similarity = SentSimilarity_(device_settings=DeviceSettings(gpu_idx=-1))
        if self.__similarity.load_released_model(model_path_script=model_path) is False:
            raise ValueError

    def inference(self, pivot_query: str, pos_query: str, neg_query: str) -> (int, float, float):
        """
        短文本分类
        :param pivot_query: pivot_query
        :param pos_query: pos_query
        :param neg_query: neg_query
        :return:
        是否pos query和pivot query的相关性大于 neg query和pivot query的相关性
        pos query和pivot query的相关性
        neg query和pivot query的相关性
        """
        _, label, y_pivot, y_pos, y_neg = self.__similarity.inference(
            pivot_query=pivot_query, pos_query=pos_query, neg_query=neg_query
        )
        score1 = torch.cosine_similarity(y_pivot, y_pos)
        score2 = torch.cosine_similarity(y_pivot, y_neg)
        return label, score1, score2

    def sent2vec(self, query: str) -> torch.FloatTensor:
        """
        短文本转向量
        :param query:
        :return:
        """
        return self.__similarity.sent_encode(query=query)

    def sent_encode_batch(self, queries: List[str]) -> torch.FloatTensor:
        """
        短文本转向量(批量)
        :param queries:
        :return:
        """
        return self.__similarity.sent_encode_batch(queries=queries)

