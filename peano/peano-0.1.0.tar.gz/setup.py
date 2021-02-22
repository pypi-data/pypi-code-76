# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peano']

package_data = \
{'': ['*']}

install_requires = \
['influxdb-client>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'peano',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anton Panchenko',
    'author_email': 'apanchenko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
