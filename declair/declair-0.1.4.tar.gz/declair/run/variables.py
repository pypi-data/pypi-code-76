from ..exception import InvalidConfigException
from .special_entries import VAR_KEY, VAR_INSTANCE_KEY
from .insertion import make_insert_func_recursive

def _generic_insert_var(obj, variable, key):
    if obj[key] not in variable:
        raise InvalidConfigException(
            "Variable '{}' used but not defined".format(obj[key]))
    return variable[obj[key]]

# Distinction between the two functions below shows up in
# declair.run.execute._config_to_execute, where their order is crucial

@make_insert_func_recursive(VAR_KEY)
def insert_var(obj, variable):
    return _generic_insert_var(obj, variable, VAR_KEY)

@make_insert_func_recursive(VAR_INSTANCE_KEY)
def insert_var_instance(obj, variable):
    return _generic_insert_var(obj, variable, VAR_INSTANCE_KEY)
