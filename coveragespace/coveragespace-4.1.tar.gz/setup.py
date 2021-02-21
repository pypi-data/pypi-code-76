# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveragespace', 'coveragespace.tests']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4',
 'coverage>=4.0',
 'docopt>=0.6',
 'minilog>=2.0,<3.0',
 'requests>=2.0,<3.0']

entry_points = \
{'console_scripts': ['coveragespace = coveragespace.cli:main']}

setup_kwargs = {
    'name': 'coveragespace',
    'version': '4.1',
    'description': 'A place to track your code coverage metrics.',
    'long_description': '# Overview\n\nThe official command-line client for [The Coverage Space](http://coverage.space).\n\n[![Unix Build Status](https://img.shields.io/travis/jacebrowning/coverage-space-cli/main.svg?label=unix)](https://travis-ci.org/jacebrowning/coverage-space-cli)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/coverage-space-cli/main.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/coverage-space-cli)\n[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/coverage-space-cli/main.svg)](https://coveralls.io/r/jacebrowning/coverage-space-cli)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/coverage-space-cli.svg)](https://scrutinizer-ci.com/g/jacebrowning/coverage-space-cli/?branch=main)\n[![PyPI Version](https://img.shields.io/pypi/v/coveragespace.svg)](https://pypi.org/project/coveragespace)\n[![PyPI License](https://img.shields.io/pypi/l/coveragespace.svg)](https://pypi.org/project/coveragespace)\n\n# Setup\n\n## Requirements\n\n- Python 3.6+\n\n## Installation\n\nInstall this tool globally with [pipx](https://pipxproject.github.io/pipx/) (or pip):\n\n```text\n$ pipx install coveragespace\n```\nor add it to your [Poetry](https://python-poetry.org/docs/) project:\n\n```text\n$ poetry add coveragespace\n```\n\n# Usage\n\nTo update the value for a test coverage metric:\n\n```text\n$ coveragespace update <metric>\n```\n\nwhere `<metric>` is one of:\n\n- **unit**\n- **integration**\n- **overall**\n\nFor example, after running unit tests with code coverage enabled:\n\n```text\n$ coveragespace update unit\n```\n\nwhich will attempt to extract the current coverage data from your project directory and compare that with the last known value. The coverage value can also be manually specified:\n\n```text\n$ coveragespace update <metric> <value>\n```\n',
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://coverage.space/client/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
