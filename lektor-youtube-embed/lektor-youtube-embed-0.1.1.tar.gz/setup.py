# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lektor_youtube_embed']

package_data = \
{'': ['*']}

install_requires = \
['lektor>=3.0.0,<4.0.0']

entry_points = \
{'lektor.plugins': ['youtube-embed = lektor_youtube_embed:YoutubeEmbedPlugin']}

setup_kwargs = {
    'name': 'lektor-youtube-embed',
    'version': '0.1.1',
    'description': 'Lektor template filter to convert youtube links to embeds',
    'long_description': '# lektor-youtube-embed\n\n[![Run tests](https://github.com/cigar-factory/lektor-youtube-embed/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/cigar-factory/lektor-youtube-embed/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/cigar-factory/lektor-youtube-embed/branch/main/graph/badge.svg?token=2bz0MnPazy)](https://codecov.io/gh/cigar-factory/lektor-youtube-embed)\n[![PyPI Version](https://img.shields.io/pypi/v/lektor-youtube-embed.svg)](https://pypi.org/project/lektor-youtube-embed/)\n![License](https://img.shields.io/pypi/l/lektor-youtube-embed.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Flektor-youtube-embed%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n\nLektor template filter to convert youtube links to embeds\n\n## Installation\n\n```\npip install lektor-youtube-embed\n```\n\n## Usage\n\n```\n{{ "https://www.youtube.com/watch?v=9Yk9iRDESDo" | youtube }}\n```\n\n```\n{{ "https://youtu.be/BdXDT-5jci0" | youtube(width=640, height=480, attrs={\'class\': \'video\'}) }}\n```\n',
    'author': 'chris48s',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cigar-factory/lektor-youtube-embed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
