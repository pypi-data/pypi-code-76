# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mpan']
setup_kwargs = {
    'name': 'mpan',
    'version': '1.0.0',
    'description': "A parsing library for the UK's MPAN energy standard",
    'long_description': '[![Limejump logo](https://raw.githubusercontent.com/limejump/mpan/master/logo.png)](https://limejump.com/)\n\n\n# mpan\n\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n`mpan` is a library to help you parse the UK energy industry\'s MPAN number format.\n\n\n## How it works\n\n```python\nfrom mpan import InvalidMPANError, MPAN\n\n\nmpan = MPAN("018011002012345678385")\n\nprint(mpan.core)  # 2012345678385\nprint(mpan.identifier)  # 12345678\nprint(mpan.is_short)  # False\nprint(mpan.profile_class.description)  # "Domestic unrestricted"\nprint(mpan.distributor.is_dno)  # True\nprint(mpan.distributor.area)  # "Southern England"\n\nif mpan.is_valid:\n    print("Looks good to me!")\n\ntry:\n    mpan.check()\nexcept InvalidMPANError:\n    print("This MPAN is broken")\n```\n\nThere\'s also a shortcut if you just want validation:\n\n```python\nfrom mpan import is_valid\n\n\nif is_valid("<an MPAN string>"):\n    print("Looks good to me too!")\n```\n\n\n## Installation\n\nIt\'s on PyPI:\n\n```shell\n$ pip install mpan\n```\n\n\n## Requirements\n\nThis is a pure-python module with no external dependencies.  However, you\'ll\nneed to be running Python 3.8 or higher.\n\n\n## Development\n\n### Setting up a Local Development Environment\n\nWe\'re using [Poetry](https://python-poetry.org/), so if you want to make some\nchanges, you should install that and then just run `poetry install`.  This will\npull in all the development dependencies like `pytest`, `isort`, etc.\n\n\n### Deployment/Releases\n\nTo build, use Poetry:\n\n```shell\n$ poetry build\n```\n\nTo publish a new release, use Poetry for that too:\n\n```shell\n$ poetry publish\n```\n\n\n## Testing\n\nWhen inside your virtualenv, just run:\n\n```shell\n$ pytest\n```\n\n\n## External Documentation\n\nThis is based largely on the [Wikipedia article](https://en.wikipedia.org/wiki/Meter_Point_Administration_Number)\non the MPAN standard.  The validation code for example is cribbed right from\nthere.\n',
    'author': 'Limejump Developers',
    'author_email': 'info@limejump.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/limejump/mpan',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
