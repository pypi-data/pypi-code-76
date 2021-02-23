"""
Functions responsible for executing experiments from configurations.
"""

from datetime import datetime
from pathlib import Path

from .const import (DEF_KEY_ENV_PARAMS, DEF_KEY_EXECUTE_TIME, DEF_KEY_TYPE,
                    DEF_TYPE_RUN, DEF_TYPE_SEARCH, DEF_TYPE_EXTEND,
                    DEF_KEY_EXPERIMENT_NAME)
from .env import Environment, get_path_env
from .serialization import load_file
from .exception import InvalidConfigException
from .run.execute import execute_run
from .search.execute import execute_search
from .extend.execute import execute_extend

def get_execute_type(dict_):
    return dict_.get(DEF_KEY_TYPE)

def _attach_timestamp(dict_):
    dict_[DEF_KEY_EXECUTE_TIME] = datetime.utcnow().isoformat()

def execute_definition(dict_, env, filepath=None):
    _attach_timestamp(dict_)
    type_ = get_execute_type(dict_)
    if type_ == DEF_TYPE_RUN:
        return execute_run(dict_, env)
    elif type_ == DEF_TYPE_SEARCH:
        return execute_search(dict_, env)
    elif type_ == DEF_TYPE_EXTEND:
        # extend relies on relative paths, so a path must be provided if extend
        # type is to be used
        if filepath is None:
            raise ValueError("filepath cannot be None if 'type' is 'extend'")
        return execute_extend(dict_, env, execute_definition, filepath)
    else:
        raise InvalidConfigException(
            "Experiment definition has no valid 'type' entry.")

def execute_file(filepath, env=None):
    dict_ = load_file(filepath)
    # If the name is not defined, we want to insert the name of the file being
    # executed
    if DEF_KEY_EXPERIMENT_NAME not in dict_:
        dict_[DEF_KEY_EXPERIMENT_NAME] = Path(filepath).name
    if env is None and DEF_KEY_ENV_PARAMS not in dict_:
        env = get_path_env(filepath)
    elif DEF_KEY_ENV_PARAMS in dict_:
        env = Environment.from_dict(dict_[DEF_KEY_ENV_PARAMS])
    try:
        return execute_definition(dict_, env, filepath=filepath)
    except InvalidConfigException:
        raise InvalidConfigException(
            "Error in experiment definition: {}".format(filepath))
