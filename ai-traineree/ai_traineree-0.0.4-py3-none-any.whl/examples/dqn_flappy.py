import gym
import gym_pygame  # Import registers

from ai_traineree.agents.rainbow import RainbowAgent as Agent
from ai_traineree.env_runner import EnvRunner
from ai_traineree.loggers import TensorboardLogger
from ai_traineree.tasks import GymTask


env_name = 'Pixelcopter-PLE-v0'  # action=1 to start
# env_name = "FlappyBird-PLE-v0"  # Likely doesn't work because of assets
# env_name = "Pong-PLE-v0"  # action=2 to start
env = gym.make(env_name)
task = GymTask(env, seed=0)
task.hooks['post_reset_hook'] = lambda self: self.env.step(1)
data_logger = TensorboardLogger()

config = {
    'update_freq': 5,
}
agent = Agent(task.state_size, task.action_size, **config)
env_runner = EnvRunner(task, agent, data_logger=data_logger)

print('Action space:', env.action_space)
print('Obsevation space:', env.observation_space)
print('Obsevation space high:', env.observation_space.high)
print('Obsevation space low:', env.observation_space.low)

scores = env_runner.run(reward_goal=10, max_episodes=1000, eps_decay=0.99, force_new=True)
env_runner.interact_episode(render=True)
