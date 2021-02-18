# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['avault']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['avault = avault.avault:main']}

setup_kwargs = {
    'name': 'avault',
    'version': '0.1.1',
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
