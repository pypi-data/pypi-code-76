# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biobeaker']

package_data = \
{'': ['*']}

install_requires = \
['baseconvert==1.0.0.a4',
 'numpy==1.19.2',
 'tensorflow-addons==0.12.1',
 'tensorflow==2.4.1']

setup_kwargs = {
    'name': 'biobeaker',
    'version': '0.0.2',
    'description': 'Coming soon',
    'long_description': '# BEAKER\n\n[![Build Status](https://travis-ci.com/jguhlin/beaker.svg?branch=main)](https://travis-ci.com/jguhlin/beaker) [![codecov](https://codecov.io/gh/jguhlin/beaker/branch/main/graph/badge.svg?token=C83YL05H8H)](undefined)\n\nImplementation of BEAKER Machine Learning Model by [Joseph Guhlin](https://github.com/jguhlin) and [Rachael Ashby](https://github.com/r-ashby).\n\nMore info coming soon\n\n# Code Format\nWe use python black code formatter for this repo.\n\n',
    'author': 'Joseph Guhlin',
    'author_email': 'joseph.guhlin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jguhlin/beaker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
