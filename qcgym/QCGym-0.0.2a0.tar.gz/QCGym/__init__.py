from gym.envs.registration import register

register(
    id='cross-res-env',
    entry_point='QCGym.environments:GenericEnv',
)
