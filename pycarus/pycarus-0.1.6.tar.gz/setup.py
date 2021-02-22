# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycarus',
 'pycarus.datasets',
 'pycarus.geometry',
 'pycarus.learning',
 'pycarus.learning.data']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.3.0,<0.4.0',
 'h5py>=3.1.0,<4.0.0',
 'open3d>=0.12.0,<0.13.0',
 'pytorch3d>=0.3.0,<0.4.0',
 'torch>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'pycarus',
    'version': '0.1.6',
    'description': 'Utilities for computer vision and 3D geometry',
    'long_description': None,
    'author': 'Luca De Luigi',
    'author_email': 'lucadeluigi91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.9.0',
}


setup(**setup_kwargs)
