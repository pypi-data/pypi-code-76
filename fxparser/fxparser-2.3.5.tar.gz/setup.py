# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fxparser']

package_data = \
{'': ['*'], 'fxparser': ['assets/*']}

install_requires = \
['emoji>=0.6.0,<0.7.0', 'spacy>=2.3.5,<3.0.0', 'tensorflow>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'fxparser',
    'version': '2.3.5',
    'description': 'A forex message parser to extract information such as symbols, tps, and sls',
    'long_description': None,
    'author': 'Danny',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
