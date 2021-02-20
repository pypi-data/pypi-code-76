# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本分类模型导出

Authors: fubo
Date: 2019/11/28 00:00:00
"""

import sys
import logging
import argparse
from ...model.sent_classifier import DeviceSettings
from ...model.sent_classifier import SentClassify


def main():
    log_format_string = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format_string, stream=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument("ckpt_path", type=str, help="CKPT path of model")
    parser.add_argument("release_path", type=str, help="Release path of model")
    args = parser.parse_args()
    release_path = args.release_path
    ckpt_path = args.ckpt_path
    sent_classify = SentClassify(device_settings=DeviceSettings(gpu_idx=-1))
    if sent_classify.load_model_ckpt(model_path_ckpt=ckpt_path) is False:
        logging.error("Failed to load ckpt model")
        return -1
    if sent_classify.release_model(model_path_ckpt=ckpt_path, model_path_script=release_path):
        logging.error("Failed to release model")
        return -2

    return 0


if __name__ == '__main__':
    main()
