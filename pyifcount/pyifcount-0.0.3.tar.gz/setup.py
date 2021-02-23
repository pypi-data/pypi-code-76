# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyifcount']

package_data = \
{'': ['*']}

install_requires = \
['prometheus-client>=0.9.0,<0.10.0', 'pyyaml>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['pyifcount = pyifcount.cli:main']}

setup_kwargs = {
    'name': 'pyifcount',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'Shoma FUKUDA',
    'author_email': 'fkshom+pypi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fkshom',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
