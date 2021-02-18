import random


def generate_param_state(param_base, gaconf):
    new_param = {**param_base, 'foo': random.randint(0, 10)}
    return new_param
