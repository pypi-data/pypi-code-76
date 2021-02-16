# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scythe', 'scythe.cli', 'scythe.clock']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'arc-cli>=2.0.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['scythe = scythe.cli:cli']}

setup_kwargs = {
    'name': 'scythe-cli',
    'version': '0.4.0',
    'description': 'A Harvest is always better with a good tool',
    'long_description': None,
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
