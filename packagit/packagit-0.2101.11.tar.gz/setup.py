# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['packagit']
install_requires = \
['GitPython>=3.1.13,<4.0.0']

setup_kwargs = {
    'name': 'packagit',
    'version': '0.2101.11',
    'description': 'Increment version, create and push tag for release',
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
