import inspect


def suffix_join(array: list, sep: str = '', suffix_sep: str = None):
    """Returns similarly to str.join() however allows you to specify a different final join separator

    Example:
        ', '.join(["One", "Two", "Three"])  # => 'One, Two, Three'
        suffix_join(["One", "Two", "Three"], sep=', ', suffix_sep=" or ")  # => 'One, Two or Three'
    """
    if suffix_sep is None:
        suffix_sep = sep
    if len(array) >= 2:
        return sep.join(array[:-1]) + suffix_sep + array[-1]
    return sep.join(array)


def _retrieve_name(var, offset=1):
    """Get the python variable name of the calling variable i.e. _retrieve_name(a) == 'a'"""
    caller_locals = inspect.currentframe()
    for _ in range(offset):
        caller_locals = caller_locals.f_back
    caller_locals = caller_locals.f_locals.items()
    return suffix_join([name for name, value in caller_locals if value is var], sep=', ', suffix_sep=' or ')


def pretty_print_values(*args, **kwargs):
    """Print variables and values using introspection.

    Example:
        # Instead of print(f"variable1={variable1}, variable2={variable2}, ..., variableN={variableN}")
        pretty_print_values(variable1, variable2, variableN)
    """
    names = list(map(lambda x: _retrieve_name(x, offset=3), args))
    names = {name: value for name, value in zip(names, args)}
    names.update(kwargs)
    pp_string = suffix_join([f"{name}={value}" for name, value in names.items()], sep=', ', suffix_sep=' and ')
    print(pp_string)
    return pp_string
