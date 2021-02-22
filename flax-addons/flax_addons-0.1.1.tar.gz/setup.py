# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flax_addons',
 'flax_addons.layers',
 'flax_addons.preprocessing',
 'flax_addons.utils',
 'flax_addons.utils.cuda']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.2.7,<0.3.0',
 'jaxlib>=0.1.61,<0.2.0',
 'librosa>=0.8.0,<0.9.0',
 'numpy>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'flax-addons',
    'version': '0.1.1',
    'description': 'flax addons',
    'long_description': '# flax-addons',
    'author': 'machineko',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/machineko/flax-addons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
