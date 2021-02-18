# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afisys_monitor']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'humanfriendly>=9.1,<10.0',
 'reprint>=0.5.2,<0.6.0',
 'tabulate>=0.8.7,<0.9.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['afisys-monitor = afisys_monitor:main']}

setup_kwargs = {
    'name': 'afisys-monitor',
    'version': '0.2.0',
    'description': 'CLI monitor for various screens',
    'long_description': None,
    'author': 'Anders Johansen',
    'author_email': 'afinvold@fastmail.fm',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
