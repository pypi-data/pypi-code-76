# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zum']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.1,<0.17.0', 'tomlkit>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['zum = zum.cli:dispatcher']}

setup_kwargs = {
    'name': 'zum',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Zum\n',
    'author': 'Daniel Leal',
    'author_email': 'dlleal@uc.cl',
    'maintainer': 'Daniel Leal',
    'maintainer_email': 'dlleal@uc.cl',
    'url': 'https://github.com/daleal/zum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
