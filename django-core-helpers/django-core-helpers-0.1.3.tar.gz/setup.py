# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['core_helpers',
 'core_helpers.api',
 'core_helpers.api.filters',
 'core_helpers.api.serializers',
 'core_helpers.api.views',
 'core_helpers.db',
 'core_helpers.db.fields',
 'core_helpers.db.managers',
 'core_helpers.db.models']

package_data = \
{'': ['*']}

install_requires = \
['environs>=9.3.1,<10.0.0', 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{'docs': ['sphinx>=3.4.3,<4.0.0', 'sphinx-rtd-theme>=0.5.1,<0.6.0'],
 'test': ['requests>=2.25.1,<3.0.0',
          'requests-mock>=1.8.0,<2.0.0',
          'pytest-django>=4.1.0,<5.0.0',
          'pytest>=6.2.2,<7.0.0',
          'codecov>=2.1.11,<3.0.0',
          'coverage>=5.4,<6.0',
          'freezegun>=1.1.0,<2.0.0',
          'pytest-cov>=2.11.1,<3.0.0',
          'pytest-pythonpath>=0.7.3,<0.8.0']}

setup_kwargs = {
    'name': 'django-core-helpers',
    'version': '0.1.3',
    'description': 'Core helpers for Django and Django Rest Framework',
    'long_description': '# Django Core Helpers\n\n[![Python Version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/)\n[![codecov](https://codecov.io/gh/onufrienkovi/django-core-helpers/branch/master/graph/badge.svg)](https://codecov.io/gh/onufrienkovi/django-core-helpers)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n## Quickstart\n\nInstall\n\n```console\npip install django-core-helpers\n```\n\n## Prerequisites\n\nYou will need:\n\n- `python3.8` (see `pyproject.toml` for full version)\n- `django` with version `3.0`\n\n\n## Development\n\nWhen developing locally, we use:\n\n- [`editorconfig`](http://editorconfig.org/) plugin (**required**)\n- [`poetry`](https://github.com/python-poetry/poetry) (**required**)\n- [`pyenv`](https://github.com/pyenv/pyenv) (**required**)  \n- `pycharm 2017+` or `vscode`\n\n\n## Documentation\n\nFull documentation is available here: [`docs/`](docs).\n',
    'author': 'Vyacheslav Onufrienko',
    'author_email': 'onufrienkovi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/onufrienkovi/django-core-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
