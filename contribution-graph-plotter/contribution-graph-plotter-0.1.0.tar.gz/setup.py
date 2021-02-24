# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contribution_graph_plotter']

package_data = \
{'': ['*'], 'contribution_graph_plotter': ['templates/*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'numpy>=1.20.1,<2.0.0']

setup_kwargs = {
    'name': 'contribution-graph-plotter',
    'version': '0.1.0',
    'description': 'Plots anything into a GitHub contribution graph.',
    'long_description': None,
    'author': 'Jan-Benedikt Jagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
