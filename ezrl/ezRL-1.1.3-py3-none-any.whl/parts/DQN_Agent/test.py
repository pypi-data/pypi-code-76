
# Deep Q Network AI

import sys
import matplotlib.pyplot as plt
from relpath import add_import_path
add_import_path("../")
# Catcherゲーム [catcher_game]
from catcher_game import game_step, action_ls, human_obs, ai_obs, gen_init_state
# Deep Q Network AI [DQN_Agent]
from DQN_Agent import DQN_Agent

# 【動作確認・使用例】
if __name__ == "__main__":
	train_ai = DQN_Agent(action_ls = action_ls, ai_obs = ai_obs) # Deep Q Network AI
	episode_n = 700	# エピソード数
	total_reward_ls = []
	for episode_idx in range(episode_n):
		# state, actionの初期化
		action, state = "initial_action", gen_init_state(game_params = {})
		reward_ls = []
		# ゲーム進行
		while state["finished"] is False:
			state, reward = game_step(state, action)
			action = train_ai.think(state, reward) # 行動決定
			reward_ls.append(reward)
		total_reward_ls.append(sum(reward_ls))
		print("Episode #%d, Reward: %.1f"%(episode_idx, total_reward_ls[-1]))
	# 獲得報酬の推移を表示
	plt.plot(total_reward_ls)
	plt.show()
	# state, actionの初期化
	action, state = "initial_action", gen_init_state(game_params = {})
	# テストプレイ
	while state["finished"] is False:
		human_obs(state, waitKey_msec = 100) # 人間用の観測関数
		state, reward = game_step(state, action)
		action = train_ai.think(state, reward)
