import contextlib
import glob
import inspect
import itertools
import functools

import yaml

from ioc import provider
from ioc import schema
from ioc.requirement import DeclaredRequirement
from ioc.requirement import NOT_PROVIDED
from ioc.requirement import NO_DEFAULT
from ioc.exc import UnsatisfiedDependency
from ioc.exc import MissingDependencies
from ioc.pkg import setup
from ioc.pkg import teardown
from ioc.provider import get_unsatisfied_dependencies


__version__ = '1.3.11'


__all__ = [
    'inject',
    'is_satisfied',
    'provide',
    'require',
    'setup',
    'teardown',
]


def require(names, *args, **kwargs):
    req = provider.get_requirement(names)
    if req is not None:
        return req

    return DeclaredRequirement(provider, names, *args, **kwargs)


def provide(name, value, force=False, tags=None):
    """Register a Python object as a dependency under the key `name`."""
    provider.register(name, value, force=force, tags=tags)
    return value


def retire(name):
    return provider.retire(name)


def override(name, value):
    return provide(name, value, force=True)


def load(dependencies, override=False):
    s = schema.Parser(override=override).load(dependencies)
    s.resolve(schema.Resolver())


def load_config(filenames=['etc/ioc.conf', 'etc/ioc.conf.d/*'], override=True):
    for filepath in itertools.chain(*[glob.glob(x) for x in filenames]):
        with open(filepath) as f:
            load(yaml.safe_load(f.read()), override=override)


def is_satisfied(name):
    return provider.is_satisfied(name)


def tagged(tag):
    return provider.tagged(tag)


class class_property(object):

    def __init__(self, name, factory=None, default=NO_DEFAULT):
        self.name = name
        self.factory = factory or (lambda x: x)
        self.dep = require(name, default=default)
        self.default = default

    def __get__(self, obj, objtype):
        if self.dep._injected is NOT_PROVIDED:
            self.dep._setup()
        return self.factory(self.dep)


class inject:
    """Ensures that `injected` is made available under
    `name`.

    For decorated classes, this implies that the decorator
    sets an attribute `name` on the class with a
    :class:`class_property` instance pointing to `injected`.
    """

    @classmethod
    def context(cls, name, injected):
        """Shortcut to inject a contextual dependency in the function call
        scope.
        """
        return cls(name, injected, scope='function')

    def __init__(self, name, injected, scope='process'):
        self.attname = name
        self.injected = injected
        self.scope = scope

    def __call__(self, obj):
        if inspect.isclass(obj):
            d = self._decorate_class(obj)
        elif inspect.iscoroutinefunction(obj):
            d = self._decorate_coroutinefunction(obj)
        elif inspect.isfunction(obj):
            d = self._decorate_function(obj)
        else:
            raise ValueError("Can only decorate classes and functions atm.")
        return d

    def _decorate_class(self, obj):
        setattr(obj, self.attname, class_property(self.injected))
        return obj

    def _decorate_function(self, obj):
        @functools.wraps(obj)
        def f(*args, **kwargs):
            kwargs[self.attname] = require(self.injected)
            return obj(*args, **kwargs)
        return f

    def _decorate_coroutinefunction(self, obj):
        @functools.wraps(obj)
        async def f(*args, **kwargs):
            dep = require(self.injected)
            if hasattr(dep, 'as_context'):
                dep = dep.as_context()
            async with _ensure_async_context(dep, self.scope) as ctx:
                kwargs[self.attname] = ctx
                return await obj(*args, **kwargs)
        return f


@contextlib.asynccontextmanager
async def _ensure_async_context(dep, scope):
    if scope != 'function':
        yield dep
    else:
        is_context_manager = hasattr(dep, '__aenter__')
        try:
            yield (await dep.__aenter__()) if is_context_manager else dep
        except Exception as e:
            if is_context_manager:
                await dep.__aexit__(type(e), e, None)
            raise
        else:
            if is_context_manager:
                await dep.__aexit__(None, None, None)


def call(name, *args, **kwargs):
    """Invoke the dependency identified by `name` with
    the given positional and keyword arguments.
    """
    pass


def check():
    """Inspect the provider and raise an exception if there are missing
    dependencies.
    """
    missing = get_unsatisfied_dependencies()
    if missing:
        raise MissingDependencies(missing)
