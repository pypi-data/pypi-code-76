# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splink_data_standardisation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'splink-data-standardisation',
    'version': '0.2.5',
    'description': '',
    'long_description': None,
    'author': 'Robin Linacre',
    'author_email': 'robin.linacre@digital.justice.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
