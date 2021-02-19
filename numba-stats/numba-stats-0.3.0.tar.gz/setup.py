# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numba_stats']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.49,<0.50', 'numpy>=1.18,<2.0', 'scipy>=1.5,<2.0']

setup_kwargs = {
    'name': 'numba-stats',
    'version': '0.3.0',
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
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
