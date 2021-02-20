# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
通用数据定义

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import os
import hashlib
from typing import List, Tuple

from pydantic import BaseModel
from enum import Enum
import torch


class ModelState(Enum):
    """ 模型状态 """
    # 预测状态
    INFERENCE = 0
    TRAIN = 1


class BerType(Enum):
    """ bert类型 """
    # 常规Bert
    NORM_BERT = 0

    # Lite Bert
    LITE_BERT = 1


class ModelDataType(Enum):
    """ 模型数据类型 """
    # 训练数据
    TRAIN = 0

    # 验证数据
    VALID = 1


class DeviceSettings(BaseModel):
    """ 模型使用的设备信息（GPU） """
    # gpu的device序号(-1表示使用CPU)
    gpu_idx: int = -1


class ExportModelSettings(BaseModel):
    """ 导出模型文件配置 """

    # 导出模型文件配置文件
    model_config_file: str = "config.json"

    # 主模型文件
    model_file: str = "model.pt"

    # 第三方词典文件
    third_dict_dir: str = "dict"


class CoachSettings(BaseModel):
    """ 训练配置 """
    # tf board 日志存放路径
    tf_log_dir: str = "log"

    # 模型训练环境临时模型存储路径
    train_models_dir: str = "train_dir"

    # 第三方资源路径
    dict_dir: str = "dict"

    # 数据集路径
    data_dir: str = "data"

    # 模型文件名
    model_file: str = "model.pkl"

    # 模型配置文件名
    model_conf_file: str = "config.json"

    # 训练集文件名
    train_data_set_file: str = ""

    # 验证集文件名
    valid_data_set_file: str = ""

    # valid模型的频次per epoch
    valid_interval: int = 1

    # 模型训练最大epoch数量
    max_epoch_times: int = 100

    # 训练集的batch size
    train_batch_size: int = 10

    # 验证集的batch size
    valid_batch_size: int = 0

    # 学习率
    lr: float = 0.000001

    # 学习率的衰减率
    lr_weight_decay: float = 0.0000005


class ModelSettings(BaseModel):
    """ 模型配置 """

    # 模型名称
    model_name: str = ""

    # 模型描述
    model_describe: str = ""


class Utils(object):
    """ 常用工具 """

    @staticmethod
    def data_sign_sha512(data):
        """
        data 签名
        :param data:
        :return:
        """
        sha512 = hashlib.sha512()
        sha512.update(data.encode("utf-8"))
        return sha512.hexdigest()

    @staticmethod
    def data_sign_md5(data):
        """
        data 签名
        :param data:
        :return:
        """
        md5 = hashlib.md5()
        md5.update(data.encode("utf-8"))
        return md5.hexdigest()

    @staticmethod
    def reciprocal_log_nature_sum(num: int, values: torch.LongTensor) -> float:
        """
        自然数迭代的log倒数和
        num: 序列数量 batch * num
        """
        return float(torch.sum(values / torch.log2(torch.linspace(1, num, steps=num) + 2), dim=0))


class Metric(object):
    @staticmethod
    def positional_weighted_rpf(
            ground_truth: torch.LongTensor,
            scores: torch.FloatTensor,
            point_count: int = 10
    ) -> torch.FloatTensor:
        """
        基于位置权重的RPF
        ground_truth: 标注结果 batch * instance_count
        scores: 预测分数 batch * instance_count
        point_count: 阈值数量
        return point_count * batch * 4(point, recall, precision, f-score)
        """
        # ground_truth = torch.LongTensor([[1, 0, 1, 0]])
        # scores = torch.FloatTensor([[0.55, 0.13, 0.63, 0.99]])
        if point_count < 1:
            raise ValueError
        if point_count == 1:
            thresholds = [0.5]
        else:
            thresholds = [(i * 1.0) / point_count for i in range(point_count)]

        results = torch.zeros(point_count, ground_truth.shape[0], 4)
        ground_truth_count = ground_truth.sum(dim=1)

        for index, threshold in enumerate(thresholds):
            # 阈值
            threshold_m = threshold * torch.ones(ground_truth.shape[0], 1)

            # 阈值过滤
            predict_score = scores * (scores >= threshold)
            predict_count = (predict_score > 0).sum(dim=1)

            # 排序预测结果
            predict_score_values, predict_score_index = torch.sort(predict_score, descending=True)

            # 标注确认正确的数据
            confirm_label = ground_truth * predict_score
            confirm_count = (confirm_label > 0).sum(dim=1)

            # 召回
            recall = torch.unsqueeze(confirm_count.float() / ground_truth_count.float(), 1)

            # 精确率
            precision = torch.zeros(ground_truth.shape[0], 1)
            for i in range(confirm_label.shape[0]):
                predict_full = torch.ones(int(predict_count[i]))
                predict_select = (
                        (confirm_label[i, :].index_select(0, predict_score_index[i, :int(predict_count[i])])) > 0
                ).long()
                denominator = Utils.reciprocal_log_nature_sum(int(predict_count[i]), predict_full)
                numerator = Utils.reciprocal_log_nature_sum(int(predict_count[i]), predict_select)
                precision[i, 0] = numerator / (denominator + 0.0000000001)

            # F-Score
            f_score = (2 * recall * precision) / (recall + precision + 0.0000000001)

            results[index, :, :] = torch.cat((threshold_m, recall, precision, f_score), dim=1)

        return results

    @staticmethod
    def ranking_mean_average_precision(relevant_counts: List[int], correct_index: List[List[int]]) -> Tuple:
        """
        排序的NDCG指标
        :param relevant_counts: 相关文档数量列表
        :param correct_index: 正确文档列表位置（从1开始）
        """
        if (len(relevant_counts) <= 0) or (len(relevant_counts) != len(correct_index)):
            # 计算的检索数量不一致
            return -1.0, []

        sum_ap = 0.0
        aps = []
        for i, count in enumerate(relevant_counts):
            index = correct_index[i]
            if min(index) < 1:
                # 正确文档的位置不在正确的范围
                return -1.0, []
            scores = [(j + 1) / index[j] if j < len(index) else 0.0 for j in range(count)]
            aps.append(1.0 * sum(scores) / len(scores))
            sum_ap = sum_ap + aps[-1]

        return 1.0 * sum_ap / len(relevant_counts), aps


class Const(object):
    """ 通用的常量 """
    # 最小正数
    MIN_POSITIVE_NUMBER = 0.0000000001

    # bert预训练模型
    BERT_MODEL_PATH = os.sep.join(
        os.path.abspath(__file__).split(os.sep)[:-1] + [
            "..", "third_models", "transformer.models", "bert_model_pytorch"
        ]
    )
    # albert预训练模型
    ALBERT_MODEL_PATH = os.sep.join(
        os.path.abspath(__file__).split(os.sep)[:-1] + [
            "..", "third_models", "transformer.models", "albert_tiny_pytorch"
        ]
    )
