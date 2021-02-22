# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['armorstand', 'armorstand.date', 'armorstand.youtube']

package_data = \
{'': ['*']}

install_requires = \
['youtube_dl>=2021.2.10,<2022.0.0']

setup_kwargs = {
    'name': 'armorstand',
    'version': '21.2.22.20.27',
    'description': 'All my utility functions',
    'long_description': '# Armorstand\n\n> **Util functions.**',
    'author': 'ninest',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninest/armorstand/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
