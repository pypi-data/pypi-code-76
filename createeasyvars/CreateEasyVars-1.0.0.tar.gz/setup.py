# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['createeasyvars']
setup_kwargs = {
    'name': 'createeasyvars',
    'version': '1.0.0',
    'description': 'Welcome to the new library for creating lightweight variables such as: string, int, bool. Creating a variable is very easy!',
    'long_description': None,
    'author': 'tikotstudio',
    'author_email': 'tikotstudio@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
