# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3wm', 's3wm.layouts', 's3wm.tests', 's3wm_core']

package_data = \
{'': ['*']}

install_requires = \
['frozendict>=1.2,<2.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-xlib>=0.29,<0.30']

entry_points = \
{'console_scripts': ['s3wm = s3wm.main:main']}

setup_kwargs = {
    'name': 's3wm',
    'version': '0.1.2',
    'description': 'Simple Window manager.',
    'long_description': "![GitHub Workflow Status](https://img.shields.io/github/workflow/status/s3rius/s3wm/Release%20s3wm?style=for-the-badge)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/s3wm?style=for-the-badge)](https://pypi.org/project/s3wm)\n[![PyPI](https://img.shields.io/pypi/v/s3wm?style=for-the-badge)](https://pypi.org/project/s3wm)\n\n# S3WM\n\n🛠️⚙️This is a WIP project. Don't beleive in README ⚙️🛠️\n\n\nThis project is a yet another `Window manager`.\n\nMain Idea behind this project is `modularity` and\nwindow manager `configuration in Python`.\n\nYou can even `bind a python function` to some key combination.\n\n## How to Run/test\n\n```bash\n# start nested X11 session with Xephyr\nXephyr :1 +xinerama -screen 1280x720 -reset -terminate &\n# Run it with proper DISPLAY ENV\nDISPLAY=:1.0 s3wm\n# To grab or release host keys press `Ctrl` + `Shift`\n```\n",
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
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
