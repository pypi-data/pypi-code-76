# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deetly']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=3.4.0,<4.0.0',
 'isodate>=0.6.0,<0.7.0',
 'pandas>=1.0.1,<2.0.0',
 'plotly>=4.6.0,<5.0.0',
 'pyarrow>=0.16.0,<0.17.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.22.0,<3.0.0',
 'schema>=0.7.2,<0.8.0']

entry_points = \
{'console_scripts': ['deetly = deetly.console:main']}

setup_kwargs = {
    'name': 'deetly',
    'version': '0.0.12',
    'description': 'toolkit for creating data packages',
    'long_description': None,
    'author': 'Paul Bencze',
    'author_email': 'paul@idelab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
