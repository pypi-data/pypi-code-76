import os
import random
from os import path

import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from ml_platform_client.algorithm_base import AlgorithmBase, PredictorBase
from ml_platform_client.minio_accessor import MinIOAccessor
from ml_platform_client.config import global_config
# from minio_accessor import MinIOAccessor
# from algorithm.algorithm_base import AlgorithmBase
# from algorithm.algorithm_base import PredictorBase


class MyAlgorithm(AlgorithmBase):
    train_status_map = {}

    def train(self, model_id: str, model_path: str, data_config: dict, parameters: dict, extend: dict):
        # 拉取训练数据
        location = data_config['location']
        filename = 'temp'
        MinIOAccessor.fget_object(location, filename)

        # 数据处理
        df = pd.read_csv(filename)
        X = df[['weight', 'height']]
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(df['gender'])

        # 模型定义
        lr = LogisticRegression()

        # 模型训练
        lr.fit(X, y)

        # 保存到磁盘
        local_model_path = model_id
        joblib.dump(lr, local_model_path)

        # 上传minio
        MinIOAccessor.save_object(local_model_path, path.join(model_path, local_model_path))

        os.remove(filename)
        os.remove(local_model_path)

    def load(self, model_id: str, model_path: str) -> PredictorBase:
        print(global_config.minio_host)
        # 从minio拉取模型文件
        full_path = path.join(model_path, model_id)
        temp_model = 'temp_model'
        MinIOAccessor.fget_object(full_path, 'temp_model')

        # 加载到内存
        lr = joblib.load(temp_model)
        os.remove(temp_model)

        # 返回predictor对象
        predictor = MyPredictor(lr)
        return predictor

    def status(self, model_id):
        return 'completed'


class MyPredictor(PredictorBase):

    def predict(self, features: dict):
        weight = features['weight']
        height = features['height']
        result = self.model.predict([[weight, height]]).tolist()[0]
        label = None
        if result == 1:
            label = '男'
        if result == 0:
            label = '女'
        return [{'label': label, 'score': 100}]


class FakeAlgorithm(AlgorithmBase):
    train_map = {}

    def train(self, model_id: str, model_path: str, data_config: dict, parameters: dict, extend: dict):
        # 拉取训练数据
        pass

    def load(self, model_id: str, model_path: str) -> PredictorBase:
        # 从minio拉取模型文件
        # 返回predictor对象
        predictor = FakePredictor(None)
        return predictor

    def status(self, model_id):
        return 'completed'


class FakePredictor(PredictorBase):

    def predict(self, features: dict, uuid: str):
        return [{'label': random.randint(0, 10), 'score': 100}]
