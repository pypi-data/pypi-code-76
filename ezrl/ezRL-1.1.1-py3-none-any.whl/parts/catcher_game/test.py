
import sys
import random
from sout import sout
from relpath import add_import_path
add_import_path("../")
# Catcherゲーム [catcher_game]
from catcher_game import game_step, action_ls, human_obs, gen_init_state

# ランダム選択AI
class RandomPlayer:
	# 初期化処理
	def __init__(self, all_action_ls,
		game_func = None, ai_obs = None):
		self.all_action_ls = all_action_ls
	# 行動決定
	def think(self, state = None, reward = None):
		action = random.choice(self.all_action_ls)
		return action

# 動作確認・使用例
if __name__ == "__main__":
	# 全てのアクション
	ai = RandomPlayer(action_ls, game_func = None, ai_obs = None) # ランダム選択AI
	# state, actionの初期化
	action = "initial_action"
	state = gen_init_state(game_params = {})
	# ゲーム進行
	while state["finished"] is False:
		state, reward = game_step(state, action)
		action = ai.think(state, reward) # 行動決定
		# 人間用の観測関数 [catcher_game]
		human_obs(state, waitKey_msec = 200)