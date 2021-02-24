# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['summarize_cross_validation_score']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0', 'pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'summarize-cross-validation-score',
    'version': '0.1.0',
    'description': 'summarizes the output of cross_validate function',
    'long_description': None,
    'author': 'Debananda Sarkar',
    'author_email': 'sarkar.debananda.1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
