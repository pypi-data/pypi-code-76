from ..exception import InvalidConfigException
from .const import SEARCH_TYPE_GRID, SEARCH_TYPE_HYPEROPT
from ..const import DEF_KEY_SEARCH_MODE, DEF_KEY_EXPERIMENT_NAME
from .grid import execute_gridsearch
from .hyperopt import execute_hyperopt_search

def execute_search(config, env):
    if DEF_KEY_EXPERIMENT_NAME not in config:
        raise InvalidConfigException("'experiment_name' field missing and could not be obtained from experiment filename")
    if config[DEF_KEY_SEARCH_MODE] == SEARCH_TYPE_GRID:
        execute_gridsearch(config, env)
    elif config[DEF_KEY_SEARCH_MODE] ==SEARCH_TYPE_HYPEROPT:
        execute_hyperopt_search(config, env)
    else:
        raise NotImplementedError("Search of type {} is not implemented".format(config[DEF_KEY_SEARCH_MODE]))
