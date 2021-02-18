"""Exposes the settings declared in the environment variable
``UNIMATRIX_SETTINGS_MODULE``."""
import contextlib
import functools
import importlib
import inspect
import itertools
import os

import unimatrix.environ
from unimatrix.exceptions import ImproperlyConfigured


class Settings:
    """Proxy object to load settings lazily."""
    not_initialized = object()

    @property
    def available(self) -> list:
        """Return the list of available settings."""
        if not self.__is_initialized:
            self.initialize()
        return list(sorted(set(itertools.chain(
            self.__overrides\
                if self.__overrides != self.not_initialized\
                else [],
            dict.keys(self.__values),
            dict.keys(self.__environ)
        ))))

    def __init__(self, env=None):
        self.__is_initialized = False
        self.__environ = env or {}
        self.__overrides = self.not_initialized
        self.__values = {}

    def destroy(self):
        """Reset the :class:`~unimatrix.conf.Settings` object to
        a pristine state.
        """
        self.__is_initialized = False
        self.__environ = {}
        self.__overrides = self.not_initialized
        self.__values = {}

    def initialize(self):
        """Initialize the settings using system environment variables and
        the Python module specified by ``UNIMATRIX_SETTINGS_MODULE``.
        """
        if self.__is_initialized:
            raise RuntimeError
        settings = self._get_settings_module()
        if settings is not None:
            for attname, value in inspect.getmembers(settings):
                if not str.isupper(attname):
                    continue
                self.__values[attname] = value

        # Add the values to the environ dictionary.
        for attname, value in inspect.getmembers(unimatrix.environ):
            if not str.isupper(attname):
                continue
            self.__environ[attname] = value

        self.__is_initialized = True

    @contextlib.contextmanager
    def override(self, **settings):
        """Override the settings with the given values. Not thread-safe."""
        if self.__overrides != self.not_initialized:
            raise RuntimeError("Nested overrides are not supported.")
        try:
            self.__overrides = settings
            yield
        finally:
            self.__overrides = self.not_initialized

    def with_overrides(self, **overrides):
        """Decorates a function to use the given settings overrides."""
        def decorator_factory(func):
            @functools.wraps(func)
            def f(*args, **kwargs):
                with self.override(**overrides):
                    return func(*args, **kwargs)
            return f
        return decorator_factory

    def _get_settings_module(self):
        os.environ.setdefault('DEPLOYMENT_ENV', 'production')
        settings = None
        if os.getenv('UNIMATRIX_SETTINGS_MODULE'):
            module_qualname = os.getenv('UNIMATRIX_SETTINGS_MODULE')
            try:
                settings = importlib.import_module(module_qualname)
            except ImportError:
                raise ImproperlyConfigured(
                    "Can not import settings module %s" % module_qualname)
        return settings

    def __getattr__(self, attname):
        if not self.__is_initialized:
            self.initialize()
        value = sentinel = object()
        if self.__overrides != self.not_initialized:
            value = self.__overrides.get(attname, sentinel)
        if value == sentinel:
            value = self.__values.get(attname, sentinel)
        if value == sentinel:
            value = self.__environ.get(attname, sentinel)
        if value == sentinel:
            raise AttributeError("No such setting: %s" % attname)
        return value


settings = Settings()
