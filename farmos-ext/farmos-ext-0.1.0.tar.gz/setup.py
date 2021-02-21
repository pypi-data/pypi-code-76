# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['farmos_ext', 'farmos_ext.cli', 'farmos_ext.reporting']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'farmOS>=0.2.0,<0.3.0',
 'prompt-toolkit>=3.0.16,<4.0.0']

setup_kwargs = {
    'name': 'farmos-ext',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lucas Brendel',
    'author_email': 'lucasbrendel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
