from os import environ
from pydoge.utils import get_yaml_file, group_dict_keys


class Config:
    def __init__(self, config_file=None, group_values=False, limit=0):
        if config_file is not None:
            values = get_yaml_file(config_file)
            for key, value in values.items():
                self.__dict__[key] = value

        env = {}
        for key, value in environ.items():
            env[key.lower()] = value

        if limit > 0:
            keys = list(env.keys())[-limit:]
            env = {key: env[key] for key in keys}

        if group_values:
            env = group_dict_keys(env)

            for key, value in env.items():
                self.__dict__[key.lower()] = value

    def get_keys(self):
        return self.__dict__.keys()
