# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinyevent']

package_data = \
{'': ['*'], 'tinyevent': ['.idea/*', '.idea/inspectionProfiles/*']}

setup_kwargs = {
    'name': 'tinyevent',
    'version': '0.1.0',
    'description': 'A tiny event module',
    'long_description': None,
    'author': 'afmelin',
    'author_email': 'afmelin@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
