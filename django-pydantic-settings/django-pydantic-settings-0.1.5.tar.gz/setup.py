# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_settings']

package_data = \
{'': ['*']}

install_requires = \
['Django>=1.11', 'dj-database-url>=0.5.0,<0.6.0', 'pydantic>=1.7.3,<2.0.0']

extras_require = \
{u'sentry': ['sentry-sdk']}

setup_kwargs = {
    'name': 'django-pydantic-settings',
    'version': '0.1.5',
    'description': 'Manage Django settings with Pydantic.',
    'long_description': '# django-pydantic-settings\n\n## Use pydantic settings management to simplify configuration of Django settings.\n\nVery much a work in progress, but reads the standard DJANGO_SETTINGS_MODULE environment variable (defaulting to pydantic_settings.Settings) to load a sub-class of pydantic_settings.Settings. All settings (that have been defined in pydantic_settings.Settings) can be overridden with environment variables. A special DatabaseSettings class is used to allow multiple databases to be configured simply with DSNs. In theory, django-pydantic-settings should be compatible with any version of Django that runs on Python 3.6+ (which means Django 1.11 and on), but has so far only been tested against Django 3.1.\n\n## Installation & Setup\n\nInstall django-pydantic-settings:\n\n```\npip install django-pydantic-settings\n```\n\nModify your Django project\'s `manage.py` file to use django-pydantic-settings, it should look something like this:\n\n```python\n#!/usr/bin/env python\n"""Django\'s command-line utility for administrative tasks."""\nimport sys\n\nfrom pydantic_settings import SetUp\n\n\ndef main():\n    """Run administrative tasks."""\n    SetUp().configure()\n\n    try:\n        from django.core.management import execute_from_command_line\n    except ImportError as exc:\n        raise ImportError(\n            "Couldn\'t import Django. Are you sure it\'s installed and "\n            "available on your PYTHONPATH environment variable? Did you "\n            "forget to activate a virtual environment?"\n        ) from exc\n    execute_from_command_line(sys.argv)\n\n\nif __name__ == "__main__":\n    main()\n```\n\nYour `wsgi.py` and/or `asgi.py` files will need to be modified similarly, and look something like this:\n\n```python\nfrom django.core.wsgi import get_wsgi_application\n\nfrom pydantic_settings import SetUp\n\nSetUp().configure()\napplication = get_wsgi_application()\n```\n\nThe `SetUp` class will automatically look for the standard `DJANGO_SETTINGS_MODULE` environment variable, read it, confirm that it points to an existing Python module, and load that module. Your `DJANGO_SETTINGS_MODULE` variable should point to a `pydantic_settings.settings.Settings` sub-class (though technically any Python class that defines a `dict()` method which returns a Python dictionary of key/value pairs matching the required Django settings will work). Calling the `configure()` method will then use the specified module to configure your project\'s Django settings.\n\n## Database configuration\n\nBy defining multiple `DatabaseDsn` attributes of the `DatabaseSettings` class, you can easily configure one or more database connections with environment variables. DSNs are parsed using dj-database-url.\n\n```python\nclass DatabaseSettings(BaseSettings):\n    default: DatabaseDsn = Field(env="DATABASE_URL")\n    secondary: DatabaseDsn = Field(env="SECONDARY_DATABASE_URL")\n```\n\n```python\n\xe2\x9d\xaf DATABASE_URL=sqlite:///foo SECONDARY_DATABASE_URL=sqlite:///bar ./settings_test/manage.py shell\nPython 3.9.1 (default, Jan  8 2021, 17:17:43)\n[Clang 12.0.0 (clang-1200.0.32.28)] on darwin\nType "help", "copyright", "credits" or "license" for more information.\n(InteractiveConsole)\n>>> from django.conf import settings\n...\n>>> pp.pprint(settings.DATABASES)\n{   \'default\': {   \'ATOMIC_REQUESTS\': False,\n                   \'AUTOCOMMIT\': True,\n                   \'CONN_MAX_AGE\': 0,\n                   \'ENGINE\': \'django.db.backends.sqlite3\',\n                   \'HOST\': \'\',\n                   \'NAME\': \'foo\',\n                   \'OPTIONS\': {},\n                   \'PASSWORD\': \'\',\n                   \'PORT\': \'\',\n                   \'TEST\': {   \'CHARSET\': None,\n                               \'COLLATION\': None,\n                               \'MIGRATE\': True,\n                               \'MIRROR\': None,\n                               \'NAME\': None},\n                   \'TIME_ZONE\': None,\n                   \'USER\': \'\'},\n    \'secondary\': {   \'CONN_MAX_AGE\': 0,\n                     \'ENGINE\': \'django.db.backends.sqlite3\',\n                     \'HOST\': \'\',\n                     \'NAME\': \'bar\',\n                     \'PASSWORD\': \'\',\n                     \'PORT\': \'\',\n                     \'USER\': \'\'}}\n>>>\n```\n',
    'author': 'Josh Ourisman',
    'author_email': 'me@josho.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joshourisman/django-pydantic-settings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
