# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
模型层管理

Authors: fubo
Date: 2019/11/28 00:00:00
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import torch
import transformers
from .common import BerType, Const


class EmbeddingLayer(torch.nn.Module):
    """
    Embedding lookup table层
    """
    def __init__(self, vocab_size, dim):
        super().__init__()
        self.layer = torch.nn.Embedding(vocab_size, dim)
        torch.nn.init.uniform_(self.layer.weight)

    def forward(self, x):
        """
        :param x:
        :return:
        """
        return self.layer(x)


class BertEmbeddingLayer(torch.nn.Module):
    """
    Bert embedding 层
    """
    def __init__(self, bert_type=BerType.LITE_BERT):
        super().__init__()
        self.layer = None

        if bert_type == BerType.NORM_BERT:
            self.layer = transformers.BertModel.from_pretrained(Const.BERT_MODEL_PATH)

        if bert_type == BerType.LITE_BERT:
            self.layer = transformers.AutoModel.from_config(
                transformers.AlbertConfig.from_pretrained(Const.ALBERT_MODEL_PATH)
            )

        self.hidden_size = self.layer.config.hidden_size

    def forward(self, x):
        """
        向后计算
        :param x:
        :return:
        """
        if self.layer is None:
            return None
        return self.layer(x)


class SelfAttentionLayer(torch.nn.Module):
    """
    自注意力层
    """
    def __init__(self, embedding_size, attention_vector_size):
        super().__init__()
        self.converge_layer = torch.nn.Linear(
            in_features=embedding_size,
            out_features=attention_vector_size,
            bias=False
        )
        self.attention_layer = torch.nn.Linear(in_features=attention_vector_size, out_features=1, bias=False)
        torch.nn.init.xavier_uniform_(self.converge_layer.weight)
        torch.nn.init.xavier_uniform_(self.attention_layer.weight)

    def forward(self, x):
        """
        向后计算
        :param x:
        :return:
        """
        y = torch.tanh(self.converge_layer(x))
        attention = torch.softmax(self.attention_layer(y), dim=1)
        x = torch.bmm(attention.transpose(1, 2), x).squeeze(dim=1)
        return x, attention.squeeze(dim=2)


class LinearLayer(torch.nn.Module):
    """
    全连接层
    """
    def __init__(self, n_input_dim, n_output_dim, with_bias=False):
        super().__init__()
        self.linear_layer = torch.nn.Linear(
            in_features=n_input_dim,
            out_features=n_output_dim,
            bias=with_bias
        )
        torch.nn.init.xavier_uniform_(self.linear_layer.weight)

    def forward(self, x):
        """
        向后计算
        :param x:
        :return:
        """
        return self.linear_layer(x)


class BertSentEncodeAvePoolingLayer(torch.nn.Module):
    """
    基于bert average pooling句编码layer
    """
    def __init__(self, sent_encode_dim, bert_type=BerType.LITE_BERT):
        """
        :param sent_encode_dim:
        :param bert_type:
        """
        super().__init__()
        # Embedding映射层##########
        self.embedding_layer = BertEmbeddingLayer(bert_type=bert_type)
        embedding_dim = self.embedding_layer.hidden_size

        # Encode linear layer
        self.linear_layer = LinearLayer(embedding_dim, sent_encode_dim)

    def forward(self, x):
        """
        :param x:
        :return:
        """
        return self.linear_layer(self.embedding_layer(x)[1])


class BertSentEncodeTermLevelLayer(torch.nn.Module):
    """
    基于bert layer，term粒度
    """
    def __init__(self, bert_type=BerType.LITE_BERT):
        """
        :param bert_type:
        """
        super().__init__()
        # Embedding映射层##########
        self.embedding_layer = BertEmbeddingLayer(bert_type=bert_type)

    def forward(self, x):
        """
        :param x:
        :return:
        """
        return self.embedding_layer(x)[0]


class BertSentEncodeSelfAttentionLayer(torch.nn.Module):
    """
    基于bert self-attention句编码layer
    """
    def __init__(self, sent_encode_dim, attention_vector_size=64, bert_type=BerType.LITE_BERT):
        """
        基于bert的句向量编码
        :param sent_encode_dim:
        :param attention_vector_size:
        :param bert_type:
        """
        super().__init__()

        # Embedding映射层##########
        self.embedding_layer = BertEmbeddingLayer(bert_type=bert_type)
        embedding_dim = self.embedding_layer.hidden_size

        # 自注意力layer
        self.self_attention_layer = SelfAttentionLayer(
            embedding_size=embedding_dim,
            attention_vector_size=attention_vector_size
        )

        # Encode linear layer
        self.linear_layer = LinearLayer(embedding_dim, sent_encode_dim)

    def forward(self, x):
        """

        :param x:
        :return:
        """
        return self.linear_layer(self.self_attention_layer(self.embedding_layer(x)[0])[0])


class CrossLayer(torch.nn.Module):
    """
    Cross layer part in Cross and Deep Network
    The ops in this module is x_0 * x_l^T * w_l + x_l + b_l for each layer l, and x_0 is the init input of this module
    """

    def __init__(self, input_feature_num, cross_layer):
        """
        :param input_feature_num: total num of input_feature, including of the embedding feature and dense feature
        :param cross_layer: the number of layer in this module expect of init op
        """
        super().__init__()
        self.cross_layer = cross_layer + 1  # add the first calculate
        weight_w = []
        weight_b = []
        batch_norm = []
        for i in range(self.cross_layer):
            weight_w.append(torch.nn.Parameter(torch.nn.init.normal_(torch.empty(input_feature_num))))
            weight_b.append(torch.nn.Parameter(torch.nn.init.normal_(torch.empty(input_feature_num))))
            batch_norm.append(torch.nn.BatchNorm1d(input_feature_num, affine=False))
        self.weight_w = torch.nn.ParameterList(weight_w)
        self.weight_b = torch.nn.ParameterList(weight_b)
        self.batch_norm = torch.nn.ModuleList(batch_norm)

    def forward(self, x):
        """
        向后计算
        :param x:
        :return:
        """
        output = x
        x = x.reshape(x.shape[0], -1, 1)
        for i in range(self.cross_layer):
            output = torch.matmul(torch.bmm(x, torch.transpose(output.reshape(output.shape[0], -1, 1), 1, 2)),
                                  self.weight_w[i]) + self.weight_b[i] + output
            output = self.batch_norm[i](output)
        return output
