# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyintroduction']

package_data = \
{'': ['*'], 'jrpyintroduction': ['data/*', 'vignettes/*']}

install_requires = \
['matplotlib>=3.0', 'numpy>=1.19', 'pandas>=1']

setup_kwargs = {
    'name': 'jrpyintroduction',
    'version': '0.2.1',
    'description': 'Jumping Rivers: Introduction to Python',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
