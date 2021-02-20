# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['replay']

package_data = \
{'': ['*'], 'replay': ['UNKNOWN.egg-info/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pillow>=7.1.1,<8.0.0',
 'regex>=2020.4.4,<2021.0.0',
 'scandir>=1.10.0,<2.0.0',
 'tqdm>=4.55.0,<5.0.0']

entry_points = \
{'console_scripts': ['replay = replay:make_video']}

setup_kwargs = {
    'name': 'photo-replay',
    'version': '0.1.2',
    'description': 'Makes a movie from a photo library',
    'long_description': None,
    'author': 'Arvid Larsson',
    'author_email': 'arvla626@student.liu.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
