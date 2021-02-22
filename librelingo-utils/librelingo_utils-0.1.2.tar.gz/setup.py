# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['librelingo_utils']

package_data = \
{'': ['*']}

install_requires = \
['librelingo-types>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'librelingo-utils',
    'version': '0.1.2',
    'description': 'Utilities to be used in LibreLingo-related-packages',
    'long_description': None,
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
