"""Some utility functions module."""


def camel_to_snake(s):
    """ converts CamelCase string to camel_case\
        taken from https://stackoverflow.com/a/44969381

        :param s: some string
        :type s: str:

        :return: a camel_case string
        :rtype: str:
    """
    no_camel = ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')
    return no_camel.replace('__', '_')


def create_query_sting(param_dict):
    """ turns a dict into a query string
    :param param_dict: a dictionary
    :type param_dict: dict

    :return: a clean query string
    :rtype: str
    """
    params = "&".join(
        [
            f"{key}={value}" for key, value in param_dict.items()
        ]
    )
    return params.replace('#', '%23')
