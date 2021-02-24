# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toy_pypkg']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0', 'pytest>=6.2.2,<7.0.0']

setup_kwargs = {
    'name': 'toy-pypkg',
    'version': '0.1.0',
    'description': 'Toy python packag (test)',
    'long_description': None,
    'author': 'mmyz',
    'author_email': 'yzmarco.ma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
