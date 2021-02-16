# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astro_ph']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4.0',
 'feedparser>=6.0,<7.0',
 'fire>=0.4,<0.5',
 'pyppeteer>=0.2,<0.3',
 'typing-extensions>=3.7,<4.0']

entry_points = \
{'console_scripts': ['astro-ph = astro_ph.cli:cli']}

setup_kwargs = {
    'name': 'astro-ph',
    'version': '0.2.1',
    'description': 'Translate and post arXiv articles to Slack',
    'long_description': '# astro-ph\n\n[![PyPI](https://img.shields.io/pypi/v/astro-ph.svg?label=PyPI&style=flat-square)](https://pypi.org/project/astro-ph/)\n[![Python](https://img.shields.io/pypi/pyversions/astro-ph.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/astro-ph/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/astro-ph/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/astro-ph/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nTranslate and post arXiv articles to Slack\n\n## Installation\n\n```shell\n$ pip install astro_ph\n```\n\n## Usage\n\n```shell\n$ astro-ph slack --help\n```\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/astro-ph/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
