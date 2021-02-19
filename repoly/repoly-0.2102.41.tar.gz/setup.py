# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repoly',
 'repoly.app',
 'repoly.geometry',
 'repoly.geometry.abs',
 'repoly.geometry.abs.mixin',
 'repoly.gui',
 'repoly.gui.abs']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.0.1,<7.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['repoly = repoly.app.main:run']}

setup_kwargs = {
    'name': 'repoly',
    'version': '0.2102.41',
    'description': 'Rectilinear polygons',
    'long_description': None,
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
