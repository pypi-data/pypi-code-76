import gym
import numpy as np
from gym import spaces

from gym_cabworld.envs.game import Game
from gym_cabworld.envs.game_multi_agent import MultiAgentGame


class CustomEnv(gym.Env):
    def __init__(self, mode):
        """
        Create OpenAiGym with Pygame
        """
        self.mode = mode
        self.pygame = Game(self.mode)
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(
            np.array([[-1] * 14]), np.array([[1] * 14]), dtype=np.int
        )

    def reset(self):
        """
        Reset Game
        """
        del self.pygame
        self.pygame = Game(self.mode)
        obs = self.pygame.observe()
        return obs

    def step(self, actions):
        """
        Execute one step in environment
        """
        self.pygame.action(actions)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        """
        Render PyGame
        """
        self.pygame.view()


class MarlEnv(CustomEnv):
    def __init__(self, game_mode):
        """
        Multi Agent with 2 random cabs and 3 random passengers
        """
        self.pygame = MultiAgentGame(game_mode)
        number_cabs = self.pygame.number_cabs
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(
            np.array([[-1] * 14] * number_cabs),
            np.array([[1] * 14] * number_cabs),
            dtype=np.int,
        )
        self.game_mode = game_mode

    def reset(self):
        del self.pygame
        self.pygame = MultiAgentGame(self.game_mode)
        obs = self.pygame.observe()
        return obs


class CustomEnv0(CustomEnv):
    def __init__(self):
        super().__init__(0)


class CustomEnv1(MarlEnv):
    def __init__(self):
        super().__init__(1)


class CustomEnv2(CustomEnv):
    def __init__(self):
        super().__init__(2)


class CustomEnv3(MarlEnv):
    def __init__(self):
        super().__init__(3)
