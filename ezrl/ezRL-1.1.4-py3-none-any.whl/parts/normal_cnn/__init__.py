
# シンプルなCNN [normal_cnn]

import sys
import numpy as np
from keras import layers
from keras.models import Model

# 標準的な畳み込み層
def normal_conv_layer(x, n_filter, kernel_size):
	x = layers.Conv2D(n_filter, kernel_size, padding = "same")(x)
	x = layers.BatchNormalization()(x)
	x = layers.Activation("relu")(x)
	return x

# skip-connection有りの畳み込み層
def residual_layer(x, n_filter, kernel_size):
	prev_x = x # skip_connection用に退避
	x = layers.Conv2D(n_filter, kernel_size, padding = "same")(x)
	x = layers.BatchNormalization()(x)
	x = layers.Activation("relu")(x)
	x = layers.Conv2D(n_filter, kernel_size, padding = "same")(x)
	x = layers.BatchNormalization()(x)
	x = layers.add([x, prev_x])	# 合流部
	x = layers.Activation("relu")(x)
	return x

# 全結合層
def dense_layer(x, unit_n, activation = None):
	x = layers.Dense(unit_n, activation = activation)(x)
	return x

# シンプルなCNN [normal_cnn]
class Normal_CNN():
	# 初期化処理
	def __init__(self, n_out, nn_param, loss = "mse", optimizer = "sgd"):
		self.keras_model = None
		self.n_out = n_out
		self.nn_param = nn_param
		self.loss = loss
		self.optimizer = optimizer
	# 学習
	def fit(self, input_ls, output_ls, epochs = 10):
		if self.keras_model is None:
			image_shape = input_ls[0].shape
			# keras-cnnの初期化
			ret_nn = self.instantiate_nn(input_shape = image_shape)
			self.keras_model = ret_nn
		self.keras_model.fit(input_ls, output_ls, epochs = epochs)
	# サンプル中の1つのバッチで勾配を更新
	def train_on_batch(self, input_ls, output_ls):
		if self.keras_model is None:
			image_shape = input_ls[0].shape
			# keras-cnnの初期化
			ret_nn = self.instantiate_nn(input_shape = image_shape)
			self.keras_model = ret_nn
		loss_value = self.keras_model.train_on_batch(input_ls, output_ls)
		return loss_value
	# 予測
	def predict(self, input_ls):
		pred_ls = self.keras_model.predict(input_ls)
		return pred_ls
	# keras-cnnの初期化
	def instantiate_nn(self, input_shape):
		# 入力層の定義
		inputs = layers.Input(shape = input_shape)
		# 畳み込み層の定義
		feature = inputs
		for one_info in self.nn_param["conv_layer_info"]:
			n_filter = one_info["n_filter"]
			kernel_size = one_info["kernel_size"]
			feature = normal_conv_layer(feature, n_filter, kernel_size)	# skip-connection有りの畳み込み層
		# Flatten
		feature = layers.Flatten()(feature)
		# 全結合層、出力層の定義
		for one_info in self.nn_param["dense_layer_info"]:
			unit_n = one_info["unit_n"]
			activation = one_info["activation"]
			feature = dense_layer(feature, unit_n = unit_n, activation = activation)	# 全結合層
		output_activation = self.nn_param["output_activation"]
		outputs = dense_layer(feature, unit_n = self.n_out, activation = output_activation)	# 出力層
		# 層をまとめる
		model = Model(inputs = inputs, outputs = outputs)
		model.compile(loss = self.loss, optimizer = self.optimizer)
		return model