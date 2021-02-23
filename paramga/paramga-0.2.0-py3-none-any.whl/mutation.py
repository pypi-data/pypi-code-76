import random
from .random_helpers import set_seed


def mutate_param_state(param, gaconf):
    param_copy = {**param}
    for k, var in gaconf.items():
        assert var['type'] == 'number'
        r = random.randint(-var['step'], var['step'])
        if r == 0:
            continue
        param_copy[k] = param[k] + r
    return param_copy
