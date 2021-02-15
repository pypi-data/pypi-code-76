# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysparkly', 'pysparkly.extensions']

package_data = \
{'': ['*']}

install_requires = \
['py-deco>=0.1.0,<0.2.0', 'pyspark>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'pysparkly',
    'version': '0.1.1',
    'description': 'Pyspark useful functions and extensions',
    'long_description': None,
    'author': 'ugo-quelhas',
    'author_email': 'ugo.quelhas@edu.devinci.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
