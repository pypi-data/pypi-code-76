# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['moonbeam']
setup_kwargs = {
    'name': 'moonbeam',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Andrew',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
