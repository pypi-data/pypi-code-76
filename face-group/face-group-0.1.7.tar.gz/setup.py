# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['face_group']

package_data = \
{'': ['*']}

install_requires = \
['face-recognition>=1.3.0,<2.0.0', 'rich>=9.11.1,<10.0.0']

entry_points = \
{'console_scripts': ['face-group = face_group.cli:group_faces']}

setup_kwargs = {
    'name': 'face-group',
    'version': '0.1.7',
    'description': 'Grouping rgb and infra people`s faces by folders using face features.',
    'long_description': '# Face group\n> Grouping rgb and infra people`s faces by folders using face features\n\n[![PyPI Version][pypi-image]][pypi-url]\n[![Build Status][build-image]][build-url]\n[![codecov][codecov-image]][codecov-url]\n\n`face-group` finds faces using dlib\n\n\n## Installation\n```\nsudo apt-get install build-essential cmake\npip install face-group\n```\n## Usage\n```\n$ face-group --help\nUsage: face-group [OPTIONS]\n\n  It groups the faces of similar people\n\nOptions:\n  -i, --input-dir PATH   Path of directory with rgb and infra images.\n  -o, --output-dir PATH  Path of output directory (default=\'out\').\n  -v, --verbose BOOLEAN  Show info or not.\n  -m, --model [hog|cnn]  Type of backend for computing features.\n  -c, --cpus INTEGER     Number of CPU cores to use in parallel (can speed up\n                         processing lots of images). -1 means "use all in\n                         system".\n\n  --help                 Show this message and exit.\n```\n\n<!-- Badges -->\n\n[pypi-image]: https://img.shields.io/pypi/v/face-group\n[pypi-url]: https://pypi.org/project/face-group/\n[build-image]: https://github.com/Irlirion/face-group/actions/workflows/main.yml/badge.svg\n[build-url]: https://github.com/Irlirion/face-group/actions/workflows/main.yml\n[codecov-image]: https://codecov.io/gh/Irlirion/face-group/branch/master/graph/badge.svg?token=DH534TCGX7\n[codecov-url]: https://codecov.io/gh/Irlirion/face-group',
    'author': 'irlirion',
    'author_email': 'irlirion@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Irlirion/face-group',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
