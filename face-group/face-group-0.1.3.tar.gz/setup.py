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
    'version': '0.1.3',
    'description': 'Simple project for grouping faces of people by encodings.',
    'long_description': '# Face group\n> Grouping rgb and infra people`s faces by folders using face features\n\n`face-group` finds faces using dlib\n\nParameters:\n- *input-dir* - path of directory with rgb and infra images\n- *output-dir* - path of output directory (default="out")\n- *verbose* - show info or not\n\n## Installation\n```\npip install face-group\n```\n## Usage\n```\n$ face-group --help\nUsage: face-group [OPTIONS]\n\n  It groups the faces of similar people\n\nOptions:\n  -i, --input-dir PATH   Path of directory with rgb and infra images.\n  -o, --output-dir PATH  Path of output directory (default=\'out\').\n  -v, --verbose BOOLEAN  Show info or not.\n  --help                 Show this message and exit.\n```\n',
    'author': 'irlirion',
    'author_email': 'irlirion@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
