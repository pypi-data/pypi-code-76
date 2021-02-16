import sys
import inspect

# Until poetry fixes this https://github.com/python-poetry/poetry/issues/144
# This hack is necessary to report correct __version__
# inside the project
# Version printing part 0
from pathlib import Path
import configparser


def asdict(obj):
    """Helper to create a dictionary out of the class attributes (fields/variables)"""
    obj_dict = obj.__class__.__dict__
    return {k: getattr(obj, k) for k, v in obj_dict.items()
            if not k.startswith('_')
            and not inspect.isfunction(v)
            and not inspect.ismethod(v)}


def schema_decorator(decorators_state, cls):
    """Adds cls to decorator_state"""
    decorators_state['schema'] = cls()
    return cls


def get_pkg_version():
    # Version printing part 1
    # Enables version printing out of the box
    # Idea is, that when poetry is used, this will look up the version
    # in its configuration.
    version = '0.0.1'
    toml = Path('pyproject.toml')
    if toml.exists():
        parser = configparser.ConfigParser()
        parser.read(toml)

        tool_section = parser['tool.poetry']
        if 'version' in tool_section:
            quoted = tool_section['version']
            version = quoted.replace('"', '')

    return version


def is_iterable(value):
    # v_is_iterable = False
    iterables = [tuple, list, set]
    # try:
    #     if type(value) is type:
    #         v_is_iterable = iter(value()) is not None
    #     else:
    #         v_is_iterable = iter(value) is not None
    # except TypeError:
    #     pass

    return (type(value) in iterables or value in iterables)
    # return v_is_iterable


def should_wrap_as_list(value, target_type):
    """Helper for casting. Casting a str in list will split it..."""
    res = False
    if not is_iterable(value) and is_iterable(target_type):
        res = True
    elif isinstance(value, str) and (target_type is not str and is_iterable(target_type)):
        res = True

    return res

class MetaSchema(type):
    """
    Validate, cast types, wrap configuration and invoke 'post_hook' method for
    the Schema class
    """

    def __new__(mcs, name, bases, namespace, **kwds):
        cls = type.__new__(mcs, name, bases, namespace)

        # post init hook
        cls.post_init(cls)

        # Parsing type descriptors
        if '__annotations__' in namespace:
            for attr, t in namespace['__annotations__'].items():
                # Validation
                try:
                    value = namespace[attr]
                    schema_value = getattr(cls, attr)

                    # TODO: Nested types. This only wraps a single iterable

                    if should_wrap_as_list(value, t):
                        value = [value]

                    if should_wrap_as_list(schema_value, t):
                        schema_value = [schema_value]

                    # Type casting
                    if t(value) == t(schema_value):
                        if getattr(cls, attr) is not None:
                            setattr(cls, attr, t(value))
                    else:
                        setattr(cls, attr, t(schema_value))
                except TypeError as ex:
                    print('given parameters or defined defaults were of incorrect type:')
                    # print(f'{cls.__qualname__}.{ann} -> {ex.args}')  # f-strings require >=3.6
                    print('{}.{} -> {}'.format(cls.__qualname__, attr, ex.args))
                    sys.exit(1)

        setattr(cls, 'version', get_pkg_version())

        # TODO: Maybe check that given parameters matched the schema?
        # Even a fuzzy search to suggest close matches

        # Wrap schema with c (configuration decorator
        cls._wrap(cls)

        return cls

    def __init__(cls, name, bases, namespace, **kwds):
        super().__init__(name, bases, namespace)
