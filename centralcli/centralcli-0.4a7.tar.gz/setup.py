# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['centralcli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'Pygments>=2.7.3,<3.0.0',
 'aiohttp>=3.7.3,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'certifi>=2020.12.5,<2021.0.0',
 'colorama>=0.4.4,<0.5.0',
 'halo>=0.0.31,<0.0.32',
 'idna>=2.10,<3.0',
 'pendulum>=2.1.2,<3.0.0',
 'pycentral>=0.0.1,<0.0.2',
 'pylibyaml>=0.1.0,<0.2.0',
 'rich>=9.10.0,<10.0.0',
 'shellingham>=1.3.2,<2.0.0',
 'tablib>=3.0.0,<4.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tinydb>=4.3.0,<5.0.0',
 'typer>=0.3.2,<0.4.0',
 'urllib3>=1.26.2,<2.0.0']

entry_points = \
{'console_scripts': ['cencli = centralcli.cli:app']}

setup_kwargs = {
    'name': 'centralcli',
    'version': '0.4a7',
    'description': 'A CLI for interacting with Aruba Central (Cloud Management Platform).  Facilitates bulk imports, exports, reporting.  A handy tool if you have devices managed by Aruba Central.',
    'long_description': "*Rough Work in Progress at this point. Recommend 'watching' this repo if interested to monitor progress*\n\nA CLI app for interacting with Aruba Central Clound Management Platform. The aim is to support a lot of the common work-flows via a simple CLI with auto-complete, help text etc.  Bulk tasks supported via import-files.\n\n**Work in Progress pre-alpha**\n\nAdditional Documentation to follow.",
    'author': 'Wade Wells (Pack3tL0ss)',
    'author_email': 'wade@consolepi.org',
    'maintainer': 'Wade Wells (Pack3tL0ss)',
    'maintainer_email': 'wade@consolepi.org',
    'url': 'https://github.com/Pack3tL0ss/central-api-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
