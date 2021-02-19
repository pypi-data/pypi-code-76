# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carling', 'carling.io', 'carling.iter_utils', 'carling.test_utils']

package_data = \
{'': ['*']}

install_requires = \
['apache_beam>=2.22.0,<3.0.0', 'deepdiff>=5.0.2,<6.0.0']

setup_kwargs = {
    'name': 'carling',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Adam Moore',
    'author_email': 'adam@mcdigital.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
