# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['librelingo_fakes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'librelingo-fakes',
    'version': '0.1.1',
    'description': 'Fake data for testing LibreLingo-related packages',
    'long_description': None,
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
