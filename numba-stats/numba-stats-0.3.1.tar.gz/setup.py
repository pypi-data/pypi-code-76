# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numba_stats']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=3.4', 'numba>=0.49', 'numpy>=1.18', 'scipy>=1.5']

setup_kwargs = {
    'name': 'numba-stats',
    'version': '0.3.1',
    'description': '',
    'long_description': None,
    'author': 'Hans Dembinski',
    'author_email': 'hans.dembinski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
