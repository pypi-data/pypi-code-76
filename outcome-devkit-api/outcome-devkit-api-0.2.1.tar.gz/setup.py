# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome',
 'outcome.devkit_api',
 'outcome.devkit_api.fixtures',
 'outcome.devkit_api.pact',
 'outcome.devkit_api.pact.pactman',
 'outcome.devkit_api.pact.pactman.mock']

package_data = \
{'': ['*'], 'outcome.devkit_api.fixtures': ['keys/*']}

install_requires = \
['PyJWT[crypto]>=2.0.1,<3.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'outcome-devkit>=6.0.2,<7.0.0',
 'outcome-utils>=5.0.3,<6.0.0',
 'pactman>=2.28.0,<3.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'outcome-devkit-api',
    'version': '0.2.1',
    'description': 'Development tools for APIs.',
    'long_description': '# devkit-api-py\n![ci-badge](https://github.com/outcome-co/devkit-api-py/workflows/Release/badge.svg?branch=v0.2.1) ![version-badge](https://img.shields.io/badge/version-0.2.1-brightgreen)\n\nDescription TBD\n\n## Usage\n\n```sh\npoetry add outcome-devkit-api\n```\n\n## Development\n\nRemember to run `./bootstrap.sh` when you clone the repository.\n',
    'author': 'Outcome Engineering',
    'author_email': 'engineering@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/devkit-api-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
