from collections import ChainMap
import inspect
import sys
import os
from functools import partial
from typing import Dict

from clima.fire import Fire

from clima import schema, utils, password_store, env
from clima import docstring, configfile
from pathlib import Path


class RequiredParameterException(Exception):
    pass


DECORATORS_STATE = {
    'schema': None,
    'generated': None,
}

schema_decorator = partial(schema.schema_decorator, DECORATORS_STATE)


class Configurable:
    """Configuration management"""
    # TODO: idiomatic handling for use cases that apply to NamedTuple
    __configured = None

    def _get_configured(self):
        return self.__configured

    def _set_configured(self, dct: dict):
        self.__configured = dct

    def _chain_configurations(self, params: dict, _schema):
        """Chains all configuration options together"""
        cm = ChainMap(
            params,
            utils.filter_fields(os.environ, _schema),
            env.get_env(_schema),
            _schema._get_configfile_asdict(),
            password_store.get_secrets(_schema),
            _schema._asdict()
        )

        # self.__configured = dict(cm)
        return dict(cm)

    def _init(self, _schema: schema.MetaSchema):
        is_schema = isinstance(_schema, schema.MetaSchema)
        if not is_schema:
            raise TypeError('The configuration should inherit Schema')

        # Allows using Schema as a subclass only
        c.__configured = _schema

        # Allows deoorator usage with @c.init
        return schema_decorator(_schema)

    def __call__(self, cls, *, noprepare=False):
        """
        Decorator to define the Cli object
        """
        _cli = cli(cls)
        if not noprepare:
            global DECORATORS_STATE
            prepare(DECORATORS_STATE['generated'], DECORATORS_STATE['schema'])

        return _cli

    def __repr__(self):
        return repr(self.__configured)

    def __getattr__(self, item):
        res = None
        if self.__configured is not None:
            try:
                res = self.__configured[item]
            except Exception:
                res = getattr(self.__configured, item)

        if res is None:
            raise RequiredParameterException(f'Missing argument for "{item}"')
        return res

    def __getitem__(self, item):
        c_item = self.__configured[item]
        if c_item is None:
            print('none')
        return c_item

    def _clear(self):
        """Testing requires clearing global state"""

        c.__configured = None

        global DECORATORS_STATE
        DECORATORS_STATE = {
            'schema': None,
            'generated': None,
        }


c = Configurable()


def add_to_decorators(key, value):
    DECORATORS_STATE[key] = value


def cast_as_annotated(_schema, attr, container=None, value=None):
    """Schema is annotated with types. These types are used to
    recast the value (value == container[attr] if not specified in kwargs)
    in container (container == _schema if not specified in kwargs)
    """
    if container is None:
        container = _schema

    if value is None:
        value = getattr(container, attr)
    result = value

    if hasattr(type(_schema), '__annotations__'):
        annotated_type = type(_schema).__annotations__.get(attr)
        if annotated_type is not None:

            # TODO: Nested types. Here we'll wrap a string or uniterable into an iterable
            # To prevent surprises such as 'VST' -> ('V', 'S', 'T') when expecting ('VST')
            if schema.should_wrap_as_list(value, annotated_type):
                result = annotated_type([value])
            else:
                result = annotated_type(value)
    return result


