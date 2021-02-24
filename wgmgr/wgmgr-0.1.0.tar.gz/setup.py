# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wgmgr', 'wgmgr.cli', 'wgmgr.templates']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'colorama>=0.4.4,<0.5.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['wgmgr = wgmgr.cli.main:app']}

setup_kwargs = {
    'name': 'wgmgr',
    'version': '0.1.0',
    'description': 'Easily manage wireguard configs.',
    'long_description': None,
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
