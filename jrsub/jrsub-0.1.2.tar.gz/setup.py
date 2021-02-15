# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrsub']

package_data = \
{'': ['*']}

install_requires = \
['jtran>=0.2.13,<0.3.0', 'tqdm>=4.56.2,<5.0.0']

setup_kwargs = {
    'name': 'jrsub',
    'version': '0.1.2',
    'description': 'Python package for working with Warodai and Yarxi dictionaries',
    'long_description': '# JRSub\n[![PyPI](https://img.shields.io/pypi/v/jrsub.svg)](https://pypi.python.org/pypi/jrsub)\n[![Build Status](https://travis-ci.com/kateabr/jsub.svg?branch=master)](https://travis-ci.com/kateabr/jsub)',
    'author': 'Ekaterina Biryukova',
    'author_email': 'kateabr@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kateabr/jrsub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
