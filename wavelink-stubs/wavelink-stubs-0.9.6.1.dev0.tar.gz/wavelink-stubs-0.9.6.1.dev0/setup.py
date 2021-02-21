# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wavelink-stubs']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.2.5', 'mypy>=0.800', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'wavelink-stubs',
    'version': '0.9.6.1.dev0',
    'description': 'wavelink stubs',
    'long_description': '# Wavelink Stubs',
    'author': 'Josh',
    'author_email': 'josh@josh-is.gay',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bijij/wavelink-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
