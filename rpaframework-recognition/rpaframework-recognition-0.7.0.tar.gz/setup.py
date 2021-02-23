# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['RPA', 'RPA.recognition']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.19.3',
 'opencv-python>=4.4.0,<5.0.0',
 'pillow>=8.0.1,<9.0.0',
 'pytesseract>=0.3.6,<0.4.0',
 'rpaframework-core>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'rpaframework-recognition',
    'version': '0.7.0',
    'description': 'Core utilities used by RPA Framework',
    'long_description': 'rpaframework-recognition\n========================\n\nThis library enablous various recognition features with `RPA Framework`_\nlibraries, such as image template matching.\n\n.. _RPA Framework: https://rpaframework.org\n',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rpaframework.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
