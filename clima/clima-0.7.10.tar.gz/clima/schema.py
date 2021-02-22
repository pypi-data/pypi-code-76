import sys
import inspect

# Until poetry fixes this https://github.com/python-poetry/poetry/issues/144
# This hack is necessary to report correct __version__
# inside the project
# Version printing part 0
from pathlib import Path
import configparser
from importlib import metadata


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


def get_importing_frame():
    piece = inspect.stack()[0]
    for frame in inspect.getouterframes(piece.frame):
        code_context = frame.code_context
        if isinstance(code_context, list):
            code = code_context[0]
            if 'clima' in code and 'import' in code and 'core' not in code:
                return frame


def deduce_importer_version():
    """experimental way of deducing the version from the package that
    imports clima
    """
    from importlib import util
    version = None
    try:
        frame = get_importing_frame()
        p = Path(frame.filename)
        parent = str(p.parent.name)
        importer_package = None
        while importer_package is None:
            spec = util.find_spec(parent)
            if hasattr(spec, 'name'):
                importer_package = spec.name
        version = metadata.version(importer_package)
    except:
        pass

    return version


def parse_version_from_pyproject_toml():
    toml = Path('pyproject.toml')
    version = None
    if toml.exists():
        parser = configparser.ConfigParser()
        parser.read(toml)

        tool_section = parser['tool.poetry']
        if 'version' in tool_section:
            quoted = tool_section['version']
            version = quoted.replace('"', '')
    return version


def get_pkg_version():
    # Version printing part 1
    # Enables version printing out of the box
    # Idea is, that when poetry is used, this will look up the version
    # in its configuration.

    if (version := deduce_importer_version()) is not None:
        pass
    elif (version := parse_version_from_pyproject_toml()) is not None:
        pass
    else:
        version = '0.0.1'

    return version


def is_iterable(value):
    iterables = [tuple, list, set]

    return (type(value) in iterables or value in iterables)


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
