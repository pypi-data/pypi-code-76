# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['librelingo_tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'librelingo-types>=0.1.0,<0.2.0',
 'pyfakefs>=4.3.3,<5.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'slugify>=0.0.1,<0.0.2',
 'snapshottest>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'librelingo-tools',
    'version': '0.1.3',
    'description': 'Tools for authoring LibreLingo courses',
    'long_description': None,
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
