from gym.envs.registration import register

register(
    id='cross-res-env-v0',
    entry_point='QCGym.environments:GenericEnv',
)
