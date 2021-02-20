# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slow_start_rewatch',
 'slow_start_rewatch.http_server',
 'slow_start_rewatch.reddit',
 'slow_start_rewatch.schedule']

package_data = \
{'': ['*'],
 'slow_start_rewatch.http_server': ['static/*',
                                    'static/css/*',
                                    'static/img/*',
                                    'templates/*']}

install_requires = \
['anyconfig>=0.9.11,<0.10.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'flask>=1.1.2,<2.0.0',
 'importlib_metadata>=1.6.0,<2.0.0',
 'praw>=7.0.0,<8.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'scalpl>=0.4.1,<0.5.0',
 'structlog>=20.1.0,<21.0.0']

entry_points = \
{'console_scripts': ['slow-start-rewatch = slow_start_rewatch.__main__:main']}

setup_kwargs = {
    'name': 'slow-start-rewatch',
    'version': '0.2.2',
    'description': 'Make cute things happen!',
    'long_description': '<p align="center">\n  <img src="https://raw.githubusercontent.com/slow-start-fans/slow-start-rewatch/master/assets/happy_shion.gif" width="384" height="360" />\n</p>\n\n\n# Slow Start Rewatch\n\n[![Build Status](https://travis-ci.com/slow-start-fans/slow-start-rewatch.svg?branch=master)](https://travis-ci.com/slow-start-fans/slow-start-rewatch)\n[![Coverage](https://coveralls.io/repos/github/slow-start-fans/slow-start-rewatch/badge.svg?branch=master)](https://coveralls.io/github/slow-start-fans/slow-start-rewatch?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/slow-start-rewatch.svg)](https://pypi.org/project/slow-start-rewatch/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n\n## Missions\n\nMake cute things happen!\n\nProvide a command-line utility for hosting an awesome Slow Start Rewatch.\n\n\n## Features\n\n- Schedule a submission of multiple Reddit posts\n- The templates for posts can be stored in Reddit\'s wiki or local files\n- Each post can include a navigation section with links to other posts which are automatically updated after the submission of new posts\n- Reddit authorization via OAuth2 using a local HTTP server with cute GIFs\n- Storing the refresh token locally to keep the authorization active\n- Submitting text posts with thumbnails\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n\n\n## Installation\n\n```bash\npip install slow-start-rewatch\n```\n\nUpgrade:\n\n```bash\npip install -U slow-start-rewatch\n```\n\n\n## Usage\n\nWhen started for the first time the location of the schedule must be set.\n\n1. Using the schedule stored in Reddit\'s wiki:\n\n```bash\nslow-start-rewatch -w /r/subreddit/wiki/wiki-path\n```\n\n2. Using the schedule stored in the local YAML file:\n\n```bash\nslow-start-rewatch -f /path/to/the/schedule.yml\n```\n\nAfter the location of the schedule is stored in the local config, the program can be launched without any parameters:\n\n```bash\nslow-start-rewatch\n```\n\n\n## License\n\n[MIT](https://github.com/slow-start-fans/slow-start-rewatch/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package).\n\nGitHub avatar art by [yunyunmaru](https://www.pixiv.net/en/users/24452545).\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/slow-start-fans/slow-start-rewatch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
