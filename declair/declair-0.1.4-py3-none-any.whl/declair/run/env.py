from ..exception import EnvironmentException, InvalidConfigException

from .insertion import make_insert_func_recursive

from .special_entries import ENV_KEY

# TODO: Document default
@make_insert_func_recursive(ENV_KEY)
def insert_env(obj, env):
    """
    Inserts environment variables into a nested run configuration 
    dictionary and returns the resultant dictionary. That is, replaces
    dictionaries of form 
        {"__env__": ("some", "multipart", "key")}
    with 
        env["some"]["multipart"]["key"]
    for arbitrary number of elements in the list key.
    """
    try:
        key = obj[ENV_KEY]
        if isinstance(key, str):
            try:
                return env[key]
            except KeyError:
                if 'default' in obj:
                    return obj['default']
                else:
                    raise
        elif isinstance(key, list) or isinstance(key, tuple):
            try:
                return env.get_nested_key(key)
            except KeyError:
                if 'default' in obj:
                    return obj['default']
                else:
                    raise
        else:
            raise InvalidConfigException("__env__ entry key must be either a string or a list or a tuple, but is {}".format(type(key)))
    except Exception as e:
        raise EnvironmentException("Failed to load entry from environment: {}".format(
            obj)) from e
