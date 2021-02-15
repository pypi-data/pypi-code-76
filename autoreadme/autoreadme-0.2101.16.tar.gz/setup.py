# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['autoreadme']
setup_kwargs = {
    'name': 'autoreadme',
    'version': '0.2101.16',
    'description': 'Generate READMEs with collapsable code and corresponding output from Python.',
    'long_description': None,
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
