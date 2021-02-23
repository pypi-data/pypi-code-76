# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bailiwick', 'tests', 'tests.units']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bailiwick',
    'version': '0.0.0.dev0',
    'description': 'Manage program contexts',
    'long_description': '# bailiwick\nPython library for managing contexts\n',
    'author': 'Toshio Kuratomi',
    'author_email': 'a.badger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abadger/bailiwick',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
