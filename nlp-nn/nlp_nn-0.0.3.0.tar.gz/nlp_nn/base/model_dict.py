# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
词典管理

Authors: fubo01
Date: 2019/11/28 00:00:00
"""
from .abstract import AbstractTagger


class TagsDict(AbstractTagger):
    """
    标签管理
    """

    def __init__(self, tags_file, need_padding_tag=False):
        super().__init__()
        with open(tags_file, "r") as fp:
            self.tags_idx = [line.strip("\r\n") for line in fp.readlines()]

        if need_padding_tag is True:
            self.tags_idx = [self.padding_tag] + self.tags_idx

        self.tags = {term: idx for idx, term in enumerate(self.tags_idx)}

    def tag2id(self, tag: str) -> int:
        """
        label转ID
        :param tag: tag
        :return:
        """
        return self.tags.get(tag, 0)

    def id2tag(self, idx: int) -> str:
        """
        ID转label
        :param idx: label id
        :return:
        """
        if idx >= len(self.tags_idx) or idx < 0:
            return ""
        return self.tags_idx[idx]
