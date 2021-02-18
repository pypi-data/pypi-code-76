# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['lager']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'lager',
    'version': '0.15.0',
    'description': 'EZ-PZ logging based on loguru',
    'long_description': None,
    'author': 'jesse rubin',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
