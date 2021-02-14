# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['meshless']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0']

setup_kwargs = {
    'name': 'meshless.py',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Tiago Vilela',
    'author_email': 'tiagovla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
