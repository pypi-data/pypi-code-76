# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['octalearn-poetry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'octalearn-poetry',
    'version': '0.1.0',
    'description': 'A sample project for showing basic python package management',
    'long_description': None,
    'author': 'Aldrin',
    'author_email': 'akmontan@ucsc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
