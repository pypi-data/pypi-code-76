# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['porto_task']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.4,<4.0.0',
 'numpy==1.19.5',
 'pandas>=1.2.2,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'tensorflow>=2.4.1,<3.0.0']

setup_kwargs = {
    'name': 'porto-task',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Scirpus22',
    'author_email': 'yurikamysh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
