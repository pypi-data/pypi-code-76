# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['GPIOLibrary']

package_data = \
{'': ['*']}

install_requires = \
['robotframework>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'robotframework-gpio',
    'version': '0.1.0a0',
    'description': "Robot Framework Library for GPIO Interface on Raspberry Pi's",
    'long_description': "# GPIOLibrary\n\nRobot Framework library for interfacing GPIO pins on Raspberry Pi's.\n\n## Installation\n",
    'author': 'Yusuf Can Bayrak',
    'author_email': 'yusufcanbayrak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
