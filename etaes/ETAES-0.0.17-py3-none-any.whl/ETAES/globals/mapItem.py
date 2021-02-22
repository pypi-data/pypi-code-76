#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :mapItem.py
# @Time     :2021/2/2
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import os
import sklearn.metrics as metrics
import sklearn.linear_model as linear_model
import sklearn.preprocessing as preprocessing
import sklearn.model_selection as model_selection
import sklearn.tree as tree
import sklearn.impute as impute
import sklearn.base as base
import sklearn.ensemble as emsemble
import sklearn.neighbors as neighbors
import sklearn.svm as svm

import lightgbm as lgb
import importlib
import sys


# TODO(jiawei.li@shopee.com): To many module need to load ?
def build_mapping_classes():
    mapping_classes = [
        metrics,
        linear_model,
        preprocessing,
        model_selection,
        tree,
        impute,
        base,
        lgb,
        emsemble,
        neighbors,
        svm,
    ]
    import site
    excute_path = site.getsitepackages()[0]  + '/TEST_ETAE'
    sys.path.append(excute_path)
    params = importlib.import_module('externals')
    mapping_classes.append(params)
    return mapping_classes
