# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['autoreadme']
install_requires = \
['packagit>=0.2101.11,<0.2102.0']

setup_kwargs = {
    'name': 'autoreadme',
    'version': '0.2101.17',
    'description': 'Generate READMEs with collapsable code and corresponding output from Python.',
    'long_description': None,
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
