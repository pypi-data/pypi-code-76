# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ment']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['m = ment.main:main']}

setup_kwargs = {
    'name': 'ment',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kawagh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