def cli(cls):
    """Decorator that wraps the command line interface specific class with fire"""
    state = DECORATORS_STATE

    CliClass = cls

    def init(self, **cli_args):
        """Generated init"""
        s = state['schema']

        # Cast everything according to schema before Cli.post_init
        for attr, cli_arg_value in cli_args.items():
            if hasattr(s, attr):
                setattr(s, attr, cast_as_annotated(s, attr, value=cli_arg_value))
            s: type(s) = s

        if hasattr(s, 'cwd'):
            p: Path = getattr(s, 'cwd')
            if not p.is_absolute():
                setattr(s, 'cwd', Path.cwd() / p)

        # if hasattr(CliClass, 'post_init'):
        #     CliClass.post_init(s)

        # # TODO: consider if really necessary
        # for attr, annotated in cli_args.items():
        #     if hasattr(s, attr):
        #         cli_args[attr] = cast_as_annotated(s, attr)

        global c
        cm = c._chain_configurations(cli_args, s)
        # initialize_cli(cli_args, s)

        tmp_c = Configurable()
        tmp_c._set_configured(cm)
        # TODO: consider if really necessary
        for attr in s._asdict():
            if attr in cm:
                setattr(tmp_c, attr, cast_as_annotated(s, attr, container=tmp_c))

        if hasattr(CliClass, 'post_init'):
            CliClass.post_init(tmp_c)

            # TODO: consider if really necessary
            for attr in s._asdict():
                if hasattr(tmp_c, attr):
                    setattr(tmp_c, attr, cast_as_annotated(s, attr, container=tmp_c))

        for attr in tmp_c._get_configured():
            setattr(c, attr, getattr(tmp_c, attr))
            # c._set_configured(tmp_c._get_configured())

    cls_attrs = dict(
        __init__=init,
        __repr__=cls.__repr__,
        **{m_name: m for m_name, m in cls.__dict__.items() if not m_name.startswith('_')}
    )

    _Cli = type('Cli', (cls,), cls_attrs)
    state['generated'] = _Cli

    return _Cli


class Schema(object, metaclass=schema.MetaSchema):
    """Base class for the user's configuration class"""

    def _get_configfile_asdict(self):
        result: Dict = {}

        configfile_path = configfile.get_config_path(self)
        if configfile_path is not None:
            result = utils.filter_fields(configfile.read_config(configfile_path), self)
            result = utils.type_correct_with(result, self)

        return result

    def _asdict(self):
        return schema.asdict(self)

    def _wrap(self):
        # TODO: Figure this out so Schema could live inside schema.py file
        c._init(self)

    @staticmethod
    def post_init(self, *args):
        pass

    @property
    def _fields(self):
        fields = [
            k for k in self.__dir__()
            if not k.startswith('_') and not inspect.ismethod(getattr(self, k))
        ]
        return fields

    def __call__(self, *args, **kwargs):
        pass


def prepare_signatures(cls, schema):
    """Adds possible parameters gathered from Schema to all methods
    defined in the 'Cli' class (decorated with @c). This way the parameters
    are the same for all methods, but at the same time they don't need to
    be duplicated in every method signature.
    """

    methods = {
        k: v for k, v in cls.__dict__.items()
        if not k.startswith('_') and inspect.isfunction(v)
    }

    params_with_post_init = [
        inspect.Parameter(name=field, kind=inspect._VAR_KEYWORD)
        for field in schema._fields
    ]

    # pop the post_init from the end of parameters
    params = [prm for prm in params_with_post_init if prm.name != 'post_init']

    # Hacking sys.argv to include positional keywords with assumed keyword names
    # as I couldn't find another workaround to tell python-fire how to parse these
    # The alternative had been to integrate python-fire with tighter coupling into this
    if len(sys.argv) > 2 and not any(['-h' in sys.argv, '--help' in sys.argv]):
        new_args = sys.argv[0:2]
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]
            prm = params[i - 2]

            if isinstance(arg, str) and arg.startswith('--') and not arg.endswith('--'):
                # After the first explicit `--param` append the rest of args as is i.e.
                # no need to parse for positional arguments after this point
                new_args += sys.argv[i:]
                break
            else:
                new_args.append(f'--{prm.name}')
                new_args.append(f'{arg}')
                i += 1
        sys.argv = new_args

    for m_name, method in methods.items():
        sig = inspect.signature(method)
        new_parameters = [v for v in sig.parameters.values()]
        new_parameters += params

        method.__signature__ = sig.replace(parameters=new_parameters)


def prepare(cls, schema: Schema):
    """Beef: prepares signatures, docstrings and initiates fire for the cli-magic"""
    prepare_signatures(cls, schema)
    docstring.wrap_method_docstring(cls, schema)

    with utils.suppress_traceback():

        if len(sys.argv) > 1 and sys.argv[-1] == 'version':
            # Version printing part 2
            print(schema.version)

        else:
            Fire(cls)
