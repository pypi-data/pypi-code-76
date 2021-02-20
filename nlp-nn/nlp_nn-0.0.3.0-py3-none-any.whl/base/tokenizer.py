# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
query序列化

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import copy
from typing import List

import jieba
import transformers
from .abstract import AbstractTokenizer
from .common import BerType, Const
from .model_data import Tokens


class JiebaTokenizer(AbstractTokenizer):
    """
    jieba token化
    """

    def __init__(self, user_dict, terms, max_sent_len):
        super().__init__(max_sent_len)

        jieba.initialize(dictionary=user_dict)
        self.__terms_idx_token = {self.padding_idx: self.padding}
        self.__terms_idx = {self.padding: self.padding_idx}
        with open(terms, "r", encoding="utf-8") as fp:
            self.__terms_idx = {term.strip("\r\n"): idx + 2 for idx, term in enumerate(fp.readlines())}
            self.__terms_idx_token = {idx + 2: term.strip("\r\n") for idx, term in enumerate(fp.readlines())}

    def convert_ids_to_tokens(self, ids: List[int]) -> List[str]:
        """
        id转化token
        """
        return [self.__terms_idx_token.get(idx, self.padding) for idx in ids]

    def tokenize(self, query: str) -> Tokens:
        """
        query序列化
        :param query:
        :return:
        """
        output_tokens = Tokens(query=query, tokens=[], padding_tokens=[])
        if self.__terms_idx is None:
            return output_tokens

        output_tokens.tokens = copy.deepcopy(
            [self.__terms_idx.get(term, self.padding_idx) for term in jieba.cut(query)]
        )
        if self.max_length == 0:
            return output_tokens

        if len(output_tokens.tokens) < self.max_length:
            output_tokens.padding_tokens = output_tokens.tokens + \
                                           [self.padding_idx] * (self.max_length - len(output_tokens.tokens))
        else:
            output_tokens.padding_tokens = copy.deepcopy(output_tokens.tokens[:self.max_length])

        return output_tokens


class BertTokenizer(AbstractTokenizer):
    """
    Bert token化
    """

    def __init__(self, max_sent_len, bert_type=BerType.LITE_BERT, split_by_bert=True):
        super().__init__(max_sent_len)
        self.__split_by_bert = split_by_bert

        self.__tokenizer = None

        if bert_type == BerType.NORM_BERT:
            self.__tokenizer = transformers.BertTokenizer.from_pretrained(Const.BERT_MODEL_PATH)

        if bert_type == BerType.LITE_BERT:
            self.__tokenizer = transformers.BertTokenizer.from_pretrained(Const.ALBERT_MODEL_PATH)

        self.padding_idx = self.__tokenizer.pad_token_id
        self.padding = self.__tokenizer.pad_token

    def convert_ids_to_tokens(self, ids: List[int]) -> List[str]:
        """
        id转化token
        """
        return self.__tokenizer.convert_ids_to_tokens(ids=ids)

    def tokenize(self, query: str) -> Tokens:
        """
        query序列化
        :param query:
        :return:
        """
        output_tokens = Tokens(query=query, tokens=[], padding_tokens=[])
        if self.__tokenizer is None:
            return output_tokens
        if self.__split_by_bert:
            output_tokens.tokens = copy.deepcopy(self.__tokenizer.encode(query, add_special_tokens=False))
        else:
            output_tokens.tokens = self.__tokenizer.convert_tokens_to_ids(list(query.lower()))

        if self.max_length == 0:
            return output_tokens

        if len(output_tokens.tokens) < self.max_length:
            output_tokens.padding_tokens = output_tokens.tokens + \
                                           [self.padding_idx] * (self.max_length - len(output_tokens.tokens))
        else:
            output_tokens.padding_tokens = copy.deepcopy(output_tokens.tokens[:self.max_length])

        return output_tokens
