"""Storing persistent application settings on any platform using a context
manager instance.
"""

import os
import json

from appdirs import user_config_dir

from .application import Application

__all__ = ['Settings']

class Settings:
    """Storing persistent application settings on any platform.

    >>> with Settings() as settings:
    ...    settings['app'] = {'name': 'My App', users=['Monty', 'John'])
    ...    name = settings.get('app').get('name')
    """

    suffix = 'qutie'

    def __init__(self, persistent=True):

        self.persistent = persistent
        self.__settings = {}

    @property
    def persistent(self):
        return self.__persistent

    @persistent.setter
    def persistent(self, value):
        self.__persistent = value

    @property
    def filename(self):
        app = Application.instance()
        appname = app.name
        appauthor = app.organization
        path = user_config_dir(appname, appauthor)
        return f'{path}.{self.suffix}'

    def __enter__(self):
        """Read application settings from filesystem (if existing)."""
        filename = self.filename
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                try:
                    self.__settings = json.load(f)
                except json.JSONDecodeError:
                    self.__settings = {}
        return self.__settings

    def __exit__(self, *exc):
        """Write application settings to filesystem."""
        if self.persistent:
            filename = self.filename
            path = os.path.dirname(filename)
            if not os.path.exists(path):
                os.makedirs(path)
            with open(filename, 'w') as f:
                # Can raise exception!
                f.write(json.dumps(self.__settings))
        self.__settings = {}
        return False
