# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataclass_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dataclass-utils',
    'version': '0.7.2',
    'description': '',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
