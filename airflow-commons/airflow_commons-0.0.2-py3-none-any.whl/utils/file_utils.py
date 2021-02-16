from codecs import open as codec_open

import yaml


def read_sql(sql_file: str, **kwargs):
    """
    Returns formatted sql with given format map

    :param sql_file: relative location of sql file
    :param kwargs:
    :return: sql query as string
    """
    with codec_open(sql_file, "r", encoding="utf8") as f:
        return f.read().format_map(kwargs)


def read_config(config_file: str):
    """
    Reads config from a configuration file and returns a config dictionary

    :param config_file: relative location of config file
    :return: configs as dictionary
    """
    stream = codec_open(config_file, "r")
    return yaml.safe_load(stream)
