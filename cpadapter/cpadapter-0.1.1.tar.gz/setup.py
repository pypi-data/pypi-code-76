# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpadapter']

package_data = \
{'': ['*']}

install_requires = \
['lightgbm>=3.1,<4.0',
 'matplotlib>=3.0,<4.0',
 'nonconformist>=2.1.0,<3.0.0',
 'numpy>=1.19,<2.0',
 'pandas>=1.1,<2.0',
 'seaborn>=0.11,<0.12',
 'sklearn>=0.0,<0.1',
 'typing>=3.7,<4.0']

setup_kwargs = {
    'name': 'cpadapter',
    'version': '0.1.1',
    'description': 'This package adapts different models in order to create confidence intervals using conformal prediction',
    'long_description': None,
    'author': 'mjesusugarte',
    'author_email': 'maria.jesus@spikelab.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
