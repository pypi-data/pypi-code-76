# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
数据类定义

Authors: fubo
Date: 2019/11/28 00:00:00
"""
from pydantic import BaseModel
from typing import List


class LabelResult(BaseModel):
    """ 分类类别结果 """
    # 类别ID
    label_idx: int

    # 类别名
    label_name: str

    # 类别分数
    score: float


class EntityElemResult(BaseModel):
    """ 实体结果 """
    # 实体标签ID
    entity_idx: int

    # 实体标签
    entity_label: str

    # 实体标签分数
    entity_score: float

    # 原始实体term
    raw_value: str

    # 原始实体term起始未知
    term_start: int

    # 原始实体term长度
    value_length: int


class ClassifyResult(BaseModel):
    """ 分类结果 """
    labels: List[LabelResult]


class EntityResult(BaseModel):
    """ 实体结果 """
    entities: List[EntityElemResult]


class IntentSlotResult(BaseModel):
    """ 意图实体结果 """
    # 意图结果
    intent: LabelResult

    # 实体结果
    entities: EntityResult


class Tokens(BaseModel):
    """ token序列数据 """
    # 原始query
    query: str

    # 分词token的id序列
    tokens: List[int]

    # 分词token的id序列，padding到最大长度
    padding_tokens: List[int]


class TaggingSample(BaseModel):
    """ tagging问题数据 """
    # query
    queries: List[str]

    # label
    labels: List[str]


class TokenLabel(BaseModel):
    """ 实体标签 """
    # 实体名
    label: str

    # 起始点
    pos: int

    # 长度
    length: int

    # 实体内容
    text: str = ""


class IntentEntitySample(BaseModel):
    """ intent slot数据 """
    # query
    query: str

    # 意图label
    intent_label: str

    # 实体label
    entity_labels: List[TokenLabel] = []


class TextClassifySample(BaseModel):
    """ 文本分类问题数据 """
    # query
    queries: List[str]

    # label
    labels: List[str]


class TokenClassifySample(BaseModel):
    # query
    query: str

    # 实体label
    token_labels: List[TokenLabel] = []
