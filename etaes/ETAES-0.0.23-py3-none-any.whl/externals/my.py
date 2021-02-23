#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :my.py
# @Time     :2021/2/4
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
fig = plt.figure()
fig.set(alpha=0.2)

def get_info(inputs):
    return inputs.info()

def get_desc(inputs):
    return inputs.describe()

def survived(inputs):
    plt.subplot2grid((2, 3), (0, 0))  # 在一张大图里分列几个小图
    inputs.Survived.value_counts().plot(kind='bar')  # 柱状图 
    plt.title(u"获救情况 (1为获救)")  # 标题
    plt.ylabel(u"人数")

    plt.subplot2grid((2, 3), (0, 1))
    inputs.Pclass.value_counts().plot(kind="bar")
    plt.ylabel(u"人数")
    plt.title(u"乘客等级分布")

    plt.subplot2grid((2, 3), (0, 2))
    plt.scatter(inputs.Survived, inputs.Age)
    plt.ylabel(u"年龄")  # 设定纵坐标名称
    plt.grid(b=True, which='major', axis='y')
    plt.title(u"按年龄看获救分布 (1为获救)")

    plt.subplot2grid((2, 3), (1, 0), colspan=2)
    inputs.Age[inputs.Pclass == 1].plot(kind='kde')
    inputs.Age[inputs.Pclass == 2].plot(kind='kde')
    inputs.Age[inputs.Pclass == 3].plot(kind='kde')
    plt.xlabel(u"年龄")  # plots an axis lable
    plt.ylabel(u"密度")
    plt.title(u"各等级的乘客年龄分布")
    plt.legend((u'头等舱', u'2等舱', u'3等舱'), loc='best')  # sets our legend for our graph.

    plt.subplot2grid((2, 3), (1, 2))
    inputs.Embarked.value_counts().plot(kind='bar')
    plt.title(u"各登船口岸上船人数")
    plt.ylabel(u"人数")
    return plt

def attribute(inputs):
    Survived_0 = inputs.Pclass[inputs.Survived == 0].value_counts()
    Survived_1 = inputs.Pclass[inputs.Survived == 1].value_counts()
    df = pd.DataFrame({u'获救': Survived_1, u'未获救': Survived_0})
    df.plot(kind='bar', stacked=True)
    plt.title(u"各乘客等级的获救情况")
    plt.xlabel(u"乘客等级")
    plt.ylabel(u"人数")
    return plt

class LabelEncoderAdv(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):

    def __init__(self, unknown_original_value='unknown',
                 unknown_encoded_value=-1):
        """
        It differs from LabelEncoder by handling new classes and providing a value for it [Unknown]
        Unknown will be added in fit and transform will take care of new item. It gives unknown class id
        """
        self.unknown_original_value = unknown_original_value
        self.unknown_encoded_value = unknown_encoded_value
        self.label_encoder = sklearn.preprocessing.LabelEncoder()
        self.classes_ = None

    def fit(self, X, y=None):
        """
        This will fit the encoder for all the unique values and introduce unknown value
        :param X: A list of string
        :return: self
        """
        y = sklearn.utils.validation.column_or_1d(X, warn=True)

        self.label_encoder = self.label_encoder.fit(list(X) + ['unknown'])
        self.classes_ = self.label_encoder.classes_

        return self

    def transform(self, y):
        sklearn.utils.validation.check_is_fitted(self, 'classes_')
        y = sklearn.utils.validation.column_or_1d(y, warn=True)

        indices = np.isin(y, self.classes_)

        y_transformed = np.searchsorted(self.classes_, y)
        y_transformed[~indices] = self.unknown_encoded_value
        y_transformed_temp = np.sort(y_transformed)
        return y_transformed

    def inverse_transform(self, y):
        sklearn.utils.validation.check_is_fitted(self, 'classes_')

        labels = np.arange(len(self.classes_))
        indices = np.isin(y, labels)

        y_transformed = np.asarray(self.classes_[y], dtype=object)
        y_transformed[~indices] = self.unknown_original_value
        return y_transformed

def fittransform(inputs, cols):
    for col in cols:
        X = inputs[col]
        y = sklearn.utils.validation.column_or_1d(X, warn=True)
        label_encoder = sklearn.preprocessing.LabelEncoder.fit(list(X) + ['unknown'])
        classes = label_encoder.classes_
        y = sklearn.utils.validation.column_or_1d(y, warn=True)
        indices = np.isin(y, classes)

        y_transformed = np.searchsorted(classes, y)
        y_transformed[~indices] = -1
        inputs[col] = y_transformed
    return inputs

def timeMapper(inputs, cols, result_column, time_interval_min):
    outputs = inputs
    def colmapper(x):
        return x % (3600 * 24) // (time_interval_min * 60)
    for idx, col in enumerate(cols):
        X = outputs[col]
        mapped_col = X.apply(colmapper).values
        mapped_col_name = result_column + '_' + str(idx)
        outputs[mapped_col_name] = mapped_col
    return outputs
