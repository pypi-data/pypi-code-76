# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parsenvy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'parsenvy',
    'version': '3.0.0',
    'description': 'Enviously elegant environment variable parsing',
    'long_description': "########################################################\nParsenvy: Enviously Elegant Environment Variable Parsing\n########################################################\n\n**Parsenvy** is an *enviously* elegant environment variable parsing Python library.\n\n.. image:: https://readthedocs.org/projects/parsenvy/badge/?version=latest&style=plastic\n        :target: https://parsenvy.readthedocs.io/en/latest\n        :alt: main Documentation Status\n\n.. image:: https://github.com/nkantar/Parsenvy/actions/workflows/code-quality-checks.yml/badge.svg?branch=main\n        :target: https://github.com/nkantar/Parsenvy/actions/workflows/code-quality-checks.yml\n        :alt: Github Actions\n\n.. image:: https://badge.fury.io/py/Parsenvy.svg\n        :target: https://badge.fury.io/py/Parsenvy\n        :alt: badgefury svg\n\n.. image:: https://img.shields.io/github/commits-since/nkantar/Parsenvy/3.0.0\n        :target: https://github.com/nkantar/Parsenvy/blob/main/CHANGELOG.md#unreleased\n        :alt: Unreleased chages\n\n.. image:: https://img.shields.io/github/license/nkantar/Parsenvy\n        :target: https://github.com/nkantar/Parsenvy/blob/main/LICENSE\n        :alt: License: BSD-3-Clause\n\nEnvironment variables are strings by default. This can be *rather* inconvenient if you're dealing with a number of them, and in a variety of desired types. Parsenvy aims to provide an intuitive, explicit interface for retrieving these values in appropriate types with *human-friendly* syntax.\n\n\nFeatures\n--------\n\n- Compatible with Python 3.6+ only (the last Python 2 compatible version was `1.0.2 <https://github.com/nkantar/Parsenvy/releases/tag/1.0.2>`_).\n- Fully tested on Linux, macOS, and Windows.\n- No dependencies outside of the Python standard library.\n- BSD (3-Clause) licensed.\n- Utterly awesome.\n- Now with `docs <https://parsenvy.readthedocs.io>`_!\n\n\nExamples\n--------\n\n.. code-block:: python\n\n    >>> import parsenvy\n    >>> parsenvy.bool('BOOL_ENV_VAR')  # BOOL_ENV_VAR=True\n    True\n    >>> parsenvy.int('INT_ENV_VAR')  # INT_ENV_VAR=13\n    13\n    >>> parsenvy.float('FLOAT_ENV_VAR')  # FLOAT_ENV_VAR=555.55\n    555.55\n    >>> parsenvy.list('LIST_ENV_VAR')  # LIST_ENV_VAR=shiver,me,timbers\n    ['shiver', 'me', 'timbers']\n    >>> parsenvy.tuple('TUPLE_ENV_VAR')  # TUPLE_ENV_VAR=hello,world\n    ('hello', 'world')\n    >>> parsenvy.str('STR_ENV_VAR')  # STR_ENV_VAR=meep\n    'meep'\n    >>> parsenvy.set('SET_ENV_VAR')  # SET_ENV_VAR=wat,wut,wot\n    set(['wat', 'wut', 'wot'])\n\n\nInstall\n-------\n\n.. code-block:: shell\n\n    pip install parsenvy\n\n\nContributing\n------------\n\nContributions are welcome, and more information is available in the `contributing guide <https://parsenvy.readthedocs.io/en/latest/contributing.html>`_.\n",
    'author': 'Nik Kantar',
    'author_email': 'nik@nkantar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/Parsenvy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
