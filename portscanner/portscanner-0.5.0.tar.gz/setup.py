# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portscanner', 'portscanner.mixins']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0', 'black>=20.8b1,<21.0', 'colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['portscanner = portscanner.console:run']}

setup_kwargs = {
    'name': 'portscanner',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'GoodiesHQ',
    'author_email': 'aarcher73k@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
