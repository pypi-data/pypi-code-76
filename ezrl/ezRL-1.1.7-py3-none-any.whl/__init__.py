
import sys
import cv2
import random
import numpy as np
from sout import sout
# 共通部品 [utils.py]
from .parts.utils import show_img
# Deep Q Network AI [DQN_Agent]
from .parts.DQN_Agent import DQN_Agent
# Catcherゲーム [catcher_game]
from .parts import catcher_game

# ランダムAI
class RandomPlayer:
	# 初期化処理
	def __init__(self, action_ls):
		self.action_ls = action_ls
	# テスト用プレーヤーを生成
	def gen_test(self):
		test_ai = self
		return test_ai
	# アクションを考える
	def think(self, state, reward):
		action = random.choice(self.action_ls)
		return action

# # debug用人間プレーヤー
# class HumanPlayer:
# 	# 初期化処理
# 	def __init__(self, action_dic):
# 		self.action_dic = action_dic
# 	# アクションを考える
# 	def think(self, obs_img):
# 		cv2.imshow("obs_img", obs_img)
# 		cv2.waitKey(1)
# 		while True:
# 			print("action: %s"%(", ".join(list(self.action_dic))))
# 			action = input("action>").strip()
# 			if action in self.action_dic: return self.action_dic[action]
# 	# 報酬をAIにフィードバック
# 	def report_reward(self, reward):
# 		print("報酬を%.2fもらえました"%reward)

# # テスト用ゲーム (紅白ゲーム)
# class RW_Game:
# 	# 初期化処理
# 	def __init__(self, round_n):
# 		self.round_n = round_n
# 		self.q_idx = 0	# 何問目か
# 		# 次の正解を作る
# 		self.renew_ans()
# 	# 現在のプレーヤーを返す
# 	def now_player(self):
# 		return 0	# 1人用ゲームなので手番は変化しない
# 	# 観測
# 	def observe(self, p_id = None):
# 		# 終了している場合はobserveできない
# 		if self.finished() is True: raise Exception("[error] 既にゲームが終了しています。")
# 		# p_id指定なし(現在の手番)の場合は、p_id==0とする(1人用ゲームなので)
# 		if p_id is None: p_id = 0
# 		# 画像を作る
# 		obs_img = np.zeros((200,200,3), dtype = np.uint8)
# 		obs_img[:,:,:] = 220	# 全て白で塗る
# 		if self.true_ans == 0:
# 			obs_img[:,:,:-1] = 30
# 		return obs_img
# 	# アクションの実行
# 	def action(self, action):
# 		# 終了している場合はactionできない
# 		if self.finished() is True: raise Exception("[error] 既にゲームが終了しています。")
# 		# actionの型の判定
# 		if len(action) != 2: raise Exception("[error] actionの型が不正です")
# 		# action配列のデコード
# 		r_value, w_value = action
# 		rw_action = int(w_value > r_value)
# 		# rewardの設定
# 		reward = int(self.true_ans == rw_action)
# 		# 出題数をインクリメント
# 		self.q_idx += 1
# 		# 次の正解を作る
# 		self.renew_ans()
# 		return reward
# 	# 次の正解を作る
# 	def renew_ans(self):
# 		self.true_ans = int(random.random()*2)
# 	# 終了判定
# 	def finished(self):
# 		if self.q_idx >= self.round_n: return True
# 		return False

# # 対戦フィールド (arena)
# def arena(game, player_ls, show_flag = True):
# 	if show_flag is True: print("arena: 対戦開始")
# 	while True:
# 		# 今のプレーヤー
# 		p_id = game.now_player()
# 		# 観測
# 		obs_img = game.observe()
# 		# アクションを考える
# 		action = player_ls[p_id].think(obs_img)
# 		# アクションの実行
# 		reward = game.action(action)
# 		# 報酬をAIにフィードバック
# 		player_ls[p_id].report_reward(reward)
# 		# 終了判定
# 		if game.finished() is True: break
# 	if show_flag is True: print("arena: 対戦終了")

# # 対戦フィールド (arena)
# def arena(game, player_ls):
# 	while True:
# 		# 今のプレーヤー
# 		p_id = game.now_player()
# 		print("───────")
# 		# AIによる観測
# 		print("\n<<action前状態>>")
# 		obs_text, obs_img = game.observe(p_id)
# 		print(obs_text)
# 		action = players[p_id].think(obs_img)
# 		# アクション
# 		game.action(action)
# 		# 終了判定
# 		if game.finished() is True: break
# 		# AIによる観測
# 		print("\n<<action後状態>>")
# 		obs_text, obs_img = game.observe(p_id)
# 		print(obs_text)
# 		# 状態の観測値の表示
# 		obs_img = cv2.resize(obs_img, None, fx = 10, fy = 10, interpolation = cv2.INTER_NEAREST)
# 		cv2.imshow("observation_image", obs_img)
# 		cv2.waitKey(0)
# 		cv2.destroyAllWindows()
