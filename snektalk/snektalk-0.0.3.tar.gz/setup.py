# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snektalk']

package_data = \
{'': ['*'], 'snektalk': ['assets/*', 'assets/scripts/*', 'assets/style/*']}

install_requires = \
['coleo>=0.2.1,<0.3.0',
 'hrepr>=0.3.9,<0.4.0',
 'jurigged>=0.1.5,<0.2.0',
 'sanic>=20.9.1,<21.0.0']

entry_points = \
{'console_scripts': ['sktk = snektalk.cli:main',
                     'snektalk = snektalk.cli:main']}

setup_kwargs = {
    'name': 'snektalk',
    'version': '0.0.3',
    'description': 'Advanced Python REPL',
    'long_description': '\n# TODO\n\nPackage is not functional yet.\n',
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/breuleux/snektalk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
