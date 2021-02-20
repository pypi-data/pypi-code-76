
# シンプルなCNN [normal_cnn]

import sys
import numpy as np
from relpath import add_import_path
from sklearn import datasets, model_selection, metrics
add_import_path("../")
# シンプルなCNN [normal_cnn]
from normal_cnn import Normal_CNN

# 【動作確認・使用例】
if __name__ == '__main__':
	# CNNの構成の設定
	nn_param = {
		"conv_layer_info": [
			{"n_filter": 8, "kernel_size": (5, 5)},
			{"n_filter": 8, "kernel_size": (5, 5)},
			{"n_filter": 8, "kernel_size": (5, 5)},
		],
		"dense_layer_info": [
			{"unit_n": 8, "activation": "relu"},
		],
		"output_activation": "softmax",
	}
	# 出力層のユニット数
	n_class = 10
	# モデルの定義
	cnn = Normal_CNN(n_class, nn_param, loss = "categorical_crossentropy")	# シンプルなCNN [normal_cnn]

	# 軽量数字データセット
	digits = datasets.load_digits()
	img_shape = (8, 8, 1)
	y = digits["target"]
	X = np.array([flat_img.reshape(img_shape) for flat_img in digits["data"]])
	# 学習データ、テストデータの分離
	splited = model_selection.train_test_split(
											X, 
											y, 
											test_size = 0.33)
	X_train, X_test, y_train, y_test = splited
	# モデルの学習・予測
	from keras.utils.np_utils import to_categorical
	categ_train = to_categorical(y_train, num_classes = n_class)	# one-hot encoding
	cnn.fit(X_train, categ_train)	# 学習
	categorical_pred = cnn.predict(X_test)	# 予測
	y_pred = [np.argmax(one_pred) for one_pred in categorical_pred]
	# 予測結果の表示
	accuracy = metrics.accuracy_score(y_test, y_pred)
	cof_mat = metrics.confusion_matrix(y_test, y_pred)
	print("Accuracy: %.2f"%accuracy)
	print("Confusion matrix:")
	print(cof_mat)
