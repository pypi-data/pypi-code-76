# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apologies']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0', 'cattrs>=1.1.1,<2.0.0', 'pendulum>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'apologies',
    'version': '0.1.33',
    'description': 'Python code to play a game similar to Sorry',
    'long_description': '# Apologies Python Library\n\n[![pypi](https://img.shields.io/pypi/v/apologies.svg)](https://pypi.org/project/apologies/)\n[![license](https://img.shields.io/pypi/l/apologies.svg)](https://github.com/pronovic/apologies/blob/master/LICENSE)\n[![wheel](https://img.shields.io/pypi/wheel/apologies.svg)](https://pypi.org/project/apologies/)\n[![python](https://img.shields.io/pypi/pyversions/apologies.svg)](https://pypi.org/project/apologies/)\n[![Test Suite](https://github.com/pronovic/apologies/workflows/Test%20Suite/badge.svg)](https://github.com/pronovic/apologies/actions?query=workflow%3A%22Test+Suite%22)\n[![docs](https://readthedocs.org/projects/apologies/badge/?version=stable&style=flat)](https://apologies.readthedocs.io/en/stable/)\n[![coverage](https://coveralls.io/repos/github/pronovic/apologies/badge.svg?branch=master)](https://coveralls.io/github/pronovic/apologies?branch=master)\n\n[Apologies](https://github.com/pronovic/apologies) is a Python library that implements a game similar to the [Sorry](https://en.wikipedia.org/wiki/Sorry!_(game)) board game.  On UNIX-like platforms, it includes a console demo that plays the game with automated players, intended for use by developers and not by end users.  See the [documentation](https://apologies.readthedocs.io/en/stable) for notes about the public interface.\n\nIt was written as a learning exercise and technology demonstration effort, and\nserves as a complete example of how to manage a modern (circa 2020) Python\nproject, including style checks, code formatting, integration with IntelliJ, CI\nbuilds at GitHub, and integration with PyPI and Read the Docs.\n',
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/apologies/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
