# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_anvil',
 'python_anvil.api_resources',
 'python_anvil.api_resources.mutations',
 'python_anvil.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'dataclasses-json>=0.5.2,<0.6.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.25.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['anvil = python_anvil.cli:cli']}

setup_kwargs = {
    'name': 'python-anvil',
    'version': '0.1.1',
    'description': 'Anvil API',
    'long_description': '# Anvil API Library\n\n[![PyPI Version](https://img.shields.io/pypi/v/python-anvil.svg)](https://pypi.org/project/python-anvil)\n[![PyPI License](https://img.shields.io/pypi/l/python-anvil.svg)](https://pypi.org/project/python-anvil)\n\nThis is a library that provides an interface to access the [Anvil API](https://www.useanvil.com/developers) from applications\nwritten in the Python programming language.\n\nAnvil is a suite of tools for integrating document-based workflows and PDFs within your application:\n\n1. Anvil Workflows converts your PDF forms into simple, intuitive websites that \n   fill the PDFs and gather signatures for you.\n2. Anvil PDF Filling API allows you to fill any PDF with JSON data.\n3. Anvil PDF Generation API allows you to create new PDFs.\n4. Anvil Etch E-sign API allows you to request signatures on a PDF signing packet.\n\nCurrently, this API library only supports our PDF filling API and our GraphQL API.\n\n### Documentation\n\nGeneral API documentation: [Anvil API docs](https://www.useanvil.com/docs)\n\n# Setup\n\n## Requirements\n\n* Python 3.6+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install python-anvil\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add python-anvil\n```\n\n',
    'author': 'Allan Almazan',
    'author_email': 'allan@useanvil.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.useanvil.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
