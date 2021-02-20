
# Deep Q Network AI [DQN_Agent]

import sys
import numpy as np
import random
from collections import deque
from keras.models import clone_model
from keras.optimizers import RMSprop
from relpath import add_import_path
add_import_path("../")
# シンプルなCNN [normal_cnn]
from normal_cnn import Normal_CNN

# 攪拌 + リサンプリングするためのインデックスのリストを生成
def gen_random_idx_ls(n, ratio):
	idx_ls = random.sample(list(range(n)), k = int(n * ratio))
	return idx_ls

# Deep Q Network AI [DQN_Agent]
class DQN_Agent:
	# 初期化処理
	def __init__(self, action_ls, ai_obs, 
				learning_interval_epi = 3, clone_interval_epi = 10,
				gamma = 0.9, buffer_size = 5000,
				eps_start = 0.5, eps_end = 0.0, eps_decay_end_epi_n = 500):
		# ゲーム側から提供される情報
		self.action_ls = action_ls	# action一覧
		self.action_idx_dict = {a:i for i, a in enumerate(action_ls)} # アクション名から通し番号を取り出す辞書
		self.ai_obs = ai_obs	# AI用の観測関数
		# 各種パラメータ
		self.learning_interval_epi = learning_interval_epi	# 学習をするまでのエピソード数
		self.clone_interval_epi = clone_interval_epi	# NNを入れ替えるまでのエピソード数
		self.eps_start = eps_start	# 開始時のランダムなactionをとる確率
		self.eps_end = eps_end	# 終了時のランダムなactionをとる確率
		self.eps_decay_end_epi_n = eps_decay_end_epi_n	# Epsilonが安定するまでのエピソード数
		self.eps = self.eps_start	# ランダムなactionをとる確率
		self.gamma = gamma	# 割引率
		self.train_data_ratio = 0.1 # Experience Replay時にlogから取り出すデータの割合
		# 学習に使うデータの格納場所
		self.playlog_ls = deque([{"now_finished": True}], maxlen = buffer_size)	# プレイ記録の格納場所
		# 内部状態
		self.nn_initialized = False	# NNが初期化されているか
		self.episode_cnt = 0	# 累積エピソード回数
		# ニューラルネットの構成
		nn_param = {
			"conv_layer_info": [
				# {"n_filter": 8, "kernel_size": (5, 5)},
				# {"n_filter": 16, "kernel_size": (5, 5)},
				# {"n_filter": 32, "kernel_size": (5, 5)},
			],
			"dense_layer_info": [
				{"unit_n": 512, "activation": "relu"},
				{"unit_n": 128, "activation": "relu"},
				{"unit_n": 32, "activation": "relu"},
				{"unit_n": 8, "activation": "relu"},
			],
			"output_activation": None
		}
		# Q関数を近似するニューラルネットの定義
		self.q_network = Normal_CNN(len(action_ls),
									nn_param,
									loss = "mse",
									optimizer = RMSprop())	# シンプルなCNN [normal_cnn]
	# 行動方策
	def policy(self, obs_img):
		# Epsilon Greedyにより、一定確率でランダムな行動を選ぶ
		if random.random() < self.eps:
			# ランダムに行動を選ぶ
			selected_a = random.choice(self.action_ls)
		else:
			# Q値が最も高いactionを選ぶ
			q_ls = self.q_network.predict(np.array([obs_img]))[0]
			best_a_idx = max([(i, q) for i, q in enumerate(q_ls)], key = lambda x: x[1])[0]
			selected_a = self.action_ls[best_a_idx]
		return selected_a
	# 行動選択、記憶、学習
	def think(self, state, reward):
		# 観測
		obs_img = self.ai_obs(state)
		# q_networkが未初期化の場合、初期化
		if self.nn_initialized is False:
			self.q_network.train_on_batch(np.array([obs_img]), np.array([[0 for _ in self.action_ls]]))
			self.target_network = clone_model(self.q_network.keras_model)
			self.nn_initialized = True
		# 行動方策による行動の選択
		selected_a = self.policy(obs_img)
		# 一つ前Stepのログの要素を参照する
		def get_prev_log(key):
			if self.playlog_ls[-1]["now_finished"] is True: return None
			return self.playlog_ls[-1][key]
		if state["finished"] is True: selected_a = "finish_action"
		# 結果の追記
		self.playlog_ls.append({
			"prev_obs": get_prev_log("now_obs"), "prev_action": get_prev_log("now_action"),
			"now_obs": obs_img,	"now_action": selected_a,
			"now_reward": reward, "now_finished": state["finished"]
		})
		# エピソード終了に伴う処理
		if state["finished"] is True: self.terminate_episode()
		return selected_a	# 選択したactionを返す
	# エピソード終了に伴う処理
	def terminate_episode(self):
		# エピソード数のインクリメント
		self.episode_cnt += 1
		# モデルの学習
		if self.episode_cnt % self.learning_interval_epi == 0:
			self.train_model()
		# ターゲットモデルの更新
		if self.episode_cnt % self.clone_interval_epi == 0:
			self.update_target_network()
		# Epsilonの更新
		self.update_eps()
	# モデルの学習
	def train_model(self):
		filtered_playlog_ls = [e for e in self.playlog_ls if e.get("prev_obs", None) is not None]
		# 学習データ(入力側)の生成
		input_ls = np.array([one_log["prev_obs"] for one_log in filtered_playlog_ls])
		# 学習データ(出力側)の生成
		esitimated_ls = self.target_network.predict(input_ls)	# 学習の安定のため、重みを固定したNNによってQ値を計算
		output_ls = np.array(esitimated_ls)
		for log_idx, one_log in enumerate(filtered_playlog_ls):
			# エピソード終了の1つ前のstateのみ遷移先基準のQ値が計算できないため、条件分岐
			if one_log["now_finished"] is True:
				gain = one_log["now_reward"]
			else:
				next_s_max_q = max(esitimated_ls[log_idx + 1])
				gain = one_log["now_reward"] + self.gamma * next_s_max_q
			# 実際に取った行動のQ値のみ更新
			action_idx = self.action_idx_dict[one_log["prev_action"]]	# アクション名から通し番号を取り出す辞書
			output_ls[log_idx][action_idx] = gain
		# 攪拌 + リサンプリングして学習
		idx_ls = gen_random_idx_ls(n = len(input_ls), ratio = self.train_data_ratio)	# 攪拌 + リサンプリングするためのインデックスのリストを生成
		loss = self.q_network.train_on_batch(input_ls[idx_ls], output_ls[idx_ls])
		# print("loss: %.4f"%loss)
	# ターゲットモデルの更新
	def update_target_network(self):
		self.target_network.set_weights(self.q_network.keras_model.get_weights())
		# print("teacher model is updated.")
	# Epsilonの更新
	def update_eps(self):
		eps_s, eps_e = self.eps_start, self.eps_end
		eps_cnt = self.episode_cnt
		decay_end_epi_n = self.eps_decay_end_epi_n
		if self.episode_cnt >= decay_end_epi_n:
			self.eps = eps_e
		else:
			self.eps = eps_s - eps_cnt * (eps_s - eps_e) / decay_end_epi_n
		# print("Epsilon: %.2f"%self.eps)