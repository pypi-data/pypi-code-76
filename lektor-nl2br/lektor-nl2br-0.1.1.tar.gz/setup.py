# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lektor_nl2br']

package_data = \
{'': ['*']}

install_requires = \
['lektor>=3.0.0,<4.0.0']

entry_points = \
{'lektor.plugins': ['nl2br = lektor_nl2br:Nl2BrPlugin']}

setup_kwargs = {
    'name': 'lektor-nl2br',
    'version': '0.1.1',
    'description': 'Lektor template filter to convert linebreaks to <br> tags',
    'long_description': '# lektor-nl2br\n\n[![Run tests](https://github.com/cigar-factory/lektor-nl2br/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/cigar-factory/lektor-nl2br/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/cigar-factory/lektor-nl2br/branch/main/graph/badge.svg?token=0TVXPBzH8j)](https://codecov.io/gh/cigar-factory/lektor-nl2br)\n[![PyPI Version](https://img.shields.io/pypi/v/lektor-nl2br.svg)](https://pypi.org/project/lektor-nl2br/)\n![License](https://img.shields.io/pypi/l/lektor-nl2br.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Flektor-nl2br%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nLektor template filter to convert linebreaks to `<br>` tags\n\n## Installation\n\n```\npip install lektor-nl2br\n```\n\n## Usage\n\n```\n{{ "a line\\nanother line" | nl2br }}\n```\n',
    'author': 'chris48s',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cigar-factory/lektor-nl2br',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
