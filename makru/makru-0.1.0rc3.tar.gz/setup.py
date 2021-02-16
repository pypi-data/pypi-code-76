# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makru']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'clint>=0.5.1,<0.6.0',
 'httpx>=0.16.1,<0.17.0',
 'pluginbase>=1.0,<2.0',
 'semver>=2.13,<3.0']

entry_points = \
{'console_scripts': ['makru = makru.main:main']}

setup_kwargs = {
    'name': 'makru',
    'version': '0.1.0rc3',
    'description': 'Makru is a building system framework',
    'long_description': None,
    'author': 'thisLight',
    'author_email': 'l1589002388@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
