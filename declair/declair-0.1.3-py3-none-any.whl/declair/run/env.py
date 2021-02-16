from ..exception import EnvironmentException

from .insertion import make_insert_func_recursive

from .special_entries import ENV_KEY

def _get_nested_dict(key, dict_, default=None, default_given=False):
    try:
        if not isinstance(key, list) and not isinstance(key, tuple):
            raise EnvironmentException("Environment key '{}' must be a list or tuple but is string".format(key, type(key).__name__))
        if len(key) > 1:
            return _get_nested_dict(key[1:], dict_.get(key[0], {}), 
                                    default=default, default_given=default_given)
        else:
            if default_given:
                return dict_.get(key[0], default)
            else:
                return dict_[key[0]]
    except (KeyError, IndexError, AttributeError, TypeError):
        raise EnvironmentException(
            "Unable to get key {} from {}".format(
                key[0], dict_))

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
        if 'default' in obj:
            return _get_nested_dict(obj[ENV_KEY], env, 
                                    default=obj['default'], default_given=True)
        else:
            return _get_nested_dict(obj[ENV_KEY], env)
    except EnvironmentException:
        raise EnvironmentException("Failed to load entry from environment: {}".format(
            obj))
