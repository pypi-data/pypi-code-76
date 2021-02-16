# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['utube_search']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'aiohttp>=3.7.3,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'python-rapidjson>=1.0,<2.0',
 'rich>=9.11.0,<10.0.0',
 'typer>=0.3.2,<0.4.0',
 'uvloop>=0.15.0,<0.16.0']

entry_points = \
{'console_scripts': ['utube = utube_search.cli:app']}

setup_kwargs = {
    'name': 'utube-search',
    'version': '0.1.0',
    'description': 'An async API and a cli tool to search youtube.',
    'long_description': None,
    'author': 'unrahul',
    'author_email': 'rahulunair@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
