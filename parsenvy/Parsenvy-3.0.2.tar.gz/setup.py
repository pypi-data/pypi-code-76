# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parsenvy']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=3.5.1,<4.0.0',
          'sphinx-rtd-theme>=0.5.1,<0.6.0',
          'm2r2>=0.2.7,<0.3.0']}

setup_kwargs = {
    'name': 'parsenvy',
    'version': '3.0.2',
    'description': 'Enviously elegant environment variable parsing',
    'long_description': "########################################################\nParsenvy: Enviously Elegant Environment Variable Parsing\n########################################################\n\n**Parsenvy** is an *enviously* elegant environment variable parsing Python library.\n\n.. image:: https://readthedocs.org/projects/parsenvy/badge/?version=latest&style=plastic\n        :target: https://parsenvy.readthedocs.io/en/latest\n        :alt: main Documentation Status\n\n.. image:: https://github.com/nkantar/Parsenvy/actions/workflows/code-quality-checks.yml/badge.svg?branch=main\n        :target: https://github.com/nkantar/Parsenvy/actions/workflows/code-quality-checks.yml\n        :alt: Github Actions\n\n.. image:: https://badge.fury.io/py/parsenvy.svg\n        :target: https://badge.fury.io/py/parsenvy\n        :alt: badgefury svg\n\n.. image:: https://img.shields.io/github/commits-since/nkantar/Parsenvy/3.0.2\n        :target: https://github.com/nkantar/Parsenvy/blob/main/CHANGELOG.md#unreleased\n        :alt: Unreleased chages\n\n.. image:: https://img.shields.io/github/license/nkantar/Parsenvy\n        :target: https://github.com/nkantar/Parsenvy/blob/main/LICENSE\n        :alt: License: BSD-3-Clause\n\nEnvironment variables are strings by default. This can be *rather* inconvenient if you're dealing with a number of them, and in a variety of desired types. Parsenvy aims to provide an intuitive, explicit interface for retrieving these values in appropriate types with *human-friendly* syntax.\n\n\nFeatures\n--------\n\n- Compatible with Python 3.6+ only (the last Python 2 compatible version was `1.0.2 <https://github.com/nkantar/Parsenvy/releases/tag/1.0.2>`_).\n- Fully tested on Linux, macOS, and Windows.\n- No dependencies outside of the Python standard library.\n- BSD (3-Clause) licensed.\n- Utterly awesome.\n- Now with `docs <https://parsenvy.readthedocs.io>`_!\n\n\nExamples\n--------\n\n.. code-block:: python\n\n    >>> import parsenvy\n\n    >>> parsenvy.bool('DEBUG_ENABLED')  # DEBUG_ENABLED=True\n    True\n\n    >>> parsenvy.int('POSTS_PER_PAGE')  # POSTS_PER_PAGE=13\n    13\n\n    >>> parsenvy.float('EXCHANGE_RATE')  # EXCHANGE_RATE=42.911\n    42.911\n\n    >>> parsenvy.list('INVALID_USERNAMES')  # INVALID_USERNAMES=admin,superuser,user,webmaster\n    ['admin', 'superuser', 'user', 'webmaster']\n\n    >>> parsenvy.tuple('SAMPLE_GREETING')  # SAMPLE_GREETING=Hello,world!\n    ('Hello', 'world!')\n\n    >>> parsenvy.set('ALLOWED_CATEGORIES')  # ALLOWED_CATEGORIES=python,vim,git\n    {'python', 'vim', 'git'}\n\n    >>> parsenvy.str('DB_PREFIX')  # DB_PREFIX=dj_\n    'dj_'\n\n\nInstall\n-------\n\n.. code-block:: shell\n\n    pip install parsenvy\n\n\nContributing\n------------\n\nContributions are welcome, and more information is available in the `contributing guide <https://parsenvy.readthedocs.io/en/latest/contributing.html>`_.\n",
    'author': 'Nik Kantar',
    'author_email': 'nik@nkantar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/Parsenvy',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
