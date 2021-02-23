# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wap', 'wap.commands']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17.0,<0.18.0',
 'attrs>=20.3.0,<21.0.0',
 'click>=7.1.2,<8.0.0',
 'requests>=2.25.1,<3.0.0',
 'strictyaml>=1.3.2,<2.0.0']

entry_points = \
{'console_scripts': ['wap = wap.__main__:main']}

setup_kwargs = {
    'name': 'wow-addon-packager',
    'version': '0.3.0',
    'description': 'A tool that builds your World of Warcraft addon and uploads them to CurseForge',
    'long_description': None,
    'author': 'Tim Martin',
    'author_email': 'tim@timmart.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
