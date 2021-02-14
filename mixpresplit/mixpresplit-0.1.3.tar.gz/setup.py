# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mixpresplit']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'wavinfo>=1.6,<2.0']

entry_points = \
{'console_scripts': ['mixpresplit = mixpresplit.cli:main']}

setup_kwargs = {
    'name': 'mixpresplit',
    'version': '0.1.3',
    'description': 'CLI Utility that allows splitting mixpre polywav files',
    'long_description': None,
    'author': 'David Huss',
    'author_email': 'dh@atoav.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
