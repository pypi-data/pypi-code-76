# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本分类模型训练

Authors: fubo
Date: 2019/11/28 00:00:00
"""

import os
import sys
import logging
import argparse
from ...model.sent_classifier import SentClassifyModelSettings, SentClassifyCoachSettings, DeviceSettings
from ...model.sent_classifier import SentClassify


def main():
    local_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
    log_format_string = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format_string, stream=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max_tokens", type=int, help="Max text tokens length", default=200, required=False
    )
    parser.add_argument(
        "--sent_encode_dim", type=int, help="Sentence encoding vector dim", default=512, required=False
    )
    parser.add_argument(
        "--attention_vector_size", type=int, help="Attention layer dim", default=256, required=False
    )
    parser.add_argument(
        "--drop_out_prob", type=float, help="Drop out probability", default=0.2, required=False
    )
    parser.add_argument(
        "--gpu_idx", type=int, help="GPU index(-1 for CPU)", default=-1, required=False
    )
    parser.add_argument(
        "--tf_log_dir", type=str, help="Tensor board log path",
        default=os.sep.join([local_path, "log"]), required=False
    )
    parser.add_argument(
        "--train_dir", type=str, help="Train env path",
        default=os.sep.join([local_path, "train_dir"]), required=False
    )
    parser.add_argument(
        "--dict_dir", type=str, help="Dict path",
        default=os.sep.join([local_path, "dict"]), required=False
    )
    parser.add_argument(
        "--data_dir", type=str, help="Data path", default=os.sep.join([local_path, "data"]), required=False
    )
    parser.add_argument(
        "--pkl_model_file", type=str, help="Pickel model file name", default="sent_classify.pkl", required=False
    )
    parser.add_argument(
        "--class_label", type=str, help="Class label file", default="labels.dic", required=False
    )
    parser.add_argument(
        "--train_data_set_file", type=str, help="Train data file", default="sample.train", required=False
    )
    parser.add_argument(
        "--valid_data_set_file", type=str, help="Valid data file", default="sample.valid", required=False
    )
    parser.add_argument(
        "--train_batch_size", type=int, help="Train batch size", default=256, required=False
    )
    parser.add_argument(
        "--valid_batch_size", type=int, help="Valid batch size", default=256, required=False
    )
    parser.add_argument(
        "--lr", type=float, help="Learning rate", default=0.0005, required=False
    )
    parser.add_argument(
        "--lr_weight_decay", type=float, help="Learning rate decay rate", default=0.000005, required=False
    )
    parser.add_argument(
        "--model_name", type=str, help="Model name", default=local_path.split(os.sep)[-1], required=False
    )
    parser.add_argument(
        "--model_describe", type=str, help="Model describe", default=local_path.split(os.sep)[-1], required=False
    )

    args = parser.parse_args()
    device_settings = DeviceSettings(gpu_idx=args.gpu_idx)
    coach_settings = SentClassifyCoachSettings(
        tf_log_dir=args.tf_log_dir,
        train_models_dir=args.train_dir,
        dict_dir=args.dict_dir,
        data_dir=args.data_dir,
        model_file=args.pkl_model_file,
        class_label=args.class_label,
        train_data_set_file=args.train_data_set_file,
        valid_data_set_file=args.valid_data_set_file,
        train_batch_size=args.train_batch_size,
        valid_batch_size=args.valid_batch_size,
        lr=args.lr,
        lr_weight_decay=args.lr_weight_decay
    )
    model_settings = SentClassifyModelSettings(
        model_name=args.model_name,
        model_describe=args.model_describe,
        max_tokens=args.max_tokens,
        sent_encode_dim=args.sent_encode_dim,
        attention_vector_size=args.attention_vector_size,
        drop_out_prob=args.drop_out_prob
    )

    model = SentClassify(
        device_settings=device_settings,
        coach_settings=coach_settings,
        model_settings=model_settings
    )
    model.prepare_for_training()
    model.start_training()


if __name__ == '__main__':
    main()
