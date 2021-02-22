# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py2gds']

package_data = \
{'': ['*']}

install_requires = \
['neo4j>=4.2,<5.0']

setup_kwargs = {
    'name': 'py2gds',
    'version': '0.1.2',
    'description': 'Library to build Neo4j queries with special attention on Graph Data Science library calls.',
    'long_description': None,
    'author': 'Pablo Cabezas',
    'author_email': 'pabcabsal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
