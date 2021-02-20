# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alexpackagetest']

package_data = \
{'': ['*']}

install_requires = \
['pandas']

entry_points = \
{'console_scripts': ['alexpackagetest = alexpackagetest:main']}

setup_kwargs = {
    'name': 'alexpackagetest',
    'version': '0.1.5',
    'description': 'Package for testing PyPI Poetry implementation.',
    'long_description': '# About\n\n## Description\n\nThis is a test package built by Alex. It has a couple of functions.\n\n## License\n\nMIT\n\n## Installation\n\n```\npoetry add alexpackagetest\n```\n\n## GitHub Repository\n\nhttps://github.com/Alex-Angelico/alextestpackage\n',
    'author': 'Alex Angelico',
    'author_email': 'alex.angelico@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Alex-Angelico/alextestpackage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
