from os import environ

from modular_message_bot.config.config_collection import DictConfigProvider


def build_env_config(priority: int) -> DictConfigProvider:
    environ_map = {}
    for key, value in environ.items():
        environ_map[key] = value
    return DictConfigProvider(environ_map, "ENV config dict provider", priority)
