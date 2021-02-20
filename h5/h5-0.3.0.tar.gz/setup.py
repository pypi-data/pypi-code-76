# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['h5']

package_data = \
{'': ['*']}

install_requires = \
['h5py']

setup_kwargs = {
    'name': 'h5',
    'version': '0.3.0',
    'description': 'H5py utils',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
