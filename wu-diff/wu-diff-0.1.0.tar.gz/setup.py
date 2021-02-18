# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wu_diff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wu-diff',
    'version': '0.1.0',
    'description': 'Wu(O(NP)) algorithm',
    'long_description': None,
    'author': 'maiseaux',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
